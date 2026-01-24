#!/usr/bin/env python3
"""
Test para verificar que el backend genera resultados determinísticos
"""

import sys
from pathlib import Path
import requests
import json

# Agregar el backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

def test_backend_determinism():
    """Test para verificar determinismo del backend"""
    
    # Coordenadas de prueba (las mismas que usa el usuario en el frontend)
    test_coords = {
        "lat_min": 25.522344,
        "lat_max": 25.522344,
        "lon_min": -70.36133799999999,
        "lon_max": -70.36133799999999
    }
    
    print("🧪 TESTING BACKEND DETERMINISM")
    print(f"📍 Coordenadas de prueba: {test_coords}")
    print("=" * 50)
    
    results = []
    
    # Hacer 5 llamadas al backend
    for i in range(5):
        try:
            response = requests.post(
                "http://localhost:8003/analyze",
                json=test_coords,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extraer datos relevantes
                stats = data.get("statistical_results", {})
                wreck_candidates = stats.get("wreck_candidates", 0)
                total_anomalies = stats.get("total_anomalies", 0)
                high_priority = stats.get("high_priority_targets", 0)
                
                result = {
                    "test": i + 1,
                    "wreck_candidates": wreck_candidates,
                    "total_anomalies": total_anomalies,
                    "high_priority_targets": high_priority
                }
                
                results.append(result)
                
                print(f"✅ Test {i+1}: {wreck_candidates} candidatos, {total_anomalies} anomalías, {high_priority} alta prioridad")
                
            else:
                print(f"❌ Test {i+1}: Error HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Test {i+1}: Error - {e}")
    
    print("=" * 50)
    
    # Analizar resultados
    if len(results) >= 2:
        first_result = results[0]
        all_identical = True
        
        for result in results[1:]:
            if (result["wreck_candidates"] != first_result["wreck_candidates"] or
                result["total_anomalies"] != first_result["total_anomalies"] or
                result["high_priority_targets"] != first_result["high_priority_targets"]):
                all_identical = False
                break
        
        if all_identical:
            print("✅ RESULTADO: BACKEND ES DETERMINÍSTICO")
            print(f"   Todos los tests retornaron: {first_result['wreck_candidates']} candidatos")
        else:
            print("❌ RESULTADO: BACKEND NO ES DETERMINÍSTICO")
            print("   Resultados diferentes:")
            for result in results:
                print(f"   Test {result['test']}: {result['wreck_candidates']} candidatos")
    else:
        print("❌ RESULTADO: NO SE PUDIERON COMPLETAR SUFICIENTES TESTS")
    
    return results

if __name__ == "__main__":
    test_backend_determinism()