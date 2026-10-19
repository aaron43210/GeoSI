# -*- coding: utf-8 -*-
"""
GeoSI Agent Loop — the supervised pipeline for one request
═══════════════════════════════════════════════════════════

Every surface (QGIS plugin, REST API, MCP) reaches this loop through the
SupervisorAgent. Each phase is done by one agent of the session's team
(``geosi_engine.agents.team``):

    screen      Permission & Safety refuses destructive or injected requests;
                Validation reports layers the request names but that aren't loaded
    split       "A and then B" → sub-tasks, each run through the loop below,
                outputs fed forward
    for attempt in 1..max_attempts:
        plan        Planning (rules → deterministic → templates → LLM with feedback)
        critique    Reflection critic; unknown tools → re-plan without executing
        validate    Validation (tools, layers, fields, expressions) → re-plan on errors
        optimize    Workflow Optimization suggestions (advisory)
        execute     GIS Agent runs each step through the permission gate;
                    a step that needs approval pauses the run (resume later)
        verify      Verification checks the result against the request
        reflect     Reflection turns the problem into feedback for the next plan
    answer      Report Generation answers questions from result data and
                writes the execution report

When every attempt fails the result says so plainly instead of reporting a
partial run as success, and no wrong layers are returned.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from geosi_engine.agents.verification import QUESTION_RE
from geosi_engine.models import ExecutionPlan, ExecutionResult, Layer

logger = logging.getLogger("geosi_engine.agent_loop")

# Split "A and then B" into sub-tasks only where the next part starts with an
# action verb ("... band 3 as red and band 4 as NIR" must stay whole).
_VERBS = (
    "buffer|clip|dissolve|intersect|reproject|select|extract|find|count|add|calculate|compute|"
    "merge|join|create|make|convert|simplify|smooth|fix|generate|filter|keep|sum|export|save|"
    "centroid|union|difference|densify|explode|rasterize|polygonize|aggregate"
)
_SPLIT_RE = re.compile(
    rf",?\s+(?:and then|then|after that|and|,)\s+(?=(?:{_VERBS})\b)", re.IGNORECASE
)
# References to the previous step's output inside a later sub-task
_REF_RE = re.compile(
    r"\b(the (?:result|output|outputs|new layer|previous layer|buffer(?:ed)?(?: layer| zones?| areas?| polygons?)?)"
    r"|them|it|those|these)\b",
    re.IGNORECASE,
)
_THEIR_RE = re.compile(r"\btheir\b", re.IGNORECASE)


@dataclass
class Attempt:
    plan: ExecutionPlan
    result: ExecutionResult
    problem: Optional[str] = None


@dataclass
class LoopReport:
    attempts: List[Attempt] = field(default_factory=list)

    def summary(self) -> str:
        lines = []
        for i, a in enumerate(self.attempts, 1):
            tools = " → ".join(s.tool_name for s in a.plan.steps) or "(no steps)"
            lines.append(f"Attempt {i}: {tools} — " + ("ok" if a.problem is None else a.problem))
        return "\n".join(lines)


@dataclass
class PausedRun:
    """Where a run stopped for approval, so it can continue exactly there."""
    query: str
    request: Any
    plan: ExecutionPlan
    attempt_no: int
    report: LoopReport
    # Multi-step request context
    pieces: List[str] = field(default_factory=list)
    piece_index: int = 0
    done: List[str] = field(default_factory=list)
    reasoning: List[str] = field(default_factory=list)


class AgentLoop:
    """Drives one request through the agent team (see module docstring)."""

    def __init__(self, engine, max_attempts: int = 3):
        self.engine = engine
        self.max_attempts = max_attempts
        self.last_plan: Optional[ExecutionPlan] = None
        self.paused: Dict[str, PausedRun] = {}
        self._team = None
        self._supervisor = None
        # Set by the UI: should_stop() → True cancels before the next attempt;
        # on_progress(percent) reports progress.
        self.should_stop = lambda: False
        self.on_progress = None

    # ── team ──────────────────────────────────────────────────────────

    @property
    def team(self):
        if self._team is None:
            from geosi_engine.agents.team import AgentTeam

            self._team = AgentTeam(self.engine, supervisor=self._supervisor)
        return self._team

    def attach_supervisor(self, supervisor) -> None:
        self._supervisor = supervisor
        if self._team is not None:
            self._team.attach_supervisor(supervisor)

    # ── public ────────────────────────────────────────────────────────

    def run(self, query: str) -> ExecutionResult:
        self.last_plan = ExecutionPlan()
        refusal = self.team.permission.screen_request(query)
        if refusal is None:
            missing = self.team.validation.check_request(query, self.engine.state)
            refusal = f"⚠ {missing}" if missing else None
        if refusal:
            return ExecutionResult(success=False, answer=refusal, reasoning=refusal, error=refusal)

        pieces = [p.strip() for p in _SPLIT_RE.split(query) if p and p.strip()]
        if len(pieces) > 1:
            return self._run_chain(query, pieces)
        return self._run_single(query)

    def resume(self, action_id: str, approved: bool) -> ExecutionResult:
        """Continue a run paused at *action_id* (after the approval was resolved)."""
        paused = self.paused.pop(action_id, None)
        if paused is None:
            msg = f"No paused request for action {action_id!r} in this session."
            return ExecutionResult(success=False, answer=msg, error=msg)
        if not approved:
            msg = "✋ The step was rejected, so it was not run and nothing was changed."
            return ExecutionResult(success=False, answer=msg, error="rejected by user", denied=True)

        result = self._run_single(paused.query, request=paused.request, resume_plan=paused.plan,
                                  start_attempt=paused.attempt_no, report=paused.report)
        if paused.pieces and result.approval_pending is None:
            if not result.success:
                return self._chain_failed(paused.pieces, paused.piece_index, paused.reasoning, result)
            out = self._final_output(self.last_plan, result)
            paused.done.append(paused.pieces[paused.piece_index])
            paused.reasoning.append(f"── Sub-task {paused.piece_index + 1}: {paused.query}\n{result.reasoning}")
            prev = self._register_intermediate(out) if isinstance(out, Layer) else None
            return self._run_chain(paused.query, paused.pieces, start=paused.piece_index + 1, prev=prev,
                                   done=paused.done, reasoning=paused.reasoning, last=result)
        return result

    # ── multi-step requests ───────────────────────────────────────────

    def _run_chain(self, query: str, pieces: List[str], start: int = 0, prev: Optional[Layer] = None,
                   done: Optional[List[str]] = None, reasoning: Optional[List[str]] = None,
                   last: Optional[ExecutionResult] = None) -> ExecutionResult:
        """Run sub-tasks in order, each verified, feeding outputs forward."""
        done = done if done is not None else []
        reasoning = reasoning if reasoning is not None else []
        result = last or ExecutionResult()
        for i in range(start, len(pieces)):
            piece = pieces[i]
            if prev is not None:
                piece = self._bind_reference(piece, prev.name)
            logger.info(f"Sub-task {i + 1}/{len(pieces)}: {piece}")
            result = self._run_single(piece)
            if result.approval_pending:
                paused = self.paused.get(result.approval_pending)
                if paused is not None:
                    paused.pieces, paused.piece_index = pieces, i
                    paused.done, paused.reasoning = done, reasoning
                result.answer = f"⏸ Sub-task {i + 1} of {len(pieces)} ('{piece}') needs approval. {result.answer}"
                return result
            reasoning.append(f"── Sub-task {i + 1}: {piece}\n{result.reasoning}")
            if not result.success:
                return self._chain_failed(pieces, i, reasoning, result, piece)
            out = self._final_output(self.last_plan, result)
            if isinstance(out, Layer) and i < len(pieces) - 1:
                prev = self._register_intermediate(out)
            done.append(piece)
        result.reasoning = "\n\n".join(reasoning)
        if not QUESTION_RE.search(pieces[-1]):
            result.answer = f"✅ Done in {len(pieces)} steps: " + " → ".join(done)
        return result

    @staticmethod
    def _chain_failed(pieces, i, reasoning, result, piece=None) -> ExecutionResult:
        piece = piece or pieces[i]
        result.answer = f"❌ Sub-task {i + 1} of {len(pieces)} failed ('{piece}'). {result.answer}"
        result.reasoning = "\n\n".join(reasoning)
        return result

    def _register_intermediate(self, layer: Layer) -> Layer:
        """Make a sub-task's output addressable by name for the next sub-task."""
        state = self.engine.state
        if state.get_layer(layer.name) is layer:
            return layer  # the executor already registered this exact output
        base, n, name = layer.name, 2, layer.name
        while state.get_layer(name) is not None:
            name, n = f"{base}_{n}", n + 1
        layer.name = name
        state.add_layer(layer)
        return layer

    def _bind_reference(self, piece: str, layer_name: str) -> str:
        if _REF_RE.search(piece):
            return _REF_RE.sub(layer_name, piece, count=1)
        if _THEIR_RE.search(piece):
            return _THEIR_RE.sub(layer_name, piece, count=1)
        if any(n.lower() in piece.lower() for n in self.engine.state.list_layers()):
            return piece
        joiner = "to" if piece.lower().startswith(("add", "join", "attach")) else "of"
        return f"{piece} {joiner} {layer_name}"

    # ── one task: plan → check → execute → verify → re-plan ───────────

    def _run_single(self, query: str, request: Any = None, resume_plan: Optional[ExecutionPlan] = None,
                    start_attempt: int = 1, report: Optional[LoopReport] = None) -> ExecutionResult:
        team = self.team
        state = self.engine.state
        request = request if request is not None else self.engine.agent.parse(query, state)
        self.last_plan = ExecutionPlan(request=request)
        report = report or LoopReport()
        feedback: Optional[str] = None
        suggestions: List[str] = []

        for attempt_no in range(start_attempt, self.max_attempts + 1):
            if self.should_stop():
                break
            self._progress(100.0 * (attempt_no - 1) / self.max_attempts + 5)

            if resume_plan is not None:
                plan, resume_plan = resume_plan, None
            else:
                plan = self._plan(query, feedback)
            if not plan.steps:
                if not report.attempts:
                    # Nothing runnable (refused, no planner): surface the explanation
                    return self.engine.executor.run(plan)
                break  # re-planning produced nothing; keep earlier attempts
            self.last_plan = plan

            problem = self._check_plan(plan)
            if problem is None:
                suggestions = self._suggestions(plan)
                result = self.engine.executor.run(plan, step_runner=team.gis.execute_step)
                if result.approval_pending:
                    self.paused[result.approval_pending] = PausedRun(
                        query=query, request=request, plan=plan, attempt_no=attempt_no, report=report)
                    return result
                if result.denied:
                    return result  # policy refusals are final, never re-planned around
                verdict = team.verification.verify(query, plan, result, state)
                problem = None if verdict.passed else verdict.issues[0]
                if verdict.passed:
                    result.warnings.extend(f.message for f in verdict.warnings())
            else:
                result = ExecutionResult(success=False, answer=problem, error=problem,
                                         plan_source=plan.plan_source)

            report.attempts.append(Attempt(plan, result, problem))
            if problem is None:
                break
            logger.info(f"Attempt {attempt_no} rejected: {problem}")
            if not self.engine.agent.can_replan():
                break
            feedback = team.reflection.feedback_for(plan, problem)

        if not report.attempts:
            msg = "⏹ Stopped before anything ran."
            return ExecutionResult(success=False, answer=msg, error=msg)
        self._progress(95)
        final = report.attempts[-1]
        result = final.result
        result.plan_source = final.plan.plan_source
        if len(report.attempts) > 1:
            result.reasoning = f"{report.summary()}\n\n{result.reasoning}"
        result.warnings.extend(s for s in suggestions if s not in result.warnings)

        if final.problem is not None:
            result.success = False
            result.error = final.problem
            result.answer = (
                f"❌ I could not complete this reliably after {len(report.attempts)} "
                f"attempt(s). Last problem: {final.problem}"
            )
            result.results = {}  # don't hand wrong layers to the user as an answer
        elif QUESTION_RE.search(query):
            answer = team.reporter.answer(query, final.plan, result)
            if answer:
                result.answer = answer
        result.report = team.reporter.render_summary(final.plan, result,
                                                     getattr(self.engine, "_session_id", ""))
        return result

    def _plan(self, query: str, feedback: Optional[str]) -> ExecutionPlan:
        layers = self.engine.state.list_layers()
        sid = getattr(self.engine, "_session_id", "")
        if feedback:
            return self.team.planning.plan(query=query, available_layers=layers, session_id=sid,
                                           feedback=feedback)
        return self.team.planning.plan(query=query, available_layers=layers, session_id=sid)

    def _check_plan(self, plan: ExecutionPlan) -> Optional[str]:
        """Reflection critic + Validation before anything runs."""
        critic = self.team.reflection.critic(plan)
        if not critic.ok:
            return "; ".join(f"{f.tool_name}: {f.message}" for f in critic.errors())
        report = self.team.validation.validate(plan, self.engine.state)
        if not report.ok:
            return "; ".join(i.message for i in report.errors())
        return None

    def _suggestions(self, plan: ExecutionPlan) -> List[str]:
        """Workflow Optimization (advisory, never blocks)."""
        try:
            opt = self.team.optimizer.analyze(plan)
            return [s.message for s in opt.suggestions]
        except Exception as exc:  # pragma: no cover - advisory only
            logger.debug(f"Workflow optimization skipped: {exc}")
            return []

    def _progress(self, pct: float) -> None:
        if self.on_progress is not None:
            try:
                self.on_progress(pct)
            except Exception:
                pass

    @staticmethod
    def _final_output(plan: ExecutionPlan, result: ExecutionResult):
        if not plan.steps:
            return None
        return (result.results or {}).get(plan.steps[-1].output_name)
