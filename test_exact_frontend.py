#!/usr/bin/env python3
"""
Test exacto del frontend para debug
"""

import requests
import json

def test_exact_frontend_data():
    print("Test exacto de datos frontend")
    print("=" * 50)
    
    # Datos EXACTAMENTE como los envía el frontend
    regionData = {
        "lat_min": 13.4,
        "lat_max": 13.43,
        "lon_min": 103.86,
        "lon_max": 103.88,
        "resolution_m": 100,
        "region_name": "Región Arqueológica Investigada",
        "include_explainability": False,
        "include_validation_metrics": False,
        "layers_to_analyze": [
            "ndvi_vegetation", "thermal_lst", "sar_backscatter", 
            "surface_roughness", "soil_salinity", "seismic_resonance",
            "elevation_dem", "sar_l_band", "icesat2_profiles",
            "vegetation_height", "soil_moisture",
            "lidar_fullwave", "dem_multiscale", "spectral_roughness",
            "pseudo_lidar_ai", "multitemporal_topo"
        ],
        "active_rules": ["all"]
    }
    
    print("Enviando datos:")
    print(f"  lat_min: {regionData['lat_min']}")
    print(f"  lat_max: {regionData['lat_max']}")
    print(f"  lon_min: {regionData['lon_min']}") 
    print(f"  lon_max: {regionData['lon_max']}")
    print(f"  resolution_m: {regionData['resolution_m']}")
    print(f"  region_name: {regionData['region_name']}")
    
    try:
        headers = {
            'Origin': 'http://localhost:8080',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(
            'http://localhost:8002/analyze',
            headers=headers,
            json=regionData,
            timeout=30
        )
        
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS: Análisis completado")
            print(f"Analysis ID: {data.get('analysis_id')}")
        else:
            print(f"ERROR: {response.status_code}")
            try:
                error = response.json()
                print(f"Error details: {json.dumps(error, indent=2)}")
            except:
                print(f"Response text: {response.text}")
                
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_exact_frontend_data()