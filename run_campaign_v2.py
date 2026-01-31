import asyncio
import httpx
import json
import os
from datetime import datetime

async def run_discovery_campaign_v2():
    # Definición de los nuevos objetivos científicos
    targets = [
        {
            "id": "gunung_padang",
            "name": "Gunung Padang (Indonesia) - Subsurface Stratigraphy",
            "lat": -6.9956,
            "lon": 107.0560,
            "delta": 0.0045,  # ~0.8 km²
            "mode": "Subsurface / Anthropogenic",
            "description": "Modelado de terrazas y rellenos antróficos sobre base volcánica."
        },
        {
            "id": "zona_del_silencio",
            "name": "Zona del Silencio (Mexico) - Arid Pattern Detection",
            "lat": 26.6850,
            "lon": -103.7550,
            "delta": 0.015,   # ~8 km²
            "mode": "Hybrid Subsurface + Surface",
            "description": "Detección de alineamientos líticos y corrales antiguos en entorno desértico."
        }
    ]
    
    url = "http://localhost:8003/api/scientific/analyze"
    campaign_results = {}
    
    print(f"\n🚀 INICIANDO CAMPAÑA DE DESCUBRIMIENTO V2: GUNUNG PADANG & ZONA DEL SILENCIO")
    print(f"=========================================================================")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        for target in targets:
            payload = {
                "lat_min": target["lat"] - target["delta"],
                "lat_max": target["lat"] + target["delta"],
                "lon_min": target["lon"] - target["delta"],
                "lon_max": target["lon"] + target["delta"],
                "region_name": target["name"]
            }
            
            print(f"\n🔬 Ejecutando escaneo: {target['name']}...")
            try:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    campaign_results[target["id"]] = result
                    print(f"✅ Completado. ESS Score: {result.get('archaeological_results', {}).get('anomaly_score', 0):.3f}")
                else:
                    print(f"❌ Error en {target['name']}: {response.status_code}")
                    print(response.text)
            except Exception as e:
                print(f"❌ Excepción en {target['name']}: {e}")
                
    # Guardar resultados en JSON para persistencia local
    with open("campaign_v2_results.json", "w", encoding="utf-8") as f:
        json.dump(campaign_results, f, indent=2, ensure_ascii=False)
        
    print(f"\n💾 Campaña V2 completada. Datos guardados en campaign_v2_results.json")
    return campaign_results

if __name__ == "__main__":
    asyncio.run(run_discovery_campaign_v2())
