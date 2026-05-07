# -*- coding: utf-8 -*-
"""
GeoSI Engine - GIS Tool Base Class (universal, framework-agnostic)

The engine core is intentionally independent of QGIS. It defines the
tool contract (`GISTool`), a portable helper base (`PortableTool`), and
a spec-only tool (`BackendTool`) whose execution is delegated to a
pluggable backend.

Surfaces wire their own backend:

    - geosi_plugin/qgis_bridge.py  -> QGIS Processing backend
    - geosi_server / CLI           -> GeoPandas/Rasterio portable backend
    - Tests                        -> mock backend

No `qgis`, `PyQt`, `processing`, or `osgeo` imports live in the engine.
"""

from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional
import logging
import time

from geosi_engine.models import (
    ToolSpec,
    ToolParameter,
    ToolResult,
)

logger = logging.getLogger("geosi_engine.base")


# ---------------------------------------------------------------------------
# Abstract base contract
# ---------------------------------------------------------------------------

class GISTool(ABC):
    """Every GIS tool implements `spec()` and `execute()`."""

    @abstractmethod
    def spec(self) -> ToolSpec:
        ...

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        ...

    def validate(self, **kwargs) -> Optional[str]:
        spec = self.spec()
        for param in spec.parameters:
            if param.required and param.name not in kwargs:
                return f"Missing required parameter: {param.name}"
        return None

    def safe_execute(self, **kwargs) -> ToolResult:
        validation_error = self.validate(**kwargs)
        if validation_error:
            return ToolResult(
                success=False,
                error=validation_error,
                message=f"Parameter validation failed for {self.spec().name}",
            )
        start = time.time()
        try:
            result = self.execute(**kwargs)
            elapsed = (time.time() - start) * 1000
            logger.info(f"{self.spec().name} ok in {elapsed:.1f}ms")
            return result
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            logger.error(f"{self.spec().name} failed in {elapsed:.1f}ms: {e}")
            return ToolResult(
                success=False,
                error=str(e),
                message=f"Tool {self.spec().name} failed with error",
            )


# ---------------------------------------------------------------------------
# Portable tools (GeoPandas / Rasterio / Shapely)
# ---------------------------------------------------------------------------

class PortableTool(GISTool):
    """Subclass when the tool runs without any host framework."""

    def spec(self) -> ToolSpec:
        raise NotImplementedError("Subclass must implement spec()")

    def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError("Subclass must implement execute()")


# ---------------------------------------------------------------------------
# Backend-dispatched tools (host injects the executor)
# ---------------------------------------------------------------------------

# A backend callable: (algorithm_id, parameters_dict) -> ToolResult
BackendFn = Callable[[str, Dict[str, object]], ToolResult]

_BACKENDS: Dict[str, BackendFn] = {}


def register_backend(name: str, fn: BackendFn) -> None:
    """Host surfaces call this once at startup to install a backend."""
    _BACKENDS[name] = fn


def get_backend(name: str) -> Optional[BackendFn]:
    return _BACKENDS.get(name)


def clear_backends() -> None:
    _BACKENDS.clear()


class BackendTool(GISTool):
    """
    Spec-only tool whose execution is delegated to a named backend.

    Used for the ~130 GIS operations that are most cleanly expressed as
    QGIS Processing algorithms inside the plugin, but must also be
    pluggable to a GeoPandas backend on the server/CLI surface.
    """

    def __init__(
        self,
        name: str,
        description: str,
        category: str,
        parameters: List[ToolParameter],
        algorithm: Optional[str] = None,
        qgis_algorithm: Optional[str] = None,
        display_name: str = "",
        outputs: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        backend: str = "qgis",
    ):
        algorithm = algorithm or qgis_algorithm
        if algorithm is None:
            raise ValueError("BackendTool requires 'algorithm' or 'qgis_algorithm'")
        self._spec = ToolSpec(
            name=name,
            display_name=display_name or name.replace("_", " ").title(),
            description=description,
            category=category,
            parameters=parameters,
            outputs=outputs or ["OUTPUT"],
            tags=tags or [],
            qgis_algorithm=algorithm,
            requires_qgis=(backend == "qgis"),
        )
        self._algorithm = algorithm
        self._backend_name = backend

    def spec(self) -> ToolSpec:
        return self._spec

    def execute(self, **kwargs) -> ToolResult:
        parameters = dict(kwargs)
        parameters.setdefault("OUTPUT", "memory:")
        fn = get_backend(self._backend_name)
        if fn is None:
            return ToolResult(
                success=False,
                error=(
                    f"No '{self._backend_name}' backend registered. "
                    f"Load this tool from the QGIS plugin or register a "
                    f"portable backend via geosi_engine.base.register_backend()."
                ),
                message=f"Tool '{self._spec.name}' has no active backend.",
            )
        return fn(self._algorithm, parameters)


# Backwards-compatible alias: existing tool modules import `QGISProcessingTool`.
# It now resolves to the universal, backend-dispatched `BackendTool`.
QGISProcessingTool = BackendTool
