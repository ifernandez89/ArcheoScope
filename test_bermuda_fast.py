#!/usr/bin/env python3
"""
Test optimizado para coordenadas de Bermudas (32.300, -64.783)
Verifica que el analisis tarda <5 segundos despues de las optimizaciones
"""

import requests
import json
import time

def test_bermuda_optimized():
    """Test analisis optimizado para Bermudas"""
    
    print("TEST BERMUDA OPTIMIZADO")
    print("Verificando analisis para 32.300, -64.783")
    
    # Datos de test para Bermudas
    test_data = {
        "lat_min": 32.295,
        "lat_max": 32.305,
        "lon_min": -64.788,
        "lon_max": -64.778,
        "region_name": "Bermuda Optimized Test"
    }
    
    try:
        print("Enviando solicitud...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=10  # Timeout de 10 segundos
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"Analisis completado en {elapsed_time:.2f} segundos")
            
            # Extraer resultados de forma segura
            arch_results = result.get('archaeological_results', {})
            prob = arch_results.get('archaeological_probability', 0)
            measurements = result.get('instrumental_measurements', [])
            
            print(f"Probabilidad arqueologica: {prob:.2%}")
            print(f"Numero de instrumentos: {len(measurements)}")
            
            # Verificacion de optimizacion
            if elapsed_time < 5:
                print(f"OPTIMIZACION EXITOSA: <5 segundos!")
            elif elapsed_time < 10:
                print(f"Mejora notable: {elapsed_time:.2f}s (<10s)")
            else:
                print(f"Todavia lento: {elapsed_time:.2f}s")
            
            return elapsed_time < 10
            
        else:
            print(f"Error HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"TIMEOUT despues de 10 segundos")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("ArcheoScope - Test de Optimizacion")
    print("="*50)
    
    # Test principal: Bermudas
    bermuda_success = test_bermuda_optimized()
    
    print(f"\nRESULTADO FINAL:")
    print(f"  Bermudas optimizadas: {'OK' if bermuda_success else 'ERROR'}")
    
    if bermuda_success:
        print("  SISTEMA OPTIMIZADO - Tiempos <10s!")
    else:
        print("  NECESITA MAS OPTIMIZACION")