#!/usr/bin/env python3
"""
Debug script para identificar cuellos de botella en mission_real_data_scan.py
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("debug_mission")

async def test_single_small_zone():
    """Test con una zona muy pequeña para identificar el problema"""
    
    print("\n" + "="*80)
    print("🔍 DEBUG: Testing single small zone")
    print("="*80)
    
    try:
        from territorial_inferential_tomography import TerritorialInferentialTomographyEngine
        from territorial_context_profile import AnalysisObjective
        from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        
        print("✅ Imports successful")
        
        # Zona MUY pequeña para test rápido
        test_zone = {
            "name": "Bermuda Micro Test",
            "lat_min": 26.570,
            "lat_max": 26.575,  # Solo 0.005 grados (~500m)
            "lon_min": -78.830,
            "lon_max": -78.825,
            "resolution_m": 100.0  # Resolución más baja para test
        }
        
        print(f"\n📍 Test Zone: {test_zone['name']}")
        print(f"   Size: {test_zone['lat_max'] - test_zone['lat_min']:.4f}° x {test_zone['lon_max'] - test_zone['lon_min']:.4f}°")
        print(f"   Resolution: {test_zone['resolution_m']}m")
        
        # Initialize components
        print("\n⏳ Initializing RealDataIntegratorV2...")
        start = datetime.now()
        integrator = RealDataIntegratorV2()
        elapsed = (datetime.now() - start).total_seconds()
        print(f"✅ Integrator initialized in {elapsed:.2f}s")
        
        print("\n⏳ Initializing TIMT Engine...")
        start = datetime.now()
        engine = TerritorialInferentialTomographyEngine(integrator)
        elapsed = (datetime.now() - start).total_seconds()
        print(f"✅ Engine initialized in {elapsed:.2f}s")
        
        # Run analysis with timeout
        print("\n⏳ Starting analysis with 120s timeout...")
        start = datetime.now()
        
        try:
            result = await asyncio.wait_for(
                engine.analyze_territory(
                    lat_min=test_zone['lat_min'],
                    lat_max=test_zone['lat_max'],
                    lon_min=test_zone['lon_min'],
                    lon_max=test_zone['lon_max'],
                    analysis_objective=AnalysisObjective.VALIDATION,
                    resolution_m=test_zone['resolution_m']
                ),
                timeout=120.0
            )
            
            elapsed = (datetime.now() - start).total_seconds()
            print(f"\n✅ Analysis completed in {elapsed:.2f}s")
            print(f"   Territorial Coherence: {result.territorial_coherence_score:.3f}")
            print(f"   Scientific Rigor: {result.scientific_rigor_score:.3f}")
            
            return True
            
        except asyncio.TimeoutError:
            elapsed = (datetime.now() - start).total_seconds()
            print(f"\n⏱️ TIMEOUT after {elapsed:.2f}s")
            print("   ❌ Even small zone is timing out - likely data fetching issue")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.error("Test failed", exc_info=True)
        return False

async def test_integrator_only():
    """Test solo el integrador de datos"""
    
    print("\n" + "="*80)
    print("🔍 DEBUG: Testing RealDataIntegratorV2 initialization")
    print("="*80)
    
    try:
        from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        
        print("\n⏳ Initializing integrator...")
        start = datetime.now()
        
        integrator = RealDataIntegratorV2()
        
        elapsed = (datetime.now() - start).total_seconds()
        print(f"✅ Integrator initialized in {elapsed:.2f}s")
        
        # Check connectors
        print("\n📊 Connector Status:")
        for name, connector in integrator.connectors.items():
            status = "✅ OK" if connector is not None else "❌ FAILED"
            print(f"   {name}: {status}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.error("Integrator test failed", exc_info=True)
        return False

async def main():
    print("🚀 ArcheoScope Mission Scan Debugger")
    print("   Purpose: Identify performance bottlenecks\n")
    
    # Test 1: Integrator initialization
    print("\n" + "="*80)
    print("TEST 1: Integrator Initialization")
    print("="*80)
    success1 = await test_integrator_only()
    
    if not success1:
        print("\n❌ Integrator initialization failed - fix this first!")
        return
    
    # Test 2: Small zone analysis
    print("\n" + "="*80)
    print("TEST 2: Small Zone Analysis")
    print("="*80)
    success2 = await test_single_small_zone()
    
    if not success2:
        print("\n❌ Small zone analysis failed or timed out")
        print("\n🔍 Possible issues:")
        print("   1. Data fetching is too slow (API timeouts)")
        print("   2. Missing credentials for satellite APIs")
        print("   3. Network connectivity issues")
        print("   4. Processing bottleneck in TIMT engine")
        print("\n💡 Recommendations:")
        print("   - Check internet connection")
        print("   - Verify API credentials in database")
        print("   - Check logs for specific API errors")
        print("   - Consider reducing resolution or zone size")
    else:
        print("\n✅ All tests passed!")
        print("   The system is working, but large zones may still be slow.")
        print("   Consider:")
        print("   - Using smaller zones")
        print("   - Increasing timeout values")
        print("   - Running zones sequentially with breaks")

if __name__ == "__main__":
    asyncio.run(main())
