#!/usr/bin/env python3
"""
Test de timing para un solo sitio
"""

import requests
import json
import time

API_URL = "http://localhost:8002"

def test_giza():
    """Probar Giza y medir tiempo"""
    
    print("🏛️  TEST: Giza Pyramids")
    print("="*60)
    
    request_data = {
        "lat_min": 29.969,
        "lat_max": 29.989,
        "lon_min": 31.124,
        "lon_max": 31.144,
        "region_name": "Giza Pyramids Test",
        "resolution_m": 1000
    }
    
    print(f"📡 Enviando request...")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json=request_data,
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        print(f"⏱️  Tiempo total: {elapsed:.2f} segundos")
        
        if response.status_code == 200:
            result = response.json()
            
            prob = result.get("archaeological_results", {}).get("archaeological_probability", 0)
            env = result.get("environment_classification", {}).get("environment_type", "unknown")
            
            print(f"✅ Status: {response.status_code}")
            print(f"🌍 Ambiente: {env}")
            print(f"📊 Probabilidad: {prob:.2%}")
            
            # Verificar si hay explicación IA
            ai_exp = result.get("ai_explanations", {})
            ai_available = ai_exp.get("ai_available", False)
            
            print(f"🤖 IA disponible: {'✅ SÍ' if ai_available else '❌ NO'}")
            
            if ai_available:
                explanation = ai_exp.get("explanation", "")
                print(f"💬 Explicación IA ({len(explanation)} chars):")
                print(f"   {explanation[:200]}...")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        print(f"❌ TIMEOUT después de {elapsed:.2f} segundos")
        return False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ Error después de {elapsed:.2f} segundos: {e}")
        return False

if __name__ == "__main__":
    test_giza()
