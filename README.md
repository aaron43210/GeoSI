# GeoSI v2: Autonomous Geospatial Intelligence Platform

GeoSI v2 is a next-generation autonomous AI platform designed to automate complex Geographic Information Systems (GIS) workflows. By combining a 14-Agent Mixture-of-Agents (MoA) pipeline, a hybrid GraphRAG knowledge base, and headless PyQGIS/GDAL execution, GeoSI serves as an autonomous GIS analyst capable of planning, executing, and verifying spatial analysis natively.

## Ultimate Aim
The ultimate goal of GeoSI is to **eliminate the manual bottleneck in geospatial analysis**. By translating natural language intent into deterministic, mathematically verified spatial operations, GeoSI enables disaster response teams, urban planners, and environmental scientists to perform advanced GIS workflows in minutes rather than weeks—without ever needing to open a desktop GUI like ArcGIS or QGIS.

## Key Capabilities
* **100% Local Inference**: Runs entirely offline using local LLMs (Ollama) to ensure data privacy and security for government and enterprise datasets.
* **Agentic Execution**: A 14-specialist agent network handles intent routing, spatial planning, code execution, QA verification, and reporting.
* **Headless GIS Engine**: Executes robust C++ backed spatial math using PyQGIS, GDAL, OGR, and Rasterio.
* **GraphRAG**: Fuses semantic vector search (Qdrant) with structural cross-referencing (Neo4j) to dynamically retrieve GIS manuals and methodologies before generating plans.
* **Aho-Corasick Guardrails**: Enterprise-grade security that blocks prompt injections and destructive operations in $O(T)$ time.

## Quick Start
1. Ensure `docker` and `docker compose` are installed.
2. Spin up the data infrastructure (PostGIS, Qdrant, Neo4j, Redis):
   ```bash
   docker compose up -d
   ```
3. Install the Python dependencies (includes the C++ optimized chunker):
   ```bash
   pip install -e .
   ```
4. Start the FastAPI backend or MCP server to begin interacting with the agents.

## Documentation Navigation
* [Architecture Deep Dive](architecture.md)
* [Codebase Connections & Module Mapping](connections.md)
* [Agent Definitions & Communication](agents.md)

## QGIS Plugin (experimental)
The `geosi_plugin/` folder is a QGIS plugin (QGIS 3.28+ and QGIS 4 / Qt6, Linux, macOS and Windows). The engine packages are bundled into the plugin zip, so users install nothing else.

* **Build:** `python scripts/package_plugin.py` → `dist/geosi_plugin-<version>.zip` (`--check` validates `metadata.txt` only).
* **Install locally:** QGIS → *Plugins → Manage and Install Plugins → Install from ZIP*. Enable *Show also experimental plugins* in Settings.
* **Smoke test:** `QT_QPA_PLATFORM=offscreen python tests/plugin_smoke.py "dist/geosi_plugin-*.zip"` using QGIS's Python.
* **CI/CD:** `.github/workflows/plugin.yml` builds the zip, loads it in QGIS LTR + latest (Docker) and conda-forge QGIS on Ubuntu, macOS and Windows. Pushing a tag `v<version>` matching `metadata.txt` creates a GitHub pre-release with the zip and, if the `QGIS_PLUGIN_USER` / `QGIS_PLUGIN_PASSWORD` secrets (OSGeo ID) are set, uploads it to plugins.qgis.org.
* **LLM provider:** configure Ollama or an API key via environment variables (see `.env.example`); without one, planning falls back to rules.
