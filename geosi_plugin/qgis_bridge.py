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

from geosi_engine.base import register_backend
from geosi_engine.models import ToolResult

logger = logging.getLogger("geosi_plugin.qgis_bridge")


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
        result = processing.run(algorithm_id, parameters)
        return ToolResult(
            success=True,
            output=result,
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
