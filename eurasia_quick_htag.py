import asyncio
import httpx
import json
import math
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

# DEFINICIÓN DEL EJE EURASIA (QUICK-HTAG)
EURASIA_NODES = [
    {"name": "Central_Anatolia", "lat": 38.0, "lon": 32.5, "radius_km": 1.5},
    {"name": "Ustyurt_Plateau", "lat": 44.0, "lon": 55.5, "radius_km": 1.5},
    {"name": "Fergana_Core", "lat": 40.4, "lon": 71.8, "radius_km": 1.5}
]

async def scan_quick_htag(node):
    print(f"\n🚜 EJECUTANDO QUICK-HTAG: {node['name']}...")
    
    # Protocolo 1 Centro + 4 Radiales
    points = [
        {"dir": "CENTER", "d_lat": 0, "d_lon": 0},
        {"dir": "NORTH", "d_lat": node['radius_km']/111, "d_lon": 0},
        {"dir": "SOUTH", "d_lat": -node['radius_km']/111, "d_lon": 0},
        {"dir": "EAST", "d_lat": 0, "d_lon": node['radius_km']/(111 * math.cos(math.radians(node['lat'])))},
        {"dir": "WEST", "d_lat": 0, "d_lon": -node['radius_km']/(111 * math.cos(math.radians(node['lat'])))}
    ]
    
    results = []
    async with httpx.AsyncClient(timeout=300.0) as client:
        for p in points:
            lat = node["lat"] + p["d_lat"]
            lon = node["lon"] + p["d_lon"]
            payload = {
                "lat_min": lat - 0.01, "lat_max": lat + 0.01,
                "lon_min": lon - 0.01, "lon_max": lon + 0.01,
                "region_name": f"Quick_{node['name']}_{p['dir']}",
                "resolution_m": 100.0
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
    print(f"📊 AVG G1: {avg_g1:.4f}")
    
    # Decisión Inmediata
    if avg_g1 > 0.93:
        status = "🔥 HTAG-CTA (Canon Potential)"
    elif avg_g1 > 0.90:
        status = "✅ HTAG-PRIME (High Interest)"
    elif avg_g1 > 0.88:
        status = "ℹ️ HTAG-NODAL (Local Interest)"
    else:
        status = "❌ NATURAL (Discard)"
        
    print(f"📢 VERDICTO: {status}")
    return {"node": node['name'], "avg_g1": avg_g1, "status": status}

async def main():
    print("="*70)
    print("🌍 MISIÓN: EJECUCIÓN HEURÍSTICA EURASIA (HTAG-MONTE)")
    print("="*70)
    
    mission_summary = []
    for node in EURASIA_NODES:
        res = await scan_quick_htag(node)
        mission_summary.append(res)
        
    print("\n" + "="*70)
    print("🏁 RESUMEN ESTRATÉGICO EURASIA")
    print("="*70)
    for m in mission_summary:
        print(f"- {m['node']}: {m['avg_g1']:.4f} -> {m['status']}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
