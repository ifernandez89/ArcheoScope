#!/usr/bin/env python3
"""
Debug CORS headers en tiempo real
"""

import asyncio
import aiohttp
import json

async def test_cors_debug():
    print("Debug CORS headers")
    print("=" * 60)
    
    # Headers exactos que envía el navegador
    headers = {
        'Origin': 'http://localhost:8080',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    test_data = {
        "lat_min": 13.4,
        "lat_max": 13.43,
        "lon_min": 103.86,
        "lon_max": 103.88,
        "region_name": "Angkor_Wat_CORS_Debug",
        "resolution_m": 100,
        "layers_to_analyze": ["ndvi_anomaly"]
    }
    
    # Test POST request exactamente como el navegador
    async with aiohttp.ClientSession() as session:
        print("\nEnviando petición POST a /analyze")
        print(f"   Origin: {headers['Origin']}")
        print(f"   Content-Type: {headers['Content-Type']}")
        
        try:
            async with session.post(
                'http://localhost:8002/analyze',
                headers=headers,
                json=test_data,
                timeout=30
            ) as response:
                print(f"\nResponse Status: {response.status}")
                print(f"Response Headers:")
                
                for header, value in response.headers.items():
                    if 'access-control' in header.lower() or 'origin' in header.lower():
                        print(f"   {header}: {value}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"\nResponse OK")
                    print(f"   Analysis ID: {data.get('analysis_id', 'N/A')}")
                    print(f"   Real Validation: {'real_archaeological_validation' in data}")
                    print(f"   Data Transparency: {'data_source_transparency' in data}")
                else:
                    text = await response.text()
                    print(f"\nError Response: {text}")
                    
        except Exception as e:
            print(f"\nException: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_cors_debug())