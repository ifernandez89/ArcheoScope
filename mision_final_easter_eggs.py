import asyncio
import httpx
import json
import math
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

EASTER_EGGS = [
    {"name": "EL_DORADO_AMAZONAS", "lat": -3.0, "lon": -60.0, "radius_km": 2.0},
    {"name": "PUERTA_AUSTRALIA", "lat": -12.0, "lon": 142.0, "radius_km": 2.0},
    {"name": "ESTRECHO_DE_ANIAN", "lat": 65.0, "lon": -168.0, "radius_km": 2.0}
]

async def scan_quick_htag(node):
    print(f"\n🥚 INVESTIGANDO MISTERIO: {node['name']}...")
    
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
                "lat_min": lat - 0.015, "lat_max": lat + 0.015,
                "lon_min": lon - 0.015, "lon_max": lon + 0.015,
                "region_name": f"EasterEgg_{node['name']}_{p['dir']}",
                "resolution_m": 120.0
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
    
    if avg_g1 > 0.90:
        status = "🔥 HALLAZGO CRÍTICO (HTAG-PRIME)"
    elif avg_g1 > 0.88:
        status = "ℹ️ RESONANCIA DETECTADA (HTAG-NODAL)"
    else:
        status = "❄️ NATURAL / DISEÑO SIMBÓLICO"
        
    print(f"📢 RESULTADO: {status}")
    return {"node": node['name'], "avg_g1": avg_g1, "status": status}

async def main():
    print("="*80)
    print("🛸 ARCHEOSCOPE: MISIÓN FINAL 'EASTER EGGS' (BIBLIOTECA DE MONTE)")
    print("="*80)
    
    mission_log = []
    for node in EASTER_EGGS:
        res = await scan_quick_htag(node)
        mission_log.append(res)
        
    print("\n" + "="*80)
    print("🏁 INFORME DE LA BIBLIOTECA DE MONTE FINALIZADO")
    print("="*80)
    for m in mission_log:
        print(f"- {m['node']}: G1 {m['avg_g1']:.4f} -> {m['status']}")
    
    # Guardar en JSON para persistencia
    with open("EASTER_EGGS_RESULTS.json", "w") as f:
        json.dump(mission_log, f, indent=2)
    
    print("\n✅ Datos registrados y listos para su incorporación al Canon.")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
