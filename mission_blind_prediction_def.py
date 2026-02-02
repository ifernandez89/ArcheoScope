#!/usr/bin/env python3
"""
MISIÓN DE PREDICCIÓN CIEGA - FASE 2: EXTREMOS Y FRONTERAS
========================================================

Protocolo de Predicción Científica (D, E, F):
- Opción D: Nubia (Corredor del Nilo Medio)
- Opción E: Mesopotamia Norte (Tells agrícolas)
- Opción F: Amazonía Occidental (Interfluvios)

Autor: Antigravity AI
Fecha: 2026-02-02
"""

import asyncio
import httpx
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Configuración de sitios de la Fase 2
FASE_2_SITES = [
    {
        "id": "BLIND_D",
        "name": "Nilo Medio - Nubia (Sudán)",
        "lat": 18.600,
        "lon": 31.800,
        "delta_km": 3.0,
        "context": "Corredor subestudiado, cultura piramidal/monticular nubia",
        "prediction": "CHI alto (2+1 alineado al Nilo), montículos jerárquicos",
        "material_expected": "Piedra arenisca + Adobe"
    },
    {
        "id": "BLIND_E",
        "name": "Mesopotamia Norte (Iraq/Siria)",
        "lat": 36.300,
        "lon": 41.000,
        "delta_km": 2.5,
        "context": "Tells agrícolas no urbanos, origen de la complejidad",
        "prediction": "Reinterpretación de tell triple, Ziggurat fantasma",
        "material_expected": "Ladrillo de barro (Adobe)"
    },
    {
        "id": "BLIND_F",
        "name": "Amazonía Occidental (Brasil/Perú)",
        "lat": -6.500,
        "lon": -69.000,
        "delta_km": 4.0,
        "context": "Interfluvios selva, geoglifos recientes, terra preta",
        "prediction": "Patrón 2+1 en terraplenes, CHI 0.75-0.85 (Anomalía en selva)",
        "material_expected": "Tierra armada (Terra Preta / Arcilla)"
    }
]

async def analyze_with_retry(client, url, payload, retries=3):
    for i in range(retries):
        try:
            response = await client.post(url, json=payload, timeout=300.0)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"      ⚠️  Intento {i+1}: 404 (Esperando al motor...)")
                await asyncio.sleep(5)
            else:
                print(f"      ⚠️  Intento {i+1}: HTTP {response.status_code}")
        except Exception as e:
            print(f"      ⚠️  Error de conexión: {e}")
            await asyncio.sleep(2)
    return None

async def run_phase_2():
    print("\n" + "="*90)
    print("🔬 MISIÓN PREDICCIÓN CIEGA - FASE 2: EXTREMOS Y FRONTERAS")
    print("="*90)
    
    results = []
    url = "http://localhost:8003/api/scientific/analyze"
    
    async with httpx.AsyncClient(timeout=None) as client:
        for i, site in enumerate(FASE_2_SITES, 1):
            print(f"\n[{i}/3] ANALIZANDO: {site['name']}")
            print(f"   📍 Coordenadas: {site['lat']}, {site['lon']}")
            print(f"   🎯 Predicción: {site['prediction']}")
            
            delta_deg = site['delta_km'] / 111.0
            payload = {
                "lat_min": site['lat'] - delta_deg,
                "lat_max": site['lat'] + delta_deg,
                "lon_min": site['lon'] - delta_deg,
                "lon_max": site['lon'] + delta_deg,
                "region_name": f"BLIND_DEF_{site['id']}"
            }
            
            data = await analyze_with_retry(client, url, payload)
            
            if data:
                timt = {
                    "success": True,
                    "classification": data.get('official_classification', {}).get('veredicto', 'UNKNOWN'),
                    "g1_geometry": data.get('etp_summary', {}).get('coherencia_3d', 0),
                    "g2_persistence": data.get('etp_summary', {}).get('persistencia_temporal', 0),
                    "g4_modularity": data.get('official_classification', {}).get('metrics', {}).get('g4_modularity', 0),
                    "msf": data.get('official_classification', {}).get('metrics', {}).get('msf', 1.0),
                    "is_anthropic": data.get('official_classification', {}).get('is_anthropic', False)
                }
                print(f"   ✅ ÉXITO: {timt['classification']} (G1: {timt['g1_geometry']:.3f})")
            else:
                timt = {"success": False, "error": "Failed after retries"}
                print(f"   ❌ FALLO TOTAL")

            results.append({
                "site": site,
                "timt_analysis": timt,
                "timestamp": datetime.utcnow().isoformat()
            })
            
    # Guardar resultados
    filename = f"BLIND_PREDICTION_FASE_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*90}")
    print(f"✅ FASE 2 COMPLETADA -> {filename}")
    print(f"{'='*90}\n")

if __name__ == "__main__":
    asyncio.run(run_phase_2())
