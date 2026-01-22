#!/usr/bin/env python3
import requests

try:
    response = requests.get('http://localhost:8004/status/detailed', timeout=5)
    if response.status_code == 200:
        print("✅ Backend funcionando correctamente")
        data = response.json()
        print(f"   - Backend: {data.get('backend_status', 'unknown')}")
        print(f"   - IA: {data.get('ai_status', 'unknown')}")
        print(f"   - Volumétrico: {data.get('volumetric_engine', 'unknown')}")
    else:
        print(f"❌ Backend error: {response.status_code}")
except Exception as e:
    print(f"❌ Error conectando: {e}")