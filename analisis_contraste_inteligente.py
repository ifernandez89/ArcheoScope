import asyncio
import httpx
import json
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

# COORDINATES FOR CONTRAST TEST
# 1. Anatolia SE (Confirmed HTAG-CTA)
# 2. Central Valley, CA (Modern Industrial Agriculture - Grid)
# 3. Brasilia (Modern Planned City - Axial)

SITES = [
    {"name": "Anatolia_SE_CTA", "lat": 37.15, "lon": 39.05, "type": "HTAG_ANOMALY"},
    {"name": "California_Grid", "lat": 36.5, "lon": -120.0, "type": "MODERN_INDUSTRIAL"},
    {"name": "Brasilia_Axial", "lat": -15.78, "lon": -47.93, "type": "MODERN_PLANNED"}
]

async def contrast_analysis():
    print("="*80)
    print("🧪 CONTRASTE INTELIGENTE: DEFINIENDO LA FIRMA HTAG-CTA")
    print("="*80)
    
    results = []
    async with httpx.AsyncClient(timeout=300.0) as client:
        for s in SITES:
            print(f"\n📡 ANALIZANDO: {s['name']} ({s['type']})...")
            payload = {
                "lat_min": s["lat"] - 0.02, "lat_max": s["lat"] + 0.02,
                "lon_min": s["lon"] - 0.02, "lon_max": s["lon"] + 0.02,
                "region_name": f"Contrast_{s['name']}",
                "resolution_m": 100.0
            }
            try:
                response = await client.post(URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    g1 = data['official_classification']['metrics_applied'].get('g1_geometry', 0)
                    hrm = data.get('scientific_output', {}).get('hrm_analysis', {})
                    
                    print(f"   ✅ G1 Score: {g1:.4f}")
                    results.append({"name": s["name"], "g1": g1, "type": s["type"]})
            except:
                print(f"   ❌ Error en {s['name']}")

    print("\n" + "="*80)
    print("🏁 INFORME DE CONTRASTE")
    print("="*80)
    # Comparison logic
    for r in results:
        print(f"- {r['name']}: G1 {r['g1']:.4f} [{r['type']}]")
    
    print("\n📦 CONCLUSIÓN ESTRATÉGICA:")
    print("  - Si HTAG-CTA (Anatolia) iguala o supera a California/Brasilia, estamos ante")
    print("    una ingeniería territorial de escala y precisión industrial moderna.")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(contrast_analysis())
