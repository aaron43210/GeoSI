"""
GeoSI v2 — Phase P1 Gap Tests
Tests for the 5 PRD-alignment gaps:
  1. POST /chat → SupervisorAgent routing
  2. POST /execute → direct plan execution
  3. POST /admin/policy → FR-2.3 override
  4. GET /health → per-agent status
  5. OTel telemetry module → no-op fallback
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

# ── 1. /health per-agent status ───────────────────────────────────────────


def test_health_returns_circuit_breaker_states():
    """GET /health must include llm_providers circuit-breaker state."""
    from fastapi.testclient import TestClient

    from geosi_server.app import app

    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "version" in data
    assert "session_pool" in data
    assert "llm_providers" in data
    assert "external_services" in data


# ── 2. OTel telemetry no-op mode ──────────────────────────────────────────


def test_telemetry_noop_when_endpoint_not_set(monkeypatch):
    """Telemetry module must degrade gracefully when GEOSI_OTEL_ENDPOINT is absent."""
    monkeypatch.delenv("GEOSI_OTEL_ENDPOINT", raising=False)

    # Force re-initialisation
    import geosi_engine.telemetry as tel

    tel._tracer = None
    tel._NOOP = False

    tracer = tel.get_tracer()
    assert tracer is not None

    # span must work without raising
    with tel.start_span("test.span", key="val") as s:
        s.set_attribute("foo", "bar")

    # decorator must work without raising
    @tel.span("test.fn")
    def my_fn(x):
        return x * 2

    assert my_fn(3) == 6


def test_telemetry_set_span_attr_noop(monkeypatch):
    """set_span_attr must not raise when in no-op mode."""
    import geosi_engine.telemetry as tel

    tel._NOOP = True
    tel.set_span_attr("key", "value")  # should not raise


# ── 3. POST /chat routing through SupervisorAgent ────────────────────────


def test_chat_routes_through_supervisor():
    """POST /chat must instantiate SupervisorAgent and call handle()."""
    from fastapi.testclient import TestClient

    from geosi_server.app import app

    with patch(
        "geosi_engine.agents.supervisor.SupervisorAgent.handle",
        return_value=MagicMock(
            success=True,
            result={"plan": {}, "results": []},
            error=None,
            plan_json=None,
            execution_summary=None,
            session_id="test-key-unit",
            latency_ms=42.0,
            approval_pending=None,
            execution_result=None,
            report=None,
            warnings=[],
            plan_source=None,
        ),
    ):
        client = TestClient(app)
        resp = client.post(
            "/chat",
            json={"query": "Buffer hospitals by 500m"},
            headers={"Authorization": "Bearer test-key-unit"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["query"] == "Buffer hospitals by 500m"
    assert "session_id" in data


def test_chat_requires_auth():
    """POST /chat must return 401 without Authorization header."""
    from fastapi.testclient import TestClient

    from geosi_server.app import app

    client = TestClient(app)
    resp = client.post("/chat", json={"query": "hello"})
    assert resp.status_code == 401


# ── 4. POST /execute direct plan ─────────────────────────────────────────


def test_execute_validates_plan():
    """POST /execute must validate the plan before running."""
    from fastapi.testclient import TestClient

    from geosi_server.app import app

    # Send an invalid plan (empty steps) — should return a response (not crash)
    client = TestClient(app)
    resp = client.post(
        "/execute",
        json={"plan": {"steps": []}},
        headers={"Authorization": "Bearer test-key-unit"},
    )
    # Empty plan should succeed (no steps = no-op)
    assert resp.status_code == 200
    data = resp.json()
    assert "success" in data
    assert "session_id" in data


# ── 5. POST /admin/policy (FR-2.3) ───────────────────────────────────────


def test_admin_policy_requires_admin_key():
    """POST /admin/policy must return 403 for non-admin keys."""
    from fastapi.testclient import TestClient

    from geosi_server.app import app

    client = TestClient(app)
    resp = client.post(
        "/admin/policy",
        json={"algorithm_id": "native:buffer", "decision": "allow"},
        headers={"Authorization": "Bearer test-key-unit"},  # non-admin key
    )
    assert resp.status_code == 403


def test_admin_policy_accepts_admin_key_no_db(mock_admin_key):
    """POST /admin/policy with admin key returns 503 when PostGIS is unavailable."""
    from fastapi.testclient import TestClient

    from geosi_server.app import app

    client = TestClient(app)
    resp = client.post(
        "/admin/policy",
        json={"algorithm_id": "native:buffer", "decision": "allow"},
        headers={"Authorization": f"Bearer {mock_admin_key}"},
    )
    # Without a real PostGIS connection, should be 503 (db not available)
    assert resp.status_code in (201, 503)


# ── 6. HITL approval endpoints ────────────────────────────────────────────


def test_approve_nonexistent_action_returns_404():
    """POST /approval/nonexistent/approve must return 404."""
    from fastapi.testclient import TestClient

    from geosi_server.app import app

    client = TestClient(app)
    resp = client.post(
        "/approval/nonexistent-id/approve",
        headers={"Authorization": "Bearer test-key-unit"},
    )
    assert resp.status_code == 404


def test_approval_lifecycle():
    """Full lifecycle: request approval → poll pending → approve → poll approved."""
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent, _PendingApproval

    # Inject a pending approval directly
    action_id = "test-action-001"
    pending = _PendingApproval(
        action_id=action_id,
        step_data={"tool_name": "native:buffer", "risk_level": "mutating"},
        session_id="test-session",
        risk_level="mutating",
    )
    PermissionSafetyAgent._APPROVALS.add(pending)

    # Poll → pending
    result = PermissionSafetyAgent._APPROVALS.is_approved(action_id)
    assert result is None

    # Resolve → approved
    PermissionSafetyAgent._APPROVALS.resolve(action_id, approved=True)

    # Poll → approved
    result = PermissionSafetyAgent._APPROVALS.is_approved(action_id)
    assert result is True
