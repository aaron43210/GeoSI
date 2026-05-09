# -*- coding: utf-8 -*-
"""
GeoSI Server Entry Point

Creates the FastAPI application and wires up the GeoSI routes. Runs
standalone (outside QGIS) so the same parser / planner / executor can
be reached over HTTP by the QGIS plugin or any other client.
"""

import os
from typing import Dict

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from geosi_server.app.api.routes import router
from geosi_server.app.core.config import settings


# --- Security -------------------------------------------------------------
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

DEV_MODE = os.environ.get("GEOSI_DEV_MODE", "true").lower() in {"1", "true", "yes"}
MASTER_KEY = os.environ.get("GEOSI_MASTER_KEY", "geosi_secret_123")


async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if DEV_MODE:
        return "guest"
    if api_key_header and api_key_header == MASTER_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )


# --- Application ----------------------------------------------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router, prefix="/api", dependencies=[Depends(get_api_key)]
)
app.include_router(
    router, prefix="/api/v1", dependencies=[Depends(get_api_key)]
)


@app.get("/", tags=["system"])
def root() -> Dict[str, str]:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/health", tags=["system"])
def root_health() -> Dict[str, str]:
    """Unauthenticated liveness probe (outside the /api prefix)."""
    return {"status": "ok", "version": settings.app_version}
