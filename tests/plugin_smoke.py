"""
Headless smoke test for the packaged GeoSI QGIS plugin.

Runs inside a real QGIS Python environment (QGIS Docker image, conda-forge
qgis, or a desktop install). It unzips the built plugin into a temp folder,
loads it the way QGIS does (classFactory → initGui → open dock → unload)
against a minimal fake iface, and checks that Processing tools were found.

Usage:
    QT_QPA_PLATFORM=offscreen python tests/plugin_smoke.py dist/geosi_plugin-*.zip
"""

from __future__ import annotations

import glob
import os
import sys
import tempfile
import zipfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _processing_paths() -> list[str]:
    from qgis.core import QgsApplication

    return [
        os.path.join(QgsApplication.pkgDataPath(), "python", "plugins"),
        os.path.join(QgsApplication.prefixPath(), "share", "qgis", "python", "plugins"),
        os.path.join(QgsApplication.prefixPath(), "python", "plugins"),
        "/usr/share/qgis/python/plugins",
    ]


def main(zip_pattern: str) -> int:
    matches = glob.glob(zip_pattern)
    if not matches:
        print(f"no plugin zip matches {zip_pattern}", file=sys.stderr)
        return 1

    from qgis.core import QgsApplication
    from qgis.PyQt.QtWidgets import QMainWindow

    app = QgsApplication([], True)
    app.initQgis()
    sys.path.extend(p for p in _processing_paths() if os.path.isdir(p))
    from processing.core.Processing import Processing

    Processing.initialize()

    class FakeMessageBar:
        def pushMessage(self, *args, **kwargs):
            print("messageBar:", args)

    class FakeIface:
        def __init__(self):
            self.window = QMainWindow()
            self.docks = []

        def mainWindow(self):
            return self.window

        def messageBar(self):
            return FakeMessageBar()

        def addToolBarIcon(self, action):
            pass

        def removeToolBarIcon(self, action):
            pass

        def addPluginToMenu(self, menu, action):
            pass

        def removePluginMenu(self, menu, action):
            pass

        def addDockWidget(self, area, dock):
            self.window.addDockWidget(area, dock)
            self.docks.append(dock)

        def removeDockWidget(self, dock):
            self.window.removeDockWidget(dock)
            self.docks.remove(dock)

    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(matches[0]) as zf:
            zf.extractall(tmp)
        sys.path.insert(0, tmp)

        import geosi_plugin

        iface = FakeIface()
        plugin = geosi_plugin.classFactory(iface)
        plugin.initGui()
        plugin.action.setChecked(True)  # opens the dock and starts the engine

        assert plugin.engine is not None, "engine failed to start"
        assert plugin.tool_count > 0, "no QGIS Processing tools discovered"
        assert len(iface.docks) == 1, "dock was not added"
        bundled = os.path.dirname(sys.modules["geosi_engine"].__file__)
        assert bundled.startswith(tmp), f"engine not loaded from plugin zip: {bundled}"

        print(f"OK: {plugin.tool_count} QGIS tools, engine from {bundled}")
        plugin.unload()
        assert not iface.docks, "dock not removed on unload"

    app.exitQgis()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "dist/geosi_plugin-*.zip"))
