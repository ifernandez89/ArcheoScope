#!/usr/bin/env python3
"""
Test directo del método de optimización - saltar todo el endpoint
"""

import sys
sys.path.append('C:\\Python\\ArcheoScope\\backend')

from core_anomaly_detector import CoreAnomalyDetector
from environment_classifier import EnvironmentClassifier
from validation.real_archaeological_validator import RealArchaeologicalValidator
from data.archaeological_loader import ArchaeologicalDataLoader
import time

def test_direct_optimization():
    """Test directo del CoreAnomalyDetector optimizado"""
    
    print("TEST DIRECTO - CoreAnomalyDetector OPTIMIZADO")
    print("Probando Bermudas (32.300, -64.783)")
    
    try:
        # Inicializar componentes
        start_init = time.time()
        env_classifier = EnvironmentClassifier()
        validator = RealArchaeologicalValidator()
        loader = ArchaeologicalDataLoader()
        
        detector = CoreAnomalyDetector(env_classifier, validator, loader)
        init_time = time.time() - start_init
        print(f"Inicialización: {init_time:.2f}s")
        
        # Test análisis
        start_analysis = time.time()
        result = detector.detect_anomaly(
            32.300, -64.783,
            32.295, 32.305,
            -64.788, -64.778,
            "Bermuda Direct Test"
        )
        analysis_time = time.time() - start_analysis
        
        print(f"Análisis: {analysis_time:.2f}s")
        print(f"Ambiente: {result.environment_type}")
        print(f"Probabilidad: {result.archaeological_probability:.2%}")
        print(f"Mediciones: {len(result.measurements)}")
        
        if analysis_time < 5:
            print("✅ OPTIMIZACIÓN EXITOSA: <5 segundos!")
        elif analysis_time < 10:
            print(f"⚠️ Mejora notable: {analysis_time:.2f}s")
        else:
            print(f"❌ Todavía lento: {analysis_time:.2f}s")
        
        return analysis_time < 10
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_direct_optimization()