"""
GeoSI dock integration test — runs the real plugin UI inside headless QGIS.

    QT_QPA_PLATFORM=offscreen python -m tests.qgis_integration \
        [--plugin dist/geosi_plugin-*.zip] [--shots DIR] [--llm]

Covers the model-connection gate (not connected → request waits → continue
offline / connect → request runs), built-in commands, chips, links, undo,
layer sync, file drops and escaping. ``--llm`` also checks a live Ollama
answer (needs Ollama running with a chat model). ``--shots`` saves dock
screenshots. Exit code 1 if any check fails.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import zipfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
UNREACHABLE = "http://127.0.0.1:9"
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  → {detail}"), flush=True)


def chat_text(dock):
    return dock.chat_display.toPlainText()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plugin", default="dist/geosi_plugin-*.zip")
    ap.add_argument("--shots", default="")
    ap.add_argument("--llm", action="store_true")
    args = ap.parse_args()

    from qgis.core import QgsApplication, QgsProject, QgsVectorLayer
    from qgis.PyQt.QtCore import QUrl

    app = QgsApplication([], True)
    app.initQgis()
    for p in (
        os.path.join(QgsApplication.pkgDataPath(), "python", "plugins"),
        os.path.join(QgsApplication.prefixPath(), "python", "plugins"),
        "/usr/share/qgis/python/plugins",
    ):
        if os.path.isdir(p):
            sys.path.append(p)
    from processing.core.Processing import Processing

    Processing.initialize()
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from tests.agent_bench import data
    from tests.agent_bench.run_bench import FakeIface, _import_plugin, _load_base_layers

    class Iface(FakeIface):
        def __init__(self):
            super().__init__()
            from qgis.gui import QgsMapCanvas

            self.canvas = QgsMapCanvas()
            self.active = None

        def mapCanvas(self):
            return self.canvas

        def activeLayer(self):
            return self.active

    plugin_mod = _import_plugin(args.plugin)
    paths = data.build(tempfile.mkdtemp(prefix="geosi_it_data_"))
    shots = args.shots
    if shots:
        os.makedirs(shots, exist_ok=True)

    def snap(dock, name):
        if not shots:
            return
        dock.dock.setFloating(True)
        dock.dock.resize(420, 780)
        dock.dock.show()
        for _ in range(5):
            app.processEvents()
        dock.dock.grab().save(os.path.join(shots, f"{name}.png"))

    def open_dock(endpoint=UNREACHABLE, model="llama3"):
        os.environ["OLLAMA_ENDPOINT"] = endpoint
        os.environ["OLLAMA_MODEL"] = model
        _load_base_layers(paths)
        iface = Iface()
        plugin = plugin_mod.classFactory(iface)
        plugin.initGui()
        assert plugin._init_engine()
        from geosi_plugin.prompt_dock import GeoSIDock

        agent = plugin.engine.agent
        agent._ollama_endpoint, agent._ollama_model, agent._api_base = endpoint, model, ""
        # Synchronous so each step can be asserted
        dock = GeoSIDock(iface, plugin.engine, supervisor=plugin.supervisor, run_in_background=False)
        return plugin, dock, iface

    def send(dock, text):
        dock.input_box.setText(text)
        dock._on_submit()

    def layer_names():
        return sorted(lyr.name() for lyr in QgsProject.instance().mapLayers().values())

    # ── 1. No model: notice + in-chat card, request waits ─────────────
    plugin, dock, iface = open_dock()
    s = dock.llm_status
    check("not connected is detected", s is not None and not s.ok and s.problem == "ollama_unreachable", s)
    check("status chip says not connected", "Not connected" in dock.status_chip.text(), dock.status_chip.text())
    check("notice bar shown", not dock.notice.isHidden() and "No model connected" in dock.notice_title.text())
    check("chat card explains the fix", "ollama serve" in chat_text(dock))
    check("connection card is in the chat first", "Ollama isn't reachable" in chat_text(dock))
    snap(dock, "1_not_connected")

    before = layer_names()
    send(dock, "buffer hospitals by 500 m")
    check("request is held, not run", dock._pending_query == "buffer hospitals by 500 m" and layer_names() == before)
    check("user is told it will run after connecting", "as soon as a model is connected" in chat_text(dock))

    # ── 2. Continue offline runs the held request ──────────────────────
    dock._on_continue_offline()
    after = layer_names()
    check("held request ran offline", len(after) == len(before) + 1, f"{before} → {after}")
    check(
        "chip shows Offline, notice switches to info",
        "Offline" in dock.status_chip.text() and dock.notice.property("level") == "info",
    )
    snap(dock, "2_offline_ran")

    # ── 3. Undo removes the result layer ───────────────────────────────
    dock._on_undo()
    check("undo restores the project", layer_names() == before, layer_names())
    check("undo reports success", "Undone" in chat_text(dock), chat_text(dock)[-200:])

    # ── 4. Built-in commands, links, chips, escaping ───────────────────
    for cmd, expect in (
        ("help", "Things you can ask"),
        ("tools", "by category"),
        ("layers", "hospitals"),
        ("search buffer", "match 'buffer'"),
    ):
        seen = len(chat_text(dock))
        send(dock, cmd)
        check(f"command '{cmd}' answers", expect in chat_text(dock)[seen:], chat_text(dock)[seen:][:120])
    dock._on_anchor(QUrl("geosi:prompt?q=Buffer%20roads%20by%2050%20m"))
    check("suggestion link fills the prompt", dock.input_box.text() == "Buffer roads by 50 m", dock.input_box.text())
    dock.input_box.setText("buffer @hos")
    dock._on_input_changed()
    check(
        "@ completer offers the layer",
        "@hospitals" in dock._completer_model.stringList(),
        dock._completer_model.stringList(),
    )
    dock.input_box.setText("count features")
    iface.active = QgsProject.instance().mapLayersByName("hospitals")[0]
    dock._on_append_selected()
    check("Selection chip names the active layer", "@hospitals" in dock.input_box.text(), dock.input_box.text())
    dock._on_append_extent()
    check("Map view chip adds the extent", "map extent" in dock.input_box.text(), dock.input_box.text())
    dock._append_error("<b>not bold</b>")
    check("errors are shown as text, not HTML", "<b>not bold</b>" in chat_text(dock))

    # ── 5. Layer sync follows removals and renames ─────────────────────
    dock._sync_layers()
    project = QgsProject.instance()
    roads = project.mapLayersByName("roads")[0]
    roads.setName("streets")
    project.removeMapLayer(project.mapLayersByName("parcels")[0].id())
    dock._sync_layers()
    names = dock.engine.state.list_layers()
    check("sync drops removed and renamed layers", "parcels" not in names and "roads" not in names, names)
    check("sync adds the renamed layer", "streets" in names, names)

    # ── 6. Dropping a zipped shapefile ─────────────────────────────────
    tmp = tempfile.mkdtemp(prefix="geosi_it_zip_")
    shp = os.path.join(tmp, "zones.shp")
    from qgis.core import QgsCoordinateTransformContext, QgsVectorFileWriter

    src = QgsVectorLayer(paths["flood_zones"], "fz", "ogr")
    opts = QgsVectorFileWriter.SaveVectorOptions()
    opts.driverName = "ESRI Shapefile"
    QgsVectorFileWriter.writeAsVectorFormatV3(src, shp, QgsCoordinateTransformContext(), opts)
    zpath = os.path.join(tmp, "zones.zip")
    with zipfile.ZipFile(zpath, "w") as z:
        for f in os.listdir(tmp):
            if f.startswith("zones.") and not f.endswith(".zip"):
                z.write(os.path.join(tmp, f), f)
    dock._load_dropped_file(zpath)
    check("zipped shapefile drop loads", project.mapLayersByName("zones"), layer_names())
    shutil.rmtree(tmp, ignore_errors=True)
    plugin.unload()

    # ── 7. Connecting later runs the held request automatically ────────
    plugin, dock, iface = open_dock()
    before = layer_names()
    send(dock, "create centroids of flood_zones")
    if args.llm:
        dock.engine.agent._ollama_endpoint = "http://localhost:11434"
        dock._check_connection(announce=True)
        s = dock.llm_status
        check("connects to running Ollama", s.ok and s.provider == "ollama", s)
        check("missing model falls back to an installed one", s.ok and s.model != "llama3" or s.model, s)
        check("chip shows the model", s.model in dock.status_chip.text(), dock.status_chip.text())
        check("notice hidden once connected", dock.notice.isHidden())
        check("held request ran after connecting", len(layer_names()) == len(before) + 1, layer_names())
        snap(dock, "3_connected")

        send(dock, "What is NDVI?")
        text = chat_text(dock)
        check("live model answers a question", "NDVI" in text.split("What is NDVI?")[-1] and len(text) > 200)
        snap(dock, "4_llm_answer")
    plugin.unload()

    # ── 8. Dark theme ──────────────────────────────────────────────────
    from qgis.PyQt.QtGui import QColor, QPalette

    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
    pal.setColor(QPalette.ColorRole.WindowText, QColor("#eeeeee"))
    app.setPalette(pal)
    plugin, dock, iface = open_dock()
    from geosi_plugin.ui_theme import DARK

    check("dark QGIS theme gives the dark palette", dock.t is DARK)
    snap(dock, "5_dark_not_connected")
    plugin.unload()

    failed = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed", flush=True)
    # Skip QGIS teardown: exitQgis() can segfault on macOS after headless runs,
    # which would mask the real result
    sys.stdout.flush()
    os._exit(1 if failed else 0)


if __name__ == "__main__":
    sys.exit(main())
