#!/usr/bin/env python3
"""
ARCHEOSCOPE - AUTOPSIA DEL TARGET C
====================================
Misión de Validación Estadística y Anatómica Rigurosa.

FASE 1: Controles Negativos (N, E, S)
FASE 2: Anatomía de Alta Resolución (50m)
FASE 3: Evaluación Conceptual
"""

import asyncio
import httpx
import json
import os
from datetime import datetime

# Configuración del Target C
TARGET_C = {
    "lat": 37.1500,
    "lon": 39.0500,
    "name": "Target C (Original)"
}

# Cálculo de offsets para 15km
# 1 deg lat ~ 111 km
# 1 deg lon ~ 111 * cos(37.15) ~ 88.6 km
LAT_OFFSET = 15 / 111.32
LON_OFFSET = 15 / (111.32 * 0.797)

CONTROLS = [
    {"name": "Control Norte (+15km)", "lat": TARGET_C["lat"] + LAT_OFFSET, "lon": TARGET_C["lon"]},
    {"name": "Control Este (+15km)", "lat": TARGET_C["lat"], "lon": TARGET_C["lon"] + LON_OFFSET},
    {"name": "Control Sur (-15km)", "lat": TARGET_C["lat"] - LAT_OFFSET, "lon": TARGET_C["lon"]}
]

URL = "http://localhost:8003/api/scientific/analyze"

async def run_scan(name, lat, lon, resolution=150.0, delta_km=1.0):
    delta_deg = delta_km / 111.0
    payload = {
        "lat_min": lat - delta_deg,
        "lat_max": lat + delta_deg,
        "lon_min": lon - delta_deg,
        "lon_max": lon + delta_deg,
        "region_name": name,
        "resolution_m": resolution
    }
    
    print(f"\n📡 ESCANEANDO: {name}...")
    print(f"   📍 {lat:.4f}, {lon:.4f} | Res: {resolution}m")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        try:
            response = await client.post(URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                official = data.get('official_classification', {})
                metrics = official.get('metrics_applied', {})
                g1 = metrics.get('g1_geometry', 0)
                veredicto = official.get('veredicto', 'UNKNOWN')
                
                print(f"   ✅ COMPLETADO - G1: {g1:.4f} | Veredicto: {veredicto}")
                return {
                    "name": name,
                    "lat": lat,
                    "lon": lon,
                    "g1": g1,
                    "g4": metrics.get('g4_modularity', 0),
                    "veredicto": veredicto,
                    "full_data": data
                }
            else:
                print(f"   ❌ ERROR {response.status_code}")
                return None
        except Exception as e:
            print(f"   ❌ EXCEPCIÓN: {e}")
            return None

async def main():
    print("="*90)
    print("🔬 ARCHEOSCOPE: AUTOPSIA PROTOCOLARIA DEL TARGET C")
    print("="*90)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "controls": [],
        "target_c_high_res": None
    }
    
    # FASE 1: CONTROLES NEGATIVOS
    print("\n[FASE 1] Ejecutando 3 controles espejo (Validación Estadística)...")
    for control in CONTROLS:
        res = await run_scan(control["name"], control["lat"], control["lon"], resolution=150.0)
        if res:
            results["controls"].append(res)
    
    # FASE 2: ANATOMÍA DE ALTA RESOLUCIÓN (TARGET C)
    print("\n[FASE 2] Anatomía del Nodo (Escaneo Quirúrgico 50m)...")
    target_res = await run_scan("Target C (Autopsia 50m)", TARGET_C["lat"], TARGET_C["lon"], resolution=50.0)
    if target_res:
        results["target_c_high_res"] = target_res
        
        # Extraer detalles específicos solicitados
        sci_output = target_res["full_data"].get("scientific_output", {})
        hrm = sci_output.get("hrm_analysis", {})
        
        print("\n🔍 DETALLES ANATÓMICOS (HRM & SAR):")
        print(f"   - Eje Dominante/Estructura: {hrm.get('analisis_morfologico', 'Analizando...')}")
        print(f"   - Probabilidad Antrópica: {sci_output.get('anthropic_origin_probability', 'N/A')}")
        print(f"   - Recomendación: {sci_output.get('recommended_action', 'N/A')}")
    
    # Guardar Reporte Final de Autopsia
    report_file = f"AUTOPSIA_TARGET_C_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print("\n" + "="*90)
    print("🏁 AUTOPSIA FINALIZADA")
    print(f"📄 Reporte generado: {report_file}")
    
    # Comparativa rápida
    print("\n📊 COMPARATIVA ESTADÍSTICA (G1):")
    for c in results["controls"]:
        status = "PASSED" if c["g1"] < 0.90 else "WARNING"
        print(f"   - {c['name']}: {c['g1']:.4f} ({status})")
    
    if results["target_c_high_res"]:
        g1_trg = results["target_c_high_res"]["g1"]
        diff = g1_trg - max([c["g1"] for c in results["controls"]] if results["controls"] else [0])
        print(f"   - TARGET C @ 50m: {g1_trg:.4f} (Δ vs Controles: +{diff:.4f})")
    print("="*90 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
