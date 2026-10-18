# -*- coding: utf-8 -*-
"""
GeoSI Engine — State Manager

Tracks all spatial layers, execution history, and intermediate results
across the lifetime of a GeoSI session. Both the QGIS Plugin and
FastAPI Server maintain one StateManager instance.

See FILE_CONNECTIONS.md:
    - IMPORTS FROM: models.py
    - USED BY: executor.py, geosi_plugin/, geosi_server/
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from copy import copy
import logging

from geosi_engine.models import (
    Layer,
    ToolResult,
    StepLog,
    ExecutionStatus,
)

logger = logging.getLogger("geosi_engine.state")


class StateManager:
    """
    Manages the spatial workspace state for a GeoSI session.

    Responsibilities:
        1. Layer tracking — keep a name→Layer map of every loaded layer
        2. Result caching — store intermediate results so downstream
           steps can reference them by name
        3. Execution history — log every tool execution for transparency
        4. CRS tracking — record the project CRS for reprojection checks

    Attributes:
        layers: Name → Layer dictionary of all loaded layers
        results: Name → ToolResult dictionary of intermediate outputs
        history: Ordered list of StepLog entries
        project_crs: Default CRS for the workspace (e.g. "EPSG:4326")
    """

    def __init__(self, project_crs: str = "EPSG:4326"):
        """
        Initialize a fresh state manager.

        Args:
            project_crs: Default coordinate reference system.
        """
        self.layers: Dict[str, Layer] = {}
        self.results: Dict[str, Any] = {}
        self.history: List[StepLog] = []
        self.project_crs: str = project_crs
        self._created_at: str = datetime.now().isoformat()
        # Checkpoint stack for undo / rollback (Architecture Module 7).
        # Each checkpoint is (op_id, layers_snapshot, results_snapshot).
        self._checkpoints: List[tuple] = []

    # ── Layer management ──────────────────────────────────────────────

    def add_layer(self, layer: Layer) -> None:
        """Add or replace a layer in the workspace."""
        self.layers[layer.name] = layer
        logger.info(f"Layer added: {layer}")

    def get_layer(self, name: str) -> Optional[Layer]:
        """Get a layer by name. Returns None if not found."""
        return self.layers.get(name)

    def remove_layer(self, name: str) -> bool:
        """Remove a layer. Returns True if it existed."""
        if name in self.layers:
            del self.layers[name]
            logger.info(f"Layer removed: {name}")
            return True
        return False

    def list_layers(self) -> List[str]:
        """Return a list of all loaded layer names."""
        return list(self.layers.keys())

    # ── Result caching ────────────────────────────────────────────────

    def save_result(self, name: str, result: Any) -> None:
        """
        Store an intermediate result by name.

        If the result contains a Layer in its output, also register
        that layer in self.layers so later steps can reference it.
        """
        self.results[name] = result

        # Auto-register output layers
        if isinstance(result, ToolResult) and isinstance(result.output, Layer):
            output_layer = result.output
            if not output_layer.name:
                output_layer.name = name
            self.add_layer(output_layer)

    def get_result(self, name: str) -> Optional[Any]:
        """Retrieve a cached intermediate result."""
        return self.results.get(name)

    # ── Execution history ─────────────────────────────────────────────

    def log_step(self, step_log: StepLog) -> None:
        """Append a step execution log entry."""
        self.history.append(step_log)
        status_icon = "✅" if step_log.status == ExecutionStatus.SUCCESS else "❌"
        logger.info(
            f"{status_icon} Step {step_log.step_id}: "
            f"{step_log.tool_name} → {step_log.status.value} "
            f"({step_log.duration_ms:.0f}ms)"
        )

    def get_history(self) -> List[StepLog]:
        """Return the full execution history."""
        return list(self.history)

    # ── Workspace utilities ───────────────────────────────────────────

    def clear(self) -> None:
        """Reset the entire workspace state."""
        self.layers.clear()
        self.results.clear()
        self.history.clear()
        logger.info("Workspace state cleared")

    # -- Checkpoints / undo / rollback ------------------------------------

    def checkpoint(self, op_id: str) -> str:
        """
        Snapshot the current workspace (shallow-copied layer / result dicts).

        Returns the op_id so callers can rollback_to() it later.
        """
        self._checkpoints.append((op_id, copy(self.layers), copy(self.results)))
        return op_id

    def undo(self) -> bool:
        """Revert to the most recent checkpoint. Returns False if empty."""
        if not self._checkpoints:
            return False
        _, layers, results = self._checkpoints.pop()
        self.layers = layers
        self.results = results
        logger.info("State reverted (undo)")
        return True

    def rollback_to(self, op_id: str) -> bool:
        """Revert to a named checkpoint, discarding everything after it."""
        for idx in range(len(self._checkpoints) - 1, -1, -1):
            if self._checkpoints[idx][0] == op_id:
                _, layers, results = self._checkpoints[idx]
                self.layers = layers
                self.results = results
                self._checkpoints = self._checkpoints[:idx]
                logger.info(f"State rolled back to checkpoint {op_id}")
                return True
        return False

    def summary(self) -> Dict[str, Any]:
        """Return a compact summary of the current state."""
        return {
            "layer_count": len(self.layers),
            "layers": self.list_layers(),
            "result_count": len(self.results),
            "history_count": len(self.history),
            "project_crs": self.project_crs,
            "created_at": self._created_at,
        }
