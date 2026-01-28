#!/usr/bin/env python3
"""
Test específico: Valle del Indo - Zona rural Harappa periférica
Sistemas agrícolas invisibles de la Civilización del Indo

Coordenadas: 30.7°N, 72.9°E (zona rural periférica)
Objetivo: Detectar sistemas agrícolas antiguos (canales, campos organizados, drenaje)
Expectativa: 20-35% probabilidad arqueológica
"""

import requests
import json
from datetime import datetime
import sys

def test_indus_valley_agricultural_systems():
    """
    Ejecutar análisis de sistemas agrícolas invisibles del Valle del Indo.
    
    Enfoque: Detectar infraestructura agrícola sutil de la civilización del Indo:
    - Canales de irrigación antiguos
    - Sistemas de campos organizados
    - Redes de drenaje
    - Patrones de asentamiento rural
    """
    
    # URL del backend
    backend_url = "http://localhost:8004"
    
    print("🏺 ARCHEOSCOPE - Valle del Indo: Sistemas Agrícolas Invisibles")
    print("=" * 65)
    print(f"📍 Sitio: Harappa periférica (Valle del Indo)")
    print(f"🎯 Objetivo: Sistemas agrícolas de la Civilización del Indo")
    print(f"📌 Coordenadas: 30.7°N, 72.9°E (zona rural)")
    print(f"📏 Área: ~5 km² (infraestructura agrícola periférica)")
    print(f"🎲 Expectativa: 20-35% probabilidad arqueológica")
    print()
    
    # Verificar estado del sistema
    try:
        print("🔍 Verificando estado del sistema...")
        status_response = requests.get(f"{backend_url}/status/detailed", timeout=10)
        
        if status_response.status_code == 200:
            status = status_response.json()
            print(f"✅ Backend: {status['backend_status']}")
            print(f"🤖 IA: {status['ai_status']}")
            print(f"📊 Motor volumétrico: {status['volumetric_engine']}")
            print(f"🔬 Validación académica: {status['capabilities']['academic_validation']}")
            print()
        else:
            print(f"⚠️ Estado del sistema: {status_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return None
    
    # Configurar análisis específico para sistemas agrícolas del Indo
    analysis_request = {
        "lat_min": 30.695,  # Zona rural sur
        "lat_max": 30.705,  # ~1.1 km norte-sur
        "lon_min": 72.895,  # Zona rural oeste  
        "lon_max": 72.905,  # ~1.1 km este-oeste
        
        "resolution_m": 300,  # Resolución fina para captar sistemas agrícolas
        
        # Capas específicas para detectar sistemas agrícolas antiguos
        "layers_to_analyze": [
            "ndvi_vegetation",      # Patrones de cultivo y irrigación
            "thermal_lst",          # Firmas térmicas de canales y drenaje
            "sar_backscatter",      # Geometría de campos y canales
            "surface_roughness",    # Microtopografía de sistemas de riego
            "soil_salinity",        # Indicadores de manejo hídrico intensivo
            "seismic_resonance"     # Estructuras de drenaje enterradas
        ],
        
        # Reglas arqueológicas específicas para agricultura del Indo
        "active_rules": [
            "linear_anthropogenic_structures",      # Canales de irrigación
            "geometric_field_systems",             # Campos organizados geométricamente
            "water_management_infrastructure",     # Sistemas hídricos complejos
            "agricultural_terracing",              # Terrazas y nivelación
            "settlement_periphery_patterns",       # Patrones rurales periféricos
            "drainage_network_signatures"          # Redes de drenaje (si disponible)
        ],
        
        "region_name": "Indus Valley - Harappa Agricultural Periphery",
        "include_explainability": True,   # Explicación científica detallada
        "include_validation_metrics": True  # Métricas de validación académica
    }
    
    print("🚀 Iniciando análisis de sistemas agrícolas del Indo...")
    print(f"📊 Capas especializadas: {len(analysis_request['layers_to_analyze'])}")
    print(f"🔬 Reglas agrícolas: {len(analysis_request['active_rules'])}")
    print(f"🎯 Resolución: {analysis_request['resolution_m']}m (detección fina)")
    print()
    
    try:
        # Ejecutar análisis principal
        print("⏳ Ejecutando análisis arqueológico del Valle del Indo...")
        
        analysis_response = requests.post(
            f"{backend_url}/analyze", 
            json=analysis_request,
            timeout=90  # Más tiempo para análisis detallado
        )
        
        if analysis_response.status_code == 200:
            results = analysis_response.json()
            
            print("✅ Análisis completado exitosamente")
            print()
            
            # Mostrar resultados específicos del Indo
            display_indus_valley_results(results)
            
            # Guardar resultados completos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"indus_valley_harappa_agricultural_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Resultados guardados en: {filename}")
            
            return results
            
        else:
            print(f"❌ Error en análisis: {analysis_response.status_code}")
            print(f"Respuesta: {analysis_response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error ejecutando análisis: {e}")
        return None

def display_indus_valley_results(results):
    """Mostrar resultados del análisis del Valle del Indo de forma especializada."""
    
    print("🏺 RESULTADOS - SISTEMAS AGRÍCOLAS VALLE DEL INDO")
    print("=" * 55)
    
    # Información de la región
    region_info = results.get('region_info', {})
    print(f"📍 Región: {region_info.get('name', 'Valle del Indo')}")
    print(f"📏 Área: {region_info.get('area_km2', 'N/A')} km²")
    print(f"🎯 Resolución: {region_info.get('resolution_m', 'N/A')} m")
    print()
    
    # Resultados estadísticos por capa
    stats = results.get('statistical_results', {})
    if stats:
        print("📊 ANÁLISIS POR CAPAS (Sistemas Agrícolas):")
        
        # Ordenar por probabilidad arqueológica
        layer_probs = []
        for layer_name, layer_data in stats.items():
            prob = layer_data.get('archaeological_probability', 0)
            layer_probs.append((layer_name, prob, layer_data))
        
        layer_probs.sort(key=lambda x: x[1], reverse=True)
        
        for layer_name, prob, layer_data in layer_probs:
            if prob > 0.15:  # Mostrar capas con señal significativa
                coherence = layer_data.get('geometric_coherence', 0)
                persistence = layer_data.get('temporal_persistence', 0)
                
                print(f"   🌾 {layer_name}:")
                print(f"     Probabilidad agrícola: {prob:.3f} ({prob*100:.1f}%)")
                print(f"     Coherencia geométrica: {coherence:.3f}")
                print(f"     Persistencia temporal: {persistence:.3f}")
                
                # Interpretación específica por capa
                if layer_name == "ndvi_vegetation" and prob > 0.25:
                    print(f"     💡 Posibles patrones de irrigación antigua")
                elif layer_name == "soil_salinity" and prob > 0.25:
                    print(f"     💡 Indicadores de manejo hídrico intensivo")
                elif layer_name == "sar_backscatter" and prob > 0.25:
                    print(f"     💡 Geometría de campos organizados")
                elif layer_name == "surface_roughness" and prob > 0.25:
                    print(f"     💡 Microtopografía de sistemas de riego")
        print()
    
    # Evaluación arqueológica integrada
    archaeological = results.get('physics_results', {})
    if archaeological:
        print("🏛️ EVALUACIÓN ARQUEOLÓGICA INTEGRADA:")
        
        evaluations = archaeological.get('evaluations', {})
        total_prob = 0
        count = 0
        
        for rule_name, evaluation in evaluations.items():
            prob = evaluation.get('archaeological_probability', 0)
            confidence = evaluation.get('confidence', 0)
            
            if prob > 0.2:  # Mostrar evaluaciones significativas
                print(f"   📋 {rule_name}:")
                print(f"     Probabilidad: {prob:.3f} ({prob*100:.1f}%)")
                print(f"     Confianza: {confidence:.3f}")
                
                # Detalles específicos si están disponibles
                details = evaluation.get('evidence_details', {})
                if details:
                    suspected_features = details.get('suspected_features', [])
                    if suspected_features:
                        print(f"     Características detectadas: {len(suspected_features)}")
                
                total_prob += prob
                count += 1
        
        # Score integrado
        integrated = archaeological.get('integrated_analysis', {})
        if integrated:
            print(f"\n🎯 EVALUACIÓN INTEGRADA:")
            print(f"   Score total: {integrated.get('integrated_score', 0):.3f}")
            print(f"   Clasificación: {integrated.get('classification', 'N/A')}")
            print(f"   Explicación: {integrated.get('explanation', 'N/A')}")
        elif count > 0:
            avg_prob = total_prob / count
            print(f"\n🎯 PROBABILIDAD PROMEDIO: {avg_prob:.3f} ({avg_prob*100:.1f}%)")
        print()
    
    # Interpretación específica del Valle del Indo
    print("🌾 INTERPRETACIÓN VALLE DEL INDO:")
    
    # Calcular probabilidad general
    general_prob = 0
    if stats:
        probs = [data.get('archaeological_probability', 0) for data in stats.values()]
        general_prob = sum(probs) / len(probs) if probs else 0
    
    print(f"   Probabilidad general: {general_prob:.3f} ({general_prob*100:.1f}%)")
    
    # Interpretación contextual
    if general_prob > 0.35:
        print("   🟢 ALTA probabilidad de sistemas agrícolas del Indo")
        print("   💡 Patrones consistentes con agricultura organizada")
        print("   🔍 Recomendado: Validación geofísica inmediata")
    elif general_prob > 0.20:
        print("   🟡 MODERADA probabilidad de sistemas agrícolas")
        print("   💡 Indicios de organización espacial antigua")
        print("   🔍 Recomendado: Análisis complementario")
    else:
        print("   🔴 BAJA probabilidad de sistemas agrícolas")
        print("   💡 Patrones dominantemente naturales")
        print("   🔍 Considerar otras zonas periféricas")
    
    # Contexto histórico del Indo
    print(f"\n📚 CONTEXTO CIVILIZACIÓN DEL INDO:")
    print(f"   Período: ~3300-1300 BCE")
    print(f"   Características esperadas:")
    print(f"     • Sistemas de irrigación planificados")
    print(f"     • Campos geométricamente organizados") 
    print(f"     • Redes de drenaje sofisticadas")
    print(f"     • Asentamientos rurales periféricos")
    print()
    
    # Mapa de anomalías
    anomaly_map = results.get('anomaly_map', {})
    if anomaly_map:
        stats_map = anomaly_map.get('statistics', {})
        if stats_map:
            print("🗺️ DISTRIBUCIÓN ESPACIAL:")
            print(f"   Área con anomalías: {stats_map.get('spatial_anomaly_percentage', 0):.1f}%")
            print(f"   Firmas arqueológicas: {stats_map.get('archaeological_signature_percentage', 0):.1f}%")
            print(f"   Procesos naturales: {stats_map.get('natural_percentage', 0):.1f}%")
            print()
    
    # Reporte científico
    scientific = results.get('scientific_report', {})
    if scientific:
        summary = scientific.get('summary', {})
        if summary:
            print("🔬 RESUMEN CIENTÍFICO:")
            print(f"   Anomalías detectadas: {summary.get('spatial_anomalies_detected', 0)}")
            print(f"   Alta probabilidad: {summary.get('high_probability_anomalies', 0)}")
            print(f"   Firmas confirmadas: {summary.get('confirmed_archaeological_signatures', 0)}")
            print(f"   Probabilidad integrada: {summary.get('integrated_probability', 0):.3f}")
            print()
    
    # Validación académica
    validation = results.get('validation_metrics', {})
    if validation:
        academic = validation.get('academic_quality', {})
        if academic:
            print("🎓 CALIDAD ACADÉMICA:")
            print(f"   Rigor metodológico: {academic.get('methodological_rigor', 'N/A')}")
            print(f"   Consistencia: {academic.get('consistency_score', 0):.3f}")
            print(f"   Acuerdo entre capas: {academic.get('cross_layer_agreement', 0):.3f}")
            print(f"   Listo para publicación: {validation.get('academic_standards', {}).get('publication_ready', False)}")
            print()

if __name__ == "__main__":
    print("🏺 ArcheoScope - Test Valle del Indo: Sistemas Agrícolas")
    print("Iniciando análisis de la civilización del Indo...")
    print()
    
    results = test_indus_valley_agricultural_systems()
    
    if results:
        print("\n✅ Análisis del Valle del Indo completado exitosamente")
        print("🔍 Revisa los resultados arriba y el archivo JSON generado")
        print("🌾 Sistemas agrícolas de la civilización del Indo analizados")
    else:
        print("\n❌ Error en el análisis del Valle del Indo")
        sys.exit(1)