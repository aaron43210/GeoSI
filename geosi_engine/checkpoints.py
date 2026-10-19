# -*- coding: utf-8 -*-
"""
GeoSI — Checkpoint & 1-Click Undo Engine
═══════════════════════════════════════════════════════════════════════
Records a snapshot of the QGIS project before any agent plan runs and
restores it cleanly on request.

Architecture
────────────
    CheckpointManager (singleton per engine session)
        │
        ├─ create_snapshot(project)  → Checkpoint
        │       Saves: layer IDs, temp GPKG for memory layers, style XML
        │
        └─ rollback(checkpoint)
                Removes newly added layers
                Restores removed memory layers from GPKG
                Reloads style XML for modified layers

Used by AgentLoop: before executing a plan, call create_snapshot(); if
the user clicks Undo, call rollback(checkpoint_id).

The manager is QGIS-optional — on non-QGIS environments (tests, server)
it is a no-op that returns stub checkpoints.
"""
from __future__ import annotations

import logging
import os
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("geosi_engine.checkpoints")

_SNAPSHOTS_DIR = Path(os.environ.get("GEOSI_SNAPSHOTS_DIR",
                                     Path.home() / ".geosi" / "snapshots"))


@dataclass
class LayerSnapshot:
    layer_id: str
    name: str
    source: str
    layer_type: str      # "vector" | "raster" | "plugin"
    provider: str
    crs_wkt: str
    style_xml: str       # QML style XML
    memory_gpkg: Optional[str] = None   # temp file for memory layers
    memory_layer_name: Optional[str] = None


@dataclass
class Checkpoint:
    checkpoint_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: float = field(default_factory=time.monotonic)
    layer_ids_before: List[str] = field(default_factory=list)
    layer_snapshots: Dict[str, LayerSnapshot] = field(default_factory=dict)
    query: str = ""

    def age_seconds(self) -> float:
        return time.monotonic() - self.created_at


class CheckpointManager:
    """
    Per-session checkpoint manager.

    Thread-safe; holds at most *max_checkpoints* in memory to avoid
    accumulating stale temporary GeoPackage files.
    """

    def __init__(self, max_checkpoints: int = 10) -> None:
        self._max = max_checkpoints
        self._checkpoints: Dict[str, Checkpoint] = {}
        self._lock = threading.Lock()
        _SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Public API ─────────────────────────────────────────────────────

    def create_snapshot(self, query: str = "", project: Any = None) -> Checkpoint:
        """
        Snapshot the current QGIS project state.

        Captures layer IDs, serialises memory layers to a temp GPKG, and
        saves QML style XML for every layer. Returns a Checkpoint.
        """
        project = project or self._get_project()
        cp = Checkpoint(query=query)

        if project is None:
            logger.debug("No QGIS project — returning empty checkpoint")
            with self._lock:
                self._checkpoints[cp.checkpoint_id] = cp
            return cp

        try:
            layers = project.mapLayers()
            cp.layer_ids_before = list(layers.keys())

            for lid, layer in layers.items():
                snap = self._snapshot_layer(layer, cp.checkpoint_id)
                if snap:
                    cp.layer_snapshots[lid] = snap

        except Exception as exc:
            logger.warning("Snapshot failed (non-fatal): %s", exc)

        with self._lock:
            self._checkpoints[cp.checkpoint_id] = cp
            self._evict_old()

        logger.info("Checkpoint %s created (%d layers)", cp.checkpoint_id,
                    len(cp.layer_ids_before))
        return cp

    def rollback(self, checkpoint_id: str, project: Any = None) -> bool:
        """
        Rollback to the given checkpoint.

        Removes layers added after the snapshot, restores memory layers
        from the temp GPKG, and reapplies saved QML styles.

        Returns True on success.
        """
        with self._lock:
            cp = self._checkpoints.get(checkpoint_id)
        if cp is None:
            logger.warning("Checkpoint %s not found", checkpoint_id)
            return False

        project = project or self._get_project()
        if project is None:
            return False

        try:
            current_ids = set(project.mapLayers().keys())
            before_ids  = set(cp.layer_ids_before)

            # 1. Remove layers added after the snapshot
            added_ids = current_ids - before_ids
            if added_ids:
                project.removeMapLayers(list(added_ids))
                logger.info("Rollback: removed %d layer(s)", len(added_ids))

            # 2. Restore memory layers that were present before but are now gone
            removed_ids = before_ids - set(project.mapLayers().keys())
            for lid in removed_ids:
                snap = cp.layer_snapshots.get(lid)
                if snap and snap.memory_gpkg and Path(snap.memory_gpkg).exists():
                    self._restore_memory_layer(snap, project)

            # 3. Reapply styles for layers that still exist
            for lid, snap in cp.layer_snapshots.items():
                layer = project.mapLayer(lid)
                if layer and snap.style_xml:
                    self._reapply_style(layer, snap.style_xml)

            logger.info("Rollback to checkpoint %s complete", checkpoint_id)
            return True

        except Exception as exc:
            logger.error("Rollback failed: %s", exc)
            return False

    def get(self, checkpoint_id: str) -> Optional[Checkpoint]:
        with self._lock:
            return self._checkpoints.get(checkpoint_id)

    def discard(self, checkpoint_id: str) -> None:
        """Delete a checkpoint and clean up its temp files."""
        with self._lock:
            cp = self._checkpoints.pop(checkpoint_id, None)
        if cp:
            self._cleanup(cp)

    # ── Private helpers ────────────────────────────────────────────────

    @staticmethod
    def _get_project() -> Optional[Any]:
        try:
            from qgis.core import QgsProject
            return QgsProject.instance()
        except ImportError:
            return None

    def _snapshot_layer(self, layer: Any, cp_id: str) -> Optional[LayerSnapshot]:
        try:
            lid = layer.id()
            style_xml = ""
            try:
                import xml.etree.ElementTree as ET
                doc = layer.asLayerDefinition() if hasattr(layer, "asLayerDefinition") else None
                if doc:
                    style_xml = ET.tostring(doc.documentElement() if hasattr(doc, "documentElement") else doc,
                                             encoding="unicode")
                else:
                    mgr = layer.styleManager()
                    style_xml = mgr.currentStyle() if mgr else ""
            except Exception:
                pass

            is_memory = "memory" in layer.providerType().lower() if hasattr(layer, "providerType") else False
            memory_gpkg = None
            memory_name = None

            if is_memory:
                gpkg_path = str(_SNAPSHOTS_DIR / f"{cp_id}_{lid[:8]}.gpkg")
                try:
                    from qgis.core import QgsVectorFileWriter, QgsCoordinateTransformContext
                    opts = QgsVectorFileWriter.SaveVectorOptions()
                    opts.layerName = layer.name()
                    opts.fileEncoding = "UTF-8"
                    QgsVectorFileWriter.writeAsVectorFormatV3(
                        layer, gpkg_path,
                        QgsCoordinateTransformContext(), opts,
                    )
                    memory_gpkg = gpkg_path
                    memory_name = layer.name()
                except Exception as exc:
                    logger.debug("Could not save memory layer %s to GPKG: %s", lid, exc)

            return LayerSnapshot(
                layer_id=lid,
                name=layer.name(),
                source=layer.source() if hasattr(layer, "source") else "",
                layer_type="vector" if hasattr(layer, "featureCount") else "raster",
                provider=layer.providerType() if hasattr(layer, "providerType") else "",
                crs_wkt=layer.crs().toWkt() if hasattr(layer, "crs") else "",
                style_xml=style_xml,
                memory_gpkg=memory_gpkg,
                memory_layer_name=memory_name,
            )
        except Exception as exc:
            logger.debug("Layer snapshot failed: %s", exc)
            return None

    @staticmethod
    def _restore_memory_layer(snap: LayerSnapshot, project: Any) -> None:
        try:
            from qgis.core import QgsVectorLayer
            layer = QgsVectorLayer(
                f"{snap.memory_gpkg}|layername={snap.memory_layer_name}",
                snap.name, "ogr",
            )
            if layer.isValid():
                project.addMapLayer(layer)
                logger.info("Restored memory layer: %s", snap.name)
        except Exception as exc:
            logger.debug("Restore memory layer failed: %s", exc)

    @staticmethod
    def _reapply_style(layer: Any, style_xml: str) -> None:
        try:
            mgr = layer.styleManager()
            if mgr and style_xml:
                mgr.setCurrentStyle(style_xml)
                layer.triggerRepaint()
        except Exception:
            pass

    def _evict_old(self) -> None:
        """Remove oldest checkpoints when over the limit."""
        if len(self._checkpoints) <= self._max:
            return
        sorted_ids = sorted(self._checkpoints,
                             key=lambda k: self._checkpoints[k].created_at)
        for cid in sorted_ids[:len(self._checkpoints) - self._max]:
            cp = self._checkpoints.pop(cid)
            self._cleanup(cp)

    @staticmethod
    def _cleanup(cp: Checkpoint) -> None:
        for snap in cp.layer_snapshots.values():
            if snap.memory_gpkg:
                try:
                    Path(snap.memory_gpkg).unlink(missing_ok=True)
                except Exception:
                    pass
