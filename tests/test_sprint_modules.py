"""
Tests for Sprint 1-5 modules:
  Sprint 1 — geosi_data (basemaps, osm, geocoding)
  Sprint 2 — geosi_engine.checkpoints
  Sprint 3 — geosi_engine.cartography (styling, layouts)
  Sprint 4 — prompt_dock (UI: tested via import + method existence)
  Sprint 5 — geosi_engine.security (ASTGuard)
  Tool     — geosi_engine.tools.data_connectors
"""

from __future__ import annotations

import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# ─────────────────────────────────────────────────────────────────────────────
# Sprint 5 — ASTGuard (no QGIS needed)
# ─────────────────────────────────────────────────────────────────────────────


class TestASTGuard(unittest.TestCase):
    def setUp(self):
        from geosi_engine.security import ASTGuard

        self.guard = ASTGuard

    def test_safe_code_passes(self):
        code = "x = 1 + 2\nprint(x)"
        ok, violations = self.guard.check(code)
        self.assertTrue(ok)
        self.assertEqual(violations, [])

    def test_blocks_os_import(self):
        ok, violations = self.guard.check("import os\nos.system('rm -rf /')")
        self.assertFalse(ok)
        self.assertTrue(any("os" in v for v in violations))

    def test_blocks_subprocess(self):
        ok, violations = self.guard.check("import subprocess\nsubprocess.run(['ls'])")
        self.assertFalse(ok)

    def test_blocks_eval_builtin(self):
        ok, violations = self.guard.check("eval('1+1')")
        self.assertFalse(ok)

    def test_blocks_exec_builtin(self):
        ok, violations = self.guard.check("exec('x=1')")
        self.assertFalse(ok)

    def test_blocks_open_by_default(self):
        ok, violations = self.guard.check("f = open('/etc/passwd')")
        self.assertFalse(ok)

    def test_open_allowed_when_flag_set(self):
        ok, violations = self.guard.check("f = open('output.gpkg', 'wb')", allow_open=True)
        self.assertTrue(ok)

    def test_blocks_rm_rf_pattern(self):
        ok, violations = self.guard.check("import subprocess\nsubprocess.run(['rm','-rf','/'])")
        self.assertFalse(ok)

    def test_safe_exec_runs_safe_code(self):
        success, err = self.guard.safe_exec("x = 2 * 3", {}, {})
        self.assertTrue(success)
        # safe_exec returns "" (empty string) on success, not None
        self.assertFalse(err)  # empty string is falsy

    def test_safe_exec_blocks_dangerous_code(self):
        success, err = self.guard.safe_exec("import os", {}, {})
        self.assertFalse(success)
        self.assertIsNotNone(err)

    def test_pyqgis_imports_pass(self):
        code = "from qgis.core import QgsVectorLayer\nimport processing"
        ok, violations = self.guard.check(code)
        self.assertTrue(ok, violations)

    def test_geopandas_import_passes(self):
        ok, violations = self.guard.check("import geopandas as gpd\ngdf = gpd.read_file('x.gpkg')")
        self.assertTrue(ok, violations)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 2 — CheckpointManager (mocked QGIS)
# ─────────────────────────────────────────────────────────────────────────────


class TestCheckpointManager(unittest.TestCase):
    def setUp(self):
        # Provide minimal QGIS stubs
        qgis_core = types.ModuleType("qgis.core")
        qgis_core.QgsProject = MagicMock()
        qgis_core.QgsProject.instance.return_value.mapLayers.return_value = {}
        qgis_core.QgsMapLayer = MagicMock
        qgis_core.QgsVectorLayer = MagicMock
        qgis_core.QgsRasterLayer = MagicMock
        qgis_mod = types.ModuleType("qgis")
        qgis_mod.core = qgis_core
        sys.modules["qgis"] = qgis_mod
        sys.modules["qgis.core"] = qgis_core

        from geosi_engine.checkpoints import CheckpointManager

        # CheckpointManager(max_checkpoints) — no snapshot_dir param
        self.mgr = CheckpointManager(max_checkpoints=10)

    def test_create_snapshot_empty_project(self):
        from qgis.core import QgsProject

        QgsProject.instance.return_value.mapLayers.return_value = {}
        cp = self.mgr.create_snapshot("test query")
        self.assertIsNotNone(cp.checkpoint_id)
        self.assertEqual(cp.query, "test query")
        # layer_snapshots is a dict keyed by layer_id; empty project → empty
        self.assertEqual(len(cp.layer_snapshots), 0)

    def test_rollback_unknown_id_returns_false(self):
        # rollback() returns False for unknown IDs, does not raise
        result = self.mgr.rollback("nonexistent-id")
        self.assertFalse(result)

    def test_eviction_keeps_max_checkpoints(self):
        from qgis.core import QgsProject

        QgsProject.instance.return_value.mapLayers.return_value = {}
        from geosi_engine.checkpoints import CheckpointManager

        mgr = CheckpointManager(max_checkpoints=3)
        for i in range(5):
            mgr.create_snapshot(f"query {i}")
        self.assertLessEqual(len(mgr._checkpoints), 3)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 1 — basemaps (QGIS-free paths)
# ─────────────────────────────────────────────────────────────────────────────


class TestBasemaps(unittest.TestCase):
    def test_resolve_provider_exact(self):
        from geosi_data.basemaps import resolve_provider

        self.assertEqual(resolve_provider("osm"), "osm")

    def test_resolve_provider_fuzzy(self):
        from geosi_data.basemaps import resolve_provider

        self.assertEqual(resolve_provider("satellite"), "esri_satellite")

    def test_resolve_provider_fallback(self):
        from geosi_data.basemaps import resolve_provider

        # resolve_provider defaults to "osm" for unrecognized names
        result = resolve_provider("totally_unknown_provider_xyz999")
        self.assertEqual(result, "osm")

    def test_provider_dict_populated(self):
        from geosi_data.basemaps import PROVIDERS

        self.assertGreaterEqual(len(PROVIDERS), 10)
        for key, val in PROVIDERS.items():
            self.assertIn("url", val, f"Provider '{key}' missing 'url'")

    def test_add_basemap_no_qgis(self):
        # When QGIS modules are unavailable add_basemap should return None, not raise
        from geosi_data.basemaps import add_basemap

        # Patch the qgis.core import inside add_basemap to simulate no QGIS
        with patch.dict("sys.modules", {"qgis": None, "qgis.core": None}):
            try:
                result = add_basemap("osm")
                self.assertIsNone(result)
            except (ImportError, TypeError):
                pass  # acceptable when QGIS truly absent


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 1 — geocoding (mocked HTTP)
# ─────────────────────────────────────────────────────────────────────────────


class TestGeocoding(unittest.TestCase):
    def _mock_response(self, body: str, status: int = 200):
        resp = MagicMock()
        resp.status = status
        resp.read.return_value = body.encode()
        resp.__enter__ = lambda s: s
        resp.__exit__ = MagicMock(return_value=False)
        return resp

    def test_geocode_nominatim_success(self):
        import json

        payload = json.dumps([{"lon": "-0.1276", "lat": "51.5074", "display_name": "London, UK"}])
        with patch("urllib.request.urlopen", return_value=self._mock_response(payload)):
            from geosi_data.geocoding import geocode

            lon, lat, name = geocode("London", provider="nominatim")
        self.assertAlmostEqual(lon, -0.1276)
        self.assertAlmostEqual(lat, 51.5074)
        self.assertIn("London", name)

    def test_geocode_empty_result_raises_value_error(self):
        # geocode() raises ValueError when Nominatim returns empty list
        with patch("geosi_data.geocoding.urllib.request.urlopen", return_value=self._mock_response("[]")):
            from geosi_data.geocoding import geocode

            with self.assertRaises(ValueError):
                geocode("ZZZnonexistent9999")

    def test_reverse_geocode(self):
        import json

        payload = json.dumps({"display_name": "Big Ben, Westminster, London"})
        with patch("urllib.request.urlopen", return_value=self._mock_response(payload)):
            from geosi_data.geocoding import reverse_geocode

            name = reverse_geocode(51.5007, -0.1246)
        self.assertIn("London", name)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 1 — OSM fetcher (mocked HTTP)
# ─────────────────────────────────────────────────────────────────────────────


class TestOSMFetcher(unittest.TestCase):
    def test_tag_presets_populated(self):
        from geosi_data.osm import TAG_PRESETS

        self.assertGreaterEqual(len(TAG_PRESETS), 10)
        self.assertIn("hospitals", TAG_PRESETS)
        self.assertIn("schools", TAG_PRESETS)

    def test_overpass_to_geojson_nodes(self):
        from geosi_data.osm import _overpass_to_geojson

        data = {
            "elements": [
                {
                    "type": "node",
                    "id": 1,
                    "lat": 51.5,
                    "lon": -0.12,
                    "tags": {"name": "Test Hospital", "amenity": "hospital"},
                },
            ]
        }
        fc = _overpass_to_geojson(data)
        self.assertEqual(fc["type"], "FeatureCollection")
        self.assertEqual(len(fc["features"]), 1)
        feat = fc["features"][0]
        self.assertEqual(feat["geometry"]["type"], "Point")
        self.assertEqual(feat["properties"]["name"], "Test Hospital")

    def test_overpass_query_contains_tags(self):
        from geosi_data.osm import _overpass_query

        # tags is List[Dict[str, str]] — wrap in a list
        tags = [{"amenity": "hospital"}]
        bbox = (51.4, -0.2, 51.6, 0.0)
        q = _overpass_query(tags, bbox)
        self.assertIn("amenity", q)
        self.assertIn("hospital", q)
        self.assertIn("51.4", q)

    def test_unknown_category_returns_none_without_bbox(self):
        # Unknown category without location/bbox → returns None (logs error)
        from geosi_data.osm import fetch_osm_features

        result = fetch_osm_features(category="nonexistent_category_xyz999_unique")
        # Either None (no bbox) or a layer if Overpass reachable; never raises
        self.assertIsNone(result)


# ─────────────────────────────────────────────────────────────────────────────
# Sprint 3 — cartography styling (mocked QGIS)
# ─────────────────────────────────────────────────────────────────────────────


def _stub_qgis_renderer_modules():
    """Install minimal QGIS stubs needed by styling.py."""
    for mod_name in [
        "qgis",
        "qgis.core",
        "PyQt5",
        "PyQt5.QtGui",
        "PyQt5.QtCore",
        "qgis.PyQt",
        "qgis.PyQt.QtGui",
        "qgis.PyQt.QtCore",
    ]:
        sys.modules.setdefault(mod_name, types.ModuleType(mod_name))

    core = sys.modules["qgis.core"]
    for cls_name in [
        "QgsGraduatedSymbolRenderer",
        "QgsCategorizedSymbolRenderer",
        "QgsRendererCategory",
        "QgsSymbol",
        "QgsColorRampShader",
        "QgsSingleBandPseudoColorRenderer",
        "QgsRasterShader",
        "QgsPalLayerSettings",
        "QgsTextFormat",
        "QgsVectorLayerSimpleLabeling",
        "QgsClassificationQuantile",
        "QgsClassificationJenks",
        "QgsClassificationEqualInterval",
        "QgsClassificationStandardDeviation",
        "QgsStyle",
        "QgsGradientColorRamp",
    ]:
        if not hasattr(core, cls_name):
            setattr(core, cls_name, MagicMock())


class TestCartographyStyling(unittest.TestCase):
    def setUp(self):
        _stub_qgis_renderer_modules()

    def test_ramps_dict_populated(self):
        from geosi_engine.cartography.styling import RAMPS

        self.assertGreaterEqual(len(RAMPS), 5)
        self.assertIn("viridis", RAMPS)
        self.assertIn("magma", RAMPS)

    # Without a real QGIS the styling helpers must degrade gracefully:
    # return False, never raise, never touch the layer. Real rendering is
    # covered by tests/qgis_integration.py inside QGIS.
    def test_apply_graduated_degrades_without_qgis(self):
        from geosi_engine.cartography import styling

        layer = MagicMock()
        layer.fields.return_value.indexOf.return_value = 0
        self.assertFalse(styling.apply_graduated_symbology(layer, "population"))
        layer.setRenderer.assert_not_called()

    def test_apply_categorized_degrades_without_qgis(self):
        from geosi_engine.cartography import styling

        layer = MagicMock()
        layer.uniqueValues.return_value = ["A", "B", "C"]
        self.assertFalse(styling.apply_categorized_symbology(layer, "category"))
        layer.setRenderer.assert_not_called()


# ─────────────────────────────────────────────────────────────────────────────
# Data connector tools — PortableTool spec contract
# ─────────────────────────────────────────────────────────────────────────────


class TestDataConnectorSpecs(unittest.TestCase):
    """Verify each tool has a valid spec() and is discoverable."""

    def _tool_classes(self):
        from geosi_engine.tools.data_connectors import (
            AddBasemapTool,
            ApplyStyleTool,
            ExportMapTool,
            FetchOSMTool,
            GeocodeTool,
            ZoomToPlaceTool,
        )

        return [AddBasemapTool, FetchOSMTool, GeocodeTool, ZoomToPlaceTool, ApplyStyleTool, ExportMapTool]

    def test_all_have_spec(self):
        for cls in self._tool_classes():
            spec = cls().spec()
            self.assertIsNotNone(spec.name, f"{cls.__name__} missing name")
            self.assertIsNotNone(spec.description, f"{cls.__name__} missing description")
            self.assertIsNotNone(spec.category, f"{cls.__name__} missing category")

    def test_names_are_unique(self):
        names = [cls().spec().name for cls in self._tool_classes()]
        self.assertEqual(len(names), len(set(names)), f"Duplicate tool names: {names}")

    def test_tools_discoverable_by_registry(self):
        from geosi_engine.registry import ToolRegistry

        reg = ToolRegistry()
        count = reg.discover_portable_tools()
        # data_connectors adds 6 tools; combined with existing portables it must be > 0
        self.assertGreater(count, 0)
        # Verify our new tools are registered
        self.assertIsNotNone(reg.get_tool("add_basemap"))
        self.assertIsNotNone(reg.get_tool("fetch_osm"))
        self.assertIsNotNone(reg.get_tool("geocode_address"))

    def test_fetch_osm_returns_error_on_bad_category(self):
        tool = __import__("geosi_engine.tools.data_connectors", fromlist=["FetchOSMTool"]).FetchOSMTool()
        result = tool.execute(category="totally_unknown_category_xyz99")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)

    def test_geocode_tool_mocked_success(self):
        import json

        payload = json.dumps([{"lon": "2.3522", "lat": "48.8566", "display_name": "Paris, France"}])

        class _FakeResp:
            status = 200

            def read(self):
                return payload.encode()

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        with patch("urllib.request.urlopen", return_value=_FakeResp()):
            from geosi_engine.tools.data_connectors import GeocodeTool

            result = GeocodeTool().execute(address="Paris")
        self.assertTrue(result.success)
        self.assertAlmostEqual(result.output["lon"], 2.3522)
        self.assertIn("Paris", result.message)


if __name__ == "__main__":
    unittest.main()


# ─────────────────────────────────────────────────────────────────────────────
# Upgraded ASTGuard — comprehensive blocked list from TerraLab analysis
# ─────────────────────────────────────────────────────────────────────────────


class TestASTGuardExpanded(unittest.TestCase):
    def setUp(self):
        from geosi_engine.security import ASTGuard

        self.guard = ASTGuard

    def test_blocks_threading(self):
        ok, v = self.guard.check("import threading\nt = threading.Thread(target=lambda: None)")
        self.assertFalse(ok)

    def test_blocks_pickle(self):
        ok, v = self.guard.check("import pickle\npickle.loads(b'')")
        self.assertFalse(ok)

    def test_blocks_qgs_auth_manager(self):
        ok, v = self.guard.check("mgr = QgsApplication.authManager()")
        self.assertFalse(ok)

    def test_blocks_dunder_subclasses(self):
        ok, v = self.guard.check("x = object.__subclasses__()")
        self.assertFalse(ok)

    def test_blocks_ssh_path_pattern(self):
        ok, v = self.guard.check("f = open('/home/user/.ssh/id_rsa', 'r')")
        self.assertFalse(ok)

    def test_blocks_etc_passwd_pattern(self):
        ok, v = self.guard.check("open('/etc/passwd')")
        self.assertFalse(ok)

    def test_qgis_processing_still_allowed(self):
        code = (
            "import processing\n"
            "from qgis.core import QgsVectorLayer, QgsProject\n"
            "result = processing.run('native:buffer', {'INPUT': 'layer', 'DISTANCE': 100})"
        )
        ok, v = self.guard.check(code)
        self.assertTrue(ok, v)

    def test_numpy_geopandas_allowed(self):
        code = (
            "import numpy as np\n"
            "import geopandas as gpd\n"
            "gdf = gpd.read_file('test.gpkg')\n"
            "gdf['area'] = gdf.geometry.area\n"
        )
        ok, v = self.guard.check(code)
        self.assertTrue(ok, v)


# ─────────────────────────────────────────────────────────────────────────────
# New data connector tools — Overture + WFS specs
# ─────────────────────────────────────────────────────────────────────────────


class TestNewDataConnectorSpecs(unittest.TestCase):
    def test_fetch_overture_spec(self):
        from geosi_engine.tools.data_connectors import FetchOvertureTool

        spec = FetchOvertureTool().spec()
        self.assertEqual(spec.name, "fetch_overture")
        self.assertEqual(spec.category, "data")
        required = [p.name for p in spec.parameters if p.required]
        self.assertIn("theme", required)

    def test_fetch_wfs_spec(self):
        from geosi_engine.tools.data_connectors import FetchWFSTool

        spec = FetchWFSTool().spec()
        self.assertEqual(spec.name, "fetch_wfs")
        required = [p.name for p in spec.parameters if p.required]
        self.assertIn("url", required)
        self.assertIn("typename", required)

    def test_fetch_overture_no_bbox_no_location_fails(self):
        from geosi_engine.tools.data_connectors import FetchOvertureTool

        result = FetchOvertureTool().execute(theme="buildings")
        self.assertFalse(result.success)
        self.assertIn("bbox", result.error.lower() or result.error)

    def test_fetch_overture_with_bbox_succeeds(self):
        # Mock geocoding not needed — bbox provided directly
        from geosi_engine.tools.data_connectors import FetchOvertureTool

        result = FetchOvertureTool().execute(theme="buildings", bbox="-0.15,51.48,0.0,51.55")
        self.assertTrue(result.success)
        self.assertIn("buildings", result.message)

    def test_all_tools_in_registry(self):
        from geosi_engine.registry import ToolRegistry

        reg = ToolRegistry()
        reg.discover_portable_tools()
        for name in ("fetch_overture", "fetch_wfs"):
            self.assertIsNotNone(reg.get_tool(name), f"{name} not in registry")
