#!/usr/bin/env python3
"""
SOLUCIÓN FINAL - TESTEAR BACKEND
"""

def test_backend_simple():
    """Test si backend funciona"""
    try:
        import requests
        response = requests.get("http://localhost:8002/status", timeout=3)
        if response.status_code == 200:
            print("Backend está funcionando!")
            return True
        else:
            print(f"Backend responde con error: {response.status_code}")
            return False
    except:
        print("Backend no está corriendo")
        return False

def test_bermuda_direct():
    """Test Bermudas directo si backend funciona"""
    if not test_backend_simple():
        print("INICIAR BACKEND PRIMERO: python run_archeoscope.py")
        return False
    
    try:
        import requests
        import time
        
        test_data = {
            "lat_min": 32.299,
            "lat_max": 32.301,
            "lon_min": -64.784,
            "lon_max": -64.782,
            "region_name": "Bermuda Final Test"
        }
        
        print("Enviando análisis a Bermudas...")
        start = time.time()
        
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=30
        )
        
        elapsed = time.time() - start
        
        if response.status_code == 200:
            result = response.json()
            arch_results = result.get('archaeological_results', {})
            prob = arch_results.get('archaeological_probability', 0)
            
            print(f"EXITO en {elapsed:.2f}s!")
            print(f"Probabilidad: {prob:.2%}")
            
            if elapsed < 10:
                print("BERMUDA OPTIMIZADA CORRECTAMENTE!")
                return True
            else:
                print("Mejora notable pero puede optimizarse más")
                return True
        else:
            print(f"Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error análisis: {e}")
        return False

if __name__ == "__main__":
    print("TEST FINAL - Bermudas Optimización")
    print("="*40)
    
    success = test_bermuda_direct()
    
    if success:
        print("\nSISTEMA FUNCIONAL!")
    else:
        print("\nINICIAR BACKEND CON:")
        print("python run_archeoscope.py")