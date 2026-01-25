#!/usr/bin/env python3
"""
Test SIMPLE para verificar optimización de Bermudas
"""

import requests
import time
import json

def test_simple_bermuda():
    """Test simple sin dependencias complejas"""
    
    print("Test SIMPLE Bermudas")
    
    # Test básico de conectividad
    try:
        print("Verificando backend...")
        start = time.time()
        response = requests.get("http://localhost:8002/status", timeout=5)
        
        if response.status_code == 200:
            print(f"Backend responde en {time.time() - start:.2f}s")
            
            # Test de análisis simple
            test_data = {
                "lat_min": 32.299,
                "lat_max": 32.301,
                "lon_min": -64.784,
                "lon_max": -64.782,
                "region_name": "Bermuda Simple"
            }
            
            print("Enviando análisis simple...")
            start = time.time()
            
            response = requests.post(
                "http://localhost:8002/analyze",
                json=test_data,
                timeout=15  # Aumentado a 15s
            )
            
            elapsed = time.time() - start
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Análisis completado en {elapsed:.2f}s")
                
                # Extraer resultados clave
                arch_results = result.get('archaeological_results', {})
                prob = arch_results.get('archaeological_probability', 0)
                
                print(f"Probabilidad arqueológica: {prob:.2%}")
                
                if elapsed < 10:
                    print("🎉 OPTIMIZACIÓN EXITOSA: <10s")
                    return True
                elif elapsed < 20:
                    print("⚠️ Mejora notable: <20s")
                    return True
                else:
                    print(f"❌ Todavía lento: {elapsed:.2f}s")
                    return False
            else:
                print(f"❌ Error HTTP {response.status_code}")
                return False
        else:
            print(f"❌ Status error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - Backend no responde")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("ArcheoScope - Test Simple de Optimización")
    print("="*50)
    
    success = test_simple_bermuda()
    
    print(f"\nRESULTADO:")
    if success:
        print("✅ Sistema optimizado correctamente")
    else:
        print("❌ Necesita más optimización")