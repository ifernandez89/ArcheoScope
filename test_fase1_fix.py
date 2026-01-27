#!/usr/bin/env python3
"""
Test FASE 1 - Validar fixes de Sentinel-2 y SAR
"""

import requests
import json

API_BASE_URL = "http://localhost:8002"

# Test con Valeriana (México - forest)
test_data = {
    "lat_min": 18.695,
    "lat_max": 18.745,
    "lon_min": -90.775,
    "lon_max": -90.725,
    "region_name": "Valeriana Test FASE1"
}

print("="*80)
print("TEST FASE 1 - Fixes Sentinel-2 + SAR")
print("="*80)
print(f"Region: {test_data['region_name']}")
print(f"BBox: [{test_data['lat_min']}, {test_data['lat_max']}] x [{test_data['lon_min']}, {test_data['lon_max']}]")
print()

try:
    response = requests.post(
        f"{API_BASE_URL}/analyze",
        json=test_data,
        timeout=120
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print("✅ ANALISIS EXITOSO")
        print()
        print("INSTRUMENTOS:")
        measurements = result.get('instrumental_measurements', [])
        print(f"  Total midiendo: {len(measurements)}")
        
        for m in measurements:
            print(f"  - {m.get('instrument_name')}: {m.get('value'):.3f} {m.get('unit')}")
        
        print()
        print("RESULTADO:")
        arch_results = result.get('archaeological_results', {})
        print(f"  Probabilidad: {arch_results.get('archaeological_probability', 0)*100:.1f}%")
        print(f"  Convergencia: {result.get('convergence_analysis', {}).get('convergence_met', False)}")
        
        # Guardar resultado
        with open('test_fase1_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        print()
        print("📄 Resultado guardado en: test_fase1_result.json")
        
    else:
        print(f"❌ ERROR HTTP {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"❌ EXCEPTION: {e}")
