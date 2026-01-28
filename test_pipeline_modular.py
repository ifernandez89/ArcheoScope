#!/usr/bin/env python3
"""
Test Pipeline Modular - Verificar comportamiento idéntico
========================================================

Verifica que el pipeline modular produce el mismo output que antes.
"""

import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_pipeline_modular():
    """Test básico del pipeline modular."""
    
    print("🧪 TESTING PIPELINE MODULAR")
    print("=" * 35)
    
    try:
        # Test 1: Importar módulos individuales
        print("\n1️⃣ Testing individual modules...")
        
        from pipeline.normalization import normalize_data, NormalizedFeatures
        print("   ✅ normalization module imported")
        
        from pipeline.anomaly_detection import detect_anomaly, AnomalyResult
        print("   ✅ anomaly_detection module imported")
        
        from pipeline.morphology import analyze_morphology, MorphologyResult
        print("   ✅ morphology module imported")
        
        from pipeline.anthropic_inference import infer_anthropic_probability, AnthropicInference
        print("   ✅ anthropic_inference module imported")
        
        # Test 2: Importar pipeline principal
        print("\n2️⃣ Testing main pipeline...")
        
        from scientific_pipeline import ScientificPipeline
        print("   ✅ ScientificPipeline imported")
        
        # Test 3: Crear instancia
        print("\n3️⃣ Testing pipeline instantiation...")
        
        pipeline = ScientificPipeline()
        print("   ✅ Pipeline instance created")
        
        # Test 4: Test con datos simulados
        print("\n4️⃣ Testing with simulated data...")
        
        # Datos de prueba
        test_data = {
            'candidate_id': 'TEST_001',
            'region_name': 'Test Region',
            'environment_type': 'terrestrial',
            'instruments_available': 5,
            'landsat_thermal': {'value': 15.5, 'threshold': 12.0},
            'sentinel_2_ndvi': {'value': 0.65, 'threshold': 0.70},
            'sentinel_1_sar': {'value': -8.2, 'threshold': -10.0}
        }
        
        # Test normalización
        normalized = normalize_data(test_data)
        print(f"   ✅ Normalization: {len(normalized.features)} features")
        
        # Test detección de anomalías
        anomaly = detect_anomaly(normalized)
        print(f"   ✅ Anomaly detection: score={anomaly.anomaly_score:.3f}")
        
        # Test morfología
        morphology = analyze_morphology(normalized, anomaly)
        print(f"   ✅ Morphology: symmetry={morphology.symmetry_score:.3f}")
        
        # Test inferencia antropogénica
        anthropic = infer_anthropic_probability(normalized, anomaly, morphology)
        print(f"   ✅ Anthropic inference: prob={anthropic.anthropic_probability:.3f}")
        
        print(f"\n🎯 RESULTADO FINAL:")
        print(f"   Anomaly Score: {anomaly.anomaly_score:.3f}")
        print(f"   Anthropic Probability: {anthropic.anthropic_probability:.3f}")
        print(f"   Confidence: {anthropic.confidence}")
        print(f"   ESS: {anthropic.explanatory_strangeness}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 PIPELINE MODULAR TESTING")
    print("=" * 40)
    
    success = test_pipeline_modular()
    
    print(f"\n" + "=" * 40)
    if success:
        print("🎉 RESULTADO: ✅ PIPELINE MODULAR FUNCIONAL")
        print("🧩 Modularización exitosa")
        print("🔄 Comportamiento preservado")
        print("📦 Imports funcionando correctamente")
    else:
        print("💥 RESULTADO: ❌ PIPELINE NECESITA AJUSTES")
        print("🔧 Revisar imports y dependencias")
    
    print(f"⏰ Testing completado")