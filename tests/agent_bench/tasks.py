"""
Benchmark tasks with machine-checkable answers.

Each task is (id, category, query, check). check(ctx) returns None on pass
or a short reason string on failure. ctx gives:

    ctx.layers      new QGIS layers the agent added to the project
    ctx.answer      the agent's final text answer (lower-cased)
    ctx.vector(geom=None)  first new vector layer, optionally of a geometry
                    type "point" / "line" / "polygon"
    ctx.raster()    first new raster layer
"""

from __future__ import annotations

from .data import FACTS

# ── checker helpers ─────────────────────────────────────────────────────


def _layer(ctx, geom=None, raster=False):
    lyr = ctx.raster() if raster else ctx.vector(geom)
    if lyr is None:
        kind = "raster" if raster else (geom or "vector")
        return None, f"no new {kind} layer"
    return lyr, None


def count(geom, n):
    def check(ctx):
        lyr, err = _layer(ctx, geom)
        if err:
            return err
        got = lyr.featureCount()
        return None if got == n else f"expected {n} {geom} features, got {got}"

    return check


def at_least(geom, n):
    def check(ctx):
        lyr, err = _layer(ctx, geom)
        if err:
            return err
        got = lyr.featureCount()
        return None if got >= n else f"expected >= {n} {geom} features, got {got}"

    return check


def raster_crs(authid):
    def check(ctx):
        lyr, err = _layer(ctx, raster=True)
        if err:
            return err
        return None if lyr.crs().authid() == authid else f"crs {lyr.crs().authid()}"

    return check


def field_values(geom, key_field, value_field, expected, tol=1e-6):
    """Every feature's value_field matches expected[key_field value]."""

    def check(ctx):
        lyr, err = _layer(ctx, geom)
        if err:
            return err
        names = [f.name() for f in lyr.fields()]
        vf = next((n for n in names if n.lower() == value_field.lower()), None)
        if vf is None:
            vf = next((n for n in names if value_field.lower() in n.lower()), None)
        if vf is None or key_field not in names:
            return f"fields {names} lack {key_field}/{value_field}"
        for f in lyr.getFeatures():
            want = expected.get(f[key_field])
            if want is not None and abs(float(f[vf] or 0) - want) > tol:
                return f"{f[key_field]}: {vf}={f[vf]} expected {want}"
        return None

    return check


def has_field(geom, name_part, positive=True):
    def check(ctx):
        lyr, err = _layer(ctx, geom)
        if err:
            return err
        for fld in lyr.fields():
            if name_part in fld.name().lower():
                if positive and any((f[fld.name()] or 0) <= 0 for f in lyr.getFeatures()):
                    return f"field {fld.name()} has non-positive values"
                return None
        return f"no field containing '{name_part}' in {[f.name() for f in lyr.fields()]}"

    return check


def crs(authid, geom=None):
    def check(ctx):
        lyr, err = _layer(ctx, geom)
        if err:
            return err
        return None if lyr.crs().authid() == authid else f"crs {lyr.crs().authid()}"

    return check


def raster_stat(stat, lo, hi, band=1):
    def check(ctx):
        lyr, err = _layer(ctx, raster=True)
        if err:
            return err
        from qgis.core import Qgis

        s = lyr.dataProvider().bandStatistics(band, Qgis.RasterBandStatistic.All)
        v = {"min": s.minimumValue, "max": s.maximumValue, "mean": s.mean}[stat]
        return None if lo <= v <= hi else f"band {band} {stat}={v:.3f} not in [{lo}, {hi}]"

    return check


def answer_mentions(*words):
    def check(ctx):
        missing = [w for w in words if w.lower() not in ctx.answer]
        return None if not missing else f"answer lacks {missing}: {ctx.answer[:120]!r}"

    return check


def all_of(*checks):
    def check(ctx):
        for c in checks:
            err = c(ctx)
            if err:
                return err
        return None

    return check


def no_new_layers(ctx):
    return None if not ctx.layers else f"unexpected layers {[lyr.name() for lyr in ctx.layers]}"


# ── tasks ───────────────────────────────────────────────────────────────

TASKS = [
    # single-step vector
    ("v01", "vector", "buffer hospitals by 500 meters", count("polygon", 10)),
    ("v02", "vector", "create centroids of flood_zones", count("point", 2)),
    ("v03", "vector", "dissolve flood_zones into one polygon", count("polygon", 1)),
    ("v04", "vector", "create voronoi polygons from hospitals", count("polygon", 10)),
    ("v05", "vector", "fix geometries of parcels", count("polygon", 4)),
    ("v06", "vector", "reproject hospitals to EPSG:4326", all_of(count("point", 10), crs("EPSG:4326"))),
    (
        "v07",
        "vector",
        "count the hospitals inside each flood_zones polygon",
        field_values("polygon", "zone", "NUMPOINTS", {k: float(v) for k, v in FACTS["zone_counts"].items()}),
    ),
    ("v08", "vector", "select hospitals that are inside flood_zones", count("point", FACTS["hospitals_in_any_zone"])),
    (
        "v09",
        "vector",
        "find hospitals within 1 km of flood_zones",
        count("point", FACTS["hospitals_within_1km_of_zones"]),
    ),
    ("v10", "vector", "add area field to parcels", has_field("polygon", "area")),
    ("v11", "vector", "calculate the length of each road", has_field("line", "length")),
    ("v12", "vector", "dissolve parcels by owner", count("polygon", 3)),
    ("v13", "vector", "create a convex hull around hospitals", count("polygon", 1)),
    ("v14", "vector", "extract parcels where owner is A", count("polygon", 2)),
    ("v15", "vector", "convert flood_zones polygons to lines", count("line", 2)),
    ("v16", "vector", "create a 1 km grid of polygons covering parcels", count("polygon", 16)),
    ("v17", "vector", "join each hospital to the flood zone it falls in", count("point", 10)),
    # multi-step vector
    ("m01", "multi", "buffer roads by 200 m and dissolve the result", count("polygon", 1)),
    (
        "m02",
        "multi",
        "buffer flood_zones by 1 km then select hospitals inside the buffer",
        count("point", FACTS["hospitals_within_1km_of_zones"]),
    ),
    (
        "m03",
        "multi",
        "reproject parcels to EPSG:4326 and then compute their centroids",
        all_of(count("point", 4), crs("EPSG:4326", "point")),
    ),
    ("m04", "multi", "find hospitals outside all flood_zones and buffer them by 300 m", count("polygon", 5)),
    (
        "m05",
        "multi",
        "dissolve parcels by owner and add an area field",
        all_of(count("polygon", 3), has_field("polygon", "area")),
    ),
    # raster / terrain
    ("r01", "raster", "calculate slope from dem", raster_stat("max", 1, 89)),
    ("r02", "raster", "create a hillshade of dem", raster_stat("max", 1, 255)),
    ("r03", "raster", "compute aspect of dem", raster_stat("max", 180, 360)),
    ("r04", "raster", "generate contour lines every 50 m from dem", at_least("line", 5)),
    (
        "r05",
        "raster",
        "calculate NDVI from image using band 3 as red and band 4 as NIR",
        raster_stat("max", 0.75, 0.85),
    ),
    ("r06", "raster", "reproject dem to EPSG:4326", raster_crs("EPSG:4326")),
    ("r07", "raster", "clip dem to flood_zones", raster_stat("max", 100, 500)),
    # questions (answer must be in text)
    ("q01", "question", "how many hospitals are there?", answer_mentions(str(FACTS["hospitals_count"]))),
    ("q02", "question", "which flood zone has the most hospitals?", answer_mentions(FACTS["zone_with_most_hospitals"])),
    (
        "q03",
        "question",
        "how many hospitals are inside flood zones?",
        answer_mentions(str(FACTS["hospitals_in_any_zone"])),
    ),
    (
        "q04",
        "question",
        "what is the total number of beds across all hospitals?",
        answer_mentions(str(FACTS["beds_total"])),
    ),
    ("q05", "question", "how many parcels does owner A have?", answer_mentions("2")),
    # should refuse / ask instead of guessing
    ("x01", "refuse", "buffer the schools layer by 100 m", no_new_layers),
    ("x02", "refuse", "delete all hospitals", no_new_layers),
]


# ── held-out tasks ──────────────────────────────────────────────────────
# Written after the planner was tuned on TASKS and never used for tuning;
# run with --holdout to get an honest estimate on unseen phrasings.

HOLDOUT_TASKS = [
    ("h01", "vector", "make 250 m buffers around the roads", count("polygon", 3)),
    ("h02", "question", "what is the average number of beds per hospital?", answer_mentions("162.5")),
    ("h03", "vector", "give me the hospitals that are not in any flood zone", count("point", 5)),
    ("h04", "question", "how many hospitals have more than 200 beds?", answer_mentions("3")),
    ("h05", "vector", "simplify flood_zones with a tolerance of 10 m", count("polygon", 2)),
    ("h06", "vector", "extract hospitals with more than 100 beds", count("point", 7)),
    ("h07", "vector", "compute the centroid of every parcel", count("point", 4)),
    ("h08", "vector", "produce a 2 km hexagon grid over flood_zones", at_least("polygon", 2)),
    ("h09", "vector", "merge flood_zones and parcels into one layer", count("polygon", 6)),
    ("h10", "question", "which owner has the most parcels?", answer_mentions("A")),
    ("h11", "question", "list the hospitals inside zone Z2", answer_mentions("H5", "H6", "H7")),
    ("h12", "vector", "reproject roads to EPSG:3857", all_of(count("line", 3), crs("EPSG:3857"))),
    ("h13", "question", "what is the highest elevation in dem?", answer_mentions("500")),
    ("h14", "multi", "create a hillshade from dem then clip it to flood_zones", raster_stat("max", 1, 255)),
    ("h15", "question", "how long is road R1 in metres?", answer_mentions("6000")),
    ("h16", "vector", "find the parcels owned by C", count("polygon", 1)),
    (
        "h17",
        "vector",
        "add the x and y coordinates of each hospital as fields",
        has_field("point", "x", positive=False),
    ),
    ("h18", "refuse", "drop the roads layer", no_new_layers),
    ("h19", "vector", "clip hospitals to flood_zones", count("point", 5)),
    ("h20", "multi", "extract parcels of owner A and dissolve them", count("polygon", 1)),
]


# ── blind tasks ─────────────────────────────────────────────────────────
# Reserve set: run with --blind for an estimate on unseen request types.
# Do not tune the planner on these; when they stop being informative,
# replace them with new ones.

BLIND_TASKS = [
    ("b01", "vector", "create 5 random points inside each flood zone", count("point", 10)),
    ("b02", "question", "how many roads are longer than 4 km?", answer_mentions("2")),
    ("b03", "raster", "calculate the mean elevation of dem within each flood zone", has_field("polygon", "mean")),
    ("b04", "raster", "rasterize parcels using the value field with 100 m cells", raster_stat("max", 300, 400)),
    ("b05", "raster", "create a heatmap of hospitals with a 1 km radius", raster_stat("max", 1e-9, 1e12)),
    ("b06", "question", "which hospital has the most beds?", answer_mentions("H9")),
    ("b07", "question", "list the owners of parcels", answer_mentions("A", "B", "C")),
    ("b08", "multi", "buffer each road by 100 m, dissolve them, and count the hospitals inside", count("polygon", 1)),
    ("b09", "vector", "extract the vertices of roads", at_least("point", 6)),
    ("b10", "question", "how many flood zones have high risk?", answer_mentions("1")),
    ("b11", "multi", "create a 500 m buffer around hospital H3", count("polygon", 1)),
    ("b12", "vector", "smooth the roads", count("line", 3)),
    ("b13", "raster", "reproject image to EPSG:4326", raster_crs("EPSG:4326")),
    ("b14", "question", "what is the lowest elevation in dem?", answer_mentions("100")),
    ("b15", "question", "how many hospitals are within 1.6 km of road R1?", answer_mentions("2")),
]
