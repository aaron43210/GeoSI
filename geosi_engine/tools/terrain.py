# -*- coding: utf-8 -*-
"""
GeoSI Engine — Terrain & 3D Analysis Tools (10 tools)

Auto-discovered by ToolRegistry.
"""

from geosi_engine.base import QGISProcessingTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


def _make_tool_class(name, display, desc, alg, params, cat="terrain"):
    param_objs = [ToolParameter(name=p[0],param_type=p[1],required=p[2],description=p[3],default=p[4] if len(p)>4 else None) for p in params]
    return type(name.title().replace("_","")+"Tool",(QGISProcessingTool,),{
        "__init__": lambda self: QGISProcessingTool.__init__(self,name=name,description=desc,category=cat,qgis_algorithm=alg,parameters=param_objs,display_name=display,tags=[name]+name.split("_"))
    })


_TOOL_DEFS = [
    ('viewshed', 'Viewshed', 'Calculate visible area from observer', 'native:viewshed', [('INPUT', 'layer', True, 'Input DEM'), ('OBSERVER_POINT', 'string', True, 'Observer coordinates'), ('OBSERVER_HEIGHT', 'number', False, 'Observer height', '1.75'), ('RADIUS', 'number', False, 'Max view radius')]),
    ('profile', 'Elevation Profile', 'Extract elevation along a line', 'native:rastersurfaceprofile', [('INPUT', 'layer', True, 'Input DEM'), ('LINE', 'layer', True, 'Profile line layer')]),
    ('volume', 'Surface Volume', 'Calculate cut/fill volumes', 'native:rastersurfacevolume', [('INPUT', 'layer', True, 'Input DEM'), ('BAND', 'number', False, 'Band', '1'), ('LEVEL', 'number', True, 'Reference level')]),
    ('watershed', 'Watershed Delineation', 'Delineate drainage basins', 'gdal:fillnodata', [('INPUT', 'layer', True, 'Input DEM')]),
    ('flow_direction', 'Flow Direction', 'Calculate water flow direction', 'native:rastercalc', [('INPUT', 'layer', True, 'Input DEM')]),
    ('flow_accumulation', 'Flow Accumulation', 'Calculate cumulative flow', 'native:rastercalc', [('INPUT', 'layer', True, 'Input flow direction raster')]),
    ('curvature', 'Curvature', 'Calculate surface curvature', 'native:rastercalc', [('INPUT', 'layer', True, 'Input DEM')]),
    ('terrain_classify', 'Terrain Classification', 'Classify terrain into landforms', 'native:reclassifybytable', [('INPUT', 'layer', True, 'Input DEM'), ('CLASSES', 'number', False, 'Number of classes', '5')]),
    ('drape_to_3d', 'Drape to 3D', 'Add Z values from DEM to 2D features', 'native:setzfromraster', [('INPUT', 'layer', True, 'Input 2D vector'), ('RASTER', 'layer', True, 'Input DEM'), ('BAND', 'number', False, 'Band', '1')]),
    ('tin_mesh', 'TIN Mesh', 'Create TIN surface from points', 'native:tininterpolation', [('INPUT', 'layer', True, 'Input point layer'), ('Z_FIELD', 'string', True, 'Elevation field'), ('EXTENT', 'string', True, 'Output extent'), ('PIXEL_SIZE', 'number', True, 'Output cell size')]),
]

import sys as _sys
_module=_sys.modules[__name__]
for _def in _TOOL_DEFS:
    _cls=_make_tool_class(*_def)
    setattr(_module,_cls.__name__,_cls)
del _sys,_module
