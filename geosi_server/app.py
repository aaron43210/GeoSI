# -*- coding: utf-8 -*-
"""
GeoSI v2 Server — FastAPI Application
═══════════════════════════════════════════════════════════════════

REST API + MCP server for GeoSI's 14-agent pipeline.

Run:
    uvicorn geosi_server.app:app --reload --port 8000

Swagger UI:
    http://localhost:8000/docs

MCP manifest:
    http://localhost:8000/mcp/manifest
"""

import os
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("geosi_server")

# ── Session Pool ────────────────────────────────────────────────────────
_pool = None
_supervisor = None          # process-wide SupervisorAgent (created once)
_startup_time: float = 0.0
_qgis_available: bool = False


def get_pool():
    """Return the global SessionPool, creating it on first call."""
    global _pool
    if _pool is None:
        from geosi_engine.session_pool import SessionPool
        from geosi_server.qgis_runtime import engine_factory, is_available
        factory = engine_factory if is_available() else None
        _pool = SessionPool(factory=factory)
        logger.info("GeoSI SessionPool initialised (QGIS=%s)", is_available())
    return _pool


def get_supervisor():
    """
    Return the process-wide SupervisorAgent.

    The supervisor is created once and reused across requests so that:
    - circuit breakers accumulate failures correctly across sessions
    - approval-pending runs stay alive in the session's engine loop
    """
    global _supervisor
    if _supervisor is None:
        from geosi_engine.agents.supervisor import SupervisorAgent
        _supervisor = SupervisorAgent(get_pool())
        logger.info("Process-wide SupervisorAgent created")
    return _supervisor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup + shutdown."""
    global _startup_time, _qgis_available
    _startup_time = time.monotonic()
    logger.info("GeoSI v2 Server starting…")

    # 1. Headless QGIS (non-fatal if not installed)
    try:
        from geosi_server.qgis_runtime import init as qgis_init
        _qgis_available = qgis_init()
    except Exception as exc:
        logger.warning("QGIS runtime init skipped: %s", exc)
        _qgis_available = False

    # 2. Session pool + supervisor (eager, so the first request is fast)
    get_pool()
    get_supervisor()

    # 3. Neo4j schema — non-blocking
    try:
        from geosi_data.neo4j_client import get_neo4j_client
        neo4j = get_neo4j_client()
        if neo4j.available:
            logger.info("Neo4j connected — schema ensured.")
        else:
            logger.warning("Neo4j unavailable — graph features disabled.")
    except Exception as exc:
        logger.warning("Neo4j init failed (non-fatal): %s", exc)

    # 4. Background graph writer — non-blocking
    try:
        from geosi_engine.graph_writer import GraphWriter
        GraphWriter.get_instance()
        logger.info("Graph writer started.")
    except Exception as exc:
        logger.warning("Graph writer init failed (non-fatal): %s", exc)

    logger.info("GeoSI v2 Server ready (uptime clock started).")
    yield

    # ── Shutdown ────────────────────────────────────────────────────────
    try:
        from geosi_engine.graph_writer import GraphWriter
        GraphWriter.get_instance().stop()
    except Exception:
        logger.debug("suppressed exception", exc_info=True)
    if _pool:
        try:
            _pool.cleanup()
        except Exception as exc:
            logger.warning("Session pool cleanup failed: %s", exc)
    try:
        from geosi_server.qgis_runtime import shutdown as qgis_shutdown
        qgis_shutdown()
    except Exception:
        logger.debug("suppressed exception", exc_info=True)
    logger.info("GeoSI v2 Server shutdown complete.")


# ── Create FastAPI app ─────────────────────────────────────────────────
app = FastAPI(
    title="GeoSI API",
    description=(
        "GeoSI v2 — Autonomous Geospatial Intelligence Platform. "
        "14-agent pipeline: planning, validation, permission, GIS execution, "
        "verification, reporting, GraphRAG, and domain specialists."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────
cors_origins_raw = os.environ.get("GEOSI_ALLOWED_ORIGINS", "")
cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]

if not cors_origins:
    env = os.environ.get("GEOSI_ENV", "development").lower()
    if env == "production":
        raise RuntimeError(
            "GEOSI_ALLOWED_ORIGINS is required in production mode. "
            "Set it to a comma-separated list of allowed origin URLs."
        )
    logger.warning("GEOSI_ALLOWED_ORIGINS not set — defaulting to localhost for dev.")
    cors_origins = ["http://localhost:3000", "http://127.0.0.1:3000",
                    "http://localhost:8000", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Rate-limiting (simple in-process token-bucket; swap out for Redis in prod)
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded

    _limiter = Limiter(key_func=get_remote_address,
                       default_limits=[os.environ.get("GEOSI_RATE_LIMIT", "60/minute")])
    app.state.limiter = _limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("Rate limiting enabled (%s).", os.environ.get("GEOSI_RATE_LIMIT", "60/minute"))
except ImportError:
    logger.debug("slowapi not installed — rate limiting disabled.")

# ── Structured JSON logging ────────────────────────────────────────────
if os.environ.get("GEOSI_JSON_LOGS", "").lower() in {"1", "true", "yes"}:
    try:
        import json_log_formatter
        handler = logging.StreamHandler()
        handler.setFormatter(json_log_formatter.JSONFormatter())
        logging.root.addHandler(handler)
        logger.info("JSON logging enabled.")
    except ImportError:
        logger.debug("json_log_formatter not installed — plain logging.")

# ── Register route modules ─────────────────────────────────────────────
from geosi_server.rag_routes import router as rag_router  # noqa: E402 — registered after app is created
from geosi_server.workflow_routes import router as workflow_router  # noqa: E402 — registered after app is created
from geosi_server.data_routes import router as data_router  # noqa: E402 — registered after app is created
from geosi_server.viz_routes import router as viz_router  # noqa: E402 — registered after app is created
from geosi_server.chat_routes import router as chat_router  # noqa: E402 — registered after app is created
from geosi_server.admin_routes import router as admin_router  # noqa: E402 — registered after app is created
try:
    import multipart  # noqa: F401 — python-multipart; required for file upload
    from geosi_server.workspace_routes import router as workspace_router
    _workspace_router_available = True
except ImportError:
    workspace_router = None  # type: ignore[assignment]
    _workspace_router_available = False
    logger.warning("python-multipart not installed — /workspace/layers upload disabled.")
from geosi_mcp.server import router as mcp_router  # noqa: E402 — registered after app is created

app.include_router(rag_router, prefix="/rag", tags=["RAG"])
app.include_router(workflow_router, prefix="/workflow", tags=["Workflows"])
app.include_router(data_router, prefix="/layers", tags=["Data"])
app.include_router(viz_router, prefix="/viz", tags=["Visualization"])
app.include_router(chat_router, tags=["Chat", "HITL"])          # /chat, /execute, /approval/*
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
if _workspace_router_available:
    app.include_router(workspace_router, tags=["Workspace"])    # /workspace/layers
app.include_router(mcp_router, prefix="/mcp", tags=["MCP"])     # MCP tools

# ── Static web UI ──────────────────────────────────────────────────────
try:
    from fastapi.staticfiles import StaticFiles
    _static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.isdir(_static_dir):
        app.mount("/ui", StaticFiles(directory=_static_dir, html=True), name="ui")
        logger.info("Web chat UI mounted at /ui")
except Exception as exc:
    logger.warning("Web UI mount skipped: %s", exc)


# ── Global endpoints ───────────────────────────────────────────────────
from geosi_server.auth import api_key_auth  # noqa: E402 — registered after app is created


@app.get("/health", tags=["Observability"])
async def health():
    """Public health check — returns circuit-breaker states and pool stats."""
    pool = get_pool()
    pool_stats = pool.stats()
    cb_states = get_supervisor().circuit_breaker_states()

    services: dict = {}

    # PostGIS
    try:
        from geosi_data.database import Database
        services["postgis"] = "ok" if Database().available else "unavailable"
    except Exception as exc:
        services["postgis"] = f"error: {exc}"

    # Qdrant
    services["qdrant"] = "configured" if os.environ.get("QDRANT_URL") else "not_configured"

    # Neo4j
    try:
        from geosi_data.neo4j_client import get_neo4j_client
        services["neo4j"] = get_neo4j_client().circuit_state()
    except Exception as exc:
        services["neo4j"] = f"error: {exc}"

    # Graph writer
    try:
        from geosi_engine.graph_writer import GraphWriter
        services["graph_writer"] = "running" if GraphWriter.get_instance()._running else "stopped"
    except Exception:
        services["graph_writer"] = "unavailable"

    # QGIS headless
    try:
        from geosi_server.qgis_runtime import is_available
        services["qgis"] = "ok" if is_available() else "unavailable"
    except Exception:
        services["qgis"] = "unknown"

    return {
        "status": "ok",
        "version": "2.0.0",
        "session_pool": pool_stats,
        "llm_providers": cb_states,
        "external_services": services,
    }


@app.get("/ready", tags=["Observability"])
async def ready():
    """
    Readiness probe — returns 200 only when the server is ready to serve
    traffic (pool and supervisor exist, QGIS optional).
    """
    pool = get_pool()
    supervisor = get_supervisor()
    if pool is None or supervisor is None:
        from fastapi import Response
        return Response(content="not ready", status_code=503)
    uptime = time.monotonic() - _startup_time if _startup_time else 0.0
    return {"ready": True, "uptime_s": round(uptime, 1)}


@app.get("/metrics", tags=["Observability"])
async def metrics(api_key: str = Depends(api_key_auth)):
    """
    Prometheus-style text metrics (authenticated).

    Returns plain text in exposition format when Prometheus client is
    available, otherwise a JSON summary.
    """
    pool = get_pool()
    stats = pool.stats()
    uptime = time.monotonic() - _startup_time if _startup_time else 0.0

    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        from fastapi.responses import Response
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
    except ImportError:
        logger.debug("suppressed exception", exc_info=True)

    # JSON fallback
    cbs = get_supervisor().circuit_breaker_states()
    return {
        "uptime_seconds": round(uptime, 1),
        "sessions_active": stats.get("active", 0),
        "sessions_total": stats.get("total_created", 0),
        "circuit_breakers": {cb["provider"]: cb["state"] for cb in cbs},
    }


@app.get("/stats", tags=["Observability"])
async def stats_endpoint(api_key: str = Depends(api_key_auth)):
    """Get knowledge-base statistics (authenticated)."""
    engine = get_pool().get_or_create(api_key)
    return engine.get_knowledge_stats()
