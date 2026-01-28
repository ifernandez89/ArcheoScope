#!/usr/bin/env python3
"""
Test directo de Ollama para medir tiempo real
"""

import requests
import time
import json

OLLAMA_URL = "http://localhost:11434"

def test_model(model_name, prompt):
    """Probar un modelo directamente"""
    
    print(f"\n{'='*60}")
    print(f"🤖 Probando: {model_name}")
    print(f"{'='*60}")
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 200
        }
    }
    
    print(f"📝 Prompt: {prompt[:100]}...")
    print(f"⏱️  Iniciando...")
    
    start = time.time()
    
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=60
        )
        
        elapsed = time.time() - start
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '')
            
            print(f"✅ Completado en {elapsed:.2f} segundos")
            print(f"📊 Respuesta ({len(response_text)} chars):")
            print(f"   {response_text[:200]}...")
            
            return elapsed
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        elapsed = time.time() - start
        print(f"❌ TIMEOUT después de {elapsed:.2f} segundos")
        return None
    except Exception as e:
        elapsed = time.time() - start
        print(f"❌ Error después de {elapsed:.2f}s: {e}")
        return None

# Prompt corto optimizado
prompt = """Análisis arqueológico de Giza Pyramids (10000 km²).

Anomalías: thermal_anomalies (prob=0.75), sar_backscatter (prob=0.65)

En 2-3 frases: qué se detectó, interpretación arqueológica, recomendación."""

print("="*60)
print("🧪 TEST DIRECTO DE OLLAMA - COMPARACIÓN DE MODELOS")
print("="*60)

# Probar cada modelo
models = [
    "phi:latest",
    "phi4-mini-reasoning:latest",
    "qwen2.5:3b-instruct"
]

results = {}

for model in models:
    elapsed = test_model(model, prompt)
    if elapsed:
        results[model] = elapsed

# Resumen
print(f"\n{'='*60}")
print(f"📊 RESUMEN DE TIEMPOS")
print(f"{'='*60}")

for model, elapsed in sorted(results.items(), key=lambda x: x[1]):
    print(f"   {model}: {elapsed:.2f}s")

if results:
    fastest = min(results.items(), key=lambda x: x[1])
    print(f"\n🏆 Más rápido: {fastest[0]} ({fastest[1]:.2f}s)")

print(f"{'='*60}")
