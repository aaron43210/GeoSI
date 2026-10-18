# -*- coding: utf-8 -*-
"""
GeoSI Engine — Portable Tools (Non-QGIS)

These tools work in any environment using GeoPandas, Rasterio, etc.
They handle data loading, saving, and basic table manipulation.
"""

import os
from typing import Dict, Any, Optional

from geosi_engine.base import PortableTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


class LoadLayerTool(PortableTool):
    """Load spatial data from disk."""
    
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="load_spatial_data",
            display_name="Load Layer",
            description="Load a vector or raster file into the workspace",
            category="data",
            parameters=[
                ToolParameter("filepath", "string", True, "Path to the file"),
                ToolParameter("layer_name", "string", False, "Optional name for the layer")
            ]
        )

    def execute(self, filepath: str, layer_name: Optional[str] = None, **kwargs) -> ToolResult:
        if not os.path.exists(filepath):
            return ToolResult(success=False, error=f"File not found: {filepath}")
        
        name = layer_name or os.path.basename(filepath).split('.')[0]
        ext = os.path.splitext(filepath)[1].lower()
        
        try:
            # Vector loading
            if ext in ['.shp', '.geojson', '.gpkg', '.kml']:
                import geopandas as gdf
                # Prefer the pyogrio engine when available: ~3-5x faster
                # reads for large vector files. Silently fall back if
                # pyogrio is not installed.
                try:
                    data = gdf.read_file(filepath, engine="pyogrio")
                except Exception:
                    data = gdf.read_file(filepath)
                # Warm the STRtree spatial index once so downstream
                # overlays and spatial joins reuse it.
                try:
                    _ = data.sindex
                except Exception:
                    pass
                layer = Layer(
                    name=name,
                    layer_type="vector",
                    geometry_type=str(data.geometry.type.iloc[0]) if not data.empty else "unknown",
                    feature_count=len(data),
                    crs=str(data.crs) if data.crs else "unknown",
                    filepath=filepath,
                    features=data
                )
                return ToolResult(success=True, output=layer, message=f"Loaded vector layer: {name}")
            
            # Raster loading
            elif ext in ['.tif', '.tiff', '.asc', '.img']:
                import rasterio
                with rasterio.open(filepath) as src:
                    layer = Layer(
                        name=name,
                        layer_type="raster",
                        geometry_type="raster",
                        feature_count=src.count,
                        crs=str(src.crs) if src.crs else "unknown",
                        filepath=filepath,
                        features=None # We don't load full raster into memory here
                    )
                return ToolResult(success=True, output=layer, message=f"Loaded raster layer: {name}")
            
            return ToolResult(success=False, error=f"Unsupported format: {ext}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SaveLayerTool(PortableTool):
    """Save a layer to disk."""
    
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="save_layer",
            display_name="Save Layer",
            description="Save a workspace layer to a file",
            category="data",
            parameters=[
                ToolParameter("layer_name", "layer", True, "Layer to save"),
                ToolParameter("filepath", "string", True, "Destination path"),
                ToolParameter("driver", "string", False, "Format driver (GeoJSON, ESRI Shapefile, etc.)")
            ]
        )

    def execute(self, layer_name: Any, filepath: str, driver: Optional[str] = None, **kwargs) -> ToolResult:
        # Resolve layer if string passed
        layer = layer_name
        if isinstance(layer, str):
            return ToolResult(success=False, error="Layer must be a Layer object")
            
        try:
            if layer.layer_type == "vector" and layer.features is not None:
                layer.features.to_file(filepath, driver=driver)
                return ToolResult(success=True, message=f"Saved layer to {filepath}")
            return ToolResult(success=False, error="Cannot save this layer type")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class CleanLayerTool(PortableTool):
    """Clean and repair vector geometries."""
    
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="clean_layer",
            display_name="Clean Layer",
            description="Fix invalid geometries and remove empty/duplicate features",
            category="vector",
            parameters=[
                ToolParameter("layer_name", "layer", True, "Input layer"),
                ToolParameter("fix_geometries", "boolean", False, "Run fix_geometries?", "True"),
                ToolParameter("drop_empty", "boolean", False, "Drop empty geometries?", "True")
            ]
        )

    def execute(self, layer_name: Any, fix_geometries: bool = True, drop_empty: bool = True, **kwargs) -> ToolResult:
        layer = layer_name
        if layer.layer_type != "vector":
            return ToolResult(success=False, error="Only vector layers can be cleaned")
            
        try:
            gdf = layer.features.copy()
            # Single pass over the geometry column: compute validity /
            # emptiness once, then repair only the rows that need it.
            # Calling make_valid() unconditionally over millions of
            # already-valid features is a dominant cost in clean flows.
            valid_mask = gdf.geometry.is_valid
            empty_mask = gdf.geometry.is_empty
            if fix_geometries and (~valid_mask).any():
                invalid_idx = gdf.index[~valid_mask]
                gdf.loc[invalid_idx, "geometry"] = (
                    gdf.loc[invalid_idx, "geometry"].make_valid()
                )
                # Refresh the mask for the repaired rows.
                valid_mask = gdf.geometry.is_valid
            if drop_empty:
                gdf = gdf[~empty_mask & valid_mask]
            
            new_layer = Layer(
                name=f"{layer.name}_cleaned",
                layer_type="vector",
                geometry_type=layer.geometry_type,
                feature_count=len(gdf),
                crs=layer.crs,
                filepath=layer.filepath,
                features=gdf
            )
            return ToolResult(success=True, output=new_layer, message="Layer cleaned successfully")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class CalculateFieldTool(PortableTool):
    """Run an expression to create/update a field."""
    
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="calculate_field",
            display_name="Calculate Field",
            description="Create or update an attribute field using an expression",
            category="vector",
            parameters=[
                ToolParameter("layer_name", "layer", True, "Input layer"),
                ToolParameter("field_name", "string", True, "Target field name"),
                ToolParameter("expression", "string", True, "Python-style expression")
            ]
        )

    def execute(self, layer_name: Any, field_name: str, expression: str, **kwargs) -> ToolResult:
        layer = layer_name
        try:
            gdf = layer.features.copy()
            # Simple eval (caution: in production use a safer parser)
            gdf[field_name] = gdf.eval(expression)
            
            new_layer = Layer(
                name=f"{layer.name}_updated",
                layer_type="vector",
                geometry_type=layer.geometry_type,
                feature_count=len(gdf),
                crs=layer.crs,
                filepath=layer.filepath,
                features=gdf
            )
            return ToolResult(success=True, output=new_layer, message=f"Field {field_name} calculated")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# CountFeaturesTool  —  handles "Count all schools from Schools.shp" queries
# ─────────────────────────────────────────────────────────────────────────────

class CountFeaturesTool(PortableTool):
    """Count the number of features / rows in a vector layer."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="count_features",
            display_name="Count Features",
            description=(
                "Count the total number of features (rows) in a vector layer. "
                "Works with any loaded layer or a .shp / .geojson / .gpkg file path."
            ),
            category="statistics",
            parameters=[
                ToolParameter("layer_name", "layer", True,
                              "Input layer object or file path string"),
            ],
            outputs=["count"],
            tags=["count", "total", "features", "rows", "statistics", "how many"],
        )

    def execute(self, layer_name: Any, **kwargs) -> ToolResult:
        try:
            # ── Branch A: Layer object already in state (QGIS plugin path) ────
            if not isinstance(layer_name, str):
                layer = layer_name
                count = 0
                # QgsVectorLayer
                if hasattr(layer, "features") and layer.features is not None:
                    features = layer.features
                    if hasattr(features, "featureCount"):
                        count = features.featureCount()
                    elif hasattr(features, "__len__"):
                        count = len(features)
                    else:
                        count = getattr(layer, "feature_count", 0)
                else:
                    count = getattr(layer, "feature_count", 0)
                name = getattr(layer, "name", "layer")
                return ToolResult(
                    success=True,
                    output={"count": count, "layer": name},
                    message=f"Layer '{name}' has {count} feature(s).",
                )

            # ── Branch B: File path string ────────────────────────────────────
            if not os.path.exists(layer_name):
                return ToolResult(
                    success=False,
                    error=f"File not found: '{layer_name}'",
                )

            # Try geopandas first
            try:
                import geopandas as gpd
                try:
                    gdf = gpd.read_file(layer_name, engine="pyogrio")
                except Exception:
                    gdf = gpd.read_file(layer_name)
                count = len(gdf)
                name = os.path.splitext(os.path.basename(layer_name))[0]
                return ToolResult(
                    success=True,
                    output={"count": count, "layer": name},
                    message=f"Layer '{name}' has {count} feature(s).",
                )
            except ImportError:
                pass

            # Try fiona
            try:
                import fiona
                with fiona.open(layer_name) as src:
                    count = len(src)
                name = os.path.splitext(os.path.basename(layer_name))[0]
                return ToolResult(
                    success=True,
                    output={"count": count, "layer": name},
                    message=f"Layer '{name}' has {count} feature(s).",
                )
            except ImportError:
                pass

            # Try osgeo.ogr (always present in QGIS / GDAL installations)
            try:
                from osgeo import ogr
                ds = ogr.Open(layer_name)
                if ds is None:
                    return ToolResult(success=False, error=f"OGR cannot open: {layer_name}")
                lyr = ds.GetLayer(0)
                count = lyr.GetFeatureCount()
                name = os.path.splitext(os.path.basename(layer_name))[0]
                return ToolResult(
                    success=True,
                    output={"count": count, "layer": name},
                    message=f"Layer '{name}' has {count} feature(s).",
                )
            except ImportError:
                pass

            return ToolResult(
                success=False,
                error=(
                    "Cannot count features: no geospatial library available. "
                    "Install geopandas, fiona, or GDAL."
                ),
            )

        except Exception as e:
            return ToolResult(success=False, error=str(e))


# ─────────────────────────────────────────────────────────────────────────────
# ValidateGeometryTool  —  quick geometry quality check
# ─────────────────────────────────────────────────────────────────────────────

class ValidateGeometryTool(PortableTool):
    """Run a geometry validity check on a vector layer."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="validate_geometry",
            display_name="Validate Geometry",
            description="Check a vector layer for invalid, empty, or null geometries.",
            category="validation",
            parameters=[
                ToolParameter("layer_name", "layer", True,
                              "Input layer to validate"),
            ],
            outputs=["report"],
            tags=["validate", "geometry", "quality", "check", "fix"],
        )

    def execute(self, layer_name: Any, **kwargs) -> ToolResult:
        layer = layer_name
        try:
            if layer.layer_type != "vector":
                return ToolResult(success=False, error="Only vector layers can be validated.")
            gdf = layer.features
            if gdf is None or not hasattr(gdf, "geometry"):
                return ToolResult(success=False, error="Layer has no geometry column.")

            null_count    = int(gdf.geometry.isna().sum())
            empty_count   = int(gdf.geometry.is_empty.sum())
            invalid_count = int((~gdf.geometry.is_valid).sum())
            total         = len(gdf)
            valid_count   = total - null_count - empty_count - invalid_count

            report = {
                "total": total,
                "valid": valid_count,
                "invalid": invalid_count,
                "empty": empty_count,
                "null": null_count,
            }
            ok = (invalid_count == 0 and null_count == 0)
            msg = (
                f"✅ '{layer.name}': {total} features — all geometries are valid."
                if ok
                else (
                    f"⚠️ '{layer.name}': {total} total — "
                    f"{invalid_count} invalid, {empty_count} empty, {null_count} null."
                )
            )
            return ToolResult(success=ok, output=report, message=msg)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
