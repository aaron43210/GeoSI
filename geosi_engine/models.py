# -*- coding: utf-8 -*-
"""
GeoSI Engine — Data Models

This module defines ALL data structures used throughout GeoSI.
Every other file imports from here. This file has ZERO internal imports.

Data structures defined here:
    - ExecutionStatus: Success/failure status enum
    - IntentType: What the user wants to do (buffer, intersect, etc.)
    - GeometryType: Point, LineString, Polygon, Raster, etc.
    - ToolParameter: One parameter a tool expects
    - ToolSpec: Complete specification of what a tool does
    - Layer: Represents one spatial layer (vector or raster)
    - ToolResult: Result from executing one GIS tool
    - AnalysisRequest: Parsed user request with intent and entities
    - ExecutionPlan: Ordered list of tool steps to execute
    - ExecutionResult: Final result after executing a plan

Design Decisions:
    - We use dataclasses instead of Pydantic for maximum compatibility
      with both QGIS (which may have old Python) and the FastAPI server.
    - Every class has complete docstrings following the DUK coding style.
    - No external dependencies — only Python stdlib.

See FILE_CONNECTIONS.md:
    - IMPORTS FROM: (nothing — this is the foundation)
    - USED BY: every other file in geosi_engine/
"""

from typing import Dict, List, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid


# ═══════════════════════════════════════════════════════════════════════════
# ENUMERATIONS
# These are like "status codes" that help us track what's happening.
# An Enum is a class with a fixed set of named constants.
# ═══════════════════════════════════════════════════════════════════════════

class ExecutionStatus(str, Enum):
    """
    Status of an execution step or complete execution.

    These are the possible outcomes when we run a GIS tool:
        - SUCCESS: Everything worked correctly
        - PARTIAL: Some steps worked, some failed
        - FAILED: The operation could not complete
        - CANCELLED: The user stopped the operation

    Usage:
        if result.status == ExecutionStatus.SUCCESS:
            print("Operation completed successfully!")
    """
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    CANCELLED = "cancelled"


class IntentType(str, Enum):
    """
    Classification of what the user wants to do.

    When the user types a natural language query, the parser classifies
    it into one of these intent categories. This tells the agent which
    tools to consider when planning the workflow.

    Examples:
        "Buffer hospitals by 500m"      → PROXIMITY
        "Intersect parks with schools"  → OVERLAY
        "Calculate slope from DEM"      → TERRAIN
        "Find shortest route"           → NETWORK
        "Show land use change"          → TEMPORAL
        "Classify satellite image"      → AI_ML

    Usage:
        if request.intent == IntentType.PROXIMITY:
            # Consider buffer, intersect, nearest-feature tools
    """
    PROXIMITY = "proximity"                 # Find features near other features
    OVERLAY = "overlay"                     # Combine multiple layers
    GEOMETRY = "geometry"                   # Modify geometry shape
    RASTER = "raster"                       # Raster analysis and processing
    TERRAIN = "terrain"                     # 3D, elevation, slope, viewshed
    NETWORK = "network"                     # Routing and network analysis
    TEMPORAL = "temporal"                   # Time-series and change detection
    AI_ML = "ai_ml"                         # Machine learning spatial analysis
    VALIDATION = "validation"               # Check data quality
    STATISTICS = "statistics"               # Calculate spatial statistics
    DATA_MANAGEMENT = "data_management"     # Load, save, convert data
    CARTOGRAPHY = "cartography"             # Map export, geocoding
    UNKNOWN = "unknown"                     # Unable to classify


class GeometryType(str, Enum):
    """
    Types of spatial geometry.

    In GIS, every feature has a geometry type that describes its shape:
        - POINT: A single location (e.g., a hospital, a bus stop)
        - LINESTRING: A path or route (e.g., a road, a river)
        - POLYGON: An area (e.g., a park, a building footprint)
        - Multi* variants: Collections of the above
        - RASTER: A grid of pixel values (e.g., satellite image, DEM)

    This is the same classification used by QGIS internally (see
    QGIS/src/core/geometry/qgswkbtypes.h for the C++ version).
    """
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"
    MULTIPOINT = "MultiPoint"
    MULTILINESTRING = "MultiLineString"
    MULTIPOLYGON = "MultiPolygon"
    RASTER = "Raster"
    UNKNOWN = "Unknown"


# ═══════════════════════════════════════════════════════════════════════════
# TOOL SPECIFICATION
# These describe what a tool IS — its name, parameters, and capabilities.
# They do NOT contain any execution logic.
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ToolParameter:
    """
    Describes one parameter that a tool expects.

    Every GIS tool needs input data. A buffer tool needs a layer and
    a distance. An intersect tool needs two layers. This class describes
    one such parameter so the agent knows what to provide.

    Attributes:
        name: Parameter name (e.g., "distance", "layer", "field")
        param_type: Data type expected ("layer", "number", "string", "boolean")
        required: True if this parameter must be provided
        description: Human-readable explanation of what this parameter does
        example: Example value to help the user understand
        default: Default value if the parameter is not provided

    Example:
        ToolParameter(
            name="distance",
            param_type="number",
            required=True,
            description="Buffer distance in layer CRS units (usually meters)",
            example="500"
        )
    """
    name: str
    param_type: str
    required: bool = True
    description: str = ""
    example: Optional[str] = None
    default: Optional[Any] = None

    def __repr__(self):
        """Show parameter in a compact format for debugging."""
        marker = "*" if self.required else ""
        return f"{self.name}: {self.param_type}{marker}"


@dataclass
class ToolSpec:
    """
    Complete specification of what a GIS tool does.

    This is the "identity card" of a tool. It tells the agent:
        - What the tool is called
        - What it does (description)
        - What category it belongs to (vector, raster, network, etc.)
        - What parameters it needs
        - What QGIS Processing algorithm it wraps (if any)

    The ToolSpec does NOT contain execution logic. That lives in the
    tool's execute() method. This separation lets us list all tools
    and their capabilities without importing heavy GIS libraries.

    Attributes:
        name: Unique tool identifier (e.g., "buffer", "intersect", "slope")
        display_name: Human-readable name (e.g., "Buffer", "Intersection")
        description: What the tool does in plain language
        category: Tool category for grouping ("vector", "raster", "network")
        parameters: List of ToolParameter objects describing inputs
        outputs: List of output names (e.g., ["buffered_layer"])
        tags: Keywords for search (e.g., ["buffer", "grow", "distance"])
        qgis_algorithm: QGIS Processing algorithm ID (e.g., "native:buffer")
        requires_qgis: True if this tool needs QGIS to run
        requires_gpu: True if this tool benefits from GPU acceleration

    Example:
        ToolSpec(
            name="buffer",
            display_name="Buffer",
            description="Create distance-based zones around features",
            category="vector",
            parameters=[...],
            qgis_algorithm="native:buffer"
        )
    """
    name: str
    display_name: str = ""
    description: str = ""
    category: str = "general"
    parameters: List[ToolParameter] = field(default_factory=list)
    outputs: List[str] = field(default_factory=lambda: ["OUTPUT"])
    tags: List[str] = field(default_factory=list)
    qgis_algorithm: Optional[str] = None
    requires_qgis: bool = False
    requires_gpu: bool = False

    def __str__(self):
        """Show tool spec in a compact format for debugging."""
        req_params = [p for p in self.parameters if p.required]
        return f"{self.name}({', '.join(str(p) for p in req_params)})"


# ═══════════════════════════════════════════════════════════════════════════
# LAYER — Represents one spatial data layer
# This is the core data container. Every tool reads from and writes to Layers.
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Layer:
    """
    Represents one spatial data layer in the GeoSI workspace.

    A Layer can be either:
        - Vector: Contains geometric features (points, lines, polygons)
                  Stored internally as a GeoDataFrame (from geopandas)
        - Raster: Contains a grid of pixel values (elevation, imagery)
                  Stored internally as a NumPy array + metadata dict

    Both the QGIS Plugin and the FastAPI Server use this same Layer class.
    When running inside QGIS, the features can also be a QgsVectorLayer.

    Attributes:
        name: Layer name (e.g., "hospitals", "dem_elevation")
        geometry_type: Type of geometry ("Point", "Polygon", "Raster", etc.)
        feature_count: Number of features (vector) or 1 (raster)
        crs: Coordinate Reference System (e.g., "EPSG:4326", "EPSG:32643")
        filepath: Path to the source file (empty if in-memory)
        layer_type: "vector" or "raster"
        features: The actual geometry data (GeoDataFrame for vector)
        raster: The actual pixel data (NumPy array for raster)
        raster_meta: Raster metadata dict (width, height, transform, crs)
        bounds: Spatial extent as {xmin, ymin, xmax, ymax}
        fields: List of attribute field names (for vector layers)

    Example:
        # Create a vector layer
        layer = Layer(
            name="hospitals",
            geometry_type="Point",
            feature_count=42,
            crs="EPSG:4326"
        )
        layer.features = geopandas.read_file("hospitals.shp")

        # Create a raster layer
        layer = Layer(
            name="dem",
            geometry_type="Raster",
            feature_count=1,
            crs="EPSG:32643",
            layer_type="raster"
        )
        layer.raster = numpy_array
    """
    name: str
    geometry_type: str = "Unknown"
    feature_count: int = 0
    crs: str = "EPSG:4326"
    filepath: str = ""
    layer_type: str = "vector"

    # The actual spatial data — set after creation
    # We use Any type because the data depends on whether it's vector or raster
    features: Any = field(default=None, repr=False)
    raster: Any = field(default=None, repr=False)
    raster_meta: Dict[str, Any] = field(default_factory=dict, repr=False)
    bounds: Dict[str, float] = field(default_factory=dict, repr=False)
    fields: List[str] = field(default_factory=list, repr=False)

    def __str__(self):
        """Show layer info in a compact format."""
        return (
            f"Layer({self.name}, {self.layer_type}, "
            f"{self.geometry_type}, {self.feature_count} features)"
        )

    def has_features(self) -> bool:
        """Check if this vector layer has usable features."""
        return (
            self.layer_type == "vector"
            and self.features is not None
            and self.feature_count > 0
        )

    def has_raster(self) -> bool:
        """Check if this raster layer has usable data."""
        return (
            self.layer_type == "raster"
            and self.raster is not None
        )


# ═══════════════════════════════════════════════════════════════════════════
# TOOL RESULT — What a tool returns after execution
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ToolResult:
    """
    Result from executing one GIS tool.

    Every tool in GeoSI returns a ToolResult. This standardized format
    makes it easy to chain tools together — the output of one tool
    becomes the input to the next.

    Attributes:
        success: True if the tool completed without errors
        output: The result data (usually a Layer, sometimes a dict)
        message: Human-readable description of what happened
        error: Error message if the tool failed (None if success)

    Example:
        # Successful result
        result = ToolResult(
            success=True,
            output=buffered_layer,
            message="Created buffer: 500m around 42 features"
        )

        # Failed result
        result = ToolResult(
            success=False,
            error="Layer has no features to buffer"
        )
    """
    success: bool
    output: Any = None
    message: str = ""
    error: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# ANALYSIS REQUEST — What the user wants (parsed from natural language)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class AnalysisRequest:
    """
    Structured representation of a user's analysis request.

    When the user types "Find hospitals within 2km of flood zones",
    the parser converts it into an AnalysisRequest with:
        - query: The original text
        - intent: IntentType.PROXIMITY
        - entities: {"primary_layer": "hospitals", "secondary_layer": "flood_zones"}
        - parameters: {"distance_value": 2000, "distance_unit": "meters"}

    Attributes:
        query: Original natural language text
        intent: Classified intent type (from IntentType enum)
        entities: Extracted spatial entities (layer names, features)
        parameters: Extracted numerical parameters (distances, thresholds)
        constraints: Any validation warnings or questions for the user
        available_layers: Names of layers currently loaded in the workspace
        timestamp: When this request was created

    Example:
        request = AnalysisRequest(
            query="Buffer schools by 500 meters",
            intent=IntentType.PROXIMITY,
            entities={"primary_layer": "schools"},
            parameters={"distance_value": 500, "distance_unit": "meters"}
        )
    """
    query: str = ""
    intent: IntentType = IntentType.UNKNOWN
    entities: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    available_layers: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ═══════════════════════════════════════════════════════════════════════════
# EXECUTION PLAN — The agent's step-by-step plan
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ToolStep:
    """
    One step in an execution plan.

    Each step specifies which tool to run, with what parameters,
    and what the output should be called.

    Attributes:
        step_id: Unique identifier for this step (e.g., "step_1")
        tool_name: Name of the tool to execute (e.g., "buffer")
        parameters: Tool-specific parameters as a dictionary
        input_layers: Names of required input layers
        output_name: Name to assign to the result layer
        description: Human-readable description of what this step does
        depends_on: List of step_ids that must complete before this step

    Example:
        ToolStep(
            step_id="step_1",
            tool_name="buffer",
            parameters={"distance": 2000},
            input_layers=["flood_zones"],
            output_name="flood_zones_buffer_2000",
            description="Create a 2km buffer around flood zones"
        )
    """
    step_id: str = ""
    tool_name: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    input_layers: List[str] = field(default_factory=list)
    output_name: str = ""
    description: str = ""
    depends_on: List[str] = field(default_factory=list)


@dataclass
class ExecutionPlan:
    """
    Complete execution plan created by the agent.

    An ExecutionPlan is an ordered list of ToolSteps that the executor
    will run one by one. It also includes the agent's reasoning about
    why this plan was chosen.

    Attributes:
        plan_id: Unique identifier for this plan
        request: The original AnalysisRequest
        steps: Ordered list of ToolStep objects
        reasoning: The agent's explanation of why this plan was chosen
        estimated_duration: Estimated time in seconds

    Example:
        plan = ExecutionPlan(
            steps=[
                ToolStep(step_id="step_1", tool_name="buffer", ...),
                ToolStep(step_id="step_2", tool_name="intersect", ...),
            ],
            reasoning="Buffer flood zones first, then find overlapping hospitals"
        )
    """
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    request: Optional[AnalysisRequest] = None
    steps: List[ToolStep] = field(default_factory=list)
    reasoning: str = ""
    estimated_duration: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════
# EXECUTION RESULT — What the executor returns after running a plan
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class StepLog:
    """
    Log entry for one executed step.

    After each step is executed, we record what happened in a StepLog.
    This provides full transparency about the execution.

    Attributes:
        step_id: Which step this log is for
        tool_name: Which tool was executed
        status: SUCCESS, FAILED, etc.
        duration_ms: How long the step took (milliseconds)
        output_features: Number of features in the output (if vector)
        error_message: Error message if the step failed
    """
    step_id: str = ""
    tool_name: str = ""
    status: ExecutionStatus = ExecutionStatus.FAILED
    duration_ms: float = 0.0
    output_features: int = 0
    error_message: Optional[str] = None


@dataclass
class ExecutionResult:
    """
    Final result after the executor runs a complete plan.

    This is the end product of the entire GeoSI pipeline:
        User Query → Parse → Plan → Execute → ExecutionResult

    Attributes:
        success: True if all steps completed successfully
        answer: Human-readable answer for the user
        reasoning: Step-by-step explanation of the process
        error: Error message if something failed
        results: Dictionary of output layer names → Layer objects
        logs: List of StepLog entries for each executed step
        total_duration_ms: Total execution time in milliseconds

    Example:
        result = ExecutionResult(
            success=True,
            answer="Found 12 hospitals within 2km of flood zones",
            reasoning="Step 1: Buffered flood zones by 2km. Step 2: Intersected...",
            results={"hospitals_near_floods": layer_object}
        )
    """
    success: bool = False
    answer: str = ""
    reasoning: str = ""
    error: Optional[str] = None
    results: Dict[str, Any] = field(default_factory=dict)
    logs: List[StepLog] = field(default_factory=list)
    total_duration_ms: float = 0.0
