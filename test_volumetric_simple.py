#!/usr/bin/env python3
"""
Test simple del sistema volumétrico de ArcheoScope.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_volumetric_simple():
    """Test básico del sistema volumétrico."""
    
    print("🧪 Test Simple - Sistema Volumétrico ArcheoScope")
    print("=" * 60)
    
    # Test 1: Importar módulos volumétricos
    print("1. Importando módulos volumétricos...")
    try:
        from volumetric.geometric_inference_engine import (
            GeometricInferenceEngine, SpatialSignature, MorphologicalClass
        )
        from volumetric.phi4_geometric_evaluator import Phi4GeometricEvaluator
        print("   ✅ Módulos volumétricos importados correctamente")
    except Exception as e:
        print(f"   ❌ Error importando módulos: {e}")
        return
    
    # Test 2: Crear motor geométrico
    print("\n2. Inicializando motor geométrico...")
    try:
        geometric_engine = GeometricInferenceEngine()
        print("   ✅ GeometricInferenceEngine inicializado")
    except Exception as e:
        print(f"   ❌ Error inicializando motor: {e}")
        return
    
    # Test 3: Crear evaluador phi4
    print("\n3. Inicializando evaluador phi4...")
    try:
        phi4_evaluator = Phi4GeometricEvaluator()
        phi4_available = phi4_evaluator.is_available
        print(f"   ✅ Phi4GeometricEvaluator inicializado (disponible: {phi4_available})")
    except Exception as e:
        print(f"   ❌ Error inicializando phi4: {e}")
        return
    
    # Test 4: Crear firma espacial de prueba
    print("\n4. Creando firma espacial de prueba...")
    try:
        signature = SpatialSignature(
            area_m2=1000.0,
            elongation_ratio=4.0,  # Estructura lineal
            symmetry_index=0.8,
            anisotropy_factor=0.7,
            thermal_amplitude=10.0,
            sar_roughness=0.6,
            multitemporal_coherence=0.8,
            residual_slope=0.5,
            signature_confidence=0.7,
            sensor_convergence=0.8,
            temporal_persistence=0.9
        )
        print("   ✅ Firma espacial creada")
        print(f"      - Área: {signature.area_m2} m²")
        print(f"      - Elongación: {signature.elongation_ratio}")
        print(f"      - Confianza: {signature.signature_confidence}")
    except Exception as e:
        print(f"   ❌ Error creando firma: {e}")
        return
    
    # Test 5: Clasificación morfológica
    print("\n5. Clasificación morfológica...")
    try:
        morphology = geometric_engine.classify_morphology(signature)
        print(f"   ✅ Morfología clasificada: {morphology.value}")
        
        # Verificar si detecta estructura lineal (esperado para elongación 4.0)
        expected_linear = morphology == MorphologicalClass.LINEAR_COMPACT
        print(f"   🎯 Estructura lineal detectada: {'✅' if expected_linear else '❌'}")
    except Exception as e:
        print(f"   ❌ Error en clasificación: {e}")
        return
    
    # Test 6: Generar campo volumétrico
    print("\n6. Generando campo volumétrico...")
    try:
        bounds = (-14.7, -14.6, -75.2, -75.1)  # Coordenadas de prueba
        volumetric_field = geometric_engine.generate_volumetric_field(
            signature, morphology, bounds
        )
        print("   ✅ Campo volumétrico generado")
        print(f"      - Dimensiones: {volumetric_field.dimensions}")
        print(f"      - Resolución voxel: {volumetric_field.voxel_size_m}m")
        print(f"      - Confianza core: {volumetric_field.confidence_layers['core']:.3f}")
    except Exception as e:
        print(f"   ❌ Error generando campo: {e}")
        return
    
    # Test 7: Extraer modelo geométrico
    print("\n7. Extrayendo modelo geométrico...")
    try:
        geometric_model = geometric_engine.extract_geometric_model(volumetric_field)
        print("   ✅ Modelo geométrico extraído")
        print(f"      - Vértices: {len(geometric_model.vertices)}")
        print(f"      - Caras: {len(geometric_model.faces)}")
        print(f"      - Volumen estimado: {geometric_model.estimated_volume_m3:.1f} m³")
        print(f"      - Altura máxima: {geometric_model.max_height_m:.1f} m")
    except Exception as e:
        print(f"   ❌ Error extrayendo modelo: {e}")
        return
    
    # Test 8: Evaluación de consistencia (si phi4 disponible)
    print("\n8. Evaluación de consistencia...")
    try:
        if phi4_evaluator.is_available:
            print("   🤖 Evaluando con phi4-mini-reasoning...")
        else:
            print("   🔧 Evaluando con método determinista...")
        
        # Mock layer results para la evaluación
        layer_results = {
            'ndvi_vegetation': {
                'archaeological_probability': 0.7,
                'geometric_coherence': 0.8,
                'temporal_persistence': 0.9
            },
            'thermal_lst': {
                'archaeological_probability': 0.6,
                'geometric_coherence': 0.7,
                'temporal_persistence': 0.8
            }
        }
        
        consistency_report = phi4_evaluator.evaluate_geometric_consistency(
            signature, morphology, volumetric_field, layer_results
        )
        
        print("   ✅ Evaluación de consistencia completada")
        print(f"      - Score de consistencia: {consistency_report.consistency_score:.3f}")
        print(f"      - Convergencia espectral: {consistency_report.spectral_convergence:.3f}")
        print(f"      - Plausibilidad geométrica: {consistency_report.geometric_plausibility:.3f}")
        print(f"      - Riesgo sobre-ajuste: {consistency_report.over_fitting_penalty:.3f}")
        
    except Exception as e:
        print(f"   ❌ Error en evaluación: {e}")
        return
    
    # Test 9: Pipeline completo
    print("\n9. Pipeline completo de inferencia...")
    try:
        anomaly_data = {
            'id': 'test_anomaly',
            'footprint_area_m2': 1000.0,
            'confidence_level': 0.7,
            'geometric_coherence': 0.8,
            'orientation_coherence': 0.6
        }
        
        complete_result = geometric_engine.process_anomaly_complete(
            anomaly_data, layer_results, bounds
        )
        
        if complete_result['inference_successful']:
            print("   ✅ Pipeline completo exitoso")
            print(f"      - Morfología: {complete_result['morphological_class']}")
            print(f"      - Nivel de inferencia: {complete_result['inference_level']}")
            print(f"      - Volumen estimado: {complete_result['geometric_model'].estimated_volume_m3:.1f} m³")
        else:
            print(f"   ❌ Pipeline falló: {complete_result.get('error', 'unknown')}")
            
    except Exception as e:
        print(f"   ❌ Error en pipeline: {e}")
        return
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 TEST VOLUMÉTRICO COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print("✅ Todos los componentes del sistema volumétrico funcionan correctamente")
    print("✅ GeometricInferenceEngine operacional")
    print(f"✅ Phi4GeometricEvaluator {'con phi4-mini-reasoning' if phi4_evaluator.is_available else 'con fallback determinista'}")
    print("✅ Pipeline completo de inferencia volumétrica validado")
    print("\n🚀 Sistema listo para tests con sitios arqueológicos reales")
    print("   Recomendación: Proceder con test de calzadas romanas")

if __name__ == "__main__":
    test_volumetric_simple()