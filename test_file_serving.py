#!/usr/bin/env python3
"""
Test de servicio de archivos PNG/OBJ
"""

import requests
import time

def test_full_workflow():
    """Test completo: generar y descargar archivos."""
    
    print("🧪 TEST: Workflow completo de generación y descarga")
    print("="*70)
    
    # Paso 1: Generar modelo 3D
    print("\n📍 Paso 1: Generar modelo 3D para Giza...")
    
    test_data = {
        "lat": 29.9753,
        "lon": 31.1376,
        "region_name": "Giza, Egypt"
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/api/geometric-inference-3d",
            json=test_data,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"❌ Error en POST: {response.status_code}")
            print(response.text)
            return False
        
        result = response.json()
        print(f"✅ Modelo generado: {result['morphological_class']}")
        print(f"   PNG: {result['png_filename']}")
        print(f"   OBJ: {result['obj_filename']}")
        
        png_filename = result['png_filename']
        obj_filename = result['obj_filename']
        
        # Pequeña pausa para asegurar que el archivo está escrito
        time.sleep(1)
        
        # Paso 2: Descargar PNG
        print(f"\n📥 Paso 2: Descargar PNG...")
        png_url = f"http://localhost:8003/api/geometric-model/{png_filename}"
        print(f"   URL: {png_url}")
        
        png_response = requests.get(png_url, timeout=30)
        
        if png_response.status_code != 200:
            print(f"❌ Error descargando PNG: {png_response.status_code}")
            print(png_response.text)
            return False
        
        print(f"✅ PNG descargado: {len(png_response.content)} bytes")
        
        # Paso 3: Descargar OBJ
        print(f"\n📥 Paso 3: Descargar OBJ...")
        obj_url = f"http://localhost:8003/api/geometric-model/{obj_filename}"
        print(f"   URL: {obj_url}")
        
        obj_response = requests.get(obj_url, timeout=30)
        
        if obj_response.status_code != 200:
            print(f"❌ Error descargando OBJ: {obj_response.status_code}")
            print(obj_response.text)
            return False
        
        print(f"✅ OBJ descargado: {len(obj_response.content)} bytes")
        
        print("\n" + "="*70)
        print("🎉 WORKFLOW COMPLETO EXITOSO")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_full_workflow()
    exit(0 if success else 1)
