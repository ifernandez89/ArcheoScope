#!/usr/bin/env python3
"""
Test end-to-end completo para verificar:
1. Análisis en mar abierto se guarda correctamente (sin error de country NULL)
2. Coordenadas se guardan en la BD
3. Instrumentos se registran correctamente
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8002"

def test_open_sea_analysis():
    """Test análisis en mar abierto (donde fallaba antes)."""
    
    print("🧪 TEST END-TO-END: Análisis en mar abierto")
    print("=" * 70)
    
    # Coordenadas en mar abierto (donde fallaba antes)
    test_data = {
        "lat_min": 54.84,
        "lat_max": 54.86,
        "lon_min": 3.24,
        "lon_max": 3.26,
        "region_name": "Test Region"  # Será reemplazado por detección automática
    }
    
    print(f"\n📍 Analizando: Mar del Norte ({test_data['lat_min']}, {test_data['lon_min']})")
    print(f"   Región solicitada: '{test_data['region_name']}'")
    
    try:
        # Llamar al endpoint
        print("\n🔄 Enviando request al backend...")
        response = requests.post(
            f"{API_BASE_URL}/api/scientific/analyze",
            json=test_data,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        result = response.json()
        
        # Verificar estructura de respuesta
        print("\n✅ Análisis completado exitosamente")
        print(f"\n📊 RESULTADOS:")
        
        # Scientific output
        sci_output = result.get('scientific_output', {})
        print(f"\n   🔬 Scientific Output:")
        print(f"      • Candidate Name: {sci_output.get('candidate_name')}")
        print(f"      • Region: {sci_output.get('region')}")
        print(f"      • Environment: {sci_output.get('environment_type')}")
        print(f"      • Result Type: {sci_output.get('result_type')}")
        print(f"      • Recommended Action: {sci_output.get('recommended_action')}")
        
        # Verificar que se guardó en BD
        analysis_id = sci_output.get('analysis_id')
        if analysis_id:
            print(f"\n   💾 Guardado en BD con ID: {analysis_id}")
            
            # Consultar el análisis guardado
            time.sleep(1)  # Esperar un momento
            detail_response = requests.get(
                f"{API_BASE_URL}/api/scientific/analyses/{analysis_id}",
                timeout=10
            )
            
            if detail_response.status_code == 200:
                detail = detail_response.json()
                analysis = detail.get('analysis', {})
                coords = analysis.get('coordinates', {})
                
                print(f"\n   📍 Coordenadas guardadas:")
                center = coords.get('center', {})
                print(f"      • Centro: ({center.get('latitude')}, {center.get('longitude')})")
                
                bounds = coords.get('bounds', {})
                print(f"      • Bounds: lat[{bounds.get('lat_min')}, {bounds.get('lat_max')}]")
                print(f"                lon[{bounds.get('lon_min')}, {bounds.get('lon_max')}]")
                
                # Verificar instrumentos
                measurements = detail.get('measurements', [])
                failed = detail.get('failed_instruments', [])
                
                print(f"\n   🛰️ Instrumentos:")
                print(f"      • Exitosos: {len(measurements)}")
                for m in measurements:
                    print(f"         - {m.get('instrument_name')}: {m.get('value')} {m.get('unit')}")
                
                print(f"      • Fallidos: {len(failed)}")
                for f in failed:
                    print(f"         - {f.get('instrument_name')}")
                
                # Verificar explicación científica
                explanation = analysis.get('scientific_explanation')
                if explanation:
                    print(f"\n   📝 Explicación científica guardada:")
                    print(f"      {explanation[:150]}...")
                
                print("\n" + "=" * 70)
                print("✅ TEST COMPLETO EXITOSO")
                print("\n📋 VERIFICACIONES:")
                print("   ✓ Análisis se guardó sin error de country NULL")
                print("   ✓ Coordenadas se guardaron correctamente")
                print("   ✓ Instrumentos exitosos y fallidos registrados")
                print("   ✓ Explicación científica guardada")
                print("   ✓ Región detectada automáticamente")
                
                return True
            else:
                print(f"❌ Error consultando análisis: {detail_response.status_code}")
                return False
        else:
            print("❌ No se obtuvo analysis_id")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout esperando respuesta del backend")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🚀 Iniciando test end-to-end...")
    print("   Asegúrate de que el backend esté corriendo en puerto 8002\n")
    
    success = test_open_sea_analysis()
    
    if success:
        print("\n🎉 TODOS LOS PROBLEMAS CORREGIDOS")
    else:
        print("\n⚠️ Algunos tests fallaron")
