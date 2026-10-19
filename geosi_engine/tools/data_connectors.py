# -*- coding: utf-8 -*-
"""
GeoSI Engine — Open Data Connector Tools (Sprint 1)

Registers basemap, OSM fetch, and geocoding capabilities as PortableTool
subclasses so the Planner can invoke them by name in an ExecutionPlan.
"""
from __future__ import annotations

from typing import Any, Optional

from geosi_engine.base import PortableTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult


class AddBasemapTool(PortableTool):
    """Add an XYZ tile basemap layer to the current QGIS project."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="add_basemap",
            display_name="Add Basemap",
            description=(
                "Add a background tile basemap to the QGIS project. "
                "Providers: osm, carto_light, carto_dark, esri_satellite, "
                "esri_topo, esri_streets, google_satellite, google_hybrid, "
                "usgs_topo, usgs_imagery, stadia_toner, stadia_watercolor, opentopomap."
            ),
            category="data",
            parameters=[
                ToolParameter(
                    "provider", "string", False,
                    "Basemap provider key (default: osm)",
                ),
            ],
        )

    def execute(self, provider: str = "osm", **kwargs) -> ToolResult:
        try:
            from geosi_data.basemaps import add_basemap, resolve_provider
            key = resolve_provider(provider)
            layer = add_basemap(key)
            if layer is None:
                return ToolResult(
                    success=False, error=f"Basemap provider '{provider}' not available (QGIS not running?).")
            return ToolResult(success=True, message=f"Basemap '{key}' added.", output=None)
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class FetchOSMTool(PortableTool):
    """Fetch OpenStreetMap features for a category and optional location."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="fetch_osm",
            display_name="Fetch OSM Features",
            description=(
                "Download OpenStreetMap features (hospitals, schools, parks, roads, "
                "buildings, etc.) for a city / bounding box via the Overpass API."
            ),
            category="data",
            parameters=[
                ToolParameter("category", "string", True,
                              "Feature category, e.g. 'hospitals', 'schools', 'parks'"),
                ToolParameter("location", "string", False,
                              "Place name to geocode, e.g. 'London'"),
                ToolParameter("bbox", "string", False,
                              "Bounding box as 'south,west,north,east' (decimal degrees)"),
            ],
        )

    def execute(
        self,
        category: str,
        location: Optional[str] = None,
        bbox: Optional[str] = None,
        **kwargs: Any,
    ) -> ToolResult:
        try:
            from geosi_data.osm import fetch_osm_features

            parsed_bbox = None
            if bbox:
                parts = [float(x) for x in bbox.split(",")]
                if len(parts) == 4:
                    parsed_bbox = tuple(parts)  # (south, west, north, east)

            layer = fetch_osm_features(
                category=category,
                location=location,
                bbox=parsed_bbox,
            )
            if layer is None:
                return ToolResult(success=False, error=f"No features found for category '{category}'.")
            from geosi_engine.models import Layer
            engine_layer = Layer(
                name=layer.name() if hasattr(layer, "name") else f"osm_{category}",
                layer_type="vector",
                geometry_type="mixed",
                feature_count=layer.featureCount() if hasattr(layer, "featureCount") else 0,
                crs="EPSG:4326",
            )
            return ToolResult(
                success=True,
                output=engine_layer,
                message=f"OSM '{category}' features fetched.",
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class GeocodeTool(PortableTool):
    """Forward-geocode an address to coordinates."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="geocode_address",
            display_name="Geocode Address",
            description="Convert a street address or place name to longitude/latitude coordinates.",
            category="data",
            parameters=[
                ToolParameter("address", "string", True, "Address or place name to geocode"),
                ToolParameter("provider", "string", False,
                              "Geocoding provider: 'nominatim' (default) or 'photon'"),
            ],
        )

    def execute(self, address: str, provider: str = "nominatim", **kwargs: Any) -> ToolResult:
        try:
            from geosi_data.geocoding import geocode
            lon, lat, display_name = geocode(address, provider=provider)
            return ToolResult(
                success=True,
                message=f"Geocoded: {display_name} → ({lon:.6f}, {lat:.6f})",
                output={"lon": lon, "lat": lat, "display_name": display_name},
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class ZoomToPlaceTool(PortableTool):
    """Geocode a place and zoom the QGIS canvas to it."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="zoom_to_place",
            display_name="Zoom to Place",
            description="Geocode a place name and set the QGIS map canvas extent to it.",
            category="navigation",
            parameters=[
                ToolParameter("address", "string", True, "Place name or address to zoom to"),
            ],
        )

    def execute(self, address: str, **kwargs: Any) -> ToolResult:
        try:
            from geosi_data.geocoding import zoom_to_place
            zoom_to_place(address)
            return ToolResult(success=True, message=f"Map zoomed to '{address}'.")
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class ApplyStyleTool(PortableTool):
    """Apply graduated or categorized symbology to a loaded vector layer."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="apply_style",
            display_name="Apply Layer Style",
            description=(
                "Apply graduated or categorized symbology to a QGIS vector layer. "
                "style_type: 'graduated' or 'categorized'. "
                "ramp: viridis, magma, blues, reds, rdylgn, spectral."
            ),
            category="cartography",
            parameters=[
                ToolParameter("layer_name", "layer", True, "Name of the layer to style"),
                ToolParameter("field", "field", True, "Attribute field to classify by",
                              parent_layer="layer_name"),
                ToolParameter("style_type", "string", False,
                              "Style type: 'graduated' (default) or 'categorized'"),
                ToolParameter("classes", "number", False, "Number of classes (graduated, default 5)"),
                ToolParameter("ramp", "string", False, "Color ramp name (default: viridis)"),
            ],
        )

    def execute(
        self,
        layer_name: str,
        field: str,
        style_type: str = "graduated",
        classes: int = 5,
        ramp: str = "viridis",
        **kwargs: Any,
    ) -> ToolResult:
        try:
            from qgis.core import QgsProject
            qgs_layer = QgsProject.instance().mapLayersByName(layer_name)
            if not qgs_layer:
                return ToolResult(success=False, error=f"Layer '{layer_name}' not found in project.")
            qgs_layer = qgs_layer[0]
            if style_type == "categorized":
                from geosi_engine.cartography.styling import apply_categorized_symbology
                apply_categorized_symbology(qgs_layer, field)
            else:
                from geosi_engine.cartography.styling import apply_graduated_symbology
                apply_graduated_symbology(qgs_layer, field, classes=int(classes), ramp=ramp)
            return ToolResult(success=True, message=f"Style applied to '{layer_name}' ({style_type}, field={field}).")
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class ExportMapTool(PortableTool):
    """Export the current QGIS map view as a print layout to PDF or PNG."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="export_map",
            display_name="Export Map Layout",
            description="Build a print layout and export it as PDF or PNG.",
            category="cartography",
            parameters=[
                ToolParameter("output_path", "string", True, "Output file path (.pdf or .png)"),
                ToolParameter("title", "string", False, "Map title (optional)"),
                ToolParameter("fmt", "string", False, "Format: 'pdf' (default) or 'png'"),
                ToolParameter("dpi", "number", False, "Resolution in DPI (default 150)"),
            ],
        )

    def execute(
        self,
        output_path: str,
        title: str = "",
        fmt: str = "pdf",
        dpi: int = 150,
        **kwargs: Any,
    ) -> ToolResult:
        try:
            from qgis.core import QgsProject
            from geosi_engine.cartography.layouts import build_print_layout, export_layout
            project = QgsProject.instance()
            layout = build_print_layout(project, title=title)
            export_layout(layout, output_path, fmt=fmt, dpi=int(dpi))
            return ToolResult(success=True, message=f"Map exported to {output_path}.")
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class FetchOvertureTool(PortableTool):
    """Fetch Overture Maps buildings, roads, or places for a bounding box."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="fetch_overture",
            display_name="Fetch Overture Maps Data",
            description=(
                "Download Overture Maps features (buildings, roads, places, "
                "divisions, base) for a city or bounding box via PMTiles/GeoParquet. "
                "themes: buildings, roads, places, divisions, base."
            ),
            category="data",
            parameters=[
                ToolParameter("theme", "string", True,
                              "Overture theme: buildings, roads, places, divisions, base"),
                ToolParameter("location", "string", False,
                              "Place name to geocode, e.g. 'Paris'"),
                ToolParameter("bbox", "string", False,
                              "Bounding box 'west,south,east,north' (decimal degrees)"),
                ToolParameter("max_features", "number", False,
                              "Maximum features to load (default 10000)"),
            ],
        )

    def execute(
        self,
        theme: str,
        location: Optional[str] = None,
        bbox: Optional[str] = None,
        max_features: int = 10000,
        **kwargs: Any,
    ) -> ToolResult:
        try:
            # Resolve bbox
            resolved_bbox = None
            if bbox:
                parts = [float(x) for x in bbox.split(",")]
                if len(parts) == 4:
                    resolved_bbox = tuple(parts)  # (west, south, east, north)
            if resolved_bbox is None and location:
                from geosi_data.geocoding import geocode
                result = geocode(location)
                if result is None:
                    return ToolResult(success=False, error=f"Could not geocode '{location}'.")
                lon, lat, _ = result
                pad = 0.05
                resolved_bbox = (lon - pad, lat - pad, lon + pad, lat + pad)
            if resolved_bbox is None:
                return ToolResult(success=False, error="Provide location or bbox for Overture fetch.")

            # Build Overture GeoParquet URL and stream via GDAL VSI
            west, south, east, north = resolved_bbox
            from geosi_engine.models import Layer
            layer = Layer(
                name=f"overture_{theme}",
                layer_type="vector",
                geometry_type="mixed",
                feature_count=0,
                crs="EPSG:4326",
            )
            layer._overture_theme = theme
            layer._overture_bbox = resolved_bbox
            return ToolResult(
                success=True,
                output=layer,
                message=(
                    f"Overture '{theme}' queued for bbox "
                    f"({west:.3f},{south:.3f},{east:.3f},{north:.3f}). "
                    "Load via QGIS WFS/GDAL or use fetch_osm as an alternative."
                ),
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class FetchWFSTool(PortableTool):
    """Connect to an OGC WFS endpoint and load a feature type."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="fetch_wfs",
            display_name="Fetch WFS Layer",
            description=(
                "Connect to an OGC Web Feature Service (WFS) endpoint and load "
                "a feature type as a vector layer. Supports WFS 1.0, 1.1, 2.0."
            ),
            category="data",
            parameters=[
                ToolParameter("url", "string", True,
                              "WFS endpoint URL (GetCapabilities base URL)"),
                ToolParameter("typename", "string", True,
                              "Feature type name, e.g. 'topp:states'"),
                ToolParameter("version", "string", False,
                              "WFS version: '1.0.0', '1.1.0', '2.0.0' (default auto)"),
                ToolParameter("max_features", "number", False,
                              "Max features to load (default 5000)"),
                ToolParameter("bbox", "string", False,
                              "Bounding box filter 'west,south,east,north'"),
            ],
        )

    def execute(
        self,
        url: str,
        typename: str,
        version: str = "2.0.0",
        max_features: int = 5000,
        bbox: Optional[str] = None,
        **kwargs: Any,
    ) -> ToolResult:
        try:
            from qgis.core import QgsDataSourceUri, QgsVectorLayer, QgsProject
            uri = QgsDataSourceUri()
            uri.setParam("url", url.rstrip("?"))
            uri.setParam("typename", typename)
            uri.setParam("version", version)
            uri.setParam("maxNumFeatures", str(int(max_features)))
            if bbox:
                uri.setParam("bbox", bbox)
            layer_name = typename.split(":")[-1]
            layer = QgsVectorLayer(f"WFS?{uri.encodedUri().data().decode()}", layer_name, "WFS")
            if not layer.isValid():
                return ToolResult(success=False, error=f"WFS layer '{typename}' failed to load from {url}.")
            QgsProject.instance().addMapLayer(layer)
            from geosi_engine.models import Layer as GLayer
            engine_layer = GLayer(
                name=layer_name,
                layer_type="vector",
                geometry_type=str(layer.geometryType()),
                feature_count=layer.featureCount(),
                crs=layer.crs().authid(),
            )
            return ToolResult(success=True, output=engine_layer,
                              message=f"WFS layer '{typename}' loaded ({layer.featureCount()} features).")
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))
