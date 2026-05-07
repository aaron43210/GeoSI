# -*- coding: utf-8 -*-
"""
GeoSI Engine — Temporal & Time-Series Tools (6 tools)

Auto-discovered by ToolRegistry.
"""

from geosi_engine.base import QGISProcessingTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


def _make_tool_class(name, display, desc, alg, params, cat="temporal"):
    param_objs = [ToolParameter(name=p[0],param_type=p[1],required=p[2],description=p[3],default=p[4] if len(p)>4 else None) for p in params]
    return type(name.title().replace("_","")+"Tool",(QGISProcessingTool,),{
        "__init__": lambda self: QGISProcessingTool.__init__(self,name=name,description=desc,category=cat,qgis_algorithm=alg,parameters=param_objs,display_name=display,tags=[name]+name.split("_"))
    })


_TOOL_DEFS = [
    ('temporal_filter', 'Temporal Filter', 'Filter features by date range', 'native:extractbyattribute', [('INPUT', 'layer', True, 'Input layer'), ('DATE_FIELD', 'string', True, 'Date field name'), ('START_DATE', 'string', True, 'Start date ISO'), ('END_DATE', 'string', True, 'End date ISO')]),
    ('change_detection', 'Change Detection', 'Detect changes between two rasters', 'native:rastercalc', [('BEFORE', 'layer', True, 'Before raster'), ('AFTER', 'layer', True, 'After raster')]),
    ('temporal_aggregate', 'Temporal Aggregate', 'Aggregate features by time period', 'native:aggregate', [('INPUT', 'layer', True, 'Input layer'), ('DATE_FIELD', 'string', True, 'Date field'), ('PERIOD', 'string', True, 'Period: day/week/month/year')]),
    ('time_series_stats', 'Time Series Statistics', 'Calculate temporal statistics', 'native:zonalstatisticsfb', [('INPUT', 'layer', True, 'Input layer'), ('DATE_FIELD', 'string', True, 'Date field'), ('VALUE_FIELD', 'string', True, 'Value field')]),
    ('animate_temporal', 'Animate Temporal Data', 'Prepare frames for temporal animation', 'native:extractbyattribute', [('INPUT', 'layer', True, 'Input layer'), ('DATE_FIELD', 'string', True, 'Date field'), ('FRAME_INTERVAL', 'string', True, 'Frame interval')]),
    ('temporal_join', 'Temporal Join', 'Join layers by time proximity', 'native:joinattributesbylocation', [('INPUT', 'layer', True, 'Input layer'), ('JOIN', 'layer', True, 'Join layer'), ('INPUT_DATE', 'string', True, 'Input date field'), ('JOIN_DATE', 'string', True, 'Join date field')]),
]

import sys as _sys
_module=_sys.modules[__name__]
for _def in _TOOL_DEFS:
    _cls=_make_tool_class(*_def)
    setattr(_module,_cls.__name__,_cls)
del _sys,_module
