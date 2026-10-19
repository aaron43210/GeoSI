"""
GeoSI — Basemap Connectors
══════════════════════════════════════════════════════════════════════
Add XYZ tile basemaps to QGIS from natural-language requests.

Usage (from agent tools):
    from geosi_data.basemaps import add_basemap
    layer = add_basemap("esri_satellite")

The PROVIDERS dict is the catalog. Every provider is a pure WMS/XYZ
connection — no third-party Python packages needed, just QGIS core.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("geosi_data.basemaps")

# ── Tile provider catalog ──────────────────────────────────────────────
# type: "xyz" | "wms"
PROVIDERS: Dict[str, Dict[str, Any]] = {
    # OpenStreetMap
    "osm": {
        "label": "OpenStreetMap Standard",
        "url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        "type": "xyz",
        "max_zoom": 19,
        "attribution": "© OpenStreetMap contributors",
        "aliases": ["openstreetmap", "osm standard", "street map"],
    },
    # CartoDB
    "carto_light": {
        "label": "CartoDB Positron (Light)",
        "url": "https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
        "type": "xyz",
        "max_zoom": 20,
        "aliases": ["carto light", "positron", "light basemap"],
    },
    "carto_dark": {
        "label": "CartoDB Dark Matter",
        "url": "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
        "type": "xyz",
        "max_zoom": 20,
        "aliases": ["carto dark", "dark matter", "dark basemap"],
    },
    # ESRI
    "esri_satellite": {
        "label": "ESRI World Imagery (Satellite)",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "type": "xyz",
        "max_zoom": 19,
        "aliases": ["esri imagery", "satellite", "aerial", "esri satellite", "world imagery"],
    },
    "esri_topo": {
        "label": "ESRI World Topo Map",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        "type": "xyz",
        "max_zoom": 19,
        "aliases": ["esri topo", "topo map", "topographic"],
    },
    "esri_streets": {
        "label": "ESRI World Street Map",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        "type": "xyz",
        "max_zoom": 19,
        "aliases": ["esri streets", "esri street map"],
    },
    # Google (unofficial — may require terms compliance in production)
    "google_satellite": {
        "label": "Google Satellite",
        "url": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        "type": "xyz",
        "max_zoom": 20,
        "aliases": ["google satellite", "google imagery", "google aerial"],
    },
    "google_hybrid": {
        "label": "Google Hybrid",
        "url": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        "type": "xyz",
        "max_zoom": 20,
        "aliases": ["google hybrid", "google roads satellite"],
    },
    # USGS
    "usgs_topo": {
        "label": "USGS National Map (Topo)",
        "url": "https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}",
        "type": "xyz",
        "max_zoom": 16,
        "aliases": ["usgs topo", "usgs", "national map"],
    },
    "usgs_imagery": {
        "label": "USGS National Map (Imagery)",
        "url": "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}",
        "type": "xyz",
        "max_zoom": 16,
        "aliases": ["usgs imagery", "usgs satellite"],
    },
    # Stadia / Stamen
    "stadia_toner": {
        "label": "Stadia Stamen Toner",
        "url": "https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}.png",
        "type": "xyz",
        "max_zoom": 20,
        "aliases": ["toner", "stamen toner", "black white map"],
    },
    "stadia_watercolor": {
        "label": "Stadia Stamen Watercolor",
        "url": "https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.jpg",
        "type": "xyz",
        "max_zoom": 16,
        "aliases": ["watercolor", "stamen watercolor", "artistic map"],
    },
    # OpenTopoMap
    "opentopomap": {
        "label": "OpenTopoMap",
        "url": "https://tile.opentopomap.org/{z}/{x}/{y}.png",
        "type": "xyz",
        "max_zoom": 17,
        "aliases": ["opentopomap", "ot map", "hiking map"],
    },
}


try:
    import qgis.core  # noqa: F401

    _qgis_available = True
except ImportError:
    _qgis_available = False


def resolve_provider(name: str) -> Optional[str]:
    """
    Fuzzy-match *name* to a provider key.

    Checks exact key, then label (case-insensitive), then aliases.
    Returns the canonical provider key, defaulting to 'osm' if unrecognized.
    """
    nl = name.lower().strip()
    if nl in PROVIDERS:
        return nl
    for key, info in PROVIDERS.items():
        if nl == info["label"].lower():
            return key
        if any(nl == a.lower() for a in info.get("aliases", [])):
            return key
        if nl in key or nl in info["label"].lower():
            return key
    return "osm"


def list_providers() -> list[dict]:
    """Return a list of {key, label, aliases} for display."""
    return [{"key": k, "label": v["label"], "aliases": v.get("aliases", [])} for k, v in PROVIDERS.items()]


def add_basemap(provider_name: str, project=None) -> Optional[Any]:
    """
    Add a basemap tile layer to the current QGIS project.

    Parameters
    ----------
    provider_name : str
        Provider key or alias (e.g. "esri_satellite", "satellite", "OSM").
    project : QgsProject, optional
        Defaults to QgsProject.instance().

    Returns the QgsRasterLayer on success, None on failure.
    """
    if not _qgis_available:
        logger.warning("QGIS not available — basemap add skipped")
        return None

    key = resolve_provider(provider_name)
    if key is None:
        available = ", ".join(PROVIDERS.keys())
        logger.warning("Unknown basemap provider %r. Available: %s", provider_name, available)
        return None

    info = PROVIDERS[key]
    label = info["label"]

    try:
        from qgis.core import QgsProject, QgsRasterLayer

        if project is None:
            project = QgsProject.instance()

        # Build XYZ URI
        url = info["url"].replace("{", "%7B").replace("}", "%7D")
        uri = f"type=xyz" f"&url={url}" f"&zmax={info.get('max_zoom', 19)}" f"&zmin=0"
        layer = QgsRasterLayer(uri, label, "wms")
        if not layer.isValid():
            logger.error("Basemap layer invalid: %s (uri=%s)", label, uri)
            return None

        project.addMapLayer(layer, False)
        # Move to bottom of layer tree
        root = project.layerTreeRoot()
        root.insertLayer(len(root.children()), layer)

        logger.info("Added basemap: %s", label)
        return layer

    except ImportError:
        logger.warning("QGIS not available — basemap add skipped")
        return None
    except Exception as exc:
        logger.error("add_basemap failed for %s: %s", provider_name, exc)
        return None
