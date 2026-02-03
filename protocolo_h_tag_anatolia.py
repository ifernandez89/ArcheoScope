#!/usr/bin/env python3
"""
ARCHEOSCOPE - PROTOCOLO HTAG (High Coherence Territorial Anthropic Anomaly)
==========================================================================
Misión: Validación Científica Rigurosa del Target C (Anatolia).

MOVIMIENTO 1: Gradiente Radial Fino (Anillos 250m - 2km)
MOVIMIENTO 2: Análisis de Centro Negativo
MOVIMIENTO 3: Cruce Hidrológico/Ejes (Inferencia de Datos)
MOVIMIENTO 4: Blind Test Lejano (100km)
"""

import asyncio
import httpx
import json
import math
import os
from datetime import datetime

# Configuración Base
TARGET_C = {"lat": 37.1500, "lon": 39.0500, "name": "Target C"}
URL = "http://localhost:8003/api/scientific/analyze"

# Movimiento 1 & 4 Config
RADII_KM = [0.25, 0.5, 1.0, 2.0]
DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
FAR_CONTROLS = [
    {"name": "Control Lejano Norte (+100km)", "lat": 38.0500, "lon": 39.0500},
    {"name": "Control Lejano Este (+100km)", "lat": 37.1500, "lon": 40.1500},
    {"name": "Control Lejano Oeste (-100km)", "lat": 37.1500, "lon": 37.9500}
]

async def scan_point(name, lat, lon, resolution=50.0, delta_km=0.5):
    delta_deg = delta_km / 111.0
    payload = {
        "lat_min": lat - delta_deg,
        "lat_max": lat + delta_deg,
        "lon_min": lon - delta_deg,
        "lon_max": lon + delta_deg,
        "region_name": name,
        "resolution_m": resolution
    }
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        try:
            response = await client.post(URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                official = data.get('official_classification', {})
                metrics = official.get('metrics_applied', {})
                return {
                    "name": name,
                    "lat": lat,
                    "lon": lon,
                    "g1": metrics.get('g1_geometry', 0),
                    "g4": metrics.get('g4_modularity', 0),
                    "veredicto": official.get('veredicto', 'UNKNOWN'),
                    "sci": data.get('scientific_output', {})
                }
        except Exception as e:
            print(f"   [!] Error en {name}: {e}")
    return None

def get_offset(radius_km, angle_deg):
    # Simplificación: 1 deg lat = 111km, 1 deg lon = 111 * cos(lat)
    lat_off = (radius_km * math.cos(math.radians(angle_deg))) / 111.32
    lon_off = (radius_km * math.sin(math.radians(angle_deg))) / (111.32 * math.cos(math.radians(37.15)))
    return lat_off, lon_off

async def main():
    print("="*90)
    print("🛡️ PROTOCOLO HTAG: AUTOPSIA CIENTÍFICA BLINDADA")
    print("="*90)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "target_center": {},
        "radial_rings": [],
        "far_controls": []
    }

    # 0. SCAN DEL CENTRO (Para Movimiento 2)
    print("\n[M2] Analizando Centro del Nodo...")
    res_center = await scan_point("Target C Center", TARGET_C["lat"], TARGET_C["lon"], resolution=30.0)
    results["target_center"] = res_center
    if res_center:
        print(f"   🎯 Centro G1: {res_center['g1']:.4f}")

    # 1. MOVIMIENTO 1: ANILLOS RADIALES
    print(f"\n[M1] Ejecutando Granulometría Radial ({len(RADII_KM)} anillos x 8 pts)...")
    for r in RADII_KM:
        print(f"   🌑 Anillo {r*1000}m...")
        ring_data = {"radius_km": r, "points": []}
        for i, dir_name in enumerate(DIRECTIONS):
            angle = i * 45
            lat_off, lon_off = get_offset(r, angle)
            res = await scan_point(f"Ring_{r}_{dir_name}", TARGET_C["lat"] + lat_off, TARGET_C["lon"] + lon_off, resolution=50.0)
            if res:
                ring_data["points"].append(res)
                print(f"      {dir_name}: G1={res['g1']:.3f} | {res['veredicto']}")
        results["radial_rings"].append(ring_data)

    # 4. MOVIMIENTO 4: BLIND TEST LEJANO
    print("\n[M4] Ejecutando Controles Lejanos (80-120km)...")
    for ctrl in FAR_CONTROLS:
        res = await scan_point(ctrl["name"], ctrl["lat"], ctrl["lon"], resolution=150.0)
        if res:
            results["far_controls"].append(res)
            print(f"   🏠 {ctrl['name']}: G1={res['g1']:.4f} | {res['veredicto']}")

    # Guardar Reporte HTAG
    report_file = f"HTAG_ANATOLIA_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*90)
    print("🏁 PROTOCOLO COMPLETADO - REPORTE GENERADO")
    print(f"📄 Archivo: {report_file}")
    
    # Resumen Ejecutivo
    print("\n📊 DIAGNÓSTICO PRELIMINAR:")
    if res_center:
        # Movimiento 2 Check
        avg_inner_g1 = sum(p['g1'] for p in results["radial_rings"][0]["points"]) / 8
        if res_center['g1'] < avg_inner_g1:
            print("   ✅ M2: CENTRO NEGATIVO DETECTADO (Espacio Ritual/Plaza).")
        else:
            print("   ℹ️ M2: Centro Sólido (Estructura Masiva).")
            
        # Movimiento 4 Check
        max_far_g1 = max([c['g1'] for c in results["far_controls"]])
        if res_center['g1'] > max_far_g1 + 0.05:
            print(f"   ✅ M4: ANOMALÍA SELLADA (Delta vs Far: +{res_center['g1'] - max_far_g1:.4f}).")
    print("="*90)

if __name__ == "__main__":
    asyncio.run(main())
