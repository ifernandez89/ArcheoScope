#!/usr/bin/env python3
"""
Quick test without unicode characters for Windows compatibility
"""

import requests
import json

def test_simple():
    """Test basic backend functionality."""
    
    print("Testing: Backend connectivity")
    
    try:
        # Test status endpoint
        response = requests.get("http://localhost:8002/status", timeout=10)
        if response.status_code == 200:
            print("Status: OK")
        else:
            print(f"Status failed: {response.status_code}")
            return False
            
        # Test simple analysis
        test_data = {
            "lat_min": -16.55,
            "lat_max": -16.54,
            "lon_min": -68.67,
            "lon_max": -68.66,
            "region_name": "Test Region"
        }
        
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Analysis: Success")
            print(f"Result type: {result.get('archaeological_results', {}).get('result_type', 'Unknown')}")
            return True
        else:
            print(f"Analysis failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_simple()
    print(f"Result: {'OK' if success else 'ERROR'}")