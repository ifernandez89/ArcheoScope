#!/usr/bin/env python3
"""
Test de detección de anomalías en coordenadas específicas del Caribe/Atlántico
Coordenadas: 25.800, -70.000 y 25.300, -70.500
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector
from water.submarine_archaeology import SubmarineArchaeologyEngine
from ice.ice_detector import IceDetector
from ice.cryoarchaeology import CryoArchaeologyEngine

def test_caribbean_anomaly_detection():
    """Test de detección de anomalías en coordenadas específicas del Caribe"""
    
    print("🏝️ ARCHEOSCOPE - DETECCIÓN DE ANOMALÍAS EN EL CARIBE")
    print("=" * 65)
    print("Región: Atlántico Norte/Caribe - Triángulo de las Bermudas")
    print("Objetivo: Detectar anomalías arqueológicas submarinas")
    print("=" * 65)
    
    # Coordenadas de análisis
    target_coordinates = [
        {
            "name": "Punto Norte",
            "lat": 25.800,
            "lon": -70.000,
            "description": "Coordenada norte del área de análisis"
        },
        {
            "name": "Punto Sur", 
            "lat": 25.300,
            "lon": -70.500,
            "description": "Coordenada sur del área de análisis"
        },
        {
            "name": "Centro del Área",
            "lat": 25.550,  # Punto medio
            "lon": -70.250,  # Punto medio
            "description": "Centro del área de análisis"
        }
    ]
    
    water_detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    ice_detector = IceDetector()
    
    results = []
    
    print(f"\n🔍 ANALIZANDO COORDENADAS ESPECÍFICAS...")
    print("=" * 65)
    
    for i, coord in enumerate(target_coordinates, 1):
        print(f"\n📍 ANÁLISIS {i}/3: {coord['name']}")
        print(f"   Coordenadas: {coord['lat']:.3f}°N, {coord['lon']:.3f}°W")
        print(f"   Descripción: {coord['description']}")
        
        try:
            # 1. Detectar ambiente (agua vs hielo)
            water_context = water_detector.detect_water_context(coord['lat'], coord['lon'])
            ice_context = ice_detector.detect_ice_context(coord['lat'], coord['lon'])
            
            print(f"\n🌊 CONTEXTO AMBIENTAL:")
            print(f"   Agua detectada: {'✅ Sí' if water_context.is_water else '❌ No'}")
            print(f"   Hielo detectado: {'✅ Sí' if ice_context.is_ice_environment else '❌ No'}")
            
            analysis_results = {}
            
            if water_context.is_water:
                print(f"\n🌊 ANÁLISIS SUBMARINO:")
                print(f"   Tipo de agua: {water_context.water_type.value}")
                print(f"   Profundidad estimada: {water_context.estimated_depth_m:.0f}m")
                print(f"   Salinidad: {water_context.salinity_type}")
                print(f"   Potencial arqueológico: {water_context.archaeological_potential}")
                print(f"   Rutas históricas: {'Sí' if water_context.historical_shipping_routes else 'No'}")
                print(f"   Naufragios conocidos: {'Sí' if water_context.known_wrecks_nearby else 'No'}")
                print(f"   Tipo de sedimento: {water_context.sediment_type}")
                print(f"   Fuerza de corrientes: {water_context.current_strength}")
                
                # Análisis arqueológico submarino detallado
                bounds = (
                    coord['lat'] - 0.05,  # Área de 0.1° x 0.1° (~11km x 11km)
                    coord['lat'] + 0.05,
                    coord['lon'] - 0.05,
                    coord['lon'] + 0.05
                )
                
                print(f"\n🔍 EJECUTANDO ANÁLISIS ARQUEOLÓGICO SUBMARINO...")
                submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
                
                print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
                print(f"   Instrumentos utilizados: {len(submarine_results['instruments_used'])}")
                for instrument in submarine_results['instruments_used']:
                    print(f"     - {instrument.replace('_', ' ').title()}")
                
                print(f"   Anomalías volumétricas detectadas: {submarine_results['volumetric_anomalies']}")
                print(f"   Candidatos a naufragios: {len(submarine_results['wreck_candidates'])}")
                
                if submarine_results['wreck_candidates']:
                    print(f"\n⚓ CANDIDATOS A NAUFRAGIOS DETECTADOS:")
                    
                    for j, candidate in enumerate(submarine_results['wreck_candidates'], 1):
                        print(f"\n   🚢 CANDIDATO {j}:")
                        print(f"      ID: {candidate['anomaly_id']}")
                        print(f"      Coordenadas: {candidate['coordinates'][0]:.4f}, {candidate['coordinates'][1]:.4f}")
                        
                        signature = candidate['signature']
                        print(f"      Dimensiones:")
                        print(f"        - Longitud: {signature['length_m']:.1f}m")
                        print(f"        - Anchura: {signature['width_m']:.1f}m")
                        print(f"        - Altura: {signature['height_m']:.1f}m")
                        print(f"        - Orientación: {signature['orientation_degrees']:.0f}°")
                        
                        print(f"      Características:")
                        print(f"        - Profundidad de enterramiento: {signature['burial_depth_m']:.1f}m")
                        print(f"        - Confianza de detección: {signature['detection_confidence']:.2f}")
                        print(f"        - Coherencia geométrica: {signature['geometric_coherence']:.2f}")
                        
                        print(f"      Clasificación:")
                        vessel_types = candidate['vessel_type_probability']
                        top_type = max(vessel_types, key=vessel_types.get)
                        print(f"        - Tipo más probable: {top_type.replace('_', ' ').title()} ({vessel_types[top_type]:.1%})")
                        
                        print(f"      Evaluación:")
                        print(f"        - Período histórico: {candidate['historical_period'] or 'Desconocido'}")
                        print(f"        - Estado de preservación: {candidate['preservation_state']}")
                        print(f"        - Prioridad arqueológica: {candidate['archaeological_priority']}")
                        
                        print(f"      Investigación recomendada:")
                        for method in candidate['recommended_investigation']:
                            print(f"        - {method.replace('_', ' ').title()}")
                
                # Plan de investigación
                investigation_plan = submarine_results['investigation_plan']
                print(f"\n📋 PLAN DE INVESTIGACIÓN RECOMENDADO:")
                
                if investigation_plan['immediate_actions']:
                    print(f"   Acciones inmediatas:")
                    for action in investigation_plan['immediate_actions']:
                        print(f"     - {action.replace('_', ' ').title()}")
                
                if investigation_plan['phase_1_survey']:
                    print(f"   Fase 1 - Reconocimiento:")
                    for survey in investigation_plan['phase_1_survey']:
                        print(f"     - {survey.replace('_', ' ').title()}")
                
                resources = investigation_plan['resource_requirements']
                print(f"   Recursos necesarios:")
                print(f"     - Tipo de embarcación: {resources['vessel_type'].replace('_', ' ').title()}")
                print(f"     - Duración estimada: {resources['estimated_duration_days']} días")
                print(f"     - Equipo especializado: {', '.join(resources['specialized_equipment'])}")
                
                analysis_results = {
                    'environment': 'water',
                    'water_context': {
                        'type': water_context.water_type.value,
                        'depth_m': water_context.estimated_depth_m,
                        'archaeological_potential': water_context.archaeological_potential,
                        'historical_routes': water_context.historical_shipping_routes,
                        'known_wrecks': water_context.known_wrecks_nearby
                    },
                    'submarine_analysis': submarine_results,
                    'summary': {
                        'anomalies_detected': submarine_results['volumetric_anomalies'],
                        'wreck_candidates': len(submarine_results['wreck_candidates']),
                        'high_priority_targets': submarine_results['summary']['high_priority_targets'],
                        'instruments_used': len(submarine_results['instruments_used'])
                    }
                }
            
            elif ice_context.is_ice_environment:
                print(f"\n❄️ ANÁLISIS CRIOARQUEOLÓGICO:")
                print(f"   Tipo de hielo: {ice_context.ice_type.value}")
                print(f"   Espesor estimado: {ice_context.estimated_thickness_m:.0f}m")
                print(f"   Potencial arqueológico: {ice_context.archaeological_potential}")
                print(f"   Calidad de preservación: {ice_context.preservation_quality}")
                print(f"   Accesibilidad: {ice_context.accessibility}")
                
                analysis_results = {
                    'environment': 'ice',
                    'ice_context': {
                        'type': ice_context.ice_type.value,
                        'thickness_m': ice_context.estimated_thickness_m,
                        'archaeological_potential': ice_context.archaeological_potential,
                        'preservation_quality': ice_context.preservation_quality
                    }
                }
            
            else:
                print(f"\n🏔️ AMBIENTE TERRESTRE:")
                print(f"   No se detectó agua ni hielo en estas coordenadas")
                print(f"   Posible ambiente terrestre o área no cubierta")
                
                analysis_results = {
                    'environment': 'terrestrial',
                    'note': 'No water or ice environment detected'
                }
            
            # Guardar resultado
            result = {
                'coordinates': coord,
                'analysis_results': analysis_results,
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(result)
            
        except Exception as e:
            print(f"\n❌ ERROR EN ANÁLISIS: {e}")
            results.append({
                'coordinates': coord,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    
    # Resumen general del área
    print(f"\n🗺️ RESUMEN DEL ÁREA ANALIZADA")
    print("=" * 65)
    
    water_points = [r for r in results if r.get('analysis_results', {}).get('environment') == 'water']
    total_anomalies = sum(r['analysis_results']['summary']['anomalies_detected'] 
                         for r in water_points if 'summary' in r['analysis_results'])
    total_candidates = sum(r['analysis_results']['summary']['wreck_candidates'] 
                          for r in water_points if 'summary' in r['analysis_results'])
    
    print(f"Puntos analizados: {len(results)}")
    print(f"Puntos con agua: {len(water_points)}")
    print(f"Total anomalías detectadas: {total_anomalies}")
    print(f"Total candidatos a naufragios: {total_candidates}")
    
    if total_candidates > 0:
        print(f"\n🎯 HALLAZGOS SIGNIFICATIVOS:")
        print(f"   ✅ Se detectaron {total_candidates} candidatos a naufragios en el área")
        print(f"   🔍 Se recomienda investigación arqueológica detallada")
        print(f"   📊 Área con potencial arqueológico submarino confirmado")
    else:
        print(f"\n📊 EVALUACIÓN DEL ÁREA:")
        print(f"   ℹ️ No se detectaron candidatos a naufragios evidentes")
        print(f"   🌊 Área marina con condiciones normales")
        print(f"   🔍 Posible área de tránsito sin incidentes históricos")
    
    # Guardar resultados completos
    output_data = {
        'analysis_info': {
            'region': 'Caribbean/North Atlantic',
            'coordinates_analyzed': len(target_coordinates),
            'analysis_date': datetime.now().isoformat(),
            'area_description': 'Triángulo de las Bermudas - Análisis arqueológico submarino'
        },
        'summary': {
            'total_points': len(results),
            'water_points': len(water_points),
            'total_anomalies': total_anomalies,
            'total_candidates': total_candidates
        },
        'detailed_results': results
    }
    
    output_file = f"caribbean_anomaly_detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados completos guardados en: {output_file}")
    
    # Conclusión
    print(f"\n🏆 CONCLUSIÓN DEL ANÁLISIS")
    print("=" * 65)
    
    if total_candidates > 0:
        print(f"🎯 ÁREA CON POTENCIAL ARQUEOLÓGICO DETECTADO")
        print(f"   Se encontraron {total_candidates} candidatos que requieren investigación")
    else:
        print(f"🌊 ÁREA MARINA SIN ANOMALÍAS EVIDENTES")
        print(f"   Condiciones normales del fondo marino")
    
    print(f"\n🔍 Análisis de anomalías en el Caribe completado!")
    
    return output_data

if __name__ == "__main__":
    results = test_caribbean_anomaly_detection()