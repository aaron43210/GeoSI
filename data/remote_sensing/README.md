# GeoSI Documentation Corpus — Remote Sensing

Place remote sensing tutorials and documentation here.

## What to put here
- Spectral index formulas (NDVI, NDWI, NDBI, EVI, SAVI)
- Image classification techniques
- Change detection methodologies
- SAR processing guides
- Atmospheric correction documentation

## Ingestion
```bash
python -m geosi_rag.ingest_cli --source data/remote_sensing/ --collection gis_docs
```
