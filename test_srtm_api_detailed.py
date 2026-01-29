#!/usr/bin/env python3
"""Test SRTM API Detailed - Diagnóstico detallado de llamadas SRTM"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_srtm_detailed():
    """Test detallado de SRTM API."""
    
    print("="*80)
    print("TEST DETALLADO: SRTM API")
    print("="*80)
    print()
    
    # Inicializar SRTM connector directamente
    from backend.credentials_manager import CredentialsManager
    from backend.satellite_connectors.srtm_connector import SRTMConnector
    
    cm = CredentialsManager()
    srtm = SRTMConnector(credentials_manager=cm)
    
    print("✅ SRTM Connector inicializado")
    print(f"   OpenTopography key: {srtm.opentopography_key[:10] if srtm.opentopography_key else 'None'}...")
    print(f"   Earthdata username: {srtm.earthdata_username}")
    print()
    
    # Test con Giza (bbox 0.1° = ~11 km)
    lat_min, lat_max = 29.95, 30.05
    lon_min, lon_max = 31.10, 31.20
    
    print(f"📍 Región: [{lat_min:.2f}, {lat_max:.2f}] x [{lon_min:.2f}, {lon_max:.2f}]")
    print()
    
    # Test OpenTopography
    print("1️⃣ Test OpenTopography...")
    print("-" * 80)
    try:
        result = await srtm._get_srtm_opentopography(
            lat_min, lat_max, lon_min, lon_max, '30m'
        )
        if result:
            print(f"   ✅ SUCCESS: {result.get('value', 'N/A')} {result.get('unit', '')}")
        else:
            print(f"   ❌ FAILED: Returned None")
    except Exception as e:
        print(f"   ❌ EXCEPTION: {e}")
    print()
    
    # Test USGS API
    print("2️⃣ Test USGS API...")
    print("-" * 80)
    try:
        result = await srtm._get_srtm_usgs_api(
            lat_min, lat_max, lon_min, lon_max, '30m'
        )
        if result:
            print(f"   ✅ SUCCESS: {result.get('value', 'N/A')} {result.get('unit', '')}")
        else:
            print(f"   ❌ FAILED: Returned None")
    except Exception as e:
        print(f"   ❌ EXCEPTION: {e}")
    print()


if __name__ == "__main__":
    asyncio.run(test_srtm_detailed())
