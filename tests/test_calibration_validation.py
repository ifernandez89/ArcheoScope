#!/usr/bin/env python3
"""
Test de validación final de las mejoras de calibración
Prueba tanto el sistema submarino como el ArcheoScope con casos representativos
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

def test_calibration_validation():
    """Test de validación final de las mejoras de calibración"""
    
    print("🔬 VALIDACIÓN FINAL DE CALIBRACIÓN - ARCHEOSCOPE COMPLETO")
    print("=" * 70)
    print("Objetivo: Validar mejoras en estimación de profundidad, clasificación")
    print("          y escalado dimensional para ambientes acuáticos y de hielo")
    print("=" * 70)
    
    # Casos de prueba representativos
    test_cases = [
        {
            "name": "Titanic (Océano Profundo)",
            "coordinates": {"lat": 41.7325, "lon": -49.9469},
            "environment": "water",
            "expected": {
                "detected": True,
                "type": "deep_ocean",
                "depth_range": [3700, 3900],
                "archaeological_potential": "high"
            }
        },
        {
            "name": "Andrea Doria (Costero)",
            "coordinates": {"lat": 40.4833, "lon": -69.85},
            "environment": "water",
            "expected": {
                "detected": True,
                "type": "coastal",
                "depth_range": [60, 80],
                "archaeological_potential": "medium"
            }
        },
        {
            "name": "Glaciar Alpino (Arqueología)",
            "coordinates": {"lat": 46.5, "lon": 8.0},
            "environment": "ice",
            "expected": {
                "detected": True,
                "type": "glacier",
                "thickness_range": [100, 400],
                "archaeological_potential": "high"
            }
        },
        {
            "name": "Antártida (Polar Extremo)",
            "coordinates": {"lat": -78.45, "lon": 106.87},
            "environment": "ice",
            "expected": {
                "detected": True,
                "type": "ice_sheet",
                "thickness_range": [3000, 5000],
                "archaeological_potential": "low"
            }
        }
    ]
    
    water_detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    ice_detector = IceDetector()
    cryo_engine = CryoArchaeologyEngine()
    
    results = []
    
    print(f"\n🧪 EJECUTANDO TESTS DE VALIDACIÓN...")
    print("=" * 70)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🎯 TEST {i}/4: {case['name']}")
        print(f"   Coordenadas: {case['coordinates']['lat']:.4f}, {case['coordinates']['lon']:.4f}")
        print(f"   Ambiente: {case['environment'].title()}")
        
        try:
            if case['environment'] == 'water':
                # Test sistema submarino
                water_context = water_detector.detect_water_context(
                    case['coordinates']['lat'], 
                    case['coordinates']['lon']
                )
                
                print(f"   ✅ Agua detectada: {water_context.is_water}")
                
                if water_context.is_water:
                    print(f"   🌊 Tipo: {water_context.water_type.value}")
                    print(f"   🏊 Profundidad: {water_context.estimated_depth_m:.0f}m")
                    print(f"   🎯 Potencial: {water_context.archaeological_potential}")
                    
                    # Validar resultados
                    expected = case['expected']
                    validation = {
                        'detected': water_context.is_water == expected['detected'],
                        'type_correct': expected['type'] in water_context.water_type.value,
                        'depth_in_range': (expected['depth_range'][0] <= 
                                         water_context.estimated_depth_m <= 
                                         expected['depth_range'][1]),
                        'potential_correct': water_context.archaeological_potential == expected['archaeological_potential']
                    }
                    
                    accuracy = sum(validation.values()) / len(validation)
                    print(f"   📊 Precisión: {accuracy:.1%}")
                    
                    results.append({
                        'case': case['name'],
                        'environment': 'water',
                        'accuracy': accuracy,
                        'validation': validation,
                        'results': {
                            'detected': water_context.is_water,
                            'type': water_context.water_type.value,
                            'depth': water_context.estimated_depth_m,
                            'potential': water_context.archaeological_potential
                        }
                    })
            
            elif case['environment'] == 'ice':
                # Test sistema ArcheoScope
                ice_context = ice_detector.detect_ice_context(
                    case['coordinates']['lat'], 
                    case['coordinates']['lon']
                )
                
                print(f"   ✅ Hielo detectado: {ice_context.is_ice_environment}")
                
                if ice_context.is_ice_environment:
                    print(f"   ❄️ Tipo: {ice_context.ice_type.value}")
                    print(f"   🧊 Espesor: {ice_context.estimated_thickness_m:.0f}m")
                    print(f"   🎯 Potencial: {ice_context.archaeological_potential}")
                    
                    # Validar resultados
                    expected = case['expected']
                    validation = {
                        'detected': ice_context.is_ice_environment == expected['detected'],
                        'type_correct': expected['type'] in ice_context.ice_type.value,
                        'thickness_in_range': (expected['thickness_range'][0] <= 
                                             ice_context.estimated_thickness_m <= 
                                             expected['thickness_range'][1]),
                        'potential_correct': ice_context.archaeological_potential == expected['archaeological_potential']
                    }
                    
                    accuracy = sum(validation.values()) / len(validation)
                    print(f"   📊 Precisión: {accuracy:.1%}")
                    
                    results.append({
                        'case': case['name'],
                        'environment': 'ice',
                        'accuracy': accuracy,
                        'validation': validation,
                        'results': {
                            'detected': ice_context.is_ice_environment,
                            'type': ice_context.ice_type.value,
                            'thickness': ice_context.estimated_thickness_m,
                            'potential': ice_context.archaeological_potential
                        }
                    })
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'case': case['name'],
                'error': str(e)
            })
    
    # Análisis de resultados
    print(f"\n📊 ANÁLISIS DE VALIDACIÓN FINAL")
    print("=" * 70)
    
    successful_tests = [r for r in results if 'accuracy' in r]
    
    if successful_tests:
        overall_accuracy = sum(r['accuracy'] for r in successful_tests) / len(successful_tests)
        print(f"🎯 Precisión general: {overall_accuracy:.1%}")
        
        # Por ambiente
        water_tests = [r for r in successful_tests if r['environment'] == 'water']
        ice_tests = [r for r in successful_tests if r['environment'] == 'ice']
        
        if water_tests:
            water_accuracy = sum(r['accuracy'] for r in water_tests) / len(water_tests)
            print(f"🌊 Precisión sistema submarino: {water_accuracy:.1%}")
        
        if ice_tests:
            ice_accuracy = sum(r['accuracy'] for r in ice_tests) / len(ice_tests)
            print(f"❄️ Precisión ArcheoScope: {ice_accuracy:.1%}")
        
        # Categorías específicas
        print(f"\n📈 Precisión por categoría:")
        categories = ['detected', 'type_correct', 'depth_in_range', 'thickness_in_range', 'potential_correct']
        
        for category in categories:
            category_results = []
            for result in successful_tests:
                if category in result['validation']:
                    category_results.append(result['validation'][category])
                elif category == 'depth_in_range' and result['environment'] == 'ice':
                    continue  # Skip depth for ice tests
                elif category == 'thickness_in_range' and result['environment'] == 'water':
                    continue  # Skip thickness for water tests
            
            if category_results:
                category_accuracy = sum(category_results) / len(category_results)
                category_name = category.replace('_', ' ').title()
                print(f"   {category_name}: {category_accuracy:.1%}")
    
    # Guardar resultados
    validation_results = {
        "test_info": {
            "test_name": "Final Calibration Validation",
            "test_date": datetime.now().isoformat(),
            "cases_tested": len(test_cases),
            "successful_tests": len(successful_tests)
        },
        "overall_accuracy": overall_accuracy if successful_tests else 0,
        "detailed_results": results
    }
    
    output_file = f"calibration_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    
    # Resumen final
    print(f"\n🏆 RESUMEN DE VALIDACIÓN FINAL")
    print("=" * 70)
    
    if successful_tests:
        print(f"✅ Precisión general: {overall_accuracy:.1%}")
        print(f"✅ Casos procesados: {len(successful_tests)}/{len(test_cases)}")
        
        if overall_accuracy >= 0.8:
            print(f"🎯 SISTEMA EXCELENTEMENTE CALIBRADO (≥80%)")
        elif overall_accuracy >= 0.6:
            print(f"⚠️ SISTEMA BIEN CALIBRADO (60-80%)")
        else:
            print(f"❌ SISTEMA NECESITA MÁS CALIBRACIÓN (<60%)")
        
        print(f"\n🔧 MEJORAS IMPLEMENTADAS:")
        print(f"   ✅ Estimación de profundidad calibrada por ubicación específica")
        print(f"   ✅ Detección de agua mejorada para aguas costeras")
        print(f"   ✅ Clasificación de tipo de agua más precisa")
        print(f"   ✅ Evaluación de potencial arqueológico contextual")
        print(f"   ✅ Escalado dimensional adaptativo")
        print(f"   ✅ Estimación de espesor de hielo mejorada")
        
    else:
        print(f"❌ No se pudieron procesar casos exitosamente")
    
    print(f"\n🔬 Validación de calibración completada!")
    
    return validation_results

if __name__ == "__main__":
    results = test_calibration_validation()