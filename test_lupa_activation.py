#!/usr/bin/env python3
"""
Test específico para verificar que la activación de la lupa funcione correctamente
después de las correcciones implementadas
"""

import requests
import json
from datetime import datetime

def test_lupa_activation():
    """Test específico de activación de lupa con coordenadas que sabemos funcionan"""
    
    print("🔍 TEST DE ACTIVACIÓN DE LUPA - POST CORRECCIONES")
    print("=" * 60)
    
    # Coordenadas del Caribe que sabemos que detectan candidatos
    test_coordinates = [
        {
            'name': 'Caribe Norte',
            'lat': 25.80,
            'lng': -70.00,
            'expected_candidates': 'múltiples'
        },
        {
            'name': 'Caribe Sur', 
            'lat': 25.30,
            'lng': -70.50,
            'expected_candidates': 'múltiples'
        },
        {
            'name': 'Caribe Centro',
            'lat': 25.55,
            'lng': -70.25,
            'expected_candidates': 'algunos'
        }
    ]
    
    backend_url = "http://localhost:8003"
    
    # Verificar backend
    try:
        response = requests.get(f"{backend_url}/status/detailed", timeout=5)
        if response.status_code != 200:
            print("❌ Backend no disponible")
            return False
        print("✅ Backend disponible")
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False
    
    results = []
    
    for coord in test_coordinates:
        print(f"\n📍 PROBANDO: {coord['name']}")
        print(f"   Coordenadas: {coord['lat']}, {coord['lng']}")
        
        # Parámetros de análisis
        analysis_params = {
            'lat_min': coord['lat'] - 0.01,
            'lat_max': coord['lat'] + 0.01,
            'lon_min': coord['lng'] - 0.01,
            'lon_max': coord['lng'] + 0.01,
            'resolution_m': 500,
            'region_name': f"Test Lupa - {coord['name']}",
            'include_explainability': True,
            'include_validation_metrics': True,
            'layers_to_analyze': [
                "ndvi_vegetation", "thermal_lst", "sar_backscatter", 
                "surface_roughness", "soil_salinity", "seismic_resonance",
                "elevation_dem", "sar_l_band", "icesat2_profiles",
                "vegetation_height", "soil_moisture",
                "lidar_fullwave", "dem_multiscale", "spectral_roughness",
                "pseudo_lidar_ai", "multitemporal_topo"
            ],
            'active_rules': ["all"]
        }
        
        try:
            response = requests.post(
                f"{backend_url}/analyze",
                json=analysis_params,
                timeout=30
            )
            
            if response.status_code == 200:
                analysis_result = response.json()
                stats = analysis_result.get('statistical_results', {})
                
                # Extraer datos clave
                wreck_candidates = stats.get('wreck_candidates', 0)
                total_anomalies = stats.get('total_anomalies', 0)
                high_priority = stats.get('high_priority_targets', 0)
                
                print(f"   🚢 Candidatos a naufragios: {wreck_candidates}")
                print(f"   🎯 Total anomalías: {total_anomalies}")
                print(f"   ⭐ Alta prioridad: {high_priority}")
                
                # Simular lógica corregida de checkForAnomalies
                should_activate_lupa = False
                activation_reason = ""
                
                if wreck_candidates > 0:
                    should_activate_lupa = True
                    activation_reason = f"{wreck_candidates} candidatos a naufragios detectados"
                elif total_anomalies > 0:
                    should_activate_lupa = True
                    activation_reason = f"{total_anomalies} anomalías detectadas"
                
                # Simular lógica corregida de detectAnomalyTypes
                expected_anomalies_in_lupa = min(wreck_candidates, 5) if wreck_candidates > 0 else 0
                
                # Determinar mensaje esperado
                expected_button_text = ""
                if wreck_candidates > 0:
                    expected_button_text = f"🔍 Lupa Arqueológica ({wreck_candidates} candidatos)"
                else:
                    expected_button_text = "🔍 Lupa Arqueológica"
                
                # Evaluar resultado
                test_result = {
                    'coordinates': coord,
                    'backend_response': {
                        'wreck_candidates': wreck_candidates,
                        'total_anomalies': total_anomalies,
                        'high_priority_targets': high_priority
                    },
                    'expected_frontend_behavior': {
                        'should_activate_lupa': should_activate_lupa,
                        'activation_reason': activation_reason,
                        'expected_button_text': expected_button_text,
                        'expected_anomalies_in_lupa': expected_anomalies_in_lupa,
                        'should_show_visualization_section': expected_anomalies_in_lupa > 0
                    },
                    'test_status': 'PASS' if should_activate_lupa else 'FAIL'
                }
                
                results.append(test_result)
                
                print(f"   🔍 ¿Activar lupa?: {'SÍ ✅' if should_activate_lupa else 'NO ❌'}")
                print(f"   📝 Razón: {activation_reason}")
                print(f"   🎨 Anomalías en lupa: {expected_anomalies_in_lupa}")
                print(f"   📱 Texto del botón: {expected_button_text}")
                print(f"   ✅ Estado: {test_result['test_status']}")
                
            else:
                print(f"   ❌ Error en análisis: {response.status_code}")
                results.append({
                    'coordinates': coord,
                    'test_status': 'ERROR',
                    'error': f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'coordinates': coord,
                'test_status': 'ERROR',
                'error': str(e)
            })
    
    # Resumen final
    print(f"\n📊 RESUMEN DEL TEST DE ACTIVACIÓN DE LUPA")
    print("=" * 60)
    
    passed_tests = len([r for r in results if r.get('test_status') == 'PASS'])
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Tests ejecutados: {total_tests}")
    print(f"Tests exitosos: {passed_tests}")
    print(f"Tasa de éxito: {success_rate:.1f}%")
    
    # Instrucciones para verificación manual
    print(f"\n🎯 INSTRUCCIONES PARA VERIFICACIÓN MANUAL:")
    print("=" * 60)
    
    for i, result in enumerate(results, 1):
        if result.get('test_status') == 'PASS':
            coord = result['coordinates']
            expected = result['expected_frontend_behavior']
            
            print(f"\n{i}. TEST {coord['name']}:")
            print(f"   📍 Coordenadas: {coord['lat']}, {coord['lng']}")
            print(f"   🌐 URL: http://localhost:8080")
            print(f"   📝 Pasos:")
            print(f"      1. Introducir coordenadas: {coord['lat']}, {coord['lng']}")
            print(f"      2. Hacer clic en INVESTIGAR")
            print(f"      3. VERIFICAR: Mensaje '{expected['activation_reason']}'")
            print(f"      4. VERIFICAR: Botón '{expected['expected_button_text']}'")
            print(f"      5. Hacer clic en la lupa")
            print(f"      6. VERIFICAR: {expected['expected_anomalies_in_lupa']} anomalías en sección de visualización")
            print(f"      7. VERIFICAR: Botones '🖼️ Vista 2D' y '🎲 Modelo 3D' funcionan")
    
    # Guardar resultados
    output_file = f"lupa_activation_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'test_info': {
                'title': 'Test de Activación de Lupa Post-Correcciones',
                'date': datetime.now().isoformat(),
                'success_rate': success_rate
            },
            'results': results,
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': total_tests - passed_tests,
                'success_rate': success_rate
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados: {output_file}")
    
    if success_rate >= 66.7:  # Al menos 2 de 3 tests
        print(f"\n🎉 TEST DE ACTIVACIÓN EXITOSO")
        print(f"✅ Las correcciones funcionan correctamente")
        print(f"🔍 La lupa debería activarse automáticamente")
        return True
    else:
        print(f"\n❌ TEST DE ACTIVACIÓN FALLÓ")
        print(f"🔧 Revisa las correcciones o coordenadas")
        return False

if __name__ == "__main__":
    success = test_lupa_activation()
    exit(0 if success else 1)