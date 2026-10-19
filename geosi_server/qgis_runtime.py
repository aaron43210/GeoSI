"""
GeoSI Server — Headless QGIS Runtime
══════════════════════════════════════════════════════════════════════
Initialises a QgsApplication in offscreen mode so the FastAPI server
can run QGIS Processing algorithms without a display.

Usage
-----
Call ``init()`` once at application startup (lifespan) then use
``engine_factory`` as the ``SessionPool`` factory:

    pool = SessionPool(factory=engine_factory)

Each session gets its own GeoSI engine with QGIS tools already installed
and a private workspace directory under ``GEOSI_DATA_DIR``.

The module is deliberately import-safe: importing it does not start QGIS.
Only ``init()`` launches the application; if QGIS is unavailable the
function returns ``False`` and the server continues without QGIS tools.
"""

from __future__ import annotations

import logging
import os
import threading
from pathlib import Path
from typing import Any

logger = logging.getLogger("geosi_server.qgis_runtime")

# Global QgsApplication instance (one per process)
_qgs_app: Any | None = None
_init_lock = threading.Lock()

# Cap concurrent QGIS Processing calls to avoid overloading the headless instance
_MAX_CONCURRENT = int(os.environ.get("GEOSI_QGIS_CONCURRENCY", "4"))
_semaphore = threading.Semaphore(_MAX_CONCURRENT)

# Base data directory: each session gets a subdirectory here
_DATA_DIR = Path(os.environ.get("GEOSI_DATA_DIR", str(Path.home() / ".geosi" / "data")))  # nosec B108


def init() -> bool:
    """
    Initialise the headless QgsApplication exactly once.

    Returns ``True`` when QGIS is ready, ``False`` when QGIS is not available
    (the server continues without native QGIS tools — planning still works via
    the LLM cascade and deterministic planners).
    """
    global _qgs_app
    with _init_lock:
        if _qgs_app is not None:
            return True
        try:
            import processing  # noqa: F401 - triggers provider registration
            from qgis.core import QgsApplication

            os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
            qgs = QgsApplication([], False)  # False → no GUI
            qgs.initQgis()

            # Initialise Processing framework (loads all providers)
            from processing.core.Processing import Processing

            Processing.initialize()

            _qgs_app = qgs
            logger.info("Headless QGIS initialised (Processing ready)")
            return True
        except Exception as exc:
            logger.warning("QGIS not available — native tools disabled: %s", exc)
            return False


def shutdown() -> None:
    """Call at application shutdown to release QGIS resources."""
    global _qgs_app
    with _init_lock:
        if _qgs_app is not None:
            try:
                _qgs_app.exitQgis()
            except Exception as exc:
                logger.debug("QGIS exitQgis: %s", exc)
            _qgs_app = None


def is_available() -> bool:
    """Return True when the headless QgsApplication is running."""
    return _qgs_app is not None


def session_workspace(session_id: str) -> Path:
    """
    Return (and create) a private directory for *session_id*'s outputs.

    The directory is ``$GEOSI_DATA_DIR/<session_id>/``. Using per-session
    workspaces prevents output files from different sessions colliding and
    makes cleanup trivial (delete the directory).
    """
    # Sanitise: allow only alphanum, dash, underscore, dot
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in session_id)[:64]
    ws = _DATA_DIR / safe
    ws.mkdir(parents=True, exist_ok=True)
    return ws


def engine_factory(session_id: str) -> Any:
    """
    ``SessionPool`` factory: create a GeoSI engine for *session_id*.

    If QGIS is available, QGIS Processing tools are installed into the
    engine's registry. The engine's output paths default to the session
    workspace.
    """
    from geosi_engine import GeoSI

    engine = GeoSI(use_llm=True)

    # Point the engine at the session workspace so outputs land there
    ws = session_workspace(session_id)
    try:
        engine.workspace = ws
        engine._session_id = session_id
    except Exception:
        logger.debug("suppressed exception", exc_info=True)

    if is_available():
        try:
            from geosi_plugin.qgis_bridge import install

            count = install(registry=engine.registry)
            logger.debug("Session %s: %d QGIS tools installed", session_id, count)
        except Exception as exc:
            logger.warning("QGIS bridge install failed for session %s: %s", session_id, exc)
    else:
        logger.debug("Session %s: QGIS unavailable — portable tools only", session_id)

    return engine


def semaphore() -> threading.Semaphore:
    """Return the process-wide QGIS concurrency semaphore."""
    return _semaphore
