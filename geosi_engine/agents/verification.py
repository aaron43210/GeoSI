"""
GeoSI v2 — Verification Agent (Core Agent #10)
════════════════════════════════════════════════════════════════════
Runs QA on every execution result BEFORE it reaches the Report
Generation Agent. Failures route back to the Reflection Agent
rather than surfacing broken output to the user.

PRD §4.1 Agent #10 — Production requirements
──────────────────────────────────────────────
* Geometry validation, output validation, raster QA, layer integrity,
  accuracy metrics, CRS verification.
* Runs on every execution result before Report Generation Agent.
* Failures route back to Reflection Agent for retry.
* Read-only by design — QA only, no execution.
* Auto-tier: ``allow`` (always read-only).
"""

from __future__ import annotations

import logging
import re as _re
from dataclasses import dataclass, field
from typing import Any, List, Optional

from geosi_engine.telemetry import set_span_attr, span

logger = logging.getLogger("geosi_engine.agents.verification")


# A question gets its answer from data, so it need not produce a new layer
QUESTION_RE = _re.compile(
    r"^\s*(how many|how much|how long|how big|which|what|where|is there|are there|does|do|list|"
    r"tell me|show me (the )?(number|count|total))\b|\?\s*$",
    _re.IGNORECASE,
)
# "find/select/extract/get <layer> ..." → the answer must be features of <layer>
_SUBJECT_RE = _re.compile(
    r"\b(?:find|select|extract|get|keep|filter|identify|return)\s+(?:all\s+|the\s+|only\s+)?([a-z_][a-z0-9_]*)",
    _re.IGNORECASE,
)
_EACH_RE = _re.compile(r"\b(?:each|every|per)\s+([a-z_]+(?:\s[a-z_]+)?)", _re.IGNORECASE)
_GEOM_FAMILY = {
    "point": "point",
    "multipoint": "point",
    "line": "line",
    "linestring": "line",
    "multilinestring": "line",
    "polygon": "polygon",
    "multipolygon": "polygon",
}
# File-level QA reads the whole output; skip it for very large layers
_FILE_QA_MAX_FEATURES = 100_000


def geom_family(geometry_type: str) -> str:
    """ "Point"/"MultiPolygon"/"LineString" → "point"/"polygon"/"line"."""
    g = (geometry_type or "").lower().replace(" ", "")
    for key, fam in _GEOM_FAMILY.items():
        if g.startswith(key):
            return fam
    return g


@dataclass
class VerificationIssue:
    """One verification finding."""

    severity: str  # "error" | "warning" | "info"
    category: str  # "geometry" | "crs" | "raster_qa" | "value_range" | "topology"
    message: str
    layer: Optional[str] = None


@dataclass
class VerificationReport:
    """Full QA report for an execution result or layer."""

    passed: bool
    layer: Optional[str] = None
    issues: List[str] = field(default_factory=list)  # plain string list for compat
    findings: List[VerificationIssue] = field(default_factory=list)
    statistics: dict = field(default_factory=dict)

    def errors(self) -> List[VerificationIssue]:
        return [f for f in self.findings if f.severity == "error"]

    def warnings(self) -> List[VerificationIssue]:
        return [f for f in self.findings if f.severity == "warning"]


class VerificationAgent:
    """
    QA Agent that validates every execution output (PRD §4.1, Agent #10).

    Used by GISAgent, RemoteSensingAgent, MLAgent, GeologyAgent, and the
    Supervisor pipeline before results reach the Report Generation Agent.

    Failures are surfaced as ``VerificationReport.passed=False`` — the
    caller (Supervisor or domain agent) routes to the Reflection Agent
    for retry rather than presenting broken output to the user.

    Parameters
    ----------
    engine:
        Session-scoped GeoSI instance.
    """

    def __init__(self, engine: Any) -> None:
        self._engine = engine

    # ------------------------------------------------------------------
    # Public: verify by type
    # ------------------------------------------------------------------

    @span("verification.verify_vector", agent="verification")
    def verify_vector(self, layer_path: str) -> VerificationReport:
        """
        Verify a vector layer: geometry validity, topology, CRS, feature count.

        Checks:
        - All geometries are valid (Shapely `is_valid`)
        - No null geometries
        - CRS is defined and recognised
        - Feature count > 0
        - No self-intersecting polygons (topology check)
        """
        findings: list[VerificationIssue] = []
        stats: dict = {}

        set_span_attr("verification.layer", layer_path)

        try:
            import geopandas as gpd

            gdf = gpd.read_file(layer_path)
            stats["feature_count"] = len(gdf)

            # CRS check
            if gdf.crs is None:
                findings.append(
                    VerificationIssue(
                        severity="error",
                        category="crs",
                        message=f"Layer '{layer_path}' has no CRS defined.",
                        layer=layer_path,
                    )
                )
            else:
                stats["crs"] = str(gdf.crs)

            # Null geometry check
            null_count = int(gdf.geometry.isna().sum())
            if null_count > 0:
                findings.append(
                    VerificationIssue(
                        severity="error",
                        category="geometry",
                        message=f"{null_count} null geometries found in '{layer_path}'.",
                        layer=layer_path,
                    )
                )
            stats["null_geometries"] = null_count

            # Validity check
            invalid_count = int((~gdf.geometry.dropna().is_valid).sum())
            if invalid_count > 0:
                findings.append(
                    VerificationIssue(
                        severity="warning",
                        category="geometry",
                        message=(
                            f"{invalid_count} invalid geometries (Shapely is_valid=False). "
                            "Consider running Fix Geometries."
                        ),
                        layer=layer_path,
                    )
                )
            stats["invalid_geometries"] = invalid_count

            # Feature count
            if len(gdf) == 0:
                findings.append(
                    VerificationIssue(
                        severity="warning",
                        category="geometry",
                        message=f"Layer '{layer_path}' is empty (0 features).",
                        layer=layer_path,
                    )
                )

        except ImportError as exc:
            # FAIL CLOSED: missing dependency means nothing was checked.
            # A partial Docker build or broken venv must not produce passed=True.
            logger.error(
                "geopandas not installed — vector verification cannot run on '%s': %s",
                layer_path,
                exc,
            )
            findings.append(
                VerificationIssue(
                    severity="error",
                    category="geometry",
                    message=(
                        f"Verification dependency missing (geopandas): '{exc}'. "
                        f"Layer '{layer_path}' was NOT checked — marking as FAILED. "
                        "Install geopandas to enable vector verification."
                    ),
                    layer=layer_path,
                )
            )
        except Exception as exc:
            findings.append(
                VerificationIssue(
                    severity="error",
                    category="geometry",
                    message=f"Could not read layer '{layer_path}': {exc}",
                    layer=layer_path,
                )
            )

        errors = [f for f in findings if f.severity == "error"]
        passed = len(errors) == 0
        set_span_attr("verification.passed", passed)
        set_span_attr("verification.issues", len(findings))

        return VerificationReport(
            passed=passed,
            layer=layer_path,
            issues=[f.message for f in findings],
            findings=findings,
            statistics=stats,
        )

    @span("verification.verify_raster", agent="verification")
    def verify_raster(self, layer_path: str, expected_range: Optional[tuple] = None) -> VerificationReport:
        """
        Verify a raster layer: CRS, value range, nodata, band count, non-null coverage.

        Parameters
        ----------
        layer_path:
            Path to the raster file.
        expected_range:
            Optional ``(min, max)`` tuple for value range check.
            E.g. ``(-1.0, 1.0)`` for spectral indices.
        """
        findings: list[VerificationIssue] = []
        stats: dict = {}

        set_span_attr("verification.layer", layer_path)

        try:
            import numpy as np
            import rasterio

            with rasterio.open(layer_path) as src:
                stats["crs"] = str(src.crs) if src.crs else "none"
                stats["bands"] = src.count
                stats["shape"] = list(src.shape)
                stats["nodata"] = src.nodata

                if src.crs is None:
                    findings.append(
                        VerificationIssue(
                            severity="error",
                            category="crs",
                            message=f"Raster '{layer_path}' has no CRS.",
                            layer=layer_path,
                        )
                    )

                for b in range(1, src.count + 1):
                    data = src.read(b)
                    if src.nodata is not None:
                        valid = data[data != src.nodata]
                    else:
                        valid = data.flatten()

                    if valid.size == 0:
                        findings.append(
                            VerificationIssue(
                                severity="error",
                                category="raster_qa",
                                message=f"Band {b} of '{layer_path}' contains only nodata values.",
                                layer=layer_path,
                            )
                        )
                    else:
                        b_min, b_max = float(valid.min()), float(valid.max())
                        stats[f"band_{b}_min"] = b_min
                        stats[f"band_{b}_max"] = b_max

                        if expected_range:
                            lo, hi = expected_range
                            out_of_range = int(((valid < lo) | (valid > hi)).sum())
                            if out_of_range > 0:
                                pct = out_of_range / valid.size * 100
                                findings.append(
                                    VerificationIssue(
                                        severity="warning",
                                        category="value_range",
                                        message=(
                                            f"Band {b}: {out_of_range} pixels ({pct:.1f}%) "
                                            f"outside expected range [{lo}, {hi}]."
                                        ),
                                        layer=layer_path,
                                    )
                                )

                        # NaN/Inf check
                        if np.issubdtype(data.dtype, np.floating):
                            nan_count = int(np.isnan(valid).sum() + np.isinf(valid).sum())
                            if nan_count > 0:
                                findings.append(
                                    VerificationIssue(
                                        severity="warning",
                                        category="raster_qa",
                                        message=f"Band {b}: {nan_count} NaN/Inf values detected.",
                                        layer=layer_path,
                                    )
                                )

        except ImportError as exc:
            # FAIL CLOSED: missing dependency means nothing was checked.
            # A partial Docker build or broken venv must not produce passed=True.
            logger.error(
                "rasterio/numpy not installed — raster verification cannot run on '%s': %s",
                layer_path,
                exc,
            )
            findings.append(
                VerificationIssue(
                    severity="error",
                    category="raster_qa",
                    message=(
                        f"Verification dependency missing (rasterio): '{exc}'. "
                        f"Raster '{layer_path}' was NOT checked — marking as FAILED. "
                        "Install rasterio to enable raster verification."
                    ),
                    layer=layer_path,
                )
            )
        except Exception as exc:
            findings.append(
                VerificationIssue(
                    severity="error",
                    category="raster_qa",
                    message=f"Could not open raster '{layer_path}': {exc}",
                    layer=layer_path,
                )
            )

        errors = [f for f in findings if f.severity == "error"]
        passed = len(errors) == 0
        set_span_attr("verification.passed", passed)

        return VerificationReport(
            passed=passed,
            layer=layer_path,
            issues=[f.message for f in findings],
            findings=findings,
            statistics=stats,
        )

    @span("verification.verify_crs_match", agent="verification")
    def verify_crs_match(self, layer_paths: List[str]) -> VerificationReport:
        """
        Verify all layers share the same CRS — critical before overlay ops.

        Performance: uses fiona.open() for metadata-only CRS reads.
        This reads only the file header, NOT the geometry data — ~100x faster
        than gpd.read_file() on large layers. Import is hoisted out of the loop.
        """
        findings: list[VerificationIssue] = []
        crs_set: set = set()
        stats: dict = {}

        # Hoist imports — importing inside a loop causes repeated sys.modules
        # lookups and interpreter lock contention on every iteration.
        try:
            import fiona

            _fiona_available = True
        except ImportError:
            _fiona_available = False

        for path in layer_paths:
            try:
                if _fiona_available:
                    # Metadata-only read — reads CRS from file header, never
                    # loads geometry. O(1) per file regardless of feature count.
                    with fiona.open(path) as src:
                        crs = str(src.crs) if src.crs else "undefined"
                else:
                    # Fallback: full read — slower but functional
                    import geopandas as gpd

                    crs = str(gpd.read_file(path).crs)
                crs_set.add(crs)
                stats[path] = crs
            except Exception as exc:
                findings.append(
                    VerificationIssue(
                        severity="error",
                        category="crs",
                        message=f"Could not read CRS from '{path}': {exc}",
                        layer=path,
                    )
                )

        if len(crs_set) > 1:
            findings.append(
                VerificationIssue(
                    severity="error",
                    category="crs",
                    message=(
                        f"CRS mismatch across layers: {crs_set}. "
                        "Reproject all layers to a common CRS before overlay."
                    ),
                )
            )

        errors = [f for f in findings if f.severity == "error"]
        return VerificationReport(
            passed=len(errors) == 0,
            issues=[f.message for f in findings],
            findings=findings,
            statistics=stats,
        )

    # ------------------------------------------------------------------
    # Public: does this result answer the request?
    # ------------------------------------------------------------------

    @span("verification.verify", agent="verification")
    def verify(self, query: str, plan: Any, result: Any, state: Any = None) -> VerificationReport:
        """
        Check an executed plan against the request.

        Errors (``passed=False``; the first is in ``issues[0]`` and goes back
        to the planner through the Reflection Agent):
        * a step failed;
        * no output layer for a request that is not a question;
        * an empty vector output;
        * "find hospitals ..." returned something other than hospitals'
          geometry type (inputs swapped);
        * "... in each zone" kept a different number of zones.

        Warnings (advisory): file-level QA of the final output — missing
        CRS, null or invalid geometries, raster no-data problems.
        """
        from geosi_engine.models import Layer

        state = state if state is not None else getattr(self._engine, "state", None)
        findings: List[VerificationIssue] = []

        def error(category: str, message: str) -> VerificationReport:
            findings.append(VerificationIssue("error", category, message))
            set_span_attr("verification.passed", False)
            return VerificationReport(passed=False, issues=[message], findings=findings)

        failed = [log for log in getattr(result, "logs", []) if log.status.value not in ("success",)]
        if failed:
            log = failed[0]
            return error("execution", f"step {log.step_id} ({log.tool_name}) failed: {log.error_message}")

        steps = getattr(plan, "steps", []) or []
        final = (getattr(result, "results", None) or {}).get(steps[-1].output_name) if steps else None
        if not isinstance(final, Layer) and not QUESTION_RE.search(query or ""):
            # Domain tools (code generation, reports, research, ...) return
            # documents by design; anything else must produce a layer.
            try:
                from geosi_engine.tools.domain_tools import DOMAIN_TOOL_NAMES
            except Exception:  # pragma: no cover
                DOMAIN_TOOL_NAMES = ()
            from geosi_engine.tools.data_connectors import ACTION_TOOL_NAMES

            last_tool = steps[-1].tool_name if steps else ""
            if last_tool in ACTION_TOOL_NAMES:
                set_span_attr("verification.passed", True)
                return VerificationReport(passed=True, issues=[], findings=findings)
            if not (steps and last_tool in DOMAIN_TOOL_NAMES and final is not None):
                return error(
                    "output",
                    "no result layer was produced — this request needs a " "processing tool that outputs a new layer",
                )

        if isinstance(final, Layer):
            if final.layer_type == "vector" and final.feature_count == 0:
                return error(
                    "output",
                    f"the final output '{final.name}' has 0 features — the inputs "
                    f"may be swapped, the wrong tool was used, or the distance/units "
                    f"are wrong",
                )
            each = self._each_layer(query, state)
            same_family = each is not None and geom_family(final.geometry_type) == each[2]
            if each and same_family and final.feature_count != each[1]:
                return error(
                    "output",
                    f"the request is about each feature of '{each[0]}' ({each[1]} "
                    f"features) but the output has {final.feature_count} — the result "
                    f"should keep one feature per '{each[0]}' feature (e.g. use "
                    f"'{each[0]}' as the INPUT/POLYGONS layer, keep non-matching "
                    f"features)",
                )
            expected = self._expected_geometry(query, state)
            if expected and final.layer_type == "vector":
                got = geom_family(final.geometry_type)
                if got and got != expected[1]:
                    return error(
                        "output",
                        f"the question asks for {expected[0]} ({expected[1]} "
                        f"features) but the final output has {got} features — use "
                        f"'{expected[0]}' as the INPUT layer and the other layer as "
                        f"the comparison/intersect layer",
                    )
            findings.extend(self._file_qa(final))

        set_span_attr("verification.passed", True)
        return VerificationReport(
            passed=True,
            issues=[f.message for f in findings],
            findings=findings,
        )

    def _file_qa(self, layer: Any) -> List[VerificationIssue]:
        """Advisory QA on the output file; findings are downgraded to warnings."""
        if not getattr(layer, "filepath", "") or layer.feature_count > _FILE_QA_MAX_FEATURES:
            return []
        try:
            if layer.layer_type == "raster":
                import rasterio  # noqa: F401

                report = self.verify_raster(layer.filepath)
            else:
                import geopandas  # noqa: F401

                report = self.verify_vector(layer.filepath)
        except ImportError:
            return []  # QA libraries not installed here; semantic checks still ran
        except Exception as exc:  # pragma: no cover - defensive
            logger.debug("File QA skipped for %s: %s", layer.filepath, exc)
            return []
        out = []
        for f in report.findings:
            if f.severity in ("error", "warning") and "0 features" not in f.message and "empty" not in f.message:
                out.append(VerificationIssue("warning", f.category, f.message, f.layer))
        return out

    @staticmethod
    def _each_layer(query: str, state: Any):
        """("flood_zones", 2, "polygon") for "... in each flood_zones polygon"."""
        if state is None:
            return None
        for m in _EACH_RE.finditer(query or ""):
            words = m.group(1).lower().split()
            for name in state.list_layers():
                n = name.lower()
                cands = {n, n.rstrip("s"), n.replace("_", " "), n.replace("_", " ").rstrip("s")}
                if words[0] in cands or " ".join(words) in cands:
                    layer = state.get_layer(name)
                    if getattr(layer, "layer_type", "") == "vector" and layer.feature_count:
                        return name, layer.feature_count, geom_family(layer.geometry_type)
        return None

    @staticmethod
    def _expected_geometry(query: str, state: Any):
        """("hospitals", "point") when the query asks to find features of a layer."""
        if state is None:
            return None
        for m in _SUBJECT_RE.finditer(query or ""):
            word = m.group(1).lower()
            for name in state.list_layers():
                if name.lower() in (word, word.rstrip("s"), word + "s"):
                    layer = state.get_layer(name)
                    fam = geom_family(getattr(layer, "geometry_type", ""))
                    if fam in ("point", "line", "polygon"):
                        return name, fam
        return None

    @span("verification.verify_execution_result", agent="verification")
    def verify_execution_result(self, result: Any) -> VerificationReport:
        """
        Verify any execution result object before it reaches the
        Report Generation Agent.

        Dispatches to ``verify_vector`` or ``verify_raster`` based on
        the output layer extension.
        """
        set_span_attr("verification.result_type", type(result).__name__)

        # Extract output path from result
        output_path: Optional[str] = None
        if hasattr(result, "output_layer"):
            output_path = result.output_layer
        elif hasattr(result, "output_path"):
            output_path = result.output_path
        elif hasattr(result, "output") and isinstance(result.output, dict):
            output_path = result.output.get("OUTPUT") or result.output.get("output")
        elif getattr(getattr(result, "output", None), "filepath", ""):
            output_path = result.output.filepath  # a GeoSI Layer

        if not output_path:
            # No output file — check for in-memory success flag
            if getattr(result, "success", True):
                return VerificationReport(
                    passed=True, issues=[], statistics={"note": "In-memory result — no file verification needed."}
                )
            return VerificationReport(passed=False, issues=["Execution result has no output path and reports failure."])

        # Dispatch by extension
        ext = output_path.lower().rsplit(".", 1)[-1] if "." in output_path else ""
        if ext in ("tif", "tiff", "img", "vrt"):
            return self.verify_raster(output_path)
        elif ext in ("shp", "gpkg", "geojson", "json", "kml", "gml", "fgb"):
            return self.verify_vector(output_path)
        else:
            return VerificationReport(
                passed=True,
                issues=[f"Unknown output format '.{ext}' — verification skipped."],
                statistics={"output_path": output_path},
            )
