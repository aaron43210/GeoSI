# GeoSI v2 — QGIS Workflow Templates
## Ready-to-use workflow examples for the GIS Execution Agent

Each workflow below maps directly to an `ExecutionPlan` with `ToolSteps`.

---

## 1. Buffer + Clip (Most Common Workflow)

**Task:** "Buffer hospitals by 500m and clip to study area boundary"

```python
# QGIS Processing chain
import processing

# Step 1: Buffer
buffered = processing.run("native:buffer", {
    'INPUT': 'hospitals',
    'DISTANCE': 500,
    'SEGMENTS': 5,
    'END_CAP_STYLE': 0,
    'JOIN_STYLE': 0,
    'MITER_LIMIT': 2,
    'DISSOLVE': False,
    'OUTPUT': 'memory:'
})['OUTPUT']

# Step 2: Clip to boundary
result = processing.run("native:clip", {
    'INPUT': buffered,
    'OVERLAY': 'study_area_boundary',
    'OUTPUT': '/output/hospitals_buffer_500m_clipped.gpkg'
})
```

---

## 2. Spatial Join (Count Points in Polygons)

**Task:** "Count how many schools are in each district"

```python
joined = processing.run("native:joinattributesbylocation", {
    'INPUT': 'districts',
    'PREDICATE': [0],          # intersects
    'JOIN': 'schools',
    'JOIN_FIELDS': [],
    'METHOD': 0,               # one-to-many
    'DISCARD_NONMATCHING': False,
    'PREFIX': 'school_',
    'OUTPUT': 'memory:'
})

# Then count by district
counted = processing.run("native:countpointsinpolygon", {
    'POLYGONS': 'districts',
    'POINTS': 'schools',
    'WEIGHT': None,
    'CLASSFIELD': None,
    'FIELD': 'school_count',
    'OUTPUT': '/output/districts_school_count.gpkg'
})
```

---

## 3. Watershed Delineation

**Task:** "Delineate watershed for pour point at coordinates X,Y"

```python
# Step 1: Fill sinks
filled = processing.run("grass7:r.fill.dir", {
    'input': 'dem_raster',
    'output': 'memory:',
    'direction': 'memory:'
})

# Step 2: Flow direction
flow_dir = processing.run("grass7:r.watershed", {
    'elevation': 'dem_raster',
    'drainage': 'memory:',
    'accumulation': 'memory:',
    'threshold': 1000,
    'flags': 's'
})

# Step 3: Extract watershed
watershed = processing.run("grass7:r.water.outlet", {
    'input': flow_dir['drainage'],
    'output': 'memory:',
    'coordinates': '36.8219,1.2921'   # pour point lon,lat
})

# Step 4: Vectorize
vector = processing.run("gdal:polygonize", {
    'INPUT': watershed['output'],
    'BAND': 1,
    'FIELD': 'watershed_id',
    'OUTPUT': '/output/watershed.gpkg'
})
```

---

## 4. NDVI from Sentinel-2

**Task:** "Calculate NDVI from Sentinel-2 image"

```python
# Using Raster Calculator
ndvi = processing.run("qgis:rastercalculator", {
    'EXPRESSION': '("B8@1" - "B4@1") / ("B8@1" + "B4@1")',
    'LAYERS': ['sentinel2_image.tif'],
    'CELLSIZE': 0,
    'EXTENT': None,
    'CRS': None,
    'OUTPUT': '/output/ndvi.tif'
})

# Alternative: gdal:rastercalculator for large files
ndvi_gdal = processing.run("gdal:rastercalculator", {
    'INPUT_A': 'sentinel2_image.tif',
    'BAND_A': 8,    # NIR
    'INPUT_B': 'sentinel2_image.tif',
    'BAND_B': 4,    # RED
    'FORMULA': '(A - B) / (A + B)',
    'NO_DATA': -9999,
    'RTYPE': 5,     # Float32
    'OPTIONS': 'COMPRESS=LZW',
    'OUTPUT': '/output/ndvi.tif'
})
```

---

## 5. Zonal Statistics

**Task:** "Calculate average elevation within each district polygon"

```python
zonal_stats = processing.run("native:zonalstatisticsfb", {
    'INPUT': 'districts',
    'INPUT_RASTER': 'dem_raster',
    'RASTER_BAND': 1,
    'COLUMN_PREFIX': 'elev_',
    'STATISTICS': [0, 1, 2, 3, 4, 5, 6],  # count,sum,mean,median,std,min,max
    'OUTPUT': '/output/districts_elevation_stats.gpkg'
})
```

---

## 6. Raster Slope + Aspect

**Task:** "Calculate slope and aspect from DEM"

```python
# Slope
slope = processing.run("native:slope", {
    'INPUT': 'dem_raster',
    'Z_FACTOR': 1,
    'OUTPUT': '/output/slope_degrees.tif'
})

# Aspect
aspect = processing.run("native:aspect", {
    'INPUT': 'dem_raster',
    'Z_FACTOR': 1,
    'OUTPUT': '/output/aspect_degrees.tif'
})

# Hillshade (for visualisation)
hillshade = processing.run("native:hillshade", {
    'INPUT': 'dem_raster',
    'Z_FACTOR': 1,
    'AZIMUTH': 315,
    'V_ANGLE': 45,
    'OUTPUT': '/output/hillshade.tif'
})
```

---

## 7. Dissolve by Attribute

**Task:** "Merge all polygons with the same district_name into one polygon"

```python
dissolved = processing.run("native:dissolve", {
    'INPUT': 'parcels',
    'FIELD': ['district_name'],
    'SEPARATE_DISJOINT': False,
    'OUTPUT': '/output/districts_dissolved.gpkg'
})
```

---

## 8. Nearest Facility Analysis

**Task:** "Find the nearest hospital for each village"

```python
nearest = processing.run("native:shortestpathpointtopoint", {
    'INPUT': 'road_network',
    'STRATEGY': 0,          # Shortest path
    'START_POINT': 'villages',
    'END_POINT': 'hospitals',
    'OUTPUT': '/output/nearest_hospital_paths.gpkg'
})

# Simpler: straight-line nearest neighbour
nearest_simple = processing.run("native:joinbynearest", {
    'INPUT': 'villages',
    'INPUT_2': 'hospitals',
    'FIELDS_TO_COPY': ['hospital_name', 'hospital_type'],
    'DISCARD_NONMATCHING': False,
    'PREFIX': 'nearest_',
    'NEIGHBORS': 1,
    'MAX_DISTANCE': None,
    'OUTPUT': '/output/villages_nearest_hospital.gpkg'
})
```

---

## 9. Landslide Susceptibility (Multi-Criteria)

**Task:** "Map landslide susceptibility"

```python
# Weight each factor (example weights)
SLOPE_WEIGHT = 0.35
ASPECT_WEIGHT = 0.15
GEOLOGY_WEIGHT = 0.25
LANDUSE_WEIGHT = 0.15
DISTANCE_FAULT_WEIGHT = 0.10

# Step 1: Reclassify each factor to 1-5 scale
slope_reclass = processing.run("native:reclassifybytable", {
    'INPUT_RASTER': 'slope',
    'RASTER_BAND': 1,
    'TABLE': [0, 10, 1, 10, 20, 2, 20, 35, 3, 35, 50, 4, 50, 90, 5],
    'NO_DATA': -9999,
    'OUTPUT': 'memory:'
})

# Step 2: Weighted overlay (Raster Calculator)
susceptibility = processing.run("qgis:rastercalculator", {
    'EXPRESSION': (
        f'("slope_reclass@1" * {SLOPE_WEIGHT}) + '
        f'("aspect_reclass@1" * {ASPECT_WEIGHT}) + '
        f'("geology_reclass@1" * {GEOLOGY_WEIGHT}) + '
        f'("landuse_reclass@1" * {LANDUSE_WEIGHT}) + '
        f'("distance_fault_reclass@1" * {DISTANCE_FAULT_WEIGHT})'
    ),
    'LAYERS': ['slope_reclass', 'aspect_reclass', 'geology_reclass',
               'landuse_reclass', 'distance_fault_reclass'],
    'OUTPUT': '/output/landslide_susceptibility.tif'
})
```

---

## 10. Reproject Layer

**Task:** "Reproject shapefile from WGS84 to UTM Zone 37N"

```python
reprojected = processing.run("native:reprojectlayer", {
    'INPUT': 'input_layer',
    'TARGET_CRS': 'EPSG:32637',  # UTM Zone 37N
    'OPERATION': '+proj=pipeline +step +proj=unitconvert +xy_in=deg '
                 '+step +proj=utm +zone=37 +ellps=WGS84',
    'OUTPUT': '/output/layer_utm37n.gpkg'
})
```

---

## Common EPSG Codes Quick Reference

| EPSG | Name | Use Case |
|---|---|---|
| 4326 | WGS 84 (Geographic) | GPS coordinates, global |
| 3857 | Web Mercator | Web maps (Google, OSM) |
| 32636 | UTM Zone 36N | East Africa |
| 32637 | UTM Zone 37N | East Africa (Kenya, Ethiopia) |
| 32632 | UTM Zone 32N | West Africa |
| 4263 | Minna (Nigeria) | Nigeria national |
| 20135 | Adindan UTM 35N | East Africa |
| 21035 | Arc 1960 UTM 35S | Tanzania |
