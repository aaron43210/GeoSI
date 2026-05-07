# GeoSI - Geospatial Superintelligence

**The autonomous intelligence layer for professional GIS.**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](#)
[![Status](https://img.shields.io/badge/status-production--ready-green.svg)](#)
[![Platform](https://img.shields.io/badge/platform-QGIS%20%7C%20Python%20%7C%20API-orange.svg)](#)
[![LLM](https://img.shields.io/badge/LLM-Ollama%20%7C%20Gemini%20%7C%20Claude-teal.svg)](#)

---

## The Vision

> *"The beginning of geospatial superintelligence - making complex
> spatial analysis as simple as asking a question."*

GeoSI bridges natural language and professional GIS. You ask a
geospatial question; GeoSI plans a multi-step workflow across 125
tools (vector, raster, terrain, network, ML, cartography) and runs it
on the layers you already have open in QGIS. No scripting, no menus,
no SQL.

---

## Three-Surface Architecture

```
               +----------------------+
               |  geosi_engine/       |   universal core
               |  (no QGIS, no Qt)    |   parser  agent  executor
               |  125 tools, backend  |   state   validation
               |  dispatch pattern    |   conversation memory
               +----------+-----------+
                          ^
      installs "qgis"     |              no backend installed
      backend at boot     |              -> BackendTools report
            +-------------+-------------+     "run from QGIS" error
            |                           |
+-----------+-----------+   +-----------+-----------+
|  geosi_plugin/        |   |  geosi_server/ (opt.) |
|  QGIS dock widget     |   |  FastAPI REST         |
|  Layers panel sync    |   |  OSM auto-fetch when  |
|  Processing bridge    |   |  layer is missing     |
+-----------------------+   +-----------------------+
```

- **Engine** is pure Python. Zero QGIS imports. Importable anywhere.
- **Plugin** is the only code that touches QGIS. It reads the Layers
  panel and dispatches tools through QGIS Processing.
- **Server** is optional and independent of the plugin.

---

## Quick Start (Plugin)

### 1. Install Ollama (recommended, keeps everything local)

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral        # or: llama3.1, qwen2.5, phi3, gemma2
ollama serve               # usually auto-starts
```

### 2. Install GeoSI in QGIS

Copy the `geosi_plugin/` folder into your QGIS plugins directory:

- **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/geosi_plugin/`
- **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/geosi_plugin/`
- **Windows:** `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\geosi_plugin\`

Copy the `geosi_engine/` package to the same parent `python/plugins/`
directory (it must be importable by QGIS's Python).

Restart QGIS. Enable **GeoSI - AI Agent** in Plugins -> Manage and
Install Plugins.

### 3. Use it

- Load any vector or raster layer into the QGIS Layers panel.
- Click the GeoSI toolbar button. The dock opens on the right.
- Click the **LLM** button, confirm `http://localhost:11434` and the
  model name (default `mistral`), hit **Test Ollama**, then
  **Save and Reload**.
- Type a question in plain English and press Enter.

```
You: Buffer Schools by 500 meters
You: Intersect that with Kerala
You: Export result as GeoJSON
```

Try `help`, `layers`, or `tools` at any time.

---

## Supported LLMs (priority order)

| Priority | Provider | Setup |
|---|---|---|
| 1 | **Ollama** (local) | `ollama pull mistral` |
| 2 | Google Gemini | `export GEMINI_API_KEY=...` |
| 3 | Anthropic Claude | Paste key into the dock's LLM panel |
| 4 | OpenAI | `export OPENAI_API_KEY=...` |
| 5 | Rule-based keyword parser | Always on, no setup |

Each provider has a 1.5-second availability probe, so missing ones
fall through instantly. GeoSI always produces an answer, even offline.

---

## Capability Highlights

- **125 tools**, auto-discovered across 9 domains
  (vector, raster, network, terrain, temporal, AI/ML, cartography,
  validation, portable I/O).
- **Multi-step planning** - GeoSI decomposes compound queries
  ("find flood-risk hospitals within 2km of rivers") into chained
  tool calls.
- **Layer validation** - references a missing layer? GeoSI replies
  "Layer 'X' not found" and lists what is loaded, with fuzzy
  suggestions.
- **Conversation memory** - follow-ups reuse prior context.
- **Explainable** - every result shows the plan and the reasoning.

---

## Repository Layout

| Path | Purpose |
|---|---|
| `geosi_engine/` | Universal core (no QGIS). Tools, parser, agent, executor. |
| `geosi_plugin/` | QGIS desktop plugin. Dock, QGIS Processing bridge. |
| `geosi_server/` | Optional FastAPI REST surface. |
| `Data_06_2_2026/` | Example Kerala shapefiles for testing. |
| `prompts.md` | Suggested prompts for vector and raster workflows. |
| `Connections.md` | Full architecture and flow documentation. |

---

## Example Prompts

See [`prompts.md`](prompts.md) for a complete catalog. A taste:

- *"Buffer Schools by 1 km and intersect with TVM_Corp"*
- *"Count features in Assets"*
- *"Calculate slope and hillshade from DEM"*
- *"Cluster Schools using DBSCAN with eps=500"*
- *"Export the intersection as GeoJSON"*
- *"Check Assets for invalid geometries and fix them"*

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Layer 'X' not found" | Load the layer into the QGIS Layers panel first, then retry. |
| "Ollama not reachable" | `ollama serve` in a terminal, or click LLM -> Test Ollama. |
| "No tools loaded" | Engine init failed - check the QGIS Python console for a traceback. |
| Slow first query | Ollama warms up the model on the first call. Subsequent queries are fast. |
| Wrong tool picked | Try a more specific phrasing, or use `tools` to see categories. |

---

## Roadmap

- [x] **v1.0** - Core engine, 80 tools, basic plugin.
- [x] **v2.0** - Ollama-first, 125 tools, universal engine, validation,
      conversation memory, three clean surfaces.
- [ ] **v2.5** - GeoPandas backend for the server, batch mode.
- [ ] **v3.0** - Real-time satellite stream monitoring, 3D viewshed.
- [ ] **v4.0** - Predictive spatial modelling, autonomous decision
      support.

---

## Author

**AARON R** - Digital University Kerala (DUK)
[aaronr.ds25@duk.ac.in](mailto:aaronr.ds25@duk.ac.in)

GeoSI is an open-vision project: the beginning of geospatial
superintelligence built for the domain.

*© 2026 GeoSI Project.*
