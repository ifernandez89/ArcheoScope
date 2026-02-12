#!/usr/bin/env python3
"""
Test de integración final - Sistema completo
"""

import requests
import time

def test_location_full(lat, lon, region_name, expected_class):
    """Test completo de una ubicación."""
    
    print(f"\n{'='*70}")
    print(f"🗺️  {region_name}")
    print(f"   Coordenadas: {lat}, {lon}")
    print(f"   Esperado: {expected_class}")
    print('='*70)
    
    # Generar modelo
    test_data = {
        "lat": lat,
        "lon": lon,
        "region_name": region_name
    }
    
    try:
        # POST: Generar
        response = requests.post(
            "http://localhost:8003/api/geometric-inference-3d",
            json=test_data,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"❌ Error POST: {response.status_code}")
            return False
        
        result = response.json()
        
        # Verificar clasificación
        actual_class = result['morphological_class'].upper()
        print(f"\n✅ Clasificación: {actual_class}")
        print(f"   Origen: {result['cultural_origin']}")
        print(f"   Confianza: {result['confidence']:.2%}")
        
        if actual_class != expected_class.upper():
            print(f"   ⚠️  Se esperaba: {expected_class}")
            return False
        
        # Esperar escritura de archivos
        time.sleep(1)
        
        # GET: Descargar PNG
        png_url = f"http://localhost:8003/api/geometric-model/{result['png_filename']}"
        png_response = requests.get(png_url, timeout=30)
        
        if png_response.status_code != 200:
            print(f"❌ Error GET PNG: {png_response.status_code}")
            return False
        
        print(f"   📥 PNG: {len(png_response.content):,} bytes")
        
        # GET: Descargar OBJ
        obj_url = f"http://localhost:8003/api/geometric-model/{result['obj_filename']}"
        obj_response = requests.get(obj_url, timeout=30)
        
        if obj_response.status_code != 200:
            print(f"❌ Error GET OBJ: {obj_response.status_code}")
            return False
        
        print(f"   📥 OBJ: {len(obj_response.content):,} bytes")
        print(f"\n   🎯 ✅ TEST EXITOSO")
        
        return True
        
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        return False


if __name__ == "__main__":
    print("\n🚀 TEST DE INTEGRACIÓN FINAL - SISTEMA COMPLETO")
    print("="*70)
    
    tests = [
        # Test 1: Rapa Nui (MOAI)
        (-27.126, -109.287, "Rapa Nui (Easter Island)", "MOAI"),
        
        # Test 2: Giza (SPHINX o clase egipcia)
        (29.979, 31.134, "Giza, Egypt", "SPHINX"),
        
        # Test 3: Rapa Nui - Rano Raraku (MOAI)
        (-27.112, -109.349, "Rapa Nui - Rano Raraku", "MOAI"),
    ]
    
    results = []
    for lat, lon, name, expected in tests:
        results.append(test_location_full(lat, lon, name, expected))
        time.sleep(2)  # Pausa entre tests
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN FINAL")
    print("="*70)
    passed = sum(results)
    total = len(results)
    print(f"✅ Exitosos: {passed}/{total}")
    print(f"❌ Fallidos: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 SISTEMA COMPLETAMENTE FUNCIONAL")
        print("   ✅ Clasificación geográfica correcta")
        print("   ✅ Generación de modelos 3D")
        print("   ✅ Servicio de archivos PNG/OBJ")
        print("   ✅ Pipeline completo operativo")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
    
    print("="*70)
    exit(0 if passed == total else 1)
