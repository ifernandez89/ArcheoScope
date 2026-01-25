#!/usr/bin/env python3
"""
TEST BERMUDA DIRECTO SIN IMPORTS
"""

import requests
import time

def test_bermuda_simple():
    """Test simple directo"""
    try:
        test_data = {
            "lat_min": 32.299,
            "lat_max": 32.301,
            "lon_min": -64.784,
            "lon_max": -64.782,
            "region_name": "Bermuda Test"
        }
        
        print("Enviando a Bermudas...")
        start = time.time()
        
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=15
        )
        
        elapsed = time.time() - start
        
        if response.status_code == 200:
            result = response.json()
            arch_results = result.get('archaeological_results', {})
            prob = arch_results.get('archaeological_probability', 0)
            
            print(f"EXITO: {elapsed:.2f}s")
            print(f"Probabilidad: {prob:.2%}")
            
            if elapsed < 5:
                print("BERMUDA OPTIMIZADA!")
                return True
            elif elapsed < 10:
                print("Mejora notable")
                return True
            else:
                print(f"Todavia lento: {elapsed:.2f}s")
                return False
        else:
            print(f"Error: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("TEST BERMUDA FINAL")
    print("="*30)
    
    success = test_bermuda_simple()
    
    if success:
        print("\nSISTEMA OPTIMIZADO!")
    else:
        print("\nRequiere más trabajo")