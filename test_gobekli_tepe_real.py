import asyncio
import httpx
import json
import os
import sys

async def test_gobekli_tepe():
    # Coordenadas y configuración solicitadas por el usuario
    # Lat: 37.2231° N, Lon: 38.9226° E
    # ΔLat: ±0.0035, ΔLon: ±0.0035
    
    lat = 37.2231
    lon = 38.9226
    delta = 0.0035
    
    payload = {
        "lat_min": lat - delta,
        "lat_max": lat + delta,
        "lon_min": lon - delta,
        "lon_max": lon + delta,
        "region_name": "Göbekli Tepe - Subsurface Scan"
    }
    
    url = "http://localhost:8003/api/scientific/analyze"
    
    print(f"\n🚀 Iniciando barrido SUBSURFACE en Göbekli Tepe...")
    print(f"📍 Centro: {lat}, {lon}")
    print(f"📐 Área: ~0.25 km²")
    print(f"🛠️ Configuración: Depth 0.5 - 8.0m | Mode: Subsurface / Anthropogenic")
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            print("\n⏳ Ejecutando pipeline científico (esto puede tardar unos minutos)...")
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
                print("=" * 60)
                
                # Extraer datos clave del resultado
                analysis_id = result.get('analysis_id')
                coherence = result.get('territorial_coherence_score', 0)
                rigor = result.get('scientific_rigor_score', 0)
                
                arch_results = result.get('archaeological_results', {})
                prob = arch_results.get('anthropic_probability', 0)
                score = arch_results.get('anomaly_score', 0)
                action = arch_results.get('recommended_action', 'N/A')
                
                etp = result.get('etp_summary', {})
                ess_vol = etp.get('ess_volumetrico', 0)
                ess_temp = etp.get('ess_temporal', 0)
                
                print(f"🆔 Analysis ID: {analysis_id}")
                print(f"📊 Coherencia Territorial: {coherence:.3f}")
                print(f"🧪 Rigor Científico: {rigor:.3f}")
                print("-" * 30)
                print(f"🎯 PROBABILIDAD ANTROPOGÉNICA: {prob * 100:.1f}%")
                print(f"🔍 ANOMALY SCORE (ESS): {score:.3f}")
                print(f"🧱 ESS VOLUMÉTRICO (Subsurface): {ess_vol:.3f}")
                print(f"⏳ PERSISTENCIA TEMPORAL: {ess_temp:.3f}")
                print(f"📢 ACCIÓN RECOMENDADA: {action}")
                print("=" * 60)
                
                # Guardar resultado en un JSON para referencia
                filename = "gobekli_tepe_real_scan.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Datos completos guardados en: {filename}")
                
                return result
            else:
                print(f"\n❌ ERROR: El servidor respondió con status {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"\n❌ ERROR de conexión: {e}")
            print("Asegúrate de que el backend esté corriendo (python run_archeoscope.py)")
            return None

if __name__ == "__main__":
    asyncio.run(test_gobekli_tepe())
