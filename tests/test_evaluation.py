"""
GeoSI v2 — Evaluation Tests (Phase P2, FR-7.1/7.2)
golden_set is imported without the 'tests.' prefix because pytest
adds the tests/ directory to sys.path automatically.
"""

from __future__ import annotations

import os
import sys

# Ensure tests/ is on the path so golden_set.py can be imported directly
_TESTS_DIR = os.path.dirname(__file__)
if _TESTS_DIR not in sys.path:
    sys.path.insert(0, _TESTS_DIR)


# ── Golden Set Tests ──────────────────────────────────────────────────────


def test_golden_set_has_exactly_150_queries():
    """FR-7.1: Golden set must have exactly 150 queries."""
    from golden_set import GOLDEN_SET

    assert len(GOLDEN_SET) == 150


def test_golden_set_no_duplicate_ids():
    """All query IDs must be unique."""
    from golden_set import GOLDEN_SET

    ids = [q.query_id for q in GOLDEN_SET]
    assert len(ids) == len(set(ids)), "Duplicate query IDs found"


def test_golden_set_agent_scopes():
    """Each agent scope must have the exact expected count."""
    from golden_set import load_golden_set

    assert len(load_golden_set("planning")) == 50
    assert len(load_golden_set("research")) == 25
    assert len(load_golden_set("gis")) == 25
    assert len(load_golden_set("geology")) == 20
    assert len(load_golden_set("remote_sensing")) == 15
    assert len(load_golden_set("ml")) == 15


def test_golden_set_all_have_query_and_answer():
    """Every query must have non-empty query text and expected_answer."""
    from golden_set import GOLDEN_SET

    for q in GOLDEN_SET:
        assert q.query, f"Query {q.query_id} has empty query"
        assert q.expected_answer, f"Query {q.query_id} has empty expected_answer"


def test_load_golden_set_filter_returns_subset():
    """load_golden_set with scope filter returns correct subset only."""
    from golden_set import GOLDEN_SET, load_golden_set

    planning = load_golden_set("planning")
    assert all(q.agent_scope == "planning" for q in planning)
    assert len(planning) < len(GOLDEN_SET)


def test_load_golden_set_none_returns_all():
    """load_golden_set(None) returns the full 150-query set."""
    from golden_set import GOLDEN_SET, load_golden_set

    all_queries = load_golden_set(None)
    assert len(all_queries) == len(GOLDEN_SET)


def test_golden_set_query_ids_have_correct_prefix():
    """Query IDs must follow naming convention (prefix + 3-digit number)."""
    from golden_set import GIS_QUERIES, PLANNING_QUERIES, RESEARCH_QUERIES

    for q in PLANNING_QUERIES:
        assert q.query_id.startswith("P")
    for q in RESEARCH_QUERIES:
        assert q.query_id.startswith("R")
    for q in GIS_QUERIES:
        assert q.query_id.startswith("G")


# ── RAGAS Runner Tests ────────────────────────────────────────────────────


def test_ragas_runner_initialises_without_ragas_installed():
    """RAGASRunner must initialise without crashing when ragas is not installed."""
    from geosi_engine.evaluation.ragas_runner import RAGASRunner

    runner = RAGASRunner(engine=None)
    assert runner is not None
    # ragas not installed in test env → heuristic mode
    assert isinstance(runner._ragas_available, bool)


def test_ragas_runner_heuristic_score_perfect_overlap():
    """Heuristic scorer returns high scores when answer terms appear in contexts."""
    from geosi_engine.evaluation.ragas_runner import GoldenQuery, RAGASRunner

    runner = RAGASRunner(engine=None)
    q = GoldenQuery(
        query_id="T001",
        query="NDVI vegetation",
        expected_answer="NDVI vegetation analysis uses NIR and RED bands",
        contexts=["NDVI vegetation analysis NIR RED"],
        agent_scope="research",
    )
    scores = runner._heuristic_score(q, q.contexts)
    assert scores["faithfulness"] > 0.5
    assert scores["context_precision"] > 0.5


def test_ragas_runner_heuristic_zero_score_no_overlap():
    """Heuristic scorer returns near-zero faithfulness when no overlap exists."""
    from geosi_engine.evaluation.ragas_runner import GoldenQuery, RAGASRunner

    runner = RAGASRunner(engine=None)
    q = GoldenQuery(
        query_id="T002",
        query="aaaa bbbb cccc",
        expected_answer="xxxx yyyy zzzz",
        contexts=["completely different content here"],
        agent_scope="gis",
    )
    scores = runner._heuristic_score(q, q.contexts)
    assert scores["faithfulness"] == 0.0  # No overlap between answer and contexts


def test_ragas_runner_heuristic_empty_context():
    """Heuristic scorer handles empty context gracefully — no ZeroDivisionError."""
    from geosi_engine.evaluation.ragas_runner import GoldenQuery, RAGASRunner

    runner = RAGASRunner(engine=None)
    q = GoldenQuery("T003", "buffer", "Use native:buffer", contexts=[], agent_scope="gis")
    scores = runner._heuristic_score(q, [])
    assert scores["context_precision"] == 0.0
    assert 0.0 <= scores["faithfulness"] <= 1.0
    assert 0.0 <= scores["answer_relevancy"] <= 1.0


def test_ragas_runner_run_small_set():
    """Runner completes a 6-query set and returns a valid summary."""
    from golden_set import load_golden_set

    from geosi_engine.evaluation.ragas_runner import RAGASRunner

    runner = RAGASRunner(engine=None, batch_size=3)
    queries = load_golden_set("gis")[:6]
    summary = runner.run(queries)

    assert summary.total_queries == 6
    assert 0.0 <= summary.mean_faithfulness <= 1.0
    assert 0.0 <= summary.mean_context_precision <= 1.0
    assert isinstance(summary.per_agent, dict)
    assert "gis" in summary.per_agent
    # Heuristic mode → gate is always False (only real RAGAS + LLM can PASS)
    assert not summary.gate_passed


def test_ragas_runner_batch_streaming_fewer_than_batch():
    """Runner handles N < batch_size correctly without padding errors."""
    from golden_set import load_golden_set

    from geosi_engine.evaluation.ragas_runner import RAGASRunner

    runner = RAGASRunner(engine=None, batch_size=20)
    queries = load_golden_set("ml")[:5]  # 5 < batch_size=20
    summary = runner.run(queries)
    assert summary.total_queries == 5


def test_ragas_summary_per_agent_breakdown():
    """Per-agent breakdown includes all agent scopes present in the queried sample."""
    from golden_set import GOLDEN_SET

    from geosi_engine.evaluation.ragas_runner import RAGASRunner

    runner = RAGASRunner(engine=None, batch_size=10)
    queries = GOLDEN_SET[:20]
    summary = runner.run(queries)

    scopes_in_queries = {q.agent_scope for q in queries}
    for scope in scopes_in_queries:
        assert scope in summary.per_agent, f"Missing scope '{scope}' in per_agent breakdown"


def test_ragas_eval_result_error_gives_passed_false():
    """EvalResult with an error must not be counted as passed."""
    from geosi_engine.evaluation.ragas_runner import EvalResult

    r = EvalResult(query_id="ERR1", query="test", agent_scope="gis", error="simulated error")
    assert not r.passed


def test_ragas_runner_duration_recorded():
    """EvalRunSummary must record positive duration_s."""
    from golden_set import load_golden_set

    from geosi_engine.evaluation.ragas_runner import RAGASRunner

    runner = RAGASRunner(engine=None, batch_size=5)
    summary = runner.run(load_golden_set("research")[:5])
    assert summary.duration_s > 0.0


def test_ragas_thresholds_match_prd():
    """Threshold constants must match PRD §2 Goal 6 (faithfulness ≥ 0.85, precision ≥ 0.75)."""
    from geosi_engine.evaluation.ragas_runner import CONTEXT_PRECISION_THRESHOLD, FAITHFULNESS_THRESHOLD

    assert FAITHFULNESS_THRESHOLD == 0.85
    assert CONTEXT_PRECISION_THRESHOLD == 0.75
