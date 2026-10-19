# -*- coding: utf-8 -*-
"""
GeoSI Engine — Agent (v2: Dynamic Tool-Aware Planning)
═══════════════════════════════════════════════════════════════════

Plans GIS workflows using LLMs (Ollama → Gemini → Claude → rules).

KEY DIFFERENCE FROM v1:
    v1 had hardcoded tool names ("buffer", "intersect", "slope").
    v2 works with dynamically discovered names ("native_buffer", "gdal_slope").
    The agent uses the registry's alias index for fuzzy resolution,
    so "buffer" still works even though the canonical name is "native_buffer".

Architecture
────────────
    User Query
      ↓ parse()
    AnalysisRequest (intent, entities, parameters)
      ↓ plan()
    ExecutionPlan (steps with tool names + parameters)

Planning Priority:
    1. Well-understood ops (buffer, clip, ndvi) → rule-based (instant, reliable)
    2. Ollama (local LLM, no API key needed)
    3. Gemini (Google API)
    4. Claude (Anthropic API)
    5. Rule-based fallback (always works)

Data Structures
───────────────
    _OPERATION_TO_ALGORITHM: Dict mapping canonical ops → QGIS algorithm IDs
    Uses O(1) hash lookups throughout planning pipeline.
"""

import os
import json
import re
import logging
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher

from geosi_engine.models import (
    AnalysisRequest,
    ExecutionPlan,
    ToolStep,
    IntentType,
)
from geosi_engine.parser import QueryParser
from geosi_engine.registry import ToolRegistry
from geosi_engine.state import StateManager
from geosi_engine.validation import ValidationEngine, ValidationReport
from geosi_engine.conversation import ConversationManager

logger = logging.getLogger("geosi_engine.agent")


# ═══════════════════════════════════════════════════════════════════════════
# OPERATION → QGIS ALGORITHM MAPPING
#
# Maps canonical operation names (from the parser) to QGIS algorithm IDs.
# These are the ACTUAL IDs that processing.run() expects.
#
# The registry's alias index means we can use either format:
#   - "native_buffer" (canonical, from auto-discovery)
#   - "buffer" (alias, resolved by ToolRegistry._alias_index)
#
# Complexity: O(1) dict lookup per operation
# ═══════════════════════════════════════════════════════════════════════════

_OPERATION_TO_ALGORITHM: Dict[str, str] = {
    # ── Vector operations ──────────────────────────────────────────────
    "buffer":               "native_buffer",
    "intersect":            "native_intersection",
    "clip":                 "native_clip",
    "union":                "native_union",
    "difference":           "native_difference",
    "symmetric_difference": "native_symmetricaldifference",
    "dissolve":             "native_dissolve",
    "centroid":             "native_centroids",
    "fix_geometries":       "native_fixgeometries",
    "simplify":             "native_simplifygeometries",
    "convex_hull":          "native_minimumboundinggeometry",
    "voronoi":              "native_voronoipolygons",
    "reproject":            "native_reprojectlayer",
    "join_attributes":      "native_joinattributestable",
    "extract_by_attribute": "native_extractbyattribute",

    # ── Raster / Terrain operations ────────────────────────────────────
    "slope":                "native_slope",
    "aspect":               "native_aspect",
    "hillshade":            "native_hillshade",
    "contour":              "gdal_contour",
    "raster_calc":          "native_rastercalc",

    # ── NDVI / NDWI (spectral indices) ─────────────────────────────────
    "ndvi":                 "native_rastercalc",
    "ndwi":                 "native_rastercalc",

    # ── Network ────────────────────────────────────────────────────────
    "shortest_path":        "native_shortestpathpointtopoint",

    # ── Statistics ─────────────────────────────────────────────────────
    "count_features":       "native_countfeaturesinregions",

    # ── Cartography ────────────────────────────────────────────────────
    "export_geojson":       "native_savefeatures",
}

# ── Default plan templates per intent (fallback when LLM is unavailable)
_DEFAULT_PLANS: Dict[IntentType, List[str]] = {
    IntentType.PROXIMITY:       ["buffer", "intersect"],
    IntentType.OVERLAY:         ["intersect"],
    IntentType.GEOMETRY:        ["dissolve"],
    IntentType.RASTER:          ["raster_calc"],
    IntentType.TERRAIN:         ["slope"],
    IntentType.NETWORK:         ["shortest_path"],
    IntentType.AI_ML:           ["count_features"],
    IntentType.CARTOGRAPHY:     ["export_geojson"],
    IntentType.STATISTICS:      ["count_features"],
    IntentType.DATA_MANAGEMENT: ["reproject"],
    IntentType.VALIDATION:      ["count_features"],
    IntentType.TEMPORAL:        ["count_features"],
    IntentType.UNKNOWN:         ["count_features"],
}


class GeoSIAgent:
    """
    Plans multi-step GIS workflows using LLMs + rule-based fallback.
    Works exclusively with layers available in the QGIS layer panel.

    v2 Enhancement: Tool names are resolved dynamically through the
    ToolRegistry's alias system, so the agent doesn't need to know
    whether "buffer" maps to "native_buffer" or "qgis_buffer".

    Phase 2 Enhancement: Optional KnowledgeManager integration provides
    contextual GIS documentation, similar past workflows, and feedback
    signals before planning.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        use_llm: bool = True,
        conversation: Optional[ConversationManager] = None,
        knowledge=None,
    ):
        self.registry = registry
        self.parser = QueryParser(use_llm=use_llm)
        self.validator = ValidationEngine()
        self.use_llm = use_llm
        self.conversation = conversation or ConversationManager(
            system_prompt="You are GeoSI, a GIS workflow planner."
        )
        self._ollama_endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
        self._ollama_model = self._detect_ollama_model()
        self._tool_retriever = None  # created lazily; see _relevant_tools()
        # Optional hosted model behind an OpenAI-compatible API (OpenAI, Groq,
        # OpenRouter, Together, LM Studio, ...). When set it is used for
        # planning and answers before Ollama; tool search stays local.
        self._api_base = os.environ.get("GEOSI_LLM_BASE_URL", "").rstrip("/")
        self._api_key = os.environ.get("GEOSI_LLM_API_KEY", "")
        self._api_model = os.environ.get("GEOSI_LLM_MODEL", "")
        self._anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self._gemini_key = (
            os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
            or ""
        )
        self.layer_suggestions: Optional[List[Tuple[str, float]]] = None

        # ── Phase 2: Knowledge Layer ───────────────────────────────────
        # Optional KnowledgeManager for RAG-enhanced planning
        self.knowledge = knowledge
        self._last_knowledge_context = None

    # ── LLM detection ─────────────────────────────────────────────────

    def _detect_ollama_model(self) -> str:
        model = os.environ.get("OLLAMA_MODEL", "mistral")
        try:
            import urllib.request
            import json
            req = urllib.request.Request(f"{self._ollama_endpoint}/api/tags")
            with urllib.request.urlopen(req, timeout=1.5) as resp:  # nosec B310
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    models = [m.get("name") for m in data.get("models", [])]
                    # Embedding-only models cannot generate plans
                    models = [m for m in models if m and "embed" not in m]
                    if models and model not in models and f"{model}:latest" not in models:
                        for pref in ["llama3.2:3b", "llama3:latest", "llama3", "qwen2.5-coder:14b", "mistral"]:
                            if pref in models:
                                return pref
                        return models[0]
        except Exception:
            logger.debug("suppressed exception", exc_info=True)
        return model

    # ── Public API ─────────────────────────────────────────────────────

    def parse(self, query: str, state: StateManager) -> AnalysisRequest:
        """Parse a natural language query into an AnalysisRequest."""
        layer_names = state.list_layers() if state else []
        return self.parser.parse(query, layer_names)

    def plan(
        self,
        request: AnalysisRequest,
        state: Optional[StateManager] = None,
        feedback: Optional[str] = None,
    ) -> ExecutionPlan:
        """
        Create an ExecutionPlan from an AnalysisRequest.

        Priority:
            1. Retrieve knowledge context (Phase 2)
            2. Validate layers exist
            3. Well-understood ops → rule-based (skip LLM)
            4. Ollama → Gemini → Claude → rule-based fallback
        """
        self._prompt_state = state

        # ── Phase 2: Retrieve knowledge context ────────────────────────
        self._last_knowledge_context = None
        if self.knowledge:
            try:
                self._last_knowledge_context = self.knowledge.retrieve_context(
                    request.query
                )
                logger.info(
                    f"Knowledge context: {self._last_knowledge_context}"
                )
            except Exception as e:
                logger.warning(f"Knowledge retrieval failed: {e}")

        # ── Validate layers exist in QGIS ──────────────────────────────
        if state:
            valid, error_msg = self.validate_layers_exist(request, state)
            if not valid:
                return ExecutionPlan(
                    request=request, steps=[],
                    reasoning=error_msg or "Layer validation failed",
                )

        # ── Well-understood operations: skip LLM entirely ──────────────
        operation = request.parameters.get("operation", "")
        well_understood = {
            "clip", "buffer", "intersect", "union", "difference",
            "dissolve", "centroid", "convex_hull", "simplify", "voronoi", "fix_geometries",
            "slope", "aspect", "hillshade", "contour",
            "ndvi", "ndwi", "reproject", "join_attributes",
            "extract_by_attribute",
        }
        # A retry from the agent loop always goes to the LLM with the
        # problem from the previous attempt; rules would repeat themselves.
        if operation in well_understood and not feedback and self._is_simple_request(request.query):
            logger.info(f"Op '{operation}' well-understood → rule-based plan")
            plan = self._plan_with_rules(request)
            plan.plan_source = "rule_based"
            return plan

        # ── Deterministic shortcuts tried before the LLM ───────────────
        if not feedback:
            for planner in (self._plan_field_statistics, self._plan_attribute_filter,
                            self._plan_grid, self._plan_merge, self._plan_from_template):
                plan = planner(request, state)
                if plan is not None:
                    logger.info(f"Deterministic plan: {plan.reasoning}")
                    if planner != self._plan_from_template:
                        plan.plan_source = "deterministic"
                    return plan

        # ── LLM cascade ────────────────────────────────────────────────
        # Each provider is guarded by the Supervisor's circuit breaker when
        # one is attached (``breakers``): a provider that keeps failing is
        # skipped until its reset window passes.
        self._prompt_state = state
        self._feedback = feedback
        breakers = getattr(self, "breakers", None) or {}
        try:
            if self.use_llm:
                for name, fn in self._llm_providers():
                    breaker = breakers.get(name)
                    if breaker is not None and not breaker.is_available():
                        logger.info(f"Skipping {name}: circuit breaker open")
                        continue
                    try:
                        plan = fn(request)
                    except Exception as e:
                        if breaker is not None:
                            breaker.record_failure()
                        logger.warning(f"{name} planning failed: {e}")
                        continue
                    if breaker is not None:
                        breaker.record_success()
                    plan.plan_source = f"{name}:{self._provider_model(name)}"
                    if self._validate_plan_layers(plan, request.available_layers):
                        return plan
                    logger.warning(f"{name} plan referenced nonexistent layers")
        finally:
            self._feedback = None

        if feedback:
            return ExecutionPlan(request=request, steps=[], reasoning="Re-planning failed",
                                 plan_source="none")
        plan = self._plan_with_rules(request)
        plan.plan_source = "rule_based"
        return plan

    def _provider_model(self, name: str) -> str:
        return {
            "api": self._api_model,
            "ollama": self._ollama_model,
            "gemini": os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
            "anthropic": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
        }.get(name, "")

    def _state_layer(self, name):
        state = getattr(self, "_prompt_state", None)
        return state.get_layer(name) if state and name else None

    _COMPOUND_RE = re.compile(
        r"\b(and then|then|after that|followed by|and (?:also )?(?:buffer|clip|dissolve|intersect|"
        r"reproject|select|extract|count|add|calculate|compute|merge|join|centroid|simplify)|"
        r"by (?!\d)[a-z_]+|per [a-z_]+|for each|where|with (?:a|an) [a-z_]+ field|outside|not in)\b",
        re.IGNORECASE,
    )

    def _is_simple_request(self, query: str) -> bool:
        """
        Rules only know one operation with default options. Anything with a
        second operation ("... and dissolve"), a grouping field ("by owner")
        or a condition ("where", "outside") goes to the LLM instead.
        """
        return not self._COMPOUND_RE.search(query or "")

    def can_replan(self) -> bool:
        """True when an LLM is reachable to produce a corrected plan."""
        if not self.use_llm:
            return False
        if self._gemini_key or self._anthropic_key or self._api_configured():
            return True
        try:
            import requests
            return requests.get(f"{self._ollama_endpoint}/api/tags", timeout=1.5).ok
        except Exception:
            return False

    def answer_from_evidence(self, question: str, evidence: str) -> Optional[str]:
        """Answer a question in plain words from result data (local LLM)."""
        if not self.use_llm:
            return None
        prompt = (
            "You are GeoSI, a GIS assistant. Answer the user's question using ONLY the "
            "data below. Do the arithmetic yourself (count rows, sum values) and give "
            "exact numbers and names. Reply in one or two short sentences.\n\n"
            f"DATA:\n{evidence[:6000]}\n\nQUESTION: {question}\nANSWER:"
        )
        if self._api_configured():
            try:
                return self._api_chat(prompt, json_mode=False).strip() or None
            except Exception as e:
                logger.warning(f"API answer failed, trying Ollama: {e}")
        try:
            import requests
            resp = requests.post(
                f"{self._ollama_endpoint}/api/generate",
                json={"model": self._ollama_model, "prompt": prompt, "stream": False,
                      "options": {"temperature": 0.0}},
                timeout=120,
            )
            resp.raise_for_status()
            text = resp.json().get("response", "").strip()
            return text or None
        except Exception as e:
            logger.warning(f"Answering from evidence failed: {e}")
            return None

    # ── LLM provider list ──────────────────────────────────────────────

    def _llm_providers(self):
        """Yield (name, callable) tuples for available LLM providers."""
        if self._api_configured():
            yield ("api", self._plan_with_api)
        yield ("ollama", self._plan_with_ollama)
        if self._gemini_key:
            yield ("gemini", self._plan_with_gemini)
        if self._anthropic_key:
            yield ("anthropic", self._plan_with_anthropic)

    # ── Layer validation ───────────────────────────────────────────────

    def find_similar_layers(
        self, layer_name: str, available_layers: List[str], threshold: float = 0.6
    ) -> List[Tuple[str, float]]:
        """
        Find similar layer names using SequenceMatcher fuzzy matching.

        Algorithm: Pairwise string similarity via Ratcliff/Obershelp
        Complexity: O(A * L) where A = available layers, L = avg name length
        """
        if not available_layers or not layer_name:
            return []
        matches = []
        layer_lower = layer_name.lower()
        for available in available_layers:
            available_lower = available.lower()
            if available_lower == layer_lower:
                matches.append((available, 1.0))
            else:
                ratio = SequenceMatcher(None, layer_lower, available_lower).ratio()
                if ratio >= threshold:
                    matches.append((available, ratio))
        return sorted(matches, key=lambda x: x[1], reverse=True)

    # Patterns that indicate the query doesn't need any loaded layers.
    _LAYER_FREE_RE = re.compile(
        r"""
        ^(?:hi|hello|hey|howdy|greetings?|help|what\s+can\s+you|who\s+are\s+you) |
        \b(?:generate|write|create|show|give\s+me|make)\b.{0,40}
            \b(?:code|script|example|snippet|template|function|class)\b |
        \b(?:what\s+is|what\s+are|how\s+(?:do\s+I|to)|explain|describe|define|tell\s+me\s+about)\b |
        \b(?:list\s+(?:all\s+)?(?:tools?|algorithms?|operations?|capabilities?)) |
        \b(?:NDVI|NDWI|CRS|WGS|EPSG|GeoJSON|shapefile|GeoPackage|FlatGeobuf|WKT|WKB|
           raster|vector|polygon|linestring|geometry|projection|reprojection|
           coordinate|spatial\s+join|dissolve|buffer|clip|intersect)\b(?![^?]*\blayer\b)
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def _query_needs_layers(self, query: str) -> bool:
        """Return False when the query is conversational / educational / code-gen."""
        if self._LAYER_FREE_RE.search(query or ""):
            return False
        # Any spatial verb + named layer → needs layers
        spatial_verbs = re.compile(
            r"\b(buffer|clip|dissolve|intersect|reproject|select|extract|join|"
            r"merge|union|difference|count|centroid|convex.hull|simplify|fix|"
            r"rasterize|polygonize|calculate|compute|aggregate)\b",
            re.IGNORECASE,
        )
        return bool(spatial_verbs.search(query or ""))

    def validate_layers_exist(
        self, request: AnalysisRequest, state: StateManager
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate that requested layers exist in the QGIS project.
        Returns (is_valid, error_message).

        Conversational queries, code-generation requests, and educational
        GIS questions bypass the "no layers loaded" check entirely.
        """
        if not state:
            return False, "No state manager available"

        # Don't block the response for layer-free intents
        if not self._query_needs_layers(request.query or ""):
            return True, None

        available = state.list_layers()
        if not available:
            return False, (
                "No layers loaded. Please load a shapefile first, or "
                "reference one by filename."
            )

        # Check primary layer exists
        primary = request.entities.get("primary_layer")
        if primary:
            primary_lower = primary.lower()
            primary_stem = os.path.splitext(primary_lower)[0]
            available_lower = [l.lower() for l in available]
            available_stems = [os.path.splitext(l)[0].lower() for l in available]

            matched = (
                primary_lower in available_lower
                or primary_stem in available_lower
                or primary_lower in available_stems
                or primary_stem in available_stems
            )
            if not matched:
                similar = self.find_similar_layers(primary, available, 0.5)
                self.layer_suggestions = similar
                if similar:
                    suggestions = ", ".join(
                        f"'{s[0]}' ({s[1]:.0%} match)" for s in similar[:3]
                    )
                    return False, f"Layer '{primary}' not found. Did you mean: {suggestions}?"
                layers_list = "\n  - ".join(available)
                return False, f"Layer '{primary}' not found.\n\nAvailable layers:\n  - {layers_list}"

        return True, None

    # ── Rule-based planning ────────────────────────────────────────────

    def _resolve_tool_name(self, operation: str) -> Optional[str]:
        """
        Resolve a canonical operation name to a registered tool name.

        Strategy (O(1) each step, stops at first hit):
            1. Direct lookup in _OPERATION_TO_ALGORITHM
            2. Direct lookup in registry (exact name or alias)
            3. Fallback: try "native_" prefix

        Args:
            operation: Canonical op name (e.g. "buffer", "clip")

        Returns:
            Registered tool name or None
        """
        # 1. Check our mapping table
        mapped = _OPERATION_TO_ALGORITHM.get(operation)
        if mapped and self.registry.get_tool(mapped):
            return mapped

        # 2. Try direct registry lookup (uses alias index)
        if self.registry.get_tool(operation):
            return operation

        # 3. Try with native_ prefix
        native_name = f"native_{operation}"
        if self.registry.get_tool(native_name):
            return native_name

        return None

    def _plan_with_rules(self, request: AnalysisRequest) -> ExecutionPlan:
        """
        Create a plan using rule-based pattern matching.

        This is the most reliable planner — it handles all well-understood
        GIS operations without needing an LLM.
        """

        # Conversational, educational, or code-generation queries should not
        # receive a dummy spatial step like count_features.
        if not self._query_needs_layers(request.query or ""):
            return ExecutionPlan(
                request=request,
                steps=[],
                reasoning="Conversational / code-generation query — handled by conversation engine",
                plan_source="conversational",
            )

        # ── Determine which operations to run ──────────────────────────
        operation = request.parameters.get("operation", "")
        if operation:
            op_names = [operation]
        else:
            op_names = _DEFAULT_PLANS.get(request.intent, ["count_features"])

        steps = []
        for i, op_name in enumerate(op_names):
            # Resolve to a registered tool name
            tool_name = self._resolve_tool_name(op_name)
            if not tool_name:
                logger.warning(f"Could not resolve operation '{op_name}' to a tool")
                continue

            tool = self.registry.get_tool(tool_name)
            if not tool:
                continue

            spec = tool.spec()
            params = {}
            desc_parts = [spec.display_name]

            # ── Fill parameters based on operation type ─────────────────
            primary = request.entities.get("primary_layer") or request.entities.get("layer")
            # Word order decides roles: "clip A to B" → INPUT A, OVERLAY B
            state = getattr(self, "_prompt_state", None)
            mentioned = self._mentioned_layers(request.query, state) if state else []
            if mentioned:
                primary = mentioned[0]
                if len(mentioned) > 1:
                    request.entities["secondary_layer"] = mentioned[1]
            primary_layer = self._state_layer(primary)
            is_raster = getattr(primary_layer, "layer_type", "") == "raster"

            # Raster inputs need the GDAL raster equivalents of vector ops
            raster_tool = {
                "reproject": "gdal_warpreproject",
                "clip": "gdal_cliprasterbymasklayer",
            }.get(op_name) if is_raster else None
            if raster_tool and self.registry.get_tool(raster_tool):
                tool_name = raster_tool
                spec = self.registry.get_tool(raster_tool).spec()

            # Set the first parameter (usually INPUT) to the primary layer
            if spec.parameters:
                params[spec.parameters[0].name] = primary
            else:
                params["INPUT"] = primary

            # Operation-specific parameter wiring
            if op_name == "buffer":
                dist = request.parameters.get("distance_value")
                if dist:
                    params["DISTANCE"] = dist
                    desc_parts.append(f"by {dist}m")

            elif op_name == "clip" and tool_name == "gdal_cliprasterbymasklayer":
                mask = request.entities.get("secondary_layer") or next(
                    (l for l in (request.available_layers or []) if l != primary
                     and getattr(self._state_layer(l), "layer_type", "") == "vector"), None)
                if mask:
                    params["MASK"] = mask
                    params["CROP_TO_CUTLINE"] = True
                    desc_parts.append(f"to {mask}")

            elif op_name == "convex_hull":
                params["TYPE"] = 3  # one convex hull around all features

            elif op_name == "contour":
                m = re.search(r"(?:every|interval(?: of)?)\s+(\d+(?:\.\d+)?)", request.query or "", re.I)
                params["INTERVAL"] = float(m.group(1)) if m else 10.0
                desc_parts.append(f"every {params['INTERVAL']:g}")

            elif op_name in ("intersect", "clip", "union", "difference", "symmetric_difference"):
                overlay = request.entities.get("secondary_layer")
                if overlay:
                    params["OVERLAY"] = overlay
                    desc_parts.append(f"with {overlay}")
                else:
                    for layer in (request.available_layers or []):
                        if layer.lower() != (primary or "").lower():
                            params["OVERLAY"] = layer
                            desc_parts.append(f"with {layer}")
                            break

            elif op_name == "reproject":
                match = re.search(r"(?i)(EPSG:\d+)", request.query or "")
                if match:
                    params["TARGET_CRS"] = match.group(1).upper()
                    desc_parts.append(f"to {params['TARGET_CRS']}")

            elif op_name == "extract_by_attribute":
                filters = request.parameters.get("filters", [])
                if filters:
                    params["FIELD"] = filters[0]["field"]
                    params["VALUE"] = filters[0]["value"]
                    params["OPERATOR"] = 0

            elif op_name in ("ndvi", "ndwi") and is_raster and self.registry.get_tool("gdal_rastercalculator"):
                # One multi-band image: (A - B) / (A + B) with band numbers
                # taken from the query ("band 3 as red", "band 4 as NIR").
                q = (request.query or "").lower()
                def band_for(name, default):
                    m = re.search(rf"band\s*(\d+)\s*(?:as|=|is|for)\s*(?:the\s*)?{name}", q) or \
                        re.search(rf"{name}\s*(?:band)?\s*(?:=|is|:)?\s*(?:band\s*)?(\d+)", q)
                    return int(m.group(1)) if m else default
                if op_name == "ndvi":
                    a, b = band_for("nir", 4), band_for("red", 3)
                else:
                    a, b = band_for("green", 2), band_for("nir", 4)
                tool_name = "gdal_rastercalculator"
                params = {"INPUT_A": primary, "BAND_A": a, "INPUT_B": primary, "BAND_B": b,
                          "FORMULA": "(A.astype(float)-B)/(A.astype(float)+B)", "RTYPE": 5}
                desc_parts = [f"{op_name.upper()} from bands {a} and {b} of {primary}"]

            elif op_name in ("ndvi", "ndwi"):
                available = request.available_layers or []
                red = primary or (available[0] if available else "")
                nir = request.entities.get("secondary_layer") or (available[1] if len(available) > 1 else "")
                b4 = [l for l in available if "B4" in l.upper()]
                b5 = [l for l in available if "B5" in l.upper()]
                if b4 and b5:
                    red, nir = b4[0], b5[0]
                if op_name == "ndvi":
                    params["RED_BAND"] = red
                    params["NIR_BAND"] = nir
                else:
                    params["GREEN_BAND"] = red
                    params["NIR_BAND"] = nir
                desc_parts.append(f"using {red} and {nir}")

            elif op_name in ("slope", "aspect", "hillshade", "contour"):
                pass  # Terrain tools only need INPUT (DEM)

            step = ToolStep(
                step_id=f"step_{i + 1}",
                tool_name=tool_name,
                parameters=params,
                output_name=f"step_{i + 1}_output",
                description=" ".join(desc_parts),
            )
            steps.append(step)

        return ExecutionPlan(
            request=request, steps=steps,
            reasoning="Rule-based plan (reliable, no LLM needed)",
        )

    # ── LLM-based planning ─────────────────────────────────────────────

    _STOPWORDS = frozenset(
        "a an the of in on to by for from with and or each every all into "
        "within inside using use layer layers my me please create make get "
        "find show calculate compute run do".split()
    )

    def _relevant_tools(self, query: str, top_k: int = 12) -> List[str]:
        """
        Pick the tools to show the LLM: semantic search over tool
        descriptions with the Ollama embedding model, falling back to
        keyword overlap when no embedding model is available.
        """
        if self._tool_retriever is None:
            from geosi_engine.tool_retriever import ToolRetriever
            self._tool_retriever = ToolRetriever(self.registry, endpoint=self._ollama_endpoint)
        ranked = self._tool_retriever.rank(query, top_k=top_k)
        return ranked or self._rank_tools_for_query(query)[:top_k]

    _OUTSIDE_RE = re.compile(r"\b(outside|not (?:in|inside|within)|away from|disjoint|beyond)\b", re.I)
    _INSIDE_RE = re.compile(r"\b(inside|within|in|intersect(?:s|ing)?|overlap(?:s|ping)?|falls? in|located in)\b", re.I)

    _TEMPLATE_MIN_SIMILARITY = 0.84
    _STAT_RE = re.compile(
        r"\b(total|sum|average|mean|median|minimum|maximum|min|max|highest|lowest|largest|smallest|"
        r"biggest|statistics|stats)\b", re.I)

    def _plan_field_statistics(self, request, state) -> Optional[ExecutionPlan]:
        """"total beds across hospitals" → basic statistics of hospitals.beds."""
        query = request.query or ""
        if not state or not self._STAT_RE.search(query):
            return None
        tool = "native_basicstatisticsforfields"
        if not self.registry.get_tool(tool):
            tool = "qgis_basicstatisticsforfields"
            if not self.registry.get_tool(tool):
                return None
        mentioned = self._mentioned_layers(query, state)
        # "mean elevation within each zone" is zonal statistics, not a whole-raster summary
        per_zone = bool(re.search(r"\b(each|every|per|by)\b", query, re.I)) or any(
            state.get_layer(n).layer_type == "vector" for n in mentioned)
        for name in mentioned:
            layer = state.get_layer(name)
            if layer.layer_type == "raster" and per_zone:
                continue
            if layer.layer_type == "raster" and self.registry.get_tool("native_rasterlayerstatistics"):
                return self._one_step_plan(request, "native_rasterlayerstatistics",
                                           {"INPUT": name, "BAND": 1}, f"Raster statistics of {name}")
            for f in (getattr(layer, "fields", None) or []):
                if f != "fid" and re.search(rf"\b{re.escape(f)}\b", query, re.I):
                    return self._one_step_plan(request, tool, {"INPUT_LAYER": name, "FIELD_NAME": f},
                                               f"Field statistics for {name}.{f}")
        # "highest elevation" style questions about the only raster
        rasters = [n for n in state.list_layers() if state.get_layer(n).layer_type == "raster"]
        if len(rasters) == 1 and not per_zone and re.search(r"\b(elevation|height|value|pixel)s?\b", query, re.I) \
                and self.registry.get_tool("native_rasterlayerstatistics"):
            return self._one_step_plan(request, "native_rasterlayerstatistics",
                                       {"INPUT": rasters[0], "BAND": 1}, f"Raster statistics of {rasters[0]}")
        return None

    # ── more deterministic planners ───────────────────────────────────

    def _one_step_plan(self, request, tool, params, why) -> ExecutionPlan:
        step = ToolStep(step_id="step_1", tool_name=tool, parameters=params,
                        output_name="step_1_output", description=why)
        return ExecutionPlan(request=request, steps=[step], reasoning=why)

    @staticmethod
    def _mentioned_layers(query: str, state) -> List[str]:
        """Loaded layers named in the query, in order of appearance."""
        low = (query or "").lower()
        found = []
        for name in state.list_layers():
            n = name.lower()
            forms = {n, n.replace("_", " "), n.rstrip("s"), n.replace("_", " ").rstrip("s")}
            spans = [(m.start(), m.end()) for f in forms if len(f) > 2
                     for m in re.finditer(rf"\b{re.escape(f)}(?![a-z0-9])", low)]
            if spans:
                found.append((min(spans), name))
        # A shorter name inside a longer match ("roads" in "roads_buffer") is not a mention
        found.sort(key=lambda x: (x[0][0], -(x[0][1] - x[0][0])))
        out, taken = [], []
        for (start, end), name in found:
            if any(a <= start < b for a, b in taken):
                continue
            taken.append((start, end))
            out.append(name)
        return out

    _CMP_WORDS = [
        (r"(?:more than|greater than|over|above|higher than|>)", ">"),
        (r"(?:at least|>=|no less than)", ">="),
        (r"(?:less than|fewer than|under|below|lower than|<)", "<"),
        (r"(?:at most|<=|no more than)", "<="),
        (r"(?:equal to|equals|=|==)", "="),
    ]
    _FILTER_VERB_RE = re.compile(
        r"\b(find|extract|select|give|list|show|get|keep|filter|which|how many|how (?:long|big|large|far|much)|"
        r"count|where|with|owned|whose|of type|that have|having)\b", re.I)

    def _plan_attribute_filter(self, request, state) -> Optional[ExecutionPlan]:
        """
        "hospitals with more than 100 beds", "parcels owned by C", "road R1":
        a numeric comparison on a field, or a word that is an actual value of
        a text field → extract by expression. Skipped when the request names
        another operation (buffer, dissolve, ...), which goes to its planner.
        """
        query = request.query or ""
        if not state or not self._FILTER_VERB_RE.search(query):
            return None
        op = request.parameters.get("operation")
        if op and op not in ("extract_by_attribute", "clip"):
            return None
        tool = "native_extractbyexpression"
        if not self.registry.get_tool(tool):
            return None
        for name in self._mentioned_layers(query, state):
            layer = state.get_layer(name)
            if layer.layer_type != "vector":
                continue
            types = getattr(layer, "field_types", {}) or {}
            # numeric comparison: "more than 200 beds" / "beds greater than 200"
            for f, ftype in types.items():
                if ftype != "number":
                    continue
                fpat = re.escape(f).rstrip("s") + "s?"
                for words, sym in self._CMP_WORDS:
                    m = (re.search(rf"\b{words}\s+(-?\d+(?:\.\d+)?)\s+{fpat}\b", query, re.I)
                         or re.search(rf"\b{fpat}\s+(?:is\s+|are\s+)?{words}\s+(-?\d+(?:\.\d+)?)", query, re.I))
                    if m:
                        expr = f'"{f}" {sym} {m.group(1)}'
                        return self._one_step_plan(request, tool, {"INPUT": name, "EXPRESSION": expr},
                                                   f"Filter {name} where {expr}")
            # value match: a query token that is a real value of a text field
            tokens = re.findall(r"[A-Za-z0-9_.-]+", query)
            layer_words = {w for n in state.list_layers() for w in re.split(r"[_\s]", n.lower())}
            for f, values in (getattr(layer, "field_values", {}) or {}).items():
                for v in values:
                    sv = str(v)
                    if sv.lower() in layer_words:
                        continue
                    hit = sv in tokens if len(sv) > 1 or sv.isupper() else False
                    if len(sv) > 1 and not hit:
                        hit = sv.lower() in (t.lower() for t in tokens)
                    if hit:
                        expr = f'"{f}" = \'{sv}\''
                        return self._one_step_plan(request, tool, {"INPUT": name, "EXPRESSION": expr},
                                                   f"Filter {name} where {expr}")
        return None

    _GRID_TYPES = [("hexagon", 4), ("diamond", 3), ("point", 0), ("line", 1)]

    def _plan_grid(self, request, state) -> Optional[ExecutionPlan]:
        """"a 2 km hexagon grid over flood_zones" → native:creategrid."""
        query = request.query or ""
        if not state or not re.search(r"\bgrid\b", query, re.I) or not self.registry.get_tool("native_creategrid"):
            return None
        spacing = request.parameters.get("distance_value")
        layers = self._mentioned_layers(query, state)
        if not spacing or not layers:
            return None
        gtype = next((t for word, t in self._GRID_TYPES if re.search(rf"\b{word}", query, re.I)), 2)
        params = {"TYPE": gtype, "EXTENT": layers[0], "HSPACING": spacing, "VSPACING": spacing, "CRS": layers[0]}
        return self._one_step_plan(request, "native_creategrid", params,
                                   f"Grid (type {gtype}) of {spacing:g} m over {layers[0]}")

    def _plan_merge(self, request, state) -> Optional[ExecutionPlan]:
        """"merge A and B into one layer" → native:mergevectorlayers."""
        query = request.query or ""
        if not state or not re.search(r"\b(merge|combine|append)\b", query, re.I) \
                or not self.registry.get_tool("native_mergevectorlayers"):
            return None
        layers = [n for n in self._mentioned_layers(query, state) if state.get_layer(n).layer_type == "vector"]
        if len(layers) < 2:
            return None
        return self._one_step_plan(request, "native_mergevectorlayers", {"LAYERS": layers},
                                   f"Merge {', '.join(layers)}")

    def _plan_from_template(self, request, state) -> Optional[ExecutionPlan]:
        """Use a verified example directly when the request closely paraphrases it."""
        if not state:
            return None
        self._prompt_state = state
        from geosi_engine.plan_examples import instantiate
        self._examples_for(request.query, k=1)  # builds the selector
        scored = self._example_selector.select_scored(request.query, 1, state.list_layers())
        if not scored or scored[0][1] < self._TEMPLATE_MIN_SIMILARITY:
            return None
        example, score = scored[0]
        layers = {n: state.get_layer(n) for n in state.list_layers()}
        steps = instantiate(example, request.query, layers)
        if not steps:
            return None
        for st in steps:
            name = st["tool_name"]
            if not self.registry.get_tool(name):
                alt = ("native_" + name[5:]) if name.startswith("qgis_") else ("qgis_" + name[7:])
                if not self.registry.get_tool(alt):
                    return None
                st["tool_name"] = alt
        plan = ExecutionPlan(
            request=request,
            steps=[ToolStep(step_id=st["step_id"], tool_name=st["tool_name"], parameters=dict(st["parameters"]),
                            output_name=st["output_name"], description=f"As in: {example['query']}")
                   for st in steps],
            reasoning=f"Matched verified example '{example['query']}' (similarity {score:.2f})",
            plan_source="template",
        )
        if not self._validate_plan_layers(plan, request.available_layers):
            return None
        logger.info(plan.reasoning)
        return plan

    def _repair_spatial_predicate(self, step, spec_params, request) -> None:
        """
        The spatial relationship comes from the user's words, not the model:
        small models often pick the wrong PREDICATE index (e.g. disjoint for
        "inside"). Option text is mapped to the index by the QGIS bridge.
        """
        if "PREDICATE" not in {p.name for p in spec_params} or request is None:
            return
        query = request.query or ""
        if self._OUTSIDE_RE.search(query):
            step.parameters["PREDICATE"] = "disjoint"
        elif self._INSIDE_RE.search(query):
            step.parameters["PREDICATE"] = "intersect"

    def _examples_for(self, query: str, k: int = 3) -> List[Dict]:
        """Most similar verified plans from the few-shot library."""
        if getattr(self, "_example_selector", None) is None:
            from geosi_engine.plan_examples import ExampleSelector
            if self._tool_retriever is None:
                from geosi_engine.tool_retriever import ToolRetriever
                self._tool_retriever = ToolRetriever(self.registry, endpoint=self._ollama_endpoint)
            self._example_selector = ExampleSelector(embed_fn=self._tool_retriever._embed)
        state = getattr(self, "_prompt_state", None)
        layer_names = state.list_layers() if state else []
        usable = []
        for e in self._example_selector.select(query, k=k + 2, layer_names=layer_names):
            # QGIS 3 vs 4 moved some algorithms between qgis: and native:
            steps = []
            for st in e["steps"]:
                name = st["tool_name"]
                alt = ("native_" + name[5:]) if name.startswith("qgis_") else ("qgis_" + name[7:])
                name = name if self.registry.get_tool(name) else alt
                if not self.registry.get_tool(name):
                    break
                steps.append({**st, "tool_name": name})
            else:
                usable.append({**e, "steps": steps})
        return usable[:k]

    def _rank_tools_for_query(self, query: str) -> List[str]:
        """
        Rank tool names by keyword overlap with the query.

        Name/display-name/tag hits weigh 3, description hits 1; native QGIS
        algorithms get a small boost as the most reliable providers.
        Complexity: O(N * W) for N tools and W query words.
        """
        words = {
            w.rstrip("s") if len(w) > 3 else w
            for w in re.findall(r"[a-z]+", query.lower())
            if w not in self._STOPWORDS and len(w) > 2
        }
        if not words:
            return []
        scored = []
        for spec in self.registry.list_tools():
            title = " ".join([spec.name, spec.display_name, *spec.tags]).lower()
            desc = spec.description.lower()
            score = sum(3 for w in words if w in title) + sum(1 for w in words if w in desc)
            if score:
                if spec.name.startswith(("native_", "qgis_")):
                    score += 0.5
                scored.append((score, spec.name))
        scored.sort(key=lambda s: (-s[0], s[1]))
        return [name for _, name in scored]

    def _get_prompt(self, request: AnalysisRequest) -> str:
        """Build the LLM prompt with tool catalog and knowledge context."""
        tool_catalog = []
        for spec in self.registry.list_tools():
            tool_catalog.append({
                "name": spec.name,
                "description": spec.description[:200],  # Token budget
                "parameters": [
                    {"name": p.name, "type": p.param_type, "required": p.required}
                    for p in spec.parameters[:8]  # Limit params per tool
                ],
            })

        examples = self._examples_for(request.query)

        # If catalog is too large for LLM context (e.g. 700+ QGIS algorithms),
        # send the tools whose name/description best match the query words.
        # Taking the first N alphabetically would mostly offer GDAL raster tools.
        if len(tool_catalog) > 100:
            ranked = self._relevant_tools(request.query)
            example_tools = [st["tool_name"] for e in examples for st in e["steps"]]
            ranked = example_tools + [t for t in ranked if t not in example_tools]
            if ranked:
                keep = set(ranked[:15])  # small local models choose better from few
                tool_catalog = [t for t in tool_catalog if t["name"] in keep]
                tool_catalog.sort(key=lambda t: ranked.index(t["name"]))

        if len(tool_catalog) > 100:
            # Send only the most relevant tools based on intent
            intent_categories = {
                IntentType.PROXIMITY: ["vector"],
                IntentType.OVERLAY: ["vector"],
                IntentType.GEOMETRY: ["vector"],
                IntentType.RASTER: ["raster"],
                IntentType.TERRAIN: ["terrain", "raster"],
                IntentType.NETWORK: ["network"],
            }
            relevant_cats = intent_categories.get(request.intent, [])
            if relevant_cats:
                tool_catalog = [
                    t for t in tool_catalog
                    if any(cat in t.get("description", "").lower() for cat in relevant_cats)
                ][:80]
            else:
                tool_catalog = tool_catalog[:80]

        # ── Phase 2: Inject knowledge context if available ──────────
        layer_lines = []
        state = getattr(self, "_prompt_state", None)
        for name in request.available_layers:
            layer = state.get_layer(name) if state else None
            if layer is None:
                layer_lines.append(f"- {name}")
                continue
            fields = [f for f in (getattr(layer, "fields", None) or []) if f != "fid"]
            layer_lines.append(
                f"- {name}: {layer.layer_type} {layer.geometry_type}, "
                f"{layer.feature_count} features, crs {layer.crs}"
                + (f", fields {fields}" if fields else "")
            )
        layers_section = "\n".join(layer_lines) or "(none)"

        feedback_section = ""
        if getattr(self, "_feedback", None):
            feedback_section = (
                "\nYOUR PREVIOUS ATTEMPT WAS WRONG. Fix it with a different plan:\n"
                f"{self._feedback}\n"
            )

        examples_section = ""
        if examples:
            from geosi_engine.plan_examples import format_examples
            examples_section = (
                "\nWorked examples (same JSON format; adapt tools/parameters, use YOUR layer names):\n"
                + format_examples(examples) + "\n"
            )

        knowledge_section = ""
        if self._last_knowledge_context and self._last_knowledge_context.has_knowledge():
            knowledge_section = f"\n{self._last_knowledge_context.context_prompt}\n"

        return f"""You are GeoSI, an advanced geospatial workflow planner.

CRITICAL RULES:
1. ONLY use tool names from the "Available tools" list below. Tools are
   listed most relevant first; prefer the first tool that does the job.
2. ONLY reference layer names from the "Available layers" list below.
3. NEVER use load_spatial_data. ALL layers are ALREADY loaded.
4. Every step MUST use exactly one tool with its exact parameter names,
   and MUST set every parameter marked "required": true.
5. Use as few steps as possible.
{knowledge_section}
Available tools:
{json.dumps(tool_catalog, indent=2)}

{examples_section}
Available layers:
{layers_section}
{feedback_section}
User query: "{request.query}"

Return ONLY valid JSON:
{{
  "reasoning": "Step-by-step explanation.",
  "steps": [
    {{
      "step_id": "step_1",
      "tool_name": "exact_tool_name",
      "parameters": {{ "PARAM": "value" }},
      "output_name": "step_1_output",
      "description": "What this step does",
      "depends_on": []
    }}
  ]
}}"""

    def _plan_with_ollama(self, request: AnalysisRequest) -> ExecutionPlan:
        import json
        import urllib.request
        try:
            req = urllib.request.Request(f"{self._ollama_endpoint}/api/tags")
            with urllib.request.urlopen(req, timeout=1.5) as resp:  # nosec B310
                pass
        except Exception as exc:
            raise RuntimeError(f"Ollama unreachable: {exc}")

        # Each plan is self-contained: the prompt already carries the tools,
        # layers and any retry feedback. Re-sending earlier prompts (each with
        # a full tool catalog) would overflow a small model's context.
        prompt = self._get_prompt(request)
        payload = json.dumps({
            "model": self._ollama_model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.0},
        }).encode("utf-8")
        post_req = urllib.request.Request(
            f"{self._ollama_endpoint}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(post_req, timeout=120) as resp:  # nosec B310
            data = json.loads(resp.read().decode("utf-8"))
            text = data.get("response", "")
            return self._json_to_plan(request, text)

    # ── OpenAI-compatible hosted models ───────────────────────────────

    def _api_configured(self) -> bool:
        return bool(self._api_base and self._api_model)

    def _api_chat(self, prompt: str, json_mode: bool = True, base: Optional[str] = None,
                  key: Optional[str] = None, model: Optional[str] = None) -> str:
        """One chat completion; plain HTTP so QGIS needs no extra packages."""
        import requests

        base = (base or self._api_base).rstrip("/")
        key = self._api_key if key is None else key
        body = {
            "model": model or self._api_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        headers = {"Content-Type": "application/json"}
        if key:
            headers["Authorization"] = f"Bearer {key}"
        for attempt in range(3):
            resp = requests.post(f"{base}/chat/completions", json=body, headers=headers, timeout=120)
            if resp.status_code == 429 and attempt < 2:  # rate limited: back off and retry
                import time
                time.sleep(float(resp.headers.get("retry-after", 2 * (attempt + 1))))
                continue
            if resp.status_code >= 400:
                # Never log headers (they carry the key); the body has the reason
                raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:300]}")
            return resp.json()["choices"][0]["message"]["content"] or ""
        raise RuntimeError("rate limited")

    def _plan_with_api(self, request: AnalysisRequest) -> ExecutionPlan:
        return self._json_to_plan(request, self._api_chat(self._get_prompt(request)))

    def _plan_with_gemini(self, request: AnalysisRequest) -> ExecutionPlan:
        """Gemini through Google's OpenAI-compatible endpoint (plain HTTP)."""
        text = self._api_chat(
            self._get_prompt(request),
            base=os.environ.get("GEMINI_BASE_URL",
                                "https://generativelanguage.googleapis.com/v1beta/openai"),
            key=self._gemini_key,
            model=self._provider_model("gemini"),
        )
        return self._json_to_plan(request, text)

    def _plan_with_anthropic(self, request: AnalysisRequest) -> ExecutionPlan:
        """Claude through the Anthropic Messages API (plain HTTP, no SDK)."""
        import requests

        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self._anthropic_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self._provider_model("anthropic"),
                "max_tokens": 2048,
                "temperature": 0.0,
                "messages": [{"role": "user", "content": self._get_prompt(request)}],
            },
            timeout=120,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:300]}")
        blocks = resp.json().get("content", [])
        text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
        return self._json_to_plan(request, text)

    def _json_to_plan(self, request: AnalysisRequest, text: str) -> ExecutionPlan:
        text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        if not text.startswith("{") and "{" in text:
            text = text[text.index("{"):text.rindex("}") + 1]
        data = json.loads(text)
        # Keep only known ToolStep fields; larger models add their own keys
        allowed = set(ToolStep.__dataclass_fields__)
        steps = [ToolStep(**{k: v for k, v in s.items() if k in allowed}) for s in data.get("steps", [])]
        return ExecutionPlan(
            request=request, steps=steps,
            reasoning=data.get("reasoning", ""),
        )

    def _validate_plan_layers(self, plan: ExecutionPlan, available_layers: list) -> bool:
        """
        Check that an LLM plan only uses known tools and real layers.

        Only parameters the tool declares as layers are checked, so values
        such as "EPSG:4326" or "1000m" are not mistaken for layer names.
        Outputs of earlier steps count as layers for later steps.
        """
        if not plan.steps:
            return True
        known = set(available_layers or [])
        for step in plan.steps:
            tool = self.registry.get_tool(step.tool_name)
            if tool is None:
                logger.warning(f"LLM plan uses unknown tool: '{step.tool_name}'")
                return False
            spec_params = tool.spec().parameters
            self._repair_spatial_predicate(step, spec_params, plan.request)
            # Small models often lowercase QGIS keys ("input" for INPUT);
            # map them to the real names and drop keys the tool doesn't have
            # (outputs are assigned by the bridge).
            by_lower = {p.name.lower(): p.name for p in spec_params}
            step.parameters = {
                by_lower[k.lower()]: v
                for k, v in (step.parameters or {}).items()
                if k.lower() in by_lower
            }
            layer_params = {p.name for p in spec_params if p.param_type == "layer"}
            for key, value in (step.parameters or {}).items():
                if key not in layer_params or not isinstance(value, str):
                    continue
                if value in known or (value.startswith("step_") and "_output" in value):
                    continue
                logger.warning(f"LLM plan references unknown layer: '{value}' ({key})")
                return False
            if step.output_name:
                known.add(step.output_name)
        return True

    # ── Plan validation & error recovery ───────────────────────────────

    def validate_plan(
        self, plan: ExecutionPlan, state: Optional[StateManager] = None
    ) -> ValidationReport:
        """Validate an ExecutionPlan against the tool registry and state."""
        report = ValidationReport()
        known_steps: set = set()
        for step in plan.steps:
            tool = self.registry.get_tool(step.tool_name)
            spec = tool.spec() if tool else None
            if spec is None:
                from geosi_engine.validation import ValidationIssue
                report.add(ValidationIssue(
                    "error", "unknown_tool",
                    f"Step {step.step_id}: tool '{step.tool_name}' not found.",
                ))
                continue
            for param in spec.parameters:
                if param.required and param.name not in (step.parameters or {}):
                    from geosi_engine.validation import ValidationIssue
                    report.add(ValidationIssue(
                        "error", "missing_parameter",
                        f"Step {step.step_id}: missing '{param.name}'.",
                    ))
            if state is not None:
                pre = self.validator.validate_operation_preconditions(step, state)
                report.issues.extend(pre.issues)
                if not pre.ok:
                    report.ok = False
            known_steps.add(step.step_id)
        return report

    def recover_from_error(
        self, error: Exception, plan: ExecutionPlan,
        failed_step_id: Optional[str] = None,
    ) -> ExecutionPlan:
        """
        Produce a fallback plan by dropping failed steps and dependents.

        Algorithm: Iterative transitive closure over depends_on graph.
        Complexity: O(S²) worst case, O(S) typical (sparse dependency graph)
        """
        if failed_step_id is None and plan.steps:
            failed_step_id = plan.steps[-1].step_id
        dropped = {failed_step_id} if failed_step_id else set()
        changed = True
        while changed:
            changed = False
            for step in plan.steps:
                if step.step_id in dropped:
                    continue
                if any(d in dropped for d in (step.depends_on or [])):
                    dropped.add(step.step_id)
                    changed = True
        surviving = [s for s in plan.steps if s.step_id not in dropped]
        note = f"\n[recovery] dropped {sorted(dropped)} after error: {error}"
        return ExecutionPlan(
            request=plan.request, steps=surviving,
            reasoning=(plan.reasoning or "") + note,
        )
