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
"""

import os
import sys
import logging

logger = logging.getLogger("geosi_plugin")


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

        # ── Ensure plugin directory is in sys.path ─────────────────────
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(plugin_dir)
        for path in (plugin_dir, parent_dir):
            if path not in sys.path:
                sys.path.insert(0, path)

    def initGui(self):
        """
        Called by QGIS when the plugin is activated.

        Creates the toolbar action and initializes the GeoSI engine
        with dynamic QGIS tool discovery.
        """
        from qgis.PyQt.QtWidgets import QAction
        from qgis.PyQt.QtGui import QIcon

        # ── Create toolbar action ──────────────────────────────────────
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
        self.action = QAction(icon, "GeoSI Chat", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.triggered.connect(self._toggle_dock)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&GeoSI", self.action)

        # ── Initialize the engine ──────────────────────────────────────
        self._init_engine()

        logger.info(
            f"GeoSI v2 initialized: {self.tool_count} QGIS tools "
            f"+ {self.engine.registry.tool_count() - self.tool_count} portable tools"
        )

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
        """
        from geosi_engine import GeoSI
        from geosi_plugin.qgis_bridge import install

        # Step 1: Create the engine (portable tools only at this point)
        self.engine = GeoSI(use_llm=True)

        # Step 2: Dynamic discovery — THIS IS THE KEY LINE
        # install() reads every algorithm from QGIS Processing Registry
        # and creates a BackendTool for each one. After this call,
        # the registry contains 1000+ tools the LLM can use.
        self.tool_count = install(registry=self.engine.registry)

    def _toggle_dock(self, checked: bool):
        """Show or hide the GeoSI chat dock widget."""
        if self.dock is None:
            from geosi_plugin.prompt_dock import GeoSIDock
            self.dock = GeoSIDock(self.iface, self.engine)
            self.iface.addDockWidget(
                __import__("qgis.PyQt.QtCore", fromlist=["Qt"]).Qt.RightDockWidgetArea,
                self.dock,
            )
        if checked:
            self.dock.show()
        else:
            self.dock.hide()

    def unload(self):
        """Called by QGIS when the plugin is deactivated."""
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&GeoSI", self.action)
        if self.dock:
            self.iface.removeDockWidget(self.dock)
            self.dock = None
        self.engine = None
