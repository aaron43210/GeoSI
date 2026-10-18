# GeoSI Documentation Corpus — QGIS Docs

Place QGIS documentation files here for ingestion into the GIS knowledge base.

## Supported Formats
- `.md` — Markdown
- `.txt` — Plain text
- `.html` — HTML pages
- `.pdf` — PDF documents
- `.rst` — reStructuredText

## What to put here
- QGIS User Guide chapters
- QGIS Processing algorithm documentation
- QGIS tutorials and how-tos
- Plugin documentation

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/qgis_docs/ --collection gis_docs
```
