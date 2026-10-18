# -*- coding: utf-8 -*-
"""
GeoSI RAG — Document Ingestion CLI
═══════════════════════════════════════════════════════════════════

CLI tool for manual document ingestion into the RAG pipeline.

Usage:
    python -m geosi_rag.ingest_cli --source data/qgis_docs/ --collection gis_docs
    python -m geosi_rag.ingest_cli --source data/gdal_docs/ --collection gis_docs --chunk-size 1024
    python -m geosi_rag.ingest_cli --list-collections
"""

import argparse
import sys
import time
import logging


def main():
    parser = argparse.ArgumentParser(
        prog="geosi_rag.ingest_cli",
        description="GeoSI RAG — Ingest documents into the vector knowledge base",
    )
    parser.add_argument(
        "--source",
        type=str,
        help="Directory containing documents to ingest",
    )
    parser.add_argument(
        "--collection",
        type=str,
        default="gis_docs",
        help="Target Qdrant collection (default: gis_docs)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=512,
        help="Chunk size in characters (default: 512)",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=64,
        help="Chunk overlap in characters (default: 64)",
    )
    parser.add_argument(
        "--list-collections",
        action="store_true",
        help="List all Qdrant collections and exit",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    from geosi_rag.rag_service import RAGService

    print("═" * 60)
    print("  GeoSI RAG — Document Ingestion Pipeline")
    print("═" * 60)
    print()

    # Initialize RAG service
    print("Initializing RAG service...")
    rag = RAGService()

    if not rag.available:
        print(
            "\n❌ RAG service unavailable. Ensure:\n"
            "   1. sentence-transformers is installed\n"
            "   2. qdrant-client is installed\n"
            "   3. Qdrant is running (or using in-memory mode)\n"
        )
        sys.exit(1)

    print(f"  ✅ Embeddings: {rag.embeddings}")
    print(f"  ✅ Qdrant: {rag.store}")
    print()

    # List collections
    if args.list_collections:
        print("Collections:")
        for name in ["gis_docs", "gis_workflows", "geosi_history"]:
            info = rag.store.collection_info(name)
            if info:
                print(f"  📦 {name}: {info['points_count']} points, status={info['status']}")
            else:
                print(f"  ⬜ {name}: not created")
        sys.exit(0)

    # Require --source for ingestion
    if not args.source:
        parser.error("--source is required for document ingestion")

    # Run ingestion
    print(f"Source:     {args.source}")
    print(f"Collection: {args.collection}")
    print(f"Chunk size: {args.chunk_size} chars (overlap: {args.overlap})")
    print()

    start = time.time()
    count = rag.ingest_documents(
        directory=args.source,
        collection=args.collection,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
    elapsed = time.time() - start

    print()
    print("─" * 40)
    if count > 0:
        print(f"✅ Ingested {count} chunks in {elapsed:.1f}s")
        info = rag.store.collection_info(args.collection)
        if info:
            print(f"   Collection '{args.collection}': {info['points_count']} total points")
    else:
        print("⚠  No chunks were ingested. Check that:")
        print(f"   - '{args.source}' contains supported files (.md, .txt, .html, .pdf, .rst)")
        print("   - Files are not empty")
    print()


if __name__ == "__main__":
    main()
