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
    Queries run as a QgsTask (QGIS task manager) so the GUI never freezes.
    The task's on_finished callback runs on the main thread, which is
    where result layers are added to the project. Stop cancels the task;
    the agent loop stops before its next attempt.

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
        self._task = None
        # Run queries as a QgsTask so QGIS stays responsive. Tests that need
        # the result synchronously set this to False.
        self.run_in_background = True

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
        send_btn = self.send_btn = QPushButton("Send")
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

        # Stop button (enabled while a request is running)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet(
            "background-color: #b33; color: white; "
            "border: none; border-radius: 4px; padding: 8px 12px;"
        )
        self.stop_btn.clicked.connect(self._on_stop)
        input_layout.addWidget(self.stop_btn)

        settings_btn = QPushButton("⚙")
        settings_btn.setToolTip("GeoSI settings (models, Ollama URL, retries)")
        settings_btn.setStyleSheet("border: none; padding: 8px 6px; font-size: 16px;")
        settings_btn.clicked.connect(self._on_settings)
        input_layout.addWidget(settings_btn)

        layout.addLayout(input_layout)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #aaa; padding: 2px;")
        layout.addWidget(self.status_label)
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

        if self._task is not None:
            self._append_system("⏳ Still working on the previous request — press Stop to cancel it.")
            return

        # ── Sync QGIS layers to engine state (main thread) ─────────────
        self._sync_layers()
        self._append_system("⏳ Planning and executing...")

        if not self.run_in_background:
            self._show_result(*self._run_query(query))
            return

        # ── Run plan → execute → verify in a QGIS background task ──────
        # The worker only touches files and the engine; result layers are
        # added to the project back on the main thread in _on_task_done.
        from qgis.core import QgsApplication, QgsTask

        task = QgsTask.fromFunction(
            f"GeoSI: {query[:50]}", self._task_body, query, on_finished=self._on_task_done
        )
        self._task = task
        task.progressChanged.connect(self._on_progress)
        self._set_busy(True)
        QgsApplication.taskManager().addTask(task)

    def _run_query(self, query, task=None):
        """Run the engine; returns (result, error_text). Safe off the main thread."""
        loop = getattr(self.engine, "loop", None)
        if loop is not None:
            loop.should_stop = task.isCanceled if task is not None else (lambda: False)
            loop.on_progress = task.setProgress if task is not None else None
        try:
            return self.engine.run(query), None
        except Exception as e:
            return None, f"Error: {e}\n{traceback.format_exc()}"

    def _task_body(self, task, query):
        return self._run_query(query, task)

    def _on_task_done(self, exception, value=None):
        self._task = None
        self._set_busy(False)
        if exception is not None:
            self._append_error(f"Error: {exception}")
            return
        if value is None:
            self._append_system("⏹ Stopped.")
            return
        self._show_result(*value)

    def _on_progress(self, pct):
        self.status_label.setText(f"Working… {pct:.0f}%")

    def _on_stop(self):
        if self._task is not None:
            self._task.cancel()
            self.status_label.setText("Stopping after the current step…")

    def _on_settings(self):
        from .settings import SettingsDialog, apply

        dlg = SettingsDialog(self.dock)
        if dlg.exec_():
            apply(self.engine, dlg.values)
            agent = self.engine.agent
            model = agent._api_model if agent._api_configured() else agent._ollama_model
            where = "hosted API" if agent._api_configured() else "local Ollama"
            self._append_system(f"⚙ Settings saved — planning with <b>{model}</b> ({where})")

    def _set_busy(self, busy):
        self.stop_btn.setEnabled(busy)
        self.send_btn.setEnabled(not busy)
        self.status_label.setText("Working…" if busy else "")

    def _show_result(self, result, error):
        if error:
            self._append_error(error)
            return
        if result.success:
            self._append_assistant(result.answer)
            if result.reasoning:
                self._append_system(
                    f"<details><summary>📋 Reasoning</summary>"
                    f"<pre>{result.reasoning}</pre></details>"
                )
            # Auto-load output layers into QGIS (main thread)
            self._load_result_layers(result)
        else:
            self._append_error(result.answer or result.error or "Unknown error")
            if result.reasoning:
                self._append_system(
                    f"<details><summary>📋 What was tried</summary>"
                    f"<pre>{result.reasoning}</pre></details>"
                )

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

                    fields, field_types, field_values = [], {}, {}
                    if layer_type == "vector":
                        try:
                            from .qgis_bridge import field_metadata
                            fields = [f.name() for f in qgs_layer.fields()]
                            field_types, field_values = field_metadata(qgs_layer)
                        except Exception:
                            pass
                    engine_layer = Layer(
                        name=name,
                        geometry_type=geom_type,
                        feature_count=feature_count,
                        crs=crs,
                        filepath=qgs_layer.source().split("|")[0],
                        layer_type=layer_type,
                        fields=fields,
                        field_types=field_types,
                        field_values=field_values,
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
