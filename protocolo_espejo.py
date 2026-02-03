import asyncio
import httpx
import json
from datetime import datetime

URL = "http://localhost:8003/api/scientific/analyze"

# DEFINICIÓN DE EJES EN ESPEJO
MIRROR_AXIS = {
    "ORIGIN": {"name": "Patagonia_Base", "lat": -44.5, "lon": -69.0, "g1_prev": 0.9425},
    "MIRROR": {"name": "Gobi_Mirror", "lat": 44.5, "lon": 111.0}
}

async def scan_mirror():
    print("="*70)
    print("🔮 PROTOCOLO: VALIDACIÓN DE EJES EN ESPEJO (URBANO MONTE)")
    print("="*70)
    print(f"\n📍 Buscando resonancia en el Espejo Norte: {MIRROR_AXIS['MIRROR']['name']}")
    print(f"   Coordenadas: {MIRROR_AXIS['MIRROR']['lat']}, {MIRROR_AXIS['MIRROR']['lon']}")
    
    payload = {
        "lat_min": MIRROR_AXIS['MIRROR']['lat'] - 0.015, 
        "lat_max": MIRROR_AXIS['MIRROR']['lat'] + 0.015,
        "lon_min": MIRROR_AXIS['MIRROR']['lon'] - 0.015, 
        "lon_max": MIRROR_AXIS['MIRROR']['lon'] + 0.015,
        "region_name": "Gobi_Mirror_Resonance",
        "resolution_m": 100.0  # Alta precisión para el eje
    }
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            response = await client.post(URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                metrics = data['official_classification']['metrics_applied']
                g1 = metrics.get('g1_geometry', 0)
                veredicto = data['official_classification']['veredicto']
                
                print(f"\n✅ ESCANEO COMPLETADO")
                print(f"   - G1 Espejo (Gobi): {g1:.4f}")
                print(f"   - Veredicto: {veredicto}")
                
                delta = abs(g1 - MIRROR_AXIS['ORIGIN']['g1_prev'])
                print(f"   - Δ vs Patagonia: {delta:.4f}")
                
                print("\n📊 CONCLUSIÓN ESTRATÉGICA:")
                if g1 > 0.90:
                    print("   🔥 RESONANCIA DETECTADA. La Rejilla de Coherencia es REAL.")
                    print("   - Ambos hemisferios comparten un orden territorial idéntico en el mismo eje.")
                else:
                    print("   ℹ️ DISONANCIA. Patagonia es un evento aislado o el eje de Monte está desviado.")
                    
                # Guardar resultado
                report = {
                    "timestamp": datetime.now().isoformat(),
                    "origin": MIRROR_AXIS['ORIGIN'],
                    "mirror": {
                        "name": MIRROR_AXIS['MIRROR']['name'],
                        "g1": g1,
                        "veredicto": veredicto,
                        "delta": delta
                    }
                }
                with open("MIRROR_AXIS_VALIDATION.json", "w") as f:
                    json.dump(report, f, indent=2)
                    
            else:
                print(f"❌ ERROR API: {response.status_code}")
        except Exception as e:
            print(f"❌ EXCEPCIÓN: {e}")

if __name__ == "__main__":
    asyncio.run(scan_mirror())
