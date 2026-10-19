# -*- coding: utf-8 -*-
"""
GeoSI v2 — Neo4j Graph Schema Definitions (Phase P9, FR-8.4)
════════════════════════════════════════════════════════════════════
Node and relationship type constants and builder helpers.

Node types:
  :Dataset    — a spatial dataset (layer, raster, PostGIS table)
  :Workflow   — an ExecutionPlan / series of ToolSteps
  :Agent      — one of the 14 GeoSI agents
  :Execution  — one run of a Workflow (linked to geosi_audit_log)
  :Tool       — a QGIS processing tool / algorithm

Relationship types:
  (Execution)-[:USED]->(Dataset)
  (Execution)-[:RAN_BY]->(Agent)
  (Execution)-[:FOLLOWS]->(Workflow)
  (Workflow)-[:CONTAINS]->(Tool)
  (Dataset)-[:DERIVED_FROM]->(Dataset)
  (Dataset)-[:RELATED_TO]->(Dataset)   ← used by GraphRAG (P10)
"""
from __future__ import annotations

from typing import Any, Dict


# ── Node label constants ──────────────────────────────────────────────────

class NodeLabel:
    DATASET   = "Dataset"
    WORKFLOW  = "Workflow"
    AGENT     = "Agent"
    EXECUTION = "Execution"
    TOOL      = "Tool"


# ── Relationship type constants ───────────────────────────────────────────

class RelType:
    USED         = "USED"
    RAN_BY       = "RAN_BY"
    FOLLOWS      = "FOLLOWS"
    CONTAINS     = "CONTAINS"
    DERIVED_FROM = "DERIVED_FROM"
    RELATED_TO   = "RELATED_TO"
    PRECEDES     = "PRECEDES"


# ── Node property builders ────────────────────────────────────────────────

def build_dataset_props(
    name: str,
    path: str,
    crs: str = "",
    geometry_type: str = "",
    feature_count: int = 0,
    source: str = "",
) -> Dict[str, Any]:
    """Build properties dict for a :Dataset node."""
    return {
        "dataset_id": _make_dataset_id(name, path),
        "name": name,
        "path": path,
        "crs": crs,
        "geometry_type": geometry_type,
        "feature_count": feature_count,
        "source": source,
    }


def build_workflow_props(plan_id: str, query: str, step_count: int, session_id: str = "") -> Dict[str, Any]:
    """Build properties dict for a :Workflow node."""
    return {
        "plan_id": plan_id,
        "query": query[:500],  # truncate for storage
        "step_count": step_count,
        "session_id": session_id,
    }


def build_agent_props(agent_name: str, phase: str = "") -> Dict[str, Any]:
    """Build properties dict for an :Agent node."""
    return {
        "name": agent_name,
        "phase": phase,
    }


def build_execution_props(
    audit_id: str,
    plan_id: str,
    session_id: str,
    status: str,
    duration_ms: float = 0.0,
    risk_level: str = "",
) -> Dict[str, Any]:
    """Build properties dict for an :Execution node."""
    return {
        "audit_id": audit_id,
        "plan_id": plan_id,
        "session_id": session_id,
        "status": status,
        "duration_ms": duration_ms,
        "risk_level": risk_level,
    }


def build_tool_props(tool_name: str, provider: str = "", risk_level: str = "") -> Dict[str, Any]:
    """Build properties dict for a :Tool node."""
    return {
        "tool_id": tool_name,
        "name": tool_name,
        "provider": provider or _infer_provider(tool_name),
        "risk_level": risk_level,
    }


# ── Internal helpers ──────────────────────────────────────────────────────

def _make_dataset_id(name: str, path: str) -> str:
    """Deterministic dataset ID from name + path. O(1)."""
    import hashlib
    return hashlib.sha256(f"{name}:{path}".encode()).hexdigest()[:16]


def _infer_provider(tool_name: str) -> str:
    """Infer QGIS processing provider from tool algorithm ID."""
    if ":" not in tool_name:
        return "unknown"
    return tool_name.split(":")[0]
