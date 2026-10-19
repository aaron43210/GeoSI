"""
GeoSI Data Layer — PostGIS Integration
═══════════════════════════════════════════════════════════════════

Provides persistent spatial data storage via PostGIS:
    - Database: Connection pool and session management
    - PostGISManager: GeoDataFrame ↔ PostGIS I/O
    - LayerRepository: CRUD for spatial layers
    - ProjectRepository: CRUD for GIS projects
    - MetadataRepository: Workflow history and execution results
"""

from geosi_data.database import Database
from geosi_data.layer_repository import LayerRepository
from geosi_data.metadata_repository import MetadataRepository
from geosi_data.postgis_manager import PostGISManager
from geosi_data.project_repository import ProjectRepository

__all__ = [
    "Database",
    "PostGISManager",
    "LayerRepository",
    "ProjectRepository",
    "MetadataRepository",
]
