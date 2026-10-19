"""
GeoSI Data Layer — PostGIS Manager
═══════════════════════════════════════════════════════════════════

Handles GeoDataFrame ↔ PostGIS I/O for spatial layer persistence.

Uses geopandas.to_postgis() / read_postgis() for geometry transfer,
creating one PostGIS table per spatial layer.

Design:
    - Layer geometries are stored in dedicated tables (geosi_lyr_<name>)
    - Layer metadata is stored in the geosi_layers table (via LayerRepository)
    - Raster layers store only metadata (filepath), not pixel data
"""

import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger("geosi_data.postgis_manager")


def _sanitize_table_name(name: str) -> str:
    """
    Convert a layer name to a safe PostGIS table name.

    Rules:
        - Lowercase, alphanumeric + underscores only
        - Prefix with 'geosi_lyr_' to avoid collisions
        - Max 63 chars (PostgreSQL identifier limit)
    """
    clean = re.sub(r"[^a-z0-9_]", "_", name.lower())
    clean = re.sub(r"_+", "_", clean).strip("_")
    table = f"geosi_lyr_{clean}"
    return table[:63]


class PostGISManager:
    """
    Manages GeoDataFrame ↔ PostGIS spatial data transfer.

    Usage:
        from geosi_data import Database, PostGISManager
        db = Database()
        pgis = PostGISManager(db)
        pgis.save_layer(layer)
        loaded = pgis.load_layer("hospitals")
    """

    def __init__(self, database):
        """
        Args:
            database: Database instance with an active engine.
        """
        self.db = database
        self._engine = database._engine if database.available else None

    def save_layer(self, layer, table_name: Optional[str] = None) -> str:
        """
        Save a GeoSI Layer's features to a PostGIS table.

        Args:
            layer: GeoSI Layer with a GeoDataFrame in .features
            table_name: Override table name (default: auto-generated from layer.name)

        Returns:
            The PostGIS table name where data was stored.

        Raises:
            RuntimeError: If PostGIS is unavailable or layer has no features.
        """
        if not self._engine:
            raise RuntimeError("PostGIS is not available")

        if not hasattr(layer, "features") or layer.features is None:
            raise RuntimeError(f"Layer '{layer.name}' has no features (GeoDataFrame) to save")

        import geopandas as gpd

        table = table_name or _sanitize_table_name(layer.name)
        gdf = layer.features

        # Register this (sanitizer-produced, regex-safe) table in the SQL
        # allow-list so a later load_layer()/delete_layer() on it passes
        # validate_and_quote() instead of being rejected as "unknown table".
        try:
            from geosi_engine.agents.validation import get_allow_list

            get_allow_list().register(table)
        except Exception:
            logger.debug("suppressed exception", exc_info=True)

        if not isinstance(gdf, gpd.GeoDataFrame):
            raise RuntimeError(f"Layer '{layer.name}' features must be a GeoDataFrame, " f"got {type(gdf).__name__}")

        gdf.to_postgis(
            table,
            self._engine,
            if_exists="replace",
            index=True,
            index_label="gid",
        )

        logger.info(f"Saved layer '{layer.name}' → PostGIS table '{table}' " f"({layer.feature_count} features)")
        return table

    def load_layer(self, table_name: str, layer_name: Optional[str] = None):
        """
        Load a spatial layer from a PostGIS table into a GeoSI Layer.

        Args:
            table_name: PostGIS table name (e.g., 'geosi_lyr_hospitals')
            layer_name: Name to assign to the Layer (default: derived from table)

        Returns:
            GeoSI Layer with features loaded as GeoDataFrame.

        Raises:
            RuntimeError: If PostGIS is unavailable or table not found.
        """
        if not self._engine:
            raise RuntimeError("PostGIS is not available")

        import geopandas as gpd

        from geosi_engine.models import Layer

        try:
            from geosi_engine.agents.validation import get_allow_list

            safe_table = get_allow_list().validate_and_quote(table_name)
            gdf = gpd.read_postgis(
                f"SELECT * FROM {safe_table}",  # nosec B608 — safe_table validated by TableAllowList
                self._engine,
                geom_col="geometry",
            )
        except ValueError as exc:
            raise RuntimeError(f"Unsafe table name rejected: {exc}") from exc
        except Exception as e:
            raise RuntimeError(f"Failed to load table '{table_name}': {e}") from e

        # Derive layer name from table name if not provided
        name = layer_name or table_name.replace("geosi_lyr_", "")

        # Determine geometry type
        geom_type = "Unknown"
        if not gdf.empty and gdf.geometry is not None:
            geom_type = gdf.geometry.iloc[0].geom_type

        # Get CRS
        crs = str(gdf.crs) if gdf.crs else "EPSG:4326"

        # Build bounds
        bounds = {}
        if not gdf.empty:
            total_bounds = gdf.total_bounds
            bounds = {
                "xmin": float(total_bounds[0]),
                "ymin": float(total_bounds[1]),
                "xmax": float(total_bounds[2]),
                "ymax": float(total_bounds[3]),
            }

        layer = Layer(
            name=name,
            geometry_type=geom_type,
            feature_count=len(gdf),
            crs=crs,
            layer_type="vector",
            fields=list(gdf.columns.drop("geometry", errors="ignore")),
        )
        layer.features = gdf
        layer.bounds = bounds

        logger.info(f"Loaded layer '{name}' from PostGIS table '{table_name}' " f"({len(gdf)} features)")
        return layer

    def delete_layer(self, table_name: str) -> bool:
        """
        Drop a PostGIS table.

        Args:
            table_name: Table to drop.

        Returns:
            True if table was dropped successfully.
        """
        if not self._engine:
            raise RuntimeError("PostGIS is not available")

        from sqlalchemy import text

        try:
            from geosi_engine.agents.validation import get_allow_list

            safe_table = get_allow_list().validate_and_quote(table_name)
            with self._engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {safe_table} CASCADE"))
                conn.commit()
            logger.info("Dropped PostGIS table '%s'", table_name)
            return True
        except ValueError as exc:
            logger.error("Unsafe table name rejected for DROP: %s", exc)
            return False
        except Exception as exc:
            logger.error("Failed to drop table '%s': %s", table_name, exc)
            return False

    def list_layers(self) -> List[Dict[str, Any]]:
        """
        List all GeoSI layer tables in the PostGIS database.

        Returns:
            List of dicts with table_name, geometry_type, srid, num_rows.
        """
        if not self._engine:
            return []

        from sqlalchemy import text

        try:
            with self._engine.connect() as conn:
                # Find all geosi_lyr_* tables
                result = conn.execute(
                    text(
                        "SELECT table_name FROM information_schema.tables "
                        "WHERE table_schema = 'public' "
                        "AND table_name LIKE 'geosi_lyr_%'"
                    )
                )
                tables = [row[0] for row in result]

            # These names come from the DB catalog (trusted) and all carry the
            # sanitizer's ``geosi_lyr_`` prefix. Register them so the per-table
            # COUNT(*) below (and later load/delete calls) pass the allow-list.
            # The docstring on TableAllowList states the list is "populated at
            # startup from PostGISManager.list_layers()" — this is where.
            try:
                from geosi_engine.agents.validation import get_allow_list

                get_allow_list().register_many(tables)
            except Exception:
                logger.debug("suppressed exception", exc_info=True)

            layers: List[Dict[str, Any]] = []
            for table in tables:
                info: Dict[str, Any] = {
                    "table_name": table,
                    "name": table.replace("geosi_lyr_", ""),
                }
                try:
                    from geosi_engine.agents.validation import get_allow_list

                    safe_table = get_allow_list().validate_and_quote(table)
                    with self._engine.connect() as conn:
                        # Use allow-list-quoted identifier; COUNT(*) table ref is safe
                        count_result = conn.execute(
                            # safe_table is validated by TableAllowList.validate_and_quote()
                            text(f"SELECT COUNT(*) FROM {safe_table}")  # nosec B608
                        )
                        info["feature_count"] = count_result.scalar()

                        # Parameterized geometry_columns lookup (G4 fix)
                        geom_result = conn.execute(
                            text("SELECT type, srid FROM geometry_columns " "WHERE f_table_name = :tname"),
                            {"tname": table},
                        )
                        geom_row = geom_result.fetchone()
                        if geom_row:
                            info["geometry_type"] = geom_row[0]
                            info["srid"] = geom_row[1]
                except (ValueError, Exception):
                    logger.debug("suppressed exception", exc_info=True)
                layers.append(info)

            return layers
        except Exception as e:
            logger.error(f"Failed to list layers: {e}")
            return []

    def layer_exists(self, table_name: str) -> bool:
        """Check if a PostGIS table exists."""
        if not self._engine:
            return False

        from sqlalchemy import text

        try:
            with self._engine.connect() as conn:
                # Parameterized query — never interpolate table_name (G4 fix)
                result = conn.execute(
                    text(
                        "SELECT EXISTS ("
                        "  SELECT 1 FROM information_schema.tables "
                        "  WHERE table_schema = 'public' "
                        "  AND table_name = :tname"
                        ")"
                    ),
                    {"tname": table_name},
                )
                return bool(result.scalar())
        except Exception:
            return False
