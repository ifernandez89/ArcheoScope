#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_modis():
    print("="*60)
    print("TEST MODIS LST")
    print("="*60)
    
    from satellite_connectors.real_data_integrator import RealDataIntegrator
    integrator = RealDataIntegrator()
    
    # Giza
    lat_min, lat_max = 29.97, 29.98
    lon_min, lon_max = 31.13, 31.14
    
    result = await integrator.get_instrument_measurement(
        instrument_name="modis_lst",
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max
    )
    
    if result:
        print(f"\n[OK] MODIS FUNCIONA")
        print(f"   Inercia termica: {result.get('value')}")
        print(f"   Status: {result.get('status')}")
    else:
        print(f"\n[FAIL] MODIS FALLA")

if __name__ == "__main__":
    asyncio.run(test_modis())
