#!/usr/bin/env python3
"""
MISIÓN DE PREDICCIÓN CIEGA - PRIORIDAD ALTA (F + E)
==================================================

1. AMAZONÍA OCCIDENTAL (Interfluvios) - El Bombazo
2. MESOPOTAMIA NORTE (Tells agrícolas) - El Ziggurat Fantasma

Autor: Antigravity AI
Fecha: 2026-02-02
"""

import asyncio
import httpx
import json
from datetime import datetime

PRIORITY_SITES = [
    {
        "id": "BLIND_F",
        "name": "Amazonía Occidental (Brasil/Perú)",
        "lat": -6.500,
        "lon": -69.000,
        "delta_km": 4.0,
        "context": "Interfluvios selva, geoglifos, tierra negra",
        "prediction": "Patrón 2+1 en terraplenes, CHI 0.75-0.85",
        "material_expected": "Tierra armada / Terra Preta"
    },
    {
        "id": "BLIND_E",
        "name": "Mesopotamia Norte (Iraq/Siria)",
        "lat": 36.300,
        "lon": 41.000,
        "delta_km": 2.5,
        "context": "Tells agrícolas, origen urbano",
        "prediction": "Reinterpretación tell triple, Ziggurat fantasma",
        "material_expected": "Ladrillo de barro / Adobe"
    }
]

async def analyze_with_retry(client, url, payload, retries=3):
    for i in range(retries):
        try:
            response = await client.post(url, json=payload, timeout=600.0) # Aumentado el timeout para selva
            if response.status_code == 200:
                return response.json()
            else:
                print(f"      ⚠️  Intento {i+1}: HTTP {response.status_code}")
                await asyncio.sleep(5)
        except Exception as e:
            print(f"      ⚠️  Error: {e}")
            await asyncio.sleep(2)
    return None

async def run_priority_mission():
    print("\n" + "="*90)
    print("🚀 MISIÓN PRIORITARIA: AMAZONÍA (F) + MESOPOTAMIA (E)")
    print("="*90)
    
    results = []
    url = "http://localhost:8003/api/scientific/analyze"
    
    async with httpx.AsyncClient(timeout=None) as client:
        for i, site in enumerate(PRIORITY_SITES, 1):
            print(f"\n[{i}/2] ANALIZANDO OBJETIVO: {site['name']}")
            print(f"   📍 {site['lat']}, {site['lon']}")
            print(f"   🎯 Predicción: {site['prediction']}")
            
            delta_deg = site['delta_km'] / 111.0
            payload = {
                "lat_min": site['lat'] - delta_deg,
                "lat_max": site['lat'] + delta_deg,
                "lon_min": site['lon'] - delta_deg,
                "lon_max": site['lon'] + delta_deg,
                "region_name": f"PRIORITY_{site['id']}"
            }
            
            data = await analyze_with_retry(client, url, payload)
            
            if data:
                res = {
                    "site_id": site['id'],
                    "name": site['name'],
                    "veredicto": data.get('official_classification', {}).get('veredicto', 'UNKNOWN'),
                    "is_anthropic": data.get('official_classification', {}).get('is_anthropic', False),
                    "g1_geometry": data.get('etp_summary', {}).get('coherencia_3d', 0),
                    "g3_anomaly": data.get('etp_summary', {}).get('ess_volumetrico', 0),
                    "g4_modularity": data.get('official_classification', {}).get('metrics', {}).get('g4_modularity', 0),
                    "narrative": data.get('etp_summary', {}).get('narrative_explanation', '')
                }
                print(f"   ✅ RESULTADO: {res['veredicto']}")
                print(f"   📊 G1: {res['g1_geometry']:.3f} | G4: {res['g4_modularity']}")
                results.append(res)
            else:
                print(f"   ❌ FALLO EN EL OBJETIVO")

    # Guardar resultados
    out = f"PRIORITY_MISSION_FE_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*90}")
    print(f"✅ CAMPAÑA FINALIZADA -> {out}")
    print(f"{'='*90}\n")

if __name__ == "__main__":
    asyncio.run(run_priority_mission())
