"""
GeoSI — OpenStreetMap Overpass Extractor
═══════════════════════════════════════════════════════════════════════
Fetch OpenStreetMap features by category and location (or QGIS canvas
extent) directly from the Overpass API and return them as an in-memory
QGIS vector layer.

Usage:
    from geosi_data.osm import fetch_osm_features
    layer = fetch_osm_features("hospitals", "London")
    layer = fetch_osm_features("buildings", bbox=(xmin, ymin, xmax, ymax))
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("geosi_data.osm")

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# ── Tag presets ───────────────────────────────────────────────────────
# Maps natural-language categories to Overpass tag filters
TAG_PRESETS: Dict[str, List[Dict[str, str]]] = {
    "hospitals": [{"amenity": "hospital"}],
    "clinics": [{"amenity": "clinic"}, {"amenity": "doctors"}],
    "schools": [{"amenity": "school"}],
    "universities": [{"amenity": "university"}],
    "pharmacies": [{"amenity": "pharmacy"}],
    "restaurants": [{"amenity": "restaurant"}],
    "cafes": [{"amenity": "cafe"}],
    "banks": [{"amenity": "bank"}],
    "atms": [{"amenity": "atm"}],
    "parking": [{"amenity": "parking"}],
    "parks": [{"leisure": "park"}],
    "playgrounds": [{"leisure": "playground"}],
    "sports": [{"leisure": "sports_centre"}, {"leisure": "stadium"}],
    "hotels": [{"tourism": "hotel"}],
    "tourist": [{"tourism": "attraction"}],
    "museums": [{"tourism": "museum"}],
    "buildings": [{"building": "yes"}],
    "roads": [{"highway": "primary"}, {"highway": "secondary"}, {"highway": "residential"}],
    "motorways": [{"highway": "motorway"}],
    "railways": [{"railway": "rail"}],
    "waterways": [{"waterway": "river"}, {"waterway": "stream"}],
    "water": [{"natural": "water"}],
    "forests": [{"landuse": "forest"}, {"natural": "wood"}],
    "residential": [{"landuse": "residential"}],
    "industrial": [{"landuse": "industrial"}],
    "fire_stations": [{"amenity": "fire_station"}],
    "police": [{"amenity": "police"}],
    "post_offices": [{"amenity": "post_office"}],
    "bus_stops": [{"highway": "bus_stop"}, {"public_transport": "stop_position"}],
    "supermarkets": [{"shop": "supermarket"}],
    "fuel": [{"amenity": "fuel"}],
    "charging": [{"amenity": "charging_station"}],
}


def resolve_category(name: str) -> Optional[List[Dict[str, str]]]:
    """Fuzzy-match a natural-language category to tag presets."""
    nl = name.lower().strip().rstrip("s")  # simple stemming
    for key, tags in TAG_PRESETS.items():
        if nl in key or key in nl:
            return tags
    return None


def geocode_bbox(place: str, padding_deg: float = 0.05) -> Optional[Tuple[float, float, float, float]]:
    """
    Geocode *place* with Nominatim and return (south, west, north, east)
    padded by *padding_deg* degrees.
    """
    try:
        import urllib.parse
        import urllib.request

        params = urllib.parse.urlencode(
            {
                "q": place,
                "format": "json",
                "limit": "1",
            }
        )
        req = urllib.request.Request(
            f"{NOMINATIM_URL}?{params}",
            headers={"User-Agent": "GeoSI/2.0 (geosi-plugin)"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:  # nosec B310
            data = json.loads(resp.read())
        if not data:
            return None
        bb = data[0].get("boundingbox")  # [south, north, west, east]
        if bb and len(bb) == 4:
            s, n, w, e = float(bb[0]), float(bb[1]), float(bb[2]), float(bb[3])
            return (s - padding_deg, w - padding_deg, n + padding_deg, e + padding_deg)
        # Fallback: point + padding
        lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
        return (lat - padding_deg, lon - padding_deg, lat + padding_deg, lon + padding_deg)
    except Exception as exc:
        logger.warning("Nominatim geocoding failed for %r: %s", place, exc)
        return None


def _overpass_query(
    tags: List[Dict[str, str]],
    bbox: Tuple[float, float, float, float],  # (south, west, north, east)
) -> str:
    """Build an Overpass QL query for the given tags and bounding box."""
    s, w, n, e = bbox
    bbox_str = f"{s},{w},{n},{e}"
    parts = []
    for tag_dict in tags:
        for k, v in tag_dict.items():
            if v == "yes":
                filter_ = f'["{k}"]'
            else:
                filter_ = f'["{k}"="{v}"]'
            parts.append(f"node{filter_}({bbox_str});")
            parts.append(f"way{filter_}({bbox_str});")
            parts.append(f"relation{filter_}({bbox_str});")
    union = "(\n  " + "\n  ".join(parts) + "\n);"
    return f"[out:json][timeout:30];\n{union}\nout body;\n>;\nout skel qt;"


def _overpass_to_geojson(data: dict) -> dict:
    """Convert Overpass JSON response to a GeoJSON FeatureCollection."""
    nodes: Dict[int, dict] = {}
    features = []

    for el in data.get("elements", []):
        if el["type"] == "node":
            nodes[el["id"]] = el

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        if el["type"] == "node" and tags:
            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [el["lon"], el["lat"]]},
                    "properties": {"osm_id": el["id"], "osm_type": "node", **tags},
                }
            )
        elif el["type"] == "way" and "nodes" in el:
            coords = [[nodes[n]["lon"], nodes[n]["lat"]] for n in el["nodes"] if n in nodes]
            if len(coords) >= 2:
                if coords[0] == coords[-1] and len(coords) >= 4:
                    geom = {"type": "Polygon", "coordinates": [coords]}
                else:
                    geom = {"type": "LineString", "coordinates": coords}
                features.append(
                    {
                        "type": "Feature",
                        "geometry": geom,
                        "properties": {"osm_id": el["id"], "osm_type": "way", **tags},
                    }
                )

    return {"type": "FeatureCollection", "features": features}


def _centroid(coords: List[List[float]]) -> List[float]:
    ring = coords[:-1] if len(coords) > 1 and coords[0] == coords[-1] else coords
    return [sum(c[0] for c in ring) / len(ring), sum(c[1] for c in ring) / len(ring)]


def single_geometry(geojson: dict) -> Tuple[dict, str]:
    """
    One geometry type per layer, as QGIS needs. The dominant type wins:
    points keep building outlines as their centre point (a hospital mapped
    as an area is still a hospital); lines keep closed ways as their outline;
    polygons drop stray points and lines.
    """
    feats = geojson.get("features", [])
    counts = {"Point": 0, "LineString": 0, "Polygon": 0}
    for f in feats:
        counts[f["geometry"]["type"]] = counts.get(f["geometry"]["type"], 0) + 1
    dominant = max(counts, key=lambda k: (counts[k], k == "Point"))
    out = []
    for f in feats:
        g = f["geometry"]
        if g["type"] == dominant:
            out.append(f)
        elif dominant == "Point" and g["type"] == "Polygon":
            out.append({**f, "geometry": {"type": "Point", "coordinates": _centroid(g["coordinates"][0])}})
        elif dominant == "LineString" and g["type"] == "Polygon":
            out.append({**f, "geometry": {"type": "LineString", "coordinates": g["coordinates"][0]}})
    return {"type": "FeatureCollection", "features": out}, dominant


# The public Overpass servers are often busy; these mirrors serve the same API
OVERPASS_MIRRORS = [
    OVERPASS_URL,
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]
_RETRY_STATUS = {429, 502, 503, 504}


def overpass_request(query: str, timeout: float = 60) -> dict:
    """POST an Overpass QL query, moving to the next mirror when one is overloaded or down."""
    import urllib.error

    last: Exception = RuntimeError("no Overpass server configured")
    for url in OVERPASS_MIRRORS:
        req = urllib.request.Request(
            url,
            data=urllib.parse.urlencode({"data": query}).encode(),
            headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "GeoSI/2.0"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310 — fixed Overpass mirrors
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code not in _RETRY_STATUS:
                raise
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = exc
        logger.warning("Overpass server %s unavailable (%s); trying the next mirror", url, last)
    raise last


def fetch_osm_to_file(
    category: str,
    location: Optional[str] = None,
    bbox: Optional[Tuple[float, float, float, float]] = None,
    out_dir: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Download OSM features to a GeoJSON file without touching QGIS, so it is
    safe in a background task. Returns {path, name, count, geometry} or None.
    """
    import tempfile

    tags = resolve_category(category)
    if tags is None:
        if "=" in category:
            k, v = category.split("=", 1)
            tags = [{k.strip(): v.strip()}]
        else:
            tags = [{"amenity": category}]
    if bbox is None and location:
        bbox = geocode_bbox(location)
    if bbox is None:
        logger.error("No bounding box — provide location or bbox")
        return None
    raw = overpass_request(_overpass_query(tags, bbox))
    geojson, geometry = single_geometry(_overpass_to_geojson(raw))
    if not geojson["features"]:
        return None
    slug = re.sub(r"[^A-Za-z0-9]+", "_", f"{category} {location or ''}").strip("_").lower()
    name = f"osm_{slug}"
    out_dir = out_dir or tempfile.mkdtemp(prefix="geosi_osm_")
    path = os.path.join(out_dir, f"{name}.geojson")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(geojson, fh)
    return {"path": path, "name": name, "count": len(geojson["features"]), "geometry": geometry}


def fetch_osm_features(
    category: str,
    location: Optional[str] = None,
    bbox: Optional[Tuple[float, float, float, float]] = None,
    canvas_bbox: Optional[Tuple[float, float, float, float]] = None,
) -> Optional[Any]:
    """
    Fetch OpenStreetMap features and return a QGIS in-memory vector layer.

    Parameters
    ----------
    category : str
        Natural-language category, e.g. "hospitals", "parks", "buildings".
    location : str, optional
        Place name to geocode (e.g. "London", "Seattle, WA").
    bbox : tuple, optional
        Explicit (south, west, north, east) bounding box in WGS84.
    canvas_bbox : tuple, optional
        Current QGIS canvas (xmin, ymin, xmax, ymax) converted to
        (south, west, north, east) automatically.
    """
    tags = resolve_category(category)
    if tags is None:
        # Try treating the category itself as a raw key=value tag
        if "=" in category:
            k, v = category.split("=", 1)
            tags = [{k.strip(): v.strip()}]
        else:
            tags = [{"amenity": category}]
        logger.debug("Unknown category %r — using tags %s", category, tags)

    # Resolve bounding box
    if bbox is None and canvas_bbox is not None:
        xmin, ymin, xmax, ymax = canvas_bbox
        bbox = (ymin, xmin, ymax, xmax)  # → (south, west, north, east)
    if bbox is None and location:
        bbox = geocode_bbox(location)
    if bbox is None:
        logger.error("No bounding box — provide location or bbox")
        return None

    # Fetch from Overpass
    query = _overpass_query(tags, bbox)
    try:
        raw = overpass_request(query)
    except Exception as exc:
        logger.error("Overpass request failed: %s", exc)
        return None

    geojson = _overpass_to_geojson(raw)
    n_features = len(geojson["features"])
    logger.info("Overpass returned %d features for %r", n_features, category)
    if n_features == 0:
        return None

    # Load into QGIS in-memory layer
    try:
        from qgis.core import QgsProject, QgsVectorLayer

        layer_name = f"OSM_{category}" + (f"_{location}" if location else "")
        layer = QgsVectorLayer(json.dumps(geojson), layer_name, "ogr")
        if not layer.isValid():
            # Fall back to temp file
            import tempfile

            # Use NamedTemporaryFile (delete=False) instead of insecure mktemp
            with tempfile.NamedTemporaryFile(mode="w", suffix=".geojson", delete=False) as tf:
                tmp = tf.name
                json.dump(geojson, tf)
            layer = QgsVectorLayer(tmp, layer_name, "ogr")
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            return layer
        logger.error("OSM layer invalid after loading")
        return None
    except ImportError:
        logger.warning("QGIS not available — returning raw GeoJSON dict")
        return geojson
