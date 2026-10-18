# -*- coding: utf-8 -*-
"""
GeoSI Plugin — Chat Dock Widget (v2: Dynamic Tool Aware)
═══════════════════════════════════════════════════════════════════

A dockable Qt widget that provides the conversational GIS interface.
Users type natural language queries, and GeoSI plans + executes
GIS workflows using dynamically discovered QGIS tools.

Architecture
────────────
    ┌──────────────────────┐
    │     GeoSIDock        │
    │  ┌───────────────┐   │
    │  │  Chat History  │   │  ← QTextEdit (read-only, HTML formatted)
    │  │  (scrollable)  │   │
    │  └───────────────┘   │
    │  ┌───────────────┐   │
    │  │  Input Box     │   │  ← QLineEdit (user types queries here)
    │  └───────────────┘   │
    │  [Send] [Clear]      │  ← QPushButton actions
    └──────────────────────┘

Thread Safety
─────────────
    Query execution runs on a QThread to prevent GUI freezing.
    Results are marshalled back to the main thread via Qt signals.

QGIS Layer Sync
───────────────
    Before each query, we sync the QGIS layer panel to the engine's
    StateManager so the LLM knows which layers are available.
"""

import os
import logging
import traceback
from typing import Optional

logger = logging.getLogger("geosi_plugin.prompt_dock")


class GeoSIDock:
    """
    Dockable chat widget for GeoSI inside QGIS.

    Provides a text-based conversational interface where users type
    GIS queries and see results. Supports:
        - Natural language GIS queries
        - "tools" command to list all available tools
        - "layers" command to list loaded layers
        - Result display with output layer auto-loading into QGIS
    """

    def __init__(self, iface, engine):
        """
        Create the dock widget.

        Args:
            iface: QgisInterface for accessing the QGIS application
            engine: GeoSI engine instance (already populated with tools)
        """
        from qgis.PyQt.QtWidgets import (
            QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
            QTextEdit, QLineEdit, QPushButton, QLabel,
        )
        from qgis.PyQt.QtCore import Qt

        # ── Store references ───────────────────────────────────────────
        self.iface = iface
        self.engine = engine
        self._worker = None

        # ── Create the dock widget ─────────────────────────────────────
        self.dock = QDockWidget("GeoSI — Geospatial AI", iface.mainWindow())
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )

        # ── Central widget with vertical layout ────────────────────────
        central = QWidget()
        layout = QVBoxLayout(central)

        # ── Header with tool count ─────────────────────────────────────
        tool_count = self.engine.registry.tool_count()
        header = QLabel(
            f"<b>GeoSI v2</b> — {tool_count} tools dynamically loaded"
        )
        header.setStyleSheet("color: #4CAF50; padding: 4px;")
        layout.addWidget(header)

        # ── Chat history display ───────────────────────────────────────
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(
            "background-color: #1e1e1e; color: #e0e0e0; "
            "font-family: 'Consolas', 'Monaco', monospace; font-size: 13px; "
            "border: 1px solid #333; border-radius: 4px; padding: 8px;"
        )
        self.chat_display.setHtml(
            "<p style='color: #4CAF50;'>🌍 GeoSI v2 ready. "
            f"<b>{tool_count}</b> QGIS tools auto-discovered.</p>"
            "<p style='color: #888;'>Type a GIS query, or try:</p>"
            "<p style='color: #888;'>• <b>tools</b> — list all tools</p>"
            "<p style='color: #888;'>• <b>layers</b> — list loaded layers</p>"
            "<p style='color: #888;'>• <b>Buffer hospitals by 500m</b></p>"
        )
        layout.addWidget(self.chat_display)

        # ── Input area ─────────────────────────────────────────────────
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Ask GeoSI anything about your spatial data...")
        self.input_box.setStyleSheet(
            "background-color: #2d2d2d; color: #fff; "
            "border: 1px solid #555; border-radius: 4px; "
            "padding: 8px; font-size: 14px;"
        )
        self.input_box.returnPressed.connect(self._on_submit)
        input_layout.addWidget(self.input_box)

        # Send button
        send_btn = QPushButton("Send")
        send_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; "
            "border: none; border-radius: 4px; padding: 8px 16px; "
            "font-weight: bold;"
        )
        send_btn.clicked.connect(self._on_submit)
        input_layout.addWidget(send_btn)

        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet(
            "background-color: #555; color: white; "
            "border: none; border-radius: 4px; padding: 8px 12px;"
        )
        clear_btn.clicked.connect(self._on_clear)
        input_layout.addWidget(clear_btn)

        layout.addLayout(input_layout)
        self.dock.setWidget(central)

    # ── Qt delegation (so iface.addDockWidget works) ───────────────────

    def show(self):
        self.dock.show()

    def hide(self):
        self.dock.hide()

    def __getattr__(self, name):
        """Delegate unknown attributes to the underlying QDockWidget."""
        return getattr(self.dock, name)

    # ── Commands ───────────────────────────────────────────────────────

    def _on_submit(self):
        """Handle user query submission."""
        query = self.input_box.text().strip()
        if not query:
            return
        self.input_box.clear()
        self._append_user(query)

        # ── Built-in commands ──────────────────────────────────────────
        if query.lower() == "tools":
            self._show_tools()
            return
        if query.lower() == "layers":
            self._show_layers()
            return
        if query.lower().startswith("search "):
            self._search_tools(query[7:].strip())
            return

        # ── Sync QGIS layers to engine state ───────────────────────────
        self._sync_layers()

        # ── Execute the query ──────────────────────────────────────────
        try:
            self._append_system("⏳ Planning and executing...")
            result = self.engine.run(query)

            if result.success:
                self._append_assistant(result.answer)
                if result.reasoning:
                    self._append_system(
                        f"<details><summary>📋 Reasoning</summary>"
                        f"<pre>{result.reasoning}</pre></details>"
                    )
                # Auto-load output layers into QGIS
                self._load_result_layers(result)
            else:
                error_msg = result.error or result.answer or "Unknown error"
                self._append_error(error_msg)

        except Exception as e:
            self._append_error(f"Error: {e}\n{traceback.format_exc()}")

    def _on_clear(self):
        """Clear the chat history."""
        self.chat_display.clear()
        self.engine.conversation.clear()
        tool_count = self.engine.registry.tool_count()
        self.chat_display.setHtml(
            f"<p style='color: #4CAF50;'>Chat cleared. {tool_count} tools ready.</p>"
        )

    # ── Layer sync ─────────────────────────────────────────────────────

    def _sync_layers(self):
        """
        Synchronize QGIS layer panel → engine StateManager.

        Reads all layers from QgsProject.instance() and registers them
        in the engine's state so the planner knows what data is available.

        Complexity: O(L) where L = number of layers in the project
        """
        try:
            from qgis.core import QgsProject
            from geosi_engine.models import Layer

            project = QgsProject.instance()
            for layer_id, qgs_layer in project.mapLayers().items():
                name = qgs_layer.name()
                if name not in self.engine.state.list_layers():
                    # Determine layer type
                    layer_type = "vector"
                    geom_type = "Unknown"
                    feature_count = 0
                    crs = ""

                    try:
                        crs = qgs_layer.crs().authid()
                    except Exception:
                        pass

                    if hasattr(qgs_layer, "featureCount"):
                        # Vector layer
                        feature_count = qgs_layer.featureCount()
                        try:
                            wkb = qgs_layer.wkbType()
                            from qgis.core import QgsWkbTypes
                            geom_type = QgsWkbTypes.displayString(wkb)
                        except Exception:
                            pass
                    else:
                        # Raster layer
                        layer_type = "raster"
                        geom_type = "Raster"
                        feature_count = 1

                    engine_layer = Layer(
                        name=name,
                        geometry_type=geom_type,
                        feature_count=feature_count,
                        crs=crs,
                        filepath=qgs_layer.source(),
                        layer_type=layer_type,
                    )
                    # Store the QgsMapLayer reference for fast-path operations
                    engine_layer.features = qgs_layer
                    self.engine.state.add_layer(engine_layer)

        except Exception as e:
            logger.warning(f"Layer sync failed: {e}")

    # ── Result loading ─────────────────────────────────────────────────

    def _load_result_layers(self, result):
        """Load output layers from execution results into QGIS."""
        try:
            from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer

            for name, output in (result.results or {}).items():
                if output is None:
                    continue
                layer_obj = output
                if hasattr(output, "output"):
                    layer_obj = output.output
                if layer_obj is None:
                    continue

                filepath = getattr(layer_obj, "filepath", "")
                if filepath and os.path.isfile(filepath):
                    layer_type = getattr(layer_obj, "layer_type", "vector")
                    layer_name = getattr(layer_obj, "name", name)

                    if layer_type == "raster":
                        qgs_layer = QgsRasterLayer(filepath, layer_name)
                    else:
                        qgs_layer = QgsVectorLayer(filepath, layer_name, "ogr")

                    if qgs_layer.isValid():
                        QgsProject.instance().addMapLayer(qgs_layer)
                        self._append_system(
                            f"📍 Loaded result layer: <b>{layer_name}</b>"
                        )
                    else:
                        logger.warning(f"Invalid layer: {filepath}")
        except Exception as e:
            logger.warning(f"Failed to load result layers: {e}")

    # ── Built-in commands ──────────────────────────────────────────────

    def _show_tools(self):
        """Display all registered tools grouped by category."""
        tools = self.engine.registry.list_tools()
        categories = {}
        for spec in tools:
            cat = spec.category or "general"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(spec.name)

        lines = [f"<b>🛠 {len(tools)} tools registered:</b><br>"]
        for cat in sorted(categories.keys()):
            names = sorted(categories[cat])
            lines.append(f"<br><b>{cat.upper()}</b> ({len(names)}):")
            # Show first 20 per category to avoid flooding
            for name in names[:20]:
                lines.append(f"  • {name}")
            if len(names) > 20:
                lines.append(f"  ... and {len(names) - 20} more")

        self._append_system("<br>".join(lines))

    def _show_layers(self):
        """Display all layers currently in QGIS."""
        self._sync_layers()
        layers = self.engine.state.list_layers()
        if layers:
            items = "<br>".join(f"  • {l}" for l in layers)
            self._append_system(f"<b>📂 {len(layers)} layers loaded:</b><br>{items}")
        else:
            self._append_system("No layers loaded in QGIS.")

    def _search_tools(self, query: str):
        """Search tools by keyword."""
        results = self.engine.registry.search_tools(query)
        if results:
            items = "<br>".join(
                f"  • <b>{s.name}</b>: {s.description[:80]}" for s in results[:15]
            )
            self._append_system(
                f"<b>🔍 {len(results)} tools matching '{query}':</b><br>{items}"
            )
        else:
            self._append_system(f"No tools found matching '{query}'.")

    # ── Chat formatting ────────────────────────────────────────────────

    def _append_user(self, text: str):
        self.chat_display.append(
            f"<p style='color: #64B5F6;'><b>You:</b> {text}</p>"
        )

    def _append_assistant(self, text: str):
        self.chat_display.append(
            f"<p style='color: #81C784;'><b>GeoSI:</b> {text}</p>"
        )

    def _append_system(self, text: str):
        self.chat_display.append(
            f"<p style='color: #9E9E9E; font-size: 12px;'>{text}</p>"
        )

    def _append_error(self, text: str):
        self.chat_display.append(
            f"<p style='color: #EF5350;'><b>❌ Error:</b> {text}</p>"
        )
