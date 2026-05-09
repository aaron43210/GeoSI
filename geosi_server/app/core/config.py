# -*- coding: utf-8 -*-
"""
GeoSI Server Configuration
"""


class Settings:
    """
    Store simple application settings.
    """

    def __init__(self):
        self.app_name = "GeoSI Server"
        self.app_version = "0.1.0"
        self.app_description = "GeoSI FastAPI runtime running alongside the QGIS plugin."


settings = Settings()
