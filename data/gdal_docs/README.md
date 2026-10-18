# GeoSI Documentation Corpus — GDAL Docs

Place GDAL/OGR documentation here.

## What to put here
- GDAL raster driver documentation
- OGR vector format documentation
- gdal_translate, gdalwarp, ogr2ogr usage guides
- GDAL Python API reference

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/gdal_docs/ --collection gis_docs
```
