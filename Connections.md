# GeoSI - Complete Architecture and Component Connections

**Last Updated:** 7 May 2026
**Purpose:** Single-file map of how every piece of GeoSI connects.

---

## Project Overview

GeoSI (Geospatial Superintelligence) is a conversational geospatial AI
system. Users type plain-English questions; GeoSI plans and runs
multi-step GIS workflows across 125 tools. It is built around three
clean surfaces:

1. **`geosi_engine/`** - the universal, framework-free core. No QGIS,
   no PyQt, no GDAL imports. Runs inside the plugin, a FastAPI server,
   Jupyter, or a test harness without modification.
2. **`geosi_plugin/`** - the QGIS desktop surface. The only code that
   imports `qgis` lives here. It syncs the QGIS Layers panel into the
   engine, installs a `"qgis"` backend for the BackendTool dispatch,
   and renders the chat dock.
3. **`geosi_server/`** - the optional REST surface (FastAPI). Prefers
   user-loaded layers and falls back to an OSM auto-fetch when a
   recognisable feature name is referenced but not loaded.

**Primary LLM:** Ollama (local, no API key required).
**Fallbacks:** Gemini, Anthropic Claude, keyword-based rules.

---

## Directory Structure

```
project/
├── geosi_engine/              (universal core - no QGIS)
│   ├── __init__.py            GeoSI facade class
│   ├── models.py              Data contracts (Layer, ToolSpec, ExecutionPlan)
│   ├── base.py                GISTool / PortableTool / BackendTool + backend registry
│   ├── registry.py            Auto-discovers tools in tools/*
│   ├── state.py               Workspace (layers, history, checkpoints)
│   ├── parser.py              NL -> AnalysisRequest (Ollama-first)
│   ├── agent.py               AnalysisRequest -> ExecutionPlan
│   ├── executor.py            ExecutionPlan -> ExecutionResult
│   ├── validation.py          Geometry / CRS / topology checks
│   ├── conversation.py        Multi-turn conversation memory
│   └── tools/
│       ├── vector.py          40 vector tools
│       ├── raster.py          25 raster tools
│       ├── network.py         8 routing tools
│       ├── terrain.py         10 terrain/DEM tools
│       ├── temporal.py        6 time-series tools
│       ├── ai_ml.py           10 ML/stats tools
│       ├── cartography.py     10 export/geocode tools
│       ├── validation.py      10 QA tools
│       └── portable.py        2 cross-platform I/O tools
├── geosi_plugin/              (QGIS surface - only code that imports qgis)
│   ├── __init__.py            classFactory()
│   ├── geosi_plugin.py        Installs QGIS backend, builds toolbar/action
│   ├── qgis_bridge.py         Registers "qgis" backend with engine
│   ├── prompt_dock.py         Interactive chat dock (Ollama config, chat log)
│   └── metadata.txt           Plugin metadata
└── geosi_server/              (optional FastAPI - independent of QGIS)
    └── app/services/osm_fetcher.py    OSM Overpass auto-fetch fallback
```

---

## The Three Surfaces

| Surface | Owns | Uses QGIS | Uses OSM auto-fetch |
|---|---|---|---|
| **Engine** | Tools, parser, agent, executor, state | No | No |
| **Plugin** | QGIS Layers panel sync, chat dock, QGIS Processing bridge | Yes | No |
| **Server** | REST endpoints, workspace persistence | No | Yes (only when layer missing) |

---

## Backend Dispatch Pattern

`BackendTool` (alias: `QGISProcessingTool`) is the universal
spec-carrying class used by almost every built-in tool. It never
imports QGIS. Execution is delegated to a backend installed at
runtime via `geosi_engine.base.register_backend(name, fn)`.

- Plugin startup (`qgis_bridge.install()`) calls
  `register_backend("qgis", _run_qgis_algorithm)`.
- Server startup registers no backend, so BackendTools return a clear
  error telling the user to run from QGIS or use a portable tool.

This keeps the engine exportable as a pure Python library.

---

## Data Flow: User Prompt -> Result

```
1. User types in prompt_dock.py QLineEdit
2. GeoSIDock._run_query() handles meta-commands (help / layers / tools / clear)
3. GeoSIDock._sync_qgis_layers() copies QgsProject.mapLayers() into state
4. _QueryWorker thread calls GeoSI.query(text)

Inside the engine:
5. agent.parse(text, state)         -> QueryParser -> AnalysisRequest
6. agent.validate_layers_exist(req) -> "Layer not found" if missing
7. agent.plan(req)                  -> ExecutionPlan (Ollama-first)
8. executor.run(plan)               -> walks each ToolStep
       - registry.execute_tool(name, **params)
       - BackendTool -> qgis backend -> processing.run()

9. ExecutionResult returns to GeoSIDock._on_result()
10. Chat dock renders answer + reasoning + suggestions
```

---

## LLM Priority Chain

| Priority | Provider | Trigger |
|---|---|---|
| 1 | **Ollama** (local) | Always tried first. 1.5s availability probe, 30s generate timeout. |
| 2 | Google Gemini | If `GEMINI_API_KEY` env var set |
| 3 | Anthropic Claude | If `ANTHROPIC_API_KEY` env var set (QgsSettings: `GeoSI/anthropic_api_key`) |
| 4 | OpenAI | If `OPENAI_API_KEY` env var set |
| 5 | Keyword rules | Always works offline; handles every built-in intent |

Each provider failure logs a warning and falls through. The keyword
fallback is comprehensive enough to drive all 125 tools.

---

## Layer Not Found Flow

A user references `hospitals` but only `Assets` and `Kerala` are in
the QGIS Layers panel. The engine responds:

```
parser.parse("Buffer hospitals by 500m", ["Assets", "Kerala"])
  -> request.entities["primary_layer"] = "hospitals"

agent.validate_layers_exist(request, state)
  -> primary "hospitals" not in available layers
  -> find_similar_layers("hospitals", ["Assets","Kerala"]) == []
  -> returns (False, "Layer 'hospitals' not found.\n\n
                     Available layers:\n  - Assets\n  - Kerala")

agent.plan(...)   -> empty ExecutionPlan with that message as reasoning
executor.run(...) -> ExecutionResult(success=False, answer=that message)
prompt_dock       -> renders the error in red and lists loaded layers
```

The plugin **never** fetches data from OSM. The user is always told
to load the layer first.

---

## Intent Types and Tool Categories

| Intent | Example prompts | Candidate tools |
|---|---|---|
| PROXIMITY | "within 500m of ...", "nearest park" | buffer, intersect, nearest_join |
| OVERLAY | "intersect A with B", "clip A to B" | intersect, union_layer, difference, clip, symmetric_difference |
| GEOMETRY | "centroids of parks", "simplify" | centroid, dissolve, convex_hull, voronoi, simplify |
| RASTER | "ndvi", "zonal stats", "reclassify" | raster_calc, zonal_stats, reclassify, raster_mask |
| TERRAIN | "slope", "hillshade", "viewshed" | slope, aspect, hillshade, contour, viewshed, watershed |
| NETWORK | "shortest path", "service area" | shortest_path, service_area, od_matrix |
| TEMPORAL | "change 2015 to 2022", "time series" | temporal_filter, change_detection |
| AI_ML | "cluster crime points", "hotspots" | kmeans_cluster, dbscan, getis_ord_gi, moran_i, idw |
| VALIDATION | "check geometry", "topology" | fix_geometries, check_validity, topology_check |
| STATISTICS | "count", "mean of ..." | zonal_stats, count_features |
| DATA_MGMT | "reproject to 4326", "load shp" | reproject, load_spatial_data, save_layer |
| CARTOGRAPHY | "export GeoJSON", "geocode" | export_geojson, export_shapefile, geocode |

Total: **125 tools** auto-discovered by `ToolRegistry.discover_tools()`.

---

## Interactive Chat Commands

Meta-commands handled by the dock (never sent to the engine):

| Command | What it shows |
|---|---|
| `help` | Example prompts adapted to the layers currently loaded |
| `layers` | Every loaded layer with type, geometry, feature count, CRS |
| `tools` | Tool-count-per-category summary |
| `clear` / `cls` | Clear the chat log and greet again |

The LLM button reveals the Ollama endpoint / model and the optional
cloud keys. "Test Ollama" pings `/api/tags` and lists installed
models; "Save and Reload" persists to QgsSettings and reboots the
engine.

---

## Ollama Configuration

| Key | Default | Stored in |
|---|---|---|
| `OLLAMA_ENDPOINT` | `http://localhost:11434` | QgsSettings `GeoSI/ollama_endpoint` |
| `OLLAMA_MODEL` | `mistral` | QgsSettings `GeoSI/ollama_model` |

Recommended models (tested): `mistral`, `llama3.1`, `llama3.2`,
`qwen2.5`, `phi3`, `gemma2`. Install with `ollama pull <name>`.

---

## Error Handling and Recovery

| Component | Failure | Recovery |
|---|---|---|
| Parser | Ollama offline | 1.5s probe fails; try next provider |
| Parser | All LLMs fail | Rule-based keyword parser (always succeeds) |
| Parser | Bad JSON from LLM | Tolerant extraction, then keyword fallback |
| Agent | Layer missing | Empty plan with clear error + similar-layer suggestions |
| Agent | Ollama down | Gemini -> Anthropic -> rule-based plan |
| Executor | Tool raises | Log error; continue with next step; partial result |
| QGIS Backend | `processing` unavailable | Tool returns `ToolResult(success=False)` |
| Plugin | Engine init fails | Traceback printed; dock shows error |
| Dock | Query fails | Chat shows error + lists loaded layers |

---

## Common Workflows

### Workflow 1: Buffer + Intersect

```
User: "Find residential zones within 500m of hospitals"

parser:  intent=PROXIMITY, entities={primary:hospitals, secondary:residential}
         parameters={distance_value:500, distance_unit:meters}
agent:   plan = [buffer(hospitals, 500), intersect(prev, residential)]
exec:    buffer output registered as step_1_output;
         intersect reads step_1_output + residential;
         final Layer stored in state.
```

### Workflow 2: Raster NDVI

```
User: "Calculate NDVI from Sentinel2_red and Sentinel2_nir"

parser:  intent=RASTER, operation=ndvi
agent:   plan = [ndvi(RED=Sentinel2_red, NIR=Sentinel2_nir)]
exec:    BackendTool dispatches to "qgis" backend ->
         processing.run("native:rastercalc", {...}) -> NDVI raster.
```

### Workflow 3: Layer Not Found

```
User: "Buffer rivers by 100m"     (only Assets and Kerala are loaded)

parser:  primary="rivers"
agent:   validate_layers_exist -> False
plan:    empty, reasoning="Layer 'rivers' not found. Available: Assets, Kerala"
dock:    shows the error in red and lists loaded layers.
```

---

## Quick Reference

| Need | Class / Module | Key method |
|---|---|---|
| Run NL query | `geosi_engine.GeoSI` | `.query(text)` |
| List tools | `ToolRegistry` | `.list_tools(category=None)` |
| Run a tool directly | `ToolRegistry` | `.execute_tool(name, **params)` |
| Parse text only | `QueryParser` | `.parse(text, layers)` |
| Plan only | `GeoSIAgent` | `.plan(request, state)` |
| Execute only | `ExecutionEngine` | `.run(plan)` |
| Install QGIS backend | `qgis_bridge` | `.install()` |
| Chat dock UI | `GeoSIDock` | `_run_query()`, `_sync_qgis_layers()` |

---

## Summary

GeoSI is a three-surface architecture around one universal engine:

- **Engine** = language-model-aware GIS brain with 125 tools.
- **Plugin** = the only QGIS-specific code; chats, syncs layers, runs
  tools through QGIS Processing.
- **Server** = optional REST surface that can auto-fetch OSM data when
  it is clearly safe to do so.

Four rules keep it clean:

1. The engine never imports QGIS.
2. The plugin only operates on layers already in the QGIS Layers panel
   and never auto-fetches data.
3. Ollama is first; everything else is a fallback.
4. Every failure path ends in a user-readable message, never a crash.
