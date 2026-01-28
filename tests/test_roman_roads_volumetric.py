#!/usr/bin/env python3
"""
Test Específico: Calzadas Romanas Enterradas - Inferencia Volumétrica

🥇 CASO IDEAL PARA ARCHEOSCOPE:
- Geometría clara (rectas largas, intersecciones)
- Totalmente enterradas en muchos tramos
- Detectables por: NDVI desacoplado, SAR backscatter, compactación persistente, amplitud térmica
- No requieren altura monumental
- Hay validación histórica clara

OBJETIVO: Demostrar que "ArcheoScope detecta caminos romanos sin saberlo"

SITIOS DE TESTING:
1. Vía Appia (Italia) - Tramo enterrado cerca de Roma
2. Vía Augusta (España) - Tramo en Cataluña
3. Red romana en Galia (Francia) - Intersecciones enterradas
4. Calzada romana en Germania (Alemania) - Limes fronterizo

VALIDACIÓN: Si ArcheoScope detecta geometría lineal persistente con las características
esperadas de compactación y desacople vegetal, el sistema funciona correctamente.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import numpy as np
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_roman_roads_volumetric():
    """Test específico para calzadas romanas enterradas."""
    
    print("🏛️ ARCHEOSCOPE - TEST CALZADAS ROMANAS ENTERRADAS")
    print("=" * 70)
    print("🎯 OBJETIVO: Detectar geometría lineal sin saber que son caminos romanos")
    print("🔬 PARADIGMA: 'ArcheoScope detecta caminos romanos sin saberlo'")
    print("=" * 70)
    
    # Importar sistema
    try:
        from api.main import (
            initialize_system, system_components, RegionRequest,
            create_archaeological_region_data, perform_spatial_anomaly_analysis,
            perform_archaeological_evaluation, generate_volumetric_inference,
            calculate_area_km2
        )
        print("✅ Sistema ArcheoScope importado correctamente")
        
    except ImportError as e:
        print(f"❌ Error importando sistema: {e}")
        return
    
    # Inicializar sistema
    print("\n🔧 Inicializando sistema...")
    success = initialize_system()
    if not success:
        print("❌ Fallo en inicialización")
        return
    
    geometric_engine = system_components.get('geometric_engine')
    phi4_evaluator = system_components.get('phi4_evaluator')
    
    print(f"✅ Sistema inicializado")
    print(f"   - Motor geométrico: {'✅' if geometric_engine else '❌'}")
    print(f"   - Evaluador phi4: {'✅' if phi4_evaluator and phi4_evaluator.is_available else '⚠️ Determinista'}")
    
    # CASOS DE CALZADAS ROMANAS
    roman_road_cases = [
        {
            "id": "via_appia_buried",
            "name": "Vía Appia - Tramo Enterrado",
            "description": "Tramo de la Vía Appia enterrado cerca de Roma",
            "coordinates": {
                "lat_min": 41.8520, "lat_max": 41.8580,  # Sur de Roma
                "lon_min": 12.5120, "lon_max": 12.5180
            },
            "resolution_m": 300,
            "historical_context": {
                "construction_period": "312 BCE",
                "width_m": 4.1,  # Ancho estándar romano
                "construction": "polygonal_stone_base_with_gravel",
                "depth_m": 1.5,  # Profundidad típica
                "orientation": "SE-NW"  # Orientación hacia Brindisi
            },
            "expected_signatures": {
                "ndvi_decoupling": "vegetation_stress_over_compacted_substrate",
                "thermal_amplitude": "higher_thermal_inertia_stone_base",
                "sar_backscatter": "increased_roughness_buried_stones",
                "geometric_coherence": "linear_persistent_anomaly"
            }
        },
        {
            "id": "via_augusta_catalonia",
            "name": "Vía Augusta - Cataluña",
            "description": "Tramo enterrado de Vía Augusta en Cataluña",
            "coordinates": {
                "lat_min": 41.3900, "lat_max": 41.3960,  # Cerca de Barcelona
                "lon_min": 2.1500, "lon_max": 2.1560
            },
            "resolution_m": 250,
            "historical_context": {
                "construction_period": "218 BCE",
                "width_m": 4.5,
                "construction": "stone_slabs_with_mortar",
                "depth_m": 1.2,
                "orientation": "N-S"  # Siguiendo la costa
            },
            "expected_signatures": {
                "ndvi_decoupling": "linear_vegetation_anomaly",
                "thermal_amplitude": "thermal_contrast_buried_road",
                "sar_backscatter": "linear_roughness_signature",
                "geometric_coherence": "high_linearity_persistence"
            }
        },
        {
            "id": "gallic_road_intersection",
            "name": "Red Romana Galia - Intersección",
            "description": "Intersección de caminos romanos enterrados en Galia",
            "coordinates": {
                "lat_min": 46.7800, "lat_max": 46.7860,  # Centro de Francia
                "lon_min": 4.8400, "lon_max": 4.8460
            },
            "resolution_m": 400,
            "historical_context": {
                "construction_period": "50 BCE",
                "width_m": 3.8,
                "construction": "gravel_and_stone_foundation",
                "depth_m": 1.0,
                "orientation": "intersection_cross_pattern"
            },
            "expected_signatures": {
                "ndvi_decoupling": "cross_pattern_vegetation_stress",
                "thermal_amplitude": "intersection_thermal_signature",
                "sar_backscatter": "orthogonal_linear_features",
                "geometric_coherence": "high_geometric_regularity"
            }
        },
        {
            "id": "limes_germanicus",
            "name": "Limes Germanicus - Calzada Fronteriza",
            "description": "Calzada romana del Limes en Germania",
            "coordinates": {
                "lat_min": 50.0800, "lat_max": 50.0860,  # Renania, Alemania
                "lon_min": 7.1200, "lon_max": 7.1260
            },
            "resolution_m": 350,
            "historical_context": {
                "construction_period": "85 CE",
                "width_m": 3.5,
                "construction": "timber_and_gravel_military_road",
                "depth_m": 0.8,
                "orientation": "E-W"  # Siguiendo el Limes
            },
            "expected_signatures": {
                "ndvi_decoupling": "military_road_compaction_signature",
                "thermal_amplitude": "moderate_thermal_contrast",
                "sar_backscatter": "linear_compaction_feature",
                "geometric_coherence": "military_precision_geometry"
            }
        }
    ]
    
    # Ejecutar tests para cada calzada romana
    results = []
    
    for i, case in enumerate(roman_road_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/4: {case['name']}")
        print(f"{'='*70}")
        print(f"📍 Ubicación: {case['description']}")
        print(f"🏛️ Contexto histórico: {case['historical_context']['construction_period']}")
        print(f"📏 Ancho esperado: {case['historical_context']['width_m']}m")
        print(f"📐 Orientación: {case['historical_context']['orientation']}")
        
        try:
            # Crear request
            class MockRequest:
                def __init__(self, coords, resolution):
                    self.region_name = case['name']
                    self.lat_min = coords['lat_min']
                    self.lat_max = coords['lat_max']
                    self.lon_min = coords['lon_min']
                    self.lon_max = coords['lon_max']
                    self.resolution_m = resolution
                    self.layers_to_analyze = [
                        "ndvi_vegetation", "thermal_lst", "sar_backscatter", 
                        "surface_roughness", "soil_salinity"
                    ]
                    self.active_rules = ["all"]
            
            request = MockRequest(case['coordinates'], case['resolution_m'])
            
            print(f"\n📊 Análisis de área:")
            area_km2 = calculate_area_km2(request)
            print(f"   - Área total: {area_km2:.3f} km²")
            print(f"   - Resolución: {request.resolution_m}m")
            
            # Análisis completo
            print(f"\n🔍 Ejecutando análisis arqueológico...")
            
            # 1. Crear datos
            datasets = create_archaeological_region_data(request)
            print(f"   ✅ Datasets: {len(datasets)} capas espectrales")
            
            # 2. Análisis espacial
            spatial_results = perform_spatial_anomaly_analysis(datasets, request.layers_to_analyze)
            
            # Evaluar firmas esperadas para calzadas romanas
            print(f"\n🛣️ EVALUACIÓN DE FIRMAS DE CALZADA ROMANA:")
            
            # NDVI desacoplado (vegetación estresada sobre sustrato compactado)
            ndvi_result = spatial_results.get('ndvi_vegetation', {})
            ndvi_prob = ndvi_result.get('archaeological_probability', 0)
            ndvi_coherence = ndvi_result.get('geometric_coherence', 0)
            
            print(f"   🌱 NDVI Desacoplado:")
            print(f"      - Probabilidad arqueológica: {ndvi_prob:.3f}")
            print(f"      - Coherencia geométrica: {ndvi_coherence:.3f}")
            print(f"      - Indicativo de compactación: {'✅' if ndvi_prob > 0.5 and ndvi_coherence > 0.6 else '❌'}")
            
            # Amplitud térmica (inercia térmica de base de piedra)
            thermal_result = spatial_results.get('thermal_lst', {})
            thermal_prob = thermal_result.get('archaeological_probability', 0)
            thermal_persistence = thermal_result.get('temporal_persistence', 0)
            
            print(f"   🌡️ Amplitud Térmica:")
            print(f"      - Probabilidad arqueológica: {thermal_prob:.3f}")
            print(f"      - Persistencia temporal: {thermal_persistence:.3f}")
            print(f"      - Inercia térmica detectada: {'✅' if thermal_prob > 0.4 and thermal_persistence > 0.6 else '❌'}")
            
            # SAR backscatter (rugosidad de piedras enterradas)
            sar_result = spatial_results.get('sar_backscatter', {})
            sar_prob = sar_result.get('archaeological_probability', 0)
            sar_coherence = sar_result.get('geometric_coherence', 0)
            
            print(f"   📡 SAR Backscatter:")
            print(f"      - Probabilidad arqueológica: {sar_prob:.3f}")
            print(f"      - Coherencia geométrica: {sar_coherence:.3f}")
            print(f"      - Rugosidad lineal detectada: {'✅' if sar_prob > 0.4 and sar_coherence > 0.5 else '❌'}")
            
            # 3. Evaluación de reglas arqueológicas
            archaeological_results = perform_archaeological_evaluation(datasets, request.active_rules)
            contradictions = archaeological_results.get('contradictions', [])
            
            print(f"\n⚖️ Reglas arqueológicas activadas: {len(contradictions)}")
            for contradiction in contradictions:
                rule_name = contradiction.get('rule', 'unknown')
                rule_prob = contradiction.get('archaeological_probability', 0)
                print(f"   - {rule_name}: {rule_prob:.3f}")
            
            # 4. INFERENCIA VOLUMÉTRICA ESPECÍFICA PARA CALZADAS
            print(f"\n🏗️ INFERENCIA VOLUMÉTRICA DE CALZADA ROMANA...")
            
            volumetric_inference = generate_volumetric_inference(
                spatial_results, archaeological_results, request
            )
            
            if volumetric_inference.get('volumetric_model_available', False):
                print(f"   ✅ INFERENCIA VOLUMÉTRICA EXITOSA")
                
                # Análisis específico para calzadas
                summary = volumetric_inference['analysis_summary']
                footprints = volumetric_inference['footprint_analysis']['2d_footprints']
                morphologies = volumetric_inference['footprint_analysis']['morphological_classification']
                
                print(f"\n   📊 Resultados volumétricos:")
                print(f"      - Anomalías procesadas: {summary['successful_inferences']}")
                print(f"      - Volumen total: {summary['total_estimated_volume_m3']:.1f} m³")
                print(f"      - Cobertura: {summary['area_coverage_percentage']:.2f}%")
                
                # Verificar detección de estructura lineal
                linear_detected = 'estructura_lineal_compactada' in morphologies
                print(f"\n   🛣️ DETECCIÓN DE ESTRUCTURA LINEAL:")
                print(f"      - Estructura lineal detectada: {'✅ SÍ' if linear_detected else '❌ NO'}")
                
                if linear_detected:
                    linear_count = morphologies['estructura_lineal_compactada']
                    print(f"      - Cantidad de estructuras lineales: {linear_count}")
                    
                    # Analizar características de las estructuras lineales
                    linear_footprints = [fp for fp in footprints if fp.get('morphological_class') == 'estructura_lineal_compactada']
                    
                    for j, fp in enumerate(linear_footprints):
                        print(f"      - Estructura lineal {j+1}:")
                        print(f"        * Área: {fp['area_m2']:.0f} m²")
                        print(f"        * Volumen estimado: {fp['estimated_volume_m3']:.1f} m³")
                        print(f"        * Altura máxima: {fp['max_height_m']:.1f} m")
                        print(f"        * Confianza: {fp['confidence_level']:.3f}")
                        
                        # Estimar dimensiones de calzada
                        area_m2 = fp['area_m2']
                        # Asumir estructura lineal con ratio 10:1 (longitud:ancho)
                        estimated_width = np.sqrt(area_m2 / 10)
                        estimated_length = area_m2 / estimated_width
                        
                        print(f"        * Dimensiones estimadas: {estimated_length:.0f}m x {estimated_width:.1f}m")
                        
                        # Comparar con dimensiones históricas esperadas
                        expected_width = case['historical_context']['width_m']
                        width_match = abs(estimated_width - expected_width) / expected_width < 0.5  # ±50%
                        
                        print(f"        * Ancho esperado: {expected_width}m")
                        print(f"        * Coincidencia dimensional: {'✅' if width_match else '❌'}")
                
                # Evaluación phi4 (si disponible)
                phi4_analysis = volumetric_inference.get('phi4_geometric_evaluation')
                if phi4_analysis:
                    print(f"\n   🤖 Evaluación phi4:")
                    print(f"      - Consistencia: {phi4_analysis['mean_consistency_score']:.3f}")
                    print(f"      - Anti-pareidolia: {'✅' if phi4_analysis['anti_pareidolia_active'] else '❌'}")
                
                # VALIDACIÓN ESPECÍFICA PARA CALZADAS ROMANAS
                print(f"\n   ✅ VALIDACIÓN CALZADA ROMANA:")
                
                validation_score = 0
                validation_total = 6
                
                # 1. Estructura lineal detectada
                if linear_detected:
                    validation_score += 1
                    print(f"      ✅ Estructura lineal detectada")
                else:
                    print(f"      ❌ Estructura lineal NO detectada")
                
                # 2. NDVI desacoplado significativo
                if ndvi_prob > 0.5 and ndvi_coherence > 0.6:
                    validation_score += 1
                    print(f"      ✅ NDVI desacoplado significativo")
                else:
                    print(f"      ❌ NDVI desacoplado insuficiente")
                
                # 3. Amplitud térmica detectada
                if thermal_prob > 0.4 and thermal_persistence > 0.6:
                    validation_score += 1
                    print(f"      ✅ Amplitud térmica detectada")
                else:
                    print(f"      ❌ Amplitud térmica insuficiente")
                
                # 4. SAR backscatter coherente
                if sar_prob > 0.4 and sar_coherence > 0.5:
                    validation_score += 1
                    print(f"      ✅ SAR backscatter coherente")
                else:
                    print(f"      ❌ SAR backscatter insuficiente")
                
                # 5. Coherencia geométrica general alta
                mean_coherence = np.mean([r.get('geometric_coherence', 0) for r in spatial_results.values()])
                if mean_coherence > 0.6:
                    validation_score += 1
                    print(f"      ✅ Coherencia geométrica alta ({mean_coherence:.3f})")
                else:
                    print(f"      ❌ Coherencia geométrica baja ({mean_coherence:.3f})")
                
                # 6. Persistencia temporal alta
                mean_persistence = np.mean([r.get('temporal_persistence', 0) for r in spatial_results.values()])
                if mean_persistence > 0.7:
                    validation_score += 1
                    print(f"      ✅ Persistencia temporal alta ({mean_persistence:.3f})")
                else:
                    print(f"      ❌ Persistencia temporal baja ({mean_persistence:.3f})")
                
                validation_percentage = validation_score / validation_total
                print(f"\n   🏆 SCORE VALIDACIÓN: {validation_score}/{validation_total} ({validation_percentage:.1%})")
                
                # Resultado del test
                test_result = {
                    "case_id": case['id'],
                    "case_name": case['name'],
                    "detection_successful": linear_detected,
                    "validation_score": validation_percentage,
                    "signatures_detected": {
                        "ndvi_decoupling": ndvi_prob > 0.5 and ndvi_coherence > 0.6,
                        "thermal_amplitude": thermal_prob > 0.4 and thermal_persistence > 0.6,
                        "sar_backscatter": sar_prob > 0.4 and sar_coherence > 0.5,
                        "geometric_coherence": mean_coherence > 0.6,
                        "temporal_persistence": mean_persistence > 0.7
                    },
                    "volumetric_results": {
                        "total_volume_m3": summary['total_estimated_volume_m3'],
                        "area_coverage_percent": summary['area_coverage_percentage'],
                        "linear_structures_detected": morphologies.get('estructura_lineal_compactada', 0)
                    },
                    "historical_validation": {
                        "expected_width_m": case['historical_context']['width_m'],
                        "expected_depth_m": case['historical_context']['depth_m'],
                        "construction_period": case['historical_context']['construction_period']
                    },
                    "phi4_consistency": phi4_analysis['mean_consistency_score'] if phi4_analysis else None
                }
                
                if validation_percentage >= 0.7:
                    print(f"   🎯 RESULTADO: ✅ CALZADA ROMANA DETECTADA EXITOSAMENTE")
                elif validation_percentage >= 0.5:
                    print(f"   🎯 RESULTADO: ⚠️ DETECCIÓN PARCIAL - REQUIERE VALIDACIÓN")
                else:
                    print(f"   🎯 RESULTADO: ❌ DETECCIÓN FALLIDA")
                
            else:
                print(f"   ❌ INFERENCIA VOLUMÉTRICA FALLIDA")
                reason = volumetric_inference.get('reason', 'Desconocida')
                print(f"   💭 Razón: {reason}")
                
                test_result = {
                    "case_id": case['id'],
                    "case_name": case['name'],
                    "detection_successful": False,
                    "failure_reason": reason,
                    "validation_score": 0.0
                }
            
            results.append(test_result)
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            
            results.append({
                "case_id": case['id'],
                "case_name": case['name'],
                "detection_successful": False,
                "error": str(e),
                "validation_score": 0.0
            })
    
    # RESUMEN FINAL
    print(f"\n{'='*70}")
    print("🏆 RESUMEN - TEST CALZADAS ROMANAS")
    print(f"{'='*70}")
    
    successful_detections = len([r for r in results if r.get('detection_successful', False)])
    high_validation_scores = len([r for r in results if r.get('validation_score', 0) >= 0.7])
    
    print(f"📊 Calzadas analizadas: {len(results)}")
    print(f"📊 Estructuras lineales detectadas: {successful_detections}/{len(results)}")
    print(f"📊 Validaciones exitosas (≥70%): {high_validation_scores}/{len(results)}")
    
    # Análisis por caso
    print(f"\n🛣️ ANÁLISIS POR CALZADA:")
    for result in results:
        name = result['case_name']
        detected = result.get('detection_successful', False)
        score = result.get('validation_score', 0)
        
        status = "✅" if detected and score >= 0.7 else "⚠️" if detected else "❌"
        print(f"   {status} {name}: {score:.1%} validación")
        
        if 'signatures_detected' in result:
            signatures = result['signatures_detected']
            detected_count = sum(signatures.values())
            print(f"      - Firmas detectadas: {detected_count}/5")
            
        if 'volumetric_results' in result:
            vol_results = result['volumetric_results']
            linear_count = vol_results.get('linear_structures_detected', 0)
            if linear_count > 0:
                print(f"      - Estructuras lineales: {linear_count}")
    
    # Evaluación del paradigma
    print(f"\n🧪 EVALUACIÓN DEL PARADIGMA:")
    print(f"   'ArcheoScope detecta caminos romanos sin saberlo'")
    
    paradigm_success = successful_detections >= 2  # Al menos 50% de éxito
    geometric_detection = any(r.get('signatures_detected', {}).get('geometric_coherence', False) for r in results)
    temporal_persistence = any(r.get('signatures_detected', {}).get('temporal_persistence', False) for r in results)
    
    print(f"   {'✅' if paradigm_success else '❌'} Detección ciega de geometría lineal")
    print(f"   {'✅' if geometric_detection else '❌'} Coherencia geométrica detectada")
    print(f"   {'✅' if temporal_persistence else '❌'} Persistencia temporal verificada")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"archeoscope_roman_roads_test_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_metadata": {
                "timestamp": timestamp,
                "test_type": "roman_roads_volumetric_inference",
                "paradigm": "detect_geometry_without_knowing_what_it_is",
                "target_morphology": "estructura_lineal_compactada"
            },
            "test_cases": roman_road_cases,
            "results": results,
            "summary": {
                "total_cases": len(results),
                "successful_detections": successful_detections,
                "high_validation_scores": high_validation_scores,
                "paradigm_validated": paradigm_success
            }
        }, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {results_file}")
    
    if paradigm_success:
        print(f"\n🎉 ¡PARADIGMA VALIDADO!")
        print(f"   ArcheoScope detecta geometría de calzadas romanas sin conocimiento previo")
        print(f"   Sistema listo para casos más complejos (Teotihuacán, Nazca, Tells)")
    else:
        print(f"\n⚠️ Paradigma requiere ajustes")
        print(f"   Revisar detección de estructuras lineales y firmas espectrales")
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    test_roman_roads_volumetric()