import asyncio
import httpx
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

async def analyze_visoko():
    # Coordenadas proporcionadas: {43.9888, 18.1701}
    # Valle de Visoko, Bosnia - Colina Visočica (Pirámide del Sol)
    lat, lon = 43.9888, 18.1701
    delta = 0.006
    
    payload = {
        "lat_min": lat - delta,
        "lat_max": lat + delta,
        "lon_min": lon - delta,
        "lon_max": lon + delta,
        "region_name": "Visoko - Pyramid of the Sun (Visočica Hill)"
    }
    
    url = "http://localhost:8003/api/scientific/analyze"
    
    print(f"\n🚀 INICIANDO ANÁLISIS CIENTÍFICO: VISOKO (BOSNIA)")
    print(f"====================================================")
    print(f"📍 Coordenadas: {lat}, {lon}")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        try:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ ANÁLISIS COMPLETADO")
                
                # Guardar datos
                filename = "visoko_scan_results.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                return result
            else:
                print(f"❌ ERROR: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")

if __name__ == "__main__":
    asyncio.run(analyze_visoko())
