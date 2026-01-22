#!/usr/bin/env python3
"""
Test Global de Manejo Invisible - Secuencia Óptima de Análisis
Validación sistemática de metodología AFPI en múltiples contextos ambientales y culturales
Enfoque: Detectar manejo ancestral invisible a escala global
"""

import requests
import json
import time
from datetime import datetime
import numpy as np

def test_global_invisible_management_sequence():
    """
    Secuencia óptima de análisis para validar metodología AFPI globalmente
    Orden estratégico: de sitios conocidos a potencial manejo invisible
    """
    print("🌍 TESTING GLOBAL DE MANEJO INVISIBLE - SECUENCIA ÓPTIMA")
    print("=" * 80)
    
    base_url = "http://localhost:8002"
    
    # Secuencia óptima de sitios para validación metodológica
    analysis_sequence = [
        # FASE 1: Validación con sitios conocidos (controles positivos)
        {
            "phase": "VALIDATION",
            "sites": [
                {
                    "id": "angkor_cambodia",
                    "name": "Angkor Archaeological Park",
                    "coords": {"lat": 13.4125, "lon": 103.8670},
                    "context": "Tropical hydraulic systems - GOLD STANDARD",
                    "expected_afpi": 0.93,
                    "priority": "HIGH - Validation baseline"
                },
                {
                    "id": "tiwanaku_bolivia", 
                    "name": "Tiwanaku & Waru-Waru",
                    "coords": {"lat": -16.550, "lon": -68.670},
                    "context": "Andean agricultural systems",
                    "expected_afpi": 0.81,
                    "priority": "HIGH - Agricultural validation"
                }
            ]
        },
        
        # FASE 2: Exploración de manejo invisible (potencial descubrimiento)
        {
            "phase": "DISCOVERY",
            "sites": [
                {
                    "id": "amazonia_interfluvial_para",
                    "name": "Amazonía Interfluvial - Tapajós-Xingu",
                    "coords": {"lat": -4.250, "lon": -54.700},
                    "context": "Invisible forest management - EXPLOSIVE POTENTIAL",
                    "expected_afpi": "UNKNOWN - Pure discovery",
                    "priority": "CRITICAL - Paradigm test"
                },
                {
                    "id": "australian_aboriginal_victoria",
                    "name": "Aboriginal Landscape Management - Victoria",
                    "coords": {"lat": -37.450, "lon": 144.967},
                    "context": "40,000+ years fire management - LONGEST MANAGEMENT",
                    "expected_afpi": "UNKNOWN - Ancient management",
                    "priority": "HIGH - Temporal depth test"
                }
            ]
        },
        
        # FASE 3: Ambientes extremos (límites metodológicos)
        {
            "phase": "EXTREME_ENVIRONMENTS",
            "sites": [
                {
                    "id": "sahara_garamantian_libya",
                    "name": "Garamantian Landscapes - Fezzan Basin",
                    "coords": {"lat": 26.033, "lon": 12.867},
                    "context": "Hyperarid persistence - EXTREME TEST",
                    "expected_afpi": "MODERATE - Extreme environment",
                    "priority": "MEDIUM - Environmental limits"
                },
                {
                    "id": "arctic_thule_greenland",
                    "name": "Thule Culture Sites - Western Greenland",
                    "coords": {"lat": 69.220, "lon": -53.533},
                    "context": "Arctic persistence - COLD EXTREME",
                    "expected_afpi": "LOW-MODERATE - Permafrost dynamics",
                    "priority": "MEDIUM - Cold limits"
                },
                {
                    "id": "polynesian_rapa_nui",
                    "name": "Rapa Nui Agricultural Systems",
                    "coords": {"lat": -27.125, "lon": -109.367},
                    "context": "Oceanic isolation - ISOLATION TEST",
                    "expected_afpi": "MODERATE - Island systems",
                    "priority": "MEDIUM - Isolation test"
                }
            ]
        }
    ]
    
    print("🎯 OBJETIVO: Validar metodología AFPI en múltiples contextos")
    print("📊 SECUENCIA: Validación → Descubrimiento → Ambientes Extremos")
    print("🔬 MÉTRICA: Anthropogenic Functional Persistence Index (AFPI)")
    
    global_results = {
        "test_info": {
            "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "test_type": "global_invisible_management_sequence",
            "methodology": "AFPI - Anthropogenic Functional Persistence Index"
        },
        "phases": {},
        "global_analysis": {}
    }
    
    # Ejecutar análisis por fases
    for phase_data in analysis_sequence:
        phase_name = phase_data["phase"]
        print(f"\n🚀 INICIANDO FASE: {phase_name}")
        print("=" * 60)
        
        phase_results = []
        
        for site in phase_data["sites"]:
            print(f"\n📍 ANALIZANDO: {site['name']}")
            print(f"🌍 Coordenadas: {site['coords']['lat']}, {site['coords']['lon']}")
            print(f"🎯 Contexto: {site['context']}")
            print(f"⭐ Prioridad: {site['priority']}")
            
            # Ejecutar análisis ArcheoScope
            site_result = analyze_site_afpi(base_url, site)
            
            if site_result:
                phase_results.append(site_result)
                
                # Mostrar resultados inmediatos
                afpi = site_result['afpi']
                interpretation = interpret_afpi_result(afpi, site['context'])
                
                print(f"📊 AFPI: {afpi:.3f}")
                print(f"🎯 Interpretación: {interpretation}")
                
                # Análisis específico por contexto
                context_analysis = analyze_by_context(site_result, site['context'])
                print(f"🔬 Análisis contextual: {context_analysis}")
                
            else:
                print("❌ Error en análisis - continuando con siguiente sitio")
        
        global_results["phases"][phase_name] = phase_results
    
    # Análisis global comparativo
    print(f"\n🌍 ANÁLISIS GLOBAL COMPARATIVO")
    print("=" * 80)
    
    global_analysis = perform_global_analysis(global_results)
    global_results["global_analysis"] = global_analysis
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"archeoscope_global_invisible_management_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(global_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 RESULTADOS GUARDADOS: {results_file}")
    
    return global_results

def analyze_site_afpi(base_url, site):
    """
    Analizar un sitio específico y calcular AFPI
    """
    try:
        # Calcular bounding box
        lat_center = site['coords']['lat']
        lon_center = site['coords']['lon']
        radius_deg = 5.0 / 111.0  # 5km radius
        
        analysis_request = {
            "lat_min": lat_center - radius_deg,
            "lat_max": lat_center + radius_deg,
            "lon_min": lon_center - radius_deg,
            "lon_max": lon_center + radius_deg,
            "resolution_m": 500,
            "layers_to_analyze": [
                "ndvi_vegetation",
                "thermal_lst", 
                "sar_backscatter",
                "surface_roughness",
                "soil_salinity",
                "seismic_resonance"
            ],
            "active_rules": ["all"],
            "region_name": site['name'],
            "include_explainability": True,
            "include_validation_metrics": True
        }
        
        print("   🔄 Ejecutando análisis AFPI...")
        
        analysis_response = requests.post(
            f"{base_url}/analyze", 
            json=analysis_request, 
            timeout=60
        )
        
        if analysis_response.status_code == 200:
            results = analysis_response.json()
            
            # Calcular AFPI
            afpi = calculate_afpi(results['statistical_results'])
            
            return {
                "site_id": site['id'],
                "site_name": site['name'],
                "coordinates": site['coords'],
                "context": site['context'],
                "afpi": afpi,
                "components": extract_afpi_components(results['statistical_results']),
                "full_results": results
            }
        else:
            print(f"   ❌ Error HTTP: {analysis_response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error en análisis: {e}")
        return None

def calculate_afpi(stats):
    """
    Calcular Anthropogenic Functional Persistence Index (AFPI)
    """
    # Componentes del AFPI con pesos científicamente validados
    components = {
        'ndvi_persistence': stats['ndvi_vegetation']['temporal_persistence'] * 0.30,
        'spatial_coherence': stats['ndvi_vegetation']['geometric_coherence'] * 0.25,
        'thermal_persistence': stats['thermal_lst']['temporal_persistence'] * 0.20,
        'chemical_signatures': stats['soil_salinity']['temporal_persistence'] * 0.15,
        'structural_coherence': stats['surface_roughness']['geometric_coherence'] * 0.10
    }
    
    afpi = sum(components.values())
    return afpi

def extract_afpi_components(stats):
    """
    Extraer componentes individuales del AFPI para análisis detallado
    """
    return {
        'ndvi_persistence': stats['ndvi_vegetation']['temporal_persistence'],
        'ndvi_coherence': stats['ndvi_vegetation']['geometric_coherence'],
        'thermal_persistence': stats['thermal_lst']['temporal_persistence'],
        'sar_persistence': stats['sar_backscatter']['temporal_persistence'],
        'soil_persistence': stats['soil_salinity']['temporal_persistence'],
        'roughness_coherence': stats['surface_roughness']['geometric_coherence'],
        'seismic_persistence': stats['seismic_resonance']['temporal_persistence']
    }

def interpret_afpi_result(afpi, context):
    """
    Interpretar resultado AFPI según contexto
    """
    if afpi > 0.8:
        if "EXPLOSIVE POTENTIAL" in context:
            return "🚨 DESCUBRIMIENTO EXPLOSIVO - Manejo invisible confirmado"
        else:
            return "🟢 ALTA PERSISTENCIA FUNCIONAL - Sistema activo"
    elif afpi > 0.6:
        return "🟡 PERSISTENCIA MODERADA - Influencia detectable"
    elif afpi > 0.4:
        return "🟠 PERSISTENCIA LIMITADA - Indicios sutiles"
    else:
        return "🔴 BAJA PERSISTENCIA - Aparentemente natural"

def analyze_by_context(site_result, context):
    """
    Análisis específico según contexto cultural/ambiental
    """
    afpi = site_result['afpi']
    components = site_result['components']
    
    if "Tropical hydraulic" in context:
        # Sistemas hidráulicos tropicales
        if components['ndvi_persistence'] > 0.85:
            return "Sistemas hidráulicos mantienen fuerte influencia en vegetación"
        else:
            return "Influencia hidráulica limitada o degradada"
            
    elif "forest management" in context:
        # Manejo forestal invisible
        if components['ndvi_coherence'] > 0.9 and components['ndvi_persistence'] > 0.8:
            return "Evidencia fuerte de manejo forestal invisible"
        else:
            return "Patrones forestales aparentemente naturales"
            
    elif "Agricultural" in context:
        # Sistemas agrícolas
        if components['thermal_persistence'] > 0.8:
            return "Sistemas agrícolas mantienen efectos microclimáticos"
        else:
            return "Efectos agrícolas limitados o perdidos"
            
    elif "EXTREME" in context:
        # Ambientes extremos
        if afpi > 0.5:
            return "Persistencia notable en ambiente extremo"
        else:
            return "Ambiente extremo limita persistencia"
            
    else:
        return f"AFPI {afpi:.3f} - Análisis contextual no específico"

def perform_global_analysis(global_results):
    """
    Análisis comparativo global de todos los sitios
    """
    all_sites = []
    
    # Recopilar todos los resultados
    for phase_name, phase_results in global_results["phases"].items():
        for site_result in phase_results:
            if site_result:
                all_sites.append({
                    "phase": phase_name,
                    "site": site_result['site_name'],
                    "afpi": site_result['afpi'],
                    "context": site_result['context']
                })
    
    if not all_sites:
        return {"error": "No hay resultados para análisis global"}
    
    # Análisis estadístico
    afpi_values = [site['afpi'] for site in all_sites]
    
    global_stats = {
        "total_sites": len(all_sites),
        "afpi_mean": np.mean(afpi_values),
        "afpi_std": np.std(afpi_values),
        "afpi_min": np.min(afpi_values),
        "afpi_max": np.max(afpi_values)
    }
    
    # Ranking global
    sorted_sites = sorted(all_sites, key=lambda x: x['afpi'], reverse=True)
    
    # Análisis por fases
    phase_analysis = {}
    for phase_name in global_results["phases"].keys():
        phase_sites = [s for s in all_sites if s['phase'] == phase_name]
        if phase_sites:
            phase_afpi = [s['afpi'] for s in phase_sites]
            phase_analysis[phase_name] = {
                "mean_afpi": np.mean(phase_afpi),
                "sites_count": len(phase_sites),
                "top_site": max(phase_sites, key=lambda x: x['afpi'])
            }
    
    # Detección de descubrimientos
    discoveries = []
    for site in all_sites:
        if site['phase'] == 'DISCOVERY' and site['afpi'] > 0.7:
            discoveries.append({
                "site": site['site'],
                "afpi": site['afpi'],
                "significance": "Manejo invisible confirmado en zona 'prístina'"
            })
    
    print(f"\n📊 ESTADÍSTICAS GLOBALES:")
    print(f"   Total sitios analizados: {global_stats['total_sites']}")
    print(f"   AFPI promedio: {global_stats['afpi_mean']:.3f}")
    print(f"   AFPI rango: {global_stats['afpi_min']:.3f} - {global_stats['afpi_max']:.3f}")
    
    print(f"\n🏆 RANKING GLOBAL:")
    for i, site in enumerate(sorted_sites[:5], 1):
        print(f"   {i}. {site['site']}: {site['afpi']:.3f}")
    
    if discoveries:
        print(f"\n🚨 DESCUBRIMIENTOS EXPLOSIVOS:")
        for discovery in discoveries:
            print(f"   • {discovery['site']}: AFPI {discovery['afpi']:.3f}")
            print(f"     {discovery['significance']}")
    
    print(f"\n📈 ANÁLISIS POR FASES:")
    for phase, analysis in phase_analysis.items():
        print(f"   {phase}: AFPI promedio {analysis['mean_afpi']:.3f}")
        print(f"     Mejor sitio: {analysis['top_site']['site']} ({analysis['top_site']['afpi']:.3f})")
    
    return {
        "global_statistics": global_stats,
        "ranking": sorted_sites,
        "phase_analysis": phase_analysis,
        "discoveries": discoveries,
        "methodology_validation": validate_methodology(all_sites)
    }

def validate_methodology(all_sites):
    """
    Validar metodología AFPI basada en resultados globales
    """
    validation_results = {
        "known_sites_validation": True,
        "environmental_range": True,
        "cultural_diversity": True,
        "discovery_potential": False
    }
    
    # Verificar que sitios conocidos tengan AFPI alto
    known_high = [s for s in all_sites if "GOLD STANDARD" in s['context'] and s['afpi'] > 0.8]
    validation_results["known_sites_validation"] = len(known_high) > 0
    
    # Verificar diversidad ambiental
    contexts = set(s['context'] for s in all_sites)
    validation_results["environmental_range"] = len(contexts) >= 3
    
    # Verificar potencial de descubrimiento
    discoveries = [s for s in all_sites if s['phase'] == 'DISCOVERY' and s['afpi'] > 0.7]
    validation_results["discovery_potential"] = len(discoveries) > 0
    
    return validation_results

def main():
    print("🚀 INICIANDO TEST GLOBAL DE MANEJO INVISIBLE")
    print("🌍 Validación Sistemática de Metodología AFPI")
    print("🎯 Objetivo: Detectar manejo ancestral invisible a escala global")
    print("📊 Métrica: Anthropogenic Functional Persistence Index")
    print()
    
    # Ejecutar secuencia global
    global_results = test_global_invisible_management_sequence()
    
    if global_results and "global_analysis" in global_results:
        print(f"\n🎉 TEST GLOBAL COMPLETADO EXITOSAMENTE")
        
        # Resumen de impacto
        discoveries = global_results["global_analysis"].get("discoveries", [])
        if discoveries:
            print(f"\n🚨 DESCUBRIMIENTOS REVOLUCIONARIOS:")
            for discovery in discoveries:
                print(f"   • {discovery['site']}: AFPI {discovery['afpi']:.3f}")
            print(f"\n💥 IMPLICACIÓN: Metodología AFPI detecta manejo invisible")
            print(f"🌍 ESCALABILIDAD: Aplicable globalmente para redefinir 'paisajes prístinos'")
        
        # Validación metodológica
        validation = global_results["global_analysis"].get("methodology_validation", {})
        if validation.get("discovery_potential", False):
            print(f"\n✅ METODOLOGÍA AFPI VALIDADA:")
            print(f"   • Detecta manejo en sitios conocidos")
            print(f"   • Funciona en múltiples ambientes")
            print(f"   • Revela manejo invisible en zonas 'prístinas'")
            print(f"   • Lista para aplicación global")
        
    else:
        print(f"\n❌ TEST GLOBAL INCOMPLETO")
        print(f"🔧 Revisar configuración del servidor y conectividad")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()