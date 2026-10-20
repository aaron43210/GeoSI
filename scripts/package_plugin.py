#!/usr/bin/env python3
"""
Build the GeoSI QGIS plugin zip (cross-platform: Linux, macOS, Windows).

The zip contains a single top-level ``geosi_plugin/`` folder, as the QGIS
plugin repository requires, with the engine packages bundled inside it:

    geosi_plugin/
        __init__.py, geosi_plugin.py, prompt_dock.py, qgis_bridge.py
        metadata.txt, icon.png, LICENSE
        geosi_engine/  geosi_knowledge/  geosi_data/  geosi_rag/

Usage:
    python scripts/package_plugin.py            # -> dist/geosi_plugin-<version>.zip
    python scripts/package_plugin.py --check    # validate metadata only
"""

from __future__ import annotations

import argparse
import configparser
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = ROOT / "geosi_plugin"
PLUGIN_NAME = "geosi_plugin"

# Pure-Python packages the plugin imports at runtime.
BUNDLED_PACKAGES = ["geosi_engine", "geosi_knowledge", "geosi_data", "geosi_rag"]

REQUIRED_METADATA = [
    "name",
    "qgisMinimumVersion",
    "description",
    "about",
    "version",
    "author",
    "email",
    "repository",
    "tracker",
    "icon",
]
EXCLUDED_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".so", ".pyd", ".dylib", ".dll", ".cpp", ".o"}


def read_metadata() -> configparser.SectionProxy:
    parser = configparser.ConfigParser(interpolation=None)
    parser.optionxform = str  # keep key case (qgisMinimumVersion)
    parser.read(PLUGIN_DIR / "metadata.txt", encoding="utf-8")
    return parser["general"]


def validate(meta: configparser.SectionProxy) -> list[str]:
    errors = [f"metadata.txt: missing '{k}'" for k in REQUIRED_METADATA if not meta.get(k, "").strip()]
    if not re.fullmatch(r"\d+\.\d+(\.\d+)?([-.]?[A-Za-z0-9.]+)?", meta.get("version", "")):
        errors.append(f"metadata.txt: invalid version {meta.get('version')!r}")
    # QGIS treats a plugin without these as QGIS 3 only and refuses it in QGIS 4
    try:
        if float(meta.get("qgisMaximumVersion", "3.99")) < 4:
            errors.append("metadata.txt: qgisMaximumVersion must be >= 4.0 (e.g. 4.99) for QGIS 4")
    except ValueError:
        errors.append(f"metadata.txt: invalid qgisMaximumVersion {meta.get('qgisMaximumVersion')!r}")
    if meta.get("supportsQt6", "").lower() != "true":
        errors.append("metadata.txt: supportsQt6=True is required for QGIS 4 (Qt6)")
    if meta.get("experimental", "").lower() != "true":
        errors.append("metadata.txt: experimental must be True for this release")
    for name in (meta.get("icon", ""), "__init__.py", "LICENSE"):
        if name and not (PLUGIN_DIR / name).exists() and not (ROOT / name).exists():
            errors.append(f"missing plugin file: {name}")
    for pkg in BUNDLED_PACKAGES:
        if not (ROOT / pkg / "__init__.py").exists():
            errors.append(f"missing bundled package: {pkg}")
    return errors


def iter_files(base: Path):
    for path in sorted(base.rglob("*")):
        if path.is_dir() or EXCLUDED_DIRS.intersection(path.relative_to(ROOT).parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES or path.name.startswith("."):
            continue
        yield path


def build(meta: configparser.SectionProxy, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"{PLUGIN_NAME}-{meta['version']}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in iter_files(PLUGIN_DIR):
            # as_posix() keeps forward slashes in the archive on Windows too
            zf.write(path, f"{PLUGIN_NAME}/{path.relative_to(PLUGIN_DIR).as_posix()}")
        if not (PLUGIN_DIR / "LICENSE").exists():
            zf.write(ROOT / "LICENSE", f"{PLUGIN_NAME}/LICENSE")
        for pkg in BUNDLED_PACKAGES:
            for path in iter_files(ROOT / pkg):
                zf.write(path, f"{PLUGIN_NAME}/{path.relative_to(ROOT).as_posix()}")
    return zip_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="validate metadata and exit")
    ap.add_argument("--out", type=Path, default=ROOT / "dist", help="output directory")
    args = ap.parse_args()

    meta = read_metadata()
    errors = validate(meta)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"metadata OK: {meta['name']} {meta['version']} (experimental={meta['experimental']})")
    if args.check:
        return 0

    zip_path = build(meta, args.out)
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
    print(f"built {zip_path} ({len(names)} files, {zip_path.stat().st_size // 1024} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
