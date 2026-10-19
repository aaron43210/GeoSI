"""
GeoSI Engine — Tool Base Classes (universal, framework-agnostic)
═══════════════════════════════════════════════════════════════════

Defines the tool contract hierarchy:

    GISTool (ABC)          ← abstract base, defines spec() + execute()
    ├── PortableTool       ← runs without any host framework (GeoPandas/Rasterio)
    └── BackendTool        ← spec-only, delegates to a pluggable backend

The engine core has ZERO QGIS imports. Surfaces wire their own backend:
    - geosi_plugin/qgis_bridge.py  → QGIS Processing backend
    - Tests                        → mock backend

Design Pattern: Strategy Pattern
    BackendTool uses the Strategy pattern via register_backend().
    The algorithm remains the same (spec + dispatch), but the execution
    strategy (QGIS vs GeoPandas vs mock) is injected at runtime.

Data Structures:
    _BACKENDS: Dict[str, Callable] — O(1) hash-table lookup for backends
"""

import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple

from geosi_engine.models import (
    ToolParameter,
    ToolResult,
    ToolSpec,
)

logger = logging.getLogger("geosi_engine.base")


# ═══════════════════════════════════════════════════════════════════════════
# Abstract base contract — every GIS tool must implement these methods
# ═══════════════════════════════════════════════════════════════════════════


class GISTool(ABC):
    """
    Abstract base class for all GIS tools in GeoSI.

    Every tool must provide:
        spec()    → ToolSpec describing the tool's identity and parameters
        execute() → ToolResult after running the operation

    The safe_execute() wrapper adds parameter validation and timing.
    """

    @abstractmethod
    def spec(self) -> ToolSpec:
        """Return the tool's specification (name, params, description)."""
        ...

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Run the tool with the given parameters."""
        ...

    def validate(self, **kwargs) -> Optional[str]:
        """
        Validate that all required parameters are present.

        Complexity: O(P) where P = number of parameters in the spec.
        Returns None if valid, or an error string if invalid.
        """
        spec = self.spec()
        for param in spec.parameters:
            if param.required and param.name not in kwargs:
                return f"Missing required parameter: {param.name}"
        return None

    def safe_execute(self, **kwargs) -> ToolResult:
        """
        Execute with validation and timing.

        Pipeline:
            1. Validate parameters → O(P)
            2. Execute the tool → varies by implementation
            3. Log timing → O(1)
        """
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


# ═══════════════════════════════════════════════════════════════════════════
# Portable tools — run without any host framework (GeoPandas / Rasterio)
# ═══════════════════════════════════════════════════════════════════════════


class PortableTool(GISTool):
    """Subclass when the tool runs without any host framework."""

    def spec(self) -> ToolSpec:
        raise NotImplementedError("Subclass must implement spec()")

    def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError("Subclass must implement execute()")


# ═══════════════════════════════════════════════════════════════════════════
# Backend dispatch — Strategy Pattern for pluggable execution
#
# _BACKENDS is a hash table mapping backend names to callables.
# register_backend() is called once by each surface at startup:
#   - QGIS plugin calls register_backend("qgis", _run_qgis_algorithm)
#   - Tests call register_backend("mock", mock_fn)
#
# Lookup is O(1) amortized via Python dict.
# ═══════════════════════════════════════════════════════════════════════════

# Backend callable signature: (algorithm_id: str, params: dict) → ToolResult
BackendFn = Callable[[str, Dict[str, object]], ToolResult]

# Hash table of registered backends — O(1) lookup
_BACKENDS: Dict[str, BackendFn] = {}


def register_backend(name: str, fn: BackendFn) -> None:
    """
    Register a backend execution strategy.

    Called once by each surface at startup:
        register_backend("qgis", _run_qgis_algorithm)

    Complexity: O(1)
    """
    _BACKENDS[name] = fn


def get_backend(name: str) -> Optional[BackendFn]:
    """Get a registered backend by name. O(1) dict lookup."""
    return _BACKENDS.get(name)


def clear_backends() -> None:
    """Clear all registered backends (used in tests)."""
    _BACKENDS.clear()
    global _INSPECTOR, _EXPRESSION_VALIDATOR, _ROW_READER
    _INSPECTOR = None
    _EXPRESSION_VALIDATOR = None
    _ROW_READER = None


# Layer inspector: (Layer, max_rows) → text summary of the layer's contents.
# The QGIS plugin registers one so the agent loop can read results back
# (attribute rows, raster band statistics) without importing QGIS itself.
InspectorFn = Callable[..., str]
_INSPECTOR: Optional[InspectorFn] = None


def register_inspector(fn: InspectorFn) -> None:
    global _INSPECTOR
    _INSPECTOR = fn


def get_inspector() -> Optional[InspectorFn]:
    return _INSPECTOR


# Row reader: (Layer, max_rows) → attribute rows as dicts. Lets answers be
# computed exactly from result tables (the QGIS plugin registers one).
RowReaderFn = Callable[..., List[Dict[str, Any]]]
_ROW_READER: Optional[RowReaderFn] = None


def register_row_reader(fn: RowReaderFn) -> None:
    global _ROW_READER
    _ROW_READER = fn


def get_row_reader() -> Optional[RowReaderFn]:
    return _ROW_READER


# UI actions: tools that must touch the QGIS GUI or project (add a basemap,
# move the map) hand a callable to run_in_ui(). Requests run in a background
# task, and Qt objects may only be used from the main thread, so while a UI is
# attached the call is queued and the plugin runs it on the main thread once
# the request finishes. With no UI (server, tests) it runs immediately.
_UI_LOCK = threading.Lock()
_UI_QUEUE: List[Tuple[str, Callable[[], Any]]] = []
_UI_ATTACHED = False
_UI_IFACE: Any = None


def attach_ui(attached: bool = True, iface: Any = None) -> None:
    """Called by the plugin dock; ``iface`` is the QgisInterface map actions should use."""
    global _UI_ATTACHED, _UI_IFACE
    _UI_ATTACHED = attached
    _UI_IFACE = iface if attached else None
    if not attached:
        drain_ui_actions()


def ui_iface() -> Any:
    """The attached QgisInterface, else QGIS's global one (None outside QGIS)."""
    if _UI_IFACE is not None:
        return _UI_IFACE
    try:
        from qgis.utils import iface

        return iface
    except ImportError:
        return None


def run_in_ui(description: str, fn: Callable[[], Any]) -> Any:
    if not _UI_ATTACHED:
        return fn()
    with _UI_LOCK:
        _UI_QUEUE.append((description, fn))
    return None


def drain_ui_actions() -> List[Tuple[str, Callable[[], Any]]]:
    with _UI_LOCK:
        items = list(_UI_QUEUE)
        _UI_QUEUE.clear()
    return items


# Expression validator: (expression) → error message, or None when valid.
# The QGIS plugin registers one backed by QgsExpression so the Validation
# Agent can reject malformed QGIS expressions before a tool runs.
ExpressionValidatorFn = Callable[[str], Optional[str]]
_EXPRESSION_VALIDATOR: Optional[ExpressionValidatorFn] = None


def register_expression_validator(fn: ExpressionValidatorFn) -> None:
    global _EXPRESSION_VALIDATOR
    _EXPRESSION_VALIDATOR = fn


def get_expression_validator() -> Optional[ExpressionValidatorFn]:
    return _EXPRESSION_VALIDATOR


class BackendTool(GISTool):
    """
    Spec-only tool that delegates execution to a named backend.

    In GeoSI v2, ALL QGIS tools are BackendTool instances created
    dynamically by auto_discover_qgis_tools() in qgis_bridge.py.

    The tool stores the QGIS algorithm ID (e.g. "native:buffer") and
    when execute() is called, it looks up the "qgis" backend callable
    and passes the algorithm + parameters to it.

    Design Pattern: Strategy Pattern
        The BackendTool is the Context, the backend callable is the Strategy.
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
        risk_level: str = "read_only",
    ):
        # Accept either 'algorithm' or 'qgis_algorithm' for compatibility
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
            risk_level=risk_level,
        )
        self._algorithm = algorithm
        self._backend_name = backend

    def spec(self) -> ToolSpec:
        return self._spec

    def execute(self, **kwargs) -> ToolResult:
        """
        Dispatch to the registered backend.

        1. Build parameters dict from kwargs
        2. Look up the backend callable (O(1) hash lookup)
        3. Call backend(algorithm_id, parameters)
        """
        parameters = dict(kwargs)
        parameters.setdefault("OUTPUT", "memory:")

        # O(1) backend lookup
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


# Backwards-compatible alias
QGISProcessingTool = BackendTool
