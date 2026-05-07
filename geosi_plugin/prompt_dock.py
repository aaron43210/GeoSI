# -*- coding: utf-8 -*-
"""
GeoSI - Prompt Dock Widget (powered by geosi_engine)

A conversational panel inside QGIS that sends natural-language GIS
questions to the universal engine. This module is the only part of
GeoSI that imports QGIS. The engine itself stays framework-free.

Design rules enforced here:

    * Only layers currently loaded in the QGIS Layers panel are usable.
      If the user asks for a layer that is not loaded, the dock replies
      with a clear "Layer not found" message and lists what is loaded.
    * Ollama is the first-choice LLM. The settings panel lets the user
      point GeoSI at any local Ollama endpoint and pick the model.
      Cloud keys (Claude / Gemini) are optional fallbacks.
    * The chat stays interactive: every turn is timestamped, the input
      is cleared after each send, and long responses wrap cleanly.
"""

import os
import datetime

from qgis.PyQt.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QHBoxLayout, QLabel, QComboBox,
)
from qgis.PyQt.QtCore import Qt, QThread, pyqtSignal
from qgis.core import QgsSettings, QgsProject


# ---------------------------------------------------------------------------
# Qt5 / Qt6 compatibility helpers
# ---------------------------------------------------------------------------

def _resolve_dock_area(name):
    area = getattr(Qt, name, None)
    if area is not None:
        return area
    dock_area_enum = getattr(Qt, "DockWidgetArea", None)
    if dock_area_enum is not None:
        return getattr(dock_area_enum, name, None)
    return None


def _get_echo_mode_password():
    try:
        return QLineEdit.Password
    except AttributeError:
        try:
            return QLineEdit.EchoMode.Password
        except AttributeError:
            return None


# ---------------------------------------------------------------------------
# Background worker so the chat stays responsive while the engine runs
# ---------------------------------------------------------------------------

class _QueryWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, engine, query: str):
        super().__init__()
        self.engine = engine
        self.query = query

    def run(self):
        try:
            result = self.engine.query(self.query)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


# ---------------------------------------------------------------------------
# Main dock widget
# ---------------------------------------------------------------------------

class GeoSIDock(QDockWidget):
    """Conversational dock that wires the QGIS Layers panel to GeoSI."""

    def __init__(self, iface, parent=None):
        super().__init__("GeoSI - Geospatial Superintelligence", parent)
        self.iface = iface
        self.engine = None
        self._worker = None
        self._history = []  # [(role, text, timestamp)]

        left_area = _resolve_dock_area("LeftDockWidgetArea")
        right_area = _resolve_dock_area("RightDockWidgetArea")
        if left_area is not None and right_area is not None:
            self.setAllowedAreas(left_area | right_area)

        # -- Build UI --------------------------------------------------------
        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Header
        header_row = QHBoxLayout()
        header_lbl = QLabel("GeoSI - Geospatial Superintelligence")
        f = header_lbl.font(); f.setBold(True); f.setPointSize(11)
        header_lbl.setFont(f)
        header_row.addWidget(header_lbl)
        header_row.addStretch()

        self.reload_btn = QPushButton("Reload")
        self.reload_btn.setFixedWidth(70)
        self.reload_btn.setToolTip("Reload engine and re-sync QGIS layers")
        self.reload_btn.clicked.connect(self._init_engine)
        header_row.addWidget(self.reload_btn)

        self.llm_btn = QPushButton("LLM")
        self.llm_btn.setFixedWidth(50)
        self.llm_btn.setToolTip("Configure Ollama endpoint / model and API keys")
        self.llm_btn.clicked.connect(self._toggle_llm_panel)
        header_row.addWidget(self.llm_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedWidth(60)
        self.clear_btn.setToolTip("Clear chat history")
        self.clear_btn.clicked.connect(self._clear_chat)
        header_row.addWidget(self.clear_btn)
        layout.addLayout(header_row)

        # LLM configuration panel (hidden by default)
        self.llm_panel = QWidget()
        llm_layout = QVBoxLayout(self.llm_panel)
        llm_layout.setContentsMargins(0, 0, 0, 0)

        # Ollama row
        ollama_row = QHBoxLayout()
        ollama_row.addWidget(QLabel("Ollama URL:"))
        self.ollama_url = QLineEdit()
        self.ollama_url.setPlaceholderText("http://localhost:11434")
        ollama_row.addWidget(self.ollama_url)

        ollama_row.addWidget(QLabel("Model:"))
        self.ollama_model = QComboBox()
        self.ollama_model.setEditable(True)
        self.ollama_model.addItems([
            "mistral", "llama3", "llama3.1", "llama3.2",
            "qwen2.5", "codellama", "phi3", "gemma2",
        ])
        ollama_row.addWidget(self.ollama_model)
        llm_layout.addLayout(ollama_row)

        # Cloud key row (optional fallback)
        api_row = QHBoxLayout()
        api_row.addWidget(QLabel("Claude key (optional):"))
        self.api_input = QLineEdit()
        echo_mode = _get_echo_mode_password()
        if echo_mode is not None:
            self.api_input.setEchoMode(echo_mode)
        self.api_input.setPlaceholderText("sk-ant-... (leave blank if using Ollama)")
        api_row.addWidget(self.api_input)
        llm_layout.addLayout(api_row)

        # Save / test buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.test_btn = QPushButton("Test Ollama")
        self.test_btn.clicked.connect(self._test_ollama)
        btn_row.addWidget(self.test_btn)
        self.save_btn = QPushButton("Save and Reload")
        self.save_btn.clicked.connect(self._save_llm_config)
        btn_row.addWidget(self.save_btn)
        llm_layout.addLayout(btn_row)

        self.llm_panel.setVisible(False)
        layout.addWidget(self.llm_panel)

        # Chat display
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet(
            "background:#1e1e1e; color:#d4d4d4;"
            " font-family:Consolas,monospace; font-size:12px; padding:6px;"
        )
        layout.addWidget(self.chat)

        # Input row
        input_row = QHBoxLayout()
        self.prompt = QLineEdit()
        self.prompt.setPlaceholderText(
            "Ask a GIS question - e.g. 'Buffer hospitals by 500m'"
        )
        self.prompt.setStyleSheet("padding:6px; font-size:12px;")
        self.prompt.returnPressed.connect(self._run_query)
        input_row.addWidget(self.prompt)

        self.run_btn = QPushButton("Run")
        self.run_btn.setStyleSheet(
            "background:#007acc; color:white;"
            " padding:6px 14px; font-weight:bold;"
        )
        self.run_btn.clicked.connect(self._run_query)
        input_row.addWidget(self.run_btn)
        layout.addLayout(input_row)

        self.setWidget(self.main_widget)

        self._load_llm_config()
        self._init_engine()
        self._greet()

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def _load_llm_config(self):
        s = QgsSettings()
        url = s.value("GeoSI/ollama_endpoint", "http://localhost:11434")
        model = s.value("GeoSI/ollama_model", "mistral")
        key = s.value("GeoSI/anthropic_api_key", "")
        self.ollama_url.setText(url or "http://localhost:11434")
        idx = self.ollama_model.findText(model or "mistral")
        if idx >= 0:
            self.ollama_model.setCurrentIndex(idx)
        else:
            self.ollama_model.setEditText(model or "mistral")
        self.api_input.setText(key or "")
        os.environ["OLLAMA_ENDPOINT"] = url or "http://localhost:11434"
        os.environ["OLLAMA_MODEL"] = model or "mistral"
        if key:
            os.environ["ANTHROPIC_API_KEY"] = key

    def _save_llm_config(self):
        s = QgsSettings()
        url = self.ollama_url.text().strip() or "http://localhost:11434"
        model = self.ollama_model.currentText().strip() or "mistral"
        key = self.api_input.text().strip()
        s.setValue("GeoSI/ollama_endpoint", url)
        s.setValue("GeoSI/ollama_model", model)
        s.setValue("GeoSI/anthropic_api_key", key)
        os.environ["OLLAMA_ENDPOINT"] = url
        os.environ["OLLAMA_MODEL"] = model
        if key:
            os.environ["ANTHROPIC_API_KEY"] = key
        self.llm_panel.setVisible(False)
        self._msg(
            f"Saved. Ollama={url} model={model}. Reloading engine...",
            kind="success",
        )
        self._init_engine()

    def _toggle_llm_panel(self):
        self.llm_panel.setVisible(not self.llm_panel.isVisible())

    def _test_ollama(self):
        try:
            import urllib.request
            import json
            url = self.ollama_url.text().strip() or "http://localhost:11434"
            req = urllib.request.Request(f"{url}/api/tags")
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("name", "?") for m in data.get("models", [])]
            if models:
                self._msg(
                    f"Ollama OK at {url}. Installed models: {', '.join(models)}",
                    kind="success",
                )
            else:
                self._msg(
                    f"Ollama reachable at {url} but no models are installed. "
                    f"Run 'ollama pull mistral' in a terminal.",
                    kind="warn",
                )
        except Exception as exc:
            self._msg(
                f"Ollama is not reachable ({exc}). GeoSI will fall back to "
                f"Claude or keyword parsing.",
                kind="warn",
            )

    # ------------------------------------------------------------------
    # Engine lifecycle
    # ------------------------------------------------------------------

    def _init_engine(self):
        try:
            import sys
            for mod in [m for m in list(sys.modules) if m.startswith("geosi_engine")]:
                del sys.modules[mod]

            import geosi_engine
            self.engine = geosi_engine.GeoSI()

            tool_count = len(self.engine.registry.list_tools())
            self._msg(
                f"GeoSI Engine v{self.engine.version} ready - "
                f"{tool_count} tools loaded.",
                kind="success",
            )
            self._sync_qgis_layers(verbose=True)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            self._msg(f"Engine init failed: {e}", kind="error")

    def _greet(self):
        self._msg(
            "Welcome. Type any GIS question in plain English. "
            "GeoSI uses only the layers in your QGIS Layers panel. "
            "Type 'help' for examples, 'layers' to list loaded layers, "
            "or 'tools' to see tool categories.",
            kind="info",
        )

    # ------------------------------------------------------------------
    # Query dispatch
    # ------------------------------------------------------------------

    def _run_query(self):
        query = self.prompt.text().strip()
        if not query:
            return

        # Meta-commands (handled locally, never sent to the engine)
        lower = query.lower()
        if lower == "help":
            self._show_help()
            self.prompt.clear()
            return
        if lower == "layers":
            self._show_layers()
            self.prompt.clear()
            return
        if lower == "tools":
            self._show_tool_summary()
            self.prompt.clear()
            return
        if lower in {"clear", "cls"}:
            self._clear_chat()
            self.prompt.clear()
            return

        self._msg(query, kind="user")
        self.prompt.clear()

        if not self.engine:
            self._msg("Engine not ready. Click Reload.", kind="error")
            return

        # Refresh the layer list from QGIS right before every query so
        # users can load a new shapefile and ask about it immediately.
        loaded = self._sync_qgis_layers(verbose=False)
        if not loaded:
            self._msg(
                "No layers are loaded in the QGIS Layers panel. "
                "Add a vector or raster layer first (Layer -> Add Layer).",
                kind="warn",
            )
            return

        self.run_btn.setEnabled(False)
        self._msg("Thinking...", kind="info")

        self._worker = _QueryWorker(self.engine, query)
        self._worker.finished.connect(self._on_result)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_result(self, result: dict):
        self.run_btn.setEnabled(True)

        if not result.get("success"):
            self._msg(result.get("answer", "Failed."), kind="error")
            # Surface similar-layer suggestions from the agent
            if self.engine and hasattr(self.engine.agent, "layer_suggestions"):
                suggestions = self.engine.agent.layer_suggestions or []
                if suggestions:
                    self._msg("Did you mean one of these loaded layers?", kind="info")
                    for layer_name, score in suggestions[:5]:
                        self._msg(f"  - {layer_name}  ({score:.0%} match)", kind="info")
                else:
                    loaded = self.engine.state.list_layers()
                    if loaded:
                        self._msg(
                            "Layers currently in the QGIS Layers panel:\n  - "
                            + "\n  - ".join(loaded),
                            kind="info",
                        )
        else:
            self._msg(result.get("answer", "Done."), kind="success")

        if result.get("reasoning"):
            self._msg(result["reasoning"], kind="info")

    def _on_error(self, err: str):
        self.run_btn.setEnabled(True)
        self._msg(f"Error: {err}", kind="error")

    # ------------------------------------------------------------------
    # Layer sync - reads QGIS Layers panel only, no OSM auto-fetch
    # ------------------------------------------------------------------

    def _sync_qgis_layers(self, verbose: bool = False):
        if not self.engine:
            return []
        loaded_names = []
        try:
            from qgis.core import QgsMapLayer
            from geosi_engine.models import Layer

            project = QgsProject.instance()
            for layer_id, ql in project.mapLayers().items():
                name = ql.name()
                loaded_names.append(name)
                if self.engine.state.get_layer(name):
                    continue

                ltype = "raster" if ql.type() == QgsMapLayer.RasterLayer else "vector"
                geom_type = "Raster" if ltype == "raster" else "Unknown"
                try:
                    geom_type = ql.geometryType().name
                except Exception:
                    pass

                layer = Layer(
                    name=name,
                    geometry_type=geom_type,
                    feature_count=ql.featureCount() if ltype == "vector" else 1,
                    crs=ql.crs().authid(),
                    filepath=ql.source(),
                    layer_type=ltype,
                )
                layer.features = ql
                self.engine.state.add_layer(layer)

            if verbose:
                if loaded_names:
                    self._msg(
                        "Layers synced from QGIS: " + ", ".join(loaded_names),
                        kind="info",
                    )
                else:
                    self._msg(
                        "No layers in the QGIS Layers panel yet. Load one to start.",
                        kind="warn",
                    )
        except Exception as e:
            print(f"GeoSI: layer sync warning: {e}")
        return loaded_names

    # ------------------------------------------------------------------
    # Helpers for meta-commands
    # ------------------------------------------------------------------

    def _show_layers(self):
        loaded = self._sync_qgis_layers(verbose=False)
        if not loaded:
            self._msg(
                "No layers loaded. Open Layer -> Add Layer in QGIS.",
                kind="warn",
            )
            return
        rows = []
        for ln in loaded:
            layer_obj = self.engine.state.get_layer(ln) if self.engine else None
            if layer_obj:
                rows.append(
                    f"  - {ln}  ({layer_obj.layer_type}, "
                    f"{layer_obj.geometry_type}, "
                    f"{layer_obj.feature_count} features, {layer_obj.crs})"
                )
            else:
                rows.append(f"  - {ln}")
        self._msg("Loaded layers:\n" + "\n".join(rows), kind="info")

    def _show_tool_summary(self):
        if not self.engine:
            return
        by_cat = {}
        for spec in self.engine.registry.list_tools():
            by_cat.setdefault(spec.category or "other", []).append(spec.name)
        lines = ["Tool categories available:"]
        for cat, names in sorted(by_cat.items()):
            lines.append(f"  - {cat}: {len(names)} tools")
        lines.append("")
        lines.append(
            "Type a natural-language question; GeoSI selects the right tools."
        )
        self._msg("\n".join(lines), kind="info")

    def _show_help(self):
        loaded = self.engine.state.list_layers() if self.engine else []
        first = loaded[0] if loaded else "<your_layer>"
        second = loaded[1] if len(loaded) > 1 else "<another_layer>"
        examples = [
            f"Buffer {first} by 500 meters",
            f"Intersect {first} with {second}",
            f"Clip {first} to {second}",
            f"Dissolve {first} by name",
            f"Calculate slope from {first}  (raster)",
            f"Calculate NDVI from {first}  (raster with red+NIR bands)",
            f"Cluster {first} using DBSCAN with eps=200",
            f"Export {first} as GeoJSON",
            f"Count features in {first}",
            f"Find hotspots in {first}",
        ]
        msg = "Examples you can try:\n  - " + "\n  - ".join(examples)
        msg += "\n\nCommands: help | layers | tools | clear"
        msg += "\nConfiguration: click LLM to set Ollama endpoint or Claude key."
        self._msg(msg, kind="info")

    def _clear_chat(self):
        self.chat.clear()
        self._history.clear()
        self._greet()

    # ------------------------------------------------------------------
    # Chat rendering
    # ------------------------------------------------------------------

    def _msg(self, text: str, kind: str = "normal"):
        colors = {
            "user":    "#569cd6",
            "success": "#4ec9b0",
            "error":   "#f44747",
            "warn":    "#dcdcaa",
            "info":    "#9cdcfe",
            "normal":  "#d4d4d4",
        }
        color = colors.get(kind, "#d4d4d4")
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        role = "You" if kind == "user" else "GeoSI"
        self._history.append((role, text, ts))

        safe = (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>")
        )
        html = (
            f'<div style="margin-top:8px; color:{color};">'
            f'<span style="color:#6a9955;">[{ts}]</span> '
            f'<b>{role}:</b><br>{safe}'
            f'</div>'
        )
        self.chat.append(html)
        self.chat.verticalScrollBar().setValue(
            self.chat.verticalScrollBar().maximum()
        )
