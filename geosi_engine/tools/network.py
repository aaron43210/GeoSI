# -*- coding: utf-8 -*-
"""
GeoSI Engine — Network & Routing Tools (8 tools)

Auto-discovered by ToolRegistry.
"""

from geosi_engine.base import QGISProcessingTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


def _make_tool_class(name, display, desc, alg, params, cat="network"):
    param_objs = [ToolParameter(name=p[0],param_type=p[1],required=p[2],description=p[3],default=p[4] if len(p)>4 else None) for p in params]
    return type(name.title().replace("_","")+"Tool",(QGISProcessingTool,),{
        "__init__": lambda self: QGISProcessingTool.__init__(self,name=name,description=desc,category=cat,qgis_algorithm=alg,parameters=param_objs,display_name=display,tags=[name]+name.split("_"))
    })


_TOOL_DEFS = [
    ('shortest_path', 'Shortest Path', 'Find shortest path between two points', 'native:shortestpathpointtopoint', [('INPUT', 'layer', True, 'Network line layer'), ('START_POINT', 'string', True, 'Start point coords'), ('END_POINT', 'string', True, 'End point coords'), ('STRATEGY', 'number', False, '0=shortest 1=fastest', '0')]),
    ('service_area', 'Service Area', 'Calculate reachable area from point', 'native:serviceareafrompoint', [('INPUT', 'layer', True, 'Network line layer'), ('START_POINT', 'string', True, 'Center point'), ('TRAVEL_COST', 'number', True, 'Max travel cost')]),
    ('shortest_path_layer', 'Shortest Path (Layer)', 'Route between point layers', 'native:shortestpathpointtolayer', [('INPUT', 'layer', True, 'Network layer'), ('START_POINT', 'string', True, 'Start point'), ('END_POINTS', 'layer', True, 'Destination points')]),
    ('network_lines_to_graph', 'Build Network Graph', 'Convert lines to routable graph', 'native:serviceareafromlayer', [('INPUT', 'layer', True, 'Input line layer'), ('POINTS', 'layer', True, 'Service points'), ('TRAVEL_COST', 'number', True, 'Travel cost')]),
    ('split_lines_at_points', 'Split Lines at Points', 'Break lines where points intersect', 'native:splitwithlines', [('INPUT', 'layer', True, 'Input line layer'), ('LINES', 'layer', True, 'Split lines')]),
    ('line_intersections', 'Line Intersections', 'Find where lines cross', 'native:lineintersections', [('INPUT', 'layer', True, 'First line layer'), ('INTERSECT', 'layer', True, 'Second line layer')]),
    ('connect_points', 'Connect Points', 'Create lines between ordered points', 'native:pointstopath', [('INPUT', 'layer', True, 'Input point layer'), ('ORDER_FIELD', 'string', True, 'Order field'), ('GROUP_FIELD', 'string', False, 'Group field')]),
    ('network_cost_matrix', 'OD Cost Matrix', 'Origin-destination cost matrix', 'native:shortestpathpointtolayer', [('INPUT', 'layer', True, 'Network layer'), ('ORIGINS', 'layer', True, 'Origin points'), ('DESTINATIONS', 'layer', True, 'Destination points')]),
]

import sys as _sys
_module=_sys.modules[__name__]
for _def in _TOOL_DEFS:
    _cls=_make_tool_class(*_def)
    setattr(_module,_cls.__name__,_cls)
del _sys,_module
