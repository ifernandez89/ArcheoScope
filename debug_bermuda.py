#!/usr/bin/env python3
"""
Debug real-time del backend para Bermudas
"""

import requests
import json
import time

def debug_bermuda_realtime():
    """Debug paso a paso del backend"""
    
    print("DEBUG REALTIME - Bermudas")
    print("Coordenadas: 32.300, -64.783")
    
    # 1. Test status endpoint
    try:
        print("\n1. Verificando /status...")
        start = time.time()
        response = requests.get("http://localhost:8002/status", timeout=3)
        
        if response.status_code == 200:
            print(f"   Status OK en {time.time() - start:.2f}s")
            print(f"   Backend: {response.json()}")
        else:
            print(f"   ERROR Status: {response.status_code}")
            return
    except Exception as e:
        print(f"   ERROR Status: {e}")
        return
    
    # 2. Test análisis con logging en tiempo real
    try:
        print("\n2. Iniciando análisis con logging...")
        
        test_data = {
            "lat_min": 32.299,
            "lat_max": 32.301,
            "lon_min": -64.784,
            "lon_max": -64.782,
            "region_name": "Bermuda Debug"
        }
        
        print("   Enviando solicitud...")
        start = time.time()
        
        # Stream response para ver logging en tiempo real
        response = requests.post(
            "http://localhost:8002/analyze",
            json=test_data,
            timeout=20,
            stream=False
        )
        
        elapsed = time.time() - start
        print(f"   Respuesta recibida en {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            
            # Extraer información clave
            print(f"   ✓ HTTP 200 OK")
            print(f"   ✓ Ambiente: {result.get('environment_classification', {}).get('environment_type', 'Unknown')}")
            print(f"   ✓ Probabilidad: {result.get('archaeological_results', {}).get('archaeological_probability', 0):.2%}")
            
            # Tiempo total
            if elapsed < 5:
                print(f"   🎉 OPTIMIZADO: {elapsed:.2f}s <5s")
            elif elapsed < 10:
                print(f"   ⚠️ Mejorado: {elapsed:.2f}s <10s")
            else:
                print(f"   ❌ Todavía lento: {elapsed:.2f}s")
                
            # Ver estructura de respuesta
            print(f"   ✓ Keys: {list(result.keys())}")
            
        else:
            print(f"   ❌ HTTP {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            
    except requests.exceptions.Timeout:
        elapsed = time.time() - start
        print(f"   ❌ TIMEOUT después de {elapsed:.2f}s")
        print("   → Posible bucle infinito en procesamiento")
    except Exception as e:
        elapsed = time.time() - start
        print(f"   ❌ Error después de {elapsed:.2f}s: {e}")

if __name__ == "__main__":
    print("ArcheoScope - Debug Realtime")
    print("="*40)
    debug_bermuda_realtime()