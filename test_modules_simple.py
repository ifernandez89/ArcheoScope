#!/usr/bin/env python3
"""
Test Simple de Módulos - 5 Correcciones
========================================

Test básico para verificar que los módulos se pueden importar y usar.
"""

import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

print("="*80)
print("TEST SIMPLE DE MÓDULOS")
print("="*80)

# Test 1: SAR Enhanced Processing
print("\n1. SAR Enhanced Processing")
try:
    from sar_enhanced_processing import process_sar_enhanced
    import numpy as np
    
    # Test con datos 2D
    sar_2d = np.random.normal(-12, 3, (50, 50))
    sar_2d[20:30, 20:30] += 5  # Estructura
    
    result = process_sar_enhanced(-12.0, sar_2d)
    
    print(f"   ✅ Módulo cargado")
    print(f"   Structural index: {result['sar_structural_index']:.3f}")
    print(f"   Processing mode: {result['processing_mode']}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Coverage Assessment
print("\n2. Coverage Assessment")
try:
    from pipeline.coverage_assessment import calculate_coverage_score
    
    instruments = ['sentinel_2_ndvi', 'sentinel_1_sar', 'landsat_thermal', 'srtm_elevation']
    assessment = calculate_coverage_score(instruments)
    
    print(f"   ✅ Módulo cargado")
    print(f"   Coverage score: {assessment.coverage_score:.2f}")
    print(f"   Coverage quality: {assessment.coverage_quality.value}")
    print(f"   Core coverage: {assessment.core_coverage:.2f}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Scientific Narrative
print("\n3. Scientific Narrative")
try:
    from scientific_narrative import generate_archaeological_narrative
    
    narrative = generate_archaeological_narrative(
        thermal_stability=0.93,
        sar_structural_index=0.52,
        icesat2_rugosity=15.7,
        ndvi_persistence=0.06,
        tas_score=0.58,
        coverage_score=0.65,
        environment_type="arid",
        flags=['THERMAL_ANCHOR_ZONE']
    )
    
    print(f"   ✅ Módulo cargado")
    print(f"   Clasificación: {narrative.classification.value}")
    print(f"   Confianza: {narrative.confidence:.2f}")
    print(f"   Prioridad: {narrative.priority}")
    print(f"   Declaración: {narrative.main_statement}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: TAS Adaptive
print("\n4. TAS Environment-Aware")
try:
    from temporal_archaeological_signature import TemporalArchaeologicalSignatureEngine
    
    engine = TemporalArchaeologicalSignatureEngine(integrator=None)
    
    # Test árido con thermal anchor
    score_arid = engine._calculate_tas_score(
        ndvi_persistence=0.1,
        thermal_stability=0.95,
        sar_coherence=0.5,
        stress_frequency=0.2,
        environment_type="arid"
    )
    
    # Test templado
    score_temperate = engine._calculate_tas_score(
        ndvi_persistence=0.1,
        thermal_stability=0.95,
        sar_coherence=0.5,
        stress_frequency=0.2,
        environment_type="temperate"
    )
    
    print(f"   ✅ Módulo cargado")
    print(f"   TAS score (árido): {score_arid:.3f}")
    print(f"   TAS score (templado): {score_temperate:.3f}")
    print(f"   Pesos adaptativos: {'✅ SÍ' if score_arid != score_temperate else '❌ NO'}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*80)
print("TEST COMPLETADO")
print("="*80)
