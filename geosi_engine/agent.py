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
import logging
from typing import Dict, List, Optional, Any, Tuple
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
    "simplify":             "native_simplifygeometries",
    "convex_hull":          "native_convexhull",
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
            import requests
            resp = requests.get(f"{self._ollama_endpoint}/api/tags", timeout=1.5)
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

    # ── Public API ─────────────────────────────────────────────────────

    def parse(self, query: str, state: StateManager) -> AnalysisRequest:
        """Parse a natural language query into an AnalysisRequest."""
        layer_names = state.list_layers() if state else []
        return self.parser.parse(query, layer_names)

    def plan(
        self, request: AnalysisRequest, state: Optional[StateManager] = None
    ) -> ExecutionPlan:
        """
        Create an ExecutionPlan from an AnalysisRequest.

        Priority:
            1. Retrieve knowledge context (Phase 2)
            2. Validate layers exist
            3. Well-understood ops → rule-based (skip LLM)
            4. Ollama → Gemini → Claude → rule-based fallback
        """
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
            "dissolve", "centroid", "convex_hull", "simplify",
            "slope", "aspect", "hillshade", "contour",
            "ndvi", "ndwi", "reproject", "join_attributes",
            "extract_by_attribute",
        }
        if operation in well_understood:
            logger.info(f"Op '{operation}' well-understood → rule-based plan")
            return self._plan_with_rules(request)

        # ── LLM cascade ────────────────────────────────────────────────
        if self.use_llm:
            for name, fn in self._llm_providers():
                try:
                    plan = fn(request)
                    if self._validate_plan_layers(plan, request.available_layers):
                        return plan
                    logger.warning(f"{name} plan referenced nonexistent layers")
                except Exception as e:
                    logger.warning(f"{name} planning failed: {e}")

        return self._plan_with_rules(request)

    # ── LLM provider list ──────────────────────────────────────────────

    def _llm_providers(self):
        """Yield (name, callable) tuples for available LLM providers."""
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

    def validate_layers_exist(
        self, request: AnalysisRequest, state: StateManager
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate that requested layers exist in the QGIS project.
        Returns (is_valid, error_message).
        """
        if not state:
            return False, "No state manager available"

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
        query_lower = (request.query or "").lower()

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
                import re
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

    def _get_prompt(self, request: AnalysisRequest) -> str:
        """Build the LLM prompt with tool catalog and knowledge context."""
        tool_catalog = []
        for spec in self.registry.list_tools():
            tool_catalog.append({
                "name": spec.name,
                "description": spec.description[:200],  # Token budget
                "parameters": [
                    {"name": p.name, "type": p.param_type}
                    for p in spec.parameters[:8]  # Limit params per tool
                ],
            })

        # If catalog is too large for LLM context, only send top categories
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
        knowledge_section = ""
        if self._last_knowledge_context and self._last_knowledge_context.has_knowledge():
            knowledge_section = f"\n{self._last_knowledge_context.context_prompt}\n"

        return f"""You are GeoSI, an advanced geospatial workflow planner.

CRITICAL RULES:
1. ONLY use tool names from the "Available tools" list below.
2. ONLY reference layer names from the "Available layers" list below.
3. NEVER use load_spatial_data. ALL layers are ALREADY loaded.
4. Every step MUST use exactly one tool with its exact parameter names.
{knowledge_section}
Available tools:
{json.dumps(tool_catalog, indent=2)}

Available layers: {request.available_layers}
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
        import requests
        try:
            requests.get(f"{self._ollama_endpoint}/api/tags", timeout=1.5)
        except Exception as exc:
            raise RuntimeError(f"Ollama unreachable: {exc}")

        self.conversation.add_user_message(self._get_prompt(request))
        context = self.conversation.get_context(include_system=True)
        response = requests.post(
            f"{self._ollama_endpoint}/api/generate",
            json={"model": self._ollama_model, "prompt": context, "stream": False, "temperature": 0.0},
            timeout=120,
        )
        response.raise_for_status()
        text = response.json().get("response", "")
        self.conversation.add_assistant_message(text)
        return self._json_to_plan(request, text)

    def _plan_with_gemini(self, request: AnalysisRequest) -> ExecutionPlan:
        import google.generativeai as genai
        genai.configure(api_key=self._gemini_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(self._get_prompt(request))
        return self._json_to_plan(request, response.text)

    def _plan_with_anthropic(self, request: AnalysisRequest) -> ExecutionPlan:
        import anthropic
        client = anthropic.Anthropic(api_key=self._anthropic_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            messages=[{"role": "user", "content": self._get_prompt(request)}],
        )
        return self._json_to_plan(request, response.content[0].text)

    def _json_to_plan(self, request: AnalysisRequest, text: str) -> ExecutionPlan:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        data = json.loads(text)
        steps = [ToolStep(**s) for s in data.get("steps", [])]
        return ExecutionPlan(
            request=request, steps=steps,
            reasoning=data.get("reasoning", ""),
        )

    def _validate_plan_layers(self, plan: ExecutionPlan, available_layers: list) -> bool:
        """Check that all layer references in an LLM plan actually exist."""
        if not available_layers or not plan.steps:
            return True
        available_set = set(available_layers)
        for step in plan.steps:
            for key, value in (step.parameters or {}).items():
                if isinstance(value, str) and value not in available_set:
                    try:
                        float(value)
                        continue
                    except (ValueError, TypeError):
                        pass
                    if value.lower() in ("memory:", "temporary_output", "true", "false"):
                        continue
                    if value.startswith("step_") and "_output" in value:
                        continue
                    logger.warning(f"LLM plan references unknown layer: '{value}'")
                    return False
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
