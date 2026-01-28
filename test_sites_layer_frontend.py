#!/usr/bin/env python3
"""
Test Sites Layer Frontend Integration
Verifica que los endpoints de la capa de sitios funcionen correctamente
"""

import requests
import json

API_BASE_URL = "http://localhost:8002"

def test_sites_layer_endpoint():
    """Test GET /api/scientific/sites/layer"""
    print("🔍 Testing sites layer endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/scientific/sites/layer?limit=10")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sites layer endpoint OK")
            print(f"   Total sites: {data['metadata']['total']}")
            print(f"   Features: {len(data['features'])}")
            
            if data['features']:
                first = data['features'][0]
                print(f"   First site: {first['properties']['name']}")
                print(f"   Coordinates: {first['geometry']['coordinates']}")
            
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_candidates_endpoint():
    """Test GET /api/scientific/sites/candidates"""
    print("\n🔍 Testing candidates endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/scientific/sites/candidates?limit=10")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Candidates endpoint OK")
            print(f"   Total candidates: {data['total']}")
            
            if data['candidates']:
                first = data['candidates'][0]
                print(f"   First candidate: {first['name']}")
                print(f"   Metrics: Origin {first['metrics']['origin']:.0%}, "
                      f"Activity {first['metrics']['activity']:.0%}, "
                      f"Anomaly {first['metrics']['anomaly']:.0%}")
                print(f"   ESS: {first['metrics']['ess'].upper()}")
            
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_sites_stats():
    """Test GET /api/scientific/sites/stats"""
    print("\n🔍 Testing sites stats endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/scientific/sites/stats")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sites stats endpoint OK")
            print(f"   Total sites: {data['total_sites']}")
            print(f"   Control sites: {data['control_sites']}")
            print(f"   Recent additions: {data['recent_additions']}")
            
            if data['by_country']:
                top_country = data['by_country'][0]
                print(f"   Top country: {top_country['country']} ({top_country['count']} sites)")
            
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def test_backend_status():
    """Test backend is running"""
    print("🔍 Testing backend status...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"❌ Backend returned: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running on port 8002")
        print("   Run: python run_archeoscope.py")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🏺 ArcheoScope - Sites Layer Frontend Integration Test")
    print("=" * 60)
    
    # Test backend
    if not test_backend_status():
        print("\n⚠️ Backend must be running to test endpoints")
        print("   Start backend: python run_archeoscope.py")
        exit(1)
    
    # Test endpoints
    results = []
    results.append(test_sites_layer_endpoint())
    results.append(test_candidates_endpoint())
    results.append(test_sites_stats())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
        print("\n🎉 Frontend integration ready!")
        print("   Open: frontend/index.html")
        print("   Click: 📍 Mostrar Sitios Conocidos")
    else:
        print("❌ Some tests failed")
        print("   Check backend logs for errors")
    
    print("=" * 60)
