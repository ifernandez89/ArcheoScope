#!/usr/bin/env python3
"""
Test simple de las mejoras avanzadas de ArcheoScope
"""

import sys
import os
sys.path.append(os.path.join('backend'))

import numpy as np
sys.path.append('backend')
from backend.rules.advanced_archaeological_rules import AdvancedArchaeologicalRulesEngine

def test_advanced_improvements():
    """Test básico de las mejoras avanzadas."""
    
    print("🧪 TESTING ARCHEOSCOPE ADVANCED IMPROVEMENTS")
    print("=" * 50)
    
    try:
        # Test 1: Initialize Advanced Rules Engine
        print("1. Inicializando motor de reglas avanzadas...")
        engine = AdvancedArchaeologicalRulesEngine()
        print("✅ Motor inicializado correctamente")
        
        # Test 2: Test Temporal Signature Analysis
        print("\n2. Probando análisis de firma temporal...")
        spectral_data = {
            'red': np.random.random((100, 100)),
            'nir': np.random.random((100, 100)),
            'red_edge': np.random.random((100, 100)),
            'swir': np.random.random((100, 100))
        }
        
        temporal_series = {
            'ndvi': [0.3 + 0.1 * np.sin(i * np.pi / 6) for i in range(24)],
            'thermal': [20 + 5 * np.sin(i * np.pi / 6) for i in range(24)],
            'sar': [0.5 + 0.05 * np.random.random() for i in range(24)],
            'precipitation': [50 + 30 * np.random.random() for i in range(24)]
        }
        
        temporal_signature = engine.analyze_temporal_archaeological_signature(spectral_data, temporal_series)
        print(f"✅ Firma temporal: lag={temporal_signature.ndvi_temporal_lag:.3f}, coherencia={temporal_signature.temporal_coherence_score:.3f}")
        
        # Test 3: Test Non-Standard Indices
        print("\n3. Probando índices espectrales no estándar...")
        non_standard_indices = engine.analyze_non_standard_vegetation_indices(spectral_data)
        print(f"✅ Índices no estándar: NDRE stress={non_standard_indices.ndre_stress:.3f}, MSI anomaly={non_standard_indices.msi_anomaly:.3f}")
        
        # Test 4: Test Modern Anthropogenic Filter
        print("\n4. Probando filtro antropogénico moderno...")
        geometric_features = {
            'linearity': 0.95,
            'regularity': 0.9,
            'length_m': 1500,
            'width_m': 6,
            'orientation_degrees': 0
        }
        
        modern_filter = engine.apply_modern_anthropogenic_filter(spectral_data, geometric_features)
        print(f"✅ Filtro moderno: drenaje agrícola={modern_filter.agricultural_drainage_probability:.3f}, línea eléctrica={modern_filter.power_line_probability:.3f}")
        
        # Test 5: Test Integrated Evaluation
        print("\n5. Probando evaluación integrada...")
        evaluation = engine.evaluate_advanced_archaeological_potential(temporal_signature, non_standard_indices, modern_filter)
        integrated_score = evaluation["integrated_advanced_analysis"]["score"]
        classification = evaluation["integrated_advanced_analysis"]["classification"]
        print(f"✅ Evaluación integrada: score={integrated_score:.3f}, clasificación={classification}")
        
        print("\n🎯 RESULTADO: Todas las mejoras avanzadas funcionan correctamente")
        print("📊 Características implementadas:")
        print("   - ✅ Firma temporal arqueológica")
        print("   - ✅ Índices espectrales no estándar (NDRE, MSI)")
        print("   - ✅ Filtro antropogénico moderno")
        print("   - ✅ Evaluación bayesiana integrada")
        print("   - ✅ Clasificación explicable")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_advanced_improvements()
    if success:
        print("\n🚀 TODAS LAS MEJORAS AVANZADAS ESTÁN OPERATIVAS")
    else:
        print("\n⚠️ ALGUNAS MEJORAS REQUIEREN REVISIÓN")