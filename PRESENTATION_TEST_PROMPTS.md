# GeoSI Presentation Test Prompts (50 Comprehensive Workflows)

**Data Layers Available:**
- `Assets` - Point layer with 724 features
- `TVM_Corp` - Polygon layer (Thiruvananthapuram Corporation boundary)
- `Schools` - Point layer (school locations)
- `Kerala` - Polygon layer (state boundary)

---

## Section 1: Vector Overlay Operations (10 prompts)

### 1. Clip Assets from TVM_Corp
Clips the Assets layer to the TVM_Corp boundary.
```
"Clip Assets from TVM_Corp"
```

### 2. Intersect Assets with Kerala
Finds overlapping areas between Assets and Kerala.
```
"Intersect Assets with Kerala"
```

### 3. Find union of TVM_Corp and Kerala
Combines TVM_Corp and Kerala into a single layer.
```
"Create a union of TVM_Corp and Kerala"
```

### 4. Symmetric difference of TVM_Corp and Kerala
Shows areas in either TVM_Corp or Kerala but not both.
```
"Find symmetric difference between TVM_Corp and Kerala"
```

### 5. Difference of Kerala and TVM_Corp
Removes TVM_Corp area from Kerala.
```
"Remove TVM_Corp from Kerala and show the difference"
```

### 6. Buffer Assets by 500 meters
Creates 500m buffer zones around each asset.
```
"Buffer all Assets by 500 meters"
```

### 7. Buffer Schools by 1000 meters
Creates 1km buffer zones around each school.
```
"Buffer Schools by 1 kilometer"
```

### 8. Intersect buffered Assets with Schools
Finds schools within buffered asset zones.
```
"Buffer Assets by 500m then intersect with Schools"
```

### 9. Clip Schools to TVM_Corp
Filters schools that fall within Thiruvananthapuram.
```
"Clip Schools to the TVM_Corp boundary"
```

### 10. Union of all layers
Combines all loaded layers.
```
"Create a union of Assets, Schools, and TVM_Corp"
```

---

## Section 2: Spatial Analysis & Proximity (10 prompts)

### 11. Find assets within 2km of schools
Proximity analysis between two point layers.
```
"Find all Assets within 2 kilometers of Schools"
```

### 12. Find schools near TVM boundary
Identifies schools close to TVM_Corp edge.
```
"Find Schools within 1km of the TVM_Corp boundary"
```

### 13. Nearest school to each asset
Calculates closest school for every asset.
```
"For each Asset, find the nearest School"
```

### 14. Distance from assets to Kerala boundary
Measures proximity to state boundary.
```
"Calculate distance from each Asset to Kerala boundary"
```

### 15. Assets outside TVM_Corp buffer
Finds assets far from TVM corporation area.
```
"Find Assets outside a 500m buffer of TVM_Corp"
```

### 16. Schools in high-density asset zones
Identifies schools in asset-rich areas.
```
"Find Schools that are within 1km of 3 or more Assets"
```

### 17. Coverage analysis
Determines spatial coverage of schools.
```
"What percentage of TVM_Corp is covered by 2km school buffers"
```

### 18. Service area planning
Analyzes which assets can serve each school.
```
"For each School, list Assets within 5km"
```

### 19. Accessibility analysis
Evaluates asset accessibility from schools.
```
"Find Assets that are more than 10km from any School"
```

### 20. Intersection density
Measures overlap between buffered layers.
```
"Find the intersection of 500m buffers around Assets and Schools"
```

---

## Section 3: Geometry Operations (10 prompts)

### 21. Centroids of TVM_Corp
Calculates geometric center of TVM_Corp.
```
"Calculate the centroid of TVM_Corp"
```

### 22. Convex hull of Schools
Creates smallest polygon containing all schools.
```
"Create a convex hull around all Schools"
```

### 23. Convex hull of Assets
Creates smallest polygon containing all assets.
```
"Generate convex hull of Assets"
```

### 24. Simplify Kerala boundary
Reduces complexity of state boundary.
```
"Simplify the Kerala geometry"
```

### 25. Simplify TVM_Corp boundary
Reduces TVM_Corp polygon vertices.
```
"Simplify TVM_Corp geometry to reduce complexity"
```

### 26. Smooth Assets locations
Smooth jagged point distributions.
```
"Smooth the geometry of Assets"
```

### 27. Densify Kerala boundary
Adds more vertices to Kerala polygon.
```
"Densify the Kerala geometry for better precision"
```

### 28. Bounding boxes of all layers
Creates rectangular envelopes around features.
```
"Create bounding boxes for all layers"
```

### 29. Minimum enclosing circles around Schools
Finds smallest circle containing each school.
```
"Calculate minimum enclosing circles around Schools"
```

### 30. Voronoi polygons from Assets
Creates Voronoi tessellation around asset points.
```
"Create Voronoi polygons from Assets"
```

---

## Section 4: Advanced Analysis (10 prompts)

### 31. Dissolve Assets by attribute
Merges assets with same attribute value.
```
"Dissolve Assets by attribute to group similar features"
```

### 32. Count assets in TVM_Corp
Counts feature in clipped area.
```
"Count how many Assets are inside TVM_Corp"
```

### 33. Count schools in Kerala
Counts all schools in state.
```
"Count all Schools within Kerala"
```

### 34. Add geometry attributes to Assets
Calculates area and perimeter for assets.
```
"Add geometry attributes like area and perimeter to Assets"
```

### 35. Add geometry attributes to Schools
Calculates spatial properties of school points.
```
"Add geometry attributes to Schools"
```

### 36. Create grid over Kerala
Generates regular grid covering state.
```
"Create a 5km grid over Kerala"
```

### 37. Generate random points in TVM_Corp
Creates random point distribution.
```
"Generate 100 random points within TVM_Corp"
```

### 38. Create points along school connections
Generates intermediate points between schools.
```
"Create points at 1km intervals along lines connecting Schools"
```

### 39. Spatial statistics
Calculates mean coordinates of assets.
```
"Calculate the mean coordinates center of all Assets"
```

### 40. Fix geometries in all layers
Repairs invalid geometries.
```
"Fix any invalid geometries in Assets and Schools"
```

---

## Section 5: Real-World Scenarios (10 prompts)

### 41. Urban planning - School coverage
Analyzes school accessibility across region.
```
"Identify areas within TVM_Corp not covered by 2km school buffers"
```

### 42. Infrastructure planning
Plans infrastructure based on density.
```
"Find clusters of Assets within TVM_Corp for infrastructure planning"
```

### 43. Resource allocation
Determines optimal resource distribution.
```
"For each Asset, count how many Schools are within 5km"
```

### 44. Environmental impact
Analyzes area affected by asset buffers.
```
"Calculate the total area affected by 1km buffers around Assets"
```

### 45. Transportation planning
Routes between assets and schools.
```
"Find the shortest route connecting all Schools through Assets"
```

### 46. Emergency response planning
Identifies service coverage gaps.
```
"Find any Assets that are more than 3km from the nearest School"
```

### 47. Demographic analysis
Analyzes spatial distribution patterns.
```
"Analyze the spatial distribution of Assets and Schools"
```

### 48. Boundary analysis
Studies administrative boundaries.
```
"Find what percentage of Assets are within 1km of TVM_Corp boundary"
```

### 49. Network analysis
Creates connectivity relationships.
```
"Connect each Asset to its 3 nearest Schools"
```

### 50. Regional planning
Multi-layer integration analysis.
```
"Create a composite layer showing Assets and Schools both within TVM_Corp with 1km buffers"
```

---

## Expected Results Summary

| Prompt Group | Expected Output | Complexity |
|---|---|---|
| Overlay Operations | Single polygon layer (clipped/merged) | ⭐ |
| Spatial Analysis | Distance metrics / attribute tables | ⭐⭐ |
| Geometry Operations | Modified/computed geometries | ⭐⭐ |
| Advanced Analysis | Derived features / statistics | ⭐⭐⭐ |
| Real-World Scenarios | Multi-step analysis results | ⭐⭐⭐ |

---

## Testing Workflow

### Before Running Tests:
1. **Load all four layers** into QGIS:
   - `Assets.shp` 
   - `TVM_Corp.shp`
   - `Schools.shp`
   - `Kerala.shp`

2. **Open GeoSI dock** and verify:
   - ✅ Engine ready with 125 tools loaded
   - ✅ All 4 layers synced from QGIS panel
   - ✅ QGIS backend registered

3. **Check settings**:
   - Ollama running (or fallback to rule-based parser)
   - Console open for debug output

### During Tests:
1. Type each prompt into the GeoSI query box
2. Check console for:
   - `✅ QGIS algorithm completed: native:...`
   - `✅ Memory layer added to QGIS project`
3. Verify output layer appears in Layers panel
4. Inspect result for correctness

### Documentation of Results:
- ✅ = Successfully executed
- ⚠️ = Executed but needs review
- ❌ = Failed - check error log

---

## Layer Information

### Assets.shp
- **Type**: Point Vector
- **Features**: 724
- **Geometry**: Point
- **CRS**: EPSG:4326 (WGS84)
- **Source**: Asset locations (utilities, infrastructure, etc.)

### TVM_Corp.shp
- **Type**: Polygon Vector
- **Features**: 1 (or multiple districts)
- **Geometry**: Polygon
- **CRS**: EPSG:4326
- **Source**: Thiruvananthapuram Corporation boundary

### Schools.shp
- **Type**: Point Vector
- **Features**: Variable
- **Geometry**: Point
- **CRS**: EPSG:4326
- **Source**: School locations

### Kerala.shp
- **Type**: Polygon Vector
- **Features**: 1 (state boundary)
- **Geometry**: Polygon
- **CRS**: EPSG:4326
- **Source**: Kerala state administrative boundary

---

## Notes for Presentation

### Strengths to Highlight:
✅ **Natural Language Processing**: User can ask in plain English  
✅ **Multi-Step Workflows**: Complex analyses in one query  
✅ **Real-Time Execution**: Tools run directly in QGIS  
✅ **Error Handling**: Clear messages for missing data  
✅ **125+ Built-in Tools**: Vector, raster, spatial analysis, AI/ML  
✅ **Local-First**: Ollama offline by default  

### Demo Flow:
1. Start with simple overlay (Clip Assets from TVM_Corp)
2. Show proximity analysis (Buffer + Intersect)
3. Demonstrate geometry operations (Centroids, Convex Hull)
4. Run real-world scenario (urban planning coverage)
5. Show fallback behavior (rules-based when offline)

---

## Troubleshooting

### Issue: Output layer not appearing
- **Check**: Are all input layers loaded?
- **Solution**: Reload QGIS, re-add layers
- **Debug**: Check console for "[GeoSI qgis_bridge]" messages

### Issue: "Layer not found" error
- **Check**: Layer name spelling
- **Solution**: Use exact names from Layers panel
- **Example**: "Assets" not "assets" (case-sensitive)

### Issue: Tool takes >30 seconds
- **Cause**: Large dataset or complex analysis
- **Solution**: Try with smaller subset or simpler operation

### Issue: Memory error
- **Cause**: Too many features in operation
- **Solution**: Clip to smaller region first

---

## Generated: 8 May 2026 | GeoSI v1.0.0

---

## Section 6: Raster & Imagery Operations

### 51. Calculate NDVI (Vegetation Index)
Calculates the Normalized Difference Vegetation Index using Red and NIR bands.
```
"Calculate the NDVI using the B4 layer as the Red band and the B5 layer as the NIR band."
```

### 52. Calculate NDWI (Water Index)
Calculates the Normalized Difference Water Index.
```
"Calculate the NDWI using the Green band and NIR band layers."
```

### 53. Generate Hillshade
Creates a 3D shaded relief from a Digital Elevation Model.
```
"Generate a hillshade from the DEM_Elevation layer."
```
