# -*- coding: utf-8 -*-
"""
GeoSI API Schemas

These Pydantic models define the request and response shapes used by FastAPI.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ToolParameterResponse(BaseModel):
    """Describe one tool parameter."""

    name: str
    type_: str
    required: bool
    description: str = ""
    example: Optional[str] = None


class ToolSpecResponse(BaseModel):
    """Describe one available tool."""

    name: str
    description: str
    category: str
    parameters: List[ToolParameterResponse]


class LayerLoadRequest(BaseModel):
    """Request body for loading vector or raster spatial data."""

    filepath: str = Field(
        ...,
        description="Absolute or repo-relative path to a spatial dataset",
    )
    layer_name: Optional[str] = None


class DigitizeLayerRequest(BaseModel):
    """Request body for creating a digitized vector layer."""

    name: str
    geometry_type: str = Field(..., description="Point, LineString, or Polygon")
    crs: str = "EPSG:4326"
    features_geojson: Dict[str, Any]


class SaveLayerRequest(BaseModel):
    """Request body for saving a layer to disk."""

    layer_name: str
    filepath: str
    driver: Optional[str] = None


class CleanLayerRequest(BaseModel):
    """Request body for cleaning and correcting vector data."""

    layer_name: str
    fix_geometries: bool = True
    drop_empty: bool = True
    drop_duplicates: bool = False


class CalculateFieldRequest(BaseModel):
    """Request body for editing attributes through a field calculation."""

    layer_name: str
    field_name: str
    expression: str


class SelectRequest(BaseModel):
    """Request body for selecting features by attribute or location."""

    layer_name: str
    where: Optional[str] = None
    spatial_layer_name: Optional[str] = None
    predicate: str = "intersects"


class BufferRequest(BaseModel):
    """Request body for the buffer operation."""

    layer_name: str
    distance: float = Field(..., gt=0)
    dissolve: bool = False


class IntersectRequest(BaseModel):
    """Request body for the intersect operation."""

    layer_a: str
    layer_b: str


class OverlayRequest(BaseModel):
    """Request body for overlay analysis."""

    layer_a: str
    layer_b: str
    operation: str = Field(..., description="intersect, union, clip, or erase")


class SpatialJoinRequest(BaseModel):
    """Request body for joining data by spatial relationship."""

    target_layer: str
    join_layer: str
    how: str = "inner"
    predicate: str = "intersects"


class DissolveRequest(BaseModel):
    """Request body for dissolving features."""

    layer_name: str
    by_attribute: Optional[str] = None


class ProximityRequest(BaseModel):
    """Request body for nearest-feature analysis."""

    source_layer: str
    target_layer: str
    max_distance: Optional[float] = Field(default=None, gt=0)


class NetworkRequest(BaseModel):
    """Request body for shortest-path network analysis."""

    network_layer: str
    start: List[float] = Field(..., min_length=2, max_length=2)
    end: List[float] = Field(..., min_length=2, max_length=2)
    weight_field: Optional[str] = None


class SurfaceRequest(BaseModel):
    """Request body for slope, aspect, hillshade, and contour generation."""

    raster_layer: str
    operation: str = Field(..., description="slope, aspect, hillshade, or contour")
    z_factor: float = 1.0
    output_filepath: Optional[str] = None


class InterpolationRequest(BaseModel):
    """Request body for IDW interpolation."""

    point_layer: str
    value_field: str
    cell_size: float = Field(..., gt=0)
    power: float = Field(2.0, gt=0)
    output_filepath: Optional[str] = None


class RasterAlgebraRequest(BaseModel):
    """Request body for raster calculator operations."""

    expression: str
    raster_layers: Dict[str, str] = Field(
        ...,
        description="Mapping of expression alias to loaded raster layer name",
    )
    output_name: str = "raster_calculation"
    output_filepath: Optional[str] = None


class MapExportRequest(BaseModel):
    """Request body for exporting a map image."""

    layer_names: List[str]
    output_filepath: str
    title: str = "GeoSI Map"


class GeocodeRequest(BaseModel):
    """Request body for converting an address to coordinates."""

    address: str
    provider: str = "nominatim"


class ReverseGeocodeRequest(BaseModel):
    """Request body for converting coordinates to an address."""

    longitude: float
    latitude: float
    provider: str = "nominatim"


class QueryRequest(BaseModel):
    """Request body for a natural language query."""

    query: str


class QueryResponse(BaseModel):
    """Response for a natural language query."""

    success: bool
    answer: str
    reasoning: str
    error: Optional[str] = None


class LayerResponse(BaseModel):
    """Metadata returned for a loaded or generated layer."""

    name: str
    geometry_type: str
    feature_count: int
    crs: str
    filepath: str = ""
    layer_type: str = "vector"


class AnalyzeRequest(BaseModel):
    """Request body for the full parse + plan + execute pipeline."""

    query: str


class AnalyzeResponse(BaseModel):
    """Full transparency response for /api/v1/analyze."""

    success: bool
    answer: str = ""
    reasoning: str = ""
    error: Optional[str] = None
    intent: Optional[str] = None
    entities: Dict[str, Any] = Field(default_factory=dict)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    logs: List[Dict[str, Any]] = Field(default_factory=list)


class ValidateRequest(BaseModel):
    """Request body for /api/v1/validate. At least one target is required."""

    layer_name: Optional[str] = None
    layer_a: Optional[str] = None
    layer_b: Optional[str] = None
    required_fields: Optional[List[str]] = None


class ValidationIssueResponse(BaseModel):
    """One validation issue."""

    severity: str
    code: str
    message: str
    layer: Optional[str] = None


class ValidateResponse(BaseModel):
    """Aggregate validation report."""

    ok: bool
    issues: List[ValidationIssueResponse] = Field(default_factory=list)
    stats: Dict[str, Any] = Field(default_factory=dict)


class OperationResponse(BaseModel):
    """Generic response for one GIS operation."""

    success: bool
    message: str = ""
    error: Optional[str] = None
    layer: Optional[LayerResponse] = None
    data: Optional[Dict[str, Any]] = None


class ExportRequest(BaseModel):
    """Request body for exporting analysis results as shapefile."""

    query: str = Field(..., description="Natural language query to analyze")
    filename: str = Field(..., description="Output filename (without extension)")
    output_dir: Optional[str] = Field(
        "outputs",
        description="Output directory for the shapefile"
    )


class ExportResponse(BaseModel):
    """Response for shapefile export operation."""

    success: bool
    message: str = ""
    error: Optional[str] = None
    output_file: Optional[str] = None
    files: Optional[List[str]] = None
    features_count: Optional[int] = None
    geometry_type: Optional[str] = None
