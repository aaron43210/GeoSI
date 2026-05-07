# GeoSI Server

This folder contains a separate FastAPI-based runtime for GeoSI.

The existing `geosi_plugin/` QGIS plugin remains unchanged. This server app is a parallel starting point for running GeoSI outside QGIS.

## Initial Scope

- Health check endpoint
- Tool registry endpoint
- In-memory layer workspace
- Shapefile loading endpoint
- Basic buffer analysis endpoint
- Basic intersect analysis endpoint

## Layout

```text
geosi_server/
  app/
    api/
    core/
    intelligence/
    services/
    main.py
  requirements.txt
```

## Run Locally

1. Create a virtual environment.
2. Install dependencies from `geosi_server/requirements.txt`.
3. Start the API:

```bash
cd geosi_server
uvicorn app.main:app --reload
```

The API will start at `http://127.0.0.1:8000`.

## First Endpoints

- `GET /health`
- `GET /tools`
- `GET /layers`
- `POST /layers/load`
- `POST /analysis/buffer`
- `POST /analysis/intersect`

## Notes

- The current workspace is in memory only.
- Loaded layers are not persisted yet.
- GIS execution currently depends on `geopandas` for vector operations.
- This is the safe first step before extracting more code out of the QGIS plugin.
