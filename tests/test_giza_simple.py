#!/usr/bin/env python3
"""
Simple test for Giza without Unicode
"""

import sys
sys.path.append('backend')

from api.main import system_components, initialize_system
from pydantic import BaseModel

# Initialize system
print("Initializing system...")
initialize_system()

# Create request
class RegionRequest(BaseModel):
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    region_name: str
    resolution_m: int = 1000
    layers_to_analyze: list = ["ndvi", "thermal", "sar"]
    active_rules: list = ["vegetation_decoupling", "thermal_residuals"]
    include_explainability: bool = False
    include_validation_metrics: bool = False

request = RegionRequest(
    lat_min=29.965,
    lat_max=29.985,
    lon_min=31.128,
    lon_max=31.148,
    region_name="Giza Pyramids"
)

print(f"\nTesting with Giza coordinates: {request.lat_min}, {request.lon_min}")

# Test environment classifier
env_classifier = system_components.get('environment_classifier')
if env_classifier:
    center_lat = (request.lat_min + request.lat_max) / 2
    center_lon = (request.lon_min + request.lon_max) / 2
    
    env_context = env_classifier.classify(center_lat, center_lon)
    print(f"\nEnvironment detected: {env_context.environment_type.value}")
    print(f"Confidence: {env_context.confidence}")
    print(f"Primary sensors: {env_context.primary_sensors}")
    
    # Check if it's ice or water
    from environment_classifier import EnvironmentType
    
    is_ice = env_context.environment_type in [
        EnvironmentType.POLAR_ICE,
        EnvironmentType.GLACIER,
        EnvironmentType.PERMAFROST
    ]
    
    is_water = env_context.environment_type in [
        EnvironmentType.DEEP_OCEAN,
        EnvironmentType.SHALLOW_SEA,
        EnvironmentType.COASTAL,
        EnvironmentType.LAKE,
        EnvironmentType.RIVER
    ]
    
    print(f"\nIs ice environment: {is_ice}")
    print(f"Is water environment: {is_water}")
    print(f"Should use terrestrial analysis: {not is_ice and not is_water}")
    
    if not is_ice and not is_water:
        print("\nWill proceed with terrestrial analysis")
        print("This is where the error might occur...")
        
        # Try to import the functions that will be called
        try:
            from api.main import create_archaeological_region_data
            print("\ncreate_archaeological_region_data imported successfully")
            
            # Try to call it
            print("\nCalling create_archaeological_region_data...")
            datasets = create_archaeological_region_data(request)
            print(f"Datasets created: {type(datasets)}")
            if isinstance(datasets, dict):
                print(f"Keys: {list(datasets.keys())}")
                for key, value in datasets.items():
                    if value is None:
                        print(f"  WARNING: {key} is None!")
                    else:
                        print(f"  {key}: {type(value)}")
            
        except Exception as e:
            print(f"\nERROR in create_archaeological_region_data: {e}")
            import traceback
            traceback.print_exc()
else:
    print("Environment classifier not available")
