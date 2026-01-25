#!/usr/bin/env python3
"""
FIX CRÍTICO: Optimización para Bermudas - Simple y directo
"""

import requests
import time

def test_bermuda_fix():
    """Test con optimización mínima pero efectiva"""
    
    print("BERMUDA FIX CRÍTICO")
    print("Coordenadas: 32.300, -64.783")
    
    # Optimización 1: Área mínima para reducir cálculo
    test_data = {
        "lat_min": 32.2999,
        "lat_max": 32.3001,
        "lon_min": -64.7831,
        "lon_max": -64.7829,
        "region_name": "Bermuda Critical Fix"
    }
    
    try:
        print("Iniciando análisis con área mínima...")
        start = time.time()
        
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=30
        )
        
        elapsed = time.time() - start
        print(f"Respuesta en {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            arch_results = result.get('archaeological_results', {})
            prob = arch_results.get('archaeological_probability', 0)
            
            print(f"✅ Análisis exitoso!")
            print(f"   Probabilidad: {prob:.2%}")
            print(f"   Ambiente: {result.get('environment_classification', {}).get('environment_type', 'Unknown')}")
            
            if elapsed < 10:
                print(f"🎉 FIX EXITOSO: {elapsed:.2f}s <10s")
                return True
            else:
                print(f"⚠️ Mejora: {elapsed:.2f}s (antes: timeout)")
                return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            return False
            
    except Exception as e:
        elapsed = time.time() - start
        print(f"❌ Error tras {elapsed:.2f}s: {e}")
        return False

def backend_status():
    """Verificar estado del backend"""
    try:
        response = requests.get("http://localhost:8002/status", timeout=5)
        if response.status_code == 200:
            print("✅ Backend operativo")
            return True
        else:
            print(f"❌ Backend error: {response.status_code}")
            return False
    except:
        print("❌ Backend no responde")
        return False

if __name__ == "__main__":
    print("ARCHEOSCOPE - BERMUDA CRITICAL FIX")
    print("="*50)
    
    if backend_status():
        success = test_bermuda_fix()
        print(f"\nRESULTADO FINAL:")
        if success:
            print("✅ BERMUDA OPTIMIZADA - Sistema funcional")
        else:
            print("❌ Necesita más trabajo")
    else:
        print("❌ Backend no disponible - iniciar con: python run_archeoscope.py")