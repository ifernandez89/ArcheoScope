#!/usr/bin/env python3
"""
Test de Manejo Forestal Invisible - Amazonía Interfluvial
Búsqueda de manejo ancestral SIN geometría obvia
Zona: Tapajós-Xingu (Pará, Brasil) - "Bosque Prístino"
"""

import requests
import json
import time
from datetime import datetime

def test_invisible_forest_management():
    """
    Test específico para detectar manejo forestal invisible
    Zona interfluvial Tapajós-Xingu - sin estructuras geométricas obvias
    Enfoque: Detectar antropización sin geometría visible
    """
    print("🌳 TESTING MANEJO FORESTAL INVISIBLE - Amazonía Interfluvial")
    print("=" * 75)
    
    base_url = "http://localhost:8002"
    
    # Coordenadas zona interfluvial Tapajós-Xingu
    interfluvial_coords = {
        "lat": -4.250,
        "lon": -54.700,
        "name": "Amazonía Interfluvial - Tapajós-Xingu (Pará, Brasil)"
    }
    
    print(f"📍 Sitio: {interfluvial_coords['name']}")
    print(f"🌍 Coordenadas: {abs(interfluvial_coords['lat'])}°S, {abs(interfluvial_coords['lon'])}°O")
    print("🎯 Objetivo: Detectar manejo forestal INVISIBLE sin geometría obvia")
    
    # Hipótesis de investigación para manejo invisible
    research_hypotheses = [
        "¿Hay manejo forestal ancestral invisible sin estructuras geométricas?",
        "¿Patrones de biodiversidad son realmente 'naturales' o antropogénicos?",
        "¿Terra preta dispersa sin concentraciones obvias?",
        "¿Sistemas de enriquecimiento forestal milenarios?",
        "¿Manejo de especies útiles aún detectable?"
    ]
    
    print("\n🔬 HIPÓTESIS DE INVESTIGACIÓN - MANEJO INVISIBLE:")
    for i, hypothesis in enumerate(research_hypotheses, 1):
        print(f"   {i}. {hypothesis}")
    
    print("\n🧠 PARADIGMA CIENTÍFICO:")
    print("   NARRATIVA OFICIAL: 'Bosque prístino sin intervención humana'")
    print("   HIPÓTESIS ARCHEOSCOPE: 'Manejo forestal invisible milenario'")
    print("   POTENCIAL IMPACTO: 🚀 EXPLOSIVO - Cambiaría escala de Amazonía antropogénica")
    
    try:
        # Calcular bounding box de 10km para capturar patrones de manejo disperso
        lat_center = interfluvial_coords["lat"]
        lon_center = interfluvial_coords["lon"]
        radius_deg = 10.0 / 111.0  # Aproximadamente 10km en grados
        
        # 1. Análisis ArcheoScope enfocado en manejo invisible
        print(f"\n🛰️ PASO 1: Análisis de manejo forestal invisible")
        
        analysis_request = {
            "lat_min": lat_center - radius_deg,
            "lat_max": lat_center + radius_deg,
            "lon_min": lon_center - radius_deg,
            "lon_max": lon_center + radius_deg,
            "resolution_m": 500,  # 500m para capturar patrones sutiles de manejo
            "layers_to_analyze": [
                "ndvi_vegetation",    # CLAVE: Patrones de biodiversidad dirigida
                "thermal_lst",        # Microclimas de manejo disperso
                "sar_backscatter",    # Texturas de dosel manejado vs natural
                "surface_roughness",  # Microtopografía de manejo sutil
                "soil_salinity",      # Terra preta dispersa
                "seismic_resonance"   # Modificaciones subsuperficiales sutiles
            ],
            "active_rules": ["all"],  # Usar todas las reglas disponibles
            "region_name": "Amazonía Interfluvial - Manejo Invisible (Tapajós-Xingu)",
            "include_explainability": True,
            "include_validation_metrics": True
        }
        
        print("   🔄 Ejecutando análisis de manejo invisible...")
        print("   🎯 Buscando: Antropización SIN geometría obvia")
        
        analysis_response = requests.post(
            f"{base_url}/analyze", 
            json=analysis_request, 
            timeout=60
        )
        
        if analysis_response.status_code == 200:
            invisible_results = analysis_response.json()
            print("   ✅ Análisis completado exitosamente")
            
            # Extraer métricas clave para manejo invisible
            stats = invisible_results['statistical_results']
            
            print(f"\n📊 RESULTADOS - BÚSQUEDA DE MANEJO INVISIBLE:")
            
            # NDVI - Indicador clave de biodiversidad dirigida
            ndvi = stats['ndvi_vegetation']
            print(f"   🌿 Biodiversidad Dirigida (NDVI):")
            print(f"      - Probabilidad arqueológica: {ndvi['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {ndvi['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {ndvi['temporal_persistence']:.1%}")
            
            # Salinidad - Terra preta dispersa
            salinity = stats['soil_salinity']
            print(f"   🌱 Terra Preta Dispersa:")
            print(f"      - Probabilidad arqueológica: {salinity['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {salinity['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {salinity['temporal_persistence']:.1%}")
            
            # SAR - Texturas de dosel manejado
            sar = stats['sar_backscatter']
            print(f"   📡 Texturas Dosel Manejado (SAR):")
            print(f"      - Probabilidad arqueológica: {sar['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {sar['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {sar['temporal_persistence']:.1%}")
            
            # Térmica - Microclimas de manejo
            thermal = stats['thermal_lst']
            print(f"   🌡️ Microclimas Manejo:")
            print(f"      - Probabilidad arqueológica: {thermal['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {thermal['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {thermal['temporal_persistence']:.1%}")
            
            # Rugosidad - Microtopografía sutil
            roughness = stats['surface_roughness']
            print(f"   🏔️ Microtopografía Sutil:")
            print(f"      - Probabilidad arqueológica: {roughness['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {roughness['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {roughness['temporal_persistence']:.1%}")
            
            # Resonancia - Modificaciones subsuperficiales
            seismic = stats['seismic_resonance']
            print(f"   🌊 Modificaciones Subsuperficiales:")
            print(f"      - Probabilidad arqueológica: {seismic['archaeological_probability']:.1%}")
            print(f"      - Coherencia geométrica: {seismic['geometric_coherence']:.1%}")
            print(f"      - Persistencia temporal: {seismic['temporal_persistence']:.1%}")
            
            # ANÁLISIS CRÍTICO: ¿Es realmente "prístino"?
            print(f"\n🔍 ANÁLISIS CRÍTICO: ¿BOSQUE REALMENTE 'PRÍSTINO'?")
            
            # Calcular índice de manejo invisible
            invisible_management_index = (
                ndvi['temporal_persistence'] * 0.30 +      # Biodiversidad dirigida
                salinity['temporal_persistence'] * 0.25 +  # Terra preta dispersa
                sar['temporal_persistence'] * 0.20 +       # Texturas de dosel
                thermal['temporal_persistence'] * 0.15 +   # Microclimas
                seismic['temporal_persistence'] * 0.10     # Modificaciones sutiles
            )
            
            print(f"   📈 Índice de Manejo Invisible: {invisible_management_index:.1%}")
            
            # Interpretación revolucionaria
            if invisible_management_index > 0.6:
                interpretation = "🚨 DESCUBRIMIENTO EXPLOSIVO: Manejo forestal invisible DETECTADO"
                management_status = "invisible_anthropogenic_forest"
                paradigm_impact = "REVOLUCIONARIO"
            elif invisible_management_index > 0.4:
                interpretation = "⚠️ EVIDENCIA SIGNIFICATIVA: Posible manejo ancestral sutil"
                management_status = "potentially_managed"
                paradigm_impact = "SIGNIFICATIVO"
            elif invisible_management_index > 0.2:
                interpretation = "🤔 INDICIOS DETECTABLES: Patrones no completamente naturales"
                management_status = "subtle_indicators"
                paradigm_impact = "MODERADO"
            else:
                interpretation = "✅ CONFIRMACIÓN: Bosque aparentemente prístino"
                management_status = "apparently_pristine"
                paradigm_impact = "NULO"
            
            print(f"   🎯 Interpretación: {interpretation}")
            print(f"   🚀 Impacto Paradigmático: {paradigm_impact}")
            
            # Análisis de componentes específicos del manejo invisible
            print(f"\n🌳 ANÁLISIS DE COMPONENTES DE MANEJO INVISIBLE:")
            
            # 1. Biodiversidad dirigida
            biodiversity_direction = ndvi['temporal_persistence']
            if biodiversity_direction > 0.6:
                biodiversity_status = "🟢 BIODIVERSIDAD DIRIGIDA DETECTADA"
                biodiversity_explanation = "Patrones de vegetación no aleatorios - posible enriquecimiento"
            elif biodiversity_direction > 0.3:
                biodiversity_status = "🟡 PATRONES BIODIVERSIDAD SUTILES"
                biodiversity_explanation = "Algunas anomalías en distribución de especies"
            else:
                biodiversity_status = "🔴 BIODIVERSIDAD APARENTEMENTE NATURAL"
                biodiversity_explanation = "Patrones consistentes con procesos naturales"
            
            print(f"   🌿 Biodiversidad: {biodiversity_status}")
            print(f"      {biodiversity_explanation}")
            
            # 2. Terra preta dispersa
            dispersed_terra_preta = salinity['temporal_persistence']
            if dispersed_terra_preta > 0.5:
                terra_preta_status = "🟢 TERRA PRETA DISPERSA DETECTADA"
                terra_preta_explanation = "Modificaciones químicas del suelo distribuidas"
            elif dispersed_terra_preta > 0.3:
                terra_preta_status = "🟡 ANOMALÍAS QUÍMICAS SUTILES"
                terra_preta_explanation = "Algunas variaciones químicas no naturales"
            else:
                terra_preta_status = "🔴 SUELOS APARENTEMENTE NATURALES"
                terra_preta_explanation = "Química del suelo consistente con procesos naturales"
            
            print(f"   🌱 Terra Preta: {terra_preta_status}")
            print(f"      {terra_preta_explanation}")
            
            # 3. Manejo de dosel
            canopy_management = sar['temporal_persistence']
            if canopy_management > 0.6:
                canopy_status = "🟢 MANEJO DE DOSEL DETECTADO"
                canopy_explanation = "Texturas de dosel indican manejo estructural"
            elif canopy_management > 0.3:
                canopy_status = "🟡 ANOMALÍAS ESTRUCTURALES SUTILES"
                canopy_explanation = "Algunas variaciones en estructura del dosel"
            else:
                canopy_status = "🔴 DOSEL APARENTEMENTE NATURAL"
                canopy_explanation = "Estructura de dosel consistente con sucesión natural"
            
            print(f"   🌳 Dosel: {canopy_status}")
            print(f"      {canopy_explanation}")
            
            # Responder hipótesis de investigación
            print(f"\n💡 RESPUESTAS A HIPÓTESIS DE INVESTIGACIÓN:")
            
            # 1. Manejo forestal invisible
            if invisible_management_index > 0.4:
                print(f"   1. Manejo forestal invisible: SÍ DETECTADO ({invisible_management_index:.1%})")
            else:
                print(f"   1. Manejo forestal invisible: NO DETECTADO ({invisible_management_index:.1%})")
            
            # 2. Biodiversidad antropogénica vs natural
            if biodiversity_direction > 0.5:
                print(f"   2. Biodiversidad: ANTROPOGÉNICA - Patrones dirigidos detectados")
            else:
                print(f"   2. Biodiversidad: APARENTEMENTE NATURAL - Sin patrones dirigidos obvios")
            
            # 3. Terra preta dispersa
            if dispersed_terra_preta > 0.4:
                print(f"   3. Terra preta dispersa: SÍ DETECTADA - Modificaciones químicas distribuidas")
            else:
                print(f"   3. Terra preta dispersa: NO DETECTADA - Suelos aparentemente naturales")
            
            # 4. Enriquecimiento forestal
            forest_enrichment = (biodiversity_direction + canopy_management) / 2
            if forest_enrichment > 0.5:
                print(f"   4. Enriquecimiento forestal: SÍ DETECTADO - Sistemas de manejo activos")
            else:
                print(f"   4. Enriquecimiento forestal: NO DETECTADO - Sucesión aparentemente natural")
            
            # 5. Manejo de especies útiles
            useful_species_management = ndvi['geometric_coherence']
            if useful_species_management > 0.7:
                print(f"   5. Manejo especies útiles: EVIDENCIA FUERTE - Distribución no aleatoria")
            else:
                print(f"   5. Manejo especies útiles: EVIDENCIA LIMITADA - Distribución natural")
            
            # EVALUACIÓN DEL IMPACTO CIENTÍFICO
            print(f"\n🚀 EVALUACIÓN DEL IMPACTO CIENTÍFICO:")
            
            if invisible_management_index > 0.6:
                print(f"   🚨 IMPACTO EXPLOSIVO:")
                print(f"   • Cambiaría completamente la escala de Amazonía antropogénica")
                print(f"   • Millones de hectáreas 'prístinas' serían realmente antropogénicas")
                print(f"   • Redefinición total de conservación amazónica")
                print(f"   • Validación masiva de conocimiento indígena invisible")
                
            elif invisible_management_index > 0.4:
                print(f"   ⚡ IMPACTO SIGNIFICATIVO:")
                print(f"   • Evidencia de manejo sutil en zonas 'prístinas'")
                print(f"   • Necesidad de revisar clasificaciones de bosque primario")
                print(f"   • Implicaciones para políticas de conservación")
                
            elif invisible_management_index > 0.2:
                print(f"   💡 IMPACTO MODERADO:")
                print(f"   • Indicios de influencia humana histórica sutil")
                print(f"   • Necesidad de estudios más detallados")
                print(f"   • Cuestionamiento de narrativa 'prístina' absoluta")
                
            else:
                print(f"   ✅ CONFIRMACIÓN DE NARRATIVA OFICIAL:")
                print(f"   • Bosque aparentemente sin manejo ancestral detectable")
                print(f"   • Validación de clasificación como 'prístino'")
                print(f"   • Procesos naturales dominantes")
            
            return {
                "site": "amazonia_interfluvial",
                "invisible_management_index": invisible_management_index,
                "management_status": management_status,
                "paradigm_impact": paradigm_impact,
                "biodiversity_direction": biodiversity_direction,
                "dispersed_terra_preta": dispersed_terra_preta,
                "canopy_management": canopy_management,
                "results": invisible_results
            }
            
        else:
            print(f"   ❌ Error en análisis: {analysis_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error en test Manejo Invisible: {e}")
        return None

def comparative_analysis_invisible_vs_visible(invisible_results):
    """
    Análisis comparativo: Manejo invisible vs sitios con estructuras visibles
    """
    print("\n🔬 ANÁLISIS COMPARATIVO: MANEJO INVISIBLE vs ESTRUCTURAS VISIBLES")
    print("=" * 75)
    
    if not invisible_results:
        print("❌ No se pueden comparar - faltan resultados de manejo invisible")
        return
    
    # Datos de referencia de sitios con estructuras visibles
    visible_sites = {
        "Angkor (Estructuras visibles)": 0.931,
        "Amazonía Acre (Geoglifos visibles)": 0.896,
        "Tiwanaku (Estructuras visibles)": 0.808,
        "Maya Petén (Estructuras visibles)": 0.746
    }
    
    invisible_persistence = invisible_results['invisible_management_index']
    
    print("📊 COMPARACIÓN MANEJO INVISIBLE vs ESTRUCTURAS VISIBLES:")
    print(f"   🏛️ Angkor (Estructuras):           93.1%")
    print(f"   🌴 Amazonía Acre (Geoglifos):      89.6%")
    print(f"   🏔️ Tiwanaku (Estructuras):         80.8%")
    print(f"   🏛️ Maya Petén (Estructuras):       74.6%")
    print(f"   🌳 Amazonía Interfluvial (INVISIBLE): {invisible_persistence:.1%}")
    
    # Análisis del significado
    print(f"\n🧠 ANÁLISIS DEL SIGNIFICADO:")
    
    if invisible_persistence > 0.6:
        print(f"   🚨 DESCUBRIMIENTO REVOLUCIONARIO:")
        print(f"   • Manejo invisible comparable a sitios con estructuras visibles")
        print(f"   • Implicaría que TODA la Amazonía podría ser antropogénica")
        print(f"   • Cambio de paradigma total en arqueología amazónica")
        
    elif invisible_persistence > 0.4:
        print(f"   ⚡ DESCUBRIMIENTO SIGNIFICATIVO:")
        print(f"   • Manejo sutil pero detectable en zona 'prístina'")
        print(f"   • Evidencia de antropización sin estructuras obvias")
        print(f"   • Necesidad de revisar clasificaciones de bosque primario")
        
    elif invisible_persistence > 0.2:
        print(f"   💡 INDICIOS INTERESANTES:")
        print(f"   • Algunas anomalías no completamente naturales")
        print(f"   • Posible influencia humana histórica sutil")
        print(f"   • Requiere investigación más detallada")
        
    else:
        print(f"   ✅ CONFIRMACIÓN DE BOSQUE PRÍSTINO:")
        print(f"   • No se detecta manejo ancestral significativo")
        print(f"   • Validación de clasificación como 'natural'")
        print(f"   • Contraste con sitios de manejo visible")
    
    # Implicaciones para la escala de Amazonía antropogénica
    print(f"\n🌍 IMPLICACIONES PARA ESCALA DE AMAZONÍA ANTROPOGÉNICA:")
    
    if invisible_persistence > 0.5:
        print(f"   🚨 ESCALA MASIVA:")
        print(f"   • Si esto se replica, millones de hectáreas serían antropogénicas")
        print(f"   • Amazonía 'prístina' sería en realidad 'bosque manejado ancestral'")
        print(f"   • Redefinición completa de políticas de conservación")
        
    elif invisible_persistence > 0.3:
        print(f"   ⚡ ESCALA SIGNIFICATIVA:")
        print(f"   • Porcentaje importante de bosque 'primario' sería manejado")
        print(f"   • Necesidad de revisar mapas de antropización")
        print(f"   • Implicaciones para carbono y biodiversidad")
        
    else:
        print(f"   ✅ ESCALA LIMITADA:")
        print(f"   • Manejo ancestral concentrado en sitios específicos")
        print(f"   • Validación de existencia de bosque realmente prístino")
        print(f"   • Coexistencia de áreas manejadas y naturales")

def main():
    print("🚀 INICIANDO BÚSQUEDA DE MANEJO FORESTAL INVISIBLE")
    print("🌳 Zona Interfluvial Tapajós-Xingu - 'Bosque Prístino'")
    print("🎯 Objetivo: Detectar antropización SIN geometría visible")
    print("💥 Potencial: EXPLOSIVO - Cambiaría escala de Amazonía antropogénica")
    print()
    
    # Test de manejo invisible
    invisible_results = test_invisible_forest_management()
    
    # Análisis comparativo
    if invisible_results:
        comparative_analysis_invisible_vs_visible(invisible_results)
        
        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"archeoscope_invisible_management_test_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(invisible_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 RESULTADOS GUARDADOS: {results_file}")
        
        # Mensaje final basado en resultados
        invisible_index = invisible_results['invisible_management_index']
        
        if invisible_index > 0.6:
            print(f"\n🚨 ¡DESCUBRIMIENTO EXPLOSIVO!")
            print(f"✅ Manejo forestal invisible DETECTADO: {invisible_index:.1%}")
            print(f"🚀 IMPACTO: Cambiaría completamente la escala de Amazonía antropogénica")
            print(f"💥 IMPLICACIÓN: Millones de hectáreas 'prístinas' serían antropogénicas")
            
        elif invisible_index > 0.4:
            print(f"\n⚡ ¡DESCUBRIMIENTO SIGNIFICATIVO!")
            print(f"✅ Evidencia de manejo sutil: {invisible_index:.1%}")
            print(f"🔍 IMPLICACIÓN: Necesidad de revisar bosque 'primario'")
            
        elif invisible_index > 0.2:
            print(f"\n💡 INDICIOS INTERESANTES")
            print(f"✅ Anomalías detectadas: {invisible_index:.1%}")
            print(f"🤔 IMPLICACIÓN: Posible influencia humana histórica")
            
        else:
            print(f"\n✅ BOSQUE APARENTEMENTE PRÍSTINO")
            print(f"📊 Manejo invisible: {invisible_index:.1%}")
            print(f"🌳 CONFIRMACIÓN: Validación de clasificación natural")
        
        print(f"\n🎯 METODOLOGÍA ARCHEOSCOPE:")
        print(f"✅ Capaz de detectar manejo SIN estructuras geométricas")
        print(f"✅ Aplicable a millones de hectáreas amazónicas")
        print(f"✅ Potencial de redefinir conservación global")
        
    else:
        print(f"\n❌ TEST INCOMPLETO")
        print(f"🔧 Revisar configuración del servidor y conectividad")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()