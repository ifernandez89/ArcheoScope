#!/usr/bin/env python3
"""
Debug version of the backend to identify the 'summary' error
"""

import sys
from pathlib import Path
import traceback

# Add backend to path
sys.path.append(str(Path(__file__).parent / "archeoscope" / "backend"))

try:
    from archeoscope.backend.api.main import app
    print("✅ Backend imported successfully")
    
    # Try to run a simple analysis
    from archeoscope.backend.api.main import analyze_archaeological_region
    from archeoscope.backend.api.main import RegionRequest
    
    # Create a simple request
    request = RegionRequest(
        lat_min=-16.55,
        lat_max=-16.54,
        lon_min=-68.67,
        lon_max=-68.66,
        resolution_m=2000,
        region_name="Debug Test",
        layers_to_analyze=["ndvi_vegetation"],
        active_rules=["vegetation_topography_decoupling"],
        include_explainability=False,
        include_validation_metrics=False
    )
    
    print("🔍 Testing analysis function directly...")
    
    try:
        result = analyze_archaeological_region(request)
        print("✅ Analysis completed successfully")
        print(f"Result keys: {list(result.keys()) if hasattr(result, 'keys') else 'Not a dict'}")
    except Exception as e:
        print(f"❌ Error in analysis: {e}")
        print("Full traceback:")
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ Error importing backend: {e}")
    traceback.print_exc()