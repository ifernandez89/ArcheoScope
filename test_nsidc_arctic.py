#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_nsidc():
    print("="*60)
    print("TEST NSIDC EN ÁRTICO")
    print("="*60)
    
    from satellite_connectors.nsidc_connector import NSIDCConnector
    
    nsidc = NSIDCConnector()
    
    # Ártico (donde SÍ hay hielo marino)
    lat_min, lat_max = 75.0, 75.1
    lon_min, lon_max = -150.0, -149.9
    
    print(f"\nLlamando a NSIDC sea ice en Ártico...")
    result = await nsidc.get_sea_ice_concentration(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max
    )
    
    if result:
        print(f"\n[OK] NSIDC FUNCIONA")
        print(f"   Status: {result.status.value}")
        print(f"   Valor: {result.value} {result.unit}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Fuente: {result.source}")
        if result.processing_notes:
            print(f"   Notas: {result.processing_notes}")
    else:
        print(f"\n[FAIL] NSIDC NO DEVOLVIO DATOS")

if __name__ == "__main__":
    asyncio.run(test_nsidc())
