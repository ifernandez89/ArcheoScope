#!/usr/bin/env python3
"""
Test Simple del Sistema de Validación IA - ArcheoScope

Test directo de los componentes sin requerir backend completo.
"""

import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.append(str(backend_path))

def test_ai_validation_assistant():
    """Test directo del AnomalyValidationAssistant."""
    
    print("🔍 TEST 1: AnomalyValidationAssistant")
    print("=" * 50)
    
    try:
        from ai.anomaly_validation_assistant import (
            AnomalyValidationAssistant, 
            InstrumentalFeatures
        )
        
        # Crear instancia
        validator = AnomalyValidationAssistant()
        
        print(f"✅ AnomalyValidationAssistant creado")
        print(f"   - IA disponible: {'✅' if validator.is_available else '❌'}")
        print(f"   - Umbral validación: {validator.validation_threshold}")
        print(f"   - Umbral inconsistencias: {validator.inconsistency_threshold}")
        
        # Test con features simuladas
        test_features = InstrumentalFeatures(
            tile_id="TEST-001",
            terrain_type="desert",
            signals={"sar": 0.81, "thermal": 0.67, "dem": 0.72},
            geometry_score=0.88,
            temporal_persistence=0.65,
            historical_proximity=0.12,
            convergence_count=3,
            environment_confidence=0.89
        )
        
        print(f"\n📊 Features de test:")
        print(f"   - Tile: {test_features.tile_id}")
        print(f"   - Terreno: {test_features.terrain_type}")
        print(f"   - Señales: {test_features.signals}")
        print(f"   - Geometría: {test_features.geometry_score:.2f}")
        print(f"   - Convergencia: {test_features.convergence_count}")
        
        # Test de validación
        test_measurements = [
            {"instrument": "SAR", "value": 0.81, "threshold": 0.7, "exceeds_threshold": True},
            {"instrument": "Thermal", "value": 0.67, "threshold": 0.6, "exceeds_threshold": True},
            {"instrument": "DEM", "value": 0.72, "threshold": 0.65, "exceeds_threshold": True}
        ]
        
        current_score = 0.75
        context = {"region": "Test Region", "analysis_type": "validation_test"}
        
        print(f"\n🤖 Ejecutando validación IA...")
        print(f"   - Score actual: {current_score:.3f}")
        print(f"   - Mediciones: {len(test_measurements)}")
        
        result = validator.validate_anomaly(
            instrumental_features=test_features,
            raw_measurements=test_measurements,
            current_score=current_score,
            context=context
        )
        
        print(f"\n✅ Validación completada:")
        print(f"   - Coherente: {'✅' if result.is_coherent else '❌'}")
        print(f"   - Confianza: {result.confidence_score:.3f}")
        print(f"   - Riesgo FP: {result.false_positive_risk:.3f}")
        print(f"   - Inconsistencias: {len(result.detected_inconsistencies)}")
        print(f"   - Recomendaciones: {len(result.recommended_actions)}")
        
        if result.detected_inconsistencies:
            print(f"   - Inconsistencias detectadas:")
            for inc in result.detected_inconsistencies[:3]:
                print(f"     • {inc}")
        
        print(f"   - Razonamiento: {result.validation_reasoning[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integrated_validator():
    """Test del IntegratedAIValidator (sin backend completo)."""
    
    print("\n🔍 TEST 2: IntegratedAIValidator (componentes)")
    print("=" * 50)
    
    try:
        from ai.integrated_ai_validator import IntegratedAIValidator
        
        # Test sin componentes completos (solo estructura)
        validator = IntegratedAIValidator(
            core_detector=None,  # Simular sin detector
            archaeological_assistant=None
        )
        
        print(f"✅ IntegratedAIValidator creado")
        print(f"   - Disponible: {'✅' if validator.is_available else '❌'} (esperado ❌ sin componentes)")
        print(f"   - AI Validator: {'✅' if validator.ai_validator.is_available else '❌'}")
        
        # Test de estructura de clases
        from ai.integrated_ai_validator import IntegratedAnalysisResult
        
        # Crear resultado simulado
        mock_result = IntegratedAnalysisResult(
            base_detection={"test": "data"},
            ai_validation=None,
            final_score=0.75,
            original_score=0.70,
            integrated_explanation="Test explanation",
            quality_metrics={"overall_quality": "good"},
            final_recommendations=["Test recommendation"]
        )
        
        print(f"✅ IntegratedAnalysisResult creado")
        print(f"   - Score original: {mock_result.original_score:.3f}")
        print(f"   - Score final: {mock_result.final_score:.3f}")
        print(f"   - Ajuste: {mock_result.final_score - mock_result.original_score:+.3f}")
        print(f"   - Calidad: {mock_result.quality_metrics['overall_quality']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_structures():
    """Test de estructuras de datos."""
    
    print("\n🔍 TEST 3: Estructuras de Datos")
    print("=" * 50)
    
    try:
        from ai.anomaly_validation_assistant import (
            AnomalyValidationResult,
            InstrumentalFeatures
        )
        
        # Test InstrumentalFeatures
        features = InstrumentalFeatures(
            tile_id="AR-ANT-034",
            terrain_type="ice",
            signals={"sar": 0.81, "thermal": 0.67, "dem": 0.72},
            geometry_score=0.88,
            temporal_persistence=0.45,
            historical_proximity=0.12,
            convergence_count=4,
            environment_confidence=0.91
        )
        
        print(f"✅ InstrumentalFeatures:")
        print(f"   - Tile: {features.tile_id}")
        print(f"   - Terreno: {features.terrain_type}")
        print(f"   - Señales: {len(features.signals)} instrumentos")
        print(f"   - Convergencia: {features.convergence_count}")
        
        # Test AnomalyValidationResult
        validation_result = AnomalyValidationResult(
            is_coherent=True,
            confidence_score=0.87,
            validation_reasoning="Test reasoning",
            detected_inconsistencies=["Test inconsistency"],
            scoring_adjustments={"ai_boost": 0.05},
            false_positive_risk=0.15,
            recommended_actions=["Test action"],
            methodological_notes="Test notes"
        )
        
        print(f"✅ AnomalyValidationResult:")
        print(f"   - Coherente: {'✅' if validation_result.is_coherent else '❌'}")
        print(f"   - Confianza: {validation_result.confidence_score:.3f}")
        print(f"   - Riesgo FP: {validation_result.false_positive_risk:.3f}")
        print(f"   - Ajustes: {validation_result.scoring_adjustments}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_assistant_base():
    """Test del ArchaeologicalAssistant base."""
    
    print("\n🔍 TEST 4: ArchaeologicalAssistant Base")
    print("=" * 50)
    
    try:
        from ai.archaeological_assistant import ArchaeologicalAssistant
        
        assistant = ArchaeologicalAssistant()
        
        print(f"✅ ArchaeologicalAssistant creado")
        print(f"   - Disponible: {'✅' if assistant.is_available else '❌'}")
        print(f"   - OpenRouter habilitado: {'✅' if assistant.openrouter_enabled else '❌'}")
        print(f"   - Ollama habilitado: {'✅' if assistant.ollama_enabled else '❌'}")
        
        if assistant.openrouter_enabled:
            print(f"   - Modelo OpenRouter: {assistant.openrouter_model}")
            print(f"   - API Key configurada: {'✅' if assistant.openrouter_api_key else '❌'}")
        
        if assistant.ollama_enabled:
            print(f"   - Modelo Ollama: {assistant.ollama_model}")
            print(f"   - URL Ollama: {assistant.ollama_url}")
        
        print(f"   - Timeout: {assistant.ai_timeout}s")
        print(f"   - Max tokens: {assistant.max_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar tests simples."""
    
    print("🧠 SISTEMA DE VALIDACIÓN IA - TEST SIMPLE")
    print("=" * 80)
    print("Test directo de componentes sin backend completo")
    print("=" * 80)
    
    tests = [
        ("AnomalyValidationAssistant", test_ai_validation_assistant),
        ("IntegratedAIValidator", test_integrated_validator),
        ("Estructuras de Datos", test_data_structures),
        ("ArchaeologicalAssistant Base", test_ai_assistant_base)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error en test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE TESTS SIMPLES")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 RESULTADO: {passed}/{total} tests exitosos ({passed/total:.1%})")
    
    if passed == total:
        print("🎉 ¡COMPONENTES DE VALIDACIÓN IA FUNCIONANDO!")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Configurar OPENROUTER_API_KEY para IA completa")
        print("   2. Iniciar backend completo: python run_archeoscope.py")
        print("   3. Ejecutar tests completos: python test_ai_validation_system.py")
    else:
        print("⚠️ Algunos componentes tienen problemas")
        print("\n🔧 REVISAR:")
        print("   1. Dependencias instaladas correctamente")
        print("   2. Estructura de archivos")
        print("   3. Imports y paths")

if __name__ == "__main__":
    main()