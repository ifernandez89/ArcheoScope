import asyncio
import httpx
import json
import os
from datetime import datetime

async def run_machu_picchu_benchmark():
    # Coordenadas y zonas clave para validación (Machu Picchu Mode)
    # Delta pequeño para máxima resolución: 0.002 (~220m)
    targets = [
        {
            "id": "mp_agriculture",
            "name": "Machu Picchu - Sector Agrícola (Terrazas)",
            "lat": -13.1631,
            "lon": -72.5450,
            "delta": 0.002
        },
        {
            "id": "mp_urban",
            "name": "Machu Picchu - Sector Urbano (Control Estructural)",
            "lat": -13.1632,
            "lon": -72.5459,
            "delta": 0.002
        },
        {
            "id": "mp_north_slope",
            "name": "Machu Picchu - Ladera Norte (Ingeniería Extrema)",
            "lat": -13.1615,
            "lon": -72.5448,
            "delta": 0.002
        }
    ]
    
    url = "http://localhost:8003/api/scientific/analyze"
    benchmark_results = {}
    
    print(f"\n🏔️ INICIANDO BENCHMARK GLOBAL: MACHU PICCHU (VALIDACIÓN DE SISTEMA)")
    print(f"================================================================")
    print(f"🛠️ Configuración: Subsurface Structural | Depth 0-8m | High Slope Sens")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        for target in targets:
            payload = {
                "lat_min": target["lat"] - target["delta"],
                "lat_max": target["lat"] + target["delta"],
                "lon_min": target["lon"] - target["delta"],
                "lon_max": target["lon"] + target["delta"],
                "region_name": target["name"]
            }
            
            print(f"\n🔍 Escaneando: {target['name']}...")
            try:
                # El backend gestiona los filtros (Slope/Hydro) internamente según el contexto TCP
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    benchmark_results[target["id"]] = result
                    
                    arch = result.get('archaeological_results', {})
                    etp = result.get('etp_summary', {})
                    
                    print(f"✅ Completado. Anomaly Score: {arch.get('anomaly_score', 0):.3f}")
                    print(f"🧱 ESS Volumétrico: {etp.get('ess_volumetrico', 0):.3f}")
                    print(f"📏 DIL Score (Profundidad): {result.get('scientific_output', {}).get('dil_score', 0):.3f}")
                else:
                    print(f"❌ Error en {target['name']}: {response.status_code}")
            except Exception as e:
                print(f"❌ Excepción en {target['name']}: {e}")

    # Persistencia de resultados
    output_filename = "machu_picchu_benchmark_results.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Benchmark completado. Datos guardados en {output_filename}")
    return benchmark_results

if __name__ == "__main__":
    asyncio.run(run_machu_picchu_benchmark())
