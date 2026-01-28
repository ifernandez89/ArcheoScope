#!/usr/bin/env python3
"""Test de instrumentos que SI funcionan"""

import sys
import asyncio
sys.path.insert(0, 'backend')

from satellite_connectors.real_data_integrator import RealDataIntegrator

async def test():
    integrator = RealDataIntegrator()
    
    print("="*80)
    print("TEST DE INSTRUMENTOS QUE FUNCIONAN")
    print("="*80)
    
    # Valeriana, Mexico (selva)
    bbox = {
        'lat_min': 18.695,
        'lat_max': 18.745,
        'lon_min': -90.775,
        'lon_max': -90.725
    }
    
    # Test NSIDC
    print("\n1. NSIDC Sea Ice:")
    result = await integrator.get_instrument_measurement(
        'nsidc_sea_ice',
        **bbox
    )
    if result:
        print(f"   Valor: {result['value']}")
        print(f"   Fuente: {result['source']}")
        print(f"   Modo: {result.get('data_mode', 'N/A')}")
    else:
        print("   FALLO")
    
    # Test ICESat-2
    print("\n2. ICESat-2:")
    result = await integrator.get_instrument_measurement(
        'icesat2',
        **bbox
    )
    if result:
        print(f"   Valor: {result['value']}")
        print(f"   Fuente: {result['source']}")
    else:
        print("   FALLO")
    
    # Test Landsat Thermal
    print("\n3. Landsat Thermal:")
    result = await integrator.get_instrument_measurement(
        'landsat_thermal',
        **bbox
    )
    if result:
        print(f"   Valor: {result['value']}")
        print(f"   Fuente: {result['source']}")
    else:
        print("   FALLO")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    asyncio.run(test())
