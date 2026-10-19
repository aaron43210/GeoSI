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
                    # Try conversational / code-gen answer before giving up
                    conv = self._conversational_answer(query, plan)
                    if conv is not None:
                        return conv
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

    # ── Conversational / code-gen fallback ───────────────────────────────

    # Queries that ask for code or scripts
    _CODE_RE = re.compile(
        r"\b(?:generate|write|create|show|give\s+me|make|example)\b.{0,50}"
        r"\b(?:code|script|snippet|example|template|function|class)\b",
        re.IGNORECASE,
    )
    # Greetings / help
    _GREET_RE = re.compile(
        r"^(?:hi|hello|hey|howdy|greetings?|help|what\s+can\s+you|who\s+are\s+you)",
        re.IGNORECASE,
    )
    # GIS knowledge questions
    _KNOWLEDGE_RE = re.compile(
        r"\b(?:what\s+is|what\s+are|how\s+(?:do\s+I|to|does)|explain|describe|define"
        r"|tell\s+me\s+about|difference\s+between|when\s+(?:to|should))\b",
        re.IGNORECASE,
    )

    _GREETING_REPLY = (
        "👋 Hi! I'm **GeoSI**, your autonomous geospatial assistant.\n\n"
        "I can help you:\n"
        "• **Analyse layers** — buffer, clip, dissolve, reproject, spatial join …\n"
        "• **Answer GIS questions** — CRS, NDVI, projections, file formats …\n"
        "• **Generate code** — GeoPandas, PyQGIS, GDAL, Rasterio snippets\n"
        "• **Remote sensing** — NDVI, NDWI, band math on your rasters\n\n"
        "Load a layer to run spatial operations, or just ask me anything!"
    )

    def _conversational_answer(
        self, query: str, plan: "ExecutionPlan"
    ) -> Optional["ExecutionResult"]:
        """
        Return a conversational ExecutionResult for non-spatial queries so the
        engine never blocks on "no layers loaded."

        Priority:
            1. Greetings / help  → canned reply (no LLM cost)
            2. Code-gen request  → LLM in chat mode (or a built-in template)
            3. GIS question      → LLM in chat mode (or a best-effort answer)

        Returns None when the query is clearly spatial and the empty-plan
        reasoning (e.g. "No layers loaded") should surface as-is.
        """
        from geosi_engine.models import ExecutionResult

        q = (query or "").strip()

        # 1. Greetings
        if self._GREET_RE.match(q):
            layers = self.engine.state.list_layers()
            footer = (
                f"\n\n📂 Loaded layers: {', '.join(layers)}"
                if layers else "\n\n📂 No layers loaded yet."
            )
            return ExecutionResult(success=True, answer=self._GREETING_REPLY + footer)

        is_code = bool(self._CODE_RE.search(q))
        is_knowledge = bool(self._KNOWLEDGE_RE.search(q))
        if not is_code and not is_knowledge:
            return None  # spatial query with no plan → keep existing error

        # 2 & 3. Try LLM in chat mode
        try:
            llm_answer = self._llm_chat(q)
            if llm_answer:
                return ExecutionResult(success=True, answer=llm_answer)
        except Exception as exc:
            logger.debug("Conversational LLM failed: %s", exc)

        # Offline fallback for common GIS concepts
        offline = self._offline_answer(q)
        if offline:
            return ExecutionResult(success=True, answer=offline)

        return None  # couldn't answer — let the original "no steps" path handle it

    def _llm_chat(self, query: str) -> Optional[str]:
        """Ask the configured LLM in conversational mode.  Returns None on failure."""
        agent = getattr(self.engine, "agent", None)
        if agent is None:
            return None

        system = (
            "You are GeoSI, an expert GIS assistant. Answer the user's question clearly "
            "and concisely. For code requests, wrap code in ```python ... ``` blocks. "
            "For educational questions, include practical examples."
        )
        prompt = f"{system}\n\nUser: {query}\nAssistant:"

        # 1. Hosted OpenAI-compatible API if configured
        if getattr(agent, "_api_configured", lambda: False)():
            try:
                resp = agent._api_chat(prompt, json_mode=False)
                if resp and resp.strip():
                    logger.debug("Conversational answer from hosted API")
                    return resp.strip()
            except Exception as exc:
                logger.debug("Conversational API chat failed: %s", exc)

        # 2. Ollama local model
        endpoint = getattr(agent, "_ollama_endpoint", "")
        model = getattr(agent, "_ollama_model", "")
        if endpoint and model:
            try:
                import requests
                resp = requests.post(
                    f"{endpoint}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.2},
                    },
                    timeout=30,
                )
                if resp.status_code == 200:
                    text = resp.json().get("response", "").strip()
                    if text:
                        logger.debug("Conversational answer from Ollama")
                        return text
            except Exception as exc:
                logger.debug("Conversational Ollama chat failed: %s", exc)

        return None

    # Common offline answers for frequently-asked GIS questions
    _OFFLINE_FACTS: list = [
        (re.compile(r"\bNDVI\b", re.I),
         "**NDVI (Normalized Difference Vegetation Index)**\n\n"
         "Formula: `(NIR − Red) / (NIR + Red)`\n\n"
         "Values range from −1 to +1. Values above 0.3 typically indicate healthy "
         "vegetation. Use NIR and Red bands from Sentinel-2 (B8, B4) or Landsat (B5, B4)."),
        (re.compile(r"\bCRS\b|\bcoordinate reference system\b", re.I),
         "**CRS (Coordinate Reference System)**\n\n"
         "Defines how spatial data relates to Earth's surface. Common CRS:\n"
         "• **EPSG:4326** — WGS84 geographic (lon/lat, degrees)\n"
         "• **EPSG:3857** — Web Mercator (meters, used by web maps)\n"
         "• **EPSG:32633** — UTM Zone 33N (good for central Europe, meters)\n\n"
         "Always reproject layers to the same CRS before running spatial operations."),
        (re.compile(r"\bshapefile\b|\bGeoPackage\b|\bGeoJSON\b", re.I),
         "**Common GIS formats:**\n\n"
         "• **Shapefile (.shp)** — legacy multi-file format, 2 GB limit, max 10-char field names\n"
         "• **GeoPackage (.gpkg)** — modern SQLite-based, single file, no size limit ✓\n"
         "• **GeoJSON (.geojson)** — JSON-based, human-readable, WGS84 by convention\n"
         "• **FlatGeobuf (.fgb)** — binary, streamable, very fast for large datasets\n\n"
         "Prefer GeoPackage for production workflows; GeoJSON for web sharing."),
        (re.compile(r"\b(?:geopandas|dataframe|gdf)\b", re.I),
         "```python\nimport geopandas as gpd\nimport pandas as pd\nfrom shapely.geometry import Point\n\n"
         "# Sample data with 5 points and attribute fields\n"
         "data = {\n"
         "    'id': [1, 2, 3, 4, 5],\n"
         "    'site_name': ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo'],\n"
         "    'elevation_m': [120.5, 230.1, 85.0, 310.4, 150.2],\n"
         "    'status': ['Active', 'Active', 'Inactive', 'Active', 'Pending'],\n"
         "    'longitude': [-122.4194, -122.4089, -122.4285, -122.4350, -122.4010],\n"
         "    'latitude':  [ 37.7749,   37.7833,   37.7650,   37.7900,   37.7700],\n"
         "}\n\n"
         "df = pd.DataFrame(data)\n"
         "geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]\n"
         "gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')\n\n"
         "print('Created GeoDataFrame:')\n"
         "print(gdf.head())\n\n"
         "# Optional: Export to GeoPackage or GeoJSON\n"
         "# gdf.to_file('sample_points.gpkg', layer='sample_points', driver='GPKG')\n```"),
    ]

    def _offline_answer(self, query: str) -> Optional[str]:
        """Return a canned answer for common GIS questions when the LLM is offline."""
        for pattern, answer in self._OFFLINE_FACTS:
            if pattern.search(query):
                return answer
        return None

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
