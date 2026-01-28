#!/usr/bin/env python3
"""
Test para ver la estructura exacta de la respuesta de enriched-candidates
"""

import requests
import json

API_BASE = "http://localhost:8002"

url = f"{API_BASE}/archaeological-sites/enriched-candidates"
params = {
    'lat_min': 25,
    'lat_max': 30,
    'lon_min': 30,
    'lon_max': 35,
    'strategy': 'buffer',
    'max_zones': 5,
    'lidar_priority': True,
    'min_convergence': 0.4,
    'save_to_database': False
}

print("🔍 TEST: Estructura de respuesta enriched-candidates\n")

try:
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        
        print("✅ Status: 200\n")
        print("📊 Claves principales:")
        for key in data.keys():
            print(f"   - {key}")
        
        if 'candidates' in data and len(data['candidates']) > 0:
            print("\n📋 Estructura de primera candidata:")
            candidate = data['candidates'][0]
            print(json.dumps(candidate, indent=2))
        else:
            print("\n⚠️  No hay candidatas en la respuesta")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"❌ Exception: {e}")
