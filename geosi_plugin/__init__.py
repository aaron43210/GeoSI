# -*- coding: utf-8 -*-
"""GeoSI — Geospatial Superintelligence QGIS Plugin"""

import sys
import os

# Add plugin directory to sys.path so geosi_engine can be imported
_plugin_dir = os.path.dirname(__file__)
if _plugin_dir not in sys.path:
    sys.path.insert(0, _plugin_dir)


def classFactory(iface):
    from .geosi_plugin import GeoSIPlugin
    return GeoSIPlugin(iface)
