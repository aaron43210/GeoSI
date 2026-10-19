"""Workspace upload and map-visualisation API routes (FastAPI TestClient, no QGIS)."""

import contextlib
import io
import json
import zipfile

import pytest

pytest.importorskip("multipart")
gpd = pytest.importorskip("geopandas")
from fastapi.testclient import TestClient  # noqa: E402
from shapely.geometry import Point, Polygon  # noqa: E402

AUTH = {"Authorization": "Bearer test-key-unit"}
SID = "viz-test-session"


@pytest.fixture()
def client(tmp_path, monkeypatch):
    import geosi_server.qgis_runtime as rt
    from geosi_server.app import app, get_pool

    monkeypatch.setattr(rt, "_DATA_DIR", tmp_path)
    get_pool()  # make sure the pool exists
    yield TestClient(app)
    pool = get_pool()
    remove = getattr(pool, "remove", None) or getattr(pool, "evict", None)
    if remove:
        with contextlib.suppress(Exception):
            remove(SID)


def geojson_bytes(n=3):
    gdf = gpd.GeoDataFrame(
        {"name": [f"H{i}" for i in range(n)], "beds": list(range(n))},
        geometry=[Point(500000 + i * 100, 4000000) for i in range(n)],
        crs="EPSG:32633",
    )
    return gdf.to_json().encode()


def upload(client, name, data):
    return client.post(
        f"/workspace/layers?session_id={SID}",
        headers=AUTH,
        files={"file": (name, io.BytesIO(data), "application/octet-stream")},
    )


def test_upload_list_download_delete(client):
    r = upload(client, "hospitals.geojson", geojson_bytes())
    assert r.status_code == 201 and r.json()["name"] == "hospitals.geojson"
    names = [f["name"] for f in client.get(f"/workspace/layers?session_id={SID}", headers=AUTH).json()["files"]]
    assert "hospitals.geojson" in names
    dl = client.get(f"/workspace/layers/hospitals.geojson?session_id={SID}", headers=AUTH)
    assert dl.status_code == 200 and json.loads(dl.content)["type"] == "FeatureCollection"
    assert client.delete(f"/workspace/layers/hospitals.geojson?session_id={SID}", headers=AUTH).status_code in (
        200,
        204,
    )
    assert client.get(f"/workspace/layers/hospitals.geojson?session_id={SID}", headers=AUTH).status_code == 404


def test_upload_rejects_unknown_types_and_strips_paths(client):
    assert upload(client, "evil.exe", b"MZ").status_code == 422
    r = upload(client, "../../etc/zones.geojson", geojson_bytes())
    assert r.status_code == 201 and r.json()["name"] == "zones.geojson"


def test_zipped_shapefile_is_extracted(client, tmp_path):
    shp_dir = tmp_path / "src"
    shp_dir.mkdir()
    gpd.read_file(io.BytesIO(geojson_bytes())).to_file(shp_dir / "pts.shp")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for f in shp_dir.iterdir():
            z.write(f, f.name)
    r = upload(client, "pts.zip", buf.getvalue())
    assert r.status_code == 201 and r.json()["name"] == "pts.shp"


def test_zip_without_shapefile_or_too_big_is_rejected(client, monkeypatch):
    import geosi_server.workspace_routes as wr

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("readme.txt", "no shapefile here")
    assert upload(client, "a.zip", buf.getvalue()).status_code == 422

    monkeypatch.setattr(wr, "_MAX_UPLOAD_MB", 1)
    bomb = io.BytesIO()
    with zipfile.ZipFile(bomb, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("big.shp", b"\0" * (3 * 1024 * 1024))  # compresses to a few KB
    r = upload(client, "bomb.zip", bomb.getvalue())
    assert r.status_code == 422 and "expands to" in r.json()["detail"]


def test_load_then_visualise_as_wgs84_geojson(client):
    upload(client, "hospitals.geojson", geojson_bytes(5))
    r = client.post(f"/workspace/layers/hospitals.geojson/load?session_id={SID}", headers=AUTH)
    assert r.status_code == 200 and r.json()["success"], r.text
    layers = client.get(f"/viz/layers?session_id={SID}", headers=AUTH).json()["layers"]
    assert any(lyr["name"] == "hospitals" for lyr in layers)
    fc = client.get(f"/viz/layers/hospitals/geojson?session_id={SID}&limit=3", headers=AUTH).json()
    assert fc["type"] == "FeatureCollection" and len(fc["features"]) == 3
    lon, lat = fc["features"][0]["geometry"]["coordinates"]
    assert 10 < lon < 20 and 30 < lat < 40  # reprojected from UTM 33N to WGS84
    assert client.get(f"/viz/layers/hospitals/raster?session_id={SID}", headers=AUTH).status_code == 400


def test_viz_unknown_layer_and_missing_workspace_file(client):
    assert client.get(f"/viz/layers/nope/geojson?session_id={SID}", headers=AUTH).status_code == 404
    assert client.post(f"/workspace/layers/nope.geojson/load?session_id={SID}", headers=AUTH).status_code == 404


def test_polygon_layer_simplify(client):
    poly = Polygon([(500000, 4000000), (500100, 4000000), (500100, 4000100), (500000, 4000100)])
    data = gpd.GeoDataFrame({"zone": ["Z1"]}, geometry=[poly], crs="EPSG:32633").to_json().encode()
    upload(client, "zones.geojson", data)
    client.post(f"/workspace/layers/zones.geojson/load?session_id={SID}", headers=AUTH)
    fc = client.get(f"/viz/layers/zones/geojson?session_id={SID}&simplify=0.0001", headers=AUTH).json()
    assert fc["features"][0]["geometry"]["type"] == "Polygon"
