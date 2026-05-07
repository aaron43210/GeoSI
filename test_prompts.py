#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script: 30 prompts with Kerala/Schools/Assets dataset
Tests parameter extraction, intent classification, and rule-based planning
"""

import sys
import os

# Add plugin to path
sys.path.insert(0, os.path.dirname(__file__))

from geosi_engine import GeoSI
from geosi_engine.models import Layer

def test_geosi_with_prompts():
    """Test GeoSI engine with 30 different prompts."""
    
    # Initialize engine
    engine = GeoSI()
    print(f"✅ Engine initialized: {engine.version}")
    print(f"📦 {len(engine.registry.list_tools())} tools loaded\n")
    
    # Register test layers
    test_layers = [
        ("schools", "Point", 150, "EPSG:4326"),
        ("assets", "Point", 450, "EPSG:4326"),
        ("kerala", "Polygon", 1, "EPSG:4326"),
    ]
    
    for name, geom_type, count, crs in test_layers:
        layer = Layer(
            name=name,
            geometry_type=geom_type,
            feature_count=count,
            crs=crs,
            filepath=f"/path/to/{name}.shp",
            layer_type="vector"
        )
        engine.state.add_layer(layer)
    
    available_layers = engine.state.list_layers()
    print(f"📁 Available layers: {', '.join(available_layers)}\n")
    
    # 30 test prompts covering various intents and parameter extraction
    test_prompts = [
        # Proximity/Buffer tests (5)
        "Create 500 meter buffers around all schools for walkable access",
        "Buffer schools by 1 km",
        "Buffer assets with 200 meter radius",
        "Create a 500m buffer zone around schools",
        "Buffer the schools layer by 750 meters",
        
        # Overlay/Intersect tests (5)
        "Find schools that overlap with assets",
        "Intersect schools and assets layers",
        "Which schools are inside the kerala boundary",
        "Clip schools to the kerala administrative area",
        "Overlay schools with assets and find intersections",
        
        # Geometry tests (5)
        "Calculate the centroid of each school",
        "Simplify the geometry of kerala layer",
        "Create convex hull around all schools",
        "Dissolve adjacent school features",
        "Create a bounding box for schools",
        
        # Statistics tests (5)
        "Count the number of schools",
        "How many assets are there in total",
        "Summary statistics for schools",
        "Count features in the kerala layer",
        "How many schools and assets do we have",
        
        # Spatial analysis tests (5)
        "Cluster the schools by location",
        "Find the closest asset to each school",
        "Calculate distance between schools and assets",
        "Identify asset hotspots in kerala",
        "Find schools within 2km of assets",
        
        # Complex/Multi-step tests (5)
        "Buffer schools by 500m then find which assets fall within these buffers",
        "Create 1km buffers around schools and clip to kerala boundary",
        "Cluster schools and calculate statistics for each cluster",
        "Find assets within 500m of schools and count them by location",
        "Buffer assets by 250m and intersect with schools",
    ]
    
    results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    print("=" * 80)
    print("TESTING 30 PROMPTS")
    print("=" * 80 + "\n")
    
    for idx, prompt in enumerate(test_prompts, 1):
        print(f"[{idx:2d}] {prompt}")
        try:
            # Parse query
            request = engine.agent.parse(prompt, engine.state)
            print(f"    ✅ Intent: {request.intent.name}")
            print(f"    📋 Entities: {request.entities}")
            print(f"    🔢 Parameters: {request.parameters}")
            
            # Plan execution
            plan = engine.agent.plan(request, engine.state)
            
            if plan.steps:
                print(f"    📍 Plan steps: {len(plan.steps)}")
                for step in plan.steps:
                    print(f"       - {step.tool_name}: {step.parameters}")
                results["passed"] += 1
                print("    ✅ PASS\n")
            else:
                print(f"    ⚠️  No steps generated")
                results["failed"] += 1
                print("    ❌ FAIL\n")
                
        except Exception as e:
            print(f"    ❌ ERROR: {str(e)[:100]}")
            results["failed"] += 1
            results["errors"].append((idx, prompt, str(e)))
            print()
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Passed: {results['passed']}/30")
    print(f"❌ Failed: {results['failed']}/30")
    print(f"Success rate: {(results['passed']/30)*100:.1f}%\n")
    
    if results["errors"]:
        print("FAILED PROMPTS:")
        for idx, prompt, error in results["errors"]:
            print(f"  [{idx}] {prompt[:60]}...")
            print(f"       Error: {error[:80]}...\n")
    
    return results["passed"] >= 25  # Pass if 25+/30 succeed

if __name__ == "__main__":
    success = test_geosi_with_prompts()
    sys.exit(0 if success else 1)
