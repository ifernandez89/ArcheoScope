#!/usr/bin/env python3
"""
Test del nuevo sistema de diagnóstico científico de datos
"""

import requests
import json

def test_diagnostic_system():
    print("🔬 TESTING ARCHEOSCOPE DIAGNOSTIC SYSTEM")
    print("=" * 60)
    
    # Test con resolución baja (debería activar diagnóstico crítico)
    test_data_low_res = {
        "lat_min": 41.85,
        "lat_max": 41.86,
        "lon_min": 12.50,
        "lon_max": 12.51,
        "resolution_m": 500,  # Resolución baja - debería activar diagnóstico
        "region_name": "Test Low Resolution",
        "include_explainability": True,
        "include_validation_metrics": True,
        "layers_to_analyze": ["ndvi_vegetation", "thermal_lst"],
        "active_rules": ["all"]
    }
    
    print("\n1. Testing with LOW RESOLUTION (500m) - Should trigger critical diagnostic...")
    try:
        response = requests.post('http://localhost:8004/analyze', 
                               json=test_data_low_res, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis completed successfully")
            
            # Verificar campos clave para el diagnóstico
            region_info = data.get('region_info', {})
            print(f"   - Resolution: {region_info.get('resolution_m', 'unknown')}m")
            print(f"   - Area: {region_info.get('area_km2', 'unknown')} km²")
            
            # Verificar datos temporales
            temporal_data = data.get('temporal_analysis', {})
            print(f"   - Temporal windows: {temporal_data.get('available_windows', 0)}")
            
            # Verificar contexto geológico
            geological = data.get('geological_context', {})
            print(f"   - Geological context: {'✅' if geological.get('available') else '❌'}")
            
            # Verificar huella humana moderna
            modern_footprint = data.get('modern_human_footprint', {})
            print(f"   - Modern footprint: {'✅' if modern_footprint.get('comprehensive') else '❌'}")
            
            print("   - This should trigger CRITICAL diagnostic in frontend")
            
        else:
            print(f"❌ Analysis failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    # Test con resolución alta (debería ser mejor)
    test_data_high_res = {
        "lat_min": 41.85,
        "lat_max": 41.86,
        "lon_min": 12.50,
        "lon_max": 12.51,
        "resolution_m": 10,  # Resolución alta - debería ser mejor
        "region_name": "Test High Resolution",
        "include_explainability": True,
        "include_validation_metrics": True,
        "layers_to_analyze": ["ndvi_vegetation", "thermal_lst", "sar_backscatter"],
        "active_rules": ["all"]
    }
    
    print("\n2. Testing with HIGH RESOLUTION (10m) - Should be better...")
    try:
        response = requests.post('http://localhost:8004/analyze', 
                               json=test_data_high_res, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis completed successfully")
            
            region_info = data.get('region_info', {})
            print(f"   - Resolution: {region_info.get('resolution_m', 'unknown')}m")
            print("   - This should trigger BETTER diagnostic in frontend")
            
        else:
            print(f"❌ Analysis failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 FRONTEND TESTING:")
    print("   1. Open: http://localhost:8080")
    print("   2. Search coordinates: 41.85, 12.50")
    print("   3. Set resolution to 500m and click INVESTIGAR")
    print("   4. Check 'Diagnóstico Científico de Datos' section")
    print("   5. Should see: 🔴 DATOS INSUFICIENTES PARA INTERPRETACIÓN")
    print("   6. Change resolution to 10m and test again")
    print("   7. Should see improved diagnostic")
    print("\n🧠 The system should say: 'necesito ver mejor para hablar'")

if __name__ == "__main__":
    test_diagnostic_system()