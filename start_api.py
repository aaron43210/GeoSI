#!/usr/bin/env python3
import os
import sys
import subprocess

# Ensure we are running from the project root
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_DIR)

# Add root to python path
sys.path.insert(0, ROOT_DIR)

print("🌍 Starting GeoSI API Server...")
print("📍 Root Directory:", ROOT_DIR)
print("📖 Docs available at: http://127.0.0.1:8000/docs")
print("-" * 40)

try:
    # Run uvicorn
    subprocess.run([
        "uvicorn", 
        "geosi_server.app.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000", 
        "--reload"
    ])
except KeyboardInterrupt:
    print("\n🛑 Server stopped.")
except Exception as e:
    print(f"\n❌ Error starting server: {e}")
    print("Make sure you have uvicorn installed: pip install uvicorn")
