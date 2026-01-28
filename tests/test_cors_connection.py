#!/usr/bin/env python3
"""
Test de conexión CORS para ArcheoScope
Verifica que el frontend pueda comunicarse con el backend
"""

import requests
import json

def test_cors_connection():
    """Test conexión desde puerto 8080 al backend 8002"""
    
    print("Test de conexión CORS")
    print("=" * 50)
    
    # Headers que simulan petición desde frontend
    headers = {
        'Origin': 'http://localhost:8080',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Status endpoint
    print("\n1. Test endpoint /status")
    try:
        response = requests.get('http://localhost:8002/status', headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {response.headers.get('Access-Control-Allow-Origin', 'NO')}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 2: Analyze endpoint (simulado)
    print("\n2. Test endpoint /analyze (simulado)")
    test_data = {
        "lat_min": 13.4,
        "lat_max": 13.43,
        "lon_min": 103.86,
        "lon_max": 103.88,
        "region_name": "Angkor_Wat_CORS_Test",
        "resolution_m": 100,
        "layers_to_analyze": ["ndvi_anomaly", "thermal_anomaly"]
    }
    
    try:
        response = requests.post(
            'http://localhost:8002/analyze', 
            headers=headers,
            json=test_data,
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {response.headers.get('Access-Control-Allow-Origin', 'NO')}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Analysis ID: {data.get('analysis_id', 'N/A')}")
            print(f"   Validation: {'real_archaeological_validation' in data}")
            print(f"   Transparency: {'data_source_transparency' in data}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Test completado")
    
    if response.status_code == 200 and response.headers.get('Access-Control-Allow-Origin') == '*':
        print("CORS está funcionando correctamente")
        print("Frontend puede conectar con backend")
        return True
    else:
        print("Aún hay problemas con CORS")
        return False

if __name__ == "__main__":
    test_cors_connection()