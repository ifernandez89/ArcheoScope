#!/usr/bin/env python3
"""Test para verificar todas las correcciones"""

import requests
import json
import time

print("⏳ Esperando backend...")
time.sleep(20)

print("🧪 Ejecutando análisis completo...")

response = requests.post(
    'http://localhost:8003/api/scientific/analyze',
    json={
        'lat_min': 21.08,
        'lat_max': 21.17,
        'lon_min': -11.45,
        'lon_max': -11.35,
        'region_name': 'Test TODAS LAS CORRECCIONES'
    },
    timeout=300
)

result = response.json()

# Análisis de resultados
coverage = result['environment_context']['coverage_raw']
measurements = result['measurements']
success_count = sum(1 for m in measurements if m['status'] == 'SUCCESS')
total_count = len(measurements)

print(f"\n{'='*80}")
print(f"RESULTADOS DEL ANÁLISIS")
print(f"{'='*80}")
print(f"Coverage: {coverage:.1%}")
print(f"Instrumentos SUCCESS: {success_count}/{total_count}")
print(f"\nDetalle por instrumento:")
print(f"{'-'*80}")

for m in measurements:
    status_emoji = "✅" if m['status'] == 'SUCCESS' else "❌" if m['status'] == 'FAILED' else "⚠️"
    value_str = f"{m['value']:.3f}" if m['value'] is not None else "None"
    print(f"{status_emoji} {m['instrument_name']:25s} {m['status']:10s} value={value_str}")

print(f"{'-'*80}")
print(f"\nAnomalía detectada:")
print(f"  Score: {result['archaeological_results']['anomaly_score']:.2f}")
print(f"  Clasificación: {result['archaeological_results']['classification']}")
print(f"  Prioridad: {result['archaeological_results']['priority']}")

print(f"\n{'='*80}")
print(f"✅ TEST COMPLETADO")
print(f"{'='*80}")
