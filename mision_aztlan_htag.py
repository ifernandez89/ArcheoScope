import asyncio
import httpx
import json
import math
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"
AZTLAN = {"name": "Aztlan_Nayarit", "lat": 21.90, "lon": -105.47, "radius_km": 2.0}

async def scan_aztlan_htag():
    print("="*80)
    print("🛸 MISIÓN: AUDITORÍA DE AZTLÁN - LA ISLA DE LOS SIETE PUEBLOS")
    print(f"📍 Coordenadas: {AZTLAN['lat']}, {AZTLAN['lon']}")
    print("="*80)
    
    # Protocolo 1 Centro + 4 Radiales
    points = [
        {"dir": "CENTER", "d_lat": 0, "d_lon": 0},
        {"dir": "NORTH", "d_lat": AZTLAN['radius_km']/111, "d_lon": 0},
        {"dir": "SOUTH", "d_lat": -AZTLAN['radius_km']/111, "d_lon": 0},
        {"dir": "EAST", "d_lat": 0, "d_lon": AZTLAN['radius_km']/(111 * math.cos(math.radians(AZTLAN['lat'])))},
        {"dir": "WEST", "d_lat": 0, "d_lon": -AZTLAN['radius_km']/(111 * math.cos(math.radians(AZTLAN['lat'])))}
    ]
    
    results = []
    async with httpx.AsyncClient(timeout=300.0) as client:
        for p in points:
            lat = AZTLAN["lat"] + p["d_lat"]
            lon = AZTLAN["lon"] + p["d_lon"]
            payload = {
                "lat_min": lat - 0.012, "lat_max": lat + 0.012,
                "lon_min": lon - 0.012, "lon_max": lon + 0.012,
                "region_name": f"Aztlan_{p['dir']}",
                "resolution_m": 100.0
            }
            try:
                response = await client.post(URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    g1 = data['official_classification']['metrics_applied'].get('g1_geometry', 0)
                    veredicto = data['official_classification']['veredicto']
                    results.append({"dir": p["dir"], "g1": g1, "veredicto": veredicto})
                    print(f"   [{p['dir']}] G1: {g1:.4f} | {veredicto}")
            except:
                print(f"   [{p['dir']}] ERROR EN ESCANEO")
    
    if results:
        avg_g1 = sum(r['g1'] for r in results) / len(results)
        print(f"\n📊 PROMEDIO G1 AZTLÁN: {avg_g1:.4f}")
        
        status = "🔥 HTAG-HIGH (Anomalía de Infraestructura Hidráulica)" if avg_g1 > 0.90 else "ℹ️ NODO LOCAL / MARISMAS NATURALES"
        print(f"📢 RESULTADO: {status}")
    
    # Guardar resultados
    with open("AZTLAN_NAYARIT_RESULTS.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    asyncio.run(scan_aztlan_htag())
