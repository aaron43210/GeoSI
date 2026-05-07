# -*- coding: utf-8 -*-
"""
GeoSI Engine — Data Validation & QA Tools (10 tools)

Auto-discovered by ToolRegistry.
"""

from geosi_engine.base import QGISProcessingTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


def _make_tool_class(name, display, desc, alg, params, cat="validation"):
    # Convert param tuples into ToolParameter objects with metadata
    param_objs = [ToolParameter(name=p[0],param_type=p[1],required=p[2],description=p[3],default=p[4] if len(p)>4 else None) for p in params]
    # Dynamically generate a tool class inheriting from QGISProcessingTool
    # Class name: title case of tool name (e.g., "check_validity" → "CheckValidityTool")
    return type(name.title().replace("_","")+"Tool",(QGISProcessingTool,),{
        # Initialize the tool with name, description, algorithm, and params
        "__init__": lambda self: QGISProcessingTool.__init__(self,name=name,description=desc,category=cat,qgis_algorithm=alg,parameters=param_objs,display_name=display,tags=[name]+name.split("_"))
    })


_TOOL_DEFS = [
    # (tool_name, display_name, description, qgis_algorithm, [(param_name, type, required, desc, [default])])
    ('check_validity', 'Check Validity', 'Validate geometry validity', 'native:checkvalidity', [('INPUT', 'layer', True, 'Input layer')]),
    ('topology_check', 'Topology Check', 'Detect topology errors', 'native:checkvalidity', [('INPUT', 'layer', True, 'Input layer'), ('RULES', 'string', False, 'Topology rules')]),
    ('remove_duplicates', 'Remove Duplicates', 'Remove duplicate geometries', 'native:removeduplicatevertices', [('INPUT', 'layer', True, 'Input layer'), ('TOLERANCE', 'number', False, 'Distance tolerance', '0.0001')]),
    ('remove_null', 'Remove Null Geometries', 'Remove features with null geometry', 'native:removenullgeometries', [('INPUT', 'layer', True, 'Input layer')]),
    ('snap_geometries', 'Snap Geometries', 'Snap to reference layer', 'native:snapgeometries', [('INPUT', 'layer', True, 'Input layer'), ('REFERENCE', 'layer', True, 'Reference layer'), ('TOLERANCE', 'number', True, 'Snap tolerance')]),
    ('fill_holes', 'Fill Holes', 'Remove polygon holes below threshold', 'native:deleteholes', [('INPUT', 'layer', True, 'Input polygon layer'), ('MIN_AREA', 'number', False, 'Min hole area to keep', '0')]),
    ('check_crs', 'Check CRS Consistency', 'Verify CRS across layers', 'native:reprojectlayer', [('INPUT', 'layer', True, 'Input layer'), ('EXPECTED_CRS', 'string', True, 'Expected CRS')]),
    ('detect_gaps', 'Detect Gaps', 'Find gaps between polygons', 'native:checkvalidity', [('INPUT', 'layer', True, 'Input polygon layer')]),
    ('detect_overlaps', 'Detect Overlaps', 'Find overlapping polygons', 'native:intersection', [('INPUT', 'layer', True, 'Input polygon layer')]),
    ('field_stats', 'Field Statistics', 'Compute attribute field statistics', 'native:basicstatisticsforfields', [('INPUT', 'layer', True, 'Input layer'), ('FIELD_NAME', 'string', True, 'Field to analyze')]),
]

# Dynamically create tool classes and register them in the module namespace
import sys as _sys
_module=_sys.modules[__name__]
for _def in _TOOL_DEFS:
    # Generate a tool class from the definition
    _cls=_make_tool_class(*_def)
    # Add the class to the current module so it can be discovered by auto-discovery
    setattr(_module,_cls.__name__,_cls)
# Clean up temporary references
del _sys,_module
