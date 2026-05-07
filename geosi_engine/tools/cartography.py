# -*- coding: utf-8 -*-
"""
GeoSI Engine — Cartography & Export Tools (10 tools)

Auto-discovered by ToolRegistry.
"""

from geosi_engine.base import QGISProcessingTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


def _make_tool_class(name, display, desc, alg, params, cat="cartography"):
    param_objs = [ToolParameter(name=p[0],param_type=p[1],required=p[2],description=p[3],default=p[4] if len(p)>4 else None) for p in params]
    return type(name.title().replace("_","")+"Tool",(QGISProcessingTool,),{
        "__init__": lambda self: QGISProcessingTool.__init__(self,name=name,description=desc,category=cat,qgis_algorithm=alg,parameters=param_objs,display_name=display,tags=[name]+name.split("_"))
    })


_TOOL_DEFS = [
    ('export_geojson', 'Export GeoJSON', 'Save layer as GeoJSON', 'native:savefeatures', [('INPUT', 'layer', True, 'Input layer'), ('OUTPUT', 'string', True, 'Output file path')]),
    ('export_shapefile', 'Export Shapefile', 'Save layer as Shapefile', 'native:savefeatures', [('INPUT', 'layer', True, 'Input layer'), ('OUTPUT', 'string', True, 'Output .shp path')]),
    ('export_geopackage', 'Export GeoPackage', 'Save layer as GPKG', 'native:savefeatures', [('INPUT', 'layer', True, 'Input layer'), ('OUTPUT', 'string', True, 'Output .gpkg path')]),
    ('export_csv', 'Export CSV', 'Save attributes as CSV', 'native:savefeatures', [('INPUT', 'layer', True, 'Input layer'), ('OUTPUT', 'string', True, 'Output .csv path')]),
    ('export_kml', 'Export KML', 'Save layer as KML', 'native:savefeatures', [('INPUT', 'layer', True, 'Input layer'), ('OUTPUT', 'string', True, 'Output .kml path')]),
    ('geocode', 'Geocode Addresses', 'Convert addresses to coordinates', 'native:batchnominatimgeocoder', [('INPUT', 'layer', True, 'Input table layer'), ('FIELD', 'string', True, 'Address field name')]),
    ('reverse_geocode', 'Reverse Geocode', 'Convert coordinates to addresses', 'native:batchnominatimgeocoder', [('INPUT', 'layer', True, 'Input point layer')]),
    ('create_labels', 'Create Label Layer', 'Generate label points for polygons', 'native:poleofinaccessibility', [('INPUT', 'layer', True, 'Input polygon layer'), ('TOLERANCE', 'number', False, 'Tolerance', '1.0')]),
    ('style_categorized', 'Categorized Style', 'Apply categorized symbology', 'native:setlayerstyle', [('INPUT', 'layer', True, 'Input layer'), ('FIELD', 'string', True, 'Category field'), ('STYLE', 'string', False, 'Style definition')]),
    ('atlas_export', 'Atlas Export', 'Generate map atlas pages', 'native:atlaslayouttoimage', [('LAYOUT', 'string', True, 'Layout name'), ('COVERAGE', 'layer', True, 'Coverage layer'), ('OUTPUT', 'string', True, 'Output directory')]),
]

import sys as _sys
_module=_sys.modules[__name__]
for _def in _TOOL_DEFS:
    _cls=_make_tool_class(*_def)
    setattr(_module,_cls.__name__,_cls)
del _sys,_module
