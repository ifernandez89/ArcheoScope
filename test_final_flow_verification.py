#!/usr/bin/env python3
"""
Test final para verificar que el flujo completo funcione después de las correcciones
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import requests
import time

def test_final_flow():
    """Test final del flujo completo corregido"""
    
    print("🎉 TEST FINAL - VERIFICACIÓN DE CORRECCIONES")
    print("=" * 60)
    
    # Coordenadas que sabemos que funcionan
    test_coordinates = {
        'lat': 25.55,
        'lng': -70.25,
        'name': 'Centro del Triángulo - Test Final'
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
    
    # Ejecutar análisis
    analysis_params = {
        'lat_min': test_coordinates['lat'] - 0.01,
        'lat_max': test_coordinates['lat'] + 0.01,
        'lon_min': test_coordinates['lng'] - 0.01,
        'lon_max': test_coordinates['lng'] + 0.01,
        'resolution_m': 500,
        'region_name': "Región Arqueológica Investigada",
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
    
    print(f"\n🔬 Ejecutando análisis...")
    
    try:
        response = requests.post(
            f"{backend_url}/analyze",
            json=analysis_params,
            timeout=30
        )
        
        if response.status_code == 200:
            analysis_result = response.json()
            print("✅ Análisis completado")
            
            # Verificar estructura
            stats = analysis_result.get('statistical_results', {})
            wreck_candidates = stats.get('wreck_candidates', 0)
            total_anomalies = stats.get('total_anomalies', 0)
            
            print(f"\n📊 Resultados:")
            print(f"   🚢 Candidatos a naufragios: {wreck_candidates}")
            print(f"   🎯 Total anomalías: {total_anomalies}")
            
            # Simular checkForAnomalies corregida
            print(f"\n🔍 Simulando checkForAnomalies CORREGIDA...")
            
            should_activate = False
            activation_reason = ""
            
            if wreck_candidates > 0:
                should_activate = True
                activation_reason = f"{wreck_candidates} candidatos a naufragios detectados"
            elif total_anomalies > 0:
                should_activate = True
                activation_reason = f"{total_anomalies} anomalías detectadas"
            
            print(f"   ¿Activar lupa?: {'SÍ ✅' if should_activate else 'NO ❌'}")
            print(f"   Razón: {activation_reason}")
            
            # Simular detectAnomalyTypes corregida
            print(f"\n🎯 Simulando detectAnomalyTypes CORREGIDA...")
            
            expected_anomalies = min(wreck_candidates, 5) if wreck_candidates > 0 else 0
            print(f"   Anomalías esperadas en lupa: {expected_anomalies}")
            
            if expected_anomalies > 0:
                print(f"   Tipos esperados:")
                for i in range(expected_anomalies):
                    candidate_num = i + 1
                    is_high_priority = i < stats.get('high_priority_targets', 0)
                    priority = "Alta" if is_high_priority else "Media"
                    print(f"      {candidate_num}. Candidato a Naufragio {candidate_num} ({priority} prioridad)")
            
            # Verificar anomaly_map para mensaje final
            print(f"\n📋 Verificando mensaje final...")
            anomaly_map = analysis_result.get('anomaly_map', {})
            
            if 'statistics' in anomaly_map:
                map_stats = anomaly_map['statistics']
                spatial_anomalies = map_stats.get('spatial_anomaly_pixels', 0)
                archaeological_signatures = map_stats.get('archaeological_signature_pixels', 0)
                
                if archaeological_signatures > 0:
                    expected_message = "ANOMALÍAS ARQUEOLÓGICAS DETECTADAS"
                elif spatial_anomalies > 0:
                    expected_message = "ANOMALÍAS ESPACIALES DETECTADAS"
                else:
                    expected_message = "NO SE ENCONTRARON ANOMALÍAS"
                
                print(f"   Mensaje esperado: {expected_message}")
            else:
                print(f"   ⚠️ No hay estadísticas en anomaly_map - mensaje dependerá de candidatos")
            
            # Crear resumen de verificación
            verification_result = {
                'test_info': {
                    'title': 'Verificación Final del Flujo Corregido',
                    'date': datetime.now().isoformat(),
                    'coordinates': test_coordinates
                },
                'backend_results': {
                    'wreck_candidates': wreck_candidates,
                    'total_anomalies': total_anomalies,
                    'high_priority_targets': stats.get('high_priority_targets', 0)
                },
                'expected_frontend_behavior': {
                    'should_activate_lupa': should_activate,
                    'activation_reason': activation_reason,
                    'expected_anomalies_in_lupa': expected_anomalies,
                    'should_show_visualization_section': expected_anomalies > 0
                },
                'test_instructions': [
                    "1. Abrir http://localhost:8080",
                    f"2. Introducir coordenadas: {test_coordinates['lat']}, {test_coordinates['lng']}",
                    "3. Hacer clic en INVESTIGAR",
                    "4. VERIFICAR: Aparece mensaje de análisis completado",
                    f"5. VERIFICAR: Aparece botón '🔍 Lupa Arqueológica ({wreck_candidates} candidatos)'",
                    "6. Hacer clic en la lupa",
                    f"7. VERIFICAR: Sección '🎨 Visualización de Anomalías Detectadas' visible",
                    f"8. VERIFICAR: Muestra {expected_anomalies} anomalías para seleccionar",
                    "9. VERIFICAR: Botones '🖼️ Vista 2D' y '🎲 Modelo 3D' funcionan"
                ],
                'success_criteria': {
                    'lupa_button_appears': should_activate,
                    'visualization_section_active': expected_anomalies > 0,
                    'anomalies_generated': expected_anomalies,
                    'image_generation_available': True
                }
            }
            
            # Guardar verificación
            output_file = f"final_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(verification_result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Verificación guardada: {output_file}")
            
            print(f"\n🎯 INSTRUCCIONES PARA VERIFICAR MANUALMENTE:")
            for instruction in verification_result['test_instructions']:
                print(f"   {instruction}")
            
            if should_activate and expected_anomalies > 0:
                print(f"\n✅ PREDICCIÓN: El flujo debería funcionar completamente")
                print(f"🔍 La lupa debería activarse automáticamente")
                print(f"🎨 La sección de visualización debería aparecer")
                print(f"🖼️ Los botones de generación deberían funcionar")
                return True
            else:
                print(f"\n⚠️ ADVERTENCIA: Pocas anomalías detectadas")
                print(f"🔍 La lupa podría no activarse")
                return False
                
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_final_flow()
    if success:
        print(f"\n🎉 VERIFICACIÓN EXITOSA")
        print(f"✅ Las correcciones deberían resolver todos los bugs")
        print(f"🔍 Prueba manualmente siguiendo las instrucciones")
    else:
        print(f"\n❌ VERIFICACIÓN FALLÓ")
        print(f"🔧 Revisa la configuración o coordenadas")