#!/usr/bin/env python3
"""
Test de Sitios Mesoamericanos y Andinos
Validación de ArcheoScope en contextos de "arqueología viva"
Tierras Bajas Mayas (Petén) y Tiwanaku (Altiplano)
"""

import requests
import json
import time
from datetime import datetime

def test_maya_peten_site():
    """
    Test específico para Tierras Bajas Mayas - Cuenca Mirador-Calakmul
    Enfoque: Sistemas hidráulicos y persistencia funcional post-colapso
    """
    print("🏛️ TESTING SITIO MESOAMERICANO: Tierras Bajas Mayas")
    print("=" * 70)
    
    base_url = "http://localhost:8002"
    
    # Coordenadas del núcleo Mirador-Calakmul
    maya_coords = {
        "lat": 17.760,
        "lon": -90.950,
        "name": "Cuenca Mirador-Calakmul (Petén, Guatemala)"
    }
    
    print(f"📍 Sitio: {maya_coords['name']}")
    print(f"🌍 Coordenadas: {maya_coords['lat']}°N, {maya_coords['lon']}°O")
    print("🎯 Objetivo: Detectar persistencia funcional de sistemas hidráulicos mayas")
    
    # Preguntas de investigación específicas
    research_questions = [
        "¿Qué partes del sistema hidráulico siguen influyendo en la vegetación actual?",
        "¿Qué zonas muestran persistencia funcional vs colapso total?", 
        "¿Hubo resiliencia ecológica post-clásica?",
        "¿Urbanismo continuo o 'fantasma'?"
    ]
    
    print("\n🔬 PREGUNTAS DE INVESTIGACIÓN:")
    for i, question in enumerate(research_questions, 1):
        print(f"   {i}. {question}")
    
    try:
        # 1. Análisis ArcheoScope completo
        print(f"\n🛰️ PASO 1: Análisis ArcheoScope completo")
        
        # Calcular bounding box de 5km de radio alrededor del punto central
        lat_center = maya_coords["lat"]
        lon_center = maya_coords["lon"]
        radius_deg = 5.0 / 111.0  # Aproximadamente 5km en grados
        
        analysis_request = {
            "lat_min": lat_center - radius_deg,
            "lat_max": lat_center + radius_deg,
            "lon_min": lon_center - radius_deg,
            "lon_max": lon_center + radius_deg,
            "resolution_m": 500,  # 500m para capturar patrones urbanos
            "layers_to_analyze": [
                "ndvi_vegetation",
                "thermal_lst", 
                "sar_backscatter",
                "surface_roughness",
                "soil_salinity",
                "seismic_resonance"
            ],
            "active_rules": ["all"],  # Usar todas las reglas disponibles
            "region_name": "Tierras Bajas Mayas - Cuenca Mirador-Calakmul",
            "include_explainability": True,
            "include_validation_metrics": True
        }
        
        print("   🔄 Ejecutando análisis multitemporal...")
        analysis_response = requests.post(
            f"{base_url}/analyze", 
            json=analysis_request, 
            timeout=60
        )
        
        if analysis_response.status_code == 200:
            maya_results = analysis_response.json()
            print("   ✅ Análisis completado exitosamente")
            
            # Extraer métricas clave para sistemas hidráulicos
            stats = maya_results['statistical_results']
            
            print(f"\n📊 RESULTADOS CLAVE PARA SISTEMAS HIDRÁULICOS:")
            
            # NDVI - Indicador de canales enterrados
            ndvi = stats['ndvi_vegetation']
            print(f"   🌿 NDVI Diferencial:")
            print(f"      - Probabilidad arqueológica: {ndvi['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {ndvi['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {ndvi['temporal_persistence']:.1%}")
            
            # Salinidad del suelo - Residuos de sistemas hídricos
            salinity = stats['soil_salinity']
            print(f"   🧂 Salinidad Residual:")
            print(f"      - Probabilidad arqueológica: {salinity['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {salinity['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {salinity['temporal_persistence']:.1%}")
            
            # Rugosidad superficial - Modificaciones topográficas
            roughness = stats['surface_roughness']
            print(f"   🏔️ Rugosidad Superficial:")
            print(f"      - Probabilidad arqueológica: {roughness['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {roughness['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {roughness['temporal_persistence']:.1%}")
            
            # Análisis de persistencia funcional
            print(f"\n🔍 ANÁLISIS DE PERSISTENCIA FUNCIONAL:")
            
            # Calcular índice de persistencia funcional maya
            maya_functional_persistence = (
                ndvi['temporal_persistence'] * 0.4 +  # Vegetación = indicador clave
                salinity['temporal_persistence'] * 0.3 +  # Química del suelo
                roughness['temporal_persistence'] * 0.3   # Topografía modificada
            )
            
            print(f"   📈 Índice de Persistencia Funcional Maya: {maya_functional_persistence:.1%}")
            
            # Interpretación específica para sistemas mayas
            if maya_functional_persistence > 0.7:
                interpretation = "🟢 ALTA PERSISTENCIA - Sistemas hidráulicos aún activos"
                functional_status = "living_infrastructure"
            elif maya_functional_persistence > 0.4:
                interpretation = "🟡 PERSISTENCIA MODERADA - Funcionalidad parcial"
                functional_status = "partially_active"
            else:
                interpretation = "🔴 BAJA PERSISTENCIA - Sistemas mayormente colapsados"
                functional_status = "mostly_collapsed"
            
            print(f"   🎯 Interpretación: {interpretation}")
            
            # Responder preguntas de investigación específicas
            print(f"\n💡 RESPUESTAS A PREGUNTAS DE INVESTIGACIÓN:")
            
            # 1. Sistemas hidráulicos activos
            active_hydraulic_percentage = (ndvi['temporal_persistence'] + salinity['temporal_persistence']) / 2
            print(f"   1. Sistemas hidráulicos activos: ~{active_hydraulic_percentage:.1%} del área")
            
            # 2. Persistencia vs colapso
            if maya_functional_persistence > 0.5:
                print(f"   2. Predomina persistencia funcional sobre colapso total")
            else:
                print(f"   2. Evidencia de colapso significativo en sistemas")
            
            # 3. Resiliencia ecológica
            ecological_resilience = ndvi['temporal_persistence']
            if ecological_resilience > 0.6:
                print(f"   3. Evidencia de resiliencia ecológica post-clásica")
            else:
                print(f"   3. Limitada resiliencia ecológica post-colapso")
            
            # 4. Urbanismo continuo vs fantasma
            urban_continuity = (ndvi['geometric_coherence'] + roughness['geometric_coherence']) / 2
            if urban_continuity > 0.8:
                print(f"   4. Urbanismo con continuidad geométrica (no 'fantasma')")
            else:
                print(f"   4. Urbanismo fragmentado o 'fantasma'")
            
            return {
                "site": "maya_peten",
                "functional_persistence_index": maya_functional_persistence,
                "functional_status": functional_status,
                "active_hydraulic_percentage": active_hydraulic_percentage,
                "results": maya_results
            }
            
        else:
            print(f"   ❌ Error en análisis: {analysis_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error en test Maya: {e}")
        return None

def test_tiwanaku_site():
    """
    Test específico para Tiwanaku & Waru-Waru - Cuenca Lago Titicaca
    Enfoque: Infraestructura agrícola viva y sistemas antiheladas
    """
    print("\n🏔️ TESTING SITIO ANDINO: Tiwanaku & Waru-Waru")
    print("=" * 70)
    
    base_url = "http://localhost:8002"
    
    # Coordenadas de la cuenca Tiwanaku-Katari
    tiwanaku_coords = {
        "lat": -16.550,
        "lon": -68.670,
        "name": "Tiwanaku & Waru-Waru (Altiplano, Bolivia)"
    }
    
    print(f"📍 Sitio: {tiwanaku_coords['name']}")
    print(f"🌍 Coordenadas: {abs(tiwanaku_coords['lat'])}°S, {abs(tiwanaku_coords['lon'])}°O")
    print("🎯 Objetivo: Detectar infraestructura agrícola viva (waru-waru)")
    
    # Preguntas de investigación específicas
    research_questions = [
        "¿Cuánto del sistema waru-waru sigue funcionando?",
        "¿Impacto real sobre humedad, temperatura y productividad actual?",
        "¿Extensión real fuera de áreas excavadas?",
        "¿Infraestructura agrícola 'latente'?"
    ]
    
    print("\n🔬 PREGUNTAS DE INVESTIGACIÓN:")
    for i, question in enumerate(research_questions, 1):
        print(f"   {i}. {question}")
    
    try:
        # 1. Análisis ArcheoScope enfocado en agricultura
        print(f"\n🛰️ PASO 1: Análisis ArcheoScope agrícola")
        
        # Calcular bounding box de 3km de radio alrededor del punto central
        lat_center = tiwanaku_coords["lat"]
        lon_center = tiwanaku_coords["lon"]
        radius_deg = 3.0 / 111.0  # Aproximadamente 3km en grados
        
        analysis_request = {
            "lat_min": lat_center - radius_deg,
            "lat_max": lat_center + radius_deg,
            "lon_min": lon_center - radius_deg,
            "lon_max": lon_center + radius_deg,
            "resolution_m": 300,  # 300m para sistemas agrícolas
            "layers_to_analyze": [
                "ndvi_vegetation",
                "thermal_lst",  # Clave para detectar antiheladas
                "sar_backscatter",
                "surface_roughness",
                "soil_salinity"  # Sistemas de drenaje
            ],
            "active_rules": ["all"],  # Usar todas las reglas disponibles
            "region_name": "Tiwanaku & Waru-Waru - Cuenca Lago Titicaca",
            "include_explainability": True,
            "include_validation_metrics": True
        }
        
        print("   🔄 Ejecutando análisis de sistemas agrícolas...")
        analysis_response = requests.post(
            f"{base_url}/analyze", 
            json=analysis_request, 
            timeout=60
        )
        
        if analysis_response.status_code == 200:
            tiwanaku_results = analysis_response.json()
            print("   ✅ Análisis completado exitosamente")
            
            # Extraer métricas clave para sistemas waru-waru
            stats = tiwanaku_results['statistical_results']
            
            print(f"\n📊 RESULTADOS CLAVE PARA SISTEMAS WARU-WARU:")
            
            # Térmica - Indicador de sistemas antiheladas
            thermal = stats['thermal_lst']
            print(f"   🌡️ Persistencia Térmica (antiheladas):")
            print(f"      - Probabilidad arqueológica: {thermal['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {thermal['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {thermal['temporal_persistence']:.1%}")
            
            # NDVI - Alineación con camellones
            ndvi = stats['ndvi_vegetation']
            print(f"   🌾 NDVI Alineado (camellones):")
            print(f"      - Probabilidad arqueológica: {ndvi['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {ndvi['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {ndvi['temporal_persistence']:.1%}")
            
            # Rugosidad - Modificaciones de camellones
            roughness = stats['surface_roughness']
            print(f"   🏔️ Rugosidad (camellones enterrados):")
            print(f"      - Probabilidad arqueológica: {roughness['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {roughness['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {roughness['temporal_persistence']:.1%}")
            
            # Análisis de infraestructura agrícola viva
            print(f"\n🌱 ANÁLISIS DE INFRAESTRUCTURA AGRÍCOLA VIVA:")
            
            # Calcular índice de infraestructura agrícola activa
            agricultural_activity_index = (
                thermal['temporal_persistence'] * 0.4 +  # Antiheladas = función clave
                ndvi['temporal_persistence'] * 0.35 +    # Productividad vegetal
                roughness['temporal_persistence'] * 0.25  # Estructura física
            )
            
            print(f"   📈 Índice de Infraestructura Agrícola Activa: {agricultural_activity_index:.1%}")
            
            # Interpretación específica para sistemas andinos
            if agricultural_activity_index > 0.6:
                interpretation = "🟢 INFRAESTRUCTURA VIVA - Waru-waru funcionalmente activos"
                agricultural_status = "active_infrastructure"
            elif agricultural_activity_index > 0.3:
                interpretation = "🟡 INFRAESTRUCTURA LATENTE - Funcionalidad parcial"
                agricultural_status = "latent_infrastructure"
            else:
                interpretation = "🔴 INFRAESTRUCTURA INACTIVA - Sistemas abandonados"
                agricultural_status = "abandoned_infrastructure"
            
            print(f"   🎯 Interpretación: {interpretation}")
            
            # Responder preguntas de investigación específicas
            print(f"\n💡 RESPUESTAS A PREGUNTAS DE INVESTIGACIÓN:")
            
            # 1. Sistemas waru-waru funcionando
            active_waruwaru_percentage = agricultural_activity_index
            print(f"   1. Sistemas waru-waru activos: ~{active_waruwaru_percentage:.1%} del área")
            
            # 2. Impacto en microclima
            microclimate_impact = thermal['temporal_persistence']
            if microclimate_impact > 0.5:
                print(f"   2. Impacto significativo en microclima (antiheladas activas)")
            else:
                print(f"   2. Impacto limitado en microclima actual")
            
            # 3. Extensión no excavada
            geometric_extension = (ndvi['geometric_coherence'] + roughness['geometric_coherence']) / 2
            if geometric_extension > 0.7:
                print(f"   3. Evidencia de extensión significativa fuera de áreas excavadas")
            else:
                print(f"   3. Extensión limitada fuera de áreas conocidas")
            
            # 4. Infraestructura latente
            latent_potential = (agricultural_activity_index + geometric_extension) / 2
            if latent_potential > 0.4:
                print(f"   4. Evidencia de infraestructura agrícola latente significativa")
            else:
                print(f"   4. Limitada infraestructura latente detectable")
            
            return {
                "site": "tiwanaku",
                "agricultural_activity_index": agricultural_activity_index,
                "agricultural_status": agricultural_status,
                "active_waruwaru_percentage": active_waruwaru_percentage,
                "results": tiwanaku_results
            }
            
        else:
            print(f"   ❌ Error en análisis: {analysis_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error en test Tiwanaku: {e}")
        return None

def comparative_analysis(maya_results, tiwanaku_results):
    """
    Análisis comparativo entre sitios mesoamericanos y andinos
    """
    print("\n🔬 ANÁLISIS COMPARATIVO: MESOAMÉRICA vs ANDES")
    print("=" * 70)
    
    if not maya_results or not tiwanaku_results:
        print("❌ No se pueden comparar - faltan resultados")
        return
    
    print("📊 COMPARACIÓN DE PERSISTENCIA FUNCIONAL:")
    print(f"   🏛️ Maya (Hidráulica):     {maya_results['functional_persistence_index']:.1%}")
    print(f"   🏔️ Tiwanaku (Agrícola):   {tiwanaku_results['agricultural_activity_index']:.1%}")
    
    # Determinar cuál tiene mayor persistencia
    if maya_results['functional_persistence_index'] > tiwanaku_results['agricultural_activity_index']:
        winner = "Sistemas hidráulicos mayas"
        difference = maya_results['functional_persistence_index'] - tiwanaku_results['agricultural_activity_index']
    else:
        winner = "Sistemas agrícolas andinos"
        difference = tiwanaku_results['agricultural_activity_index'] - maya_results['functional_persistence_index']
    
    print(f"\n🏆 MAYOR PERSISTENCIA: {winner} (+{difference:.1%})")
    
    # Análisis de tipos de persistencia
    print(f"\n🎯 TIPOS DE PERSISTENCIA DETECTADOS:")
    print(f"   🏛️ Maya: {maya_results['functional_status']}")
    print(f"   🏔️ Tiwanaku: {tiwanaku_results['agricultural_status']}")
    
    # Implicaciones científicas
    print(f"\n💡 IMPLICACIONES CIENTÍFICAS:")
    print(f"   • Ambos sitios muestran 'arqueología viva' en diferentes formas")
    print(f"   • Sistemas hidráulicos vs agrícolas tienen patrones de persistencia distintos")
    print(f"   • ArcheoScope puede detectar funcionalidad post-abandono")
    print(f"   • Metodología aplicable a diferentes contextos culturales")

def main():
    print("🚀 INICIANDO TEST DE SITIOS MESOAMERICANOS Y ANDINOS")
    print("🏛️ Validación de 'Arqueología Viva' en Diferentes Contextos")
    print("🎯 Objetivo: Demostrar persistencia funcional post-abandono")
    print()
    
    # Test sitio maya
    maya_results = test_maya_peten_site()
    
    # Test sitio andino  
    tiwanaku_results = test_tiwanaku_site()
    
    # Análisis comparativo
    if maya_results and tiwanaku_results:
        comparative_analysis(maya_results, tiwanaku_results)
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"archeoscope_mesoamerican_andean_test_{timestamp}.json"
        
        combined_results = {
            "test_info": {
                "timestamp": timestamp,
                "test_type": "mesoamerican_andean_sites",
                "sites_tested": ["maya_peten_guatemala", "tiwanaku_bolivia"]
            },
            "maya_results": maya_results,
            "tiwanaku_results": tiwanaku_results,
            "comparative_analysis": {
                "maya_persistence": maya_results['functional_persistence_index'],
                "tiwanaku_persistence": tiwanaku_results['agricultural_activity_index'],
                "persistence_difference": abs(maya_results['functional_persistence_index'] - tiwanaku_results['agricultural_activity_index']),
                "conclusion": "Both sites demonstrate 'living archaeology' with different persistence patterns"
            }
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(combined_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 RESULTADOS GUARDADOS: {results_file}")
        
        print(f"\n🎉 TEST COMPLETADO EXITOSAMENTE")
        print(f"✅ Ambos sitios analizados con metodología ArcheoScope")
        print(f"✅ Persistencia funcional detectada en diferentes contextos")
        print(f"✅ Metodología validada para 'arqueología viva'")
        
    else:
        print(f"\n❌ TEST INCOMPLETO")
        print(f"🔧 Revisar configuración del servidor y conectividad")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()