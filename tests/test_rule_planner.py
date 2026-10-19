"""Offline planning end to end: parse → rule / deterministic plan, against stand-in QGIS tools."""

import pytest

from geosi_engine import GeoSI
from geosi_engine.base import PortableTool
from geosi_engine.models import Layer, ToolParameter, ToolResult, ToolSpec

# Stand-ins for the QGIS algorithms the planners use, with their real first parameters
TOOLS = {
    "native_buffer": ["INPUT", "DISTANCE"],
    "native_clip": ["INPUT", "OVERLAY"],
    "native_intersection": ["INPUT", "OVERLAY"],
    "native_union": ["INPUT", "OVERLAY"],
    "native_difference": ["INPUT", "OVERLAY"],
    "native_dissolve": ["INPUT", "FIELD"],
    "native_centroids": ["INPUT"],
    "native_fixgeometries": ["INPUT"],
    "native_simplifygeometries": ["INPUT", "TOLERANCE"],
    "native_minimumboundinggeometry": ["INPUT", "TYPE"],
    "native_voronoipolygons": ["INPUT"],
    "native_reprojectlayer": ["INPUT", "TARGET_CRS"],
    "native_slope": ["INPUT"],
    "native_aspect": ["INPUT"],
    "native_hillshade": ["INPUT"],
    "gdal_contour": ["INPUT", "INTERVAL"],
    "gdal_cliprasterbymasklayer": ["INPUT", "MASK"],
    "gdal_warpreproject": ["INPUT", "TARGET_CRS"],
    "native_rastercalc": ["EXPRESSION", "LAYERS"],
    "gdal_rastercalculator": ["INPUT_A", "BAND_A", "INPUT_B", "BAND_B", "FORMULA"],
    "native_basicstatisticsforfields": ["INPUT_LAYER", "FIELD_NAME"],
    "native_rasterlayerstatistics": ["INPUT", "BAND"],
    "native_extractbyexpression": ["INPUT", "EXPRESSION"],
    "native_extractbylocation": ["INPUT", "PREDICATE", "INTERSECT"],
    "native_creategrid": ["TYPE", "EXTENT", "HSPACING", "VSPACING", "CRS"],
    "native_mergevectorlayers": ["LAYERS"],
}


class _Stub(PortableTool):
    def __init__(self, name, params):
        self._name, self._params = name, params

    def spec(self):
        return ToolSpec(
            name=self._name,
            display_name=self._name.split("_", 1)[1].title(),
            description=self._name,
            category="test",
            parameters=[
                ToolParameter(p, "layer" if p.startswith("INPUT") else "string", False, p) for p in self._params
            ],
        )

    def execute(self, **kwargs):
        return ToolResult(success=True)


@pytest.fixture(scope="module")
def engine():
    eng = GeoSI(use_llm=False)
    for name, params in TOOLS.items():
        eng.registry.register_tool(_Stub(name, params))
    for name, geom, kind, fields, values in (
        ("hospitals", "Point", "vector", ["name", "beds"], {"name": ["H1", "H2"]}),
        ("parcels", "Polygon", "vector", ["owner", "area"], {"owner": ["A", "B", "C"]}),
        ("flood_zones", "Polygon", "vector", ["zone"], {"zone": ["Z1", "Z2"]}),
        ("roads", "LineString", "vector", ["road"], {"road": ["R1", "R2"]}),
        ("dem", "Raster", "raster", [], {}),
        ("image", "Raster", "raster", [], {}),
    ):
        eng.state.add_layer(
            Layer(
                name=name,
                geometry_type=geom,
                layer_type=kind,
                feature_count=3,
                fields=fields,
                field_types={f: ("number" if f in ("beds", "area") else "text") for f in fields},
                field_values=values,
            )
        )
    return eng


def plan(engine, query):
    request = engine.agent.parse(query, engine.state)
    result = engine.agent.plan(request, engine.state)
    assert result.steps, f"no plan for {query!r}: {result.reasoning}"
    step = result.steps[0]
    return step.tool_name, step.parameters


@pytest.mark.parametrize(
    "query, tool, expected",
    [
        ("buffer hospitals by 500 m", "native_buffer", {"INPUT": "hospitals", "DISTANCE": 500.0}),
        ("buffer roads by 2 miles", "native_buffer", {"INPUT": "roads", "DISTANCE": pytest.approx(3218.688)}),
        ("clip roads to flood_zones", "native_clip", {"INPUT": "roads", "OVERLAY": "flood_zones"}),
        ("intersect parcels with flood_zones", "native_intersection", {"INPUT": "parcels", "OVERLAY": "flood_zones"}),
        ("dissolve parcels by owner", "native_dissolve", {"INPUT": "parcels", "FIELD": ["owner"]}),
        ("dissolve flood_zones into one polygon", "native_dissolve", {"INPUT": "flood_zones"}),
        ("create centroids of flood_zones", "native_centroids", {"INPUT": "flood_zones"}),
        ("fix geometries of parcels", "native_fixgeometries", {"INPUT": "parcels"}),
        ("create a convex hull around hospitals", "native_minimumboundinggeometry", {"TYPE": 3}),
        ("create voronoi polygons from hospitals", "native_voronoipolygons", {"INPUT": "hospitals"}),
        ("reproject parcels to EPSG:4326", "native_reprojectlayer", {"TARGET_CRS": "EPSG:4326"}),
        ("calculate slope from dem", "native_slope", {"INPUT": "dem"}),
        ("compute aspect of dem", "native_aspect", {"INPUT": "dem"}),
        ("create a hillshade of dem", "native_hillshade", {"INPUT": "dem"}),
        ("generate contour lines every 50 m from dem", "gdal_contour", {"INTERVAL": 50.0}),
        ("clip dem to flood_zones", "gdal_cliprasterbymasklayer", {"INPUT": "dem", "MASK": "flood_zones"}),
        ("reproject dem to EPSG:4326", "gdal_warpreproject", {"TARGET_CRS": "EPSG:4326"}),
        (
            "calculate NDVI from image using band 3 as red and band 4 as NIR",
            "gdal_rastercalculator",
            {"INPUT_A": "image", "BAND_A": 4, "BAND_B": 3},
        ),
        (
            "what is the total number of beds across all hospitals?",
            "native_basicstatisticsforfields",
            {"INPUT_LAYER": "hospitals", "FIELD_NAME": "beds"},
        ),
        (
            "how many hospitals are inside flood_zones?",
            "native_extractbylocation",
            {"INPUT": "hospitals", "PREDICATE": "intersect", "INTERSECT": "flood_zones"},
        ),
        (
            "create a 1 km grid of polygons covering parcels",
            "native_creategrid",
            {"EXTENT": "parcels", "HSPACING": 1000.0},
        ),
        ("merge flood_zones and parcels", "native_mergevectorlayers", {"LAYERS": ["flood_zones", "parcels"]}),
    ],
)
def test_offline_plans(engine, query, tool, expected):
    got_tool, params = plan(engine, query)
    assert got_tool == tool
    for key, value in expected.items():
        assert params.get(key) == value, (key, params)


def test_attribute_filter_uses_real_field_values(engine):
    tool, params = plan(engine, "hospitals with more than 100 beds")
    assert tool == "native_extractbyexpression" and "beds" in params["EXPRESSION"] and "100" in params["EXPRESSION"]


def test_no_layers_loaded_blocks_spatial_tasks():
    eng = GeoSI(use_llm=False)
    req = eng.agent.parse("buffer hospitals by 500 m", eng.state)
    result = eng.agent.plan(req, eng.state)
    assert not result.steps and "No layers loaded" in result.reasoning


def test_conversational_query_gets_empty_plan(engine):
    req = engine.agent.parse("explain what a buffer is", engine.state)
    result = engine.agent.plan(req, engine.state)
    assert not result.steps and result.plan_source == "conversational"
