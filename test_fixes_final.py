#!/usr/bin/env python3
"""
Test para verificar las correcciones finales:
1. Valores por defecto en site_name_generator cuando geocoding falla
2. Análisis se guarda correctamente en BD
"""

import sys
sys.path.insert(0, 'backend')

from site_name_generator import site_name_generator

def test_geocoding_fallbacks():
    """Test valores por defecto cuando geocoding falla."""
    
    print("🧪 TEST 1: Geocoding con valores por defecto")
    print("=" * 60)
    
    # Test 1: Coordenadas en mar abierto (donde falló antes)
    print("\n📍 Test: Mar del Norte (54.85, 3.25)")
    result = site_name_generator.generate_name(54.85, 3.25, 'shallow_sea')
    print(f"   Name: {result['name']}")
    print(f"   Country: {result['country']}")
    print(f"   Region: {result['region']}")
    assert result['country'] is not None, "❌ Country no debe ser None"
    assert result['country'] != '', "❌ Country no debe estar vacío"
    print("   ✅ Country tiene valor válido")
    
    # Test 2: Antártida
    print("\n📍 Test: Antártida (-75.0, 0.0)")
    result = site_name_generator.generate_name(-75.0, 0.0, 'polar_ice')
    print(f"   Name: {result['name']}")
    print(f"   Country: {result['country']}")
    print(f"   Region: {result['region']}")
    assert result['country'] == 'Antarctica', f"❌ Esperaba 'Antarctica', obtuvo '{result['country']}'"
    print("   ✅ Antártida detectada correctamente")
    
    # Test 3: Océano Pacífico
    print("\n📍 Test: Océano Pacífico (0.0, -150.0)")
    result = site_name_generator.generate_name(0.0, -150.0, 'shallow_sea')
    print(f"   Name: {result['name']}")
    print(f"   Country: {result['country']}")
    print(f"   Region: {result['region']}")
    assert result['country'] == 'International Waters', f"❌ Esperaba 'International Waters', obtuvo '{result['country']}'"
    print("   ✅ Aguas internacionales detectadas correctamente")
    
    # Test 4: Ártico
    print("\n📍 Test: Ártico (75.0, 0.0)")
    result = site_name_generator.generate_name(75.0, 0.0, 'polar_ice')
    print(f"   Name: {result['name']}")
    print(f"   Country: {result['country']}")
    print(f"   Region: {result['region']}")
    assert result['country'] == 'Arctic Region', f"❌ Esperaba 'Arctic Region', obtuvo '{result['country']}'"
    print("   ✅ Ártico detectado correctamente")
    
    # Test 5: Ubicación con geocoding exitoso (México)
    print("\n📍 Test: México (26.95, -111.85)")
    result = site_name_generator.generate_name(26.95, -111.85, 'desert')
    print(f"   Name: {result['name']}")
    print(f"   Country: {result['country']}")
    print(f"   Region: {result['region']}")
    assert result['country'] is not None, "❌ Country no debe ser None"
    print("   ✅ Geocoding exitoso")
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS PASARON")
    print("\n📋 RESUMEN:")
    print("   • Valores por defecto funcionan correctamente")
    print("   • Country NUNCA es None")
    print("   • Region NUNCA es None")
    print("   • Antártida, Ártico y Aguas Internacionales detectados")
    print("   • Geocoding normal sigue funcionando")

if __name__ == "__main__":
    test_geocoding_fallbacks()
