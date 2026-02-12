#!/usr/bin/env python3
"""
Test de clasificación geográfica para múltiples regiones
"""

import requests
import json

def test_location(lat, lon, region_name, expected_class=None):
    """Test una ubicación específica."""
    
    print(f"\n{'='*70}")
    print(f"📍 TEST: {region_name}")
    print(f"   Coordenadas: {lat}, {lon}")
    if expected_class:
        print(f"   Esperado: {expected_class}")
    print('='*70)
    
    test_data = {
        "lat": lat,
        "lon": lon,
        "region_name": region_name
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/api/geometric-inference-3d",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Clase: {result['morphological_class'].upper()}")
            print(f"   Origen: {result['cultural_origin']}")
            print(f"   Confianza: {result['confidence']:.2%}")
            print(f"   Score: {result['morphological_score']:.4f}")
            
            if expected_class:
                if result['morphological_class'].upper() == expected_class.upper():
                    print(f"   🎯 ✅ CORRECTO")
                    return True
                else:
                    print(f"   ❌ ERROR: Se esperaba {expected_class}")
                    return False
            return True
            
        else:
            print(f"❌ ERROR HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        return False


if __name__ == "__main__":
    print("\n🌍 TEST DE CLASIFICACIÓN GEOGRÁFICA")
    print("="*70)
    
    results = []
    
    # Test 1: Rapa Nui (debe ser MOAI)
    results.append(test_location(
        -27.126, -109.287,
        "Rapa Nui (Easter Island)",
        expected_class="MOAI"
    ))
    
    # Test 2: Giza, Egipto (debe ser clase egipcia)
    results.append(test_location(
        29.979, 31.134,
        "Giza, Egypt",
        expected_class=None  # Puede ser SPHINX, COLOSSUS, o EGYPTIAN_STATUE
    ))
    
    # Test 3: Luxor, Egipto (Colosos de Memnon)
    results.append(test_location(
        25.720, 32.610,
        "Luxor, Egypt (Colossi of Memnon)",
        expected_class=None
    ))
    
    # Test 4: Rapa Nui - segunda prueba (consistencia)
    results.append(test_location(
        -27.112, -109.349,
        "Rapa Nui - Rano Raraku",
        expected_class="MOAI"
    ))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"✅ Exitosos: {passed}/{total}")
    print(f"❌ Fallidos: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TODOS LOS TESTS PASARON")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
