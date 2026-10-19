# -*- coding: utf-8 -*-
"""
GeoSI v2 — Workflow Optimization Agent (Optional Agent #13)
════════════════════════════════════════════════════════════════════
Compares workflows, suggests faster execution paths, removes
unnecessary steps, and learns best practices from execution history.

PRD §4.2 Optional Agent #13 — Production notes
────────────────────────────────────────────────
* Reads from ``WorkflowMemory`` / ``geosi_eval_runs`` — read-only.
* Always ``allow``-tier — never executes or modifies data.
* Produces an ``OptimizationReport`` for the user to review.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from geosi_engine.telemetry import span, set_span_attr

logger = logging.getLogger("geosi_engine.agents.workflow_optimization")


@dataclass
class OptimizationSuggestion:
    """A single workflow optimization suggestion."""
    type: str               # "remove_step" | "reorder" | "replace_tool" | "parallelize" | "cache"
    step_index: Optional[int] = None
    message: str = ""
    estimated_time_saving_s: float = 0.0
    confidence: float = 1.0  # 0–1


@dataclass
class OptimizationReport:
    """Result of workflow optimization analysis."""
    success: bool
    original_step_count: int = 0
    optimized_step_count: int = 0
    suggestions: List[OptimizationSuggestion] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    similar_workflows: List[Dict[str, Any]] = field(default_factory=list)
    estimated_total_saving_s: float = 0.0
    error: Optional[str] = None


class WorkflowOptimizationAgent:
    """
    Workflow Optimization Agent (PRD §4.2, Agent #13).

    Reads ``WorkflowMemory`` and ``geosi_eval_runs`` to:
    - Find similar successful past workflows.
    - Identify redundant steps (same output, different tool).
    - Suggest step ordering improvements (dependency-aware).
    - Recommend caching opportunities.
    - Surface best-practice patterns from execution history.

    Always read-only; always ``allow``-tier.

    Parameters
    ----------
    engine:
        Session-scoped GeoSI instance.
    """

    def __init__(self, engine: Any) -> None:
        self._engine = engine

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    @span("workflow_opt.analyze", agent="workflow_optimization")
    def analyze(self, plan: Any) -> OptimizationReport:
        """
        Analyse an ``ExecutionPlan`` and return optimization suggestions.

        This is the primary entry point called by the Supervisor before
        execution (advisory only — does not modify the plan).
        """
        steps = getattr(plan, "steps", [])
        set_span_attr("wfo.step_count", len(steps))

        suggestions: list[OptimizationSuggestion] = []
        best_practices: list[str] = []

        # ── Check 1: redundant steps (same tool_name back-to-back) ────
        suggestions.extend(self._detect_redundant_steps(steps))

        # ── Check 2: order dependencies ────────────────────────────────
        suggestions.extend(self._check_step_ordering(steps))

        # ── Check 3: high-risk steps that could be batched ────────────
        suggestions.extend(self._suggest_batching(steps))

        # ── Check 4: load best practices from workflow memory ─────────
        best_practices = self._load_best_practices(plan)

        # ── Check 5: find similar past workflows ─────────────────────
        similar = self._find_similar_workflows(plan)

        total_saving = sum(s.estimated_time_saving_s for s in suggestions)
        set_span_attr("wfo.suggestions", len(suggestions))
        set_span_attr("wfo.estimated_saving_s", total_saving)

        return OptimizationReport(
            success=True,
            original_step_count=len(steps),
            optimized_step_count=max(0, len(steps) - len([s for s in suggestions if s.type == "remove_step"])),
            suggestions=suggestions,
            best_practices=best_practices,
            similar_workflows=similar,
            estimated_total_saving_s=total_saving,
        )

    @span("workflow_opt.compare", agent="workflow_optimization")
    def compare_workflows(self, plan_a: Any, plan_b: Any) -> Dict[str, Any]:
        """
        Compare two ExecutionPlans and return a diff-style analysis.
        """
        steps_a = getattr(plan_a, "steps", [])
        steps_b = getattr(plan_b, "steps", [])

        tools_a = {getattr(s, "tool_name", "") for s in steps_a}
        tools_b = {getattr(s, "tool_name", "") for s in steps_b}

        return {
            "plan_a_steps": len(steps_a),
            "plan_b_steps": len(steps_b),
            "tools_only_in_a": sorted(tools_a - tools_b),
            "tools_only_in_b": sorted(tools_b - tools_a),
            "shared_tools": sorted(tools_a & tools_b),
            "recommendation": (
                f"Plan A uses {len(steps_a)} steps, Plan B uses {len(steps_b)} steps. "
                f"{'Plan B is shorter.' if len(steps_b) < len(steps_a) else 'Plan A is shorter.' if len(steps_a) < len(steps_b) else 'Same length.'}"
            ),
        }

    # ------------------------------------------------------------------
    # Internal analysis helpers
    # ------------------------------------------------------------------

    def _detect_redundant_steps(self, steps: list) -> list[OptimizationSuggestion]:
        """Flag consecutive steps using the same tool with identical parameters."""
        suggestions: list[OptimizationSuggestion] = []
        for i in range(1, len(steps)):
            prev = steps[i - 1]
            curr = steps[i]
            if (getattr(prev, "tool_name", "") == getattr(curr, "tool_name", "")
                    and getattr(prev, "parameters", {}) == getattr(curr, "parameters", {})):
                suggestions.append(OptimizationSuggestion(
                    type="remove_step", step_index=i,
                    message=(
                        f"Step {i+1} ('{getattr(curr, 'tool_name', '?')}') is identical to Step {i}. "
                        "Consider removing the duplicate."
                    ),
                    estimated_time_saving_s=2.0,
                    confidence=0.95,
                ))
        return suggestions

    def _check_step_ordering(self, steps: list) -> list[OptimizationSuggestion]:
        """Check for obvious ordering improvements — e.g., reprojection should come first."""
        suggestions: list[OptimizationSuggestion] = []
        tool_names = [getattr(s, "tool_name", "") for s in steps]

        reproject_indices = [i for i, t in enumerate(tool_names) if "reproject" in t.lower()]
        for idx in reproject_indices:
            if idx > 0:
                suggestions.append(OptimizationSuggestion(
                    type="reorder", step_index=idx,
                    message=(
                        f"Reprojection (step {idx+1}) should ideally run before other operations. "
                        "Move it to the beginning to avoid processing data in mismatched CRS."
                    ),
                    estimated_time_saving_s=1.5,
                    confidence=0.8,
                ))

        # Flag dissolve-after-clip pattern. Match by substring because the real
        # registry names are prefixed (e.g. "native_clip", "native_dissolve"),
        # so exact "clip"/"dissolve" membership would never fire.
        ci = next((i for i, t in enumerate(tool_names) if "clip" in t.lower()), -1)
        di = next((i for i, t in enumerate(tool_names) if "dissolve" in t.lower()), -1)
        if ci >= 0 and di >= 0 and di < ci:
            suggestions.append(OptimizationSuggestion(
                type="reorder",
                message="Dissolve before Clip can reduce the dataset size before clipping — more efficient.",
                estimated_time_saving_s=3.0,
                confidence=0.7,
            ))
        return suggestions

    def _suggest_batching(self, steps: list) -> list[OptimizationSuggestion]:
        """Suggest batching read-only operations that could run in parallel."""
        read_only = [
            (i, s) for i, s in enumerate(steps)
            if getattr(s, "risk_level", "") == "read_only"
        ]
        if len(read_only) > 2:
            indices = [i + 1 for i, _ in read_only]
            return [OptimizationSuggestion(
                type="parallelize",
                message=(
                    f"Steps {indices} are all read-only and could be parallelized "
                    "if they don't share output dependencies."
                ),
                estimated_time_saving_s=len(read_only) * 1.0,
                confidence=0.6,
            )]
        return []

    def _load_best_practices(self, plan: Any) -> list[str]:
        """Load relevant best practices from WorkflowMemory."""
        practices: list[str] = []
        try:
            if self._engine.knowledge and hasattr(self._engine.knowledge, "workflow_memory"):
                wm = self._engine.knowledge.workflow_memory
                query = getattr(plan, "reasoning", "") or "GIS workflow best practices"
                # WorkflowMemory exposes find_similar(query, limit) → [WorkflowExample].
                results = wm.find_similar(query, limit=3)
                for r in results:
                    name = getattr(r, "name", "")
                    desc = getattr(r, "description", "") or ""
                    practices.append(f"{name}: {desc}".strip(": ").strip() or str(r))
        except Exception as exc:
            logger.debug("Best practices retrieval failed: %s", exc)

        if not practices:
            # Sensible built-in defaults
            practices = [
                "Always validate CRS consistency before overlay operations.",
                "Use spatial indexes (ST_CreateIndex) on large PostGIS tables for faster queries.",
                "Clip data to the study area before running computationally expensive operations.",
                "Use File GeoPackage (.gpkg) instead of Shapefile for outputs — no column name truncation.",
            ]
        return practices

    def _find_similar_workflows(self, plan: Any) -> list[dict]:
        """Find similar successful past workflows from geosi_eval_runs / workflow memory."""
        similar: list[dict] = []
        try:
            db = self._get_db()
            if db and db.available:
                from geosi_data.db_models import EvalRunRecord
                with db.get_session() as sess:
                    records = (
                        sess.query(EvalRunRecord)
                        .filter(EvalRunRecord.status == "success")
                        .order_by(EvalRunRecord.created_at.desc())
                        .limit(3)
                        .all()
                    )
                    for r in records:
                        similar.append({
                            "id": r.id,
                            "job_type": getattr(r, "job_type", ""),
                            "created_at": str(getattr(r, "created_at", "")),
                            "metrics": getattr(r, "metrics", {}),
                        })
        except Exception as exc:
            logger.debug("Could not load similar workflows: %s", exc)
        return similar

    def _get_db(self):
        try:
            if self._engine and self._engine.data:
                return self._engine.data.get("database")
        except Exception:
            logger.debug("suppressed exception", exc_info=True)
        return None
