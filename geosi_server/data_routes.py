# -*- coding: utf-8 -*-
"""
GeoSI Server — Data Routes
═══════════════════════════════════════════════════════════════════

Endpoints:
    GET    /layers           — List all layers
    GET    /layers/{name}    — Get layer details
    DELETE /layers/{name}    — Delete a layer
    GET    /projects         — List all projects
    POST   /projects         — Create/update a project
"""

import logging
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from geosi_server.auth import api_key_auth, admin_auth
from pydantic import Field

logger = logging.getLogger("geosi_server.data")
router = APIRouter()


# ── Request/Response models ────────────────────────────────────────────

class LayerInfo(BaseModel):
    id: Optional[str] = None
    name: str
    geometry_type: str = "Unknown"
    crs: str = "EPSG:4326"
    feature_count: int = 0
    layer_type: str = "vector"
    table_name: Optional[str] = None
    filepath: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None


class LayerListResponse(BaseModel):
    layers: List[LayerInfo]


class ProjectInfo(BaseModel):
    id: Optional[str] = None
    name: str
    description: str = ""
    crs: str = "EPSG:4326"
    layer_names: List[str] = []
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None


class ProjectListResponse(BaseModel):
    projects: List[ProjectInfo]


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field("", description="Project description")
    crs: str = Field("EPSG:4326", description="Project CRS")
    layer_names: List[str] = Field(default_factory=list, description="Layer names")


# ── Layer Endpoints ────────────────────────────────────────────────────

@router.get("", response_model=LayerListResponse)
async def list_layers(api_key: str = Depends(api_key_auth)):
    """List all available spatial layers."""
    from geosi_server.app import get_pool
    engine = get_pool().get_or_create(api_key)

    if not engine.data:
        return {"layers": []}
    layers = engine.data["layers"].list_all()
    return {"layers": [LayerInfo(**layer) for layer in layers]}


# ── Project Endpoints ──────────────────────────────────────────────────
# NOTE: these literal "/projects" routes MUST be declared before the
# parameterized "/{name}" layer routes below. FastAPI/Starlette matches in
# registration order, so if "/{name}" came first a GET /layers/projects would
# be captured as a layer named "projects" and these endpoints would be dead.

@router.get("/projects", response_model=ProjectListResponse)
async def list_projects(api_key: str = Depends(api_key_auth)):
    """List all GIS projects."""
    from geosi_server.app import get_pool
    engine = get_pool().get_or_create(api_key)

    if not engine.data:
        return {"projects": []}
    projects = engine.data["projects"].list_projects()
    return {"projects": [ProjectInfo(**p) for p in projects]}


@router.post("/projects", response_model=ProjectInfo)
async def create_project(req: ProjectCreateRequest, api_key: str = Depends(api_key_auth)):
    """Create a new GIS project."""
    from geosi_server.app import get_pool
    engine = get_pool().get_or_create(api_key)

    if not engine.data:
        raise HTTPException(status_code=503, detail="PostGIS not available")

    project_id = engine.data["projects"].save_project(
        name=req.name,
        description=req.description,
        crs=req.crs,
        layer_names=req.layer_names,
    )

    if not project_id:
        raise HTTPException(status_code=500, detail="Failed to create project")

    project = engine.data["projects"].load_project(req.name)
    return ProjectInfo(**project)


@router.get("/{name}", response_model=LayerInfo)
async def get_layer(name: str, api_key: str = Depends(api_key_auth)):
    """Get metadata for a specific layer."""
    from geosi_server.app import get_pool
    engine = get_pool().get_or_create(api_key)

    if not engine.data:
        raise HTTPException(status_code=503, detail="PostGIS not available")
    layer = engine.data["layers"].get_by_name(name)
    if not layer:
        raise HTTPException(status_code=404, detail=f"Layer {name} not found")
    return layer


@router.delete("/{name}")
async def delete_layer(name: str, api_key: str = Depends(admin_auth)):
    """Delete a spatial layer from the database (admin only)."""
    from geosi_server.app import get_pool
    engine = get_pool().get_or_create(api_key)

    if not engine.data:
        raise HTTPException(status_code=503, detail="PostGIS not available")

    # Delete metadata
    deleted_meta = engine.data["layers"].delete(name)

    # Delete PostGIS table
    # Simple sanitization inline (or we can assume postgis_manager allow-list handles it)
    table_name = f"geosi_lyr_{name.lower().replace(' ', '_')}"
    deleted_table = engine.data["postgis"].delete_layer(table_name)

    if not deleted_meta and not deleted_table:
        raise HTTPException(status_code=404, detail=f"Failed to delete {name}")
    return {"status": "deleted", "layer": name}

