"""
GeoSI v2 — Planning Agent
════════════════════════════════════════════════════════════════════
Turns a request into an ``ExecutionPlan`` and annotates every step with
the risk it carries, so the Permission & Safety Agent can gate it.

Planning itself is delegated to the engine's planner (``GeoSIAgent``),
which tries, in order:

    1. fixed rules for simple operations (buffer, clip, dissolve, ...)
    2. deterministic planners (attribute filters, statistics, grids, merges)
    3. verified example templates (close paraphrases of known-good plans)
    4. the LLM cascade — hosted OpenAI-compatible API, then Ollama — with
       the most relevant tools found by semantic search and worked examples

Re-planning after a failed check passes the problem as ``feedback``; the
planner then always asks the LLM for a corrected plan.

When a Supervisor is attached, each LLM provider call goes through its
per-provider circuit breaker so a failing provider is skipped quickly.

Risk model
──────────
QGIS Processing writes results to new layers and never changes its inputs,
so most tools are ``read_only`` for existing data. Risk comes from what a
tool does outside the session:

* ``destructive`` — deletes or overwrites existing data: SQL execution,
  truncating tables, ``OVERWRITE=True``.
* ``mutating`` — changes files or databases the user owns: writing to an
  explicit path, importing into a database, assigning a projection in
  place, network downloads, and domain tools that write artifacts.
* ``read_only`` — everything else.

The QGIS bridge classifies each discovered algorithm (``ToolSpec.risk_level``);
parameters can raise the level (an explicit output path, ``OVERWRITE``).
"""

from __future__ import annotations

import logging
import os
import re
import tempfile
from typing import Any, Optional

from geosi_engine.models import ExecutionPlan

logger = logging.getLogger("geosi_engine.agents.planning")

_RISK_ORDER = {"read_only": 0, "mutating": 1, "destructive": 2}

# Name fragments of non-QGIS tools that delete or overwrite data. QGIS
# algorithms are classified by the bridge instead: "native:deletecolumn"
# writes a new layer without the column and is not destructive.
_DESTRUCTIVE_KEYWORDS: frozenset[str] = frozenset(
    {
        "deletefield",
        "delete_field",
        "drop_table",
        "droptable",
        "truncate",
        "executesql",
        "execute_sql",
        "delete_layer",
        "destroy",
        "overwrite",
    }
)

# Domain-agent tools declare their own risk (they may write model artifacts).
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

_TEMP_DIR = os.path.realpath(tempfile.gettempdir())


def _is_user_path(value: Any) -> bool:
    """An explicit file path outside the temp/session area."""
    if not isinstance(value, str) or not value or value == "TEMPORARY_OUTPUT":
        return False
    if value.startswith("memory:"):
        return False
    if value.startswith(("ogr:", "postgres:", "postgis:")):
        return True  # writing into a database
    if not re.search(r"[\\/]|\.[a-z0-9]{2,5}$", value, re.I):
        return False  # a layer name, not a path
    real = os.path.realpath(os.path.expanduser(value))
    session_root = os.path.realpath(os.environ.get("GEOSI_DATA_DIR", _TEMP_DIR))
    return not (real.startswith(_TEMP_DIR) or real.startswith(session_root))


def compute_risk_level(tool_name: str, parameters: dict[str, Any], spec: Any = None) -> str:
    """
    Risk of running *tool_name* with *parameters* (see module docstring).

    *spec* is the tool's ``ToolSpec`` when known; its ``risk_level`` comes
    from the QGIS bridge's classification of the algorithm.
    """
    name = (tool_name or "").lower()
    if name in DOMAIN_TOOL_RISK:
        return DOMAIN_TOOL_RISK[name]

    level = "read_only"
    spec_level = getattr(spec, "risk_level", None)
    if spec_level in _RISK_ORDER:
        level = spec_level
    elif spec is None or not getattr(spec, "qgis_algorithm", None):
        if any(kw in name for kw in _DESTRUCTIVE_KEYWORDS):
            level = "destructive"

    params = parameters or {}
    overwrite = str(params.get("OVERWRITE", params.get("overwrite", ""))).lower()
    if overwrite in ("true", "1", "yes"):
        level = "destructive"
    elif any(key.upper().endswith("OUTPUT") and _is_user_path(v) for key, v in params.items()):
        level = level if _RISK_ORDER[level] >= _RISK_ORDER["mutating"] else "mutating"
    return level


def _compute_risk_level(tool_name: str, parameters: dict[str, Any]) -> str:
    """Backward-compatible name (no ToolSpec available)."""
    return compute_risk_level(tool_name, parameters)


class PlanningAgent:
    """
    Produces risk-annotated ``ExecutionPlan``s through the engine's planner.

    Parameters
    ----------
    engine:
        Session-scoped ``GeoSI`` instance (registry, state, planner).
    supervisor:
        Optional ``SupervisorAgent`` whose circuit breakers guard LLM calls.
    """

    def __init__(self, engine: Any, supervisor: Any = None) -> None:
        self._engine = engine
        self._supervisor = supervisor

    def plan(
        self,
        query: str,
        available_layers: Optional[list[str]] = None,
        session_id: str = "",
        feedback: Optional[str] = None,
    ) -> ExecutionPlan:
        """
        Plan *query* against the session's loaded layers.

        ``feedback`` describes why the previous attempt was rejected; the
        planner then asks the LLM for a different plan.
        """
        agent = getattr(self._engine, "agent", None)
        state = getattr(self._engine, "state", None)
        if agent is None:
            return ExecutionPlan(reasoning=f"No planner available for: {query}", plan_source="empty_fallback")

        if self._supervisor is not None:
            agent.breakers = self._supervisor.provider_breakers()

        request = agent.parse(query, state)
        if available_layers:
            known = set(request.available_layers or [])
            request.available_layers = list(request.available_layers or []) + [
                n for n in available_layers if n not in known
            ]
        plan = agent.plan(request, state, feedback=feedback)
        plan.request = plan.request or request

        registry = getattr(self._engine, "registry", None)
        for step in plan.steps:
            tool = registry.get_tool(step.tool_name) if registry is not None else None
            spec = tool.spec() if tool is not None else None
            level = compute_risk_level(step.tool_name, step.parameters, spec)
            # Keep a stricter level the planner set explicitly
            if _RISK_ORDER.get(step.risk_level, 0) < _RISK_ORDER[level]:
                step.risk_level = level

        flags = getattr(getattr(agent, "_last_knowledge_context", None), "guardrail_flags", None)
        if flags:
            plan.guardrail_flags = list(flags)

        logger.info("Planning complete: %d step(s), source=%s", len(plan.steps), plan.plan_source)
        return plan
