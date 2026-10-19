# -*- coding: utf-8 -*-
"""
GeoSI — Geocoding (Nominatim + Photon)
══════════════════════════════════════════════════════════════════════
Forward and reverse geocoding without any third-party Python packages —
just stdlib urllib.

Usage:
    from geosi_data.geocoding import geocode, reverse_geocode, zoom_to_place
"""
from __future__ import annotations

import json
import logging
import urllib.parse
import urllib.request
from typing import Optional, Tuple

logger = logging.getLogger("geosi_data.geocoding")

_NOMINATIM = "https://nominatim.openstreetmap.org"
_PHOTON = "https://photon.komoot.io"
_UA = "GeoSI/2.0 (geosi-plugin; contact=geosi@geosi.io)"


def geocode(
    address: str,
    provider: str = "nominatim",
) -> Tuple[float, float, str]:
    """
    Forward geocode *address*.

    Returns (lon, lat, display_name) or raises ValueError.
    """
    if provider == "photon":
        res = _photon_geocode(address)
    else:
        res = _nominatim_geocode(address)
    if res is None:
        raise ValueError(f"No geocoding results found for {address!r}")
    return res


def reverse_geocode(lat: float, lon: float) -> Optional[str]:
    """Reverse geocode a point to a human-readable address."""
    try:
        params = urllib.parse.urlencode({
            "lat": lat, "lon": lon, "format": "json",
        })
        req = urllib.request.Request(
            f"{_NOMINATIM}/reverse?{params}",
            headers={"User-Agent": _UA},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:  # nosec B310
            data = json.loads(resp.read())
        return data.get("display_name")
    except Exception as exc:
        logger.warning("Reverse geocode failed (%s, %s): %s", lat, lon, exc)
        return None


def zoom_to_place(address: str, project=None) -> Optional[Tuple[float, float]]:
    """
    Geocode *address* and zoom the QGIS map canvas to it.

    Returns (lon, lat) on success, None on failure.
    """
    result = geocode(address)
    if result is None:
        return None
    lon, lat, display = result
    logger.info("Zoomed to %r → %s (%f, %f)", address, display, lon, lat)
    try:
        from qgis.core import QgsRectangle, QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform
        from qgis.utils import iface

        canvas = iface.mapCanvas()
        # 0.05-degree box around the point
        rect = QgsRectangle(lon - 0.05, lat - 0.05, lon + 0.05, lat + 0.05)
        # Transform from WGS84 to canvas CRS if needed
        canvas_crs = canvas.mapSettings().destinationCrs()
        wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
        if canvas_crs != wgs84:
            xform = QgsCoordinateTransform(wgs84, canvas_crs, QgsProject.instance())
            rect = xform.transformBoundingBox(rect)
        canvas.setExtent(rect)
        canvas.refresh()
    except Exception as exc:
        logger.debug("Canvas zoom skipped: %s", exc)
    return lon, lat


# ── Providers ──────────────────────────────────────────────────────────

def _nominatim_geocode(address: str) -> Optional[Tuple[float, float, str]]:
    params = urllib.parse.urlencode({
        "q": address, "format": "json", "limit": "1", "addressdetails": "0",
    })
    req = urllib.request.Request(
        f"{_NOMINATIM}/search?{params}",
        headers={"User-Agent": _UA},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:  # nosec B310
        data = json.loads(resp.read())
    if not data:
        return None
    r = data[0]
    return float(r["lon"]), float(r["lat"]), r.get("display_name", address)


def _photon_geocode(address: str) -> Optional[Tuple[float, float, str]]:
    params = urllib.parse.urlencode({"q": address, "limit": "1"})
    req = urllib.request.Request(
        f"{_PHOTON}/api?{params}",
        headers={"User-Agent": _UA},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:  # nosec B310
        data = json.loads(resp.read())
    features = data.get("features", [])
    if not features:
        return None
    f = features[0]
    coords = f["geometry"]["coordinates"]
    name = f["properties"].get("name") or address
    return float(coords[0]), float(coords[1]), name
