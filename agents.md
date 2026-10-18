# GeoSI Agent Roster & Interaction Guide

The GeoSI platform is powered by 14 specialized Python modules located in `geosi_engine/agents/`. This document outlines what they are and how you can communicate with them.

## The 14 Agents

### Orchestration & Routing
1. **`supervisor.py`**: The Orchestrator. Manages the overall conversation state and delegates tasks.
2. **`permission_safety.py`**: The Guardrail. Blocks prompt injections and malicious inputs.
3. **`reflection.py`**: The Intent Router & Error Interpreter. Classifies requests and debugs Python execution errors dynamically.
4. **`research.py`**: The GraphRAG Agent & Data Crawler. Pulls technical documentation from Qdrant/Neo4j and fetches external WFS/WMS datasets.

### Planning & Execution
5. **`planning.py`**: The Architect. Drafts exact, deterministic `ToolSteps` (e.g., Run `native:buffer`).
6. **`validation.py`**: The Static Analyzer. Reviews the Planner's output to catch missing parameters *before* execution.
7. **`workflow_optimization.py`**: The Tool Selector. Chooses the most mathematically efficient PyQGIS/GDAL tool for the job.
8. **`code_generation.py`**: The Executor. Headlessly executes the planned PyQGIS/GDAL code.

### Verification & Output
9. **`verification.py`**: The QA Inspector. Reads output file headers to verify Coordinate Reference Systems (CRS) and geometric validity.
10. **`report_generation.py`**: The Reporter. Synthesizes execution logs and spatial metrics into a human-readable final summary.

### Specialized Domain Agents
11. **`gis_agent.py`**: The core foundational agent containing base spatial analysis logic.
12. **`remote_sensing.py`**: Handles satellite imagery, NDVI calculation, and raster math.
13. **`geology.py`**: Handles terrain modeling, DEMs, and surface analysis.
14. **`machine_learning.py`**: Handles spatial clustering, predictive modeling, and random forest classification on geographic data.

---

## How to Talk to the Agents

There are two primary ways to interact with the Agentic Engine from your workspace.

### 1. Via the REST API (Fully Local, Ollama)
If you are running the FastAPI backend with local models (e.g., Llama 3 via Ollama), you can send direct natural language POST requests. The Supervisor will automatically parse the intent and invoke the pipeline.

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Buffer the hospitals layer by 5 miles and find intersecting flood zones."}'
```

### 2. Via MCP (Model Context Protocol)
If you want to use **Claude Desktop** as the UI, you can connect it to the GeoSI MCP server. Claude will act as the master intelligence, invoking GeoSI's agents as "Tools".

**In your `claude_desktop_config.json`:**
```json
{
  "mcpServers": {
    "geosi": {
      "command": "fastmcp",
      "args": ["run", "/Users/aaronr/Desktop/GEOSI/geosi_mcp/server.py"]
    }
  }
}
```

Once connected, you can simply type in the Claude Desktop app:
> *"Use GeoSI to calculate the NDVI for the Sentinel-2 imagery in my downloads folder and generate a report."*

Claude will trigger the MCP server, which routes the command into our `remote_sensing.py` and `report_generation.py` agents!
