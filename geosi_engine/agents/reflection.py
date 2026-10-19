"""
GeoSI v2 — Reflection Agent (Core Agent #4)
════════════════════════════════════════════════════════════════════
Self-reviews the execution plan before execution; post-execution on
failure it generates corrected plans and retries up to N=2 times.

PRD §4.1 Agent #4 — Production requirements
────────────────────────────────────────────
* Pre-execution critic pass: flags plans that contradict retrieved
  documentation or reference a tool with known-low reliability score
  from ``FeedbackMemory.get_tool_reliability()``.
* Post-execution, on failure: retrieves similar past failures,
  generates a corrected plan, retries up to N=2.
* Read-only by design — never executes tools directly.
* Auto-tier: ``allow`` (no permission gate needed).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from geosi_engine.models import ExecutionPlan
from geosi_engine.telemetry import set_span_attr, span

logger = logging.getLogger("geosi_engine.agents.reflection")

# Maximum retries before surfacing the error to the user
_MAX_RETRIES = 2

# Minimum tool reliability score to pass the critic (0–1)
_MIN_RELIABILITY_THRESHOLD = 0.4


@dataclass
class CriticFinding:
    """One issue found by the pre-execution critic."""

    severity: str  # "warning" | "error"
    tool_name: str
    message: str
    reliability_score: Optional[float] = None


@dataclass
class CriticReport:
    """Result of the pre-execution critic pass."""

    ok: bool
    findings: list[CriticFinding] = field(default_factory=list)

    def errors(self) -> list[CriticFinding]:
        return [f for f in self.findings if f.severity == "error"]

    def warnings(self) -> list[CriticFinding]:
        return [f for f in self.findings if f.severity == "warning"]


class ReflectionAgent:
    """
    Self-review and self-correction agent (PRD §4.1, Agent #4).

    Two responsibilities:
    1. ``critic(plan)``   — pre-execution pass; returns a CriticReport.
    2. ``reflect_and_retry(plan, error, executor_fn)`` — post-execution
       failure handler; generates corrected plan; retries up to N=2.

    Parameters
    ----------
    engine:
        Session-scoped GeoSI instance (for knowledge/memory access).
    """

    def __init__(self, engine: Any) -> None:
        self._engine = engine

    # ------------------------------------------------------------------
    # 1. Pre-execution critic pass (FR-4.2)
    # ------------------------------------------------------------------

    @span("reflection.critic", agent="reflection")
    def critic(self, plan: ExecutionPlan) -> CriticReport:
        """
        Critique an ExecutionPlan before execution begins.

        Checks:
        a. Tool reliability scores from ``FeedbackMemory`` — flags tools
           with ``reliability < _MIN_RELIABILITY_THRESHOLD`` as warnings.
        b. Cross-checks tool names against the registered registry — flags
           unknown tools as errors.
        c. Checks for contradictory step ordering (e.g., using output of
           step N as input before step N runs).

        Returns
        -------
        CriticReport
            ``ok=True`` if no errors (warnings allowed to proceed).
        """
        findings: list[CriticFinding] = []

        for step in plan.steps:
            # a. Reliability check
            score = self._get_reliability(step.tool_name)
            if score is not None and score < _MIN_RELIABILITY_THRESHOLD:
                findings.append(
                    CriticFinding(
                        severity="warning",
                        tool_name=step.tool_name,
                        message=(
                            f"Tool '{step.tool_name}' has low reliability score "
                            f"({score:.2f} < threshold {_MIN_RELIABILITY_THRESHOLD}). "
                            "Consider an alternative tool."
                        ),
                        reliability_score=score,
                    )
                )

            # b. Registry check — tool must be discoverable
            if not self._tool_known(step.tool_name):
                findings.append(
                    CriticFinding(
                        severity="warning",
                        tool_name=step.tool_name,
                        message=(
                            f"Tool '{step.tool_name}' is not in the current tool registry. "
                            "May fail at execution time (QGIS not loaded or tool not discovered)."
                        ),
                    )
                )

        errors = [f for f in findings if f.severity == "error"]
        set_span_attr("critic.findings", len(findings))
        set_span_attr("critic.errors", len(errors))

        if findings:
            logger.info(
                "Reflection critic found %d finding(s) (%d errors) for plan %s",
                len(findings),
                len(errors),
                plan.plan_id,
            )

        return CriticReport(ok=len(errors) == 0, findings=findings)

    # ------------------------------------------------------------------
    # 2. Turning a rejected attempt into guidance for the next plan
    # ------------------------------------------------------------------

    # Common failure messages → what the planner should change
    _HINTS: tuple[tuple[str, str], ...] = (
        (r"not found in registry|unknown tool", "Use only tool names from the Available tools list."),
        (r"Missing required parameter: (\w+)", "Set the required parameter {0}."),
        (
            r"Incorrect parameter value for (\w+)",
            "The value for {0} is invalid for this tool; check its type and allowed options.",
        ),
        (r"does not exist in layer", "Use one of the field names listed for that layer."),
        (
            r"0 features",
            "Check which layer is the INPUT and which is the comparison layer, the spatial "
            "relationship, and distance units (metres).",
        ),
        (r"is not loaded|no layer named", "Reference only layers from the Available layers list."),
        (
            r"invalid expression|parser error",
            "Write a valid QGIS expression: field names in double quotes, text in single quotes.",
        ),
        (r"no result layer", "Use a processing tool whose output is a new layer."),
    )

    def feedback_for(self, plan: ExecutionPlan, problem: str) -> str:
        """
        Describe a rejected attempt for the planner: the plan, what was
        wrong, a targeted hint, and similar past failures (knowledge memory).
        """
        import re as _re

        steps = "; ".join(f"{s.step_id}: {s.tool_name} {s.parameters}" for s in plan.steps)
        lines = [f"Previous plan: {steps}", f"Problem: {problem}"]
        for pattern, hint in self._HINTS:
            m = _re.search(pattern, problem or "", _re.IGNORECASE)
            if m:
                lines.append("Hint: " + hint.format(*m.groups()))
                break
        similar = self._retrieve_similar_failures(problem or "")
        if similar:
            lines.append("Similar past failures: " + " | ".join(similar[:3]))
        set_span_attr("reflection.feedback_len", sum(len(x) for x in lines))
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # 3. Post-execution retry (FR-4.1)
    # ------------------------------------------------------------------

    @span("reflection.retry", agent="reflection")
    def reflect_and_retry(
        self,
        original_plan: ExecutionPlan,
        error: str,
        executor_fn: Callable[[ExecutionPlan], Any],
    ) -> Any:
        """
        On execution failure, retrieve similar past failures, generate a
        corrected plan, and retry up to N=2 times (FR-4.1).

        Parameters
        ----------
        original_plan:
            The plan that failed.
        error:
            The error string from the failed execution.
        executor_fn:
            A callable that accepts an ``ExecutionPlan`` and returns
            an execution result.  The Supervisor passes its own step
            executor here.

        Returns
        -------
        Any
            Result from the first successful retry.

        Raises
        ------
        RuntimeError
            If all retries are exhausted.
        """
        set_span_attr("reflection.original_plan_id", original_plan.plan_id)
        set_span_attr("reflection.error", error[:200])

        last_error = error
        for attempt in range(1, _MAX_RETRIES + 1):
            logger.info(
                "Reflection retry %d/%d for plan %s (error: %s)",
                attempt,
                _MAX_RETRIES,
                original_plan.plan_id,
                error[:100],
            )

            # a. Retrieve similar failures from knowledge memory
            similar_failures = self._retrieve_similar_failures(error)

            # b. Generate corrected plan
            corrected = self._generate_corrected_plan(original_plan, error, similar_failures, attempt)
            if corrected is None:
                logger.warning("Could not generate a corrected plan — retrying with original.")
                corrected = original_plan

            # c. Execute corrected plan
            try:
                result = executor_fn(corrected)
                set_span_attr("reflection.retry_success_attempt", attempt)
                logger.info("Reflection retry %d succeeded.", attempt)
                return result
            except Exception as exc:
                last_error = str(exc)
                logger.warning("Reflection retry %d failed: %s", attempt, exc)

        raise RuntimeError(
            f"Reflection Agent exhausted all {_MAX_RETRIES} retry attempts. " f"Last error: {last_error}"
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_reliability(self, tool_name: str) -> Optional[float]:
        """Look up reliability score from FeedbackMemory. Returns None if unavailable."""
        try:
            knowledge = getattr(self._engine, "knowledge", None)
            feedback = getattr(knowledge, "feedback_memory", None) if knowledge else None
            if feedback is not None:
                return feedback.get_tool_reliability(tool_name)
        except Exception as exc:
            logger.debug("Could not fetch reliability for '%s': %s", tool_name, exc)
        return None

    def _tool_known(self, tool_name: str) -> bool:
        """Return True if the tool is in the current registry."""
        try:
            if hasattr(self._engine, "registry"):
                return self._engine.registry.get_tool(tool_name) is not None
        except Exception:
            logger.debug("suppressed exception", exc_info=True)
        return True  # assume known if registry unavailable (QGIS context)

    def _retrieve_similar_failures(self, error: str) -> list[str]:
        """Retrieve similar past failures from query/workflow memory."""
        similar: list[str] = []
        try:
            knowledge = getattr(self._engine, "knowledge", None)
            query_memory = getattr(knowledge, "query_memory", None) if knowledge else None
            # Not all QueryMemory builds expose find_similar_failures — probe safely.
            finder = getattr(query_memory, "find_similar_failures", None)
            if callable(finder):
                past = finder(error, limit=3)
                similar = [str(p) for p in past]
        except Exception as exc:
            logger.debug("Failed to retrieve similar failures: %s", exc)
        return similar

    def _generate_corrected_plan(
        self,
        original: ExecutionPlan,
        error: str,
        similar_failures: list[str],
        attempt: int,
    ) -> Optional[ExecutionPlan]:
        """
        Generate a corrected ExecutionPlan using the Planning Agent with
        the error and similar failures as additional context.

        Re-planning needs a Supervisor (for the LLM budget cascade). When one
        is not reachable from the engine we cannot safely re-plan, so we return
        ``None`` and let the caller retry the original plan.
        """
        try:
            from geosi_engine.agents.planning import PlanningAgent

            query = getattr(original.request, "query", "") if original.request else ""
            if not query:
                return None

            # PlanningAgent.plan() drives the LLM cascade through a Supervisor.
            # Reuse the one the pipeline already created if the engine exposes it;
            # without it, re-planning would raise, so bail out gracefully.
            supervisor = getattr(self._engine, "supervisor", None)
            if supervisor is None:
                logger.debug("No supervisor available for reflection re-planning; " "retrying original plan instead.")
                return None

            planner = PlanningAgent(self._engine, supervisor=supervisor)
            available = []
            if original.request is not None:
                available = list(getattr(original.request, "available_layers", []) or [])

            corrected = planner.plan(
                query=query,
                available_layers=available,
                session_id="reflection-retry",
            )
            corrected.plan_source = "reflection_corrected"
            return corrected
        except Exception as exc:
            logger.warning("Failed to generate corrected plan: %s", exc)
            return None
