#!/usr/bin/env python3
"""Probar análisis en nueva ubicación para verificar nombres de instrumentos."""

import requests

API_BASE = "http://localhost:8002"

# Probar en México (zona agrícola)
test_data = {
    "lat_min": 26.94,
    "lat_max": 26.96,
    "lon_min": -111.86,
    "lon_max": -111.84,
    "region_name": "Sonora Mexico Test"
}

print("\n🧪 TEST: Análisis en nueva ubicación (México)")
print("="*60)

response = requests.post(
    f"{API_BASE}/api/scientific/analyze",
    json=test_data,
    timeout=120
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"✅ Análisis exitoso")
    print(f"\nRegión: {result['request_info']['region_name']}")
    print(f"Ambiente: {result['environment_context']['environment_type']}")
    print(f"Instrumentos disponibles: {len(result['environment_context']['available_instruments'])}")
    print(f"Instrumentos que midieron: {len(result['instrumental_measurements'])}")
    
    print(f"\n📊 MEDICIONES:")
    for m in result['instrumental_measurements']:
        print(f"  ✅ {m['instrument_name']:<30} = {m['value']:.3f} ({m['data_mode']})")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text[:500])
