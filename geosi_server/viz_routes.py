# -*- coding: utf-8 -*-
"""
GeoSI v2 — Visualization Routes (map/3D data source for the web console)
════════════════════════════════════════════════════════════════════
Serves the *live, in-session* working layers (``engine.state.layers``) to the
browser so the map/3D panel renders exactly what the agent produced — not a
copy, not a mock. Vector layers become WGS84 GeoJSON ``FeatureCollection``s;
raster layers become a WGS84 bounding box plus an optional downsampled PNG
overlay.

Every endpoint is Bearer-authed (same contract as ``/chat``) and session
scoped: ``session_id`` falls back to the API key, matching ``chat_routes``.

Degrade-safe by design: if GeoPandas / rasterio / matplotlib are absent, the
endpoints return a clear, structured error instead of raising — the UI simply
shows "geometry unavailable" rather than breaking.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from geosi_server.auth import api_key_auth

logger = logging.getLogger("geosi_server.viz")
router = APIRouter()

# A hard cap so a pathological layer can never stream millions of features
# into a browser tab and wedge it.
_MAX_FEATURES = 50_000
_MAX_RASTER_PX = 1024


# ── Models ─────────────────────────────────────────────────────────────

class VizLayer(BaseModel):
    name: str
    layer_type: str = "vector"          # "vector" | "raster"
    geometry_type: str = "Unknown"
    crs: str = "EPSG:4326"
    feature_count: int = 0
    bounds_wgs84: Optional[List[float]] = None   # [minLng, minLat, maxLng, maxLat]
    fields: List[str] = []


class VizLayerList(BaseModel):
    layers: List[VizLayer]


# ── Helpers ────────────────────────────────────────────────────────────

def _engine(api_key: str, session_id: Optional[str]):
    from geosi_server.app import get_pool
    return get_pool().get_or_create(session_id or api_key)


def _session_layers(engine) -> Dict[str, Any]:
    state = getattr(engine, "state", None)
    return dict(getattr(state, "layers", {}) or {})


def _load_gdf(layer):
    """Return a GeoDataFrame for *layer*, loading from disk if needed.

    Raises ``RuntimeError`` with a human-readable reason when geometry cannot
    be produced (missing geopandas, no features, unreadable file).
    """
    import importlib.util
    if importlib.util.find_spec("geopandas") is None:  # pragma: no cover
        raise RuntimeError("geopandas not available")

    gdf = getattr(layer, "features", None)
    if gdf is None:
        fp = getattr(layer, "filepath", "") or ""
        if not fp:
            raise RuntimeError("layer has no in-memory features and no filepath")
        import geopandas
        gdf = geopandas.read_file(fp)
    return gdf


def _to_wgs84(gdf, declared_crs: str):
    """Reproject *gdf* to EPSG:4326, assuming *declared_crs* when unset."""
    if gdf.crs is None and declared_crs:
        try:
            gdf = gdf.set_crs(declared_crs, allow_override=True)
        except Exception:
            logger.debug("suppressed exception", exc_info=True)
    try:
        if gdf.crs is not None:
            gdf = gdf.to_crs(4326)
    except Exception as exc:
        logger.debug("Reprojection to WGS84 failed: %s", exc)
    return gdf


def _bounds_wgs84(layer) -> Optional[List[float]]:
    """Best-effort WGS84 [minLng, minLat, maxLng, maxLat] for a layer."""
    # Vector: derive from the (reprojected) geometry.
    if getattr(layer, "layer_type", "vector") == "vector":
        try:
            gdf = _to_wgs84(_load_gdf(layer), getattr(layer, "crs", ""))
            minx, miny, maxx, maxy = gdf.total_bounds
            return [float(minx), float(miny), float(maxx), float(maxy)]
        except Exception:
            return None
    # Raster: transform the native bounds dict if present.
    b = getattr(layer, "bounds", {}) or {}
    if {"xmin", "ymin", "xmax", "ymax"} <= set(b):
        try:
            from pyproj import Transformer
            src = getattr(layer, "crs", "") or "EPSG:4326"
            tf = Transformer.from_crs(src, "EPSG:4326", always_xy=True)
            minx, miny = tf.transform(b["xmin"], b["ymin"])
            maxx, maxy = tf.transform(b["xmax"], b["ymax"])
            return [float(minx), float(miny), float(maxx), float(maxy)]
        except Exception:
            return [float(b["xmin"]), float(b["ymin"]),
                    float(b["xmax"]), float(b["ymax"])]
    return None


# ── Endpoints ──────────────────────────────────────────────────────────

@router.get("/layers", response_model=VizLayerList, tags=["Visualization"])
async def list_viz_layers(
    api_key: str = Depends(api_key_auth),
    session_id: Optional[str] = Query(None),
):
    """List the live working layers for a session (what the map should draw)."""
    engine = _engine(api_key, session_id)
    out: List[VizLayer] = []
    for name, layer in _session_layers(engine).items():
        out.append(VizLayer(
            name=name,
            layer_type=getattr(layer, "layer_type", "vector"),
            geometry_type=getattr(layer, "geometry_type", "Unknown"),
            crs=getattr(layer, "crs", "EPSG:4326"),
            feature_count=int(getattr(layer, "feature_count", 0) or 0),
            bounds_wgs84=_bounds_wgs84(layer),
            fields=list(getattr(layer, "fields", []) or []),
        ))
    return VizLayerList(layers=out)


@router.get("/layers/{name}/geojson", tags=["Visualization"])
async def layer_geojson(
    name: str,
    api_key: str = Depends(api_key_auth),
    session_id: Optional[str] = Query(None),
    limit: int = Query(_MAX_FEATURES, ge=1, le=_MAX_FEATURES),
    simplify: float = Query(0.0, ge=0.0, description="Tolerance in degrees; 0 = none"),
):
    """Return a WGS84 GeoJSON ``FeatureCollection`` for a vector layer."""
    engine = _engine(api_key, session_id)
    layer = _session_layers(engine).get(name)
    if layer is None:
        raise HTTPException(status_code=404, detail=f"Layer {name!r} not in session")
    if getattr(layer, "layer_type", "vector") == "raster":
        raise HTTPException(status_code=400, detail="Raster layer — use /raster")

    try:
        gdf = _to_wgs84(_load_gdf(layer), getattr(layer, "crs", ""))
    except RuntimeError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    if len(gdf) > limit:
        gdf = gdf.iloc[:limit]
    if simplify > 0:
        try:
            gdf = gdf.copy()
            gdf["geometry"] = gdf.geometry.simplify(simplify, preserve_topology=True)
        except Exception as exc:
            logger.debug("Simplify skipped: %s", exc)

    import json
    fc = json.loads(gdf.to_json())
    fc["_meta"] = {
        "name": name,
        "returned": len(gdf),
        "geometry_type": getattr(layer, "geometry_type", "Unknown"),
        "truncated": int(getattr(layer, "feature_count", len(gdf)) or 0) > len(gdf),
    }
    return fc


@router.get("/layers/{name}/raster", tags=["Visualization"])
async def layer_raster(
    name: str,
    api_key: str = Depends(api_key_auth),
    session_id: Optional[str] = Query(None),
):
    """Return WGS84 bounds + an optional downsampled PNG overlay for a raster."""
    engine = _engine(api_key, session_id)
    layer = _session_layers(engine).get(name)
    if layer is None:
        raise HTTPException(status_code=404, detail=f"Layer {name!r} not in session")
    if getattr(layer, "layer_type", "vector") != "raster":
        raise HTTPException(status_code=400, detail="Vector layer — use /geojson")

    bounds = _bounds_wgs84(layer)
    image = _render_raster_png(layer)
    return {
        "name": name,
        "bounds_wgs84": bounds,
        "image": image,            # data: URL or None
        "crs": getattr(layer, "crs", "EPSG:4326"),
    }


# ── Raster rendering (fully guarded; None on any missing dependency) ────

def _render_raster_png(layer) -> Optional[str]:
    """Downsample a raster to a PNG ``data:`` URL. Returns None if impossible.

    Single-band → viridis colormap; 3+ band → RGB composite. Pure best-effort:
    any missing dependency (numpy / PIL / rasterio) yields None so the UI falls
    back to drawing just the footprint box.
    """
    try:
        import numpy as np
        from PIL import Image
        import base64
        import io
    except Exception as exc:  # pragma: no cover - env without numpy/PIL
        logger.debug("Raster PNG skipped (no numpy/PIL): %s", exc)
        return None

    arr = getattr(layer, "raster", None)
    try:
        if arr is None:
            fp = getattr(layer, "filepath", "") or ""
            if not fp:
                return None
            import rasterio
            with rasterio.open(fp) as ds:
                count = min(ds.count, 3)
                arr = ds.read(list(range(1, count + 1)))  # (bands, h, w)
        arr = np.asarray(arr)
        if arr.ndim == 2:
            arr = arr[np.newaxis, ...]

        # Downsample to keep the overlay light.
        _, h, w = arr.shape
        scale = max(1, int(max(h, w) / _MAX_RASTER_PX))
        if scale > 1:
            arr = arr[:, ::scale, ::scale]

        if arr.shape[0] >= 3:
            rgb = np.transpose(arr[:3], (1, 2, 0)).astype("float64")
            for c in range(3):
                band = rgb[..., c]
                lo, hi = np.nanpercentile(band, [2, 98])
                rgb[..., c] = np.clip((band - lo) / (hi - lo + 1e-9), 0, 1) * 255
            img = Image.fromarray(rgb.astype("uint8"), mode="RGB")
        else:
            band = arr[0].astype("float64")
            lo, hi = np.nanpercentile(band, [2, 98])
            norm = np.clip((band - lo) / (hi - lo + 1e-9), 0, 1)
            try:
                from matplotlib import cm
                rgba = (cm.get_cmap("viridis")(norm) * 255).astype("uint8")
                img = Image.fromarray(rgba, mode="RGBA")
            except Exception:
                gray = (norm * 255).astype("uint8")
                img = Image.fromarray(gray, mode="L")

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/png;base64,{b64}"
    except Exception as exc:
        logger.debug("Raster PNG render failed for %s: %s",
                     getattr(layer, "name", "?"), exc)
        return None
