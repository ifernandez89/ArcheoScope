#!/usr/bin/env python3
"""
Test para debuggear el flujo completo y verificar que los mensajes aparezcan correctamente
"""

import requests
import json
from datetime import datetime

def test_complete_flow_debug():
    """Test completo del flujo con debugging detallado"""
    
    print("🔍 TEST DE FLUJO COMPLETO - DEBUG DETALLADO")
    print("=" * 60)
    
    # Coordenadas que sabemos que funcionan
    test_coordinates = {
        'lat': 25.55,
        'lng': -70.25,
        'name': 'Centro del Caribe - Debug Test'
    }
    
    print(f"📍 Coordenadas: {test_coordinates['lat']}, {test_coordinates['lng']}")
    
    # Verificar backend
    backend_url = "http://localhost:8003"
    
    try:
        response = requests.get(f"{backend_url}/status/detailed", timeout=5)
        if response.status_code == 200:
            print("✅ Backend disponible")
        else:
            print("❌ Backend no responde")
            return False
    except Exception as e:
        print(f"❌ Backend no disponible: {e}")
        return False
    
    # Ejecutar análisis exactamente como lo hace el frontend
    analysis_params = {
        'lat_min': test_coordinates['lat'] - 0.005,
        'lat_max': test_coordinates['lat'] + 0.005,
        'lon_min': test_coordinates['lng'] - 0.005,
        'lon_max': test_coordinates['lng'] + 0.005,
        'resolution_m': 500,
        'region_name': "Región Arqueológica Investigada",
        'include_explainability': True,
        'include_validation_metrics': True,
        'layers_to_analyze': [
            # Base (6)
            "ndvi_vegetation", "thermal_lst", "sar_backscatter", 
            "surface_roughness", "soil_salinity", "seismic_resonance",
            # Enhanced (5)
            "elevation_dem", "sar_l_band", "icesat2_profiles",
            "vegetation_height", "soil_moisture",
            # NUEVAS CAPAS AVANZADAS (5)
            "lidar_fullwave", "dem_multiscale", "spectral_roughness",
            "pseudo_lidar_ai", "multitemporal_topo"
        ],
        'active_rules': ["all"]
    }
    
    print(f"\n🔬 Ejecutando análisis (simulando frontend)...")
    print(f"📊 Parámetros: {json.dumps(analysis_params, indent=2)}")
    
    try:
        response = requests.post(
            f"{backend_url}/analyze",
            json=analysis_params,
            timeout=30
        )
        
        if response.status_code == 200:
            analysis_result = response.json()
            print("✅ Análisis completado exitosamente")
            
            # Verificar estructura completa
            print(f"\n📋 ESTRUCTURA DE RESPUESTA:")
            print(f"   🔑 Claves principales: {list(analysis_result.keys())}")
            
            if 'statistical_results' in analysis_result:
                stats = analysis_result['statistical_results']
                print(f"   📊 statistical_results: {list(stats.keys())}")
                
                # Datos clave para la lupa
                wreck_candidates = stats.get('wreck_candidates', 0)
                total_anomalies = stats.get('total_anomalies', 0)
                high_priority = stats.get('high_priority_targets', 0)
                
                print(f"   🚢 wreck_candidates: {wreck_candidates}")
                print(f"   🎯 total_anomalies: {total_anomalies}")
                print(f"   ⭐ high_priority_targets: {high_priority}")
            else:
                print("   ❌ NO HAY statistical_results")
            
            if 'anomaly_map' in analysis_result:
                anomaly_map = analysis_result['anomaly_map']
                print(f"   🗺️ anomaly_map: {list(anomaly_map.keys())}")
                
                if 'statistics' in anomaly_map:
                    map_stats = anomaly_map['statistics']
                    print(f"   📈 anomaly_map.statistics: {list(map_stats.keys())}")
                    
                    spatial_anomalies = map_stats.get('spatial_anomaly_pixels', 0)
                    archaeological_signatures = map_stats.get('archaeological_signature_pixels', 0)
                    
                    print(f"   🎯 spatial_anomaly_pixels: {spatial_anomalies}")
                    print(f"   🏛️ archaeological_signature_pixels: {archaeological_signatures}")
                else:
                    print("   ❌ NO HAY anomaly_map.statistics")
            else:
                print("   ❌ NO HAY anomaly_map")
            
            # Simular exactamente lo que hace checkForAnomalies CORREGIDA
            print(f"\n🔍 SIMULANDO checkForAnomalies CORREGIDA:")
            
            if 'statistical_results' in analysis_result:
                stats = analysis_result['statistical_results']
                
                wreck_candidates = stats.get('wreck_candidates', 0)
                total_anomalies = stats.get('total_anomalies', 0)
                
                should_activate_lupa = False
                activation_reason = ''
                
                if wreck_candidates > 0:
                    should_activate_lupa = True
                    activation_reason = f"{wreck_candidates} candidatos a naufragios detectados"
                elif total_anomalies > 0:
                    should_activate_lupa = True
                    activation_reason = f"{total_anomalies} anomalías detectadas"
                
                print(f"   ¿Activar lupa?: {'SÍ ✅' if should_activate_lupa else 'NO ❌'}")
                print(f"   Razón: {activation_reason}")
                
                if should_activate_lupa:
                    print(f"   📱 Texto del botón: 🔍 Lupa Arqueológica ({wreck_candidates} candidatos)")
                    print(f"   💬 Mensaje esperado: 🔍 ¡ANOMALÍAS DETECTADAS! {activation_reason}")
                
                # Simular detectAnomalyTypes
                expected_anomalies = min(wreck_candidates, 5) if wreck_candidates > 0 else 0
                print(f"   🎨 Anomalías en lupa: {expected_anomalies}")
                
            else:
                print("   ❌ NO SE PUEDE SIMULAR - Falta statistical_results")
            
            # Verificar mensaje final basado en anomaly_map
            print(f"\n📋 SIMULANDO MENSAJE FINAL:")
            
            if 'anomaly_map' in analysis_result and 'statistics' in analysis_result['anomaly_map']:
                map_stats = analysis_result['anomaly_map']['statistics']
                spatial_anomalies = map_stats.get('spatial_anomaly_pixels', 0)
                archaeological_signatures = map_stats.get('archaeological_signature_pixels', 0)
                
                if archaeological_signatures > 0:
                    expected_message = "ANOMALÍAS ARQUEOLÓGICAS DETECTADAS"
                elif spatial_anomalies > 0:
                    expected_message = "ANOMALÍAS ESPACIALES DETECTADAS"
                else:
                    expected_message = "NO SE ENCONTRARON ANOMALÍAS"
                
                print(f"   📢 Mensaje final esperado: {expected_message}")
            else:
                print(f"   📢 Mensaje final: Dependerá de candidatos detectados")
            
            # Crear resumen de debugging
            debug_result = {
                'test_info': {
                    'title': 'Debug del Flujo Completo',
                    'date': datetime.now().isoformat(),
                    'coordinates': test_coordinates
                },
                'backend_response_structure': {
                    'has_statistical_results': 'statistical_results' in analysis_result,
                    'has_anomaly_map': 'anomaly_map' in analysis_result,
                    'has_anomaly_map_statistics': 'anomaly_map' in analysis_result and 'statistics' in analysis_result.get('anomaly_map', {}),
                    'main_keys': list(analysis_result.keys())
                },
                'expected_frontend_behavior': {
                    'should_activate_lupa': should_activate_lupa if 'statistical_results' in analysis_result else False,
                    'activation_reason': activation_reason if 'statistical_results' in analysis_result else 'No data',
                    'expected_anomalies_in_lupa': expected_anomalies if 'statistical_results' in analysis_result else 0,
                    'should_show_message': True
                },
                'debugging_steps': [
                    "1. Verificar que showAnalysisStatusMessage aparezca al inicio",
                    "2. Verificar que hideAnalysisStatusMessage se ejecute al final",
                    "3. Verificar que safeDisplayResults se ejecute sin errores",
                    "4. Verificar que checkForAnomalies se ejecute UNA SOLA VEZ",
                    "5. Verificar que showMessage se ejecute con el mensaje correcto",
                    "6. Verificar que el botón de lupa aparezca automáticamente"
                ]
            }
            
            # Guardar debug
            output_file = f"flow_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(debug_result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Debug guardado: {output_file}")
            
            print(f"\n🎯 PASOS PARA VERIFICAR MANUALMENTE:")
            print(f"1. Abrir http://localhost:8080")
            print(f"2. Abrir DevTools (F12) y ir a Console")
            print(f"3. Introducir coordenadas: {test_coordinates['lat']}, {test_coordinates['lng']}")
            print(f"4. Hacer clic en INVESTIGAR")
            print(f"5. OBSERVAR en Console:")
            print(f"   - Mensajes de showAnalysisStatusMessage")
            print(f"   - Llamada a safeDisplayResults")
            print(f"   - Llamada a checkForAnomalies")
            print(f"   - Mensajes de showMessage")
            print(f"6. VERIFICAR en UI:")
            print(f"   - Aparece mensaje de inicio de análisis")
            print(f"   - Aparece mensaje de finalización")
            print(f"   - Aparece botón de lupa automáticamente")
            
            return True
                
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_flow_debug()
    if success:
        print(f"\n🎉 DEBUG COMPLETADO")
        print(f"✅ Usa las instrucciones para verificar manualmente")
    else:
        print(f"\n❌ DEBUG FALLÓ")
        print(f"🔧 Revisa la configuración del backend")