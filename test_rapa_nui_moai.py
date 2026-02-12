#!/usr/bin/env python3
"""
Test de clasificación MOAI para coordenadas de Rapa Nui (Isla de Pascua)
"""

import requests
import json

def test_rapa_nui_moai():
    """Test con coordenadas reales de Rapa Nui."""
    
    print("🗿 TEST: Clasificación MOAI en Rapa Nui")
    print("=" * 60)
    
    # Coordenadas de Rapa Nui (Isla de Pascua)
    test_data = {
        "lat": -27.126101597871173,
        "lon": -109.28676072066652,
        "region_name": "Rapa Nui (Easter Island)"
    }
    
    print(f"\n📍 Coordenadas: {test_data['lat']}, {test_data['lon']}")
    print(f"📍 Región: {test_data['region_name']}")
    
    try:
        print("\n🔄 Enviando solicitud al endpoint...")
        response = requests.post(
            "http://localhost:8003/api/geometric-inference-3d",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ RESPUESTA EXITOSA")
            print("=" * 60)
            print(f"🏛️  Clase Morfológica: {result['morphological_class']}")
            print(f"🌍 Origen Cultural: {result['cultural_origin']}")
            print(f"📊 Confianza: {result['confidence']:.2%}")
            print(f"📊 Score Morfológico: {result['morphological_score']:.4f}")
            print(f"📦 Volumen: {result['volume_m3']:.2f} m³")
            print(f"🖼️  Imagen PNG: {result['png_filename']}")
            print(f"📐 Modelo OBJ: {result['obj_filename']}")
            
            # Verificar si es MOAI
            if result['morphological_class'].upper() == 'MOAI':
                print("\n🎯 ✅ CORRECTO: Clasificado como MOAI")
                return True
            else:
                print(f"\n❌ ERROR: Clasificado como {result['morphological_class']}")
                print("   Se esperaba: MOAI")
                print("\n📋 Detalles completos:")
                print(json.dumps(result, indent=2))
                return False
                
        else:
            print(f"\n❌ ERROR HTTP {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"\n❌ EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_rapa_nui_moai()
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST EXITOSO: MOAI correctamente clasificado")
    else:
        print("⚠️  TEST FALLIDO: Revisar clasificación")
    print("=" * 60)
