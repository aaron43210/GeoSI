# -*- coding: utf-8 -*-
"""
GeoSI v2 — Chat & HITL Routes
════════════════════════════════════════════════════════════════════
Primary user-facing endpoints (PRD §5.4, §11):

  POST /chat    — natural-language query through SupervisorAgent
  POST /execute — direct plan execution from a pre-built ExecutionPlan

HITL approval endpoints:

  POST /approval/{action_id}/approve  — approve a pending step → returns resumed result
  POST /approval/{action_id}/reject   — reject  a pending step → returns rejected result
  GET  /approval/{action_id}          — poll the status of a pending approval

Key design:
  • ``/chat`` runs ``supervisor.handle()`` in a threadpool executor so the
    async event loop is never blocked by QGIS / LLM calls.
  • ``/approval/{id}/approve`` calls ``supervisor.resume(action_id, approved=True)``
    and returns the *resumed execution result* — not just a status flag.
    The browser never needs to re-send the original query.
  • A single process-wide SupervisorAgent is used so approval-pending runs
    survive between the original ``/chat`` call and the later ``/approval``
    call (the PausedRun lives in the engine's AgentLoop, which the pool holds).
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from geosi_server.auth import api_key_auth

logger = logging.getLogger("geosi_server.chat")
router = APIRouter()


# ── Request / Response models ─────────────────────────────────────────

class ChatRequest(BaseModel):
    """Natural-language query sent to the Supervisor Agent."""
    query: str = Field(..., min_length=1, max_length=4096)
    session_id: Optional[str] = Field(None)
    available_layers: List[str] = Field(default_factory=list)
    surface: str = Field("rest")
    context: Dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    """Supervisor Agent response."""
    success: bool
    query: str
    session_id: str
    answer: Optional[str] = None
    plan: Optional[Dict[str, Any]] = None
    results: Optional[List[str]] = None
    report: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    plan_source: Optional[str] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    approval_pending: Optional[str] = None  # action_id when HITL is needed


class ExecuteRequest(BaseModel):
    """Direct plan execution — for clients that pre-build an ExecutionPlan."""
    plan: Dict[str, Any] = Field(...)
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
    reason: Optional[str] = Field(None)


class ApprovalResponse(BaseModel):
    """Response from an approval/reject call — carries the resumed result."""
    action_id: str
    approved: bool
    resolved: bool
    # Resumed execution fields (mirrors ChatResponse fields)
    success: bool = False
    answer: Optional[str] = None
    plan: Optional[Dict[str, Any]] = None
    results: Optional[List[str]] = None
    report: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    error: Optional[str] = None
    latency_ms: float = 0.0


class ApprovalStatus(BaseModel):
    action_id: str
    status: str     # "pending" | "approved" | "rejected"
    resolved: bool


# ── Helpers ───────────────────────────────────────────────────────────

def _supervisor_response_to_chat(resp, query: str, session_id: str) -> ChatResponse:
    """Convert a SupervisorResponse into a ChatResponse."""
    summary = resp.execution_summary or {}
    steps = summary.get("steps") if isinstance(summary, dict) else None
    results: Optional[List[str]] = None
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

    exec_result = getattr(resp, "execution_result", None)
    warnings = list(getattr(exec_result, "warnings", []) or [])
    report = getattr(exec_result, "report", None) or getattr(resp, "report", None)
    plan_source = getattr(exec_result, "plan_source", None) or getattr(resp, "plan_source", None)

    return ChatResponse(
        success=resp.success,
        query=query,
        session_id=session_id,
        answer=str(resp.result) if resp.result else None,
        plan=resp.plan_json,
        results=results,
        report=report,
        warnings=warnings,
        plan_source=plan_source,
        error=resp.error,
        latency_ms=resp.latency_ms,
        approval_pending=resp.approval_pending,
    )


def _supervisor_response_to_approval(resp, action_id: str, approved: bool) -> ApprovalResponse:
    """Convert a SupervisorResponse into an ApprovalResponse."""
    summary = resp.execution_summary or {}
    steps = summary.get("steps") if isinstance(summary, dict) else None
    results: Optional[List[str]] = None
    if steps:
        results = [
            f"{s.get('tool_name', '?')}: {'ok' if s.get('success') else s.get('error', '?')}"
            for s in steps
        ]
    exec_result = getattr(resp, "execution_result", None)
    return ApprovalResponse(
        action_id=action_id,
        approved=approved,
        resolved=True,
        success=resp.success,
        answer=str(resp.result) if resp.result else None,
        plan=resp.plan_json,
        results=results,
        report=getattr(exec_result, "report", None) or getattr(resp, "report", None),
        warnings=list(getattr(exec_result, "warnings", []) or []),
        error=resp.error,
        latency_ms=resp.latency_ms,
    )


# ── Endpoints ─────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(req: ChatRequest, api_key: str = Depends(api_key_auth)):
    """
    Primary user-facing endpoint (PRD §5.4, §11).

    Routes natural-language queries through:
        SupervisorAgent → PlanningAgent → ValidationAgent →
        PermissionSafetyAgent → GISAgent

    Runs the pipeline in a thread-pool executor so the async event loop
    is never blocked by QGIS Processing or LLM calls.

    Returns ``approval_pending`` when a mutating step needs confirmation.
    Call ``POST /approval/{action_id}/approve`` to resume.
    """
    from geosi_server.app import get_supervisor
    from geosi_engine.agents.supervisor import SupervisorRequest

    session_id = req.session_id or api_key
    supervisor = get_supervisor()
    sup_request = SupervisorRequest(
        query=req.query,
        session_id=session_id,
        available_layers=req.available_layers,
        context=req.context,
        surface=req.surface,
    )

    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(None, supervisor.handle, sup_request)
    return _supervisor_response_to_chat(resp, req.query, session_id)


@router.post("/execute", response_model=ExecuteResponse, tags=["Chat"])
async def execute(req: ExecuteRequest, api_key: str = Depends(api_key_auth)):
    """
    Direct plan execution — for clients that pre-build an ExecutionPlan.

    Skips the LLM planning step and routes straight to validation +
    permission + execution.
    """
    from geosi_server.app import get_pool
    from geosi_engine.agents.validation import ValidationAgent
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent
    from geosi_engine.agents.gis_agent import GISAgent
    from geosi_engine.models import ExecutionPlan, ToolStep
    import time

    pool = get_pool()
    session_id = req.session_id or api_key
    engine = pool.get_or_create(session_id)
    start = time.monotonic()

    try:
        plan_data = req.plan
        steps = [ToolStep(**s) for s in plan_data.get("steps", [])]
        plan = ExecutionPlan(
            plan_id=plan_data.get("plan_id", ""),
            steps=steps,
            reasoning=plan_data.get("reasoning", ""),
            guardrail_flags=plan_data.get("guardrail_flags", []),
            plan_source=plan_data.get("plan_source", "client"),
        )

        validation = ValidationAgent(engine)
        report = validation.validate(plan, engine.state)
        if not report.ok:
            errors = [i.message for i in report.errors()]
            raise ValueError(f"Plan validation failed: {'; '.join(errors)}")

        permission = PermissionSafetyAgent(engine)
        gis = GISAgent(engine, permission_agent=permission)
        loop = asyncio.get_event_loop()

        results = []
        for step in plan.steps:
            result = await loop.run_in_executor(
                None, gis.execute_step, step, engine.state
            )
            results.append(f"{step.tool_name}: {'ok' if result.success else result.error}")

        latency_ms = (time.monotonic() - start) * 1000
        return ExecuteResponse(success=True, session_id=session_id,
                               results=results, latency_ms=latency_ms)

    except ValueError as exc:
        latency_ms = (time.monotonic() - start) * 1000
        return ExecuteResponse(success=False, session_id=session_id,
                               error=str(exc), latency_ms=latency_ms)
    except Exception as exc:
        logger.error("Execute failed for session %s: %s", session_id, exc, exc_info=True)
        latency_ms = (time.monotonic() - start) * 1000
        return ExecuteResponse(success=False, session_id=session_id,
                               error=str(exc), latency_ms=latency_ms)


# ── HITL Approval endpoints ───────────────────────────────────────────

@router.post(
    "/approval/{action_id}/approve",
    response_model=ApprovalResponse,
    tags=["HITL"],
)
async def approve_action(
    action_id: str,
    req: ApprovalRequest = ApprovalRequest(),
    api_key: str = Depends(api_key_auth),
):
    """
    Approve a pending HITL action and return the *resumed execution result*.

    The pipeline continues from where it paused — you get back the same
    ChatResponse-style answer you would have received if the step had been
    allowed automatically.  The browser never needs to re-send the original
    query.
    """
    from geosi_server.app import get_supervisor
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent

    pending = PermissionSafetyAgent._APPROVALS.get(action_id)
    if pending is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No pending approval found for action_id={action_id!r}",
        )

    supervisor = get_supervisor()
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(
        None, supervisor.resume, action_id, True, pending.session_id
    )
    return _supervisor_response_to_approval(resp, action_id, approved=True)


@router.post(
    "/approval/{action_id}/reject",
    response_model=ApprovalResponse,
    tags=["HITL"],
)
async def reject_action(
    action_id: str,
    req: ApprovalRequest = ApprovalRequest(),
    api_key: str = Depends(api_key_auth),
):
    """Reject a pending HITL action."""
    from geosi_server.app import get_supervisor
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent

    pending = PermissionSafetyAgent._APPROVALS.get(action_id)
    if pending is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No pending approval found for action_id={action_id!r}",
        )

    supervisor = get_supervisor()
    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(
        None, supervisor.resume, action_id, False, pending.session_id
    )
    return _supervisor_response_to_approval(resp, action_id, approved=False)


@router.get(
    "/approval/{action_id}",
    response_model=ApprovalStatus,
    tags=["HITL"],
)
async def poll_approval(action_id: str, api_key: str = Depends(api_key_auth)):
    """Poll whether a HITL action is still pending."""
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
