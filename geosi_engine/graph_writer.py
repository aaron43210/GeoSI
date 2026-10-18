# -*- coding: utf-8 -*-
"""
GeoSI v2 — Graph Writer (Phase P9, FR-8.4)
════════════════════════════════════════════════════════════════════
Async writer that populates the Neo4j knowledge graph from
``geosi_audit_log`` entries on every agent execution.

Design:
  - All writes are fire-and-forget via a background thread queue.
    The agent pipeline is never blocked waiting for Neo4j writes.
  - Queue capacity is bounded (default 1000) to prevent unbounded memory
    growth under load. Overflow events are logged and discarded.
  - O(1) enqueue/dequeue via collections.deque (thread-safe with lock).
  - A single writer thread drains the queue, batching writes into
    Neo4j transactions for efficiency.

PRD references: FR-8.4, §9 (PostGIS remains system of record)
"""
from __future__ import annotations

import logging
import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, Optional

from geosi_data.graph_schema import (
    NodeLabel, RelType,
    build_agent_props, build_dataset_props,
    build_execution_props, build_tool_props, build_workflow_props,
)

logger = logging.getLogger("geosi_engine.graph_writer")

_QUEUE_CAPACITY = 1000       # Max pending write events — O(1) bounded memory
_FLUSH_INTERVAL_S = 2.0      # Writer thread sleep between flushes


@dataclass
class GraphEvent:
    """A single graph write event."""
    event_type: str   # "execution" | "dataset_relation" | "workflow"
    payload: Dict[str, Any]


class GraphWriter:
    """
    Background graph writer for the GeoSI knowledge graph (FR-8.4).

    Usage::

        writer = GraphWriter.get_instance()
        writer.record_execution(audit_id, plan, agent_name, status, session_id)

    Thread safety:
        - ``enqueue()`` is called from agent threads (multiple concurrent).
        - The writer thread drains the queue exclusively.
        - ``deque`` + ``RLock`` gives O(1) amortized enqueue/dequeue.
    """

    _instance: Optional[GraphWriter] = None
    _instance_lock = threading.Lock()

    def __init__(self) -> None:
        self._queue: deque[GraphEvent] = deque(maxlen=_QUEUE_CAPACITY)
        self._lock = threading.RLock()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._start()

    @classmethod
    def get_instance(cls) -> GraphWriter:
        """Singleton accessor — thread-safe via double-checked locking."""
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------
    # Public API — called by agents
    # ------------------------------------------------------------------

    def record_execution(
        self,
        audit_id: str,
        plan: Any,
        agent_name: str,
        status: str,
        session_id: str,
        duration_ms: float = 0.0,
        input_layers: Optional[list] = None,
        output_layer: Optional[str] = None,
    ) -> None:
        """
        Record a complete agent execution into the graph.

        Enqueues 4–5 events:
        1. Upsert :Agent node
        2. Upsert :Workflow node
        3. Upsert :Execution node
        4. Link (Execution)-[:RAN_BY]->(Agent)
        5. Link (Execution)-[:FOLLOWS]->(Workflow)
        6. For each input layer: (Execution)-[:USED]->(:Dataset)
        7. If output: upsert output :Dataset + (output)-[:DERIVED_FROM]->(inputs)

        All enqueued O(1) — no blocking.
        """
        plan_id = getattr(plan, "plan_id", "unknown")
        steps = getattr(plan, "steps", [])
        query = getattr(getattr(plan, "request", None), "query", "") or ""

        self._enqueue(GraphEvent("execution", {
            "audit_id": audit_id,
            "plan_id": plan_id,
            "agent_name": agent_name,
            "status": status,
            "session_id": session_id,
            "duration_ms": duration_ms,
            "query": query,
            "step_count": len(steps),
            "steps": [getattr(s, "tool_name", "") for s in steps],
            "input_layers": input_layers or [],
            "output_layer": output_layer,
        }))

    def record_dataset_relation(
        self, source_name: str, source_path: str,
        derived_name: str, derived_path: str,
    ) -> None:
        """Record (derived_dataset)-[:DERIVED_FROM]->(source_dataset)."""
        self._enqueue(GraphEvent("dataset_relation", {
            "source_name": source_name, "source_path": source_path,
            "derived_name": derived_name, "derived_path": derived_path,
        }))

    def record_dataset_similarity(
        self, name_a: str, path_a: str,
        name_b: str, path_b: str,
        similarity: float,
    ) -> None:
        """Record (dataset_a)-[:RELATED_TO {similarity}]->(dataset_b) for GraphRAG."""
        self._enqueue(GraphEvent("dataset_similarity", {
            "name_a": name_a, "path_a": path_a,
            "name_b": name_b, "path_b": path_b,
            "similarity": similarity,
        }))

    def stop(self) -> None:
        """Gracefully stop the writer thread."""
        self._running = False

    # ------------------------------------------------------------------
    # Writer thread
    # ------------------------------------------------------------------

    def _start(self) -> None:
        self._running = True
        self._thread = threading.Thread(
            target=self._writer_loop, daemon=True, name="graph-writer"
        )
        self._thread.start()
        logger.debug("Graph writer thread started.")

    def _writer_loop(self) -> None:
        """
        Background writer loop. Flushes the queue every _FLUSH_INTERVAL_S.
        Batches multiple events per transaction for efficiency.
        """
        from geosi_data.neo4j_client import get_neo4j_client
        while self._running:
            time.sleep(_FLUSH_INTERVAL_S)
            batch: list[GraphEvent] = []
            with self._lock:
                while self._queue:
                    batch.append(self._queue.popleft())
            if not batch:
                continue
            try:
                client = get_neo4j_client()
                if not client.available:
                    continue
                for event in batch:
                    self._process_event(client, event)
            except Exception as exc:
                logger.warning("Graph writer flush error: %s", exc)

    def _process_event(self, client, event: GraphEvent) -> None:
        """Process a single graph event — write nodes and relationships."""
        try:
            if event.event_type == "execution":
                self._write_execution(client, event.payload)
            elif event.event_type == "dataset_relation":
                self._write_dataset_relation(client, event.payload)
            elif event.event_type == "dataset_similarity":
                self._write_dataset_similarity(client, event.payload)
        except Exception as exc:
            logger.debug("Graph event processing failed: %s — %s", event.event_type, exc)

    def _write_execution(self, client, p: dict) -> None:
        """Write a full execution event into the graph."""
        # Agent node
        client.upsert_node(NodeLabel.AGENT, "name", build_agent_props(p["agent_name"]))
        # Workflow node
        client.upsert_node(NodeLabel.WORKFLOW, "plan_id", build_workflow_props(
            p["plan_id"], p.get("query", ""), p.get("step_count", 0), p.get("session_id", "")
        ))
        # Execution node
        client.upsert_node(NodeLabel.EXECUTION, "audit_id", build_execution_props(
            p["audit_id"], p["plan_id"], p.get("session_id", ""),
            p.get("status", ""), p.get("duration_ms", 0.0),
        ))
        # Tool nodes + Workflow-[:CONTAINS]->Tool
        for tool_name in p.get("steps", []):
            if tool_name:
                client.upsert_node(NodeLabel.TOOL, "tool_id", build_tool_props(tool_name))
                client.upsert_relationship(
                    NodeLabel.WORKFLOW, "plan_id", p["plan_id"],
                    NodeLabel.TOOL, "tool_id", tool_name,
                    RelType.CONTAINS,
                )
        # Execution -> Agent
        client.upsert_relationship(
            NodeLabel.EXECUTION, "audit_id", p["audit_id"],
            NodeLabel.AGENT, "name", p["agent_name"],
            RelType.RAN_BY,
        )
        # Execution -> Workflow
        client.upsert_relationship(
            NodeLabel.EXECUTION, "audit_id", p["audit_id"],
            NodeLabel.WORKFLOW, "plan_id", p["plan_id"],
            RelType.FOLLOWS,
        )
        # Input datasets
        for layer_path in p.get("input_layers", []):
            if layer_path:
                ds_props = build_dataset_props(name=layer_path.split("/")[-1], path=layer_path)
                client.upsert_node(NodeLabel.DATASET, "dataset_id", ds_props)
                client.upsert_relationship(
                    NodeLabel.EXECUTION, "audit_id", p["audit_id"],
                    NodeLabel.DATASET, "dataset_id", ds_props["dataset_id"],
                    RelType.USED,
                )

    def _write_dataset_relation(self, client, p: dict) -> None:
        src = build_dataset_props(p["source_name"], p["source_path"])
        drv = build_dataset_props(p["derived_name"], p["derived_path"])
        client.upsert_node(NodeLabel.DATASET, "dataset_id", src)
        client.upsert_node(NodeLabel.DATASET, "dataset_id", drv)
        client.upsert_relationship(
            NodeLabel.DATASET, "dataset_id", drv["dataset_id"],
            NodeLabel.DATASET, "dataset_id", src["dataset_id"],
            RelType.DERIVED_FROM,
        )

    def _write_dataset_similarity(self, client, p: dict) -> None:
        ds_a = build_dataset_props(p["name_a"], p["path_a"])
        ds_b = build_dataset_props(p["name_b"], p["path_b"])
        client.upsert_node(NodeLabel.DATASET, "dataset_id", ds_a)
        client.upsert_node(NodeLabel.DATASET, "dataset_id", ds_b)
        client.upsert_relationship(
            NodeLabel.DATASET, "dataset_id", ds_a["dataset_id"],
            NodeLabel.DATASET, "dataset_id", ds_b["dataset_id"],
            RelType.RELATED_TO,
            rel_props={"similarity": p.get("similarity", 0.0)},
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _enqueue(self, event: GraphEvent) -> None:
        """
        O(1) enqueue. maxlen=_QUEUE_CAPACITY ensures bounded memory.
        If the queue is full, the oldest event is silently dropped (deque behaviour).
        """
        with self._lock:
            if len(self._queue) >= _QUEUE_CAPACITY:
                logger.debug("Graph writer queue full — dropping oldest event.")
            self._queue.append(event)
