# -*- coding: utf-8 -*-
"""
GeoSI Persistence Layer (In-Process, Standalone)

A self-contained cache + telemetry store used by the GeoSI server. No
external databases or services are contacted; everything lives in the
running process.

Design notes for the GIS use case:
    * GeoJSON is cached keyed by (layer_name, layer_version, bbox,
      simplify_tolerance, limit) so map panning + zooming can reuse
      previously rendered tiles without re-serializing full layers.
    * Validation reports are cached by (layer_name, layer_version) so
      repeated QA passes over a 1M feature layer return instantly.
    * A layer `version` counter is the single invalidation token: every
      write to a layer bumps the version, which invalidates every
      downstream cache entry for that layer in O(1).
    * Telemetry is kept in a bounded ring buffer so the server records
      recent timings without unbounded memory growth.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from collections import deque
from typing import Any, Deque, Dict, List, Optional, Tuple

logger = logging.getLogger("geosi_server.persistence")


class _MemoryBackend:
    """In-process store for layer metadata and caches."""

    def __init__(self) -> None:
        # Thread-safe lock for all dictionary operations
        self._lock = threading.Lock()
        # Layer metadata: key = (workspace_id, layer_name), value = layer record
        self._layers: Dict[Tuple[str, str], Dict[str, Any]] = {}
        # GeoJSON cache: key = (workspace_id, layer_name, version, bbox, tolerance, limit)
        self._geojson: Dict[Tuple[str, str, int, str, float, int], Dict[str, Any]] = {}
        # Validation report cache: key = (workspace_id, layer_name, version)
        self._validation: Dict[Tuple[str, str, int], Dict[str, Any]] = {}

    def upsert_layer(self, workspace_id: str, record: Dict[str, Any]) -> None:
        with self._lock:
            self._layers[(workspace_id, record["layer_name"])] = dict(record)

    def get_layer(self, workspace_id: str, layer_name: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            value = self._layers.get((workspace_id, layer_name))
            return dict(value) if value else None

    def delete_layer(self, workspace_id: str, layer_name: str) -> None:
        with self._lock:
            self._layers.pop((workspace_id, layer_name), None)

    def list_layers(self, workspace_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                dict(v)
                for (ws, _), v in self._layers.items()
                if ws == workspace_id
            ]

    def get_geojson(
        self,
        workspace_id: str,
        layer_name: str,
        layer_version: int,
        bbox: str,
        simplify_tolerance: float,
        limit_n: int,
    ) -> Optional[Dict[str, Any]]:
        key = (
            workspace_id,
            layer_name,
            layer_version,
            bbox,
            simplify_tolerance,
            limit_n,
        )
        with self._lock:
            value = self._geojson.get(key)
            return dict(value) if value else None

    def put_geojson(self, workspace_id: str, record: Dict[str, Any]) -> None:
        key = (
            workspace_id,
            record["layer_name"],
            record["layer_version"],
            record["bbox"],
            record["simplify_tolerance"],
            record["limit_n"],
        )
        with self._lock:
            self._geojson[key] = dict(record)

    def invalidate_layer_caches(self, workspace_id: str, layer_name: str) -> None:
        with self._lock:
            for key in list(self._geojson.keys()):
                if key[0] == workspace_id and key[1] == layer_name:
                    self._geojson.pop(key, None)
            for key in list(self._validation.keys()):
                if key[0] == workspace_id and key[1] == layer_name:
                    self._validation.pop(key, None)

    def get_validation(
        self, workspace_id: str, layer_name: str, layer_version: int
    ) -> Optional[Dict[str, Any]]:
        with self._lock:
            value = self._validation.get((workspace_id, layer_name, layer_version))
            return dict(value) if value else None

    def put_validation(self, workspace_id: str, record: Dict[str, Any]) -> None:
        key = (workspace_id, record["layer_name"], record["layer_version"])
        with self._lock:
            self._validation[key] = dict(record)


class PersistenceService:
    """
    In-process facade over the memory backend. All GIS-level callers
    use this single entry point so the server stays database-free while
    keeping the hot-path caches and telemetry that matter for GIS
    performance.
    """

    # Max telemetry entries kept in a bounded ring buffer
    _METRICS_MAX = 1024

    def __init__(self, workspace_id: Optional[str] = None) -> None:
        # Initialize workspace ID from param, env var, or default
        self.workspace_id = workspace_id or os.environ.get(
            "GEOSI_WORKSPACE_ID", "default"
        )
        # Backend provides thread-safe cache dictionaries
        self._memory = _MemoryBackend()
        # Lock for appending metrics to the bounded deque
        self._metrics_lock = threading.Lock()
        # Ring buffer (auto-evicts oldest when full)
        self._metrics: Deque[Dict[str, Any]] = deque(maxlen=self._METRICS_MAX)
        logger.info("Persistence: in-process backend active")

    # -- layer metadata --------------------------------------------------

    def upsert_layer(self, record: Dict[str, Any]) -> None:
        self._memory.upsert_layer(self.workspace_id, record)

    def get_layer_version(self, layer_name: str) -> int:
        local = self._memory.get_layer(self.workspace_id, layer_name)
        if local:
            return int(local.get("version", 1))
        return 0

    def delete_layer(self, layer_name: str) -> None:
        self._memory.delete_layer(self.workspace_id, layer_name)
        self._memory.invalidate_layer_caches(self.workspace_id, layer_name)

    def invalidate_layer(self, layer_name: str) -> None:
        self._memory.invalidate_layer_caches(self.workspace_id, layer_name)

    # -- GeoJSON cache ---------------------------------------------------

    def get_geojson(
        self,
        layer_name: str,
        layer_version: int,
        bbox: str = "",
        simplify_tolerance: float = 0.0,
        limit_n: int = 0,
    ) -> Optional[Dict[str, Any]]:
        hit = self._memory.get_geojson(
            self.workspace_id, layer_name, layer_version,
            bbox, simplify_tolerance, limit_n,
        )
        if hit:
            return hit.get("payload")
        return None

    def put_geojson(
        self,
        layer_name: str,
        layer_version: int,
        payload: Dict[str, Any],
        crs: str = "EPSG:4326",
        bbox: str = "",
        simplify_tolerance: float = 0.0,
        limit_n: int = 0,
    ) -> None:
        record = {
            "layer_name": layer_name,
            "layer_version": layer_version,
            "bbox": bbox,
            "simplify_tolerance": simplify_tolerance,
            "limit_n": limit_n,
            "payload": payload,
            "crs": crs,
        }
        self._memory.put_geojson(self.workspace_id, record)

    # -- validation cache ------------------------------------------------

    def get_validation(
        self, layer_name: str, layer_version: int
    ) -> Optional[Dict[str, Any]]:
        return self._memory.get_validation(
            self.workspace_id, layer_name, layer_version
        )

    def put_validation(
        self,
        layer_name: str,
        layer_version: int,
        report: Dict[str, Any],
        sampled: bool = False,
        sample_size: int = 0,
    ) -> None:
        record = {
            "layer_name": layer_name,
            "layer_version": layer_version,
            "report": report,
            "sampled": sampled,
            "sample_size": sample_size,
        }
        self._memory.put_validation(self.workspace_id, record)

    # -- telemetry -------------------------------------------------------

    def record_metric(
        self,
        operation: str,
        duration_ms: float,
        feature_count: int = 0,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        entry = {
            "operation": operation,
            "duration_ms": duration_ms,
            "feature_count": feature_count,
            "meta": meta or {},
            "recorded_at": time.time(),
        }
        with self._metrics_lock:
            self._metrics.append(entry)

    def recent_metrics(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._metrics_lock:
            if limit <= 0 or limit >= len(self._metrics):
                return list(self._metrics)
            return list(self._metrics)[-limit:]


class Timer:
    """Tiny context manager for operation telemetry."""

    def __init__(
        self,
        persistence: PersistenceService,
        operation: str,
        feature_count: int = 0,
        meta: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._persistence = persistence
        self._operation = operation
        self._feature_count = feature_count
        self._meta = meta or {}
        self._start = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        duration_ms = (time.perf_counter() - self._start) * 1000.0
        self._persistence.record_metric(
            self._operation, duration_ms, self._feature_count, self._meta
        )


persistence = PersistenceService()
