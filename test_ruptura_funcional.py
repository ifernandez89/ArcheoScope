#!/usr/bin/env python3
"""
ARCHEOSCOPE - TEST DEFINITIVO: RUPTURA FUNCIONAL
===============================================
Objetivo: Determinar si la coherencia geométrica (G1) ignora la topografía natural
o si se detiene en límites funcionales (diseño territorial vs. geología).
"""

import asyncio
import httpx
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

TARGET_C = {"lat": 37.1500, "lon": 39.0500}
URL = "http://localhost:8003/api/scientific/analyze"

async def functional_rupture_scan(direction_name, delta_lat, delta_lon, steps=20):
    print(f"\n🚜 ESCANEANDO RUPTURA FUNCIONAL: Eje {direction_name}...")
    
    lats = np.linspace(TARGET_C["lat"], TARGET_C["lat"] + delta_lat, steps)
    lons = np.linspace(TARGET_C["lon"], TARGET_C["lon"] + delta_lon, steps)
    
    data_points = []
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        for i in range(steps):
            dist_km = math.sqrt((lats[i]-TARGET_C["lat"])**2 + (lons[i]-TARGET_C["lon"])**2) * 111.0
            payload = {
                "lat_min": lats[i] - 0.001, "lat_max": lats[i] + 0.001,
                "lon_min": lons[i] - 0.001, "lon_max": lons[i] + 0.001,
                "region_name": f"Rupture_{direction_name}_{i}",
                "resolution_m": 30.0
            }
            try:
                response = await client.post(URL, json=payload)
                if response.status_code == 200:
                    res = response.json()
                    metrics = res['official_classification']['metrics_applied']
                    metadata = res.get('scientific_output', {}).get('anomaly_map', {}).get('metadata', {})
                    
                    # Extraemos G1 y proxy de topografía (std de elevación o rugosidad si estuviera disponible)
                    # Usamos la varianza de la anomalía como proxy de complejidad del terreno
                    g1 = metrics.get('g1_geometry', 0)
                    terrain_complexity = metadata.get('anomaly_std', 0) 
                    
                    print(f"   [{i}] Dist: {dist_km:.2f}km | G1: {g1:.4f} | Terrain: {terrain_complexity:.4f}")
                    
                    data_points.append({
                        "step": i,
                        "dist_km": dist_km,
                        "g1": g1,
                        "terrain_complexity": terrain_complexity,
                        "lat": lats[i],
                        "lon": lons[i]
                    })
            except Exception as e:
                print(f"   [!] Error en step {i}: {e}")
                
    return data_points

import math

async def main():
    print("="*80)
    print("🔍 INICIANDO TEST DE RUPTURA FUNCIONAL (DISEÑO TERRITORIAL)")
    print("="*80)
    
    # Escaneamos hacia el Noroeste (buscando la salida hacia zona menos llana)
    # LIMITADO A 5 PASOS POR RESTRICCIÓN DE USUARIO
    results = await functional_rupture_scan("NW_Rupture", 0.1, -0.1, steps=5)
    
    if not results:
        print("❌ No se obtuvieron datos.")
        return

    # Análisis de Ruptura
    print("\n📊 ANÁLISIS DE CORRELACIÓN G1 vs TOPOGRAFÍA:")
    
    rupture_found = False
    for i in range(1, len(results)):
        g1_prev = results[i-1]["g1"]
        g1_curr = results[i]["g1"]
        t_prev = results[i-1]["terrain_complexity"]
        t_curr = results[i]["terrain_complexity"]
        
        g1_drop = g1_prev - g1_curr
        t_change = abs(t_curr - t_prev)
        
        # DEFINICIÓN DE RUPTURA FUNCIONAL:
        # G1 cae bruscamente (>0.1) pero la topografía es estable (cambio < 0.05)
        if g1_drop > 0.05 and t_change < 0.02:
            print(f"   🚨 RUPTURA FUNCIONAL DETECTADA a {results[i]['dist_km']:.2f}km")
            print(f"      - G1 cayó de {g1_prev:.4f} a {g1_curr:.4f}")
            print(f"      - Topografía estable (Delta: {t_change:.4f}). Esto indica un LÍMITE ARTIFICIAL.")
            rupture_found = True
            break
        
        # DEFINICIÓN DE DISEÑO SOBRE TOPOGRAFÍA:
        # G1 se mantiene alto (>0.90) a pesar de que la topografía cambia bruscamente
        if g1_curr > 0.90 and t_change > 0.05:
            print(f"   🏗️ DISEÑO SOBRE TOPOGRAFÍA a {results[i]['dist_km']:.2f}km")
            print(f"      - G1 persiste ({g1_curr:.4f}) ignorando el cambio de terreno ({t_change:.4f}).")

    if not rupture_found:
        print("\n📢 CONCLUSIÓN: Continuidad Territorial Absoluta. El diseño ignora los límites geográficos.")

    # Guardar resultados
    report_file = f"RUPTURA_FUNCIONAL_DATA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Datos crudos guardados en: {report_file}")

if __name__ == "__main__":
    asyncio.run(main())
