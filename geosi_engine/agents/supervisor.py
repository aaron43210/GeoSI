# -*- coding: utf-8 -*-
"""
GeoSI v2 — Supervisor Agent
════════════════════════════════════════════════════════════════════
The single entry-point for ALL four client surfaces:
  • QGIS plugin dock
  • Web UI
  • REST API (geosi_server/)
  • MCP server (geosi_mcp/)

NO surface may call a domain agent (Planning, GIS, RS, ML, Geology)
directly — everything routes through ``SupervisorAgent.handle()``.

Key responsibilities (PRD §4, FR-6)
────────────────────────────────────
1. Session management — delegates to ``SessionPool``.
2. LLM cascade with per-request timeout budget (Ollama → Gemini →
   Claude → rule-based fallback).
3. Per-provider circuit breaker: after N consecutive failures within
   a time window, the provider is skipped for the rest of the session.
4. Routes requests to the correct downstream agent sequence:
   Planning → Validation → Permission & Safety → GIS / RS / ML / Geology.
5. Orchestrates the audit log and OTel spans across the full pipeline.
"""
from __future__ import annotations

import logging
import os
import time
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from geosi_engine.telemetry import start_span, set_span_attr

logger = logging.getLogger("geosi_engine.agents.supervisor")

# ---------------------------------------------------------------------------
# Configuration (overridable via env vars)
# ---------------------------------------------------------------------------
_TOTAL_BUDGET_S = float(os.environ.get("LLM_TOTAL_BUDGET_SECONDS", "30"))
_PROVIDER_TIMEOUT_S = float(os.environ.get("LLM_PROVIDER_TIMEOUT_SECONDS", "10"))
_CB_FAILURE_THRESHOLD = int(os.environ.get("CIRCUIT_BREAKER_FAILURE_THRESHOLD", "3"))
_CB_RESET_S = float(os.environ.get("CIRCUIT_BREAKER_RESET_SECONDS", "120"))


# ---------------------------------------------------------------------------
# Circuit Breaker
# ---------------------------------------------------------------------------

class CBState(str, Enum):
    CLOSED = "closed"       # normal operation
    OPEN = "open"           # failing — skip this provider
    HALF_OPEN = "half_open" # probe: allow one trial call


@dataclass
class CircuitBreaker:
    """
    Per-provider circuit breaker.

    State machine:
        CLOSED  → (N consecutive failures in window) → OPEN
        OPEN    → (reset_seconds elapsed)            → HALF_OPEN
        HALF_OPEN → (success)                        → CLOSED
        HALF_OPEN → (failure)                        → OPEN (reset timer)
    """

    provider: str
    failure_threshold: int = _CB_FAILURE_THRESHOLD
    reset_seconds: float = _CB_RESET_S
    state: CBState = CBState.CLOSED
    _failures: int = field(default=0, repr=False)
    _window_start: float = field(default_factory=time.monotonic, repr=False)
    _opened_at: float = field(default=0.0, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record_success(self) -> None:
        with self._lock:
            self._failures = 0
            self.state = CBState.CLOSED

    def record_failure(self) -> None:
        with self._lock:
            now = time.monotonic()
            # Reset failure window if > reset_seconds has passed since last failure
            if now - self._window_start > self.reset_seconds:
                self._failures = 0
                self._window_start = now
            self._failures += 1
            if self._failures >= self.failure_threshold:
                self.state = CBState.OPEN
                self._opened_at = now
                logger.warning(
                    "Circuit breaker OPEN for provider '%s' after %d failures",
                    self.provider,
                    self._failures,
                )

    def is_available(self) -> bool:
        """Return True if this provider should be attempted."""
        with self._lock:
            if self.state == CBState.CLOSED:
                return True
            if self.state == CBState.OPEN:
                if time.monotonic() - self._opened_at >= self.reset_seconds:
                    self.state = CBState.HALF_OPEN
                    logger.info(
                        "Circuit breaker HALF_OPEN for provider '%s' — probing",
                        self.provider,
                    )
                    return True
                return False
            # HALF_OPEN: allow one trial
            return True

    def status(self) -> dict[str, Any]:
        with self._lock:
            return {
                "provider": self.provider,
                "state": self.state.value,
                "failures": self._failures,
                "threshold": self.failure_threshold,
            }


# ---------------------------------------------------------------------------
# Request / Response types
# ---------------------------------------------------------------------------

@dataclass
class SupervisorRequest:
    query: str
    session_id: str
    available_layers: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    surface: str = "rest"  # "rest" | "qgis" | "mcp" | "web"


@dataclass
class SupervisorResponse:
    success: bool
    result: Any = None
    error: Optional[str] = None
    plan_json: Optional[dict[str, Any]] = None
    execution_summary: Optional[dict[str, Any]] = None
    approval_pending: Optional[str] = None
    session_id: str = ""
    latency_ms: float = 0.0


# ---------------------------------------------------------------------------
# Supervisor Agent
# ---------------------------------------------------------------------------

class SupervisorAgent:
    """
    Single entry-point for all GeoSI client surfaces.

    Parameters
    ----------
    pool:
        ``SessionPool`` instance managed by the server/plugin layer.
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool
        self._circuit_breakers: dict[str, CircuitBreaker] = {
            "ollama": CircuitBreaker(provider="ollama"),
            "gemini": CircuitBreaker(provider="gemini"),
            "claude": CircuitBreaker(provider="claude"),
        }

    # ------------------------------------------------------------------
    # Public handle() — the ONLY authorised entry point
    # ------------------------------------------------------------------

    def handle(self, request: SupervisorRequest) -> SupervisorResponse:
        """
        Process a user request end-to-end.

        Pipeline (Phase 1):
            1. Retrieve/create session-scoped engine.
            2. Invoke Planning Agent with LLM cascade + budget.
            3. Invoke Validation Agent.
            4. Invoke Permission & Safety Agent.
            5. Dispatch to GIS Agent (other domain agents in later phases).
            6. Return result.

        All downstream agent calls are guarded by the total budget.
        Every hand-off is wrapped in an OTel span (FR-7.3).
        """
        start = time.monotonic()

        with start_span(
            "supervisor.handle",
            **{"session.id": request.session_id, "surface": request.surface}
        ) as root_span:
            try:
                root_span.set_attribute("query.length", len(request.query))
                engine = self._pool.get_or_create(request.session_id)
                pipe = self._run_pipeline(request, engine)
                latency = (time.monotonic() - start) * 1000
                root_span.set_attribute("latency_ms", latency)
                return SupervisorResponse(
                    success=True,
                    result=pipe.get("answer"),
                    plan_json=pipe.get("plan_json"),
                    execution_summary=pipe.get("execution_summary"),
                    approval_pending=pipe.get("approval_pending"),
                    session_id=request.session_id,
                    latency_ms=latency,
                )
            except Exception as exc:
                latency = (time.monotonic() - start) * 1000
                logger.error(
                    "Supervisor pipeline failed for session %s: %s",
                    request.session_id,
                    exc,
                    exc_info=True,
                )
                return SupervisorResponse(
                    success=False,
                    error=str(exc),
                    session_id=request.session_id,
                    latency_ms=latency,
                )

    def circuit_breaker_states(self) -> list[dict[str, Any]]:
        """Return all circuit breaker statuses for the /health endpoint."""
        return [cb.status() for cb in self._circuit_breakers.values()]

    # ------------------------------------------------------------------
    # LLM cascade with budget + circuit breaker
    # ------------------------------------------------------------------

    def run_with_budget(
        self,
        providers: list[str],
        fn: Callable[[str], Any],
        budget_seconds: float = _TOTAL_BUDGET_S,
        per_provider_timeout: float = _PROVIDER_TIMEOUT_S,
    ) -> Any:
        """
        Try each LLM provider in order, respecting the total budget.

        Parameters
        ----------
        providers:
            Ordered list of provider names to try.
        fn:
            Callable that accepts a provider name and returns a result.
            May raise any exception on failure.
        budget_seconds:
            Total wall-clock time across all provider attempts.
        per_provider_timeout:
            Time limit per individual provider attempt.

        Returns
        -------
        Any
            Result from the first successful provider call.

        Raises
        ------
        RuntimeError
            If all providers fail or the budget is exhausted.
        """
        deadline = time.monotonic() + budget_seconds
        last_error: Optional[Exception] = None

        for provider in providers:
            cb = self._circuit_breakers.get(provider)
            if cb and not cb.is_available():
                logger.debug("Skipping provider '%s' — circuit breaker OPEN", provider)
                continue

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError(
                    f"LLM budget exhausted after trying providers: {providers}"
                )

            effective_timeout = min(per_provider_timeout, remaining)

            import concurrent.futures

            # NOTE: deliberately NOT using `with ThreadPoolExecutor(...)` here.
            # The context-manager exit calls shutdown(wait=True), which blocks
            # until the submitted call returns — so a hung provider would stall
            # the whole cascade for its full generation time, defeating both the
            # per-provider timeout and the total budget. Instead we shut the
            # executor down with wait=False so a timed-out provider is abandoned
            # and we move on to the next one immediately.
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            future = executor.submit(fn, provider)
            try:
                result = future.result(timeout=effective_timeout)
                if cb:
                    cb.record_success()
                return result
            except concurrent.futures.TimeoutError:
                future.cancel()
                logger.warning(
                    "Provider '%s' timed out after %.1fs", provider, effective_timeout
                )
                if cb:
                    cb.record_failure()
                last_error = TimeoutError(f"{provider} timed out")
            except Exception as exc:
                logger.warning("Provider '%s' failed: %s", provider, exc)
                if cb:
                    cb.record_failure()
                last_error = exc
            finally:
                # Release the worker without blocking on an in-flight call.
                executor.shutdown(wait=False, cancel_futures=True)

        raise RuntimeError(
            f"All providers failed. Last error: {last_error}"
        ) from last_error

    # ------------------------------------------------------------------
    # Internal pipeline
    # ------------------------------------------------------------------

    def _run_pipeline(self, request: SupervisorRequest, engine: Any) -> dict[str, Any]:
        """
        Coordinate the full agent pipeline (PRD §4, FR-6).

        Single plan→reflect→validate→permission→execute→verify→report loop —
        the Golden Rule: there is no second routing brain. Domain agents
        (RS / ML / Geology / CodeGen / Report / Research) are reached as
        registered tools dispatched by the GIS Agent, so they flow through
        exactly this pipeline like any other tool.

        Each agent hand-off is wrapped in its own OTel span (FR-7.3).

        Returns a dict with keys ``answer``, ``plan_json``,
        ``execution_summary``, ``approval_pending``.
        """
        import dataclasses

        from geosi_engine.agents.planning import PlanningAgent
        from geosi_engine.agents.validation import ValidationAgent
        from geosi_engine.agents.permission_safety import PermissionSafetyAgent
        from geosi_engine.agents.gis_agent import (
            GISAgent,
            ApprovalPendingError,
            PermissionDeniedError,
        )
        from geosi_engine.agents.reflection import ReflectionAgent
        from geosi_engine.agents.verification import VerificationAgent
        from geosi_engine.agents.workflow_optimization import WorkflowOptimizationAgent
        from geosi_engine.models import ExecutionPlan, ExecutionResult, ToolResult

        planning = PlanningAgent(engine, supervisor=self)
        validation = ValidationAgent(engine)
        permission = PermissionSafetyAgent(engine)
        gis = GISAgent(engine, permission_agent=permission)
        reflection = ReflectionAgent(engine)
        verification = VerificationAgent(engine)
        workflow_opt = WorkflowOptimizationAgent(engine)

        # Expose this Supervisor on the engine so agents that need the LLM
        # cascade for re-planning (e.g. ReflectionAgent._generate_corrected_plan)
        # can reach it instead of constructing a PlanningAgent with supervisor=None.
        try:
            engine.supervisor = self  # type: ignore[attr-defined]
        except Exception:
            pass

        # ── Step 1: plan ───────────────────────────────────────────────
        with start_span("planning.plan", **{"agent.name": "planning", "session.id": request.session_id}):
            plan = planning.plan(
                query=request.query,
                available_layers=request.available_layers,
                session_id=request.session_id,
            )
            set_span_attr("plan.steps", len(plan.steps))
            set_span_attr("plan.source", plan.plan_source)

        plan_json = dataclasses.asdict(plan)

        # ── Step 2: reflection pre-check (non-blocking critic) ─────────
        with start_span("reflection.critic", **{"agent.name": "reflection"}):
            try:
                critic = reflection.critic(plan)
                set_span_attr("reflection.ok", critic.ok)
                if not critic.ok:
                    msgs = [f"{f.tool_name}: {f.message}" for f in critic.errors()]
                    logger.warning(
                        "Reflection critic flagged plan %s: %s", plan.plan_id, msgs
                    )
                for w in critic.warnings():
                    logger.info("Reflection warning [%s]: %s", w.tool_name, w.message)
            except Exception as exc:  # non-fatal — critic is advisory
                logger.debug("Reflection critic skipped: %s", exc)

        # ── Step 2b: workflow optimization (advisory, read-only) ───────
        # Agent #13 — surfaces redundant/reorderable steps and best
        # practices from execution history. Never mutates the plan.
        wfo_report: Optional[dict[str, Any]] = None
        with start_span("workflow_opt.analyze", **{"agent.name": "workflow_optimization"}):
            try:
                opt = workflow_opt.analyze(plan)
                wfo_report = {
                    "original_step_count": opt.original_step_count,
                    "optimized_step_count": opt.optimized_step_count,
                    "estimated_total_saving_s": opt.estimated_total_saving_s,
                    "suggestions": [
                        {
                            "type": s.type,
                            "step_index": s.step_index,
                            "message": s.message,
                            "estimated_time_saving_s": s.estimated_time_saving_s,
                            "confidence": s.confidence,
                        }
                        for s in opt.suggestions
                    ],
                    "best_practices": opt.best_practices,
                }
                set_span_attr("wfo.suggestions", len(opt.suggestions))
                for s in opt.suggestions:
                    logger.info("Workflow optimization [%s]: %s", s.type, s.message)
            except Exception as exc:  # non-fatal — optimization is advisory
                logger.debug("Workflow optimization skipped: %s", exc)

        # ── Step 3: validate ───────────────────────────────────────────
        with start_span("validation.validate", **{"agent.name": "validation"}):
            report = validation.validate(plan, engine.state)
            if not report.ok:
                errors = [i.message for i in report.errors()]
                raise ValueError(f"Plan validation failed: {'; '.join(errors)}")
            set_span_attr("validation.ok", True)

        # ── Step 4: guardrail check at pipeline boundary ───────────────
        with start_span("permission_safety.guardrail_check", **{"agent.name": "permission_safety"}):
            if plan.guardrail_flags:
                logger.warning(
                    "Plan carries guardrail flags from retrieval: %s",
                    plan.guardrail_flags,
                )
                set_span_attr("guardrail.flags", str(plan.guardrail_flags))

        # ── Step 5: execute each step through the GIS Agent ────────────
        # Permission gate fires here (mutating → HITL). The loop stops the
        # moment a step needs approval or is denied, returning partials.
        results: list[ToolResult] = []
        step_summaries: list[dict[str, Any]] = []
        approval_pending: Optional[str] = None
        denied_reason: Optional[str] = None
        all_ok = True

        for step in plan.steps:
            with start_span(
                "gis_agent.execute_step",
                **{
                    "agent.name": "gis_agent",
                    "tool.name": step.tool_name,
                    "tool.risk_level": step.risk_level,
                }
            ):
                try:
                    result = gis.execute_step(step, engine.state)
                except ApprovalPendingError as ap:
                    approval_pending = ap.action_id
                    all_ok = False
                    set_span_attr("step.approval_pending", ap.action_id)
                    step_summaries.append({
                        "step_id": step.step_id,
                        "tool_name": step.tool_name,
                        "risk_level": step.risk_level,
                        "success": False,
                        "approval_pending": ap.action_id,
                    })
                    logger.info(
                        "Pipeline halted — step '%s' awaits approval (action_id=%s)",
                        step.tool_name, ap.action_id,
                    )
                    break
                except PermissionDeniedError as pd:
                    denied_reason = str(pd)
                    all_ok = False
                    set_span_attr("step.denied", True)
                    step_summaries.append({
                        "step_id": step.step_id,
                        "tool_name": step.tool_name,
                        "risk_level": step.risk_level,
                        "success": False,
                        "denied": True,
                        "error": denied_reason,
                    })
                    logger.warning("Pipeline halted — step '%s' denied: %s", step.tool_name, denied_reason)
                    break

                # ── Generic step failure → one reflection self-correction ──
                if not result.success:
                    set_span_attr("step.success", False)
                    with start_span("reflection.reflect_and_retry", **{"agent.name": "reflection"}):
                        def _exec_one(p: ExecutionPlan) -> ToolResult:
                            last: Optional[ToolResult] = None
                            for s in p.steps:
                                r = gis.execute_step(s, engine.state)
                                if not r.success:
                                    raise RuntimeError(r.error or f"step {s.step_id} failed")
                                last = r
                            if last is None:
                                raise RuntimeError("corrected plan produced no steps")
                            return last
                        single = ExecutionPlan(
                            plan_id=f"{plan.plan_id}-retry-{step.step_id}",
                            steps=[step],
                            reasoning=f"Self-correction for failed step {step.step_id}",
                            plan_source=plan.plan_source,
                        )
                        try:
                            result = reflection.reflect_and_retry(
                                single, result.error or "step failed", _exec_one
                            )
                            set_span_attr("reflection.recovered", True)
                        except Exception as exc:
                            logger.info("Reflection retry exhausted for '%s': %s", step.tool_name, exc)

                set_span_attr("step.success", bool(result.success))
                results.append(result)
                if not result.success:
                    all_ok = False

                # ── Verification after mutating steps ───────────────────
                verification_passed: Optional[bool] = None
                if step.risk_level != "read_only" and result.success:
                    with start_span("verification.verify", **{"agent.name": "verification"}):
                        try:
                            vr = verification.verify_execution_result(result)
                            verification_passed = vr.passed
                            set_span_attr("verification.passed", vr.passed)
                            if not vr.passed:
                                logger.warning(
                                    "Verification failed for '%s': %s",
                                    step.tool_name, vr.issues,
                                )
                        except Exception as exc:
                            logger.debug("Verification skipped for '%s': %s", step.tool_name, exc)

                step_summaries.append({
                    "step_id": step.step_id,
                    "tool_name": step.tool_name,
                    "risk_level": step.risk_level,
                    "success": bool(result.success),
                    "verification_passed": verification_passed,
                    "error": result.error,
                    "message": result.message,
                })

        # ── Step 6: report generation → human-readable answer ──────────
        answer = self._generate_answer(
            engine, plan, results, all_ok, approval_pending, denied_reason, request.session_id
        )

        execution_summary = {
            "plan_id": plan.plan_id,
            "plan_source": plan.plan_source,
            "total_steps": len(plan.steps),
            "executed_steps": len(step_summaries),
            "all_success": all_ok and approval_pending is None and denied_reason is None,
            "approval_pending": approval_pending,
            "denied_reason": denied_reason,
            "steps": step_summaries,
            "optimization": wfo_report,
        }

        return {
            "answer": answer,
            "plan_json": plan_json,
            "execution_summary": execution_summary,
            "approval_pending": approval_pending,
        }

    def _generate_answer(
        self,
        engine: Any,
        plan: Any,
        results: list,
        all_ok: bool,
        approval_pending: Optional[str],
        denied_reason: Optional[str],
        session_id: str,
    ) -> str:
        """
        Build the human-readable answer via the Report Generation Agent
        (execution_summary report). Falls back to a plain string if the
        report agent is unavailable so the pipeline never hard-fails on
        answer formatting.
        """
        if approval_pending:
            return (
                f"⏸ Approval required before continuing. "
                f"Approve or reject action `{approval_pending}` to proceed."
            )
        if denied_reason:
            return f"⛔ Request stopped by policy: {denied_reason}"

        try:
            import tempfile
            from geosi_engine.models import ExecutionResult
            from geosi_engine.agents.report_generation import (
                ReportGenerationAgent,
                ReportRequest,
            )

            last = results[-1] if results else None
            exec_result = ExecutionResult(
                success=all_ok,
                answer=(last.message if last else "") or "",
                reasoning=getattr(plan, "reasoning", "") or "",
                error=(None if all_ok else (last.error if last else "execution failed")),
                results={},
                logs=[],
                total_duration_ms=0.0,
            )
            out_path = f"{tempfile.gettempdir()}/geosi_summary_{session_id or 'session'}.md"
            rr = ReportGenerationAgent(engine).generate(
                ReportRequest(
                    report_type="execution_summary",
                    plan=plan,
                    execution_result=exec_result,
                    session_id=session_id,
                    output_path=out_path,
                )
            )
            if rr.success and rr.content:
                return rr.content
        except Exception as exc:
            logger.debug("Report generation skipped: %s", exc)

        # Fallback: concise plain-text summary
        n_ok = sum(1 for r in results if getattr(r, "success", False))
        if not results:
            return "No steps were executed."
        if all_ok:
            last = results[-1]
            return (getattr(last, "message", None) or "Completed successfully.")
        return f"Partial completion: {n_ok}/{len(results)} steps succeeded."
