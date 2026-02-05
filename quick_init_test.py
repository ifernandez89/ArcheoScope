#!/usr/bin/env python3
"""
Test rápido de inicialización - sin análisis completo
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("🚀 Quick Initialization Test")
print("="*80)

# Test 1: Import modules
print("\n1️⃣ Testing imports...")
start = datetime.now()
try:
    from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
    from territorial_inferential_tomography import TerritorialInferentialTomographyEngine
    from territorial_context_profile import AnalysisObjective
    elapsed = (datetime.now() - start).total_seconds()
    print(f"   ✅ Imports OK ({elapsed:.2f}s)")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Initialize integrator
print("\n2️⃣ Initializing RealDataIntegratorV2...")
start = datetime.now()
try:
    integrator = RealDataIntegratorV2()
    elapsed = (datetime.now() - start).total_seconds()
    print(f"   ✅ Integrator initialized ({elapsed:.2f}s)")
    
    # Count connectors
    active = sum(1 for c in integrator.connectors.values() if c is not None)
    total = len(integrator.connectors)
    print(f"   📊 Active connectors: {active}/{total}")
    
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    sys.exit(1)

# Test 3: Initialize engine
print("\n3️⃣ Initializing TIMT Engine...")
start = datetime.now()
try:
    engine = TerritorialInferentialTomographyEngine(integrator)
    elapsed = (datetime.now() - start).total_seconds()
    print(f"   ✅ Engine initialized ({elapsed:.2f}s)")
except Exception as e:
    print(f"   ❌ Engine initialization failed: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("✅ All initialization tests passed!")
print("\n💡 System is ready. Full analysis will be slow due to:")
print("   - Real satellite data downloads (Sentinel-1, Sentinel-2, Landsat)")
print("   - Multiple API calls per zone (15 instruments)")
print("   - Large zones require more processing time")
print("\n📊 Expected times:")
print("   - Small zone (0.01° x 0.01°): 1-3 minutes")
print("   - Medium zone (0.1° x 0.1°): 5-10 minutes")
print("   - Large zone (1° x 2°): 20-40 minutes")
