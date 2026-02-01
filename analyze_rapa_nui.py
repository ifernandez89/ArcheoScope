import asyncio
import httpx
import json
import os
from datetime import datetime

async def analyze_rapa_nui():
    # Coordenadas proporcionadas: {-27.112414483608426, -109.39492370163526}
    # Rapa Nui (Isla de Pascua), Chile.
    lat = -27.11241
    lon = -109.39492
    delta = 0.005  # Área de ~1km x 1km
    
    payload = {
        "lat_min": lat - delta,
        "lat_max": lat + delta,
        "lon_min": lon - delta,
        "lon_max": lon + delta,
        "region_name": "Rapa Nui - Sector Ahu Akivi / Interior"
    }
    
    url = "http://localhost:8003/api/scientific/analyze"
    
    print(f"\n🚀 INICIANDO ANÁLISIS CIENTÍFICO: RAPA NUI")
    print(f"==============================================")
    print(f"📍 Coordenadas: {lat}, {lon}")
    print(f"📐 Área: ~1.2 km²")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        try:
            print(f"\n🔍 Ejecutando escaneo tomográfico (TIMT)...")
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
                
                # Resumen de resultados
                analysis_id = result.get('analysis_id')
                arch_results = result.get('archaeological_results', {})
                etp = result.get('etp_summary', {})
                
                print(f"🆔 ID: {analysis_id}")
                print(f"🎯 Anomaly Score: {arch_results.get('anomaly_score', 0):.3f}")
                print(f"🧱 ESS Volumétrico: {etp.get('ess_volumetrico', 0):.3f}")
                print(f"📊 Coherencia Territorial: {result.get('territorial_coherence_score', 0):.3f}")
                
                # Guardar resultado
                filename = "rapa_nui_scan_results.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Datos completos guardados en: {filename}")
                
                return result
            else:
                print(f"❌ ERROR: El servidor respondió con status {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")
            return None

if __name__ == "__main__":
    asyncio.run(analyze_rapa_nui())
