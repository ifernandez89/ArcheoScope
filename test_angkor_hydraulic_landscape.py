#!/usr/bin/env python3
"""
Test específico: Análisis del paisaje hidráulico de Angkor (Camboya)
Zona NO monumental - infraestructura periférica (canales, reservorios, campos)

Coordenadas: 13.44 N, 103.86 E
Área: 5-10 km² excluyendo templos visibles
"""

import requests
import json
from datetime import datetime
import sys

def test_angkor_hydraulic_analysis():
    """
    Ejecutar análisis del sistema hidráulico periférico de Angkor.
    
    Enfoque: Detectar canales antiguos, reservorios, y campos agrícolas
    que NO son los templos famosos sino la infraestructura de soporte.
    """
    
    # URL del backend
    backend_url = "http://localhost:8004"
    
    print("🏺 ARCHEOSCOPE - Análisis Paisaje Hidráulico Angkor")
    print("=" * 60)
    print(f"📍 Sitio: Angkor (Camboya) - Zona NO monumental")
    print(f"🎯 Objetivo: Paisaje hidráulico periférico")
    print(f"📌 Coordenadas: 13.44 N, 103.86 E")
    print(f"📏 Área: ~7 km² (excluyendo templos visibles)")
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
            print()
        else:
            print(f"⚠️ Estado del sistema: {status_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return None
    
    # Configurar análisis específico para paisaje hidráulico
    analysis_request = {
        "lat_min": 13.435,  # Zona periférica norte
        "lat_max": 13.445,  # ~1.1 km norte-sur
        "lon_min": 103.855, # Zona periférica oeste  
        "lon_max": 103.865, # ~1.1 km este-oeste
        
        "resolution_m": 500,  # Resolución media para captar infraestructura
        
        # Capas específicas para detectar sistemas hidráulicos antiguos
        "layers_to_analyze": [
            "ndvi_vegetation",      # Diferencias vegetación por humedad
            "thermal_lst",          # Firmas térmicas de canales/reservorios
            "sar_backscatter",      # Geometría lineal de canales
            "surface_roughness",    # Topografía sutil de terraplenes
            "soil_salinity",        # Indicadores de manejo hídrico
            "seismic_resonance"     # Estructuras enterradas
        ],
        
        # Reglas arqueológicas específicas
        "active_rules": [
            "linear_anthropogenic_structures",    # Canales lineales
            "geometric_field_systems",           # Campos organizados
            "water_management_infrastructure",   # Sistemas hídricos
            "agricultural_terracing",            # Terrazas agrícolas
            "settlement_periphery_patterns"      # Patrones periféricos
        ],
        
        "region_name": "Angkor Hydraulic Landscape (Non-Monumental)",
        "include_explainability": True,   # Explicación científica detallada
        "include_validation_metrics": True  # Métricas de validación
    }
    
    print("🚀 Iniciando análisis del paisaje hidráulico...")
    print(f"📊 Capas a analizar: {len(analysis_request['layers_to_analyze'])}")
    print(f"🔬 Reglas activas: {len(analysis_request['active_rules'])}")
    print()
    
    try:
        # Ejecutar análisis principal
        print("⏳ Ejecutando análisis arqueológico...")
        
        analysis_response = requests.post(
            f"{backend_url}/analyze", 
            json=analysis_request,
            timeout=60
        )
        
        if analysis_response.status_code == 200:
            results = analysis_response.json()
            
            print("✅ Análisis completado exitosamente")
            print()
            
            # Mostrar resultados clave
            display_angkor_results(results)
            
            # Guardar resultados completos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"angkor_hydraulic_analysis_{timestamp}.json"
            
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

def display_angkor_results(results):
    """Mostrar resultados del análisis de Angkor de forma estructurada."""
    
    print("🏺 RESULTADOS - PAISAJE HIDRÁULICO ANGKOR")
    print("=" * 50)
    
    # Información de la región
    region_info = results.get('region_info', {})
    print(f"📍 Región: {region_info.get('name', 'Angkor Hydraulic')}")
    print(f"📏 Área: {region_info.get('area_km2', 'N/A')} km²")
    print(f"🎯 Resolución: {region_info.get('resolution_m', 'N/A')} m")
    print()
    
    # Resultados estadísticos
    stats = results.get('statistical_results', {})
    if stats:
        print("📊 ANÁLISIS ESTADÍSTICO:")
        print(f"   Anomalías detectadas: {stats.get('total_anomalies', 0)}")
        print(f"   Confianza promedio: {stats.get('average_confidence', 0):.3f}")
        print(f"   Cobertura espacial: {stats.get('spatial_coverage', 0):.1%}")
        print()
    
    # Resultados arqueológicos (renombrado de physics_results)
    archaeological = results.get('physics_results', {})
    if archaeological:
        print("🏛️ EVALUACIÓN ARQUEOLÓGICA:")
        
        evaluations = archaeological.get('evaluations', {})
        for rule_name, evaluation in evaluations.items():
            prob = evaluation.get('archaeological_probability', 0)
            confidence = evaluation.get('confidence', 0)
            
            if prob > 0.3:  # Solo mostrar probabilidades significativas
                print(f"   {rule_name}:")
                print(f"     Probabilidad: {prob:.3f}")
                print(f"     Confianza: {confidence:.3f}")
        
        # Score integrado
        integrated = archaeological.get('integrated_analysis', {})
        if integrated:
            print(f"\n🎯 SCORE INTEGRADO: {integrated.get('integrated_score', 0):.3f}")
            print(f"   Clasificación: {integrated.get('classification', 'N/A')}")
            print(f"   Explicación: {integrated.get('explanation', 'N/A')}")
        print()
    
    # Interpretaciones de IA
    ai_explanations = results.get('ai_explanations', {})
    if ai_explanations:
        print("🤖 INTERPRETACIÓN IA:")
        
        interpretation = ai_explanations.get('interpretation', '')
        if interpretation:
            print(f"   {interpretation}")
        
        archaeological_significance = ai_explanations.get('archaeological_significance', '')
        if archaeological_significance:
            print(f"   Significado: {archaeological_significance}")
        print()
    
    # Mapa de anomalías
    anomaly_map = results.get('anomaly_map', {})
    if anomaly_map:
        print("🗺️ MAPA DE ANOMALÍAS:")
        
        hotspots = anomaly_map.get('hotspots', [])
        print(f"   Puntos calientes detectados: {len(hotspots)}")
        
        for i, hotspot in enumerate(hotspots[:3]):  # Mostrar top 3
            intensity = hotspot.get('intensity', 0)
            coords = hotspot.get('coordinates', [])
            print(f"   Hotspot {i+1}: Intensidad {intensity:.3f} en {coords}")
        print()
    
    # Reporte científico
    scientific = results.get('scientific_report', {})
    if scientific:
        print("🔬 REPORTE CIENTÍFICO:")
        
        methodology = scientific.get('methodology', '')
        if methodology:
            print(f"   Metodología: {methodology}")
        
        conclusions = scientific.get('conclusions', [])
        if conclusions:
            print("   Conclusiones:")
            for conclusion in conclusions[:2]:  # Top 2 conclusiones
                print(f"     • {conclusion}")
        print()
    
    # Explicabilidad (si está disponible)
    explainability = results.get('explainability_analysis', {})
    if explainability:
        print("📋 EXPLICABILIDAD CIENTÍFICA:")
        
        explanations = explainability.get('explanations', [])
        print(f"   Explicaciones generadas: {len(explanations)}")
        
        for exp in explanations[:2]:  # Mostrar primeras 2
            anomaly_id = exp.get('anomaly_id', 'N/A')
            prob = exp.get('archaeological_probability', 0)
            explanation = exp.get('explanation', '')
            
            print(f"   {anomaly_id}: P={prob:.3f}")
            print(f"     {explanation[:100]}...")
        print()
    
    # Estado del sistema
    system_status = results.get('system_status', {})
    if system_status:
        print("⚙️ ESTADO DEL SISTEMA:")
        print(f"   Procesamiento: {system_status.get('processing_time', 'N/A')}")
        print(f"   Módulos activos: {system_status.get('active_modules', 'N/A')}")
        print()

if __name__ == "__main__":
    print("🏺 ArcheoScope - Test Paisaje Hidráulico Angkor")
    print("Iniciando análisis...")
    print()
    
    results = test_angkor_hydraulic_analysis()
    
    if results:
        print("\n✅ Análisis completado exitosamente")
        print("🔍 Revisa los resultados arriba y el archivo JSON generado")
    else:
        print("\n❌ Error en el análisis")
        sys.exit(1)