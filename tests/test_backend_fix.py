#!/usr/bin/env python3
"""
Test script to verify backend is working after API fixes
"""

import requests
import json

def test_backend():
    """Test the backend with a simple analysis request"""
    
    print("🧪 Testing ArcheoScope Backend...")
    
    # Test 1: Status check
    try:
        response = requests.get("http://localhost:8003/status/detailed")
        if response.status_code == 200:
            print("✅ Status endpoint working")
            status = response.json()
            print(f"   Backend: {status['backend_status']}")
            print(f"   AI: {status['ai_status']}")
            print(f"   Volumetric: {status['volumetric_engine']}")
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        return False
    
    # Test 2: Simple analysis request
    try:
        print("\n🔍 Testing analysis endpoint...")
        
        # Simple coordinates (Rome area)
        test_request = {
            "lat_min": 41.87,
            "lat_max": 41.88,
            "lon_min": 12.50,
            "lon_max": 12.51,
            "resolution_m": 1000,
            "layers_to_analyze": [
                "ndvi_vegetation", 
                "thermal_lst", 
                "sar_backscatter"
            ],
            "active_rules": ["all"],
            "region_name": "Test Region Rome",
            "include_explainability": False,
            "include_validation_metrics": False
        }
        
        response = requests.post(
            "http://localhost:8003/analyze",
            json=test_request,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Analysis endpoint working")
            result = response.json()
            print(f"   Region: {result.get('region_info', {}).get('region_name', 'Unknown')}")
            print(f"   Statistical results: {len(result.get('statistical_results', {}))}")
            print(f"   Anomaly map: {'✅' if result.get('anomaly_map') else '❌'}")
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if success:
        print("\n🎉 Backend test PASSED - Ready for frontend testing!")
    else:
        print("\n💥 Backend test FAILED - Check logs for issues")