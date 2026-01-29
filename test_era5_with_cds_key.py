#!/usr/bin/env python3
"""Test ERA5 con CDS API Key"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_era5():
    print("="*80)
    print("🌍 TEST ERA5 CON CDS API KEY")
    print("="*80)
    print()
    
    from backend.satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
    
    integrator = RealDataIntegratorV2()
    
    # Giza
    lat_min, lat_max = 29.95, 30.05
    lon_min, lon_max = 31.10, 31.20
    
    print("📍 Test: Giza, Egipto")
    print()
    
    result = await integrator.get_instrument_measurement_robust(
        'era5_climate', lat_min, lat_max, lon_min, lon_max
    )
    
    print()
    print(f"Status: {result.status}")
    print(f"Value: {result.value}")
    print(f"Reason: {result.reason}")
    
    if result.status.name == 'SUCCESS':
        print()
        print("✅ ERA5 FUNCIONA CON CDS KEY!")
        return True
    else:
        print()
        print("❌ ERA5 sigue fallando")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_era5())
    sys.exit(0 if success else 1)
