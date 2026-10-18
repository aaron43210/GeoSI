# GeoSI v2 — Phase 0: Codebase Audit

**Audited:** July 2026  
**Codebase version:** v2.0.0 (`GEOSI.zip`, ~10,572 LOC across 6 packages)  
**Against:** `prd1.md` (GeoSI v2 primary PRD) + `prd.md` (v3 addendum/supplement)  
**Status:** ✅ Complete — ready to proceed to Phase 1 planning

---

## 1. Package → Agent / Layer Mapping

### `geosi_engine/` (Core Reasoning Engine)

| File | Current Role | v2 Destination | Action |
|------|-------------|----------------|--------|
| `__init__.py` (GeoSI facade) | Single monolithic entry point, wires all components | **Supervisor Agent** scaffold → becomes `geosi_engine/agents/supervisor.py` | REFACTOR — extract session pool, route all 4 surfaces through it |
| `agent.py` (GeoSIAgent, LLM cascade) | LLM provider cascade: Ollama → Gemini → Claude → rule-based; builds `ExecutionPlan` | **Planning Agent** core → `geosi_engine/agents/planning.py` | MODIFY — add Pydantic function-calling schemas, replace `json.loads(text)` (G1) |
| `parser.py` (QueryParser) | NL → `AnalysisRequest` intent/entity extraction | **Planning Agent** (query-parse sub-step) | KEEP + MODIFY — same location, add structured output binding |
| `executor.py` (ExecutionEngine) | Runs `ToolStep`s against registry/state, catches errors | **Execution Dispatcher** component of Supervisor | MODIFY — add hard-coded Permission & Safety check before every `execute_step()` call |
| `models.py` (Pydantic models) | `ExecutionPlan`, `ToolStep`, `AnalysisRequest`, `Layer`, etc. | **Shared schema layer** used by all agents | EXTEND — add `risk_level: Literal["read_only","mutating","destructive"]` to `ToolStep`; add `ExecutionPlan.guardrail_flags`; add `ApprovalResult`; add `AgentMessage` inter-agent type |
| `validation.py` (ValidationEngine) | Geometry, CRS, attribute, and precondition validation | **Validation Agent** core → `geosi_engine/agents/validation.py` | MODIFY — add SQL allow-list check (G4), wrap in agent class |
| `registry.py` (ToolRegistry) | Discovers and stores `GISTool`/`BackendTool` instances | **GIS Agent** tool registry (KEEP) | KEEP — only add `get_risk_level(algorithm_id)` method |
| `state.py` (StateManager) | Tracks layers, results, history per session | **Session state** for Supervisor's SessionPool | KEEP + extend with `session_id`, TTL metadata |
| `conversation.py` (ConversationManager) | Per-session LLM conversation history | Lives inside session state, used by Planning Agent | KEEP — isolate per session in SessionPool |
| `base.py` (GISTool ABC, register_backend) | Abstract tool base class + backend registration | Used by both GIS Agent (QGIS backend) and portable tools | KEEP |
| `tools/portable.py` | Pure-Python portable GIS tools (field calculator) | **GIS Agent** portable tool set | MODIFY — fix `gdf.eval(expression)` → safe AST evaluator (G12) |

### `geosi_rag/` (Knowledge Retrieval — KEEP AS-IS)

| File | Current Role | v2 Destination | Action |
|------|-------------|----------------|--------|
| `retriever.py` (Retriever, RRF hybrid) | Hybrid semantic+keyword search with RRF(k=60) | **Knowledge Layer** retrieval engine | ✅ **KEEP** — already 2026 best-practice; add OTel span only |
| `reranker.py` (Reranker, CrossEncoder) | Cross-encoder reranking with score-fallback | **Knowledge Layer** reranker | ✅ **KEEP** — add `/health` mode reporting (degraded vs. full) |
| `qdrant_store.py` (QdrantStore) | Qdrant vector DB client wrapper | **Knowledge Layer** vector store | ✅ **KEEP** — add collection-level guardrail flag support |
| `embedding_service.py` (EmbeddingService) | Local BAAI/bge-large-en-v1.5 embeddings | **Knowledge Layer** encoder | ✅ **KEEP** |
| `rag_service.py` (RAGService) | End-to-end RAG pipeline (retrieve → rerank → assemble) | **Knowledge Layer** service called by Planning/Research/Geology agents | MODIFY — add guardrail scanning step before returning context (FR-3.1) |
| `chunker.py` (Chunker) | Document chunking for indexing | Ingestion pipeline | ✅ **KEEP** |
| `document_loader.py` (DocumentLoader) | PDF/HTML/text document loading | Ingestion pipeline | ✅ **KEEP** |
| `ingest_cli.py` | CLI for ingesting documents into Qdrant | Ingestion pipeline | ✅ **KEEP** |

### `geosi_knowledge/` (Memory & Learning Loop)

| File | Current Role | v2 Destination | Action |
|------|-------------|----------------|--------|
| `knowledge_manager.py` (KnowledgeManager) | Orchestrates RAGService + WorkflowMemory + QueryMemory + FeedbackMemory; `learn_from_execution()` feedback loop | **Knowledge Layer** orchestrator; `learn_from_execution()` feeds Reflection Agent | ✅ **KEEP** — extend `learn_from_execution()` to write to PostGIS (Phase 5, G9) |
| `feedback_memory.py` (FeedbackMemory) | JSON-persisted per-tool success stats, failure patterns, `get_tool_reliability()` | **Reflection Agent** data source; `get_tool_reliability()` used by pre-execution critic | MODIFY Phase 5 — migrate JSON → `geosi_feedback_history` PostGIS table (FR-8.2) |
| `query_memory.py` (QueryMemory) | JSON-persisted query history, pattern detection | Knowledge layer / Supervisor session history | MODIFY Phase 5 — migrate JSON → `geosi_query_history` PostGIS table (FR-8.2) |
| `workflow_memory.py` (WorkflowMemory) | Qdrant-backed workflow example storage, `find_similar()` | Used by Planning Agent and Reflection Agent | ✅ **KEEP** |
| `builtin_workflows.py` | 15 built-in workflow templates | Cold-start knowledge base for Knowledge Layer | ✅ **KEEP** |

### `geosi_data/` (Data Layer)

| File | Current Role | v2 Destination | Action |
|------|-------------|----------------|--------|
| `database.py` (Database) | SQLAlchemy PostGIS connection manager; **has hardcoded `geosi:geosi` fallback (G3)** | **Data Layer** DB connection | MODIFY — remove `_DEFAULT_URL` fallback, fail closed in production mode (G3 fix) |
| `db_models.py` (ORM models) | `SpatialLayerRecord`, `ProjectRecord`, `WorkflowHistoryRecord`, `ExecutionResultRecord` | **Data Layer** schema | EXTEND — add `geosi_audit_log`, `geosi_policy_overrides`, `geosi_eval_runs`, `geosi_query_history`, `geosi_feedback_history` tables (FR-8); replace `create_all()` with Alembic migrations |
| `postgis_manager.py` (PostGISManager) | GeoDataFrame ↔ PostGIS I/O; **f-string SQL injection surfaces (G4)** | **Data Layer** spatial I/O | MODIFY — replace `f"SELECT * FROM {table_name}"`, `f"DROP TABLE IF EXISTS {table_name}"`, `f"SELECT COUNT(*) FROM {table}"` with `quoted_name` + allow-list (G4 fix) |
| `layer_repository.py` | CRUD for `SpatialLayerRecord` ORM | **Data Layer** repository | KEEP + extend for audit writes |
| `project_repository.py` | CRUD for `ProjectRecord` ORM | **Data Layer** repository | KEEP |
| `metadata_repository.py` | Metadata/stats storage | **Data Layer** repository; extend for audit log | EXTEND — add `write_audit_log()` method (FR-8.3) |

### `geosi_server/` (Presentation Layer — REST)

| File | Current Role | v2 Destination | Action |
|------|-------------|----------------|--------|
| `app.py` (FastAPI app) | Creates app, global singleton `_engine = None` **(G10)**, wildcard CORS + credentials **(G2)** | **Presentation Layer** REST surface | MODIFY — replace singleton with `SessionPool`, fix CORS (G2), add AuthN middleware (G2), add `/admin/policy` endpoint |
| `rag_routes.py` | `/rag/*` endpoints | **Presentation Layer** RAG routes | ADD auth dependency to all routes |
| `workflow_routes.py` | `/workflow/*` endpoints | **Presentation Layer** workflow routes | ADD auth dependency to all routes |
| `data_routes.py` | `/layers/*` endpoints including DELETE | **Presentation Layer** data routes | SCOPE DELETE to admin role; ADD auth dependency |

### `geosi_plugin/` (Presentation Layer — QGIS)

| File | Current Role | v2 Destination | Action |
|------|-------------|----------------|--------|
| `qgis_bridge.py` (dynamic discovery) | ★ **Core innovation**: dynamic QGIS Processing algorithm discovery; `_run_qgis_algorithm()` | **GIS Agent** execution backend | ✅ **KEEP** discovery logic entirely; ADD `check_permission()` call before every `processing.run()` invocation for non-read-only algorithms (G5 fix) |
| `prompt_dock.py` (QGIS dock UI) | Chat UI in QGIS dock | **Presentation Layer** QGIS surface; Phase 4 — add HITL approval dialog | EXTEND Phase 4 — add `ask`-tier approval diff/preview widget |
| `geosi_plugin.py` | QGIS plugin entry point, init/unload | Presentation Layer plugin bootstrap | KEEP |

---

## 2. New Files / Packages Required (v2 Additions)

| New file/package | Phase | Purpose |
|-----------------|-------|---------|
| `geosi_engine/agents/supervisor.py` | P1 | Supervisor Agent: SessionPool, circuit breaker, cost budget, single entry point |
| `geosi_engine/agents/planning.py` | P1 | Planning Agent: structured Pydantic planning, function-calling per provider, retry logic |
| `geosi_engine/agents/validation.py` | P1 | Validation Agent: wraps ValidationEngine, adds SQL allow-list, `gdf.eval` fix |
| `geosi_engine/agents/permission_safety.py` | P1 | Permission & Safety Agent: policy table, guardrail scanner, `check_permission()`, `request_approval()` |
| `geosi_engine/agents/gis_agent.py` | P1 | GIS Agent: wraps qgis_bridge + portable tools; mandatory permission check |
| `geosi_server/auth.py` | P1 | API key / JWT auth middleware + dependency |
| `geosi_engine/guardrails.py` | P1 | Prompt-injection pattern scanner; attaches `guardrail_flags` to context objects |
| `geosi_engine/session_pool.py` | P1 | `SessionPool` class: LRU cache of GeoSI instances keyed by session/API key, TTL eviction |
| `geosi_engine/agents/reflection.py` | P5 | Reflection Agent: pre-exec critic, post-exec retry loop |
| `geosi_engine/agents/verification.py` | P5 | Verification Agent: geometry QA, raster QA, accuracy metrics |
| `geosi_engine/agents/remote_sensing.py` | P6 | Remote Sensing Agent: Sentinel/Landsat NDVI/NDWI/EVI/SAR |
| `geosi_engine/agents/ml_agent.py` | P6 | ML Agent: Scikit-Learn/PyTorch/TF classification/clustering/forecasting |
| `geosi_engine/agents/geology.py` | P7 | Geology Agent: geological mapping, cross-sections, prospectivity |
| `geosi_engine/agents/report_generation.py` | P7 | Report Generation Agent: PDF maps, methodology, audit-linked reports |
| `geosi_engine/agents/research.py` | P8 | Research Agent: literature retrieval, summarization, citations (read-only) |
| `geosi_engine/agents/workflow_optimization.py` | P8 | Workflow Optimization Agent: reads eval_runs, suggests faster paths |
| `geosi_engine/agents/code_generation.py` | P8 | Code Generation Agent: PyQGIS/GeoPandas scripts — NEVER auto-executed |
| `geosi_eval/` (package) | P2 | RAGAS evaluation harness, golden query set, CI gate, `geosi_eval_runs` writer |
| `geosi_mcp/` (package, FastMCP) | P4 | MCP server: `run_query`, `search_gis_docs`, `suggest_workflow`, `list_layers`, `get_layer`, `approve_pending_action` |
| `migrations/` (Alembic) | P1 | DB migrations for all new tables (replaces `create_all()`) |
| `Dockerfile` | P3 | Multi-stage build for `geosi_server` |
| `docker-compose.yml` | P3 | Full stack: server + PostGIS + Qdrant + Ollama |
| `.env.example` | P0/P1 | All required secrets documented, no working defaults |
| `pyproject.toml` | P0 | pinned deps, ruff + mypy config, pytest config |
| `.pre-commit-config.yaml` | P0 | ruff + mypy + pytest pre-commit hooks |

---

## 3. Gap Confirmation — All G1–G13 Still Present

Grep results confirm all 13 gaps from the PRD predecessor audit are **still present in the v2.0.0 codebase**:

| Gap | Location | Status |
|-----|----------|--------|
| **G1** `json.loads(text)` plan parsing | `agent.py:579`, `parser.py:750,757`, `conversation.py:137`, `parser.py:724` | ✅ CONFIRMED |
| **G2** `allow_origins=["*"]` + `allow_credentials=True` | `geosi_server/app.py:65` | ✅ CONFIRMED |
| **G3** Hardcoded `geosi:geosi` fallback credential | `geosi_data/database.py:27` (`_DEFAULT_URL`) | ✅ CONFIRMED |
| **G4** f-string SQL injection | `postgis_manager.py:128,191,228,235,262` | ✅ CONFIRMED (5 locations, more than originally counted) |
| **G5** No allow/ask/deny permission tiers; `processing.run()` runs directly | `qgis_bridge.py` (no check), `executor.py` (no gate) | ✅ CONFIRMED |
| **G6** No prompt-injection guardrails on RAG-retrieved content | `rag_service.py`, `knowledge_manager.py` — no scanning | ✅ CONFIRMED |
| **G7** No evaluation harness, no RAGAS/golden-set, no CI gate | No `geosi_eval/` package exists | ✅ CONFIRMED |
| **G8** No OTel tracing/observability | No spans in any pipeline stage | ✅ CONFIRMED |
| **G9** Memory split: `~/.geosi/*.json` + Qdrant + PostGIS, no Alembic | `feedback_memory.py`, `query_memory.py` use `~/.geosi/*.json`; `db_models.py` uses `create_all()` | ✅ CONFIRMED |
| **G10** Global singleton `_engine = None` | `geosi_server/app.py:24` | ✅ CONFIRMED |
| **G11** No containerization, no CI/CD | No `Dockerfile`, no `.github/workflows/` | ✅ CONFIRMED |
| **G12** `gdf.eval(expression)` in portable.py | `geosi_engine/tools/portable.py:191` | ✅ CONFIRMED |
| **G13** No MCP server | No `geosi_mcp/` package | ✅ CONFIRMED |

---

## 4. What is Confirmed KEEP (Do Not Rebuild)

| Component | File | Why |
|-----------|------|-----|
| Dynamic QGIS tool discovery | `geosi_plugin/qgis_bridge.py` | Zero hardcoded tools; uses `QgsApplication.processingRegistry()` — superior design confirmed by PRD |
| Hybrid RRF retriever (k=60) | `geosi_rag/retriever.py` | Exact 2026 best-practice formula; confirmed correct |
| Cross-encoder reranker + fallback | `geosi_rag/reranker.py` | Correct pattern; only add health reporting |
| Local BGE embeddings | `geosi_rag/embedding_service.py` | No external API dependency; cost/latency win |
| `learn_from_execution()` feedback loop | `geosi_knowledge/knowledge_manager.py` | Genuine Reflexion-style memory; extend only |
| 15 built-in workflow templates | `geosi_knowledge/builtin_workflows.py` | Good cold-start corpus |
| FastAPI as server framework | `geosi_server/app.py` | Correct; add security middleware, don't switch |
| ValidationEngine geometry/CRS checks | `geosi_engine/validation.py` | Solid; wrap in Validation Agent |
| StateManager checkpoint/undo logic | `geosi_engine/state.py` | Correct; use per-session |

---

## 5. LOC Summary

| Package | Files | LOC (approx) | v2 Fate |
|---------|-------|-------------|---------|
| `geosi_engine/` | 11 | ~4,200 | Major refactor + new agents sub-package |
| `geosi_rag/` | 9 | ~2,600 | Mostly KEEP; guardrail scanning + OTel |
| `geosi_knowledge/` | 6 | ~1,400 | KEEP; PostGIS migration in Phase 5 |
| `geosi_data/` | 6 | ~1,200 | SQL fix + new tables + Alembic |
| `geosi_server/` | 5 | ~600 | AuthN + CORS fix + session pool |
| `geosi_plugin/` | 3 | ~800 | KEEP bridge; HITL dock in Phase 4 |
| **Total existing** | **40** | **~10,800** | |
| **New (v2)** | ~25+ | ~6,000+ est. | Phased additions |

---

## 6. Phase 0 Deliverables Checklist

- [x] All packages read and audited
- [x] Module → agent/layer mapping table complete
- [x] All 13 gaps (G1–G13) confirmed present by grep
- [x] KEEP / MODIFY / NEW classification for every file
- [ ] `pyproject.toml` with pinned deps, ruff + mypy config (next step)
- [ ] `.env.example` with all secrets documented, no working defaults (next step)
- [ ] `pytest` configured with coverage reporting (next step)
- [ ] Pre-commit hooks configured (next step)
- [ ] Lint/type-check baseline established (next step)

---

*Last updated: Phase 0 audit — July 2026*
