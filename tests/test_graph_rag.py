# -*- coding: utf-8 -*-
"""
GeoSI v2 — GraphRAG Engine Tests (Phase P10, FR-8.4)
Tests RRF fusion, graceful Neo4j fallback, Research agent graph_search.
"""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock


# ── GraphRAGEngine Tests ───────────────────────────────────────────────────

def test_graph_rag_rrf_merge_combines_both_lists():
    """RRF must merge results from both Qdrant and Neo4j lists."""
    from geosi_engine.graph_rag import GraphRAGEngine, GraphRAGResult

    engine = GraphRAGEngine(engine=MagicMock(), neo4j_client=MagicMock())

    list_a = [
        GraphRAGResult(text="NDVI vegetation index", source="qdrant", score=0.9),
        GraphRAGResult(text="Random Forest classification", source="qdrant", score=0.8),
    ]
    list_b = [
        GraphRAGResult(text="Random Forest classification", source="neo4j", score=0.7),
        GraphRAGResult(text="Landsat data processing", source="neo4j", score=0.6),
    ]

    fused = engine._rrf_merge(list_a, list_b, top_k=5)

    # "Random Forest classification" appears in both lists — should rank highest
    assert len(fused) >= 2
    texts = [r.text for r in fused]
    assert "Random Forest classification" in texts
    # The dual-appearing document should have higher RRF score
    rf_result = next(r for r in fused if "Random Forest" in r.text)
    other_results = [r for r in fused if "Random Forest" not in r.text]
    if other_results:
        # RF result got a boost from appearing in both lists
        assert rf_result.score >= min(r.score for r in other_results)


def test_graph_rag_rrf_source_marked_as_merged():
    """RRF output results must have source='merged'."""
    from geosi_engine.graph_rag import GraphRAGEngine, GraphRAGResult

    engine = GraphRAGEngine(engine=MagicMock(), neo4j_client=MagicMock())
    list_a = [GraphRAGResult(text="doc1", source="qdrant", score=0.9)]
    list_b = [GraphRAGResult(text="doc2", source="neo4j", score=0.8)]
    fused = engine._rrf_merge(list_a, list_b, top_k=5)
    assert all(r.source == "merged" for r in fused)


def test_graph_rag_rrf_top_k_respected():
    """RRF must return exactly top_k results when candidates > top_k."""
    from geosi_engine.graph_rag import GraphRAGEngine, GraphRAGResult

    engine = GraphRAGEngine(engine=MagicMock(), neo4j_client=MagicMock())
    list_a = [GraphRAGResult(text=f"doc_{i}", source="qdrant") for i in range(20)]
    list_b = [GraphRAGResult(text=f"graph_{i}", source="neo4j") for i in range(20)]

    fused = engine._rrf_merge(list_a, list_b, top_k=5)
    assert len(fused) == 5


def test_graph_rag_rrf_empty_lists():
    """RRF on empty lists must return empty list without error."""
    from geosi_engine.graph_rag import GraphRAGEngine

    engine = GraphRAGEngine(engine=MagicMock(), neo4j_client=MagicMock())
    fused = engine._rrf_merge([], [], top_k=5)
    assert fused == []


def test_graph_rag_rrf_deduplication():
    """RRF must deduplicate identical text entries."""
    from geosi_engine.graph_rag import GraphRAGEngine, GraphRAGResult

    engine = GraphRAGEngine(engine=MagicMock(), neo4j_client=MagicMock())
    # Same text from both sources
    list_a = [GraphRAGResult(text="NDVI formula", source="qdrant", score=0.9)]
    list_b = [GraphRAGResult(text="NDVI formula", source="neo4j", score=0.8)]

    fused = engine._rrf_merge(list_a, list_b, top_k=5)
    # Must not produce duplicate entries
    texts = [r.text for r in fused]
    assert len(texts) == len(set(texts)), "Duplicate texts in RRF output"


def test_graph_rag_search_no_knowledge_no_crash():
    """GraphRAG search with no knowledge/Neo4j must return empty gracefully."""
    from geosi_engine.graph_rag import GraphRAGEngine

    mock_engine = MagicMock()
    mock_engine.knowledge = None
    mock_neo4j = MagicMock()
    mock_neo4j.available = False

    rag = GraphRAGEngine(engine=mock_engine, neo4j_client=mock_neo4j)
    results = rag.search("NDVI vegetation analysis", top_k=5)
    assert isinstance(results, list)
    # Should return empty without crashing


def test_graph_rag_qdrant_search_with_results():
    """Qdrant search results must be wrapped in GraphRAGResult objects."""
    from geosi_engine.graph_rag import GraphRAGEngine

    mock_result = MagicMock()
    mock_result.text = "NDVI is computed from NIR and RED bands"
    mock_result.score = 0.92
    mock_result.metadata = {}

    mock_engine = MagicMock()
    mock_engine.knowledge.search_gis_docs.return_value = [mock_result]

    mock_neo4j = MagicMock()
    mock_neo4j.available = False

    rag = GraphRAGEngine(engine=mock_engine, neo4j_client=mock_neo4j)
    results = rag._qdrant_search("NDVI", "gis_docs", 5)

    assert len(results) == 1
    assert results[0].source == "qdrant"
    assert "NDVI" in results[0].text


def test_graph_rag_cross_reference_unavailable_neo4j():
    """cross_reference must return [] when Neo4j is unavailable."""
    from geosi_engine.graph_rag import GraphRAGEngine

    mock_neo4j = MagicMock()
    mock_neo4j.available = False

    rag = GraphRAGEngine(engine=MagicMock(), neo4j_client=mock_neo4j)
    result = rag.cross_reference("some-dataset-id")
    assert result == []


def test_graph_rag_rrf_constant_k_parameter():
    """RRF constant k=60 must be used (standard recommendation)."""
    from geosi_engine.graph_rag import _RRF_K
    assert _RRF_K == 60, f"RRF k should be 60, got {_RRF_K}"


# ── Research Agent GraphRAG Integration ──────────────────────────────────

def test_research_agent_graph_search_no_knowledge():
    """graph_search must succeed with no knowledge/Neo4j."""
    from geosi_engine.agents.research import ResearchAgent

    engine = MagicMock()
    engine.knowledge = None
    permission = MagicMock()
    agent = ResearchAgent(engine=engine, permission_agent=permission)

    result = agent.graph_search("NDVI vegetation analysis", top_k=5)
    assert result.success
    assert result.query == "NDVI vegetation analysis"
    assert isinstance(result.papers, list)


def test_research_agent_graph_search_returns_research_result():
    """graph_search must return a properly typed ResearchResult."""
    from geosi_engine.agents.research import ResearchAgent, ResearchResult

    agent = ResearchAgent(engine=MagicMock(knowledge=None), permission_agent=MagicMock())
    result = agent.graph_search("spatial autocorrelation", top_k=3)

    assert isinstance(result, ResearchResult)
    assert result.query == "spatial autocorrelation"
    assert isinstance(result.citations, list)
    assert isinstance(result.guardrail_flags, list)


def test_research_agent_has_graph_search_method():
    """ResearchAgent must expose a graph_search method (P10 requirement)."""
    from geosi_engine.agents.research import ResearchAgent
    assert hasattr(ResearchAgent, "graph_search"), \
        "ResearchAgent missing graph_search() — P10 requirement not met"
