"""Unit tests for the plan → execute → verify → re-plan loop (no QGIS, no LLM)."""

from geosi_engine.agent_loop import AgentLoop
from geosi_engine.models import (
    AnalysisRequest, ExecutionPlan, ExecutionResult, ExecutionStatus, Layer, StepLog, ToolStep,
)
from geosi_engine.state import StateManager


def _layer(name, geom, n=3, kind="vector"):
    return Layer(name=name, geometry_type=geom, feature_count=n, layer_type=kind, filepath=f"/tmp/{name}")


def _plan(tool="native_buffer"):
    return ExecutionPlan(request=AnalysisRequest(query="q"), steps=[
        ToolStep(step_id="step_1", tool_name=tool, parameters={"INPUT": "hospitals"}, output_name="out"),
    ])


def _result(output=None, ok=True, error=None):
    log = StepLog(step_id="step_1", tool_name="native_buffer",
                  status=ExecutionStatus.SUCCESS if ok else ExecutionStatus.FAILED, error_message=error)
    return ExecutionResult(success=ok, answer="✅ done" if ok else "❌", results={"out": output}, logs=[log])


class FakeAgent:
    def __init__(self, plans, replan=True):
        self.plans = list(plans)
        self.feedback = []
        self._replan = replan

    def parse(self, query, state):
        return AnalysisRequest(query=query)

    def plan(self, request, state, feedback=None):
        self.feedback.append(feedback)
        return self.plans.pop(0) if self.plans else ExecutionPlan(request=request)

    def can_replan(self):
        return self._replan

    def answer_from_evidence(self, question, evidence):
        return f"ANSWER from {evidence.splitlines()[0]}"


class FakeExecutor:
    def __init__(self, results):
        self.results = list(results)

    def run(self, plan, step_runner=None):
        if not plan.steps:
            return ExecutionResult(success=False, answer=plan.reasoning or "nothing to do")
        return self.results.pop(0)


class FakeEngine:
    def __init__(self, plans, results, replan=True):
        self.state = StateManager()
        self.state.add_layer(_layer("hospitals", "Point", 10))
        self.state.add_layer(_layer("flood_zones", "Polygon", 2))
        self.agent = FakeAgent(plans, replan)
        self.executor = FakeExecutor(results)


def test_success_first_try():
    eng = FakeEngine([_plan()], [_result(_layer("buf", "Polygon"))])
    res = AgentLoop(eng).run("buffer hospitals by 500 m")
    assert res.success
    assert eng.agent.feedback == [None]


def test_failed_step_triggers_replan_with_error():
    eng = FakeEngine([_plan(), _plan()], [_result(ok=False, error="Missing INPUT"), _result(_layer("b", "Polygon"))])
    res = AgentLoop(eng).run("buffer hospitals by 500 m")
    assert res.success
    assert "Missing INPUT" in eng.agent.feedback[1]
    assert "Attempt 1" in res.reasoning


def test_empty_output_is_rejected():
    eng = FakeEngine([_plan(), _plan()], [_result(_layer("x", "Point", 0)), _result(_layer("y", "Point", 4))])
    res = AgentLoop(eng).run("buffer hospitals by 500 m")
    assert res.success
    assert "0 features" in eng.agent.feedback[1]


def test_wrong_geometry_for_subject_is_rejected():
    # "find hospitals ..." must return points; polygons mean swapped inputs
    eng = FakeEngine([_plan(), _plan()], [_result(_layer("z", "Polygon", 2)), _result(_layer("h", "Point", 7))])
    res = AgentLoop(eng).run("find hospitals within 1 km of flood_zones")
    assert res.success
    assert "hospitals" in eng.agent.feedback[1] and "point" in eng.agent.feedback[1]


def test_gives_up_honestly_and_drops_wrong_layers():
    bad = lambda: _result(_layer("z", "Polygon", 2))  # noqa: E731
    eng = FakeEngine([_plan(), _plan(), _plan()], [bad(), bad(), bad()])
    res = AgentLoop(eng, max_attempts=3).run("find hospitals within 1 km of flood_zones")
    assert not res.success
    assert res.results == {}
    assert "after 3 attempt" in res.answer


def test_no_replan_without_llm():
    eng = FakeEngine([_plan()], [_result(ok=False, error="boom")], replan=False)
    res = AgentLoop(eng).run("buffer hospitals by 500 m")
    assert not res.success and len(eng.agent.feedback) == 1


def test_destructive_request_is_refused():
    eng = FakeEngine([_plan()], [_result(_layer("b", "Polygon"))])
    res = AgentLoop(eng).run("delete all hospitals")
    assert not res.success
    assert eng.agent.feedback == []  # never planned


def test_remove_duplicates_is_not_destructive():
    eng = FakeEngine([_plan()], [_result(_layer("b", "Point"))])
    assert AgentLoop(eng).run("remove duplicate geometries from hospitals").success


def test_non_question_without_layer_is_rejected():
    eng = FakeEngine([_plan(), _plan()], [_result("a message"), _result(_layer("b", "Polygon"))])
    res = AgentLoop(eng).run("buffer hospitals by 500 m")
    assert res.success
    assert "no result layer" in eng.agent.feedback[1]


def test_question_answered_from_evidence():
    eng = FakeEngine([_plan()], [_result({"COUNT": 10})])
    res = AgentLoop(eng).run("how many hospitals are there?")
    assert res.success
    assert res.answer.startswith("ANSWER from")


def test_stop_before_running():
    eng = FakeEngine([_plan()], [_result(_layer("b", "Polygon"))])
    loop = AgentLoop(eng)
    loop.should_stop = lambda: True
    res = loop.run("buffer hospitals by 500 m")
    assert not res.success and "Stopped" in res.answer


def test_each_layer_feature_count_is_checked():
    # "in each flood_zones polygon" → one output feature per zone (2)
    eng = FakeEngine([_plan(), _plan()], [_result(_layer("p", "Polygon", 5)), _result(_layer("z", "Polygon", 2))])
    res = AgentLoop(eng).run("count the hospitals inside each flood_zones polygon")
    assert res.success
    assert "each feature of 'flood_zones'" in eng.agent.feedback[1]


def test_multi_step_request_is_chained():
    eng = FakeEngine([_plan(), _plan()], [_result(_layer("buffer_result", "Polygon", 3)),
                                          _result(_layer("dissolve_result", "Polygon", 1))])
    res = AgentLoop(eng).run("buffer hospitals by 200 m and dissolve the result")
    assert res.success
    assert "2 steps" in res.answer
    assert eng.state.get_layer("buffer_result") is not None  # intermediate is addressable


def test_missing_named_layer_is_reported():
    eng = FakeEngine([_plan()], [_result(_layer("b", "Polygon"))])
    res = AgentLoop(eng).run("buffer the schools layer by 100 m")
    assert not res.success and "schools" in res.answer


def test_how_many_uses_exact_feature_count():
    eng = FakeEngine([_plan()], [_result(_layer("filtered", "Point", 3))])
    res = AgentLoop(eng).run("how many hospitals have more than 200 beds?")
    assert res.success and res.answer.startswith("3 ")


def test_into_one_layer_is_not_a_missing_layer():
    eng = FakeEngine([_plan()], [_result(_layer("merged", "Polygon", 6))])
    assert AgentLoop(eng).run("merge hospitals and flood_zones into one layer").success


def test_each_check_allows_different_geometry():
    # "5 random points in each zone" → 10 points is right, not "one per zone"
    eng = FakeEngine([_plan()], [_result(_layer("pts", "Point", 10))])
    assert AgentLoop(eng).run("create 5 random points inside each flood_zones polygon").success


# ── Conversational / layer-free tests ────────────────────────────────────────

def test_greeting_answered_without_layers():
    """'hi' must succeed even with no layers loaded."""
    eng = FakeEngine([], [])  # no layers, no plans, no results
    eng.state = __import__("geosi_engine.state", fromlist=["StateManager"]).StateManager()
    res = __import__("geosi_engine.agent_loop", fromlist=["AgentLoop"]).AgentLoop(eng).run("hi")
    assert res.success
    assert "GeoSI" in res.answer or "hi" in res.answer.lower() or res.answer


def test_gis_question_not_blocked_without_layers():
    """Educational GIS questions must not be rejected when no layers are loaded."""
    from geosi_engine.agent_loop import AgentLoop
    from geosi_engine.state import StateManager
    eng = FakeEngine([], [])
    eng.state = StateManager()
    res = AgentLoop(eng).run("What is NDVI?")
    # Must succeed (answer or no-steps graceful) — must NOT return the "no layers" error
    assert "No layers" not in (res.answer or "")
    assert "No layers" not in (res.error or "")


def test_code_gen_not_blocked_without_layers():
    """Code-gen queries must not be rejected when no layers are loaded."""
    from geosi_engine.agent_loop import AgentLoop
    from geosi_engine.state import StateManager
    eng = FakeEngine([], [])
    eng.state = StateManager()
    res = AgentLoop(eng).run("Generate GeoPandas code to buffer points by 500 m")
    assert "No layers" not in (res.answer or "")
    assert "No layers" not in (res.error or "")


def test_validation_check_request_skips_greeting():
    """check_request must not report missing layers for a greeting."""
    from geosi_engine.agents.validation import ValidationAgent
    from geosi_engine.state import StateManager
    eng = FakeEngine([], [])
    eng.state = StateManager()
    va = ValidationAgent(eng)
    assert va.check_request("hello, what can you do?", eng.state) is None


def test_validation_check_request_skips_knowledge_query():
    """check_request must not report missing layers for a knowledge question."""
    from geosi_engine.agents.validation import ValidationAgent
    from geosi_engine.state import StateManager
    eng = FakeEngine([], [])
    eng.state = StateManager()
    va = ValidationAgent(eng)
    assert va.check_request("What is a CRS and how do I reproject?", eng.state) is None
