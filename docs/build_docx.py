"""Generate the GeoSI handbook (GeoSI_Handbook.docx)."""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = Path(__file__).resolve().parent.parent / "GeoSI_Handbook.docx"

NAVY = RGBColor(0x0B, 0x2A, 0x4A)
TEAL = RGBColor(0x10, 0x8A, 0x92)
MUTED = RGBColor(0x55, 0x5F, 0x6D)


def h(doc, text, level=1, color=NAVY):
    p = doc.add_heading("", level=level)
    r = p.add_run(text)
    r.font.color.rgb = color
    r.font.name = "Calibri"


def para(doc, text, size=11, color=None, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size); r.font.name = "Calibri"
    if color: r.font.color.rgb = color
    r.italic = italic
    return p


def bullets(doc, items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        r = p.add_run(it)
        r.font.size = Pt(11); r.font.name = "Calibri"


def code(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.name = "Consolas"; r.font.size = Pt(10)


def build():
    doc = Document()
    styles = doc.styles["Normal"]
    styles.font.name = "Calibri"; styles.font.size = Pt(11)

    # Cover
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("GeoSI"); r.font.size = Pt(60); r.bold = True; r.font.color.rgb = NAVY
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Geospatial Superintelligence  Handbook"); r.font.size = Pt(22); r.font.color.rgb = TEAL
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("The beginning of geospatial superintelligence."); r.italic = True; r.font.size = Pt(14); r.font.color.rgb = MUTED
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Aaron R  Digital University Kerala  v2.0  2026"); r.font.size = Pt(12); r.font.color.rgb = MUTED
    doc.add_page_break()

    # Table of contents (manual, simple)
    h(doc, "Contents", level=1)
    bullets(doc, [
        "1. Introduction",
        "2. Architecture",
        "3. Installation",
        "4. Getting Started",
        "5. Interactive Chat and Meta-Commands",
        "6. Tool Catalogue (125 tools)",
        "7. Example Workflows",
        "8. Public API Reference",
        "9. Configuration",
        "10. Error Handling and Recovery",
        "11. Troubleshooting",
        "12. Roadmap",
    ])
    doc.add_page_break()

    # 1. Introduction
    h(doc, "1. Introduction", level=1)
    para(doc, "GeoSI is a conversational geospatial AI system. Users type plain-English questions; GeoSI plans and runs multi-step GIS workflows across 125 tools on the layers already loaded in QGIS. It is designed for analysts, planners, researchers, and domain experts who want spatial intelligence without menu archaeology or scripting.")
    para(doc, "GeoSI is built around three clean surfaces: a universal engine with zero framework imports, a QGIS plugin that hosts the chat dock, and an optional FastAPI server. Ollama is the default local LLM, making GeoSI fully offline-capable.")

    # 2. Architecture
    h(doc, "2. Architecture", level=1)
    h(doc, "2.1 Three-Surface Model", level=2)
    bullets(doc, [
        "geosi_engine/  universal core. No QGIS, no Qt, no GDAL imports.",
        "geosi_plugin/  the only code that imports qgis. Reads the Layers panel, dispatches through QGIS Processing.",
        "geosi_server/  optional FastAPI REST surface. OSM auto-fetch fallback when a layer is missing and the name is recognisable.",
    ])
    h(doc, "2.2 Backend Dispatch Pattern", level=2)
    para(doc, "BackendTool is the universal spec-carrying class used by most tools. It never imports QGIS. Execution is delegated to a backend installed at runtime via register_backend(name, fn). The plugin installs the 'qgis' backend at startup; the engine alone returns a clear error message telling the user the tool requires QGIS.")
    h(doc, "2.3 Data Flow", level=2)
    bullets(doc, [
        "User types a query in the chat dock.",
        "Plugin syncs QGIS Layers panel into engine state.",
        "Parser produces an AnalysisRequest (Ollama-first, rule-based fallback).",
        "Agent validates that referenced layers exist; returns a clear error if not.",
        "Agent produces an ExecutionPlan (multi-step, explainable).",
        "Executor runs each ToolStep; BackendTool dispatches to QGIS Processing.",
        "Dock renders answer, reasoning, and layer suggestions.",
    ])

    # 3. Installation
    h(doc, "3. Installation", level=1)
    h(doc, "3.1 Ollama (recommended)", level=2)
    code(doc, "curl -fsSL https://ollama.com/install.sh | sh\nollama pull mistral\nollama serve")
    h(doc, "3.2 QGIS plugin", level=2)
    para(doc, "Copy the geosi_plugin/ and geosi_engine/ folders into your QGIS plugin directory:")
    bullets(doc, [
        "Linux: ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/",
        "macOS: ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/",
        "Windows: %APPDATA%\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\",
    ])
    para(doc, "Restart QGIS and enable 'GeoSI  AI Agent' under Plugins  Manage and Install Plugins.")

    # 4. Getting Started
    h(doc, "4. Getting Started", level=1)
    para(doc, "Load a vector or raster layer into QGIS. Open the GeoSI dock from the toolbar. Click the LLM button, confirm the Ollama endpoint and model, press Test Ollama, then Save and Reload.")
    para(doc, "Type a question in plain English:")
    code(doc, "You: Buffer Schools by 500 meters\nYou: Intersect that with Kerala\nYou: Export result as GeoJSON")

    # 5. Interactive chat
    h(doc, "5. Interactive Chat and Meta-Commands", level=1)
    bullets(doc, [
        "help  example prompts tailored to your loaded layers.",
        "layers  lists loaded layers with type, geometry, feature count, CRS.",
        "tools  shows how many tools are available per category.",
        "clear / cls  clears the chat log.",
    ])

    # 6. Tool catalogue
    h(doc, "6. Tool Catalogue (125 tools)", level=1)
    table = doc.add_table(rows=1, cols=2); table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    hdr[0].text = "Category"; hdr[1].text = "Highlights"
    rows = [
        ("Vector (40)", "buffer, intersect, clip, dissolve, voronoi, delaunay, centroid, convex_hull, concave_hull, spatial_join, nearest_join, reproject, fix_geometries"),
        ("Raster (25)", "raster_calc, ndvi, ndwi, ndbi, evi, zonal_stats, reclassify, mask, resample, mosaic, clip_raster, focal_mean"),
        ("Terrain (10)", "slope, aspect, hillshade, contour, viewshed, watershed, flow_direction, flow_accumulation, TRI, TPI"),
        ("Network (8)", "shortest_path, service_area, isochrone, od_matrix, catchment_area"),
        ("Temporal (6)", "temporal_filter, change_detection, time_series_aggregate"),
        ("AI/ML (10)", "kmeans_cluster, dbscan, getis_ord_gi, moran_i, idw, kriging, anomaly_detect"),
        ("Cartography (10)", "export_geojson, export_shapefile, export_kml, geocode, reverse_geocode"),
        ("Validation (10)", "fix_geometries, check_validity, topology_check, duplicate_features, null_geometry, crs_consistency"),
        ("Portable (2)", "count_features, load_spatial_data  work without QGIS"),
    ]
    for cat, hi in rows:
        r = table.add_row().cells
        r[0].text = cat; r[1].text = hi

    # 7. Workflows
    h(doc, "7. Example Workflows", level=1)
    h(doc, "7.1 Buffer and Intersect", level=2)
    code(doc, "You: Find residential zones within 500m of hospitals\n\nplan: buffer(hospitals, 500)  intersect(prev, residential)")
    h(doc, "7.2 NDVI", level=2)
    code(doc, "You: Calculate NDVI from Sentinel2_red and Sentinel2_NIR")
    h(doc, "7.3 Clustering", level=2)
    code(doc, "You: Cluster Schools using DBSCAN with eps=500")

    # 8. API
    h(doc, "8. Public API Reference", level=1)
    h(doc, "8.1 Facade", level=2)
    code(doc, "from geosi_engine import GeoSI\nengine = GeoSI()\nresult = engine.query('Buffer Schools by 500m')\n# result['success'], result['answer'], result['plan'], result['reasoning']")
    h(doc, "8.2 Tool Registry", level=2)
    code(doc, "engine.registry.list_tools(category='vector')\nengine.registry.execute_tool('buffer', INPUT='Schools', DISTANCE=500)")
    h(doc, "8.3 Parser / Agent / Executor", level=2)
    code(doc, "request = engine.agent.parse('Buffer Schools by 500m', engine.state)\nplan    = engine.agent.plan(request, engine.state)\nresult  = engine.executor.run(plan)")
    h(doc, "8.4 State Management", level=2)
    code(doc, "from geosi_engine.models import Layer\nengine.state.add_layer(Layer(name='Schools', layer_type='vector', ...))\nengine.state.list_layers()\nengine.state.checkpoint('before_buffer')")
    h(doc, "8.5 Backend Registration (Plugin Only)", level=2)
    code(doc, "from geosi_engine.base import register_backend\nregister_backend('qgis', lambda step: processing.run(step.algorithm, step.parameters))")

    # 9. Configuration
    h(doc, "9. Configuration", level=1)
    table = doc.add_table(rows=1, cols=3); table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    hdr[0].text = "Key"; hdr[1].text = "Default"; hdr[2].text = "Stored In"
    cfg = [
        ("OLLAMA_ENDPOINT", "http://localhost:11434", "QgsSettings GeoSI/ollama_endpoint"),
        ("OLLAMA_MODEL", "mistral", "QgsSettings GeoSI/ollama_model"),
        ("GEMINI_API_KEY", "", "Environment variable"),
        ("ANTHROPIC_API_KEY", "", "QgsSettings GeoSI/anthropic_api_key"),
        ("OPENAI_API_KEY", "", "Environment variable"),
    ]
    for k, v, s in cfg:
        r = table.add_row().cells
        r[0].text = k; r[1].text = v; r[2].text = s

    # 10. Error handling
    h(doc, "10. Error Handling and Recovery", level=1)
    bullets(doc, [
        "Parser  Ollama offline: 1.5s probe fails, falls through to next provider.",
        "Parser  bad JSON: tolerant extraction then keyword fallback.",
        "Agent  layer missing: empty plan with 'Layer not found' message and fuzzy suggestions.",
        "Executor  tool raises: log error, continue with next step, return partial result.",
        "Backend  QGIS unavailable: tool returns ToolResult(success=False) with a clear message.",
    ])

    # 11. Troubleshooting
    h(doc, "11. Troubleshooting", level=1)
    table = doc.add_table(rows=1, cols=2); table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    hdr[0].text = "Symptom"; hdr[1].text = "Fix"
    ts = [
        ("Layer 'X' not found", "Load the layer into the QGIS Layers panel, then retry."),
        ("Ollama not reachable", "Run `ollama serve`, or click LLM  Test Ollama in the dock."),
        ("No tools loaded", "Engine init failed  check the QGIS Python console traceback."),
        ("Slow first query", "Ollama warms up the model on first call; subsequent queries are fast."),
        ("Wrong tool picked", "Use a more specific phrasing, or type `tools` to see categories."),
    ]
    for sym, fix in ts:
        r = table.add_row().cells
        r[0].text = sym; r[1].text = fix

    # 12. Roadmap
    h(doc, "12. Roadmap", level=1)
    bullets(doc, [
        "v1.0  Core engine, 80 tools, basic plugin. (done)",
        "v2.0  Ollama-first, 125 tools, universal engine, validation, conversation memory. (done)",
        "v2.5  GeoPandas backend for server, batch mode, notebook integration.",
        "v3.0  Real-time satellite stream monitoring, 3D viewshed, XR visualisation.",
        "v4.0  Predictive spatial modelling, autonomous decision support.",
    ])

    # Close
    para(doc, "")
    para(doc, "GeoSI is an open-vision project: the beginning of geospatial superintelligence built for the domain.", color=MUTED, italic=True)
    para(doc, " 2026 GeoSI Project  Aaron R  Digital University Kerala.", color=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
