#!/usr/bin/env python3
"""
Test para debuggear el flujo completo desde investigación hasta lupa
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import requests
import time

def test_complete_flow():
    """Test del flujo completo con debugging detallado"""
    
    print("🔍 TEST DE FLUJO COMPLETO - DEBUGGING DETALLADO")
    print("=" * 60)
    
    # Coordenadas que sabemos que funcionan
    test_coordinates = {
        'lat': 25.55,
        'lng': -70.25,
        'name': 'Centro del Triángulo - Debugging'
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
    
    # Simular el análisis exacto que hace el frontend
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
    
    print(f"\n🔬 PASO 1: Ejecutando análisis (igual que frontend)...")
    
    try:
        response = requests.post(
            f"{backend_url}/analyze",
            json=analysis_params,
            timeout=30
        )
        
        if response.status_code == 200:
            analysis_result = response.json()
            print("✅ Análisis completado")
            
            # PASO 2: Verificar estructura de respuesta
            print(f"\n📊 PASO 2: Verificando estructura de respuesta...")
            required_keys = ['region_info', 'statistical_results', 'anomaly_map']
            
            for key in required_keys:
                if key in analysis_result:
                    print(f"   ✅ {key}: Presente")
                else:
                    print(f"   ❌ {key}: FALTANTE")
                    return False
            
            # PASO 3: Verificar datos estadísticos
            print(f"\n📈 PASO 3: Verificando datos estadísticos...")
            stats = analysis_result.get('statistical_results', {})
            
            print(f"   Estructura: {type(stats)}")
            print(f"   Claves: {list(stats.keys())}")
            
            # Verificar si hay candidatos
            wreck_candidates = stats.get('wreck_candidates', 0)
            total_anomalies = stats.get('total_anomalies', 0)
            
            print(f"   🚢 Candidatos a naufragios: {wreck_candidates}")
            print(f"   🎯 Total anomalías: {total_anomalies}")
            
            # PASO 4: Simular checkForAnomalies
            print(f"\n🔍 PASO 4: Simulando función checkForAnomalies...")
            
            # El frontend busca statistical_results con archaeological_probability
            # Pero el backend devuelve wreck_candidates y total_anomalies
            
            # Verificar si hay datos que deberían activar la lupa
            should_activate_lupa = False
            activation_reason = ""
            
            if wreck_candidates > 0:
                should_activate_lupa = True
                activation_reason = f"{wreck_candidates} candidatos a naufragios detectados"
            elif total_anomalies > 0:
                should_activate_lupa = True
                activation_reason = f"{total_anomalies} anomalías detectadas"
            
            print(f"   ¿Debería activarse la lupa?: {'SÍ' if should_activate_lupa else 'NO'}")
            print(f"   Razón: {activation_reason}")
            
            # PASO 5: Verificar datos de anomaly_map
            print(f"\n🗺️ PASO 5: Verificando anomaly_map...")
            anomaly_map = analysis_result.get('anomaly_map', {})
            
            if 'statistics' in anomaly_map:
                map_stats = anomaly_map['statistics']
                print(f"   Estadísticas del mapa: {map_stats}")
                
                spatial_anomalies = map_stats.get('spatial_anomaly_pixels', 0)
                archaeological_signatures = map_stats.get('archaeological_signature_pixels', 0)
                
                print(f"   🎯 Píxeles anómalos espaciales: {spatial_anomalies}")
                print(f"   🏛️ Firmas arqueológicas: {archaeological_signatures}")
                
                # Esto es lo que usa generateAnalysisSummary
                if archaeological_signatures > 0:
                    print(f"   ✅ Debería mostrar: 'ANOMALÍAS ARQUEOLÓGICAS DETECTADAS'")
                elif spatial_anomalies > 0:
                    print(f"   ✅ Debería mostrar: 'ANOMALÍAS ESPACIALES DETECTADAS'")
                else:
                    print(f"   ℹ️ Debería mostrar: 'NO SE ENCONTRARON ANOMALÍAS'")
            else:
                print(f"   ❌ No hay estadísticas en anomaly_map")
            
            # PASO 6: Diagnóstico del problema
            print(f"\n🔧 PASO 6: Diagnóstico del problema...")
            
            # Problema 1: Desajuste de estructura de datos
            if wreck_candidates > 0 or total_anomalies > 0:
                print(f"   🐛 PROBLEMA IDENTIFICADO:")
                print(f"      - Backend detecta anomalías: {wreck_candidates} candidatos, {total_anomalies} anomalías")
                print(f"      - Pero checkForAnomalies busca 'archaeological_probability' en statistical_results")
                print(f"      - statistical_results contiene: {list(stats.keys())}")
                print(f"      - NO contiene datos por instrumento con probabilidades")
                
                print(f"\n   💡 SOLUCIÓN REQUERIDA:")
                print(f"      - Modificar checkForAnomalies para manejar la estructura real del backend")
                print(f"      - O modificar el backend para devolver probabilidades por instrumento")
            
            # Crear datos de prueba para el frontend
            frontend_test_data = {
                'coordinates': test_coordinates,
                'analysis_result': analysis_result,
                'diagnosis': {
                    'backend_detects_anomalies': wreck_candidates > 0 or total_anomalies > 0,
                    'frontend_structure_mismatch': True,
                    'should_activate_lupa': should_activate_lupa,
                    'activation_reason': activation_reason,
                    'problem': 'checkForAnomalies busca archaeological_probability pero backend devuelve wreck_candidates',
                    'solution': 'Modificar checkForAnomalies para manejar estructura real'
                },
                'test_timestamp': datetime.now().isoformat()
            }
            
            # Guardar diagnóstico
            output_file = f"flow_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(frontend_test_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Diagnóstico guardado: {output_file}")
            
            if should_activate_lupa:
                print(f"\n✅ CONCLUSIÓN: El backend SÍ detecta anomalías")
                print(f"❌ PROBLEMA: checkForAnomalies no puede procesarlas por desajuste de estructura")
                return True
            else:
                print(f"\n❌ CONCLUSIÓN: El backend NO detecta anomalías suficientes")
                return False
                
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    if success:
        print(f"\n🎯 SIGUIENTE PASO: Corregir checkForAnomalies para manejar estructura real del backend")
    else:
        print(f"\n❌ REVISAR: Backend o coordenadas")