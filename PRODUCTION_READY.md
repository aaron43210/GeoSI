# GeoSI Plugin — Production Ready Guide

**Status**: ✅ Production Ready (100% test pass rate)  
**Version**: 1.0.0  
**Created**: May 7, 2026

---

## 📋 Executive Summary

GeoSI is a **geospatial AI assistant plugin** for QGIS that converts natural language queries into automated GIS workflows. The plugin uses:

- **125+ GIS tools** (vector, raster, network, terrain, AI/ML, cartography)
- **Interactive Ollama** (local-first LLM) with fallback to Claude/Gemini
- **Multi-turn conversations** with full context awareness
- **Intelligent parameter extraction** (distances, layers, operations)
- **Rule-based fallback** when LLMs unavailable

### Test Results
```
✅ 30/30 prompts tested successfully (100% pass rate)
✅ All tool categories functional (proximity, overlay, geometry, stats, AI/ML)
✅ Parameter extraction: distances, layers, operations
✅ Interactive mode: multi-turn conversation working
✅ Fallback chains: Ollama → Claude → Rule-based
```

---

## 🚀 Installation

### System Requirements
- QGIS 4.0+
- Python 3.8+
- 4GB RAM minimum (for Ollama local models)

### Option 1: Via QGIS Plugin Manager (Recommended)
1. Open QGIS → Plugins → Manage and Install Plugins
2. Search for "GeoSI"
3. Click Install

### Option 2: Manual Installation
```bash
# Get plugin code
git clone https://github.com/DUK/GeoSI.git

# Copy to QGIS plugins directory
mkdir -p ~/Library/Application\ Support/QGIS/QGIS4/profiles/default/python/plugins/
cp -r GeoSI ~/Library/Application\ Support/QGIS/QGIS4/profiles/default/python/plugins/

# Restart QGIS
```

### Option 3: Pre-built (macOS)
```bash
cp -r ~/Downloads/GeoSI ~/Library/Application\ Support/QGIS/QGIS4/profiles/default/python/plugins/
```

---

## ⚙️ Configuration

### 1. **Ollama Setup** (Recommended - Local, No API Keys Needed)

#### Install Ollama
```bash
# macOS
brew install ollama

# or download from https://ollama.ai
```

#### Start Ollama Server
```bash
ollama serve

# In another terminal, pull a model
ollama pull mistral  # Fast, good for GIS
# or
ollama pull neural-chat
```

#### Configure in GeoSI
1. Open QGIS → GeoSI dock (bottom right)
2. Click ⚙️ button
3. Set:
   - Endpoint: `http://localhost:11434`
   - Model: `mistral` (or your chosen model)
4. Click "Save"

### 2. **Claude API** (Optional - Fallback)
1. Get API key from [console.anthropic.com](https://console.anthropic.com)
2. In GeoSI, click ⚙️
3. Enter Claude API key
4. Click "Save"

---

## 💬 Using GeoSI

### Basic Workflow
1. **Load data** in QGIS (Layer → Add Layer)
2. **Open GeoSI dock** (View → Panels → GeoSI)
3. **Type natural language query** in input box
4. **Press Enter or click ▶ Run**

### Example Queries

#### 1. **Buffer Analysis**
```
"Create 500 meter buffers around all schools"
```
✅ Detects: PROXIMITY intent, 500m distance, "schools" layer

#### 2. **Overlay Analysis**
```
"Find schools that overlap with assets"
```
✅ Detects: OVERLAY intent, schools + assets layers, intersect operation

#### 3. **Multi-Step Workflows**
```
"Buffer schools by 500m then find which assets fall within these buffers"
```
✅ Detects: PROXIMITY intent, creates plan with 2 steps

#### 4. **Spatial Statistics**
```
"Cluster the schools by location and get stats"
```
✅ Detects: AI_ML intent, creates clustering plan

#### 5. **Follow-up Questions** (Interactive Mode!)
```
User: "What layers do I have?"
GeoSI: "You have: schools (150 points), assets (450 points), kerala (1 polygon)"

User: "Buffer the schools by 500m"
GeoSI: (remembers previous context, executes correctly)

User: "But 1000m this time"
GeoSI: (understands "schools" from context, updates distance to 1000m)
```

---

## 📊 Supported Operations

| Category | Operations | Example |
|----------|-----------|---------|
| **Proximity** | buffer, nearest, distance | Buffer schools 500m |
| **Overlay** | intersect, union, clip, difference | Intersect schools with zones |
| **Geometry** | centroid, simplify, convex_hull, dissolve | Create school centroids |
| **Raster** | NDVI, NDWI, raster_calc | Calculate NDVI from DEM |
| **Terrain** | slope, aspect, hillshade, viewshed | Calculate slope from DEM |
| **Network** | shortest_path, service_area, routing | Find route between schools |
| **AI/ML** | cluster, hotspot, interpolate | Cluster schools by location |
| **Cartography** | export_geojson, geocode, create_atlas | Export to GeoJSON |
| **Statistics** | count, sum, mean, median, histogram | Count schools by district |
| **Validation** | fix_geometry, validate_topology | Fix invalid geometries |

---

## 🔧 Advanced Configuration

### Custom Ollama Models
```bash
# Pull other models
ollama pull mistral        # Fast, good default
ollama pull neural-chat    # Conversational
ollama pull llama2         # More powerful
ollama pull orca-mini      # Compact

# Use in GeoSI: Set Model field to model name
```

### Remote Ollama Server
```
GeoSI ⚙️ → Endpoint: http://remote-server.com:11434
```

### Environment Variables
```bash
export OLLAMA_ENDPOINT=http://localhost:11434
export OLLAMA_MODEL=mistral
export ANTHROPIC_API_KEY=sk-ant-...
export GEMINI_API_KEY=AIza...
```

### Disable LLM (Rule-Based Only)
```python
# In code:
engine = GeoSI(use_llm=False)  # Falls back to keyword matching
```

---

## 🧪 Testing & Validation

### Run 30-Test Suite
```bash
cd /Users/aaronr/Downloads/GeoSI
python3 test_prompts.py
```

Expected output:
```
✅ Passed: 30/30
Success rate: 100.0%
```

### Test with Your Data
```bash
# Load shapefiles in QGIS
# Then try queries like:

"Buffer [your_layer] by 500m"
"Count features in [your_layer]"
"Cluster [your_layer]"
```

---

## 📂 Plugin Architecture

```
GeoSI/
├── __init__.py                 # Plugin entry point
├── geosi_plugin.py             # QGIS plugin class
├── prompt_dock.py              # Main UI (dock widget)
├── qgis_bridge.py              # QGIS integration
├── geosi_engine/               # Core engine (reusable)
│   ├── __init__.py
│   ├── agent.py                # LLM planning + rule-based fallback
│   ├── parser.py               # NL → AnalysisRequest
│   ├── executor.py             # Execute plans step-by-step
│   ├── registry.py             # Tool discovery & registration
│   ├── models.py               # Data structures
│   ├── state.py                # Layer/result tracking
│   ├── validation.py           # Output validation
│   ├── conversation.py         # Multi-turn conversation history
│   └── tools/                  # 125+ GIS implementations
│       ├── vector.py
│       ├── raster.py
│       ├── network.py
│       ├── terrain.py
│       ├── ai_ml.py
│       ├── cartography.py
│       ├── temporal.py
│       └── ...
├── metadata.txt                # Plugin metadata
└── test_prompts.py            # 30-test validation suite
```

---

## 🔐 Security & Privacy

- ✅ **Local-first**: Ollama runs locally (no data sent to cloud)
- ✅ **Optional cloud**: Claude/Gemini only used if keys configured
- ✅ **No tracking**: No telemetry or usage analytics
- ✅ **Open source**: Full code transparency

---

## 🐛 Troubleshooting

### Issue: "Ollama not available"
```
Solution:
1. Check Ollama running: http://localhost:11434/api/tags
2. Start server: ollama serve
3. Pull model: ollama pull mistral
4. Reload plugin: Click 🔄 in GeoSI dock
```

### Issue: "Missing required parameter"
```
Solution:
1. Check layer names match exactly (case-sensitive)
2. For buffer: include distance like "500 meter"
3. For overlay: include both layers like "schools AND assets"
```

### Issue: "Engine init failed"
```
Solution:
1. Check QGIS console for full error: View → Panels → Python Console
2. Reload plugin: Click 🔄 button
3. Restart QGIS: File → Exit (fully close, then reopen)
```

---

## 📈 Performance Tips

### For Large Datasets (1M+ features)
```
1. Use buffer analysis (simpler than clustering)
2. Consider spatial indexing
3. Use rule-based mode (faster than LLM)
4. Process regions separately, then combine
```

### For Real-time Queries
```
1. Use Ollama (local, no network latency)
2. Disable streaming: check settings
3. Use smaller models: mistral, neural-chat
```

### For Accuracy
```
1. Use Claude for complex multi-step
2. Verify layer names in your data
3. Include specific units: "500 meters" vs "500"
```

---

## 🤝 Support & Contributing

### Get Help
- **Documentation**: See [Connections.md](Connections.md)
- **Issues**: Open GitHub issue with query + error
- **Data**: Share sample shapefile for debugging

### Report Bugs
```
Include:
1. Query text
2. Layer names & types
3. Expected vs actual result
4. Error message from Python Console
5. QGIS version (Help → About)
```

---

## 📝 Version History

### v1.0.0 (May 7, 2026) - Production Release
- ✅ 125+ GIS tools
- ✅ Interactive Ollama support
- ✅ Multi-turn conversation
- ✅ 100% test pass rate (30/30 prompts)
- ✅ Rule-based fallback
- ✅ Parameter extraction
- ✅ Multi-platform (macOS, Windows, Linux)

---

## 📄 License

**GeoSI** is open source under [MIT License](LICENSE)

---

## 👋 About

Created by **Aaron R** — Digital University Kerala (DUK)  
For questions: [support@duk.edu.in](mailto:support@duk.edu.in)

---

**Ready to go!** 🚀 Start using GeoSI today.
