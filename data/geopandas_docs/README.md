# GeoSI Documentation Corpus — GeoPandas Docs

Place GeoPandas documentation here.

## What to put here
- GeoPandas user guide
- GeoDataFrame operations (spatial joins, overlays, dissolve)
- Geometry operations and CRS management
- I/O (read_file, to_file, to_postgis)

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/geopandas_docs/ --collection gis_docs
```
