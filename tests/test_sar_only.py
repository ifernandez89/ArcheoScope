#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_sar():
    print("="*60)
    print("TEST SENTINEL-1 SAR")
    print("="*60)
    
    from satellite_connectors.planetary_computer import PlanetaryComputerConnector
    
    pc = PlanetaryComputerConnector()
    
    # Giza
    lat_min, lat_max = 29.97, 29.98
    lon_min, lon_max = 31.13, 31.14
    
    print(f"\nLlamando a get_sar_data...")
    result = await pc.get_sar_data(
        lat_min=lat_min,
        lat_max=lat_max,
        lon_min=lon_min,
        lon_max=lon_max
    )
    
    if result:
        print(f"\n[OK] SAR FUNCIONA")
        print(f"   VV mean: {result.indices.get('vv_mean')}")
        print(f"   Confidence: {result.confidence}")
    else:
        print(f"\n[FAIL] SAR FALLA - revisar logs arriba")

if __name__ == "__main__":
    asyncio.run(test_sar())
