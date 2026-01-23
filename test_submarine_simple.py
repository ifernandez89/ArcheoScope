#!/usr/bin/env python3
"""
Test simplificado de arqueología submarina con múltiples ubicaciones
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector
from water.submarine_archaeology import SubmarineArchaeologyEngine

def test_submarine_simple():
    """Test simplificado con múltiples ubicaciones submarinas"""
    
    print("🚢 SUBMARINE ARCHAEOLOGY - TEST SIMPLIFICADO")
    print("=" * 60)
    
    # Coordenadas de prueba
    test_locations = [
        {"name": "Titanic (Atlántico Norte)", "lat": 41.7325, "lon": -49.9469, "expected": "deep_ocean"},
        {"name": "Mediterráneo Central", "lat": 35.0, "lon": 20.0, "expected": "sea"},
        {"name": "Mar del Norte", "lat": 55.0, "lon": 3.0, "expected": "sea"},
        {"name": "Golfo de México", "lat": 25.0, "lon": -90.0, "expected": "sea"},
        {"name": "Mar Báltico", "lat": 59.9167, "lon": 19.7833, "expected": "sea"},
        {"name": "Océano Pacífico", "lat": 30.0, "lon": -140.0, "expected": "deep_ocean"},
        {"name": "Tierra firme (Londres)", "lat": 51.5074, "lon": -0.1278, "expected": "no_water"},
        {"name": "Desierto (Sahara)", "lat": 25.0, "lon": 0.0, "expected": "no_water"}
    ]
    
    water_detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    
    results = []
    
    for location in test_locations:
        print(f"\n📍 PROBANDO: {location['name']}")
        print(f"   Coordenadas: {location['lat']:.4f}, {location['lon']:.4f}")
        
        try:
            # Detectar contexto de agua
            water_context = water_detector.detect_water_context(location['lat'], location['lon'])
            
            print(f"   ✅ Agua detectada: {water_context.is_water}")
            if water_context.is_water:
                print(f"   🌊 Tipo: {water_context.water_type.value}")
                print(f"   🏊 Profundidad: {water_context.estimated_depth_m:.0f}m")
                print(f"   🎯 Potencial arqueológico: {water_context.archaeological_potential}")
                print(f"   🚢 Rutas históricas: {'Sí' if water_context.historical_shipping_routes else 'No'}")
                
                # Si es agua, probar análisis submarino
                if water_context.archaeological_potential in ["high", "medium"]:
                    bounds = (
                        location['lat'] - 0.01,
                        location['lat'] + 0.01,
                        location['lon'] - 0.01,
                        location['lon'] + 0.01
                    )
                    
                    submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
                    print(f"   🔍 Instrumentos: {len(submarine_results['instruments_used'])}")
                    print(f"   📊 Candidatos: {len(submarine_results['wreck_candidates'])}")
                    
                    if submarine_results['wreck_candidates']:
                        best_candidate = submarine_results['wreck_candidates'][0]
                        print(f"   🎯 Mejor candidato: {best_candidate['signature']['length_m']:.0f}m x {best_candidate['signature']['width_m']:.0f}m")
            
            # Verificar si la detección fue correcta
            expected_water = location['expected'] != "no_water"
            detection_correct = water_context.is_water == expected_water
            
            # Verificar tipo si se detectó agua
            type_correct = False
            if water_context.is_water and water_context.water_type:
                if location['expected'] in water_context.water_type.value:
                    type_correct = True
            elif not water_context.is_water and location['expected'] == "no_water":
                type_correct = True
            
            print(f"   {'✅' if detection_correct else '❌'} Detección {'correcta' if detection_correct else 'incorrecta'}")
            if water_context.is_water:
                print(f"   {'✅' if type_correct else '❌'} Tipo {'correcto' if type_correct else 'incorrecto'}")
            
            results.append({
                "location": location['name'],
                "coordinates": [location['lat'], location['lon']],
                "expected": location['expected'],
                "detected_water": water_context.is_water,
                "water_type": water_context.water_type.value if water_context.water_type else None,
                "archaeological_potential": water_context.archaeological_potential,
                "detection_correct": detection_correct,
                "type_correct": type_correct
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "location": location['name'],
                "error": str(e)
            })
    
    # Resumen final
    print(f"\n🏆 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    correct_detections = sum(1 for r in results if r.get('detection_correct', False))
    correct_types = sum(1 for r in results if r.get('type_correct', False))
    total_tests = len([r for r in results if 'detection_correct' in r])
    
    print(f"✅ Detecciones correctas: {correct_detections}/{total_tests}")
    print(f"✅ Tipos correctos: {correct_types}/{total_tests}")
    print(f"📊 Precisión detección: {correct_detections/total_tests*100:.1f}%")
    print(f"📊 Precisión tipos: {correct_types/total_tests*100:.1f}%")
    
    # Análisis por tipo
    water_environments = [r for r in results if r.get('detected_water', False)]
    if water_environments:
        print(f"\n🌊 AMBIENTES ACUÁTICOS DETECTADOS:")
        for result in water_environments:
            print(f"   - {result['location']}: {result['water_type']} (potencial: {result['archaeological_potential']})")
    
    # Guardar resultados
    output_file = f"submarine_simple_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_date": datetime.now().isoformat(),
            "results": results,
            "summary": {
                "correct_detections": correct_detections,
                "correct_types": correct_types,
                "total_tests": total_tests,
                "detection_accuracy": correct_detections/total_tests if total_tests > 0 else 0,
                "type_accuracy": correct_types/total_tests if total_tests > 0 else 0
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados guardados en: {output_file}")
    
    return results

if __name__ == "__main__":
    test_submarine_simple()