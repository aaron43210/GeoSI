# -*- coding: utf-8 -*-
"""
GeoSI Engine — Agent (LLM-Powered Planning)

Plans GIS workflows using Ollama (local-first), Google Gemini, or Anthropic Claude LLMs.
Ollama is tried first if available; then falls back to Gemini, then Claude, then rule-based planning.
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

_DEFAULT_PLANS: Dict[IntentType, List[str]] = {
    IntentType.PROXIMITY:       ["buffer", "intersect"],
    IntentType.OVERLAY:         ["intersect"],
    IntentType.GEOMETRY:        ["clean_layer"],
    IntentType.RASTER:          ["raster_calc"],
    IntentType.TERRAIN:         ["slope"],
    IntentType.NETWORK:         ["shortest_path"],
    IntentType.AI_ML:           ["kmeans_cluster", "hotspot_analysis"],
    IntentType.CARTOGRAPHY:     ["export_geojson"],
    IntentType.STATISTICS:      ["count_features"],
    IntentType.DATA_MANAGEMENT: ["load_spatial_data"],
    IntentType.VALIDATION:      ["validate_geometry"],
    IntentType.TEMPORAL:        ["load_spatial_data"],
    IntentType.UNKNOWN:         ["count_features"],
}

class GeoSIAgent:
    """
    Plans multi-step GIS workflows using Gemini or Claude.
    Only works with layers available in QGIS layer panel.
    """

    def __init__(self, registry: ToolRegistry, use_llm: bool = True, conversation: Optional[ConversationManager] = None):
        self.registry = registry
        self.parser = QueryParser(use_llm=use_llm)
        self.validator = ValidationEngine()
        self.use_llm = use_llm
        self.conversation = conversation or ConversationManager(
            system_prompt="You are a GIS workflow planner. You help users analyze geospatial data and create analysis plans."
        )
        self._ollama_endpoint = self._detect_ollama_endpoint()
        self._ollama_model = self._detect_ollama_model()
        self._anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self._gemini_key = os.environ.get("GEMINI_API_KEY", "")
        self.layer_suggestions: Optional[List[Tuple[str, float]]] = None  # For UI to show similar layers

    def _detect_ollama_endpoint(self) -> str:
        return os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")

    def _detect_ollama_model(self) -> str:
        model = os.environ.get("OLLAMA_MODEL", "mistral")
        try:
            import requests
            endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
            resp = requests.get(f"{endpoint}/api/tags", timeout=1.5)
            if resp.status_code == 200:
                models = [m.get("name") for m in resp.json().get("models", [])]
                if models and model not in models:
                    # Prefer a small fast model if available
                    for pref in ["llama3.2:3b", "qwen2.5-coder:14b", "mistral"]:
                        if pref in models:
                            return pref
                    return models[0]
        except Exception:
            pass
        return model

    def parse(self, query: str, state: StateManager) -> AnalysisRequest:
        layer_names = state.list_layers() if state else []
        return self.parser.parse(query, layer_names)

    def find_similar_layers(self, layer_name: str, available_layers: List[str], threshold: float = 0.6) -> List[Tuple[str, float]]:
        """
        Find similar layer names using fuzzy matching.
        Returns list of (layer_name, similarity_score) tuples sorted by score descending.
        """
        if not available_layers or not layer_name:
            return []
        
        matches = []
        layer_lower = layer_name.lower()
        for available in available_layers:
            available_lower = available.lower()
            # Check exact match first
            if available_lower == layer_lower:
                matches.append((available, 1.0))
            else:
                # Fuzzy match
                ratio = SequenceMatcher(None, layer_lower, available_lower).ratio()
                if ratio >= threshold:
                    matches.append((available, ratio))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)

    def validate_layers_exist(self, request: AnalysisRequest, state: StateManager) -> Tuple[bool, Optional[str]]:
        """
        Validate that requested layers exist in available layers.
        Returns (is_valid, error_message).
        If similar layers found, sets self.layer_suggestions for UI.
        """
        if not state:
            return False, "No state manager available"

        available = state.list_layers()
        if not available:
            return False, (
                "No layers loaded. Please load a shapefile first, or reference one by filename "
                "(e.g. 'Count schools from Schools.shp')."
            )

        # If the parser could not resolve a primary_layer but the query
        # clearly names one (e.g. "Buffer hospitals by 500m" with only
        # "Schools" loaded), surface that to the user instead of silently
        # running a layerless plan.
        primary = request.entities.get("primary_layer")
        if not primary:
            import re as _re
            candidates = _re.findall(
                r"\b([A-Za-z][A-Za-z_]{3,})\b",
                request.query or "",
            )
            _STOP = {
                "buffer", "intersect", "clip", "union", "merge", "dissolve",
                "centroid", "slope", "aspect", "ndvi", "ndwi", "raster",
                "shortest", "path", "service", "area", "hotspot", "cluster",
                "count", "export", "geojson", "shapefile", "from", "with",
                "into", "within", "meters", "meter", "metre", "metres",
                "kilometers", "kilometer", "km", "miles", "feet", "yards",
                "the", "and", "near", "nearest", "find", "calculate", "show",
                "list", "layer", "layers", "between", "over", "above",
                "below", "features", "points", "feature", "point",
                "vegetative", "index", "satellite", "bands", "band", "using",
                "water", "imagery", "spatial", "compute", "extract", "generate"
            }
            noun_like = [c for c in candidates if c.lower() not in _STOP]
            # Look for nouns NOT present in any loaded layer
            loaded_lower = {l.lower() for l in available}
            loaded_stems = {os.path.splitext(l)[0].lower() for l in available}
            orphans = [
                n for n in noun_like
                if n.lower() not in loaded_lower
                and n.lower() not in loaded_stems
            ]
            if orphans:
                orphan = orphans[0]
                similar = self.find_similar_layers(orphan, available, threshold=0.5)
                self.layer_suggestions = similar
                if similar:
                    suggestions = ", ".join(
                        [f"'{s[0]}' ({s[1]:.0%} match)" for s in similar[:3]]
                    )
                    return False, (
                        f"Layer '{orphan}' not found in the QGIS Layers panel. "
                        f"Did you mean: {suggestions}?"
                    )
                layers_list = "\n  - ".join(available)
                return False, (
                    f"Layer '{orphan}' not found in the QGIS Layers panel.\n\n"
                    f"Available layers:\n  - {layers_list}"
                )

        # Check if primary layer exists (case-insensitive + stem matching)
        if primary:
            primary_lower = primary.lower()
            primary_stem  = os.path.splitext(primary_lower)[0]
            available_lower = [l.lower() for l in available]
            available_stems = [os.path.splitext(l)[0].lower() for l in available]

            matched = (
                primary_lower in available_lower
                or primary_stem in available_lower
                or primary_lower in available_stems
                or primary_stem in available_stems
            )

            if not matched:
                # Try fuzzy suggestions
                similar = self.find_similar_layers(primary, available, threshold=0.5)
                self.layer_suggestions = similar

                if similar:
                    suggestions = ", ".join(
                        [f"'{s[0]}' ({s[1]:.0%} match)" for s in similar[:3]]
                    )
                    return False, f"Layer '{primary}' not found. Did you mean: {suggestions}?"
                else:
                    layers_list = "\n  - ".join(available)
                    return False, (
                        f"Layer '{primary}' not found.\n\n"
                        f"Available layers:\n  - {layers_list}"
                    )

        return True, None

    def plan(self, request: AnalysisRequest, state: Optional[StateManager] = None) -> ExecutionPlan:
        # Validate layers exist first
        if state:
            valid, error_msg = self.validate_layers_exist(request, state)
            if not valid:
                # Return a failed plan with error message
                return ExecutionPlan(
                    request=request,
                    steps=[],
                    reasoning=error_msg or "Layer validation failed"
                )
        
        # If the parser already identified a clear, well-understood operation
        # (clip, buffer, intersect, etc.), skip the LLM — the rule-based planner
        # handles these perfectly and the LLM often generates worse plans.
        operation = request.parameters.get("operation", "")
        well_understood_ops = {
            "clip", "buffer", "intersect", "union", "difference",
            "dissolve", "centroid", "convex_hull", "simplify",
            "slope", "aspect", "hillshade", "contour",
            "ndvi", "ndwi", "reproject", "join_attributes",
        }
        if operation in well_understood_ops:
            logger.info(f"Operation '{operation}' is well-understood, using rule-based planner")
            return self._plan_with_rules(request)

        if self.use_llm:
            # Priority 1: Try Ollama first (if available)
            try:
                llm_plan = self._plan_with_ollama(request)
                if self._validate_plan_layers(llm_plan, request.available_layers):
                    return llm_plan
                logger.warning("Ollama plan referenced nonexistent layers, falling back to rules")
            except Exception as e:
                logger.warning(f"Ollama planning failed: {e}")
            
            # Priority 2: Try Gemini
            if self._gemini_key:
                try:
                    llm_plan = self._plan_with_gemini(request)
                    if self._validate_plan_layers(llm_plan, request.available_layers):
                        return llm_plan
                    logger.warning("Gemini plan referenced nonexistent layers, falling back to rules")
                except Exception as e:
                    logger.warning(f"Gemini planning failed: {e}")
            
            # Priority 3: Try Anthropic
            if self._anthropic_key:
                try:
                    llm_plan = self._plan_with_anthropic(request)
                    if self._validate_plan_layers(llm_plan, request.available_layers):
                        return llm_plan
                    logger.warning("Anthropic plan referenced nonexistent layers, falling back to rules")
                except Exception as e:
                    logger.warning(f"Anthropic planning failed: {e}")

        return self._plan_with_rules(request)

    def _validate_plan_layers(self, plan: ExecutionPlan, available_layers: list) -> bool:
        """Check that all layer references in an LLM plan actually exist."""
        if not available_layers or not plan.steps:
            return True  # can't validate, let it through
        available_set = set(available_layers)
        for step in plan.steps:
            for key, value in (step.parameters or {}).items():
                if isinstance(value, str) and value not in available_set:
                    # Check if it's a numeric value or a non-layer parameter
                    try:
                        float(value)
                        continue  # it's a number, not a layer name
                    except (ValueError, TypeError):
                        pass
                    # Skip known non-layer parameter values
                    if value.lower() in ("memory:", "temporary_output", "true", "false"):
                        continue
                    # Skip output references from previous steps (step_1_output, etc.)
                    if value.startswith("step_") and "_output" in value:
                        continue
                    logger.warning(f"LLM plan references unknown layer: '{value}' (param {key})")
                    return False
        return True

    def _plan_with_rules(self, request: AnalysisRequest) -> ExecutionPlan:
        tool_names = _DEFAULT_PLANS.get(request.intent, ["count_features"])
        query_lower = request.query.lower() if request.query else ""

        # Override generic raster_calc for specific index operations
        if request.intent == IntentType.RASTER or any(kw in query_lower for kw in [
            "ndvi", "vegetative", "vegetation", "spectral index", "band ratio",
            "ndwi", "water index",
        ]):
            if any(kw in query_lower for kw in ["ndvi", "vegetative", "vegetation", "spectral", "band ratio"]):
                tool_names = ["ndvi"]
            elif any(kw in query_lower for kw in ["ndwi", "water index"]):
                tool_names = ["ndwi"]
            elif tool_names == ["raster_calc"]:
                if not request.parameters.get("operation"):
                    tool_names = ["count_features"]

        # Override default tool with the specific operation parsed from the query.
        # This fires regardless of intent classification — if the parser found
        # "clip", the tool must be "clip" even if the LLM said intent=GEOMETRY.
        operation = request.parameters.get("operation", "")
        op_to_tool = {
            "clip": "clip", "intersect": "intersect", "union": "union_layer",
            "difference": "difference", "symmetric_difference": "symmetric_difference",
            "buffer": "buffer", "dissolve": "dissolve", "centroid": "centroid",
            "simplify": "simplify", "reproject": "reproject",
            "slope": "slope", "aspect": "aspect", "hillshade": "hillshade",
            "contour": "contour", "ndvi": "ndvi", "ndwi": "ndwi",
            "join_attributes": "join_attributes",
        }
        if operation in op_to_tool:
            tool_names = [op_to_tool[operation]]

        # Validate entity layer references: if an entity references a layer
        # that doesn't exist in available_layers, it might be a geographic name
        # in the attribute table (e.g., "Thiruvananthapuram" in Kerala's DISTRICT field).
        available_set = set(request.available_layers or [])
        secondary = request.entities.get("secondary_layer")
        
        # If secondary_layer is None but query has geographic names (features)
        # that aren't loaded layers, use them as the search term.
        if secondary is None and operation in ("clip", "extract"):
            features = request.entities.get("features", [])
            for feat in features:
                if feat not in available_set:
                    secondary = feat
                    break
        
        if (isinstance(secondary, str) and secondary not in available_set
                and operation in ("clip", "extract") 
                and self.registry.get_tool("extract_by_name")):
            # Switch from clip to extract_by_name: search the primary layer's
            # attribute table for the geographic name instead of using an overlay.
            logger.info(f"'{secondary}' not a loaded layer — switching to extract_by_name (attribute search)")
            tool_names = ["extract_by_name"]
            request.parameters["_search_term"] = secondary
            request.entities["secondary_layer"] = None
        else:
            for entity_key in ("primary_layer", "secondary_layer"):
                name = request.entities.get(entity_key)
                if isinstance(name, str) and name not in available_set:
                    logger.warning(f"Entity '{entity_key}' = '{name}' not in available layers, clearing")
                    request.entities[entity_key] = None

        steps = []
        for i, tool_name in enumerate(tool_names):
            tool = self.registry.get_tool(tool_name)
            if not tool:
                continue

            spec = tool.spec()
            params = {}
            description_parts = [tool_name]

            # Collect all parameter specs
            param_specs = {p.name: p for p in (spec.parameters or [])}

            # Primary input layer (usually first parameter: INPUT, layer, etc.)
            primary = request.entities.get("primary_layer") or request.entities.get("layer")
            if param_specs:
                first_param_name = spec.parameters[0].name
                params[first_param_name] = primary
            else:
                params["INPUT"] = primary

            # Fill in other parameters based on intent and tool
            if tool_name == "buffer":
                # Buffer tool needs DISTANCE
                dist = request.parameters.get("distance_value")
                if dist:
                    params["DISTANCE"] = dist
                    description_parts.append(f"by {dist}m")
            
            elif tool_name == "intersect" or tool_name == "intersection":
                # Intersect tool needs OVERLAY (secondary layer)
                overlay = request.entities.get("secondary_layer")
                if overlay:
                    params["OVERLAY"] = overlay
                    description_parts.append(f"with {overlay}")
                else:
                    # If no secondary layer specified, try to find another available layer
                    available = request.available_layers or []
                    for layer in available:
                        if layer.lower() != (primary or "").lower():
                            params["OVERLAY"] = layer
                            description_parts.append(f"with {layer}")
                            break
            
            elif tool_name == "clip":
                # Clip tool needs OVERLAY (the boundary to clip to)
                overlay = request.entities.get("secondary_layer")
                if overlay:
                    params["OVERLAY"] = overlay
                    description_parts.append(f"clipped to {overlay}")
                else:
                    # Fallback: pick the best remaining loaded layer as clip boundary
                    available = request.available_layers or []
                    for layer in available:
                        if layer.lower() != (primary or "").lower():
                            params["OVERLAY"] = layer
                            description_parts.append(f"clipped to {layer}")
                            break

            elif tool_name in ["union_layer", "difference", "symmetric_difference"]:
                # Two-layer overlay operations need OVERLAY
                overlay = request.entities.get("secondary_layer")
                if overlay:
                    params["OVERLAY"] = overlay
                    description_parts.append(f"with {overlay}")
                else:
                    available = request.available_layers or []
                    for layer in available:
                        if layer.lower() != (primary or "").lower():
                            params["OVERLAY"] = layer
                            description_parts.append(f"with {layer}")
                            break
            elif tool_name == "extract_by_name":
                # Smart attribute search — pass the search term
                search_term = request.parameters.get("_search_term", "")
                if search_term:
                    params["SEARCH_TERM"] = search_term
                    description_parts.append(f"searching for '{search_term}' in attribute table")

            elif tool_name in ["slope", "aspect", "hillshade", "contour"]:
                # Terrain tools usually just need input DEM
                pass
            
            elif "cluster" in tool_name.lower():
                # K-means cluster - may need NUM_CLUSTERS or EPS parameter
                threshold = request.parameters.get("threshold")
                if threshold:
                    if "NUM_CLUSTERS" in param_specs:
                        params["NUM_CLUSTERS"] = int(threshold)
                    elif "EPS" in param_specs:
                        params["EPS"] = threshold
            
            elif "hotspot" in tool_name.lower():
                # Hotspot analysis - may need secondary layer
                overlay = request.entities.get("secondary_layer")
                if overlay and "OVERLAY" in param_specs:
                    params["OVERLAY"] = overlay

            elif tool_name in ["ndvi", "ndwi"]:
                available = request.available_layers or []
                # Simple fallback: try to find B4/B5 or just use first two layers
                red_layer = primary or (available[0] if len(available) > 0 else "")
                nir_layer = request.entities.get("secondary_layer") or (available[1] if len(available) > 1 else "")
                
                # If available layers have B4 and B5, use them
                b4_layers = [l for l in available if "B4" in l.upper()]
                b5_layers = [l for l in available if "B5" in l.upper()]
                if b4_layers and b5_layers:
                    red_layer = b4_layers[0]
                    nir_layer = b5_layers[0]
                
                if tool_name == "ndvi":
                    params["RED_BAND"] = red_layer
                    params["NIR_BAND"] = nir_layer
                else:
                    params["GREEN_BAND"] = red_layer
                    params["NIR_BAND"] = nir_layer
                
                description_parts.append(f"using {red_layer} and {nir_layer}")

            step = ToolStep(
                step_id=f"step_{i+1}",
                tool_name=tool_name,
                parameters=params,
                output_name=f"step_{i+1}_output",
                description=" ".join(description_parts)
            )
            steps.append(step)
        return ExecutionPlan(request=request, steps=steps, reasoning="Rule-based fallback plan")

    def _get_prompt(self, request: AnalysisRequest) -> str:
        tool_catalog = []
        for spec in self.registry.list_tools():
            # To save tokens, only send core tools + the requested intent
            tool_catalog.append({
                "name": spec.name,
                "description": spec.description,
                "parameters": [{"name": p.name, "type": p.param_type} for p in spec.parameters]
            })
        
        return f"""You are GeoSI, an advanced geospatial workflow planner.
Your goal is to map the user's natural language request to a sequence of available GIS tools.

CRITICAL RULES — VIOLATIONS WILL CAUSE FAILURE:
1. ONLY use tool names from the "Available tools" list below. NEVER invent tools.
2. ONLY reference layer names from the "Available layers" list below. NEVER invent layer names.
3. NEVER use load_spatial_data or any file-loading tool. ALL layers are ALREADY loaded.
4. If the user mentions a file extension like .shp or .geojson, IGNORE the extension and match the layer name from the available layers list.
5. Prioritize specific tools: for NDVI use `ndvi`, for NDWI use `ndwi`, not `raster_calc`.
6. Every step MUST use exactly one tool from the catalog with its exact parameter names.

Available tools:
{json.dumps(tool_catalog, indent=2)}

Available layers: {request.available_layers}
User query: "{request.query}"

Return ONLY valid JSON matching this schema:
{{
  "reasoning": "Explain step-by-step how you chose the tools and layers.",
  "steps": [
    {{
      "step_id": "step_1",
      "tool_name": "exact_tool_name_from_catalog",
      "parameters": {{ "PARAM_NAME": "exact_layer_name_from_available_layers" }},
      "output_name": "step_1_output",
      "description": "Short human-readable task description",
      "depends_on": []
    }}
  ]
}}"""

    def _plan_with_ollama(self, request: AnalysisRequest) -> ExecutionPlan:
        import requests

        try:
            requests.get(f"{self._ollama_endpoint}/api/tags", timeout=1.5)
        except Exception as exc:
            raise RuntimeError(f"Ollama not reachable at {self._ollama_endpoint}: {exc}")

        self.conversation.add_user_message(self._get_prompt(request))
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
        
        # Add assistant response to conversation history
        self.conversation.add_assistant_message(text)
        
        return self._json_to_plan(request, text)

    def _plan_with_anthropic(self, request: AnalysisRequest) -> ExecutionPlan:
        import anthropic
        client = anthropic.Anthropic(api_key=self._anthropic_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            messages=[{"role": "user", "content": self._get_prompt(request)}],
        )
        return self._json_to_plan(request, response.content[0].text)

    def _plan_with_gemini(self, request: AnalysisRequest) -> ExecutionPlan:
        import google.generativeai as genai
        genai.configure(api_key=self._gemini_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(self._get_prompt(request))
        return self._json_to_plan(request, response.text)

    def _json_to_plan(self, request: AnalysisRequest, text: str) -> ExecutionPlan:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"): text = text[:-3]
        data = json.loads(text)
        steps = [ToolStep(**s) for s in data.get("steps", [])]
        return ExecutionPlan(request=request, steps=steps, reasoning=data.get("reasoning", ""))

    # ── Plan validation & error recovery (Architecture Module 2) ──────

    def validate_plan(
        self, plan: ExecutionPlan, state: Optional[StateManager] = None
    ) -> ValidationReport:
        """
        Validate an ExecutionPlan against the tool registry and state.

        Returns a ValidationReport aggregating unknown tools, unknown
        layers, and missing required parameters for every step.
        """
        report = ValidationReport()
        known_steps: set = set()
        for step in plan.steps:
            tool = self.registry.get_tool(step.tool_name)
            spec = tool.spec() if tool else None

            if spec is None:
                from geosi_engine.validation import ValidationIssue
                report.add(ValidationIssue(
                    "error", "unknown_tool",
                    f"Step {step.step_id}: tool '{step.tool_name}' not in registry.",
                ))
                continue

            for param in spec.parameters:
                if param.required and param.name not in (step.parameters or {}):
                    from geosi_engine.validation import ValidationIssue
                    report.add(ValidationIssue(
                        "error", "missing_parameter",
                        f"Step {step.step_id}: required parameter "
                        f"'{param.name}' is missing.",
                    ))

            for dep in step.depends_on or []:
                if dep not in known_steps:
                    from geosi_engine.validation import ValidationIssue
                    report.add(ValidationIssue(
                        "error", "bad_dependency",
                        f"Step {step.step_id} depends on unknown step '{dep}'.",
                    ))

            if state is not None:
                pre = self.validator.validate_operation_preconditions(step, state)
                report.issues.extend(pre.issues)
                if not pre.ok:
                    report.ok = False

            known_steps.add(step.step_id)
        return report

    def recover_from_error(
        self,
        error: Exception,
        plan: ExecutionPlan,
        failed_step_id: Optional[str] = None,
    ) -> ExecutionPlan:
        """
        Produce a fallback ExecutionPlan when a step fails.

        Strategy:
        1. Drop the failed step and any steps depending (directly or
           transitively) on it.
        2. Append a note to the plan reasoning so the UI can surface why
           the recovery plan looks different.

        This matches Module 2 / FR-08 of GEOSI_COMPLETE_ARCHITECTURE.md.
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
        note = (
            f"\n[recovery] dropped step(s) {sorted(dropped)} after error: {error}"
        )
        return ExecutionPlan(
            request=plan.request,
            steps=surviving,
            reasoning=(plan.reasoning or "") + note,
        )
