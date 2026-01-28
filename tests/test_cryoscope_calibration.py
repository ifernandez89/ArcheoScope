#!/usr/bin/env python3
"""
Test de calibración de ArcheoScope con sitios reales de anomalías de hielo
Incluye lagos subglaciales, cráteres, grietas y depresiones documentadas
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import numpy as np

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from ice.ice_detector import IceDetector
from ice.cryoarchaeology import CryoArchaeologyEngine

def test_cryoscope_calibration():
    """Test de calibración con múltiples sitios reales de anomalías de hielo"""
    
    print("❄️ ARCHEOSCOPE - TEST DE CALIBRACIÓN CON ANOMALÍAS REALES")
    print("=" * 70)
    print("Sitios de prueba: Lagos subglaciales, cráteres, grietas y depresiones")
    print("Objetivo: Calibrar detección de geometrías y volumetrías bajo hielo")
    print("=" * 70)
    
    # Sitios de prueba con datos reales
    test_sites = [
        {
            "name": "Lago Vostok (Antártida)",
            "coordinates": {"lat": -78.45, "lon": 106.87},
            "type": "subglacial_lake",
            "size_km": {"length": 250, "width": 50, "depth": 0.5},
            "ice_thickness_m": 4000,
            "description": "Lago subglacial líquido bajo 4km de hielo",
            "validation": "GPR y estudios sísmicos",
            "expected_detection": {
                "ice_environment": True,
                "ice_type": "ice_sheet",
                "thickness_range": [3000, 5000],
                "archaeological_potential": "low",  # Muy profundo
                "preservation_quality": "excellent"
            }
        },
        {
            "name": "Grieta Thwaites (Antártida)",
            "coordinates": {"lat": -75.0, "lon": -104.0},
            "type": "deep_fracture",
            "size_km": {"length": 10, "width": 0.5, "depth": 0.8},
            "ice_thickness_m": 2000,
            "description": "Grieta profunda en glaciar, cambios volumétricos",
            "validation": "Radar y estudios satelitales",
            "expected_detection": {
                "ice_environment": True,
                "ice_type": "glacier",
                "thickness_range": [1500, 2500],
                "archaeological_potential": "low",  # Antártida
                "preservation_quality": "excellent"
            }
        },
        {
            "name": "Depresión Groenlandia",
            "coordinates": {"lat": 72.0, "lon": -38.0},
            "type": "subglacial_depression",
            "size_km": {"diameter": 5, "depth": 0.3},
            "ice_thickness_m": 1500,
            "description": "Depresión subglacial documentada con radar",
            "validation": "Radar aéreo y gravimetría",
            "expected_detection": {
                "ice_environment": True,
                "ice_type": "ice_sheet",
                "thickness_range": [1000, 2000],
                "archaeological_potential": "low",  # Groenlandia profunda
                "preservation_quality": "excellent"
            }
        },
        {
            "name": "Cráter Hiawatha (Groenlandia)",
            "coordinates": {"lat": 77.5, "lon": -63.25},
            "type": "impact_crater",
            "size_km": {"diameter": 31, "depth": 0.32},
            "ice_thickness_m": 930,
            "description": "Cráter de impacto subglacial circular",
            "validation": "ICESat-2, CryoSat-2, radar",
            "expected_detection": {
                "ice_environment": True,
                "ice_type": "ice_sheet",
                "thickness_range": [800, 1200],
                "archaeological_potential": "low",  # Groenlandia
                "preservation_quality": "excellent"
            }
        },
        {
            "name": "Lagos Mercer-Whillans (Antártida)",
            "coordinates": {"lat": -84.0, "lon": 135.0},
            "type": "subglacial_lakes",
            "size_km": {"area": 45, "depth": 0.01},
            "ice_thickness_m": 1200,
            "description": "Lagos subglaciales poco profundos",
            "validation": "GPR, resistividad, gravimetría",
            "expected_detection": {
                "ice_environment": True,
                "ice_type": "ice_sheet",
                "thickness_range": [1000, 1500],
                "archaeological_potential": "low",  # Antártida
                "preservation_quality": "excellent"
            }
        },
        {
            "name": "Glaciar Alpino (Alpes Suizos)",
            "coordinates": {"lat": 46.5, "lon": 8.0},
            "type": "alpine_glacier",
            "size_km": {"length": 15, "width": 2, "thickness": 0.2},
            "ice_thickness_m": 200,
            "description": "Glaciar alpino con potencial arqueológico",
            "validation": "Sitio de control para arqueología alpina",
            "expected_detection": {
                "ice_environment": True,
                "ice_type": "glacier",
                "thickness_range": [100, 400],
                "archaeological_potential": "high",  # Alpes = actividad humana
                "preservation_quality": "excellent"
            }
        }
    ]
    
    ice_detector = IceDetector()
    cryoarchaeology_engine = CryoArchaeologyEngine()
    
    results = []
    
    print(f"\n🧪 EJECUTANDO TESTS DE CALIBRACIÓN...")
    print("=" * 70)
    
    for i, site in enumerate(test_sites, 1):
        print(f"\n📍 TEST {i}/6: {site['name']}")
        print(f"   Coordenadas: {site['coordinates']['lat']:.2f}, {site['coordinates']['lon']:.2f}")
        print(f"   Tipo: {site['type'].replace('_', ' ').title()}")
        print(f"   Tamaño: {site['description']}")
        
        try:
            # Detectar contexto de hielo
            ice_context = ice_detector.detect_ice_context(
                site['coordinates']['lat'], 
                site['coordinates']['lon']
            )
            
            print(f"   ✅ Hielo detectado: {ice_context.is_ice_environment}")
            
            if ice_context.is_ice_environment:
                print(f"   🏔️ Tipo detectado: {ice_context.ice_type.value}")
                print(f"   🧊 Espesor: {ice_context.estimated_thickness_m:.0f}m")
                print(f"   🎯 Potencial arqueológico: {ice_context.archaeological_potential}")
                print(f"   🏛️ Preservación: {ice_context.preservation_quality}")
                print(f"   🚶 Accesibilidad: {ice_context.accessibility}")
                
                # Análisis crioarqueológico si es apropiado
                cryo_results = None
                if ice_context.archaeological_potential in ["high", "medium"]:
                    bounds = (
                        site['coordinates']['lat'] - 0.1,
                        site['coordinates']['lat'] + 0.1,
                        site['coordinates']['lon'] - 0.1,
                        site['coordinates']['lon'] + 0.1
                    )
                    
                    cryo_results = cryoarchaeology_engine.analyze_cryo_area(ice_context, bounds)
                    print(f"   🔍 Instrumentos: {len(cryo_results['instruments_used'])}")
                    print(f"   📊 Candidatos: {len(cryo_results['cryo_candidates'])}")
            
            # Validar contra datos esperados
            expected = site['expected_detection']
            validation_results = {}
            
            # Validar detección de hielo
            validation_results['ice_detected'] = ice_context.is_ice_environment == expected['ice_environment']
            
            # Validar tipo de hielo
            if ice_context.ice_type:
                validation_results['ice_type_correct'] = expected['ice_type'] in ice_context.ice_type.value
            else:
                validation_results['ice_type_correct'] = False
            
            # Validar espesor (rango aproximado)
            if ice_context.estimated_thickness_m:
                thickness_in_range = (expected['thickness_range'][0] <= 
                                    ice_context.estimated_thickness_m <= 
                                    expected['thickness_range'][1])
                validation_results['thickness_reasonable'] = thickness_in_range
            else:
                validation_results['thickness_reasonable'] = False
            
            # Validar potencial arqueológico
            validation_results['archaeological_potential_correct'] = (
                ice_context.archaeological_potential == expected['archaeological_potential']
            )
            
            # Validar preservación
            validation_results['preservation_correct'] = (
                ice_context.preservation_quality == expected['preservation_quality']
            )
            
            # Calcular precisión general
            accuracy = sum(validation_results.values()) / len(validation_results)
            
            print(f"   🎯 Precisión: {accuracy:.1%}")
            print(f"      - Hielo detectado: {'✅' if validation_results['ice_detected'] else '❌'}")
            print(f"      - Tipo correcto: {'✅' if validation_results['ice_type_correct'] else '❌'}")
            print(f"      - Espesor razonable: {'✅' if validation_results['thickness_reasonable'] else '❌'}")
            print(f"      - Potencial arqueológico: {'✅' if validation_results['archaeological_potential_correct'] else '❌'}")
            print(f"      - Preservación: {'✅' if validation_results['preservation_correct'] else '❌'}")
            
            # Guardar resultados
            site_result = {
                "site_name": site['name'],
                "coordinates": site['coordinates'],
                "site_type": site['type'],
                "real_data": site,
                "detection_results": {
                    "ice_detected": ice_context.is_ice_environment,
                    "ice_type": ice_context.ice_type.value if ice_context.ice_type else None,
                    "estimated_thickness_m": ice_context.estimated_thickness_m,
                    "archaeological_potential": ice_context.archaeological_potential,
                    "preservation_quality": ice_context.preservation_quality,
                    "accessibility": ice_context.accessibility,
                    "confidence": ice_context.confidence
                },
                "validation": validation_results,
                "accuracy": accuracy,
                "cryo_analysis": {
                    "performed": cryo_results is not None,
                    "candidates": len(cryo_results['cryo_candidates']) if cryo_results else 0,
                    "instruments": len(cryo_results['instruments_used']) if cryo_results else 0
                }
            }
            
            results.append(site_result)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "site_name": site['name'],
                "error": str(e)
            })
    
    # Análisis de resultados generales
    print(f"\n📊 ANÁLISIS DE RESULTADOS DE CALIBRACIÓN")
    print("=" * 70)
    
    successful_tests = [r for r in results if 'accuracy' in r]
    
    if successful_tests:
        # Precisión general
        overall_accuracy = np.mean([r['accuracy'] for r in successful_tests])
        print(f"🎯 Precisión general del sistema: {overall_accuracy:.1%}")
        
        # Análisis por categoría
        categories = ['ice_detected', 'ice_type_correct', 'thickness_reasonable', 
                     'archaeological_potential_correct', 'preservation_correct']
        
        print(f"\n📈 Precisión por categoría:")
        for category in categories:
            category_accuracy = np.mean([r['validation'][category] for r in successful_tests])
            category_name = category.replace('_', ' ').title()
            print(f"   {category_name}: {category_accuracy:.1%}")
        
        # Análisis por tipo de sitio
        print(f"\n🏔️ Precisión por tipo de sitio:")
        site_types = {}
        for result in successful_tests:
            site_type = result['site_type']
            if site_type not in site_types:
                site_types[site_type] = []
            site_types[site_type].append(result['accuracy'])
        
        for site_type, accuracies in site_types.items():
            avg_accuracy = np.mean(accuracies)
            print(f"   {site_type.replace('_', ' ').title()}: {avg_accuracy:.1%} ({len(accuracies)} sitios)")
        
        # Detecciones exitosas
        successful_detections = sum(1 for r in successful_tests if r['validation']['ice_detected'])
        print(f"\n✅ Detecciones exitosas: {successful_detections}/{len(successful_tests)}")
        
        # Análisis crioarqueológico
        cryo_analyses = sum(1 for r in successful_tests if r['cryo_analysis']['performed'])
        total_candidates = sum(r['cryo_analysis']['candidates'] for r in successful_tests)
        print(f"🔍 Análisis crioarqueológicos realizados: {cryo_analyses}")
        print(f"📊 Total de candidatos detectados: {total_candidates}")
    
    # Recomendaciones de calibración
    print(f"\n🔧 RECOMENDACIONES DE CALIBRACIÓN")
    print("=" * 70)
    
    if successful_tests:
        # Identificar áreas de mejora
        weak_categories = []
        for category in categories:
            category_accuracy = np.mean([r['validation'][category] for r in successful_tests])
            if category_accuracy < 0.8:  # Menos del 80%
                weak_categories.append(category.replace('_', ' ').title())
        
        if weak_categories:
            print(f"⚠️ Áreas que necesitan calibración:")
            for category in weak_categories:
                print(f"   - {category}")
        else:
            print(f"✅ Todas las categorías tienen precisión > 80%")
        
        # Recomendaciones específicas
        print(f"\n💡 Recomendaciones específicas:")
        
        # Análisis de espesor
        thickness_errors = []
        for result in successful_tests:
            if not result['validation']['thickness_reasonable']:
                real_thickness = result['real_data']['ice_thickness_m']
                detected_thickness = result['detection_results']['estimated_thickness_m']
                if detected_thickness:
                    error_ratio = abs(detected_thickness - real_thickness) / real_thickness
                    thickness_errors.append(error_ratio)
        
        if thickness_errors:
            avg_thickness_error = np.mean(thickness_errors)
            print(f"   - Calibrar estimación de espesor (error promedio: {avg_thickness_error:.1%})")
        
        # Análisis de potencial arqueológico
        potential_errors = sum(1 for r in successful_tests 
                             if not r['validation']['archaeological_potential_correct'])
        if potential_errors > 0:
            print(f"   - Ajustar evaluación de potencial arqueológico ({potential_errors} errores)")
        
        # Análisis por región
        polar_sites = [r for r in successful_tests if abs(r['coordinates']['lat']) > 60]
        alpine_sites = [r for r in successful_tests if abs(r['coordinates']['lat']) <= 60]
        
        if polar_sites:
            polar_accuracy = np.mean([r['accuracy'] for r in polar_sites])
            print(f"   - Precisión en regiones polares: {polar_accuracy:.1%}")
        
        if alpine_sites:
            alpine_accuracy = np.mean([r['accuracy'] for r in alpine_sites])
            print(f"   - Precisión en regiones alpinas: {alpine_accuracy:.1%}")
    
    # Guardar resultados completos
    print(f"\n💾 GUARDANDO RESULTADOS DE CALIBRACIÓN...")
    
    calibration_results = {
        "test_info": {
            "test_name": "ArcheoScope Calibration with Real Ice Anomalies",
            "test_date": datetime.now().isoformat(),
            "sites_tested": len(test_sites),
            "successful_tests": len(successful_tests)
        },
        "overall_metrics": {
            "overall_accuracy": overall_accuracy if successful_tests else 0,
            "successful_detections": successful_detections if successful_tests else 0,
            "total_sites": len(test_sites)
        },
        "detailed_results": results,
        "calibration_recommendations": weak_categories if successful_tests else []
    }
    
    output_file = f"archeoscope_calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(calibration_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultados guardados en: {output_file}")
    
    # Resumen final
    print(f"\n🏆 RESUMEN DE CALIBRACIÓN ARCHEOSCOPE")
    print("=" * 70)
    
    if successful_tests:
        print(f"✅ Precisión general: {overall_accuracy:.1%}")
        print(f"✅ Sitios procesados exitosamente: {len(successful_tests)}/{len(test_sites)}")
        print(f"✅ Detecciones de hielo correctas: {successful_detections}/{len(successful_tests)}")
        
        if overall_accuracy >= 0.8:
            print(f"🎯 SISTEMA BIEN CALIBRADO (≥80% precisión)")
        elif overall_accuracy >= 0.6:
            print(f"⚠️ SISTEMA NECESITA AJUSTES (60-80% precisión)")
        else:
            print(f"❌ SISTEMA NECESITA RECALIBRACIÓN (<60% precisión)")
    else:
        print(f"❌ No se pudieron procesar sitios exitosamente")
    
    print(f"\n❄️ Calibración de ArcheoScope completada!")
    
    return calibration_results

if __name__ == "__main__":
    results = test_cryoscope_calibration()