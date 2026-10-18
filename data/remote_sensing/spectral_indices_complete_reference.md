# Remote Sensing Spectral Indices — Complete Reference
## GeoSI v2 Knowledge Base

All formulas use standard band notation. QGIS Raster Calculator expressions provided.

---

## Vegetation Indices

### NDVI — Normalized Difference Vegetation Index
**Formula:** `(NIR - RED) / (NIR + RED)`
**Range:** -1.0 to +1.0
**Interpretation:**
| Value | Meaning |
|---|---|
| < 0.0 | Water, snow, clouds, bare rock |
| 0.0 – 0.2 | Bare soil, sparse vegetation |
| 0.2 – 0.4 | Shrubland, grassland |
| 0.4 – 0.6 | Moderate vegetation (cropland) |
| 0.6 – 1.0 | Dense healthy vegetation, tropical forest |

**Sentinel-2 QGIS Expression:**
```
("B8@1" - "B4@1") / ("B8@1" + "B4@1")
```
**Landsat-8/9 QGIS Expression:**
```
("B5@1" - "B4@1") / ("B5@1" + "B4@1")
```
**Google Earth Engine (Python):**
```python
ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
```
**Limitations:** Saturates in dense canopy; sensitive to soil background; atmosphere affects results.

---

### EVI — Enhanced Vegetation Index
**Formula:** `2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)`
**Range:** -1.0 to +1.0 (practical range: -0.2 to 0.9)
**Advantage over NDVI:** Less affected by atmospheric conditions and soil background
**QGIS Expression (Sentinel-2):**
```
2.5 * ("B8@1" - "B4@1") / ("B8@1" + 6 * "B4@1" - 7.5 * "B2@1" + 1)
```
**GEE (Python):**
```python
evi = image.expression(
    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
    {'NIR': image.select('B8'), 'RED': image.select('B4'), 'BLUE': image.select('B2')}
).rename('EVI')
```

---

### SAVI — Soil Adjusted Vegetation Index
**Formula:** `((NIR - RED) / (NIR + RED + L)) * (1 + L)`  where L = 0.5 (default)
**Best for:** Areas with sparse vegetation where soil background dominates
**QGIS Expression (Sentinel-2):**
```
(("B8@1" - "B4@1") / ("B8@1" + "B4@1" + 0.5)) * 1.5
```

---

## Water Indices

### NDWI — Normalized Difference Water Index (McFeeters 1996)
**Formula:** `(GREEN - NIR) / (GREEN + NIR)`
**Detects:** Surface water bodies
**QGIS Expression (Sentinel-2):**
```
("B3@1" - "B8@1") / ("B3@1" + "B8@1")
```
**Threshold:** Values > 0.3 typically indicate open water

---

### MNDWI — Modified NDWI (Xu 2006)
**Formula:** `(GREEN - SWIR1) / (GREEN + SWIR1)`
**Detects:** Water in urban environments (suppresses built-up land noise)
**QGIS Expression (Sentinel-2):**
```
("B3@1" - "B11@1") / ("B3@1" + "B11@1")
```

---

## Built-up / Urban Indices

### NDBI — Normalized Difference Built-up Index
**Formula:** `(SWIR1 - NIR) / (SWIR1 + NIR)`
**Detects:** Urban areas, impervious surfaces
**QGIS Expression (Sentinel-2):**
```
("B11@1" - "B8@1") / ("B11@1" + "B8@1")
```

---

## Fire / Burn Indices

### NBR — Normalized Burn Ratio
**Formula:** `(NIR - SWIR2) / (NIR + SWIR2)`
**Detects:** Burned areas, fire severity
**QGIS Expression (Sentinel-2):**
```
("B8@1" - "B12@1") / ("B8@1" + "B12@1")
```

### dNBR — Differenced NBR (burn severity)
**Formula:** `NBR_pre - NBR_post`
**Severity classes:**
| dNBR Range | Burn Severity |
|---|---|
| < -0.25 | High post-fire regrowth |
| -0.25 to 0.1 | Unburned |
| 0.1 to 0.27 | Low severity |
| 0.27 to 0.44 | Moderate-low severity |
| 0.44 to 0.66 | Moderate-high severity |
| > 0.66 | High severity |

---

## Land Surface Temperature (LST)

### LST from Landsat-8/9 (Radiometric approach)
**Steps:**
1. Convert DN to Top-of-Atmosphere Radiance: `L = ML * Qcal + AL`
2. Convert Radiance to Brightness Temperature: `T = K2 / ln(K1/L + 1) - 273.15`
3. Calculate NDVI, then Proportion of Vegetation: `Pv = ((NDVI - NDVImin) / (NDVImax - NDVImin))^2`
4. Calculate Land Surface Emissivity: `LSE = 0.004 * Pv + 0.986`
5. Calculate LST: `LST = T / (1 + (0.00115 * T / 1.4388) * ln(LSE))`

**Landsat-9 Constants:** K1 = 774.8853, K2 = 1321.0789 (Band 10)

---

## Sentinel-2 Band Reference

| Band | Name | Wavelength | Resolution | Use |
|---|---|---|---|---|
| B1 | Coastal aerosol | 443 nm | 60 m | Aerosol correction |
| B2 | Blue | 490 nm | 10 m | Water, soil |
| B3 | Green | 560 nm | 10 m | Vegetation peak |
| B4 | Red | 665 nm | 10 m | Chlorophyll |
| B5 | Red Edge 1 | 705 nm | 20 m | Vegetation stress |
| B6 | Red Edge 2 | 740 nm | 20 m | Vegetation stress |
| B7 | Red Edge 3 | 783 nm | 20 m | LAI |
| B8 | NIR (broad) | 842 nm | 10 m | Vegetation |
| B8A | NIR (narrow) | 865 nm | 20 m | Vegetation |
| B9 | Water vapour | 945 nm | 60 m | Atmospheric correction |
| B11 | SWIR 1 | 1610 nm | 20 m | Moisture, fire |
| B12 | SWIR 2 | 2190 nm | 20 m | Geology, fire |

---

## Landsat-8/9 Band Reference

| Band | Name | Wavelength | Resolution | Use |
|---|---|---|---|---|
| B1 | Ultra Blue (Coastal) | 435–451 nm | 30 m | Coastal, aerosol |
| B2 | Blue | 452–512 nm | 30 m | Water, soil |
| B3 | Green | 533–590 nm | 30 m | Vegetation |
| B4 | Red | 636–673 nm | 30 m | Chlorophyll |
| B5 | Near Infrared | 851–879 nm | 30 m | Vegetation |
| B6 | SWIR 1 | 1566–1651 nm | 30 m | Moisture |
| B7 | SWIR 2 | 2107–2294 nm | 30 m | Geology |
| B8 | Panchromatic | 503–676 nm | 15 m | Sharpening |
| B9 | Cirrus | 1363–1384 nm | 30 m | Cloud detection |
| B10 | TIRS 1 | 10.6–11.2 µm | 100 m | Thermal/LST |
| B11 | TIRS 2 | 11.5–12.5 µm | 100 m | Thermal/LST |

---

## Documents You Still Need to Provide

The following documents are behind authentication or paywalls and cannot be auto-fetched:

1. **ESA Sentinel-2 Level-2A Product Specification** (registration required at scihub.copernicus.eu)
2. **USGS Landsat Collection 2 Level-2 Science Product Guide** (downloadable from usgs.gov after login)
3. **GRASS GIS 8.x Module Reference** (large PDF — download from grass.osgeo.org/learn/manuals/)
4. **Your organisation's internal GIS workflows and reports** (proprietary)
5. **SAGA GIS Algorithm documentation** (from saga-gis.org — very large)
6. **FAO Soil Survey Methods** (if doing soil mapping)
7. **Your local government spatial data standards** (country-specific)

To ingest any of these once you have them:
```bash
PYTHONPATH=. python geosi_rag/ingest_cli.py \
  --source /path/to/your/pdf_or_docs \
  --collection gis_docs
```
