# -*- coding: utf-8 -*-
"""
GeoSI v2 — Production Pipeline Tests (Plan Verification, NO MOCKS)
════════════════════════════════════════════════════════════════════
These tests exercise the real ``GeoSI`` engine and a real ``ToolRegistry``
seeded with real ``ToolSpec``s (portable + domain tools). There are NO
``MagicMock`` objects for the system under test — only real engine state and,
where a plan must be supplied as INPUT, hand-built real ``ExecutionPlan``s.

Covers plan Parts A / B / D1 / D2 / D3:
  * Part A — the planner grounds its prompt in the real registry (real tool
    names, required-parameter flags) and annotates risk from the registry.
  * Part B — knowledge-layer context reaches the planner prompt.
  * Part D1 — the 6 domain tools are registered and resolvable via
    ``registry.get_tool``.
  * Part D2 — a ``generate_code`` step returns review-only code and is never
    executed (Contract 1).
  * Part D3 — ``SupervisorResponse`` has ``approval_pending``;
    ``dataclasses.asdict(plan)`` round-trips; a mutating step halts the loop
    with ``approval_pending`` set; ``handle()`` populates ``plan_json``.

Runnable with pytest OR directly: ``PYTHONPATH=. python3 tests/test_production_pipeline.py``
"""
from __future__ import annotations

import dataclasses

from geosi_engine import GeoSI
from geosi_engine.models import ExecutionPlan, ToolStep
from geosi_engine.tools.domain_tools import DOMAIN_TOOL_NAMES
from geosi_engine.agents.planning import PlanningAgent
from geosi_engine.agents.supervisor import (
    SupervisorAgent,
    SupervisorRequest,
    SupervisorResponse,
)


class _RealPool:
    """A real session pool: real GeoSI engines, rule-based planner (no LLM)."""

    def __init__(self) -> None:
        self._engines: dict[str, GeoSI] = {}

    def get_or_create(self, sid: str) -> GeoSI:
        if sid not in self._engines:
            eng = GeoSI(use_llm=False, enable_knowledge=False)
            eng._session_id = sid  # type: ignore[attr-defined]
            self._engines[sid] = eng
        return self._engines[sid]


def _engine() -> GeoSI:
    return GeoSI(use_llm=False, enable_knowledge=False)


# ── Part D1: domain tools registered + resolvable ──────────────────────

def test_domain_tools_registered_and_resolvable():
    eng = _engine()
    for name in DOMAIN_TOOL_NAMES:
        tool = eng.registry.get_tool(name)
        assert tool is not None, f"domain tool '{name}' not registered"
        spec = tool.spec()
        assert spec.name == name
        assert spec.requires_qgis is False


# ── Part A: the planner grounds its prompt in the real registry ────────

def test_prompt_lists_real_tool_names():
    eng = _engine()
    request = eng.agent.parse("write code to dissolve polygons", eng.state)
    prompt = eng.agent._get_prompt(request)
    assert "Available tools:" in prompt
    assert "generate_code" in prompt  # a real registered tool name


def test_prompt_marks_required_parameters():
    eng = _engine()
    request = eng.agent.parse("count features", eng.state)
    prompt = eng.agent._get_prompt(request)
    assert '"required"' in prompt


def test_planning_agent_annotates_risk_from_registry():
    eng = _engine()
    plan = ExecutionPlan(steps=[ToolStep(step_id="s1", tool_name="machine_learning")])
    eng.agent.plan = lambda request, state, feedback=None: plan  # fixed plan (INPUT injection)
    out = PlanningAgent(eng).plan("classify land cover", [], "s1")
    assert out.steps[0].risk_level == "mutating"


# ── Part B: knowledge context reaches the planner prompt ───────────────

def test_knowledge_context_reaches_prompt():
    eng = _engine()

    class _Ctx:
        context_prompt = "KNOWLEDGE: use native:buffer for distance zones"

        def has_knowledge(self):
            return True

    eng.agent._last_knowledge_context = _Ctx()
    request = eng.agent.parse("buffer the roads", eng.state)
    assert "KNOWLEDGE: use native:buffer" in eng.agent._get_prompt(request)


# ── Part D3: dataclasses.asdict round-trips the plan ───────────────────

def test_plan_asdict_roundtrips():
    plan = ExecutionPlan(
        plan_id="p1",
        steps=[ToolStep(step_id="s1", tool_name="native_buffer",
                        parameters={"DISTANCE": 500}, risk_level="mutating")],
        reasoning="buffer",
        plan_source="function_calling",
    )
    d = dataclasses.asdict(plan)
    assert d["plan_id"] == "p1"
    assert d["steps"][0]["tool_name"] == "native_buffer"
    assert d["steps"][0]["parameters"]["DISTANCE"] == 500


def test_supervisor_response_has_approval_pending():
    assert "approval_pending" in {f.name for f in dataclasses.fields(SupervisorResponse)}


# ── Part D2: generate_code is review-only, never executed ──────────────

def test_generate_code_review_only():
    eng = _engine()
    tool = eng.registry.get_tool("generate_code")
    result = tool.execute(target_language="geopandas", query="dissolve by region")
    assert result.success
    assert isinstance(result.output, dict)
    assert result.output.get("requires_human_review") is True
    assert "NOT executed" in (result.message or "")


# ── Part D3: full pipeline — mutating step halts with approval_pending ──

def _patch_planner(monkeypatch_or_none, plan: ExecutionPlan):
    """Replace PlanningAgent.plan to return a fixed real plan (INPUT injection)."""
    def _plan(self, query, available_layers=None, session_id="", feedback=None):
        return plan
    PlanningAgent.plan = _plan  # type: ignore[assignment]


def test_pipeline_halts_on_mutating_step():
    plan = ExecutionPlan(
        plan_id="p-ml",
        steps=[ToolStep(step_id="s1", tool_name="machine_learning",
                        parameters={"job_type": "classification",
                                    "algorithm": "random_forest"},
                        description="classify land cover", risk_level="mutating")],
        reasoning="ml", plan_source="function_calling",
    )
    _orig = PlanningAgent.plan
    try:
        _patch_planner(None, plan)
        sup = SupervisorAgent(_RealPool())
        resp = sup.handle(SupervisorRequest(query="classify", session_id="s-ml"))
        assert resp.success is True
        assert resp.approval_pending, "mutating step must halt with an action_id"
        assert isinstance(resp.plan_json, dict)
        assert resp.plan_json["plan_id"] == "p-ml"
        steps = (resp.execution_summary or {}).get("steps", [])
        assert steps and steps[0]["approval_pending"] == resp.approval_pending
    finally:
        PlanningAgent.plan = _orig  # type: ignore[assignment]


def test_pipeline_runs_readonly_codegen_without_approval():
    plan = ExecutionPlan(
        plan_id="p-cg",
        steps=[ToolStep(step_id="s1", tool_name="generate_code",
                        parameters={"target_language": "geopandas"},
                        description="dissolve polygons", risk_level="read_only")],
        reasoning="cg", plan_source="function_calling",
    )
    _orig = PlanningAgent.plan
    try:
        _patch_planner(None, plan)
        sup = SupervisorAgent(_RealPool())
        resp = sup.handle(SupervisorRequest(query="write code", session_id="s-cg"))
        assert resp.success is True
        assert resp.approval_pending is None
        steps = (resp.execution_summary or {}).get("steps", [])
        assert steps and steps[0]["success"] is True
    finally:
        PlanningAgent.plan = _orig  # type: ignore[assignment]


# ── Direct runner (no pytest needed) ───────────────────────────────────

if __name__ == "__main__":
    import logging
    logging.disable(logging.CRITICAL)
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL  {t.__name__}: {exc!r}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    raise SystemExit(1 if failed else 0)
