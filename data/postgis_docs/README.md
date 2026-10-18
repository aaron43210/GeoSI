# GeoSI Documentation Corpus — PostGIS Docs

Place PostGIS documentation here.

## What to put here
- PostGIS spatial function reference (ST_Buffer, ST_Intersects, etc.)
- PostGIS raster documentation
- Spatial indexing (GiST) documentation
- SQL patterns for geospatial queries

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/postgis_docs/ --collection gis_docs
```
