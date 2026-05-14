# -*- coding: utf-8 -*-
"""
GeoSI - QGIS Backend Bridge

This module is loaded only inside the QGIS plugin process. It registers
a "qgis" backend with `geosi_engine.base.register_backend` so that every
BackendTool in the universal engine dispatches to QGIS Processing when
the user is running GeoSI inside QGIS.

The engine itself has zero QGIS imports; all QGIS coupling lives here.
"""

import logging
import sys
import os
import tempfile
import uuid

# Ensure plugin directory is in sys.path
plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

from geosi_engine.base import register_backend
from geosi_engine.models import ToolResult

logger = logging.getLogger("geosi_plugin.qgis_bridge")

# Raster extensions for output type detection
_RASTER_ALGORITHMS = {
    "native:slope", "native:aspect", "native:hillshade", "native:ruggednessindex",
    "qgis:slope", "qgis:aspect", "qgis:hillshade", "qgis:ruggednessindex",
    "gdal:slope", "gdal:aspect", "gdal:hillshade", "gdal:roughness",
    "gdal:fillnodata", "gdal:translate", "gdal:warpreproject", "gdal:cliprasterbyextent",
    "gdal:cliprasterbymasklayer", "gdal:contour", "gdal:rastercalculator",
    "native:rastercalc", "native:createconstantrasterlayer",
    "native:rastersurfacevolume", "native:rastersampling",
    "saga:slopeaspectcurvature",
}


def _make_temp_output(algorithm_id: str) -> str:
    """Generate a temp file path with the correct extension for the algorithm."""
    uid = uuid.uuid4().hex[:8]
    algo_short = algorithm_id.split(":")[-1] if ":" in algorithm_id else algorithm_id
    if algorithm_id.lower() in _RASTER_ALGORITHMS:
        ext = ".tif"
    else:
        ext = ".gpkg"
    return os.path.join(tempfile.gettempdir(), f"geosi_{algo_short}_{uid}{ext}")


def _detect_layer_type(algorithm_id: str) -> str:
    """Return 'raster' or 'vector' based on the algorithm."""
    return "raster" if algorithm_id.lower() in _RASTER_ALGORITHMS else "vector"


def _run_qgis_algorithm(algorithm_id: str, parameters: dict) -> ToolResult:
    try:
        import processing  # provided by QGIS runtime
    except ImportError:
        return ToolResult(
            success=False,
            error="QGIS Processing is not available in this environment.",
            message="This tool must be run from inside QGIS.",
        )
    try:
        from geosi_engine.models import Layer
        
        # Unwrap GeoSI Layer objects back to actual QgsMapLayer objects
        # This is CRITICAL for thread safety: passing a string name forces QGIS to 
        # search QgsProject (a GUI singleton) from a background thread, causing a crash.
        # However, passing QgsMapLayer directly is ALSO dangerous. We should use filepath.
        unwrapped_params = {}
        for k, v in parameters.items():
            if isinstance(v, Layer):
                # Always prefer file path for thread safety in background processing
                if v.filepath and os.path.isfile(v.filepath):
                    unwrapped_params[k] = v.filepath
                elif hasattr(v, "features") and v.features is not None:
                    try:
                        # Try to use layer ID instead of the object itself
                        unwrapped_params[k] = v.features.id()
                    except Exception:
                        unwrapped_params[k] = v.features
                else:
                    unwrapped_params[k] = v.name
            else:
                unwrapped_params[k] = v
        
        # ── KEY FIX: Replace "memory:" with a temp file path ──────────
        output_file = None
        if unwrapped_params.get("OUTPUT") in ("memory:", "TEMPORARY_OUTPUT", None, ""):
            output_file = _make_temp_output(algorithm_id)
            unwrapped_params["OUTPUT"] = output_file
            logger.info(f"Redirected OUTPUT to temp file: {output_file}")
                
        # --- DEBUG LOGGING ---
        with open("/tmp/geosi_bridge.log", "a") as dbg:
            dbg.write(f"\n--- EXEC: {algorithm_id} ---\n")
            dbg.write(f"PARAMS: {unwrapped_params}\n")
        
        logger.info(f"Running {algorithm_id} with params: {unwrapped_params}")
        result = processing.run(algorithm_id, unwrapped_params)
        logger.info(f"Result from {algorithm_id}: {result}")
        
        with open("/tmp/geosi_bridge.log", "a") as dbg:
            dbg.write(f"RESULT: {result}\n")
        
        # ── Wrap output in a GeoSI Layer object ───────────────────────
        output_value = result.get("OUTPUT", "")
        output_path = None
        
        # Determine the actual output path
        if isinstance(output_value, str) and os.path.isfile(output_value):
            output_path = output_value
        elif output_file and os.path.isfile(output_file):
            output_path = output_file
        else:
            # Try to extract path from QgsMapLayer object
            try:
                if hasattr(output_value, 'source'):
                    src = output_value.source()
                    if os.path.isfile(src):
                        output_path = src
            except Exception:
                pass
        
        with open("/tmp/geosi_bridge.log", "a") as dbg:
            dbg.write(f"OUTPUT PATH: {output_path}\n")
            if output_path and os.path.isfile(output_path):
                size = os.path.getsize(output_path)
                dbg.write(f"FILE SIZE: {size} bytes\n")
            else:
                size = 0
                
        # Validation: Did the algorithm actually produce a file?
        if not output_path or not os.path.isfile(output_path) or size < 100:
            error_msg = f"Algorithm {algorithm_id} completed but output file was invalid (size: {size} bytes). Check QGIS log."
            logger.error(error_msg)
            
            with open("/tmp/geosi_bridge.log", "a") as dbg:
                dbg.write(f"ERROR: {error_msg}\n")
                
            return ToolResult(
                success=False,
                error=error_msg,
                message=f"QGIS algorithm silently failed to produce output: {algorithm_id}",
            )

        layer_type = _detect_layer_type(algorithm_id)
        algo_name = algorithm_id.split(":")[-1] if ":" in algorithm_id else algorithm_id
        output_layer = Layer(
            name=f"{algo_name}_result",
            filepath=output_path,
            layer_type=layer_type,
            geometry_type="raster" if layer_type == "raster" else "unknown",
            feature_count=1,
            crs="",  # Will be read from file when loaded
        )
        logger.info(f"Wrapped output as Layer: {output_path} ({layer_type})")
        return ToolResult(
            success=True,
            output=output_layer,
            message=f"QGIS algorithm completed: {algorithm_id}",
        )
    except Exception as e:
        logger.error(f"QGIS algorithm failed: {algorithm_id}: {e}")
        return ToolResult(
            success=False,
            error=str(e),
            message=f"QGIS algorithm failed: {algorithm_id}",
        )


def install() -> None:
    """Register the QGIS backend with the universal engine."""
    register_backend("qgis", _run_qgis_algorithm)
    logger.info("GeoSI: QGIS backend installed.")
