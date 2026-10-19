"""
Synthetic benchmark data with known answers (requires QGIS + GDAL).

All layers are in EPSG:32643 (UTM 43N, metres) around x=500000, y=1400000.

    hospitals   10 points  fields: name, beds
    flood_zones  2 polygons fields: zone, risk      Z1 holds H0,H1   Z2 holds H5,H6,H7
    roads        3 lines    fields: road, type      R1 horizontal 6 km, R2 vertical 3 km, R3 diagonal
    parcels      4 polygons fields: owner, value    2x2 grid of 2 km squares, owners A,A,B,C
    dem          raster 100x100 @ 30 m, a single smooth hill (max at the centre)
    image        raster 4 bands (B,G,R,NIR) 50x50 @ 60 m; left half vegetated, right half bare

Geometry facts used by the checkers are kept in FACTS.
"""

from __future__ import annotations

import math
import os

FACTS = {
    "hospitals_count": 10,
    "zone_counts": {"Z1": 2, "Z2": 3},
    "zone_with_most_hospitals": "Z2",
    "hospitals_in_any_zone": 5,
    "hospitals_within_1km_of_zones": 7,  # in a zone or within 1 km of one
    "parcels_by_owner": {"A": 2, "B": 1, "C": 1},
    "road_r1_length": 6000.0,
    "dem_max": 500.0,
    "beds_total": sum(50 + 25 * i for i in range(10)),
}

HOSPITALS = [
    # (name, x, y)       inside Z1 -> H0, H1 ; inside Z2 -> H5, H6, H7
    ("H0", 500500, 1400500),
    ("H1", 501500, 1401500),
    ("H2", 503500, 1400500),  # 500 m east of Z1
    ("H3", 504200, 1401000),  # 1.2 km east of Z1
    ("H4", 505600, 1401000),  # 600 m west of Z2
    ("H5", 507000, 1401000),
    ("H6", 508000, 1402000),
    ("H7", 509000, 1401500),
    ("H8", 500500, 1406000),  # far north
    ("H9", 512500, 1405500),  # far north-east
]
ZONES = [
    ("Z1", "high", "POLYGON((500000 1400000,503000 1400000,503000 1402000,500000 1402000,500000 1400000))"),
    ("Z2", "medium", "POLYGON((506200 1400200,510000 1400200,510000 1403000,506200 1403000,506200 1400200))"),
]
ROADS = [
    ("R1", "primary", "LINESTRING(500000 1399000,506000 1399000)"),
    ("R2", "secondary", "LINESTRING(511000 1399000,511000 1402000)"),
    ("R3", "track", "LINESTRING(500000 1404000,504000 1407000)"),
]
PARCELS = [
    ("A", 100, "POLYGON((500000 1408000,502000 1408000,502000 1410000,500000 1410000,500000 1408000))"),
    ("A", 200, "POLYGON((502000 1408000,504000 1408000,504000 1410000,502000 1410000,502000 1408000))"),
    ("B", 300, "POLYGON((500000 1410000,502000 1410000,502000 1412000,500000 1412000,500000 1410000))"),
    ("C", 400, "POLYGON((502000 1410000,504000 1410000,504000 1412000,502000 1412000,502000 1410000))"),
]
CRS = "EPSG:32643"


def _vector(path, name, geom, fields, rows):
    from qgis.core import (
        QgsCoordinateTransformContext,
        QgsFeature,
        QgsField,
        QgsGeometry,
        QgsPointXY,
        QgsVectorFileWriter,
        QgsVectorLayer,
    )
    from qgis.PyQt.QtCore import QMetaType

    types = {str: QMetaType.Type.QString, int: QMetaType.Type.Int, float: QMetaType.Type.Double}
    mem = QgsVectorLayer(f"{geom}?crs={CRS}", name, "memory")
    pr = mem.dataProvider()
    pr.addAttributes([QgsField(n, types[t]) for n, t in fields])
    mem.updateFields()
    for *attrs, g in rows:
        f = QgsFeature(mem.fields())
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(*g)) if isinstance(g, tuple) else QgsGeometry.fromWkt(g))
        f.setAttributes(list(attrs))
        pr.addFeature(f)
    opts = QgsVectorFileWriter.SaveVectorOptions()
    opts.driverName = "GPKG"
    opts.layerName = name
    err = QgsVectorFileWriter.writeAsVectorFormatV3(mem, path, QgsCoordinateTransformContext(), opts)
    assert err[0] == QgsVectorFileWriter.WriterError.NoError, err


def _raster(path, bands, x0, y0, res):
    from osgeo import gdal, osr

    h, w = len(bands[0]), len(bands[0][0])
    ds = gdal.GetDriverByName("GTiff").Create(path, w, h, len(bands), gdal.GDT_Float32)
    ds.SetGeoTransform((x0, res, 0, y0, 0, -res))
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(32643)
    ds.SetProjection(srs.ExportToWkt())
    for i, band in enumerate(bands, start=1):
        import numpy as np

        b = ds.GetRasterBand(i)
        b.WriteArray(np.array(band, dtype="float32"))
        b.SetNoDataValue(-9999)
    ds.FlushCache()
    ds = None


def build(out_dir: str) -> dict:
    """Write all benchmark layers into out_dir; return {layer_name: path}."""
    os.makedirs(out_dir, exist_ok=True)
    paths = {}

    p = paths["hospitals"] = os.path.join(out_dir, "hospitals.gpkg")
    _vector(
        p,
        "hospitals",
        "Point",
        [("name", str), ("beds", int)],
        [(n, 50 + 25 * i, (x, y)) for i, (n, x, y) in enumerate(HOSPITALS)],
    )
    p = paths["flood_zones"] = os.path.join(out_dir, "flood_zones.gpkg")
    _vector(p, "flood_zones", "Polygon", [("zone", str), ("risk", str)], ZONES)
    p = paths["roads"] = os.path.join(out_dir, "roads.gpkg")
    _vector(p, "roads", "LineString", [("road", str), ("type", str)], ROADS)
    p = paths["parcels"] = os.path.join(out_dir, "parcels.gpkg")
    _vector(p, "parcels", "Polygon", [("owner", str), ("value", int)], PARCELS)

    # DEM: one smooth hill, 500 m at the centre, 100 m at the corners
    n = 100
    dem = [[100 + 400 * math.exp(-(((c - 50) ** 2 + (r - 50) ** 2) / 600.0)) for c in range(n)] for r in range(n)]
    p = paths["dem"] = os.path.join(out_dir, "dem.tif")
    _raster(p, [dem], 500000, 1403000, 30)

    # Image: B, G, R, NIR. Left half vegetation (NIR >> R), right half bare soil.
    m = 50

    def band(left, right):
        return [[left if c < m // 2 else right for c in range(m)] for _ in range(m)]

    p = paths["image"] = os.path.join(out_dir, "image.tif")
    _raster(p, [band(0.04, 0.12), band(0.08, 0.14), band(0.05, 0.20), band(0.50, 0.25)], 500000, 1403000, 60)
    return paths
