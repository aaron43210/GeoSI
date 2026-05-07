# -*- coding: utf-8 -*-
"""
GeoSI Engine — Tools Package

This package contains all 130+ GIS tool implementations organized by domain:
    - vector.py     → 40 vector geometry + overlay tools
    - raster.py     → 25 raster terrain + analysis tools
    - network.py    → 8 routing + network analysis tools
    - terrain.py    → 10 3D + terrain analysis tools
    - temporal.py   → 6 time-series analysis tools
    - ai_ml.py      → 10 ML spatial analysis tools
    - validation.py → 10 geometry validation tools
    - cartography.py → 10 export + geocoding tools

Tools are auto-discovered by the ToolRegistry via class introspection.
Each module defines concrete GISTool subclasses.

See FILE_CONNECTIONS.md:
    - IMPORTS FROM: base.py, models.py
    - REGISTERED BY: registry.py (auto-discovery)
"""
