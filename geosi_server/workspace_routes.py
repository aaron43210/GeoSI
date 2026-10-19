# -*- coding: utf-8 -*-
"""
GeoSI Server — Workspace Layer Routes
═══════════════════════════════════════════════════════════════════════
Manage the file-system workspace for a session's uploaded layers.

    POST   /workspace/layers          — upload a vector/raster file
                                        (GeoJSON, GeoTIFF, zipped shapefile)
    GET    /workspace/layers          — list uploaded layer files
    GET    /workspace/layers/{name}   — download a layer file
    DELETE /workspace/layers/{name}   — delete a layer file
    POST   /workspace/layers/{name}/load — load an uploaded file into the
                                           session's engine state

All endpoints require Bearer auth.  ``session_id`` defaults to the API key.
"""
from __future__ import annotations

import logging
import os
import shutil
import zipfile
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from geosi_server.auth import api_key_auth

logger = logging.getLogger("geosi_server.workspace")
router = APIRouter()

_ALLOWED_EXTS = {
    ".geojson", ".json",
    ".tif", ".tiff",
    ".gpkg",
    ".zip",   # shapefile bundle
    ".csv",
    ".kml", ".kmz",
    ".fgb",   # FlatGeobuf
}
_MAX_UPLOAD_MB = int(os.environ.get("GEOSI_MAX_UPLOAD_MB", "200"))


# ── Models ─────────────────────────────────────────────────────────────

class WorkspaceFile(BaseModel):
    name: str
    size_bytes: int
    path: str


class WorkspaceList(BaseModel):
    session_id: str
    files: List[WorkspaceFile]


class LoadResult(BaseModel):
    success: bool
    name: str
    message: str


# ── Helpers ────────────────────────────────────────────────────────────

def _workspace(session_id: str) -> Path:
    from geosi_server.qgis_runtime import session_workspace
    return session_workspace(session_id)


def _engine(api_key: str, session_id: Optional[str]):
    from geosi_server.app import get_pool
    return get_pool().get_or_create(session_id or api_key)


def _safe_name(filename: str) -> str:
    """Strip path components and replace unsafe chars."""
    base = Path(filename).name
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in base)


def _unzip_shapefile(zip_path: Path, dest_dir: Path) -> Path:
    """Unzip a shapefile bundle into *dest_dir*, return path to the .shp."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest_dir)
    shps = list(dest_dir.rglob("*.shp"))
    if not shps:
        raise ValueError("Zip does not contain a .shp file")
    return shps[0]


# ── Endpoints ─────────────────────────────────────────────────────────

@router.post(
    "/workspace/layers",
    response_model=WorkspaceFile,
    status_code=status.HTTP_201_CREATED,
    tags=["Workspace"],
)
async def upload_layer(
    file: UploadFile = File(..., description="Vector or raster file to upload"),
    api_key: str = Depends(api_key_auth),
    session_id: Optional[str] = Query(None),
):
    """
    Upload a spatial file into the session workspace.

    Supported formats: GeoJSON, GeoTIFF, GeoPackage, FlatGeobuf, CSV,
    KML/KMZ, and zipped shapefiles (.zip containing .shp).

    Zip bundles are extracted automatically; the shapefile path is
    stored for subsequent ``/load`` calls.
    """
    sid = session_id or api_key
    ws = _workspace(sid)

    # Validate filename / extension
    safe = _safe_name(file.filename or "upload")
    ext = Path(safe).suffix.lower()
    if ext not in _ALLOWED_EXTS:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type {ext!r}. Allowed: {sorted(_ALLOWED_EXTS)}",
        )

    dest = ws / safe
    content = await file.read()

    # Size guard
    if len(content) > _MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {_MAX_UPLOAD_MB} MB upload limit.",
        )

    dest.write_bytes(content)
    logger.info("Uploaded %s (%d bytes) → %s", safe, len(content), dest)

    # Handle zipped shapefiles: extract and point at the .shp
    if ext == ".zip":
        extract_dir = ws / (Path(safe).stem + "_shp")
        extract_dir.mkdir(exist_ok=True)
        try:
            shp = _unzip_shapefile(dest, extract_dir)
            dest.unlink()          # remove the .zip
            dest = shp
            safe = shp.name
        except Exception as exc:
            dest.unlink(missing_ok=True)
            shutil.rmtree(extract_dir, ignore_errors=True)
            raise HTTPException(status_code=422, detail=f"Zip extraction failed: {exc}")

    return WorkspaceFile(name=safe, size_bytes=dest.stat().st_size, path=str(dest))


@router.get("/workspace/layers", response_model=WorkspaceList, tags=["Workspace"])
async def list_workspace_layers(
    api_key: str = Depends(api_key_auth),
    session_id: Optional[str] = Query(None),
):
    """List files currently in the session workspace."""
    sid = session_id or api_key
    ws = _workspace(sid)
    files = []
    for p in sorted(ws.iterdir()):
        if p.is_file() and p.suffix.lower() in _ALLOWED_EXTS | {".shp", ".dbf", ".prj", ".shx"}:
            files.append(WorkspaceFile(name=p.name, size_bytes=p.stat().st_size, path=str(p)))
    return WorkspaceList(session_id=sid, files=files)


@router.get("/workspace/layers/{name}", tags=["Workspace"])
async def download_layer(
    name: str,
    api_key: str = Depends(api_key_auth),
    session_id: Optional[str] = Query(None),
):
    """Download a file from the session workspace."""
    sid = session_id or api_key
    ws = _workspace(sid)
    safe = _safe_name(name)
    dest = ws / safe
    if not dest.exists() or not dest.is_file():
        raise HTTPException(status_code=404, detail=f"{name!r} not found in workspace")
    return FileResponse(str(dest), filename=safe)


@router.delete(
    "/workspace/layers/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Workspace"],
)
async def delete_workspace_layer(
    name: str,
    api_key: str = Depends(api_key_auth),
    session_id: Optional[str] = Query(None),
):
    """Delete a file from the session workspace."""
    sid = session_id or api_key
    ws = _workspace(sid)
    safe = _safe_name(name)
    dest = ws / safe
    if not dest.exists():
        raise HTTPException(status_code=404, detail=f"{name!r} not found in workspace")
    dest.unlink()
    logger.info("Deleted workspace file: %s (session %s)", safe, sid)


@router.post(
    "/workspace/layers/{name}/load",
    response_model=LoadResult,
    tags=["Workspace"],
)
async def load_workspace_layer(
    name: str,
    api_key: str = Depends(api_key_auth),
    session_id: Optional[str] = Query(None),
):
    """
    Load a workspace file into the session's engine state so the agent
    can reference it by name in subsequent queries.

    The layer name is derived from the filename stem.
    """
    sid = session_id or api_key
    ws = _workspace(sid)
    safe = _safe_name(name)

    # Accept both plain name and name with extension
    candidates = [ws / safe] + [ws / (Path(safe).stem + ext) for ext in _ALLOWED_EXTS | {".shp"}]
    dest = next((p for p in candidates if p.exists() and p.is_file()), None)
    if dest is None:
        raise HTTPException(status_code=404, detail=f"{name!r} not found in workspace")

    engine = _engine(api_key, session_id)
    layer_name = dest.stem.replace("-", "_")

    try:
        from geosi_engine.models import Layer
        layer = Layer(
            name=layer_name,
            filepath=str(dest),
            layer_type="raster" if dest.suffix.lower() in {".tif", ".tiff"} else "vector",
            geometry_type="Unknown",
            feature_count=0,
        )
        # Try to populate feature count from geopandas (non-fatal)
        if layer.layer_type == "vector":
            try:
                import geopandas as gpd
                gdf = gpd.read_file(str(dest))
                layer.feature_count = len(gdf)
                geom_types = gdf.geom_type.dropna().unique().tolist()
                if geom_types:
                    layer.geometry_type = geom_types[0]
            except Exception:
                logger.debug("suppressed exception", exc_info=True)
        engine.state.add_layer(layer)
        logger.info("Loaded workspace layer %s (%s) into session %s", layer_name, dest, sid)
        return LoadResult(
            success=True,
            name=layer_name,
            message=f"Layer '{layer_name}' loaded from {dest.name} ({layer.feature_count} features).",
        )
    except Exception as exc:
        logger.error("Failed to load workspace layer %s: %s", name, exc)
        raise HTTPException(status_code=500, detail=str(exc))
