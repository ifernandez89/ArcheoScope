#!/usr/bin/env python3
"""
Test the analyze function directly
"""

import sys
import asyncio
sys.path.insert(0, 'backend')

from api.main import analyze_archaeological_region, RegionRequest

async def test():
    print("Testing analyze_archaeological_region function directly...")
    
    request = RegionRequest(
        lat_min=41.85,
        lat_max=41.86,
        lon_min=12.51,
        lon_max=12.52,
        region_name="Test Region"
    )
    
    try:
        result = await analyze_archaeological_region(request)
        print("✅ Function executed successfully!")
        print(f"Result type: {type(result)}")
        if isinstance(result, dict):
            print(f"Result keys: {list(result.keys())[:10]}")
        return result
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test())
    if result:
        print("\n✅ Test passed!")
    else:
        print("\n❌ Test failed!")
