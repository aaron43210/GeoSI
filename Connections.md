# GeoSI — Complete Architecture & Component Connections

**Last Updated:** 7 May 2026  
**Purpose:** Reduce token usage by mapping the entire codebase structure and dependencies

---

## Project Overview

GeoSI (Geospatial Superintelligence) is a QGIS plugin that allows users to perform GIS operations via natural language prompts. It leverages an AI agent to parse user intent, plan multi-step workflows, and execute GIS tools via QGIS Processing or GeoPandas.

**Architecture Principle:** The engine core is framework-agnostic (no QGIS imports). Only the plugin surface (qgis_bridge.py) couples to QGIS.

---

## Directory Structure & Component Map

### Root Level Files
| File | Purpose | Key Exports |
|------|---------|-------------|
| `__init__.py` | Plugin entry factory | `classFactory()` → returns `GeoSIPlugin` |
| `geosi_plugin.py` | Main plugin class | `GeoSIPlugin` class; manages toolbar, dock widget, GUI |
| `metadata.txt` | QGIS plugin metadata | Plugin name, version, CRS support, description |
| `prompt_dock.py` | Qt dock widget UI | `GeoSIDock` class; chat interface, query runner, API key mgmt |
| `qgis_bridge.py` | QGIS backend adapter | Registers QGIS processing backend with engine |

### Engine Package (`geosi_engine/`)
| Module | Lines | Purpose | Key Classes/Functions |
|--------|-------|---------|----------------------|
| `__init__.py` | ~70 | Package entry; public API | `GeoSI` convenience class |
| `models.py` | ~600+ | Data structures (NO imports) | `ExecutionStatus`, `IntentType`, `GeometryType`, `ToolParameter`, `ToolSpec`, `Layer`, `ToolResult`, `AnalysisRequest`, `ExecutionPlan`, `ExecutionResult` |
| `base.py` | ~250+ | Abstract tool contract | `GISTool` (abstract), `PortableTool`, `BackendTool`, `QGISProcessingTool`, `register_backend()`, `get_backend()` |
| `registry.py` | ~200+ | Tool discovery & execution hub | `ToolRegistry` class; auto-discovers tools in `tools/` package |
| `state.py` | ~200+ | Workspace state tracking | `StateManager` class; manages layers, results, history, checkpoints |
| `parser.py` | ~1000+ | NL→structured request | `QueryParser` class; LRU cache, LLM fallback, regex keyword mapping |
| `agent.py` | ~500+ | Multi-step workflow planning | `GeoSIAgent` class; parses, validates layers, plans execution |
| `executor.py` | ~200+ | Step-by-step execution | `ExecutionEngine` class; runs `ExecutionPlan`, wires outputs to inputs |
| `validation.py` | ~300+ | Spatial data validation | `ValidationEngine` class; geometry, topology, CRS, operation precondition checks |

### Tools Package (`geosi_engine/tools/`)
Tools auto-discovered and registered by `ToolRegistry.discover_tools()` via class introspection.

| Module | Tool Count | Domain | Tool Pattern |
|--------|-----------|--------|--------------|
| `vector.py` | 40 | Geometry & overlay | Buffer, intersect, union, clip, dissolve, centroid, simplify, etc. |
| `raster.py` | 25 | Raster analysis | Slope, aspect, hillshade, NDVI, zonal stats, clip, warp, etc. |
| `network.py` | 8 | Routing & graphs | Shortest path, service area, cost matrix, network building |
| `terrain.py` | 10 | 3D & terrain | Viewshed, profile, watershed, flow direction, TIN mesh, etc. |
| `temporal.py` | 6 | Time-series | Temporal filter, change detection, temporal aggregation |
| `ai_ml.py` | 10 | Spatial ML | Clustering, hotspot, interpolation (IDW, kriging), anomaly detection |
| `cartography.py` | 10 | Export & styling | GeoJSON/Shapefile/KML export, geocoding, labeling, atlas |
| `validation.py` | 10 | Data QA | Geometry validity, topology check, CRS consistency, gap/overlap detection |
| `portable.py` | 2+ | Cross-platform | Load/save via GeoPandas, Rasterio (non-QGIS) |
| `__init__.py` | — | Package marker | Imports & tool patterns documented |

**Total Tools:** 80+ auto-discovered tools

---

## Data Flow & Component Interactions

### Flow 1: User Types Prompt → Results Display

```
1. User types natural language query in prompt_dock.py → GeoSIDock.prompt QLineEdit
2. User presses Enter or clicks "▶ Run" → GeoSIDock._run_query()
3. GeoSIDock._sync_qgis_layers() → pulls current QGIS layers into StateManager
4. _QueryWorker thread spawns → calls GeoSI.query(query_text)
5. Inside GeoSI.query():
   a. agent.parse(query, state) → QueryParser produces AnalysisRequest
   b. agent.plan(request, state) → GeoSIAgent produces ExecutionPlan
   c. executor.run(plan) → ExecutionEngine executes each ToolStep
6. ExecutionResult sent back to _on_result() → chat display updated
7. If success, QGIS canvas refreshed with output layers
```

**LLM Priority Chain:**
1. ✅ **Ollama** (local-first, no API key required) — http://localhost:11434
2. ✅ **Google Gemini** (if GEMINI_API_KEY set)
3. ✅ **Anthropic Claude** (if ANTHROPIC_API_KEY set)
4. ✅ **Keyword-based fallback** (always available, no LLM required)

### Flow 2: Tool Discovery & Registration

```
1. ToolRegistry.__init__(auto_discover=True) called by GeoSI.__init__()
2. discover_tools() walks geosi_engine.tools/ package
3. For each module (vector.py, raster.py, etc.):
   - Dynamically created tool classes inherit from GISTool subclasses
   - Each class implements spec() and execute()
   - Tool instance created and registered in ToolRegistry._tools dict
4. ToolRegistry ready to execute by tool name
```

### Flow 3: Execution Plan → Step Output Wiring

```
ExecutionEngine.run(plan: ExecutionPlan) → ExecutionResult:
  for step in plan.steps:
    1. Resolve step input parameters
    2. Substitute references to prior step outputs (step_outputs dict)
    3. Call registry.execute_tool(step.tool_name, **resolved_params)
    4. Capture ToolResult, store in step_outputs[step.output_name]
    5. Auto-register output Layer in state.layers
    6. Log execution time, success/failure
  return ExecutionResult with all logs, outputs, final answer
```

---

## Key Dependencies & Imports

### Imports Pattern

| Module | Imports From | Purpose |
|--------|--------------|---------|
| `__init__.py` (plugin) | None (PyQt, QGIS only) | Entry point |
| `geosi_plugin.py` | `qgis_bridge`, `prompt_dock` | Plugin GUI |
| `prompt_dock.py` | `geosi_engine` (GeoSI class only) | Query dispatcher |
| `qgis_bridge.py` | `geosi_engine.base`, `models` | Backend registration |
| **Engine modules** | — | **No QGIS imports ever** |
| `models.py` | stdlib only (dataclasses, enum, typing) | Foundation (imported by all) |
| `base.py` | `models` | Abstract contracts, backend dispatch |
| `registry.py` | `base`, `models`, all `tools/*.py` | Tool discovery & execution |
| `state.py` | `models` | Workspace state |
| `parser.py` | `models` | NL parsing (LLM optional) |
| `agent.py` | `models`, `parser`, `registry`, `state`, `validation` | Planning & layer validation |
| `executor.py` | `models`, `registry`, `state` | Execution |
| `validation.py` | `models` | Data validation |
| All `tools/*.py` | `base`, `models` | Tool implementations |
| `portable.py` | `base`, `models`, geopandas/rasterio (optional) | Cross-platform tools |

### Dependency Tree (Simplified)

```
models.py (foundation — no deps)
  ↑
  ├─ base.py
  │   ├─ tools/* (all tool modules)
  │   └─ backend dispatch
  ├─ state.py
  ├─ parser.py
  ├─ validation.py
  └─ registry.py
      ├─ base.py → tools/*
      ├─ agent.py
      └─ executor.py

GeoSI (convenience class in __init__.py)
  ├─ ToolRegistry
  ├─ StateManager
  └─ (used by agent & executor)

UI Layer:
  prompt_dock.py (GeoSIDock)
    ├─ GeoSI engine instance
    └─ qgis_bridge (registers backend)
```

---

## State Management

### StateManager Lifecycle

| Method | Responsibility |
|--------|-----------------|
| `__init__()` | Create fresh workspace (empty layers, results, history, checkpoints) |
| `add_layer(layer)` | Register spatial layer by name |
| `get_layer(name)` | Lookup layer by name |
| `list_layers()` | Return all layer names |
| `save_result(name, result)` | Cache intermediate result; auto-register output Layer |
| `add_checkpoint(op_id)` | Snapshot layers & results for undo |
| `rollback(op_id)` | Restore from checkpoint |

**Auto-Registration:** If a ToolResult contains an output Layer, StateManager automatically registers it in `self.layers` so downstream steps can reference it.

---

## Tool Types & Execution Models

### Tool Base Classes (from `base.py`)

| Class | Backend | Execution | Example |
|-------|---------|-----------|---------|
| `PortableTool` | Self-implemented | Direct Python (GeoPandas, Rasterio) | `LoadLayerTool` in `portable.py` |
| `QGISProcessingTool` | QGIS | Delegates to `processing.run()` via registered "qgis" backend | Most vector/raster tools |
| `BackendTool` | Pluggable | Calls backend function by name | For dynamic dispatch |

### Execution Flow (QGISProcessingTool Example)

```
1. ToolRegistry.execute_tool("buffer", INPUT=layer, DISTANCE=500)
2. get_tool("buffer") returns BufferTool instance
3. BufferTool.safe_execute(INPUT=layer, DISTANCE=500)
   a. Validation: check required params
   b. Call self.execute() → BackendTool.execute() (spec'd, no impl)
   c. Call backend_fn("native:buffer", {INPUT, DISTANCE})
   d. qgis_bridge._run_qgis_algorithm() → processing.run()
   e. Catch result or error → ToolResult
   f. Log timing, return ToolResult
```

---

## Intent Classification (Parser)

The parser maps natural language to `IntentType` enum:

| Intent | Keywords | Tools Considered |
|--------|----------|-------------------|
| PROXIMITY | buffer, within, near, distance, radius | buffer, intersect, nearest-feature |
| OVERLAY | intersect, union, clip, difference, merge | all overlay tools |
| GEOMETRY | centroid, simplify, convex hull, dissolve | geometry transformation tools |
| RASTER | NDVI, raster calc, band, zonal stats | raster analysis tools |
| TERRAIN | slope, aspect, viewshed, DEM, contour | terrain tools |
| NETWORK | route, shortest path, service area | routing tools |
| TEMPORAL | change detection, time series, trend | temporal tools |
| AI_ML | cluster, classify, interpolate, hotspot | ML/stats tools |
| VALIDATION | check validity, topology, gaps, CRS | validation tools |
| STATISTICS | count, sum, mean, stats | aggregation tools |
| DATA_MANAGEMENT | load, save, convert, export | portable tools |
| CARTOGRAPHY | export, geocode, style, map | cartography tools |
| UNKNOWN | fallback | basic tools (count, intersect) |

---

## Error Handling & Fallbacks

| Component | Failure Scenario | Recovery |
|-----------|------------------|----------|
| **Parser** | Ollama not available | Fall back to Gemini/Anthropic/keyword |
| **Parser** | All LLMs fail | Fall back to regex keyword matching |
| **Parser** | Bad LLM JSON response | Tolerant extraction, then keyword fallback |
| **Agent** | Ollama not responding | Fall back to Gemini/Anthropic/rules |
| **Agent** | Layer not found | Fuzzy matching; suggest similar layer names |
| **Executor** | Tool execution fails | Log error, continue to next step (partial result) |
| **QGIS Backend** | processing not available | Return ToolResult.success=False |
| **Plugin Init** | Engine load fails | Print traceback, show error in QGIS message bar |
| **Dock Toggle** | First dock creation | Create GeoSIDock() on first click, cache it |

---

## Configuration & Storage

### Ollama (Local LLM)
- **Endpoint:** `OLLAMA_ENDPOINT` (default: `http://localhost:11434`)
- **Model:** `OLLAMA_MODEL` (default: `mistral`)
- **Stored in:** QgsSettings (QGIS native settings db)
- **Keys:** "GeoSI/ollama_endpoint", "GeoSI/ollama_model"
- **Advantage:** No API keys needed, runs locally, completely private
- **Setup:** Install Ollama from https://ollama.ai, run `ollama pull mistral`

### API Key Storage (Fallback)
- **Claude:** `ANTHROPIC_API_KEY` stored in QgsSettings key "GeoSI/anthropic_api_key"
- **Gemini:** `GEMINI_API_KEY` environment variable
- **Priority:** Ollama is tried first; cloud APIs only if Ollama fails

### Tool Caching
- **LRU Cache:** In-process query cache (normalized query + layer list)
- **Disk Cache:** Optional JSON cache in QGIS profile directory
- **Rationale:** Repeated prompts skip expensive LLM calls

---

## Performance Notes

### Token/Latency Reduction Strategies
1. **No QGIS imports in engine** → Portable across server, CLI, tests
2. **Tool auto-discovery via reflection** → Dynamic tool loading
3. **Parser caching** → Repeated queries instant
4. **Fuzzy layer matching** → Users can type "schoo" for "School_Districts.shp"
5. **Validation before execution** → Fail fast with clear errors
6. **Backend dispatch abstraction** → Easy to swap QGIS ↔ GeoPandas
7. **Step output wiring** → Intermediate results feed downstream without saving

---

## Common Workflows

### Scenario 1: Vector Buffer & Intersect

```
User: "Buffer hospitals by 500m and intersect with residential zones"

1. Parser identifies: PROXIMITY intent, entities {layer: "hospitals", distance: "500m"}
2. Agent plans: [buffer(layer="hospitals", distance=500), intersect(prev_output, "residential")]
3. Executor:
   Step 1: registry.execute_tool("buffer", INPUT="hospitals", DISTANCE=500)
           → BufferedHospitals layer registered
   Step 2: registry.execute_tool("intersect", INPUT="BufferedHospitals", OVERLAY="residential")
           → result layer returned
4. Result displayed in QGIS canvas
```

### Scenario 2: Raster NDVI Calculation

```
User: "Calculate NDVI from red and NIR bands"

1. Parser: RASTER intent, {red_band: "red", nir_band: "nir"}
2. Agent: [ndvi(red_band, nir_band)]
3. Executor:
   registry.execute_tool("ndvi", RED_BAND="red", NIR_BAND="nir")
   → processing.run("native:rastercalc", {RED=red, NIR=nir})
   → NDVI raster output
4. Rendered in QGIS
```

### Scenario 3: No QGIS Available (Server/CLI)

```
User API call: POST /geosi/query?q="Buffer parks by 100m"

1. Server does NOT install qgis backend
2. Parser identifies PROXIMITY
3. Agent tries to plan but has no tools (engine in server mode)
4. Or: Server registers "geopandas" backend instead of "qgis"
5. Executor calls _run_geopandas_algorithm() → GeoPandas code
6. Result returned as GeoJSON
```

---

## Key Files to Edit for Common Tasks

| Task | Primary File(s) |
|------|-----------------|
| Add new tool | `geosi_engine/tools/{domain}.py` (add tuple to `_TOOL_DEFS`) |
| Change UI layout | `prompt_dock.py` (GeoSIDock.__init__ layout section) |
| Modify parser keywords | `geosi_engine/parser.py` (`_INTENT_KEYWORDS` dict) |
| Add data model field | `geosi_engine/models.py` (dataclass definition) |
| Support new backend (GeoPandas) | `qgis_bridge.py` analog + `register_backend()` call |
| Adjust validation rules | `geosi_engine/validation.py` (ValidationEngine methods) |
| Change execution logic | `geosi_engine/executor.py` (ExecutionEngine.run method) |
| Add agent planning logic | `geosi_engine/agent.py` (GeoSIAgent.plan method) |

---

## Summary

**GeoSI is a 3-tier architecture:**

1. **UI Tier** (prompt_dock.py, geosi_plugin.py): Qt widgets, QGIS integration
2. **Engine Tier** (geosi_engine/): Framework-agnostic planning & execution
3. **Tools Tier** (geosi_engine/tools/): 80+ domain-specific GIS operations

**Key Principles:**
- ✅ Engine has NO QGIS imports → reusable in FastAPI, CLI, tests
- ✅ Tools auto-discovered via reflection → easy to add new tools
- ✅ Backend dispatch abstraction → pluggable backends (QGIS, GeoPandas, etc.)
- ✅ State management → layer caching, result tracking, undo/redo support
- ✅ Parser resilience → LLM fallback to regex keyword matching
- ✅ Step wiring → outputs flow to inputs seamlessly

---

## Quick Reference

| Concept | Class/Module | Key Method |
|---------|-------------|-----------|
| Main entry | `geosi_engine.GeoSI` | `.query(text)` |
| All tools | `geosi_engine.registry.ToolRegistry` | `.discover_tools()`, `.execute_tool()` |
| Parsing | `geosi_engine.parser.QueryParser` | `.parse(query, layers)` |
| Planning | `geosi_engine.agent.GeoSIAgent` | `.plan(request, state)` |
| Execution | `geosi_engine.executor.ExecutionEngine` | `.run(plan)` |
| State | `geosi_engine.state.StateManager` | `.add_layer()`, `.save_result()` |
| Validation | `geosi_engine.validation.ValidationEngine` | `.validate_geometry()`, `.validate_operation()` |
| Plugin UI | `prompt_dock.GeoSIDock` | `_run_query()`, `_init_engine()` |
| QGIS Bridge | `qgis_bridge` | `.install()` → registers backend |

