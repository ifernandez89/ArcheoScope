#!/usr/bin/env python3
"""
Test rápido de Ollama con qwen2.5:3b-instruct
"""

import os
import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from dotenv import load_dotenv
load_dotenv('.env.local')

from ai.archaeological_assistant import ArchaeologicalAssistant

def test_ollama_qwen():
    """Probar que Ollama esté usando qwen correctamente"""
    
    print("="*80)
    print("🧪 TEST: Ollama con qwen2.5:3b-instruct")
    print("="*80)
    
    # Crear asistente
    assistant = ArchaeologicalAssistant()
    
    print(f"\n📋 CONFIGURACIÓN:")
    print(f"   Ollama habilitado: {assistant.ollama_enabled}")
    print(f"   OpenRouter habilitado: {assistant.openrouter_enabled}")
    print(f"   Modelo Ollama: {assistant.ollama_model}")
    print(f"   URL Ollama: {assistant.ollama_url}")
    print(f"   Disponible: {assistant.is_available}")
    
    if not assistant.is_available:
        print("\n❌ ERROR: Asistente no disponible")
        return False
    
    # Preparar datos de prueba
    test_data = {
        "region_name": "Giza Pyramids Test",
        "environment": "desert",
        "anomalies_detected": 3,
        "instruments_converging": 2,
        "measurements": [
            {"instrument": "thermal_anomalies", "value": 8.5, "threshold": 5.0, "exceeds": True},
            {"instrument": "sar_backscatter", "value": -5.2, "threshold": -3.0, "exceeds": True}
        ]
    }
    
    print(f"\n🔬 DATOS DE PRUEBA:")
    print(f"   Región: {test_data['region_name']}")
    print(f"   Ambiente: {test_data['environment']}")
    print(f"   Anomalías: {test_data['anomalies_detected']}")
    
    # Generar explicación
    print(f"\n🤖 GENERANDO EXPLICACIÓN CON {assistant.ollama_model}...")
    
    try:
        # Preparar datos en el formato correcto
        anomalies = [
            {
                "type": "thermal_anomaly",
                "value": 8.5,
                "threshold": 5.0,
                "confidence": "high"
            },
            {
                "type": "sar_backscatter",
                "value": -5.2,
                "threshold": -3.0,
                "confidence": "moderate"
            }
        ]
        
        rule_evaluations = {
            "environment": "desert",
            "archaeological_probability": 0.75,
            "instruments_converging": 2,
            "minimum_required": 2
        }
        
        explanation = assistant.explain_archaeological_anomalies(
            anomalies,
            rule_evaluations,
            test_data
        )
        
        print(f"\n✅ RESPUESTA RECIBIDA:")
        print(f"   AI disponible: {explanation.get('ai_available', False)}")
        print(f"   Modelo usado: {explanation.get('model_used', 'unknown')}")
        print(f"   Longitud respuesta: {len(explanation.get('explanation', ''))} caracteres")
        
        if explanation.get('explanation'):
            print(f"\n📝 EXPLICACIÓN:")
            print("-" * 80)
            print(explanation['explanation'][:500])
            if len(explanation['explanation']) > 500:
                print("...")
            print("-" * 80)
        
        print(f"\n✅ TEST EXITOSO")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ollama_qwen()
    sys.exit(0 if success else 1)
