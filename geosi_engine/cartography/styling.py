# -*- coding: utf-8 -*-
"""
GeoSI — Automated Symbology & Labeling
════════════════════════════════════════════════════════════════════
Apply professional cartographic styles to QGIS layers from code.

All functions are QGIS-aware and degrade gracefully if not running
inside QGIS (they log a warning and return False).
"""
from __future__ import annotations

import logging
from typing import Any, List, Optional

logger = logging.getLogger("geosi_engine.cartography.styling")

# Standard diverging/sequential color ramps available in all QGIS installs
RAMPS = {
    "viridis": "Viridis", "magma": "Magma", "plasma": "Plasma",
    "blues": "Blues", "reds": "Reds", "greens": "Greens",
    "rdylgn": "RdYlGn", "spectral": "Spectral",
    "rdbu": "RdBu", "piyg": "PiYG",
    "ylgnbu": "YlGnBu", "ylorbr": "YlOrBr",
}

METHODS = {
    "quantile": "quantile",
    "jenks": "jenks",
    "natural_breaks": "jenks",
    "equal": "equal",
    "equal_interval": "equal",
    "standard_deviation": "stddev",
    "pretty": "pretty",
}


def apply_graduated_symbology(
    layer: Any,
    field: str,
    classes: int = 5,
    ramp: str = "viridis",
    method: str = "quantile",
    opacity: float = 1.0,
) -> bool:
    """
    Apply a graduated (choropleth) symbology to *layer* based on *field*.

    Parameters
    ----------
    layer : QgsVectorLayer
    field : str        — numeric field to classify
    classes : int      — number of classes (2–20)
    ramp : str         — color ramp name (viridis, blues, reds, …)
    method : str       — classification method (quantile, jenks, equal)
    opacity : float    — layer opacity 0–1

    Returns True on success.
    """
    try:
        from qgis.core import (
            QgsGraduatedSymbolRenderer,
            QgsClassificationQuantile,
            QgsClassificationJenks,
            QgsClassificationEqualInterval,
            QgsClassificationStdDev,
            QgsStyle,
            QgsSymbol,
        )

        style = QgsStyle.defaultStyle()
        ramp_name = RAMPS.get(ramp.lower(), ramp)
        color_ramp = style.colorRamp(ramp_name)
        if color_ramp is None:
            logger.warning("Color ramp %r not found — using Viridis", ramp_name)
            color_ramp = style.colorRamp("Viridis")

        method_key = METHODS.get(method.lower(), "quantile")
        classification_map = {
            "quantile": QgsClassificationQuantile,
            "jenks":    QgsClassificationJenks,
            "equal":    QgsClassificationEqualInterval,
            "stddev":   QgsClassificationStdDev,
        }
        classifier = classification_map.get(method_key, QgsClassificationQuantile)()

        renderer = QgsGraduatedSymbolRenderer(field)
        renderer.setClassificationMethod(classifier)
        renderer.setSourceColorRamp(color_ramp)
        renderer.updateClasses(layer, classes)

        layer.setRenderer(renderer)
        layer.setOpacity(opacity)
        layer.triggerRepaint()

        logger.info("Graduated symbology applied: %s → %s (%d classes, %s)",
                    layer.name(), field, classes, ramp)
        return True

    except ImportError:
        logger.warning("QGIS not available — graduated symbology skipped")
        return False
    except Exception as exc:
        logger.error("apply_graduated_symbology failed: %s", exc)
        return False


def apply_categorized_symbology(
    layer: Any,
    field: str,
    palette: Optional[List[str]] = None,
    opacity: float = 1.0,
) -> bool:
    """
    Apply a categorized (qualitative) symbology to *layer* based on *field*.

    Each unique value in *field* gets a distinct color. If *palette* is None,
    uses QGIS's default random colours or the 'Paired' ColorBrewer ramp.
    """
    try:
        from qgis.core import (
            QgsCategorizedSymbolRenderer,
            QgsRendererCategory,
            QgsSymbol,
            QgsStyle,
        )

        # Collect unique values
        idx = layer.fields().indexFromName(field)
        if idx < 0:
            logger.warning("Field %r not found in %s", field, layer.name())
            return False

        values = sorted({f[field] for f in layer.getFeatures() if f[field] is not None})
        if not values:
            return False

        # Build color list
        if palette:
            colors = palette
        else:
            style = QgsStyle.defaultStyle()
            ramp = style.colorRamp("Paired") or style.colorRamp("Spectral")
            colors = []
            for i, _ in enumerate(values):
                t = i / max(len(values) - 1, 1)
                c = ramp.color(t) if ramp else None
                colors.append(c.name() if c else "#aaaaaa")

        cats = []
        geom_type = layer.geometryType()  # 0=Point, 1=Line, 2=Polygon
        for i, val in enumerate(values):
            sym = QgsSymbol.defaultSymbol(geom_type)
            color = colors[i % len(colors)]
            if isinstance(color, str):
                from qgis.PyQt.QtGui import QColor
                sym.setColor(QColor(color))
            else:
                sym.setColor(color)
            cats.append(QgsRendererCategory(val, sym, str(val)))

        renderer = QgsCategorizedSymbolRenderer(field, cats)
        layer.setRenderer(renderer)
        layer.setOpacity(opacity)
        layer.triggerRepaint()

        logger.info("Categorized symbology: %s → %s (%d categories)",
                    layer.name(), field, len(values))
        return True

    except ImportError:
        logger.warning("QGIS not available — categorized symbology skipped")
        return False
    except Exception as exc:
        logger.error("apply_categorized_symbology failed: %s", exc)
        return False


def apply_labeling(
    layer: Any,
    field: str,
    font_size: int = 9,
    halo: bool = True,
    bold: bool = False,
) -> bool:
    """
    Apply rule-based labeling to *layer* using *field*.

    Adds a white text halo for legibility by default.
    """
    try:
        from qgis.core import (
            QgsPalLayerSettings,
            QgsTextFormat,
            QgsTextBufferSettings,
            QgsVectorLayerSimpleLabeling,
        )
        from qgis.PyQt.QtGui import QFont, QColor

        text_format = QgsTextFormat()
        font = QFont("Arial", font_size)
        font.setBold(bold)
        text_format.setFont(font)
        text_format.setSize(font_size)
        text_format.setColor(QColor("#111111"))

        if halo:
            buffer = QgsTextBufferSettings()
            buffer.setEnabled(True)
            buffer.setSize(1.0)
            buffer.setColor(QColor("white"))
            text_format.setBuffer(buffer)

        pal = QgsPalLayerSettings()
        pal.fieldName = field
        pal.setFormat(text_format)
        pal.enabled = True

        layer.setLabeling(QgsVectorLayerSimpleLabeling(pal))
        layer.setLabelsEnabled(True)
        layer.triggerRepaint()

        logger.info("Labels applied: %s → %s (size=%d)", layer.name(), field, font_size)
        return True

    except ImportError:
        logger.warning("QGIS not available — labeling skipped")
        return False
    except Exception as exc:
        logger.error("apply_labeling failed: %s", exc)
        return False


def apply_raster_pseudocolor(
    layer: Any,
    ramp: str = "viridis",
    n_classes: int = 10,
    band: int = 1,
) -> bool:
    """
    Apply a pseudocolor renderer to a raster layer.

    Good for DEMs, NDVI outputs, and any single-band raster.
    """
    try:
        from qgis.core import (
            QgsSingleBandPseudoColorRenderer,
            QgsRasterShader,
            QgsColorRampShader,
            QgsStyle,
        )

        style = QgsStyle.defaultStyle()
        ramp_name = RAMPS.get(ramp.lower(), ramp)
        color_ramp = style.colorRamp(ramp_name) or style.colorRamp("Viridis")

        stats = layer.dataProvider().bandStatistics(band)
        mn, mx = stats.minimumValue, stats.maximumValue

        shader_func = QgsColorRampShader(mn, mx, color_ramp, QgsColorRampShader.Interpolated)
        shader_func.setClassificationMode(QgsColorRampShader.Quantile)
        shader_func.classifyColorRamp(n_classes)

        shader = QgsRasterShader()
        shader.setRasterShaderFunction(shader_func)

        renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), band, shader)
        layer.setRenderer(renderer)
        layer.triggerRepaint()

        logger.info("Pseudocolor applied: %s (band %d, %s)", layer.name(), band, ramp)
        return True

    except ImportError:
        logger.warning("QGIS not available — raster pseudocolor skipped")
        return False
    except Exception as exc:
        logger.error("apply_raster_pseudocolor failed: %s", exc)
        return False
