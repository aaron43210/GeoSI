# -*- coding: utf-8 -*-
"""
GeoSI plan examples — few-shot library for the LLM planner
══════════════════════════════════════════════════════════

Verified plans for request types small local models get wrong on their
own (wrong tool, swapped inputs, missing parameters). For each request the
most similar examples (embedding similarity with the same Ollama model the
tool retriever uses; keyword overlap as fallback) are shown in the prompt,
and their tools are guaranteed a place in the tool list.

Layer names in the examples are deliberately different from real data so
the model copies the pattern, not the names.
"""

from __future__ import annotations

import json
import logging
import math
import re
from typing import Dict, List, Optional

logger = logging.getLogger("geosi_engine.plan_examples")


def _step(tool: str, params: Dict, out: str = "step_1_output", sid: str = "step_1") -> Dict:
    return {"step_id": sid, "tool_name": tool, "parameters": params, "output_name": out}


EXAMPLES: List[Dict] = [
    {"query": "select schools that are inside districts",
     "steps": [_step("native_extractbylocation", {"INPUT": "schools", "PREDICATE": [6], "INTERSECT": "districts"})]},
    {"query": "find wells that intersect the floodplain",
     "steps": [_step("native_extractbylocation", {"INPUT": "wells", "PREDICATE": [0], "INTERSECT": "floodplain"})]},
    {"query": "find shops outside all parks",
     "steps": [_step("native_extractbylocation", {"INPUT": "shops", "PREDICATE": [2], "INTERSECT": "parks"})]},
    {"query": "find stations within 2 km of rivers",
     "steps": [_step("native_extractwithindistance", {"INPUT": "stations", "REFERENCE": "rivers", "DISTANCE": 2000})]},
    {"query": "add an area field to lakes",
     "steps": [_step("native_fieldcalculator", {"INPUT": "lakes", "FIELD_NAME": "area", "FIELD_TYPE": 0,
                                                "FORMULA": "$area"})]},
    {"query": "calculate the length of each river",
     "steps": [_step("native_fieldcalculator", {"INPUT": "rivers", "FIELD_NAME": "length", "FIELD_TYPE": 0,
                                                "FORMULA": "$length"})]},
    {"query": "create a 500 m grid of polygons covering farms",
     "steps": [_step("native_creategrid", {"TYPE": 2, "EXTENT": "farms", "HSPACING": 500, "VSPACING": 500,
                                           "CRS": "farms"})]},
    {"query": "what is the total population of all towns",
     "steps": [_step("qgis_basicstatisticsforfields", {"INPUT_LAYER": "towns", "FIELD_NAME": "population"})]},
    {"query": "how many roads are of type primary",
     "steps": [_step("native_extractbyattribute", {"INPUT": "roads", "FIELD": "type", "OPERATOR": 0,
                                                   "VALUE": "primary"})]},
    {"query": "extract buildings where height is greater than 20",
     "steps": [_step("native_extractbyexpression", {"INPUT": "buildings", "EXPRESSION": "\"height\" > 20"})]},
    {"query": "dissolve counties by state",
     "steps": [_step("native_dissolve", {"INPUT": "counties", "FIELD": ["state"]})]},
    {"query": "which park has the most trees",
     "steps": [_step("native_countpointsinpolygon", {"POLYGONS": "parks", "POINTS": "trees", "FIELD": "NUMPOINTS"})]},
    {"query": "count the trees in each park",
     "steps": [_step("native_countpointsinpolygon", {"POLYGONS": "parks", "POINTS": "trees", "FIELD": "NUMPOINTS"})]},
    {"query": "join each school to the district it falls in",
     "steps": [_step("native_joinattributesbylocation", {"INPUT": "schools", "JOIN": "districts", "PREDICATE": [0],
                                                         "METHOD": 1})]},
    {"query": "add the x and y coordinates of each well as fields",
     "steps": [_step("native_addxyfields", {"INPUT": "wells"})]},
    {"query": "convert lakes polygons to lines",
     "steps": [_step("native_polygonstolines", {"INPUT": "lakes"})]},
]


_LAYER_KEYS = {"INPUT", "INPUT_LAYER", "INTERSECT", "REFERENCE", "POLYGONS", "POINTS", "JOIN",
               "OVERLAY", "MASK", "EXTENT", "INPUT_A", "INPUT_B"}


def _layer_words(example: Dict) -> List[str]:
    """Layer names used by an example (values of its layer-type parameters)."""
    names = set()
    for st in example["steps"]:
        for key, v in st["parameters"].items():
            if key in _LAYER_KEYS and isinstance(v, str):
                names.add(v)
    return sorted(names, key=len, reverse=True)


def abstract(text: str, layer_names) -> str:
    """
    Replace layer names with "X" so similarity reflects the operation
    ("find X within 2 km of X"), not the topic ("flood" ~ "floodplain").
    """
    out = text.lower()
    for name in sorted({n.lower() for n in layer_names}, key=len, reverse=True):
        forms = {name, name.replace("_", " "), name.rstrip("s"), name.replace("_", " ").rstrip("s")}
        for form in sorted(forms, key=len, reverse=True):
            if len(form) > 2:
                out = re.sub(rf"\b{re.escape(form)}s?\b", "X", out)
    return out


def _words(text: str) -> set:
    return {w.rstrip("s") for w in re.findall(r"[a-z]+", text.lower()) if len(w) > 2}


class ExampleSelector:
    """Pick the examples most similar to a query."""

    def __init__(self, embed_fn=None):
        self._embed = embed_fn  # list[str] -> list[unit vectors]
        self._vectors: Optional[List[List[float]]] = None

    def _ensure(self) -> bool:
        if self._vectors is not None:
            return bool(self._vectors)
        self._vectors = []
        if self._embed is None:
            return False
        try:
            self._vectors = self._embed(
                [f"search_document: {abstract(e['query'], _layer_words(e))}" for e in EXAMPLES]
            )
        except Exception as e:
            logger.debug(f"example embedding unavailable: {e}")
            self._vectors = []
        return bool(self._vectors)

    def select(self, query: str, k: int = 3, layer_names=()) -> List[Dict]:
        return [e for e, _ in self.select_scored(query, k, layer_names)]

    def select_scored(self, query: str, k: int = 3, layer_names=()) -> List[tuple]:
        """[(example, similarity)] best first; similarity is cosine (or keyword overlap)."""
        scores: List[float]
        query = abstract(query, layer_names)
        if self._ensure():
            try:
                q = self._embed([f"search_query: {query}"])[0]
                scores = [sum(a * b for a, b in zip(q, v)) for v in self._vectors]
            except Exception:
                scores = []
        else:
            scores = []
        if not scores:
            qw = _words(query)
            scores = []
            for e in EXAMPLES:
                ew = _words(abstract(e["query"], _layer_words(e)))
                scores.append(len(qw & ew) / math.sqrt(1 + len(ew)))
        ranked = sorted(range(len(EXAMPLES)), key=lambda i: -scores[i])
        return [(EXAMPLES[i], scores[i]) for i in ranked[:k]]


def format_examples(examples: List[Dict]) -> str:
    blocks = []
    for e in examples:
        blocks.append(f'Request: "{e["query"]}"\nPlan: ' + json.dumps({"steps": e["steps"]}))
    return "\n\n".join(blocks)


# ── Template instantiation ──────────────────────────────────────────────
#
# When a request is a close paraphrase of a verified example, the example
# itself is the most reliable plan. Its layer names, distances, field names
# and values are mapped onto the request; if anything cannot be mapped the
# template is not used and the LLM plans instead.

_NUM_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(km|kilometers?|kilometres?|m|meters?|metres?)?\b", re.I)


def _numbers(text: str) -> List[tuple]:
    """[(value_in_metres_or_raw, raw_value)] in order of appearance."""
    out = []
    for m in _NUM_RE.finditer(text):
        raw = float(m.group(1))
        unit = (m.group(2) or "").lower()
        out.append((raw * 1000 if unit.startswith("k") else raw, raw))
    return out


def _mentions(text: str, names) -> List[str]:
    """Layer names mentioned in text, in order of first appearance."""
    low = text.lower()
    found = []
    for name in names:
        forms = {name.lower(), name.lower().replace("_", " "), name.lower().rstrip("s"),
                 name.lower().replace("_", " ").rstrip("s")}
        pos = [m.start() for f in forms if len(f) > 2 for m in re.finditer(rf"\b{re.escape(f)}", low)]
        if pos:
            found.append((min(pos), name))
    return [n for _, n in sorted(found)]


def instantiate(example: Dict, query: str, layers: Dict[str, object]) -> Optional[List[Dict]]:
    """
    Map an example's plan onto the query. layers: {name: Layer} of the
    project. Returns concrete steps, or None when the mapping is unclear.
    """
    ex_q = example["query"].lower()
    q = query.lower()
    ex_layers = _mentions(ex_q, _layer_words(example))
    q_layers = _mentions(q, list(layers))
    if len(q_layers) != len(ex_layers):
        return None
    layer_map = dict(zip(ex_layers, q_layers))

    ex_nums, q_nums = _numbers(ex_q), _numbers(q)
    if len(ex_nums) != len(q_nums):
        return None
    num_map = {}
    for (ex_m, ex_raw), (q_m, q_raw) in zip(ex_nums, q_nums):
        # Distances are metres in the plan: "2 km" (2000) → the query's metres
        num_map[ex_m] = q_m
        if ex_raw != ex_m:
            num_map.setdefault(ex_raw, q_raw)

    q_words = re.findall(r"[a-z0-9_]+", q, re.I)

    def field_of(layer_name: str) -> Optional[str]:
        fields = [f for f in (getattr(layers.get(layer_name), "fields", None) or []) if f != "fid"]
        for f in fields:
            if re.search(rf"\b{re.escape(f.lower())}\b", q):
                return f
        return None

    def value_after(field: str) -> Optional[str]:
        pattern = rf"\b{re.escape(field.lower())}\b\s*(?:is|=|==|equals|of)?\s*['\"]?([A-Za-z0-9_.-]+)"
        m = re.search(pattern, query, re.I)
        return m.group(1) if m else None

    steps = []
    for st in example["steps"]:
        params = {}
        input_layer = None
        for key, val in st["parameters"].items():
            if key == "CRS" and isinstance(val, str) and val in layer_map:
                params[key] = layer_map[val]
            elif isinstance(val, str) and val in layer_map:
                params[key] = layer_map[val]
                input_layer = input_layer or layer_map[val]
            elif isinstance(val, (int, float)) and not isinstance(val, bool) and key not in (
                    "PREDICATE", "TYPE", "FIELD_TYPE", "OPERATOR", "METHOD"):
                if float(val) in num_map:
                    params[key] = num_map[float(val)]
                elif num_map:
                    return None
                else:
                    params[key] = val
            elif isinstance(val, str) and key in ("EXPRESSION",):
                return None  # expressions need the LLM
            elif isinstance(val, (str, list)) and key in ("FIELD", "FIELD_NAME", "GROUP_BY") and \
                    any(isinstance(v, str) and v.lower() in ex_q and v.lower() not in q for v in
                        (val if isinstance(val, list) else [val])):
                f = field_of(input_layer) if input_layer else None
                if f is None:
                    return None
                params[key] = [f] if isinstance(val, list) else f
            elif isinstance(val, str) and key == "VALUE" and val.lower() in ex_q and val.lower() not in q:
                field = params.get("FIELD")
                v = value_after(field) if isinstance(field, str) else None
                if v is None:
                    return None
                params[key] = v
            else:
                params[key] = val
        steps.append({**st, "parameters": params})
    return steps if q_words else None
