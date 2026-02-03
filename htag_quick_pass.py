import asyncio
import httpx
import json

TARGETS = [
    {"name": "Valle del Ferganá", "lat": 40.4, "lon": 71.8},
    {"name": "Piedemonte Indo-Iraní", "lat": 28.8, "lon": 66.6},
    {"name": "África Oriental interior", "lat": 15.3, "lon": 32.5}
]
URL = "http://localhost:8003/api/scientific/analyze"

async def htag_quick_pass(name, lat, lon):
    print(f"\n🚀 HTAG QUICK PASS: {name}...")
    # Radio 2km -> 0.018 grados aprox
    delta = 0.018
    payload = {
        "lat_min": lat - delta, "lat_max": lat + delta,
        "lon_min": lon - delta, "lon_max": lon + delta,
        "region_name": f"QuickPass_{name}",
        "resolution_m": 150.0  # Liviano
    }
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(URL, json=payload)
            if response.status_code == 200:
                res = response.json()
                official = res.get('official_classification', {})
                metrics = official.get('metrics_applied', {})
                g1 = metrics.get('g1_geometry', 0)
                veredicto = official.get('veredicto', 'UNKNOWN')
                
                print(f"   ✅ RESULTADO: G1={g1:.4f} | Veredicto: {veredicto}")
                
                # Criterio de Decisión
                if g1 < 0.88:
                    status = "❌ DISCARD (Natural/Noise)"
                elif g1 <= 0.92:
                    status = "ℹ️ NOTE (Low Interest)"
                else:
                    status = "🔥 DEEPEN (High HTAG Potential)"
                
                print(f"   📢 DECISION: {status}")
                return {"name": name, "g1": g1, "veredicto": veredicto, "status": status}
            else:
                print(f"   ❌ ERROR {response.status_code}")
        except Exception as e:
            print(f"   [!] Error: {e}")
    return None

async def main():
    print("="*60)
    print("🌍 INICIANDO BARRIDO GLOBAL: PROTOCOLO ULTRA-LIVIANO")
    print("="*60)
    
    results = []
    for t in TARGETS:
        res = await htag_quick_pass(t["name"], t["lat"], t["lon"])
        if res:
            results.append(res)
            
    print("\n" + "="*60)
    print("🏁 RESUMEN DE MISIÓN")
    print("="*60)
    for r in results:
        print(f" - {r['name']}: G1={r['g1']:.3f} -> {r['status']}")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
