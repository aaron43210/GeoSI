# -*- coding: utf-8 -*-
"""
GeoSI Data Layer — Layer Repository
═══════════════════════════════════════════════════════════════════

CRUD operations for SpatialLayerRecord metadata in PostGIS.
This tracks *metadata* about layers — the actual geometry data
is managed by PostGISManager in separate tables.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

logger = logging.getLogger("geosi_data.layer_repository")


class LayerRepository:
    """
    CRUD repository for spatial layer metadata.

    Usage:
        repo = LayerRepository(database)
        repo.save(layer)
        info = repo.get_by_name("hospitals")
        all_layers = repo.list_all()
    """

    def __init__(self, database):
        self.db = database

    def save(self, layer, table_name: Optional[str] = None) -> Optional[str]:
        """
        Save layer metadata to the geosi_layers table.

        Args:
            layer: GeoSI Layer object
            table_name: PostGIS table where geometries are stored

        Returns:
            Record ID, or None if save failed.
        """
        if not self.db.available:
            return None

        from geosi_data.db_models import SpatialLayerRecord

        try:
            with self.db.get_session() as session:
                # Check if layer already exists
                existing = (
                    session.query(SpatialLayerRecord)
                    .filter_by(name=layer.name)
                    .first()
                )

                if existing:
                    # Update existing record
                    existing.geometry_type = layer.geometry_type
                    existing.crs = layer.crs
                    existing.feature_count = layer.feature_count
                    existing.layer_type = layer.layer_type
                    existing.table_name = table_name
                    existing.filepath = layer.filepath
                    existing.metadata_json = {
                        "fields": layer.fields,
                        "bounds": layer.bounds,
                    }
                    existing.updated_at = datetime.now(timezone.utc)
                    logger.info(f"Updated layer metadata: {layer.name}")
                    return existing.id
                else:
                    # Create new record
                    record = SpatialLayerRecord(
                        name=layer.name,
                        geometry_type=layer.geometry_type,
                        crs=layer.crs,
                        feature_count=layer.feature_count,
                        layer_type=layer.layer_type,
                        table_name=table_name,
                        filepath=layer.filepath,
                        metadata_json={
                            "fields": layer.fields,
                            "bounds": layer.bounds,
                        },
                    )
                    session.add(record)
                    session.flush()
                    logger.info(f"Saved layer metadata: {layer.name}")
                    return record.id

        except Exception as e:
            logger.error(f"Failed to save layer metadata: {e}")
            return None

    def get(self, layer_id: str) -> Optional[Dict[str, Any]]:
        """Get layer metadata by ID."""
        if not self.db.available:
            return None

        from geosi_data.db_models import SpatialLayerRecord

        try:
            with self.db.get_session() as session:
                record = session.get(SpatialLayerRecord, layer_id)
                if record:
                    return self._to_dict(record)
                return None
        except Exception as e:
            logger.error(f"Failed to get layer {layer_id}: {e}")
            return None

    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get layer metadata by name."""
        if not self.db.available:
            return None

        from geosi_data.db_models import SpatialLayerRecord

        try:
            with self.db.get_session() as session:
                record = (
                    session.query(SpatialLayerRecord)
                    .filter_by(name=name)
                    .first()
                )
                if record:
                    return self._to_dict(record)
                return None
        except Exception as e:
            logger.error(f"Failed to get layer '{name}': {e}")
            return None

    def list_all(self) -> List[Dict[str, Any]]:
        """List all layer metadata records."""
        if not self.db.available:
            return []

        from geosi_data.db_models import SpatialLayerRecord

        try:
            with self.db.get_session() as session:
                records = (
                    session.query(SpatialLayerRecord)
                    .order_by(SpatialLayerRecord.created_at.desc())
                    .all()
                )
                return [self._to_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Failed to list layers: {e}")
            return []

    def delete(self, name: str) -> bool:
        """Delete layer metadata by name."""
        if not self.db.available:
            return False

        from geosi_data.db_models import SpatialLayerRecord

        try:
            with self.db.get_session() as session:
                record = (
                    session.query(SpatialLayerRecord)
                    .filter_by(name=name)
                    .first()
                )
                if record:
                    session.delete(record)
                    logger.info(f"Deleted layer metadata: {name}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to delete layer '{name}': {e}")
            return False

    @staticmethod
    def _to_dict(record) -> Dict[str, Any]:
        """Convert a SpatialLayerRecord to a plain dict."""
        return {
            "id": record.id,
            "name": record.name,
            "geometry_type": record.geometry_type,
            "crs": record.crs,
            "feature_count": record.feature_count,
            "layer_type": record.layer_type,
            "table_name": record.table_name,
            "filepath": record.filepath,
            "metadata": record.metadata_json,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None,
        }
