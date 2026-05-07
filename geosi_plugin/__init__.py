# -*- coding: utf-8 -*-
"""GeoSI — Geospatial Superintelligence QGIS Plugin"""


def classFactory(iface):
    from .geosi_plugin import GeoSIPlugin
    return GeoSIPlugin(iface)
