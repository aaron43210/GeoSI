"""
GeoSI agent benchmark — runs every task through the real plugin in headless QGIS.

    QT_QPA_PLATFORM=offscreen python -m tests.agent_bench.run_bench \
        [--plugin dist/geosi_plugin-*.zip | --plugin geosi_plugin] \
        [--only v01,q02] [--category raster] [--json results.json]

Needs a QGIS Python environment. LLM planning uses Ollama (OLLAMA_MODEL,
default auto-detect); without it the rule-based planner is scored alone.
Exit code is 0 unless --min-score is given and the overall score is below it.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import tempfile
import time
import zipfile
from collections import defaultdict

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


class Ctx:
    def __init__(self, layers, answer):
        self.layers = layers
        self.answer = (answer or "").lower()

    def vector(self, geom=None):
        from qgis.core import QgsVectorLayer, QgsWkbTypes

        want = {"point": QgsWkbTypes.GeometryType.PointGeometry,
                "line": QgsWkbTypes.GeometryType.LineGeometry,
                "polygon": QgsWkbTypes.GeometryType.PolygonGeometry}.get(geom)
        for lyr in reversed(self.layers):  # last produced layer is the answer
            if isinstance(lyr, QgsVectorLayer) and (want is None or lyr.geometryType() == want):
                return lyr
        return None

    def raster(self):
        from qgis.core import QgsRasterLayer

        return next((l for l in reversed(self.layers) if isinstance(l, QgsRasterLayer)), None)


class FakeIface:
    def __init__(self):
        from qgis.PyQt.QtWidgets import QMainWindow

        self.window = QMainWindow()

    def mainWindow(self):
        return self.window

    def messageBar(self):
        class Bar:
            def pushMessage(self, *a, **k):
                pass
        return Bar()

    def addToolBarIcon(self, a): pass
    def removeToolBarIcon(self, a): pass
    def addPluginToMenu(self, m, a): pass
    def removePluginMenu(self, m, a): pass
    def addDockWidget(self, area, d): self.window.addDockWidget(area, d)
    def removeDockWidget(self, d): self.window.removeDockWidget(d)


def _import_plugin(spec: str):
    """Import geosi_plugin from a built zip (glob ok) or a source directory."""
    if spec.endswith(".zip") or "*" in spec:
        matches = sorted(glob.glob(spec))
        if not matches:
            sys.exit(f"no plugin zip matches {spec}")
        target = tempfile.mkdtemp(prefix="geosi_bench_plugin_")
        zipfile.ZipFile(matches[-1]).extractall(target)
        sys.path.insert(0, target)
    else:
        sys.path.insert(0, os.path.dirname(os.path.abspath(spec)))
    import geosi_plugin
    return geosi_plugin


def _load_base_layers(paths):
    from qgis.core import QgsProject, QgsRasterLayer, QgsVectorLayer

    project = QgsProject.instance()
    project.clear()
    for name, path in paths.items():
        lyr = QgsRasterLayer(path, name) if path.endswith(".tif") else QgsVectorLayer(path, name, "ogr")
        assert lyr.isValid(), f"invalid base layer {path}"
        project.addMapLayer(lyr)
    return set(project.mapLayers())


def run_task(plugin_mod, paths, query):
    from qgis.core import QgsProject

    base = _load_base_layers(paths)
    plugin = plugin_mod.classFactory(FakeIface())
    plugin.initGui()
    plugin.action.setChecked(True)
    if plugin.engine is None:
        return None, "", "engine failed to start", 0.0

    captured = {}
    real_run = plugin.engine.run

    def run_and_capture(q):
        captured["result"] = real_run(q)
        return captured["result"]

    plugin.engine.run = run_and_capture
    start = time.time()
    plugin.dock.run_in_background = False  # score the result synchronously
    plugin.dock.input_box.setText(query)
    plugin.dock._on_submit()
    elapsed = time.time() - start

    project = QgsProject.instance()
    new_layers = [project.mapLayer(i) for i in project.mapLayers() if i not in base]
    result = captured.get("result")
    answer = ""
    if result is not None:
        answer = " ".join(filter(None, [result.answer, result.error or ""]))
    plugin.unload()
    return new_layers, answer, None, elapsed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plugin", default="dist/geosi_plugin-*.zip")
    ap.add_argument("--only", default="")
    ap.add_argument("--category", default="")
    ap.add_argument("--json", default="")
    ap.add_argument("--min-score", type=float, default=None)
    ap.add_argument("--holdout", action="store_true", help="run the held-out tasks instead")
    ap.add_argument("--blind", action="store_true", help="run the blind reserve tasks instead")
    ap.add_argument("--verbose", action="store_true", help="print engine logs (plans, retries)")
    args = ap.parse_args()
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.INFO, format="      [%(name)s] %(message)s")
        for noisy in ("urllib3", "httpx", "geosi_engine.registry", "geosi_engine.tools.domain_tools"):
            logging.getLogger(noisy).setLevel(logging.WARNING)

    from qgis.core import QgsApplication

    app = QgsApplication([], True)
    app.initQgis()
    for p in (os.path.join(QgsApplication.pkgDataPath(), "python", "plugins"),
              os.path.join(QgsApplication.prefixPath(), "python", "plugins"),
              "/usr/share/qgis/python/plugins"):
        if os.path.isdir(p):
            sys.path.append(p)
    from processing.core.Processing import Processing
    Processing.initialize()

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from tests.agent_bench import data
    from tests.agent_bench.tasks import BLIND_TASKS, HOLDOUT_TASKS, TASKS

    plugin_mod = _import_plugin(args.plugin)
    paths = data.build(tempfile.mkdtemp(prefix="geosi_bench_data_"))

    only = {t for t in args.only.split(",") if t}
    pool = BLIND_TASKS if args.blind else HOLDOUT_TASKS if args.holdout else TASKS
    tasks = [t for t in pool if (not only or t[0] in only) and (not args.category or t[1] == args.category)]

    rows = []
    for task_id, category, query, check in tasks:
        layers, answer, fatal, elapsed = run_task(plugin_mod, paths, query)
        if fatal:
            reason = fatal
        else:
            try:
                reason = check(Ctx(layers, answer))
            except Exception as e:  # checker crash counts as a failure
                reason = f"checker error: {e}"
        ok = reason is None
        rows.append({"id": task_id, "category": category, "query": query, "pass": ok,
                     "reason": reason, "seconds": round(elapsed, 1), "answer": answer[:300]})
        print(f"{'PASS' if ok else 'FAIL'} {task_id:4} {elapsed:5.1f}s  {query}" + ("" if ok else f"\n      → {reason}"),
              flush=True)

    by_cat = defaultdict(lambda: [0, 0])
    for r in rows:
        by_cat[r["category"]][0] += r["pass"]
        by_cat[r["category"]][1] += 1
    total = sum(r["pass"] for r in rows)
    score = 100.0 * total / max(1, len(rows))
    print("\n── score by category ──")
    for cat, (p, n) in sorted(by_cat.items()):
        print(f"  {cat:9} {p:2}/{n:<2}  {100.0 * p / n:5.1f}%")
    print(f"  {'overall':9} {total:2}/{len(rows):<2}  {score:5.1f}%")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"score": score, "by_category": by_cat, "tasks": rows}, fh, indent=2)
    app.exitQgis()
    return 1 if args.min_score is not None and score < args.min_score else 0


if __name__ == "__main__":
    sys.exit(main())
