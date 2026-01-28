#!/usr/bin/env python3
"""
Test environment classifier integration
"""

import requests
import json

# Test Giza (should be DESERT)
print("=" * 60)
print("TEST 1: GIZA PYRAMIDS (should be DESERT)")
print("=" * 60)

data = {
    "lat_min": 29.965,
    "lat_max": 29.985,
    "lon_min": 31.128,
    "lon_max": 31.148,
    "region_name": "Giza Pyramids"
}

try:
    response = requests.post(
        'http://localhost:8002/analyze',
        json=data,
        timeout=60
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        region_info = result.get('region_info', {})
        env = region_info.get('environment', {})
        
        print(f"\n✅ SUCCESS")
        print(f"Environment type: {env.get('type', 'N/A')}")
        print(f"Confidence: {env.get('confidence', 'N/A')}")
        print(f"Analysis type: {region_info.get('analysis_type', 'N/A')}")
        
        # Save result
        with open('giza_environment_test.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("\n💾 Result saved to: giza_environment_test.json")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST 2: ANTARCTICA (should be POLAR_ICE)")
print("=" * 60)

data2 = {
    "lat_min": -75.5,
    "lat_max": -75.0,
    "lon_min": 0.0,
    "lon_max": 0.5,
    "region_name": "Antarctica Test"
}

try:
    response = requests.post(
        'http://localhost:8002/analyze',
        json=data2,
        timeout=60
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        region_info = result.get('region_info', {})
        env = region_info.get('environment', {})
        
        print(f"\n✅ SUCCESS")
        print(f"Environment type: {env.get('type', 'N/A')}")
        print(f"Confidence: {env.get('confidence', 'N/A')}")
        print(f"Analysis type: {region_info.get('analysis_type', 'N/A')}")
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")
