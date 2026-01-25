#!/usr/bin/env python3
"""
Test specific coordinates: 32.300, -64.783
"""

import requests
import json

def test_coordinates():
    """Test analysis for specific coordinates."""
    
    print("Testing coordinates: 32.300, -64.783")
    
    # Create small region around the point
    test_data = {
        "lat_min": 32.295,
        "lat_max": 32.305,
        "lon_min": -64.788,
        "lon_max": -64.778,
        "region_name": "Bermuda Test"
    }
    
    try:
        print("Sending analysis request...")
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract key results
            arch_result = result.get('archaeological_results', {})
            spatial_context = result.get('spatial_context', {})
            ai_explanations = result.get('ai_explanations', {})
            
            print(f"Analysis successful!")
            print(f"Result type: {arch_result.get('result_type', 'Unknown')}")
            print(f"Confidence: {arch_result.get('confidence', 0):.2f}")
            print(f"Archaeological probability: {arch_result.get('archaeological_probability', 0):.2f}")
            print(f"Affected pixels: {arch_result.get('affected_pixels', 0)}")
            print(f"Area: {spatial_context.get('area_km2', 0):.2f} km²")
            
            if ai_explanations.get('ai_available', False):
                print(f"AI explanation: {ai_explanations.get('explanation', 'No explanation')[:200]}...")
            else:
                print("AI explanation: Not available")
            
            return True
        else:
            print(f"Analysis failed: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_coordinates()
    print(f"\nFinal result: {'SUCCESS' if success else 'FAILED'}")