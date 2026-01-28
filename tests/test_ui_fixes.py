#!/usr/bin/env python3
"""
Test script to verify UI fixes are working
"""

import requests
import json
import time

def test_backend_connection():
    """Test if backend is responding"""
    try:
        response = requests.get('http://localhost:8004/status/detailed', timeout=5)
        if response.status_code == 200:
            print("✅ Backend connection successful")
            data = response.json()
            print(f"   - Backend status: {data.get('backend_status', 'unknown')}")
            print(f"   - AI status: {data.get('ai_status', 'unknown')}")
            print(f"   - Volumetric engine: {data.get('volumetric_engine', 'unknown')}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_analysis_endpoint():
    """Test analysis endpoint with simple data"""
    try:
        test_data = {
            "lat_min": 41.85,
            "lat_max": 41.86,
            "lon_min": 12.50,
            "lon_max": 12.51,
            "resolution_m": 500,
            "region_name": "Test Region",
            "include_explainability": True,
            "include_validation_metrics": True,
            "layers_to_analyze": ["ndvi_vegetation", "thermal_lst"],
            "active_rules": ["all"]
        }
        
        print("🔍 Testing analysis endpoint...")
        response = requests.post('http://localhost:8004/analyze', 
                               json=test_data, 
                               timeout=30)
        
        if response.status_code == 200:
            print("✅ Analysis endpoint working")
            data = response.json()
            
            # Check for undefined values in response
            response_str = json.dumps(data)
            if 'undefined' in response_str.lower():
                print("⚠️ Found 'undefined' values in API response")
                return False
            else:
                print("✅ No 'undefined' values found in API response")
                
            # Check key fields exist
            required_fields = ['region_info', 'anomaly_map', 'scientific_report']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"⚠️ Missing required fields: {missing_fields}")
                return False
            else:
                print("✅ All required fields present in response")
                return True
        else:
            print(f"❌ Analysis endpoint returned status {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def main():
    print("🧪 TESTING ARCHEOSCOPE UI FIXES")
    print("=" * 50)
    
    # Test 1: Backend connection
    print("\n1. Testing backend connection...")
    backend_ok = test_backend_connection()
    
    if not backend_ok:
        print("❌ Backend not available, skipping analysis test")
        return
    
    # Test 2: Analysis endpoint
    print("\n2. Testing analysis endpoint...")
    analysis_ok = test_analysis_endpoint()
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"✅ Backend connection: {'PASS' if backend_ok else 'FAIL'}")
    print(f"✅ Analysis endpoint: {'PASS' if analysis_ok else 'FAIL'}")
    
    if backend_ok and analysis_ok:
        print("\n🎉 All tests passed! UI fixes should be working.")
        print("   - Frontend available at: http://localhost:8080")
        print("   - Backend API at: http://localhost:8004")
        print("   - Try the frontend in your browser to test the UI fixes")
    else:
        print("\n⚠️ Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()