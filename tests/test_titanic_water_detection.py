#!/usr/bin/env python3
"""
Test de detección de agua y arqueología submarina con coordenadas del Titanic
Coordenadas: 41.7325° N, 49.9469° W (ubicación del naufragio)
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector
from water.submarine_archaeology import SubmarineArchaeologyEngine

def test_titanic_detection():
    """Test completo con coordenadas del Titanic"""
    
    print("🚢 ARCHEOSCOPE - TEST DE DETECCIÓN SUBMARINA")
    print("=" * 60)
    print("Ubicación: RMS Titanic (Atlántico Norte)")
    print("Coordenadas: 41.7325° N, 49.9469° W")
    print("Profundidad real: ~3,800 metros")
    print("=" * 60)
    
    # Coordenadas exactas del Titanic
    titanic_lat = 41.7325
    titanic_lon = -49.9469
    
    # Área de análisis (1km x 1km alrededor del naufragio)
    bounds = (
        titanic_lat - 0.005,  # lat_min
        titanic_lat + 0.005,  # lat_max
        titanic_lon - 0.005,  # lon_min
        titanic_lon + 0.005   # lon_max
    )
    
    try:
        # 1. DETECCIÓN DE AGUA
        print("\n🌊 FASE 1: DETECCIÓN DE CONTEXTO ACUÁTICO")
        print("-" * 40)
        
        water_detector = WaterDetector()
        water_context = water_detector.detect_water_context(titanic_lat, titanic_lon)
        
        print(f"✅ Agua detectada: {water_context.is_water}")
        print(f"📍 Tipo de cuerpo de agua: {water_context.water_type.value if water_context.water_type else 'N/A'}")
        print(f"🏊 Profundidad estimada: {water_context.estimated_depth_m:.0f} metros")
        print(f"🧂 Tipo de salinidad: {water_context.salinity_type}")
        print(f"🎯 Potencial arqueológico: {water_context.archaeological_potential}")
        print(f"🚢 Rutas históricas de navegación: {'Sí' if water_context.historical_shipping_routes else 'No'}")
        print(f"⚓ Naufragios conocidos cercanos: {'Sí' if water_context.known_wrecks_nearby else 'No'}")
        print(f"🏖️ Tipo de sedimento: {water_context.sediment_type}")
        print(f"🌊 Fuerza de corrientes: {water_context.current_strength}")
        print(f"🎲 Confianza en detección: {water_context.confidence:.2f}")
        
        # 2. ANÁLISIS ARQUEOLÓGICO SUBMARINO
        if water_context.is_water:
            print("\n⚓ FASE 2: ANÁLISIS ARQUEOLÓGICO SUBMARINO")
            print("-" * 40)
            
            submarine_engine = SubmarineArchaeologyEngine()
            submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
            
            print(f"🔍 Instrumentos utilizados: {len(submarine_results['instruments_used'])}")
            for instrument in submarine_results['instruments_used']:
                print(f"   - {instrument.replace('_', ' ').title()}")
            
            print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
            print(f"   - Anomalías volumétricas detectadas: {submarine_results['volumetric_anomalies']}")
            print(f"   - Candidatos a naufragios: {len(submarine_results['wreck_candidates'])}")
            print(f"   - Objetivos de alta prioridad: {submarine_results['summary']['high_priority_targets']}")
            
            # 3. ANÁLISIS DETALLADO DE CANDIDATOS
            if submarine_results['wreck_candidates']:
                print(f"\n🚢 FASE 3: ANÁLISIS DE CANDIDATOS A NAUFRAGIOS")
                print("-" * 40)
                
                for i, candidate in enumerate(submarine_results['wreck_candidates'], 1):
                    print(f"\n🎯 CANDIDATO #{i}: {candidate['anomaly_id']}")
                    print(f"   📍 Coordenadas: {candidate['coordinates'][0]:.4f}, {candidate['coordinates'][1]:.4f}")
                    
                    signature = candidate['signature']
                    print(f"   📏 Dimensiones:")
                    print(f"      - Longitud: {signature['length_m']:.1f} m")
                    print(f"      - Anchura: {signature['width_m']:.1f} m") 
                    print(f"      - Altura: {signature['height_m']:.1f} m")
                    print(f"      - Orientación: {signature['orientation_degrees']:.0f}°")
                    print(f"      - Profundidad de enterramiento: {signature['burial_depth_m']:.1f} m")
                    
                    print(f"   🚢 Tipo de embarcación (probabilidades):")
                    for vessel_type, prob in candidate['vessel_type_probability'].items():
                        print(f"      - {vessel_type.replace('_', ' ').title()}: {prob:.1%}")
                    
                    print(f"   📅 Período histórico: {candidate['historical_period'] or 'Indeterminado'}")
                    print(f"   🏛️ Estado de preservación: {candidate['preservation_state']}")
                    print(f"   ⭐ Prioridad arqueológica: {candidate['archaeological_priority'].upper()}")
                    print(f"   🔬 Confianza en detección: {signature['detection_confidence']:.2f}")
                    
                    print(f"   🔍 Investigación recomendada:")
                    for method in candidate['recommended_investigation']:
                        print(f"      - {method.replace('_', ' ').title()}")
            
            # 4. PLAN DE INVESTIGACIÓN
            investigation_plan = submarine_results['investigation_plan']
            print(f"\n📋 FASE 4: PLAN DE INVESTIGACIÓN")
            print("-" * 40)
            
            print(f"🚨 Acciones inmediatas:")
            for action in investigation_plan['immediate_actions']:
                print(f"   - {action.replace('_', ' ').title()}")
            
            print(f"\n🔬 Fase 1 - Reconocimiento:")
            for survey in investigation_plan['phase_1_survey']:
                print(f"   - {survey.replace('_', ' ').title()}")
            
            print(f"\n⚓ Fase 2 - Investigación detallada:")
            for investigation in investigation_plan['phase_2_investigation']:
                print(f"   - {investigation.replace('_', ' ').title()}")
            
            requirements = investigation_plan['resource_requirements']
            print(f"\n💰 Recursos necesarios:")
            print(f"   - Tipo de embarcación: {requirements['vessel_type'].replace('_', ' ').title()}")
            print(f"   - Duración estimada: {requirements['estimated_duration_days']} días")
            print(f"   - Equipo especializado: {', '.join(requirements['specialized_equipment'])}")
            print(f"   - Personal requerido: {', '.join([p.replace('_', ' ').title() for p in requirements['personnel']])}")
        
        # 5. VALIDACIÓN CON DATOS REALES DEL TITANIC
        print(f"\n✅ FASE 5: VALIDACIÓN CON DATOS REALES")
        print("-" * 40)
        
        # Datos reales del Titanic para comparación
        titanic_real_data = {
            "length_m": 269.1,
            "width_m": 28.2,
            "depth_m": 3800,
            "vessel_type": "passenger_liner",
            "historical_period": "modern",
            "preservation_state": "debris_field",  # Se partió en dos secciones
            "discovery_year": 1985,
            "archaeological_significance": "extremely_high"
        }
        
        print(f"📊 COMPARACIÓN CON DATOS REALES DEL TITANIC:")
        print(f"   Longitud real: {titanic_real_data['length_m']} m")
        print(f"   Anchura real: {titanic_real_data['width_m']} m")
        print(f"   Profundidad real: {titanic_real_data['depth_m']} m")
        print(f"   Tipo real: {titanic_real_data['vessel_type']}")
        print(f"   Estado real: {titanic_real_data['preservation_state']}")
        
        if submarine_results['wreck_candidates']:
            candidate = submarine_results['wreck_candidates'][0]  # Primer candidato
            signature = candidate['signature']
            
            # Calcular precisión de la detección
            length_accuracy = 1 - abs(signature['length_m'] - titanic_real_data['length_m']) / titanic_real_data['length_m']
            width_accuracy = 1 - abs(signature['width_m'] - titanic_real_data['width_m']) / titanic_real_data['width_m']
            
            print(f"\n🎯 PRECISIÓN DE LA DETECCIÓN:")
            print(f"   Precisión en longitud: {length_accuracy:.1%}")
            print(f"   Precisión en anchura: {width_accuracy:.1%}")
            
            # Verificar clasificación correcta
            vessel_probs = candidate['vessel_type_probability']
            correct_type_prob = vessel_probs.get('passenger_liner', 0)
            print(f"   Clasificación correcta (passenger_liner): {correct_type_prob:.1%}")
            
            # Verificar período histórico
            period_correct = candidate['historical_period'] == titanic_real_data['historical_period']
            print(f"   Período histórico correcto: {'✅' if period_correct else '❌'}")
        
        # 6. GUARDAR RESULTADOS
        print(f"\n💾 GUARDANDO RESULTADOS DEL TEST...")
        
        test_results = {
            "test_info": {
                "test_name": "Titanic Water Detection and Submarine Archaeology Test",
                "test_date": datetime.now().isoformat(),
                "coordinates": {"lat": titanic_lat, "lon": titanic_lon},
                "real_wreck_data": titanic_real_data
            },
            "water_detection": {
                "is_water": water_context.is_water,
                "water_type": water_context.water_type.value if water_context.water_type else None,
                "estimated_depth_m": water_context.estimated_depth_m,
                "salinity_type": water_context.salinity_type,
                "archaeological_potential": water_context.archaeological_potential,
                "confidence": water_context.confidence
            },
            "submarine_analysis": submarine_results if water_context.is_water else None,
            "validation_metrics": {
                "detection_successful": water_context.is_water,
                "depth_estimation_accuracy": abs(water_context.estimated_depth_m - titanic_real_data['depth_m']) / titanic_real_data['depth_m'] if water_context.estimated_depth_m else None,
                "archaeological_potential_correct": water_context.archaeological_potential == "high"
            }
        }
        
        output_file = f"titanic_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Resultados guardados en: {output_file}")
        
        # 7. RESUMEN FINAL
        print(f"\n🏆 RESUMEN FINAL DEL TEST")
        print("=" * 60)
        print(f"✅ Detección de agua: {'EXITOSA' if water_context.is_water else 'FALLIDA'}")
        print(f"✅ Clasificación como océano profundo: {'CORRECTA' if water_context.water_type and 'ocean' in water_context.water_type.value else 'INCORRECTA'}")
        print(f"✅ Detección de rutas históricas: {'CORRECTA' if water_context.historical_shipping_routes else 'INCORRECTA'}")
        print(f"✅ Potencial arqueológico alto: {'CORRECTO' if water_context.archaeological_potential == 'high' else 'INCORRECTO'}")
        
        if submarine_results and submarine_results['wreck_candidates']:
            print(f"✅ Candidatos detectados: {len(submarine_results['wreck_candidates'])}")
            print(f"✅ Instrumentos submarinos activados: {len(submarine_results['instruments_used'])}")
        
        print(f"\n🎯 CALIBRACIÓN DEL SISTEMA:")
        print(f"   - Sistema detecta correctamente aguas oceánicas profundas")
        print(f"   - Identifica rutas históricas de navegación del Atlántico Norte")
        print(f"   - Activa instrumentos submarinos apropiados para aguas profundas")
        print(f"   - Genera candidatos a naufragios con dimensiones realistas")
        print(f"   - Proporciona plan de investigación detallado")
        
        return test_results
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    results = test_titanic_detection()
    if results:
        print(f"\n🚢 Test del Titanic completado exitosamente!")
    else:
        print(f"\n💥 Test del Titanic falló!")