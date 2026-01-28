#!/usr/bin/env python3
"""
Test rápido de Valeriana para verificar clasificación de ambiente
"""

import requests
import json

API_BASE_URL = "http://localhost:8002"

# Valeriana - Ciudad Maya
bbox = {
    "lat_min": 18.695,
    "lat_max": 18.745,
    "lon_min": -90.775,
    "lon_max": -90.725,
    "region_name": "Valeriana - Test Clasificación"
}

print("🔍 Testeando clasificación de ambiente para Valeriana...")
print(f"📍 Coordenadas: {bbox['lat_min']}, {bbox['lon_min']}")

try:
    response = requests.post(
        f"{API_BASE_URL}/analyze",
        json=bbox,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        
        env = result.get('environment_classification', {})
        print(f"\n✅ Ambiente detectado: {env.get('environment_type')}")
        print(f"   Confianza: {env.get('confidence', 0)*100:.1f}%")
        print(f"   Sensores primarios: {env.get('primary_sensors', [])}")
        
        # Verificar que NO sea deep_ocean
        if env.get('environment_type') == 'deep_ocean':
            print("\n❌ ERROR: Valeriana (selva mexicana) detectada como océano profundo!")
        elif env.get('environment_type') == 'forest':
            print("\n✅ CORRECTO: Valeriana detectada como bosque/selva")
        else:
            print(f"\n⚠️  Ambiente detectado: {env.get('environment_type')}")
        
    else:
        print(f"❌ Error HTTP {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
