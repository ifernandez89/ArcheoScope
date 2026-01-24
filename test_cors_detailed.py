#!/usr/bin/env python3
"""
Detailed CORS test to see actual error
"""

import requests
import json

headers = {
    'Origin': 'http://localhost:8080',
    'Content-Type': 'application/json'
}

data = {
    "lat_min": 41.85,
    "lat_max": 41.86,
    "lon_min": 12.51,
    "lon_max": 12.52,
    "region_name": "Test CORS"
}

try:
    response = requests.post(
        'http://localhost:8002/analyze',
        headers=headers,
        json=data,
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text[:500]}")
    
except Exception as e:
    print(f"Error: {e}")
