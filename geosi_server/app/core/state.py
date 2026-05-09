# -*- coding: utf-8 -*-
"""
GeoSI Server Workspace State

Holds loaded layers in memory and keeps a monotonic `version` counter per
layer so downstream caches (GeoJSON, validation reports) can invalidate
in O(1) rather than rebuilding from scratch.

The workspace is also bridged to the engine's StateManager: every
mutation propagates once, which removes the O(L) full-sync loop that
used to run on every API call.
"""

from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


class LayerRecord:
    """Metadata about one loaded layer."""

    def __init__(
        self,
        name: str,
        geometry_type: str,
        feature_count: int,
        crs: str,
        filepath: str = "",
        layer_type: str = "vector",
        version: int = 1,
    ):
        self.name = name
        self.geometry_type = geometry_type
        self.feature_count = feature_count
        self.crs = crs
        self.filepath = filepath
        self.layer_type = layer_type
        self.version = version
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at


class WorkspaceState:
    """
    Track loaded layers, their metadata, and an invalidation version
    counter per layer. Mutations propagate through registered listeners
    (e.g. the engine StateManager) so no periodic sync is ever needed.
    """

    def __init__(self):
        self.layers: Dict[str, Any] = {}
        self.metadata: Dict[str, LayerRecord] = {}
        self._listeners: List[Callable[[str, str, Any], None]] = []

    # -- listener plumbing ------------------------------------------------

    def add_listener(self, listener: Callable[[str, str, Any], None]) -> None:
        """
        Register a callback invoked as listener(event, name, layer) where
        event is one of: 'added', 'removed', 'replaced'.
        """
        self._listeners.append(listener)

    def _emit(self, event: str, name: str, layer: Any) -> None:
        for listener in self._listeners:
            try:
                listener(event, name, layer)
            except Exception:
                # Listener failure must never break a GIS operation.
                pass

    # -- layer CRUD -------------------------------------------------------

    def add_layer(self, name: str, layer: Any, record: LayerRecord):
        """Store a layer; bumps version and emits the correct event."""
        existing = self.metadata.get(name)
        if existing is not None:
            record.version = existing.version + 1
        record.updated_at = datetime.utcnow()
        event = "replaced" if existing is not None else "added"
        self.layers[name] = layer
        self.metadata[name] = record
        self._emit(event, name, layer)

    def remove_layer(self, name: str) -> bool:
        if name not in self.layers:
            return False
        layer = self.layers.pop(name)
        self.metadata.pop(name, None)
        self._emit("removed", name, layer)
        return True

    def get_layer(self, name: str) -> Optional[Any]:
        return self.layers.get(name)

    def get_record(self, name: str) -> Optional[LayerRecord]:
        return self.metadata.get(name)

    def get_version(self, name: str) -> int:
        record = self.metadata.get(name)
        return record.version if record else 0

    def has_layer(self, name: str) -> bool:
        return name in self.layers

    def list_records(self) -> List[LayerRecord]:
        return list(self.metadata.values())
