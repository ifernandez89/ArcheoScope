#!/usr/bin/env python3
"""
Análisis ArcheoScope de Angkor (Camboya)
Coordenadas: 13.4125, 103.8670
Objetivo: Separar infraestructura viva vs colapsada, detectar persistencia funcional
"""

import requests
import json

def analyze_angkor_with_archeoscope():
    print("🏛️ ANÁLISIS ARCHEOSCOPE - ANGKOR ARCHAEOLOGICAL PARK")
    print("=" * 80)
    
    # Coordenadas de Angkor del catálogo LIDAR
    lat = 13.4125
    lon = 103.8670
    offset = 0.0325  # Área ampliada para cubrir el complejo completo (~7km²)
    
    print(f"📍 Coordenadas centrales: {lat}, {lon}")
    print(f"🎯 Área de análisis: ±{offset}° (~7km² del complejo)")
    print(f"🛰️ LIDAR disponible: 2012-2015, múltiples campañas")
    print(f"🌿 Desafío: Separar infraestructura viva vs colapsada bajo selva")
    
    # Configuración específica para Angkor
    angkor_analysis = {
        "lat_min": lat - offset,
        "lat_max": lat + offset,
        "lon_min": lon - offset,
        "lon_max": lon + offset,
        "resolution_m": 10,  # Sentinel-2 para análisis temporal
        "region_name": "Angkor Archaeological Park - ArcheoScope Analysis",
        "include_explainability": True,
        "include_validation_metrics": True,
        
        # Configuración optimizada para Angkor
        "temporal_integration": {
            "enable_automatic": True,
            "years_range": "5-7",
            "seasonal_alignment": True,
            "exclusion_moderna": True,
            "target_years": [2017, 2019, 2020, 2022, 2023, 2024],  # 6 años
            "seasonal_window": "november-february",  # Estación seca
            "validation_mode": "reaffirm_or_discard"
        },
        
        "layers_to_analyze": [
            "ndvi_vegetation",      # Clave: detectar patrones bajo vegetación
            "thermal_lst",          # Estructuras de piedra vs agua/vegetación
            "sar_backscatter",      # Geometría bajo dosel forestal
            "surface_roughness",    # Canales, terrazas, estructuras
            "soil_salinity",        # Sistemas hidráulicos antiguos
            "seismic_resonance"     # Cavidades, túneles, estructuras huecas
        ],
        "active_rules": ["all"],
        "analysis_mode": "integrated_temporal_automatic_angkor"
    }
    
    print("\n🌊 OBJETIVOS ESPECÍFICOS PARA ANGKOR:")
    print("   • Detectar redes hidráulicas (canales, reservorios, terrazas)")
    print("   • Separar infraestructura funcional vs colapsada")
    print("   • Identificar urbanismo disperso bajo selva")
    print("   • Evaluar persistencia funcional de sistemas de agua")
    print("   • Distinguir estructuras activas vs abandonadas")
    
    print("\n⏳ ANÁLISIS TEMPORAL ESPECÍFICO:")
    print("   • Años: 2017-2024 (7 años)")
    print("   • Ventana: noviembre-febrero (estación seca)")
    print("   • Propósito: Detectar variaciones estacionales en sistemas hídricos")
    print("   • Exclusión moderna: Activada para filtrar infraestructura reciente")
    
    try:
        print("\n🔍 Ejecutando análisis ArcheoScope completo...")
        response = requests.post('http://localhost:8002/analyze', 
                               json=angkor_analysis, 
                               timeout=45)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Análisis ArcheoScope de Angkor completado")
            
            return data
            
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def print_detailed_analysis_results(data):
    """Imprimir resultados detallados del análisis de Angkor"""
    
    print("\n" + "="*80)
    print("🏛️ RESULTADOS DETALLADOS - ANÁLISIS ARCHEOSCOPE DE ANGKOR")
    print("="*80)
    
    # Información de la región
    region_info = data.get('region_info', {})
    print(f"\n📍 INFORMACIÓN DE LA REGIÓN:")
    print(f"   - Nombre: {region_info.get('name', 'N/A')}")
    print(f"   - Área analizada: {region_info.get('area_km2', 0):.2f} km²")
    print(f"   - Resolución: {region_info.get('resolution_m', 0)}m")
    print(f"   - Tipo de análisis: {region_info.get('analysis_type', 'N/A')}")
    
    # Resultados estadísticos (anomalías espaciales)
    statistical_results = data.get('statistical_results', {})
    print(f"\n📊 ANOMALÍAS ESPACIALES DETECTADAS:")
    
    for layer, results in statistical_results.items():
        if isinstance(results, dict):
            arch_prob = results.get('archaeological_probability', 0)
            geom_coherence = results.get('geometric_coherence', 0)
            temp_persistence = results.get('temporal_persistence', 0)
            spatial_anomalies = results.get('spatial_anomalies', {})
            
            print(f"\n   🔬 {layer.upper()}:")
            print(f"      - Probabilidad arqueológica: {arch_prob:.3f}")
            print(f"      - Coherencia geométrica: {geom_coherence:.3f}")
            print(f"      - Persistencia temporal: {temp_persistence:.3f}")
            
            if spatial_anomalies:
                anomaly_pixels = spatial_anomalies.get('anomaly_pixels', 0)
                anomaly_percentage = spatial_anomalies.get('anomaly_percentage', 0)
                mean_value = spatial_anomalies.get('mean_value', 0)
                
                print(f"      - Píxeles anómalos: {anomaly_pixels} ({anomaly_percentage:.2f}%)")
                print(f"      - Valor promedio: {mean_value:.3f}")
    
    # Análisis temporal integrado
    temporal_sensor = data.get('temporal_sensor_analysis', {})
    if temporal_sensor:
        print(f"\n⏳ ANÁLISIS TEMPORAL INTEGRADO:")
        print(f"   - Años analizados: {temporal_sensor.get('years_analyzed', [])}")
        print(f"   - Ventana estacional: {temporal_sensor.get('seasonal_window', 'N/A')}")
        print(f"   - Score de persistencia: {temporal_sensor.get('persistence_score', 0):.3f}")
        print(f"   - Estabilidad (CV): {temporal_sensor.get('cv_stability', 0):.3f}")
        print(f"   - Resultado de validación: {temporal_sensor.get('validation_result', 'N/A')}")
        print(f"   - Exclusión moderna aplicada: {'✅' if temporal_sensor.get('exclusion_moderna_applied') else '❌'}")
    
    # Análisis integrado
    integrated_analysis = data.get('integrated_analysis', {})
    if integrated_analysis:
        print(f"\n🔗 ANÁLISIS INTEGRADO:")
        print(f"   - Score básico: {integrated_analysis.get('basic_score', 0):.3f}")
        print(f"   - Score avanzado: {integrated_analysis.get('advanced_score', 0):.3f}")
        print(f"   - Score temporal: {integrated_analysis.get('temporal_score', 0):.3f}")
        print(f"   - Score exclusión moderna: {integrated_analysis.get('modern_exclusion_score', 0):.3f}")
        print(f"   - Score integrado final: {integrated_analysis.get('integrated_score', 0):.3f}")
        print(f"   - Clasificación: {integrated_analysis.get('classification', 'N/A')}")
        print(f"   - Validación temporal: {integrated_analysis.get('temporal_validation', 'N/A')}")
        print(f"   - Nivel de confianza: {integrated_analysis.get('confidence_level', 0):.3f}")
    
    # Explicaciones IA
    ai_explanations = data.get('ai_explanations', {})
    if ai_explanations:
        print(f"\n🤖 EXPLICACIONES IA ARQUEOLÓGICA:")
        print(f"   - IA disponible: {'✅' if ai_explanations.get('ai_available') else '❌'}")
        
        explanations = ai_explanations.get('explanations', {})
        for layer, explanation in explanations.items():
            if explanation:
                print(f"   - {layer}: {explanation}")
    
    # Reporte científico
    scientific_report = data.get('scientific_report', {})
    if scientific_report:
        print(f"\n📋 REPORTE CIENTÍFICO:")
        summary = scientific_report.get('summary', {})
        if summary:
            print(f"   - Anomalías totales detectadas: {summary.get('total_anomalies_detected', 0)}")
            print(f"   - Capas con evidencia arqueológica: {summary.get('layers_with_archaeological_evidence', 0)}")
            print(f"   - Nivel de confianza general: {summary.get('overall_confidence_level', 'N/A')}")
            print(f"   - Recomendación: {summary.get('recommendation', 'N/A')}")
    
    # Estado del sistema
    system_status = data.get('system_status', {})
    if system_status:
        print(f"\n⚙️ ESTADO DEL SISTEMA:")
        print(f"   - Análisis completado: {'✅' if system_status.get('analysis_completed') else '❌'}")
        print(f"   - Tiempo de procesamiento: {system_status.get('processing_time_seconds', 'N/A')} segundos")
        print(f"   - IA utilizada: {'✅' if system_status.get('ai_used') else '❌'}")
        print(f"   - Reglas evaluadas: {system_status.get('rules_evaluated', 0)}")
        print(f"   - Anomalías detectadas: {system_status.get('anomalies_detected', 0)}")

def interpret_angkor_results(data):
    """Interpretación específica para Angkor"""
    
    print(f"\n" + "="*80)
    print("🌊 INTERPRETACIÓN ESPECÍFICA PARA ANGKOR")
    print("="*80)
    
    statistical_results = data.get('statistical_results', {})
    temporal_sensor = data.get('temporal_sensor_analysis', {})
    integrated_analysis = data.get('integrated_analysis', {})
    
    print(f"\n🏛️ ANÁLISIS DE INFRAESTRUCTURA HIDRÁULICA:")
    
    # Análisis de NDVI (vegetación - clave para detectar canales)
    ndvi_results = statistical_results.get('ndvi_vegetation', {})
    if ndvi_results:
        ndvi_prob = ndvi_results.get('archaeological_probability', 0)
        ndvi_persistence = ndvi_results.get('temporal_persistence', 0)
        
        print(f"   🌱 VEGETACIÓN (Canales y terrazas):")
        print(f"      - Probabilidad arqueológica: {ndvi_prob:.3f}")
        print(f"      - Persistencia temporal: {ndvi_persistence:.3f}")
        
        if ndvi_prob > 0.6 and ndvi_persistence > 0.7:
            print(f"      ✅ FUERTE evidencia de canales/terrazas bajo vegetación")
        elif ndvi_prob > 0.4:
            print(f"      🟡 MODERADA evidencia de modificación del paisaje")
        else:
            print(f"      ❌ Baja evidencia de estructuras bajo vegetación")
    
    # Análisis térmico (estructuras de piedra vs agua)
    thermal_results = statistical_results.get('thermal_lst', {})
    if thermal_results:
        thermal_prob = thermal_results.get('archaeological_probability', 0)
        thermal_coherence = thermal_results.get('geometric_coherence', 0)
        
        print(f"\n   🌡️ TÉRMICO (Estructuras de piedra vs agua):")
        print(f"      - Probabilidad arqueológica: {thermal_prob:.3f}")
        print(f"      - Coherencia geométrica: {thermal_coherence:.3f}")
        
        if thermal_prob > 0.5 and thermal_coherence > 0.7:
            print(f"      ✅ DETECTADAS estructuras de piedra con geometría coherente")
        elif thermal_prob > 0.3:
            print(f"      🟡 Posibles estructuras térmicamente diferenciadas")
        else:
            print(f"      ❌ Sin evidencia térmica clara de estructuras")
    
    # Análisis SAR (geometría bajo dosel)
    sar_results = statistical_results.get('sar_backscatter', {})
    if sar_results:
        sar_prob = sar_results.get('archaeological_probability', 0)
        sar_coherence = sar_results.get('geometric_coherence', 0)
        
        print(f"\n   📡 SAR (Geometría bajo dosel forestal):")
        print(f"      - Probabilidad arqueológica: {sar_prob:.3f}")
        print(f"      - Coherencia geométrica: {sar_coherence:.3f}")
        
        if sar_prob > 0.6 and sar_coherence > 0.8:
            print(f"      ✅ EXCELENTE penetración: estructuras geométricas bajo selva")
        elif sar_prob > 0.4:
            print(f"      🟡 Estructuras parcialmente detectadas bajo vegetación")
        else:
            print(f"      ❌ Limitada penetración del dosel forestal")
    
    # Análisis de salinidad (sistemas hidráulicos)
    salinity_results = statistical_results.get('soil_salinity', {})
    if salinity_results:
        salinity_prob = salinity_results.get('archaeological_probability', 0)
        salinity_persistence = salinity_results.get('temporal_persistence', 0)
        
        print(f"\n   🧂 SALINIDAD (Sistemas hidráulicos antiguos):")
        print(f"      - Probabilidad arqueológica: {salinity_prob:.3f}")
        print(f"      - Persistencia temporal: {salinity_persistence:.3f}")
        
        if salinity_prob > 0.5 and salinity_persistence > 0.6:
            print(f"      ✅ DETECTADOS patrones de drenaje/irrigación antiguos")
        elif salinity_prob > 0.3:
            print(f"      🟡 Posibles trazas de sistemas hídricos")
        else:
            print(f"      ❌ Sin evidencia clara de sistemas hidráulicos")
    
    # Evaluación de persistencia funcional
    print(f"\n🔄 EVALUACIÓN DE PERSISTENCIA FUNCIONAL:")
    
    if temporal_sensor:
        persistence_score = temporal_sensor.get('persistence_score', 0)
        cv_stability = temporal_sensor.get('cv_stability', 1.0)
        validation_result = temporal_sensor.get('validation_result', '')
        
        print(f"   - Score de persistencia: {persistence_score:.3f}")
        print(f"   - Estabilidad temporal: {cv_stability:.3f}")
        print(f"   - Resultado: {validation_result}")
        
        if persistence_score > 0.7 and cv_stability < 0.2:
            print(f"   ✅ INFRAESTRUCTURA FUNCIONALMENTE PERSISTENTE")
            print(f"      → Sistemas hídricos probablemente aún activos")
        elif persistence_score > 0.4:
            print(f"   🟡 INFRAESTRUCTURA PARCIALMENTE FUNCIONAL")
            print(f"      → Algunos sistemas pueden estar activos")
        else:
            print(f"   ❌ INFRAESTRUCTURA MAYORMENTE COLAPSADA")
            print(f"      → Sistemas probablemente abandonados")
    
    # Síntesis final
    print(f"\n🎯 SÍNTESIS PARA ANGKOR:")
    
    if integrated_analysis:
        integrated_score = integrated_analysis.get('integrated_score', 0)
        classification = integrated_analysis.get('classification', '')
        
        print(f"   - Score integrado: {integrated_score:.3f}")
        print(f"   - Clasificación: {classification}")
        
        if integrated_score > 0.7:
            print(f"\n   🏆 RESULTADO EXCEPCIONAL:")
            print(f"      ✅ ArcheoScope detecta infraestructura hidráulica compleja")
            print(f"      ✅ Separación exitosa de sistemas vivos vs colapsados")
            print(f"      ✅ Urbanismo disperso identificado bajo selva")
            print(f"      → POTENCIA SIGNIFICATIVAMENTE los datos LIDAR existentes")
        elif integrated_score > 0.5:
            print(f"\n   🎯 RESULTADO POSITIVO:")
            print(f"      ✅ Evidencia clara de infraestructura arqueológica")
            print(f"      🟡 Separación parcial de sistemas funcionales")
            print(f"      → COMPLEMENTA efectivamente los datos LIDAR")
        else:
            print(f"\n   ⚠️ RESULTADO LIMITADO:")
            print(f"      🟡 Evidencia arqueológica detectada pero débil")
            print(f"      → Requiere refinamiento de parámetros")

def main():
    print("🚀 INICIANDO ANÁLISIS ARCHEOSCOPE DE ANGKOR")
    print("🎯 Objetivo: Potenciar datos LIDAR con análisis temporal y espectral")
    print()
    
    # Ejecutar análisis
    results = analyze_angkor_with_archeoscope()
    
    if results:
        # Imprimir resultados detallados
        print_detailed_analysis_results(results)
        
        # Interpretación específica para Angkor
        interpret_angkor_results(results)
        
        # Guardar resultados
        output_filename = f"angkor_archeoscope_analysis_complete.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Resultados completos guardados en: {output_filename}")
        
    else:
        print("\n❌ ANÁLISIS FALLÓ")
        print("🔧 Verificar que el servidor ArcheoScope esté ejecutándose")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()