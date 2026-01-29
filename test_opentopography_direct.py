#!/usr/bin/env python3
"""Test OpenTopography API Direct - Test directo sin wrapper"""

import requests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_opentopography_direct():
    """Test directo de OpenTopography API."""
    
    print("="*80)
    print("TEST DIRECTO: OpenTopography API")
    print("="*80)
    print()
    
    # Obtener API key de BD
    from backend.credentials_manager import CredentialsManager
    cm = CredentialsManager()
    api_key = cm.get_credential("opentopography", "api_key")
    
    if not api_key:
        print("❌ No API key found in BD")
        return False
    
    print(f"✅ API Key: {api_key[:10]}...{api_key[-5:]}")
    print()
    
    # Coordenadas de Giza (bbox 0.1° = ~11 km)
    lat_min, lat_max = 29.95, 30.05
    lon_min, lon_max = 31.10, 31.20
    
    print(f"📍 Región: [{lat_min:.2f}, {lat_max:.2f}] x [{lon_min:.2f}, {lon_max:.2f}]")
    print()
    
    # Construir URL y parámetros
    url = "https://cloud.sdsc.edu/v1/raster/globaldem"
    params = {
        'demtype': 'SRTMGL1',
        'south': lat_min,
        'north': lat_max,
        'west': lon_min,
        'east': lon_max,
        'outputFormat': 'GTiff',
        'API_Key': api_key
    }
    
    print("🔄 Llamando OpenTopography API...")
    print(f"   URL: {url}")
    print(f"   Params: {params}")
    print()
    
    try:
        response = requests.get(url, params=params, timeout=60)
        
        print(f"📡 Response:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"   Content-Length: {len(response.content)} bytes")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS: API returned data")
            print(f"   Content preview: {response.content[:100]}")
            return True
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response text: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_opentopography_direct()
    sys.exit(0 if success else 1)
