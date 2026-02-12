#!/usr/bin/env python3
"""
Test - Motor de Inferencia Geométrica (MIG)
===========================================

Prueba el pipeline completo:
1. Datos ArcheoScope → Reglas geométricas
2. Reglas → Geometría 3D
3. Geometría → PNG + OBJ
"""

import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

from geometric_inference_engine import GeometricInferenceEngine


def test_puerto_rico_north():
    """Test con datos reales de Puerto Rico North."""
    
    print("="*80)
    print("🧪 TEST 1: Puerto Rico North")
    print("="*80)
    
    # Datos reales del deep analysis
    data = {
        'scale_invariance': 0.995,
        'angular_consistency': 0.910,
        'coherence_3d': 0.886,
        'sar_rigidity': 0.929,
        'stratification_index': 0.375,
        'estimated_area_m2': 10000.0
    }
    
    mig = GeometricInferenceEngine()
    
    result = mig.run_complete_inference(
        archeoscope_data=data,
        output_name="puerto_rico_north_structure",
        use_ai=False  # Heurísticas por ahora
    )
    
    print(f"\n✅ Resultados:")
    print(f"   Clase: {result['structure_class']}")
    print(f"   Confianza: {result['confidence']:.3f}")
    print(f"   Volumen: {result['volume_m3']:.0f} m³")
    print(f"   PNG: {result['png']}")
    print(f"   OBJ: {result['obj']}")
    print()


def test_mystery_location():
    """Test con Mystery Location (18.98, -67.48)."""
    
    print("="*80)
    print("🧪 TEST 2: Mystery Location")
    print("="*80)
    
    # Datos del análisis reciente
    data = {
        'scale_invariance': 0.995,  # Asumiendo similar
        'angular_consistency': 0.001,  # MUY BAJO (sospechoso)
        'coherence_3d': 0.886,
        'sar_rigidity': 0.872,
        'stratification_index': 0.717,  # ALTO (3 capas)
        'estimated_area_m2': 15000.0
    }
    
    mig = GeometricInferenceEngine()
    
    result = mig.run_complete_inference(
        archeoscope_data=data,
        output_name="mystery_location_structure",
        use_ai=False
    )
    
    print(f"\n✅ Resultados:")
    print(f"   Clase: {result['structure_class']}")
    print(f"   Confianza: {result['confidence']:.3f}")
    print(f"   Volumen: {result['volume_m3']:.0f} m³")
    print(f"   PNG: {result['png']}")
    print(f"   OBJ: {result['obj']}")
    print()


def test_pyramidal_structure():
    """Test con estructura piramidal ideal."""
    
    print("="*80)
    print("🧪 TEST 3: Estructura Piramidal Ideal")
    print("="*80)
    
    # Datos ideales para pirámide
    data = {
        'scale_invariance': 0.98,
        'angular_consistency': 0.95,
        'coherence_3d': 0.92,
        'sar_rigidity': 0.90,
        'stratification_index': 0.2,  # Baja (no escalonada)
        'estimated_area_m2': 52900.0  # ~230m × 230m (Giza)
    }
    
    mig = GeometricInferenceEngine()
    
    result = mig.run_complete_inference(
        archeoscope_data=data,
        output_name="pyramidal_structure",
        use_ai=False
    )
    
    print(f"\n✅ Resultados:")
    print(f"   Clase: {result['structure_class']}")
    print(f"   Confianza: {result['confidence']:.3f}")
    print(f"   Volumen: {result['volume_m3']:.0f} m³")
    print(f"   PNG: {result['png']}")
    print(f"   OBJ: {result['obj']}")
    print()


def test_stepped_platform():
    """Test con plataforma escalonada."""
    
    print("="*80)
    print("🧪 TEST 4: Plataforma Escalonada")
    print("="*80)
    
    # Datos para estructura escalonada
    data = {
        'scale_invariance': 0.96,
        'angular_consistency': 0.92,
        'coherence_3d': 0.88,
        'sar_rigidity': 0.85,
        'stratification_index': 0.75,  # ALTA (escalonada)
        'estimated_area_m2': 40000.0
    }
    
    mig = GeometricInferenceEngine()
    
    result = mig.run_complete_inference(
        archeoscope_data=data,
        output_name="stepped_platform",
        use_ai=False
    )
    
    print(f"\n✅ Resultados:")
    print(f"   Clase: {result['structure_class']}")
    print(f"   Confianza: {result['confidence']:.3f}")
    print(f"   Volumen: {result['volume_m3']:.0f} m³")
    print(f"   PNG: {result['png']}")
    print(f"   OBJ: {result['obj']}")
    print()


if __name__ == "__main__":
    print("\n🧠 MIG - MOTOR DE INFERENCIA GEOMÉTRICA - TESTS\n")
    
    try:
        test_puerto_rico_north()
        test_mystery_location()
        test_pyramidal_structure()
        test_stepped_platform()
        
        print("="*80)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("="*80)
        print("\n📁 Revisa la carpeta 'geometric_models/' para ver los resultados")
        print("   - *.png: Visualizaciones 3D")
        print("   - *.obj: Modelos 3D (importables en AutoCAD/Blender)")
        
    except Exception as e:
        print(f"\n❌ Error en tests: {e}")
        import traceback
        traceback.print_exc()
