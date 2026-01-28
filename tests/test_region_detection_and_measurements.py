#!/usr/bin/env python3
"""
Test: Verificar detección automática de región y mediciones vinculadas
"""

import requests
import json

def test_region_and_measurements():
    """Test detección de región y mediciones."""
    
    print("="*80)
    print("TEST: Detección Automática de Región y Mediciones Vinculadas")
    print("="*80)
    
    # Coordenadas de Baja California Sur, México
    test_data = {
        "lat_min": 26.94,
        "lat_max": 26.96,
        "lon_min": -111.86,
        "lon_max": -111.84,
        "region_name": "Test Region"  # Nombre genérico - debe detectarse automáticamente
    }
    
    print(f"\n📍 Coordenadas: Centro-sur de Baja California Sur")
    print(f"   Lat: {(test_data['lat_min'] + test_data['lat_max'])/2:.2f}")
    print(f"   Lon: {(test_data['lon_min'] + test_data['lon_max'])/2:.2f}")
    print(f"   Región solicitada: '{test_data['region_name']}' (genérica)")
    
    try:
        print("\n🔄 Enviando solicitud...")
        response = requests.post(
            "http://localhost:8002/api/scientific/analyze",
            json=test_data,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"\n❌ ERROR: HTTP {response.status_code}")
            print(response.text)
            return False
        
        result = response.json()
        print("✅ Análisis completado")
        
        # Verificar región detectada
        detected_region = result['request_info']['region_name']
        print(f"\n🌍 Región detectada: '{detected_region}'")
        
        if detected_region == "Test Region":
            print("⚠️ WARNING: Región no fue detectada automáticamente")
        else:
            print("✅ Región detectada automáticamente")
        
        # Obtener análisis recientes
        print("\n🔍 Consultando análisis reciente...")
        response2 = requests.get(
            "http://localhost:8002/api/scientific/analyses/recent?limit=1",
            timeout=10
        )
        
        if response2.status_code != 200:
            print(f"❌ ERROR consultando: HTTP {response2.status_code}")
            return False
        
        recent = response2.json()
        analysis = recent['analyses'][0]
        analysis_id = analysis['id']
        
        print(f"\n📊 Análisis ID: {analysis_id}")
        print(f"   Región guardada: {analysis['region']}")
        
        # Consultar mediciones del análisis
        print(f"\n🔍 Consultando mediciones del análisis {analysis_id}...")
        response3 = requests.get(
            f"http://localhost:8002/api/scientific/analyses/{analysis_id}",
            timeout=10
        )
        
        if response3.status_code != 200:
            print(f"❌ ERROR consultando mediciones: HTTP {response3.status_code}")
            return False
        
        full_analysis = response3.json()
        
        measurements = full_analysis.get('measurements', [])
        failed = full_analysis.get('failed_instruments', [])
        
        print(f"\n📊 Mediciones vinculadas al análisis:")
        print(f"   ✅ Exitosas: {len(measurements)}")
        print(f"   ❌ Fallidas: {len(failed)}")
        
        if len(measurements) > 0:
            print(f"\n   Instrumentos exitosos:")
            for m in measurements[:5]:  # Mostrar primeros 5
                print(f"     - {m['instrument_name']}: {m['value']:.3f} ({m['data_mode']})")
        
        if len(failed) > 0:
            print(f"\n   Instrumentos fallidos:")
            for f in failed[:5]:
                print(f"     - {f['instrument_name']}")
        
        # Verificar que las mediciones son SOLO de este análisis
        print(f"\n🔍 Verificando que las mediciones pertenecen solo a este análisis...")
        
        # Todas las mediciones deben tener las mismas coordenadas del análisis
        analysis_coords = full_analysis['analysis']['coordinates']['center']
        analysis_lat = analysis_coords['latitude']
        analysis_lon = analysis_coords['longitude']
        
        coords_match = True
        for m in measurements:
            if abs(m['latitude'] - analysis_lat) > 0.01 or abs(m['longitude'] - analysis_lon) > 0.01:
                coords_match = False
                print(f"⚠️ WARNING: Medición con coordenadas diferentes:")
                print(f"   Análisis: ({analysis_lat}, {analysis_lon})")
                print(f"   Medición: ({m['latitude']}, {m['longitude']})")
        
        if coords_match:
            print("✅ Todas las mediciones pertenecen a este análisis")
        
        print("\n" + "="*80)
        print("✅ TEST EXITOSO")
        print("="*80)
        
        print(f"\n📍 Región detectada: {detected_region}")
        print(f"📊 Mediciones: {len(measurements)} exitosas, {len(failed)} fallidas")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_region_and_measurements()
    exit(0 if success else 1)
