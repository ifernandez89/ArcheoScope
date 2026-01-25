#!/usr/bin/env python3
"""
Test simple POST endpoint
"""

import requests
import json

# Test 1: POST to /academic/explainability/analyze (which also takes RegionRequest)
print("Testing /academic/explainability/analyze endpoint...")

data = {
    "lat_min": 41.85,
    "lat_max": 41.86,
    "lon_min": 12.51,
    "lon_max": 12.52,
    "region_name": "Test Region"
}

try:
    response = requests.post(
        'http://localhost:8002/academic/explainability/analyze',
        json=data,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Endpoint works!")
        print(f"Response keys: {list(response.json().keys())}")
    else:
        print(f"❌ Error: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
