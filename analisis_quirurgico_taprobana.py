import asyncio
import httpx
import json
import math
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

# TAPROBANA EAST POINT (Surgical Analysis)
# Original node: 7.0, 81.0
# East offset (1.5km): lon + 0.0136
TAPROBANA_EAST = {"lat": 7.0, "lon": 81.0136}

async def surgical_taprobana_scan():
    print("="*80)
    print("🔬 ANÁLISIS QUIRÚRGICO: EL ANCLA DE TAPROBANA (EAST NODE)")
    print(f"📍 Coordenadas: {TAPROBANA_EAST['lat']}, {TAPROBANA_EAST['lon']}")
    print("="*80)
    
    # Escaneo Quirúrgico de 30m
    payload = {
        "lat_min": TAPROBANA_EAST["lat"] - 0.005, 
        "lat_max": TAPROBANA_EAST["lat"] + 0.005,
        "lon_min": TAPROBANA_EAST["lon"] - 0.005, 
        "lon_max": TAPROBANA_EAST["lon"] + 0.005,
        "region_name": "Taprobana_East_Surgical",
        "resolution_m": 30.0
    }
    
    print("\n📡 Iniciando escaneo de alta resolución (30m)...")
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        try:
            response = await client.post(URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                sci_output = data.get('scientific_output', {})
                hrm = sci_output.get('hrm_analysis', {})
                metrics = data['official_classification']['metrics_applied']
                g1 = metrics.get('g1_geometry', 0)
                
                print(f"\n✅ ANÁLISIS COMPLETADO - G1: {g1:.4f}")
                
                # Clasificación en la escala ECC
                if g1 > 0.93: ecc = "ECC-3 (HTAG-CTA)"
                elif g1 > 0.90: ecc = "ECC-2 (HTAG-NODAL)"
                else: ecc = "ECC-1 (INTERFAZ)"
                
                print(f"   - Clasificación ECC: {ecc}")
                print(f"   - Prob. Antrópica: {sci_output.get('anthropic_origin_probability', 0):.4f}")
                
                print("\n🔍 DETALLES DEL HRM (Anomalías Submarinas):")
                morph = hrm.get('analisis_morfologico', 'Analizando micro-textura...')
                print(f"   {morph}")
                
                # Guardar Reporte Específico
                report_file = f"SURGICAL_TAPROBANA_REPORT_{datetime.now().strftime('%H%M%S')}.json"
                with open(report_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"\n📄 Reporte guardado: {report_file}")
                
            else:
                print(f"❌ Error API: {response.status_code}")
        except Exception as e:
            print(f"❌ Excepción: {e}")

if __name__ == "__main__":
    asyncio.run(surgical_taprobana_scan())
