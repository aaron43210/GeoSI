# GeoSI v2 — Complete Project Reference
### Your Autonomous Geospatial Intelligence Platform — Everything You Need to Know

---

## Table of Contents
1. [What Is GeoSI v2?](#1-what-is-geosi-v2)
2. [What GeoSI Can Do Right Now](#2-what-geosi-can-do-right-now)
3. [GeoSI vs QGIS vs ArcGIS — Detailed Comparison](#3-geosi-vs-qgis-vs-arcgis)
4. [How to Deploy as a Fully Agentic App](#4-how-to-deploy-as-a-fully-agentic-app)
5. [Manual Requirements — What YOU Need to Do](#5-manual-requirements--what-you-need-to-do)
6. [Complete Directory Reference — Every File Explained](#6-complete-directory-reference)
7. [Debugging Guide](#7-debugging-guide)
8. [Environment Variables Reference](#8-environment-variables-reference)
9. [API Quick Reference](#9-api-quick-reference)

---

## 1. What Is GeoSI v2?

GeoSI v2 is an **autonomous multi-agent geospatial intelligence platform** that wraps QGIS, PostGIS, satellite data, and machine learning into a single LLM-powered system.

Instead of clicking menus in QGIS or writing Python scripts manually, you describe what you want in natural language — and GeoSI's 14-agent pipeline plans, validates, executes, and reports the result.

### Core Philosophy

```
You say:   "Buffer all hospitals by 500m and clip to Lagos boundary"

GeoSI:     ↳ SupervisorAgent   — routes query to correct agents
           ↳ PlanningAgent     — generates QGIS tool workflow
           ↳ ValidationAgent   — checks CRS, layer names, tool IDs
           ↳ ReflectionAgent   — scores plan quality (0-10)
           ↳ PermissionSafety  — HITL gate for destructive ops
           ↳ GISExecutionAgent — runs native:buffer + native:clip
           ↳ VerificationAgent — checks output is valid
           ↳ ReportGenAgent    — returns result + explanation
```

> **Nothing executes without human approval for mutating/destructive operations.** This is a hard architectural invariant enforced in every pipeline path.

---

## 2. What GeoSI Can Do Right Now

### GIS Operations (via 500+ QGIS Processing tools)

| Category | Operations |
|---|---|
| **Vector** | Buffer, clip, intersect, union, dissolve, spatial join, centroid, merge, split, snap, simplify, voronoi, convex hull |
| **Raster** | Slope, aspect, hillshade, zonal stats, proximity, raster calc, clip by mask, mosaic, polygonize |
| **Hydrology** | Flow direction, flow accumulation, watershed, fill sinks, stream extraction |
| **Topology** | Fix geometries, delete duplicates, check validity, sliver removal |
| **Network** | Shortest path, service area |
| **Sampling** | Random points, stratified sampling, fishnet grid, raster value extraction |
| **Field** | Area, perimeter, length, coordinate fields, custom QGIS expressions |
| **Reprojection** | Any CRS ↔ CRS via EPSG codes (native:reprojectlayer) |

### Remote Sensing

| Capability | Details |
|---|---|
| **Spectral indices** | NDVI, EVI, NDWI, NDBI, SAVI, NBR, LST, SAVI, dNBR |
| **Atmospheric correction** | DOS1 guidance, Sen2Cor workflow |
| **Change detection** | Image differencing, log-ratio, dNBR pre/post fire |
| **SAR** | Backscatter, coherence, InSAR concepts |
| **Classification** | Random Forest, CNN on satellite imagery |
| **Supported sensors** | Sentinel-2, Landsat-8/9, ASTER, MODIS |

### Machine Learning

| Capability | Details |
|---|---|
| **Classification** | Random Forest, Gradient Boosting, SVM for land cover |
| **Clustering** | K-Means, DBSCAN spatial clustering |
| **Regression** | Spatial regression, feature importance, Kriging concepts |
| **Evaluation** | Confusion matrix, Kappa, F1, RMSE, spatial cross-validation |
| **Model storage** | joblib serialisation, model registry in PostGIS |

### Geology

| Capability | Details |
|---|---|
| **Structural** | Fold analysis, fault mapping, lineament detection from DEM |
| **Stratigraphy** | Borehole correlation, cross-section generation |
| **Prospectivity** | Weights-of-evidence, multi-criteria scoring |
| **Susceptibility** | Landslide mapping (slope × aspect × lithology × proximity) |
| **Remote sensing** | Lithological mapping from Sentinel-2 SWIR/NIR ratios |

### Knowledge & Research

| Capability | Details |
|---|---|
| **Semantic search** | Qdrant vector DB with HNSW index (O(log N)) |
| **Hybrid RAG** | BM25 + dense vector + RRF fusion |
| **GraphRAG** | Neo4j graph + Qdrant → cross-referenced results (P10) |
| **Literature review** | 150-query golden set across 6 agent scopes |
| **Citation** | Auto-formatted references from retrieved documents |

### Security & Observability

| Capability | Details |
|---|---|
| **API Key auth** | Bearer token, constant-time HMAC comparison |
| **Permission tiers** | read / write / admin enforcement |
| **HITL approval** | Destructive ops require `approve_pending_action` |
| **Guardrails** | Code injection blocked, `requires_human_review=True` enforced |
| **Audit log** | Every action → `geosi_audit_log` in PostGIS |
| **OpenTelemetry** | Distributed traces on every agent handoff |
| **RAGAS gating** | Faithfulness ≥ 0.85 · Context Precision ≥ 0.75 |

---

## 3. GeoSI vs QGIS vs ArcGIS

### Full Feature Matrix

| Feature | GeoSI v2 | QGIS 3.x | ArcGIS Pro |
|---|:---:|:---:|:---:|
| **Natural language interface** | ✅ Full | ❌ | ❌ |
| **Autonomous workflow planning** | ✅ 14-agent | ❌ Manual | ⚠️ ModelBuilder |
| **LLM-powered analysis** | ✅ Gemini/Ollama/Claude | ❌ | ✅ Esri AI (paid) |
| **Free & open source** | ✅ Yes | ✅ Yes | ❌ $3,600+/yr |
| **QGIS processing (500+ tools)** | ✅ All | ✅ All | ❌ Esri only |
| **GDAL / GRASS / SAGA** | ✅ Via QGIS | ✅ Full | ❌ |
| **Python auto-generation** | ✅ CodeGenAgent | ✅ Manual | ✅ ArcPy (manual) |
| **PostGIS native integration** | ✅ Built-in | ⚠️ Plugin | ⚠️ Connector |
| **Neo4j knowledge graph** | ✅ Built-in | ❌ | ❌ |
| **RAG / semantic search** | ✅ Qdrant | ❌ | ❌ |
| **REST API** | ✅ FastAPI | ❌ | ✅ ArcGIS Server |
| **MCP (Claude/Cursor)** | ✅ 6 tools | ❌ | ❌ |
| **Docker / K8s deploy** | ✅ Full | ❌ | ❌ SaaS |
| **CI/CD pipeline** | ✅ GitHub Actions | ❌ | ❌ |
| **Satellite index computation** | ✅ Full | ⚠️ Manual | ✅ Raster Functions |
| **ML integration** | ✅ sklearn + joblib | ⚠️ Plugins | ✅ Deep Learning toolkit |
| **Geology / borehole** | ✅ GeologyAgent | ⚠️ Plugins | ✅ Paid add-ons |
| **Human-in-the-loop safety** | ✅ Hard enforced | ❌ | ❌ |
| **Complete audit trail** | ✅ PostGIS log | ❌ | ⚠️ Enterprise only |
| **Session memory** | ✅ Redis + PostGIS | ❌ | ❌ |
| **RAGAS evaluation gating** | ✅ Built-in | ❌ | ❌ |
| **GraphRAG cross-reference** | ✅ RRF fusion | ❌ | ❌ |

### Position Summary

```
QGIS:    Best-in-class FREE GIS desktop — but YOU do all the work manually
ArcGIS:  Enterprise power — $3,600+/user/year, closed, SaaS lock-in
GeoSI:   QGIS power + LLM autonomy + enterprise features + completely FREE
```

> **GeoSI is what QGIS would be if it had an AI brain, a REST API, autonomous agents, and an enterprise observability stack.**

### What GeoSI Cannot Do (Yet)
- ❌ **3D scene rendering** — ArcGIS Pro / QGIS 3D view are desktop-native
- ❌ **Real-time streaming** — No live sensor / IoT integration
- ❌ **StoryMaps / Dashboards** — No ArcGIS StoryMaps equivalent
- ❌ **ESRI enterprise geodatabase** (`.gdb`) — Limited support
- ❌ **Offline mobile field app** — Web/desktop only for now

---

## 4. How to Deploy as a Fully Agentic App

### Option A — Local Development (Quickest)

```bash
# 1. Install QGIS 3.34+ from qgis.org (needed for QGIS plugin only)

# 2. Set up Python environment
cd /Users/aaronr/Desktop/GEOSI
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Fill in secrets
cp .env.example .env
# Edit .env — at minimum set POSTGRES_PASSWORD, GEOSI_API_KEYS, GEMINI_API_KEY

# 4. Start backing services
docker compose up -d postgres qdrant neo4j redis

# 5. Run migrations
PYTHONPATH=. alembic upgrade head

# 6. Start the server
PYTHONPATH=. uvicorn geosi_server.app:app --reload --port 8000

# 7. Test
curl http://localhost:8000/health
```

### Option B — Full Docker Stack (Production-Ready)

```bash
cp .env.example .env        # fill in all values
docker compose up -d        # starts all 7 services

# Watch logs
docker compose logs -f geosi_server

# Test
curl http://localhost/health
```

**Services that start automatically:**

| Service | Port | Purpose |
|---|---|---|
| `geosi_server` | 8000 (internal) | FastAPI — all agents |
| `nginx` | 80, 443 | Reverse proxy, rate limiting, security headers |
| `postgres` | 5432 | PostGIS — spatial data, audit log, eval runs |
| `qdrant` | 6333, 6334 | Vector DB — semantic search |
| `neo4j` | 7474 (UI), 7687 (Bolt) | Knowledge graph |
| `redis` | 6379 | Session cache |
| `otel_collector` | 4317, 4318 | OpenTelemetry traces |

### Option C — Kubernetes (Enterprise Scale)

```bash
# 1. Create namespace + ConfigMap + HPA + PodDisruptionBudget
kubectl apply -f k8s/service.yaml

# 2. Create secrets (never in git)
kubectl create secret generic geosi-secrets \
  --from-literal=database-url='postgresql://geosi:PASS@postgres-svc:5432/geosi' \
  --from-literal=neo4j-password='YOUR_PASS' \
  --from-literal=redis-url='redis://:PASS@redis-svc:6379/0' \
  --from-literal=api-keys='key1,key2' \
  --from-literal=admin-keys='adminkey' \
  --from-literal=mcp-token='your-mcp-token' \
  -n geosi

# 3. Deploy
kubectl apply -f k8s/deployment.yaml -n geosi

# 4. Watch rollout
kubectl rollout status deployment/geosi-server -n geosi
```

Auto-scales 2 → 10 pods at CPU 70% or memory 80%. Zero-downtime rolling updates (maxUnavailable=0). PodDisruptionBudget ensures ≥1 pod always available.

### Option D — Connect Claude / Cursor via MCP

Add to your Claude Desktop config (`~/.config/claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "geosi": {
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

Then in Claude: *"Use the GeoSI MCP tools to buffer all hospitals by 500m"*

### Option E — Install QGIS Plugin

```bash
PLUGIN_DIR=~/.local/share/QGIS/QGIS3/profiles/default/python/plugins
cp -r geosi_plugin "$PLUGIN_DIR/geosi_plugin"
# QGIS → Plugins → Manage and Install Plugins → Enable "GeoSI"
# A "GeoSI" panel appears on the right side of QGIS
```

---

## 5. Manual Requirements — What YOU Need to Do

> These cannot be automated — they require your direct action.

### 🔴 CRITICAL — Must Do Before Anything Works

#### A. Fill in `.env`
```bash
cp .env.example .env
# Open .env and set these minimum required values:
```

| Variable | What to Set | Where to Get |
|---|---|---|
| `POSTGRES_PASSWORD` | A strong password | Make it up |
| `NEO4J_PASSWORD` | A strong password | Make it up |
| `REDIS_PASSWORD` | A strong password | Make it up |
| `GEOSI_API_KEYS` | Comma-separated client API keys | Make them up: `key1,key2` |
| `GEOSI_ADMIN_KEYS` | Admin API key | Make it up: `adminkey` |
| `GEOSI_ALLOWED_ORIGINS` | Your frontend URL | `http://localhost:3000` |
| `GEMINI_API_KEY` | Google Gemini key | [aistudio.google.com](https://aistudio.google.com) — FREE |

#### B. Get at Least One LLM Provider

| Provider | Cost | Setup |
|---|---|---|
| **Google Gemini** | FREE tier | [aistudio.google.com](https://aistudio.google.com) → Create API key |
| **Ollama (local)** | FREE, private | [ollama.ai](https://ollama.ai) → `ollama pull llama3.2` |
| **Anthropic Claude** | Pay-per-use | [console.anthropic.com](https://console.anthropic.com) |

#### C. Install QGIS 3.34+ (Only for the Desktop Plugin)
- Download from **[qgis.org/download](https://qgis.org/download/)**
- The FastAPI server works **without** QGIS (graceful degradation)
- QGIS is only needed if you want the in-QGIS panel

### 🟡 IMPORTANT — Needed for Full Functionality

#### D. Ingest Your Documents into the Knowledge Base
Without this, `search_gis_docs` returns nothing:

```bash
# Put your GIS reports, papers, manuals in a folder then:
PYTHONPATH=. python geosi_rag/ingest_cli.py \
  --source /path/to/your/documents \
  --collection gis_docs \
  --chunk-size 512
# Supported: PDF, TXT, DOCX, MD, CSV
```

#### E. Run Database Migrations
```bash
# After PostgreSQL is running:
PYTHONPATH=. alembic upgrade head
# Creates: geosi_audit_log, geosi_eval_runs, geosi_sessions, geosi_layers, etc.
```

#### F. Create Qdrant Collections (if not auto-created)
```bash
curl -X PUT http://localhost:6333/collections/gis_docs \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 768, "distance": "Cosine"}}'

curl -X PUT http://localhost:6333/collections/research_papers \
  -H "Content-Type: application/json" \
  -d '{"vectors": {"size": 768, "distance": "Cosine"}}'
```

### 🟢 OPTIONAL — For Production

#### G. Create `otel-config.yaml` (needed by docker-compose)
```yaml
# /Users/aaronr/Desktop/GEOSI/otel-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
exporters:
  logging:
    loglevel: info
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [logging]
```

#### H. Set Up SSL / HTTPS
In `nginx.conf`, uncomment and fill:
```nginx
listen 443 ssl;
ssl_certificate     /etc/nginx/certs/fullchain.pem;
ssl_certificate_key /etc/nginx/certs/privkey.pem;
```
Get a free cert: `certbot --nginx -d yourdomain.com`

#### I. GitHub Secrets for CI/CD
In your GitHub repo → Settings → Secrets → Actions:
- `CODECOV_TOKEN` — from [codecov.io](https://codecov.io)
- `OPENAI_API_KEY` or `GOOGLE_API_KEY` — for RAGAS LLM eval in CI

---

## 6. Complete Directory Reference

Every file in the project with what it does and when to look at it.

```
/Users/aaronr/Desktop/GEOSI/
│
├── .env.example            ← COPY to .env, fill in all secrets — START HERE
├── pyproject.toml          ← Python project config, pytest settings, ruff/mypy config
├── requirements.txt        ← Runtime Python dependencies
├── alembic.ini             ← DB migration config (points to DATABASE_URL)
├── nginx.conf              ← Reverse proxy: rate limiting, security headers, CORS
├── docker-compose.yml      ← Full 7-service stack (all services defined here)
├── Dockerfile.server       ← Multi-stage FastAPI image (builder + non-root runtime)
├── prd1.md                 ← SOURCE OF TRUTH — ALL requirements, ALWAYS read this
├── AUDIT.md                ← Phase completion audit log
├── Connections.md          ← Service integration diagram
│
├── .github/workflows/
│   └── ci.yml              ← 7-stage GitHub Actions CI/CD pipeline
│                              Stages: lint → typecheck → unit tests → RAGAS gate
│                                     → bandit security → Docker build → integration
│
├── k8s/
│   ├── deployment.yaml     ← K8s Deployment: rolling update, init container (Alembic),
│   │                          non-root security, liveness/readiness/startup probes
│   └── service.yaml        ← Namespace + Service + ConfigMap + HPA (2-10 pods) + PDB
│
├── alembic/
│   └── versions/           ← Auto-generated migration scripts (do NOT edit manually)
│
│
├── geosi_engine/           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   │                       🧠  THE BRAIN — 14-agent AI engine
│   │                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   ├── __init__.py         ← GeoSIEngine factory, package exports
│   ├── agent.py            ← BaseAgent: OTel spans, audit logging, CB states
│   │                          ⚡ Every agent inherits from here
│   ├── base.py             ← GeoSI base config, engine init, provider selection
│   ├── models.py           ← ALL Pydantic v2 schemas:
│   │                          ExecutionPlan, ToolStep, SupervisorRequest,
│   │                          AgentResponse, PermissionTier, RiskLevel
│   │                          ⚡ Change data shapes here
│   ├── executor.py         ← QGIS tool execution dispatcher
│   │                          ⚡ Debug here when tools fail to run
│   ├── parser.py           ← NL query → structured ExecutionPlan (LLM call)
│   │                          ⚡ Debug here when wrong tools are selected
│   ├── guardrails.py       ← Safety scanning: blocks code injection, detects PII
│   │                          ⚡ Debug here when content is flagged unexpectedly
│   ├── validation.py       ← Plan completeness + CRS + layer name validation
│   ├── registry.py         ← QGIS tool registry (500+ tools, O(1) dict lookup)
│   │                          ⚡ Add new QGIS tools here
│   ├── conversation.py     ← Conversation state: history, context window mgmt
│   ├── session_pool.py     ← Thread-safe per-session engine pool (max 50 sessions)
│   │                          ⚡ Debug OOM / session leak issues here
│   ├── state.py            ← GeoSI session state: layers, last plan, history
│   ├── telemetry.py        ← OTel @span decorator + OTel SDK init
│   │                          ⚡ Add new trace spans here
│   ├── graph_rag.py        ← GraphRAG: Qdrant vector + Neo4j graph → RRF fusion
│   │                          Time O(k log k) · Space O(k)
│   │                          ⚡ Debug knowledge cross-reference issues here
│   ├── graph_writer.py     ← Background Neo4j writer: bounded O(1000) deque queue,
│   │                          daemon thread, fire-and-forget from agent pipeline
│   │                          ⚡ Debug graph write failures here
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── ragas_runner.py ← RAGAS eval: streaming O(B) memory, parallel batches,
│   │                          faithfulness ≥ 0.85, context_precision ≥ 0.75 gate
│   │                          ⚡ Debug CI eval gate failures here
│   │
│   └── agents/             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│       │                   🤖  ALL 14 AGENTS
│       │                   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│       ├── __init__.py     ← Exports all 14 agents
│       │
│       ├── supervisor.py   ← 🎯 SupervisorAgent
│       │                      Orchestrator — routes ALL queries to sub-agents
│       │                      Has circuit breakers for each sub-agent
│       │                      ⚡ Start here for ANY pipeline routing issue
│       │
│       ├── planning.py     ← 📋 PlanningAgent
│       │                      NL → ExecutionPlan with ToolSteps + risk levels
│       │                      Uses LLM + QGIS tool registry
│       │                      ⚡ Debug wrong tool selections here
│       │
│       ├── validation.py   ← ✅ ValidationAgent
│       │                      Validates plan: CRS consistency, layer availability,
│       │                      tool ID existence, parameter completeness
│       │                      ⚡ Debug unexpected plan rejections here
│       │
│       ├── reflection.py   ← 🪞 ReflectionAgent
│       │                      Scores plan quality 0–10, suggests improvements
│       │                      ⚡ Debug quality scoring issues here
│       │
│       ├── permission_safety.py ← 🔐 PermissionSafetyAgent
│       │                          Hard HITL gate for destructive operations
│       │                          Risk scoring, permission tier enforcement
│       │                          Approval store for pending actions
│       │                          ⚡ Debug unexpected blocks / approval flow here
│       │
│       ├── gis_agent.py    ← 🗺️ GISExecutionAgent
│       │                      Executes QGIS processing tools (all native/gdal/grass)
│       │                      Reads/writes PostGIS layers
│       │                      ⚡ Debug QGIS tool failures here
│       │
│       ├── remote_sensing.py ← 🛰️ RemoteSensingAgent
│       │                       Satellite indices (NDVI/EVI/NDWI/NBR/LST)
│       │                       Atmospheric correction, change detection, SAR
│       │                       ⚡ Debug index computation / band math here
│       │
│       ├── machine_learning.py ← 🤖 MLAgent
│       │                         Train/predict/evaluate sklearn models
│       │                         K-Means, DBSCAN, Random Forest, GBM
│       │                         ⚡ Debug spatial ML failures here
│       │
│       ├── geology.py      ← 🪨 GeologyAgent
│       │                      Structural geology, stratigraphy, borehole,
│       │                      landslide susceptibility, mineral prospectivity
│       │                      ⚡ Debug geology analysis failures here
│       │
│       ├── verification.py ← 🔍 VerificationAgent
│       │                      Post-execution output validation:
│       │                      geometry validity, feature count, CRS match
│       │                      ⚡ Debug outputs that pass but are wrong
│       │
│       ├── report_generation.py ← 📄 ReportGenAgent
│       │                          Generates Markdown / HTML / PDF reports
│       │                          from execution results
│       │                          ⚡ Debug malformed / empty reports here
│       │
│       ├── research.py     ← 🔬 ResearchAgent
│       │                      Qdrant RAG search + GraphRAG graph_search()
│       │                      Literature review, citation formatting
│       │                      ⚡ Debug knowledge retrieval failures here
│       │
│       ├── workflow_optimization.py ← ⚡ WorkflowOptAgent
│       │                              Performance analysis, step reordering,
│       │                              parallel execution suggestions
│       │                              ⚡ Debug optimisation suggestions here
│       │
│       └── code_generation.py ← 💻 CodeGenAgent
│                                  Generates QGIS Python PyQGIS snippets
│                                  All output has requires_human_review=True
│                                  ⚡ Debug syntax errors in generated code


├── geosi_server/           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   │                       🌐  FastAPI REST API
│   │                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   ├── app.py              ← Main FastAPI app: lifespan, router registration,
│   │                          Neo4j schema bootstrap, graph writer startup
│   │                          ⚡ Start here for HTTP 500 / startup failures
│   ├── auth.py             ← API key auth dependency + admin key check
│   │                          ⚡ 401/403 errors → check this + .env keys
│   ├── chat_routes.py      ← POST /chat, POST /execute, GET+POST /approval/*
│   │                          ⚡ Chat flow + HITL approval flow
│   ├── rag_routes.py       ← GET /rag/search, GET /rag/collections
│   │                          ⚡ Knowledge search endpoint failures
│   ├── workflow_routes.py  ← POST /workflow/plan, GET /workflow/history
│   │                          ⚡ Planning endpoint issues
│   ├── data_routes.py      ← GET /layers, POST /layers/upload
│   │                          ⚡ Layer listing / file upload failures
│   └── admin_routes.py     ← POST /admin/policy, GET /admin/audit
│                              ⚡ Admin policy / audit log issues


├── geosi_mcp/              ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   │                       🔌  MCP Server — Claude/Cursor integration
│   │                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   ├── __init__.py
│   ├── auth.py             ← HMAC constant-time bearer token (timing-attack safe)
│   │                          ⚡ MCP 401 errors → check GEOSI_MCP_TOKEN
│   └── server.py           ← 6 FR-5.1 JSON-RPC 2.0 tools
│                              Mounted at /mcp by app.py
│                              ⚡ GET /mcp/manifest to verify tools are registered


├── geosi_data/             ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   │                       🗄️  Data Layer — PostGIS + Neo4j
│   │                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   ├── database.py         ← SQLAlchemy engine + session factory
│   │                          ⚡ DB connection failures start here
│   ├── db_models.py        ← All SQLAlchemy ORM table models
│   │                          geosi_audit_log, geosi_eval_runs, geosi_sessions…
│   │                          ⚡ Schema mismatch → run alembic upgrade head
│   ├── postgis_manager.py  ← PostGIS spatial operations (ST_Buffer, ST_Intersects…)
│   │                          ⚡ Spatial query failures
│   ├── layer_repository.py ← Layer CRUD: create, read, update, delete
│   ├── metadata_repository.py ← Document/dataset metadata storage
│   ├── project_repository.py  ← Project management CRUD
│   ├── graph_schema.py     ← Neo4j node/rel type constants + property builders
│   │                          NodeLabel, RelType, build_dataset_props()…
│   └── neo4j_client.py     ← Neo4j driver: pool, circuit breaker, O(1) node lookup
│                              ⚡ Check .circuit_state() → should be "CLOSED"


├── geosi_rag/              ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   │                       📚  RAG Ingestion & Retrieval Pipeline
│   │                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   ├── document_loader.py  ← PDF / DOCX / TXT / MD / CSV loader
│   │                          ⚡ Document load failures
│   ├── chunker.py          ← Semantic + sliding-window text chunking
│   ├── embedding_service.py ← sentence-transformers embedding generation
│   │                           ⚡ Embedding failures → model not downloaded
│   ├── qdrant_store.py     ← Qdrant collection management + upsert
│   │                          ⚡ Vector DB write failures
│   ├── retriever.py        ← Hybrid BM25 + dense retrieval + RRF fusion
│   ├── reranker.py         ← Cross-encoder reranking (optional)
│   ├── rag_service.py      ← End-to-end RAG orchestration
│   └── ingest_cli.py       ← CLI: `python geosi_rag/ingest_cli.py --source ...`


├── geosi_knowledge/        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   │                       🧠  Memory & Built-in Knowledge
│   │                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   ├── knowledge_manager.py ← Central knowledge access (search, ingest, stats)
│   │                           ⚡ Knowledge retrieval failures start here
│   ├── feedback_memory.py   ← User feedback storage + retrieval
│   ├── query_memory.py      ← Per-session query history
│   ├── workflow_memory.py   ← Successful workflow templates
│   └── builtin_workflows.py ← 50+ pre-built QGIS workflow examples
│                               (buffer, clip, NDVI, watershed, etc.)


├── geosi_plugin/           ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   │                       🖥️  QGIS Desktop Plugin
│   │                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│   ├── __init__.py         ← QGIS classFactory — plugin entry point
│   ├── geosi_plugin.py     ← Plugin init / cleanup / menu registration
│   ├── prompt_dock.py      ← The GeoSI dockable panel UI inside QGIS
│   │                          ⚡ QGIS UI issues (layout, signals, slots)
│   └── qgis_bridge.py      ← Bridge: GeoSI engine ↔ QGIS Python API
│                              Uses: QgsProject, QgsVectorLayer, QgsRasterLayer,
│                                    QgsProcessing, QgsApplication
│                              ⚡ QGIS API failures / layer access issues


└── tests/                  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    │                       🧪  Test Suite — 95 tests, 0 failures
    │                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ├── conftest.py          ← Shared fixtures, env isolation (dev mode forced)
    ├── golden_set.py        ← 150-query evaluation dataset (6 scopes)
    ├── test_phase1_core.py  ← Core engine + BaseAgent tests
    ├── test_phase1_gaps.py  ← Edge cases + boundary conditions
    ├── test_agents_p5_p8.py ← All 14 agents: permission, planning, ML, geology…
    ├── test_evaluation.py   ← P2: RAGAS runner + golden set integrity (12 tests)
    ├── test_mcp.py          ← P4: MCP auth, tools, dispatch, FR-5.2 (13 tests)
    ├── test_neo4j.py        ← P9: Neo4j client, circuit breaker, graph writer (15 tests)
    └── test_graph_rag.py    ← P10: GraphRAG, RRF fusion, Research agent (12 tests)
```

---

## 7. Debugging Guide

### The Golden Rule — Always Check in This Order

```
1. GET /health              → Which services are up/down?
2. docker compose logs      → What errors appear in server logs?
3. geosi_audit_log          → What did the agents actually do?
4. pytest tests/            → Do all 95 tests still pass?
5. GET /mcp/manifest        → Are MCP tools still registered?
```

### Problem → File Map

| Symptom | First File | Debug Command |
|---|---|---|
| Server won't start | `geosi_server/app.py` | `uvicorn geosi_server.app:app --reload` |
| 401 Unauthorized | `geosi_server/auth.py` | Check `GEOSI_API_KEYS` in `.env` |
| Wrong plan generated | `geosi_engine/agents/planning.py` | Add `print()` in `plan()` |
| Plan rejected | `geosi_engine/agents/validation.py` | Check `validate()` error message |
| HITL never triggers | `geosi_engine/agents/permission_safety.py` | Check `risk_level` on ToolStep |
| QGIS tool fails | `geosi_engine/executor.py` | Verify `tool_name` is valid alg ID |
| Knowledge returns empty | `geosi_knowledge/knowledge_manager.py` | Did you ingest documents? |
| Qdrant error | `geosi_rag/qdrant_store.py` | `curl localhost:6333/collections` |
| Neo4j error | `geosi_data/neo4j_client.py` | Check `.circuit_state()` |
| MCP tools missing | `geosi_mcp/server.py` | `GET /mcp/manifest` |
| DB schema mismatch | `geosi_data/db_models.py` | `alembic upgrade head` |
| Report empty | `geosi_engine/agents/report_generation.py` | Check result object |
| RAGAS gate failing | `geosi_engine/evaluation/ragas_runner.py` | Check mean_faithfulness score |

### Diagnostic Commands

```bash
# Full system health
curl http://localhost:8000/health | python -m json.tool

# Neo4j circuit breaker state
python -c "
from geosi_data.neo4j_client import get_neo4j_client
c = get_neo4j_client()
print('Available:', c.available, '| State:', c.circuit_state())
"

# Run 10-query evaluation (no LLM needed)
python -c "
import sys; sys.path.insert(0,'tests')
from golden_set import load_golden_set
from geosi_engine.evaluation.ragas_runner import RAGASRunner
runner = RAGASRunner(engine=None)
s = runner.run(load_golden_set('gis')[:10])
print(f'Faithfulness:      {s.mean_faithfulness:.3f}  (need ≥ 0.85)')
print(f'Context Precision: {s.mean_context_precision:.3f}  (need ≥ 0.75)')
print(f'Gate: {\"PASS\" if s.gate_passed else \"FAIL (heuristic mode)\"}')
"

# View latest audit log entries
docker exec -it geosi_postgres psql -U geosi -d geosi -c \
  "SELECT agent_name, action_type, risk_level, status, created_at
   FROM geosi_audit_log ORDER BY created_at DESC LIMIT 10;"

# Check Qdrant collections
curl http://localhost:6333/collections

# Test MCP tools
curl http://localhost:8000/mcp/manifest | python -m json.tool

# Full test suite
source venv/bin/activate
PYTHONPATH=. pytest tests/ -v --tb=short

# Test with coverage
PYTHONPATH=. pytest tests/ --cov=geosi_engine --cov=geosi_server \
  --cov-report=term-missing -q
```

### Common Errors and Fixes

| Error Message | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'qgis'` | QGIS not installed | Install QGIS; set `QGIS_PREFIX_PATH` |
| `ConnectionRefusedError [Errno 61] PostgreSQL` | DB not running | `docker compose up -d postgres` |
| `qdrant_client.http.exceptions.UnexpectedResponse 404` | Collection missing | Run ingest CLI or create collection |
| `RuntimeError: GEOSI_ALLOWED_ORIGINS is required` | Production mode, no origins set | Set `GEOSI_ALLOWED_ORIGINS` in `.env` |
| `neo4j.exceptions.ServiceUnavailable` | Neo4j not reachable | System degrades gracefully; check docker |
| `alembic.exc.CommandError: Can't locate revision` | Migrations out of sync | `alembic stamp head` then `alembic upgrade head` |
| `Task requires_human_review=True blocked` | HITL gate triggered (expected) | Call `POST /approval/{action_id}` to approve |
| `HTTPException 401 Invalid MCP token` | Wrong `GEOSI_MCP_TOKEN` | Match token in `.env` and client config |
| `ragas.metrics import deprecated` | Old ragas version | Fixed: uses `ragas.metrics.collections` |
| `TypeError: BaseModel positional args` | Pydantic v2 breaking change | Fixed: all models use kwargs |

---

## 8. Environment Variables Reference

```bash
# ── REQUIRED ────────────────────────────────────────────────────────
POSTGRES_DB=geosi
POSTGRES_USER=geosi
POSTGRES_PASSWORD=          # MUST SET — strong password
NEO4J_USER=neo4j
NEO4J_PASSWORD=             # MUST SET — strong password
REDIS_PASSWORD=             # MUST SET — strong password
GEOSI_API_KEYS=key1,key2    # MUST SET — comma-separated client keys
GEOSI_ADMIN_KEYS=adminkey   # MUST SET — must also appear in GEOSI_API_KEYS
GEOSI_ALLOWED_ORIGINS=http://localhost:3000   # MUST SET in production

# ── LLM (pick at least one) ─────────────────────────────────────────
GEMINI_API_KEY=             # Google Gemini — free tier available
OLLAMA_BASE_URL=http://localhost:11434   # Local Ollama
ANTHROPIC_API_KEY=          # Claude (optional)
OPENAI_API_KEY=             # GPT-4 (optional, used in RAGAS CI)

# ── SERVICES ────────────────────────────────────────────────────────
QDRANT_URL=http://localhost:6333
NEO4J_URI=bolt://localhost:7687
DATABASE_URL=postgresql://geosi:PASS@localhost:5432/geosi
REDIS_URL=redis://:PASS@localhost:6379/0

# ── MCP ─────────────────────────────────────────────────────────────
GEOSI_MCP_TOKEN=            # Bearer token for Claude/Cursor MCP access

# ── TELEMETRY ───────────────────────────────────────────────────────
GEOSI_OTEL_ENDPOINT=http://localhost:4317
GEOSI_SERVICE_NAME=geosi-server
GEOSI_ENV=development       # development | production

# ── TUNING ──────────────────────────────────────────────────────────
GEOSI_SESSION_POOL_MAX=50   # Max concurrent GeoSI sessions
GEOSI_EVAL_BATCH_SIZE=10    # RAGAS evaluation parallel batch size
NEO4J_CB_THRESHOLD=5        # Circuit breaker: failures before OPEN
NEO4J_CB_RESET_S=60         # Circuit breaker: reset window (seconds)
```

---

## 9. API Quick Reference

Base URL: `http://localhost:8000`
Auth: `X-API-Key: your_api_key` header on all endpoints except `/health`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System health + service status (public) |
| `GET` | `/stats` | Knowledge base statistics |
| `POST` | `/chat` | Natural language GIS query |
| `POST` | `/execute` | Execute an approved ExecutionPlan |
| `GET` | `/approval/pending` | List pending HITL approval requests |
| `POST` | `/approval/{id}/approve` | Approve a pending action |
| `POST` | `/approval/{id}/reject` | Reject a pending action |
| `GET` | `/rag/search?q=NDVI` | Semantic knowledge search |
| `GET` | `/rag/collections` | List Qdrant collections |
| `POST` | `/workflow/plan` | Generate a workflow plan |
| `GET` | `/workflow/history` | Recent workflow history |
| `GET` | `/layers` | List QGIS project layers |
| `POST` | `/layers/upload` | Upload a spatial file |
| `GET` | `/admin/audit` | Audit log (admin key) |
| `POST` | `/admin/policy` | Update agent policies (admin key) |
| `GET` | `/mcp/manifest` | MCP server manifest |
| `GET` | `/mcp/tools` | All 6 MCP tool definitions |
| `POST` | `/mcp/call` | Execute MCP tool (JSON-RPC 2.0) |

### Example Requests

```bash
# Natural language GIS query
curl -X POST http://localhost:8000/chat \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Buffer all hospitals by 500m and clip to Lagos boundary",
    "session_id": "session-001",
    "available_layers": ["hospitals", "lagos_boundary"]
  }'

# Semantic search
curl "http://localhost:8000/rag/search?q=NDVI+vegetation&limit=5" \
  -H "X-API-Key: your_api_key"

# MCP tool call
curl -X POST http://localhost:8000/mcp/call \
  -H "Authorization: Bearer your_mcp_token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "id": 1,
    "method": "search_gis_docs",
    "params": {"query": "watershed delineation", "limit": 5}
  }'

# Approve pending HITL action
curl -X POST "http://localhost:8000/approval/ACTION_ID/approve" \
  -H "X-API-Key: your_api_key"
```

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Surfaces                           │
│   QGIS Plugin  │  Web/API Client  │  Claude (MCP)  │  Cursor    │
└──────────────────────┬───────────────────────────────────────────┘
                       │  HTTPS
              ┌────────▼────────┐
              │   nginx (P3)    │  Rate limit · Security headers
              │   Port 80/443   │  No wildcard CORS
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  FastAPI Server │  /chat /mcp /rag /workflow /admin
              │  Port 8000      │
              └────────┬────────┘
                       │
        ┌──────────────▼─────────────────┐
        │         14-Agent Pipeline       │
        │                                 │
        │  SupervisorAgent                │
        │    ├─ PlanningAgent             │
        │    ├─ ValidationAgent           │
        │    ├─ ReflectionAgent           │
        │    ├─ PermissionSafetyAgent ←HITL│
        │    ├─ GISExecutionAgent  ←QGIS  │
        │    ├─ RemoteSensingAgent        │
        │    ├─ MLAgent                   │
        │    ├─ GeologyAgent              │
        │    ├─ VerificationAgent         │
        │    ├─ ReportGenAgent            │
        │    ├─ ResearchAgent  ←GraphRAG  │
        │    ├─ WorkflowOptAgent          │
        │    └─ CodeGenAgent              │
        └──────────────┬─────────────────┘
                       │  OTel spans on every handoff
        ┌──────────────┼─────────────────────────────┐
        │              │                              │
   PostGIS         Qdrant                      Neo4j (P9)
   (audit log,   (vector RAG,              (graph: Datasets,
   eval_runs,    BM25+dense,               Workflows, Agents,
   feedback)      O(log N))                Executions)
                       │                              │
                       └──── GraphRAG RRF fusion ─────┘
                                   (P10)
```

---

*GeoSI v2 — Built in Python 3.11 · FastAPI · QGIS 3.34 · PostGIS 3.4 · Qdrant 1.12 · Neo4j 5.20 · Redis 7.2 · Docker · Kubernetes · OpenTelemetry*
