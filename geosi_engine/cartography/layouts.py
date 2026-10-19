# -*- coding: utf-8 -*-
"""
GeoSI — Print Layout Generator
════════════════════════════════════════════════════════════════════
Programmatically build a QGIS Print Layout (map + legend + scale bar
+ north arrow + title) and export to PDF or PNG.

Usage:
    from geosi_engine.cartography.layouts import build_print_layout, export_layout

    layout = build_print_layout(project, title="Flood Risk Zones")
    export_layout(layout, "flood_map.pdf")
"""
from __future__ import annotations

import logging
import os
from typing import Any, Optional

logger = logging.getLogger("geosi_engine.cartography.layouts")

PAGE_SIZES = {
    "a4":  (297, 210),   # landscape (w, h) in mm
    "a3":  (420, 297),
    "a2":  (594, 420),
    "letter": (279, 216),
    "legal":  (356, 216),
}


def build_print_layout(
    project: Any = None,
    title: str = "GeoSI Map",
    orientation: str = "landscape",
    page_size: str = "a4",
    include_legend: bool = True,
    include_scale_bar: bool = True,
    include_north_arrow: bool = True,
    include_title: bool = True,
    extent: Any = None,   # QgsRectangle; None = project extent
) -> Optional[Any]:
    """
    Build a print layout and return the QgsPrintLayout object.

    Parameters
    ----------
    project : QgsProject, optional
    title : str
    orientation : "landscape" | "portrait"
    page_size : "a4" | "a3" | "a2" | "letter" | "legal"
    include_legend / include_scale_bar / include_north_arrow / include_title : bool
    extent : QgsRectangle, optional  — override the map frame extent

    Returns the QgsPrintLayout, or None if QGIS is unavailable.
    """
    try:
        from qgis.core import (
            QgsProject, QgsPrintLayout, QgsLayoutSize, QgsUnitTypes,
            QgsLayoutItemMap, QgsLayoutItemLegend, QgsLayoutItemScaleBar,
            QgsLayoutItemLabel,
        )
        from qgis.PyQt.QtCore import QRectF
        from qgis.PyQt.QtGui import QFont
    except ImportError:
        logger.warning("QGIS not available — build_print_layout skipped")
        return None

    if project is None:
        project = QgsProject.instance()

    # ── Page setup ─────────────────────────────────────────────────────
    w_mm, h_mm = PAGE_SIZES.get(page_size.lower(), (297, 210))
    if orientation.lower() == "portrait":
        w_mm, h_mm = min(w_mm, h_mm), max(w_mm, h_mm)
    else:
        w_mm, h_mm = max(w_mm, h_mm), min(w_mm, h_mm)

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(title)

    page = layout.pageCollection().pages()[0]
    page.setPageSize(
        QgsLayoutSize(w_mm, h_mm, QgsUnitTypes.LayoutMillimeters)
    )

    # ── Map frame ──────────────────────────────────────────────────────
    margin = 10          # mm
    legend_w = 45 if include_legend else 0
    map_w = w_mm - 2 * margin - legend_w
    map_h = h_mm - 2 * margin - (15 if include_title else 0) - (12 if include_scale_bar else 0)

    map_item = QgsLayoutItemMap(layout)
    map_item.setRect(QRectF(0, 0, map_w, map_h))
    map_item.attemptSetSceneRect(QRectF(margin, margin + (15 if include_title else 0), map_w, map_h))
    layout.addLayoutItem(map_item)

    if extent:
        map_item.setExtent(extent)
    elif project.viewSettings():
        try:
            map_item.zoomToExtent(project.viewSettings().defaultViewExtent())
        except Exception:
            logger.debug("suppressed exception", exc_info=True)

    map_item.refresh()

    # ── Title ──────────────────────────────────────────────────────────
    if include_title:
        title_item = QgsLayoutItemLabel(layout)
        title_item.setText(title)
        title_item.setFont(QFont("Arial", 14, QFont.Bold))
        title_item.attemptSetSceneRect(QRectF(margin, margin, w_mm - 2 * margin, 12))
        layout.addLayoutItem(title_item)

    # ── Legend ─────────────────────────────────────────────────────────
    if include_legend:
        legend = QgsLayoutItemLegend(layout)
        legend.setLinkedMap(map_item)
        legend.setTitle("Legend")
        legend.attemptSetSceneRect(
            QRectF(margin + map_w + 5, margin + (15 if include_title else 0),
                   legend_w - 5, map_h)
        )
        layout.addLayoutItem(legend)

    # ── Scale bar ──────────────────────────────────────────────────────
    if include_scale_bar:
        scale = QgsLayoutItemScaleBar(layout)
        scale.setLinkedMap(map_item)
        scale.setStyle("Single Box")
        scale.setNumberOfSegments(4)
        scale.setUnitsPerSegment(1000)
        scale.applyDefaultSize()
        scale.attemptSetSceneRect(
            QRectF(margin, h_mm - margin - 10, 60, 8)
        )
        layout.addLayoutItem(scale)

    # ── North arrow ────────────────────────────────────────────────────
    if include_north_arrow:
        try:
            from qgis.core import QgsLayoutItemPicture
            arrow = QgsLayoutItemPicture(layout)
            # Use QGIS built-in north arrow SVG
            from qgis.core import QgsApplication
            # pkgDataPath() resolves the install dir on Windows, macOS and Linux
            svg = os.path.join(QgsApplication.pkgDataPath(), "svg", "arrows", "NorthArrow_04.svg")
            arrow.setPicturePath(svg)
            arrow.attemptSetSceneRect(QRectF(w_mm - margin - 15, h_mm - margin - 20, 12, 18))
            layout.addLayoutItem(arrow)
        except Exception as exc:
            logger.debug("North arrow skipped: %s", exc)

    logger.info("Print layout %r built (%s %s %.0fx%.0fmm)",
                title, orientation, page_size, w_mm, h_mm)
    return layout


def export_layout(
    layout: Any,
    output_path: str,
    fmt: str = "pdf",
    dpi: int = 300,
) -> bool:
    """
    Export a QgsPrintLayout to PDF or PNG.

    Parameters
    ----------
    layout : QgsPrintLayout
    output_path : str  — full path including extension
    fmt : "pdf" | "png" | "svg"
    dpi : int

    Returns True on success.
    """
    try:
        from qgis.core import (
            QgsLayoutExporter,
        )

        exporter = QgsLayoutExporter(layout)

        fmt = fmt.lower()
        if fmt == "png":
            settings = QgsLayoutExporter.ImageExportSettings()
            settings.dpi = dpi
            result = exporter.exportToImage(output_path, settings)
        elif fmt == "svg":
            settings = QgsLayoutExporter.SvgExportSettings()
            result = exporter.exportToSvg(output_path, settings)
        else:  # pdf
            settings = QgsLayoutExporter.PdfExportSettings()
            settings.dpi = dpi
            result = exporter.exportToPdf(output_path, settings)

        ok = result == QgsLayoutExporter.Success
        if ok:
            logger.info("Layout exported to %s (%s, %d dpi)", output_path, fmt, dpi)
        else:
            logger.error("Layout export failed (code %d) → %s", result, output_path)
        return ok

    except ImportError:
        logger.warning("QGIS not available — layout export skipped")
        return False
    except Exception as exc:
        logger.error("export_layout failed: %s", exc)
        return False
