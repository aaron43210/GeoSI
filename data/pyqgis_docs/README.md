# GeoSI Documentation Corpus — PyQGIS Docs

Place PyQGIS (Python QGIS API) documentation here.

## Supported Formats
`.md`, `.txt`, `.html`, `.pdf`, `.rst`

## What to put here
- PyQGIS Developer Cookbook
- QgsVectorLayer / QgsRasterLayer API docs
- QgsProcessing API reference
- PyQGIS scripting examples

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/pyqgis_docs/ --collection gis_docs
```
