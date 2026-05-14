# -*- coding: utf-8 -*-
"""
GeoSI — Geospatial Superintelligence QGIS Plugin

Version: 1.0.0 (Intelligent Layer Auto-Loading)
Status: Production-ready for QGIS 3.22 - 4.99

Features:
    - 128 advanced GIS tools via natural language
    - ✨ Automatic layer loading to QGIS Layers Panel
    - Complete Watershed Analysis workflow (5-step hydrological pipeline)
    - Multi-step workflow orchestration with instant result visibility
    - Ollama/Claude/Gemini LLM support
    - Qt5/Qt6 compatible (QGIS 3.x and 4.x support)
    - Dark mode premium UI

Architecture:
    - Universal engine (no QGIS imports in core)
    - Plugin-specific bridge for QGIS Processing dispatch
    - Intelligent layer converter (GeoSI Layer → QGIS layer)
    - Framework-independent: works in plugin, server, Jupyter, CLI

QGIS 4 Compatibility:
    - Full Qt6 support with Qt5 fallbacks
    - Tested on QGIS 3.22, 4.0+ 
    - Automatic Qt version detection
    - No deprecated QGIS APIs
"""
import os
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction


class GeoSIPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.dock = None
        self.action = None
        self.plugin_dir = os.path.dirname(__file__)

    def initGui(self):
        try:
            # Install the QGIS backend so universal BackendTools dispatch
            # to QGIS Processing while running inside the plugin.
            try:
                from .qgis_bridge import install as install_qgis_backend
                install_qgis_backend()
            except Exception as e:
                print(f"GeoSI: QGIS backend install warning: {e}")

            icon_path = os.path.join(self.plugin_dir, 'icon.png')
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
            else:
                icon = QIcon()  # Empty icon if file not found
            
            self.action = QAction(icon, 'GeoSI — AI Agent', self.iface.mainWindow())
            self.action.setToolTip('Open GeoSI AI prompt panel')
            self.action.triggered.connect(self.toggle_dock)
            self.iface.addToolBarIcon(self.action)
            self.iface.addPluginToMenu('&GeoSI', self.action)
            print("✅ GeoSI plugin GUI initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing GeoSI GUI: {e}")
            import traceback
            traceback.print_exc()

    def _resolve_right_dock_area(self):
        """Return right dock area constant compatible with Qt5/Qt6."""
        area = getattr(Qt, 'RightDockWidgetArea', None)
        if area is not None:
            return area

        dock_area_enum = getattr(Qt, 'DockWidgetArea', None)
        if dock_area_enum is not None:
            area = getattr(dock_area_enum, 'RightDockWidgetArea', None)
            if area is not None:
                return area

        raise AttributeError('Qt right dock area enum not found')

    def unload(self):
        self.iface.removePluginMenu('&GeoSI', self.action)
        self.iface.removeToolBarIcon(self.action)
        if self.dock:
            self.iface.removeDockWidget(self.dock)
            self.dock = None

    def toggle_dock(self):
        try:
            if self.dock is None:
                from .prompt_dock import GeoSIDock
                self.dock = GeoSIDock(self.iface)
                self.iface.addDockWidget(
                    self._resolve_right_dock_area(), self.dock)
                self.dock.show()
            else:
                self.dock.setVisible(not self.dock.isVisible())
        except Exception as e:
            print(f"❌ Error toggling dock: {e}")
            try:
                self.iface.messageBar().pushCritical(
                    'GeoSI', f'Failed to open plugin panel: {e}')
            except Exception:
                pass
            import traceback
            traceback.print_exc()
