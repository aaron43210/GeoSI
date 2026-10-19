# -*- coding: utf-8 -*-
"""
GeoSI v2 — Offline Live-Registry Documentation Generator (Plan Part C)
════════════════════════════════════════════════════════════════════
Generates Markdown documentation for EVERY tool GeoSI can actually run,
straight from the live ``ToolRegistry`` (QGIS Processing + GDAL + portable
tools). This is the always-available, zero-hallucination doc source: the
docs describe the exact tools, algorithm ids and parameters the engine
resolves at runtime, so once ingested the planner is grounded in real
capability rather than guessed tool names.

Fail-closed: if QGIS is not importable we log an error and exit non-zero.
We NEVER emit fabricated/placeholder docs — absent QGIS means absent docs.

Usage (must run inside a QGIS-enabled Python, headless is fine):
    QT_QPA_PLATFORM=offscreen \\
        PYTHONPATH=. python3 -m geosi_rag.qgis_registry_docs --out data/registry_docs/

Then ingest the generated Markdown into the knowledge base:
    PYTHONPATH=. python3 -m geosi_rag.ingest_cli \\
        --source data/registry_docs --collection gis_docs

Each tool entry carries:
  * registry name (what ``get_tool`` / the executor resolve — NOT the label)
  * the backing ``qgis_algorithm`` id (e.g. ``native:buffer``)
  * the FULL ``shortHelpString`` (the registry truncates to 300 chars; here
    we re-pull the untruncated help directly from the processing registry)
  * a parameter table (name / type / required / description)
  * a copy-pasteable example ``ToolStep`` JSON the planner can emulate
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger("geosi_rag.qgis_registry_docs")

_CATEGORY_FILES = {
    "vector": "vector.md",
    "raster": "raster.md",
    "terrain": "terrain.md",
    "analysis": "analysis.md",
    "network": "network.md",
    "database": "database.md",
    "codegen": "codegen.md",
    "report": "report.md",
    "research": "research.md",
    "remote_sensing": "remote_sensing.md",
    "machine_learning": "machine_learning.md",
    "geology": "geology.md",
    "general": "general.md",
}


def _full_help_map() -> Dict[str, str]:
    """
    Map ``qgis_algorithm`` id → untruncated ``shortHelpString``.

    The registry stores a 300-char-truncated description to save LLM tokens;
    for documentation we want the complete help text, so re-pull it directly
    from the live processing registry.
    """
    help_map: Dict[str, str] = {}
    try:
        from qgis.core import QgsApplication
        proc = QgsApplication.processingRegistry()
        if proc is None:
            return help_map
        for alg in proc.algorithms():
            try:
                full = alg.shortHelpString() or alg.shortDescription() or ""
                if full:
                    help_map[alg.id()] = full
            except Exception:  # pragma: no cover - per-alg defensive
                logger.debug("suppressed exception", exc_info=True)
                continue
    except Exception as exc:  # pragma: no cover - no QGIS
        logger.debug("Could not pull full help strings: %s", exc)
    return help_map


def _example_toolstep(spec: Any) -> str:
    """Build a copy-pasteable example ``ToolStep`` JSON for *spec*."""
    params: Dict[str, Any] = {}
    for p in getattr(spec, "parameters", []) or []:
        if not getattr(p, "required", False):
            continue
        example = getattr(p, "example", None)
        if example is not None:
            params[p.name] = example
        elif getattr(p, "param_type", "") == "layer":
            params[p.name] = "<layer_name>"
        elif getattr(p, "param_type", "") == "number":
            params[p.name] = 0
        elif getattr(p, "param_type", "") == "boolean":
            params[p.name] = False
        else:
            params[p.name] = f"<{p.name}>"
    step = {
        "step_id": "step_1",
        "tool_name": spec.name,
        "parameters": params,
        "input_layers": [],
        "output_name": f"{spec.name}_output",
        "description": f"Run {spec.display_name or spec.name}",
        "risk_level": "mutating" if getattr(spec, "requires_qgis", False) else "read_only",
    }
    return json.dumps(step, indent=2)


def _render_tool(spec: Any, full_help: Dict[str, str]) -> str:
    """Render one tool as a Markdown section."""
    lines: List[str] = []
    lines.append(f"### `{spec.name}`")
    lines.append("")
    if spec.display_name and spec.display_name != spec.name:
        lines.append(f"**Display name:** {spec.display_name}  ")
    if getattr(spec, "qgis_algorithm", None):
        lines.append(f"**QGIS algorithm:** `{spec.qgis_algorithm}`  ")
    lines.append(f"**Category:** `{spec.category}` · "
                 f"**Requires QGIS:** {bool(getattr(spec, 'requires_qgis', False))} · "
                 f"**Requires GPU:** {bool(getattr(spec, 'requires_gpu', False))}")
    lines.append("")

    desc = full_help.get(getattr(spec, "qgis_algorithm", "") or "", "") or spec.description or ""
    if desc:
        lines.append(desc.strip())
        lines.append("")

    params = getattr(spec, "parameters", []) or []
    if params:
        lines.append("| Parameter | Type | Required | Description |")
        lines.append("|-----------|------|----------|-------------|")
        for p in params:
            d = (getattr(p, "description", "") or "").replace("\n", " ").replace("|", "\\|")
            lines.append(
                f"| `{p.name}` | {getattr(p, 'param_type', '')} | "
                f"{'yes' if getattr(p, 'required', False) else 'no'} | {d} |"
            )
        lines.append("")

    if getattr(spec, "outputs", None):
        lines.append(f"**Outputs:** {', '.join(spec.outputs)}")
        lines.append("")

    lines.append("**Example ToolStep:**")
    lines.append("")
    lines.append("```json")
    lines.append(_example_toolstep(spec))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def generate(out_dir: str) -> int:
    """
    Build the registry, iterate its tools, and write per-category Markdown.

    Returns the number of tools documented (0 means nothing was discovered —
    treated as a failure by the CLI).
    """
    from geosi_engine.registry import ToolRegistry

    registry = ToolRegistry()

    # Portable tools are always available (GeoPandas / Rasterio loaders).
    try:
        registry.discover_portable_tools()
    except Exception as exc:
        logger.warning("Portable tool discovery failed: %s", exc)

    # QGIS Processing + GDAL — the bulk of the surface.
    try:
        from geosi_plugin.qgis_bridge import auto_discover_qgis_tools
        n = auto_discover_qgis_tools(registry)
        logger.info("Discovered %d QGIS/GDAL algorithms", n)
    except Exception as exc:
        logger.error("QGIS discovery failed: %s", exc)

    specs = registry.list_tools()
    if not specs:
        logger.error(
            "No tools discovered — refusing to emit docs. Run this inside a "
            "QGIS-enabled Python (QT_QPA_PLATFORM=offscreen)."
        )
        return 0

    full_help = _full_help_map()

    # Group specs by category.
    by_cat: Dict[str, List[Any]] = {}
    for spec in specs:
        by_cat.setdefault(spec.category or "general", []).append(spec)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "# GeoSI Tool Registry — Live Documentation",
        "",
        f"Auto-generated from the live `ToolRegistry`. **{len(specs)} tools** "
        f"across **{len(by_cat)} categories**.",
        "",
        "Each tool's `tool_name` below is the exact identifier the planner must "
        "emit and the executor resolves. Use the example `ToolStep` JSON as the "
        "grounding template.",
        "",
        "## Categories",
        "",
    ]

    total = 0
    for category in sorted(by_cat):
        cat_specs = sorted(by_cat[category], key=lambda s: s.name)
        fname = _CATEGORY_FILES.get(category, f"{category}.md")
        header = [
            f"# {category.replace('_', ' ').title()} Tools",
            "",
            f"{len(cat_specs)} tool(s) in category `{category}`.",
            "",
        ]
        body = [_render_tool(s, full_help) for s in cat_specs]
        (out / fname).write_text("\n".join(header + body), encoding="utf-8")
        index_lines.append(f"- [{category}](./{fname}) — {len(cat_specs)} tool(s)")
        total += len(cat_specs)
        logger.info("Wrote %s (%d tools)", fname, len(cat_specs))

    (out / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    logger.info("Documentation written to %s (%d tools)", out, total)
    return total


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate GeoSI live-registry documentation (QGIS required)."
    )
    parser.add_argument("--out", default="data/registry_docs/",
                        help="Output directory for generated Markdown.")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    # Fail-closed on missing QGIS — no fake docs.
    try:
        import qgis.core  # noqa: F401
    except Exception:
        logger.error(
            "qgis.core is not importable. This generator must run inside a "
            "QGIS-enabled Python interpreter (set QT_QPA_PLATFORM=offscreen "
            "for headless). Aborting without writing any docs."
        )
        return 2

    count = generate(args.out)
    return 0 if count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
