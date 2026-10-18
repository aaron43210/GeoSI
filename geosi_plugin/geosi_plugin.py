# -*- coding: utf-8 -*-
"""
GeoSI Plugin — QGIS Plugin Entry Point (v2: Dynamic Discovery)
═══════════════════════════════════════════════════════════════════

This module handles:
    1. Plugin lifecycle (initGui / unload)
    2. Toolbar action to toggle the chat dock
    3. Engine initialization with dynamic QGIS tool discovery

v2 Key Change:
    After creating the GeoSI engine, we call qgis_bridge.install(registry)
    which automatically discovers ALL available QGIS Processing algorithms
    and registers them as tools the LLM can use.

Works with both Qt5 (QGIS 3.x) and Qt6 (QGIS 4.x).
"""

import logging
import os
import traceback

logger = logging.getLogger("geosi_plugin")

MENU_NAME = "&GeoSI"


class GeoSIPlugin:
    """
    Main QGIS plugin class. Created by classFactory().

    Lifecycle:
        classFactory(iface)  → creates GeoSIPlugin instance
        initGui()            → adds toolbar button, initializes engine
        unload()             → removes toolbar button, cleans up
    """

    def __init__(self, iface):
        """
        Constructor. Called by classFactory() when QGIS loads the plugin.

        Args:
            iface: QgisInterface — provides access to the QGIS application
                   (map canvas, menu bar, message bar, etc.)
        """
        self.iface = iface
        self.dock = None
        self.action = None
        self.engine = None
        self.tool_count = 0  # Number of dynamically discovered tools

    def initGui(self):
        """
        Called by QGIS when the plugin is activated.

        Creates the toolbar action. The engine is started lazily the first
        time the dock is opened so a slow or failing engine never blocks
        QGIS startup.
        """
        from qgis.PyQt.QtGui import QIcon
        try:
            from qgis.PyQt.QtGui import QAction  # Qt6
        except ImportError:
            from qgis.PyQt.QtWidgets import QAction  # Qt5

        # ── Create toolbar action ──────────────────────────────────────
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
        self.action = QAction(icon, "GeoSI Chat", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.toggled.connect(self._toggle_dock)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(MENU_NAME, self.action)

    def _init_engine(self):
        """
        Initialize the GeoSI engine and dynamically discover QGIS tools.

        This is the v2 magic:
            1. Create the engine (starts with only portable tools)
            2. Call qgis_bridge.install(registry) to:
               a. Register the QGIS backend callable
               b. Scan QgsApplication.processingRegistry().algorithms()
               c. Create BackendTool for each algorithm
               d. Register all tools in the engine's ToolRegistry

        Returns:
            True if the engine is ready, False otherwise (error shown to user).
        """
        if self.engine is not None:
            return True
        try:
            from geosi_engine import GeoSI
            from .qgis_bridge import install

            # Step 1: Create the engine (portable tools only at this point)
            engine = GeoSI(use_llm=True)

            # Step 2: Dynamic discovery — reads every algorithm from the
            # QGIS Processing Registry and creates a BackendTool for each.
            self.tool_count = install(registry=engine.registry)
            self.engine = engine
        except Exception as e:  # noqa: BLE001 — surface any startup failure
            logger.error("GeoSI engine failed to start:\n%s", traceback.format_exc())
            self._show_error(f"GeoSI engine failed to start: {e}")
            return False

        logger.info(
            "GeoSI v2 initialized: %d QGIS tools + %d portable tools",
            self.tool_count,
            self.engine.registry.tool_count() - self.tool_count,
        )
        return True

    def _show_error(self, message):
        try:
            from qgis.core import Qgis
            self.iface.messageBar().pushMessage("GeoSI", message, level=Qgis.Critical, duration=10)
        except Exception:  # noqa: BLE001
            logger.error(message)

    def _toggle_dock(self, checked: bool):
        """Show or hide the GeoSI chat dock widget."""
        if not checked:
            if self.dock is not None:
                self.dock.hide()
            return

        if self.dock is None:
            if not self._init_engine():
                self.action.setChecked(False)
                return
            from qgis.PyQt.QtCore import Qt
            from .prompt_dock import GeoSIDock

            self.dock = GeoSIDock(self.iface, self.engine)
            self.iface.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock.dock)
            # Keep the toolbar button in sync when the user closes the dock
            self.dock.dock.visibilityChanged.connect(self._on_dock_visibility)
        self.dock.show()

    def _on_dock_visibility(self, visible: bool):
        if self.action is not None and self.action.isChecked() != visible:
            self.action.blockSignals(True)
            self.action.setChecked(visible)
            self.action.blockSignals(False)

    def unload(self):
        """Called by QGIS when the plugin is deactivated."""
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu(MENU_NAME, self.action)
            self.action.deleteLater()
            self.action = None
        if self.dock:
            self.iface.removeDockWidget(self.dock.dock)
            self.dock.dock.deleteLater()
            self.dock = None
        self.engine = None
