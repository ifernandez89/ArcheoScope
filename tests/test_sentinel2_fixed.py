#!/usr/bin/env python3
"""Test Sentinel-2 sin stackstac"""

import sys
import asyncio
sys.path.insert(0, 'backend')

from satellite_connectors.planetary_computer import PlanetaryComputerConnector

async def test():
    pc = PlanetaryComputerConnector()
    
    print(f"Planetary Computer disponible: {pc.available}")
    
    # Valeriana, Mexico
    result = await pc.get_multispectral_data(
        lat_min=18.695,
        lat_max=18.745,
        lon_min=-90.775,
        lon_max=-90.725
    )
    
    if result:
        print(f"EXITO!")
        print(f"  NDVI: {result.get('ndvi_mean', 'N/A')}")
        print(f"  Fuente: {result.get('source', 'N/A')}")
        print(f"  Fecha: {result.get('acquisition_date', 'N/A')}")
    else:
        print("FALLO: No se obtuvieron datos")

if __name__ == "__main__":
    asyncio.run(test())
