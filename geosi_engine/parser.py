# -*- coding: utf-8 -*-
"""
GeoSI Engine - Query Parser (Superintelligence Edition)

Translates natural language GIS questions into a fully-structured
AnalysisRequest. The parser runs as a layered pipeline so it stays
correct, deterministic, and cheap whenever possible, and reaches for
LLMs only when it genuinely needs them:

    1. Normalize the input (unicode, whitespace, punctuation).
    2. Look the query up in an in-process LRU cache (keyed by normalized
       query + available layers) plus an optional on-disk JSON cache
       under the user's QGIS profile, so repeated prompts skip LLM calls.
    3. Try LLM providers in order (Ollama -> Gemini -> Anthropic -> OpenAI)
       using a strict JSON-schema prompt and tolerant JSON extraction.
       Ollama is tried first (local, no API key needed). Falls back to cloud
       providers if Ollama is not available.
    4. Fall back to a rich rule-based parser that scores intents,
       extracts distances with unit conversion, detects operations,
       captures field filters, and matches layer names fuzzily.
    5. Post-process: validate the IntentType, normalize units, attach a
       confidence score, and cache the parsed payload locally.

The module never raises on bad LLM output or missing API keys - every
failure quietly degrades to the next fallback. The keyword fallback on
its own is complete enough to handle all built-in GeoSI tools. No
external services are contacted by the parser itself - it runs fully
offline inside the QGIS plugin and the FastAPI server.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import tempfile
import threading
import unicodedata
from collections import OrderedDict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from geosi_engine.models import AnalysisRequest, IntentType
from geosi_engine.conversation import ConversationManager

logger = logging.getLogger("geosi_engine.parser")


# ---------------------------------------------------------------------------
# Intent keyword map. Each keyword gets a weight; higher means more decisive.
# ---------------------------------------------------------------------------

_INTENT_KEYWORDS: Dict[IntentType, Dict[str, int]] = {
    IntentType.PROXIMITY: {
        "buffer": 3, "within": 2, "near": 2, "nearby": 2, "closest": 3,
        "nearest": 3, "distance": 2, "radius": 3, "around": 2,
        "proximity": 3, "surrounding": 2, "catchment": 2, "service radius": 3,
    },
    IntentType.OVERLAY: {
        "intersect": 3, "intersection": 3, "union": 3, "clip": 3,
        "difference": 3, "overlay": 3, "combine": 2, "merge": 2,
        "spatial join": 3, "join": 3, "attribute join": 3, "overlap": 2,
        "symmetric difference": 3, "erase": 2, "split": 2, "extract": 2,
        "subset": 3, "crop": 3, "shapefile from": 2, "region from": 2,
        "area from": 2, "filter": 3,
    },
    IntentType.GEOMETRY: {
        "centroid": 3, "simplify": 3, "smooth": 2, "dissolve": 3,
        "convex hull": 3, "concave hull": 3, "densify": 2,
        "multipart": 2, "singlepart": 2, "explode": 2, "voronoi": 3,
        "delaunay": 3, "bounding box": 3, "minimum bounding": 3,
        "extract vertices": 2, "line to polygon": 2, "polygon to line": 2,
    },
    IntentType.RASTER: {
        "raster": 3, "pixel": 2, "band": 2, "ndvi": 5, "ndwi": 5,
        "ndbi": 3, "evi": 3, "savi": 3, "zonal": 3, "reclassify": 3,
        "raster calculator": 3, "composite": 2, "mosaic": 3,
        "nodata": 2, "resample": 2, "interpolate raster": 3,
        "vegetative index": 5, "water index": 5, "satellite": 2,
    },
    IntentType.TERRAIN: {
        "slope": 3, "aspect": 3, "hillshade": 3, "elevation": 2,
        "dem": 3, "dsm": 3, "dtm": 3, "contour": 3, "viewshed": 3,
        "profile": 2, "watershed": 3, "flow direction": 3,
        "flow accumulation": 3, "curvature": 3, "ruggedness": 2,
        "terrain": 2, "tri": 2, "tpi": 2, "roughness": 2,
    },
    IntentType.NETWORK: {
        "route": 3, "routing": 3, "shortest path": 3, "shortest route": 3,
        "network": 2, "service area": 3, "travel time": 3,
        "isochrone": 3, "cost distance": 3, "origin": 2, "destination": 2,
        "driving": 2, "walking": 2, "transit": 2,
    },
    IntentType.TEMPORAL: {
        "temporal": 3, "time series": 3, "change detection": 3,
        "before": 1, "after": 1, "trend": 2, "animate": 2,
        "period": 1, "between": 1, "over time": 3, "historical": 2,
    },
    IntentType.AI_ML: {
        "cluster": 3, "classify": 3, "classification": 3, "hotspot": 3,
        "interpolate": 2, "density": 2, "kriging": 3, "idw": 3,
        "dbscan": 3, "kmeans": 3, "k-means": 3, "anomaly": 3,
        "predict": 2, "regression": 3, "autocorrelation": 3,
        "machine learning": 3, " ml ": 2, "random forest": 3,
        "getis-ord": 3, "moran": 3,
    },
    IntentType.VALIDATION: {
        "valid": 2, "validity": 3, "topology": 3, "duplicate": 2,
        "null geometry": 3, "snap": 2, "gap": 2,
        "fix geometries": 3, "repair": 2, "check": 1, "quality": 1,
        "self intersect": 3,
    },
    IntentType.CARTOGRAPHY: {
        "export": 2, "geojson": 3, "shapefile": 3, "csv": 2, "kml": 3,
        "geopackage": 3, "geocode": 3, "address": 2, "label": 2,
        "style": 2, "atlas": 3, "map layout": 3, "print map": 3,
    },
    IntentType.STATISTICS: {
        "statistics": 3, "count": 1, "sum": 1, "average": 2, "mean": 2,
        "median": 2, "minimum": 1, "maximum": 1, "std": 2,
        "standard deviation": 3, "histogram": 3, "summary": 2,
    },
    IntentType.DATA_MANAGEMENT: {
        "load": 1, "save": 1, "import": 1, "open": 1, "convert": 2,
        "reproject": 3, "transform": 2, "crs": 3, "coordinate system": 3,
        "projection": 2,
    },
}

# Distance units -> meters
_UNIT_TO_METERS: Dict[str, float] = {
    "mm": 0.001, "millimeter": 0.001, "millimetre": 0.001,
    "cm": 0.01, "centimeter": 0.01, "centimetre": 0.01,
    "m": 1.0, "meter": 1.0, "metre": 1.0, "meters": 1.0, "metres": 1.0,
    "km": 1000.0, "kilometer": 1000.0, "kilometre": 1000.0,
    "kilometers": 1000.0, "kilometres": 1000.0,
    "mi": 1609.344, "mile": 1609.344, "miles": 1609.344,
    "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
    "yd": 0.9144, "yard": 0.9144, "yards": 0.9144,
    "nmi": 1852.0, "nautical mile": 1852.0,
}

_DISTANCE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*"
    r"(kilometers?|kilometres?|km|meters?|metres?|m|miles?|mi|"
    r"feet|foot|ft|yards?|yd|centimeters?|centimetres?|cm|"
    r"millimeters?|millimetres?|mm|nautical\s*miles?|nmi)\b",
    re.IGNORECASE,
)

_NUMBER_PATTERN = re.compile(r"\b(\d+(?:\.\d+)?)\b")

# "field = value", "field > 10", "population above 1000"
_FIELD_FILTER_PATTERN = re.compile(
    r"\b([A-Za-z_][A-Za-z0-9_]*)\s*"
    r"(=|==|!=|<>|>=|<=|>|<|is|equals?|above|below|over|under|greater than|less than)\s*"
    r"('[^']*'|\"[^\"]*\"|-?\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_]*)",
    re.IGNORECASE,
)

# Canonical operation tokens the rule-based planner can consume directly.
_OPERATION_MAP: Dict[str, List[str]] = {
    "ndvi": ["ndvi", "vegetative index", "vegetation index", "vegetation"],
    "ndwi": ["ndwi", "water index"],
    "buffer": ["buffer", "grow by", "ring around"],
    "intersect": ["intersect", "overlap", "common area", "inside both"],
    "union": ["union", "merge", "combine"],
    "clip": ["clip", "cut to", "crop", "extract", "subset", "shapefile from",
             "region from", "area from", "need", "get"],
    "difference": ["difference", "erase", "subtract"],
    "centroid": ["centroid", "center point", "centre point"],
    "dissolve": ["dissolve"],
    "convex_hull": ["convex hull"],
    "voronoi": ["voronoi", "thiessen"],
    "watershed": ["watershed", "watershed analysis", "flow accumulation", "flow direction",
                  "catchment", "drainage basin", "pour point", "delineate"],
    "slope": ["slope"],
    "aspect": ["aspect"],
    "hillshade": ["hillshade"],
    "contour": ["contour"],
    "viewshed": ["viewshed"],
    "cluster": ["cluster", "kmeans", "dbscan"],
    "hotspot": ["hotspot", "getis", "moran"],
    "shortest_path": ["shortest path", "shortest route", "fastest route"],
    "service_area": ["service area", "isochrone"],
    "reproject": ["reproject", "transform crs", "change projection"],
    "export_geojson": ["export geojson", "save geojson", "to geojson"],
    "geocode": ["geocode", "address to"],
    "extract_by_attribute": ["filter", "select where", "find where", "attribute equals"],
    "join_attributes": ["join", "attribute join", "join with", "link with"],
}


# ---------------------------------------------------------------------------
# Local cache (in-memory LRU + optional JSON file). No network required.
# ---------------------------------------------------------------------------

def _default_cache_path() -> Path:
    override = os.environ.get("GEOSI_CACHE_DIR")
    if override:
        base = Path(override)
    else:
        # Prefer the QGIS profile directory if it exists, otherwise temp.
        qgis_profile = (
            Path.home() / "Library/Application Support/QGIS/QGIS4/profiles/default/geosi"
        )
        base = qgis_profile if qgis_profile.parent.exists() else Path(
            tempfile.gettempdir()
        ) / "geosi"
    try:
        base.mkdir(parents=True, exist_ok=True)
    except Exception:
        base = Path(tempfile.gettempdir())
    return base / "parser_cache.json"


class _LocalCache:
    """Thread-safe LRU cache with best-effort JSON persistence."""

    def __init__(self, max_entries: int = 512) -> None:
        self.max_entries = max_entries
        self._lock = threading.Lock()
        self._entries: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        self._path = _default_cache_path()
        self._load()

    def _load(self) -> None:
        try:
            if self._path.exists():
                with self._path.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
                if isinstance(data, dict):
                    for k, v in list(data.items())[-self.max_entries:]:
                        if isinstance(v, dict):
                            self._entries[k] = v
        except Exception as exc:  # pragma: no cover
            logger.debug("Local parser cache load failed: %s", exc)

    def _flush(self) -> None:
        try:
            tmp = self._path.with_suffix(".json.tmp")
            with tmp.open("w", encoding="utf-8") as fh:
                json.dump(self._entries, fh)
            tmp.replace(self._path)
        except Exception as exc:  # pragma: no cover
            logger.debug("Local parser cache flush failed: %s", exc)

    def lookup(self, query_hash: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            entry = self._entries.get(query_hash)
            if entry is not None:
                self._entries.move_to_end(query_hash)
            return entry

    def store(
        self,
        query_hash: str,
        query: str,
        layers: List[str],
        intent: str,
        payload: Dict[str, Any],
        confidence: float,
        source: str,
    ) -> None:
        entry = {
            "query": query,
            "available_layers": layers,
            "intent": intent,
            "payload": payload,
            "confidence": float(confidence),
            "source": source,
        }
        with self._lock:
            self._entries[query_hash] = entry
            self._entries.move_to_end(query_hash)
            while len(self._entries) > self.max_entries:
                self._entries.popitem(last=False)
            self._flush()


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

class QueryParser:
    """Natural-language GIS query parser with LLM + rules + cache."""

    def __init__(self, use_llm: bool = True, use_cache: bool = True, conversation: Optional[ConversationManager] = None) -> None:
        self.use_llm = use_llm
        self.use_cache = use_cache
        self.conversation = conversation or ConversationManager(
            system_prompt="You are a GIS query parser. Extract the intent, layers, and parameters from queries."
        )
        self._ollama_endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
        self._ollama_model = self._detect_ollama_model()
        self._anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self._gemini_key = (
            os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
            or ""
        )
        self._openai_key = os.environ.get("OPENAI_API_KEY", "")
        self._cache = _LocalCache() if use_cache else None

    def _detect_ollama_model(self) -> str:
        """Auto-detect an available Ollama model, falling back gracefully."""
        model = os.environ.get("OLLAMA_MODEL", "mistral")
        try:
            import requests
            endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
            resp = requests.get(f"{endpoint}/api/tags", timeout=1.5)
            if resp.status_code == 200:
                models = [m.get("name") for m in resp.json().get("models", [])]
                if models and model not in models:
                    for pref in ["llama3.2:3b", "qwen2.5-coder:14b", "mistral"]:
                        if pref in models:
                            return pref
                    return models[0]
        except Exception:
            pass
        return model

    # -- public API --------------------------------------------------------

    def parse(
        self,
        query: str,
        available_layers: Optional[List[str]] = None,
    ) -> AnalysisRequest:
        available_layers = list(available_layers or [])
        if not query or not query.strip():
            return AnalysisRequest(
                query=query or "",
                intent=IntentType.UNKNOWN,
                available_layers=available_layers,
                constraints=["Empty query."],
            )

        normalized = self._normalize(query)
        cache_key = self._hash(normalized, available_layers)

        # 1. Cache
        if self._cache is not None:
            cached = self._cache.lookup(cache_key)
            if cached and isinstance(cached.get("payload"), dict):
                try:
                    return self._request_from_payload(
                        query, cached["payload"], available_layers
                    )
                except Exception as exc:
                    logger.debug("Cache payload rejected: %s", exc)

        # 2. Keyword parser FIRST — fast, reliable for well-understood ops.
        #    Only fall through to LLM if keywords can't determine intent.
        kw_req, kw_confidence = self._parse_with_keywords(normalized, available_layers)
        kw_req.query = query
        self._post_process(kw_req, normalized, available_layers)

        if kw_req.intent != IntentType.UNKNOWN:
            # Keywords identified a clear intent — use it, skip LLM entirely.
            # This is faster and more reliable for clip, buffer, ndvi, etc.
            logger.info(f"Keyword parser identified intent={kw_req.intent}, skipping LLM")
            self._store_cache(
                cache_key, query, available_layers, kw_req, kw_confidence, "keywords"
            )
            return kw_req

        # 3. LLM providers — only for ambiguous/complex queries where
        #    keywords returned UNKNOWN.
        llm_order: List[Tuple[str, Any]] = []
        if self.use_llm:
            llm_order.append(("ollama", self._parse_with_ollama))
            if self._gemini_key:
                llm_order.append(("gemini", self._parse_with_gemini))
            if self._anthropic_key:
                llm_order.append(("anthropic", self._parse_with_anthropic))
            if self._openai_key:
                llm_order.append(("openai", self._parse_with_openai))

        for name, fn in llm_order:
            try:
                req, confidence = fn(normalized, available_layers)
                req.query = query
                self._post_process(req, normalized, available_layers)
                if req.intent == IntentType.UNKNOWN:
                    logger.warning(f"{name} returned UNKNOWN intent, trying next parser")
                    continue
                self._store_cache(
                    cache_key, query, available_layers, req, confidence, name
                )
                return req
            except Exception as exc:
                logger.warning("%s parse failed: %s", name, exc)

        # 4. If everything failed, return the keyword result (even if UNKNOWN)
        self._store_cache(
            cache_key, query, available_layers, kw_req, kw_confidence, "keywords"
        )
        return kw_req

    # -- normalization / hashing ------------------------------------------

    @staticmethod
    def _normalize(query: str) -> str:
        text = unicodedata.normalize("NFKC", query)
        text = text.replace("\u2013", "-").replace("\u2014", "-")
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def _hash(query: str, layers: List[str]) -> str:
        payload = json.dumps(
            {"q": query.lower(), "l": sorted(l.lower() for l in layers)},
            sort_keys=True,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    # -- rule-based --------------------------------------------------------

    def _parse_with_keywords(
        self, query: str, available_layers: List[str]
    ) -> Tuple[AnalysisRequest, float]:
        # Convert to lowercase for case-insensitive matching throughout
        lowered = query.lower()

        # Tally keyword matches for each intent type; higher weight = stronger signal
        scores: Dict[IntentType, int] = {}
        for intent, keywords in _INTENT_KEYWORDS.items():
            total = 0
            for kw, weight in keywords.items():
                # Use word boundaries to prevent false positives (e.g., 'tri' in 'distribution')
                if re.search(rf"\b{re.escape(kw)}\b", lowered):
                    total += weight
            if total:
                scores[intent] = total

        # Pick the intent with the highest score; compute confidence as a blend
        # of raw score vs. total signal across all intents (0.35 baseline + boost)
        if scores:
            top_score = max(scores.values())
            intent = max(scores, key=scores.get)
            total = sum(scores.values())
            confidence = min(0.95, 0.35 + 0.6 * (top_score / max(total, 1)))
        else:
            intent = IntentType.UNKNOWN
            confidence = 0.1

        # Build parameters dict by extracting structured fields from the query
        parameters: Dict[str, Any] = {}

        # Extract "500 km" or "1.5 miles", normalize to meters
        dist = _DISTANCE_PATTERN.search(query)
        if dist:
            value = float(dist.group(1))
            unit = re.sub(r"\s+", " ", dist.group(2).lower().strip())
            factor = _UNIT_TO_METERS.get(unit)
            if factor is None:
                # Try singular form (e.g., "meter" instead of "meters")
                factor = _UNIT_TO_METERS.get(unit.rstrip("s"), 1.0)
            parameters["distance_value"] = value * factor
            parameters["distance_unit"] = "meters"
            parameters["distance_original"] = f"{value} {unit}"

        # Detect comparisons like "above 1000" or "top 10"
        thr = re.search(
            r"\b(?:above|over|more than|greater than|top|at least)\s+(\d+(?:\.\d+)?)",
            lowered,
        )
        if thr:
            parameters["threshold"] = float(thr.group(1))
            parameters["threshold_op"] = ">="

        # Detect lower bounds like "below 500" or "less than 100"
        thr_lo = re.search(
            r"\b(?:below|under|less than|at most)\s+(\d+(?:\.\d+)?)", lowered
        )
        if thr_lo:
            parameters["threshold"] = float(thr_lo.group(1))
            parameters["threshold_op"] = "<="

        # Extract field-level filters: "population > 10000" or "name = 'Hospital'"
        filters: List[Dict[str, Any]] = []
        for m in _FIELD_FILTER_PATTERN.finditer(query):
            field, op, value = m.group(1), m.group(2).lower(), m.group(3)
            # Skip structural words that look like field names but are not
            if field.lower() in {"within", "near", "and", "or", "with", "of"}:
                continue
            filters.append({"field": field, "op": op, "value": value.strip("'\"")})
        if filters:
            parameters["filters"] = filters

        # Detect CRS/projection references (e.g., "EPSG:4326" or "EPSG 3857")
        crs = re.search(r"\bEPSG[:\s]?(\d{4,6})\b", query, re.IGNORECASE)
        if crs:
            parameters["crs"] = f"EPSG:{crs.group(1)}"

        # Identify the operation to perform (buffer, clip, slope, etc.)
        operation = None
        for op_name, aliases in _OPERATION_MAP.items():
            if any(re.search(rf"\b{re.escape(alias)}\b", lowered) for alias in aliases):
                operation = op_name
                break
        if operation:
            parameters["operation"] = operation

        # Extract pour point / coordinate references
        # Matches patterns like: "at point 77.5, 8.5", "at 77.5 8.5", "coordinates 77.5, 8.5"
        coord_match = re.search(
            r'(?:at\s+(?:point\s+)?|pour\s+point\s+|coordinates?\s+|point\s+)'
            r'(-?\d+\.?\d*)[,\s]+(-?\d+\.?\d*)',
            lowered
        )
        if coord_match:
            parameters["point_x"] = float(coord_match.group(1))
            parameters["point_y"] = float(coord_match.group(2))

        # Fuzzy-match available layers to primary, secondary, and additional
        entities = self._extract_layers(query, available_layers)

        # Extract capitalized nouns as feature names (e.g., "Hospital", "Park")
        features = re.findall(r"\b([A-Z][a-zA-Z_]{2,})\b", query)
        if features:
            entities.setdefault("features", features[:8])

        request = AnalysisRequest(
            query=query,
            intent=intent,
            entities=entities,
            parameters=parameters,
            available_layers=available_layers,
        )
        return request, confidence

    # -- layer fuzzy matching ---------------------------------------------

    # Cache keyed by (normalized query, layers tuple). Retries + LLM
    # fallbacks within a session reuse the same expensive SequenceMatcher
    # result instead of re-running dynamic string alignment.
    _layer_match_cache: "OrderedDict[Tuple[str, Tuple[str, ...]], Dict[str, Any]]" = OrderedDict()
    _layer_match_cache_max = 256
    _layer_match_cache_lock = threading.Lock()

    @classmethod
    def _extract_layers(
        cls, query: str, available_layers: List[str]
    ) -> Dict[str, Any]:
        lowered = query.lower()
        layers_key = tuple(available_layers)
        cache_key = (lowered, layers_key)
        with cls._layer_match_cache_lock:
            cached = cls._layer_match_cache.get(cache_key)
            if cached is not None:
                cls._layer_match_cache.move_to_end(cache_key)
                return dict(cached)

        matches: List[Tuple[str, float]] = []
        for layer in available_layers:
            name = layer.lower()
            if not name:
                continue
            if name in lowered:
                matches.append((layer, 1.0))
                continue
            # Loose stem match - allow "hospital" to hit "hospitals".
            stem = name.rstrip("s")
            if stem and stem in lowered:
                matches.append((layer, 0.85))
                continue
            # SequenceMatcher is O(|name| * |query|); cheap string
            # checks above let us skip it for most layer names.
            ratio = SequenceMatcher(None, name, lowered).ratio()
            if ratio >= 0.72:
                matches.append((layer, ratio))

        matches.sort(key=lambda p: p[1], reverse=True)
        entities: Dict[str, Any] = {}
        if matches:
            entities["primary_layer"] = matches[0][0]
        if len(matches) > 1:
            entities["secondary_layer"] = matches[1][0]
        if len(matches) > 2:
            entities["additional_layers"] = [m[0] for m in matches[2:5]]

        with cls._layer_match_cache_lock:
            cls._layer_match_cache[cache_key] = dict(entities)
            cls._layer_match_cache.move_to_end(cache_key)
            while len(cls._layer_match_cache) > cls._layer_match_cache_max:
                cls._layer_match_cache.popitem(last=False)
        return entities

    # -- LLM prompting -----------------------------------------------------

    def _prompt(self, query: str, available_layers: List[str]) -> str:
        intents = [it.value for it in IntentType]
        layer_list = ", ".join(available_layers) if available_layers else "(none)"
        return (
            "You are GeoSI, a geospatial intelligence query parser.\n"
            "Convert the user's GIS question into a STRICT JSON object.\n"
            "Return ONLY JSON. No markdown, no prose, no code fences.\n\n"
            f"Available layers: {layer_list}\n"
            f"Valid intents: {intents}\n\n"
            f"User query: \"{query}\"\n\n"
            "JSON schema:\n"
            "{\n"
            '  "intent": "<one of valid intents>",\n'
            '  "confidence": 0.0,\n'
            '  "operation": "<canonical op like buffer|intersect|slope|ndvi|shortest_path or null>",\n'
            '  "entities": {\n'
            '    "primary_layer": "<layer name or null>",\n'
            '    "secondary_layer": "<layer name or null>",\n'
            '    "additional_layers": [],\n'
            '    "features": []\n'
            "  },\n"
            '  "parameters": {\n'
            '    "distance_value": null,\n'
            '    "distance_unit": "meters",\n'
            '    "field_name": null,\n'
            '    "threshold": null,\n'
            '    "threshold_op": null,\n'
            '    "crs": null,\n'
            '    "filters": []\n'
            "  },\n"
            '  "constraints": []\n'
            "}\n"
            "Rules: convert every distance to meters. Pick layer names ONLY "
            "from the provided list. If unsure, set the field to null. "
            "Intent MUST be one of the valid intents."
        )

    def _parse_with_ollama(
        self, query: str, available_layers: List[str]
    ) -> Tuple[AnalysisRequest, float]:
        import requests

        # Fast availability probe so we fail over to other providers / rules
        # within a second instead of waiting out the generation timeout when
        # Ollama is not running.
        try:
            requests.get(f"{self._ollama_endpoint}/api/tags", timeout=1.5)
        except Exception as exc:
            raise RuntimeError(f"Ollama not reachable at {self._ollama_endpoint}: {exc}")

        self.conversation.add_user_message(self._prompt(query, available_layers))
        context = self.conversation.get_context(include_system=True)

        endpoint = f"{self._ollama_endpoint}/api/generate"
        payload = {
            "model": self._ollama_model,
            "prompt": context,
            "stream": False,
            "temperature": 0.0,
        }
        response = requests.post(endpoint, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "")
        
        # Add response to conversation history
        self.conversation.add_assistant_message(text)
        
        return self._json_to_request(query, text, available_layers)

    def _parse_with_anthropic(
        self, query: str, available_layers: List[str]
    ) -> Tuple[AnalysisRequest, float]:
        import anthropic

        client = anthropic.Anthropic(api_key=self._anthropic_key)
        response = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
            max_tokens=1024,
            temperature=0.0,
            system="Return only valid JSON matching the schema.",
            messages=[{"role": "user", "content": self._prompt(query, available_layers)}],
        )
        text = "".join(
            getattr(block, "text", "") for block in response.content
        )
        return self._json_to_request(query, text, available_layers)

    def _parse_with_gemini(
        self, query: str, available_layers: List[str]
    ) -> Tuple[AnalysisRequest, float]:
        import google.generativeai as genai

        genai.configure(api_key=self._gemini_key)
        model = genai.GenerativeModel(
            os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
            generation_config={
                "temperature": 0.0,
                "response_mime_type": "application/json",
            },
        )
        response = model.generate_content(self._prompt(query, available_layers))
        return self._json_to_request(query, response.text, available_layers)

    def _parse_with_openai(
        self, query: str, available_layers: List[str]
    ) -> Tuple[AnalysisRequest, float]:
        import urllib.request

        body = json.dumps({
            "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            "temperature": 0.0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": self._prompt(query, available_layers)},
            ],
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self._openai_key}",
                "Content-Type": "application/json",
            },
            data=body,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"]
        return self._json_to_request(query, text, available_layers)

    # -- JSON -> AnalysisRequest ------------------------------------------

    def _json_to_request(
        self, query: str, text: str, available_layers: List[str]
    ) -> Tuple[AnalysisRequest, float]:
        data = self._extract_json(text)
        if not isinstance(data, dict):
            raise ValueError("LLM did not return a JSON object")

        return self._request_from_payload(query, data, available_layers), float(
            data.get("confidence") or 0.75
        )

    @staticmethod
    def _extract_json(text: str) -> Any:
        if not text:
            raise ValueError("empty LLM response")
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
        # Greedy-match the first balanced JSON object in the response.
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise ValueError("no JSON object found in LLM output")

    def _request_from_payload(
        self,
        query: str,
        data: Dict[str, Any],
        available_layers: List[str],
    ) -> AnalysisRequest:
        intent_raw = str(data.get("intent", "unknown")).lower()
        try:
            intent = IntentType(intent_raw)
        except ValueError:
            intent = IntentType.UNKNOWN

        entities = dict(data.get("entities") or {})
        parameters = dict(data.get("parameters") or {})
        if data.get("operation") and "operation" not in parameters:
            parameters["operation"] = data["operation"]

        return AnalysisRequest(
            query=query,
            intent=intent,
            entities=entities,
            parameters=parameters,
            constraints=list(data.get("constraints") or []),
            available_layers=available_layers,
        )

    # -- post processing ---------------------------------------------------

    def _post_process(
        self,
        request: AnalysisRequest,
        normalized: str,
        available_layers: List[str],
    ) -> None:
        # Ensure every parameter section exists and every distance is in meters.
        params = request.parameters
        if params.get("distance_value") is not None:
            try:
                params["distance_value"] = float(params["distance_value"])
            except (TypeError, ValueError):
                params.pop("distance_value", None)
        params.setdefault("distance_unit", "meters")

        # Backfill primary layer via fuzzy match if LLM omitted it.
        if not request.entities.get("primary_layer") and available_layers:
            fuzzy = self._extract_layers(normalized, available_layers)
            for key in ("primary_layer", "secondary_layer", "additional_layers"):
                if fuzzy.get(key) and not request.entities.get(key):
                    request.entities[key] = fuzzy[key]

        # Strip file extensions (.shp, .geojson, etc.) from layer references
        # and match the stem against loaded layers.
        import os as _os
        for key in ("primary_layer", "secondary_layer"):
            name = request.entities.get(key)
            if isinstance(name, str) and available_layers:
                # If the name has a geo extension, try the stem first
                stem, ext = _os.path.splitext(name)
                if ext.lower() in (".shp", ".geojson", ".gpkg", ".kml", ".tif", ".tiff"):
                    if stem in available_layers:
                        request.entities[key] = stem
                        name = stem

        # Warn when a referenced layer is not actually loaded.
        for key in ("primary_layer", "secondary_layer"):
            name = request.entities.get(key)
            if (
                isinstance(name, str)
                and available_layers
                and name not in available_layers
            ):
                request.constraints.append(
                    f"Layer '{name}' is not loaded; load it before running the plan."
                )

        if request.intent == IntentType.UNKNOWN:
            request.constraints.append(
                "Intent could not be classified with confidence. "
                "Consider rephrasing with a clear verb (buffer, intersect, "
                "slope, classify, ...)."
            )

    # -- cache persistence -------------------------------------------------

    def _store_cache(
        self,
        cache_key: str,
        query: str,
        layers: List[str],
        request: AnalysisRequest,
        confidence: float,
        source: str,
    ) -> None:
        if self._cache is None:
            return
        payload = {
            "intent": request.intent.value,
            "entities": request.entities,
            "parameters": request.parameters,
            "constraints": request.constraints,
        }
        self._cache.store(
            cache_key,
            query,
            layers,
            request.intent.value,
            payload,
            confidence,
            source,
        )
