# -*- coding: utf-8 -*-
"""
GeoSI Agent Loop — plan → execute → verify → re-plan
═════════════════════════════════════════════════════

Turns the one-shot pipeline into an agent that checks its own work:

    for attempt in 1..max_attempts:
        plan     (rules for well-understood ops, otherwise the LLM;
                  later attempts always go to the LLM with feedback)
        execute  (ExecutionEngine.run)
        verify   (step errors, empty outputs, wrong kind of output)
        if ok → stop, else feed the problem back into the next plan

    question?  → read the result data back and let the LLM answer in words

When every attempt fails the result says so plainly instead of reporting a
partial run as success.

Verification is deliberately conservative and uses only facts about the
outputs (geometry type, feature count, layer type) so it works for any of
the hundreds of QGIS tools without per-tool rules.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import List, Optional

from geosi_engine.base import get_inspector
from geosi_engine.models import ExecutionPlan, ExecutionResult, Layer

logger = logging.getLogger("geosi_engine.agent_loop")

_QUESTION_RE = re.compile(
    r"^\s*(how many|how much|which|what|where|is there|are there|does|do|list|tell me|"
    r"show me (the )?(number|count|total))\b|\?\s*$",
    re.IGNORECASE,
)
# "find/select/extract/get <layer> ..." → the answer must be features of <layer>
_SUBJECT_RE = re.compile(
    r"\b(?:find|select|extract|get|keep|filter|identify|return)\s+(?:all\s+|the\s+|only\s+)?([a-z_][a-z0-9_]*)",
    re.IGNORECASE,
)
# Requests that would destroy data are never executed by the agent.
_DESTRUCTIVE_RE = re.compile(
    r"\b(delete|drop|remove|erase|wipe|truncate|overwrite)\b(?!\s+(duplicate|duplicates|null|empty|holes?))",
    re.IGNORECASE,
)
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
_NAMED_LAYER_RE = re.compile(r"\b(?:the\s+)?([a-z_][a-z0-9_]*)\s+layer\b", re.IGNORECASE)
_NOT_LAYER_WORDS = {"the", "a", "an", "this", "that", "new", "result", "output", "input", "each",
                    "every", "same", "previous", "vector", "raster", "point", "line", "polygon",
                    "one", "single", "another", "separate", "combined", "merged", "final", "temporary",
                    "my", "your", "base", "current", "active", "selected", "any", "all", "other", "first",
                    "second", "last", "target", "source", "reference", "mask", "empty", "two", "three"}
_EACH_RE = re.compile(r"\b(?:each|every|per)\s+([a-z_]+(?:\s[a-z_]+)?)", re.IGNORECASE)
_GEOM_FAMILY = {"point": "point", "multipoint": "point", "line": "line", "linestring": "line",
                "multilinestring": "line", "polygon": "polygon", "multipolygon": "polygon"}


def _geom_family(geometry_type: str) -> str:
    g = (geometry_type or "").lower().replace(" ", "")
    for key, fam in _GEOM_FAMILY.items():
        if g.startswith(key):
            return fam
    return g


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


class AgentLoop:
    """Drives parse → plan → execute → verify → re-plan for one query."""

    def __init__(self, engine, max_attempts: int = 3):
        self.engine = engine
        self.max_attempts = max_attempts
        self.last_plan: Optional[ExecutionPlan] = None
        # Set by the UI: should_stop() → True cancels before the next attempt;
        # on_progress(percent) reports progress.
        self.should_stop = lambda: False
        self.on_progress = None

    # ── public ────────────────────────────────────────────────────────

    def run(self, query: str) -> ExecutionResult:
        self.last_plan = ExecutionPlan()
        if _DESTRUCTIVE_RE.search(query):
            msg = ("⚠ GeoSI does not delete or overwrite data. If you meant to create a "
                   "filtered copy, ask e.g. \"extract hospitals where beds > 100\".")
            return ExecutionResult(success=False, answer=msg, reasoning=msg, error=msg)
        missing = self._missing_named_layer(query)
        if missing:
            loaded = ", ".join(self.engine.state.list_layers()) or "none"
            msg = f"⚠ There is no layer named '{missing}' in the project. Loaded layers: {loaded}."
            return ExecutionResult(success=False, answer=msg, reasoning=msg, error=msg)

        pieces = [p.strip() for p in _SPLIT_RE.split(query) if p and p.strip()]
        if len(pieces) > 1:
            return self._run_chain(pieces)
        return self._run_single(query)

    # ── multi-step requests ───────────────────────────────────────────

    def _run_chain(self, pieces: List[str]) -> ExecutionResult:
        """Run sub-tasks in order, each verified, feeding outputs forward."""
        prev: Optional[Layer] = None
        done: List[str] = []
        reasoning: List[str] = []
        result = ExecutionResult()
        for i, piece in enumerate(pieces, 1):
            if prev is not None:
                piece = self._bind_reference(piece, prev.name)
            logger.info(f"Sub-task {i}/{len(pieces)}: {piece}")
            result = self._run_single(piece)
            reasoning.append(f"── Sub-task {i}: {piece}\n{result.reasoning}")
            if not result.success:
                result.answer = (f"❌ Sub-task {i} of {len(pieces)} failed ('{piece}'). "
                                 f"{result.answer}")
                result.reasoning = "\n\n".join(reasoning)
                return result
            out = self._final_output(self.last_plan, result)
            if isinstance(out, Layer) and i < len(pieces):
                prev = self._register_intermediate(out)
            done.append(piece)
        result.reasoning = "\n\n".join(reasoning)
        if not _QUESTION_RE.search(pieces[-1]):
            result.answer = f"✅ Done in {len(pieces)} steps: " + " → ".join(done)
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

    def _missing_named_layer(self, query: str) -> Optional[str]:
        """'buffer the schools layer' when no 'schools' layer is loaded."""
        names = {n.lower() for n in self.engine.state.list_layers()}
        for m in _NAMED_LAYER_RE.finditer(query):
            word = m.group(1).lower()
            if word in _NOT_LAYER_WORDS:
                continue
            if word not in names and word.rstrip("s") not in names and word + "s" not in names:
                return word
        return None

    # ── one task: plan → execute → verify → re-plan ───────────────────

    def _run_single(self, query: str) -> ExecutionResult:
        agent = self.engine.agent
        state = self.engine.state
        request = agent.parse(query, state)
        self.last_plan = ExecutionPlan(request=request)
        report = LoopReport()
        feedback: Optional[str] = None

        for attempt_no in range(1, self.max_attempts + 1):
            if self.should_stop():
                break
            self._progress(100.0 * (attempt_no - 1) / self.max_attempts + 5)
            plan = agent.plan(request, state, feedback=feedback)
            if not plan.steps:
                if attempt_no == 1 or not report.attempts:
                    # Nothing runnable (unknown layer, refused, no planner):
                    # surface the planner's explanation as-is.
                    return self.engine.executor.run(plan)
                break  # re-planning produced nothing; keep earlier attempts

            self.last_plan = plan
            result = self.engine.executor.run(plan)
            problem = self.verify(query, plan, result)
            report.attempts.append(Attempt(plan, result, problem))
            if problem is None:
                break
            logger.info(f"Attempt {attempt_no} rejected: {problem}")
            if not agent.can_replan():
                break
            feedback = self._feedback(plan, problem)

        if not report.attempts:
            msg = "⏹ Stopped before anything ran."
            return ExecutionResult(success=False, answer=msg, error=msg)
        self._progress(95)
        final = report.attempts[-1]
        result = final.result
        if len(report.attempts) > 1:
            result.reasoning = f"{report.summary()}\n\n{result.reasoning}"

        if final.problem is not None:
            result.success = False
            result.error = final.problem
            result.answer = (
                f"❌ I could not complete this reliably after {len(report.attempts)} "
                f"attempt(s). Last problem: {final.problem}"
            )
            # Don't hand wrong layers to the user as an answer
            result.results = {}
            return result

        if re.match(r"\s*how many\b", query, re.I):
            out = self._final_output(final.plan, result)
            if isinstance(out, Layer) and _geom_family(out.geometry_type) in ("point", "line", "polygon"):
                # Counting is exact from the layer; small models miscount rows.
                result.answer = (f"{out.feature_count} — the result layer '{out.name}' has "
                                 f"{out.feature_count} matching feature(s).")
                return result
        if _QUESTION_RE.search(query):
            answer = self._answer_question(query, result)
            if answer:
                result.answer = answer
        return result

    def _progress(self, pct: float) -> None:
        if self.on_progress is not None:
            try:
                self.on_progress(pct)
            except Exception:
                pass

    # ── verification ──────────────────────────────────────────────────

    def verify(self, query: str, plan: ExecutionPlan, result: ExecutionResult) -> Optional[str]:
        """Return a description of what is wrong with the result, or None."""
        failed = [log for log in result.logs if log.status.value != "success"]
        if failed:
            log = failed[0]
            return f"step {log.step_id} ({log.tool_name}) failed: {log.error_message}"

        final = self._final_output(plan, result)
        if not isinstance(final, Layer) and not _QUESTION_RE.search(query):
            return ("no result layer was produced — this request needs a processing tool "
                    "that outputs a new layer")
        if isinstance(final, Layer):
            if final.layer_type == "vector" and final.feature_count == 0:
                return (f"the final output '{final.name}' has 0 features — the inputs may be "
                        f"swapped, the wrong tool was used, or the distance/units are wrong")
            each = self._each_layer(query)
            # One output feature per input feature is only expected when the
            # output keeps the input's geometry type ("count X in each zone" →
            # zones); "5 random points in each zone" or "buffer each point"
            # legitimately produce a different number or type.
            same_family = each is not None and _geom_family(final.geometry_type) == each[2]
            if each and same_family and final.feature_count != each[1]:
                return (f"the request is about each feature of '{each[0]}' ({each[1]} features) but "
                        f"the output has {final.feature_count} — the result should keep one feature per "
                        f"'{each[0]}' feature (e.g. use '{each[0]}' as the INPUT/POLYGONS layer, keep "
                        f"non-matching features)")
            expected = self._expected_geometry(query)
            if expected and final.layer_type == "vector":
                got = _geom_family(final.geometry_type)
                if got and got != expected[1]:
                    return (f"the question asks for {expected[0]} ({expected[1]} features) but the "
                            f"final output has {got} features — use '{expected[0]}' as the INPUT "
                            f"layer and the other layer as the comparison/intersect layer")
        return None

    def _final_output(self, plan: ExecutionPlan, result: ExecutionResult):
        if not plan.steps:
            return None
        return (result.results or {}).get(plan.steps[-1].output_name)

    def _each_layer(self, query: str):
        """("flood_zones", 2, "polygon") for "... in each flood_zones polygon"."""
        state = self.engine.state
        for m in _EACH_RE.finditer(query):
            words = m.group(1).lower().split()
            for name in state.list_layers():
                n = name.lower()
                cands = {n, n.rstrip("s"), n.replace("_", " "), n.replace("_", " ").rstrip("s")}
                if words[0] in cands or " ".join(words) in cands:
                    layer = state.get_layer(name)
                    if getattr(layer, "layer_type", "") == "vector" and layer.feature_count:
                        return name, layer.feature_count, _geom_family(layer.geometry_type)
        return None

    def _expected_geometry(self, query: str):
        """("hospitals", "point") when the query asks to find features of a layer."""
        state = self.engine.state
        for m in _SUBJECT_RE.finditer(query):
            word = m.group(1).lower()
            for name in state.list_layers():
                if name.lower() in (word, word.rstrip("s"), word + "s"):
                    layer = state.get_layer(name)
                    fam = _geom_family(getattr(layer, "geometry_type", ""))
                    if fam in ("point", "line", "polygon"):
                        return name, fam
        return None

    @staticmethod
    def _feedback(plan: ExecutionPlan, problem: str) -> str:
        steps = "; ".join(
            f"{s.step_id}: {s.tool_name} {s.parameters}" for s in plan.steps
        )
        return f"Previous plan: {steps}\nProblem: {problem}"

    # ── question answering ────────────────────────────────────────────

    def _answer_question(self, query: str, result: ExecutionResult) -> Optional[str]:
        inspector = get_inspector()
        evidence = []
        for name, out in (result.results or {}).items():
            if isinstance(out, Layer) and inspector is not None:
                try:
                    evidence.append(inspector(out, 40))
                except Exception as e:
                    logger.debug(f"inspect {name} failed: {e}")
            elif isinstance(out, dict):
                evidence.append(f"{name}: {out}")
            elif out is not None:
                evidence.append(f"{name}: {out}")
        if result.answer:
            evidence.append(f"tool message: {result.answer}")
        if not evidence:
            return None
        return self.engine.agent.answer_from_evidence(query, "\n".join(evidence))
