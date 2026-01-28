#!/usr/bin/env python3
"""
Test simple endpoints to see which ones work
"""

import requests
import json

endpoints = [
    ('GET', 'http://localhost:8002/', 'Status'),
    ('GET', 'http://localhost:8002/status', 'Status endpoint'),
    ('POST', 'http://localhost:8002/falsification-protocol', 'Falsification protocol'),
    ('POST', 'http://localhost:8002/academic/validation/blind-test', 'Blind test'),
]

for method, url, name in endpoints:
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"Method: {method}")
    print('='*60)
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                print(f"Response: {json.dumps(response.json(), indent=2)[:200]}")
            except:
                print(f"Response: {response.text[:200]}")
        else:
            print(f"Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {e}")
