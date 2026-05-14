# GeoSI — Geospatial Superintelligence QGIS Plugin

**Version 1.0.0** — Quantum Hydrology & Complex Workflows Update

A state-of-the-art AI agent that lives inside QGIS. Transform your GIS workflows with natural language prompts and 128 advanced spatial analysis tools.

## 🎯 Key Features

### 🎯 Automatic Layer Loading
- **✨ All tool outputs instantly appear in QGIS Layers Panel**
- No manual file selection required — just ask and results load
- Intelligent format detection (raster, vector, multi-layer)
- See [LAYER_AUTO_LOADING.md](LAYER_AUTO_LOADING.md) for details

### AI-Powered Workflows
- **Natural Language Interface**: Type prompts instead of clicking menus
- **Multi-Step Orchestration**: Complex workflows execute in a single command
- **128 Integrated Tools**: Vector, raster, terrain, network, ML, and temporal analysis
- **Intelligent Parsing**: Ollama-first LLM support (Claude/Gemini fallbacks)

### What's New in v1.0.0

#### 🌊 **Complete Watershed Analysis Workflow**
- 5-step hydrological pipeline: DEM preprocessing → flow direction → flow accumulation → delineation → polygonization
- D8 flow direction algorithm
- Customizable flow threshold and fill distance
- Full watershed statistics output
- Perfect for: drainage basin analysis, flood modeling, water resource planning

#### ⚙️ **Complex Workflow Framework**
- Multi-step orchestration engine
- Automatic error handling and validation
- All intermediate outputs available
- Metadata tracking across steps

#### 🎨 **Premium User Interface**
- Dark mode with modern typography
- Qt6 compatibility for QGIS 4
- Real-time AI insight boxes
- Responsive chat interface

## 📋 System Requirements

| Component | Requirement |
|-----------|-------------|
| QGIS Version | 3.22 - 4.99 |
| Python | 3.8+ |
| Qt | Qt5 (QGIS 3.x) or Qt6 (QGIS 4.x) |
| Optional LLM | Ollama (local), Claude API, Google Gemini |

## 🚀 Installation

1. **Install from ZIP** (for QGIS 3.22+):
   
   **QGIS 3.x:**
   - Extract to: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/` (Linux/Mac)
   - Or: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\` (Windows)
   
   **QGIS 4.x:**
   - Extract to: `~/.local/share/QGIS/QGIS4/profiles/default/python/plugins/` (Linux/Mac)
   - Or: `%APPDATA%\QGIS\QGIS4\profiles\default\python\plugins\` (Windows)

2. **Enable in QGIS**:
   - Plugins → Manage and Install Plugins
   - Search for "GeoSI"
   - Click Install

3. **Configure LLM** (optional):
   - Click ⚙️ in the GeoSI panel
   - Add Ollama endpoint or API keys

## 🎮 Quick Start

1. **Open GeoSI Panel**: Click toolbar icon (🌍) or Plugins → GeoSI
2. **Load Data**: Open your shapefile/raster in QGIS
3. **Type a Prompt**: 
   ```
   Perform complete watershed analysis on DEM
   ```
4. **View Results**: Outputs appear in QGIS Layers panel

## 📖 Example Prompts

### Watershed & Hydrology
- `Analyze watersheds from DEM with threshold 500`
- `Calculate flow direction and accumulation on DEM`
- `Delineate drainage basins from elevation model`

### Vector Analysis
- `Buffer Schools by 500 meters`
- `Intersect Schools with Kerala`
- `Count points in polygon for Schools within Kerala`

### Raster Analysis
- `Calculate slope from DEM`
- `Reclassify DEM into 5 elevation zones`
- `Calculate NDVI from Landsat bands`

### Complex Multi-Step
- `Buffer hospitals, intersect with flood zones, calculate affected population`
- `Clip roads to study area, find intersections with rivers, export results`

## 🛠 Troubleshooting

### Plugin Won't Load
- Ensure QGIS version is 3.22 or higher
- Check Python path in QGIS Settings
- Review QGIS log (Help → Log Messages)

### Tools Not Appearing
- Click 🔄 reload button in GeoSI panel
- Restart QGIS
- Check QGIS console for import errors

### LLM Not Working
- Verify Ollama is running: `http://localhost:11434`
- Set API key: In ⚙️ Config panel or `ANTHROPIC_API_KEY` env var
- Try keyword-based fallback (no LLM required)

### QGIS 4 Compatibility Issues
- Qt6 is fully supported (automatic detection)
- Report issues with details on: https://github.com/geosi/geosi-qgis-plugin/issues

## 🔌 Architecture

```
geosi_plugin/
├── __init__.py              Loader
├── geosi_plugin.py          Main plugin class
├── qgis_bridge.py           QGIS backend dispatch
├── prompt_dock.py           UI dock widget
└── geosi_engine/            Universal engine (no QGIS imports)
    ├── agent.py             Planning
    ├── executor.py          Execution
    ├── parser.py            NL parsing
    └── tools/               128 GIS tools
```

**Key Design**: The engine is framework-independent. Same code runs in:
- QGIS plugin (with QGIS processing backend)
- FastAPI server (with portable backend)
- Jupyter notebooks (with GeoPandas backend)
- CLI tools

## 📊 Available Tools by Category

| Category | Count | Examples |
|----------|-------|----------|
| Vector | 40 | Buffer, intersect, union, dissolve, clip |
| Raster | 25 | NDVI, reclassify, focal stats, warp |
| Terrain | 10 | **Watershed workflow**, slope, aspect, viewshed |
| Network | 8 | Shortest path, service area, OD matrix |
| AI/ML | 10 | K-means, hotspot analysis, IDW interpolation |
| Cartography | 10 | Export, geocode, styling, labels |
| Validation | 10 | Geometry check, topology, CRS validation |
| Temporal | 6 | Change detection, temporal aggregate |
| Portable I/O | 2 | Load/save layers |

## 🔐 Privacy & Data

- **No data is sent to external servers** by default
- Local Ollama LLM runs entirely on your machine
- Optional: Use Claude/Gemini API (your credentials)
- All layers stay in QGIS project



### v1.0.0 (Intelligent Layer Auto-Loading)
- ✨ Automatic layer loading to QGIS Layers Panel
- 🎯 Smart format detection (raster/vector)
- 📊 GeoSI Layer → QGIS layer conversion
- 🔄 Results instantly visible after analysis
- 📈 Real-time user feedback for each layer
- 🛡️ Enhanced error handling & validation
- 📚 Comprehensive auto-loading documentation


- ✨ Complete Watershed Analysis workflow (5-step pipeline)
- ✨ Complex multi-step workflow orchestration framework
- 🔧 Qt6 & QGIS 4 full compatibility
- 🎨 Premium dark UI redesign
- 📊 128 total GIS tools
- 🚀 Improved QGIS backend system


- 🎉 Core AI agent
- 🛠 127 GIS tools
- 🧠 Ollama LLM integration

## 🤝 Contributing

Report bugs or request features:
- GitHub: https://github.com/geosi/geosi-qgis-plugin/issues
- Email: aaronr.ds25@duk.ac.in

## 📄 License

GeoSI — Geospatial Superintelligence

## 🙏 Acknowledgments

- QGIS Foundation & community
- Ollama for local LLM support
- Anthropic Claude & Google Gemini APIs
- All contributors and users

---

**Ready to transform your GIS workflows?** Open the GeoSI panel and start analyzing! 🚀
