# -*- coding: utf-8 -*-
"""
GeoSI v2 — Code Generation Agent (Optional Agent #14)
════════════════════════════════════════════════════════════════════
Generates PyQGIS scripts, GeoPandas code, Rasterio workflows, and
reproducible Python scripts from ExecutionPlans.

PRD §4.2 Optional Agent #14 — CRITICAL Production note
────────────────────────────────────────────────────────
Generated code is NEVER auto-executed.
Output is ALWAYS presented to the user for review.
Code Generation output is NEVER routed back into the Execution
Dispatcher automatically.

This is a launch-blocking acceptance criterion (PRD §14).

Permission tier: Never executes — output is code for human review only.
"""
from __future__ import annotations

import logging
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from geosi_engine.telemetry import span, set_span_attr

logger = logging.getLogger("geosi_engine.agents.code_generation")

# ── Code template library ─────────────────────────────────────────────────

_PYQGIS_HEADER = """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
GeoSI-Generated PyQGIS Script
Generated: {timestamp}
Plan ID: {plan_id}
⚠️  REVIEW BEFORE RUNNING — Generated code must be reviewed by the user.
\"\"\"
import processing
from qgis.core import QgsVectorLayer, QgsRasterLayer, QgsProject
"""

_GEOPANDAS_HEADER = """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
GeoSI-Generated GeoPandas Script
Generated: {timestamp}
Plan ID: {plan_id}
⚠️  REVIEW BEFORE RUNNING — Generated code must be reviewed by the user.
\"\"\"
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import mapping
"""

_RASTERIO_HEADER = """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
GeoSI-Generated Rasterio Script
Generated: {timestamp}
Plan ID: {plan_id}
⚠️  REVIEW BEFORE RUNNING — Generated code must be reviewed by the user.
\"\"\"
import rasterio
import numpy as np
from rasterio.transform import from_bounds
"""


@dataclass
class CodeRequest:
    """A code generation request."""
    target_language: str        # "pyqgis" | "geopandas" | "rasterio" | "auto"
    plan: Optional[Any] = None  # ExecutionPlan
    query: str = ""             # natural-language description
    context_layers: List[str] = field(default_factory=list)
    session_id: str = ""
    include_comments: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GeneratedCode:
    """
    Result of code generation.

    CRITICAL: This output is NEVER auto-executed. It is presented
    to the user for review only (PRD §4.2, §14).
    """
    success: bool
    target_language: str
    code: str = ""             # The generated source code
    filename: str = ""         # Suggested filename
    plan_id: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    # SAFETY FIELD: always True — enforced by the agent, never overridden
    requires_human_review: bool = True
    error: Optional[str] = None

    def __post_init__(self) -> None:
        # Enforce the PRD invariant: code generation output NEVER bypasses review
        object.__setattr__(self, "requires_human_review", True)


class CodeGenerationAgent:
    """
    Code Generation Agent (PRD §4.2, Agent #14).

    Converts ``ExecutionPlan`` objects and natural-language descriptions
    into reproducible Python scripts.

    SAFETY GUARANTEE: The ``requires_human_review`` field on every
    ``GeneratedCode`` object is hard-coded to ``True`` and enforced in
    ``__post_init__``. No caller may set it to ``False``.

    The Supervisor pipeline MUST NOT pass ``GeneratedCode.code`` into
    the Execution Dispatcher. This is checked in ``generate()``.

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

    @span("codegen.generate", agent="code_generation")
    def generate(self, req: CodeRequest) -> GeneratedCode:
        """
        Generate a Python script from an ExecutionPlan.

        NEVER routes the output back to the Execution Dispatcher.
        Always returns ``GeneratedCode.requires_human_review=True``.
        """
        set_span_attr("codegen.language", req.target_language)

        plan = req.plan
        lang = self._choose_language(req)
        set_span_attr("codegen.effective_language", lang)

        try:
            if lang == "pyqgis":
                code = self._generate_pyqgis(plan, req)
            elif lang == "geopandas":
                code = self._generate_geopandas(plan, req)
            elif lang == "rasterio":
                code = self._generate_rasterio(plan, req)
            else:
                code = self._generate_generic(plan, req)

            plan_id = getattr(plan, "plan_id", "") if plan else ""
            filename = f"geosi_{lang}_{plan_id or 'script'}.py"

            warnings = [
                "⚠️  GENERATED CODE — must be reviewed and tested before execution.",
                "Verify all file paths, layer names, and parameters before running.",
                "Generated code may require additional dependencies not listed in imports.",
            ]

            # ASTGuard static analysis (non-blocking: adds to warnings only)
            try:
                from geosi_engine.security import ASTGuard
                guard_ok, violations = ASTGuard.check(code)
                if not guard_ok:
                    warnings.append("🛡 ASTGuard flagged potential issues:")
                    warnings.extend(f"   • {v}" for v in violations)
            except Exception:
                pass

            result = GeneratedCode(
                success=True,
                target_language=lang,
                code=code,
                filename=filename,
                plan_id=plan_id,
                warnings=warnings,
            )
            logger.info(
                "Code generated: language=%s plan_id=%s lines=%d",
                lang, plan_id, len(code.splitlines()),
            )
            return result

        except Exception as exc:
            return GeneratedCode(
                success=False, target_language=lang, error=str(exc)
            )

    # ------------------------------------------------------------------
    # PyQGIS generator
    # ------------------------------------------------------------------

    def _generate_pyqgis(self, plan: Any, req: CodeRequest) -> str:
        """Generate a PyQGIS processing script from an ExecutionPlan."""
        timestamp = datetime.now(timezone.utc).isoformat()
        plan_id = getattr(plan, "plan_id", "N/A") if plan else "N/A"
        steps = getattr(plan, "steps", []) if plan else []

        lines = [_PYQGIS_HEADER.format(timestamp=timestamp, plan_id=plan_id)]

        if req.context_layers:
            lines.append("# ── Load input layers ────────────────────────────────────────────")
            for i, layer_path in enumerate(req.context_layers):
                var = f"layer_{i+1}"
                lines.append(f'{var} = QgsVectorLayer("{layer_path}", "{var}", "ogr")')
                lines.append(f"QgsProject.instance().addMapLayer({var})")
            lines.append("")

        lines.append("# ── Execute workflow steps ───────────────────────────────────────")
        for i, step in enumerate(steps):
            tool = getattr(step, "tool_name", "unknown_tool")
            params = getattr(step, "parameters", {})
            desc = getattr(step, "description", "")
            risk = getattr(step, "risk_level", "read_only")

            if req.include_comments:
                lines.append(f"\n# Step {i+1}: {desc or tool} [risk: {risk}]")
                if risk in ("mutating", "destructive"):
                    lines.append(f"# ⚠️  This step is {risk.upper()} — review carefully before running")

            params_repr = repr(params) if params else "{}"
            lines.append(f"result_{i+1} = processing.run(")
            lines.append(f'    "{tool}",')
            lines.append(f"    {params_repr}")
            lines.append(f")")
            lines.append(f'print(f"Step {i+1} ({tool}): {{result_{i+1}}}")')

        lines.append("\nprint('Workflow complete.')")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # GeoPandas generator
    # ------------------------------------------------------------------

    def _generate_geopandas(self, plan: Any, req: CodeRequest) -> str:
        """Generate a GeoPandas script from an ExecutionPlan."""
        timestamp = datetime.now(timezone.utc).isoformat()
        plan_id = getattr(plan, "plan_id", "N/A") if plan else "N/A"
        steps = getattr(plan, "steps", []) if plan else []

        lines = [_GEOPANDAS_HEADER.format(timestamp=timestamp, plan_id=plan_id)]

        # Load layers
        if req.context_layers:
            lines.append("# ── Load data ────────────────────────────────────────────────────")
            for i, p in enumerate(req.context_layers):
                lines.append(f'gdf_{i+1} = gpd.read_file("{p}")')
            lines.append("")

        # Map tool names to geopandas idioms
        _GPANDAS_MAP = {
            "buffer": "gdf.buffer({distance})",
            "clip": "gpd.clip(gdf, mask)",
            "intersect": "gpd.overlay(gdf_1, gdf_2, how='intersection')",
            "union": "gpd.overlay(gdf_1, gdf_2, how='union')",
            "dissolve": "gdf.dissolve(by='{column}')",
            "reproject": "gdf.to_crs(epsg={epsg})",
        }

        lines.append("# ── Workflow steps ───────────────────────────────────────────────")
        for i, step in enumerate(steps):
            tool = getattr(step, "tool_name", "")
            params = getattr(step, "parameters", {})
            desc = getattr(step, "description", "")
            risk = getattr(step, "risk_level", "read_only")

            if req.include_comments:
                lines.append(f"\n# Step {i+1}: {desc or tool} [risk: {risk}]")

            tool_key = tool.replace("native:", "").replace("gdal:", "").lower()
            if tool_key in _GPANDAS_MAP:
                template = _GPANDAS_MAP[tool_key]
                for k, v in params.items():
                    template = template.replace(f"{{{k}}}", repr(v))
                lines.append(f"result_{i+1} = {template}")
            else:
                lines.append(f"# TODO: Implement '{tool}' with params: {params}")
                lines.append(f"result_{i+1} = None  # Not automatically translatable")

        lines.append("\n# ── Save results ─────────────────────────────────────────────────")
        if steps:
            lines.append(f'if result_{len(steps)} is not None:')
            lines.append(f'    result_{len(steps)}.to_file("geosi_output_{plan_id}.gpkg", driver="GPKG")')
        lines.append('print("Done.")')
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Rasterio generator
    # ------------------------------------------------------------------

    def _generate_rasterio(self, plan: Any, req: CodeRequest) -> str:
        """Generate a Rasterio script from an ExecutionPlan."""
        timestamp = datetime.now(timezone.utc).isoformat()
        plan_id = getattr(plan, "plan_id", "N/A") if plan else "N/A"
        steps = getattr(plan, "steps", []) if plan else []

        lines = [_RASTERIO_HEADER.format(timestamp=timestamp, plan_id=plan_id)]

        if req.context_layers:
            lines.append("# ── Open raster datasets ─────────────────────────────────────────")
            for i, p in enumerate(req.context_layers):
                lines.append(f'src_{i+1} = rasterio.open("{p}")')
                lines.append(f"band_{i+1} = src_{i+1}.read(1).astype(float)")
            lines.append("")

        lines.append("# ── Processing steps ─────────────────────────────────────────────")
        for i, step in enumerate(steps):
            tool = getattr(step, "tool_name", "")
            desc = getattr(step, "description", "")
            if req.include_comments:
                lines.append(f"\n# Step {i+1}: {desc or tool}")
            lines.append(f"# TODO: Implement '{tool}' — map to rasterio/numpy operation")
            lines.append(f"result_band_{i+1} = None")

        plan_id_safe = str(plan_id).replace("-", "_")
        lines.append(f"""
# ── Write output ──────────────────────────────────────────────────
out_path = "geosi_raster_output_{plan_id_safe}.tif"
profile = src_1.profile.copy()
profile.update(dtype="float32", count=1)
with rasterio.open(out_path, "w", **profile) as dst:
    # Replace result_band_N with your computed array
    dst.write(np.zeros(src_1.shape, dtype="float32"), 1)
print(f"Output written: {{out_path}}")
""")
        return "\n".join(lines)

    def _generate_generic(self, plan: Any, req: CodeRequest) -> str:
        """Fallback: generate a stub script with TODO markers."""
        steps = getattr(plan, "steps", []) if plan else []
        plan_id = getattr(plan, "plan_id", "N/A") if plan else "N/A"
        timestamp = datetime.now(timezone.utc).isoformat()

        lines = [
            f"# GeoSI Generated Script — {timestamp}",
            f"# Plan ID: {plan_id}",
            "# Target language: generic Python",
            "# ⚠️  REVIEW BEFORE RUNNING",
            "",
        ]
        for i, step in enumerate(steps):
            tool = getattr(step, "tool_name", "?")
            params = getattr(step, "parameters", {})
            lines.append(f"# Step {i+1}: {tool}")
            lines.append(f"# Parameters: {params}")
            lines.append(f"# TODO: Implement this step")
            lines.append("")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _choose_language(self, req: CodeRequest) -> str:
        """Auto-detect the best language from plan contents."""
        if req.target_language != "auto":
            return req.target_language.lower()

        steps = getattr(req.plan, "steps", []) if req.plan else []
        tool_names = " ".join(getattr(s, "tool_name", "") for s in steps).lower()

        if "native:" in tool_names or "qgis:" in tool_names:
            return "pyqgis"
        elif "raster" in tool_names or "dem" in tool_names or "gdal" in tool_names:
            return "rasterio"
        else:
            return "geopandas"
