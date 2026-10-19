"""
GeoSI v2 — Dynamic QGIS Backend Bridge
═══════════════════════════════════════════════════════════════════════════

★ THE CORE INNOVATION: This module replaces 2000+ lines of hardcoded tool
definitions with ~300 lines of dynamic discovery using the QGIS Processing
Registry API (QgsApplication.processingRegistry()).

Architecture
────────────
1. auto_discover_qgis_tools(registry)
   - Iterates QgsApplication.processingRegistry().algorithms()
   - Reads each algorithm's id(), displayName(), shortHelpString()
   - Maps QgsProcessingParameter* types → GeoSI ToolParameter types
   - Creates a BackendTool for each and registers it in the ToolRegistry
   - Uses a hash-set (O(1) lookup) for deduplication

2. _run_qgis_algorithm(algorithm_id, parameters)
   - "Fast Path": For simple data queries (count, extent, CRS), bypasses
     processing.run() entirely and uses direct PyQGIS API calls (O(1))
   - "Full Path": For complex algorithms, delegates to processing.run()
     with thread-safe file-based I/O

3. install()
   - Registers the QGIS backend + triggers tool discovery

QGIS API References
───────────────────
- QgsProcessingRegistry: https://qgis.org/pyqgis/master/core/QgsProcessingRegistry.html
- QgsProcessingAlgorithm: https://qgis.org/pyqgis/master/core/QgsProcessingAlgorithm.html
- QgsProcessingParameterDefinition: https://qgis.org/pyqgis/master/core/QgsProcessingParameterDefinition.html

Data Structures & Complexity
────────────────────────────
- Algorithm lookup: O(N) one-time scan at startup, then O(1) via ToolRegistry dict
- Parameter type mapping: O(1) via _PARAM_TYPE_MAP dict (hash table)
- Fast-path routing: O(1) via _FAST_PATH_ALGORITHMS frozenset
- Raster detection: O(1) via _RASTER_ALGORITHMS frozenset
- Deduplication: O(1) via seen_ids set (hash set)

Thread Safety
─────────────
- auto_discover_qgis_tools: Called once on main thread during plugin init
- _run_qgis_algorithm: Uses file paths (not QgsMapLayer objects) to avoid
  GUI thread crashes. All temp files use uuid4 for collision-free naming.
"""

import logging
import os
import sys
import tempfile
import time
import uuid
from typing import Dict, List, Optional, Set

# ── Ensure plugin directory is importable ─────────────────────────────────
plugin_dir = os.path.dirname(__file__)
if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

# imports below need sys.path set above
from geosi_engine.base import (  # noqa: E402
    register_backend,
    register_expression_validator,
    register_inspector,
)
from geosi_engine.models import Layer, ToolParameter, ToolResult  # noqa: E402

logger = logging.getLogger("geosi_plugin.qgis_bridge")


# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS — Algorithm Classification (O(1) frozen set lookups)
# ═══════════════════════════════════════════════════════════════════════════

# Algorithms whose output is a raster file (need .tif extension)
# Using frozenset for O(1) amortized membership testing via hash table
_RASTER_ALGORITHMS: frozenset = frozenset(
    {
        "native:slope",
        "native:aspect",
        "native:hillshade",
        "native:ruggednessindex",
        "qgis:slope",
        "qgis:aspect",
        "qgis:hillshade",
        "qgis:ruggednessindex",
        "gdal:slope",
        "gdal:aspect",
        "gdal:hillshade",
        "gdal:roughness",
        "gdal:fillnodata",
        "gdal:translate",
        "gdal:warpreproject",
        "gdal:cliprasterbyextent",
        "gdal:cliprasterbymasklayer",
        "gdal:contour",
        "gdal:rastercalculator",
        "native:rastercalc",
        "native:createconstantrasterlayer",
        "native:rastersurfacevolume",
        "native:rastersampling",
        "saga:slopeaspectcurvature",
    }
)

# Algorithms that can be handled by direct PyQGIS API (fast path)
# These bypass processing.run() entirely for sub-millisecond response
_FAST_PATH_ALGORITHMS: frozenset = frozenset(
    {
        "native:countfeatures",
        "native:layerextent",
        "native:layercrs",
        "native:featurecount",
    }
)

# ═══════════════════════════════════════════════════════════════════════════
# PARAMETER TYPE MAPPING — QgsProcessingParameter* → GeoSI string types
#
# The QGIS Processing framework uses ~30+ parameter subclasses. We map
# them to 4 simple types that the LLM can understand and the engine
# can validate: "layer", "number", "boolean", "string"
#
# Complexity: O(1) dict lookup per parameter
# ═══════════════════════════════════════════════════════════════════════════

_PARAM_TYPE_MAP: Dict[str, str] = {
    # ── Layer types → "layer" ──────────────────────────────────────────
    "source": "layer",  # QgsProcessingParameterFeatureSource
    "vector": "layer",  # QgsProcessingParameterVectorLayer
    "raster": "layer",  # QgsProcessingParameterRasterLayer
    "layer": "layer",  # QgsProcessingParameterMapLayer
    "mesh": "layer",  # QgsProcessingParameterMeshLayer
    "multilayer": "layer",  # QgsProcessingParameterMultipleLayers
    "vectordestination": "layer",  # output vector
    "rasterdestination": "layer",  # output raster
    "featureSink": "layer",  # QgsProcessingParameterFeatureSink
    # ── Numeric types → "number" ──────────────────────────────────────
    "number": "number",  # QgsProcessingParameterNumber
    "distance": "number",  # QgsProcessingParameterDistance
    "scale": "number",  # QgsProcessingParameterScale
    "duration": "number",  # QgsProcessingParameterDuration
    "range": "number",  # QgsProcessingParameterRange
    # ── Boolean → "boolean" ───────────────────────────────────────────
    "boolean": "boolean",  # QgsProcessingParameterBoolean
    # ── Everything else → "string" ────────────────────────────────────
    "string": "string",  # QgsProcessingParameterString
    "field": "field",  # QgsProcessingParameterField (checked against layer fields)
    "band": "string",  # QgsProcessingParameterBand
    "expression": "expression",  # QgsProcessingParameterExpression (QgsExpression-validated)
    "crs": "string",  # QgsProcessingParameterCrs
    "enum": "enum",  # QgsProcessingParameterEnum (options listed for the planner)
    "extent": "string",  # QgsProcessingParameterExtent
    "point": "string",  # QgsProcessingParameterPoint
    "geometry": "string",  # QgsProcessingParameterGeometry
    "file": "string",  # QgsProcessingParameterFile
    "folder": "string",  # QgsProcessingParameterFolderDestination
    "matrix": "string",  # QgsProcessingParameterMatrix
    "layout": "string",  # QgsProcessingParameterLayout
    "layoutitem": "string",  # QgsProcessingParameterLayoutItem
    "color": "string",  # QgsProcessingParameterColor
    "datetime": "string",  # QgsProcessingParameterDateTime
    "databaseschema": "string",  # QgsProcessingParameterDatabaseSchema
    "databasetable": "string",  # QgsProcessingParameterDatabaseTable
    "providerconnection": "string",
    "coordinateoperation": "string",
    "maptheme": "string",
    "aggregates": "string",
    "tininputlayers": "string",
    "fieldsmapping": "string",
    "align_rasters": "string",
    "annotation": "string",
}

# ── Category mapping: QGIS group name → GeoSI category ───────────────
# Used to classify dynamically discovered algorithms into categories
# that the LLM can reason about when planning workflows
_GROUP_TO_CATEGORY: Dict[str, str] = {
    "vector": "vector",
    "geometry": "vector",
    "overlay": "vector",
    "selection": "vector",
    "analysis": "vector",
    "table": "vector",
    "raster": "raster",
    "terrain": "terrain",
    "network": "network",
    "interpolation": "raster",
    "mesh": "raster",
    "gps": "cartography",
    "cartography": "cartography",
    "plots": "cartography",
    "modeler": "general",
}

# ── Risk of each algorithm for existing data (see agents.planning) ─────
# Processing algorithms write results to new outputs, so they are
# read-only for existing data unless they act on something in place,
# write into a database or file the user owns, or reach the network.
_DESTRUCTIVE_ALGORITHMS: frozenset = frozenset(
    {
        "native:truncatetable",
        "qgis:postgisexecutesql",
        "native:postgisexecutesql",
        "qgis:postgisexecuteandloadsql",
        "native:postgisexecuteandloadsql",
        "qgis:spatialiteexecutesql",
        "native:spatialiteexecutesql",
        "native:spatialiteexecutesqlregistered",
    }
)
_MUTATING_ALGORITHMS: frozenset = frozenset(
    {
        "native:setprojection",
        "qgis:definecurrentprojection",
        "native:definecurrentprojection",
        "native:createspatialindex",
        "native:createattributeindex",
        "qgis:importintopostgis",
        "native:importintopostgis",
        "qgis:importintospatialite",
        "native:importintospatialite",
        "native:package",
        "native:filedownloader",
        "native:httprequest",
        "native:createdirectory",
        "native:setlayerencoding",
        "native:exporttospreadsheet",
        "native:savelog",
    }
)


def _algorithm_risk(alg_id: str) -> str:
    if alg_id in _DESTRUCTIVE_ALGORITHMS:
        return "destructive"
    if alg_id in _MUTATING_ALGORITHMS:
        return "mutating"
    return "read_only"


# ── Providers to skip (meta-providers that don't have real algorithms) ─
_SKIP_PROVIDERS: frozenset = frozenset(
    {
        "model",  # Graphical modeler (user models, not tools)
        "script",  # User scripts
        "preconfigured",  # Pre-configured algorithms (wrappers)
    }
)


# ═══════════════════════════════════════════════════════════════════════════
# DYNAMIC TOOL DISCOVERY
#
# This function replaces ALL of vector.py, raster.py, terrain.py,
# network.py, ai_ml.py, cartography.py, temporal.py (~2000 lines)
# with ~80 lines of dynamic introspection.
#
# Algorithm: Single-pass O(N) scan of the Processing Registry
# Data structures:
#   - seen_ids: hash set for O(1) dedup
#   - _PARAM_TYPE_MAP: hash dict for O(1) type mapping
#   - _GROUP_TO_CATEGORY: hash dict for O(1) category classification
# ═══════════════════════════════════════════════════════════════════════════


def auto_discover_qgis_tools(registry) -> int:
    """
    Dynamically discover ALL QGIS Processing algorithms and register
    them as GeoSI BackendTool instances.

    This function is the heart of GeoSI v2. Instead of manually defining
    each tool, we introspect the QGIS Processing Registry at runtime:

        QgsApplication.processingRegistry().algorithms()

    Each algorithm exposes:
        - alg.id()                    → "native:buffer"
        - alg.displayName()           → "Buffer"
        - alg.shortHelpString()       → "Creates buffer zones..."
        - alg.group()                 → "Vector geometry"
        - alg.parameterDefinitions()  → list of QgsProcessingParameterDefinition

    We map each parameter's type() string to our simple type system
    (layer/number/boolean/string) and create a BackendTool.

    Args:
        registry: The GeoSI ToolRegistry instance to populate.

    Returns:
        Number of tools successfully registered.

    Complexity:
        Time:  O(N * P) where N = number of algorithms, P = avg params per alg
        Space: O(N) for the seen_ids set + registry storage
        In practice: ~1000 algorithms × ~5 params = ~5000 iterations (~50ms)
    """
    from qgis.core import QgsApplication

    from geosi_engine.base import BackendTool

    # ── Get the processing registry from the running QGIS instance ─────
    proc_registry = QgsApplication.processingRegistry()
    if proc_registry is None:
        logger.error("QgsApplication.processingRegistry() returned None")
        return 0

    # ── Single-pass scan with hash-set deduplication ───────────────────
    # seen_ids prevents duplicate registration (some providers register
    # the same algorithm under multiple prefixes)
    seen_ids: Set[str] = set()
    registered_count = 0
    skipped_count = 0
    error_count = 0
    start_time = time.time()

    for alg in proc_registry.algorithms():
        try:
            alg_id = alg.id()  # e.g. "native:buffer"
            provider_id = alg.provider().id() if alg.provider() else ""

            # ── Skip meta-providers and duplicates (O(1) checks) ───────
            if provider_id in _SKIP_PROVIDERS:
                skipped_count += 1
                continue
            if alg_id in seen_ids:
                skipped_count += 1
                continue
            seen_ids.add(alg_id)

            # select* algorithms only change the selection on the input
            # layer and create nothing; the extract* twins do the same job
            # and produce a layer the agent can return.
            if alg_id.split(":")[-1].startswith("select") or alg_id.endswith("randomselection"):
                skipped_count += 1
                continue

            # ── Skip algorithms that cannot run here (e.g. GRASS or SAGA
            # not installed) so the LLM is never offered them ─────────
            try:
                can_run = alg.canExecute()
                if isinstance(can_run, tuple):
                    can_run = can_run[0]
            except Exception:
                can_run = True
            if not can_run:
                skipped_count += 1
                continue

            # ── Extract algorithm metadata ─────────────────────────────
            display_name = alg.displayName() or alg_id
            description = alg.shortHelpString() or alg.shortDescription() or f"Runs QGIS algorithm: {alg_id}"
            # Truncate overly long help strings to save LLM token budget
            if len(description) > 300:
                description = description[:297] + "..."

            group = (alg.group() or "general").lower()

            # ── Classify into GeoSI category (O(1) dict lookup) ────────
            category = "general"
            for keyword, cat in _GROUP_TO_CATEGORY.items():
                if keyword in group:
                    category = cat
                    break

            # ── Parse parameter definitions ────────────────────────────
            # Each QgsProcessingParameterDefinition exposes:
            #   param.name()        → "INPUT"
            #   param.description() → "Input vector layer"
            #   param.type()        → "source" (for FeatureSource)
            #   param.flags()       → bitfield with FlagHidden, FlagOptional
            #   param.isDestination() → True for output params
            tool_params: List[ToolParameter] = []

            for param in alg.parameterDefinitions():
                # Skip output/destination parameters (OUTPUT, RESULT, etc.)
                # These are handled by the bridge, not the user
                if param.isDestination():
                    continue

                # Skip hidden parameters (internal QGIS flags)
                # QgsProcessingParameterDefinition.FlagHidden = 2
                try:
                    flag_hidden = param.FlagHidden
                except AttributeError:
                    flag_hidden = 2  # fallback value
                if param.flags() & flag_hidden:
                    continue

                # ── Map QGIS parameter type → GeoSI type (O(1)) ───────
                qgis_type = param.type().lower()
                geosi_type = _PARAM_TYPE_MAP.get(qgis_type, "string")

                # ── Determine if parameter is required ─────────────────
                # QgsProcessingParameterDefinition.FlagOptional = 1
                try:
                    flag_optional = param.FlagOptional
                except AttributeError:
                    flag_optional = 1
                is_required = not bool(param.flags() & flag_optional)

                # ── Extract default value for optional params ──────────
                default_val = None
                try:
                    raw_default = param.defaultValue()
                    if raw_default is not None:
                        default_val = str(raw_default)
                except Exception:
                    logger.debug("suppressed exception", exc_info=True)
                # QGIS fills non-optional params that have a default itself
                # (e.g. native:buffer SEGMENTS=5), so only params with no
                # default must come from the plan.
                if default_val is not None:
                    is_required = False

                parent_layer = None
                options: List[str] = []
                if qgis_type == "field":
                    try:
                        parent_layer = param.parentLayerParameterName() or None
                    except Exception:
                        logger.debug("suppressed exception", exc_info=True)
                elif qgis_type == "enum":
                    try:
                        options = [str(o) for o in param.options()]
                    except Exception:
                        logger.debug("suppressed exception", exc_info=True)

                tool_params.append(
                    ToolParameter(
                        name=param.name(),
                        param_type=geosi_type,
                        required=is_required,
                        description=param.description() or param.name(),
                        default=default_val,
                        parent_layer=parent_layer,
                        options=options,
                    )
                )

            # ── Create the GeoSI tool name from the algorithm ID ───────
            # "native:buffer" → "native_buffer"
            # This creates a unique, LLM-friendly identifier
            tool_name = alg_id.replace(":", "_").replace(" ", "_").lower()

            # ── Determine tags for fuzzy search ────────────────────────
            # Split the display name and algorithm name into searchable tokens
            tags = list(set([tool_name] + tool_name.split("_") + display_name.lower().split()))

            # ── Instantiate and register the BackendTool ───────────────
            dynamic_tool = BackendTool(
                name=tool_name,
                display_name=display_name,
                description=description,
                category=category,
                parameters=tool_params,
                qgis_algorithm=alg_id,
                backend="qgis",
                tags=tags,
                risk_level=_algorithm_risk(alg_id),
            )
            registry.register_tool(dynamic_tool)
            registered_count += 1

        except Exception as e:
            error_count += 1
            logger.debug(f"Failed to register {alg_id if 'alg_id' in dir() else '?'}: {e}")

    elapsed_ms = (time.time() - start_time) * 1000
    logger.info(
        f"GeoSI: Dynamic discovery complete in {elapsed_ms:.0f}ms — "
        f"{registered_count} tools registered, "
        f"{skipped_count} skipped, {error_count} errors"
    )
    return registered_count


# ═══════════════════════════════════════════════════════════════════════════
# FAST PATH — Direct PyQGIS API for Simple Operations
#
# For operations that just READ metadata (count, extent, CRS), we bypass
# processing.run() entirely. This avoids:
#   - Temp file creation (disk I/O)
#   - Processing framework overhead (~100ms per call)
#   - Thread-safety issues with QgsProject singleton
#
# Complexity: O(1) for all fast-path operations
# ═══════════════════════════════════════════════════════════════════════════


def _try_fast_path(algorithm_id: str, parameters: dict) -> Optional[ToolResult]:
    """
    Attempt to handle a simple query using direct PyQGIS API calls.

    Returns:
        ToolResult if handled, None if the algorithm needs full processing.run()
    """
    # ── Feature count (O(1) via QgsVectorLayer.featureCount()) ──────────
    if "count" in algorithm_id.lower() or "featurecount" in algorithm_id.lower():
        input_param = parameters.get("INPUT")
        if input_param and hasattr(input_param, "features"):
            qgs_layer = input_param.features
            if qgs_layer and hasattr(qgs_layer, "featureCount"):
                count = qgs_layer.featureCount()
                return ToolResult(
                    success=True,
                    output={"count": count, "layer": input_param.name},
                    message=f"Layer '{input_param.name}' has {count} feature(s).",
                )

    # ── Layer extent (O(1) via QgsMapLayer.extent()) ───────────────────
    if "extent" in algorithm_id.lower() or "boundingbox" in algorithm_id.lower():
        input_param = parameters.get("INPUT")
        if input_param and hasattr(input_param, "features"):
            qgs_layer = input_param.features
            if qgs_layer and hasattr(qgs_layer, "extent"):
                ext = qgs_layer.extent()
                bounds = {
                    "xmin": ext.xMinimum(),
                    "ymin": ext.yMinimum(),
                    "xmax": ext.xMaximum(),
                    "ymax": ext.yMaximum(),
                }
                return ToolResult(
                    success=True,
                    output=bounds,
                    message=f"Extent: {bounds}",
                )

    # ── CRS info (O(1) via QgsMapLayer.crs()) ──────────────────────────
    if "crs" in algorithm_id.lower() or "projection" in algorithm_id.lower():
        input_param = parameters.get("INPUT")
        if input_param and hasattr(input_param, "features"):
            qgs_layer = input_param.features
            if qgs_layer and hasattr(qgs_layer, "crs"):
                crs = qgs_layer.crs()
                return ToolResult(
                    success=True,
                    output={"crs": crs.authid(), "description": crs.description()},
                    message=f"CRS: {crs.authid()} ({crs.description()})",
                )

    # Not a fast-path algorithm → return None to signal full processing
    return None


# ═══════════════════════════════════════════════════════════════════════════
# TEMP FILE GENERATION
#
# Each algorithm output gets a unique temp file path to prevent collisions
# when running concurrent queries. Uses uuid4 for cryptographic randomness.
# ═══════════════════════════════════════════════════════════════════════════


def _make_temp_output(algorithm_id: str, raster: Optional[bool] = None) -> str:
    """Generate a collision-free temp file path with correct extension."""
    uid = uuid.uuid4().hex[:8]
    # Extract the algorithm short name for human-readable filenames
    algo_short = algorithm_id.split(":")[-1] if ":" in algorithm_id else algorithm_id
    # Raster algorithms produce .tif, vector algorithms produce .gpkg
    if raster is None:
        raster = algorithm_id.lower() in _RASTER_ALGORITHMS
    ext = ".tif" if raster else ".gpkg"
    return os.path.join(tempfile.gettempdir(), f"geosi_{algo_short}_{uid}{ext}")


def _detect_layer_type(algorithm_id: str) -> str:
    """Classify algorithm output type using O(1) frozenset lookup."""
    return "raster" if algorithm_id.lower() in _RASTER_ALGORITHMS else "vector"


# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION — processing.run() with Layer Unwrapping
#
# This is the backend callable registered via register_backend("qgis", fn).
# It receives (algorithm_id, parameters_dict) and returns ToolResult.
#
# CRITICAL for thread safety:
#   - Parameters contain GeoSI Layer objects, not raw QgsMapLayer
#   - We unwrap Layer → filepath (string) before passing to processing.run()
#   - This avoids accessing QgsProject (a GUI singleton) from a worker thread
# ═══════════════════════════════════════════════════════════════════════════


def _normalize_params(algorithm_id: str, params: dict) -> dict:
    """
    Make LLM-written parameters acceptable to processing.run():
        - keys matched to the algorithm's real names case-insensitively
          ("input" → INPUT); keys the algorithm doesn't have are dropped
        - destination values from the plan are ignored; every destination
          other than OUTPUT (e.g. REPORT) is set to TEMPORARY_OUTPUT
        - enum values given as option text ("Envelope") become the index
    """
    try:
        from qgis.core import QgsApplication

        alg = QgsApplication.processingRegistry().algorithmById(algorithm_id)
    except Exception:
        alg = None
    if alg is None:
        return params

    defs = {p.name().lower(): p for p in alg.parameterDefinitions()}
    out = {}
    for key, value in params.items():
        param = defs.get(str(key).lower())
        if param is None:
            logger.info(f"Dropping unknown parameter {key!r} for {algorithm_id}")
            continue
        if param.type() == "enum" and isinstance(value, str) and not value.strip().isdigit():
            options = [o.lower() for o in param.options()]
            wanted = value.strip().lower()
            match = next((i for i, o in enumerate(options) if o == wanted or wanted in o), None)
            if match is None:
                continue  # let QGIS use the default instead of failing
            value = match
        if param.isDestination():
            continue  # outputs are always chosen by the bridge, not the plan
        out[param.name()] = value

    for param in alg.destinationParameterDefinitions():
        if param.name() not in out and param.name() != "OUTPUT":
            out[param.name()] = "TEMPORARY_OUTPUT"
    return out


def _output_kind(algorithm_id: str) -> Optional[str]:
    """
    "raster" / "vector" from the algorithm's OUTPUT destination, or None
    when the algorithm only returns values (no layer to write).
    """
    try:
        from qgis.core import QgsApplication

        alg = QgsApplication.processingRegistry().algorithmById(algorithm_id)
    except Exception:
        alg = None
    if alg is None:
        return _detect_layer_type(algorithm_id)
    out = alg.parameterDefinition("OUTPUT")
    if out is None or not out.isDestination():
        return None
    t = out.type().lower()
    if "raster" in t:
        return "raster"
    if t in ("vectordestination", "sink"):
        return "vector"
    return None  # file / folder destinations (html reports etc.)


def field_metadata(lyr, max_values: int = 50):
    """(field_types, field_values) of a QgsVectorLayer for the planner."""
    types, values = {}, {}
    for idx, f in enumerate(lyr.fields()):
        if f.name() == "fid":
            continue
        numeric = f.isNumeric()
        types[f.name()] = "number" if numeric else "text"
        if not numeric:
            try:
                uniq = list(lyr.uniqueValues(idx, max_values + 1))
                if len(uniq) <= max_values:
                    values[f.name()] = [u for u in uniq if u not in (None, "")]
            except Exception:
                logger.debug("suppressed exception", exc_info=True)
    return types, values


def describe_output(path: str, name: str, kind: str) -> Optional[Layer]:
    """Open an output file with QGIS and return a Layer with its real facts."""
    from qgis.core import QgsRasterLayer, QgsVectorLayer, QgsWkbTypes

    if kind == "raster":
        lyr = QgsRasterLayer(path, name)
        if not lyr.isValid():
            return None
        ext = lyr.extent()
        return Layer(
            name=name,
            filepath=path,
            layer_type="raster",
            geometry_type="Raster",
            feature_count=1,
            crs=lyr.crs().authid(),
            bounds={"xmin": ext.xMinimum(), "ymin": ext.yMinimum(), "xmax": ext.xMaximum(), "ymax": ext.yMaximum()},
            fields=[f"band_{i}" for i in range(1, lyr.bandCount() + 1)],
        )
    lyr = QgsVectorLayer(path, name, "ogr")
    if not lyr.isValid():
        return None
    ext = lyr.extent()
    types, values = field_metadata(lyr)
    return Layer(
        name=name,
        filepath=path,
        layer_type="vector",
        geometry_type=QgsWkbTypes.geometryDisplayString(lyr.geometryType()),
        feature_count=lyr.featureCount(),
        crs=lyr.crs().authid(),
        bounds={"xmin": ext.xMinimum(), "ymin": ext.yMinimum(), "xmax": ext.xMaximum(), "ymax": ext.yMaximum()},
        fields=[f.name() for f in lyr.fields()],
        field_types=types,
        field_values=values,
    )


def validate_expression(expression: str) -> Optional[str]:
    """Parse a QGIS expression; returns the parser error, or None when valid."""
    from qgis.core import QgsExpression

    expr = QgsExpression(str(expression))
    if expr.hasParserError():
        return expr.parserErrorString() or "invalid expression"
    return None


def describe_layer(layer: Layer, max_rows: int = 30) -> str:
    """
    Text summary of a layer's contents for the LLM: attribute rows for
    vectors, band statistics for rasters. Registered as the engine's
    layer inspector by install().
    """
    from qgis.core import Qgis, QgsRasterLayer, QgsVectorLayer

    path = getattr(layer, "filepath", "") or ""
    if getattr(layer, "layer_type", "") == "raster":
        lyr = QgsRasterLayer(path, layer.name)
        if not lyr.isValid():
            return f"{layer.name}: unreadable raster"
        lines = [f"raster {layer.name}: {lyr.width()}x{lyr.height()} px, crs {lyr.crs().authid()}"]
        try:
            all_stats = Qgis.RasterBandStatistic.All  # QGIS >= 3.36
        except AttributeError:
            from qgis.core import QgsRasterBandStats

            all_stats = QgsRasterBandStats.All
        for b in range(1, lyr.bandCount() + 1):
            st = lyr.dataProvider().bandStatistics(b, all_stats)
            lines.append(f"  band {b}: min={st.minimumValue:.4g} max={st.maximumValue:.4g} mean={st.mean:.4g}")
        return "\n".join(lines)

    # Open from the file rather than using a live project layer, which may
    # only be touched from the main thread.
    lyr = QgsVectorLayer(path, layer.name, "ogr") if path else None
    if (lyr is None or not lyr.isValid()) and isinstance(getattr(layer, "features", None), QgsVectorLayer):
        lyr = layer.features
    if not lyr.isValid():
        return f"{layer.name}: unreadable layer"
    from qgis.core import QgsWkbTypes

    names = [f.name() for f in lyr.fields() if f.name() != "fid"]
    gtype = lyr.geometryType()
    measure = {
        QgsWkbTypes.GeometryType.LineGeometry: "length_m",
        QgsWkbTypes.GeometryType.PolygonGeometry: "area_m2",
    }.get(gtype)
    lines = [f"layer {layer.name}: {lyr.featureCount()} {layer.geometry_type} features, fields {names}"]
    for i, feat in enumerate(lyr.getFeatures()):
        if i >= max_rows:
            lines.append(f"  ... {lyr.featureCount() - max_rows} more")
            break
        cells = [f"{n}={feat[n]}" for n in names]
        geom = feat.geometry()
        if measure and geom is not None and not geom.isEmpty():
            value = geom.length() if measure == "length_m" else geom.area()
            cells.append(f"{measure}={value:.1f}")
        lines.append("  " + ", ".join(cells))
    return "\n".join(lines)


def _collecting_feedback():
    """QgsProcessingFeedback that keeps reported errors for the agent."""
    from qgis.core import QgsProcessingFeedback

    class _Feedback(QgsProcessingFeedback):
        def __init__(self):
            super().__init__()
            self.errors = []

        def reportError(self, error, fatalError=False):
            self.errors.append(str(error).strip())
            super().reportError(error, fatalError)

    return _Feedback()


def _run_qgis_algorithm(algorithm_id: str, parameters: dict) -> ToolResult:
    """
    Execute a QGIS Processing algorithm with automatic parameter unwrapping
    and fast-path optimization.

    Pipeline:
        1. Try fast-path (direct PyQGIS API) → O(1) for simple queries
        2. Unwrap GeoSI Layer objects → file paths (thread safety)
        3. Redirect memory outputs → temp files (reliability)
        4. Call processing.run() → execute the algorithm
        5. Wrap output → GeoSI Layer object

    Args:
        algorithm_id: QGIS algorithm ID (e.g. "native:buffer")
        parameters: Dict of parameter name → value

    Returns:
        ToolResult with success/failure and output Layer
    """
    # ── Step 1: Try fast-path for simple operations ────────────────────
    fast_result = _try_fast_path(algorithm_id, parameters)
    if fast_result is not None:
        logger.info(f"Fast-path handled: {algorithm_id}")
        return fast_result

    # ── Step 2: Import QGIS Processing (only available inside QGIS) ────
    try:
        import processing
    except ImportError:
        return ToolResult(
            success=False,
            error="QGIS Processing is not available in this environment.",
            message="This tool must be run from inside QGIS.",
        )

    try:
        # ── Step 3: Unwrap GeoSI Layer → file paths ────────────────────
        # This is CRITICAL for thread safety. Passing QgsMapLayer objects
        # to processing.run() from a background thread causes crashes
        # because QgsProject is a main-thread singleton.
        unwrapped_params = {}
        for k, v in parameters.items():
            if isinstance(v, (list, tuple)) and any(hasattr(i, "filepath") for i in v):
                # e.g. LAYERS for merge: a list of GeoSI layers → list of paths
                unwrapped_params[k] = [
                    (
                        (
                            i.filepath
                            if getattr(i, "filepath", "") and os.path.isfile(i.filepath)
                            else getattr(i, "name", i)
                        )
                        if hasattr(i, "filepath")
                        else i
                    )
                    for i in v
                ]
            elif hasattr(v, "filepath") and hasattr(v, "layer_type"):
                # This is a GeoSI Layer object — unwrap it
                if v.filepath and os.path.isfile(v.filepath):
                    unwrapped_params[k] = v.filepath
                elif hasattr(v, "features") and v.features is not None:
                    try:
                        # Try layer ID (safe for cross-thread access)
                        unwrapped_params[k] = v.features.id()
                    except Exception:
                        unwrapped_params[k] = v.features
                else:
                    unwrapped_params[k] = v.name
            else:
                unwrapped_params[k] = v

        unwrapped_params = _normalize_params(algorithm_id, unwrapped_params)

        # ── Step 4: Redirect in-memory outputs to temp files ───────────
        # The file extension follows the algorithm's declared OUTPUT type
        # (raster destination → .tif, otherwise .gpkg).
        output_kind = _output_kind(algorithm_id)
        output_file = None
        if output_kind and unwrapped_params.get("OUTPUT") in ("memory:", "TEMPORARY_OUTPUT", None, ""):
            output_file = _make_temp_output(algorithm_id, raster=(output_kind == "raster"))
            unwrapped_params["OUTPUT"] = output_file
            logger.info(f"Redirected OUTPUT → {output_file}")

        # ── Step 5: Execute via processing.run() ───────────────────────
        logger.info(f"Running {algorithm_id} with {len(unwrapped_params)} params")
        logger.debug(f"  params: {unwrapped_params}")
        start = time.time()
        # A fresh context + feedback per run: safe from the QgsTask worker
        # thread (inputs are file paths, nothing reads the GUI project).
        from qgis.core import QgsProcessingContext

        context = QgsProcessingContext()
        feedback = _collecting_feedback()
        try:
            result = processing.run(algorithm_id, unwrapped_params, context=context, feedback=feedback)
        except Exception as e:
            # Some algorithms copy input fids, which GeoPackage rejects as
            # duplicates. FlatGeobuf has no fid constraint: retry once.
            if output_file and output_file.endswith(".gpkg") and "UNIQUE constraint failed" in str(e):
                output_file = output_file[:-5] + ".fgb"
                unwrapped_params["OUTPUT"] = output_file
                logger.info(f"Retrying {algorithm_id} with FlatGeobuf output (duplicate fids)")
                feedback = _collecting_feedback()
                result = processing.run(
                    algorithm_id, unwrapped_params, context=QgsProcessingContext(), feedback=feedback
                )
            else:
                raise
        elapsed = (time.time() - start) * 1000
        logger.info(f"Completed {algorithm_id} in {elapsed:.0f}ms")

        # ── Step 6: Algorithms with no layer output return values ──────
        # e.g. qgis:basicstatisticsforfields → {"SUM": ..., "COUNT": ...}
        if output_kind is None:
            values = {
                k: v
                for k, v in result.items()
                if isinstance(v, (int, float, str, bool)) and not str(v).endswith((".html", ".htm"))
            }
            summary = ", ".join(f"{k}={v}" for k, v in list(values.items())[:20])
            return ToolResult(
                success=True,
                output=values,
                message=f"{algorithm_id} results: {summary}",
            )

        # ── Step 7: Determine and validate the output path ─────────────
        output_value = result.get("OUTPUT", "")
        output_path = None
        if isinstance(output_value, str) and os.path.isfile(output_value.split("|")[0]):
            output_path = output_value.split("|")[0]
        elif output_file and os.path.isfile(output_file):
            output_path = output_file
        elif hasattr(output_value, "source"):
            src = output_value.source().split("|")[0]
            if os.path.isfile(src):
                output_path = src

        if not output_path:
            return ToolResult(
                success=False,
                error=f"Algorithm {algorithm_id} produced no output file",
                message=f"QGIS algorithm silently failed: {algorithm_id}",
            )

        # ── Step 8: Wrap output as a Layer carrying its real facts ─────
        algo_name = algorithm_id.split(":")[-1] if ":" in algorithm_id else algorithm_id
        output_layer = describe_output(output_path, f"{algo_name}_result", output_kind)
        if output_layer is None:
            return ToolResult(
                success=False,
                error=f"Algorithm {algorithm_id} wrote an unreadable output: {output_path}",
                message=f"QGIS algorithm silently failed: {algorithm_id}",
            )
        logger.info(
            f"Wrapped output: {output_path} ({output_layer.layer_type}, "
            f"{output_layer.geometry_type}, {output_layer.feature_count} features)"
        )
        # Some algorithms also return values next to the layer
        # (e.g. basic statistics: SUM, MEAN, COUNT) — keep them for answers.
        values = {
            k: v for k, v in result.items() if k != "OUTPUT" and isinstance(v, (int, float)) and not isinstance(v, bool)
        }
        message = f"QGIS algorithm completed: {algorithm_id}"
        if values:
            message += " (" + ", ".join(f"{k}={v:g}" for k, v in list(values.items())[:20]) + ")"
        return ToolResult(success=True, output=output_layer, message=message)

    except Exception as e:
        # QGIS often raises a generic "Unable to execute algorithm" and puts
        # the real reason in the feedback log — pass it on so the agent can fix it.
        details = getattr(locals().get("feedback"), "errors", [])
        error = "\n".join([str(e)] + [d for d in details if d and d not in str(e)])
        logger.error(f"QGIS algorithm failed: {algorithm_id}: {error}")
        return ToolResult(
            success=False,
            error=error,
            message=f"QGIS algorithm failed: {algorithm_id}",
        )


# ═══════════════════════════════════════════════════════════════════════════
# INSTALL — The single entry point called by the plugin at startup
# ═══════════════════════════════════════════════════════════════════════════


def install(registry=None) -> int:
    """
    Register the QGIS backend with the universal engine.

    If a ToolRegistry is provided, also triggers dynamic tool discovery.

    Args:
        registry: Optional ToolRegistry to populate with discovered tools.

    Returns:
        Number of dynamically discovered tools (0 if registry not provided).
    """
    register_backend("qgis", _run_qgis_algorithm)
    register_inspector(describe_layer)
    register_expression_validator(validate_expression)
    logger.info("GeoSI: QGIS backend installed.")

    tool_count = 0
    if registry is not None:
        tool_count = auto_discover_qgis_tools(registry)
        logger.info(f"GeoSI: {tool_count} QGIS tools dynamically registered.")

    return tool_count
