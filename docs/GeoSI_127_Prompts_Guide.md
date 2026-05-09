# GeoSI: Comprehensive 127-Tool Prompt Guide

This guide provides exactly **127 ready-to-use natural language prompts** for the GeoSI AI engine, categorized by function. 

> [!IMPORTANT]
> **Data Setup Instructions**
> Before running these prompts, you must load the specific data into your QGIS Layers panel (if using the plugin) or via the API:
> 
> 1. Load `/Users/aaronr/GEO_SUPER_INTELLIGENCE/Data_06_2_2026/Kerala.shp` and name it **Kerala**.
> 2. Load `/Users/aaronr/GEO_SUPER_INTELLIGENCE/Data_06_2_2026/Schools.shp` and name it **Schools**.
> 3. Load `/Users/aaronr/Desktop/DUK/ADVANCED GEOSPATIAL PROGRAMMING/Data_Rasterio_Practise/DEM.tif` and name it **DEM**.
> 4. Load `/Users/aaronr/Desktop/DUK/ADVANCED GEOSPATIAL PROGRAMMING/Data_Rasterio_Practise/LE07_L1TP_144054_20000128_20170213_01_T1_B4.TIF` and name it **Landsat\_B4**.

---

## 1. Vector Operations (40 Tools)
*Operations for points, lines, and polygons.*

1. **Buffer**: `Buffer Schools by 500 meters`
2. **Intersect**: `Intersect Schools with Kerala`
3. **Union**: `Combine Schools and Kerala`
4. **Difference**: `Find difference between Kerala and Schools`
5. **Symmetrical Difference**: `Symmetrical difference of Kerala and Schools`
6. **Clip**: `Clip Schools to Kerala boundary`
7. **Dissolve**: `Dissolve Kerala by DISTRICT field`
8. **Centroid**: `Calculate centroids for Kerala`
9. **Convex Hull**: `Create a convex hull around Schools`
10. **Voronoi**: `Generate Voronoi polygons for Schools`
11. **Delaunay Triangulation**: `Delaunay triangulation for Schools`
12. **Simplify**: `Simplify Kerala geometry by 10 meters`
13. **Smooth**: `Smooth edges of Kerala`
14. **Densify**: `Densify geometries of Kerala`
15. **Multipart to Singlepart**: `Convert Kerala to singlepart`
16. **Merge Layers**: `Merge Kerala and Schools`
17. **Reproject**: `Reproject Schools to EPSG:3857`
18. **Fix Geometries**: `Fix invalid geometries in Kerala`
19. **Spatial Join**: `Spatial join Schools to Kerala`
20. **Nearest Join**: `Find nearest Kerala district for each School`
21. **Select by Location**: `Select Schools that intersect Kerala`
22. **Extract by Attribute**: `Extract from Kerala where DISTRICT='Idukki'`
23. **Extract by Extent**: `Extract Schools within current map extent`
24. **Random Points**: `Generate 100 random points inside Kerala`
25. **Grid Create**: `Create a 1000m grid over Kerala`
26. **Points Along Lines**: `Create points along Kerala boundaries`
27. **Polygonize**: `Convert lines of Kerala to polygons`
28. **Polygons to Lines**: `Convert Kerala polygons to lines`
29. **Explode Lines**: `Explode lines of Kerala`
30. **Extend Lines**: `Extend lines in Kerala`
31. **Offset Line**: `Offset lines of Kerala by 5m`
32. **Bounding Boxes**: `Create bounding boxes for Schools`
33. **Minimum Enclosing Circle**: `Find minimum enclosing circle for Schools`
34. **Concave Hull**: `Create concave hull for Schools`
35. **Aggregate**: `Aggregate attributes in Kerala`
36. **Add Geometry Attributes**: `Calculate area and perimeter for Kerala`
37. **Count Points in Polygon**: `Count Schools inside each Kerala district`
38. **Distance Matrix**: `Calculate distance matrix for Schools`
39. **Mean Coordinates**: `Find mean center of Schools`
40. **Snap to Grid**: `Snap Schools to a 10m grid`

## 2. Raster & Imagery (25 Tools)
*Operations for TIFFs and pixel data.*

41. **NDVI**: `Calculate NDVI from Landsat_B4 and Landsat_B3`
42. **NDWI**: `Calculate NDWI from Landsat imagery`
43. **Zonal Stats**: `Calculate zonal statistics for DEM within Kerala`
44. **Raster Calculator**: `Multiply DEM by 0.3048 to convert feet to meters`
45. **Reclassify**: `Reclassify DEM into 5 elevation zones`
46. **Raster Clip**: `Clip DEM to Kerala boundary`
47. **Raster Clip by Mask**: `Mask DEM using Kerala`
48. **Warp**: `Reproject DEM to EPSG:3857`
49. **Merge Raster**: `Merge DEM with another raster`
50. **Polygonize Raster**: `Convert DEM to polygons`
51. **Rasterize**: `Convert Kerala to raster using DISTRICT field`
52. **Fill NoData**: `Fill nodata values in DEM`
53. **Proximity**: `Calculate raster proximity for DEM`
54. **Roughness**: `Calculate terrain roughness from DEM`
55. **TPI**: `Calculate Topographic Position Index for DEM`
56. **TRI**: `Calculate Terrain Ruggedness Index for DEM`
57. **Translate**: `Convert DEM to a different format`
58. **Build VRT**: `Build virtual raster from DEM`
59. **Sample Raster**: `Sample DEM values at Schools locations`
60. **Band Extract**: `Extract band 1 from Landsat_B4`
61. **RGB Composite**: `Create RGB composite from Landsat bands`
62. **Raster Statistics**: `Calculate global statistics for DEM`
63. **Align Rasters**: `Align DEM to Landsat_B4`
64. **Resample**: `Resample DEM to 30m resolution`
65. **Focal Statistics**: `Calculate 3x3 focal mean on DEM`

## 3. Terrain & Hydrology (10 Tools)
*Operations for elevation models.*

66. **Slope**: `Calculate slope from DEM`
67. **Aspect**: `Calculate aspect direction from DEM`
68. **Hillshade**: `Generate hillshade from DEM with z-factor 2`
69. **Contour**: `Extract 10m contours from DEM`
70. **Viewshed**: `Calculate viewshed from Schools on DEM`
71. **Profile**: `Extract elevation profile across Kerala`
72. **Volume**: `Calculate volume of DEM`
73. **Watershed**: `Delineate watershed basins from DEM`
74. **Flow Direction**: `Calculate flow direction on DEM`
75. **Flow Accumulation**: `Calculate flow accumulation on DEM`

## 4. Network & Routing (8 Tools)
*Operations for road networks and paths.*

76. **Shortest Path**: `Find shortest path in Kerala from 76.5,9.5 to 77.0,10.0`
77. **Service Area**: `Calculate 5km service area around Schools`
78. **Shortest Path (Layer)**: `Find routes from Schools to hospitals`
79. **Network Graph**: `Build network graph from roads`
80. **Split Lines at Points**: `Split road lines at Schools`
81. **Line Intersections**: `Find where roads cross rivers`
82. **Connect Points**: `Connect Schools into a path`
83. **OD Cost Matrix**: `Generate OD matrix between Schools and cities`

## 5. AI, ML & Statistics (10 Tools)
*Predictive modeling and grouping.*

84. **K-Means Cluster**: `Cluster Schools into 5 groups using kmeans`
85. **Spatial Cluster (DBSCAN)**: `Find dense clusters in Schools using DBSCAN`
86. **Hotspot Analysis**: `Find hotspots in Schools using Getis-Ord`
87. **IDW Interpolation**: `Interpolate Schools values using IDW`
88. **Kriging**: `Perform kriging interpolation on Schools`
89. **Point Density**: `Calculate point density for Schools`
90. **Spatial Autocorrelation**: `Calculate Moran's I for Kerala`
91. **Regression Surface**: `Fit regression surface to DEM`
92. **Anomaly Detection**: `Find spatial anomalies in Schools`
93. **Classify Raster**: `Perform unsupervised classification on Landsat`

## 6. Cartography & Export (10 Tools)
*Making maps and moving data.*

94. **Geocode**: `Geocode address 'Trivandrum, Kerala'`
95. **Reverse Geocode**: `Reverse geocode coordinate 76.9, 8.5`
96. **Create Labels**: `Generate labels for Kerala based on DISTRICT`
97. **Style Categorized**: `Apply categorized style to Kerala`
98. **Atlas Export**: `Export atlas mapbook for Kerala districts`
99. **Export GeoJSON**: `Export Schools to GeoJSON file`
100. **Export Shapefile**: `Save Kerala as a new shapefile`
101. **Export Geopackage**: `Export Schools to GeoPackage`
102. **Export CSV**: `Export Kerala attributes to CSV`
103. **Export KML**: `Export Schools to KML`

## 7. Validation & Quality (10 Tools)
*Checking data health.*

104. **Validate Geometry**: `Validate geometries in Kerala`
105. **Topology Check**: `Check topology rules for Kerala`
106. **Remove Duplicates**: `Remove duplicate features from Schools`
107. **Remove Null**: `Remove null geometries from Schools`
108. **Snap Geometries**: `Snap Schools to Kerala boundaries`
109. **Fill Holes**: `Fill polygon holes in Kerala`
110. **Check CRS**: `Check coordinate reference system of Kerala`
111. **Detect Gaps**: `Find gaps between polygons in Kerala`
112. **Detect Overlaps**: `Find overlapping areas in Kerala`
113. **Field Stats**: `Calculate statistics for fields in Kerala`

## 8. Temporal & Time Series (6 Tools)
*For tracking changes.*

114. **Temporal Filter**: `Filter Schools by date established`
115. **Change Detection**: `Detect changes between two Landsat images`
116. **Temporal Aggregate**: `Aggregate temporal data in Kerala`
117. **Time Series Stats**: `Calculate time series statistics`
118. **Animate Temporal**: `Create animation of temporal data`
119. **Temporal Join**: `Join layers by time window`

## 9. Foundation / Portable (8 Tools)
*Core data management commands.*

120. **Load Data**: `Load /Users/aaronr/GEO_SUPER_INTELLIGENCE/Data_06_2_2026/Kerala.shp`
121. **Save Layer**: `Save Schools to output.shp`
122. **Count Features**: `Count how many features are in Schools`
123. **Calculate Field**: `Calculate field Area = $area in Kerala`
124. **Clean Layer**: `Clean the Kerala layer`
125. **List Layers**: `What layers are currently loaded?`
126. **Show Tools**: `List available tools`
127. **Help Command**: `Show help information`
