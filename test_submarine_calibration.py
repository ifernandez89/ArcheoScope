#!/usr/bin/env python3
"""
Test de calibración de arqueología submarina con naufragios reales documentados
Incluye Titanic, Bismarck, Andrea Doria, Costa Concordia y anomalía del Báltico
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import numpy as np

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from water.water_detector import WaterDetector
from water.submarine_archaeology import SubmarineArchaeologyEngine

def test_submarine_calibration():
    """Test de calibración con naufragios reales documentados"""
    
    print("🚢 SUBMARINE ARCHAEOLOGY - TEST DE CALIBRACIÓN CON NAUFRAGIOS REALES")
    print("=" * 75)
    print("Sitios de prueba: Naufragios históricos y anomalías submarinas documentadas")
    print("Objetivo: Calibrar detección volumétrica, clasificación y análisis batimétrico")
    print("=" * 75)
    
    # Sitios de prueba con datos reales de naufragios
    test_wrecks = [
        {
            "name": "RMS Titanic",
            "coordinates": {"lat": 41.7325, "lon": -49.9469},
            "type": "passenger_liner",
            "depth_m": 3800,
            "dimensions": {"length_m": 269.1, "width_m": 28.2, "height_m": 53.3},
            "sunk_year": 1912,
            "material": "steel",
            "condition": "broken_in_two",
            "description": "Transatlántico de pasajeros, estructura de casco grande",
            "validation": "Muy documentado, ideal para validar detección volumétrica",
            "expected_detection": {
                "water_detected": True,
                "water_type": "deep_ocean",
                "depth_range": [3000, 4500],
                "vessel_type": "passenger_liner",
                "historical_period": "modern",
                "preservation_state": "debris_field",
                "archaeological_priority": "high"
            }
        },
        {
            "name": "Battleship Bismarck",
            "coordinates": {"lat": 48.1667, "lon": -16.2},
            "type": "warship",
            "depth_m": 4700,
            "dimensions": {"length_m": 251.0, "width_m": 36.0, "height_m": 50.0},
            "sunk_year": 1941,
            "material": "steel",
            "condition": "upright_intact",
            "description": "Acorazado alemán, geometría lineal clara",
            "validation": "Buen test de penetración sonar y validación geométrica",
            "expected_detection": {
                "water_detected": True,
                "water_type": "deep_ocean",
                "depth_range": [4000, 5000],
                "vessel_type": "warship",
                "historical_period": "modern",
                "preservation_state": "good",
                "archaeological_priority": "high"
            }
        },
        {
            "name": "SS Andrea Doria",
            "coordinates": {"lat": 40.4833, "lon": -69.85},
            "type": "passenger_liner",
            "depth_m": 70,
            "dimensions": {"length_m": 212.0, "width_m": 27.0, "height_m": 30.0},
            "sunk_year": 1956,
            "material": "steel",
            "condition": "listing_deteriorating",
            "description": "Transatlántico italiano, profundidad manejable para ROV",
            "validation": "Ideal para pruebas con ROV y fotogrametría",
            "expected_detection": {
                "water_detected": True,
                "water_type": "coastal",
                "depth_range": [50, 100],
                "vessel_type": "passenger_liner",
                "historical_period": "modern",
                "preservation_state": "poor",
                "archaeological_priority": "medium"
            }
        },
        {
            "name": "Costa Concordia",
            "coordinates": {"lat": 42.4, "lon": 10.9167},
            "type": "cruise_ship",
            "depth_m": 40,
            "dimensions": {"length_m": 290.2, "width_m": 35.5, "height_m": 52.0},
            "sunk_year": 2012,
            "material": "steel",
            "condition": "partially_submerged",
            "description": "Crucero moderno, agua poco profunda",
            "validation": "Testeo en aguas menos profundas, fácil validación visual",
            "expected_detection": {
                "water_detected": True,
                "water_type": "coastal",
                "depth_range": [20, 60],
                "vessel_type": "passenger_liner",
                "historical_period": "modern",
                "preservation_state": "excellent",
                "archaeological_priority": "low"  # Muy reciente
            }
        },
        {
            "name": "Baltic Sea Anomaly",
            "coordinates": {"lat": 59.9167, "lon": 19.7833},
            "type": "geological_formation",
            "depth_m": 90,
            "dimensions": {"diameter_m": 60, "height_m": 8},
            "discovery_year": 2011,
            "material": "rock_sediment",
            "condition": "natural_formation",
            "description": "Formación geológica circular, no artificial",
            "validation": "Test de detección artificial vs natural",
            "expected_detection": {
                "water_detected": True,
                "water_type": "sea",
                "depth_range": [80, 100],
                "vessel_type": None,  # No es un barco
                "historical_period": None,
                "preservation_state": "natural",
                "archaeological_priority": "low"
            }
        },
        {
            "name": "USS Arizona (Pearl Harbor)",
            "coordinates": {"lat": 21.365, "lon": -157.95},
            "type": "battleship",
            "depth_m": 12,
            "dimensions": {"length_m": 185.3, "width_m": 29.6, "height_m": 35.0},
            "sunk_year": 1941,
            "material": "steel",
            "condition": "memorial_site",
            "description": "Acorazado en aguas muy poco profundas",
            "validation": "Test de detección en aguas someras",
            "expected_detection": {
                "water_detected": True,
                "water_type": "coastal",
                "depth_range": [10, 20],
                "vessel_type": "warship",
                "historical_period": "modern",
                "preservation_state": "poor",
                "archaeological_priority": "high"  # Sitio memorial
            }
        }
    ]
    
    water_detector = WaterDetector()
    submarine_engine = SubmarineArchaeologyEngine()
    
    results = []
    
    print(f"\n🧪 EJECUTANDO TESTS DE CALIBRACIÓN SUBMARINA...")
    print("=" * 75)
    
    for i, wreck in enumerate(test_wrecks, 1):
        print(f"\n🚢 TEST {i}/6: {wreck['name']}")
        print(f"   Coordenadas: {wreck['coordinates']['lat']:.4f}, {wreck['coordinates']['lon']:.4f}")
        print(f"   Tipo: {wreck['type'].replace('_', ' ').title()}")
        print(f"   Profundidad: {wreck['depth_m']}m")
        print(f"   Dimensiones: {wreck['dimensions']}")
        
        try:
            # Detectar contexto de agua
            water_context = water_detector.detect_water_context(
                wreck['coordinates']['lat'], 
                wreck['coordinates']['lon']
            )
            
            print(f"   ✅ Agua detectada: {water_context.is_water}")
            
            if water_context.is_water:
                print(f"   🌊 Tipo detectado: {water_context.water_type.value}")
                print(f"   🏊 Profundidad estimada: {water_context.estimated_depth_m:.0f}m")
                print(f"   🎯 Potencial arqueológico: {water_context.archaeological_potential}")
                print(f"   🚢 Rutas históricas: {'Sí' if water_context.historical_shipping_routes else 'No'}")
                print(f"   ⚓ Naufragios conocidos: {'Sí' if water_context.known_wrecks_nearby else 'No'}")
                
                # Análisis arqueológico submarino
                bounds = (
                    wreck['coordinates']['lat'] - 0.01,
                    wreck['coordinates']['lat'] + 0.01,
                    wreck['coordinates']['lon'] - 0.01,
                    wreck['coordinates']['lon'] + 0.01
                )
                
                submarine_results = submarine_engine.analyze_submarine_area(water_context, bounds)
                print(f"   🔍 Instrumentos: {len(submarine_results['instruments_used'])}")
                print(f"   📊 Candidatos detectados: {len(submarine_results['wreck_candidates'])}")
                
                # Analizar candidatos detectados
                if submarine_results['wreck_candidates']:
                    best_candidate = submarine_results['wreck_candidates'][0]  # Primer candidato
                    candidate_signature = best_candidate['signature']
                    
                    print(f"   🎯 Mejor candidato:")
                    print(f"      - Longitud detectada: {candidate_signature['length_m']:.1f}m")
                    print(f"      - Anchura detectada: {candidate_signature['width_m']:.1f}m")
                    print(f"      - Tipo más probable: {max(best_candidate['vessel_type_probability'], key=best_candidate['vessel_type_probability'].get)}")
                    print(f"      - Confianza: {candidate_signature['detection_confidence']:.2f}")
            
            # Validar contra datos esperados
            expected = wreck['expected_detection']
            validation_results = {}
            
            # Validar detección de agua
            validation_results['water_detected'] = water_context.is_water == expected['water_detected']
            
            # Validar tipo de agua
            if water_context.water_type:
                validation_results['water_type_correct'] = expected['water_type'] in water_context.water_type.value
            else:
                validation_results['water_type_correct'] = False
            
            # Validar profundidad (rango aproximado)
            if water_context.estimated_depth_m:
                depth_in_range = (expected['depth_range'][0] <= 
                                water_context.estimated_depth_m <= 
                                expected['depth_range'][1])
                validation_results['depth_reasonable'] = depth_in_range
            else:
                validation_results['depth_reasonable'] = False
            
            # Validar potencial arqueológico
            validation_results['archaeological_potential_correct'] = (
                water_context.archaeological_potential == expected['archaeological_priority']
            )
            
            # Validar detección de naufragios (si aplica)
            if expected['vessel_type'] and submarine_results['wreck_candidates']:
                # Verificar si se detectó el tipo correcto de embarcación
                best_candidate = submarine_results['wreck_candidates'][0]
                vessel_probs = best_candidate['vessel_type_probability']
                
                # Mapear tipos esperados a tipos detectados
                type_mapping = {
                    'passenger_liner': ['passenger_liner', 'cargo_ship'],
                    'warship': ['warship'],
                    'cruise_ship': ['passenger_liner', 'yacht'],
                    'battleship': ['warship']
                }
                
                expected_types = type_mapping.get(wreck['type'], [wreck['type']])
                detected_correctly = any(vessel_type in vessel_probs and vessel_probs[vessel_type] > 0.3 
                                       for vessel_type in expected_types)
                validation_results['vessel_type_correct'] = detected_correctly
                
                # Validar dimensiones (tolerancia del 50%)
                real_length = wreck['dimensions']['length_m']
                detected_length = best_candidate['signature']['length_m']
                length_error = abs(detected_length - real_length) / real_length
                validation_results['dimensions_reasonable'] = length_error < 0.5
                
            else:
                validation_results['vessel_type_correct'] = expected['vessel_type'] is None
                validation_results['dimensions_reasonable'] = True
            
            # Calcular precisión general
            accuracy = sum(validation_results.values()) / len(validation_results)
            
            print(f"   🎯 Precisión: {accuracy:.1%}")
            print(f"      - Agua detectada: {'✅' if validation_results['water_detected'] else '❌'}")
            print(f"      - Tipo de agua: {'✅' if validation_results['water_type_correct'] else '❌'}")
            print(f"      - Profundidad razonable: {'✅' if validation_results['depth_reasonable'] else '❌'}")
            print(f"      - Potencial arqueológico: {'✅' if validation_results['archaeological_potential_correct'] else '❌'}")
            print(f"      - Tipo de embarcación: {'✅' if validation_results['vessel_type_correct'] else '❌'}")
            print(f"      - Dimensiones razonables: {'✅' if validation_results['dimensions_reasonable'] else '❌'}")
            
            # Guardar resultados
            wreck_result = {
                "wreck_name": wreck['name'],
                "coordinates": wreck['coordinates'],
                "wreck_type": wreck['type'],
                "real_data": wreck,
                "detection_results": {
                    "water_detected": water_context.is_water,
                    "water_type": water_context.water_type.value if water_context.water_type else None,
                    "estimated_depth_m": water_context.estimated_depth_m,
                    "archaeological_potential": water_context.archaeological_potential,
                    "historical_shipping_routes": water_context.historical_shipping_routes,
                    "known_wrecks_nearby": water_context.known_wrecks_nearby,
                    "confidence": water_context.confidence
                },
                "submarine_analysis": {
                    "performed": True,
                    "candidates": len(submarine_results['wreck_candidates']),
                    "instruments": len(submarine_results['instruments_used']),
                    "best_candidate": submarine_results['wreck_candidates'][0] if submarine_results['wreck_candidates'] else None
                },
                "validation": validation_results,
                "accuracy": accuracy
            }
            
            results.append(wreck_result)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "wreck_name": wreck['name'],
                "error": str(e)
            })
    
    # Análisis de resultados generales
    print(f"\n📊 ANÁLISIS DE RESULTADOS DE CALIBRACIÓN SUBMARINA")
    print("=" * 75)
    
    successful_tests = [r for r in results if 'accuracy' in r]
    
    if successful_tests:
        # Precisión general
        overall_accuracy = np.mean([r['accuracy'] for r in successful_tests])
        print(f"🎯 Precisión general del sistema: {overall_accuracy:.1%}")
        
        # Análisis por categoría
        categories = ['water_detected', 'water_type_correct', 'depth_reasonable', 
                     'archaeological_potential_correct', 'vessel_type_correct', 'dimensions_reasonable']
        
        print(f"\n📈 Precisión por categoría:")
        for category in categories:
            category_accuracy = np.mean([r['validation'][category] for r in successful_tests])
            category_name = category.replace('_', ' ').title()
            print(f"   {category_name}: {category_accuracy:.1%}")
        
        # Análisis por profundidad
        shallow_wrecks = [r for r in successful_tests if r['real_data']['depth_m'] < 100]
        deep_wrecks = [r for r in successful_tests if r['real_data']['depth_m'] >= 100]
        
        if shallow_wrecks:
            shallow_accuracy = np.mean([r['accuracy'] for r in shallow_wrecks])
            print(f"\n🏊 Precisión en aguas someras (<100m): {shallow_accuracy:.1%} ({len(shallow_wrecks)} sitios)")
        
        if deep_wrecks:
            deep_accuracy = np.mean([r['accuracy'] for r in deep_wrecks])
            print(f"🌊 Precisión en aguas profundas (≥100m): {deep_accuracy:.1%} ({len(deep_wrecks)} sitios)")
        
        # Análisis por tipo de embarcación
        vessel_types = {}
        for result in successful_tests:
            vessel_type = result['real_data']['type']
            if vessel_type not in vessel_types:
                vessel_types[vessel_type] = []
            vessel_types[vessel_type].append(result['accuracy'])
        
        print(f"\n🚢 Precisión por tipo de embarcación:")
        for vessel_type, accuracies in vessel_types.items():
            avg_accuracy = np.mean(accuracies)
            print(f"   {vessel_type.replace('_', ' ').title()}: {avg_accuracy:.1%} ({len(accuracies)} casos)")
        
        # Detecciones exitosas
        successful_detections = sum(1 for r in successful_tests if r['validation']['water_detected'])
        wreck_detections = sum(1 for r in successful_tests if r['submarine_analysis']['candidates'] > 0)
        print(f"\n✅ Detecciones de agua exitosas: {successful_detections}/{len(successful_tests)}")
        print(f"⚓ Detecciones de naufragios: {wreck_detections}/{len(successful_tests)}")
        
        # Análisis de dimensiones
        dimension_errors = []
        for result in successful_tests:
            if result['submarine_analysis']['best_candidate'] and 'dimensions' in result['real_data']:
                dimensions = result['real_data']['dimensions']
                if 'length_m' in dimensions:
                    real_length = dimensions['length_m']
                    detected_length = result['submarine_analysis']['best_candidate']['signature']['length_m']
                    error_ratio = abs(detected_length - real_length) / real_length
                    dimension_errors.append(error_ratio)
        
        if dimension_errors:
            avg_dimension_error = np.mean(dimension_errors)
            print(f"📏 Error promedio en dimensiones: {avg_dimension_error:.1%}")
    
    # Recomendaciones de calibración
    print(f"\n🔧 RECOMENDACIONES DE CALIBRACIÓN SUBMARINA")
    print("=" * 75)
    
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
        
        # Análisis de profundidad
        if 'depth_reasonable' in [cat.replace(' ', '_').lower() for cat in weak_categories]:
            print(f"   - Calibrar estimación de profundidad para diferentes tipos de agua")
        
        # Análisis de detección de embarcaciones
        detection_rate = wreck_detections / len(successful_tests)
        if detection_rate < 0.8:
            print(f"   - Mejorar detección de anomalías volumétricas (tasa actual: {detection_rate:.1%})")
        
        # Análisis por profundidad
        if shallow_wrecks and deep_wrecks:
            if abs(shallow_accuracy - deep_accuracy) > 0.2:
                print(f"   - Balancear precisión entre aguas someras y profundas")
    
    # Guardar resultados completos
    print(f"\n💾 GUARDANDO RESULTADOS DE CALIBRACIÓN SUBMARINA...")
    
    calibration_results = {
        "test_info": {
            "test_name": "Submarine Archaeology Calibration with Real Wrecks",
            "test_date": datetime.now().isoformat(),
            "wrecks_tested": len(test_wrecks),
            "successful_tests": len(successful_tests)
        },
        "overall_metrics": {
            "overall_accuracy": overall_accuracy if successful_tests else 0,
            "successful_detections": successful_detections if successful_tests else 0,
            "wreck_detections": wreck_detections if successful_tests else 0,
            "total_wrecks": len(test_wrecks)
        },
        "detailed_results": results,
        "calibration_recommendations": weak_categories if successful_tests else []
    }
    
    output_file = f"submarine_calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(calibration_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultados guardados en: {output_file}")
    
    # Resumen final
    print(f"\n🏆 RESUMEN DE CALIBRACIÓN ARQUEOLOGÍA SUBMARINA")
    print("=" * 75)
    
    if successful_tests:
        print(f"✅ Precisión general: {overall_accuracy:.1%}")
        print(f"✅ Naufragios procesados exitosamente: {len(successful_tests)}/{len(test_wrecks)}")
        print(f"✅ Detecciones de agua correctas: {successful_detections}/{len(successful_tests)}")
        print(f"⚓ Detecciones de naufragios: {wreck_detections}/{len(successful_tests)}")
        
        if overall_accuracy >= 0.8:
            print(f"🎯 SISTEMA BIEN CALIBRADO (≥80% precisión)")
        elif overall_accuracy >= 0.6:
            print(f"⚠️ SISTEMA NECESITA AJUSTES (60-80% precisión)")
        else:
            print(f"❌ SISTEMA NECESITA RECALIBRACIÓN (<60% precisión)")
    else:
        print(f"❌ No se pudieron procesar naufragios exitosamente")
    
    print(f"\n🚢 Calibración de arqueología submarina completada!")
    
    return calibration_results

if __name__ == "__main__":
    results = test_submarine_calibration()