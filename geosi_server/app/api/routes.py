# -*- coding: utf-8 -*-
"""
GeoSI API Routes

These routes expose the first server-side GIS operations:
- Health check
- Tool listing
- Layer management
- Basic vector analysis
"""

from typing import Dict, List

from fastapi import APIRouter, HTTPException

from geosi_server.app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    BufferRequest,
    CalculateFieldRequest,
    CleanLayerRequest,
    DigitizeLayerRequest,
    DissolveRequest,
    GeocodeRequest,
    IntersectRequest,
    InterpolationRequest,
    LayerLoadRequest,
    LayerResponse,
    MapExportRequest,
    NetworkRequest,
    OperationResponse,
    OverlayRequest,
    ProximityRequest,
    QueryRequest,
    QueryResponse,
    RasterAlgebraRequest,
    ReverseGeocodeRequest,
    SaveLayerRequest,
    SelectRequest,
    SpatialJoinRequest,
    SurfaceRequest,
    ToolSpecResponse,
    ValidateRequest,
    ValidateResponse,
)
from geosi_server.app.services.tool_service import tool_service


router = APIRouter()


def _raise_if_failed(result: OperationResponse) -> None:
    """
    Convert a failed service response into an HTTP error.
    """
    if not result.success:
        detail = result.error or result.message or "Operation failed"
        raise HTTPException(status_code=400, detail=detail)


@router.get("/health", tags=["system"])
def health() -> Dict[str, str]:
    """Simple API health check."""
    return {"status": "ok"}


@router.get("/tools", response_model=List[ToolSpecResponse], tags=["tools"])
def list_tools() -> List[ToolSpecResponse]:
    """Return all tools currently exposed by the API."""
    tools = tool_service.list_tools()
    return tools


@router.get("/layers", response_model=List[LayerResponse], tags=["layers"])
def list_layers() -> List[LayerResponse]:
    """Return all layers currently loaded into memory."""
    layers = tool_service.list_layers()
    return layers


@router.get("/layers/{layer_name}/geojson", tags=["layers"])
def get_layer_geojson(layer_name: str):
    """Return a layer as GeoJSON for visualization."""
    geojson = tool_service.get_layer_geojson(layer_name)
    if geojson is None:
        raise HTTPException(status_code=404, detail=f"Layer {layer_name} not found")
    return geojson


@router.post("/layers/load", response_model=OperationResponse, tags=["layers"])
def load_layer(request: LayerLoadRequest) -> OperationResponse:
    """Load vector or raster spatial data into the current workspace."""
    result = tool_service.load_layer(request.filepath, request.layer_name)
    _raise_if_failed(result)
    return result


@router.post("/layers/digitize", response_model=OperationResponse, tags=["layers"])
def digitize_layer(request: DigitizeLayerRequest) -> OperationResponse:
    """Create a vector layer from digitized GeoJSON features."""
    result = tool_service.digitize_layer(
        name=request.name,
        geometry_type=request.geometry_type,
        crs=request.crs,
        features_geojson=request.features_geojson,
    )
    _raise_if_failed(result)
    return result


@router.post("/layers/save", response_model=OperationResponse, tags=["layers"])
def save_layer(request: SaveLayerRequest) -> OperationResponse:
    """Save a workspace layer to a spatial file."""
    result = tool_service.save_workspace_layer(
        layer_name=request.layer_name,
        filepath=request.filepath,
        driver=request.driver,
    )
    _raise_if_failed(result)
    return result


@router.post("/editing/clean", response_model=OperationResponse, tags=["editing"])
def clean_layer(request: CleanLayerRequest) -> OperationResponse:
    """Clean and correct vector geometry."""
    result = tool_service.clean_workspace_layer(
        layer_name=request.layer_name,
        fix_geometries=request.fix_geometries,
        drop_empty=request.drop_empty,
        drop_duplicates=request.drop_duplicates,
    )
    _raise_if_failed(result)
    return result


@router.post("/editing/calculate-field", response_model=OperationResponse, tags=["editing"])
def calculate_field(request: CalculateFieldRequest) -> OperationResponse:
    """Create or update an attribute field."""
    result = tool_service.calculate_workspace_field(
        layer_name=request.layer_name,
        field_name=request.field_name,
        expression=request.expression,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/select", response_model=OperationResponse, tags=["analysis"])
def run_selection(request: SelectRequest) -> OperationResponse:
    """Select features by attribute expression or spatial relationship."""
    result = tool_service.select_layer_features(
        layer_name=request.layer_name,
        where=request.where,
        spatial_layer_name=request.spatial_layer_name,
        predicate=request.predicate,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/buffer", response_model=OperationResponse, tags=["analysis"])
def run_buffer(request: BufferRequest) -> OperationResponse:
    """Create a buffer around a previously loaded layer."""
    result = tool_service.buffer_layer(
        layer_name=request.layer_name,
        distance=request.distance,
        dissolve_result=request.dissolve,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/overlay", response_model=OperationResponse, tags=["analysis"])
def run_overlay(request: OverlayRequest) -> OperationResponse:
    """Run intersect, union, clip, or erase overlay analysis."""
    result = tool_service.overlay_layers(
        layer_a=request.layer_a,
        layer_b=request.layer_b,
        operation=request.operation,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/intersect", response_model=OperationResponse, tags=["analysis"])
def run_intersect(request: IntersectRequest) -> OperationResponse:
    """Find the intersection of two loaded layers."""
    result = tool_service.intersect_layers(
        layer_a=request.layer_a,
        layer_b=request.layer_b,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/spatial-join", response_model=OperationResponse, tags=["analysis"])
def run_spatial_join(request: SpatialJoinRequest) -> OperationResponse:
    """Join attributes based on spatial relationship."""
    result = tool_service.spatial_join_layers(
        target_layer=request.target_layer,
        join_layer=request.join_layer,
        how=request.how,
        predicate=request.predicate,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/dissolve", response_model=OperationResponse, tags=["analysis"])
def run_dissolve(request: DissolveRequest) -> OperationResponse:
    """Dissolve features by an attribute value."""
    result = tool_service.dissolve_layer(
        layer_name=request.layer_name,
        by_attribute=request.by_attribute,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/proximity", response_model=OperationResponse, tags=["analysis"])
def run_proximity(request: ProximityRequest) -> OperationResponse:
    """Find nearest features and measure distance."""
    result = tool_service.proximity_layers(
        source_layer=request.source_layer,
        target_layer=request.target_layer,
        max_distance=request.max_distance,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/network", response_model=OperationResponse, tags=["analysis"])
def run_network(request: NetworkRequest) -> OperationResponse:
    """Calculate shortest path over a line network."""
    result = tool_service.run_network_analysis(
        network_layer=request.network_layer,
        start=request.start,
        end=request.end,
        weight_field=request.weight_field,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/surface", response_model=OperationResponse, tags=["analysis"])
def run_surface(request: SurfaceRequest) -> OperationResponse:
    """Create slope, aspect, hillshade, or contours from elevation."""
    result = tool_service.run_surface_analysis(
        raster_layer=request.raster_layer,
        operation=request.operation,
        z_factor=request.z_factor,
        output_filepath=request.output_filepath,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/interpolate", response_model=OperationResponse, tags=["analysis"])
def run_interpolation(request: InterpolationRequest) -> OperationResponse:
    """Estimate a raster surface using IDW interpolation."""
    result = tool_service.run_interpolation(
        point_layer=request.point_layer,
        value_field=request.value_field,
        cell_size=request.cell_size,
        power=request.power,
        output_filepath=request.output_filepath,
    )
    _raise_if_failed(result)
    return result


@router.post("/analysis/raster-algebra", response_model=OperationResponse, tags=["analysis"])
def run_raster_algebra(request: RasterAlgebraRequest) -> OperationResponse:
    """Run cell-by-cell raster map algebra."""
    result = tool_service.run_raster_algebra(
        expression=request.expression,
        raster_layer_names=request.raster_layers,
        output_name=request.output_name,
        output_filepath=request.output_filepath,
    )
    _raise_if_failed(result)
    return result


@router.post("/visualization/export-map", response_model=OperationResponse, tags=["visualization"])
def export_map(request: MapExportRequest) -> OperationResponse:
    """Export a cartographic map image."""
    result = tool_service.export_workspace_map(
        layer_names=request.layer_names,
        output_filepath=request.output_filepath,
        title=request.title,
    )
    _raise_if_failed(result)
    return result


@router.post("/geocoding/geocode", response_model=OperationResponse, tags=["geocoding"])
def geocode(request: GeocodeRequest) -> OperationResponse:
    """Convert an address to coordinates."""
    result = tool_service.geocode(request.address, request.provider)
    _raise_if_failed(result)
    return result


@router.post("/geocoding/reverse", response_model=OperationResponse, tags=["geocoding"])
def reverse_geocode(request: ReverseGeocodeRequest) -> OperationResponse:
    """Convert coordinates to an address."""
    result = tool_service.reverse_geocode_location(
        longitude=request.longitude,
        latitude=request.latitude,
        provider=request.provider,
    )
    _raise_if_failed(result)
    return result


@router.post("/query", response_model=QueryResponse, tags=["intelligence"])
def run_query(request: QueryRequest) -> QueryResponse:
    """Run a natural language GIS query through the GeoSI Agent."""
    result = tool_service.run_query(request.query)
    return result


@router.post("/analyze", response_model=AnalyzeResponse, tags=["intelligence"])
def run_analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Full transparent parse + plan + execute pipeline (Architecture FR-01..04)."""
    result = tool_service.analyze(request.query)
    return AnalyzeResponse(**result)


@router.post("/validate", response_model=ValidateResponse, tags=["validation"])
def run_validate(request: ValidateRequest) -> ValidateResponse:
    """Run ValidationEngine checks on workspace layers (Architecture Module 6)."""
    result = tool_service.validate_workspace(
        layer_name=request.layer_name,
        layer_a=request.layer_a,
        layer_b=request.layer_b,
        required_fields=request.required_fields,
    )
    return ValidateResponse(**result)
