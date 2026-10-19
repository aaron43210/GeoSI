"""
GeoSI Engine — open data and map tools (basemaps, OpenStreetMap, geocoding,
WFS, styling, map export).

Requests run in a background task. Network work happens there; anything that
touches the QGIS project or map canvas goes through ``run_in_ui`` so it runs
on the main thread. Data tools write a file and return it as a Layer, which
the plugin loads like any processing result.
"""

from __future__ import annotations

import os
import tempfile
from typing import Any, Optional

from geosi_engine.base import PortableTool, run_in_ui
from geosi_engine.models import Layer, ToolParameter, ToolResult, ToolSpec

# Tools whose effect is on the map itself (no result layer to verify)
ACTION_TOOL_NAMES = frozenset({"add_basemap", "zoom_to_place", "apply_style", "export_map", "geocode_address"})


class AddBasemapTool(PortableTool):
    """Add an XYZ tile basemap under the project's layers."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="add_basemap",
            display_name="Add Basemap",
            description=(
                "Add a background tile basemap to the map. Providers: osm, carto_light, carto_dark, "
                "esri_satellite, esri_topo, esri_streets, google_satellite, google_hybrid, usgs_topo, "
                "usgs_imagery, stadia_toner, stadia_watercolor, opentopomap."
            ),
            category="data",
            parameters=[ToolParameter("provider", "string", False, "Basemap provider key (default: osm)")],
        )

    def execute(self, provider: str = "osm", **kwargs: Any) -> ToolResult:
        from geosi_data.basemaps import PROVIDERS, add_basemap, resolve_provider

        key = resolve_provider(provider or "osm")
        if key not in PROVIDERS:
            return ToolResult(success=False, error=f"Unknown basemap '{provider}'. Options: {', '.join(PROVIDERS)}")
        label = PROVIDERS[key]["label"]
        run_in_ui(f"Added the {label} basemap.", lambda: add_basemap(key))
        return ToolResult(success=True, message=f"Adding the {label} basemap.", output={"basemap": key})


class FetchOSMTool(PortableTool):
    """Download OpenStreetMap features for a place or bounding box."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="fetch_osm",
            display_name="Fetch OSM Features",
            description=(
                "Download OpenStreetMap features (hospitals, schools, parks, roads, buildings, ...) for a "
                "city or bounding box via the Overpass API, as a new layer."
            ),
            category="data",
            parameters=[
                ToolParameter("category", "string", True, "Feature category, e.g. 'hospitals', 'schools', 'parks'"),
                ToolParameter("location", "string", False, "Place name to search, e.g. 'Leeds'"),
                ToolParameter("bbox", "string", False, "Bounding box 'south,west,north,east' in degrees"),
            ],
        )

    def execute(
        self, category: str, location: Optional[str] = None, bbox: Optional[str] = None, **kwargs: Any
    ) -> ToolResult:
        from geosi_data.osm import fetch_osm_to_file

        box = None
        if bbox:
            parts = [float(x) for x in str(bbox).split(",")]
            if len(parts) != 4:
                return ToolResult(success=False, error="bbox must be 'south,west,north,east'")
            box = tuple(parts)
        if box is None and not location:
            return ToolResult(success=False, error="Say where to search: a place name or a bounding box.")
        try:
            found = fetch_osm_to_file(category, location=location, bbox=box)
        except Exception as exc:  # noqa: BLE001 — network failures are reported to the user
            return ToolResult(success=False, error=f"OpenStreetMap download failed: {exc}")
        if found is None:
            where = location or bbox
            return ToolResult(success=False, error=f"No OpenStreetMap '{category}' found for {where}.")
        layer = Layer(
            name=found["name"],
            geometry_type=found["geometry"],
            feature_count=found["count"],
            crs="EPSG:4326",
            filepath=found["path"],
            layer_type="vector",
        )
        return ToolResult(
            success=True, output=layer, message=f"Downloaded {found['count']} OpenStreetMap '{category}' features."
        )


class GeocodeTool(PortableTool):
    """Find the coordinates of an address or place name."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="geocode_address",
            display_name="Geocode Address",
            description="Convert a street address or place name to longitude/latitude coordinates.",
            category="data",
            parameters=[
                ToolParameter("address", "string", True, "Address or place name"),
                ToolParameter("provider", "string", False, "'nominatim' (default) or 'photon'"),
            ],
        )

    def execute(self, address: str, provider: str = "nominatim", **kwargs: Any) -> ToolResult:
        from geosi_data.geocoding import geocode

        try:
            lon, lat, display_name = geocode(address, provider=provider)
        except Exception as exc:  # noqa: BLE001
            return ToolResult(success=False, error=f"Couldn't find '{address}': {exc}")
        return ToolResult(
            success=True,
            message=f"{display_name}: longitude {lon:.6f}, latitude {lat:.6f}.",
            output={"lon": lon, "lat": lat, "display_name": display_name},
        )


class ZoomToPlaceTool(PortableTool):
    """Find a place and centre the map on it."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="zoom_to_place",
            display_name="Zoom to Place",
            description="Find a place name or address and move the map to it.",
            category="navigation",
            parameters=[ToolParameter("address", "string", True, "Place name or address")],
        )

    def execute(self, address: str, **kwargs: Any) -> ToolResult:
        from geosi_data.geocoding import geocode, zoom_canvas_to

        try:
            lon, lat, display_name = geocode(address)
        except Exception as exc:  # noqa: BLE001
            return ToolResult(success=False, error=f"Couldn't find '{address}': {exc}")
        run_in_ui(f"Map moved to {display_name}.", lambda: zoom_canvas_to(lon, lat))
        return ToolResult(
            success=True,
            message=f"Zooming to {display_name}.",
            output={"lon": lon, "lat": lat, "display_name": display_name},
        )


class ApplyStyleTool(PortableTool):
    """Graduated or categorized symbology for a loaded vector layer."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="apply_style",
            display_name="Apply Layer Style",
            description=(
                "Colour a vector layer by an attribute: style_type 'graduated' (numbers) or 'categorized' "
                "(classes). ramp: viridis, magma, blues, reds, rdylgn, spectral."
            ),
            category="cartography",
            parameters=[
                ToolParameter("layer_name", "layer", True, "Layer to style"),
                ToolParameter("field", "field", True, "Attribute to classify by", parent_layer="layer_name"),
                ToolParameter("style_type", "string", False, "'graduated' (default) or 'categorized'"),
                ToolParameter("classes", "number", False, "Number of classes for graduated (default 5)"),
                ToolParameter("ramp", "string", False, "Colour ramp (default viridis)"),
            ],
        )

    def execute(
        self,
        layer_name: str,
        field: str,
        style_type: str = "graduated",
        classes: int = 5,
        ramp: str = "viridis",
        **kwargs: Any,
    ) -> ToolResult:
        from qgis.core import QgsProject

        layer_name = getattr(layer_name, "name", layer_name)  # a resolved Layer or its name
        layers = QgsProject.instance().mapLayersByName(layer_name)
        if not layers:
            return ToolResult(success=False, error=f"Layer '{layer_name}' is not in the project.")
        if layers[0].fields().indexOf(field) < 0:
            names = ", ".join(f.name() for f in layers[0].fields())
            return ToolResult(success=False, error=f"Layer '{layer_name}' has no field '{field}'. Fields: {names}")

        def apply() -> bool:
            from geosi_engine.cartography.styling import apply_categorized_symbology, apply_graduated_symbology

            target = QgsProject.instance().mapLayersByName(layer_name)[0]
            if style_type == "categorized":
                return apply_categorized_symbology(target, field)
            return apply_graduated_symbology(target, field, classes=int(classes), ramp=ramp)

        run_in_ui(f"Styled {layer_name} by {field}.", apply)
        return ToolResult(success=True, message=f"Styling {layer_name} by {field} ({style_type}).")


class ExportMapTool(PortableTool):
    """Export the map as a print layout (PDF or PNG)."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="export_map",
            display_name="Export Map Layout",
            description="Build a print layout with legend, scale bar and north arrow, and export it as PDF or PNG.",
            category="cartography",
            parameters=[
                ToolParameter("output_path", "string", False, "Output file (.pdf or .png); default in temp folder"),
                ToolParameter("title", "string", False, "Map title"),
                ToolParameter("fmt", "string", False, "'pdf' (default) or 'png'"),
                ToolParameter("dpi", "number", False, "Resolution (default 150)"),
            ],
        )

    def execute(
        self, output_path: str = "", title: str = "", fmt: str = "pdf", dpi: int = 150, **kwargs: Any
    ) -> ToolResult:
        fmt = "png" if str(output_path).lower().endswith(".png") else (fmt or "pdf").lower()
        if not output_path:
            output_path = os.path.join(tempfile.mkdtemp(prefix="geosi_map_"), f"map.{fmt}")
        folder = os.path.dirname(os.path.abspath(output_path))
        if not os.path.isdir(folder):
            return ToolResult(success=False, error=f"Folder does not exist: {folder}")

        def export() -> Any:
            from qgis.core import QgsProject

            from geosi_engine.cartography.layouts import build_print_layout, export_layout

            layout = build_print_layout(QgsProject.instance(), title=title)
            return export_layout(layout, output_path, fmt=fmt, dpi=int(dpi))

        run_in_ui(f"Map exported to {output_path}.", export)
        return ToolResult(success=True, message=f"Exporting the map to {output_path}.", output={"path": output_path})


class FetchWFSTool(PortableTool):
    """Download a feature type from an OGC WFS service as a new layer."""

    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="fetch_wfs",
            display_name="Fetch WFS Layer",
            description="Download a feature type from an OGC Web Feature Service (WFS 1.0/1.1/2.0) as a new layer.",
            category="data",
            parameters=[
                ToolParameter("url", "string", True, "WFS endpoint URL"),
                ToolParameter("typename", "string", True, "Feature type name, e.g. 'topp:states'"),
                ToolParameter("version", "string", False, "'1.0.0', '1.1.0' or '2.0.0' (default)"),
                ToolParameter("max_features", "number", False, "Maximum features (default 5000)"),
            ],
        )

    def execute(
        self, url: str, typename: str, version: str = "2.0.0", max_features: int = 5000, **kwargs: Any
    ) -> ToolResult:
        from qgis.core import (
            QgsCoordinateTransformContext,
            QgsDataSourceUri,
            QgsVectorFileWriter,
            QgsVectorLayer,
            QgsWkbTypes,
        )

        if not str(url).lower().startswith(("http://", "https://")):
            return ToolResult(success=False, error="The WFS URL must start with http:// or https://")
        uri = QgsDataSourceUri()
        uri.setParam("url", url.rstrip("?"))
        uri.setParam("typename", typename)
        uri.setParam("version", version)
        uri.setParam("maxNumFeatures", str(int(max_features)))
        name = typename.split(":")[-1]
        # Not added to the project here: the data is copied to a file and the
        # plugin loads that file on the main thread.
        source = QgsVectorLayer(uri.uri(False), name, "WFS")
        if not source.isValid():
            return ToolResult(success=False, error=f"Couldn't open '{typename}' from {url}.")
        path = os.path.join(tempfile.mkdtemp(prefix="geosi_wfs_"), f"{name}.gpkg")
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        err = QgsVectorFileWriter.writeAsVectorFormatV3(source, path, QgsCoordinateTransformContext(), options)
        if err[0] != QgsVectorFileWriter.WriterError.NoError:
            return ToolResult(success=False, error=f"Couldn't save the WFS data: {err[1]}")
        layer = Layer(
            name=name,
            geometry_type=QgsWkbTypes.displayString(source.wkbType()),
            feature_count=source.featureCount(),
            crs=source.crs().authid(),
            filepath=path,
            layer_type="vector",
        )
        return ToolResult(
            success=True, output=layer, message=f"Downloaded {layer.feature_count} '{typename}' features."
        )
