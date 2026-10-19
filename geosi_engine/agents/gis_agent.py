# -*- coding: utf-8 -*-
"""
GeoSI v2 — GIS Agent
════════════════════════════════════════════════════════════════════
Wraps the existing QGIS Processing discovery and execution.

The core innovation (dynamic tool discovery via ``processingRegistry()``)
is KEPT entirely unchanged (PRD §3.1 KEEP list).

The ONLY addition (PRD FR-2, G5 fix):
  A hard-coded, non-bypassable call to ``PermissionSafetyAgent.
  check_permission()`` before ANY tool with ``risk_level != "read_only"``
  reaches ``processing.run()``.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Optional

from geosi_engine.models import ApprovalResult, PermissionDecision, ToolResult, ToolStep

logger = logging.getLogger("geosi_engine.agents.gis_agent")


class PermissionDeniedError(Exception):
    """Raised when Permission & Safety Agent denies a tool execution."""
    pass


class ApprovalPendingError(Exception):
    """Raised when a tool requires human approval that hasn't arrived yet."""
    def __init__(self, action_id: str, message: str = "") -> None:
        self.action_id = action_id
        super().__init__(message or f"Approval pending: action_id={action_id}")


class GISAgent:
    """
    Executes ``ToolStep``s from an ``ExecutionPlan``.

    Wraps the existing ``ExecutionEngine`` and ``qgis_bridge`` dynamic
    discovery — both are KEPT unchanged.

    Parameters
    ----------
    engine:
        Session-scoped ``GeoSI`` instance.
    permission_agent:
        The ``PermissionSafetyAgent`` for the current session.
    """

    def __init__(self, engine: Any, permission_agent: Any) -> None:
        self._engine = engine
        self._permission = permission_agent

    # ------------------------------------------------------------------
    # Public: execute one step
    # ------------------------------------------------------------------

    def execute_step(
        self,
        step: ToolStep,
        state: Any,
        *,
        block_on_approval: bool = False,
    ) -> ToolResult:
        """
        Execute a single ``ToolStep`` with full permission enforcement.

        Permission logic (PRD FR-2, G5 fix):
        ─────────────────────────────────────
        1. Write audit log row BEFORE execution (FR-8.3).
        2. Read-only steps → execute immediately (no latency from permission
           check — verified by test ``test_read_only_bypasses_permission``).
        3. Mutating / destructive steps → ``check_permission()``:
           - ``"deny"``  → raise ``PermissionDeniedError``
           - ``"ask"``   → raise ``ApprovalPendingError`` (caller must
                           poll ``/approval/{action_id}`` or resolve via
                           HITL widget)
           - ``"allow"`` → proceed to execution

        Parameters
        ----------
        step:
            The ``ToolStep`` to execute.
        state:
            The session ``StateManager``.
        block_on_approval:
            If ``True``, poll approval synchronously (dev/test use only).

        Returns
        -------
        ToolResult
        """
        start_ms = time.monotonic() * 1000

        # ── Step 1: audit log BEFORE execution ──────────────────────────
        decision: Optional[PermissionDecision] = None
        audit_id: Optional[str] = None

        if step.risk_level != "read_only":
            # Get permission decision FIRST, then write audit log
            decision = self._permission.check_permission(
                step.tool_name, step.risk_level
            )
            audit_id = self._permission.audit_log_before_execution(
                step,
                session_id=getattr(self._engine, "_session_id", "unknown"),
                decision=decision,
            )

            if decision.decision == "deny":
                logger.warning(
                    "GISAgent: DENIED tool='%s' risk='%s'",
                    step.tool_name,
                    step.risk_level,
                )
                if audit_id:
                    self._permission.update_audit_log(audit_id, "denied")
                raise PermissionDeniedError(
                    f"Tool '{step.tool_name}' is denied by policy "
                    f"(risk_level='{step.risk_level}')."
                )

            session_id = getattr(self._engine, "_session_id", "unknown")
            if decision.decision == "ask" and self._permission.consume_approval(step, session_id):
                # A human already approved exactly this step (resumed run)
                decision = PermissionDecision(
                    algorithm_id=step.tool_name,
                    risk_level=step.risk_level,
                    decision="allow",
                    policy_source="human_approval",
                )

            if decision.decision == "ask":
                approval_result = self._permission.request_approval(
                    step,
                    session_id=getattr(self._engine, "_session_id", "unknown"),
                )
                if block_on_approval:
                    # Synchronous polling — only for tests / CLI
                    approved = self._poll_approval(approval_result.action_id)
                    if not approved:
                        if audit_id:
                            self._permission.update_audit_log(audit_id, "rejected")
                        raise PermissionDeniedError(
                            f"Tool '{step.tool_name}' was rejected by the user."
                        )
                else:
                    # Async: raise so the caller can surface the approval flow
                    raise ApprovalPendingError(
                        action_id=approval_result.action_id,
                        message=(
                            f"Tool '{step.tool_name}' requires approval. "
                            f"action_id={approval_result.action_id}"
                        ),
                    )
        else:
            # Read-only: write a minimal audit entry but don't block
            audit_id = self._permission.audit_log_before_execution(
                step,
                session_id=getattr(self._engine, "_session_id", "unknown"),
            )

        # ── Step 2: execute via existing ExecutionEngine ─────────────────
        try:
            result = self._run_step(step, state)
            status = "success" if result.success else "failed"
            if audit_id:
                self._permission.update_audit_log(
                    audit_id, status, error=result.error
                )
            return result
        except (PermissionDeniedError, ApprovalPendingError):
            raise
        except Exception as exc:
            if audit_id:
                self._permission.update_audit_log(audit_id, "error", error=str(exc))
            raise

    # ------------------------------------------------------------------
    # Tool discovery (KEEP — wraps qgis_bridge unchanged)
    # ------------------------------------------------------------------

    def discover_tools(self) -> int:
        """
        Trigger dynamic QGIS tool discovery.

        Delegates to ``qgis_bridge.auto_discover_qgis_tools()`` — the core
        innovation that replaces 2000+ lines of hardcoded tool wrappers.
        KEEP: no changes to discovery logic.
        """
        try:
            from geosi_plugin.qgis_bridge import auto_discover_qgis_tools  # type: ignore[import]

            return auto_discover_qgis_tools(self._engine.registry)
        except ImportError:
            logger.debug(
                "QGIS bridge not available (running outside QGIS). "
                "Portable tools only."
            )
            return 0
        except Exception as exc:
            logger.warning("Tool discovery failed: %s", exc)
            return 0

    # ------------------------------------------------------------------
    # Internal: run via existing ExecutionEngine
    # ------------------------------------------------------------------

    def _run_step(self, step: ToolStep, state: Any) -> ToolResult:
        """Delegate execution to the existing ExecutionEngine (KEEP)."""
        # ── Domain tools: dispatch to the specialist agent with the FULL
        # step context (input_layers / description / session). The permission
        # gate in execute_step() has already run for mutating domain tools;
        # we reuse this session's PermissionSafetyAgent so there is no second
        # prompt on the async surface (defense-in-depth re-check only).
        try:
            from geosi_engine.tools.domain_tools import dispatch_domain_tool, is_domain_tool
            if is_domain_tool(step.tool_name):
                return dispatch_domain_tool(self._engine, step, self._permission)
        except ImportError:
            pass

        if hasattr(self._engine, "executor") and self._engine.executor:
            return self._engine.executor.execute_step(step, state)

        # If executor is not available (e.g. no QGIS), try portable tools
        tool = None
        if hasattr(self._engine, "registry"):
            tool = self._engine.registry.get_tool(step.tool_name)

        if tool is None:
            return ToolResult(
                success=False,
                error=f"Tool '{step.tool_name}' not found.",
            )

        try:
            result = tool.execute(**step.parameters)
            if isinstance(result, ToolResult):
                return result
            return ToolResult(success=True, output=result, message=str(result))
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))

    # ------------------------------------------------------------------
    # Internal: synchronous approval polling (tests only)
    # ------------------------------------------------------------------

    @staticmethod
    def _poll_approval(
        action_id: str,
        poll_interval: float = 0.1,
        max_wait: float = 5.0,
    ) -> bool:
        """Poll the approval registry (synchronous, test use only)."""
        from geosi_engine.agents.permission_safety import PermissionSafetyAgent

        elapsed = 0.0
        while elapsed < max_wait:
            result = PermissionSafetyAgent._APPROVALS.is_approved(action_id)
            if result is not None:
                return result
            time.sleep(poll_interval)
            elapsed += poll_interval
        return False
