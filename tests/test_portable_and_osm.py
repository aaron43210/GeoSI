"""Portable data tools on real files, and OpenStreetMap download handling with a mocked network."""

import io
import json
import urllib.error
from unittest.mock import patch

import pytest

gpd = pytest.importorskip("geopandas")
from shapely.geometry import Point, Polygon  # noqa: E402

from geosi_engine.models import Layer  # noqa: E402
from geosi_engine.tools.portable import (  # noqa: E402
    CalculateFieldTool,
    CleanLayerTool,
    CountFeaturesTool,
    LoadLayerTool,
    SaveLayerTool,
    ValidateGeometryTool,
)


@pytest.fixture()
def hospitals(tmp_path):
    gdf = gpd.GeoDataFrame(
        {"name": ["H1", "H2", "H3"], "beds": [50, 150, 300]},
        geometry=[Point(0, 0), Point(1, 1), Point(2, 2)],
        crs="EPSG:4326",
    )
    path = tmp_path / "hospitals.geojson"
    gdf.to_file(path, driver="GeoJSON")
    return str(path)


def load(path):
    res = LoadLayerTool().execute(filepath=path)
    assert res.success, res.error
    return res.output


def test_load_vector_and_missing_or_unsupported_file(hospitals, tmp_path):
    layer = load(hospitals)
    assert (layer.name, layer.feature_count, layer.layer_type) == ("hospitals", 3, "vector")
    assert not LoadLayerTool().execute(filepath=str(tmp_path / "nope.gpkg")).success
    (tmp_path / "notes.txt").write_text("x")
    assert "Unsupported" in LoadLayerTool().execute(filepath=str(tmp_path / "notes.txt")).error


def test_save_roundtrip(hospitals, tmp_path):
    out = tmp_path / "copy.gpkg"
    assert SaveLayerTool().execute(layer_name=load(hospitals), filepath=str(out), driver="GPKG").success
    assert len(gpd.read_file(out)) == 3
    assert not SaveLayerTool().execute(layer_name="hospitals", filepath=str(out)).success


def test_calculate_field_and_reject_code(hospitals):
    layer = load(hospitals)
    res = CalculateFieldTool().execute(layer_name=layer, field_name="beds2", expression="beds * 2")
    assert res.success and list(res.output.features["beds2"]) == [100, 300, 600]
    evil = CalculateFieldTool().execute(layer_name=layer, field_name="x", expression="__import__('os').system('id')")
    assert not evil.success and "Disallowed" in evil.error


def test_count_from_layer_and_from_path(hospitals):
    assert CountFeaturesTool().execute(layer_name=load(hospitals)).output["count"] == 3
    assert CountFeaturesTool().execute(layer_name=hospitals).output == {"count": 3, "layer": "hospitals"}
    assert not CountFeaturesTool().execute(layer_name="/no/such/file.shp").success


def test_clean_and_validate_bowtie_polygon():
    bowtie = Polygon([(0, 0), (1, 1), (1, 0), (0, 1), (0, 0)])  # self-intersecting
    gdf = gpd.GeoDataFrame({"id": [1, 2]}, geometry=[bowtie, Polygon([(0, 0), (1, 0), (1, 1)])], crs="EPSG:4326")
    layer = Layer(name="zones", layer_type="vector", geometry_type="Polygon", feature_count=2, features=gdf)
    report = ValidateGeometryTool().execute(layer_name=layer)
    assert report.success and report.output["invalid"] == 1 and "1 invalid" in report.message
    cleaned = CleanLayerTool().execute(layer_name=layer)
    assert cleaned.success and cleaned.output.features.geometry.is_valid.all()
    assert ValidateGeometryTool().execute(layer_name=cleaned.output).output["invalid"] == 0


def test_tools_refuse_rasters():
    raster = Layer(name="dem", layer_type="raster")
    assert not CleanLayerTool().execute(layer_name=raster).success
    assert not ValidateGeometryTool().execute(layer_name=raster).success


# ── OpenStreetMap ───────────────────────────────────────────────────────

OVERPASS = {
    "elements": [
        {"type": "node", "id": 1, "lat": 53.80, "lon": -1.55, "tags": {"amenity": "hospital", "name": "LGI"}},
        {"type": "node", "id": 2, "lat": 53.81, "lon": -1.56, "tags": {"amenity": "hospital", "name": "St J"}},
        {"type": "node", "id": 10, "lat": 53.0, "lon": -1.0},
        {"type": "node", "id": 11, "lat": 53.0, "lon": -0.9},
        {"type": "node", "id": 12, "lat": 53.1, "lon": -0.9},
        {"type": "way", "id": 5, "nodes": [10, 11, 12, 10], "tags": {"amenity": "hospital", "name": "Campus"}},
    ]
}


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_fetch_osm_to_file_keeps_points_and_names_the_layer(tmp_path):
    from geosi_data import osm

    with patch.object(osm, "overpass_request", return_value=OVERPASS):
        found = osm.fetch_osm_to_file("hospitals", bbox=(53.7, -1.7, 53.9, -1.4), out_dir=str(tmp_path))
    data = json.load(open(found["path"]))
    assert found["name"] == "osm_hospitals" and found["geometry"] == "Point" and found["count"] == 3
    assert {f["properties"]["name"] for f in data["features"]} == {"LGI", "St J", "Campus"}


def test_fetch_osm_needs_a_place():
    from geosi_data import osm

    assert osm.fetch_osm_to_file("hospitals") is None


def test_overpass_moves_to_the_next_mirror_when_busy():
    from geosi_data import osm

    busy = urllib.error.HTTPError(osm.OVERPASS_MIRRORS[0], 502, "Bad Gateway", {}, None)
    with patch("urllib.request.urlopen", side_effect=[busy, _Resp(json.dumps(OVERPASS).encode())]) as op:
        assert osm.overpass_request("[out:json];") == OVERPASS
    assert op.call_args_list[1].args[0].full_url == osm.OVERPASS_MIRRORS[1]


def test_overpass_does_not_retry_a_bad_query():
    from geosi_data import osm

    bad = urllib.error.HTTPError(osm.OVERPASS_MIRRORS[0], 400, "Bad Request", {}, None)
    with patch("urllib.request.urlopen", side_effect=[bad]), pytest.raises(urllib.error.HTTPError):
        osm.overpass_request("nonsense")


def test_category_presets_resolve():
    from geosi_data import osm

    assert osm.resolve_category("hospitals") and osm.resolve_category("schools")
