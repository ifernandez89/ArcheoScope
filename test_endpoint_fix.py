#!/usr/bin/env python3
"""Probar que el endpoint POST /api/scientific/analyze funciona."""

import requests
import json

API_BASE = "http://localhost:8002"

def test_analyze_endpoint():
    """Probar POST /api/scientific/analyze"""
    print("\n🧪 TEST: POST /api/scientific/analyze")
    print("="*60)
    
    test_data = {
        "lat_min": 64.19,
        "lat_max": 64.21,
        "lon_min": -51.71,
        "lon_max": -51.69,
        "region_name": "Test Endpoint Fix"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/api/scientific/analyze",
            json=test_data,
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Endpoint funcionando correctamente")
            print(f"\nRegión: {result['request_info']['region_name']}")
            print(f"Ambiente: {result['environment_context']['environment_type']}")
            print(f"Probabilidad: {result['scientific_output']['anthropic_probability']:.3f}")
            print(f"Anomaly Score: {result['scientific_output']['anomaly_score']:.3f}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_analyze_endpoint()
