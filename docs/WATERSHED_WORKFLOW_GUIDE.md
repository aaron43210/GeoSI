# Watershed Analysis Workflow Tool - Usage Guide

## Overview

The **Complete Watershed Analysis** tool (`watershed_workflow`) orchestrates a comprehensive 5-step hydrological analysis pipeline in a single execution. It's available in GeoSI as a complex multi-step workflow tool.

**Perfect for:**
- Drainage basin analysis
- Hydrological studies  
- Water resource planning
- Flood modeling preparation

---

## Quick Start Prompts

### 1. Basic Watershed Analysis
```
Perform complete watershed analysis on DEM
```

### 2. Watershed with Custom Threshold
```
Analyze watersheds from DEM with threshold of 500 cells
```

### 3. Specify Output Name
```
Run complete watershed analysis on DEM and name outputs my_basin_analysis
```

### 4. Full Custom Configuration
```
Watershed analysis on DEM with threshold 750, fill distance 150, output name study_area
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `INPUT_DEM` | layer | ✅ Yes | N/A | Input Digital Elevation Model (DEM raster) |
| `THRESHOLD` | number | ❌ No | 1000 | Flow accumulation threshold for watershed delineation (cells) |
| `FILL_DISTANCE` | number | ❌ No | 100 | Search distance for filling no-data values (meters) |
| `OUTPUT_BASENAME` | string | ❌ No | watershed_analysis | Base name for output files |

---

## Workflow Steps (Executed Automatically)

1. **Step 1: DEM Preprocessing**
   - Algorithm: `gdal:fillnodata`
   - Output: `{basename}_dem_filled`
   - Fills no-data values to ensure complete elevation coverage

2. **Step 2: Flow Direction (D8)**
   - Output: `{basename}_flow_direction`
   - Calculates which of 8 neighbor cells water flows to
   - Values: 1,2,4,8,16,32,64,128 (powers of 2 for each direction)

3. **Step 3: Flow Accumulation**
   - Output: `{basename}_flow_accumulation`
   - Sums cells flowing into each cell
   - High values = stream channels & convergence zones

4. **Step 4: Watershed Delineation**
   - Output: `{basename}_watershed_mask`
   - Thresholds flow accumulation to create watershed boundary
   - Uses specified THRESHOLD parameter

5. **Step 5: Vector Conversion & Statistics**
   - Algorithm: `gdal:polygonize`
   - Output: `{basename}_watershed_polygons`
   - Generates basin statistics (area, perimeter, elevation, flow metrics)

---

## Output Layers

All outputs are automatically generated and available in QGIS:

```
dem_preprocessed         → Filled DEM (raster)
flow_direction          → D8 flow direction (raster)
flow_accumulation       → Cumulative flow (raster)
watershed_mask          → Binary watershed boundary (raster)
watershed_polygons      → Watershed as vector polygons (vector)
statistics              → Basin statistics (metadata)
```

---

## Example Usage Scenarios

### Scenario 1: Quick Analysis on Loaded DEM
```
User input: "Analyze watershed from DEM"
GeoSI executes: watershed_workflow with INPUT_DEM=DEM
Result: 5 layers generated with default names
```

### Scenario 2: Sensitive Watersheds with Low Threshold
```
User input: "Find all small drainage basins in DEM with threshold 100"
GeoSI executes: watershed_workflow with THRESHOLD=100, FILL_DISTANCE=100
Result: More fragmented watersheds capturing smaller drainages
```

### Scenario 3: Project-Specific Output Names
```
User input: "Watershed analysis on DEM, save as Kerala_Watersheds"
GeoSI executes: watershed_workflow with OUTPUT_BASENAME=Kerala_Watersheds
Result: All outputs named Kerala_Watersheds_{step_name}
```

---

## Technical Notes

### D8 Algorithm
- Determines flow direction to steepest neighboring cell
- Encodes direction as power of 2:
  - E=1, SE=2, S=4, SW=8, W=16, NW=32, N=64, NE=128

### Flow Accumulation Threshold
- **Low threshold (100-500)**: More detailed, smaller watersheds
- **Medium threshold (1000-5000)**: Balanced, typical drainage basins
- **High threshold (10000+)**: Larger, aggregated watersheds

### Fill Distance
- Determines how far algorithm searches for surrounding values
- Higher values = smoother DEM but less detail preservation
- Typical range: 50-200 meters

---

## Error Handling

The tool validates:
- ✅ INPUT_DEM is provided
- ✅ THRESHOLD is positive
- ✅ FILL_DISTANCE is non-negative

**Common Issues:**
- **"INPUT_DEM is required"** → Load DEM raster first
- **"THRESHOLD must be positive"** → Use positive number > 0
- **"Failed to preprocess DEM"** → DEM may have invalid CRS or structure

---

## Integration with QGIS Plugin

1. **In QGIS**, open the GeoSI AI prompt panel (toolbar icon)
2. **Type** any prompt from the examples above
3. **Press Enter** or click ▶ button
4. **Monitor** the chat log for step completion messages
5. **View** output layers in QGIS Layers panel (auto-loaded)

---

## Advanced: Natural Language Queries

GeoSI understands these natural variations:

- "Run complete watershed delineation on DEM"
- "Find all basins in the elevation model"
- "Calculate flow accumulation and watershed boundaries"
- "Hydrological analysis of DEM"
- "Where is water flowing in DEM?"

---

## Tool Properties

| Property | Value |
|----------|-------|
| Tool Name | `watershed_workflow` |
| Display Name | Complete Watershed Analysis |
| Category | terrain |
| Module | `geosi_engine.tools.complex` |
| Status | Multi-step workflow |
| QGIS Algorithm | None (orchestrated workflow) |

---

## See Also

- **Existing Watershed Tool** (`watershed`) - Single-step basic delineation
- **Terrain Tools** - Slope, aspect, hillshade, viewshed, profile
- **Raster Tools** - Fill NoData, reclassify, proximity calculations
- **Vector Tools** - Clip, buffer, intersection operations
