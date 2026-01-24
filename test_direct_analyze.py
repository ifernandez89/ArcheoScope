#!/usr/bin/env python3
"""
Direct test of analyze endpoint with detailed error output
"""

import requests
import json
import traceback

url = 'http://localhost:8002/analyze'

data = {
    "lat_min": 41.85,
    "lat_max": 41.86,
    "lon_min": 12.51,
    "lon_max": 12.52,
    "region_name": "Test Region"
}

print("Sending request to:", url)
print("Data:", json.dumps(data, indent=2))

try:
    response = requests.post(url, json=data, timeout=60)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nResponse Content:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
        
except Exception as e:
    print(f"\nException occurred:")
    print(traceback.format_exc())
