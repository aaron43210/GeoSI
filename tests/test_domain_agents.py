"""Remote sensing, geology and machine-learning agents on small synthetic data."""

import os
from types import SimpleNamespace

import numpy as np
import pytest

rasterio = pytest.importorskip("rasterio")
from rasterio.transform import from_origin  # noqa: E402

from geosi_engine.agents.geology import GeologyAgent, GeologyJobRequest, weighted_overlay  # noqa: E402
from geosi_engine.agents.machine_learning import MachineLearningAgent, MLJobRequest  # noqa: E402
from geosi_engine.agents.remote_sensing import RasterJobRequest, RemoteSensingAgent, derived_path  # noqa: E402


def write_tif(path, bands, nodata=None):
    bands = [np.asarray(b, dtype="float32") for b in bands]
    h, w = bands[0].shape
    profile = dict(
        driver="GTiff",
        height=h,
        width=w,
        count=len(bands),
        dtype="float32",
        crs="EPSG:32633",
        transform=from_origin(500000, 4000000, 10, 10),
        nodata=nodata,
    )
    with rasterio.open(path, "w", **profile) as dst:
        for i, b in enumerate(bands, start=1):
            dst.write(b, i)
    return str(path)


def read(path):
    with rasterio.open(path) as src:
        return src.read(1), src.nodata


class AllowAll:
    """Permission agent stand-in that allows everything and records audits."""

    def __init__(self):
        self.audits = []

    def check_permission(self, tool, risk):
        return SimpleNamespace(decision="allow")

    def audit_log_before_execution(self, step, session_id="", decision=None):
        return "audit-1"

    def update_audit_log(self, audit_id, status, error=None):
        self.audits.append(status)


# ── Remote sensing ──────────────────────────────────────────────────────


def test_ndvi_is_correct_per_pixel_and_keeps_nodata(tmp_path):
    red = [[10, 20], [30, -9999]]
    nir = [[30, 20], [10, -9999]]
    src = write_tif(tmp_path / "scene.tif", [red, nir], nodata=-9999)
    res = RemoteSensingAgent(None, AllowAll()).compute_spectral_index("ndvi", src, {"RED": 1, "NIR": 2})
    assert res.success, res.error
    out, nodata = read(res.output_layer)
    assert np.allclose(out[0], [0.5, 0.0]) and np.isclose(out[1][0], -0.5)
    assert out[1][1] == nodata == -9999
    assert res.statistics["min"] == pytest.approx(-0.5) and res.statistics["max"] == pytest.approx(0.5)


def test_uppercase_extension_never_overwrites_the_input(tmp_path):
    src = write_tif(tmp_path / "SCENE.TIF", [[[1, 2]], [[3, 4]]])
    before = open(src, "rb").read()
    res = RemoteSensingAgent(None, AllowAll()).compute_spectral_index("NDVI", src, {"RED": 1, "NIR": 2})
    assert res.success and res.output_layer != src
    assert open(src, "rb").read() == before
    assert derived_path("/d/x.tif/a.TIF", "NDVI") == "/d/x.tif/a_NDVI.tif"


def test_unknown_index_is_rejected(tmp_path):
    res = RemoteSensingAgent(None, AllowAll()).compute_spectral_index("FOO", "x.tif", {})
    assert not res.success and "NDVI" in res.error


def test_change_detection_counts_changed_pixels(tmp_path):
    t1 = write_tif(tmp_path / "t1.tif", [[[0, 0], [0, 0]]])
    t2 = write_tif(tmp_path / "t2.tif", [[[0, 1], [0, 5]]])
    job = RasterJobRequest("change_detection", "Sentinel-2", [t1, t2], {"threshold": 0.5})
    res = RemoteSensingAgent(None, AllowAll())._dispatch(job)
    assert res.success and res.statistics["changed_pixels"] == 2 and res.statistics["pct_changed"] == 50.0


def test_change_detection_needs_two_layers():
    res = RemoteSensingAgent(None, AllowAll())._dispatch(RasterJobRequest("change_detection", "S2", ["a.tif"]))
    assert not res.success


def test_dos1_subtracts_the_dark_object(tmp_path):
    src = write_tif(tmp_path / "img.tif", [[[5, 6], [105, 205]]])
    res = RemoteSensingAgent(None, AllowAll()).atmospheric_correction(src)
    out, _ = read(res.output_layer)
    assert res.success and out.min() == pytest.approx(0, abs=0.1) and out.max() < 205


def test_execute_runs_through_permission_and_audit(tmp_path):
    src = write_tif(tmp_path / "s.tif", [[[1, 2]], [[3, 4]]])
    perm = AllowAll()
    job = RasterJobRequest("spectral_index", "S2", [src], {"index": "NDVI", "bands": {"RED": 1, "NIR": 2}})
    res = RemoteSensingAgent(SimpleNamespace(), perm).execute(job)
    assert res.success and perm.audits == ["success"]


# ── Geology ─────────────────────────────────────────────────────────────


def test_overlay_uses_every_layer_and_can_reach_high_scores(tmp_path):
    slope = write_tif(tmp_path / "slope.tif", [[[0, 10], [20, 30]]])
    litho = write_tif(tmp_path / "litho.tif", [[[0, 1], [2, 3]]])
    score, _, weights = weighted_overlay([slope, litho], [0.4, 0.3])
    assert weights == pytest.approx([0.5714, 0.4286], abs=1e-3)
    assert score.max() == pytest.approx(1.0) and score.min() == pytest.approx(0.0)


def test_overlay_masks_nodata(tmp_path):
    a = write_tif(tmp_path / "a.tif", [[[-9999, 0], [5, 10]]], nodata=-9999)
    score, _, _ = weighted_overlay([a], [1])
    assert np.isnan(score[0][0]) and score[1][1] == pytest.approx(1.0) and score[1][0] == pytest.approx(0.5)


def test_overlay_rejects_mismatched_grids(tmp_path):
    a = write_tif(tmp_path / "a.tif", [[[0, 1], [2, 3]]])
    b = write_tif(tmp_path / "b.tif", [[[0, 1, 2]]])
    with pytest.raises(ValueError, match="same grid"):
        weighted_overlay([a, b], [1, 1])


def test_landslide_reports_real_high_risk_share(tmp_path):
    slope = write_tif(tmp_path / "slope.tif", [[[0, 0], [30, 30]]])
    litho = write_tif(tmp_path / "litho.tif", [[[0, 0], [3, 3]]])
    agent = GeologyAgent(None, AllowAll())
    res = agent.landslide_susceptibility(GeologyJobRequest("landslide_susceptibility", [slope, litho]), [])
    assert res.success and res.statistics["high_risk_pct"] == 50.0
    assert os.path.isfile(res.output_layer)


def test_landslide_needs_a_layer():
    res = GeologyAgent(None, AllowAll()).landslide_susceptibility(GeologyJobRequest("x", []), [])
    assert not res.success


def test_mineral_prospectivity_equal_weights(tmp_path):
    a = write_tif(tmp_path / "a.tif", [[[0, 1]]])
    b = write_tif(tmp_path / "b.tif", [[[0, 1]]])
    res = GeologyAgent(None, AllowAll()).mineral_prospectivity(GeologyJobRequest("x", [a, b]), [])
    assert res.success and res.statistics["weights_used"] == [0.5, 0.5]
    assert res.statistics["high_prospectivity_pct"] == 50.0


# ── Machine learning ────────────────────────────────────────────────────

gpd = pytest.importorskip("geopandas")
pytest.importorskip("sklearn")


def points(tmp_path, n_per=10):
    from shapely.geometry import Point

    rng = np.random.default_rng(0)
    pts, cls, val = [], [], []
    for cx, label in ((0, "a"), (1000, "b")):
        for _ in range(n_per):
            pts.append(Point(cx + rng.normal(0, 5), rng.normal(0, 5)))
            cls.append(label)
            val.append(cx / 10 + rng.normal(0, 1))
    gdf = gpd.GeoDataFrame({"klass": cls, "value": val, "x": [p.x for p in pts]}, geometry=pts, crs="EPSG:32633")
    path = tmp_path / "pts.gpkg"
    gdf.to_file(path, driver="GPKG")
    return str(path)


def test_spatial_kmeans_finds_the_two_groups_and_writes_labels(tmp_path):
    src = points(tmp_path)
    res = MachineLearningAgent(None, AllowAll())._dispatch(
        MLJobRequest("clustering", "kmeans", [src], parameters={"n_clusters": 2})
    )
    assert res.success and res.metrics["n_clusters"] == 2 and res.metrics["silhouette_score"] > 0.9
    out = gpd.read_file(res.output_path)
    assert out.groupby("klass")["cluster"].nunique().max() == 1  # each true group is one cluster


def test_classifier_learns_from_target(tmp_path):
    src = points(tmp_path, 20)
    res = MachineLearningAgent(None, AllowAll())._dispatch(
        MLJobRequest("classification", "random_forest", [src], feature_columns=["x"], target_column="klass")
    )
    assert res.success and res.metrics["accuracy"] == 1.0 and os.path.isfile(res.output_path)


def test_regressor_and_prediction(tmp_path):
    src = points(tmp_path, 20)
    agent = MachineLearningAgent(None, AllowAll())
    trained = agent._dispatch(MLJobRequest("regression", "random_forest", [src], ["x"], "value"))
    assert trained.success and trained.metrics["r2_score"] > 0.9
    pred = agent._dispatch(MLJobRequest("predict", "random_forest", [src], ["x"], model_path=trained.output_path))
    assert pred.success and pred.metrics["n_predictions"] == 40


def test_supervised_jobs_need_a_target(tmp_path):
    res = MachineLearningAgent(None, AllowAll())._dispatch(MLJobRequest("classification", "random_forest", ["x"]))
    assert not res.success and "target_column" in res.error


def test_unknown_job_and_algorithm(tmp_path):
    agent = MachineLearningAgent(None, AllowAll())
    assert not agent._dispatch(MLJobRequest("forecast", "lstm")).success
    src = points(tmp_path)
    assert not agent._dispatch(MLJobRequest("clustering", "spectral", [src])).success
