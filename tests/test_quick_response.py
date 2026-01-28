#!/usr/bin/env python3
"""
Test rápido de respuesta del backend
"""

import requests
import json
import time

def test_quick_response():
    """Test simple de respuesta"""
    
    print("🔍 Test de respuesta rápida")
    print("="*60)
    
    # Región pequeña
    test_data = {
        "lat_min": 16.0,
        "lat_max": 16.05,
        "lon_min": -90.0,
        "lon_max": -89.95,
        "region_name": "Test Rápido"
    }
    
    print(f"📍 Región: {test_data['region_name']}")
    print(f"   Coordenadas: [{test_data['lat_min']}, {test_data['lat_max']}] x [{test_data['lon_min']}, {test_data['lon_max']}]")
    print()
    
    try:
        start = time.time()
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=60  # 60 segundos de timeout
        )
        elapsed = time.time() - start
        
        print(f"✅ Status: {response.status_code}")
        print(f"⏱️  Tiempo: {elapsed:.2f} segundos")
        
        if response.status_code == 200:
            result = response.json()
            print()
            print("📊 Resultado:")
            print(f"   Ambiente: {result.get('spatial_context', {}).get('environment_type', 'N/A')}")
            print(f"   Anomalía: {result.get('archaeological_results', {}).get('result_type', 'N/A')}")
            print(f"   Probabilidad: {result.get('archaeological_results', {}).get('archaeological_probability', 0):.2%}")
            print(f"   Mediciones: {result.get('archaeological_results', {}).get('measurements_count', 0)}")
            
            # Verificar que no hay errores críticos
            if 'error' in result:
                print(f"   ⚠️ Error: {result['error']}")
                return False
            
            print()
            print("✅ SISTEMA FUNCIONANDO CORRECTAMENTE")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text[:200]}")
            return False
            
    except requests.Timeout:
        print(f"❌ Timeout después de 60 segundos")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_quick_response()
    exit(0 if success else 1)
