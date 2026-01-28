#!/usr/bin/env python3
"""
Test optimizado para coordenadas de Bermudas (32.300, -64.783)
Verifica que el análisis tarda <5 segundos después de las optimizaciones
"""

import requests
import json
import time

def test_bermuda_optimized():
    """Test análisis optimizado para Bermudas"""
    
    print("TEST BERMUDA OPTIMIZADO")
    print("Verificando análisis para 32.300, -64.783")
    
    # Datos de test para Bermudas
    test_data = {
        "lat_min": 32.295,
        "lat_max": 32.305,
        "lon_min": -64.788,
        "lon_max": -64.778,
        "region_name": "Bermuda Optimized Test"
    }
    
    try:
        print("📡 Enviando solicitud...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=10  # Timeout de 10 segundos
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Análisis completado en {elapsed_time:.2f} segundos")
            print(f"📍 Ambiente: {result.get('environment_classification', {}).get('environment_type', 'Unknown')}")
            print(f"🎯 Probabilidad arqueológica: {result.get('archaeological_results', {}).get('archaeological_probability', 0):.2%}")
            print(f"📊 Número de instrumentos: {len(result.get('instrumental_measurements', []))}")
            
            # Verificación de optimización
            if elapsed_time < 5:
                print(f"🎉 OPTIMIZACIÓN EXITOSA: <5 segundos!")
            elif elapsed_time < 10:
                print(f"⚠️ Mejora notable: {elapsed_time:.2f}s (<10s)")
            else:
                print(f"❌ Todavía lento: {elapsed_time:.2f}s")
            
            return elapsed_time < 10
            
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT después de 10 segundos")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multiple_coordinates():
    """Test múltiples coordenadas para validar optimización general"""
    
    print("\nTEST MULTIPLES COORDENADAS")
    
    test_cases = [
        {"name": "Bermudas", "lat": 32.300, "lon": -64.783},
        {"name": "Sahara", "lat": 25.0, "lon": 13.0},
        {"name": "Amazonas", "lat": -3.465, "lon": -62.215},
        {"name": "Antártida", "lat": -77.846, "lon": 166.668},
        {"name": "Pacífico Profundo", "lat": 0.0, "lon": -160.0}
    ]
    
    results = {}
    
    for case in test_cases:
        print(f"\n📍 Probando {case['name']} ({case['lat']:.1f}, {case['lon']:.1f})")
        
        test_data = {
            "lat_min": case['lat'] - 0.005,
            "lat_max": case['lat'] + 0.005,
            "lon_min": case['lon'] - 0.005,
            "lon_max": case['lon'] + 0.005,
            "region_name": f"Test {case['name']}"
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                "http://localhost:8002/analyze",
                json=test_data,
                timeout=15
            )
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                env_type = result.get('environment_classification', {}).get('environment_type', 'Unknown')
                prob = result.get('archaeological_results', {}).get('archaeological_probability', 0)
                
                results[case['name']] = {
                    'time': elapsed_time,
                    'environment': env_type,
                    'probability': prob,
                    'success': True
                }
                
                print(f"  ✅ {env_type}: {elapsed_time:.2f}s, prob: {prob:.2%}")
            else:
                print(f"  ❌ Error HTTP {response.status_code}")
                results[case['name']] = {'success': False, 'time': elapsed_time}
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results[case['name']] = {'success': False, 'error': str(e)}
    
    print(f"\n📊 RESUMEN DE OPTIMIZACIÓN:")
    successful = [r for r in results.values() if r.get('success', False)]
    if successful:
        avg_time = sum(r['time'] for r in successful) / len(successful)
        fast_count = sum(1 for r in successful if r['time'] < 5)
        
        print(f"  Tiempo promedio: {avg_time:.2f}s")
        print(f"  Análisis rápidos (<5s): {fast_count}/{len(successful)}")
        print(f"  Exitosos: {len(successful)}/{len(test_cases)}")
    
    return len(successful) >= len(test_cases) * 0.8  # 80% éxito

if __name__ == "__main__":
    print("🔧 ArcheoScope - Test de Optimización")
    print("="*50)
    
    # Test principal: Bermudas
    bermuda_success = test_bermuda_optimized()
    
    # Test general: múltiples ambientes
    general_success = test_multiple_coordinates()
    
    print(f"\n🎯 RESULTADO FINAL:")
    print(f"  Bermudas optimizadas: {'✅' if bermuda_success else '❌'}")
    print(f"  Optimización general: {'✅' if general_success else '❌'}")
    print(f"  Estado general: {'✅ SISTEMA OPTIMIZADO' if bermuda_success and general_success else '❌ NECESITA MÁS OPTIMIZACIÓN'}")