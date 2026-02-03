import asyncio
import httpx
import json
import math
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

# OBJETIVOS DE ALTA PRIORIDAD (AUDITORÍA ESTRUCTURAL)
MONTE_CORE_NODES = [
    {"name": "Caspia_Tartaria_Core", "lat": 45.0, "lon": 63.0, "radius_km": 1.5},
    {"name": "Taprobana_Sunk_Platform", "lat": 7.0, "lon": 81.0, "radius_km": 1.5},
    {"name": "Caucasian_Iron_Gate", "lat": 42.0, "lon": 44.5, "radius_km": 1.5}
]

async def scan_structural_audit(node):
    print(f"\n🔬 AUDITANDO ESTRUCTURA: {node['name']}...")
    
    # Protocolo Quirúrgico Quick-HTAG (5 puntos)
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
                "lat_min": lat - 0.015, "lat_max": lat + 0.015,
                "lon_min": lon - 0.015, "lon_max": lon + 0.015,
                "region_name": f"Audit_{node['name']}_{p['dir']}",
                "resolution_m": 80.0 # Aumentamos resolución para la "puerta de hierro"
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
    print(f"📊 RESULTADO AUDITORÍA G1: {avg_g1:.4f}")
    
    return {"node": node['name'], "avg_g1": avg_g1}

async def main():
    print("="*80)
    print("🛡️ ARCHEOSCOPE: AUDITORÍA ESTRUCTURAL (EJE MONTE)")
    print("="*80)
    
    mission_log = []
    for node in MONTE_CORE_NODES:
        res = await scan_structural_audit(node)
        mission_log.append(res)
        
    print("\n" + "="*80)
    print("🏁 INFORME DE AUDITORÍA FINALIZADO")
    print("="*80)
    for m in mission_log:
        status = "🔥 ANOMALÍA ESTRUCTURAL" if m['avg_g1'] > 0.90 else "❄️ GEOLOGÍA DOMINANTE"
        print(f"- {m['node']}: G1 {m['avg_g1']:.4f} -> {status}")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
