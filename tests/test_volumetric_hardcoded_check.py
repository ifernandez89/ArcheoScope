#!/usr/bin/env python3
"""
Test para verificar valores hardcodeados en la generación volumétrica 3D
"""

import sys
sys.path.append('backend')
import numpy as np
import json
from backend.volumetric.geometric_inference_engine import GeometricInferenceEngine, SpatialSignature, MorphologicalClass

def test_hardcoded_values():
    """Verificar si hay valores hardcodeados en la generación 3D"""
    
    print("🔍 REVISIÓN COMPLETA DEL ENGINE VOLUMÉTRICO")
    print("=" * 60)
    
    engine = GeometricInferenceEngine()
    
    # 1. Verificar valores hardcodeados del motor
    print("\n1. VALORES HARDCODEADOS DETECTADOS:")
    print(f"   ❌ Resolución voxel: {engine.voxel_resolution_m}m (hardcodeado)")
    print(f"   ❌ Umbral confianza: {engine.confidence_threshold} (hardcodeado)")
    print(f"   ❌ Nivel inferencia: {engine.inference_level.value} (hardcodeado)")
    
    # 2. Test de variabilidad morfológica
    print("\n2. TEST DE VARIABILIDAD MORFOLÓGICA:")
    
    test_cases = [
        ("Pequeña simétrica", SpatialSignature(
            area_m2=500.0, elongation_ratio=1.2, symmetry_index=0.9,
            anisotropy_factor=0.3, thermal_amplitude=3.0, sar_roughness=0.6,
            multitemporal_coherence=0.8, residual_slope=0.4,
            signature_confidence=0.8, sensor_convergence=0.7, temporal_persistence=0.8
        )),
        ("Lineal alargada", SpatialSignature(
            area_m2=2000.0, elongation_ratio=5.0, symmetry_index=0.4,
            anisotropy_factor=0.9, thermal_amplitude=2.0, sar_roughness=0.5,
            multitemporal_coherence=0.6, residual_slope=0.6,
            signature_confidence=0.6, sensor_convergence=0.6, temporal_persistence=0.6
        )),
        ("Grande compleja", SpatialSignature(
            area_m2=8000.0, elongation_ratio=1.8, symmetry_index=0.6,
            anisotropy_factor=0.9, thermal_amplitude=8.0, sar_roughness=0.8,
            multitemporal_coherence=0.8, residual_slope=0.7,
            signature_confidence=0.9, sensor_convergence=0.8, temporal_persistence=0.9
        )),
        ("Cavidad térmica", SpatialSignature(
            area_m2=1200.0, elongation_ratio=1.5, symmetry_index=0.5,
            anisotropy_factor=0.4, thermal_amplitude=12.0, sar_roughness=0.3,
            multitemporal_coherence=0.7, residual_slope=0.5,
            signature_confidence=0.7, sensor_convergence=0.6, temporal_persistence=0.7
        ))
    ]
    
    morphologies = []
    for name, signature in test_cases:
        morphology = engine.classify_morphology(signature)
        morphologies.append(morphology.value)
        print(f"   {name}: {morphology.value}")
    
    # Verificar si siempre genera la misma morfología
    unique_morphologies = set(morphologies)
    if len(unique_morphologies) == 1:
        print(f"   ⚠️  PROBLEMA: Siempre genera '{list(unique_morphologies)[0]}'")
    else:
        print(f"   ✅ Genera {len(unique_morphologies)} morfologías diferentes")
    
    # 3. Test de generación volumétrica
    print("\n3. TEST DE GENERACIÓN VOLUMÉTRICA:")
    
    bounds = (-1.0, 1.0, -1.0, 1.0)
    
    for i, (name, signature) in enumerate(test_cases[:2], 1):
        morphology = engine.classify_morphology(signature)
        volumetric_field = engine.generate_volumetric_field(signature, morphology, bounds)
        
        print(f"   Campo {i} ({name}):")
        print(f"     - Morfología: {morphology.value}")
        print(f"     - Dimensiones: {volumetric_field.dimensions}")
        print(f"     - Probabilidad max: {np.max(volumetric_field.probability_volume):.3f}")
        print(f"     - Probabilidad promedio: {np.mean(volumetric_field.probability_volume):.3f}")
        print(f"     - Confianza core: {volumetric_field.confidence_layers['core']:.3f}")
        
        # Verificar si la distribución es siempre la misma
        prob_std = np.std(volumetric_field.probability_volume)
        if prob_std < 0.01:
            print(f"     ⚠️  Distribución muy uniforme (std={prob_std:.4f})")
        else:
            print(f"     ✅ Distribución variable (std={prob_std:.4f})")
    
    # 4. Test de modelo geométrico
    print("\n4. TEST DE MODELO GEOMÉTRICO:")
    
    signature = test_cases[0][1]  # Usar primera firma
    morphology = engine.classify_morphology(signature)
    volumetric_field = engine.generate_volumetric_field(signature, morphology, bounds)
    geometric_model = engine.extract_geometric_model(volumetric_field)
    
    print(f"   Vértices generados: {len(geometric_model.vertices)}")
    print(f"   Caras generadas: {len(geometric_model.faces)}")
    print(f"   Volumen estimado: {geometric_model.estimated_volume_m3:.2f} m³")
    print(f"   Altura máxima: {geometric_model.max_height_m:.2f} m")
    
    if len(geometric_model.vertices) == 0:
        print("   ❌ PROBLEMA: No se generan vértices")
    elif len(geometric_model.vertices) < 10:
        print("   ⚠️  Muy pocos vértices generados")
    else:
        print("   ✅ Modelo geométrico generado correctamente")
    
    # 5. Verificar valores hardcodeados específicos
    print("\n5. VALORES HARDCODEADOS ESPECÍFICOS ENCONTRADOS:")
    print("   ❌ Altura base simulada: 100m + random*10 (geometric_inference_engine.py)")
    print("   ❌ Dimensiones máximas grid: 100x100x50 (geometric_inference_engine.py)")
    print("   ❌ Umbral iso-superficie: 0.5 (geometric_inference_engine.py)")
    print("   ❌ Sigma filtro gaussiano: 1.0 (geometric_inference_engine.py)")
    print("   ❌ Color material 3D: 0x8B4513 (volumetric_lidar_app.js)")
    print("   ❌ Posición cámara: (50, 50, 50) (volumetric_lidar_app.js)")
    print("   ❌ Color fondo escena: 0xf0f0f0 (volumetric_lidar_app.js)")
    print("   ❌ URLs API: http://localhost:8002 (volumetric_lidar_app.js)")
    
    return {
        'morphology_variety': len(unique_morphologies),
        'hardcoded_values_found': True,
        'geometric_model_working': len(geometric_model.vertices) > 0
    }

if __name__ == "__main__":
    results = test_hardcoded_values()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE LA REVISIÓN:")
    print(f"   • Variedad morfológica: {results['morphology_variety']} tipos diferentes")
    print(f"   • Valores hardcodeados: {'SÍ' if results['hardcoded_values_found'] else 'NO'}")
    print(f"   • Modelo geométrico: {'FUNCIONAL' if results['geometric_model_working'] else 'DEFECTUOSO'}")
    
    if results['hardcoded_values_found']:
        print("\n🔧 RECOMENDACIONES:")
        print("   1. Parametrizar resolución voxel según datos de entrada")
        print("   2. Hacer configurables los colores y posiciones de cámara")
        print("   3. Eliminar alturas base simuladas hardcodeadas")
        print("   4. Configurar URLs API desde variables de entorno")
        print("   5. Hacer adaptativa la generación de geometría según anomalía real")