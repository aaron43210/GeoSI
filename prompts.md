# GeoSI Prompt Cookbook

A curated catalog of natural-language prompts that map cleanly onto
GeoSI's 125 tools. Use the layer names exactly as they appear in your
QGIS Layers panel - GeoSI will tell you `Layer 'X' not found` if a
name does not match.

The bundled sample data (`Data_06_2_2026/`) contains:

- `Schools` (points)
- `Assets` (points)
- `Kerala` (state polygon)
- `TVM_Corp` (Thiruvananthapuram Corporation polygon)
- `Population_Kerala.csv` (tabular, joinable)

Replace the layer names below with your own where applicable.

---

## 1. Vector Prompts

### 1.1 Basic inspection

- `Count features in Schools`
- `Show me the CRS of Kerala`
- `How many assets are in the Assets layer`
- `What is the extent of TVM_Corp`
- `Summarize Schools`

### 1.2 Proximity and buffering

- `Buffer Schools by 500 meters`
- `Buffer Assets by 1 km and dissolve the result`
- `Create a 250 m buffer around Schools, 10 segments`
- `Find Assets within 2 km of Schools`
- `Which Schools are within 3 km of TVM_Corp`

### 1.3 Overlay operations

- `Intersect Schools with TVM_Corp`
- `Clip Assets to Kerala`
- `Union Schools and Assets`
- `Difference between Kerala and TVM_Corp`
- `Symmetric difference of Schools and Assets`
- `Clip the buffer of Schools to TVM_Corp`

### 1.4 Geometry operations

- `Compute centroids of TVM_Corp`
- `Simplify Kerala with tolerance 100`
- `Smooth Kerala geometry`
- `Convex hull of Schools`
- `Concave hull of Schools with alpha 0.4`
- `Voronoi polygons for Schools`
- `Delaunay triangulation of Schools`
- `Bounding boxes for Assets`
- `Minimum enclosing circle of Schools`
- `Dissolve TVM_Corp by name`

### 1.5 Attribute and spatial joins

- `Spatial join Schools with TVM_Corp using intersects`
- `Nearest neighbor join Schools to Assets`
- `Count points in polygon: Assets per TVM_Corp`
- `Extract Schools where type = 'Government'`
- `Filter Assets where value > 1000`
- `Select features in Schools by location within TVM_Corp`

### 1.6 Transformation and CRS

- `Reproject Kerala to EPSG:4326`
- `Reproject Schools to EPSG:3857`
- `Add area, perimeter, and length fields to TVM_Corp`
- `Fix geometries in Assets`
- `Multipart to singleparts for Kerala`

### 1.7 Sampling and grids

- `Random points in extent: 500 points inside TVM_Corp`
- `Create a 1 km grid over Kerala`
- `Points along Schools every 100 meters`
- `Snap Schools to a 50 meter grid`

### 1.8 Cartography and export

- `Export Schools as GeoJSON`
- `Export TVM_Corp as Shapefile`
- `Export Kerala to KML`
- `Export Assets as CSV with geometry`
- `Geocode 'Kazhakkoottam Trivandrum'`

### 1.9 Validation and QA

- `Check Assets for invalid geometries`
- `Detect duplicate features in Schools`
- `Find null or empty geometries in Kerala`
- `Check topology of TVM_Corp for self-intersections`
- `Validate CRS consistency between Schools and Kerala`

### 1.10 Statistics

- `Mean value field of Assets`
- `Standard deviation of Population in Population_Kerala`
- `Histogram of Schools by type`
- `Summary statistics for Assets`

---

## 2. Raster Prompts

(These assume a raster layer loaded as `DEM`, `Landsat_NIR`, etc. -
replace with your actual layer names.)

### 2.1 Terrain analysis

- `Calculate slope from DEM`
- `Calculate aspect from DEM`
- `Generate hillshade from DEM at azimuth 315 altitude 45`
- `Generate contours from DEM every 10 meters`
- `Calculate terrain ruggedness index (TRI) from DEM`
- `Calculate topographic position index (TPI) from DEM`
- `Compute flow direction from DEM`
- `Compute flow accumulation from DEM`
- `Run viewshed from DEM at observer point (76.95, 8.52)`
- `Delineate watershed from DEM outlet at (76.95, 8.52)`

### 2.2 Raster algebra and indices

- `Calculate NDVI from Landsat_red and Landsat_NIR`
- `Calculate NDWI from Landsat_green and Landsat_NIR`
- `Calculate NDBI from Landsat_SWIR and Landsat_NIR`
- `Calculate EVI from Landsat_red, Landsat_NIR and Landsat_blue`
- `Raster calculator: (A - B) / (A + B) on Landsat_NIR and Landsat_red`

### 2.3 Zonal and focal operations

- `Zonal statistics of DEM in TVM_Corp (mean, min, max)`
- `Zonal statistics of NDVI in Kerala`
- `Focal mean on DEM with 3x3 window`
- `Sample DEM at Schools points`

### 2.4 Reclassification and masking

- `Reclassify DEM into 5 elevation classes`
- `Mask DEM by Kerala`
- `Clip raster DEM to TVM_Corp`
- `Set nodata to -9999 in DEM`

### 2.5 Resampling and reprojection

- `Resample DEM to 30 meter resolution`
- `Reproject DEM to EPSG:4326`
- `Mosaic DEM_tile_1 and DEM_tile_2`
- `Align NDVI to DEM grid`

### 2.6 Interpolation (vector -> raster)

- `IDW interpolation of Population from Population_Kerala, cell size 500`
- `Kriging of Population from Population_Kerala`
- `Nearest neighbor interpolation of Schools elevation, cell 100`
- `Rasterize TVM_Corp to 50 meter grid`
- `Kernel density of Schools with radius 2000 meters`

### 2.7 Classification and ML

- `Unsupervised classify DEM into 5 clusters`
- `Supervised classify Landsat using training_samples`
- `Detect anomalies in NDVI`

### 2.8 Temporal and change detection

- `Change detection between NDVI_2015 and NDVI_2024`
- `Difference of DEM_before and DEM_after`
- `Time series aggregation of NDVI monthly`

---

## 3. Network and Accessibility Prompts

- `Shortest path in Roads from (76.95, 8.52) to (76.98, 8.55)`
- `Service area in Roads from Schools within 2000 meters`
- `Isochrone of 15 minutes driving from Schools using Roads`
- `Origin-destination matrix from Schools to Assets over Roads`
- `Catchment area of Schools over Roads with 1500 meter threshold`

---

## 4. AI / ML and Spatial Statistics Prompts

- `Cluster Schools using K-means with 5 clusters`
- `Cluster Assets using DBSCAN with eps=500`
- `Find hotspots in Schools using Getis-Ord Gi*`
- `Moran's I autocorrelation of Population in Kerala`
- `Detect anomalies in Assets value field`
- `Predict population density from feature set in Kerala`

---

## 5. Compound / Multi-step Prompts

These showcase multi-step planning. GeoSI chains tools automatically.

- `Buffer Schools by 1 km, intersect with TVM_Corp, then export as GeoJSON`
- `Dissolve Kerala districts by region, compute area, and keep the five largest`
- `Cluster Assets with DBSCAN, then compute the convex hull of each cluster`
- `Clip DEM to TVM_Corp, calculate slope, and reclassify into low/medium/high`
- `Intersect flood_zones with buildings, count affected assets per TVM_Corp`
- `Compute NDVI, mask cloudy pixels, zonal mean by TVM_Corp, export CSV`
- `Shortest path from nearest school to hospital for every house in houses`

---

## 6. Conversation / Meta-commands

These are handled by the dock, not the engine:

- `help`  - example prompts tailored to your loaded layers
- `layers` - list loaded layers with type, geometry, features, CRS
- `tools` - show how many tools are available per category
- `clear` - clear the chat

---

## 7. Error-Path Prompts (expected to fail gracefully)

Useful for demos - verify GeoSI reports clear errors.

- `Buffer hospitals by 500m`  -> when `hospitals` is not loaded,
  GeoSI responds: *"Layer 'hospitals' not found. Available layers:
  Schools, Assets, Kerala, TVM_Corp."*
- `Intersect A with B`  -> when neither A nor B is loaded, GeoSI
  replies with the same pattern.
- `Buffer`  (no layer, no distance) -> GeoSI asks for clarification.

---

## Tips

- Use the **exact layer name** shown in the QGIS Layers panel.
- Units default to **meters**. Say `km`, `miles`, `feet` to override.
- For raster queries, include band names (`red`, `NIR`, etc.) when
  the tool needs them.
- If a compound prompt is too long, split it into two turns - GeoSI
  remembers context.
- Click **LLM -> Test Ollama** to confirm the local LLM is reachable
  before a demo.

Happy mapping.
