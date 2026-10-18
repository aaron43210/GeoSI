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

### How the agent works
Each request goes through a loop: **plan → run → check → re-plan** (`geosi_engine/agent_loop.py`).
* **Planning:** fixed rules for simple operations (buffer, clip, dissolve…), deterministic planners for attribute filters, field and raster statistics, grids and merges, verified example templates (`plan_examples.py`), and otherwise the local LLM (Ollama `llama3`). The LLM is shown the 12 most relevant tools, found by semantic search with `nomic-embed-text`.
* **Checking:** failed steps, empty outputs, the wrong kind of output ("find hospitals…" must return points) and per-feature requests ("in each zone") are detected. The problem is sent back to the LLM, for up to 3 attempts (configurable). If every attempt fails, GeoSI says so instead of returning a wrong layer.
* **Multi-step requests** ("buffer roads by 200 m and dissolve the result") are split into sub-tasks, each checked separately.
* **Questions** ("which zone has the most hospitals?") are answered from the result data; counts come straight from the layer.
* **Safety:** requests to delete or overwrite data are refused, and missing layers are reported.
* **UI:** requests run as a background QGIS task with a Stop button. ⚙ sets the Ollama URL, models and retries.

### Agent benchmark
`tests/agent_bench/` builds synthetic data with known answers and runs tasks through the real plugin in headless QGIS:
```bash
QT_QPA_PLATFORM=offscreen <qgis-python> -m tests.agent_bench.run_bench [--holdout | --blind] [--verbose]
```
Results on macOS, QGIS 4.2, llama3 8B + nomic-embed-text:

| Set | Purpose | Score |
|---|---|---|
| main (36 tasks) | tuning set | 36/36 |
| holdout (20) | written after tuning, then used for fixes | 20/20 |
| blind (15) | never tuned on; new request types | 7/15 |
| main, no LLM | CI regression gate (≥ 85%) | 32/36 |

The **blind** score is the realistic estimate for unfamiliar requests. Raster algorithms such as heatmaps can take minutes.
