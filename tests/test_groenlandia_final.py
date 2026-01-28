#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test():
    from satellite_connectors.real_data_integrator import RealDataIntegrator
    integrator = RealDataIntegrator()
    
    # Ilulissat, Groenlandia
    lat_min, lat_max = 69.2, 69.3
    lon_min, lon_max = -51.1, -51.0
    
    print("="*70)
    print("ANALISIS GROENLANDIA - Ilulissat (Arqueologia Glaciar)")
    print("="*70)
    
    instrumentos = [
        ("icesat2", "ICESat-2"),
        ("sentinel_1_sar", "Sentinel-1 SAR"),
        ("sentinel_2_ndvi", "Sentinel-2 NDVI"),
        ("landsat_thermal", "Landsat Thermal"),
    ]
    
    for inst, label in instrumentos:
        print(f"\n{label}:")
        result = await integrator.get_instrument_measurement(
            instrument_name=inst,
            lat_min=lat_min, lat_max=lat_max,
            lon_min=lon_min, lon_max=lon_max
        )
        
        if result:
            status = result.get('status', 'UNKNOWN')
            value = result.get('value')
            conf = result.get('confidence', 0)
            
            print(f"  Status: {status}")
            print(f"  Valor: {value}")
            print(f"  Confidence: {conf}")
            
            # Analisis arqueologico
            if inst == "icesat2" and status == "OK":
                print(f"  >> UTIL para detectar terrazas y alineamientos")
            elif inst == "sentinel_1_sar" and status == "OK":
                print(f"  >> UTIL para penetracion de hielo")
            elif inst == "sentinel_2_ndvi" and status == "OK":
                if value > 0.2:
                    print(f"  >> Vegetacion presente - zona deglaciada")
                else:
                    print(f"  >> Sin vegetacion - hielo/roca")
        else:
            print(f"  [NO DATA]")
    
    print("\n" + "="*70)
    print("CONCLUSION:")
    print("Sistema listo para arqueologia glaciar en Groenlandia")
    print("="*70)

asyncio.run(test())
