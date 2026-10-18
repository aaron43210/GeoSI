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
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("geosi_server")

# ── Session Pool (Phase 1.1) ───────────────────────────────────────────
_pool = None

def get_pool():
    """Get the global GeoSI SessionPool instance."""
    global _pool
    if _pool is None:
        from geosi_engine.session_pool import SessionPool
        _pool = SessionPool()
        logger.info("GeoSI SessionPool initialized")
    return _pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup + shutdown."""
    logger.info("GeoSI v2 Server starting...")

    # Init session pool
    get_pool()

    # Ensure Neo4j schema (P9) — non-blocking, graceful fail
    try:
        from geosi_data.neo4j_client import get_neo4j_client
        neo4j = get_neo4j_client()
        if neo4j.available:
            logger.info("Neo4j connected — schema ensured.")
        else:
            logger.warning("Neo4j unavailable — graph features disabled.")
    except Exception as exc:
        logger.warning("Neo4j init failed (non-fatal): %s", exc)

    # Start background graph writer (P9) — daemon thread
    try:
        from geosi_engine.graph_writer import GraphWriter
        GraphWriter.get_instance()
        logger.info("Graph writer started.")
    except Exception as exc:
        logger.warning("Graph writer init failed (non-fatal): %s", exc)

    logger.info("GeoSI v2 Server ready.")
    yield

    # Shutdown
    try:
        from geosi_engine.graph_writer import GraphWriter
        GraphWriter.get_instance().stop()
    except Exception:
        pass
    if _pool:
        try:
            _pool.cleanup()
        except Exception as exc:
            logger.warning("Session pool cleanup failed: %s", exc)
    logger.info("GeoSI v2 Server shutdown complete.")


# ── Create FastAPI app ─────────────────────────────────────────────────
app = FastAPI(
    title="GeoSI API",
    description=(
        "GeoSI v2 — Autonomous Geospatial Intelligence Platform. "
        "Provides RAG-powered GIS knowledge retrieval, workflow search, "
        "and spatial data management."
    ),
    version="2.0.0-dev",
    lifespan=lifespan,
)

# ── CORS (G2 fix: remove wildcard) ─────────────────────────────────────
cors_origins_raw = os.environ.get("GEOSI_ALLOWED_ORIGINS", "")
cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]

if not cors_origins:
    env = os.environ.get("GEOSI_ENV", "development").lower()
    if env == "production":
        raise RuntimeError(
            "GEOSI_ALLOWED_ORIGINS is required in production mode. "
            "Set it to a comma-separated list of allowed origin URLs."
        )
    logger.warning(
        "GEOSI_ALLOWED_ORIGINS not set. Defaulting to localhost "
        "for development mode."
    )
    cors_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register route modules ────────────────────────────────────────────
from geosi_server.rag_routes import router as rag_router
from geosi_server.workflow_routes import router as workflow_router
from geosi_server.data_routes import router as data_router
from geosi_server.viz_routes import router as viz_router
from geosi_server.chat_routes import router as chat_router
from geosi_server.admin_routes import router as admin_router
from geosi_mcp.server import router as mcp_router

app.include_router(rag_router, prefix="/rag", tags=["RAG"])
app.include_router(workflow_router, prefix="/workflow", tags=["Workflows"])
app.include_router(data_router, prefix="/layers", tags=["Data"])
app.include_router(viz_router, prefix="/viz", tags=["Visualization"])  # map/3D data source
app.include_router(chat_router, tags=["Chat", "HITL"])      # /chat, /execute, /approval/*
app.include_router(admin_router, prefix="/admin", tags=["Admin"])  # /admin/policy
app.include_router(mcp_router, prefix="/mcp", tags=["MCP"])  # FR-5.1 MCP tools


# ── Same-origin web chat UI (Part E) ───────────────────────────────────
# Served from the API origin so the browser's Bearer key never crosses an
# origin boundary — no CORS relaxation, /chat stays Bearer-authed.
try:
    from fastapi.staticfiles import StaticFiles
    _static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.isdir(_static_dir):
        app.mount("/ui", StaticFiles(directory=_static_dir, html=True), name="ui")
        logger.info("Web chat UI mounted at /ui")
except Exception as exc:  # non-fatal — API works without the UI
    logger.warning("Web UI mount skipped: %s", exc)


# ── Global endpoints ───────────────────────────────────────────────────
from geosi_server.auth import api_key_auth

@app.get("/health", tags=["Observability"])
async def health():
    """
    Health check endpoint (public).

    Returns per-agent circuit-breaker state and session-pool stats
    as required by PRD §8 Observability and §2 Goal 8.
    """
    pool = get_pool()
    pool_stats = pool.stats()

    # Circuit breaker states from a shared Supervisor instance
    # (breakers are per-process, not per-session, so we can read from any instance)
    try:
        from geosi_engine.agents.supervisor import SupervisorAgent
        _sv = SupervisorAgent(pool)
        cb_states = _sv.circuit_breaker_states()
    except Exception:
        cb_states = []

    # Check external service connectivity (non-blocking best-effort)
    services: dict = {}

    # PostGIS
    try:
        from geosi_data.database import Database
        db = Database()
        services["postgis"] = "ok" if db.available else "unavailable"
    except Exception as e:
        services["postgis"] = f"error: {e}"

    # Qdrant
    try:
        qdrant_url = os.environ.get("QDRANT_URL", "")
        services["qdrant"] = "configured" if qdrant_url else "not_configured"
    except Exception:
        services["qdrant"] = "unknown"

    # Neo4j (P9)
    try:
        from geosi_data.neo4j_client import get_neo4j_client
        neo4j = get_neo4j_client()
        services["neo4j"] = neo4j.circuit_state()
    except Exception as exc:
        services["neo4j"] = f"error: {exc}"

    # Graph writer queue (P9)
    try:
        from geosi_engine.graph_writer import GraphWriter
        gw = GraphWriter.get_instance()
        services["graph_writer"] = "running" if gw._running else "stopped"
    except Exception:
        services["graph_writer"] = "unavailable"

    return {
        "status": "ok",
        "version": "2.0.0",
        "session_pool": pool_stats,
        "llm_providers": cb_states,
        "external_services": services,
    }


@app.get("/stats", tags=["Observability"])
async def stats(api_key: str = Depends(api_key_auth)):
    """Get knowledge base statistics (authenticated)."""
    engine = get_pool().get_or_create(api_key)
    return engine.get_knowledge_stats()

