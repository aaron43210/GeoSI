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
        self.conversation = None  # Will be initialized in _init_engine

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
        self.api_btn.setToolTip("Configure LLM (Ollama / API keys)")
        self.api_btn.clicked.connect(self._toggle_api_panel)
        header_row.addWidget(self.api_btn)
        
        self.clear_history_btn = QPushButton("🗑️")
        self.clear_history_btn.setFixedWidth(30)
        self.clear_history_btn.setToolTip("Clear conversation history")
        self.clear_history_btn.clicked.connect(self._clear_history)
        header_row.addWidget(self.clear_history_btn)
        
        layout.addLayout(header_row)

        # Configuration panel (Ollama + API keys)
        self.api_panel = QWidget()
        api_layout = QVBoxLayout(self.api_panel)
        api_layout.setContentsMargins(0, 5, 0, 5)
        api_layout.setSpacing(5)
        
        # Ollama configuration
        ollama_row = QHBoxLayout()
        ollama_row.addWidget(QLabel("🦙 Ollama:"))
        self.ollama_endpoint = QLineEdit()
        self.ollama_endpoint.setPlaceholderText("http://localhost:11434")
        ollama_row.addWidget(self.ollama_endpoint)
        self.ollama_model = QLineEdit()
        self.ollama_model.setPlaceholderText("mistral")
        ollama_row.addWidget(self.ollama_model)
        ollama_save_btn = QPushButton("Save")
        ollama_save_btn.setFixedWidth(60)
        ollama_save_btn.clicked.connect(self._save_ollama_config)
        ollama_row.addWidget(ollama_save_btn)
        api_layout.addLayout(ollama_row)
        
        # Claude API key
        api_row = QHBoxLayout()
        api_row.addWidget(QLabel("🔑 Claude Key:"))
        self.api_input = QLineEdit()
        # Set password echo mode with Qt5/Qt6 compatibility
        echo_mode = _get_echo_mode_password()
        if echo_mode is not None:
            self.api_input.setEchoMode(echo_mode)
        self.api_input.setPlaceholderText("sk-ant-…")
        api_row.addWidget(self.api_input)
        save_btn = QPushButton("Save")
        save_btn.setFixedWidth(60)
        save_btn.clicked.connect(self._save_api_key)
        api_row.addWidget(save_btn)
        api_layout.addLayout(api_row)
        
        self.api_panel.setVisible(False)
        layout.addWidget(self.api_panel)

        # Chat display (Premium Dark Theme)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet("""
            QTextEdit {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Segoe UI', 'SF Pro Display', 'Roboto', sans-serif;
                line-height: 1.6;
            }
        """)
        layout.addWidget(self.chat)

        # Input row
        input_row = QHBoxLayout()
        self.prompt = QLineEdit()
        self.prompt.setPlaceholderText("Ask GeoSI Quantum...")
        self.prompt.setStyleSheet("""
            QLineEdit {
                background-color: #161b22;
                color: #f0f6fc;
                border: 2px solid #30363d;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #58a6ff;
            }
        """)
        self.prompt.returnPressed.connect(self._run_query)
        input_row.addWidget(self.prompt)

        self.run_btn = QPushButton("▶")
        self.run_btn.setToolTip("Run Analysis")
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
            QPushButton:pressed {
                background-color: #238636;
            }
            QPushButton:disabled {
                background-color: #21262d;
                color: #484f58;
            }
        """)
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
            # Import modules first (before using them)
            import sys
            from geosi_engine.conversation import ConversationManager
            
            # Create a fresh conversation manager for this session
            self.conversation = ConversationManager(
                system_prompt="""You are a helpful geospatial AI assistant. You help users with GIS analysis tasks.
Be concise, friendly, and use emojis to make responses clear. Ask clarifying questions when needed."""
            )
            
            # Load Ollama config from settings
            settings = QgsSettings()
            ollama_endpoint = settings.value("GeoSI/ollama_endpoint", "http://localhost:11434")
            ollama_model = settings.value("GeoSI/ollama_model", "mistral")
            os.environ["OLLAMA_ENDPOINT"] = ollama_endpoint
            os.environ["OLLAMA_MODEL"] = ollama_model
            
            # Load Claude API key from settings
            saved_key = settings.value("GeoSI/anthropic_api_key", "")
            if saved_key:
                os.environ["ANTHROPIC_API_KEY"] = saved_key

            # Ensure plugin directory is in sys.path for absolute module imports
            plugin_dir = os.path.dirname(__file__)
            if plugin_dir not in sys.path:
                sys.path.insert(0, plugin_dir)
            
            # FULL module cache purge - force reload from disk
            mods_to_remove = [m for m in sys.modules.keys() if m.startswith('geosi_') or 'qgis_bridge' in m]
            for mod in mods_to_remove:
                del sys.modules[mod]

            # Use absolute imports strictly to avoid split-brain module caching
            from geosi_engine import GeoSI
            from geosi_engine.base import register_backend
            self.engine = GeoSI()
            
            # ✅ Register QGIS backend directly against the global module
            import qgis_bridge
            register_backend("qgis", qgis_bridge._run_qgis_algorithm)
            
            # Inject conversation manager into agent and parser
            if hasattr(self.engine, 'agent') and self.engine.agent:
                self.engine.agent.conversation = self.conversation
            if hasattr(self.engine, 'parser') and self.engine.parser:
                self.engine.parser.conversation = self.conversation

            tool_count = len(self.engine.registry.list_tools())
            self._msg(
                f"✅ GeoSI Engine v{self.engine.version} ready — "
                f"{tool_count} tools loaded.",
                kind="success",
            )
            
            # Sync layers immediately so they're available
            self._sync_qgis_layers()
            
            # Check which LLM is available
            import requests
            try:
                requests.post(f"{ollama_endpoint}/api/generate", json={"model": ollama_model}, timeout=2)
                self._msg(f"✅ Ollama available: {ollama_model} (Interactive mode enabled)", kind="success")
            except Exception:
                self._msg("ℹ️ Ollama not available. Will try cloud providers.", kind="info")
                
            if not saved_key:
                self._msg(
                    "ℹ️ No Claude API key found. Click ⚙️ to configure.",
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
        # Load current Ollama config into UI if available
        settings = QgsSettings()
        self.ollama_endpoint.setText(settings.value("GeoSI/ollama_endpoint", "http://localhost:11434"))
        self.ollama_model.setText(settings.value("GeoSI/ollama_model", "mistral"))

    def _save_ollama_config(self):
        endpoint = self.ollama_endpoint.text().strip() or "http://localhost:11434"
        model = self.ollama_model.text().strip() or "mistral"
        
        QgsSettings().setValue("GeoSI/ollama_endpoint", endpoint)
        QgsSettings().setValue("GeoSI/ollama_model", model)
        os.environ["OLLAMA_ENDPOINT"] = endpoint
        os.environ["OLLAMA_MODEL"] = model
        
        self._msg(f"✅ Ollama config saved: {endpoint} ({model}). Reloading engine…", kind="success")
        self._init_engine()

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

    def _clear_history(self):
        """Clear conversation history and chat display."""
        if self.conversation:
            self.conversation.clear()
        self.chat.clear()
        self._msg("🗑️ Conversation history cleared.", kind="info")

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
        
        # Handle "what layers" queries
        if any(phrase in query.lower() for phrase in ["what layers", "list layers", "available layers", "show layers", "my layers"]):
            self._msg(f"You: {query}", kind="user")
            self.prompt.clear()
            self._sync_qgis_layers()
            layers = self.engine.state.list_layers() if self.engine else []
            if layers:
                self._msg(f"📁 Available layers ({len(layers)}):", kind="success")
                for layer in layers:
                    layer_obj = self.engine.state.get_layer(layer)
                    if layer_obj:
                        count = layer_obj.feature_count or "?"
                        ltype = layer_obj.layer_type or "unknown"
                        self._msg(f"  • {layer}: {count} features ({ltype})", kind="info")
            else:
                self._msg("⚠️ No layers loaded. Go to Layer → Add Layer to load shapefiles.", kind="warn")
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
            # Safely add generated layers to the QGIS canvas on the main thread
            self._add_outputs_to_canvas(result.get("results", {}))

        if result.get("reasoning"):
            self._msg(result["reasoning"], kind="info")

    def _add_outputs_to_canvas(self, results: dict):
        """Safely load execution outputs into the QGIS Layers panel."""
        print(f"GeoSI [_add_outputs_to_canvas]: called with {len(results)} result(s): {list(results.keys())}")
        try:
            from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer
            import os
            
            project = QgsProject.instance()
            layers_added = []
            
            def _is_geosi_layer(obj):
                """Duck-type check for GeoSI Layer (avoids isinstance module identity issues)."""
                return (hasattr(obj, 'filepath') and hasattr(obj, 'layer_type') and hasattr(obj, 'name'))
            
            def _load_file(filepath, name):
                """Load a file path as a QGIS layer."""
                if not filepath or not os.path.isfile(filepath):
                    print(f"GeoSI: file not found: {filepath}")
                    return False
                print(f"GeoSI: loading '{filepath}' as '{name}'")
                try:
                    if filepath.lower().endswith(('.tif', '.tiff', '.img', '.asc', '.sdat', '.nc')):
                        ql = QgsRasterLayer(filepath, name)
                    else:
                        ql = QgsVectorLayer(filepath, name, "ogr")
                    if ql and ql.isValid():
                        project.addMapLayer(ql)
                        layers_added.append(name)
                        self._msg(f"✅ Loaded: {name}", kind="success")
                        print(f"GeoSI: ✅ '{name}' added to project")
                        return True
                    else:
                        self._msg(f"⚠️ Invalid layer: {name}", kind="warn")
                        print(f"GeoSI: ⚠️ invalid: {filepath}")
                except Exception as e:
                    self._msg(f"⚠️ Load failed: {name}: {e}", kind="warn")
                    print(f"GeoSI: exception: {e}")
                return False
            
            for step_id, step_output in results.items():
                out_type = type(step_output).__name__
                print(f"GeoSI: step='{step_id}' type={out_type}")
                
                # Case 1: GeoSI Layer (duck-typed)
                if _is_geosi_layer(step_output):
                    name = step_output.name or step_id
                    fp = step_output.filepath or ''
                    print(f"GeoSI: Layer detected: name='{name}' path='{fp}' ltype='{step_output.layer_type}'")
                    _load_file(fp, name)
                
                # Case 2: dict (raw processing output)
                elif isinstance(step_output, dict):
                    print(f"GeoSI: dict keys={list(step_output.keys())}")
                    for key, val in step_output.items():
                        lname = f"{step_id}_{key}"
                        print(f"GeoSI:   k='{key}' vtype={type(val).__name__}")
                        if _is_geosi_layer(val):
                            _load_file(val.filepath or '', val.name or lname)
                        elif isinstance(val, str) and os.path.isfile(val):
                            _load_file(val, lname)
                        elif hasattr(val, 'source') and callable(getattr(val, 'source', None)):
                            try:
                                src = val.source()
                                if os.path.isfile(src):
                                    _load_file(src, lname)
                                elif hasattr(val, 'isValid') and val.isValid():
                                    project.addMapLayer(val)
                                    layers_added.append(lname)
                            except Exception as e:
                                print(f"GeoSI:   source() error: {e}")
                
                # Case 3: string file path
                elif isinstance(step_output, str) and os.path.isfile(step_output):
                    _load_file(step_output, step_id)
                
                else:
                    print(f"GeoSI: unhandled type '{out_type}' for step '{step_id}'")
            
            if layers_added:
                self._msg(f"🗺️ {len(layers_added)} layer(s) added to Layers Panel", kind="success")
            else:
                print("GeoSI: WARNING — no layers loaded")
                if results:
                    self._msg("⚠️ Output could not be loaded. Check Python console.", kind="warn")
        except Exception as e:
            import traceback
            self._msg(f"⚠️ Layer loading error: {e}", kind="warn")
            print(f"GeoSI LAYER LOAD ERROR:\n{traceback.format_exc()}")

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
        schemes = {
            "user":    {"bg": "#161b22", "border": "#30363d", "text": "#58a6ff", "icon": "👤"},
            "success": {"bg": "#161b22", "border": "#238636", "text": "#3fb950", "icon": "✅"},
            "error":   {"bg": "#161b22", "border": "#f85149", "text": "#f85149", "icon": "❌"},
            "warn":    {"bg": "#161b22", "border": "#d29922", "text": "#d29922", "icon": "⚠️"},
            "info":    {"bg": "#161b22", "border": "#30363d", "text": "#8b949e", "icon": "ℹ️"},
            "normal":  {"bg": "transparent", "border": "transparent", "text": "#c9d1d9", "icon": "🤖"},
        }
        scheme = schemes.get(kind, schemes["normal"])
        
        # Build message box
        if kind == "normal":
            html = f'<div style="color:{scheme["text"]}; margin-bottom:10px;">{text}</div>'
        else:
            prefix = f'<b>{scheme["icon"]} {kind.upper()}</b>'
            html = f"""
                <div style="background-color:{scheme["bg"]}; border: 1px solid {scheme["border"]}; 
                            border-radius: 6px; padding: 10px; margin-bottom: 10px;">
                    <div style="color:{scheme["text"]}; margin-bottom: 4px; font-size: 11px;">{prefix}</div>
                    <div style="color:#c9d1d9;">{text.replace(chr(10), "<br>")}</div>
                </div>
            """
        
        self.chat.append(html)
        self.chat.verticalScrollBar().setValue(
            self.chat.verticalScrollBar().maximum()
        )
        self.chat.verticalScrollBar().setValue(
            self.chat.verticalScrollBar().maximum()
        )
