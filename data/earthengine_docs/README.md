# GeoSI Documentation Corpus — Google Earth Engine Docs

Place Earth Engine documentation here.

## What to put here
- Earth Engine Python API guides
- ee.Image, ee.ImageCollection operations
- Sentinel-2, Landsat, MODIS dataset documentation
- Earth Engine code examples (NDVI, classification, etc.)

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/earthengine_docs/ --collection gis_docs
```
