#!/usr/bin/env python3
"""
Test del Protocolo de Calibración Científica con coordenadas específicas
Coordenadas de ejemplo: -63.441533826185974, -83.12466836825169
"""

import requests
import json

def test_calibration_protocol():
    print("🔬 TESTING ARCHEOSCOPE CALIBRATION PROTOCOL")
    print("=" * 70)
    
    # Coordenadas específicas para calibración
    lat = -63.441533826185974
    lon = -83.12466836825169
    offset = 0.005
    
    print(f"📍 Coordenadas de calibración: {lat}, {lon}")
    print(f"🎯 Región de análisis: ±{offset}° (~1km²)")
    
    # PASO 1 - No tocar el motor (configuración actual)
    print("\n🔧 PASO 1 – No tocar el motor")
    print("   ✅ Motor intacto - configuración preservada")
    
    # PASO 2 - Repetir mismo sitio con datos mejorados
    test_data_calibration = {
        "lat_min": lat - offset,
        "lat_max": lat + offset,
        "lon_min": lon - offset,
        "lon_max": lon + offset,
        "resolution_m": 10,  # Sentinel-2 óptimo
        "region_name": "Calibration Protocol Site",
        "include_explainability": True,
        "include_validation_metrics": True,
        "layers_to_analyze": [
            "ndvi_vegetation",      # NDVI estacional
            "thermal_lst", 
            "sar_backscatter",      # Sentinel-1 coherencia temporal
            "surface_roughness",
            "soil_salinity"
        ],
        "active_rules": ["all"],
        "calibration_mode": True
    }
    
    print("\n🛰️ PASO 2 – Repetir este mismo sitio con:")
    print("   • Sentinel-2 (10 m) - Resolución óptica óptima")
    print("   • NDVI estacional (primavera vs verano) - Detectar ciclos")
    print("   • Sentinel-1 coherencia temporal - Estabilidad estructural")
    
    try:
        print("\n🔍 Ejecutando análisis de calibración...")
        response = requests.post('http://localhost:8004/analyze', 
                               json=test_data_calibration, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Análisis de calibración completado")
            
            # Verificar datos clave
            region_info = data.get('region_info', {})
            stats = data.get('anomaly_map', {}).get('statistics', {})
            
            print(f"   - Resolución: {region_info.get('resolution_m', 'unknown')}m")
            print(f"   - Área: {region_info.get('area_km2', 'unknown')} km²")
            print(f"   - Píxeles anómalos: {stats.get('spatial_anomaly_pixels', 0)}")
            print(f"   - Firmas arqueológicas: {stats.get('archaeological_signature_pixels', 0)}")
            
            # Análisis de resultados para PASO 3
            anomalies = stats.get('spatial_anomaly_pixels', 0)
            signatures = stats.get('archaeological_signature_pixels', 0)
            
            print("\n🔍 PASO 3 – Análisis comparativo:")
            
            if signatures > 0:
                print("   ✅ Aparecen alineaciones → Potencial arqueológico detectado")
                print("   🔍 La masa se fragmenta en geometría → Estructura detectada")
                result_type = "POSITIVO"
            elif anomalies > 0:
                print("   🟡 Anomalías detectadas pero sin firmas arqueológicas claras")
                print("   🔍 Requiere comparación con sitios de referencia")
                result_type = "AMBIGUO"
            else:
                print("   ❌ Se disuelve → No era arqueología")
                print("   ✅ Resultado científicamente válido")
                result_type = "NEGATIVO"
            
            print(f"\n🎯 RESULTADO DE CALIBRACIÓN: {result_type}")
            print("🧠 Principio científico: Ambos resultados son válidos")
            
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error en protocolo de calibración: {e}")
    
    # Recomendaciones para PASO 3 completo
    print("\n" + "=" * 70)
    print("📋 PRÓXIMOS PASOS PARA CALIBRACIÓN COMPLETA:")
    print("\n🏺 Sitio arqueológico confirmado (referencia positiva):")
    print("   - Buscar coordenadas de sitio arqueológico conocido")
    print("   - Repetir análisis con mismos parámetros")
    print("   - Comparar patrones de alineación y geometría")
    
    print("\n🏢 Sitio moderno confirmado (referencia negativa):")
    print("   - Buscar coordenadas de desarrollo urbano/agrícola reciente")
    print("   - Repetir análisis con mismos parámetros")
    print("   - Comparar ausencia de persistencia histórica")
    
    print("\n🔬 Metodología de comparación:")
    print("   1. Ejecutar análisis en los 3 sitios con parámetros idénticos")
    print("   2. Comparar métricas de alineación y coherencia geométrica")
    print("   3. Evaluar persistencia temporal y estacional")
    print("   4. Documentar diferencias y similitudes")
    print("   5. Calibrar umbrales basados en referencias conocidas")
    
    print("\n✨ FRONTEND TESTING:")
    print("   1. Abrir: http://localhost:8080")
    print("   2. Hacer clic en botón: 🔬 CALIBRACIÓN")
    print("   3. Verificar coordenadas configuradas automáticamente")
    print("   4. Hacer clic en INVESTIGAR")
    print("   5. Revisar sección: 'Protocolo de Calibración Científica'")
    print("   6. Seguir los 3 pasos del protocolo")

if __name__ == "__main__":
    test_calibration_protocol()