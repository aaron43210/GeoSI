"""Offline capability: parsing, deterministic planners and exact answers (no QGIS, no model)."""

import pytest

from geosi_data.osm import single_geometry
from geosi_engine import GeoSI
from geosi_engine.agents.report_generation import superlative_answer
from geosi_engine.base import PortableTool, attach_ui, drain_ui_actions, run_in_ui
from geosi_engine.models import AnalysisRequest, Layer, ToolParameter, ToolResult, ToolSpec
from geosi_engine.parser import QueryParser

LAYERS = ["hospitals", "flood_zones", "parcels", "roads", "dem"]


@pytest.fixture(scope="module")
def parser():
    return QueryParser(use_llm=False, use_cache=False)


# ── Parser ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "query, filters",
    [
        ("dissolve parcels by owner", None),  # "dis-solve" is not field d / op is / value solve
        ("what is NDVI?", None),
        ("extract parcels where owner is 'A'", [{"field": "owner", "op": "is", "value": "A"}]),
        ("select parcels where area > 500", [{"field": "area", "op": ">", "value": "500"}]),
        ("select hospitals where beds>=100", [{"field": "beds", "op": ">=", "value": "100"}]),
    ],
)
def test_field_filters(parser, query, filters):
    assert parser.parse(query, LAYERS).parameters.get("filters") == filters


@pytest.mark.parametrize(
    "query, primary, secondary",
    [
        ("clip roads to flood_zones", "roads", "flood_zones"),
        ("clip flood_zones to roads", "flood_zones", "roads"),
        ("join each hospital to the flood zone it falls in", "hospitals", "flood_zones"),
        ("buffer the flood zones by 100 m", "flood_zones", None),
    ],
)
def test_layer_roles_follow_word_order(parser, query, primary, secondary):
    entities = parser.parse(query, LAYERS).entities
    assert (entities.get("primary_layer"), entities.get("secondary_layer")) == (primary, secondary)


# ── Deterministic planners ──────────────────────────────────────────────


class _FakeTool(PortableTool):
    def __init__(self, name, params):
        self._name, self._params = name, params

    def spec(self):
        return ToolSpec(
            name=self._name,
            display_name=self._name,
            description="fake",
            category="test",
            parameters=[ToolParameter(p, "string", True, p) for p in self._params],
        )

    def execute(self, **kwargs):
        return ToolResult(success=True)


@pytest.fixture()
def engine():
    eng = GeoSI(use_llm=False)
    eng.registry.register_tool(_FakeTool("native_extractbylocation", ["INPUT", "PREDICATE", "INTERSECT"]))
    for name in ("hospitals", "flood_zones"):
        eng.state.add_layer(
            Layer(
                name=name,
                geometry_type="Point" if name == "hospitals" else "Polygon",
                feature_count=3,
                layer_type="vector",
            )
        )
    return eng


def _plan(engine, planner, query):
    req = AnalysisRequest(query=query, available_layers=engine.state.list_layers())
    plan = getattr(engine.agent, planner)(req, engine.state)
    return (plan.steps[0].tool_name, plan.steps[0].parameters) if plan else None


@pytest.mark.parametrize(
    "query, expected",
    [
        ("Add an OpenStreetMap basemap", ("add_basemap", {"provider": "osm"})),
        ("add a satellite basemap", ("add_basemap", {"provider": "esri_satellite"})),
        ("zoom to Paris", ("zoom_to_place", {"address": "Paris"})),
        ("fetch hospitals in Leeds from OpenStreetMap", ("fetch_osm", {"category": "hospitals", "location": "Leeds"})),
        ("where is Nairobi?", ("geocode_address", {"address": "Nairobi"})),
        ("zoom to hospitals", None),  # a loaded layer, not a place
        ("what is a basemap?", None),
        ("buffer hospitals by 500 m", None),
    ],
)
def test_open_data_planner(engine, query, expected):
    assert _plan(engine, "_plan_open_data", query) == expected


@pytest.mark.parametrize(
    "query, predicate",
    [
        ("how many hospitals are inside flood_zones?", "intersect"),
        ("select hospitals that are outside flood_zones", "disjoint"),
        ("count the hospitals inside each flood_zones polygon", None),  # per-zone count, not a selection
        ("find hospitals within 1 km of flood_zones", None),  # distance → buffer first
    ],
)
def test_spatial_selection_planner(engine, query, predicate):
    got = _plan(engine, "_plan_spatial_selection", query)
    if predicate is None:
        assert got is None
    else:
        assert got == (
            "native_extractbylocation",
            {"INPUT": "hospitals", "PREDICATE": predicate, "INTERSECT": "flood_zones"},
        )


# ── Exact answers ───────────────────────────────────────────────────────

ZONES = [{"zone": "Z1", "NUMPOINTS": 1}, {"zone": "Z2", "NUMPOINTS": 3}, {"zone": "Z3", "NUMPOINTS": 0}]


def test_superlative_uses_the_users_words():
    assert superlative_answer("which flood zone has the most hospitals?", ZONES, ["NUMPOINTS"]) == (
        "Z2 has the most hospitals (3)."
    )
    assert superlative_answer("which zone has the fewest hospitals", ZONES, ["NUMPOINTS"]) == (
        "Z3 has the fewest hospitals (0)."
    )


def test_superlative_reports_ties_and_ignores_ids():
    rows = [
        {"id": 1, "name": "A", "beds": 120},
        {"id": 2, "name": "B", "beds": 300},
        {"id": 3, "name": "C", "beds": 300},
    ]
    assert superlative_answer("which hospital has the most beds?", rows) == "B, C have the most beds (300)."


def test_superlative_only_answers_superlatives():
    assert superlative_answer("how many hospitals?", ZONES) is None
    assert superlative_answer("which zone has the most hospitals?", []) is None


# ── OpenStreetMap geometry ──────────────────────────────────────────────


def _fc(*geoms):
    return {
        "type": "FeatureCollection",
        "features": [{"type": "Feature", "geometry": g, "properties": {}} for g in geoms],
    }


def test_points_keep_outlines_as_centre_points():
    square = {"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}
    out, kind = single_geometry(
        _fc({"type": "Point", "coordinates": [5, 5]}, {"type": "Point", "coordinates": [6, 6]}, square)
    )
    assert kind == "Point" and len(out["features"]) == 3
    assert out["features"][2]["geometry"] == {"type": "Point", "coordinates": [1.0, 1.0]}


def test_polygons_drop_stray_points():
    sq = {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]]}
    out, kind = single_geometry(_fc(sq, sq, {"type": "Point", "coordinates": [0, 0]}))
    assert kind == "Polygon" and len(out["features"]) == 2


# ── Main-thread queue for map actions ───────────────────────────────────


def test_ui_actions_run_now_without_a_ui_and_queue_with_one():
    calls = []
    assert run_in_ui("now", lambda: calls.append(1) or "done") == "done" and calls == [1]
    attach_ui(True)
    try:
        assert run_in_ui("later", lambda: calls.append(2)) is None and calls == [1]
        queued = drain_ui_actions()
        assert [d for d, _ in queued] == ["later"]
        queued[0][1]()
        assert calls == [1, 2] and drain_ui_actions() == []
    finally:
        attach_ui(False)


def test_map_actions_pass_verification_without_a_layer(engine):
    from types import SimpleNamespace

    from geosi_engine.agents.verification import VerificationAgent

    plan = SimpleNamespace(steps=[SimpleNamespace(tool_name="add_basemap", output_name="step_1_output")])
    result = SimpleNamespace(logs=[], results={"step_1_output": {"basemap": "osm"}})
    assert VerificationAgent(engine).verify("add a basemap", plan, result).passed


# ── Model-first routing ─────────────────────────────────────────────────


def _routing_engine(model_ok, model_plan=None):
    eng = GeoSI(use_llm=True)
    eng.agent.model_available = model_ok
    eng.registry.register_tool(_FakeTool("native_buffer", ["INPUT", "DISTANCE"]))
    eng.state.add_layer(Layer(name="hospitals", geometry_type="Point", feature_count=3, layer_type="vector"))
    calls = []

    def provider(request):
        calls.append(request.query)
        if model_plan is None:
            raise RuntimeError("model down")
        return model_plan

    eng.agent._llm_providers = lambda: [("ollama", provider)]
    return eng, calls


def _buffer_request(eng):
    return eng.agent.parse("buffer hospitals by 500 m", eng.state)


def test_connected_model_plans_even_simple_tasks():
    from geosi_engine.models import ExecutionPlan, ToolStep

    model_plan = ExecutionPlan(
        steps=[ToolStep(step_id="s1", tool_name="native_buffer", parameters={"INPUT": "hospitals", "DISTANCE": 500})]
    )
    eng, calls = _routing_engine(True, model_plan)
    plan = eng.agent.plan(_buffer_request(eng), eng.state)
    assert calls and plan.plan_source.startswith("ollama:")


def test_model_failure_falls_back_to_rules():
    eng, calls = _routing_engine(True, None)
    plan = eng.agent.plan(_buffer_request(eng), eng.state)
    assert calls and plan.plan_source == "rule_based" and plan.steps[0].tool_name == "native_buffer"


def test_offline_never_calls_the_model():
    eng, calls = _routing_engine(False, None)
    plan = eng.agent.plan(_buffer_request(eng), eng.state)
    assert not calls and plan.plan_source == "rule_based"


def test_retry_with_feedback_is_model_only():
    eng, calls = _routing_engine(True, None)
    plan = eng.agent.plan(_buffer_request(eng), eng.state, feedback="wrong layer")
    assert calls and not plan.steps
