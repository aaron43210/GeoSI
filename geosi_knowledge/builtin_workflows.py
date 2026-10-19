"""
GeoSI Knowledge — Built-in Workflow Templates
═══════════════════════════════════════════════════════════════════

Pre-defined workflow templates that are loaded into WorkflowMemory
on first initialization. These serve as seed knowledge so GeoSI
can recommend workflows even before any user executions.

Categories:
    - Spectral Indices: NDVI, NDWI, NDBI
    - Terrain Analysis: Slope, Hillshade, Contour
    - Vector Operations: Buffer, Intersect, Dissolve
    - Advanced: Watershed, Land Cover Classification, Change Detection
"""

from geosi_knowledge.workflow_memory import WorkflowExample


def get_builtin_workflows():
    """
    Return a list of built-in WorkflowExample templates.

    These are reference workflows that the knowledge layer uses
    to bootstrap its workflow memory.
    """
    return [
        # ── Spectral Indices ──────────────────────────────────────────
        WorkflowExample(
            name="ndvi_calculation",
            description=(
                "Calculate Normalized Difference Vegetation Index (NDVI) "
                "from multispectral imagery. NDVI = (NIR - Red) / (NIR + Red). "
                "Values range from -1 to 1, where higher values indicate "
                "denser vegetation."
            ),
            user_query="Calculate NDVI from Sentinel-2 imagery",
            tool_sequence=["native_rastercalc"],
            tags=["ndvi", "vegetation", "spectral", "sentinel", "raster", "remote_sensing"],
            output_description="Single-band raster with NDVI values (-1 to 1)",
        ),
        WorkflowExample(
            name="ndwi_calculation",
            description=(
                "Calculate Normalized Difference Water Index (NDWI) "
                "to identify water bodies. NDWI = (Green - NIR) / (Green + NIR). "
                "Positive values typically indicate water."
            ),
            user_query="Calculate NDWI to find water bodies",
            tool_sequence=["native_rastercalc"],
            tags=["ndwi", "water", "spectral", "raster", "remote_sensing"],
            output_description="Single-band raster with NDWI values (-1 to 1)",
        ),
        WorkflowExample(
            name="ndbi_calculation",
            description=(
                "Calculate Normalized Difference Built-up Index (NDBI) "
                "to identify urban/built-up areas. NDBI = (SWIR - NIR) / (SWIR + NIR)."
            ),
            user_query="Calculate NDBI for urban area detection",
            tool_sequence=["native_rastercalc"],
            tags=["ndbi", "urban", "built-up", "spectral", "raster"],
            output_description="Single-band raster with NDBI values",
        ),
        # ── Terrain Analysis ──────────────────────────────────────────
        WorkflowExample(
            name="slope_analysis",
            description=(
                "Calculate slope from a Digital Elevation Model (DEM). "
                "Slope represents the rate of change of elevation, expressed "
                "in degrees or percent."
            ),
            user_query="Calculate slope from DEM",
            tool_sequence=["native_slope"],
            tags=["slope", "terrain", "dem", "elevation", "raster"],
            output_description="Slope raster in degrees",
        ),
        WorkflowExample(
            name="hillshade_generation",
            description=(
                "Generate a hillshade rendering from a DEM for terrain "
                "visualization. Simulates illumination from a light source."
            ),
            user_query="Generate hillshade from elevation data",
            tool_sequence=["native_hillshade"],
            tags=["hillshade", "terrain", "dem", "visualization", "raster"],
            output_description="Hillshade raster (grayscale shading)",
        ),
        WorkflowExample(
            name="contour_generation",
            description=(
                "Generate contour lines from a DEM at specified intervals. "
                "Contours connect points of equal elevation."
            ),
            user_query="Create contour lines from DEM at 10m intervals",
            tool_sequence=["gdal_contour"],
            tags=["contour", "terrain", "dem", "elevation", "vector"],
            output_description="Vector layer with contour lines",
        ),
        WorkflowExample(
            name="terrain_full_analysis",
            description=(
                "Complete terrain analysis: calculate slope, aspect, and " "hillshade from a DEM in one workflow."
            ),
            user_query="Full terrain analysis from DEM",
            tool_sequence=["native_slope", "native_aspect", "native_hillshade"],
            tags=["slope", "aspect", "hillshade", "terrain", "dem"],
            output_description="Three raster layers: slope, aspect, hillshade",
        ),
        # ── Vector Operations ─────────────────────────────────────────
        WorkflowExample(
            name="buffer_analysis",
            description=(
                "Create buffer zones around features at a specified distance. "
                "Useful for proximity analysis (e.g., schools within 1km of parks)."
            ),
            user_query="Buffer hospitals by 500 meters",
            tool_sequence=["native_buffer"],
            tags=["buffer", "proximity", "vector", "distance"],
            output_description="Vector layer with buffered polygons",
        ),
        WorkflowExample(
            name="proximity_analysis",
            description=(
                "Find features within a specified distance of other features. "
                "Buffer the reference layer, then intersect with the target."
            ),
            user_query="Find schools within 2km of flood zones",
            tool_sequence=["native_buffer", "native_intersection"],
            tags=["buffer", "intersect", "proximity", "vector"],
            output_description="Vector layer with features within specified distance",
        ),
        WorkflowExample(
            name="spatial_intersection",
            description=(
                "Find the geometric intersection of two layers — areas or "
                "features that overlap between both datasets."
            ),
            user_query="Intersect parks with flood zones",
            tool_sequence=["native_intersection"],
            tags=["intersect", "overlay", "vector"],
            output_description="Vector layer with overlapping features",
        ),
        WorkflowExample(
            name="dissolve_boundaries",
            description=(
                "Merge adjacent features that share a common attribute value. "
                "Useful for aggregating administrative boundaries."
            ),
            user_query="Dissolve polygons by district name",
            tool_sequence=["native_dissolve"],
            tags=["dissolve", "merge", "aggregate", "vector"],
            output_description="Vector layer with merged polygons",
        ),
        WorkflowExample(
            name="clip_to_boundary",
            description=("Clip features to a boundary polygon, keeping only the " "portions within the clip area."),
            user_query="Clip roads to city boundary",
            tool_sequence=["native_clip"],
            tags=["clip", "extract", "vector", "boundary"],
            output_description="Vector layer clipped to boundary",
        ),
        # ── Advanced Analysis ─────────────────────────────────────────
        WorkflowExample(
            name="watershed_delineation",
            description=(
                "Delineate drainage basins (watersheds) from a DEM. "
                "Requires fill sinks → flow direction → flow accumulation → "
                "watershed boundary extraction."
            ),
            user_query="Delineate watersheds from DEM",
            tool_sequence=[
                "native_fillsinks",
                "native_flowdirection",
                "native_flowaccumulation",
            ],
            tags=["watershed", "hydrology", "dem", "drainage", "terrain"],
            output_description="Vector layer with watershed boundaries",
        ),
        WorkflowExample(
            name="land_cover_classification",
            description=(
                "Classify satellite imagery into land cover categories "
                "(vegetation, water, urban, bare soil). Typically uses "
                "supervised or unsupervised classification on multispectral bands."
            ),
            user_query="Classify land cover from satellite imagery",
            tool_sequence=["native_rastercalc"],
            tags=["classification", "land_cover", "remote_sensing", "raster", "ai_ml"],
            output_description="Classified raster with land cover categories",
        ),
        WorkflowExample(
            name="change_detection",
            description=(
                "Detect changes between two time periods by comparing "
                "raster datasets. Common approaches: image differencing, "
                "NDVI change, or post-classification comparison."
            ),
            user_query="Detect land use changes between 2020 and 2023",
            tool_sequence=["native_rastercalc"],
            tags=["change_detection", "temporal", "raster", "remote_sensing"],
            output_description="Change map raster showing areas of change",
        ),
    ]
