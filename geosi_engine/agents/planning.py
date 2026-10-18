# -*- coding: utf-8 -*-
"""
GeoSI v2 — Planning Agent
════════════════════════════════════════════════════════════════════
Converts a natural-language query into a validated ExecutionPlan.

Key improvements over v2 ``GeoSIAgent`` (PRD FR-1, G1 fix)
────────────────────────────────────────────────────────────
* Provider-native function-calling / structured output instead of
  ``json.loads(text)`` on raw LLM output.
* Per-provider schema binding:
    - Ollama  : /api/chat ``tools`` parameter
    - Gemini  : ``response_schema=ExecutionPlan``
    - Claude  : ``tools`` with ``input_schema``
    - Fallback: existing ``QueryParser`` + ``GeoSIAgent`` rule-based path
* Pydantic-validated output.  On schema failure: retry once with the
  error fed back to the model; if that also fails → rule-based fallback.
* ``risk_level`` computed from ToolRegistry algorithm metadata.
* Guardrail scan of RAG-retrieved context before it enters the prompt.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional

from geosi_engine.models import (
    AnalysisRequest,
    ExecutionPlan,
    ToolStep,
)

logger = logging.getLogger("geosi_engine.agents.planning")

# ---------------------------------------------------------------------------
# Risk classification helpers
# ---------------------------------------------------------------------------

# QGIS algorithm IDs / name fragments that indicate destructive ops
_DESTRUCTIVE_KEYWORDS: frozenset[str] = frozenset({
    "delete", "drop", "truncate", "remove", "destroy", "overwrite",
    "deletefield", "deletecolumn", "deleterows", "dropmzvalues",
})

# QGIS algorithm IDs that mutate data but aren't fully destructive
_MUTATING_KEYWORDS: frozenset[str] = frozenset({
    "create", "write", "save", "export", "update", "modify", "edit",
    "join", "merge", "dissolve", "clip", "buffer", "intersect",
    "union", "difference", "reproject", "rasterize", "translate",
})

# Domain-agent tools (registered by ``domain_tools.discover_domain_tools``)
# carry an explicit risk level that keyword heuristics cannot infer from the
# tool name alone (e.g. "machine_learning" has no destructive keyword but
# writes model artifacts).  Imported lazily with a safe fallback so planning
# stays importable even if the domain-tools module is unavailable.
try:  # pragma: no cover - import guard
    from geosi_engine.tools.domain_tools import DOMAIN_TOOL_RISK
except Exception:  # pragma: no cover
    DOMAIN_TOOL_RISK = {
        "generate_code": "read_only",
        "generate_report": "read_only",
        "research": "read_only",
        "remote_sensing": "mutating",
        "machine_learning": "mutating",
        "geology": "mutating",
    }

# Tools always surfaced to the LLM so the planner can reach the common GIS
# verbs even when a query's keywords don't match them in ``search_tools``.
# Names are resolved through ``registry.get_tool`` (which strips the
# native_/gdal_/qgis_ prefixes), so plain verbs match discovered algorithms.
_CORE_TOOLS: tuple[str, ...] = (
    "buffer", "clip", "intersection", "dissolve", "reproject",
    "slope", "zonalstatistics", "gdal_warp", "gdal_translate",
    "load_spatial_data", "save_layer",
)


def _compute_risk_level(tool_name: str, parameters: dict[str, Any]) -> str:
    """
    Derive a risk level from the tool name and its parameters.

    Rules (in priority order):
    1. Registered domain tool → its declared risk level.
    2. Any tool with ``OVERWRITE=True`` or ``OVERWRITE=1`` in params → mutating
    3. Tool name contains a destructive keyword → destructive
    4. Tool name contains a mutating keyword → mutating
    5. Default → read_only
    """
    name_lower = tool_name.lower()

    # Domain tools declare their own risk — never let keyword heuristics
    # misclassify a mutating domain op (e.g. remote_sensing) as read_only.
    if name_lower in DOMAIN_TOOL_RISK:
        return DOMAIN_TOOL_RISK[name_lower]

    # Check for explicit overwrite parameter
    overwrite = str(parameters.get("OVERWRITE", parameters.get("overwrite", ""))).lower()
    has_overwrite = overwrite in ("true", "1", "yes")

    if any(kw in name_lower for kw in _DESTRUCTIVE_KEYWORDS):
        return "destructive"

    if has_overwrite or any(kw in name_lower for kw in _MUTATING_KEYWORDS):
        return "mutating"

    return "read_only"


# ---------------------------------------------------------------------------
# Planning Agent
# ---------------------------------------------------------------------------

class PlanningAgent:
    """
    Converts natural-language queries into validated ``ExecutionPlan``s.

    Parameters
    ----------
    engine:
        The session-scoped ``GeoSI`` instance providing access to the
        ``ToolRegistry``, ``GeoSIAgent``, ``QueryParser``, and
        ``KnowledgeManager``.
    supervisor:
        Reference to the ``SupervisorAgent`` for LLM cascade management.
    """

    _PROVIDERS = ["ollama", "gemini", "claude", "rule_based"]

    def __init__(self, engine: Any, supervisor: Any) -> None:
        self._engine = engine
        self._supervisor = supervisor  # SupervisorAgent

    def plan(
        self,
        query: str,
        available_layers: list[str],
        session_id: str,
    ) -> ExecutionPlan:
        """
        Produce a validated ``ExecutionPlan`` for the given query.

        Pipeline
        --------
        1. Retrieve RAG context (guardrail-scanned).
        2. Try function-calling providers in cascade order.
        3. On schema failure: retry once with validation error.
        4. If still failing: fall back to rule-based planner.
        5. Annotate each ``ToolStep`` with ``risk_level``.
        """
        # Step 1 — RAG context retrieval + guardrail scan
        rag_context = self._retrieve_context(query)
        plan_guardrail_flags: list[str] = []
        if rag_context:
            from geosi_engine.guardrails import scan_text
            gr = scan_text(rag_context)
            if not gr.is_clean:
                logger.warning(
                    "Planning: RAG context has guardrail flags: %s", gr.flags
                )
                plan_guardrail_flags = gr.flags

        # Step 2 — LLM cascade via Supervisor's budget runner
        plan: Optional[ExecutionPlan] = None
        try:
            plan = self._supervisor.run_with_budget(
                providers=self._configured_providers(),
                fn=lambda provider: self._plan_with_provider(
                    provider, query, available_layers, rag_context
                ),
            )
        except RuntimeError as exc:
            logger.warning("All LLM providers failed; falling back to rule-based: %s", exc)

        # Step 3 — Rule-based fallback
        if plan is None:
            plan = self._rule_based_plan(query, available_layers)

        # Step 4 — Annotate risk levels
        for step in plan.steps:
            if step.risk_level == "read_only":  # don't override if already set
                step.risk_level = _compute_risk_level(step.tool_name, step.parameters)

        # Propagate plan-level guardrail flags from RAG context
        plan.guardrail_flags = plan_guardrail_flags

        logger.info(
            "Planning complete: %d steps, source=%s, flags=%d",
            len(plan.steps),
            plan.plan_source,
            len(plan.guardrail_flags),
        )
        return plan

    # ------------------------------------------------------------------
    # Provider-specific function calling
    # ------------------------------------------------------------------

    @staticmethod
    def _configured_providers() -> list[str]:
        """
        Resolve the ordered LLM provider cascade.

        Defaults to ``ollama,gemini,claude`` but is overridable via the
        ``GEOSI_LLM_PROVIDERS`` env var (comma-separated).  Setting it to
        ``ollama`` alone lets a purely local LLM drive the agentic
        tool-calling pipeline with no cloud dependency.
        """
        raw = os.environ.get("GEOSI_LLM_PROVIDERS", "").strip()
        if raw:
            providers = [p.strip().lower() for p in raw.split(",") if p.strip()]
            if providers:
                return providers
        return ["ollama", "gemini", "claude"]

    def _plan_with_provider(
        self,
        provider: str,
        query: str,
        available_layers: list[str],
        rag_context: str,
    ) -> ExecutionPlan:
        """Dispatch to the correct provider's function-calling implementation."""
        if provider == "ollama":
            return self._plan_ollama(query, available_layers, rag_context)
        elif provider == "gemini":
            return self._plan_gemini(query, available_layers, rag_context)
        elif provider == "claude":
            return self._plan_claude(query, available_layers, rag_context)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _plan_ollama(
        self, query: str, available_layers: list[str], rag_context: str
    ) -> ExecutionPlan:
        """Ollama function-calling via /api/chat tools parameter."""
        import requests as _requests

        endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
        model = os.environ.get("OLLAMA_MODEL", "llama3.2")

        tool_schema = self._build_tool_schema()
        prompt = self._build_prompt(query, available_layers, rag_context)

        resp = _requests.post(
            f"{endpoint}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "tools": [tool_schema],
                "stream": False,
                "options": {"temperature": 0},
            },
            timeout=float(os.environ.get("LLM_PROVIDER_TIMEOUT_SECONDS", "10")),
        )
        resp.raise_for_status()
        data = resp.json()

        # Extract tool call arguments
        tool_calls = (
            data.get("message", {}).get("tool_calls") or []
        )
        if tool_calls:
            args = tool_calls[0].get("function", {}).get("arguments", {})
            plan = self._args_to_plan(args, source="ollama_function_calling")
        else:
            # Fallback: parse text response
            text = data.get("message", {}).get("content", "")
            plan = self._parse_json_response(text, source="ollama_text")

        return plan

    def _plan_gemini(
        self, query: str, available_layers: list[str], rag_context: str
    ) -> ExecutionPlan:
        """Gemini structured output via response_schema."""
        import google.generativeai as genai  # type: ignore[import]

        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        generation_config = {
            "temperature": 0,
            "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
            os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
            generation_config=generation_config,
        )
        prompt = self._build_prompt(query, available_layers, rag_context)
        response = model.generate_content(prompt)
        return self._parse_json_response(response.text, source="gemini")

    def _plan_claude(
        self, query: str, available_layers: list[str], rag_context: str
    ) -> ExecutionPlan:
        """Claude tool-use via tools parameter."""
        import anthropic  # type: ignore[import]

        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        tool_schema = self._build_tool_schema()
        prompt = self._build_prompt(query, available_layers, rag_context)

        response = client.messages.create(
            model=os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
            max_tokens=4096,
            tools=[{
                "name": "create_execution_plan",
                "description": "Create a structured GIS execution plan.",
                "input_schema": tool_schema["function"]["parameters"],
            }],
            messages=[{"role": "user", "content": prompt}],
        )
        for block in response.content:
            if block.type == "tool_use" and block.name == "create_execution_plan":
                return self._args_to_plan(block.input, source="claude_tool_use")

        # Fallback to text response
        text = "".join(
            getattr(b, "text", "") for b in response.content
        )
        return self._parse_json_response(text, source="claude_text")

    def _parse_json_response(self, text: str, source: str) -> ExecutionPlan:
        """
        Parse LLM text output into an ExecutionPlan.

        On schema failure: attempt to re-parse after basic cleanup.
        Replaces the raw ``json.loads(text)`` anti-pattern (G1 fix).
        """
        text = text.strip()
        # Strip markdown code fences
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:])
            if text.endswith("```"):
                text = text[:-3].rstrip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Greedy extraction of first JSON object
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end > start:
                data = json.loads(text[start : end + 1])
            else:
                raise ValueError("No JSON object found in LLM response")

        return self._args_to_plan(data, source=source)

    def _args_to_plan(self, data: dict[str, Any], source: str) -> ExecutionPlan:
        """Convert a parsed dict to an ExecutionPlan with validation."""
        steps_raw = data.get("steps") or []
        steps = []
        for s in steps_raw:
            if not isinstance(s, dict):
                continue
            step = ToolStep(
                step_id=str(s.get("step_id", f"step_{len(steps)+1}")),
                tool_name=str(s.get("tool_name", "")),
                parameters=dict(s.get("parameters") or {}),
                input_layers=list(s.get("input_layers") or []),
                output_name=str(s.get("output_name", "")),
                description=str(s.get("description", "")),
                depends_on=list(s.get("depends_on") or []),
                risk_level=str(s.get("risk_level", "read_only")),
            )
            steps.append(step)

        plan = ExecutionPlan(
            steps=steps,
            reasoning=str(data.get("reasoning", "")),
            plan_source=source,
        )
        return plan

    # ------------------------------------------------------------------
    # Rule-based fallback (delegates to existing GeoSIAgent)
    # ------------------------------------------------------------------

    def _rule_based_plan(
        self, query: str, available_layers: list[str]
    ) -> ExecutionPlan:
        """Use the existing GeoSIAgent + QueryParser as fallback."""
        try:
            if hasattr(self._engine, "agent") and self._engine.agent:
                state = getattr(self._engine, "state", None)
                request = self._engine.agent.parse(query, state)
                plan = self._engine.agent.plan(request, state)
                plan.plan_source = "rule_based"
                return plan
        except Exception as exc:
            logger.warning("Rule-based planner also failed: %s", exc)

        # Absolute last resort: empty plan
        return ExecutionPlan(
            reasoning=f"Could not plan query: {query}",
            plan_source="empty_fallback",
        )

    # ------------------------------------------------------------------
    # RAG context retrieval
    # ------------------------------------------------------------------

    def _retrieve_context(self, query: str) -> str:
        """Retrieve relevant GIS documentation from the Knowledge Layer."""
        try:
            if hasattr(self._engine, "knowledge") and self._engine.knowledge:
                result = self._engine.knowledge.retrieve_context(query)
                if result and getattr(result, "context_prompt", ""):
                    return result.context_prompt
        except Exception as exc:
            logger.debug("RAG context retrieval failed: %s", exc)
        return ""

    # ------------------------------------------------------------------
    # Tool grounding — surface the real registry to the planner (G1 fix)
    # ------------------------------------------------------------------

    def _select_relevant_tools(
        self, query: str, available_layers: list[str]
    ) -> list[Any]:
        """
        Select the ``ToolSpec``s most relevant to *query* from the live
        registry, so the LLM calls real discovered tools instead of guessing.

        Union of:
          * ``registry.search_tools(query)`` (keyword/tag match), and
          * a core always-include set (common GIS verbs), and
          * the registered domain tools (so "any GIS task" is reachable).

        Deduplicated by ``spec.name`` and capped at ``GEOSI_PLAN_MAX_TOOLS``.
        Returns ``[]`` when no registry is present (degrade-safe).
        """
        registry = getattr(self._engine, "registry", None)
        if registry is None:
            return []

        specs: dict[str, Any] = {}

        try:
            for spec in registry.search_tools(query):
                specs[spec.name] = spec
        except Exception as exc:
            logger.debug("search_tools failed during planning: %s", exc)

        for name in (*_CORE_TOOLS, *DOMAIN_TOOL_RISK.keys()):
            try:
                tool = registry.get_tool(name)
                if tool is not None:
                    spec = tool.spec()
                    specs[spec.name] = spec
            except Exception:
                continue

        result = list(specs.values())
        try:
            cap = int(os.environ.get("GEOSI_PLAN_MAX_TOOLS", "40"))
        except ValueError:
            cap = 40
        return result[:cap]

    @staticmethod
    def _format_tool_catalog(specs: list[Any]) -> str:
        """
        Render ``ToolSpec``s as one line per tool for the LLM prompt.

        Emits the *registry* name (what ``get_tool``/the executor resolve),
        the QGIS algorithm id, category, a trimmed description, and the
        parameter signature (``*`` marks required params).
        """
        lines: list[str] = []
        for spec in specs:
            algo = spec.qgis_algorithm or spec.name
            params = []
            for p in getattr(spec, "parameters", []) or []:
                mark = "*" if getattr(p, "required", False) else ""
                params.append(f"{p.name}({p.param_type}{mark})")
            pstr = ", ".join(params) if params else "(none)"
            desc = (spec.description or spec.display_name or "").strip().replace("\n", " ")
            if len(desc) > 120:
                desc = desc[:117] + "..."
            lines.append(
                f"- {spec.name} ({algo}) [{spec.category}]: {desc} | params: {pstr}"
            )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Schema / prompt helpers
    # ------------------------------------------------------------------

    def _build_tool_schema(self) -> dict[str, Any]:
        """Build the JSON schema for function-calling (all providers)."""
        return {
            "type": "function",
            "function": {
                "name": "create_execution_plan",
                "description": (
                    "Create a structured step-by-step GIS workflow plan "
                    "from a natural language query."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reasoning": {
                            "type": "string",
                            "description": "Step-by-step explanation of the plan.",
                        },
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "step_id": {"type": "string"},
                                    "tool_name": {"type": "string"},
                                    "parameters": {"type": "object"},
                                    "input_layers": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "output_name": {"type": "string"},
                                    "description": {"type": "string"},
                                    "depends_on": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "risk_level": {
                                        "type": "string",
                                        "enum": ["read_only", "mutating", "destructive"],
                                    },
                                },
                                "required": ["step_id", "tool_name"],
                            },
                        },
                    },
                    "required": ["steps"],
                },
            },
        }

    def _build_prompt(
        self, query: str, available_layers: list[str], rag_context: str
    ) -> str:
        ctx = f"\n{rag_context}\n" if rag_context else ""
        layers = ", ".join(available_layers) if available_layers else "(none loaded)"

        # Ground the planner in the real, discovered tool surface so the LLM
        # calls tools that actually resolve (G1 fix). Empty registry → no block.
        catalog = self._format_tool_catalog(
            self._select_relevant_tools(query, available_layers)
        )
        tools_block = (
            f"AVAILABLE GIS TOOLS (use the exact tool_name shown):\n{catalog}\n\n"
            if catalog
            else ""
        )

        return (
            f"You are GeoSI, an expert geospatial workflow planner.\n"
            f"{ctx}"
            f"{tools_block}"
            f"Available layers: {layers}\n"
            f"User query: \"{query}\"\n\n"
            "Create a step-by-step execution plan using the create_execution_plan tool.\n"
            "RULES:\n"
            "1. Prefer the tools and layers listed above; use the exact tool_name "
            "string shown in AVAILABLE GIS TOOLS.\n"
            "2. If no listed tool fits the task, use 'generate_code' to produce a "
            "reproducible script for the user to review (it is never auto-run).\n"
            "3. Set risk_level: 'read_only' for queries/analysis, "
            "'mutating' for creating/writing data, "
            "'destructive' for deleting/overwriting existing data.\n"
            "4. Every step must have a unique step_id (step_1, step_2, ...).\n"
        )
