import asyncio
import httpx
import json
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

SYNC_POINTS = [
    {"name": "Malaca_Synchronicity", "lat": 2.2, "lon": 102.2}, # Nodo de tránsito forzado por Monte
    {"name": "Zambia_Interior", "lat": -14.1, "lon": 28.5}     # Punto de orden en el planisferio de 1587
]

async def monte_synchronicity_test():
    print("="*80)
    print("🧭 PROTOCOLO: SINCRONÍA DE URBANO MONTE (ZONA GRIS)")
    print("="*80)
    
    results = []
    async with httpx.AsyncClient(timeout=300.0) as client:
        for p in SYNC_POINTS:
            print(f"\n📡 ESCANEANDO NODO: {p['name']}...")
            payload = {
                "lat_min": p["lat"] - 0.02, "lat_max": p["lat"] + 0.02,
                "lon_min": p["lon"] - 0.02, "lon_max": p["lon"] + 0.02,
                "region_name": f"MonteSync_{p['name']}",
                "resolution_m": 150.0
            }
            try:
                response = await client.post(URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    g1 = data['official_classification']['metrics_applied'].get('g1_geometry', 0)
                    veredicto = data['official_classification']['veredicto']
                    
                    print(f"   ✅ G1 Detector: {g1:.4f} | Veredicto: {veredicto}")
                    
                    status = "🔥 SINCRONÍA HIGH" if g1 > 0.90 else "ℹ️ BAJA RESONANCIA"
                    print(f"   📢 RESULTADO: {status}")
                    
                    results.append({"name": p["name"], "g1": g1, "veredicto": veredicto, "status": status})
            except Exception as e:
                print(f"   ❌ ERROR en {p['name']}: {e}")

    # Reporte Final de Sincronía
    report_file = f"MONTE_SYNCHRONICITY_REPORT_{datetime.now().strftime('%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("🏁 MISIÓN FINALIZADA")
    print(f"📄 Reporte: {report_file}")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(monte_synchronicity_test())
