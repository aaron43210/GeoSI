# -*- coding: utf-8 -*-
"""
GeoSI v2 — Permission & Safety Agent
════════════════════════════════════════════════════════════════════
The most critical agent in the system (PRD §4, FR-2, FR-3).

Responsibilities
────────────────
1. ``check_permission(algorithm_id, risk_level)`` — returns
   ``"allow"`` | ``"ask"`` | ``"deny"`` by consulting:
   a. ``geosi_policy_overrides`` table (DB-stored per-deployment overrides)
   b. Default policy by risk_level: read_only→allow, mutating→ask,
      destructive→ask + typed confirmation phrase.

2. ``request_approval(action, context)`` — creates a
   ``PendingApprovalRecord`` (in-memory + DB) and returns an
   ``ApprovalResult`` with a polled ``action_id``.

3. ``scan_rag_context(context)`` — attaches ``guardrail_flags`` to
   each retrieved document; NEVER strips silently (FR-3.1).

4. ``audit_log_before_execution(step, session_id)`` — writes an
   ``AuditLogRecord`` BEFORE ``processing.run()`` executes (FR-8.3).
   The audit row exists even if the step subsequently fails.

5. ``resolve_approval(action_id, approved)`` — called by the QGIS
   HITL dock widget (Phase 4) or ``approve_pending_action`` MCP tool.
"""
from __future__ import annotations

import logging
import re
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from geosi_engine.guardrails import scan_text
from geosi_engine.models import ApprovalResult, PermissionDecision, ToolStep

logger = logging.getLogger("geosi_engine.agents.permission_safety")


# Requests that would destroy data are refused before planning
# ("remove duplicates" / "drop null geometries" create new layers and are fine).
_DESTRUCTIVE_INTENT_RE = re.compile(
    r"\b(delete|drop|remove|erase|wipe|truncate|overwrite)\b"
    r"(?!\s+(?:the\s+)?(?:duplicate|duplicates|null|empty|holes?|small|slivers?|vertices))",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Pending approval registry (in-memory)
# ---------------------------------------------------------------------------


@dataclass
class _PendingApproval:
    action_id: str
    step_data: dict[str, Any]
    session_id: str
    risk_level: str
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    resolved: bool = False
    approved: Optional[bool] = None
    consumed: bool = False  # an approved action is used by exactly one execution


def _step_signature(tool_name: str, parameters: dict[str, Any]) -> str:
    """Stable identity of a step for matching approvals to executions."""
    import json

    return f"{tool_name}|{json.dumps(parameters, sort_keys=True, default=str)}"


class _ApprovalRegistry:
    """Thread-safe in-memory store for pending approvals."""

    def __init__(self) -> None:
        self._pending: dict[str, _PendingApproval] = {}
        self._lock = threading.Lock()

    def add(self, approval: _PendingApproval) -> None:
        with self._lock:
            self._pending[approval.action_id] = approval

    def resolve(self, action_id: str, approved: bool) -> bool:
        with self._lock:
            if action_id not in self._pending:
                return False
            self._pending[action_id].resolved = True
            self._pending[action_id].approved = approved
            return True

    def get(self, action_id: str) -> Optional[_PendingApproval]:
        with self._lock:
            return self._pending.get(action_id)

    def is_approved(self, action_id: str) -> Optional[bool]:
        with self._lock:
            p = self._pending.get(action_id)
            if p is None or not p.resolved:
                return None
            return p.approved

    def consume(self, session_id: str, signature: str) -> Optional[str]:
        """
        Use up an approved, not-yet-used action for this exact step in this
        session. Returns its action_id, or None when nothing matches.
        """
        with self._lock:
            for p in self._pending.values():
                if (p.resolved and p.approved and not p.consumed
                        and p.session_id == session_id
                        and p.step_data.get("signature") == signature):
                    p.consumed = True
                    return p.action_id
        return None

    def purge(self, max_age_seconds: float = 24 * 3600) -> int:
        """Drop approvals older than *max_age_seconds* (bounded memory)."""
        cutoff = datetime.now(timezone.utc).timestamp() - max_age_seconds
        with self._lock:
            old = [k for k, p in self._pending.items()
                   if datetime.fromisoformat(p.created_at).timestamp() < cutoff]
            for k in old:
                del self._pending[k]
            return len(old)


# ---------------------------------------------------------------------------
# Permission & Safety Agent
# ---------------------------------------------------------------------------

class PermissionSafetyAgent:
    """
    Enforces the allow/ask/deny permission policy and guardrail scanning.

    Parameters
    ----------
    engine:
        Session-scoped ``GeoSI`` instance (used to access DB for policy
        overrides and audit log writes).
    """

    _APPROVALS = _ApprovalRegistry()  # class-level, shared across sessions

    def __init__(self, engine: Any) -> None:
        self._engine = engine

    # ------------------------------------------------------------------
    # 1. Permission checking
    # ------------------------------------------------------------------

    def check_permission(
        self,
        algorithm_id: str,
        risk_level: str,
    ) -> PermissionDecision:
        """
        Return a permission decision for *algorithm_id* at *risk_level*.

        Look-up order:
        1. ``geosi_policy_overrides`` table (DB).
        2. Default policy by risk_level.

        Returns
        -------
        PermissionDecision
            Contains ``decision``: ``"allow"`` | ``"ask"`` | ``"deny"``
        """
        # Step 1: check override table
        override = self._load_policy_override(algorithm_id)
        if override is not None:
            logger.debug(
                "Policy override for '%s': %s", algorithm_id, override
            )
            return PermissionDecision(
                algorithm_id=algorithm_id,
                risk_level=risk_level,
                decision=override,
                policy_source="override_table",
            )

        # Step 2: default policy by risk level
        decision = self._default_policy(risk_level)
        return PermissionDecision(
            algorithm_id=algorithm_id,
            risk_level=risk_level,
            decision=decision,
            policy_source="default",
        )

    @staticmethod
    def _default_policy(risk_level: str) -> str:
        """Map risk_level → default permission decision."""
        mapping = {
            "read_only": "allow",
            "mutating": "ask",
            "destructive": "ask",   # ask + confirmation phrase enforced by HITL
        }
        return mapping.get(risk_level, "ask")

    def _load_policy_override(self, algorithm_id: str) -> Optional[str]:
        """
        Query ``geosi_policy_overrides`` for an override entry.

        Returns the override decision string or ``None`` if not found.
        Gracefully degrades if the DB is unavailable.
        """
        try:
            db = self._get_db()
            if db is None or not db.available:
                return None
            with db.get_session() as session:
                from geosi_data.db_models import PolicyOverrideRecord
                record = (
                    session.query(PolicyOverrideRecord)
                    .filter(PolicyOverrideRecord.algorithm_id == algorithm_id)
                    .first()
                )
                if record:
                    return str(record.decision)
        except Exception as exc:
            logger.warning("Failed to load policy override: %s", exc)
        return None

    # ------------------------------------------------------------------
    # 2. Approval requests (HITL flow)
    # ------------------------------------------------------------------

    def request_approval(
        self,
        step: ToolStep,
        session_id: str,
        context: Optional[dict[str, Any]] = None,
    ) -> ApprovalResult:
        """
        Create a pending approval and return an ``ApprovalResult`` for polling.

        The QGIS dock HITL widget (Phase 4) resolves this via
        ``resolve_approval()``.  REST/MCP clients poll ``GET /approval/{id}``
        or use the ``approve_pending_action`` MCP tool.

        Parameters
        ----------
        step:
            The ``ToolStep`` that needs human approval.
        session_id:
            Current session identifier.
        context:
            Optional extra context to show in the approval UI.

        Returns
        -------
        ApprovalResult
            ``approved=False``, ``approver="pending"``, with an
            ``action_id`` the caller can poll.
        """
        action_id = str(uuid.uuid4())[:12]
        pending = _PendingApproval(
            action_id=action_id,
            step_data={
                "tool_name": step.tool_name,
                "parameters": step.parameters,
                "risk_level": step.risk_level,
                "description": step.description,
                "context": context or {},
                "signature": _step_signature(step.tool_name, step.parameters),
            },
            session_id=session_id,
            risk_level=step.risk_level,
        )
        self._APPROVALS.add(pending)
        self._persist_pending_approval(pending)
        logger.info(
            "Approval requested: action_id=%s, tool=%s, risk=%s",
            action_id,
            step.tool_name,
            step.risk_level,
        )
        return ApprovalResult(
            approved=False,
            action_id=action_id,
            approver="pending",
        )

    def resolve_approval(self, action_id: str, approved: bool) -> bool:
        """
        Resolve a pending approval (called by HITL widget or MCP tool).

        Returns ``True`` if the action_id was found and resolved.
        """
        success = self._APPROVALS.resolve(action_id, approved)
        if success:
            logger.info(
                "Approval resolved: action_id=%s, approved=%s", action_id, approved
            )
        return success

    def poll_approval(self, action_id: str) -> Optional[bool]:
        """
        Poll approval status.  Returns ``None`` if still pending.
        """
        return self._APPROVALS.is_approved(action_id)

    def consume_approval(self, step: ToolStep, session_id: str) -> Optional[str]:
        """
        Return the action_id of a human approval granted for exactly this
        step in this session (and mark it used), or None.
        """
        self._APPROVALS.purge()
        action_id = self._APPROVALS.consume(session_id, _step_signature(step.tool_name, step.parameters))
        if action_id:
            logger.info("Using approval %s for tool=%s", action_id, step.tool_name)
        return action_id

    # ------------------------------------------------------------------
    # 3. Guardrail scanning
    # ------------------------------------------------------------------

    def screen_request(self, query: str) -> Optional[str]:
        """
        Check a user request before any planning happens.

        Returns a refusal message for requests that ask to destroy data or
        that carry prompt-injection patterns; None when the request may
        proceed.
        """
        if _DESTRUCTIVE_INTENT_RE.search(query or ""):
            return ("⚠ GeoSI does not delete or overwrite data. If you meant to create a "
                    "filtered copy, ask e.g. \"extract hospitals where beds > 100\".")
        result = scan_text(query or "")
        if not result.is_clean:
            logger.warning("Request refused by guardrails: %s", result.flags)
            return ("⚠ This request contains instructions aimed at the assistant itself "
                    f"({', '.join(result.flags[:3])}), so it was not run. Please rephrase it "
                    "as a GIS task.")
        return None

    def scan_rag_context(self, context_obj: Any) -> Any:
        """
        Scan all text in a RAG context object for injection patterns.

        Attaches ``guardrail_flags`` to each ``SearchResult`` and to the
        context object itself.  Does NOT strip or silently remove content
        (FR-3.1 — annotate, never trust silently).

        Parameters
        ----------
        context_obj:
            A ``RAGResult`` (or any object with ``.documents`` and
            ``.workflows`` lists of ``SearchResult``-like objects).

        Returns
        -------
        The same *context_obj*, mutated in-place with ``guardrail_flags``
        attached to flagged items.
        """
        all_flags: list[str] = []

        for collection_attr in ("documents", "workflows"):
            items = getattr(context_obj, collection_attr, []) or []
            for item in items:
                text = getattr(item, "text", "") or ""
                result = scan_text(text)
                if not result.is_clean:
                    if hasattr(item, "metadata") and isinstance(item.metadata, dict):
                        item.metadata["guardrail_flags"] = result.flags
                    all_flags.extend(result.flags)
                    logger.warning(
                        "Guardrail flags on RAG item (source=%s): %s",
                        getattr(item, "source", "unknown"),
                        result.flags,
                    )

        if hasattr(context_obj, "guardrail_flags"):
            context_obj.guardrail_flags = all_flags

        return context_obj

    # ------------------------------------------------------------------
    # 4. Audit log (write BEFORE execution)
    # ------------------------------------------------------------------

    def audit_log_before_execution(
        self,
        step: ToolStep,
        session_id: str,
        decision: Optional[PermissionDecision] = None,
    ) -> Optional[str]:
        """
        Write an immutable audit log row BEFORE ``processing.run()`` executes.

        PRD FR-8.3: "every mutating action gets an audit-log row before
        execution, not after."

        Returns the audit log row ID, or None if DB is unavailable.
        """
        try:
            db = self._get_db()
            if db is None or not db.available:
                logger.debug("Audit log skipped — DB unavailable")
                return None

            from geosi_data.db_models import AuditLogRecord

            record = AuditLogRecord(
                session_id=session_id,
                tool_name=step.tool_name,
                parameters_json=step.parameters,
                risk_level=step.risk_level,
                decision=decision.decision if decision else "allow",
                policy_source=decision.policy_source if decision else "default",
                status="pending",
            )
            with db.get_session() as sess:
                sess.add(record)
                sess.flush()
                audit_id = record.id
            logger.debug("Audit log written: id=%s, tool=%s", audit_id, step.tool_name)
            return str(audit_id)

        except Exception as exc:
            logger.error("Failed to write audit log: %s", exc)
            return None

    def update_audit_log(
        self, audit_id: str, status: str, error: Optional[str] = None
    ) -> None:
        """Update an existing audit log row with the execution outcome."""
        try:
            db = self._get_db()
            if db is None or not db.available or not audit_id:
                return
            from geosi_data.db_models import AuditLogRecord
            with db.get_session() as sess:
                record = sess.get(AuditLogRecord, audit_id)
                if record:
                    record.status = status
                    if error:
                        record.error_message = error
        except Exception as exc:
            logger.warning("Failed to update audit log %s: %s", audit_id, exc)

    # ------------------------------------------------------------------
    # Admin: policy override CRUD
    # ------------------------------------------------------------------

    def set_policy_override(
        self,
        algorithm_id: str,
        decision: str,
        set_by: str = "admin",
    ) -> bool:
        """
        Create or update a policy override in ``geosi_policy_overrides``.

        Parameters
        ----------
        algorithm_id:
            QGIS algorithm ID (e.g. ``"native:buffer"``).
        decision:
            ``"allow"``, ``"ask"``, or ``"deny"``.
        set_by:
            Identifier of the admin who set the override.

        Returns ``True`` on success.
        """
        if decision not in ("allow", "ask", "deny"):
            raise ValueError(f"Invalid decision: {decision!r}. Must be allow/ask/deny.")

        try:
            db = self._get_db()
            if db is None or not db.available:
                return False
            from geosi_data.db_models import PolicyOverrideRecord
            with db.get_session() as sess:
                record = (
                    sess.query(PolicyOverrideRecord)
                    .filter(PolicyOverrideRecord.algorithm_id == algorithm_id)
                    .first()
                )
                if record:
                    record.decision = decision
                    record.set_by = set_by
                else:
                    sess.add(PolicyOverrideRecord(
                        algorithm_id=algorithm_id,
                        decision=decision,
                        set_by=set_by,
                    ))
            return True
        except Exception as exc:
            logger.error("Failed to set policy override: %s", exc)
            return False

    def delete_policy_override(self, algorithm_id: str) -> bool:
        """Remove a policy override. Returns ``True`` if deleted."""
        try:
            db = self._get_db()
            if db is None or not db.available:
                return False
            from geosi_data.db_models import PolicyOverrideRecord
            with db.get_session() as sess:
                deleted = (
                    sess.query(PolicyOverrideRecord)
                    .filter(PolicyOverrideRecord.algorithm_id == algorithm_id)
                    .delete()
                )
                return deleted > 0
        except Exception as exc:
            logger.error("Failed to delete policy override: %s", exc)
            return False

    def list_policy_overrides(self) -> list[dict[str, Any]]:
        """Return all policy overrides as a list of dicts."""
        try:
            db = self._get_db()
            if db is None or not db.available:
                return []
            from geosi_data.db_models import PolicyOverrideRecord
            with db.get_session() as sess:
                records = sess.query(PolicyOverrideRecord).all()
                return [
                    {
                        "algorithm_id": r.algorithm_id,
                        "decision": r.decision,
                        "set_by": r.set_by,
                        "created_at": str(r.created_at),
                    }
                    for r in records
                ]
        except Exception as exc:
            logger.error("Failed to list policy overrides: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_db(self) -> Any:
        """Return the session's Database instance, or None."""
        try:
            if hasattr(self._engine, "data") and self._engine.data:
                return self._engine.data.get("database")
        except Exception:
            logger.debug("suppressed exception", exc_info=True)
        return None

    def _persist_pending_approval(self, pending: _PendingApproval) -> None:
        """Persist pending approval to DB (best-effort)."""
        try:
            db = self._get_db()
            if db is None or not db.available:
                return
            from geosi_data.db_models import PendingApprovalRecord
            with db.get_session() as sess:
                sess.add(PendingApprovalRecord(
                    action_id=pending.action_id,
                    session_id=pending.session_id,
                    step_data_json=pending.step_data,
                    risk_level=pending.risk_level,
                    status="pending",
                ))
        except Exception as exc:
            logger.debug("Failed to persist pending approval to DB: %s", exc)
