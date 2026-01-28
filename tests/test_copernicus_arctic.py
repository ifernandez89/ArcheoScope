#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_copernicus():
    print("="*60)
    print("TEST COPERNICUS MARINE EN ÁRTICO")
    print("="*60)
    
    from satellite_connectors.copernicus_marine_connector import CopernicusMarineConnector
    
    copernicus = CopernicusMarineConnector()
    
    # Ártico
    lat_min, lat_max = 75.0, 75.1
    lon_min, lon_max = -150.0, -149.9
    
    print(f"\nLlamando a Copernicus Marine sea ice...")
    result = await copernicus.get_sea_ice_concentration(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max
    )
    
    if result:
        print(f"\n[OK] COPERNICUS FUNCIONA")
        print(f"   Concentración hielo: {result.get('sea_ice_concentration')}")
        print(f"   Confidence: {result.get('confidence')}")
        print(f"   Fuente: {result.get('source')}")
    else:
        print(f"\n[FAIL] COPERNICUS NO DEVOLVIO DATOS")

if __name__ == "__main__":
    asyncio.run(test_copernicus())
