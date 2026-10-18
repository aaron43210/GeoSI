# -*- coding: utf-8 -*-
"""
GeoSI Data Layer — Project Repository
═══════════════════════════════════════════════════════════════════

CRUD operations for GIS project definitions in PostGIS.
A project groups layers together with a CRS and description.
"""

import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger("geosi_data.project_repository")


class ProjectRepository:
    """
    CRUD repository for GIS project definitions.

    Usage:
        repo = ProjectRepository(database)
        repo.save_project("My Analysis", "Urban flood risk", "EPSG:32643", ["hospitals", "flood_zones"])
    """

    def __init__(self, database):
        self.db = database

    def save_project(
        self,
        name: str,
        description: str = "",
        crs: str = "EPSG:4326",
        layer_names: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> Optional[str]:
        """
        Save or update a project definition.

        Returns:
            Project ID, or None if save failed.
        """
        if not self.db.available:
            return None

        from geosi_data.db_models import ProjectRecord

        try:
            with self.db.get_session() as session:
                existing = (
                    session.query(ProjectRecord)
                    .filter_by(name=name)
                    .first()
                )

                if existing:
                    existing.description = description
                    existing.crs = crs
                    existing.layer_names_json = layer_names or []
                    existing.metadata_json = metadata
                    logger.info(f"Updated project: {name}")
                    return existing.id
                else:
                    record = ProjectRecord(
                        name=name,
                        description=description,
                        crs=crs,
                        layer_names_json=layer_names or [],
                        metadata_json=metadata,
                    )
                    session.add(record)
                    session.flush()
                    logger.info(f"Created project: {name}")
                    return record.id

        except Exception as e:
            logger.error(f"Failed to save project: {e}")
            return None

    def load_project(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a project definition by name."""
        if not self.db.available:
            return None

        from geosi_data.db_models import ProjectRecord

        try:
            with self.db.get_session() as session:
                record = (
                    session.query(ProjectRecord)
                    .filter_by(name=name)
                    .first()
                )
                if record:
                    return self._to_dict(record)
                return None
        except Exception as e:
            logger.error(f"Failed to load project '{name}': {e}")
            return None

    def list_projects(self) -> List[Dict[str, Any]]:
        """List all project definitions."""
        if not self.db.available:
            return []

        from geosi_data.db_models import ProjectRecord

        try:
            with self.db.get_session() as session:
                records = (
                    session.query(ProjectRecord)
                    .order_by(ProjectRecord.created_at.desc())
                    .all()
                )
                return [self._to_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Failed to list projects: {e}")
            return []

    def delete_project(self, name: str) -> bool:
        """Delete a project by name."""
        if not self.db.available:
            return False

        from geosi_data.db_models import ProjectRecord

        try:
            with self.db.get_session() as session:
                record = (
                    session.query(ProjectRecord)
                    .filter_by(name=name)
                    .first()
                )
                if record:
                    session.delete(record)
                    logger.info(f"Deleted project: {name}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to delete project '{name}': {e}")
            return False

    @staticmethod
    def _to_dict(record) -> Dict[str, Any]:
        """Convert a ProjectRecord to a plain dict."""
        return {
            "id": record.id,
            "name": record.name,
            "description": record.description,
            "crs": record.crs,
            "layer_names": record.layer_names_json,
            "metadata": record.metadata_json,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None,
        }
