#!/usr/bin/env python3
"""
Test CORS configuration for ArcheoScope
"""

import requests
import json

def test_cors_preflight():
    """Test CORS preflight request"""
    print("🔍 Testing CORS preflight (OPTIONS)...")
    
    headers = {
        'Origin': 'http://localhost:8080',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type'
    }
    
    try:
        response = requests.options(
            'http://localhost:8002/analyze',
            headers=headers,
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if 'Access-Control-Allow-Origin' in response.headers:
            print("✅ CORS headers present")
            return True
        else:
            print("❌ CORS headers missing")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cors_actual_request():
    """Test actual POST request with CORS"""
    print("\n🔍 Testing actual POST request with CORS...")
    
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
        print(f"CORS Header: {response.headers.get('Access-Control-Allow-Origin', 'NOT PRESENT')}")
        
        if response.status_code == 200:
            print("✅ Request successful")
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_backend_status():
    """Test backend status endpoint"""
    print("\n🔍 Testing backend status...")
    
    try:
        response = requests.get('http://localhost:8002/', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend operational: {data.get('status')}")
            return True
        else:
            print(f"❌ Backend not responding properly: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ARCHEOSCOPE CORS CONFIGURATION TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("Backend Status", test_backend_status()))
    results.append(("CORS Preflight", test_cors_preflight()))
    results.append(("CORS Actual Request", test_cors_actual_request()))
    
    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✅ All CORS tests passed!")
    else:
        print("\n❌ Some CORS tests failed - check configuration")
