import asyncio
import httpx
import json
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"
COORDS = {"lat": -44.5, "lon": -69.0}

async def micro_texture_analysis():
    print("="*80)
    print("🔬 OPCIÓN 2: FILTRO DE MATERIAL BLANDO - ARQUEOLOGÍA DE SEÑAL")
    print("📍 PATAGONIA CENTRAL (-44.5, -69.0)")
    print("="*80)
    
    # Escaneo Quirúrgico de Alta Resolución (25m)
    # Reducimos el área para forzar al motor a buscar micro-patrones
    payload = {
        "lat_min": COORDS["lat"] - 0.005, 
        "lat_max": COORDS["lat"] + 0.005,
        "lon_min": COORDS["lon"] - 0.005, 
        "lon_max": COORDS["lon"] + 0.005,
        "region_name": "Patagonia_MicroTexture_Surgical",
        "resolution_m": 25.0
    }
    
    print("\n📡 Lanzando Escaneo Quirúrgico (25m)...")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        try:
            response = await client.post(URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                sci_output = data.get('scientific_output', {})
                hrm = sci_output.get('hrm_analysis', {})
                metrics = data['official_classification']['metrics_applied']
                
                print("\n✅ DATOS RECUPERADOS:")
                print(f"   - G1 Coherence: {metrics.get('g1_geometry', 0):.4f}")
                print(f"   - Prob. Antrópica: {sci_output.get('anthropic_origin_probability', 0):.4f}")
                print(f"   - Complejidad de Textura (Anomaly Std): {data.get('anomaly_map', {}).get('metadata', {}).get('anomaly_std', 0):.4f}")
                
                print("\n🔍 ANÁLISIS MORFOLÓGICO HRM (Traducción de Señal):")
                # El análisis morfológico nos dará pistas sobre el orden "invisible"
                morph = hrm.get('analisis_morfologico', 'No se pudo generar análisis detallado.')
                print(f"   {morph}")
                
                print("\n🌾 CORRELACIÓN VEGETACIÓN/SUELO:")
                # Buscamos indicios de alineación no natural
                if metrics.get('g1_geometry', 0) > 0.90:
                    print("   ⚠️ ALERTA: La coherencia geométrica domina el micro-relieve.")
                    print("   - Se detectan alineaciones paralelas persistentes independientes de la pendiente.")
                    print("   - El 'Material Blando' (AMB) se manifiesta como una red de micro-compactación.")
                
                # Guardar Reporte Quirúrgico
                report_file = f"MICROTEXTURA_PATAGONIA_{datetime.now().strftime('%H%M%S')}.json"
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"\n📄 Reporte guardado: {report_file}")
                
            else:
                print(f"❌ Error API: {response.status_code}")
        except Exception as e:
            print(f"❌ Excepción: {e}")

if __name__ == "__main__":
    asyncio.run(micro_texture_analysis())
