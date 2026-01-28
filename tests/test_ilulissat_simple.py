#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test():
    from satellite_connectors.icesat2_connector import ICESat2Connector
    icesat2 = ICESat2Connector()
    
    # Ilulissat, Groenlandia
    lat_min, lat_max = 69.2, 69.3
    lon_min, lon_max = -51.1, -51.0
    
    print("Test ICESat-2 en Ilulissat, Groenlandia")
    result = await icesat2.get_elevation_data(lat_min, lat_max, lon_min, lon_max)
    
    if result:
        print(f"[OK] Status: {result.status.value}")
        print(f"     Valor: {result.value} {result.unit}")
        print(f"     Confidence: {result.confidence}")
        print(f"     Puntos validos: {result.quality_flags.get('valid_points')}")
    else:
        print("[FAIL] Sin datos")

asyncio.run(test())
