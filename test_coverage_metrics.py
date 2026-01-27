#!/usr/bin/env python3
"""Verificar que las métricas de cobertura estén en la respuesta."""

import requests
import json

API_BASE = "http://localhost:8002"

test_data = {
    "lat_min": 26.94,
    "lat_max": 26.96,
    "lon_min": -111.86,
    "lon_max": -111.84,
    "region_name": "Test Coverage Metrics"
}

print("\n🧪 TEST: Métricas de Cobertura")
print("="*60)

response = requests.post(
    f"{API_BASE}/api/scientific/analyze",
    json=test_data,
    timeout=120
)

if response.status_code == 200:
    result = response.json()
    output = result['scientific_output']
    
    print(f"✅ Análisis exitoso\n")
    print(f"📊 MÉTRICAS DE COBERTURA:")
    coverage_raw = output.get('coverage_raw', 0)
    coverage_eff = output.get('coverage_effective', 0)
    print(f"  Coverage Raw:       {coverage_raw if isinstance(coverage_raw, (int, float)) else 0:.2%}")
    print(f"  Coverage Effective: {coverage_eff if isinstance(coverage_eff, (int, float)) else 0:.2%}")
    print(f"  Instruments Measured: {output.get('instruments_measured', 0)}")
    print(f"  Instruments Available: {output.get('instruments_available', 0)}")
    
    print(f"\n🔬 RESULTADO:")
    print(f"  Probabilidad: {output['anthropic_probability']:.3f}")
    print(f"  Anomaly Score: {output['anomaly_score']:.3f}")
    print(f"  Acción: {output['recommended_action']}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text[:500])
