#!/usr/bin/env python3
"""Test rapido de Sentinel-2 con stackstac"""

import sys
sys.path.insert(0, 'backend')

from satellite_connectors.planetary_computer import PlanetaryComputerConnector

# Test Sentinel-2
pc = PlanetaryComputerConnector()

print("Testeando Sentinel-2 NDVI...")
print(f"Disponible: {pc.available}")

# Valeriana, México
result = pc.get_multispectral_data(
    lat_min=18.695,
    lat_max=18.745,
    lon_min=-90.775,
    lon_max=-90.725
)

if result:
    print(f"EXITO: NDVI = {result.get('ndvi_mean', 'N/A')}")
    print(f"Fuente: {result.get('source', 'N/A')}")
else:
    print("FALLO: No se obtuvieron datos")
