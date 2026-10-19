"""
GeoSI Plugin — classFactory Entry Point
════════════════════════════════════════

QGIS calls classFactory(iface) when loading any plugin.
This returns the main plugin object that manages the lifecycle.

In the packaged plugin the engine packages (geosi_engine, geosi_knowledge,
...) are bundled next to this file, so the plugin directory is put on
sys.path before anything imports them.
"""

import os
import sys

_PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
for _path in (_PLUGIN_DIR, os.path.dirname(_PLUGIN_DIR)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

# Ensure Plugin Reloader picks up engine changes by purging cached submodules
for _mod_name in list(sys.modules.keys()):
    if _mod_name.startswith(("geosi_engine", "geosi_plugin.", "geosi_data", "geosi_knowledge", "geosi_rag")):
        del sys.modules[_mod_name]


def classFactory(iface):
    """
    QGIS entry point. Called when QGIS loads this plugin.

    Args:
        iface: QgisInterface — provides hooks into the QGIS application

    Returns:
        GeoSIPlugin instance that manages initGui() / unload()
    """
    from .geosi_plugin import GeoSIPlugin

    return GeoSIPlugin(iface)
