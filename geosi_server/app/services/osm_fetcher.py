# -*- coding: utf-8 -*-
"""
GeoSI Server - OSM auto-fetch (server/CLI path only)

Logic: when the agent references a layer by a recognizable name
(for example "hospitals", "roads", "rivers") and that layer is not
already present in the workspace, the API may fetch it from
OpenStreetMap via the Overpass API as a convenience.

This module is intentionally isolated:
  - The QGIS plugin never imports it (it only works from the
    active QGIS layer panel).
  - The engine never imports it (the engine is framework-free).
Only the server tool service calls it.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple

import requests

from geosi_engine.models import Layer

logger = logging.getLogger("geosi_server.osm_fetcher")


# Keyword -> Overpass `[key=value]` filter. Extend as needed.
OSM_TAG_MAP: Dict[str, Tuple[str, str]] = {
    "hospital": ("amenity", "hospital"),
    "hospitals": ("amenity", "hospital"),
    "school": ("amenity", "school"),
    "schools": ("amenity", "school"),
    "park": ("leisure", "park"),
    "parks": ("leisure", "park"),
    "restaurant": ("amenity", "restaurant"),
    "restaurants": ("amenity", "restaurant"),
    "river": ("waterway", "river"),
    "rivers": ("waterway", "river"),
    "road": ("highway", "*"),
    "roads": ("highway", "*"),
    "building": ("building", "*"),
    "buildings": ("building", "*"),
    "forest": ("landuse", "forest"),
    "forests": ("landuse", "forest"),
    "bus_stop": ("highway", "bus_stop"),
    "railway": ("railway", "rail"),
    "bank": ("amenity", "bank"),
    "atm": ("amenity", "atm"),
    "pharmacy": ("amenity", "pharmacy"),
    "police": ("amenity", "police"),
}

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Default bbox: south, west, north, east (Kerala, India). Override per call.
DEFAULT_BBOX = (8.2, 74.85, 12.8, 77.5)


def can_fetch(layer_name: str) -> bool:
    """Return True if we know how to map this layer name to an OSM tag."""
    return layer_name.lower().strip() in OSM_TAG_MAP


def fetch_layer(
    layer_name: str,
    bbox: Optional[Tuple[float, float, float, float]] = None,
    timeout: int = 60,
) -> Optional[Layer]:
    """
    Fetch a named layer from OpenStreetMap and return it as a Layer.

    Returns None if the name is not in OSM_TAG_MAP or the fetch fails.
    """
    key_name = layer_name.lower().strip()
    if key_name not in OSM_TAG_MAP:
        return None

    tag_key, tag_val = OSM_TAG_MAP[key_name]
    south, west, north, east = bbox or DEFAULT_BBOX

    if tag_val == "*":
        selector = f'["{tag_key}"]'
    else:
        selector = f'["{tag_key}"="{tag_val}"]'

    query = (
        f"[out:json][timeout:{timeout}];"
        f"("
        f"  node{selector}({south},{west},{north},{east});"
        f"  way{selector}({south},{west},{north},{east});"
        f"  relation{selector}({south},{west},{north},{east});"
        f");"
        f"out geom;"
    )

    try:
        resp = requests.post(
            OVERPASS_URL,
            data={"data": query},
            timeout=timeout + 10,
        )
        resp.raise_for_status()
    except Exception as e:
        logger.warning(f"OSM fetch failed for '{layer_name}': {e}")
        return None

    try:
        import geopandas as gpd
        from shapely.geometry import LineString, Point, Polygon

        payload = resp.json()
        rows: List[dict] = []
        geoms = []
        for el in payload.get("elements", []):
            etype = el.get("type")
            if etype == "node":
                geom = Point(el["lon"], el["lat"])
            elif etype == "way" and el.get("geometry"):
                coords = [(g["lon"], g["lat"]) for g in el["geometry"]]
                if len(coords) >= 3 and coords[0] == coords[-1]:
                    geom = Polygon(coords)
                elif len(coords) >= 2:
                    geom = LineString(coords)
                else:
                    continue
            else:
                continue
            row = {"osm_id": el.get("id"), "osm_type": etype}
            row.update(el.get("tags", {}) or {})
            rows.append(row)
            geoms.append(geom)

        if not rows:
            return None

        gdf = gpd.GeoDataFrame(rows, geometry=geoms, crs="EPSG:4326")
        try:
            _ = gdf.sindex
        except Exception:
            pass

        geom_type = str(gdf.geometry.iloc[0].geom_type) if len(gdf) else "Unknown"
        return Layer(
            name=layer_name,
            layer_type="vector",
            geometry_type=geom_type,
            feature_count=len(gdf),
            crs="EPSG:4326",
            filepath=f"osm://{tag_key}={tag_val}",
            features=gdf,
        )
    except Exception as e:
        logger.warning(f"OSM parse failed for '{layer_name}': {e}")
        return None
