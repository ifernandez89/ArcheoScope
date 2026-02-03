import asyncio
import httpx
import json
import math
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

# EJE DEL NORTE (Centro de la Proyección de Monte)
NORTH_POLE_NODE = {"name": "Rupes_Nigra_Center", "lat": 89.0, "lon": 0.0, "radius_km": 1.5}

async def scan_north_axis():
    print("="*80)
    print("🧭 PROTOCOLO: EL EJE DEL NORTE (CENTRO DE MONTE)")
    print(f"📍 Coordenadas: {NORTH_POLE_NODE['lat']}, {NORTH_POLE_NODE['lon']}")
    print("="*80)
    
    # Protocolo Quirúrgico Quick-HTAG (5 puntos)
    points = [
        {"dir": "CENTER", "d_lat": 0, "d_lon": 0},
        {"dir": "NORTH", "d_lat": NORTH_POLE_NODE['radius_km']/111, "d_lon": 0},
        {"dir": "SOUTH", "d_lat": -NORTH_POLE_NODE['radius_km']/111, "d_lon": 0},
        {"dir": "EAST", "d_lat": 0, "d_lon": NORTH_POLE_NODE['radius_km']/(111 * math.cos(math.radians(NORTH_POLE_NODE['lat'])))},
        {"dir": "WEST", "d_lat": 0, "d_lon": -NORTH_POLE_NODE['radius_km']/(111 * math.cos(math.radians(NORTH_POLE_NODE['lat'])))}
    ]
    
    results = []
    async with httpx.AsyncClient(timeout=300.0) as client:
        for p in points:
            lat = NORTH_POLE_NODE["lat"] + p["d_lat"]
            # Clamp lat to 90
            if lat > 90: lat = 90.0 - (lat - 90)
            
            lon = NORTH_POLE_NODE["lon"] + p["d_lon"]
            payload = {
                "lat_min": lat - 0.01, "lat_max": lat + 0.01,
                "lon_min": lon - 0.01, "lon_max": lon + 0.01,
                "region_name": f"NorthAxis_{p['dir']}",
                "resolution_m": 150.0
            }
            try:
                response = await client.post(URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    g1 = data['official_classification']['metrics_applied'].get('g1_geometry', 0)
                    results.append(g1)
                    print(f"   [{p['dir']}] G1: {g1:.4f}")
            except:
                results.append(0)
    
    avg_g1 = sum(results) / len(results) if results else 0
    print(f"\n📊 PROMEDIO G1 (EJE DEL NORTE): {avg_g1:.4f}")
    
    # Decisión
    if avg_g1 > 0.90:
        conclusion = "🔥 IMPACTO ESTRATÉGICO: Coherencia Detectada en el Centro de Monte."
    else:
        conclusion = "❄️ RUPTURA TOTAL: El Centro de Monte es un nodo puramente ideal/simbólico."
        
    print(f"\n📢 CONCLUSIÓN: {conclusion}")
    
    return {"node": NORTH_POLE_NODE['name'], "avg_g1": avg_g1, "conclusion": conclusion}

if __name__ == "__main__":
    asyncio.run(scan_north_axis())
