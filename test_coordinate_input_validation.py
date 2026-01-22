#!/usr/bin/env python3
"""
Test para validar que calibración y análisis avanzado usen coordenadas de entrada del usuario
"""

import requests
import json

def test_coordinate_input_validation():
    print("🎯 TESTING COORDINATE INPUT VALIDATION")
    print("=" * 60)
    
    # Coordenadas de prueba del usuario (diferentes a las hardcodeadas)
    user_lat = 41.8550  # Roma, Via Appia
    user_lon = 12.5150
    offset = 0.005
    
    user_coords = {
        "lat_min": user_lat - offset,
        "lat_max": user_lat + offset,
        "lon_min": user_lon - offset,
        "lon_max": user_lon + offset
    }
    
    print(f"📍 Coordenadas del usuario: {user_lat}, {user_lon}")
    print(f"🎯 Región: {user_coords['lat_min']:.6f} a {user_coords['lat_max']:.6f}, {user_coords['lon_min']:.6f} a {user_coords['lon_max']:.6f}")
    
    # Test 1: Calibración con coordenadas del usuario
    print("\n🔬 TEST 1: Protocolo de Calibración")
    calibration_data = {
        **user_coords,
        "resolution_m": 10,
        "region_name": "User Input Calibration Test",
        "include_explainability": True,
        "include_validation_metrics": True,
        "layers_to_analyze": ["ndvi_vegetation", "thermal_lst"],
        "active_rules": ["all"],
        "calibration_mode": True
    }
    
    try:
        response = requests.post('http://localhost:8004/analyze', 
                               json=calibration_data, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            region_info = data.get('region_info', {})
            
            # Verificar que las coordenadas del análisis coinciden con las del usuario
            analyzed_lat = (region_info.get('lat_min', 0) + region_info.get('lat_max', 0)) / 2
            analyzed_lon = (region_info.get('lon_min', 0) + region_info.get('lon_max', 0)) / 2
            
            print(f"   ✅ Calibración completada")
            print(f"   📍 Coordenadas analizadas: {analyzed_lat:.6f}, {analyzed_lon:.6f}")
            print(f"   🎯 Coincidencia con usuario: {'✅' if abs(analyzed_lat - user_lat) < 0.001 and abs(analyzed_lon - user_lon) < 0.001 else '❌'}")
            
            # Verificar que NO usa coordenadas hardcodeadas
            hardcoded_lat = -63.441533826185974
            hardcoded_lon = -83.12466836825169
            uses_hardcoded = abs(analyzed_lat - hardcoded_lat) < 0.001 and abs(analyzed_lon - hardcoded_lon) < 0.001
            print(f"   🚫 NO usa coordenadas hardcodeadas: {'✅' if not uses_hardcoded else '❌ ERROR'}")
            
        else:
            print(f"   ❌ Error en calibración: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error en test de calibración: {e}")
    
    # Test 2: Análisis avanzado con coordenadas del usuario (área ampliada)
    print("\n🚀 TEST 2: Análisis Temporal-Geométrico Avanzado")
    advanced_offset = 0.01  # Área ampliada para análisis geométrico
    advanced_coords = {
        "lat_min": user_lat - advanced_offset,
        "lat_max": user_lat + advanced_offset,
        "lon_min": user_lon - advanced_offset,
        "lon_max": user_lon + advanced_offset
    }
    
    advanced_data = {
        **advanced_coords,
        "resolution_m": 10,
        "region_name": "User Input Advanced Analysis Test",
        "include_explainability": True,
        "include_validation_metrics": True,
        "temporal_analysis": {
            "enable_multiyear": True,
            "target_years": [2017, 2019, 2021, 2023, 2024]
        },
        "geometric_analysis": {
            "enable_roman_patterns": True,
            "actus_quadratus": 710.4
        },
        "layers_to_analyze": ["ndvi_vegetation", "thermal_lst", "sar_backscatter"],
        "active_rules": ["all"],
        "analysis_mode": "advanced_temporal_geometric"
    }
    
    try:
        response = requests.post('http://localhost:8004/analyze', 
                               json=advanced_data, 
                               timeout=45)
        
        if response.status_code == 200:
            data = response.json()
            region_info = data.get('region_info', {})
            
            # Verificar que las coordenadas del análisis coinciden con las del usuario
            analyzed_lat = (region_info.get('lat_min', 0) + region_info.get('lat_max', 0)) / 2
            analyzed_lon = (region_info.get('lon_min', 0) + region_info.get('lon_max', 0)) / 2
            
            print(f"   ✅ Análisis avanzado completado")
            print(f"   📍 Coordenadas analizadas: {analyzed_lat:.6f}, {analyzed_lon:.6f}")
            print(f"   🎯 Coincidencia con usuario: {'✅' if abs(analyzed_lat - user_lat) < 0.001 and abs(analyzed_lon - user_lon) < 0.001 else '❌'}")
            
            # Verificar área ampliada
            lat_span = region_info.get('lat_max', 0) - region_info.get('lat_min', 0)
            lon_span = region_info.get('lon_max', 0) - region_info.get('lon_min', 0)
            print(f"   📏 Área ampliada: {lat_span:.4f}° x {lon_span:.4f}° ({'✅' if lat_span >= 0.015 else '⚠️ pequeña'})")
            
            # Verificar que NO usa coordenadas hardcodeadas
            uses_hardcoded = abs(analyzed_lat - hardcoded_lat) < 0.001 and abs(analyzed_lon - hardcoded_lon) < 0.001
            print(f"   🚫 NO usa coordenadas hardcodeadas: {'✅' if not uses_hardcoded else '❌ ERROR'}")
            
            # Verificar detección de anomalías
            stats = data.get('anomaly_map', {}).get('statistics', {})
            anomalies = stats.get('spatial_anomaly_pixels', 0)
            print(f"   🔍 Anomalías detectadas: {anomalies} píxeles")
            
        else:
            print(f"   ❌ Error en análisis avanzado: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error en test de análisis avanzado: {e}")
    
    print("\n" + "=" * 60)
    print("📋 VALIDACIÓN DE FUNCIONALIDAD:")
    print("\n✅ CORRECTO - Ambas funciones deben:")
    print("   • Usar coordenadas de los campos de entrada del usuario")
    print("   • Si no hay coordenadas, configurar las de ejemplo")
    print("   • Mostrar mensaje indicando qué coordenadas se están usando")
    print("   • Permitir al usuario modificar las coordenadas antes del análisis")
    
    print("\n❌ INCORRECTO - Las funciones NO deben:")
    print("   • Usar coordenadas hardcodeadas ignorando la entrada del usuario")
    print("   • Sobrescribir coordenadas del usuario sin avisar")
    print("   • Usar siempre las mismas coordenadas de ejemplo")
    
    print("\n🎯 FRONTEND TESTING:")
    print("   1. Abrir: http://localhost:8080")
    print("   2. Ingresar coordenadas: 41.8550, 12.5150 (Roma)")
    print("   3. Hacer clic: 🔬 CALIBRACIÓN")
    print("   4. Verificar que usa las coordenadas ingresadas")
    print("   5. Hacer clic: 🚀 AVANZADO")
    print("   6. Verificar que amplía el área pero mantiene el centro")
    print("   7. Hacer clic: INVESTIGAR")
    print("   8. Verificar que el análisis usa las coordenadas correctas")

if __name__ == "__main__":
    test_coordinate_input_validation()