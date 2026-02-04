import asyncio
import httpx
import json
import math
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

AUDIT_NODES = [
    {"name": "ANATOLIA_SE", "lat": 37.15, "lon": 39.05},
    {"name": "PATAGONIA_ARG", "lat": -44.5, "lon": -69.0},
    {"name": "ANTARTIDA_CTRL", "lat": -64.8, "lon": -62.9}
]

async def scan_site(site):
    print(f"\n📡 AUDITANDO NODO: {site['name']}...")
    
    # 3 Puntos: Centro, Norte (1.5km), Este (1.5km)
    points = [
        {"dir": "CENTER", "d_lat": 0, "d_lon": 0},
        {"dir": "NORTH", "d_lat": 1.5/111, "d_lon": 0},
        {"dir": "EAST", "d_lat": 0, "d_lon": 1.5/(111 * math.cos(math.radians(site['lat'])))}
    ]
    
    results = []
    async with httpx.AsyncClient(timeout=300.0) as client:
        for p in points:
            lat = site["lat"] + p["d_lat"]
            lon = site["lon"] + p["d_lon"]
            payload = {
                "lat_min": lat - 0.012, "lat_max": lat + 0.012,
                "lon_min": lon - 0.012, "lon_max": lon + 0.012,
                "region_name": f"SyncTest_{site['name']}_{p['dir']}",
                "resolution_m": 100.0
            }
            try:
                response = await client.post(URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    g1 = data['official_classification']['metrics_applied'].get('g1_geometry', 0)
                    results.append({"dir": p["dir"], "g1": g1})
                    print(f"   [{p['dir']}] G1: {g1:.4f}")
            except:
                print(f"   [{p['dir']}] ERROR")
                results.append({"dir": p["dir"], "g1": 0})
    
    avg_g1 = sum(r['g1'] for r in results) / len(results) if results else 0
    print(f"📊 AVG G1 para {site['name']}: {avg_g1:.4f}")
    return {"site": site['name'], "results": results, "avg": avg_g1}

async def main():
    print("="*70)
    print("🔬 TEST DE SINCRONICIDAD ESTRUCTURAL: FINAL PIPELINE")
    print("="*70)
    
    final_data = []
    for site in AUDIT_NODES:
        res = await scan_site(site)
        final_data.append(res)
        
    print("\n" + "="*70)
    print("🏁 RESULTADO COMPARATIVO FINAL")
    print("="*70)
    for d in final_data:
        # Clasificación simplificada para auditoría
        status = "🔥 HTAG-VALIDATED" if d['avg'] > 0.90 else "❄️ NATURAL-BASELINE"
        print(f"- {d['site']}: {d['avg']:.4f} -> {status}")
    print("="*70)
    
    # Guardar reporte definitivo
    with open("FINAL_SYNC_AUDIT_REPORT.json", "w") as f:
        json.dump(final_data, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
