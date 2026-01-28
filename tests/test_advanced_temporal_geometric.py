#!/usr/bin/env python3
"""
Test del Sistema de Análisis Temporal-Geométrico Avanzado
Coordenadas específicas: -63.441533826185974, -83.12466836825169
"""

import requests
import json
import math

def test_advanced_temporal_geometric():
    print("🚀 TESTING ADVANCED TEMPORAL-GEOMETRIC ANALYSIS")
    print("=" * 80)
    
    # Coordenadas específicas para análisis avanzado
    lat = -63.441533826185974
    lon = -83.12466836825169
    offset = 0.01  # Área ampliada para análisis geométrico
    
    print(f"📍 Coordenadas de análisis: {lat}, {lon}")
    print(f"🎯 Región ampliada: ±{offset}° (~2km²)")
    
    # Configuración para análisis temporal-geométrico avanzado
    advanced_data = {
        "lat_min": lat - offset,
        "lat_max": lat + offset,
        "lon_min": lon - offset,
        "lon_max": lon + offset,
        "resolution_m": 10,  # Sentinel-2 para precisión geométrica
        "region_name": "Advanced Temporal-Geometric Analysis Site",
        "include_explainability": True,
        "include_validation_metrics": True,
        "temporal_analysis": {
            "enable_multiyear": True,
            "target_years": [2017, 2019, 2021, 2023, 2024],
            "seasonal_windows": ["march-april"]
        },
        "geometric_analysis": {
            "enable_roman_patterns": True,
            "actus_quadratus": 710.4,  # metros
            "angle_tolerance": 2.0,    # grados
            "module_tolerance": 5.0    # porcentaje
        },
        "modern_layers": {
            "include_cadastral": True,
            "include_roads": True,
            "exclusion_mode": True
        },
        "layers_to_analyze": [
            "ndvi_vegetation",      # Análisis estacional
            "thermal_lst", 
            "sar_backscatter",      # Coherencia temporal
            "surface_roughness",
            "soil_salinity"
        ],
        "active_rules": ["all"],
        "analysis_mode": "advanced_temporal_geometric"
    }
    
    print("\n⏳ ANÁLISIS TEMPORAL MULTIANUAL:")
    print("   • Ventana objetivo: 2017–2024 (7 años)")
    print("   • Ventanas estacionales: marzo-abril (consistencia)")
    print("   • Resolución: 10m (Sentinel-2)")
    print("   • Propósito: Detectar persistencia de patrones")
    
    print("\n🗺️ SUPERPOSICIÓN DE CAPAS MODERNAS:")
    print("   • Catastros modernos: Límites parcelarios actuales")
    print("   • Vías actuales: Infraestructura de transporte")
    print("   • Propósito: Exclusión de patrones modernos")
    
    print("\n📐 ANÁLISIS GEOMÉTRICO ROMANO:")
    print("   • Ángulo dominante: Orientaciones cardinales (±2°)")
    print("   • Módulo repetitivo: ≈710m actus quadratus (±5%)")
    print("   • Fracciones: 355m, 177.5m, 118.3m")
    print("   • Sistema: Cuadrícula de centuriación")
    
    try:
        print("\n🔍 Ejecutando análisis temporal-geométrico avanzado...")
        response = requests.post('http://localhost:8004/analyze', 
                               json=advanced_data, 
                               timeout=45)  # Más tiempo para análisis complejo
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Análisis avanzado completado")
            
            # Verificar datos temporales
            temporal_data = data.get('temporal_analysis', {})
            print(f"\n⏳ RESULTADOS TEMPORALES:")
            print(f"   - Ventanas disponibles: {temporal_data.get('available_windows', 0)}")
            print(f"   - Años cubiertos: {temporal_data.get('time_span_years', 0)}")
            print(f"   - Persistencia detectada: {'✅' if temporal_data.get('persistence_detected') else '❌'}")
            
            # Verificar análisis geométrico
            geometric_data = data.get('geometric_analysis', {})
            dominant_angles = geometric_data.get('dominant_angles', [])
            repetitive_distances = geometric_data.get('repetitive_distances', [])
            
            print(f"\n📐 RESULTADOS GEOMÉTRICOS:")
            print(f"   - Ángulos dominantes detectados: {len(dominant_angles)}")
            if dominant_angles:
                print(f"     Ángulos: {[f'{angle:.1f}°' for angle in dominant_angles[:5]]}")
            
            print(f"   - Distancias repetitivas: {len(repetitive_distances)}")
            if repetitive_distances:
                print(f"     Distancias: {[f'{dist:.1f}m' for dist in repetitive_distances[:5]]}")
            
            # Análisis de compatibilidad romana
            roman_compatibility = analyze_roman_compatibility(dominant_angles, repetitive_distances)
            print(f"\n🏛️ COMPATIBILIDAD ROMANA:")
            print(f"   - Ángulos romanos: {roman_compatibility['angle_matches']} coincidencias")
            print(f"   - Módulos romanos: {roman_compatibility['module_matches']} coincidencias")
            print(f"   - Confianza: {roman_compatibility['confidence']}")
            
            # Verificar capas modernas
            modern_footprint = data.get('modern_human_footprint', {})
            print(f"\n🗺️ CAPAS MODERNAS:")
            print(f"   - Datos catastrales: {'✅' if modern_footprint.get('cadastral_data') else '❌'}")
            print(f"   - Red vial: {'✅' if modern_footprint.get('road_network') else '❌'}")
            
            # Evaluación final
            stats = data.get('anomaly_map', {}).get('statistics', {})
            anomalies = stats.get('spatial_anomaly_pixels', 0)
            signatures = stats.get('archaeological_signature_pixels', 0)
            
            print(f"\n🎯 EVALUACIÓN FINAL:")
            print(f"   - Píxeles anómalos: {anomalies}")
            print(f"   - Firmas arqueológicas: {signatures}")
            
            # Criterio de validación científica
            strong_evidence = (
                roman_compatibility['angle_matches'] > 0 and
                roman_compatibility['module_matches'] > 0 and
                temporal_data.get('persistence_detected', False) and
                (modern_footprint.get('cadastral_data') or modern_footprint.get('road_network'))
            )
            
            if strong_evidence:
                print("\n🚀 RESULTADO: EVIDENCIA FUERTE")
                print("   ✅ Ángulos coinciden con orientaciones romanas")
                print("   ✅ Módulos se repiten en fracciones de 710m")
                print("   ✅ Persistencia temporal detectada")
                print("   ✅ Exclusión de patrones modernos")
                print("\n   👉 EL SISTEMA PUEDE DECIR ALGO MUY FUERTE, Y SIN RUBORIZARSE")
            elif roman_compatibility['confidence'] != 'Muy baja':
                print("\n🟡 RESULTADO: EVIDENCIA PARCIAL")
                print("   🔍 Algunos patrones geométricos detectados")
                print("   ⚠️ Requiere datos temporales o capas modernas adicionales")
            else:
                print("\n❌ RESULTADO: SIN EVIDENCIA CLARA")
                print("   🔍 No se detectaron patrones geométricos romanos")
                print("   ✅ Resultado científicamente válido")
            
        else:
            print(f"❌ Error en análisis avanzado: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error en análisis temporal-geométrico: {e}")
    
    print("\n" + "=" * 80)
    print("🎯 PRÓXIMOS PASOS PARA ANÁLISIS COMPLETO:")
    print("\n⏳ Datos temporales (2017-2024):")
    print("   - Obtener imágenes Sentinel-2 de años específicos")
    print("   - Mantener ventanas estacionales consistentes")
    print("   - Analizar persistencia de anomalías")
    
    print("\n🗺️ Capas modernas:")
    print("   - Integrar catastros oficiales actuales")
    print("   - Mapear red vial moderna completa")
    print("   - Superponer con anomalías para exclusión")
    
    print("\n📐 Análisis geométrico:")
    print("   - Medir ángulos dominantes con precisión")
    print("   - Calcular distancias repetitivas")
    print("   - Comparar con estándares romanos")
    
    print("\n✨ FRONTEND TESTING:")
    print("   1. Abrir: http://localhost:8080")
    print("   2. Hacer clic en botón: 🚀 AVANZADO")
    print("   3. Verificar área ampliada configurada")
    print("   4. Hacer clic en INVESTIGAR")
    print("   5. Revisar: 'Análisis Temporal-Geométrico Avanzado'")
    print("   6. Evaluar criterios de evidencia fuerte")

def analyze_roman_compatibility(angles, distances):
    """Analiza compatibilidad con patrones romanos"""
    roman_angles = [0, 45, 90, 135]  # Orientaciones cardinales
    roman_modules = [710.4, 355.2, 177.6, 118.4]  # Actus y fracciones
    
    angle_matches = 0
    for angle in angles:
        for roman_angle in roman_angles:
            if abs(angle - roman_angle) <= 2:  # Tolerancia ±2°
                angle_matches += 1
                break
    
    module_matches = 0
    for distance in distances:
        for roman_module in roman_modules:
            deviation = abs(distance - roman_module) / roman_module * 100
            if deviation <= 5:  # Tolerancia ±5%
                module_matches += 1
                break
    
    # Calcular confianza
    total_score = min(angle_matches * 25, 50) + min(module_matches * 25, 50)
    
    if total_score >= 75:
        confidence = "Alta (evidencia convergente)"
    elif total_score >= 50:
        confidence = "Media (patrones detectados)"
    elif total_score >= 25:
        confidence = "Baja (indicios geométricos)"
    else:
        confidence = "Muy baja (sin patrones claros)"
    
    return {
        'angle_matches': angle_matches,
        'module_matches': module_matches,
        'confidence': confidence,
        'total_score': total_score
    }

if __name__ == "__main__":
    test_advanced_temporal_geometric()