# GeoSI v3 — Production Readiness PRD
### Geospatial Superintelligence: From Prototype Agent to Production Agentic-RAG Platform

**Document owner:** Product/Engineering
**Based on:** Codebase audit of `GEOSI.zip` (v2.0.0, ~10.6k LOC across 6 packages) + IBM "Agentic AI & RAG" course corpus + live 2026 industry research
**Status:** Draft for engineering review
**Last updated:** July 2026

---

## 0. How this document was built

1. **Static audit** of the uploaded `GEOSI.zip`: `geosi_engine`, `geosi_rag`, `geosi_knowledge`, `geosi_data`, `geosi_plugin`, `geosi_server`, `Connections.md`, `GeoSI_Roadmap_and_Course_Mapping.txt`, `requirements.txt`, `metadata.txt`.
2. **Concept extraction** from the supplied course material (RAG fundamentals, chunking/embedding/vector DB internals, HNSW/FAISS/Chroma indexing, LangChain vs LangGraph, agent design patterns — Reflection, Reflexion, ReAct, Orchestrator‑Worker, multi-agent systems, tool/function calling, structured Pydantic outputs, AI agent protocols — MCP/ACP/A2A/AP2/ANP/AG‑UI, prompt engineering, evaluation).
3. **Live web verification (2026)** of current best practice for: production RAG/hybrid-search, agent-orchestration frameworks, MCP servers for QGIS/GIS, agentic AI security (OWASP Agentic Top 10), and RAG evaluation/observability tooling. Sources are listed in §12.

**Key finding:** GeoSI's core RAG pipeline is already *more* aligned with 2026 best practice than most hobby projects — it has RRF hybrid fusion (k=60), a cross‑encoder reranker with fallback, local BGE embeddings, and a "Knowledge → RAG → PostGIS" learning loop. The gaps are almost entirely in **production hardening**: authentication/authorization, structured/validated LLM outputs, tool-execution safety, observability, evaluation, containerized deployment, and adoption of the emerging **MCP** standard for tool exposure — all of which are directly addressed in the course material you supplied.

---

## 1. Executive Summary

GeoSI is a QGIS plugin + standalone engine + FastAPI server that lets a user type natural-language GIS requests (e.g., *"Buffer hospitals by 500m"*, *"Calculate NDVI from Sentinel‑2"*) and have them planned and executed against 1000+ dynamically-discovered QGIS Processing algorithms, with a memory/RAG layer (Qdrant + PostGIS) that learns from every execution.

This PRD defines what is required to take GeoSI from a **well-architected v2 prototype** to a **production-grade Geospatial Agentic-RAG platform (v3)**, using the advanced concepts from the supplied Agentic AI & RAG curriculum (structured tool calling, LangGraph-style stateful orchestration, reflection/self-correction agents, hybrid retrieval + reranking, agent protocols, guardrails) and 2026 industry-standard practices for shipping LLM agents safely at scale.

The plan is organized as:
- **Section 2** — current-state architecture and code-level findings.
- **Section 3** — what to **KEEP**, **ADD**, **MODIFY**, and **REMOVE**, mapped explicitly to course concepts.
- **Section 4–9** — full functional/non-functional requirements, data model, API, security, and evaluation specs.
- **Section 10** — phased roadmap replacing/refining the existing 10-phase roadmap.
- **Section 11** — risks.
- **Section 12** — sources.

---

## 2. Current State Assessment (code-level findings)

### 2.1 What exists today (6 packages, ~10,572 LOC)

| Package | Role | Maturity |
|---|---|---|
| `geosi_plugin/` | QGIS UI, dock widget, **dynamic discovery** of all `QgsApplication.processingRegistry()` algorithms (`qgis_bridge.py`, 627 LOC) | Solid — zero hardcoded tools, a genuinely good design |
| `geosi_engine/` | `GeoSI` facade, `QueryParser`, `GeoSIAgent` (LLM cascade: Ollama → Gemini → Claude → rule-based), `ExecutionEngine`, `ToolRegistry`, `StateManager`, `ValidationEngine`, `ConversationManager` | Functional core; planning quality gaps (see 2.3) |
| `geosi_rag/` | `RAGService`, `Retriever` (hybrid RRF, k=60), `Reranker` (cross-encoder + fallback), `QdrantStore`, `EmbeddingService` (local BGE), `Chunker`, `DocumentLoader`, `ingest_cli.py` | **Already matches 2026 best practice** for hybrid search + rerank |
| `geosi_knowledge/` | `KnowledgeManager`, `WorkflowMemory`, `QueryMemory`, `FeedbackMemory`, 15 built-in workflow templates | Good learning-loop concept; persistence is files/JSON, not concurrency-safe |
| `geosi_data/` | SQLAlchemy + GeoAlchemy2 PostGIS layer, ORM models, `PostGISManager` (GeoDataFrame ↔ PostGIS) | Functional; **default credentials and no migrations** |
| `geosi_server/` | FastAPI REST API (14 endpoints: `/rag/*`, `/workflow/*`, `/layers/*`, `/health`, `/stats`) | Functional; **zero authentication, wide-open CORS** |

### 2.2 Confirmed strengths (verified in source, keep these)
- **Dynamic tool discovery** (`qgis_bridge.py`) instead of 2000+ lines of hardcoded tool wrappers — this *is* the "tool calling" pattern from the course (LangChain `Tool`/`@tool`), applied at platform scale.
- **Hybrid retrieval with Reciprocal Rank Fusion**, `RRF_score(d) = Σ 1/(k+rank_i(d))`, `k=60` — this is the exact formula and constant recommended in the course's Chroma DB/RAG readings and confirmed as 2026 industry standard.
- **Cross-encoder reranking** (`sentence_transformers.CrossEncoder`) with graceful fallback — matches the course's "retrieve top‑k, rerank" pattern and 2026 guidance ("retrieve 20, rerank to 5").
- **Local-only embeddings** (BAAI/bge-large-en-v1.5) — no external API dependency for the knowledge layer, good for cost and data residency.
- **Learning loop**: `learn_from_execution()` writes back to `WorkflowMemory`/`QueryMemory`/`FeedbackMemory`/PostGIS — a genuine "agent that improves from feedback," aligned with the course's Reflexion/feedback-memory patterns.
- **Graceful degradation** everywhere (Qdrant, PostGIS, Ollama are all optional with fallbacks) — good resilience design.

### 2.3 Confirmed gaps (found via direct source inspection)

| # | Finding | File(s) | Why it matters (course concept it violates) |
|---|---|---|---|
| G1 | LLM plan output parsed via `json.loads(text)` / `response_format: json_object`, **not** function-calling / Pydantic-validated schema | `agent.py:579`, `parser.py:708-757` | Course "Structured Outputs for Tool Calling" + "Pydantic models" modules explicitly warn this is unreliable at scale — must move to tool-calling with typed schemas |
| G2 | FastAPI server has **no authentication middleware**, wildcard CORS `allow_origins=["*"]` combined with `allow_credentials=True` (an invalid/insecure combination) | `geosi_server/app.py` | Any FastAPI production checklist; this is an open door to any origin |
| G3 | Default PostGIS credentials hardcoded as fallback: `postgresql+psycopg2://geosi:geosi@localhost:5432/geosi` | `geosi_data/database.py` | Will ship to prod if `DATABASE_URL` is forgotten — classic secret-management failure |
| G4 | Dynamic SQL built with f-strings: `f"SELECT * FROM {table_name}"`, `f"SELECT COUNT(*) FROM {table}"` | `geosi_data/postgis_manager.py:128,228` | SQL-injection surface if `table_name` ever derives from user/LLM input |
| G5 | Tool execution accepts LLM-chosen parameters and runs `processing.run()` directly; no allow/deny/ask tiering, no dry-run, no human confirmation for destructive ops (overwrite, delete, drop) | `qgis_bridge.py`, `executor.py` | Course's "Manual Tool Calling" module explicitly teaches **allow / ask / deny** permission tiers before execution — this is the #1 pattern GeoSI is missing |
| G6 | No LLM-output guardrails (prompt-injection filtering on RAG-retrieved doc content before it re-enters the planning prompt) | `agent.py`, `knowledge_manager.py` | RAG content is untrusted; OWASP Agentic Top‑10 2026 calls this the "canonical kill chain": indirect prompt injection → excessive agency → improper output handling |
| G7 | No evaluation harness (no RAGAS/DeepEval, no golden query set, no regression gate) | *(absent)* | Course stresses "always test your results — a little tuning can make a big difference"; 2026 practice requires CI-gated eval before any prompt/index change ships |
| G8 | No tracing/observability (no LangSmith/Langfuse-equivalent spans for retrieve→rerank→plan→execute) | *(absent)* | Cannot debug production failures or measure retrieval vs. generation failure split |
| G9 | Memory persistence split across JSON files (`~/.geosi/*.json`) + Qdrant + PostGIS with no single source of truth, no migrations (Alembic), no backup/restore story | `geosi_knowledge/*`, `geosi_data/*` | Data loss / drift risk; not multi-user safe |
| G10 | Single global in-process `GeoSI` engine instance (`_engine = None` singleton in `app.py`) — no per-user/session isolation, no concurrency control | `geosi_server/app.py` | Breaks multi-tenant use; conversation/state bleed across requests |
| G11 | No containerization, no CI/CD, no plugin packaging/signing pipeline despite Phase 6/7 being on the roadmap already | *(absent)* | Roadmap correctly lists Docker/CI-CD as "most important next 6 months" — needs concrete specs, which this PRD supplies |
| G12 | `gdf.eval(expression)` used for user-suppliable field expressions | `geosi_engine/tools/portable.py:191` | Pandas `eval` can execute arbitrary-ish expressions depending on engine; needs `engine="python"` disabled + expression allow-listing |
| G13 | No standardized external tool protocol — GeoSI reinvents tool discovery/execution instead of exposing it as MCP, which several independent open-source projects (`qgis-mcp`, `gis-mcp`) already do for QGIS | `qgis_bridge.py` | Course's "Agentic AI Protocols" reading identifies MCP as the emerging standard for AI↔tool connections; not adopting it isolates GeoSI from the wider MCP-client ecosystem (Claude Desktop, Cursor, VS Code, etc.) |

---

## 3. What to KEEP / ADD / MODIFY / REMOVE

This is the direct answer to *"what all things can I include and remove"* — organized by course concept.

### 3.1 KEEP (already correct — do not rebuild)

| Component | Reason to keep |
|---|---|
| Dynamic QGIS tool discovery via `processingRegistry()` | Superior to hardcoded tool lists; matches "tool calling" pattern generically applied |
| Hybrid RRF retriever (k=60) + cross-encoder reranker | Matches 2026 best-practice hybrid-search reference architectures exactly |
| Local BGE embeddings, no external embedding API | Cost/latency/data-residency win; keep as default, allow pluggable providers (see §3.2) |
| `KnowledgeManager.learn_from_execution()` feedback loop | Genuine Reflexion-style memory; extend, don't replace |
| Optional/graceful-degradation design for Qdrant/PostGIS/Ollama | Correct resilience pattern for an on-prem/desktop-first tool |
| 15 built-in workflow templates | Good cold-start knowledge base; expand, keep the mechanism |
| FastAPI as the server framework | Right choice; add security middleware, don't switch frameworks |

### 3.2 ADD (new capabilities, mapped to course concepts)

| Add | Course concept it implements | Target module |
|---|---|---|
| **Structured, schema-validated planning** — replace free-text JSON parsing with Pydantic models bound as tool schemas (`ExecutionPlan`, `ToolStep`, `ValidatedParameters`) and function/tool-calling on every LLM provider (Ollama function-calling, Gemini function-calling, Claude tool-use) | "Structured Outputs for Tool Calling", "Pydantic for LLM Tool Calls" | `geosi_engine/agent.py`, `geosi_engine/models.py` |
| **Permission-tiered execution** (`allow` / `ask` / `deny`) with a policy table keyed by algorithm ID + destructive-flag detection (overwrite, delete, drop, truncate) | "Manual Tool Calling in LangChain" (allow/ask/deny pattern), OWASP Agentic Top‑10 "excessive agency" | `geosi_engine/executor.py` (new `PermissionEngine`) |
| **Reflection / self-critique step** before execution: a lightweight "critic" pass that re-checks the plan against retrieved GIS docs + past failures (`FeedbackMemory`) before running, and (optionally) a post-execution reflection pass that retries with a corrected plan on failure | "Building a Reflection Agent with LangGraph", Reflexion pattern | New `geosi_engine/reflection.py` |
| **Stateful graph orchestration** for multi-step workflows (parse → retrieve context → plan → validate → permission-check → execute → reflect → learn) modeled as an explicit state machine with checkpointing, instead of an implicit call chain | "LangGraph Workflows", StateGraph/nodes/edges, durable execution | Refactor `geosi_engine/__init__.py` facade into a `StateGraph`-equivalent (LangGraph itself, or an internal `WorkflowGraph`) |
| **MCP server surface** exposing GeoSI tools (buffer, clip, NDVI, workflow-suggest, rag-search) as MCP tools/resources/prompts, in addition to the existing FastAPI REST API | "Agentic AI Protocols" — MCP as the interoperability standard; validated by existing `qgis-mcp`/`gis-mcp` open-source projects | New `geosi_mcp/` package (FastMCP-based) |
| **Guardrail layer**: input sanitization on RAG-retrieved content (strip/flag "ignore previous instructions" patterns) before it enters the LLM prompt; output guardrails before executing any tool call | Course "harmful_content_safety"/prompt-injection awareness; 2026 OWASP Agentic Top‑10 | `geosi_engine/guardrails.py` (new) |
| **Evaluation harness**: RAGAS-style metrics (context precision, context recall, faithfulness, answer relevancy) on a curated golden query set + DeepEval-style CI gate for prompt/index regressions | Course "Always test your results" + 2026 RAGAS/DeepEval/Langfuse standard | New `geosi_eval/` package + CI job |
| **Observability/tracing**: OpenTelemetry spans around retrieve → rerank → plan → validate → execute → learn, exported to Langfuse (self-hostable) or an OTel collector | Course RAG pipeline diagrams; 2026 production RAG requires trace-level debugging | Cross-cutting; instrument `rag_service.py`, `agent.py`, `executor.py` |
| **AuthN/AuthZ on FastAPI**: API-key or OAuth2/JWT bearer auth, per-tenant scoping, rate limiting (e.g., `slowapi`/API gateway) | Any production API checklist; directly fixes G2 | `geosi_server/app.py` + new `geosi_server/auth.py` |
| **Secrets management**: `.env`/Docker secrets/Vault for `DATABASE_URL`, `QDRANT_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`; no hardcoded fallback credentials | Fixes G3 | `geosi_data/database.py`, deployment config |
| **Database migrations** (Alembic) for the PostGIS schema | Production data-layer hygiene | `geosi_data/` |
| **Containerization + CI/CD**: multi-stage Dockerfile(s) for `geosi_server` + Qdrant + PostGIS via `docker-compose`, GitHub Actions pipeline (lint → unit tests → eval gate → build → scan → push) | Roadmap Phase 6/7, already prioritized; this PRD gives concrete spec | New `Dockerfile`, `docker-compose.yml`, `.github/workflows/ci.yml` |
| **QGIS plugin packaging pipeline**: automated `plugin_upload.py` to the official QGIS Plugin Repository, semantic versioning, `qgisMinimumVersion` compatibility matrix testing (3.28 LTR → 3.4x/4.x) | Plugin distribution best practice validated against sibling projects (`qgis-mcp`, `qgis_salah_mcp`) which ship via the same repo | Release engineering track |
| **Multi-session/multi-tenant engine management**: replace the single global `_engine` singleton with a session-scoped engine pool (keyed by API key/session ID), each with its own `ConversationManager`/`StateManager` | Fixes G10 | `geosi_server/app.py` |
| **Human-in-the-loop (HITL) approval UI** in the QGIS dock: any `ask`-tier tool call shows a diff/preview ("This will overwrite `roads.shp` — Approve / Reject") before running | Course "Manual Tool Calling" + "Reflection" patterns + 2026 guardrail guidance (HITL is the durable control, not filtering alone) | `geosi_plugin/prompt_dock.py` |
| **Structured audit log** of every tool call: user, query, tool, params, result, latency, success/fail — immutable append-only store | 2026 EU AI Act / enterprise guardrail checklist requirement | `geosi_data/metadata_repository.py` extension |

### 3.3 MODIFY (keep the idea, change the implementation)

| Existing | Change to |
|---|---|
| `json.loads()` parsing of raw LLM text in `agent.py`/`parser.py` | Provider-native structured output / function calling with a Pydantic `ExecutionPlan` schema; validate before use; reject and retry (max 2 retries) on schema failure instead of silently falling through |
| `postgis_manager.py` f-string SQL (`f"SELECT * FROM {table_name}"`) | Use `sqlalchemy.sql.quoted_name` / identifier allow-listing against a known-table registry; never interpolate unchecked strings into SQL |
| `gdf.eval(expression)` in `portable.py` | Restrict to a vetted subset of column arithmetic (no `engine="python"`), or replace with a safe expression AST evaluator |
| CORS `allow_origins=["*"]` + `allow_credentials=True` | Explicit origin allow-list per deployment environment; disable credentials if origins must stay broad |
| File-based memory (`~/.geosi/*.json`) | Migrate to PostGIS tables (already exist: `geosi_workflow_history`, etc.) as the single source of truth; JSON files become a local dev-only cache |
| `Reranker` fallback ("score fallback" when `CrossEncoder` unavailable) | Keep as a documented degraded mode, but make it loud (logged + surfaced in `/health`) so it's never silently running in prod without the reranker |
| Roadmap Phases 3–10 (loosely ordered) | Re-sequence per §10 below — security/observability/CI move **before** GraphRAG/computer-vision, because those are launch blockers, not feature adds |

### 3.4 REMOVE / DO NOT BUILD

| Remove / avoid | Reason |
|---|---|
| Any plan to keep the default `geosi:geosi` PostGIS credentials reachable in any deployed environment | Must be impossible to deploy without explicit secret injection (fail closed, not fail open) |
| Wildcard CORS + credentials in production configs | Security hole; not a "someday" fix |
| Deleted v1 hardcoded tool files (`tools/vector.py`, `tools/raster.py`, `tools/terrain.py`, `tools/network.py`, `tools/ai_ml.py`, `tools/cartography.py`, `tools/temporal.py`) | Correctly already removed in v2 — do **not** resurrect them; dynamic discovery supersedes them entirely |
| Unauthenticated "any origin can call `/layers/{name}` DELETE" pattern | Destructive endpoint with zero auth is unacceptable in prod |
| Silent unbounded LLM-cascade retries (Ollama → Gemini → Claude → rules) with no budget/timeout ceiling | Needs an explicit per-request timeout + cost budget or it can hang/loop indefinitely under provider outage |
| Treating in-memory Qdrant / SQLite-style local mode as a production deployment target | Fine for dev; document clearly as non-production, require a real Qdrant cluster + PostGIS instance for prod |
| Building yet another bespoke agent-loop framework from scratch for the "graph orchestration" ask | Adopt or align with an existing durable-execution runtime (LangGraph, or a minimal internal state machine following the same primitives) rather than reinventing checkpointing/HITL/streaming |

---

## 4. Product Vision & Goals

**Vision:** GeoSI is the geospatial "co-pilot" that plans, validates, executes, and *remembers* GIS workflows — safely enough to run unattended on read-only queries and with human oversight on anything destructive, exposed both as a QGIS plugin and as a standards-based MCP/REST service usable from Claude Desktop, Cursor, or any MCP-compatible client.

### Goals for v3 (Production)
1. Zero unauthenticated write paths to PostGIS, Qdrant, or the QGIS project.
2. 100% of LLM-generated execution plans pass schema validation before any tool executes.
3. Every destructive operation requires an explicit `ask`-tier human approval by default.
4. p95 end-to-end latency (query → first executed step) under 4s for cached/rule-based ops, under 12s for full RAG+LLM planning.
5. RAGAS faithfulness ≥ 0.85 and context precision ≥ 0.75 on a 150+ query golden set before any release ships.
6. One-command reproducible deployment (`docker compose up`) for server + Qdrant + PostGIS.
7. GeoSI tools consumable via **both** the QGIS plugin UI **and** an MCP server, so any MCP client can drive QGIS through GeoSI's validated planning/permission layer (not raw PyQGIS code execution).

### Non-goals (v3)
- Full autonomous execution with no human oversight (deferred; Phase 10 "Autonomous GIS" remains a *research* track, not a v3 requirement).
- Multi-cloud managed hosting (v3 targets self-hosted/on-prem + single-cloud reference deployment).

---

## 5. Target Architecture (v3)

```
┌───────────────────────────────────────────────────────────────────────────┐
│  Clients                                                                  │
│  • QGIS Plugin (dock UI, HITL approval dialog)                            │
│  • MCP Clients (Claude Desktop, Cursor, VS Code, custom agents)  ← NEW    │
│  • REST API consumers (internal apps, dashboards)                         │
└───────────────┬───────────────────────────┬───────────────────────────────┘
                │ engine.run(query)          │ MCP tool calls
                ▼                            ▼
┌───────────────────────────────────────────────────────────────────────────┐
│  API / Protocol Layer                                                     │
│  geosi_server/  (FastAPI + AuthN/AuthZ + rate limiting)         MODIFIED  │
│  geosi_mcp/     (FastMCP server: tools/resources/prompts)         NEW     │
└───────────────┬───────────────────────────────────────────────────────────┘
                ▼
┌───────────────────────────────────────────────────────────────────────────┐
│  Orchestration Layer (stateful graph)                            NEW      │
│  parse → retrieve_context → plan(structured) → guardrail_check →          │
│  permission_gate → execute → reflect(on failure) → learn → audit_log      │
│  Checkpointed state, per-session isolation, timeouts + budgets            │
└───────┬─────────────┬────────────────┬───────────────────┬────────────────┘
        │              │                │                   │
        ▼              ▼                ▼                   ▼
┌──────────────┐ ┌────────────┐  ┌──────────────┐   ┌──────────────────┐
│ geosi_engine │ │ geosi_rag  │  │ geosi_knowledge│  │ geosi_data       │
│ Registry     │ │ Hybrid RRF │  │ Workflow/Query │  │ PostGIS (Alembic │
│ StateManager │ │ + Reranker │  │ /Feedback mem  │  │  migrations,     │
│ Structured   │ │ (KEEP)     │  │ (migrate JSON  │  │  audit log table)│
│ Pydantic plan│ │            │  │  → PostGIS)    │  │                  │
│ PermissionEng│ │            │  │                │  │                  │
│ (all NEW/MOD)│ │            │  │                │  │                  │
└──────────────┘ └────────────┘  └────────────────┘  └──────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────────┐
│  Observability & Eval (cross-cutting, NEW)                                │
│  OpenTelemetry traces → Langfuse; RAGAS/DeepEval CI gate;                 │
│  structured audit log; per-tool reliability dashboard (already partially │
│  present via FeedbackMemory — extend into Grafana/Prometheus)            │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Functional Requirements

### FR-1 Structured Planning
- FR-1.1 The agent MUST request tool/function-calling structured output (native to each provider) instead of free-text JSON.
- FR-1.2 Every `ExecutionPlan`/`ToolStep` MUST validate against a Pydantic schema; on validation failure, retry once with the error fed back to the model, then fall back to rule-based planning.
- FR-1.3 Plans MUST include a machine-readable `risk_level` field (`read_only` / `mutating` / `destructive`) computed from the target algorithm's metadata (e.g., writes to disk, `OVERWRITE` params, `DROP`/`DELETE` semantics).

### FR-2 Permission-Tiered Execution
- FR-2.1 Every tool invocation MUST be checked against a policy table: `allow` (auto-run), `ask` (require UI/API confirmation), `deny` (block).
- FR-2.2 Default policy: `read_only` → allow; `mutating` → ask; `destructive` → ask + require typed confirmation phrase.
- FR-2.3 Users/admins MUST be able to override policy per algorithm ID via configuration.

### FR-3 Guardrails
- FR-3.1 All content retrieved from RAG/Qdrant MUST be scanned for injection patterns ("ignore previous instructions", role-override phrases) before being placed into the planning prompt; flagged content is annotated, not silently trusted.
- FR-3.2 Tool outputs MUST be validated against expected types/ranges before being surfaced to the user or fed into subsequent steps.

### FR-4 Reflection / Self-Correction
- FR-4.1 On execution failure, the agent MUST retrieve similar past failures from `FeedbackMemory`, generate a corrected plan, and retry up to N=2 times before surfacing the error to the user.
- FR-4.2 A lightweight pre-execution critic pass MUST flag plans that contradict retrieved documentation or have a known low tool-reliability score (from `FeedbackMemory.get_tool_reliability()`).

### FR-5 MCP Interface
- FR-5.1 GeoSI MUST expose a FastMCP server surfacing: `run_query` (planning + execution), `search_gis_docs`, `suggest_workflow`, `list_layers`, `get_layer` as MCP tools; workflow templates as MCP prompts; layer/project state as MCP resources.
- FR-5.2 MCP tool calls MUST pass through the same permission/guardrail/audit pipeline as the QGIS plugin and REST API (no bypass path).
- FR-5.3 MCP server MUST support token-based auth (`GEOSI_MCP_TOKEN`), following the pattern already validated by comparable open-source QGIS MCP servers.

### FR-6 Multi-Session Engine
- FR-6.1 The FastAPI server MUST manage a pool of `GeoSI` engine instances keyed by session/API key, not a single global singleton.
- FR-6.2 Each session MUST have isolated `ConversationManager` and `StateManager` state with a configurable TTL/eviction policy.

### FR-7 Evaluation & Observability
- FR-7.1 A golden query set (≥150 natural-language GIS queries with expected tool/plan) MUST exist and run in CI on every change to prompts, retriever config, or agent logic.
- FR-7.2 RAGAS metrics (context precision, context recall, faithfulness, answer relevancy) MUST be computed against the golden set; release blocked if faithfulness < 0.85 or context precision < 0.75.
- FR-7.3 Every pipeline stage (retrieve, rerank, plan, validate, execute, learn) MUST emit an OpenTelemetry span with latency, token usage (where applicable), and outcome; exported to a self-hosted Langfuse (or equivalent) instance.

### FR-8 Data Layer
- FR-8.1 PostGIS schema changes MUST be managed via Alembic migrations; no ad-hoc `create_all()` in production.
- FR-8.2 All memory currently stored as `~/.geosi/*.json` (query history, feedback history) MUST be migrated to PostGIS-backed tables as the system of record; local JSON remains only as an offline/dev cache.
- FR-8.3 An immutable `geosi_audit_log` table MUST record every tool execution (who/what/when/params/result/risk_level/approval status).

### FR-9 Deployment
- FR-9.1 A multi-stage Dockerfile MUST build `geosi_server` with pinned dependency versions; `docker-compose.yml` MUST orchestrate `geosi_server` + Qdrant + PostGIS(+PostGIS extension) + (optional) Ollama.
- FR-9.2 CI (GitHub Actions) MUST run: lint (ruff/flake8) → type-check (mypy) → unit tests → eval gate (FR-7.2) → security scan (pip-audit/Trivy) → build → push to registry.
- FR-9.3 The QGIS plugin MUST be packaged and versioned for submission to the official QGIS Plugin Repository, with a compatibility matrix tested against QGIS 3.28 LTR and the current stable release.

---

## 7. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Security** | AuthN (API key or OAuth2/JWT) on all FastAPI and MCP endpoints; no wildcard CORS + credentials; secrets via env/Vault, never hardcoded fallbacks; SQL identifiers allow-listed, never string-interpolated; dependency scanning in CI (pip-audit, Trivy) given the 2026 supply-chain incidents affecting LLM-agent dependencies (e.g., compromised LiteLLM package) |
| **Reliability** | Per-request timeout budget across the LLM cascade (Ollama→Gemini→Claude→rules); circuit breaker if a provider fails N times in a window; idempotent tool execution where possible |
| **Performance** | p95 latency targets in §4; retrieval top-k tuned (retrieve ~20–50, rerank to 5, per 2026 hybrid-search guidance); Qdrant HNSW `ef_search`/`ef_construction`/`M` tuned and documented per collection |
| **Scalability** | Stateless FastAPI workers behind a load balancer; session state externalized to PostGIS/Redis, not in-process, so horizontal scaling doesn't break multi-turn conversations |
| **Observability** | Structured logs (JSON), OTel traces, `/health` and `/stats` extended with per-provider circuit-breaker state and reranker-fallback status |
| **Compliance/Auditability** | Immutable audit log (FR-8.3); data retention policy for query/feedback history; alignment with emerging AI-agent governance expectations (EU AI Act-style lineage/oversight for higher-risk destructive operations) |
| **Portability** | Full stack runs via `docker compose up` on a laptop; QGIS plugin remains installable standalone without the server (degrades to local/portable tools only) |
| **Maintainability** | Type-annotated, tested (≥70% coverage on `geosi_engine`/`geosi_rag`), Alembic-managed schema, CI-enforced lint/type-check |

---

## 8. Data Model Additions

| New/changed table | Purpose |
|---|---|
| `geosi_audit_log` | Immutable record of every tool call (session, user, query, tool, params, risk_level, approval_status, result, latency, timestamp) |
| `geosi_query_history` (replaces JSON) | Migrated from `~/.geosi/query_history.json`; adds `session_id`, `user_id` |
| `geosi_feedback_history` (replaces JSON) | Migrated from `~/.geosi/feedback_history.json`; adds indexing on `tool_id` for fast reliability lookups |
| `geosi_policy_overrides` | Per-deployment `allow/ask/deny` overrides keyed by algorithm ID |
| `geosi_eval_runs` | Stores RAGAS/DeepEval run results over time for regression tracking |

---

## 9. API & Protocol Changes

| Endpoint/surface | Change |
|---|---|
| `POST /rag/*`, `/workflow/*`, `/layers/*` | Add `Authorization: Bearer <token>` requirement; scope `/layers/{name}` DELETE to an "admin" role |
| CORS | Replace `allow_origins=["*"]` with environment-driven allow-list; never combine wildcard with `allow_credentials=True` |
| New: `geosi_mcp` server | `run_query`, `search_gis_docs`, `suggest_workflow`, `list_layers`, `get_layer`, `approve_pending_action` (for `ask`-tier confirmations from an MCP client) |
| New: `POST /admin/policy` | CRUD for `geosi_policy_overrides` (admin-only) |
| `GET /health` | Extend to report: reranker mode (cross-encoder vs. fallback), provider circuit-breaker states, DB/Qdrant connectivity, audit-log write health |

---

## 10. Roadmap (re-sequenced — security & production hardening moved earlier)

| Phase | Focus | Notes |
|---|---|---|
| **P1 — Done** | Query parser, planning agent, execution engine, tool registry, state manager, QGIS plugin, FastAPI, NDVI/watershed workflows | Existing |
| **P2 — Done/keep** | PostGIS, Qdrant, GIS doc corpus, RAG service, workflow knowledge base | Existing, keep as-is |
| **P3 (NEW — was missing)** | **Production hardening**: AuthN/AuthZ, secrets management, CORS fix, SQL-injection fix, structured/Pydantic outputs, permission-tiered execution, guardrails, audit log | *Moved up — was implicitly Phase 6/7 before; these are launch blockers, not later polish* |
| **P4 (NEW)** | **Evaluation & observability**: golden query set, RAGAS/DeepEval CI gate, OpenTelemetry + Langfuse tracing | *Moved up from nothing → must precede any "supervisor agent"/LangGraph work so regressions are caught* |
| **P5 (was P6/P7)** | **Containerization + CI/CD**: Docker/Compose, GitHub Actions pipeline, dependency scanning | Same content as original roadmap, sequenced earlier |
| **P6 (NEW)** | **MCP server** exposing GeoSI tools to the broader MCP client ecosystem, with permission/guardrail parity to the plugin | *New, informed by existing `qgis-mcp`/`gis-mcp` prior art* |
| **P7 (was P3/P4)** | Stateful graph orchestration (LangGraph-style: reflection loop, supervisor/worker agents, multi-agent RAG for remote sensing) | Same intent as original Phase 3/4, now built on a hardened + evaluated foundation |
| **P8 (was P5)** | Computer-vision agent (YOLO/SAM/U-Net) for imagery-based feature extraction | Unchanged intent |
| **P9 (was P8)** | Kubernetes for horizontal scaling of `geosi_server`/Qdrant | Unchanged intent |
| **P10 (was P9)** | Neo4j / GraphRAG for spatial-relationship knowledge graphs | Unchanged intent |
| **P11 (was P10)** | Autonomous GIS (research track, human-oversight retained by default) | Unchanged intent, explicitly framed as *not* a v3 requirement |

---

## 11. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| LLM cascade produces a syntactically valid but semantically wrong destructive plan | FR-2 permission tiers + FR-4 reflection/critic pass + mandatory HITL for `destructive` risk level |
| Prompt injection via poisoned GIS documentation ingested into RAG corpus | FR-3.1 guardrail scanning; source-trust tagging on ingested docs; sandboxed ingestion pipeline |
| Supply-chain compromise of an LLM/agent dependency (mirrors 2026 LiteLLM PyPI incident) | Pin exact versions, run `pip-audit`/Trivy in CI, avoid `uvx`-style "always fetch latest" install patterns for anything touching production |
| Multi-tenant state bleed from the current global singleton engine | FR-6 session-scoped engine pool |
| RAG index/prompt changes silently degrade answer quality | FR-7 CI-gated RAGAS evaluation before merge |
| Team ships fast and skips the permission/guardrail layer under deadline pressure | Treat FR-2/FR-3/FR-8.3 as launch-blocking acceptance criteria, not "nice to have," per 2026 OWASP Agentic Top‑10 guidance that these are the only durable controls against unsolved prompt-injection risk |

---

## 12. Sources (2026 research grounding this PRD)

- RAG hybrid search / RRF / reranking best practice: digitalapplied.com "Hybrid Search: BM25, Vector & Reranking Reference 2026"; lushbinary.com "RAG Production Guide 2026"; callmissed.com "RAG Best Practices 2026."
- Vector database selection for production: pingcap.com "Best Vector Databases for RAG 2026."
- Agent orchestration frameworks: alphabold.com "LangGraph Agents in Production"; docs.langchain.com "LangGraph overview"; speakeasy.com "Choosing an agent framework"; alicelabs.ai "Best AI Agent Frameworks 2026."
- MCP for QGIS/GIS (prior art validating the MCP recommendation): `github.com/jjsantos01/qgis_mcp`, `github.com/nkarasiak/qgis-mcp`, `github.com/mahdin75/gis-mcp`, `plugins.qgis.org/plugins/qgis_mcp_plugin`.
- Agentic AI security / guardrails: helpnetsecurity.com "Prompt injection still drives most agentic AI security failures in production"; iternal.ai "AI Agent Security Checklist 2026"; atlan.com "Enterprise AI Agent Guardrails Checklist 2026"; truefoundry.com "Enterprise AI Agent Security Solutions Buyer's Guide 2026."
- RAG evaluation/observability: atlan.com and helpmetest.com "LLM Evaluation Frameworks Compared 2026" (RAGAS/DeepEval/Langfuse); genai.qa "DeepEval vs RAGAS 2026"; getmaxim.ai "5 Best RAG Evaluation Tools 2026."

*(All sources reflect publicly available guidance current as of mid-2026; re-verify before major architecture decisions, as this space moves quickly.)*

---

## 13. Acceptance Criteria for "Production Ready" (Definition of Done)

- [ ] No default/fallback secrets reachable in any deployed config
- [ ] All API/MCP surfaces authenticated; CORS locked down
- [ ] 100% of tool executions pass through structured validation + permission gate
- [ ] Destructive operations require explicit human approval, logged in `geosi_audit_log`
- [ ] RAG-retrieved content guardrail-scanned before entering planning prompts
- [ ] Golden-set RAGAS evaluation passing thresholds, wired into CI
- [ ] Full stack deployable via `docker compose up` with documented `.env.example`
- [ ] MCP server live, permission/guardrail parity with plugin, token-authenticated
- [ ] QGIS plugin passes packaging checks for official repository submission
- [ ] On-call runbook + `/health` dashboard covering all external dependencies (Qdrant, PostGIS, LLM providers)

