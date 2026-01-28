#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_icesat2():
    print("="*60)
    print("TEST ICESAT-2 EN ANTÁRTIDA")
    print("="*60)
    
    from satellite_connectors.icesat2_connector import ICESat2Connector
    
    icesat2 = ICESat2Connector()
    
    # Groenlandia (donde SÍ hay cobertura ICESat-2)
    lat_min, lat_max = 72.0, 72.1
    lon_min, lon_max = -38.0, -37.9
    
    print(f"\nLlamando a ICESat-2 en Groenlandia...")
    result = await icesat2.get_elevation_data(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max
    )
    
    if result:
        print(f"\n[OK] ICESAT-2 FUNCIONA")
        print(f"   Status: {result.status.value}")
        print(f"   Valor: {result.value} {result.unit}")
        print(f"   Confidence: {result.confidence}")
        print(f"   Fuente: {result.source}")
    else:
        print(f"\n[FAIL] ICESAT-2 NO DEVOLVIO DATOS")

if __name__ == "__main__":
    asyncio.run(test_icesat2())
