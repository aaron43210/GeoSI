# -*- coding: utf-8 -*-
"""
GeoSI Data Layer — SQLAlchemy ORM Models
═══════════════════════════════════════════════════════════════════

Defines the PostGIS database schema for persistent storage:
    - SpatialLayerRecord: Metadata about stored spatial layers
    - ProjectRecord: GIS project definitions
    - WorkflowHistoryRecord: Past query → plan → result logs
    - ExecutionResultRecord: Per-step execution details

All tables use the 'geosi_' prefix to avoid collisions with
user data in the same PostGIS database.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def _uuid() -> str:
    """Generate a short UUID for primary keys."""
    return str(uuid.uuid4())[:12]


def _now() -> datetime:
    """Current UTC timestamp."""
    return datetime.now(timezone.utc)


class SpatialLayerRecord(Base):
    """
    Metadata record for a spatial layer stored in PostGIS.

    The actual geometry data is stored in a separate PostGIS table
    (one table per layer, managed by PostGISManager). This record
    tracks the metadata and the table name where geometries live.
    """
    __tablename__ = "geosi_layers"

    id = Column(String(12), primary_key=True, default=_uuid)
    name = Column(String(255), nullable=False, unique=True, index=True)
    geometry_type = Column(String(50), default="Unknown")
    crs = Column(String(50), default="EPSG:4326")
    feature_count = Column(Integer, default=0)
    layer_type = Column(String(20), default="vector")  # "vector" or "raster"
    table_name = Column(String(255), nullable=True)  # PostGIS table with geometries
    filepath = Column(Text, nullable=True)  # Original file path
    metadata_json = Column(JSON, nullable=True)  # Extra metadata (fields, bounds, etc.)
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now, onupdate=_now)

    def __repr__(self):
        return (
            f"SpatialLayerRecord(name={self.name!r}, "
            f"type={self.layer_type}, geom={self.geometry_type})"
        )


class ProjectRecord(Base):
    """
    A GIS project definition — groups layers together with a CRS.
    """
    __tablename__ = "geosi_projects"

    id = Column(String(12), primary_key=True, default=_uuid)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, default="")
    crs = Column(String(50), default="EPSG:4326")
    layer_names_json = Column(JSON, default=list)  # List of layer names in project
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now, onupdate=_now)

    def __repr__(self):
        return f"ProjectRecord(name={self.name!r}, crs={self.crs})"


class WorkflowHistoryRecord(Base):
    """
    Records a complete query → plan → result execution cycle.

    This is the primary table for workflow memory — the knowledge
    layer queries this to find similar past workflows.
    """
    __tablename__ = "geosi_workflow_history"

    id = Column(String(12), primary_key=True, default=_uuid)
    query = Column(Text, nullable=False, index=True)
    intent = Column(String(50), nullable=True)
    plan_json = Column(JSON, nullable=True)  # Serialized ExecutionPlan
    result_json = Column(JSON, nullable=True)  # Serialized ExecutionResult summary
    status = Column(String(20), default="unknown")  # success, partial, failed
    duration_ms = Column(Float, default=0.0)
    tool_sequence = Column(JSON, default=list)  # ["buffer", "intersect", ...]
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_now)

    # Relationship to per-step results
    step_results = relationship(
        "ExecutionResultRecord",
        back_populates="workflow",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"WorkflowHistoryRecord(query={self.query[:50]!r}, "
            f"status={self.status})"
        )


class ExecutionResultRecord(Base):
    """
    Per-step execution result within a workflow.

    Tracks which tool ran, whether it succeeded, timing,
    and any error messages — for the feedback memory system.
    """
    __tablename__ = "geosi_execution_results"

    id = Column(String(12), primary_key=True, default=_uuid)
    workflow_id = Column(
        String(12),
        ForeignKey("geosi_workflow_history.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    step_id = Column(String(50), nullable=False)
    tool_name = Column(String(255), nullable=False, index=True)
    status = Column(String(20), default="unknown")
    duration_ms = Column(Float, default=0.0)
    output_features = Column(Integer, default=0)
    output_path = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    parameters_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=_now)

    # Back-reference to parent workflow
    workflow = relationship("WorkflowHistoryRecord", back_populates="step_results")

    def __repr__(self):
        return (
            f"ExecutionResultRecord(step={self.step_id}, "
            f"tool={self.tool_name}, status={self.status})"
        )


# ═══════════════════════════════════════════════════════════════════════════
# v2 NEW TABLES — Security, Permission, Evaluation, Memory
# All added in Phase 1 (audit_log, policy_overrides, pending_approvals)
# and Phase 2/5 (eval_runs, query_history, feedback_history via Alembic).
# ═══════════════════════════════════════════════════════════════════════════


class AuditLogRecord(Base):
    """
    Immutable audit log for every tool execution.

    PRD FR-8.3: Written BEFORE execution begins, never deleted.
    No ``updated_at`` — once written, this record is append-only.

    ``status`` is updated post-execution but only to record outcome
    (success/failed/denied/rejected). The original pre-execution row
    always exists for forensics even if the server crashes mid-run.
    """

    __tablename__ = "geosi_audit_log"

    id = Column(String(12), primary_key=True, default=_uuid)
    session_id = Column(String(255), nullable=False, index=True)
    tool_name = Column(String(255), nullable=False, index=True)
    parameters_json = Column(JSON, nullable=True)
    risk_level = Column(String(20), default="read_only")
    decision = Column(String(10), default="allow")  # allow | ask | deny
    policy_source = Column(String(20), default="default")  # default | override_table
    status = Column(String(20), default="pending")  # pending | success | failed | denied | rejected | error
    error_message = Column(Text, nullable=True)
    # created_at only — no updated_at (immutable record)
    created_at = Column(DateTime, default=_now)

    def __repr__(self) -> str:
        return (
            f"AuditLogRecord(tool={self.tool_name!r}, "
            f"risk={self.risk_level}, decision={self.decision}, "
            f"status={self.status})"
        )


class PolicyOverrideRecord(Base):
    """
    Per-deployment permission policy overrides for specific algorithms.

    Administrators can set a specific ``decision`` for any QGIS algorithm ID.
    The ``PermissionSafetyAgent`` consults this table before applying the
    default policy (read_only→allow, mutating→ask, destructive→ask).

    Example overrides:
        native:buffer → allow   (trusted, widely used — skip approval)
        native:deletefield → deny  (never allowed in this deployment)
    """

    __tablename__ = "geosi_policy_overrides"

    id = Column(String(12), primary_key=True, default=_uuid)
    algorithm_id = Column(String(255), nullable=False, unique=True, index=True)
    decision = Column(String(10), nullable=False)  # allow | ask | deny
    set_by = Column(String(255), default="admin")
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now, onupdate=_now)

    def __repr__(self) -> str:
        return (
            f"PolicyOverrideRecord(algorithm={self.algorithm_id!r}, "
            f"decision={self.decision}, set_by={self.set_by!r})"
        )


class PendingApprovalRecord(Base):
    """
    A pending human-in-the-loop (HITL) approval request.

    Created by ``PermissionSafetyAgent.request_approval()`` when a
    mutating/destructive tool requires user confirmation.
    Resolved by the QGIS dock widget (Phase 4) or the
    ``approve_pending_action`` MCP tool.
    """

    __tablename__ = "geosi_pending_approvals"

    id = Column(String(12), primary_key=True, default=_uuid)
    action_id = Column(String(12), nullable=False, unique=True, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    step_data_json = Column(JSON, nullable=True)   # serialized ToolStep
    risk_level = Column(String(20), default="mutating")
    status = Column(String(20), default="pending")  # pending | approved | rejected | expired
    resolved_by = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now, onupdate=_now)

    def __repr__(self) -> str:
        return (
            f"PendingApprovalRecord(action_id={self.action_id!r}, "
            f"status={self.status})"
        )


class EvalRunRecord(Base):
    """
    RAGAS evaluation run results.

    Populated by ``geosi_eval.eval_runner`` (Phase 2).
    Used by ``WorkflowOptimizationAgent`` (Phase 8) to suggest
    faster execution paths based on historical performance.
    """

    __tablename__ = "geosi_eval_runs"

    id = Column(String(12), primary_key=True, default=_uuid)
    run_name = Column(String(255), nullable=True)
    # ``query`` is nullable: the ML agent, Workflow-Optimization agent, and the
    # RAGAS runner all write generic job rows (job_type/metrics/...) that have
    # no single query. Marking it NOT NULL made every one of those inserts fail
    # with an IntegrityError (silently swallowed by their try/except).
    query = Column(Text, nullable=True, default="")
    domain = Column(String(50), nullable=True)  # gis | rs | ml | geology
    expected_tools_json = Column(JSON, nullable=True)
    actual_tools_json = Column(JSON, nullable=True)
    # RAGAS metrics
    faithfulness = Column(Float, nullable=True)
    context_precision = Column(Float, nullable=True)
    context_recall = Column(Float, nullable=True)
    answer_relevancy = Column(Float, nullable=True)
    # Timing
    plan_latency_ms = Column(Float, nullable=True)
    total_latency_ms = Column(Float, nullable=True)
    # Provider used
    provider = Column(String(50), nullable=True)
    plan_source = Column(String(50), nullable=True)  # ollama_function_calling | gemini | claude | rule_based

    # ── Generic job columns ────────────────────────────────────────────────
    # Written by MachineLearningAgent._persist_eval_run, the RAGASRunner's
    # batch/summary persistence, and read back by WorkflowOptimizationAgent.
    # These were used by that code but missing from the model, so every write
    # raised ``TypeError: invalid keyword argument`` and every read raised
    # ``AttributeError`` (both swallowed) — leaving the table effectively
    # write-only-fails. Added here (all nullable) to match the real usage.
    job_type = Column(String(50), nullable=True, index=True)
    algorithm = Column(String(255), nullable=True)
    metrics = Column(JSON, nullable=True)
    status = Column(String(20), nullable=True, default="unknown", index=True)
    session_id = Column(String(255), nullable=True, index=True)
    output_path = Column(Text, nullable=True)

    created_at = Column(DateTime, default=_now)

    def __repr__(self) -> str:
        q = (self.query or self.job_type or "")[:40]
        return (
            f"EvalRunRecord(ref={q!r}, "
            f"faithfulness={self.faithfulness})"
        )


class QueryHistoryRecord(Base):
    """
    Persistent query history (Phase 5 migration from ~/.geosi/query_history.json).

    ``QueryMemory`` writes here instead of the JSON file when PostGIS is
    available. PostGIS is the system of record; JSON file is dev-only cache.
    """

    __tablename__ = "geosi_query_history"

    id = Column(String(12), primary_key=True, default=_uuid)
    session_id = Column(String(255), nullable=True, index=True)
    query = Column(Text, nullable=False, index=True)
    intent = Column(String(50), nullable=True)
    success = Column(Boolean, default=True)
    duration_ms = Column(Float, nullable=True)
    tools_used_json = Column(JSON, nullable=True)
    pattern_json = Column(JSON, nullable=True)   # detected query pattern
    created_at = Column(DateTime, default=_now)

    def __repr__(self) -> str:
        return f"QueryHistoryRecord(query={self.query[:40]!r}, success={self.success})"


class FeedbackHistoryRecord(Base):
    """
    Per-tool feedback / reliability stats (Phase 5 migration from
    ~/.geosi/feedback.json).

    ``FeedbackMemory`` writes here when PostGIS is available.
    PostGIS is the system of record; JSON file is dev-only cache.
    """

    __tablename__ = "geosi_feedback_history"

    id = Column(String(12), primary_key=True, default=_uuid)
    tool_name = Column(String(255), nullable=False, index=True)
    success = Column(Boolean, nullable=False)
    duration_ms = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    query_pattern = Column(String(100), nullable=True)  # which pattern triggered this tool
    parameters_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=_now)

    def __repr__(self) -> str:
        status = "✅" if self.success else "❌"
        return f"FeedbackHistoryRecord({status} {self.tool_name!r})"

