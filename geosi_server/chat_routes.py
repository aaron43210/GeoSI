# -*- coding: utf-8 -*-
"""
GeoSI v2 — Chat & Execute Routes (Phase P1 gap)
════════════════════════════════════════════════════════════════════
Primary user-facing endpoints (PRD §5.4, §11):

  POST /chat    — natural-language query routed through SupervisorAgent
  POST /execute — direct plan execution from a pre-built ExecutionPlan

Both surfaces route through SupervisorAgent → Planning → Validation →
Permission & Safety → GIS Agent. No bypass path exists.

Also adds the HITL approval endpoints that the MCP tool needs in Phase 4
but that REST clients need immediately:

  POST /approval/{action_id}/approve
  POST /approval/{action_id}/reject
  GET  /approval/{action_id}
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from geosi_server.auth import api_key_auth, admin_auth

logger = logging.getLogger("geosi_server.chat")
router = APIRouter()


# ── Request / Response models ─────────────────────────────────────────

class ChatRequest(BaseModel):
    """Natural-language query sent to the Supervisor Agent."""

    query: str = Field(..., min_length=1, max_length=4096, description="Natural language GIS query")
    session_id: Optional[str] = Field(None, description="Session identifier (defaults to API key)")
    available_layers: List[str] = Field(default_factory=list, description="Layers currently loaded in QGIS")
    surface: str = Field("rest", description="Client surface: rest | qgis | mcp | web")
    context: Dict[str, Any] = Field(default_factory=dict, description="Optional extra context for the Supervisor")


class ChatResponse(BaseModel):
    """Supervisor Agent response."""

    success: bool
    query: str
    session_id: str
    answer: Optional[str] = None
    plan: Optional[Dict[str, Any]] = None
    results: Optional[List[str]] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    approval_pending: Optional[str] = None  # action_id when HITL is required


class ExecuteRequest(BaseModel):
    """Direct plan execution — for clients that pre-build an ExecutionPlan."""

    plan: Dict[str, Any] = Field(..., description="Serialised ExecutionPlan dict")
    session_id: Optional[str] = Field(None)
    surface: str = Field("rest")


class ExecuteResponse(BaseModel):
    success: bool
    session_id: str
    results: Optional[List[str]] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    approval_pending: Optional[str] = None


class ApprovalRequest(BaseModel):
    """Approve or reject a pending HITL action."""
    reason: Optional[str] = Field(None, description="Optional human comment")


class ApprovalStatus(BaseModel):
    action_id: str
    status: str            # "pending" | "approved" | "rejected"
    resolved: bool


# ── Endpoints ─────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(req: ChatRequest, api_key: str = Depends(api_key_auth)):
    """
    Primary user-facing endpoint (PRD §5.4, §11).

    Routes natural-language queries through:
        SupervisorAgent → PlanningAgent → ValidationAgent →
        PermissionSafetyAgent → GISAgent

    Returns the plan and execution results, or an ``approval_pending``
    action_id if a mutating step requires HITL confirmation.
    """
    from geosi_server.app import get_pool
    from geosi_engine.agents.supervisor import SupervisorAgent, SupervisorRequest
    from geosi_engine.agents.gis_agent import ApprovalPendingError

    pool = get_pool()
    session_id = req.session_id or api_key

    supervisor = SupervisorAgent(pool)
    sup_request = SupervisorRequest(
        query=req.query,
        session_id=session_id,
        available_layers=req.available_layers,
        context=req.context,
        surface=req.surface,
    )

    response = supervisor.handle(sup_request)

    # The Supervisor surfaces HITL directly on the response (D3/D4). An
    # ``approval_pending`` action_id means the pipeline halted cleanly on a
    # mutating step awaiting human confirmation — not a failure.
    approval_action_id: Optional[str] = response.approval_pending

    # Map the structured execution summary into a flat list for clients.
    results: Optional[List[str]] = None
    summary = response.execution_summary or {}
    steps = summary.get("steps") if isinstance(summary, dict) else None
    if steps:
        results = []
        for s in steps:
            label = s.get("tool_name", "?")
            if s.get("approval_pending"):
                results.append(f"{label}: ⏸ awaiting approval ({s['approval_pending']})")
            elif s.get("denied"):
                results.append(f"{label}: ⛔ denied — {s.get('error', 'policy')}")
            elif s.get("success"):
                vp = s.get("verification_passed")
                suffix = "" if vp is None else (" ✓verified" if vp else " ⚠verification-failed")
                results.append(f"{label}: ok{suffix}")
            else:
                results.append(f"{label}: failed — {s.get('error', 'unknown error')}")

    return ChatResponse(
        success=response.success,
        query=req.query,
        session_id=session_id,
        answer=str(response.result) if response.result else None,
        plan=response.plan_json,
        results=results,
        error=response.error,
        latency_ms=response.latency_ms,
        approval_pending=approval_action_id,
    )


@router.post("/execute", response_model=ExecuteResponse, tags=["Chat"])
async def execute(req: ExecuteRequest, api_key: str = Depends(api_key_auth)):
    """
    Direct plan execution endpoint (PRD §5.4).

    Clients that pre-build an ``ExecutionPlan`` (e.g. the QGIS plugin after
    local planning) can submit it here and route it straight to validation +
    permission + execution — skipping the LLM planning step.
    """
    from geosi_server.app import get_pool
    from geosi_engine.agents.validation import ValidationAgent
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent
    from geosi_engine.agents.gis_agent import GISAgent, ApprovalPendingError, PermissionDeniedError
    from geosi_engine.models import ExecutionPlan, ToolStep
    import time

    pool = get_pool()
    session_id = req.session_id or api_key
    engine = pool.get_or_create(session_id)

    start = time.monotonic()

    try:
        # Reconstruct plan from dict
        plan_data = req.plan
        steps = [ToolStep(**s) for s in plan_data.get("steps", [])]
        plan = ExecutionPlan(
            plan_id=plan_data.get("plan_id", ""),
            steps=steps,
            reasoning=plan_data.get("reasoning", ""),
            guardrail_flags=plan_data.get("guardrail_flags", []),
            plan_source=plan_data.get("plan_source", "client"),
        )

        # Validate
        validation = ValidationAgent(engine)
        report = validation.validate(plan, engine.state)
        if not report.ok:
            errors = [i.message for i in report.errors()]
            raise ValueError(f"Plan validation failed: {'; '.join(errors)}")

        # Execute steps
        permission = PermissionSafetyAgent(engine)
        gis = GISAgent(engine, permission_agent=permission)

        results = []
        for step in plan.steps:
            result = gis.execute_step(step, engine.state, block_on_approval=False)
            results.append(f"{step.tool_name}: {'ok' if result.success else result.error}")

        latency_ms = (time.monotonic() - start) * 1000
        return ExecuteResponse(
            success=True,
            session_id=session_id,
            results=results,
            latency_ms=latency_ms,
        )

    except ApprovalPendingError as exc:
        latency_ms = (time.monotonic() - start) * 1000
        return ExecuteResponse(
            success=False,
            session_id=session_id,
            error=str(exc),
            approval_pending=exc.action_id,
            latency_ms=latency_ms,
        )
    except (ValueError, PermissionDeniedError) as exc:
        latency_ms = (time.monotonic() - start) * 1000
        return ExecuteResponse(
            success=False,
            session_id=session_id,
            error=str(exc),
            latency_ms=latency_ms,
        )


# ── HITL Approval endpoints ───────────────────────────────────────────

@router.post(
    "/approval/{action_id}/approve",
    response_model=ApprovalStatus,
    tags=["HITL"],
)
async def approve_action(
    action_id: str,
    req: ApprovalRequest = ApprovalRequest(),
    api_key: str = Depends(api_key_auth),
):
    """
    Approve a pending HITL action (FR-5.1: ``approve_pending_action``).

    Also called by the ``approve_pending_action`` MCP tool in Phase 4.
    """
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent

    # PermissionSafetyAgent._APPROVALS is a class-level registry
    resolved = PermissionSafetyAgent._APPROVALS.resolve(action_id, approved=True)
    if not resolved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No pending approval found for action_id={action_id!r}",
        )
    return ApprovalStatus(action_id=action_id, status="approved", resolved=True)


@router.post(
    "/approval/{action_id}/reject",
    response_model=ApprovalStatus,
    tags=["HITL"],
)
async def reject_action(
    action_id: str,
    req: ApprovalRequest = ApprovalRequest(),
    api_key: str = Depends(api_key_auth),
):
    """Reject a pending HITL action."""
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent

    resolved = PermissionSafetyAgent._APPROVALS.resolve(action_id, approved=False)
    if not resolved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No pending approval found for action_id={action_id!r}",
        )
    return ApprovalStatus(action_id=action_id, status="rejected", resolved=True)


@router.get(
    "/approval/{action_id}",
    response_model=ApprovalStatus,
    tags=["HITL"],
)
async def poll_approval(action_id: str, api_key: str = Depends(api_key_auth)):
    """Poll the status of a pending HITL action."""
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent

    pending = PermissionSafetyAgent._APPROVALS.get(action_id)
    if pending is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No approval record for action_id={action_id!r}",
        )
    if not pending.resolved:
        return ApprovalStatus(action_id=action_id, status="pending", resolved=False)
    return ApprovalStatus(
        action_id=action_id,
        status="approved" if pending.approved else "rejected",
        resolved=True,
    )
