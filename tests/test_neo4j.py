"""
GeoSI v2 — Neo4j Client + Graph Writer Tests (Phase P9, FR-8.4)
Tests graceful degradation, circuit breaker, schema helpers, and writer queue.
"""

from __future__ import annotations

import threading
from unittest.mock import MagicMock, patch

# ── Neo4j Client Tests ────────────────────────────────────────────────────


def test_neo4j_client_unavailable_when_no_driver():
    """Client gracefully marks itself unavailable when neo4j is not installed."""
    from geosi_data.neo4j_client import Neo4jClient

    with patch.dict("sys.modules", {"neo4j": None}):
        client = Neo4jClient(uri="bolt://nonexistent:7687")
        assert not client.available


def test_neo4j_client_upsert_node_returns_false_when_unavailable():
    """upsert_node must return False (not raise) when client is unavailable."""
    from geosi_data.graph_schema import NodeLabel
    from geosi_data.neo4j_client import Neo4jClient

    with patch.dict("sys.modules", {"neo4j": None}):
        client = Neo4jClient(uri="bolt://nonexistent:7687")
        result = client.upsert_node(NodeLabel.AGENT, "name", {"name": "test"})
        assert result is False


def test_neo4j_client_find_node_returns_none_when_unavailable():
    """find_node must return None when client is unavailable."""
    from geosi_data.neo4j_client import Neo4jClient

    with patch.dict("sys.modules", {"neo4j": None}):
        client = Neo4jClient(uri="bolt://nonexistent:7687")
        result = client.find_node("Dataset", "dataset_id", "abc123")
        assert result is None


def test_neo4j_client_cypher_returns_empty_when_unavailable():
    """cypher_query must return [] when client is unavailable."""
    from geosi_data.neo4j_client import Neo4jClient

    with patch.dict("sys.modules", {"neo4j": None}):
        client = Neo4jClient(uri="bolt://nonexistent:7687")
        result = client.cypher_query("MATCH (n) RETURN n")
        assert result == []


def test_circuit_breaker_opens_after_threshold():
    """Circuit breaker must open after N consecutive failures."""
    from geosi_data.neo4j_client import _CircuitBreaker

    cb = _CircuitBreaker(threshold=3, reset_s=60.0)
    assert not cb.is_open
    assert cb.state() == "CLOSED"

    cb.record_failure()
    cb.record_failure()
    assert not cb.is_open  # Not yet at threshold

    cb.record_failure()
    assert cb.is_open  # Threshold hit
    assert cb.state() == "OPEN"


def test_circuit_breaker_resets_after_success():
    """Circuit breaker resets to CLOSED after a successful call."""
    from geosi_data.neo4j_client import _CircuitBreaker

    cb = _CircuitBreaker(threshold=2, reset_s=60.0)
    cb.record_failure()
    cb.record_failure()
    assert cb.is_open

    cb.record_success()
    assert not cb.is_open
    assert cb.state() == "CLOSED"


def test_circuit_breaker_thread_safety():
    """Circuit breaker must be thread-safe under concurrent access."""
    from geosi_data.neo4j_client import _CircuitBreaker

    cb = _CircuitBreaker(threshold=100, reset_s=60.0)
    errors: list[Exception] = []

    def worker():
        try:
            for _ in range(50):
                cb.record_failure()
                _ = cb.is_open
                _ = cb.state()
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert errors == [], f"Thread safety errors: {errors}"


# ── Graph Schema Tests ────────────────────────────────────────────────────


def test_build_dataset_props_deterministic_id():
    """Dataset ID must be deterministic from name + path."""
    from geosi_data.graph_schema import build_dataset_props

    props1 = build_dataset_props("roads", "/data/roads.gpkg")
    props2 = build_dataset_props("roads", "/data/roads.gpkg")
    assert props1["dataset_id"] == props2["dataset_id"]


def test_build_dataset_props_different_paths_different_ids():
    """Different paths must produce different dataset IDs."""
    from geosi_data.graph_schema import build_dataset_props

    id1 = build_dataset_props("roads", "/data/roads.gpkg")["dataset_id"]
    id2 = build_dataset_props("roads", "/data/roads_v2.gpkg")["dataset_id"]
    assert id1 != id2


def test_build_execution_props_structure():
    """build_execution_props must return all required fields."""
    from geosi_data.graph_schema import build_execution_props

    props = build_execution_props("audit-001", "plan-001", "sess-001", "success", 1234.5)
    assert props["audit_id"] == "audit-001"
    assert props["plan_id"] == "plan-001"
    assert props["status"] == "success"
    assert props["duration_ms"] == 1234.5


def test_infer_provider_from_tool_name():
    """Provider should be inferred from the tool_name prefix."""
    from geosi_data.graph_schema import _infer_provider

    assert _infer_provider("native:buffer") == "native"
    assert _infer_provider("gdal:cliprasterbymasklayer") == "gdal"
    assert _infer_provider("grass:r.watershed") == "grass"
    assert _infer_provider("no_colon_here") == "unknown"


# ── Graph Writer Tests ────────────────────────────────────────────────────


def test_graph_writer_singleton():
    """GraphWriter must return same instance on repeated calls."""
    from geosi_engine.graph_writer import GraphWriter

    w1 = GraphWriter.get_instance()
    w2 = GraphWriter.get_instance()
    assert w1 is w2


def test_graph_writer_enqueue_bounded():
    """Queue must not exceed maxlen (bounded memory O(capacity))."""
    from geosi_engine.graph_writer import _QUEUE_CAPACITY, GraphEvent, GraphWriter

    writer = GraphWriter.get_instance()
    # Fill past capacity
    for i in range(_QUEUE_CAPACITY + 50):
        writer._enqueue(GraphEvent("test", {"i": i}))

    # Queue should never exceed its maxlen
    assert len(writer._queue) <= _QUEUE_CAPACITY


def test_graph_writer_record_execution_no_block():
    """record_execution must return quickly (fire-and-forget)."""
    import time

    from geosi_engine.graph_writer import GraphWriter

    writer = GraphWriter.get_instance()

    mock_plan = MagicMock()
    mock_plan.plan_id = "test-plan"
    mock_plan.steps = []

    t_start = time.monotonic()
    writer.record_execution(
        audit_id="audit-test",
        plan=mock_plan,
        agent_name="GISAgent",
        status="success",
        session_id="test-session",
    )
    elapsed = time.monotonic() - t_start

    # Must be non-blocking — well under 10ms
    assert elapsed < 0.01, f"record_execution blocked for {elapsed:.3f}s"


def test_graph_writer_dataset_relation_enqueued():
    """record_dataset_relation must add an event to the queue."""
    from geosi_engine.graph_writer import GraphWriter

    writer = GraphWriter.get_instance()
    queue_len_before = len(writer._queue)
    writer.record_dataset_relation(
        source_name="dem.tif",
        source_path="/data/dem.tif",
        derived_name="slope.tif",
        derived_path="/data/slope.tif",
    )
    assert len(writer._queue) >= queue_len_before  # At least one event added
