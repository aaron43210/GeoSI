# -*- coding: utf-8 -*-
"""
GeoSI Engine — Portable Backend

This backend intercepts QGIS processing algorithm calls (e.g. 'native:buffer')
and executes them using pure Python libraries (GeoPandas, Shapely) when the 
engine is running outside of QGIS (like in the geosi_server API).
"""

import logging
from typing import Dict, Any, Optional

import geopandas as gpd

from geosi_engine.models import ToolResult, Layer

logger = logging.getLogger("geosi_engine.backends.portable")


def _get_gdf(layer_obj: Any) -> Optional[gpd.GeoDataFrame]:
    """Extract a GeoDataFrame from a Layer object or return as-is if already a GDF."""
    if isinstance(layer_obj, Layer) and layer_obj.features is not None:
        return layer_obj.features
    if isinstance(layer_obj, gpd.GeoDataFrame):
        return layer_obj
    return None


def _to_layer(gdf: gpd.GeoDataFrame, name: str, source_layer: Layer) -> Layer:
    """Wrap a GeoDataFrame result into a GeoSI Layer object."""
    return Layer(
        name=name,
        layer_type="vector",
        geometry_type=str(gdf.geometry.type.iloc[0]) if not gdf.empty else "unknown",
        feature_count=len(gdf),
        crs=str(gdf.crs) if gdf.crs else "unknown",
        filepath=source_layer.filepath if hasattr(source_layer, 'filepath') else None,
        features=gdf
    )


def run_buffer(params: Dict[str, Any]) -> ToolResult:
    input_layer = params.get("INPUT")
    distance = float(params.get("DISTANCE", 0))
    dissolve = str(params.get("DISSOLVE", "False")).lower() in ["true", "1", "yes"]
    
    gdf = _get_gdf(input_layer)
    if gdf is None:
        return ToolResult(success=False, error="INPUT must be a valid vector layer")
        
    try:
        # Reproject to a projected CRS if in geographic (degrees) to get accurate distances
        # If distance is small (like 0.01), they might mean degrees. If > 1, they likely mean meters.
        # But for simplicity in a portable backend, we'll assume the user provided units matching the CRS.
        buffered_gdf = gdf.copy()
        buffered_gdf["geometry"] = buffered_gdf.geometry.buffer(distance)
        
        if dissolve:
            # Dissolve all features into a single geometry
            buffered_gdf = buffered_gdf.dissolve()
            
        out_name = f"{getattr(input_layer, 'name', 'layer')}_buffer"
        result_layer = _to_layer(buffered_gdf, out_name, input_layer)
        
        return ToolResult(
            success=True, 
            output=result_layer, 
            message=f"Successfully buffered layer by {distance}"
        )
    except Exception as e:
        return ToolResult(success=False, error=str(e))


def run_overlay(params: Dict[str, Any], how: str) -> ToolResult:
    input_layer = params.get("INPUT")
    overlay_layer = params.get("OVERLAY")
    
    gdf1 = _get_gdf(input_layer)
    gdf2 = _get_gdf(overlay_layer)
    
    if gdf1 is None or gdf2 is None:
        return ToolResult(success=False, error="Both INPUT and OVERLAY must be valid vector layers")
        
    try:
        # GeoPandas overlay requires the same CRS
        if gdf1.crs and gdf2.crs and gdf1.crs != gdf2.crs:
            gdf2 = gdf2.to_crs(gdf1.crs)
            
        result_gdf = gdf1.overlay(gdf2, how=how)
        
        name1 = getattr(input_layer, 'name', 'layer1')
        name2 = getattr(overlay_layer, 'name', 'layer2')
        out_name = f"{name1}_{how}_{name2}"
        
        result_layer = _to_layer(result_gdf, out_name, input_layer)
        
        return ToolResult(
            success=True, 
            output=result_layer, 
            message=f"Successfully ran {how} overlay"
        )
    except Exception as e:
        return ToolResult(success=False, error=str(e))


def run_clip(params: Dict[str, Any]) -> ToolResult:
    input_layer = params.get("INPUT")
    overlay_layer = params.get("OVERLAY")
    
    gdf1 = _get_gdf(input_layer)
    gdf2 = _get_gdf(overlay_layer)
    
    if gdf1 is None or gdf2 is None:
        return ToolResult(success=False, error="Both INPUT and OVERLAY must be valid vector layers")
        
    try:
        # GeoPandas clip requires same CRS
        if gdf1.crs and gdf2.crs and gdf1.crs != gdf2.crs:
            gdf2 = gdf2.to_crs(gdf1.crs)
            
        result_gdf = gdf1.clip(gdf2)
        
        name1 = getattr(input_layer, 'name', 'layer1')
        out_name = f"{name1}_clipped"
        
        result_layer = _to_layer(result_gdf, out_name, input_layer)
        
        return ToolResult(
            success=True, 
            output=result_layer, 
            message="Successfully clipped layer"
        )
    except Exception as e:
        return ToolResult(success=False, error=str(e))


# Map QGIS algorithm IDs to portable functions
_ALGORITHM_MAP = {
    "native:buffer": run_buffer,
    "native:intersection": lambda p: run_overlay(p, "intersection"),
    "native:union": lambda p: run_overlay(p, "union"),
    "native:difference": lambda p: run_overlay(p, "difference"),
    "native:symmetricaldifference": lambda p: run_overlay(p, "symmetric_difference"),
    "native:clip": run_clip,
}


def run_portable_algorithm(algorithm_id: str, parameters: Dict[str, object]) -> ToolResult:
    """
    Main entrypoint for the portable backend.
    Takes a QGIS algorithm ID and executes a pure Python equivalent.
    """
    logger.info(f"Portable backend intercepting algorithm: {algorithm_id}")
    
    handler = _ALGORITHM_MAP.get(algorithm_id)
    
    if handler:
        return handler(parameters)
    else:
        return ToolResult(
            success=False,
            error=f"Algorithm '{algorithm_id}' is not yet supported in the portable backend."
        )
