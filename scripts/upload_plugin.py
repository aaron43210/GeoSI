#!/usr/bin/env python3
"""
Upload a built plugin zip to the official QGIS plugin repository.

Credentials come from the environment (an OSGeo ID):
    QGIS_PLUGIN_USER, QGIS_PLUGIN_PASSWORD

Usage:
    python scripts/upload_plugin.py dist/geosi_plugin-<version>.zip
"""

from __future__ import annotations

import os
import sys
import xmlrpc.client
from urllib.parse import quote

ENDPOINT = "plugins.qgis.org/plugins/RPC2/"


def main(zip_path: str) -> int:
    user = os.environ.get("QGIS_PLUGIN_USER")
    password = os.environ.get("QGIS_PLUGIN_PASSWORD")
    if not user or not password:
        print("QGIS_PLUGIN_USER / QGIS_PLUGIN_PASSWORD not set", file=sys.stderr)
        return 1

    url = f"https://{quote(user, safe='')}:{quote(password, safe='')}@{ENDPOINT}"
    server = xmlrpc.client.ServerProxy(url)
    with open(zip_path, "rb") as fh:
        try:
            plugin_id, version_id = server.plugin.upload(xmlrpc.client.Binary(fh.read()))
        except xmlrpc.client.Fault as e:
            print(f"upload failed: {e.faultString}", file=sys.stderr)
            return 1
        except xmlrpc.client.ProtocolError as e:
            print(f"upload failed: HTTP {e.errcode} {e.errmsg}", file=sys.stderr)
            return 1
    print(f"uploaded plugin id={plugin_id} version id={version_id}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
