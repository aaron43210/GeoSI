#!/usr/bin/env python3
"""
Comprehensive GeoSI API Test Suite
Tests all endpoints including shapefile export functionality

OVERALL WORKFLOW:
================
1. Health Check → Verify API is running
2. Load Data → Load shapefiles (Schools, Kerala) into API state
3. List Layers → Verify loaded layers are accessible
4. Analyze Query → Test NLP query parsing and execution plan generation
5. List Tools → Verify 127+ GIS tools are available
6. Export Clip → Perform spatial clip operation (Schools clipped to Kerala boundary)
7. Export Buffer → Create buffer zones (500m around each school)
8. File Verification → Verify all companion files created (.shp, .shx, .dbf, .prj, .cpg)

DETAILED PROCESS EXPLANATIONS:

CLIP OPERATION WORKFLOW (Test 4):
─────────────────────────────────
Query: "Clip Schools to Kerala"
Input Layers:
  - Schools: 34 point features (school locations)
  - Kerala: 1 polygon feature (state boundary)

Process:
  1. Parse Query → Extract intent "clip", primary layer "Schools", overlay layer "Kerala"
  2. Plan Execution → Create ToolStep with tool_name="clip", parameters={INPUT: Schools, OVERLAY: Kerala}
  3. Execute Clip → GeoPandas.clip(Schools, Kerala)
     - For each school point, check if it falls within Kerala polygon
     - Keep schools inside Kerala boundary
     - Discard schools outside Kerala boundary
  4. Convert to GeoDataFrame → Extract geometry and attributes
  5. Export as Shapefile → Create .shp file with all companion files
     
Output: schools_clipped_test.shp (34 features, Point geometry)
Files Created:
  - schools_clipped_test.shp (1.0KB) → Geometry data
  - schools_clipped_test.shx (0.4KB) → Index for fast access
  - schools_clipped_test.dbf (5.0KB) → Attribute database (feature properties)
  - schools_clipped_test.prj (0.1KB) → Projection/CRS definition
  - schools_clipped_test.cpg (0.0KB) → Code page (encoding)

BUFFER OPERATION WORKFLOW (Test 5):
──────────────────────────────────
Query: "Buffer Schools by 500 meters"
Input Layer:
  - Schools: 34 point features

Process:
  1. Parse Query → Extract intent "buffer", layer "Schools", distance "500 meters"
  2. Convert Distance → 500 meters (spatial unit)
  3. Plan Execution → Create ToolStep with tool_name="buffer", parameters={INPUT: Schools, DISTANCE: 500}
  4. Execute Buffer → For each school point:
     - Create a circle/polygon around point with 500m radius
     - Buffer geometry = circle buffer around point feature
     - All 34 points become 34 polygon geometries
  5. Combine Results → Stack all buffer polygons into single layer
  6. Convert to GeoDataFrame → Extract buffer geometries and attributes
  7. Export as Shapefile → Create .shp file with all companion files

Output: schools_buffer_test.shp (34 features, Polygon geometry)
Files Created:
  - schools_buffer_test.shp (36.5KB) → Geometry data (larger due to complex polygons)
  - schools_buffer_test.shx (0.4KB) → Index
  - schools_buffer_test.dbf (5.0KB) → Attributes
  - schools_buffer_test.prj (0.1KB) → Projection
  - schools_buffer_test.cpg (0.0KB) → Encoding

KEY DIFFERENCES:
  Clip: Spatial intersection → output geometry type same as input (Point → Point)
  Buffer: Spatial expansion → output geometry always Polygon regardless of input
"""

import requests
import json
import os
import shutil
from pathlib import Path
from datetime import datetime

API = "http://127.0.0.1:8000"
TEST_OUTPUT_DIR = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Colors for terminal output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def print_header(title):
    """Print formatted header"""
    print(f"\n{BLUE}{'='*70}{NC}")
    print(f"{BLUE}{title.center(70)}{NC}")
    print(f"{BLUE}{'='*70}{NC}\n")

def print_test(name, passed, message=""):
    """Print test result"""
    status = f"{GREEN}✅ PASS{NC}" if passed else f"{RED}❌ FAIL{NC}"
    print(f"{status} | {name}")
    if message:
        print(f"       {message}")

def test_health_check():
    """Test 1: API Health Check
    
    PURPOSE: Verify the API server is running and responsive
    
    WORKFLOW:
    1. Send GET request to /api/health endpoint
    2. Check response status code (200 = OK)
    3. If API is down, all other tests will fail
    
    EXPECTED RESULT: HTTP 200 status code
    """
    print_header("TEST 1: API Health Check")
    try:
        r = requests.get(f"{API}/api/health", timeout=5)
        passed = r.status_code == 200
        print_test("API Health Check", passed, f"Status: {r.status_code}")
        return passed
    except Exception as e:
        print_test("API Health Check", False, f"Error: {str(e)}")
        return False

def test_load_data():
    """Test 2: Load Test Data
    
    PURPOSE: Load GIS layers (shapefiles) into the API workspace
    
    WORKFLOW FOR EACH LAYER:
    1. Schools.shp:
       - File path: Data_06_2_2026/Schools.shp
       - Reads shapefile with 34 point features
       - Each point = one school location with attributes (name, type, etc)
       - CRS: Projected coordinate system
    
    2. Kerala.shp:
       - File path: Data_06_2_2026/Kerala.shp
       - Reads shapefile with 14 polygon features
       - Each polygon = administrative boundary (district/region)
       - CRS: Same as Schools for spatial operations
    
    TECHNICAL STEPS:
    a) Send POST request: /api/layers/load
    b) Include JSON: {"name": "Schools", "filepath": "..."}
    c) API reads shapefile with OGR/GDAL
    d) Parses geometry (points/polygons)
    e) Stores in WorkspaceState for later operations
    f) Returns success status and feature count
    
    EXPECTED RESULTS:
    - Schools: 34 features loaded
    - Kerala: 14 features loaded
    - Both layers ready for spatial operations (clip, buffer, etc)
    """
    print_header("TEST 2: Load Test Data")
    all_passed = True
    
    test_data = [
        ("Schools", "Data_06_2_2026/Schools.shp"),
        ("Kerala", "Data_06_2_2026/Kerala.shp"),
    ]
    
    for name, filepath in test_data:
        try:
            # Send layer load request to API
            r = requests.post(f"{API}/api/layers/load",
                            json={"name": name, "filepath": filepath},
                            timeout=10)
            data = r.json()
            passed = r.status_code == 200 and data.get("success")
            msg = f"Features: {data.get('feature_count', 'N/A')}"
            print_test(f"Load {name}", passed, msg)
            all_passed = all_passed and passed
        except Exception as e:
            print_test(f"Load {name}", False, f"Error: {str(e)}")
            all_passed = False
    
    return all_passed

def test_list_layers():
    """Test 3: List Loaded Layers
    
    PURPOSE: Retrieve list of all loaded layers from workspace state
    
    WORKFLOW:
    1. Send GET request to /api/layers endpoint
    2. API queries WorkspaceState for all loaded layers
    3. For each layer, collect:
       - name: Layer identifier (Schools, Kerala)
       - feature_count: Number of features (34, 14)
       - geometry_type: Point, Polygon, LineString, etc
       - crs: Coordinate Reference System
    4. Return JSON array of layer metadata
    
    RESPONSE FORMAT:
    [
      {
        "name": "Schools",
        "feature_count": 34,
        "geometry_type": "Point",
        "crs": "EPSG:32643"
      },
      {
        "name": "Kerala",
        "feature_count": 14,
        "geometry_type": "Polygon",
        "crs": "EPSG:32643"
      }
    ]
    
    EXPECTED RESULT: At least 2 layers returned (Schools, Kerala)
    """
    print_header("TEST 3: List Loaded Layers")
    try:
        r = requests.get(f"{API}/api/layers", timeout=10)
        data = r.json()
        passed = r.status_code == 200 and len(data) >= 2
        print_test("List Layers", passed, f"Layers found: {len(data)}")
        
        if passed:
            for layer in data:
                print(f"       • {layer['name']}: {layer['feature_count']} features ({layer['geometry_type']})")
        
        return passed
    except Exception as e:
        print_test("List Layers", False, f"Error: {str(e)}")
        return False

def test_export_clip():
    """Test 4: Export Clip Operation
    
    PURPOSE: Test spatial clip operation - extract schools within Kerala boundary
    
    DETAILED CLIP WORKFLOW:
    ═══════════════════════
    Query: "Clip Schools to Kerala"
    
    STEP 1 - PARSE QUERY:
    ──────────────────────
    Input: "Clip Schools to Kerala"
    Parser extracts:
      - Intent: VECTOR (spatial operation on vector data)
      - Tool: clip
      - Primary layer: Schools (34 points)
      - Overlay layer: Kerala (14 polygons)
    
    STEP 2 - CREATE EXECUTION PLAN:
    ────────────────────────────────
    Plan {
      step_id: "step_1",
      tool_name: "clip",
      parameters: {
        INPUT: "Schools",      // Primary layer (points to be clipped)
        OVERLAY: "Kerala"      // Boundary layer (clipping boundary)
      },
      output_name: "step_1_output"
    }
    
    STEP 3 - EXECUTE SPATIAL CLIP:
    ──────────────────────────────
    Algorithm: GeoPandas.clip(gdf_schools, gdf_kerala)
    
    For each of 34 school points:
      IF point.geometry.within(kerala_polygon) THEN
        Keep point in output
      ELSE
        Discard point (outside boundary)
    
    Result: All 34 schools fall within Kerala → output has 34 features
    (If some were outside, those would be excluded)
    
    STEP 4 - CONVERT TO GEODATAFRAME:
    ─────────────────────────────────
    Extract:
      - Geometry: Point coordinates
      - Attributes: name, district, school_type, etc
      - CRS: EPSG:32643 (projected coordinate system)
    
    STEP 5 - EXPORT TO SHAPEFILE:
    ──────────────────────────────
    Create 5 companion files:
      1. schools_clipped_test.shp (1.0KB)
         → Binary geometry data (point coordinates)
      2. schools_clipped_test.shx (0.4KB)
         → Index file for fast random access
      3. schools_clipped_test.dbf (5.0KB)
         → Attribute database (feature properties: name, district, etc)
      4. schools_clipped_test.prj (0.1KB)
         → Projection file (CRS definition: EPSG:32643)
      5. schools_clipped_test.cpg (0.0KB)
         → Code page file (character encoding: UTF-8)
    
    EXPECTED RESULTS:
    ──────────────────
    - Success: true
    - Features: 34 (all schools inside Kerala)
    - Geometry Type: Point (same as input)
    - Files Created: 5 companion files
    - File Size: ~6.5KB total
    """
    print_header("TEST 4: Export Clip Operation")
    try:
        os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
        
        # Send export request with clip query
        r = requests.post(f"{API}/api/export",
                         json={
                             "query": "Clip Schools to Kerala",
                             "filename": "schools_clipped_test",
                             "output_dir": TEST_OUTPUT_DIR
                         },
                         timeout=30)
        
        result = r.json()
        # Verify: successful, 34 features, Point geometry
        passed = (r.status_code == 200 and 
                 result.get("success") and 
                 result.get("features_count") == 34 and
                 result.get("geometry_type") == "Point")
        
        msg = f"Features: {result.get('features_count')}, Geometry: {result.get('geometry_type')}"
        print_test("Export Clip", passed, msg)
        
        if result.get("files"):
            print(f"       Files created: {len(result['files'])}")
            for f in result['files'][:3]:
                print(f"       • {os.path.basename(f)}")
        
        return passed, result
    except Exception as e:
        print_test("Export Clip", False, f"Error: {str(e)}")
        return False, {}

def test_export_buffer():
    """Test 5: Export Buffer Operation
    
    PURPOSE: Test buffer operation - create 500m zones around schools
    
    DETAILED BUFFER WORKFLOW:
    ════════════════════════
    Query: "Buffer Schools by 500 meters"
    
    STEP 1 - PARSE QUERY:
    ──────────────────────
    Input: "Buffer Schools by 500 meters"
    Parser extracts:
      - Intent: VECTOR (spatial operation)
      - Tool: buffer
      - Input layer: Schools (34 points)
      - Distance: 500 meters
      - Unit: meters (from projected CRS)
    
    STEP 2 - CREATE EXECUTION PLAN:
    ────────────────────────────────
    Plan {
      step_id: "step_1",
      tool_name: "buffer",
      parameters: {
        INPUT: "Schools",        // Layer to buffer
        DISTANCE: 500,          // Buffer radius in meters
        DISSOLVE: false         // Keep individual buffers separate
      },
      output_name: "step_1_output"
    }
    
    STEP 3 - EXECUTE BUFFER OPERATION:
    ──────────────────────────────────
    Algorithm: GeoPandas.buffer(geometry, distance=500)
    
    For each of 34 school points:
      1. Get point location (x, y coordinates)
      2. Create circle around point with 500m radius
      3. Convert circle to polygon geometry
      4. Add to output layer
    
    Geometric Transformation:
      Input geometry:  Point(x, y)
      ↓ (buffer operation with 500m radius)
      Output geometry: Polygon (circular shape, ~628m diameter)
    
    Result: 34 point features → 34 polygon features
    (One polygon for each school)
    
    STEP 4 - COMBINE BUFFER RESULTS:
    ────────────────────────────────
    Stack all 34 polygon buffers into single GeoDataFrame:
    [
      Polygon(school_1_buffer) with name="School A", district="...",
      Polygon(school_2_buffer) with name="School B", district="...",
      ...
      Polygon(school_34_buffer) with name="School Z", district="..."
    ]
    
    STEP 5 - EXPORT TO SHAPEFILE:
    ──────────────────────────────
    Create 5 companion files:
      1. schools_buffer_test.shp (36.5KB)
         → Binary polygon geometries (much larger than points!)
         → Each polygon = circle around school
         → Larger size due to polygon complexity
      2. schools_buffer_test.shx (0.4KB)
         → Index file
      3. schools_buffer_test.dbf (5.0KB)
         → Attributes (inherited from Schools layer)
      4. schools_buffer_test.prj (0.1KB)
         → Projection file (same CRS as input)
      5. schools_buffer_test.cpg (0.0KB)
         → Code page file
    
    FILE SIZE COMPARISON:
    ─────────────────────
    Clipped Points:    1.0KB (simple point coordinates)
    Buffered Polygons: 36.5KB (complex polygon coordinates)
    
    Why difference? Polygons need many vertices to represent circular shape:
      Point = 1 coordinate pair (x, y)
      Circle = ~32+ coordinate pairs (approximation)
    
    EXPECTED RESULTS:
    ──────────────────
    - Success: true
    - Features: 34 (one buffer per school)
    - Geometry Type: Polygon (NOT Point!)
    - Files Created: 5 companion files
    - File Size: ~42KB total (much larger due to polygon complexity)
    """
    print_header("TEST 5: Export Buffer Operation")
    try:
        r = requests.post(f"{API}/api/export",
                         json={
                             "query": "Buffer Schools by 500 meters",
                             "filename": "schools_buffer_test",
                             "output_dir": TEST_OUTPUT_DIR
                         },
                         timeout=30)
        
        result = r.json()
        # Verify: successful, 34 features, Polygon geometry
        passed = (r.status_code == 200 and 
                 result.get("success") and 
                 result.get("features_count") == 34 and
                 result.get("geometry_type") == "Polygon")
        
        msg = f"Features: {result.get('features_count')}, Geometry: {result.get('geometry_type')}"
        print_test("Export Buffer", passed, msg)
        
        if result.get("files"):
            print(f"       Files created: {len(result['files'])}")
            for f in result['files'][:3]:
                print(f"       • {os.path.basename(f)}")
        
        return passed, result
    except Exception as e:
        print_test("Export Buffer", False, f"Error: {str(e)}")
        return False, {}

def test_file_verification():
    """Test 6: Verify Exported Shapefiles
    
    PURPOSE: Verify all companion files exist after export
    
    SHAPEFILE COMPANION FILES:
    ═════════════════════════
    A valid shapefile MUST have all these files in same directory:
    
    1. .shp (Main Shapefile)
       - Binary file containing geometry data
       - Stores coordinates for all features (points, polygons, etc)
       - Size depends on feature count and complexity
       - REQUIRED: Yes
    
    2. .shx (Shape Index)
       - Binary index file for fast random access
       - Allows GIS software to quickly jump to specific feature
       - REQUIRED: Yes (most systems enforce this)
    
    3. .dbf (Attribute Database)
       - DBase format database file
       - Stores all feature attributes (name, value, type, etc)
       - Stores one row per feature
       - Can contain multiple columns with different data types
       - REQUIRED: Yes
    
    4. .prj (Projection File)
       - Text file with coordinate reference system (CRS) definition
       - Example content: PROJCS["UTM_Zone_43N",...] (WKT format)
       - Defines how coordinates map to real-world locations
       - REQUIRED: Yes (for spatial operations to work correctly)
    
    5. .cpg (Code Page File)
       - Optional but recommended
       - Specifies character encoding (UTF-8, Latin-1, etc)
       - Ensures special characters display correctly
       - REQUIRED: No, but good to have
    
    VERIFICATION PROCESS:
    ─────────────────────
    For each exported shapefile:
    1. Check for schools_clipped_test.shp ✓
    2. Check for schools_clipped_test.shx ✓
    3. Check for schools_clipped_test.dbf ✓
    4. Check for schools_clipped_test.prj ✓
    
    Same for buffer test.
    
    EXPECTED RESULT:
    ────────────────
    All required files (shp, shx, dbf, prj) present for both exports
    """
    print_header("TEST 6: Verify Exported Shapefiles")
    all_passed = True
    
    exports = [
        ("schools_clipped_test", "Clip"),
        ("schools_buffer_test", "Buffer"),
    ]
    
    required_exts = [".shp", ".shx", ".dbf", ".prj"]
    
    for export_name, export_type in exports:
        base_path = os.path.join(TEST_OUTPUT_DIR, export_name, export_name)
        
        missing = []
        for ext in required_exts:
            if not os.path.exists(f"{base_path}{ext}"):
                missing.append(ext)
        
        passed = len(missing) == 0
        msg = f"All files present" if passed else f"Missing: {', '.join(missing)}"
        print_test(f"Verify {export_type} Files", passed, msg)
        all_passed = all_passed and passed
    
    return all_passed

def test_analyze_query():
    """Test 7: Analyze Query"""
    print_header("TEST 7: Analyze Query")
    try:
        r = requests.post(f"{API}/api/analyze",
                         json={"query": "Count features in Schools"},
                         timeout=30)
        
        result = r.json()
        passed = r.status_code == 200 and result.get("success")
        msg = f"Steps: {len(result.get('steps', []))}"
        print_test("Analyze Query", passed, msg)
        
        if result.get("steps"):
            for step in result['steps']:
                print(f"       • Step {step.get('step_id')}: {step.get('tool_name')}")
        
        return passed
    except Exception as e:
        print_test("Analyze Query", False, f"Error: {str(e)}")
        return False

def test_list_tools():
    """Test 8: List Available Tools"""
    print_header("TEST 8: List Available Tools")
    try:
        r = requests.get(f"{API}/api/tools", timeout=10)
        data = r.json()
        passed = r.status_code == 200 and len(data) > 0
        print_test("List Tools", passed, f"Tools available: {len(data)}")
        
        if passed and len(data) > 0:
            print(f"       Sample tools:")
            for tool in data[:3]:
                print(f"       • {tool['name']}: {tool['description'][:50]}...")
        
        return passed
    except Exception as e:
        print_test("List Tools", False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print_header("GeoSI API - Comprehensive Test Suite")
    print(f"API Endpoint: {API}\n")
    
    results = {
        "Health Check": test_health_check(),
        "Load Data": test_load_data(),
        "List Layers": test_list_layers(),
        "Analyze Query": test_analyze_query(),
        "List Tools": test_list_tools(),
    }
    
    # Export tests
    clip_passed, clip_result = test_export_clip()
    results["Export Clip"] = clip_passed
    
    buffer_passed, buffer_result = test_export_buffer()
    results["Export Buffer"] = buffer_passed
    
    # File verification
    results["File Verification"] = test_file_verification()
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Tests Passed: {GREEN}{passed}/{total}{NC}\n")
    
    for test_name, test_passed in results.items():
        status = f"{GREEN}✅{NC}" if test_passed else f"{RED}❌{NC}"
        print(f"{status} {test_name}")
    
    # Show exported files
    if os.path.exists(TEST_OUTPUT_DIR):
        print(f"\n{YELLOW}📁 Test Output Directory:{NC} {TEST_OUTPUT_DIR}")
        print(f"   Size: {get_dir_size(TEST_OUTPUT_DIR)}")
        
        print(f"\n{YELLOW}📄 Exported Files:{NC}")
        for root, dirs, files in os.walk(TEST_OUTPUT_DIR):
            for f in files:
                filepath = os.path.join(root, f)
                size = os.path.getsize(filepath)
                size_kb = size / 1024
                print(f"   • {os.path.relpath(filepath, TEST_OUTPUT_DIR):<40} ({size_kb:.1f}KB)")
    
    # Final result
    print(f"\n{BLUE}{'='*70}{NC}")
    if passed == total:
        print(f"{GREEN}✅ ALL TESTS PASSED{NC}".center(70))
    else:
        print(f"{RED}❌ SOME TESTS FAILED{NC}".center(70))
    print(f"{BLUE}{'='*70}{NC}\n")
    
    return passed == total

def get_dir_size(path):
    """Get total directory size"""
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total += os.path.getsize(filepath)
    
    if total < 1024:
        return f"{total}B"
    elif total < 1024*1024:
        return f"{total/1024:.1f}KB"
    else:
        return f"{total/(1024*1024):.1f}MB"

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
