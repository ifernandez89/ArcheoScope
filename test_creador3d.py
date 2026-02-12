#!/usr/bin/env python3
"""
Test de API Creador3D
======================

Tests de los diferentes endpoints de generación.
"""

import requests
import json
import time

API_BASE = "http://localhost:8004"

def test_status():
    """Test endpoint de status."""
    print("\n" + "="*70)
    print("🔍 TEST 1: Status de la API")
    print("="*70)
    
    response = requests.get(f"{API_BASE}/status")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"📁 Output dir: {data['output_dir']}")
        print(f"🎨 Modelos generados: {data['models_generated']}")
        print(f"🏛️  Morfologías disponibles: {data['morphologies_available']}")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        return False


def test_list_morphologies():
    """Test listar morfologías."""
    print("\n" + "="*70)
    print("🔍 TEST 2: Listar Morfologías")
    print("="*70)
    
    response = requests.get(f"{API_BASE}/morphologies")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total: {data['total']} morfologías")
        print("\n📋 Disponibles:")
        for morph in data['morphologies']:
            print(f"   • {morph['class']}: {morph['origin']}")
            print(f"     Ratio H/W: {morph['height_width_ratio']:.2f}, Muestras: {morph['samples']}")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        return False


def test_generate_from_parameters():
    """Test generar desde parámetros."""
    print("\n" + "="*70)
    print("🔍 TEST 3: Generar desde Parámetros")
    print("="*70)
    
    request_data = {
        "height_m": 30.0,
        "width_m": 50.0,
        "depth_m": 50.0,
        "shape_type": "pyramid",
        "output_name": "test_pyramid_custom",
        "color": "#D4A574"
    }
    
    print(f"📊 Parámetros:")
    print(f"   Tipo: {request_data['shape_type']}")
    print(f"   Dimensiones: {request_data['height_m']}m × {request_data['width_m']}m")
    
    response = requests.post(
        f"{API_BASE}/generate/parameters",
        json=request_data,
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Generación exitosa!")
        print(f"   PNG: {data['png_filename']}")
        print(f"   OBJ: {data['obj_filename']}")
        print(f"   Volumen: {data['volume_m3']:.2f} m³")
        
        # Descargar PNG
        time.sleep(1)
        png_response = requests.get(f"{API_BASE}/model/{data['png_filename']}")
        if png_response.status_code == 200:
            print(f"   📥 PNG descargado: {len(png_response.content):,} bytes")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False


def test_generate_from_morphology():
    """Test generar desde morfología."""
    print("\n" + "="*70)
    print("🔍 TEST 4: Generar desde Morfología")
    print("="*70)
    
    request_data = {
        "morphological_class": "moai",
        "scale_factor": 1.5,
        "output_name": "test_moai_scaled"
    }
    
    print(f"📊 Parámetros:")
    print(f"   Clase: {request_data['morphological_class']}")
    print(f"   Escala: {request_data['scale_factor']}x")
    
    response = requests.post(
        f"{API_BASE}/generate/morphology",
        json=request_data,
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Generación exitosa!")
        print(f"   Clase: {data['morphological_class']}")
        print(f"   Origen: {data['cultural_origin']}")
        print(f"   PNG: {data['png_filename']}")
        print(f"   Volumen: {data['volume_m3']:.2f} m³")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False


def test_generate_custom():
    """Test generar geometría custom."""
    print("\n" + "="*70)
    print("🔍 TEST 5: Generar Geometría Custom")
    print("="*70)
    
    # Pirámide simple custom
    request_data = {
        "vertices": [
            [0, 0, 0],      # Base
            [10, 0, 0],
            [10, 10, 0],
            [0, 10, 0],
            [5, 5, 15]      # Ápice
        ],
        "faces": [
            [0, 1, 4],      # Caras laterales
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4],
            [0, 2, 1],      # Base
            [0, 3, 2]
        ],
        "output_name": "test_custom_pyramid"
    }
    
    print(f"📊 Parámetros:")
    print(f"   Vértices: {len(request_data['vertices'])}")
    print(f"   Caras: {len(request_data['faces'])}")
    
    response = requests.post(
        f"{API_BASE}/generate/custom",
        json=request_data,
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Generación exitosa!")
        print(f"   PNG: {data['png_filename']}")
        print(f"   OBJ: {data['obj_filename']}")
        print(f"   Vértices: {data['vertices_count']}")
        print(f"   Caras: {data['faces_count']}")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎨 TEST SUITE - CREADOR3D API")
    print("="*70)
    print("\n⚠️  Asegúrate de que la API esté corriendo en puerto 8004")
    print("   Ejecuta: python run_creador3d.py")
    
    input("\nPresiona Enter para continuar...")
    
    results = []
    
    # Ejecutar tests
    results.append(("Status", test_status()))
    results.append(("List Morphologies", test_list_morphologies()))
    results.append(("Generate from Parameters", test_generate_from_parameters()))
    results.append(("Generate from Morphology", test_generate_from_morphology()))
    results.append(("Generate Custom", test_generate_custom()))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n🎯 Resultado: {passed}/{total} tests exitosos")
    
    if passed == total:
        print("\n🎉 ¡Todos los tests pasaron!")
    else:
        print("\n⚠️  Algunos tests fallaron")
