#!/usr/bin/env python3
"""
Test simple para debug del error 'summary'
"""

import requests
import json

def test_simple():
    """Test simple para identificar el error."""
    
    print("🔍 DEBUG: Probando análisis mínimo...")
    
    # Análisis mínimo
    analysis_request = {
        "lat_min": -16.55,
        "lat_max": -16.54,
        "lon_min": -68.67,
        "lon_max": -68.66,
        "resolution_m": 2000,  # Muy baja resolución
        "region_name": "Debug Test",
        "layers_to_analyze": ["ndvi_vegetation"],  # Solo 1 capa
        "active_rules": ["vegetation_topography_decoupling"],  # Solo 1 regla
        "include_explainability": False,
        "include_validation_metrics": False
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze", 
            json=analysis_request,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Análisis exitoso")
            
            # Verificar componentes
            components = list(result.keys())
            print(f"Componentes: {components}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_simple()
    print(f"Resultado: {'✅ OK' if success else '❌ ERROR'}")