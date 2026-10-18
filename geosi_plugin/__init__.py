# -*- coding: utf-8 -*-
"""
GeoSI Plugin — classFactory Entry Point
════════════════════════════════════════

QGIS calls classFactory(iface) when loading any plugin.
This returns the main plugin object that manages the lifecycle.
"""


def classFactory(iface):
    """
    QGIS entry point. Called when QGIS loads this plugin.

    Args:
        iface: QgisInterface — provides hooks into the QGIS application

    Returns:
        GeoSIPlugin instance that manages initGui() / unload()
    """
    from geosi_plugin.geosi_plugin import GeoSIPlugin
    return GeoSIPlugin(iface)
