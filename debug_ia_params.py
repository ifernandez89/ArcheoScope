#!/usr/bin/env python3
"""
Debug: Ver exactamente qué parámetros se envían a la IA
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from dotenv import load_dotenv
load_dotenv('.env.local')

from ai.archaeological_assistant import ArchaeologicalAssistant

# Crear asistente
assistant = ArchaeologicalAssistant()

print("="*80)
print("🔍 PARÁMETROS DE IA - DEBUG")
print("="*80)

print(f"\n📋 CONFIGURACIÓN:")
print(f"   Ollama habilitado: {assistant.ollama_enabled}")
print(f"   Modelo: {assistant.ollama_model}")
print(f"   URL: {assistant.ollama_url}")
print(f"   Timeout: {assistant.ai_timeout}s")
print(f"   Max tokens: {assistant.max_tokens}")
print(f"   Disponible: {assistant.is_available}")

# Simular datos de análisis
anomalies = [
    {
        "type": "thermal_anomalies",
        "archaeological_probability": 0.75,
        "geometric_coherence": 0.85,
        "temporal_persistence": 0.90,
        "affected_pixels": 1234,
        "suspected_features": ["buried_structures", "thermal_inertia"]
    },
    {
        "type": "sar_backscatter",
        "archaeological_probability": 0.65,
        "geometric_coherence": 0.70,
        "temporal_persistence": 0.80,
        "affected_pixels": 987,
        "suspected_features": ["surface_roughness"]
    },
    {
        "type": "ndvi_stress",
        "archaeological_probability": 0.55,
        "geometric_coherence": 0.60,
        "temporal_persistence": 0.75,
        "affected_pixels": 654,
        "suspected_features": ["vegetation_suppression"]
    }
]

rule_evaluations = {
    "rule_1": type('MockEval', (), {
        'result': type('MockResult', (), {'value': 'anomalous'})(),
        'archaeological_probability': 0.80,
        'rule_violations': ["vegetation_decoupling"]
    })()
}

context = {
    "region_name": "Giza Pyramids Complex",
    "area_km2": 10000,
    "coordinates": "29.9792, 31.1342"
}

# Construir prompt
print(f"\n📝 CONSTRUYENDO PROMPT...")
prompt = assistant._build_archaeological_prompt(anomalies, rule_evaluations, context)

print(f"\n{'='*80}")
print(f"📄 PROMPT GENERADO:")
print(f"{'='*80}")
print(prompt)
print(f"{'='*80}")

print(f"\n📊 ESTADÍSTICAS DEL PROMPT:")
print(f"   Longitud: {len(prompt)} caracteres")
print(f"   Líneas: {prompt.count(chr(10)) + 1}")
print(f"   Tokens estimados: ~{len(prompt.split())} palabras")

print(f"\n🔧 PARÁMETROS QUE SE ENVIARÍAN A OLLAMA:")
print(f"   {{")
print(f"     'model': '{assistant.ollama_model}',")
print(f"     'prompt': '[PROMPT DE {len(prompt)} CHARS]',")
print(f"     'stream': False,")
print(f"     'options': {{")
print(f"       'temperature': 0.3,")
print(f"       'top_p': 0.9,")
print(f"       'num_predict': 200")
print(f"     }}")
print(f"   }}")
print(f"   timeout: 30 segundos")

print(f"\n⏱️  TIEMPO ESTIMADO:")
print(f"   Con phi4-mini-reasoning: 15-30 segundos")
print(f"   Con qwen2.5:3b-instruct: 20-40 segundos")

print(f"\n{'='*80}")
