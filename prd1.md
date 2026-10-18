# GeoSI v2 — PRD
### Autonomous Geospatial Intelligence Platform: Multi-Agent Architecture, Production-Hardened

| | |
|---|---|
| **Document owner** | Product / Engineering — Aaron (ZapServe Interconnecting Pvt. Ltd.) |
| **Scope** | Full multi-agent architecture (per "GeoSI Ultimate Agent Architecture v2 Proposal") + production-readiness requirements derived from codebase audit of `GEOSI.zip` v2.0.0 |
| **Status** | Approved for engineering — ready to plan sprints |
| **Version** | 4.0 |
| **Last updated** | July 2026 |

---

## 0. How this PRD differs from v3

The prior PRD (v3) deliberately collapsed GeoSI's reasoning into a single stateful orchestration *graph* with 9 pipeline stages, on the theory that a monolithic graph is easier to harden and ship. This document supersedes that simplification and instead adopts the **11-core-agent + 3-optional-agent architecture** defined in the v2 proposal as the system of record, because:

- It maps cleanly onto GeoSI's actual domain breadth (GIS / Remote Sensing / ML / Geology), which a single planner-executor loop under-serves.
- It gives each domain a dedicated, independently testable and independently prompt-tuned agent, improving debuggability.
- It's explicitly designed to support Agentic RAG, Reflection, HITL, and a future GeoSI Foundation Model — the same production goals as v3, just realized through specialized agents instead of one graph with many stages.

Every production-hardening requirement from v3 (auth, structured outputs, permission tiers, guardrails, evaluation, observability, MCP, CI/CD) is **retained and re-attached to specific agents** below, so nothing from the hardening effort is lost — it's distributed across the 14-agent roster instead of centralized in one orchestrator.

---

## 1. Executive Summary

GeoSI is evolving from a QGIS plugin + FastAPI service into a full **Autonomous Geospatial Intelligence Platform**: a natural-language interface that understands GIS problems, retrieves domain knowledge, reasons across GIS / Remote Sensing / Machine Learning / Geology, plans multi-step workflows, safely executes them against QGIS/GDAL/Rasterio/GeoPandas/PyTorch, validates outputs, learns from every execution, and generates maps, reports, and explanations.

The platform is built around **11 core agents** (Supervisor, Planning, Validation, Reflection, Permission & Safety, GIS, Remote Sensing, Machine Learning, Geology, Verification, Report Generation) plus **3 optional specialized agents** (Research, Workflow Optimization, Code Generation), coordinated through a 7-layer architecture (Presentation → Reasoning → Knowledge → Domain → Execution → Data → Infrastructure).

This PRD specifies what must be true of each agent and each layer before GeoSI v2 can be called production-ready: authenticated APIs, schema-validated plans, permission-tiered execution, prompt-injection guardrails, a CI-gated evaluation harness, full observability, and a standards-based MCP interface — on top of the multi-agent reasoning core.

---

## 2. Vision

> GeoSI is an Autonomous Geospatial Intelligence Platform that understands natural language, retrieves GIS knowledge, reasons about spatial problems, plans optimal workflows, safely executes GIS operations, validates outputs, learns from previous executions, and automatically generates maps, reports, and explanations — serving as a geospatial AI copilot for researchers, engineers, government agencies, and industry.

### Goals for v2

1. Every one of the 11 core agents is independently implemented, independently testable, and independently observable.
2. Zero unauthenticated write paths to PostGIS, Neo4j, Qdrant, or the QGIS project.
3. 100% of Planning Agent outputs pass schema validation before the Execution Dispatcher runs anything.
4. Every destructive operation requires explicit human approval via the Permission & Safety Agent by default.
5. p95 latency: < 4s for cached/rule-based single-agent operations; < 15s for full multi-agent workflows involving retrieval + planning + validation + reflection.
6. RAGAS faithfulness ≥ 0.85 and context precision ≥ 0.75 on a 150+ query golden set, measured per-agent where applicable (Research Agent, Planning Agent).
7. One-command reproducible deployment (`docker compose up` for dev, Kubernetes manifests for production) of the full stack: all agents + PostGIS + Neo4j + Qdrant + Redis.
8. GeoSI is consumable via the QGIS plugin, a Web UI, a REST API, and an MCP server — all four surfaces route through the same Supervisor Agent and the same Permission & Safety Agent, never bypassing it.

### Non-goals (v2)

- Fully autonomous execution with zero human oversight remains a research track (see Roadmap P11), not a v2 requirement.
- A trained "GeoSI Foundation Model" is an explicit future direction, not built in this version — v2 uses off-the-shelf LLMs (Ollama / Gemini / Claude / rule-based fallback) orchestrated across agents.

---

## 3. Core Workflow

```
                           User
                             │
                             ▼
                 Natural Language Query
                             │
                             ▼
                     GeoSI Interface
                 (Desktop / Web / API / MCP)
                             │
                             ▼
                  Supervisor Agent (Brain)
                             │
      ┌──────────────────────┼─────────────────────────┐
      │                      │                         │
      ▼                      ▼                         ▼
 Intent Parser        Session Manager          Memory Manager
      │                      │                         │
      └──────────────────────┴─────────────────────────┘
                             │
                             ▼
                GIS Knowledge Retrieval Layer
                             │
      ┌──────────────┬───────────────┬───────────────────┐
      │              │               │                   │
      ▼              ▼               ▼                   ▼
 GIS Documentation  Workflow KB   Research Papers   User Projects
      │              │               │                   │
      └───────────────────── Qdrant (hybrid RRF + rerank) ┘
                             │
                             ▼
                     Planning Agent
             (Reasoning + Tool Selection, schema-validated)
                             │
                             ▼
                    Validation Agent
     (CRS • Layers • Parameters • Dependencies)
                             │
                             ▼
                    Reflection Agent
     (Self-check • Retry • Improve Workflow)
                             │
                             ▼
                  Permission & Safety Agent
        (Allow • Ask • Deny • Guardrails • HITL)
                             │
                             ▼
                  Execution Dispatcher
                             │
      ┌─────────────┬─────────────┬──────────────┬──────────────┐
      │             │             │              │              │
      ▼             ▼             ▼              ▼              ▼
 GIS Agent     RS Agent      ML Agent     Geology Agent   Research Agent
      │             │             │              │              │
      └─────────────┴─────────────┴──────────────┴──────────────┘
                             │
                             ▼
                    GeoSI Execution Engine
                             │
      ┌───────────┬───────────┬─────────────┬──────────────┐
      │           │           │             │              │
      ▼           ▼           ▼             ▼              ▼
     QGIS       GDAL      Rasterio     GeoPandas      PyTorch
                             │
                             ▼
           PostGIS • Neo4j • Qdrant • GeoParquet
                             │
                             ▼
                  Verification Agent
     (QA • Validation • Metrics • Geometry Checks)
                             │
                             ▼
                   Report Generation Agent
                             │
                             ▼
         Maps • Reports • Logs • Workflow Graphs
                             │
                             ▼
                 Learn From Execution
                             │
                             ▼
            Workflow Memory + Query Memory + Feedback
                             │
                             ▼
                         Qdrant / Neo4j
```

Every arrow in this diagram is also an audit-log write point (FR-8.3) and an OpenTelemetry span boundary (FR-9) — see §7 and §9.

---

## 4. Agent Specifications

### 4.1 Core Agents (11)

Each core agent below carries its own production requirements in addition to its domain responsibilities — no agent ships without auth, schema validation on its inputs/outputs, and audit logging.

#### 1. Supervisor Agent
- Controls the complete workflow; delegates tasks to downstream agents; coordinates cross-agent state; maintains execution state for the session.
- **Production requirements:** owns the multi-session engine pool (one Supervisor instance per session/API key, never a global singleton); enforces per-request timeout budgets across the LLM cascade (Ollama → Gemini → Claude → rule-based); is the single entry point for all four client surfaces (QGIS plugin, Web, REST, MCP) so no surface can bypass downstream safety agents.

#### 2. Planning Agent
- Understands user intent; generates an execution plan; selects GIS tools from the dynamically-discovered QGIS Processing registry; optimizes the workflow.
- **Production requirements:** MUST emit a schema-validated `ExecutionPlan` (Pydantic model / native provider function-calling), never raw free-text JSON parsed with `json.loads()`. On schema-validation failure, retry once with the error fed back to the model, then fall back to rule-based planning. Every `ToolStep` MUST carry a `risk_level` (`read_only` / `mutating` / `destructive`) computed from the target algorithm's metadata.

#### 3. Validation Agent
- CRS validation, layer validation, parameter validation, dependency checking, workflow consistency.
- **Production requirements:** runs *before* execution, not after; validates against a known-table/known-CRS allow-list rather than trusting LLM-supplied identifiers directly (closes the SQL/identifier-injection surface).

#### 4. Reflection Agent
- Self-reviews the execution plan; compares it against successful past workflows; detects planning mistakes; retries failed plans; improves reasoning over time.
- **Production requirements:** pre-execution critic pass flags plans that contradict retrieved documentation or reference a tool with a known-low reliability score from `FeedbackMemory.get_tool_reliability()`. Post-execution, on failure it retrieves similar past failures, generates a corrected plan, and retries up to N=2 times before surfacing the error to the user.

#### 5. Permission & Safety Agent
- Prevents dangerous operations; confirms overwrite/delete; provides prompt-injection protection; enforces output guardrails; owns tool permission policies.
- **Production requirements — this is the single most important agent for launch:**
  - Every tool invocation is checked against a policy table: `allow` (auto-run), `ask` (require confirmation), `deny` (block).
  - Default policy: `read_only` → allow; `mutating` → ask; `destructive` → ask + typed confirmation phrase.
  - All content retrieved from RAG/Qdrant is scanned for injection patterns before it enters the Planning Agent's prompt; flagged content is annotated, not silently trusted.
  - Owns the Human-in-the-Loop (HITL) approval UI surfaced in the QGIS dock and the `approve_pending_action` MCP tool.
  - Policy overrides per algorithm ID are admin-configurable via `POST /admin/policy`.

#### 6. GIS Agent
- Vector processing, raster processing, buffer, clip, union, intersect, dissolve, overlay, terrain analysis, hydrology.
- **Production requirements:** all destructive operations (overwrite, delete, drop) route through the Permission & Safety Agent before `processing.run()` is called; no direct execution path from Planning Agent to QGIS Processing.

#### 7. Remote Sensing Agent
- Sentinel, Landsat, MODIS, Planet, SAR, NDVI, NDWI, SAVI, EVI, NDBI, atmospheric correction, change detection.
- **Production requirements:** raster outputs are validated by the Verification Agent (geometry/CRS/value-range checks) before being reported back to the user; large raster jobs respect the Supervisor Agent's timeout/cost budget.

#### 8. Machine Learning Agent
- Classification, regression, clustering, forecasting, model training, model evaluation, prediction. Libraries: Scikit-Learn, PyTorch, TensorFlow.
- **Production requirements:** model training/inference jobs are tagged `mutating` at minimum (writes model artifacts) and are subject to Permission & Safety Agent review; artifacts and metrics are written to PostGIS/`geosi_eval_runs` for reproducibility.

#### 9. Geology Agent
- Geological mapping, structural geology, stratigraphic modeling, geological cross-sections, fault visualization, fold analysis, borehole correlation, 3D geological modeling, mineral prospectivity, landslide susceptibility, AI geological interpretation.
- **Production requirements:** knowledge lookups against the Geological Knowledge Qdrant collection go through the same guardrail-scanning as GIS documentation (FR-3.1) since geological interpretation content is also RAG-retrieved and therefore also an injection surface.

#### 10. Verification Agent
- Geometry validation, output validation, raster QA, layer integrity, accuracy metrics, CRS verification.
- **Production requirements:** runs on every execution result before it reaches the Report Generation Agent; failures route back to the Reflection Agent for retry rather than surfacing a broken output to the user.

#### 11. Report Generation Agent
- PDF reports, maps, workflow graphs, methodology, execution summary, sources, logs, statistics.
- **Production requirements:** every generated report is linked to its corresponding `geosi_audit_log` entry so outputs are traceable back to the exact plan, parameters, and approvals that produced them.

### 4.2 Optional Specialized Agents (3)

| Agent | Responsibilities | Production note |
|---|---|---|
| **Research Agent** | Retrieve research papers, literature review, summarization, citation generation | Its RAG output is subject to the same golden-set RAGAS evaluation (faithfulness, context precision) as the core Planning Agent's retrieval step |
| **Workflow Optimization Agent** | Compare workflows, suggest faster execution, reduce unnecessary steps, learn best practices | Reads from `WorkflowMemory`/`geosi_eval_runs`; read-only by design, always `allow`-tier |
| **Code Generation Agent** | Generate PyQGIS scripts, GeoPandas code, Rasterio workflows, export reproducible Python scripts | Generated code is never auto-executed — output is always presented to the user for review, never routed back into the Execution Dispatcher automatically |

### 4.3 Agent Roster Summary

| # | Agent | Tier | Auto-executes? |
|---|---|---|---|
| 1 | Supervisor | Core | Orchestrates only |
| 2 | Planning | Core | No — plan only, gated by Validation/Permission |
| 3 | Validation | Core | No — gate only |
| 4 | Reflection | Core | No — critique/retry only |
| 5 | Permission & Safety | Core | No — gate only, owns HITL |
| 6 | GIS | Core | `allow`/`ask` per policy |
| 7 | Remote Sensing | Core | `allow`/`ask` per policy |
| 8 | Machine Learning | Core | `ask` minimum |
| 9 | Geology | Core | `allow`/`ask` per policy |
| 10 | Verification | Core | No — QA only |
| 11 | Report Generation | Core | `allow` (report writes are non-destructive to source data) |
| 12 | Research | Optional | `allow` (read-only) |
| 13 | Workflow Optimization | Optional | `allow` (read-only) |
| 14 | Code Generation | Optional | Never — output for human review only |

**Total: 11 core + 3 optional = 14 agents.**

---

## 5. Architecture Layers

| Layer | Contents |
|---|---|
| **1 — Presentation** | Desktop (QGIS plugin), Web, API, MCP |
| **2 — Reasoning** | Supervisor, Planner, Reflection, Validation, Safety |
| **3 — Knowledge** | Qdrant (hybrid RRF k=60 + cross-encoder rerank), Workflow Memory, GIS Docs, Research Papers |
| **4 — Domain** | GIS, Remote Sensing, Machine Learning, Geology |
| **5 — Execution** | QGIS, GDAL, Rasterio, GeoPandas, PyTorch |
| **6 — Data** | PostGIS, Neo4j, Qdrant |
| **7 — Infrastructure** | FastAPI, Docker, Kubernetes, Cloud |

### 5.1 Knowledge Layer — Qdrant Collections

GIS Documentation · PyQGIS Documentation · GDAL Documentation · Rasterio Documentation · GeoPandas Documentation · PostGIS Documentation · Earth Engine Documentation · Remote Sensing Workflows · Geological Knowledge · Research Papers · Workflow Examples · User Projects · Query History · Execution History

All collections use the existing hybrid RRF retriever (k=60) + cross-encoder reranker (retrieve ~20–50, rerank to 5) — this is a KEEP from the current codebase, not a rebuild.

### 5.2 Data Layer

| Store | Contents |
|---|---|
| **PostGIS** | Spatial layers, projects, workflow history, execution results, `geosi_audit_log`, `geosi_query_history`, `geosi_feedback_history`, `geosi_policy_overrides`, `geosi_eval_runs` |
| **Neo4j** *(new in v2)* | Knowledge graph, spatial relationships, workflow graph, dataset relationships — powers cross-reference queries the Research and Geology agents need (e.g., "what workflows have used this dataset before") |
| **Qdrant** | Semantic search, hybrid search, agent memory, workflow memory |

### 5.3 Execution Layer

GIS libraries: QGIS, PyQGIS, GDAL, Rasterio, GeoPandas, Shapely, Fiona, OGR, NumPy, Pandas.
AI libraries: PyTorch, TensorFlow, Scikit-Learn, HuggingFace, SentenceTransformers.

### 5.4 API Layer

FastAPI endpoints: `/chat`, `/workflow`, `/execute`, `/rag/query`, `/rag/search`, `/ml/predict`, `/geology/analyze`, `/research/search`, `/report/generate`, plus the v3-hardening additions `/health`, `/stats`, `/admin/policy`, and the MCP surface (`geosi_mcp`).

### 5.5 Infrastructure Layer

Docker, Kubernetes, Nginx, Redis, Prometheus, Grafana, GitHub Actions.

---

## 6. What Carries Forward from the v3 Hardening Effort

Nothing from the earlier production audit is dropped — it's re-attached to specific agents/layers in this architecture:

| v3 hardening item | Where it lives in v2 |
|---|---|
| Structured, schema-validated planning (FR-1) | Planning Agent |
| Permission-tiered execution, allow/ask/deny (FR-2) | Permission & Safety Agent |
| Guardrails on RAG-retrieved content (FR-3) | Permission & Safety Agent, applied before content reaches Planning/Research/Geology agents |
| Reflection / self-correction (FR-4) | Reflection Agent |
| MCP interface (FR-5) | Presentation Layer, gated through Supervisor + Permission & Safety |
| Multi-session engine pool, no global singleton (FR-6) | Supervisor Agent |
| Evaluation & observability (FR-7) | Cross-cutting; Research & Planning agents are the primary RAGAS eval targets |
| PostGIS as system of record, Alembic migrations, audit log (FR-8) | Data Layer |
| Containerization + CI/CD, plugin packaging (FR-9) | Infrastructure Layer |
| AuthN/AuthZ, CORS lockdown, secrets management | API Layer / Infrastructure Layer |
| SQL-injection and `gdf.eval()` fixes | GIS Agent, Data Layer |

---

## 7. Functional Requirements (consolidated)

### FR-1 Structured Planning (Planning Agent)
- **FR-1.1** MUST request native provider function-calling / tool-calling, not free-text JSON.
- **FR-1.2** Every plan validates against a Pydantic schema; on failure, retry once with the error fed back, then fall back to rule-based planning.
- **FR-1.3** Every step carries a `risk_level`.

### FR-2 Permission-Tiered Execution (Permission & Safety Agent)
- **FR-2.1** Policy table: `allow` / `ask` / `deny`, keyed by algorithm ID.
- **FR-2.2** Default policy by risk level as specified in §4.1.
- **FR-2.3** Admin-overridable via `POST /admin/policy`.

### FR-3 Guardrails (Permission & Safety Agent, applied at Knowledge Layer boundary)
- **FR-3.1** All RAG-retrieved content scanned for injection patterns before entering any agent's prompt.
- **FR-3.2** Tool outputs validated against expected types/ranges before surfacing.

### FR-4 Reflection / Self-Correction (Reflection Agent)
- **FR-4.1** Up to N=2 corrected retries on execution failure, informed by `FeedbackMemory`.
- **FR-4.2** Pre-execution critic pass against retrieved docs and tool-reliability scores.

### FR-5 MCP Interface (Presentation Layer)
- **FR-5.1** Exposes `run_query`, `search_gis_docs`, `suggest_workflow`, `list_layers`, `get_layer`, `approve_pending_action`.
- **FR-5.2** MCP calls pass through Supervisor → Permission & Safety with zero bypass path.
- **FR-5.3** Token-based auth (`GEOSI_MCP_TOKEN`).

### FR-6 Multi-Session Supervisor
- **FR-6.1** Session/API-key-scoped Supervisor instances, no global singleton.
- **FR-6.2** Isolated session state with configurable TTL/eviction.

### FR-7 Evaluation & Observability
- **FR-7.1** Golden set of ≥150 queries, run in CI on every prompt/retriever/agent-logic change.
- **FR-7.2** RAGAS metrics gate: faithfulness ≥ 0.85, context precision ≥ 0.75.
- **FR-7.3** OpenTelemetry spans on every agent hand-off (Supervisor → Planning → Validation → Reflection → Permission → Execution Dispatcher → domain agent → Verification → Report Generation).

### FR-8 Data Layer
- **FR-8.1** Alembic-managed PostGIS schema, no ad-hoc `create_all()`.
- **FR-8.2** All memory migrated from JSON files to PostGIS as system of record.
- **FR-8.3** Immutable `geosi_audit_log`, written by every agent that executes or approves an action.
- **FR-8.4** *(new)* Neo4j knowledge graph populated incrementally from workflow executions and dataset relationships; Research and Geology agents query it for cross-reference lookups.

### FR-9 Deployment
- **FR-9.1** Multi-stage Dockerfile per service; `docker-compose.yml` orchestrating all agents + PostGIS + Neo4j + Qdrant + Redis for local/dev.
- **FR-9.2** Kubernetes manifests for production horizontal scaling (Roadmap P9).
- **FR-9.3** CI: lint → type-check → unit tests → eval gate → security scan → build → push.
- **FR-9.4** QGIS plugin packaged and versioned for the official Plugin Repository, tested against QGIS 3.28 LTR and current stable.

---

## 8. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Security** | AuthN (API key or OAuth2/JWT) on all FastAPI and MCP endpoints; no wildcard CORS + credentials; secrets via env/Vault, never hardcoded; SQL identifiers allow-listed; dependency scanning in CI |
| **Reliability** | Per-request timeout/cost budget across the LLM cascade; circuit breaker after N provider failures; idempotent execution where possible |
| **Performance** | p95 targets per §2 goal 5; retrieval top-k tuned per Knowledge Layer collection |
| **Scalability** | Stateless FastAPI workers behind Nginx; session state externalized to PostGIS/Redis; Kubernetes horizontal scaling of stateless agents |
| **Observability** | Structured JSON logs, OTel traces exported to Prometheus/Grafana, `/health`/`/stats` report per-agent circuit-breaker and reranker-fallback state |
| **Compliance/Auditability** | Immutable audit log per agent action; data retention policy; traceability from report → plan → approval |
| **Portability** | Full stack runs via `docker compose up` on a laptop; QGIS plugin installable standalone (degrades to local-only agents) |
| **Maintainability** | Type-annotated, ≥70% test coverage per agent module, Alembic-managed schema, CI-enforced lint/type-check |

---

## 9. Observability Model

Every agent hand-off in the Core Workflow diagram (§3) is:
1. An OpenTelemetry span (latency, token usage, outcome).
2. An audit-log write to `geosi_audit_log` (who/what/when/params/result/risk_level/approval status) for any agent capable of mutating state.
3. Surfaced in `/health` and a Grafana dashboard, broken down per-agent (success rate, latency, fallback-mode usage).

RAGAS evaluation (FR-7.2) is run per-agent where retrieval is involved: primarily the Planning Agent's context-retrieval step and the Research Agent's literature-search step, both scored against the same golden set with agent-specific query subsets.

---

## 10. Data Model Additions

| Table / Store | Purpose |
|---|---|
| `geosi_audit_log` (PostGIS) | Immutable record of every agent action |
| `geosi_query_history` (PostGIS) | Replaces JSON; adds `session_id`, `user_id` |
| `geosi_feedback_history` (PostGIS) | Replaces JSON; indexed on `tool_id` for the Reflection Agent's reliability lookups |
| `geosi_policy_overrides` (PostGIS) | Permission & Safety Agent's per-algorithm allow/ask/deny overrides |
| `geosi_eval_runs` (PostGIS) | RAGAS/DeepEval run history for CI regression tracking |
| Neo4j knowledge graph | Spatial relationships, workflow graph, dataset relationships, populated from execution history |

---

## 11. API & Protocol Summary

| Surface | Endpoints / Tools |
|---|---|
| REST (`geosi_server`) | `/chat`, `/workflow`, `/execute`, `/rag/query`, `/rag/search`, `/ml/predict`, `/geology/analyze`, `/research/search`, `/report/generate`, `/health`, `/stats`, `/admin/policy` — all authenticated |
| MCP (`geosi_mcp`) | `run_query`, `search_gis_docs`, `suggest_workflow`, `list_layers`, `get_layer`, `approve_pending_action` — token-authenticated, routed through Supervisor + Permission & Safety |
| QGIS Plugin | Dock UI + HITL approval dialog, talks to Supervisor via local engine or REST |

CORS: environment-driven allow-list only, never wildcard + credentials.

---

## 12. Roadmap

| Phase | Focus | Agents/Layers delivered |
|---|---|---|
| **P1** | Production hardening of existing core (auth, structured planning, permission tiers, guardrails, audit log) | Supervisor, Planning, Validation, Permission & Safety (MVP), GIS Agent |
| **P2** | Evaluation & observability | Golden set + RAGAS gate + OTel tracing across P1 agents |
| **P3** | Containerization + CI/CD | Docker Compose for Supervisor/Planning/Validation/GIS + PostGIS + Qdrant |
| **P4** | MCP server | Presentation Layer MCP surface, HITL `approve_pending_action` |
| **P5** | Reflection Agent + Verification Agent | Closes the self-correction and QA loop |
| **P6** | Remote Sensing Agent, Machine Learning Agent | Domain-layer expansion |
| **P7** | Geology Agent, Report Generation Agent | Domain-layer completion + reporting |
| **P8** | Optional agents: Research, Workflow Optimization, Code Generation | Read-only/advisory agents, lowest risk to add |
| **P9** | Neo4j knowledge graph + Kubernetes horizontal scaling | Data Layer + Infrastructure Layer completion |
| **P10** | GraphRAG-style cross-agent knowledge queries | Deepens Neo4j integration for Research/Geology agents |
| **P11** | Autonomous GIS (research track, HITL retained by default) | Explicitly not required for v2 GA |

---

## 13. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| 14-agent architecture increases orchestration complexity vs. a single graph | Supervisor Agent owns all cross-agent state; every hand-off is a typed, schema-validated message, not free-text — keeps agents independently testable |
| A domain agent (GIS/RS/ML/Geology) executes a destructive op without going through Permission & Safety | Execution Dispatcher hard-codes the Permission & Safety check as a non-bypassable step before any domain agent call |
| Neo4j introduces a second data store to keep consistent with PostGIS | Neo4j is populated asynchronously from `geosi_audit_log`/execution history — PostGIS remains the single source of truth; Neo4j is a derived index |
| Optional agents (Code Generation especially) get wired to auto-execute under deadline pressure | FR treats "Code Generation output is never auto-executed" as a launch-blocking acceptance criterion, not a suggestion |
| RAG index/prompt changes silently degrade a specific agent's quality | Per-agent RAGAS scoring (§9) catches regressions in Planning or Research agents independently |

---

## 14. Acceptance Criteria — Definition of Done

- [ ] All 11 core agents implemented and independently unit-tested (≥70% coverage each)
- [ ] No agent can call `processing.run()` or an equivalent mutating operation without passing through the Permission & Safety Agent
- [ ] Planning Agent output is 100% schema-validated before reaching the Execution Dispatcher
- [ ] Destructive operations require explicit human approval, logged in `geosi_audit_log`
- [ ] RAG-retrieved content is guardrail-scanned before entering any agent's prompt
- [ ] Golden-set RAGAS evaluation passes thresholds for both Planning Agent and Research Agent retrieval, wired into CI
- [ ] Full stack (all core agents + PostGIS + Neo4j + Qdrant + Redis) deployable via `docker compose up`
- [ ] MCP server live, routes through Supervisor + Permission & Safety, token-authenticated
- [ ] QGIS plugin passes packaging checks for the official repository
- [ ] Optional agents (Research, Workflow Optimization, Code Generation) ship only after all core agents meet the above, and Code Generation output is confirmed never auto-executed
- [ ] `/health` dashboard reports per-agent status, covering all external dependencies

---

## 15. Sources

- Original architecture reference: *GeoSI Ultimate Agent Architecture (v2 Proposal)* — 11 core agents, 3 optional agents, 7-layer architecture, Qdrant/PostGIS/Neo4j data layer.
- 2026 production-RAG, agent-security, and evaluation-tooling research grounding the hardening requirements (RRF/hybrid search best practice, OWASP Agentic Top-10 style guardrail guidance, RAGAS/DeepEval evaluation patterns, MCP interoperability standard).

*(Re-verify vendor/tooling specifics before major implementation decisions, as this space moves quickly.)*