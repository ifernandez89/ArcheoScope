#!/usr/bin/env python3
"""
ARCHEOSCOPE - TEST A: ANISOTROPÍA FUNCIONAL
==========================================
Buscando ejes de planificación, drenajes artificiales y alineaciones no naturales.
"""

import asyncio
import httpx
import json
import math
import numpy as np

TARGET_C = {"lat": 37.1500, "lon": 39.0500}
URL = "http://localhost:8003/api/scientific/analyze"

async def scan_line(name, start_lat, start_lon, end_lat, end_lon, steps=10):
    print(f"\n📏 ESCANEANDO EJE: {name}...")
    lats = np.linspace(start_lat, end_lat, steps)
    lons = np.linspace(start_lon, end_lon, steps)
    
    results = []
    async with httpx.AsyncClient(timeout=600.0) as client:
        for i in range(steps):
            payload = {
                "lat_min": lats[i] - 0.002, "lat_max": lats[i] + 0.002,
                "lon_min": lons[i] - 0.002, "lon_max": lons[i] + 0.002,
                "region_name": f"{name}_P{i}",
                "resolution_m": 20.0  # Alta resolución para detectar micro-ejes
            }
            try:
                response = await client.post(URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    g1 = data['official_classification']['metrics_applied']['g1_geometry']
                    results.append(g1)
                    print(f"   [{i}] G1: {g1:.4f}")
            except:
                results.append(0)
    return results

async def main():
    # EJES CARDINALES para detectar planificación ortogonal
    # Eje N-S (1km total)
    ns_axis = await scan_line("Eje Norte-Sur", TARGET_C["lat"] - 0.005, TARGET_C["lon"], TARGET_C["lat"] + 0.005, TARGET_C["lon"])
    
    # Eje E-W (1km total)
    ew_axis = await scan_line("Eje Este-Oeste", TARGET_C["lat"], TARGET_C["lon"] - 0.005, TARGET_C["lat"], TARGET_C["lon"] + 0.005)

    print("\n" + "="*60)
    print("🔬 RESULTADOS TEST A: ANISOTROPÍA")
    print("="*60)
    
    std_ns = np.std(ns_axis)
    std_ew = np.std(ew_axis)
    ratio = std_ns / std_ew if std_ew > 0 else 1
    
    print(f"📊 Varianza N-S: {std_ns:.6f}")
    print(f"📊 Varianza E-W: {std_ew:.6f}")
    print(f"📈 Ratio Anisotropía: {ratio:.4f}")

    if abs(1 - ratio) > 0.15:
        print("\n📢 RESULTADO: ANISOTROPÍA DETECTADA.")
        print("   - Existe un eje de flujo preferente no simétrico.")
        print("   - Sugiere planificación direccional (ejes de movimiento o drenaje).")
    else:
        print("\n📢 RESULTADO: ISOTROPÍA RADIAL.")
        print("   - La estructura es masiva y uniforme en todas las direcciones.")
        print("   - Típico de grandes túmulos habitacionales o centros masivos.")
    
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
