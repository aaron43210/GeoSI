#!/usr/bin/env python3
import subprocess
import sys
import os


def install_dependencies():
    """Install dependencies for the geosi_engine and geosi_server."""
    root_dir = os.path.dirname(os.path.abspath(__file__))

    req_files = [
        os.path.join(root_dir, "requirements.txt"),
        os.path.join(root_dir, "geosi_server", "requirements.txt"),
    ]

    print("--- GeoSI Dependency Installer ---")

    print("\nUpdating pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    for req in req_files:
        if os.path.exists(req):
            print(f"\nInstalling dependencies from: {req}")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", req], check=True)
                print(f"Successfully installed dependencies from {req}")
            except subprocess.CalledProcessError as e:
                print(f"Error installing dependencies for {req}: {e}")
        else:
            print(f"Warning: Requirement file not found at {req}")

    print("\n--- Installation Complete ---")
    print("Start the REST API:   python start_api.py")
    print("Install the CLI:      pip install ./CLI")
    print("Install the QGIS plugin: copy geosi_plugin/ into your QGIS plugins folder")


if __name__ == "__main__":
    install_dependencies()
