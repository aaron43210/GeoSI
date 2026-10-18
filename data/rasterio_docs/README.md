# GeoSI Documentation Corpus — Rasterio Docs

Place Rasterio documentation here.

## What to put here
- Rasterio quickstart and tutorials
- Rasterio API reference (rasterio.open, .read, .write)
- CRS handling, windowed reading, masking
- Rasterio + NumPy patterns

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/rasterio_docs/ --collection gis_docs
```
