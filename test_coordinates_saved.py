#!/usr/bin/env python3
"""
Test: Verificar que las coordenadas se guarden en analyses
"""

import requests
import json

def test_coordinates():
    """Test que las coordenadas se guarden correctamente."""
    
    print("="*80)
    print("TEST: Coordenadas en Análisis")
    print("="*80)
    
    # Coordenadas de test (Perú - ambiente mountain)
    test_data = {
        "lat_min": -13.16,
        "lat_max": -13.14,
        "lon_min": -72.56,
        "lon_max": -72.54,
        "region_name": "Test Coordinates Peru"
    }
    
    print(f"\n📍 Región: {test_data['region_name']}")
    print(f"   Bounds: [{test_data['lat_min']}, {test_data['lat_max']}] x [{test_data['lon_min']}, {test_data['lon_max']}]")
    
    center_lat = (test_data['lat_min'] + test_data['lat_max']) / 2
    center_lon = (test_data['lon_min'] + test_data['lon_max']) / 2
    print(f"   Centro esperado: ({center_lat:.4f}, {center_lon:.4f})")
    
    try:
        print("\n🔄 Enviando solicitud...")
        response = requests.post(
            "http://localhost:8002/api/scientific/analyze",
            json=test_data,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"\n❌ ERROR: HTTP {response.status_code}")
            return False
        
        result = response.json()
        print("✅ Análisis completado")
        
        # Obtener análisis recientes
        print("\n🔍 Consultando análisis recientes...")
        response2 = requests.get(
            "http://localhost:8002/api/scientific/analyses/recent?limit=1",
            timeout=10
        )
        
        if response2.status_code != 200:
            print(f"❌ ERROR consultando: HTTP {response2.status_code}")
            return False
        
        recent = response2.json()
        
        if recent['total'] == 0:
            print("❌ No se encontraron análisis")
            return False
        
        analysis = recent['analyses'][0]
        
        print("\n" + "="*80)
        print("VERIFICACIÓN DE COORDENADAS")
        print("="*80)
        
        print(f"\n📊 Análisis ID: {analysis['id']}")
        print(f"   Nombre: {analysis['candidate_name']}")
        print(f"   Región: {analysis['region']}")
        
        # Verificar coordenadas
        lat = analysis.get('latitude')
        lon = analysis.get('longitude')
        
        print(f"\n📍 Coordenadas guardadas:")
        print(f"   Latitude: {lat}")
        print(f"   Longitude: {lon}")
        
        if lat is None or lon is None:
            print("\n❌ ERROR: Coordenadas son None")
            return False
        
        # Verificar que estén cerca del centro esperado
        lat_diff = abs(lat - center_lat)
        lon_diff = abs(lon - center_lon)
        
        if lat_diff > 0.01 or lon_diff > 0.01:
            print(f"\n⚠️ WARNING: Coordenadas difieren del centro esperado")
            print(f"   Diferencia lat: {lat_diff:.6f}")
            print(f"   Diferencia lon: {lon_diff:.6f}")
        
        # Consultar análisis completo por ID
        print(f"\n🔍 Consultando análisis completo (ID {analysis['id']})...")
        response3 = requests.get(
            f"http://localhost:8002/api/scientific/analyses/{analysis['id']}",
            timeout=10
        )
        
        if response3.status_code != 200:
            print(f"❌ ERROR consultando por ID: HTTP {response3.status_code}")
            return False
        
        full_analysis = response3.json()
        
        coords = full_analysis['analysis'].get('coordinates', {})
        center = coords.get('center', {})
        bounds = coords.get('bounds', {})
        
        print(f"\n📍 Coordenadas completas:")
        print(f"   Centro:")
        print(f"     - Latitude: {center.get('latitude')}")
        print(f"     - Longitude: {center.get('longitude')}")
        print(f"   Bounding Box:")
        print(f"     - lat_min: {bounds.get('lat_min')}")
        print(f"     - lat_max: {bounds.get('lat_max')}")
        print(f"     - lon_min: {bounds.get('lon_min')}")
        print(f"     - lon_max: {bounds.get('lon_max')}")
        
        # Verificar que el bounding box coincida
        if bounds.get('lat_min') != test_data['lat_min']:
            print(f"\n⚠️ WARNING: lat_min no coincide")
        if bounds.get('lat_max') != test_data['lat_max']:
            print(f"\n⚠️ WARNING: lat_max no coincide")
        if bounds.get('lon_min') != test_data['lon_min']:
            print(f"\n⚠️ WARNING: lon_min no coincide")
        if bounds.get('lon_max') != test_data['lon_max']:
            print(f"\n⚠️ WARNING: lon_max no coincide")
        
        print("\n" + "="*80)
        print("✅ TEST EXITOSO - Coordenadas guardadas correctamente")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_coordinates()
    exit(0 if success else 1)
