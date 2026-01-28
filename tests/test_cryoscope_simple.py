#!/usr/bin/env python3
"""
Test simplificado de ArcheoScope con múltiples ambientes de hielo
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from ice.ice_detector import IceDetector
from ice.cryoarchaeology import CryoArchaeologyEngine

def test_cryoscope_simple():
    """Test simplificado con múltiples ubicaciones de hielo"""
    
    print("❄️ ARCHEOSCOPE - TEST SIMPLIFICADO DE DETECCIÓN DE HIELO")
    print("=" * 60)
    
    # Coordenadas de prueba
    test_locations = [
        {"name": "Ötzi (Alpes)", "lat": 46.7869, "lon": 10.8493, "expected": "glacier"},
        {"name": "Groenlandia Central", "lat": 72.0, "lon": -38.0, "expected": "ice_sheet"},
        {"name": "Antártida", "lat": -78.45, "lon": 106.87, "expected": "ice_sheet"},
        {"name": "Alaska (Permafrost)", "lat": 65.0, "lon": -150.0, "expected": "permafrost"},
        {"name": "Siberia (Permafrost)", "lat": 70.0, "lon": 100.0, "expected": "permafrost"},
        {"name": "Alpes Suizos", "lat": 46.5, "lon": 8.0, "expected": "glacier"},
        {"name": "Tierra templada (París)", "lat": 48.8566, "lon": 2.3522, "expected": "no_ice"},
        {"name": "Trópicos (Ecuador)", "lat": 0.0, "lon": -78.0, "expected": "no_ice"}
    ]
    
    ice_detector = IceDetector()
    cryoarchaeology_engine = CryoArchaeologyEngine()
    
    results = []
    
    for location in test_locations:
        print(f"\n📍 PROBANDO: {location['name']}")
        print(f"   Coordenadas: {location['lat']:.4f}, {location['lon']:.4f}")
        
        try:
            # Detectar contexto de hielo
            ice_context = ice_detector.detect_ice_context(location['lat'], location['lon'])
            
            print(f"   ✅ Hielo detectado: {ice_context.is_ice_environment}")
            if ice_context.is_ice_environment:
                print(f"   ❄️ Tipo: {ice_context.ice_type.value}")
                print(f"   🧊 Espesor: {ice_context.estimated_thickness_m:.0f}m")
                print(f"   🎯 Potencial arqueológico: {ice_context.archaeological_potential}")
                print(f"   🏛️ Preservación: {ice_context.preservation_quality}")
                print(f"   🚶 Accesibilidad: {ice_context.accessibility}")
                
                # Si es agua, probar análisis crioarqueológico
                if ice_context.archaeological_potential in ["high", "medium"]:
                    bounds = (
                        location['lat'] - 0.01,
                        location['lat'] + 0.01,
                        location['lon'] - 0.01,
                        location['lon'] + 0.01
                    )
                    
                    cryo_results = cryoarchaeology_engine.analyze_cryo_area(ice_context, bounds)
                    print(f"   🔍 Instrumentos: {len(cryo_results['instruments_used'])}")
                    print(f"   📊 Candidatos: {len(cryo_results['cryo_candidates'])}")
            
            # Verificar si la detección fue correcta
            expected_ice = location['expected'] != "no_ice"
            detection_correct = ice_context.is_ice_environment == expected_ice
            
            # Verificar tipo si se detectó hielo
            type_correct = False
            if ice_context.is_ice_environment and ice_context.ice_type:
                if location['expected'] in ice_context.ice_type.value:
                    type_correct = True
            elif not ice_context.is_ice_environment and location['expected'] == "no_ice":
                type_correct = True
            
            print(f"   {'✅' if detection_correct else '❌'} Detección {'correcta' if detection_correct else 'incorrecta'}")
            if ice_context.is_ice_environment:
                print(f"   {'✅' if type_correct else '❌'} Tipo {'correcto' if type_correct else 'incorrecto'}")
            
            results.append({
                "location": location['name'],
                "coordinates": [location['lat'], location['lon']],
                "expected": location['expected'],
                "detected_ice": ice_context.is_ice_environment,
                "ice_type": ice_context.ice_type.value if ice_context.ice_type else None,
                "archaeological_potential": ice_context.archaeological_potential,
                "preservation_quality": ice_context.preservation_quality,
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
    ice_environments = [r for r in results if r.get('detected_ice', False)]
    if ice_environments:
        print(f"\n❄️ AMBIENTES DE HIELO DETECTADOS:")
        for result in ice_environments:
            print(f"   - {result['location']}: {result['ice_type']} (potencial: {result['archaeological_potential']})")
    
    # Guardar resultados
    output_file = f"archeoscope_simple_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
    test_cryoscope_simple()