#!/usr/bin/env python3
"""
ARCHEOSCOPE - MISIÓN QUIRÚRGICA DE NODOS (G4-DRIVEN)
===================================================

Estrategia: Localizar NODOS aislados, no paisajes.
Filtro: El veredicto depende del G4 (Modularidad/Nodos).

Blancos:
1. Cholula (México) - El Nodo Gigante
2. Gunung Padang (Indonesia) - El Enigma Vertical
3. Nubia Central (Sudán) - La Predicción de Montículo

Autor: Antigravity AI
Fecha: 2026-02-02
"""

import asyncio
import httpx
import json
from datetime import datetime

SURGICAL_NODES = [
    {
        "id": "NODE_CHOLULA",
        "name": "Gran Pirámide de Cholula (México)",
        "lat": 19.0575,
        "lon": -98.3033,
        "delta_km": 0.8, # Muy cerrado al NODO
        "prediction": "G4 masivo (>500), CHI 2+1 probable tras erosión vertical",
        "type": "Confirmed Node"
    },
    {
        "id": "NODE_GUNUNG",
        "name": "Gunung Padang (Indonesia)",
        "lat": -6.9958,
        "lon": 107.0561,
        "delta_km": 1.0,
        "prediction": "HRM peaks críticos en estratos profundos. G4 moderado.",
        "type": "Controversial Node"
    },
    {
        "id": "NODE_NUBIA",
        "name": "Montículo Nubia (Catarata 4, Sudán)",
        "lat": 18.421,
        "lon": 32.484,
        "delta_km": 1.5,
        "prediction": "G4 > 20 → Validación de estructura piramidal erosionada.",
        "type": "Blind Prediction Node"
    }
]

async def analyze_surgical_node(client, url, site):
    """Ejecuta un análisis enfocado en el NODO."""
    delta_deg = site['delta_km'] / 111.0
    payload = {
        "lat_min": site['lat'] - delta_deg,
        "lat_max": site['lat'] + delta_deg,
        "lon_min": site['lon'] - delta_deg,
        "lon_max": site['lon'] + delta_deg,
        "region_name": f"SURGICAL_NODE_{site['id']}"
    }
    
    try:
        print(f"   📡 Escaneando NODO: {site['name']}...")
        response = await client.post(url, json=payload, timeout=600.0)
        
        if response.status_code == 200:
            data = response.json()
            metrics = data.get('official_classification', {}).get('metrics', {})
            g4 = metrics.get('g4_modularity', 0)
            veredicto = data.get('official_classification', {}).get('veredicto', 'UNKNOWN')
            
            # FILTRO CRÍTICO G4
            status_color = "🟢" if g4 >= 20 else "🔴"
            print(f"   {status_color} G4 detectado: {g4}")
            print(f"      Veredicto: {veredicto}")
            
            return {
                "id": site['id'],
                "name": site['name'],
                "g1_geometry": metrics.get('g1_geometry', 0),
                "g4_modularity": g4,
                "msf": metrics.get('msf', 1.0),
                "veredicto": veredicto,
                "anthropic": data.get('official_classification', {}).get('is_anthropic', False),
                "action": data.get('archaeological_results', {}).get('recommended_action', ''),
                "raw_data": data
            }
        else:
            print(f"   ❌ Error API {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error conexión: {e}")
        return None

async def main():
    print("\n" + "="*90)
    print("🔬 ARCHEOSCOPE: MISIÓN QUIRÚRGICA DE NODOS (FASE DE ALTA SEÑAL)")
    print("="*90)
    print(f"Estrategia: Ignorar paisajes, cazar NODOS con G4 > 20.\n")
    
    url = "http://localhost:8003/api/scientific/analyze"
    results = []
    
    async with httpx.AsyncClient(timeout=None) as client:
        for site in SURGICAL_NODES:
            print(f"\n🎯 OBJETIVO: {site['name']} ({site['type']})")
            res = await analyze_surgical_node(client, url, site)
            if res:
                results.append(res)
    
    # Reporte Final Quirúrgico
    filename = f"SURGICAL_MISSION_RESULTS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        # No guardamos todo el raw_data para el JSON de reporte limpio
        clean_results = [{k: v for k, v in r.items() if k != 'raw_data'} for r in results]
        json.dump(clean_results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*90)
    print("📊 RESUMEN QUIRÚRGICO FINAL")
    print("="*90)
    for r in results:
        indicator = "✅ [HIT]" if r['g4_modularity'] >= 20 else "❌ [NOISE]"
        print(f"{indicator} {r['name']:<40} | G4: {r['g4_modularity']:>4} | {r['veredicto']}")
    
    print(f"\n📄 Reporte guardado en: {filename}")
    print("="*90 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
