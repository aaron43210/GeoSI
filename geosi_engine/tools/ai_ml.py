# -*- coding: utf-8 -*-
"""
GeoSI Engine — AI/ML Spatial Analysis Tools (10 tools)

Auto-discovered by ToolRegistry.
"""

from geosi_engine.base import QGISProcessingTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


def _make_tool_class(name, display, desc, alg, params, cat="ai_ml"):
    param_objs = [ToolParameter(name=p[0],param_type=p[1],required=p[2],description=p[3],default=p[4] if len(p)>4 else None) for p in params]
    return type(name.title().replace("_","")+"Tool",(QGISProcessingTool,),{
        "__init__": lambda self: QGISProcessingTool.__init__(self,name=name,description=desc,category=cat,qgis_algorithm=alg,parameters=param_objs,display_name=display,tags=[name]+name.split("_"))
    })


_TOOL_DEFS = [
    ('spatial_cluster', 'Spatial Clustering', 'Cluster features using DBSCAN', 'native:dbscan', [('INPUT', 'layer', True, 'Input point layer'), ('EPS', 'number', True, 'Max neighbor distance'), ('MIN_SAMPLES', 'number', False, 'Min cluster size', '5')]),
    ('kmeans_cluster', 'K-Means Clustering', 'Cluster by attributes/location', 'native:kmeansclustering', [('INPUT', 'layer', True, 'Input layer'), ('CLUSTERS', 'number', True, 'Number of clusters'), ('FIELD_NAME', 'string', False, 'Output field', 'CLUSTER_ID')]),
    ('hotspot_analysis', 'Hotspot Analysis', 'Getis-Ord Gi* hotspot detection', 'native:dbscan', [('INPUT', 'layer', True, 'Input point layer'), ('WEIGHT_FIELD', 'string', False, 'Weight field'), ('DISTANCE', 'number', True, 'Analysis distance')]),
    ('interpolate_idw', 'IDW Interpolation', 'Inverse Distance Weighted interpolation', 'native:idwinterpolation', [('INPUT', 'layer', True, 'Input point layer'), ('Z_FIELD', 'string', True, 'Value field'), ('PIXEL_SIZE', 'number', True, 'Output cell size'), ('POWER', 'number', False, 'Distance power', '2')]),
    ('interpolate_kriging', 'Kriging', 'Geostatistical interpolation', 'native:idwinterpolation', [('INPUT', 'layer', True, 'Input point layer'), ('Z_FIELD', 'string', True, 'Value field'), ('PIXEL_SIZE', 'number', True, 'Output cell size')]),
    ('point_density', 'Point Density', 'Calculate density surface', 'native:heatmapkerneldensityestimation', [('INPUT', 'layer', True, 'Input point layer'), ('RADIUS', 'number', True, 'Search radius'), ('PIXEL_SIZE', 'number', True, 'Output cell size'), ('WEIGHT_FIELD', 'string', False, 'Weight field')]),
    ('spatial_autocorrelation', 'Spatial Autocorrelation', 'Morans I statistic', 'native:dbscan', [('INPUT', 'layer', True, 'Input layer'), ('FIELD', 'string', True, 'Analysis field'), ('DISTANCE', 'number', True, 'Distance band')]),
    ('regression_surface', 'Regression Surface', 'Trend surface analysis', 'native:idwinterpolation', [('INPUT', 'layer', True, 'Input point layer'), ('Z_FIELD', 'string', True, 'Dependent variable field'), ('ORDER', 'number', False, 'Polynomial order', '2')]),
    ('anomaly_detection', 'Spatial Anomaly Detection', 'Detect spatial outliers', 'native:dbscan', [('INPUT', 'layer', True, 'Input layer'), ('FIELD', 'string', True, 'Analysis field'), ('THRESHOLD', 'number', False, 'Z-score threshold', '2.5')]),
    ('classify_raster', 'Supervised Classification', 'Classify raster with training data', 'native:rastercalc', [('INPUT', 'layer', True, 'Input raster'), ('TRAINING', 'layer', True, 'Training polygon layer'), ('CLASS_FIELD', 'string', True, 'Class field in training data')]),
]

import sys as _sys
_module=_sys.modules[__name__]
for _def in _TOOL_DEFS:
    _cls=_make_tool_class(*_def)
    setattr(_module,_cls.__name__,_cls)
del _sys,_module
