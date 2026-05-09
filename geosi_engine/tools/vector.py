# -*- coding: utf-8 -*-
"""
GeoSI Engine — Vector Geometry & Overlay Tools (40 tools)

Auto-discovered by ToolRegistry. Each class is a concrete GISTool.
See FILE_CONNECTIONS.md for architecture.
"""

from geosi_engine.base import QGISProcessingTool, PortableTool
from geosi_engine.models import ToolSpec, ToolParameter, ToolResult, Layer


# ═══════════════════════════════════════════════════════════════
# Factory: build QGIS-backed tool classes from specifications
# ═══════════════════════════════════════════════════════════════

def _make_tool_class(name, display, desc, alg, params, cat="vector"):
    """Create a QGISProcessingTool subclass dynamically."""
    param_objs = [
        ToolParameter(
            name=p[0], param_type=p[1], required=p[2],
            description=p[3], default=p[4] if len(p) > 4 else None
        ) for p in params
    ]
    return type(name.title().replace("_", "") + "Tool", (QGISProcessingTool,), {
        "__init__": lambda self: QGISProcessingTool.__init__(
            self, name=name, description=desc, category=cat,
            qgis_algorithm=alg, parameters=param_objs,
            display_name=display, tags=[name] + name.split("_")
        )
    })


# ═══════════════════════════════════════════════════════════════
# Tool definitions — each tuple is:
#   (name, display_name, description, qgis_algorithm, params)
# ═══════════════════════════════════════════════════════════════

_TOOL_DEFS = [
    ('buffer', 'Buffer', 'Create buffer zones around features', 'native:buffer', [('INPUT', 'layer', True, 'Input vector layer'), ('DISTANCE', 'number', True, 'Buffer distance'), ('SEGMENTS', 'number', False, 'Number of segments', '5'), ('DISSOLVE', 'boolean', False, 'Dissolve results', 'False')]),
    ('intersect', 'Intersection', 'Find overlapping areas between two layers', 'native:intersection', [('INPUT', 'layer', True, 'Input layer'), ('OVERLAY', 'layer', True, 'Overlay layer')]),
    ('union_layer', 'Union', 'Combine two layers into one', 'native:union', [('INPUT', 'layer', True, 'Input layer'), ('OVERLAY', 'layer', True, 'Overlay layer')]),
    ('difference', 'Difference', 'Remove areas of overlay from input', 'native:difference', [('INPUT', 'layer', True, 'Input layer'), ('OVERLAY', 'layer', True, 'Overlay layer')]),
    ('symmetric_difference', 'Symmetric Difference', 'Keep non-overlapping areas from both layers', 'native:symmetricaldifference', [('INPUT', 'layer', True, 'Input layer'), ('OVERLAY', 'layer', True, 'Overlay layer')]),
    ('clip', 'Clip', 'Clip input layer to overlay extent', 'native:clip', [('INPUT', 'layer', True, 'Input layer'), ('OVERLAY', 'layer', True, 'Clip boundary')]),
    ('dissolve', 'Dissolve', 'Merge features by attribute', 'native:dissolve', [('INPUT', 'layer', True, 'Input layer'), ('FIELD', 'string', False, 'Dissolve field')]),
    ('centroid', 'Centroids', 'Calculate polygon centroids', 'native:centroids', [('INPUT', 'layer', True, 'Input layer')]),
    ('convex_hull', 'Convex Hull', 'Create convex hull polygons', 'native:convexhull', [('INPUT', 'layer', True, 'Input layer')]),
    ('voronoi', 'Voronoi Polygons', 'Create Voronoi/Thiessen polygons', 'native:voronoipolygons', [('INPUT', 'layer', True, 'Input point layer')]),
    ('delaunay', 'Delaunay Triangulation', 'Create Delaunay triangulation', 'native:delaunaytriangulation', [('INPUT', 'layer', True, 'Input point layer')]),
    ('simplify', 'Simplify Geometry', 'Reduce vertex count', 'native:simplifygeometries', [('INPUT', 'layer', True, 'Input layer'), ('TOLERANCE', 'number', True, 'Simplification tolerance')]),
    ('smooth', 'Smooth Geometry', 'Smooth jagged geometries', 'native:smoothgeometry', [('INPUT', 'layer', True, 'Input layer'), ('ITERATIONS', 'number', False, 'Smooth iterations', '1')]),
    ('densify', 'Densify Geometry', 'Add vertices along edges', 'native:densifygeometries', [('INPUT', 'layer', True, 'Input layer'), ('INTERVAL', 'number', True, 'Interval distance')]),
    ('multipart_to_singlepart', 'Multipart to Singleparts', 'Split multipart features', 'native:multiparttosingleparts', [('INPUT', 'layer', True, 'Input layer')]),
    ('merge_layers', 'Merge Vector Layers', 'Combine multiple layers', 'native:mergevectorlayers', [('LAYERS', 'layer', True, 'Layers to merge')]),
    ('reproject', 'Reproject Layer', 'Change coordinate reference system', 'native:reprojectlayer', [('INPUT', 'layer', True, 'Input layer'), ('TARGET_CRS', 'string', True, 'Target CRS e.g. EPSG:4326')]),
    ('fix_geometries', 'Fix Geometries', 'Repair invalid geometries', 'native:fixgeometries', [('INPUT', 'layer', True, 'Input layer')]),
    ('spatial_join', 'Spatial Join', 'Join attributes by location', 'native:joinattributesbylocation', [('INPUT', 'layer', True, 'Input layer'), ('JOIN', 'layer', True, 'Join layer'), ('PREDICATE', 'string', False, 'Spatial predicate', 'intersects')]),
    ('nearest_join', 'Nearest Neighbor Join', 'Join by closest feature', 'native:joinbynearest', [('INPUT', 'layer', True, 'Input layer'), ('INPUT_2', 'layer', True, 'Join layer'), ('MAX_DISTANCE', 'number', False, 'Max search distance')]),
    ('select_by_location', 'Select by Location', 'Select features by spatial relationship', 'native:selectbylocation', [('INPUT', 'layer', True, 'Input layer'), ('INTERSECT', 'layer', True, 'Selection layer'), ('PREDICATE', 'string', False, 'Predicate', 'intersects')]),
    ('extract_by_attribute', 'Extract by Attribute', 'Filter features by attribute value', 'native:extractbyattribute', [('INPUT', 'layer', True, 'Input layer'), ('FIELD', 'string', True, 'Field name'), ('OPERATOR', 'number', True, 'Operator (0 for =)', '0'), ('VALUE', 'string', True, 'Filter value')]),
    ('extract_by_extent', 'Extract by Extent', 'Filter features by bounding box', 'native:extractbyextent', [('INPUT', 'layer', True, 'Input layer'), ('EXTENT', 'string', True, 'Extent as xmin,ymin,xmax,ymax')]),
    ('random_points', 'Random Points in Extent', 'Generate random points', 'native:randompointsinextent', [('EXTENT', 'string', True, 'Extent'), ('POINTS_NUMBER', 'number', True, 'Number of points'), ('MIN_DISTANCE', 'number', False, 'Min distance between points', '0')]),
    ('grid_create', 'Create Grid', 'Generate a regular grid', 'native:creategrid', [('TYPE', 'number', True, 'Grid type 0=point 1=line 2=rect'), ('EXTENT', 'string', True, 'Grid extent'), ('HSPACING', 'number', True, 'Horizontal spacing'), ('VSPACING', 'number', True, 'Vertical spacing')]),
    ('points_along_lines', 'Points Along Lines', 'Create points at intervals along lines', 'native:pointsalonglines', [('INPUT', 'layer', True, 'Input line layer'), ('DISTANCE', 'number', True, 'Distance between points')]),
    ('polygonize', 'Lines to Polygons', 'Convert lines to polygons', 'native:polygonize', [('INPUT', 'layer', True, 'Input line layer')]),
    ('polygons_to_lines', 'Polygons to Lines', 'Convert polygons to boundary lines', 'native:polygonstolines', [('INPUT', 'layer', True, 'Input polygon layer')]),
    ('explode_lines', 'Explode Lines', 'Split lines at vertices', 'native:explodelines', [('INPUT', 'layer', True, 'Input line layer')]),
    ('extend_lines', 'Extend Lines', 'Extend lines by distance', 'native:extendlines', [('INPUT', 'layer', True, 'Input line layer'), ('START_DISTANCE', 'number', True, 'Start extension'), ('END_DISTANCE', 'number', True, 'End extension')]),
    ('offset_line', 'Offset Lines', 'Create parallel offset lines', 'native:offsetline', [('INPUT', 'layer', True, 'Input line layer'), ('DISTANCE', 'number', True, 'Offset distance')]),
    ('bounding_boxes', 'Bounding Boxes', 'Create bounding rectangles', 'native:boundingboxes', [('INPUT', 'layer', True, 'Input layer')]),
    ('minimum_enclosing_circle', 'Minimum Enclosing Circle', 'Smallest circle enclosing each feature', 'native:minimumenclosingcircle', [('INPUT', 'layer', True, 'Input layer')]),
    ('concave_hull', 'Concave Hull', 'Create concave hull polygons', 'native:concavehull', [('INPUT', 'layer', True, 'Input point layer'), ('ALPHA', 'number', False, 'Alpha parameter', '0.3')]),
    ('aggregate', 'Aggregate', 'Group and aggregate features', 'native:aggregate', [('INPUT', 'layer', True, 'Input layer'), ('GROUP_BY', 'string', True, 'Group by expression'), ('AGGREGATES', 'string', True, 'Aggregation definitions')]),
    ('add_geometry_attributes', 'Add Geometry Attributes', 'Calculate area/length/perimeter', 'native:addgeometryattributes', [('INPUT', 'layer', True, 'Input layer'), ('CALC_METHOD', 'number', False, 'Calculation method', '0')]),
    ('count_points_in_polygon', 'Count Points in Polygon', 'Count points per polygon', 'native:countpointsinpolygon', [('POLYGONS', 'layer', True, 'Polygon layer'), ('POINTS', 'layer', True, 'Point layer'), ('FIELD', 'string', False, 'Count field name', 'NUMPOINTS')]),
    ('distance_matrix', 'Distance Matrix', 'Calculate distances between point layers', 'native:distancematrix', [('INPUT', 'layer', True, 'Input point layer'), ('INPUT_FIELD', 'string', True, 'Input ID field'), ('TARGET', 'layer', True, 'Target point layer'), ('TARGET_FIELD', 'string', True, 'Target ID field')]),
    ('mean_coordinates', 'Mean Coordinates', 'Calculate mean coordinate center', 'native:meancoordinates', [('INPUT', 'layer', True, 'Input layer'), ('WEIGHT', 'string', False, 'Weight field')]),
    ('snap_to_grid', 'Snap to Grid', 'Snap geometries to a regular grid', 'native:snappointstogrid', [('INPUT', 'layer', True, 'Input layer'), ('HSPACING', 'number', True, 'Horizontal spacing'), ('VSPACING', 'number', True, 'Vertical spacing')]),
]

# ═══════════════════════════════════════════════════════════════
# Custom Tools (GIS Perspective: Auto-detecting schemas, preprocessing)
# ═══════════════════════════════════════════════════════════════

class JoinAttributesTool(QGISProcessingTool):
    """
    Smart Join Attributes tool.
    Automatically detects the best fields to join on if none are provided,
    taking a GIS perspective on common attribute schemas (e.g. DISTRICT, NAME, ID).
    """
    def __init__(self):
        super().__init__(
            name="join_attributes",
            display_name="Join Attributes by Field",
            description="Join tabular data to a layer, auto-detecting common fields if missing.",
            qgis_algorithm="native:joinattributestable",
            category="vector",
            tags=["join", "attribute", "merge", "table"],
            parameters=[
                ToolParameter(name="INPUT", param_type="layer", required=True, description="Input layer"),
                ToolParameter(name="FIELD", param_type="string", required=False, description="Table field"),
                ToolParameter(name="INPUT_2", param_type="layer", required=True, description="Join layer"),
                ToolParameter(name="FIELD_2", param_type="string", required=False, description="Join field")
            ]
        )

    def execute(self, **kwargs) -> ToolResult:
        import logging
        logger = logging.getLogger("geosi_engine.tools.vector")
        
        # Auto-detect fields if missing
        if not kwargs.get("FIELD") or not kwargs.get("FIELD_2"):
            layer1 = kwargs.get("INPUT")
            layer2 = kwargs.get("INPUT_2")
            
            if layer1 and layer2 and hasattr(layer1, "features") and hasattr(layer2, "features"):
                ql1 = layer1.features
                ql2 = layer2.features
                if ql1 and ql2:
                    try:
                        fields1 = [f.name() for f in ql1.fields()]
                        fields2 = [f.name() for f in ql2.fields()]
                        
                        # Priority 1: Identical names ignoring case (excluding generic IDs)
                        common = None
                        skip_generic = {"id", "fid", "objectid", "shape_area", "shape_length"}
                        for f1 in fields1:
                            for f2 in fields2:
                                if f1.lower() == f2.lower() and f1.lower() not in skip_generic:
                                    common = (f1, f2)
                                    break
                            if common: break
                        
                        # Priority 2: Generic IDs if nothing else matches
                        if not common:
                            for f1 in fields1:
                                for f2 in fields2:
                                    if f1.lower() == f2.lower():
                                        common = (f1, f2)
                                        break
                                if common: break
                                
                        if common:
                            kwargs["FIELD"] = common[0]
                            kwargs["FIELD_2"] = common[1]
                            logger.info(f"GIS Preprocessing: Auto-detected join fields: {common[0]} = {common[1]}")
                        else:
                            # Fallback to first field of each (risky but better than crashing)
                            if fields1 and fields2:
                                kwargs["FIELD"] = fields1[0]
                                kwargs["FIELD_2"] = fields2[0]
                                logger.warning("GIS Preprocessing: No common fields found. Guessing first fields.")
                    except Exception as e:
                        logger.error(f"Auto-detect fields failed: {e}")
        
        return super().execute(**kwargs)


# ═══════════════════════════════════════════════════════════════
# Generate all tool classes and inject into module namespace
# ═══════════════════════════════════════════════════════════════

import sys as _sys
_module = _sys.modules[__name__]

for _def in _TOOL_DEFS:
    _cls = _make_tool_class(*_def)
    setattr(_module, _cls.__name__, _cls)

# Clean up namespace
del _sys, _module, _def, _cls


# ═══════════════════════════════════════════════════════════════
# Smart extract tool — searches all text fields for a name
# ═══════════════════════════════════════════════════════════════

class ExtractByNameTool(QGISProcessingTool):
    """Extract features from a layer where ANY text field contains the search term.
    
    This enables queries like 'extract Thiruvananthapuram from Kerala' without
    the user needing to know the exact field name (DISTRICT, NAME, etc.).
    """
    def __init__(self):
        super().__init__(
            name="extract_by_name",
            display_name="Extract Features by Name",
            description="Extract features from a layer by searching all text attribute fields for a name",
            category="vector",
            qgis_algorithm="native:extractbyexpression",
            parameters=[
                ToolParameter("INPUT", "layer", True, "Input layer to search"),
                ToolParameter("SEARCH_TERM", "string", True, "Name to search for in attribute table"),
            ],
            tags=["extract", "filter", "attribute", "search", "name", "select"]
        )

    def execute(self, **kwargs) -> ToolResult:
        layer = kwargs.get("INPUT")
        search_term = kwargs.get("SEARCH_TERM")

        if layer is None:
            return ToolResult(success=False, error="Missing required parameter: INPUT")
        if not search_term:
            return ToolResult(success=False, error="Missing required parameter: SEARCH_TERM")

        # Build a QGIS expression that searches ALL text fields using ILIKE.
        # We get the field names from the QgsVectorLayer and build:
        #   "FIELD1" ILIKE '%search%' OR "FIELD2" ILIKE '%search%' OR ...
        qgis_layer = getattr(layer, 'features', None)
        if qgis_layer is None:
            return ToolResult(success=False, error=f"Layer '{getattr(layer, 'name', layer)}' has no QGIS reference")

        try:
            # Get all field names from the layer
            field_names = [f.name() for f in qgis_layer.fields()]
            if not field_names:
                return ToolResult(success=False, error=f"Layer has no attribute fields")
            
            # Build OR expression across all fields
            # Escape single quotes in search term
            safe_term = search_term.replace("'", "''")
            clauses = [f'"{fname}" ILIKE \'%{safe_term}%\'' for fname in field_names]
            expression = " OR ".join(clauses)
            
            print(f"[GeoSI extract_by_name] Searching '{search_term}' across {len(field_names)} fields")
            print(f"[GeoSI extract_by_name] Expression: {expression[:200]}...")
        except Exception as e:
            return ToolResult(success=False, error=f"Failed to inspect layer fields: {e}")

        params = {
            "INPUT": layer,
            "EXPRESSION": expression,
            "OUTPUT": "TEMPORARY_OUTPUT"
        }

        from geosi_engine.base import get_backend
        fn = get_backend(self._backend_name)
        if fn is None:
            return ToolResult(success=False, error="No backend registered.")
        return fn(self._algorithm, params)
