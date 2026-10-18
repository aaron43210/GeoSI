# -*- coding: utf-8 -*-
"""
GeoSI v2 — Domain Agents as Registered Tools (PRD "any GIS task")
════════════════════════════════════════════════════════════════════
Exposes the specialist domain agents (Code Generation, Report, Research,
Remote Sensing, Machine Learning, Geology) as first-class entries in the
``ToolRegistry`` so the single Supervisor plan→validate→permission→execute
loop can select and dispatch them like any other tool.

Design (preserves the Golden Rule — one pipeline, no second routing brain):
  * Each domain tool is a ``ToolSpec`` the Planning Agent can see and ground
    on, and the Validation Agent can resolve.
  * Execution is dispatched by the GIS Agent via ``dispatch_domain_tool()``
    using the FULL ``ToolStep`` (so ``input_layers`` / ``description`` /
    ``session_id`` are preserved — the generic executor would drop them).
  * The GIS Agent's permission gate is the single production HITL path; the
    domain agents' own internal gate is defense-in-depth (it returns the same
    decision, so no double prompt on the async surfaces).

Contract 1 (inviolable): ``generate_code`` returns review-only code. It is
NEVER executed — ``CodeGenerationAgent`` forces ``requires_human_review=True``.
"""
from __future__ import annotations

import logging
from typing import Any, Optional

from geosi_engine.base import GISTool
from geosi_engine.models import ToolParameter, ToolResult, ToolSpec, ToolStep

logger = logging.getLogger("geosi_engine.tools.domain_tools")

# Canonical domain-tool → risk level.  Imported by the Planning Agent so risk
# classification never misreads a mutating domain op as read_only.
DOMAIN_TOOL_RISK: dict[str, str] = {
    "generate_code": "read_only",
    "generate_report": "read_only",
    "research": "read_only",
    "remote_sensing": "mutating",
    "machine_learning": "mutating",
    "geology": "mutating",
}

DOMAIN_TOOL_NAMES = frozenset(DOMAIN_TOOL_RISK)


def is_domain_tool(name: str) -> bool:
    """True if *name* resolves to a registered domain tool."""
    return name.lower() in DOMAIN_TOOL_NAMES


# ── Tool specifications ────────────────────────────────────────────────────
# One ToolSpec per domain tool. Parameters mirror each agent's request
# dataclass so the Planning Agent can ground on them and the Validation Agent
# can resolve them. ``requires_qgis=False`` — domain agents run on the engine
# core (GeoPandas / Rasterio / scikit-learn), not the QGIS Processing backend.


def _p(name: str, ptype: str, required: bool = False,
       desc: str = "", example: Optional[str] = None) -> ToolParameter:
    return ToolParameter(name=name, param_type=ptype, required=required,
                         description=desc, example=example)


_DOMAIN_SPECS: dict[str, ToolSpec] = {
    "generate_code": ToolSpec(
        name="generate_code",
        display_name="Generate Code",
        description=(
            "Generate a reproducible Python / PyQGIS / GeoPandas / Rasterio "
            "script for the task. REVIEW-ONLY: the generated code is NEVER "
            "executed automatically. Use this when NO existing tool fits the "
            "request so the user can still accomplish any GIS task end-to-end."
        ),
        category="codegen",
        parameters=[
            _p("target_language", "string", False,
               "One of: pyqgis | geopandas | rasterio | auto", "auto"),
            _p("query", "string", False,
               "Natural-language description of what the code should do "
               "(defaults to the step description)."),
        ],
        outputs=["code"],
        tags=["code", "script", "python", "pyqgis", "geopandas", "rasterio",
              "custom", "fallback", "any-task"],
        requires_qgis=False,
    ),
    "generate_report": ToolSpec(
        name="generate_report",
        display_name="Generate Report",
        description=(
            "Produce a report (execution summary, methodology, workflow graph, "
            "statistics, or full PDF) from execution results. Non-destructive "
            "to source data."
        ),
        category="report",
        parameters=[
            _p("report_type", "string", False,
               "execution_summary | methodology | workflow_graph | statistics | full_pdf",
               "execution_summary"),
            _p("output_path", "string", False,
               "Optional path to write the report artefact to."),
        ],
        outputs=["report"],
        tags=["report", "summary", "methodology", "pdf", "statistics", "document"],
        requires_qgis=False,
    ),
    "research": ToolSpec(
        name="research",
        display_name="Research / Literature Retrieval",
        description=(
            "Retrieve research papers and documentation from the knowledge base, "
            "summarise findings, and generate citations. Read-only RAG retrieval."
        ),
        category="research",
        parameters=[
            _p("query", "string", True,
               "The research question or topic to retrieve literature for."),
            _p("max_results", "number", False, "Maximum number of sources.", "10"),
            _p("collections", "list", False,
               "Qdrant collections to search (e.g. research_papers, gis_docs)."),
        ],
        outputs=["papers"],
        tags=["research", "literature", "papers", "citation", "rag", "search"],
        requires_qgis=False,
    ),
    "remote_sensing": ToolSpec(
        name="remote_sensing",
        display_name="Remote Sensing",
        description=(
            "Satellite / raster remote-sensing operations: spectral indices "
            "(NDVI, NDWI, SAVI, EVI, NDBI, NDSI, NBR), atmospheric correction, "
            "change detection, band composites. Writes raster outputs (mutating)."
        ),
        category="remote_sensing",
        parameters=[
            _p("operation", "string", True,
               "spectral_index | atmospheric_correction | change_detection | band_composite"),
            _p("sensor", "string", True,
               "Sentinel-2 | Landsat-8 | MODIS | SAR | ...", "Sentinel-2"),
        ],
        outputs=["output_layer"],
        tags=["remote sensing", "satellite", "ndvi", "raster", "sentinel",
              "landsat", "spectral", "change detection"],
        requires_qgis=False,
    ),
    "machine_learning": ToolSpec(
        name="machine_learning",
        display_name="Machine Learning",
        description=(
            "Spatial machine learning: classification, regression, clustering, "
            "forecasting, prediction. Trains / applies models (random_forest, "
            "gradient_boosting, kmeans, lstm, ...). Writes model artefacts (mutating)."
        ),
        category="machine_learning",
        parameters=[
            _p("job_type", "string", True,
               "classification | regression | clustering | forecasting | predict"),
            _p("algorithm", "string", True,
               "random_forest | gradient_boosting | kmeans | lstm | ...",
               "random_forest"),
            _p("target_column", "string", False, "Target/label column name."),
            _p("feature_columns", "list", False, "Feature column names."),
        ],
        outputs=["model"],
        tags=["machine learning", "ml", "classification", "regression",
              "clustering", "random forest", "predict", "ai"],
        requires_qgis=False,
    ),
    "geology": ToolSpec(
        name="geology",
        display_name="Geology",
        description=(
            "Geological analysis: geological mapping, structural analysis, "
            "stratigraphic modeling, cross-sections, fault / fold analysis, "
            "borehole correlation, mineral prospectivity, landslide "
            "susceptibility, AI geological interpretation. Writes outputs (mutating)."
        ),
        category="geology",
        parameters=[
            _p("operation", "string", True,
               "geological_mapping | structural_analysis | stratigraphic_modeling | "
               "cross_section | fault_visualization | fold_analysis | "
               "borehole_correlation | mineral_prospectivity | "
               "landslide_susceptibility | ai_interpretation"),
            _p("query", "string", False,
               "Natural-language context (for ai_interpretation)."),
        ],
        outputs=["output_layer"],
        tags=["geology", "geological", "stratigraphy", "fault", "fold",
              "mineral", "landslide", "borehole", "cross section"],
        requires_qgis=False,
    ),
}


# ── Dispatch & registration ─────────────────────────────────────────────────


def _session_id(engine: Any) -> str:
    """Session id as the pool stamps it onto the engine (GISAgent convention)."""
    return getattr(engine, "_session_id", "") or ""


def _permission_for(engine: Any, permission_agent: Optional[Any]) -> Any:
    """Reuse the caller's PermissionSafetyAgent, or build one for the session."""
    if permission_agent is not None:
        return permission_agent
    from geosi_engine.agents.permission_safety import PermissionSafetyAgent
    return PermissionSafetyAgent(engine)


def dispatch_domain_tool(
    engine: Any,
    step: ToolStep,
    permission_agent: Optional[Any] = None,
) -> ToolResult:
    """
    Dispatch a domain ``ToolStep`` to its specialist agent, preserving the
    FULL step context (``input_layers`` / ``description`` / ``parameters`` /
    ``session_id``) that the generic registry executor would drop.

    The GIS Agent's permission gate has already run for mutating domain tools
    before this is reached; each domain agent re-checks as defense-in-depth
    (returning the same ``allow`` decision — no second prompt on the async path).

    Returns a ``ToolResult`` mapping each agent's native result type.
    """
    name = (step.tool_name or "").lower()
    params = dict(step.parameters or {})
    sid = _session_id(engine)
    layers = list(step.input_layers or []) or list(params.get("input_layers", []))
    query = step.description or params.get("query", "")
    perm = None  # built lazily only for agents that need it

    # ── generate_code (read-only; Contract 1: NEVER executed) ──────────────
    if name == "generate_code":
        from geosi_engine.agents.code_generation import CodeGenerationAgent, CodeRequest
        req = CodeRequest(
            target_language=params.get("target_language", "auto"),
            plan=params.get("plan"),
            query=query,
            context_layers=layers,
            session_id=sid,
            parameters=params,
        )
        gc = CodeGenerationAgent(engine).generate(req)
        return ToolResult(
            success=gc.success,
            output={
                "code": gc.code,
                "filename": gc.filename,
                "language": gc.target_language,
                "requires_human_review": gc.requires_human_review,  # always True
                "warnings": gc.warnings,
                "plan_id": gc.plan_id,
            },
            message=(
                f"Generated {gc.target_language} code for human review "
                "(NOT executed — review before running)."
                if gc.success else "Code generation failed."
            ),
            error=gc.error,
        )

    # ── generate_report (read-only) ────────────────────────────────────────
    if name == "generate_report":
        from geosi_engine.agents.report_generation import ReportGenerationAgent, ReportRequest
        req = ReportRequest(
            report_type=params.get("report_type", "execution_summary"),
            execution_result=params.get("execution_result"),
            plan=params.get("plan"),
            audit_log_id=params.get("audit_log_id"),
            session_id=sid,
            output_path=params.get("output_path"),
            parameters=params,
        )
        rr = ReportGenerationAgent(engine).generate(req)
        return ToolResult(
            success=rr.success,
            output={
                "report_type": rr.report_type,
                "content": rr.content,
                "output_path": rr.output_path,
                "statistics": rr.statistics,
                "audit_log_id": rr.audit_log_id,
            },
            message=rr.content or f"Report '{rr.report_type}' generated.",
            error=rr.error,
        )

    # ── research (read-only RAG) ───────────────────────────────────────────
    if name == "research":
        from geosi_engine.agents.research import ResearchAgent, ResearchQuery
        perm = _permission_for(engine, permission_agent)
        req = ResearchQuery(
            query=query,
            topics=params.get("topics", []),
            max_results=int(params.get("max_results", 10)),
            collections=params.get("collections", ["research_papers", "gis_docs"]),
            session_id=sid,
            include_citations=bool(params.get("include_citations", True)),
        )
        rres = ResearchAgent(engine, perm).search(req)
        return ToolResult(
            success=rres.success,
            output={
                "papers": rres.papers,
                "summary": rres.summary,
                "citations": rres.citations,
                "total_sources": rres.total_sources,
                "guardrail_flags": rres.guardrail_flags,
            },
            message=rres.summary or f"Found {rres.total_sources} source(s).",
            error=rres.error,
        )

    # ── remote_sensing (mutating) ─────────────────────────────────────────
    if name == "remote_sensing":
        from geosi_engine.agents.remote_sensing import RasterJobRequest, RemoteSensingAgent
        perm = _permission_for(engine, permission_agent)
        job = RasterJobRequest(
            operation=params.get("operation", ""),
            sensor=params.get("sensor", ""),
            input_layers=layers,
            parameters=params,
            session_id=sid,
            risk_level=step.risk_level or "mutating",
        )
        jr = RemoteSensingAgent(engine, perm).execute(job)
        return ToolResult(
            success=jr.success,
            output={
                "output_layer": jr.output_layer,
                "statistics": jr.statistics,
                "validation_passed": jr.validation_passed,
                "warnings": jr.warnings,
            },
            message=(
                f"Remote sensing '{jr.operation}' → {jr.output_layer}"
                if jr.success else f"Remote sensing '{jr.operation}' failed."
            ),
            error=jr.error,
        )

    # ── machine_learning (mutating) ───────────────────────────────────────
    if name == "machine_learning":
        from geosi_engine.agents.machine_learning import MachineLearningAgent, MLJobRequest
        perm = _permission_for(engine, permission_agent)
        job = MLJobRequest(
            job_type=params.get("job_type", ""),
            algorithm=params.get("algorithm", ""),
            input_layers=layers,
            feature_columns=params.get("feature_columns", []),
            target_column=params.get("target_column"),
            parameters=params,
            model_path=params.get("model_path"),
            output_path=params.get("output_path"),
            session_id=sid,
        )
        mr = MachineLearningAgent(engine, perm).execute(job)
        return ToolResult(
            success=mr.success,
            output={
                "job_type": mr.job_type,
                "algorithm": mr.algorithm,
                "metrics": mr.metrics,
                "output_path": mr.output_path,
                "eval_run_id": mr.eval_run_id,
            },
            message=(
                f"ML {mr.job_type} ({mr.algorithm}) complete → {mr.output_path}"
                if mr.success else f"ML {mr.job_type} failed."
            ),
            error=mr.error,
        )

    # ── geology (mutating) ─────────────────────────────────────────────────
    if name == "geology":
        from geosi_engine.agents.geology import GeologyAgent, GeologyJobRequest
        perm = _permission_for(engine, permission_agent)
        job = GeologyJobRequest(
            operation=params.get("operation", ""),
            input_layers=layers,
            parameters=params,
            query=query,
            session_id=sid,
            risk_level=step.risk_level or "mutating",
        )
        gr = GeologyAgent(engine, perm).execute(job)
        return ToolResult(
            success=gr.success,
            output={
                "output_layer": gr.output_layer,
                "interpretation": gr.interpretation,
                "statistics": gr.statistics,
                "rag_sources": gr.rag_sources,
                "guardrail_flags": gr.guardrail_flags,
            },
            message=gr.interpretation or (
                f"Geology '{gr.operation}' complete."
                if gr.success else f"Geology '{gr.operation}' failed."
            ),
            error=gr.error,
        )

    return ToolResult(
        success=False,
        error=f"'{step.tool_name}' is not a registered domain tool.",
        message=f"Unknown domain tool: {step.tool_name}",
    )


# ── GISTool wrapper (so the registry can resolve & list domain tools) ───────


class DomainTool(GISTool):
    """
    A registry-visible ``GISTool`` that fronts one domain agent.

    Holds the engine, so it is NOT no-arg auto-instantiated by
    ``ToolRegistry.discover_portable_tools`` (which would ``DomainTool()`` and
    skip on the resulting ``TypeError``) — domain tools are registered
    explicitly via ``discover_domain_tools(engine, registry)``.

    ``execute`` rebuilds a ``ToolStep`` from kwargs and defers to
    ``dispatch_domain_tool`` so the direct-registry path and the GIS Agent's
    full-context path share one implementation.
    """

    def __init__(self, engine: Any, spec: ToolSpec,
                 permission_agent: Optional[Any] = None) -> None:
        self._engine = engine
        self._spec_obj = spec
        self._permission = permission_agent

    def spec(self) -> ToolSpec:
        return self._spec_obj

    def execute(self, **kwargs) -> ToolResult:
        step = ToolStep(
            tool_name=self._spec_obj.name,
            parameters=dict(kwargs),
            input_layers=list(kwargs.get("input_layers", []) or []),
            description=str(kwargs.get("query", "") or ""),
            risk_level=DOMAIN_TOOL_RISK.get(self._spec_obj.name, "read_only"),
        )
        return dispatch_domain_tool(self._engine, step, self._permission)


def discover_domain_tools(
    engine: Any,
    registry: Any,
    permission_agent: Optional[Any] = None,
) -> int:
    """
    Register every domain agent as a ``DomainTool`` in *registry*.

    Called from ``GeoSI.__init__`` alongside ``discover_portable_tools()`` so
    the single Supervisor pipeline can plan→validate→permission→execute domain
    agents like any other tool. Returns the number registered.
    """
    count = 0
    for spec in _DOMAIN_SPECS.values():
        try:
            registry.register_tool(DomainTool(engine, spec, permission_agent))
            count += 1
        except Exception as exc:  # pragma: no cover - defensive
            logger.debug("Failed to register domain tool '%s': %s", spec.name, exc)
    logger.info("Registered %d domain tool(s)", count)
    return count


def domain_tool_specs() -> list[ToolSpec]:
    """All domain ToolSpecs (used by the Planning Agent's core-tool include set)."""
    return list(_DOMAIN_SPECS.values())
