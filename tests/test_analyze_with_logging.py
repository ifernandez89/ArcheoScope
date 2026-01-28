#!/usr/bin/env python3
"""
Test /analyze endpoint with detailed logging
"""

import requests
import json
import logging

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

data = {
    "lat_min": 41.85,
    "lat_max": 41.86,
    "lon_min": 12.51,
    "lon_max": 12.52,
    "region_name": "Test Region"
}

print("Sending request to /analyze...")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    response = requests.post(
        'http://localhost:8002/analyze',
        json=data,
        timeout=60
    )
    
    print(f"\nStatus: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print("✅ Success!")
        result = response.json()
        print(f"Response keys: {list(result.keys())}")
    else:
        print(f"❌ Error response:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
