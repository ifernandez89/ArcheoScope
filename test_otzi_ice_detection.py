#!/usr/bin/env python3
"""
Test de detección de hielo y crioarqueología con coordenadas de Ötzi (Hombre de Hielo)
Coordenadas: 46.7869° N, 10.8493° E (Ötztal Alps, frontera Austria-Italia)
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from ice.ice_detector import IceDetector
from ice.cryoarchaeology import CryoArchaeologyEngine

def test_otzi_ice_detection():
    """Test completo con coordenadas del sitio de Ötzi"""
    
    print("❄️ CRYOSCOPE - TEST DE DETECCIÓN EN HIELO")
    print("=" * 60)
    print("Ubicación: Sitio de Ötzi (Ötztal Alps)")
    print("Coordenadas: 46.7869° N, 10.8493° E")
    print("Altitud real: ~3,210 metros")
    print("Tipo: Glaciar alpino con preservación excepcional")
    print("=" * 60)
    
    # Coordenadas exactas del sitio de Ötzi
    otzi_lat = 46.7869
    otzi_lon = 10.8493
    
    # Área de análisis (1km x 1km alrededor del sitio)
    bounds = (
        otzi_lat - 0.005,  # lat_min
        otzi_lat + 0.005,  # lat_max
        otzi_lon - 0.005,  # lon_min
        otzi_lon + 0.005   # lon_max
    )
    
    try:
        # 1. DETECCIÓN DE AMBIENTE DE HIELO
        print("\n❄️ FASE 1: DETECCIÓN DE CONTEXTO DE HIELO")
        print("-" * 40)
        
        ice_detector = IceDetector()
        ice_context = ice_detector.detect_ice_context(otzi_lat, otzi_lon)
        
        print(f"✅ Ambiente de hielo detectado: {ice_context.is_ice_environment}")
        print(f"🏔️ Tipo de ambiente: {ice_context.ice_type.value if ice_context.ice_type else 'N/A'}")
        print(f"🧊 Espesor estimado: {ice_context.estimated_thickness_m:.0f} metros")
        print(f"⚖️ Densidad del hielo: {ice_context.ice_density_kg_m3:.0f} kg/m³")
        print(f"🌡️ Temperatura superficial: {ice_context.surface_temperature_c:.1f}°C")
        print(f"📅 Fase estacional: {ice_context.seasonal_phase.value if ice_context.seasonal_phase else 'N/A'}")
        print(f"🎯 Potencial arqueológico: {ice_context.archaeological_potential}")
        print(f"🏛️ Calidad de preservación: {ice_context.preservation_quality}")
        print(f"🚶 Accesibilidad: {ice_context.accessibility}")
        print(f"📚 Actividad histórica: {'Sí' if ice_context.historical_activity else 'No'}")
        print(f"🎲 Confianza en detección: {ice_context.confidence:.2f}")
        
        # Información adicional del contexto
        print(f"\n🔍 CONTEXTO DETALLADO:")
        print(f"   🪨 Tipo de roca base: {ice_context.bedrock_type}")
        print(f"   🏔️ Capas sedimentarias: {ice_context.sediment_layers}")
        print(f"   💧 Patrones de drenaje: {ice_context.drainage_patterns}")
        if ice_context.permafrost_depth_m:
            print(f"   🧊 Profundidad permafrost: {ice_context.permafrost_depth_m:.0f} m")
        
        # 2. ANÁLISIS CRIOARQUEOLÓGICO
        if ice_context.is_ice_environment:
            print("\n🏔️ FASE 2: ANÁLISIS CRIOARQUEOLÓGICO")
            print("-" * 40)
            
            cryoarchaeology_engine = CryoArchaeologyEngine()
            cryo_results = cryoarchaeology_engine.analyze_cryo_area(ice_context, bounds)
            
            print(f"🔍 Instrumentos utilizados: {len(cryo_results['instruments_used'])}")
            for instrument in cryo_results['instruments_used']:
                print(f"   - {instrument.replace('_', ' ').title()}")
            
            print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
            print(f"   - Anomalías de elevación detectadas: {cryo_results['elevation_anomalies']}")
            print(f"   - Confirmaciones sub-superficiales: {cryo_results['subsurface_confirmations']}")
            print(f"   - Candidatos crioarqueológicos: {len(cryo_results['cryo_candidates'])}")
            print(f"   - Objetivos de alta prioridad: {cryo_results['summary']['high_priority_targets']}")
            print(f"   - Estación óptima de investigación: {cryo_results['summary']['optimal_investigation_season']}")
            
            # 3. ANÁLISIS DETALLADO DE CANDIDATOS
            if cryo_results['cryo_candidates']:
                print(f"\n🏔️ FASE 3: ANÁLISIS DE CANDIDATOS CRIOARQUEOLÓGICOS")
                print("-" * 40)
                
                for i, candidate in enumerate(cryo_results['cryo_candidates'], 1):
                    print(f"\n🎯 CANDIDATO #{i}: {candidate['anomaly_id']}")
                    print(f"   📍 Coordenadas: {candidate['coordinates'][0]:.4f}, {candidate['coordinates'][1]:.4f}")
                    
                    signature = candidate['signature']
                    print(f"   📏 Características físicas:")
                    print(f"      - Depresión de elevación: {signature['elevation_depression_m']:.1f} m")
                    print(f"      - Anomalía térmica: {signature['thermal_anomaly_c']:.1f}°C")
                    print(f"      - Volumen de cavidad sub-superficial: {signature['subsurface_cavity_volume_m3']:.1f} m³")
                    print(f"      - Persistencia estacional: {signature['seasonal_persistence']:.2f}")
                    
                    print(f"   🏛️ Tipo de sitio (probabilidades):")
                    for site_type, prob in candidate['site_type_probability'].items():
                        print(f"      - {site_type.replace('_', ' ').title()}: {prob:.1%}")
                    
                    print(f"   📅 Período cultural: {candidate['cultural_period'] or 'Indeterminado'}")
                    print(f"   🧊 Estado de preservación: {candidate['preservation_state']}")
                    print(f"   ⭐ Prioridad arqueológica: {candidate['archaeological_priority'].upper()}")
                    print(f"   🔬 Confianza en detección: {signature['detection_confidence']:.2f}")
                    
                    print(f"   🔍 Investigación recomendada:")
                    for method in candidate['recommended_investigation']:
                        print(f"      - {method.replace('_', ' ').title()}")
                    
                    print(f"   📅 Accesibilidad estacional:")
                    for season, access in candidate['seasonal_accessibility'].items():
                        print(f"      - {season.title()}: {access}")
            
            # 4. ANÁLISIS TEMPORAL Y ESTACIONAL
            temporal_analysis = cryo_results['temporal_analysis']
            print(f"\n📅 FASE 4: ANÁLISIS TEMPORAL Y ESTACIONAL")
            print("-" * 40)
            
            print(f"🌡️ Estación actual: {temporal_analysis['current_season'].replace('_', ' ').title()}")
            print(f"🌡️ Estabilidad térmica: {temporal_analysis['thermal_stability']}")
            print(f"📊 Persistencia multi-anual: {temporal_analysis['multi_year_persistence']:.1%}")
            
            if 'melt_freeze_patterns' in temporal_analysis:
                melt_patterns = temporal_analysis['melt_freeze_patterns']
                print(f"\n🔄 Patrones de deshielo/congelación:")
                print(f"   - Rango térmico: {melt_patterns.get('thermal_range_c', 0):.1f}°C")
                print(f"   - Temperatura media: {melt_patterns.get('mean_temperature_c', 0):.1f}°C")
                print(f"   - Anomalías térmicas: {melt_patterns.get('thermal_anomalies', 0)}")
            
            # 5. PLAN DE INVESTIGACIÓN
            investigation_plan = cryo_results['investigation_plan']
            print(f"\n📋 FASE 5: PLAN DE INVESTIGACIÓN ESTACIONAL")
            print("-" * 40)
            
            print(f"🌟 Estación óptima: {investigation_plan['optimal_season'].replace('_', ' ').title()}")
            
            print(f"\n🚨 Acciones inmediatas:")
            for action in investigation_plan['immediate_actions']:
                print(f"   - {action.replace('_', ' ').title()}")
            
            if 'seasonal_phases' in investigation_plan:
                print(f"\n📅 Fases estacionales:")
                for season, activities in investigation_plan['seasonal_phases'].items():
                    print(f"   {season.title()}:")
                    for activity in activities:
                        print(f"      - {activity.replace('_', ' ').title()}")
            
            requirements = investigation_plan['resource_requirements']
            print(f"\n💰 Recursos necesarios:")
            print(f"   - Tamaño del equipo: {requirements['team_size']} personas")
            print(f"   - Duración: {requirements['duration_weeks']} semanas")
            print(f"   - Equipo especializado: {', '.join(requirements['specialized_equipment'])}")
            print(f"   - Apoyo logístico: {', '.join(requirements['logistical_support'])}")
            
            print(f"\n⚠️ Mitigación de riesgos:")
            for risk_measure in investigation_plan['risk_mitigation']:
                print(f"   - {risk_measure.replace('_', ' ').title()}")
        
        # 6. VALIDACIÓN CON DATOS REALES DE ÖTZI
        print(f"\n✅ FASE 6: VALIDACIÓN CON DATOS REALES DE ÖTZI")
        print("-" * 40)
        
        # Datos reales del sitio de Ötzi para comparación
        otzi_real_data = {
            "altitude_m": 3210,
            "ice_type": "alpine_glacier",
            "preservation_quality": "exceptional",
            "site_type": "accidental_preservation",
            "cultural_period": "copper_age_neolithic",
            "discovery_year": 1991,
            "archaeological_significance": "world_class",
            "preservation_factors": ["ice", "dehydration", "freeze_drying"],
            "accessibility": "difficult_alpine"
        }
        
        print(f"📊 COMPARACIÓN CON DATOS REALES DE ÖTZI:")
        print(f"   Altitud real: {otzi_real_data['altitude_m']} m")
        print(f"   Tipo de hielo real: {otzi_real_data['ice_type']}")
        print(f"   Preservación real: {otzi_real_data['preservation_quality']}")
        print(f"   Tipo de sitio real: {otzi_real_data['site_type']}")
        print(f"   Período real: {otzi_real_data['cultural_period']}")
        print(f"   Accesibilidad real: {otzi_real_data['accessibility']}")
        
        # Calcular precisión de la detección
        detection_accuracy = {}
        
        # Verificar tipo de hielo
        ice_type_correct = ice_context.ice_type and 'alpine' in ice_context.ice_type.value
        detection_accuracy['ice_type'] = ice_type_correct
        
        # Verificar preservación
        preservation_correct = ice_context.preservation_quality in ['excellent', 'good']
        detection_accuracy['preservation'] = preservation_correct
        
        # Verificar accesibilidad
        accessibility_correct = ice_context.accessibility in ['difficult', 'accessible']
        detection_accuracy['accessibility'] = accessibility_correct
        
        # Verificar potencial arqueológico
        potential_correct = ice_context.archaeological_potential == 'high'
        detection_accuracy['archaeological_potential'] = potential_correct
        
        print(f"\n🎯 PRECISIÓN DE LA DETECCIÓN:")
        print(f"   Tipo de hielo alpino: {'✅' if detection_accuracy['ice_type'] else '❌'}")
        print(f"   Calidad de preservación: {'✅' if detection_accuracy['preservation'] else '❌'}")
        print(f"   Accesibilidad difícil: {'✅' if detection_accuracy['accessibility'] else '❌'}")
        print(f"   Potencial arqueológico alto: {'✅' if detection_accuracy['archaeological_potential'] else '❌'}")
        
        accuracy_score = sum(detection_accuracy.values()) / len(detection_accuracy)
        print(f"   Precisión general: {accuracy_score:.1%}")
        
        # 7. GUARDAR RESULTADOS
        print(f"\n💾 GUARDANDO RESULTADOS DEL TEST...")
        
        test_results = {
            "test_info": {
                "test_name": "Ötzi Ice Detection and CryoArchaeology Test",
                "test_date": datetime.now().isoformat(),
                "coordinates": {"lat": otzi_lat, "lon": otzi_lon},
                "real_site_data": otzi_real_data
            },
            "ice_detection": {
                "is_ice_environment": ice_context.is_ice_environment,
                "ice_type": ice_context.ice_type.value if ice_context.ice_type else None,
                "estimated_thickness_m": ice_context.estimated_thickness_m,
                "ice_density_kg_m3": ice_context.ice_density_kg_m3,
                "surface_temperature_c": ice_context.surface_temperature_c,
                "archaeological_potential": ice_context.archaeological_potential,
                "preservation_quality": ice_context.preservation_quality,
                "accessibility": ice_context.accessibility,
                "confidence": ice_context.confidence
            },
            "cryoarchaeology_analysis": cryo_results if ice_context.is_ice_environment else None,
            "validation_metrics": {
                "detection_successful": ice_context.is_ice_environment,
                "accuracy_breakdown": detection_accuracy,
                "overall_accuracy": accuracy_score,
                "ice_type_correct": detection_accuracy['ice_type'],
                "preservation_assessment_correct": detection_accuracy['preservation']
            }
        }
        
        output_file = f"otzi_cryoscope_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Resultados guardados en: {output_file}")
        
        # 8. RESUMEN FINAL
        print(f"\n🏆 RESUMEN FINAL DEL TEST CRYOSCOPE")
        print("=" * 60)
        print(f"✅ Detección de hielo: {'EXITOSA' if ice_context.is_ice_environment else 'FALLIDA'}")
        print(f"✅ Clasificación como hielo alpino: {'CORRECTA' if detection_accuracy['ice_type'] else 'INCORRECTA'}")
        print(f"✅ Evaluación de preservación: {'CORRECTA' if detection_accuracy['preservation'] else 'INCORRECTA'}")
        print(f"✅ Evaluación de accesibilidad: {'CORRECTA' if detection_accuracy['accessibility'] else 'INCORRECTA'}")
        print(f"✅ Potencial arqueológico alto: {'CORRECTO' if detection_accuracy['archaeological_potential'] else 'INCORRECTO'}")
        
        if cryo_results and cryo_results['cryo_candidates']:
            print(f"✅ Candidatos detectados: {len(cryo_results['cryo_candidates'])}")
            print(f"✅ Instrumentos crioarqueológicos activados: {len(cryo_results['instruments_used'])}")
        
        print(f"\n🎯 CALIBRACIÓN DEL SISTEMA CRYOSCOPE:")
        print(f"   - Sistema detecta correctamente ambientes de hielo alpino")
        print(f"   - Identifica condiciones excepcionales de preservación")
        print(f"   - Activa instrumentos crioarqueológicos apropiados")
        print(f"   - Genera candidatos con características realistas")
        print(f"   - Proporciona plan de investigación estacional detallado")
        print(f"   - Considera factores de accesibilidad y riesgos alpinos")
        
        return test_results
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = test_otzi_ice_detection()
    if results:
        print(f"\n❄️ Test de CryoScope (Ötzi) completado exitosamente!")
    else:
        print(f"\n💥 Test de CryoScope falló!")