# -*- coding: utf-8 -*-
"""
GeoSI Engine — Raster Analysis Tools (25 tools)

Auto-discovered by ToolRegistry.
"""

from geosi_engine.base import QGISProcessingTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


def _make_tool_class(name, display, desc, alg, params, cat="raster"):
    param_objs = [ToolParameter(name=p[0],param_type=p[1],required=p[2],description=p[3],default=p[4] if len(p)>4 else None) for p in params]
    return type(name.title().replace("_","")+"Tool",(QGISProcessingTool,),{
        "__init__": lambda self: QGISProcessingTool.__init__(self,name=name,description=desc,category=cat,qgis_algorithm=alg,parameters=param_objs,display_name=display,tags=[name]+name.split("_"))
    })


_TOOL_DEFS = [
    ('slope', 'Slope', 'Calculate slope from DEM', 'native:slope', [('INPUT', 'layer', True, 'Input DEM raster')]),
    ('aspect', 'Aspect', 'Calculate aspect/facing direction', 'native:aspect', [('INPUT', 'layer', True, 'Input DEM raster')]),
    ('hillshade', 'Hillshade', 'Generate shaded relief', 'native:hillshade', [('INPUT', 'layer', True, 'Input DEM'), ('Z_FACTOR', 'number', False, 'Vertical exaggeration', '1'), ('AZIMUTH', 'number', False, 'Light azimuth', '315'), ('V_ANGLE', 'number', False, 'Vertical angle', '45')]),
    ('contour', 'Contour Lines', 'Generate elevation contours', 'gdal:contour', [('INPUT', 'layer', True, 'Input DEM'), ('BAND', 'number', False, 'Raster band', '1'), ('INTERVAL', 'number', True, 'Contour interval')]),
    ('raster_calc', 'Raster Calculator', 'Band math expression', 'native:rastercalc', [('EXPRESSION', 'string', True, 'Calculation expression'), ('LAYERS', 'layer', True, 'Input rasters')]),
    ('reclassify', 'Reclassify by Table', 'Reclassify raster values', 'native:reclassifybytable', [('INPUT_RASTER', 'layer', True, 'Input raster'), ('TABLE', 'string', True, 'Reclassification table')]),
    ('zonal_stats', 'Zonal Statistics', 'Calculate raster stats per polygon', 'native:zonalstatisticsfb', [('INPUT', 'layer', True, 'Polygon zones'), ('INPUT_RASTER', 'layer', True, 'Input raster'), ('STATISTICS', 'string', False, 'Statistics to compute', '0,1,2')]),
    ('raster_clip', 'Clip Raster by Extent', 'Clip raster to bounding box', 'gdal:cliprasterbyextent', [('INPUT', 'layer', True, 'Input raster'), ('EXTENT', 'string', True, 'Clip extent')]),
    ('raster_clip_mask', 'Clip Raster by Mask', 'Clip raster using vector mask', 'gdal:cliprasterbymasklayer', [('INPUT', 'layer', True, 'Input raster'), ('MASK', 'layer', True, 'Mask layer')]),
    ('warp', 'Warp/Reproject Raster', 'Reproject a raster to new CRS', 'gdal:warpreproject', [('INPUT', 'layer', True, 'Input raster'), ('TARGET_CRS', 'string', True, 'Target CRS')]),
    ('merge_raster', 'Merge Rasters', 'Merge multiple rasters into one', 'gdal:merge', [('INPUT', 'layer', True, 'Input raster layers')]),
    ('polygonize_raster', 'Raster to Vector', 'Convert raster to polygons', 'gdal:polygonize', [('INPUT', 'layer', True, 'Input raster'), ('BAND', 'number', False, 'Band number', '1')]),
    ('rasterize', 'Vector to Raster', 'Rasterize vector layer', 'gdal:rasterize', [('INPUT', 'layer', True, 'Input vector'), ('FIELD', 'string', True, 'Burn-in field'), ('UNITS', 'number', False, 'Output units', '1'), ('WIDTH', 'number', True, 'Output width'), ('HEIGHT', 'number', True, 'Output height')]),
    ('fill_nodata', 'Fill NoData', 'Interpolate missing raster values', 'gdal:fillnodata', [('INPUT', 'layer', True, 'Input raster'), ('BAND', 'number', False, 'Band', '1'), ('DISTANCE', 'number', False, 'Search distance', '100')]),
    ('proximity', 'Proximity/Distance Raster', 'Distance to nearest non-zero cell', 'gdal:proximity', [('INPUT', 'layer', True, 'Input raster'), ('BAND', 'number', False, 'Band', '1')]),
    ('roughness', 'Roughness', 'Calculate terrain roughness', 'gdal:roughness', [('INPUT', 'layer', True, 'Input DEM')]),
    ('tpi', 'Topographic Position Index', 'Calculate TPI from DEM', 'gdal:tpitopographicpositionindex', [('INPUT', 'layer', True, 'Input DEM')]),
    ('tri', 'Terrain Ruggedness Index', 'Calculate TRI from DEM', 'gdal:triterrainruggednessindex', [('INPUT', 'layer', True, 'Input DEM')]),
    ('translate', 'Translate/Convert Raster', 'Convert raster format', 'gdal:translate', [('INPUT', 'layer', True, 'Input raster'), ('TARGET_CRS', 'string', False, 'Target CRS')]),
    ('build_vrt', 'Build Virtual Raster', 'Create VRT from multiple rasters', 'gdal:buildvirtualraster', [('INPUT', 'layer', True, 'Input raster layers')]),
    ('sample_raster', 'Sample Raster Values', 'Extract raster values at points', 'native:rastersampling', [('INPUT', 'layer', True, 'Input point layer'), ('RASTERCOPY', 'layer', True, 'Input raster')]),
    ('ndvi', 'NDVI Calculator', 'Compute NDVI from multispectral imagery', 'native:rastercalc', [('RED_BAND', 'layer', True, 'Red band raster'), ('NIR_BAND', 'layer', True, 'NIR band raster')]),
    ('ndwi', 'NDWI Calculator', 'Compute NDWI water index', 'native:rastercalc', [('GREEN_BAND', 'layer', True, 'Green band raster'), ('NIR_BAND', 'layer', True, 'NIR band raster')]),
    ('band_extract', 'Extract Single Band', 'Extract one band from multiband raster', 'gdal:translate', [('INPUT', 'layer', True, 'Input raster'), ('BAND', 'number', True, 'Band number to extract')]),
    ('rgb_composite', 'RGB Composite', 'Create RGB composite from bands', 'gdal:merge', [('RED', 'layer', True, 'Red band'), ('GREEN', 'layer', True, 'Green band'), ('BLUE', 'layer', True, 'Blue band')]),
]

import sys as _sys
_module=_sys.modules[__name__]
for _def in _TOOL_DEFS:
    _cls=_make_tool_class(*_def)
    setattr(_module,_cls.__name__,_cls)
del _sys,_module
