# -*- coding: utf-8 -*-
"""
GeoSI v2 — Phase 1 Core Agent & Memory Tests
"""
from __future__ import annotations

import time
import pytest
from unittest.mock import MagicMock, patch

from geosi_engine.session_pool import SessionPool
from geosi_engine.agents.supervisor import SupervisorAgent, CircuitBreaker, CBState
from geosi_engine.agents.planning import _compute_risk_level
from geosi_engine.agents.validation import get_allow_list, safe_evaluator
from geosi_engine.agents.permission_safety import PermissionSafetyAgent
from geosi_engine.agents.gis_agent import GISAgent, PermissionDeniedError, ApprovalPendingError
from geosi_engine.models import ToolStep, ExecutionPlan


def test_session_pool_isolation():
    """Verify LRU cache returns same instance for same ID, different for others."""
    pool = SessionPool(max_size=2)
    s1 = pool.get_or_create("session_1")
    s2 = pool.get_or_create("session_2")
    assert s1 is not s2
    assert pool.get_or_create("session_1") is s1


def test_circuit_breaker():
    """Verify circuit breaker opens after N failures and half-opens after reset time."""
    cb = CircuitBreaker("test", failure_threshold=2, reset_seconds=0.1)
    
    assert cb.is_available()
    cb.record_failure()
    assert cb.is_available()
    cb.record_failure()
    
    # Threshold reached -> OPEN
    assert not cb.is_available()
    assert cb.state == CBState.OPEN
    
    # Wait for reset
    time.sleep(0.15)
    assert cb.is_available()
    assert cb.state == CBState.HALF_OPEN
    
    # Success resets to CLOSED
    cb.record_success()
    assert cb.state == CBState.CLOSED
    assert cb.is_available()


def test_risk_level_computation():
    """Risk = what the tool does to existing data (agents.planning docstring)."""
    from geosi_engine.models import ToolSpec

    # QGIS algorithms write new outputs: read-only for existing data
    buffer_spec = ToolSpec(name="native_buffer", qgis_algorithm="native:buffer")
    assert _compute_risk_level("native_buffer", {}) == "read_only"
    from geosi_engine.agents.planning import compute_risk_level
    assert compute_risk_level("native_buffer", {"DISTANCE": 500}, buffer_spec) == "read_only"
    # ...even one whose name says "delete": it writes a new layer without the column
    assert compute_risk_level("native_deletecolumn", {}, ToolSpec(
        name="native_deletecolumn", qgis_algorithm="native:deletecolumn")) == "read_only"

    # The bridge's classification of the algorithm is used
    assert compute_risk_level("native_truncatetable", {}, ToolSpec(
        name="native_truncatetable", qgis_algorithm="native:truncatetable",
        risk_level="destructive")) == "destructive"

    # Non-QGIS tools: destructive name fragments
    assert _compute_risk_level("drop_table", {}) == "destructive"
    assert _compute_risk_level("delete_field", {}) == "destructive"

    # Parameters raise the level
    assert _compute_risk_level("export_to_csv", {"OVERWRITE": True}) == "destructive"
    assert _compute_risk_level("native_buffer", {"OUTPUT": "/Users/me/data/out.gpkg"}) == "mutating"
    assert _compute_risk_level("native_buffer", {"OUTPUT": "TEMPORARY_OUTPUT"}) == "read_only"

    # Domain tools declare their own risk
    assert _compute_risk_level("machine_learning", {}) == "mutating"
    assert _compute_risk_level("generate_code", {}) == "read_only"

    # Read-only default
    assert _compute_risk_level("count_points", {}) == "read_only"

def test_table_allow_list():
    """Verify G4 SQL injection prevention."""
    allow_list = get_allow_list()
    
    # Valid pre-registered table
    assert allow_list.validate_and_quote("geosi_layers") == '"geosi_layers"'
    
    # Invalid characters
    with pytest.raises(ValueError, match="invalid characters"):
        allow_list.validate_and_quote("table; DROP TABLE users;")
        
    # Valid chars but not registered
    with pytest.raises(ValueError, match="not in the known-table allow-list"):
        allow_list.validate_and_quote("unregistered_table_123")
        
    # Register and succeed
    allow_list.register("unregistered_table_123")
    assert allow_list.validate_and_quote("unregistered_table_123") == '"unregistered_table_123"'


def test_safe_expression_evaluator():
    """Verify G12 field calculator AST checks."""
    # Safe expressions
    safe_evaluator.validate("area * 2.5")
    safe_evaluator.validate("pop_2020 - pop_2010 > 1000")
    
    # Unsafe expressions
    with pytest.raises(ValueError, match="Disallowed expression node type: 'Call'"):
        safe_evaluator.validate("__import__('os').system('echo pwned')")
        
    with pytest.raises(ValueError, match="Disallowed expression node type: 'Attribute'"):
        safe_evaluator.validate("df.__class__.__bases__")


def test_permission_safety_policies():
    """Verify allow/ask/deny logic."""
    engine = MagicMock()
    # Ensure it has a session ID
    engine.get_session = MagicMock(return_value="test")
    agent = PermissionSafetyAgent(engine=engine)
    
    # Policy override (mocked properly for no-override)
    with patch.object(agent, "_load_policy_override", return_value=None):
        # Default policies based on risk
        assert agent.check_permission("some_tool", "read_only").decision == "allow"
        assert agent.check_permission("some_tool", "mutating").decision == "ask"
        assert agent.check_permission("some_tool", "destructive").decision == "ask"
    
    # Policy override returning deny
    with patch.object(agent, "_load_policy_override", return_value="deny"):
        assert agent.check_permission("native:buffer", "read_only").decision == "deny"


def test_gis_agent_permission_enforcement():
    """Verify FR-2 / G5 hardcoded permission gate."""
    engine = MagicMock()
    permission = PermissionSafetyAgent(engine)
    gis = GISAgent(engine, permission)
    
    # Mock the execute method of the internal executor so we can verify if it gets called
    engine.executor.execute_step = MagicMock(return_value=MagicMock(success=True))
    
    with patch.object(permission, "_load_policy_override", return_value=None):
        # Read-only step bypasses permission latency (writes audit only)
        step_ro = ToolStep(tool_name="count", risk_level="read_only")
        gis.execute_step(step_ro, state=None)
        engine.executor.execute_step.assert_called_once()
        engine.executor.execute_step.reset_mock()
        
        # Mutating step -> triggers ask -> raises ApprovalPendingError
        step_mut = ToolStep(tool_name="buffer", risk_level="mutating")
        with pytest.raises(ApprovalPendingError) as exc_info:
            gis.execute_step(step_mut, state=None, block_on_approval=False)
        
        assert exc_info.value.action_id is not None
        engine.executor.execute_step.assert_not_called()
    
    # Denied step -> raises PermissionDeniedError
    step_deny = ToolStep(tool_name="delete", risk_level="destructive")
    with patch.object(permission, "check_permission", return_value=MagicMock(decision="deny")):
        with pytest.raises(PermissionDeniedError):
            gis.execute_step(step_deny, state=None, block_on_approval=False)
        engine.executor.execute_step.assert_not_called()
