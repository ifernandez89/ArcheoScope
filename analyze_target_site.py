import asyncio
import httpx
import json
import os
from datetime import datetime

async def analyze_site():
    # Coordenadas proporcionadas por el usuario
    lat, lon = 19.05815137760786, -98.30203159437866
    delta = 0.006
    
    payload = {
        "lat_min": lat - delta,
        "lat_max": lat + delta,
        "lon_min": lon - delta,
        "lon_max": lon + delta,
        "region_name": f"Target Site ({lat}, {lon})"
    }
    
    url = "http://localhost:8003/api/scientific/analyze"
    
    print(f"\n🚀 INICIANDO ANÁLISIS CIENTÍFICO: TARGET SITE")
    print(f"====================================================")
    print(f"📍 Coordenadas: {lat}, {lon}")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        try:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ ANÁLISIS COMPLETADO")
                
                # Guardar datos
                filename = "target_site_scan_results.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f"📊 Resultados guardados en: {filename}")
                
                # Mostrar resumen
                print(f"\n📝 RESUMEN DE HALLAZGOS:")
                print(f"- Anomaly Score (ESS): {result.get('ess_score', 'N/A')}")
                print(f"- 3D Coherence: {result.get('geometric_coherence', 'N/A')}")
                print(f"- TAS Score: {result.get('tas_score', 'N/A')}")
                
                return result
            else:
                print(f"❌ ERROR: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")

if __name__ == "__main__":
    asyncio.run(analyze_site())
