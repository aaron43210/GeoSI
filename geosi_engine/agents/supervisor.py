# -*- coding: utf-8 -*-
"""
GeoSI v2 — Supervisor Agent
════════════════════════════════════════════════════════════════════
The single entry point for every client surface:
  • QGIS plugin dock      (geosi_plugin/)
  • REST API + web UI     (geosi_server/)
  • MCP server            (geosi_mcp/)

No surface calls planning or execution directly — everything goes through
``SupervisorAgent.handle()`` (and ``resume()`` after an approval).

Responsibilities
────────────────
1. Sessions — one isolated engine per session id (``SessionPool``).
2. The pipeline — the session's ``AgentLoop`` drives the agent team:
   Permission & Safety → Planning → Reflection critic → Validation →
   Workflow Optimization → GIS Agent (permission gate) → Verification →
   Reflection feedback / re-plan → Report Generation.
3. LLM providers — process-wide circuit breakers per provider (hosted API,
   Ollama, Gemini, Anthropic): after N failures in a window a provider is
   skipped until its reset period passes.
4. Human-in-the-loop — a step that needs approval pauses the run and
   returns an ``approval_pending`` action id; ``resume()`` continues it.
5. Telemetry — an OpenTelemetry span per request when configured.
"""
from __future__ import annotations

import dataclasses
import logging
import os
import time
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from geosi_engine.telemetry import start_span

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
    HALF_OPEN = "half_open"  # probe: allow one trial call


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


# Process-wide breakers: every SupervisorAgent in this process shares them, so
# a provider that keeps failing is skipped for all sessions until it recovers.
_BREAKERS: dict[str, CircuitBreaker] = {}
_BREAKERS_LOCK = threading.Lock()
_PROVIDERS = ("api", "ollama", "gemini", "anthropic")


def _breaker(provider: str) -> CircuitBreaker:
    with _BREAKERS_LOCK:
        if provider not in _BREAKERS:
            _BREAKERS[provider] = CircuitBreaker(provider=provider)
        return _BREAKERS[provider]


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
    result: Any = None                      # the answer text
    error: Optional[str] = None
    plan_json: Optional[dict[str, Any]] = None
    execution_summary: Optional[dict[str, Any]] = None
    approval_pending: Optional[str] = None  # action_id when paused for approval
    session_id: str = ""
    latency_ms: float = 0.0
    execution_result: Any = None            # full ExecutionResult (output layers, logs)
    report: str = ""                        # Markdown execution report
    warnings: list[str] = field(default_factory=list)
    plan_source: str = ""


# ---------------------------------------------------------------------------
# Supervisor Agent
# ---------------------------------------------------------------------------

class SupervisorAgent:
    """
    Single entry point for all GeoSI client surfaces (QGIS plugin, REST,
    MCP, web UI).

    * Sessions: each ``session_id`` gets its own engine from the pool
      (isolated layers, results, approvals).
    * Pipeline: the session's ``AgentLoop`` runs the agent team — screen,
      plan, critique, validate, execute through the permission gate,
      verify, reflect and re-plan, answer and report.
    * LLM providers: guarded by process-wide circuit breakers (``api``,
      ``ollama``, ``gemini``, ``anthropic``).
    * Approvals: a step that needs human approval pauses the run;
      ``resume(action_id, approved)`` continues it in the right session.
    * Telemetry: one span per request (OpenTelemetry when configured).

    Parameters
    ----------
    pool:
        ``SessionPool`` (or any object with ``get_or_create(session_id)``).
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool
        self._circuit_breakers = self.provider_breakers()

    @staticmethod
    def provider_breakers() -> dict[str, CircuitBreaker]:
        return {name: _breaker(name) for name in _PROVIDERS}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def handle(self, request: SupervisorRequest) -> SupervisorResponse:
        """Process one request end-to-end in its session."""
        start = time.monotonic()
        with start_span(
            "supervisor.handle",
            **{"session.id": request.session_id, "surface": request.surface}
        ) as root_span:
            try:
                root_span.set_attribute("query.length", len(request.query))
                engine = self._pool.get_or_create(request.session_id)
                engine.loop.attach_supervisor(self)
                result = engine.run(request.query)
                response = self._response(engine, result, request.session_id, start)
                root_span.set_attribute("latency_ms", response.latency_ms)
                root_span.set_attribute("success", response.success)
                return response
            except Exception as exc:
                logger.error("Supervisor failed for session %s: %s", request.session_id, exc,
                             exc_info=True)
                return SupervisorResponse(
                    success=False, error=str(exc), session_id=request.session_id,
                    latency_ms=(time.monotonic() - start) * 1000,
                )

    def resume(self, action_id: str, approved: bool,
               session_id: Optional[str] = None) -> SupervisorResponse:
        """
        Resolve a pending approval and continue the paused run.

        The session comes from the approval record unless given.
        """
        from geosi_engine.agents.permission_safety import PermissionSafetyAgent

        start = time.monotonic()
        pending = PermissionSafetyAgent._APPROVALS.get(action_id)
        if pending is None:
            return SupervisorResponse(success=False, error=f"No pending approval {action_id!r}.",
                                      session_id=session_id or "")
        session_id = session_id or pending.session_id
        if pending.session_id != session_id:
            return SupervisorResponse(success=False, session_id=session_id,
                                      error="This approval belongs to a different session.")
        PermissionSafetyAgent._APPROVALS.resolve(action_id, approved)
        with start_span("supervisor.resume", **{"session.id": session_id, "approved": approved}):
            try:
                engine = self._pool.get_or_create(session_id)
                engine.loop.attach_supervisor(self)
                result = engine.resume(action_id, approved)
                return self._response(engine, result, session_id, start)
            except Exception as exc:
                logger.error("Resume failed for %s: %s", action_id, exc, exc_info=True)
                return SupervisorResponse(success=False, error=str(exc), session_id=session_id,
                                          latency_ms=(time.monotonic() - start) * 1000)

    def circuit_breaker_states(self) -> list[dict[str, Any]]:
        """Return all circuit breaker statuses for the /health endpoint."""
        return [cb.status() for cb in self._circuit_breakers.values()]

    # ------------------------------------------------------------------
    # LLM cascade with budget + circuit breaker (utility for callers that
    # orchestrate their own provider calls)
    # ------------------------------------------------------------------

    def run_with_budget(
        self,
        providers: list[str],
        fn: Callable[[str], Any],
        budget_seconds: float = _TOTAL_BUDGET_S,
        per_provider_timeout: float = _PROVIDER_TIMEOUT_S,
    ) -> Any:
        """
        Try each provider in order within a total time budget; each call is
        bounded by *per_provider_timeout* and its circuit breaker.
        Raises ``RuntimeError`` if all providers fail or the budget runs out.
        """
        import concurrent.futures

        deadline = time.monotonic() + budget_seconds
        last_error: Optional[Exception] = None
        for provider in providers:
            cb = self._circuit_breakers.get(provider) or _breaker(provider)
            if not cb.is_available():
                logger.debug("Skipping provider '%s' — circuit breaker OPEN", provider)
                continue
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError(f"LLM budget exhausted after trying providers: {providers}")
            # Not a ``with`` block: shutdown(wait=True) would block on a hung
            # provider and defeat the timeout. Abandon it instead.
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            future = executor.submit(fn, provider)
            try:
                result = future.result(timeout=min(per_provider_timeout, remaining))
                cb.record_success()
                return result
            except concurrent.futures.TimeoutError:
                future.cancel()
                logger.warning("Provider '%s' timed out", provider)
                cb.record_failure()
                last_error = TimeoutError(f"{provider} timed out")
            except Exception as exc:
                logger.warning("Provider '%s' failed: %s", provider, exc)
                cb.record_failure()
                last_error = exc
            finally:
                executor.shutdown(wait=False, cancel_futures=True)
        raise RuntimeError(f"All providers failed. Last error: {last_error}") from last_error

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _response(self, engine: Any, result: Any, session_id: str, start: float) -> SupervisorResponse:
        plan = getattr(engine.loop, "last_plan", None)
        plan_json = _json_safe(dataclasses.asdict(plan)) if plan is not None else None
        if plan_json is not None:
            plan_json.pop("request", None)  # parser internals, not part of the plan contract
        paused = bool(result.approval_pending)
        return SupervisorResponse(
            success=bool(result.success) or paused,
            result=result.answer,
            error=None if (result.success or paused) else (result.error or result.answer),
            plan_json=plan_json,
            execution_summary=_execution_summary(plan, result),
            approval_pending=result.approval_pending,
            session_id=session_id,
            latency_ms=(time.monotonic() - start) * 1000,
            execution_result=result,
            report=getattr(result, "report", ""),
            warnings=list(getattr(result, "warnings", []) or []),
            plan_source=getattr(result, "plan_source", "") or getattr(plan, "plan_source", ""),
        )


def _json_safe(value: Any) -> Any:
    """Round-trip through JSON (enums, dates and objects become strings)."""
    import json

    return json.loads(json.dumps(value, default=str))


def _execution_summary(plan: Any, result: Any) -> dict[str, Any]:
    logs = {log.step_id: log for log in getattr(result, "logs", []) or []}
    steps = []
    for step in getattr(plan, "steps", []) or []:
        log = logs.get(step.step_id)
        entry: dict[str, Any] = {
            "step_id": step.step_id,
            "tool_name": step.tool_name,
            "risk_level": step.risk_level,
            "executed": log is not None,
        }
        if log is not None:
            status = getattr(log.status, "value", str(log.status))
            entry.update({
                "success": status == "success",
                "duration_ms": round(log.duration_ms, 1),
                "output_features": log.output_features,
                "error": log.error_message,
            })
            if status == "pending_approval":
                entry["approval_pending"] = result.approval_pending
        steps.append(entry)
    return {
        "plan_id": getattr(plan, "plan_id", ""),
        "plan_source": getattr(result, "plan_source", "") or getattr(plan, "plan_source", ""),
        "total_steps": len(steps),
        "executed_steps": sum(1 for s in steps if s["executed"]),
        "all_success": bool(result.success),
        "approval_pending": result.approval_pending,
        "denied": bool(getattr(result, "denied", False)),
        "warnings": list(getattr(result, "warnings", []) or []),
        "steps": steps,
    }
