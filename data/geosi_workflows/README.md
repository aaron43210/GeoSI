# GeoSI Documentation Corpus — GeoSI Workflows

Place GeoSI internal workflow documentation here.

## What to put here
- Workflow examples (YAML, JSON, or Markdown)
- GeoSI usage patterns and best practices
- Custom tool documentation
- Integration guides

## Auto-populated
This directory is also auto-populated by the knowledge layer when GeoSI
learns from successful workflow executions.

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/geosi_workflows/ --collection gis_workflows
```
