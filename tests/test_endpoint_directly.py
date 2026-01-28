#!/usr/bin/env python3
"""
Test endpoint directly without HTTP to see actual error
"""

import sys
sys.path.insert(0, 'backend')

from api.main import app, RegionRequest
from fastapi.testclient import TestClient

client = TestClient(app)

print("Testing /analyze endpoint directly...")

data = {
    "lat_min": 41.85,
    "lat_max": 41.86,
    "lon_min": 12.51,
    "lon_max": 12.52,
    "region_name": "Test Region"
}

try:
    response = client.post("/analyze", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Success!")
        print(f"Response keys: {list(response.json().keys())}")
    else:
        print(f"❌ Error:")
        print(response.text)
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
