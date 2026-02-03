import asyncio
import httpx
import json
import math
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

ZONES = [
    {
        "name": "Z1_PATAGONIA",
        "center": {"lat": -44.5, "lon": -69.0},
        "points": [
            {"dir": "CENTER", "d_lat": 0, "d_lon": 0},
            {"dir": "NORTH", "d_lat": 1.5/111, "d_lon": 0},
            {"dir": "WEST", "d_lat": 0, "d_lon": -1.5/(111 * math.cos(math.radians(-44.5)))}
        ]
    },
    {
        "name": "Z2_MALVINAS_PLAT",
        "center": {"lat": -52.0, "lon": -58.5},
        "points": [
            {"dir": "CENTER", "d_lat": 0, "d_lon": 0},
            {"dir": "EAST", "d_lat": 0, "d_lon": 2.0/(111 * math.cos(math.radians(-52.0)))},
            {"dir": "SOUTH", "d_lat": -2.0/111, "d_lon": 0}
        ]
    },
    {
        "name": "Z3_ANTARTIDA",
        "center": {"lat": -64.8, "lon": -62.9},
        "points": [
            {"dir": "CENTER", "d_lat": 0, "d_lon": 0},
            {"dir": "NE", "d_lat": (1.0*math.sin(math.radians(45)))/111, "d_lon": (1.0*math.cos(math.radians(45)))/(111*math.cos(math.radians(-64.8)))},
            {"dir": "SW", "d_lat": (-1.0*math.sin(math.radians(45)))/111, "d_lon": (-1.0*math.cos(math.radians(45)))/(111*math.cos(math.radians(-64.8)))}
        ]
    }
]

async def scan_point(zone_name, p):
    lat = zone_name["center"]["lat"] + p["d_lat"]
    lon = zone_name["center"]["lon"] + p["d_lon"]
    name = f"{zone_name['name']}_{p['dir']}"
    
    payload = {
        "lat_min": lat - 0.01, "lat_max": lat + 0.01,
        "lon_min": lon - 0.01, "lon_max": lon + 0.01,
        "region_name": name,
        "resolution_m": 150.0
    }
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                metrics = data['official_classification']['metrics_applied']
                return {
                    "dir": p["dir"],
                    "g1": metrics.get('g1_geometry', 0),
                    "veredicto": data['official_classification']['veredicto']
                }
        except:
            return {"dir": p["dir"], "g1": 0, "veredicto": "ERROR"}
    return None

async def main():
    print("="*70)
    print("🧭 PROTOCOLO HTAG-9: HEMISFERIO SUR (EJE URBANO MONTE)")
    print("="*70)
    
    full_results = {}
    
    for zone in ZONES:
        print(f"\n📡 ESCANEANDO: {zone['name']}...")
        zone_data = []
        for p in zone["points"]:
            res = await scan_point(zone, p)
            if res:
                zone_data.append(res)
                print(f"   [{res['dir']}] G1: {res['g1']:.4f} | {res['veredicto']}")
        full_results[zone["name"]] = zone_data

    # Guardar reporte crudo
    report_file = f"HTAG9_RAW_RESULTS_{datetime.now().strftime('%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(full_results, f, indent=2)
    
    print("\n" + "="*70)
    print("🏁 PROTOCOLO COMPLETADO")
    print(f"📄 Datos guardados: {report_file}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
