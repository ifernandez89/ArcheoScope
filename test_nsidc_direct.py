#!/usr/bin/env python3
"""
Test directo de NSIDC para diagnosticar el problema
"""

import asyncio
import sys
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from satellite_connectors.nsidc_connector import NSIDCConnector

async def test_nsidc():
    print("="*80)
    print("TEST DIRECTO NSIDC")
    print("="*80)
    
    connector = NSIDCConnector()
    
    print(f"\nConnector creado: {connector}")
    print(f"Available: {connector.available}")
    print(f"Username: {connector.username[:5] if connector.username else 'None'}***")
    
    print("\nLlamando a get_sea_ice_concentration...")
    
    result = await connector.get_sea_ice_concentration(
        lat_min=-75.7497,
        lat_max=-75.6497,
        lon_min=-111.4030,
        lon_max=-111.3030
    )
    
    print(f"\nResultado: {result}")
    
    if result:
        print(f"  Value: {result.get('value')}")
        print(f"  Source: {result.get('source')}")
        print(f"  Confidence: {result.get('confidence')}")
    else:
        print("  ❌ None devuelto")
    
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_nsidc())
