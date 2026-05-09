# -*- coding: utf-8 -*-
"""
GeoSI Tool Service

Bridges the API layer to the unified geosi_engine. State mutations
propagate via listeners (no O(L) full-sync loops), vector serialization
is cached per (layer, version, bbox, tolerance, limit), and telemetry
is written to the persistence layer for later bottleneck analysis.
"""

import json
import os
from typing import Any, Dict, List, Optional

from geosi_server.app.core.state import LayerRecord, WorkspaceState
from geosi_server.app.schemas import (
    LayerResponse,
    OperationResponse,
    QueryResponse,
    ToolParameterResponse,
    ToolSpecResponse,
)
from geosi_server.app.services.persistence import Timer, persistence
from geosi_server.app.services.osm_fetcher import can_fetch, fetch_layer

from geosi_engine import GeoSI
from geosi_engine.models import Layer, ToolStep, ExecutionPlan, ExecutionResult


class ToolService:
    """Handle layer loading and GIS operations for the API."""

    def __init__(self):
        # Manage the local workspace (layers + records)
        self.state = WorkspaceState()
        # The GeoSI engine with the registry and executor
        self._engine = GeoSI()
        # In-process persistence for caching and telemetry
        self.persistence = persistence
        # Register a listener so every layer mutation is propagated to the engine
        # Event-driven bridge eliminates the per-call full-sync loop
        self.state.add_listener(self._on_workspace_event)

    # ------------------------------------------------------------------
    # STATE BRIDGE
    # ------------------------------------------------------------------

    def _on_workspace_event(self, event: str, name: str, layer: Any) -> None:
        # Sync layer add/replace to engine and persistence
        if event in ("added", "replaced"):
            # If the layer object is a Layer, sync it to the engine's state
            if isinstance(layer, Layer):
                self._engine.state.add_layer(layer)
            # Store or update layer metadata in persistence
            record = self.state.get_record(name)
            if record is not None:
                self.persistence.upsert_layer({
                    "layer_name": record.name,
                    "layer_type": record.layer_type,
                    "geometry_type": record.geometry_type,
                    "feature_count": record.feature_count,
                    "crs": record.crs,
                    "filepath": record.filepath,
                    "version": record.version,
                })
            # On replace, invalidate all downstream caches for this layer
            if event == "replaced":
                self.persistence.invalidate_layer(name)
        # Sync layer removal to engine and persistence
        elif event == "removed":
            self._engine.state.remove_layer(name)
            self.persistence.delete_layer(name)

    # ------------------------------------------------------------------
    # TOOL DISCOVERY
    # ------------------------------------------------------------------

    def list_tools(self) -> List[ToolSpecResponse]:
        # Return all discovered tools from the registry with their metadata
        tools = []
        for spec in self._engine.registry.list_tools():
            # Convert each tool spec to API response format
            tools.append(
                ToolSpecResponse(
                    name=spec.name,
                    description=spec.description,
                    category=spec.category,
                    # Convert parameters to response format
                    parameters=[
                        ToolParameterResponse(
                            name=p.name,
                            type_=p.param_type,
                            required=p.required,
                            description=p.description,
                            example=str(p.example) if p.example is not None else "",
                        )
                        for p in spec.parameters
                    ],
                )
            )
        return tools

    # ------------------------------------------------------------------
    # WORKSPACE HELPERS
    # ------------------------------------------------------------------

    def list_layers(self) -> List[LayerResponse]:
        return [
            LayerResponse(
                name=r.name,
                geometry_type=r.geometry_type,
                feature_count=r.feature_count,
                crs=r.crs,
                filepath=r.filepath,
                layer_type=r.layer_type,
            )
            for r in self.state.list_records()
        ]

    def get_layer_geojson(
        self,
        layer_name: str,
        bbox: Optional[List[float]] = None,
        limit: Optional[int] = None,
        simplify_tolerance: Optional[float] = None,
    ) -> Optional[dict]:
        """
        Return a GeoJSON FeatureCollection for a vector layer with
        optional viewport clipping, simplification, and feature cap.

        Caching is keyed by (layer_name, version, bbox, tolerance, limit)
        so pan/zoom interactions skip repeat serialization cost.
        """
        # Get layer metadata and the layer itself
        record = self.state.get_record(layer_name)
        layer = self.state.get_layer(layer_name)
        # Only process vector layers
        if not layer or not record or record.layer_type != "vector":
            return None

        # Extract GeoDataFrame or feature collection
        data = getattr(layer, "features", None)
        if data is None or not hasattr(data, "to_json"):
            return None

        # Normalize cache keys: bbox as string, tolerance and limit as numbers
        bbox_key = ",".join(f"{c:.6f}" for c in bbox) if bbox else ""
        tol = float(simplify_tolerance or 0.0)
        cap = int(limit or 0)

        # Try to fetch from cache; version change invalidates all entries
        cached = self.persistence.get_geojson(
            layer_name, record.version, bbox_key, tol, cap
        )
        if cached is not None:
            return cached

        # Serialize and transform (with telemetry)
        try:
            feature_count = int(len(data)) if hasattr(data, "__len__") else 0
            # Time the entire serialization/transformation pipeline
            with Timer(
                self.persistence,
                "get_layer_geojson",
                feature_count=feature_count,
                meta={"bbox": bbox_key, "tolerance": tol, "limit": cap},
            ):
                gdf = data
                # Clip to viewport bbox if provided
                if bbox and len(bbox) == 4:
                    minx, miny, maxx, maxy = bbox
                    gdf = gdf.cx[minx:maxx, miny:maxy]
                # Cap feature count
                if cap > 0 and len(gdf) > cap:
                    gdf = gdf.head(cap)
                # Simplify geometries at the specified tolerance
                if tol > 0:
                    gdf = gdf.assign(
                        geometry=gdf.geometry.simplify(
                            tol, preserve_topology=True
                        )
                    )
                # Reproject to EPSG:4326 (standard web mapping CRS)
                if gdf.crs is not None and str(gdf.crs) != "EPSG:4326":
                    gdf = gdf.to_crs("EPSG:4326")
                # Convert to GeoJSON FeatureCollection
                payload = json.loads(gdf.to_json())

            # Cache the result for future pan/zoom requests
            self.persistence.put_geojson(
                layer_name, record.version, payload,
                crs="EPSG:4326", bbox=bbox_key,
                simplify_tolerance=tol, limit_n=cap,
            )
            return payload
        except Exception as exc:
            print(f"Error converting layer to GeoJSON: {exc}")
            return None

    def _get_layer(self, layer_name: str) -> Optional[Layer]:
        return self.state.get_layer(layer_name)

    def _missing_layer(self, layer_name: str) -> OperationResponse:
        return self._error_response("Unknown layer: " + layer_name)

    # ------------------------------------------------------------------
    # ENGINE DELEGATION
    # ------------------------------------------------------------------

    def _run_tool(
        self,
        tool_name: str,
        params: Dict[str, Any],
        output_name: Optional[str] = None,
    ) -> OperationResponse:
        try:
            # Wrap the tool call in a single-step ExecutionPlan
            step_id = "api_step_1"
            out_name = output_name or f"{tool_name}_output"
            step = ToolStep(
                step_id=step_id,
                tool_name=tool_name,
                parameters=params,
                output_name=out_name,
                description=f"API call to {tool_name}",
            )
            # Create a plan with just this one step
            plan = ExecutionPlan(
                steps=[step],
                reasoning=f"Single tool execution: {tool_name}",
            )

            # Execute the plan and record timing
            with Timer(self.persistence, f"tool.{tool_name}"):
                result: ExecutionResult = self._engine.executor.run(plan)

            # Check for execution errors
            if not result.success:
                return self._error_response(result.error or "Tool execution failed")

            # Extract the output layer if present
            output_layer = result.results.get(out_name)
            if output_layer and isinstance(output_layer, Layer):
                # Store the new layer in workspace
                self._store_layer(output_layer)
                return OperationResponse(
                    success=True,
                    message=result.answer,
                    layer=self._to_layer_response(output_layer),
                )

            # Return non-layer results (e.g., statistics, reports)
            return OperationResponse(
                success=True,
                message=result.answer,
                data={"summary": result.reasoning},
            )

        except Exception as e:
            import traceback
            traceback.print_exc()
            return self._error_response(str(e))

    # ------------------------------------------------------------------
    # REFACTORED ENDPOINTS
    # ------------------------------------------------------------------

    def load_layer(self, filepath: str, layer_name: Optional[str] = None) -> OperationResponse:
        path = self._normalize_filepath(filepath)
        return self._run_tool(
            "load_spatial_data",
            {"filepath": path, "layer_name": layer_name},
            output_name=layer_name,
        )

    def digitize_layer(self, name: str, geometry_type: str, crs: str, features_geojson: Dict[str, Any]) -> OperationResponse:
        return self._error_response("Digitize not yet fully implemented in portable engine")

    def save_workspace_layer(self, layer_name: str, filepath: str, driver: Optional[str]) -> OperationResponse:
        path = self._normalize_filepath(filepath)
        return self._run_tool(
            "save_layer",
            {"layer_name": layer_name, "filepath": path, "driver": driver},
        )

    def clean_workspace_layer(self, layer_name: str, fix_geometries: bool, drop_empty: bool, drop_duplicates: bool) -> OperationResponse:
        return self._run_tool(
            "clean_layer",
            {
                "layer_name": layer_name,
                "fix_geometries": fix_geometries,
                "drop_empty": drop_empty,
            },
            output_name=f"{layer_name}_cleaned",
        )

    def calculate_workspace_field(self, layer_name: str, field_name: str, expression: str) -> OperationResponse:
        return self._run_tool(
            "calculate_field",
            {
                "layer_name": layer_name,
                "field_name": field_name,
                "expression": expression,
            },
            output_name=f"{layer_name}_calculated",
        )

    def select_layer_features(self, layer_name: str, where: Optional[str], spatial_layer_name: Optional[str], predicate: str) -> OperationResponse:
        if spatial_layer_name:
            return self._run_tool(
                "select_by_location",
                {
                    "INPUT": layer_name,
                    "INTERSECT": spatial_layer_name,
                    "PREDICATE": predicate,
                },
                output_name=f"{layer_name}_selected",
            )
        return self._run_tool(
            "extract_by_attribute",
            {"INPUT": layer_name, "FIELD": "id", "VALUE": "1"},
            output_name=f"{layer_name}_selected",
        )

    def buffer_layer(self, layer_name: str, distance: float, dissolve_result: bool) -> OperationResponse:
        return self._run_tool(
            "buffer",
            {"INPUT": layer_name, "DISTANCE": distance, "DISSOLVE": dissolve_result},
            output_name=f"{layer_name}_buffer",
        )

    def overlay_layers(self, layer_a: str, layer_b: str, operation: str) -> OperationResponse:
        tool_map = {
            "intersect": "intersect",
            "union": "union_layer",
            "difference": "difference",
            "symdiff": "symmetric_difference",
            "clip": "clip",
        }
        tool_name = tool_map.get(operation.lower(), "intersect")
        return self._run_tool(
            tool_name,
            {"INPUT": layer_a, "OVERLAY": layer_b},
            output_name=f"{layer_a}_{operation}",
        )

    def intersect_layers(self, layer_a: str, layer_b: str) -> OperationResponse:
        return self.overlay_layers(layer_a, layer_b, "intersect")

    def spatial_join_layers(self, target_layer: str, join_layer: str, how: str, predicate: str) -> OperationResponse:
        return self._run_tool(
            "spatial_join",
            {"INPUT": target_layer, "JOIN": join_layer, "PREDICATE": predicate},
            output_name=f"{target_layer}_joined",
        )

    def dissolve_layer(self, layer_name: str, by_attribute: Optional[str]) -> OperationResponse:
        return self._run_tool(
            "dissolve",
            {"INPUT": layer_name, "FIELD": by_attribute},
            output_name=f"{layer_name}_dissolved",
        )

    def proximity_layers(self, source_layer: str, target_layer: str, max_distance: Optional[float]) -> OperationResponse:
        return self._run_tool(
            "nearest_join",
            {
                "INPUT": source_layer,
                "INPUT_2": target_layer,
                "MAX_DISTANCE": max_distance,
            },
            output_name=f"{source_layer}_proximity",
        )

    def run_network_analysis(self, network_layer: str, start: List[float], end: List[float], weight_field: Optional[str]) -> OperationResponse:
        return self._run_tool(
            "shortest_path",
            {
                "INPUT": network_layer,
                "START_POINT": f"{start[0]},{start[1]}",
                "END_POINT": f"{end[0]},{end[1]}",
            },
            output_name="shortest_path_result",
        )

    def run_surface_analysis(self, raster_layer: str, operation: str, z_factor: float, output_filepath: Optional[str]) -> OperationResponse:
        tool_name = operation.lower()
        return self._run_tool(
            tool_name,
            {"INPUT": raster_layer, "Z_FACTOR": z_factor},
            output_name=f"{raster_layer}_{operation}",
        )

    def run_interpolation(self, point_layer: str, value_field: str, cell_size: float, power: float, output_filepath: Optional[str]) -> OperationResponse:
        return self._run_tool(
            "contour",
            {"INPUT": point_layer, "INTERVAL": cell_size},
            output_name="interpolation_result",
        )

    def run_raster_algebra(self, expression: str, raster_layer_names: Dict[str, str], output_name: str, output_filepath: Optional[str]) -> OperationResponse:
        return self._run_tool(
            "raster_calc",
            {
                "EXPRESSION": expression,
                "LAYERS": list(raster_layer_names.values())[0],
            },
            output_name=output_name,
        )

    def export_workspace_map(self, layer_names: List[str], output_filepath: str, title: str) -> OperationResponse:
        return self._run_tool(
            "export_geojson",
            {"INPUT": layer_names[0], "OUTPUT": output_filepath},
        )

    def geocode(self, address: str, provider: str) -> OperationResponse:
        return self._error_response("Geocoding currently works via LLM query or QGIS plugin")

    def reverse_geocode_location(self, longitude: float, latitude: float, provider: str) -> OperationResponse:
        return self._error_response("Reverse geocoding currently works via LLM query or QGIS plugin")

    def _ensure_layers_for_query(self, query_text: str) -> List[str]:
        """
        Prefer layers already loaded in the workspace. Only when a
        referenced layer is missing AND its name is recognised as an
        OSM feature do we auto-fetch from OpenStreetMap.
        """
        loaded = {r.name.lower() for r in self.state.list_records()}
        fetched: List[str] = []
        for token in query_text.lower().replace(",", " ").split():
            clean = token.strip(".!?;:'\"()[]")
            if clean and clean not in loaded and can_fetch(clean):
                layer = fetch_layer(clean)
                if layer is not None:
                    self._store_layer(layer)
                    loaded.add(clean)
                    fetched.append(clean)
        return fetched

    def run_query(self, query_text: str) -> QueryResponse:
        try:
            self._ensure_layers_for_query(query_text)
            with Timer(self.persistence, "query"):
                result = self._engine.query(query_text)
            return QueryResponse(
                success=result.get("success", False),
                answer=result.get("answer", ""),
                reasoning=result.get("reasoning", ""),
                error=result.get("error"),
            )
        except Exception as exc:
            return QueryResponse(success=False, error=str(exc))

    def analyze(self, query_text: str) -> Dict[str, Any]:
        try:
            self._ensure_layers_for_query(query_text)
            with Timer(self.persistence, "analyze"):
                request = self._engine.agent.parse(query_text, self._engine.state)
                plan = self._engine.agent.plan(request)
                plan_report = self._engine.agent.validate_plan(
                    plan, self._engine.state
                )

                if not plan_report.ok:
                    return {
                        "success": False,
                        "answer": "",
                        "reasoning": plan.reasoning,
                        "error": "; ".join(i.message for i in plan_report.errors()),
                        "intent": request.intent.value,
                        "entities": request.entities,
                        "parameters": request.parameters,
                        "steps": [s.__dict__ for s in plan.steps],
                        "logs": [],
                    }

                result = self._engine.executor.run(plan)
            return {
                "success": result.success,
                "answer": result.answer,
                "reasoning": result.reasoning,
                "error": result.error,
                "intent": request.intent.value,
                "entities": request.entities,
                "parameters": request.parameters,
                "steps": [s.__dict__ for s in plan.steps],
                "logs": [log.__dict__ for log in result.logs],
            }
        except Exception as exc:
            return {
                "success": False, "answer": "", "reasoning": "",
                "error": str(exc), "intent": None,
                "entities": {}, "parameters": {},
                "steps": [], "logs": [],
            }

    def validate_workspace(
        self,
        layer_name: Optional[str] = None,
        layer_a: Optional[str] = None,
        layer_b: Optional[str] = None,
        required_fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        from geosi_engine.validation import ValidationEngine, ValidationReport, ValidationIssue

        engine = ValidationEngine()
        report = ValidationReport()

        if layer_name:
            layer = self._engine.state.get_layer(layer_name)
            record = self.state.get_record(layer_name)
            if layer is None or record is None:
                report.add(ValidationIssue(
                    "error", "unknown_layer",
                    f"Layer '{layer_name}' is not loaded.", layer_name,
                ))
            else:
                cached = self.persistence.get_validation(
                    layer_name, record.version
                )
                if cached is not None and not required_fields:
                    return cached.get("report", {})

                with Timer(
                    self.persistence,
                    "validate.geometry+crs",
                    feature_count=record.feature_count,
                ):
                    report.issues.extend(engine.validate_geometry(layer).issues)
                    report.issues.extend(engine.validate_crs(layer).issues)
                    if required_fields:
                        report.issues.extend(engine.validate_attributes(
                            layer, required_fields).issues)
                report.stats[layer_name] = {
                    "crs": layer.crs,
                    "feature_count": layer.feature_count,
                }
                report.ok = not report.errors()
                if not required_fields:
                    self.persistence.put_validation(
                        layer_name, record.version, report.to_dict()
                    )

        if layer_a and layer_b:
            a = self._engine.state.get_layer(layer_a)
            b = self._engine.state.get_layer(layer_b)
            if a and b:
                report.issues.extend(engine.check_crs_compatibility(a, b).issues)

        report.ok = not report.errors()
        return report.to_dict()

    # ------------------------------------------------------------------
    # RESPONSE HELPERS
    # ------------------------------------------------------------------

    def _normalize_filepath(self, filepath: Optional[str]) -> str:
        clean_path = (filepath or "").strip()
        expanded_path = os.path.expanduser(clean_path)
        return os.path.abspath(expanded_path)

    def _store_layer(self, layer: Layer):
        existing = self.state.get_record(layer.name)
        next_version = (existing.version + 1) if existing else 1
        record = LayerRecord(
            name=layer.name,
            geometry_type=layer.geometry_type,
            feature_count=layer.feature_count,
            crs=layer.crs,
            filepath=layer.filepath,
            layer_type=layer.layer_type,
            version=next_version,
        )
        self.state.add_layer(layer.name, layer, record)

    def _to_layer_response(self, layer: Layer) -> LayerResponse:
        return LayerResponse(
            name=layer.name,
            geometry_type=layer.geometry_type,
            feature_count=layer.feature_count,
            crs=layer.crs,
            filepath=layer.filepath,
            layer_type=layer.layer_type,
        )

    def _error_response(self, error: str, message: str = "") -> OperationResponse:
        return OperationResponse(success=False, message=message, error=error)


tool_service = ToolService()
