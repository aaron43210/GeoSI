"""
GeoSI v2 — Report Generation Agent (Core Agent #11)
════════════════════════════════════════════════════════════════════
Generates PDF reports, maps, workflow graphs, methodology summaries,
execution logs, and statistics.

PRD §4.1 Agent #11 — Production requirements
──────────────────────────────────────────────
* Every generated report is linked to its corresponding
  ``geosi_audit_log`` entry — outputs are fully traceable back to
  the exact plan, parameters, and approvals that produced them.
* Permission tier: ``allow`` (report writes are non-destructive to
  source data — they only write report artefacts, never modify input
  layers).
* OTel span per report generation.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from geosi_engine.telemetry import set_span_attr, span

logger = logging.getLogger("geosi_engine.agents.report_generation")


@dataclass
class ReportRequest:
    """Request to generate a GeoSI report."""

    report_type: str  # "execution_summary" | "methodology" | "workflow_graph" | "full_pdf" | "statistics"
    execution_result: Optional[Any] = None
    plan: Optional[Any] = None  # ExecutionPlan
    audit_log_id: Optional[str] = None  # Links report to geosi_audit_log (PRD §4.1 requirement)
    session_id: str = ""
    output_path: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReportResult:
    """Result of report generation."""

    success: bool
    report_type: str
    output_path: Optional[str] = None
    audit_log_id: Optional[str] = None  # traceable back to audit log
    content: Optional[str] = None  # inline text for execution_summary / statistics
    statistics: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    duration_ms: float = 0.0


class ReportGenerationAgent:
    """
    Report Generation Agent (PRD §4.1, Agent #11).

    Builds reports from execution results, linking every output to its
    ``geosi_audit_log`` entry for full traceability (PRD §4.1 prod req).

    No permission gate needed — report writes are non-destructive to
    source data (tier: ``allow``).

    Parameters
    ----------
    engine:
        Session-scoped GeoSI instance.
    """

    SUPPORTED_TYPES = {
        "execution_summary": "Markdown summary of execution results",
        "methodology": "Step-by-step methodology document",
        "workflow_graph": "DOT/Mermaid workflow graph",
        "statistics": "Statistical summary of output layers",
        "full_pdf": "Complete PDF report (requires WeasyPrint)",
    }

    def __init__(self, engine: Any) -> None:
        self._engine = engine

    # ------------------------------------------------------------------
    # Public: generate
    # ------------------------------------------------------------------

    @span("report.generate", agent="report_generation")
    def generate(self, req: ReportRequest) -> ReportResult:
        """
        Generate a report from execution results.

        Every report is linked to ``audit_log_id`` so the output
        is traceable back to the exact plan, parameters, and approvals.
        """
        set_span_attr("report.type", req.report_type)
        set_span_attr("report.audit_log_id", req.audit_log_id or "")
        start = time.monotonic()

        if req.report_type not in self.SUPPORTED_TYPES:
            return ReportResult(
                success=False,
                report_type=req.report_type,
                error=f"Unknown report type '{req.report_type}'. Supported: {list(self.SUPPORTED_TYPES.keys())}",
            )

        try:
            result = self._dispatch(req)
            result.duration_ms = (time.monotonic() - start) * 1000
            result.audit_log_id = req.audit_log_id
            set_span_attr("report.output_path", result.output_path or "inline")
            logger.info(
                "Report generated: type=%s audit_log_id=%s → %s",
                req.report_type,
                req.audit_log_id,
                result.output_path or "inline",
            )
            return result
        except Exception as exc:
            return ReportResult(
                success=False,
                report_type=req.report_type,
                audit_log_id=req.audit_log_id,
                error=str(exc),
                duration_ms=(time.monotonic() - start) * 1000,
            )

    # ------------------------------------------------------------------
    # Report type generators
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Answers and in-memory summaries for the agent pipeline
    # ------------------------------------------------------------------

    @span("report.answer", agent="report_generation")
    def answer(self, query: str, plan: Any, result: Any) -> Optional[str]:
        """
        Answer a question from the executed plan's results.

        "How many ..." is answered from the result layer's exact feature
        count (small models miscount rows); other questions are answered by
        the planner's LLM from the result data (attribute rows, statistics,
        tool values) read back through the registered layer inspector.
        """
        import re as _re

        from geosi_engine.agents.verification import geom_family
        from geosi_engine.base import get_inspector
        from geosi_engine.models import Layer

        steps = getattr(plan, "steps", []) or []
        outputs = getattr(result, "results", None) or {}
        final = outputs.get(steps[-1].output_name) if steps else None
        if (
            _re.match(r"\s*how many\b", query or "", _re.I)
            and isinstance(final, Layer)
            and geom_family(final.geometry_type) in ("point", "line", "polygon")
        ):
            return (
                f"{final.feature_count} — the result layer '{final.name}' has "
                f"{final.feature_count} matching feature(s)."
            )

        inspector = get_inspector()
        evidence = []
        for name, out in outputs.items():
            if isinstance(out, Layer) and inspector is not None:
                try:
                    evidence.append(inspector(out, 40))
                except Exception as exc:
                    logger.debug("inspect %s failed: %s", name, exc)
            elif out is not None:
                evidence.append(f"{name}: {out}")
        if getattr(result, "answer", ""):
            evidence.append(f"tool message: {result.answer}")
        agent = getattr(self._engine, "agent", None)
        if not evidence or agent is None:
            return None
        return agent.answer_from_evidence(query, "\n".join(evidence))

    def render_summary(self, plan: Any, result: Any, session_id: str = "", audit_log_id: Optional[str] = None) -> str:
        """The Markdown execution summary, without writing a file."""
        return "\n".join(self._summary_lines(plan, result, session_id, audit_log_id))

    def _summary_lines(self, plan: Any, result: Any, session_id: str, audit_log_id: Optional[str]) -> List[str]:
        now = datetime.now(timezone.utc).isoformat()
        lines = [
            "# GeoSI Execution Summary",
            f"**Generated:** {now}",
            f"**Session:** {session_id or 'N/A'}",
            f"**Audit Log ID:** {audit_log_id or 'N/A'}",
            "",
        ]
        if plan:
            lines += [
                "## Execution Plan",
                f"- **Plan ID:** {getattr(plan, 'plan_id', 'N/A')}",
                f"- **Plan source:** {getattr(plan, 'plan_source', 'N/A')}",
                f"- **Steps:** {len(getattr(plan, 'steps', []))}",
                f"- **Reasoning:** {getattr(plan, 'reasoning', 'N/A')}",
                "",
            ]
            steps = getattr(plan, "steps", [])
            if steps:
                lines.append("### Steps")
                for i, step in enumerate(steps, 1):
                    lines.append(
                        f"{i}. **{getattr(step, 'tool_name', '?')}** "
                        f"(risk: `{getattr(step, 'risk_level', '?')}`) — "
                        f"{getattr(step, 'description', '')}"
                    )
                lines.append("")
        if result:
            success = getattr(result, "success", False)
            lines += ["## Result", f"- **Status:** {'✅ Success' if success else '❌ Failed'}"]
            if getattr(result, "answer", ""):
                lines.append(f"- **Answer:** {result.answer}")
            if getattr(result, "error", None):
                lines.append(f"- **Error:** {result.error}")
            for name, out in (getattr(result, "results", None) or {}).items():
                path = getattr(out, "filepath", "")
                if path:
                    count = getattr(out, "feature_count", "")
                    lines.append(
                        f"- **Output `{getattr(out, 'name', name)}`:** `{path}`"
                        + (f" ({count} features)" if getattr(out, "layer_type", "") == "vector" else "")
                    )
            for w in getattr(result, "warnings", []) or []:
                lines.append(f"- ⚠ {w}")
            if hasattr(result, "output_layer") and result.output_layer:
                lines.append(f"- **Output:** `{result.output_layer}`")
            if hasattr(result, "statistics") and result.statistics:
                lines.append("- **Statistics:**")
                for k, v in result.statistics.items():
                    lines.append(f"  - {k}: {v}")
        return lines

    def execution_summary(self, req: ReportRequest) -> ReportResult:
        """Generate a Markdown execution summary linked to the audit log."""
        lines = self._summary_lines(req.plan, req.execution_result, req.session_id, req.audit_log_id)
        content = "\n".join(lines)
        out_path = req.output_path or f"geosi_summary_{req.audit_log_id or int(time.time())}.md"
        Path(out_path).write_text(content, encoding="utf-8")
        return ReportResult(
            success=True,
            report_type="execution_summary",
            output_path=out_path,
            content=content,
            statistics={"lines": len(lines)},
        )

    def workflow_graph(self, req: ReportRequest) -> ReportResult:
        """
        Generate a Mermaid / DOT workflow graph from an ExecutionPlan.
        """
        plan = req.plan
        if not plan:
            return ReportResult(
                success=False, report_type="workflow_graph", error="plan is required for workflow_graph reports."
            )

        steps = getattr(plan, "steps", [])
        fmt = req.parameters.get("format", "mermaid")

        if fmt == "mermaid":
            lines = ["```mermaid", "graph TD"]
            prev = "Start([User Query])"
            for i, step in enumerate(steps):
                node_id = f"S{i+1}"
                label = f"{getattr(step, 'tool_name', '?')} [{getattr(step, 'risk_level', '?')}]"
                lines.append(f'    {node_id}["{label}"]')
                lines.append(f"    {prev} --> {node_id}")
                prev = node_id
            lines.append(f"    {prev} --> End([Report])")
            lines.append("```")
            content = "\n".join(lines)
        else:
            # DOT format
            dot_nodes = "\n".join(f'  s{i}[label="{getattr(s, "tool_name", "?")}"];' for i, s in enumerate(steps))
            dot_edges = "\n".join(f"  s{i} -> s{i+1};" for i in range(len(steps) - 1))
            content = f"digraph workflow {{\n{dot_nodes}\n{dot_edges}\n}}"

        ext = "md" if fmt == "mermaid" else "dot"
        out_path = req.output_path or f"geosi_workflow_{req.audit_log_id or int(time.time())}.{ext}"
        Path(out_path).write_text(content, encoding="utf-8")

        return ReportResult(
            success=True,
            report_type="workflow_graph",
            output_path=out_path,
            content=content,
            statistics={"steps": len(steps), "format": fmt},
        )

    def statistics_report(self, req: ReportRequest) -> ReportResult:
        """Generate a statistics summary from execution result output layers."""
        stats: dict = {}
        result = req.execution_result

        output_paths: list[str] = []
        if result and hasattr(result, "output_layer") and result.output_layer:
            output_paths.append(result.output_layer)
        output_paths.extend(req.parameters.get("layers", []))

        for path in output_paths:
            try:
                ext = path.lower().rsplit(".", 1)[-1]
                if ext in ("shp", "gpkg", "geojson"):
                    import geopandas as gpd

                    gdf = gpd.read_file(path)
                    stats[path] = {
                        "feature_count": len(gdf),
                        "crs": str(gdf.crs),
                        "columns": list(gdf.columns),
                        "geometry_types": gdf.geometry.geom_type.value_counts().to_dict(),
                    }
                elif ext in ("tif", "tiff"):
                    import rasterio

                    with rasterio.open(path) as src:
                        data = src.read(1)
                        valid = data[data != src.nodata] if src.nodata else data.flatten()
                        stats[path] = {
                            "bands": src.count,
                            "shape": list(src.shape),
                            "min": float(valid.min()),
                            "max": float(valid.max()),
                            "mean": float(valid.mean()),
                        }
            except Exception as exc:
                stats[path] = {"error": str(exc)}

        content = json.dumps(stats, indent=2)
        out_path = req.output_path or f"geosi_stats_{req.audit_log_id or int(time.time())}.json"
        Path(out_path).write_text(content, encoding="utf-8")

        return ReportResult(
            success=True,
            report_type="statistics",
            output_path=out_path,
            content=content,
            statistics=stats,
        )

    def full_pdf(self, req: ReportRequest) -> ReportResult:
        """
        Generate a complete PDF report using WeasyPrint.
        Falls back to Markdown if WeasyPrint is not installed.
        """
        # First generate markdown summary
        md_result = self.execution_summary(req)
        if not md_result.success:
            return md_result

        out_path = req.output_path or f"geosi_report_{req.audit_log_id or int(time.time())}"
        if not out_path.endswith(".pdf"):
            out_path += ".pdf"

        try:
            from weasyprint import HTML

            html_content = f"<html><body><pre>{md_result.content}</pre></body></html>"
            HTML(string=html_content).write_pdf(out_path)
            logger.info("PDF report written: %s", out_path)
            return ReportResult(
                success=True,
                report_type="full_pdf",
                output_path=out_path,
                statistics={"pages": 1},
            )
        except ImportError:
            # Graceful fallback to markdown
            md_out = out_path.replace(".pdf", ".md")
            Path(md_out).write_text(md_result.content or "", encoding="utf-8")
            logger.warning("WeasyPrint not available — saved as Markdown: %s", md_out)
            return ReportResult(
                success=True,
                report_type="full_pdf",
                output_path=md_out,
                content=md_result.content,
                statistics={"fallback": "markdown", "reason": "weasyprint not installed"},
            )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _dispatch(self, req: ReportRequest) -> ReportResult:
        if req.report_type == "execution_summary":
            return self.execution_summary(req)
        elif req.report_type == "workflow_graph":
            return self.workflow_graph(req)
        elif req.report_type == "statistics":
            return self.statistics_report(req)
        elif req.report_type in ("full_pdf", "methodology"):
            return self.full_pdf(req)
        return ReportResult(
            success=False, report_type=req.report_type, error=f"Report type '{req.report_type}' not yet implemented."
        )
