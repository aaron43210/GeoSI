# -*- coding: utf-8 -*-
"""
GeoSI — Prompt Dock Widget (powered by geosi_engine)

"""

import os
import importlib

from qgis.PyQt.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QHBoxLayout, QLabel
)
from qgis.PyQt.QtCore import Qt, QThread, pyqtSignal
from qgis.core import QgsSettings, QgsProject


def _resolve_dock_area(name):
    """Return a Qt dock area constant compatible with Qt5/Qt6."""
    area = getattr(Qt, name, None)
    if area is not None:
        return area
    dock_area_enum = getattr(Qt, "DockWidgetArea", None)
    if dock_area_enum is not None:
        return getattr(dock_area_enum, name, None)
    return None


def _get_echo_mode_password():
    """Return QLineEdit.Password mode compatible with Qt5/Qt6."""
    try:
        # Qt5 style - direct class attribute
        return QLineEdit.Password
    except AttributeError:
        try:
            # Qt6 style - through EchoMode enum
            return QLineEdit.EchoMode.Password
        except AttributeError:
            # Fallback - return None (won't set password mode but won't crash)
            return None


class _QueryWorker(QThread):
    """Run a GeoSI query in a background thread to keep the UI responsive."""
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


class GeoSIDock(QDockWidget):
    """
    Main dock widget for the GeoSI QGIS plugin.

    Uses geosi_engine.GeoSI as the backend — the same engine shared
    with the FastAPI server. Loads layers from the current QGIS project
    and injects them into the engine's state before each query.
    """

    def __init__(self, iface, parent=None):
        super().__init__("🌍 GeoSI — Geospatial AI", parent)
        self.iface = iface
        self.engine = None
        self._worker = None

        left_area = _resolve_dock_area("LeftDockWidgetArea")
        right_area = _resolve_dock_area("RightDockWidgetArea")
        if left_area is not None and right_area is not None:
            self.setAllowedAreas(left_area | right_area)

        # ── Build UI ──────────────────────────────────────────────────
        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        # Header row
        header_row = QHBoxLayout()
        header_lbl = QLabel("🌍 GeoSI — Geospatial Superintelligence")
        f = header_lbl.font(); f.setBold(True); f.setPointSize(11)
        header_lbl.setFont(f)
        header_row.addWidget(header_lbl)
        header_row.addStretch()

        self.reload_btn = QPushButton("🔄")
        self.reload_btn.setFixedWidth(30)
        self.reload_btn.setToolTip("Reload engine")
        self.reload_btn.clicked.connect(self._init_engine)
        header_row.addWidget(self.reload_btn)

        self.api_btn = QPushButton("⚙️")
        self.api_btn.setFixedWidth(30)
        self.api_btn.setToolTip("Set Anthropic API key")
        self.api_btn.clicked.connect(self._toggle_api_panel)
        header_row.addWidget(self.api_btn)
        layout.addLayout(header_row)

        # API key panel (hidden by default)
        self.api_panel = QWidget()
        api_row = QHBoxLayout(self.api_panel)
        api_row.setContentsMargins(0, 0, 0, 0)
        api_row.addWidget(QLabel("🔑 Claude Key:"))
        self.api_input = QLineEdit()
        # Set password echo mode with Qt5/Qt6 compatibility
        echo_mode = _get_echo_mode_password()
        if echo_mode is not None:
            self.api_input.setEchoMode(echo_mode)
        self.api_input.setPlaceholderText("sk-ant-…")
        api_row.addWidget(self.api_input)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._save_api_key)
        api_row.addWidget(save_btn)
        self.api_panel.setVisible(False)
        layout.addWidget(self.api_panel)

        # Chat display
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet(
            "background:#1e1e1e; color:#d4d4d4;"
            " font-family:monospace; font-size:12px; padding:5px;"
        )
        layout.addWidget(self.chat)

        # Input row
        input_row = QHBoxLayout()
        self.prompt = QLineEdit()
        self.prompt.setPlaceholderText("e.g. Buffer hospitals by 500m …")
        self.prompt.setStyleSheet("padding:5px; font-size:12px;")
        self.prompt.returnPressed.connect(self._run_query)
        input_row.addWidget(self.prompt)

        self.run_btn = QPushButton("▶ Run")
        self.run_btn.setStyleSheet(
            "background:#007acc; color:white; padding:5px 12px; font-weight:bold;"
        )
        self.run_btn.clicked.connect(self._run_query)
        input_row.addWidget(self.run_btn)
        layout.addLayout(input_row)

        self.setWidget(self.main_widget)

        # Initialise the engine
        self._init_engine()

    # ── Engine init ───────────────────────────────────────────────────

    def _init_engine(self):
        """(Re)initialise the shared GeoSI engine."""
        try:
            # Apply saved API key to env so geosi_engine can pick it up
            settings = QgsSettings()
            saved_key = settings.value("GeoSI/anthropic_api_key", "")
            if saved_key:
                os.environ["ANTHROPIC_API_KEY"] = saved_key

            # FULL module cache purge - force reload from disk
            import sys
            mods_to_remove = [m for m in sys.modules.keys() if m.startswith('geosi_')]
            for mod in mods_to_remove:
                del sys.modules[mod]

            # Now import fresh (all submodules will load from disk)
            import geosi_engine
            self.engine = geosi_engine.GeoSI()

            tool_count = len(self.engine.registry.list_tools())
            self._msg(
                f"✅ GeoSI Engine v{self.engine.version} ready — "
                f"{tool_count} tools loaded.",
                kind="success",
            )
            if not saved_key:
                self._msg(
                    "ℹ️ No Claude API key found. Keyword-based planning active. "
                    "Click ⚙️ to add your key for LLM planning.",
                    kind="warn",
                )
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print(f"FULL TRACEBACK:\n{tb}")
            self._msg(f"❌ Engine init failed: {e}", kind="error")
            self._msg(f"Details: {tb.split(chr(10))[-2]}", kind="error")

    # ── API key helpers ───────────────────────────────────────────────

    def _toggle_api_panel(self):
        self.api_panel.setVisible(not self.api_panel.isVisible())

    def _save_api_key(self):
        key = self.api_input.text().strip()
        if not key:
            self._msg("⚠️ No key entered.", kind="warn")
            return
        QgsSettings().setValue("GeoSI/anthropic_api_key", key)
        os.environ["ANTHROPIC_API_KEY"] = key
        self.api_panel.setVisible(False)
        self._msg("✅ API key saved. Reloading engine…", kind="success")
        self._init_engine()

    # ── Query handling ────────────────────────────────────────────────

    def _run_query(self):
        query = self.prompt.text().strip()
        if not query:
            return

        # Handle meta-commands
        if query.lower() == "help":
            self._show_help()
            self.prompt.clear()
            return

        self._msg(f"You: {query}", kind="user")
        self.prompt.clear()

        if not self.engine:
            self._msg("❌ Engine not ready. Click 🔄 to reload.", kind="error")
            return

        # Inject current QGIS layers into engine state
        self._sync_qgis_layers()

        # Disable run button while processing
        self.run_btn.setEnabled(False)
        self._msg("⏳ Thinking…")

        self._worker = _QueryWorker(self.engine, query)
        self._worker.finished.connect(self._on_result)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_result(self, result: dict):
        self.run_btn.setEnabled(True)

        if not result.get("success"):
            # Show the error / validation message
            self._msg(result.get("answer", "Failed."), kind="error")

            # Offer layer suggestions when available
            if self.engine and self.engine.agent and hasattr(self.engine.agent, "layer_suggestions"):
                suggestions = self.engine.agent.layer_suggestions
                if suggestions:
                    self._msg(
                        "💡 Did you mean one of these layers? (Copy the layer name and try again)",
                        kind="info",
                    )
                    for layer_name, score in suggestions[:5]:
                        self._msg(f"  • {layer_name} ({score:.0%} match)", kind="info")
        else:
            self._msg(result.get("answer", "Done."), kind="success")

        if result.get("reasoning"):
            self._msg(result["reasoning"], kind="info")

    def _on_error(self, err: str):
        self.run_btn.setEnabled(True)
        self._msg(f"❌ Error: {err}", kind="error")

    # ── Layer sync ────────────────────────────────────────────────────

    def _sync_qgis_layers(self):
        """
        Register all QGIS project layers into the engine's StateManager
        so the agent can reference them by name.
        """
        if not self.engine:
            return
        try:
            from qgis.core import QgsMapLayer
            from geosi_engine.models import Layer

            project = QgsProject.instance()
            for layer_id, ql in project.mapLayers().items():
                name = ql.name()
                if not self.engine.state.get_layer(name):
                    ltype = (
                        "raster"
                        if ql.type() == QgsMapLayer.RasterLayer
                        else "vector"
                    )
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
                    # Store the QGIS layer object for QGIS-backed tools
                    layer.features = ql
                    self.engine.state.add_layer(layer)
        except Exception as e:
            print(f"GeoSI: layer sync warning: {e}")

    # ── Help ──────────────────────────────────────────────────────────

    def _show_help(self):
        available = self.engine.state.list_layers() if self.engine else []
        
        if available:
            layers_str = ", ".join(available)
            self._msg(
                f"📖 GeoSI Examples:\n"
                f"  • Buffer {available[0] if available else 'layer'} by 500m\n"
                f"  • Count features in {available[0] if available else 'layer'}\n"
                f"  • Calculate area of {available[0] if available else 'layer'}\n"
                f"  • Clip {available[0] if available else 'layer'} to {available[1] if len(available) > 1 else 'another_layer'}\n\n"
                f"📁 Available Layers:\n  • " + "\n  • ".join(available) + "\n\n"
                f"Commands: help | Type ⚙️ to set Claude API key",
                kind="info",
            )
        else:
            self._msg(
                "📖 GeoSI Examples:\n"
                "  • Buffer hospitals by 500m\n"
                "  • Intersect schools with flood_zones\n"
                "  • Calculate slope from DEM\n"
                "  • Cluster crime points (eps=200)\n"
                "  • Export parks as GeoJSON\n"
                "  • Geocode address field in table\n\n"
                "⚠️ No layers loaded. Please load shapefiles first using QGIS.\n"
                "📁 Go to: Layer → Add Layer → Vector/Raster\n"
                "Commands: help | Type ⚙️ to set Claude API key",
                kind="warn",
            )

    # ── Message display ───────────────────────────────────────────────

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
        prefix = "<b>You:</b> " if kind == "user" else "<b>GeoSI:</b><br>"
        safe = text.replace("\n", "<br>")
        html = f'<div style="margin-top:8px; color:{color};">{prefix}{safe}</div>'
        self.chat.append(html)
        self.chat.verticalScrollBar().setValue(
            self.chat.verticalScrollBar().maximum()
        )
