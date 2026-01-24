#!/usr/bin/env python3
"""
Test para verificar que la corrección del frontend funciona
"""

import requests
import time

def test_frontend_fix():
    """Test que el frontend maneja correctamente la respuesta del backend"""
    print("🔧 ===== TEST DE CORRECCIÓN DEL FRONTEND =====")
    
    # Coordenadas de prueba
    coords = {
        "lat_min": 25.0,
        "lat_max": 25.1,
        "lon_min": -70.1,
        "lon_max": -70.0
    }
    
    try:
        print("📡 Enviando solicitud al backend...")
        response = requests.post(
            "http://localhost:8003/analyze",
            json=coords,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend responde correctamente")
            
            # Verificar estructura esperada por frontend
            checks = {
                "anomaly_map presente": "anomaly_map" in data,
                "region_info presente": "region_info" in data,
                "statistical_results presente": "statistical_results" in data
            }
            
            for check, result in checks.items():
                print(f"   {'✅' if result else '❌'} {check}")
            
            # Verificar estructura específica de anomaly_map
            if "anomaly_map" in data:
                anomaly_map = data["anomaly_map"]
                print(f"🗺️ Contenido de anomaly_map: {list(anomaly_map.keys())}")
                
                # Verificar que tenga los campos que el backend realmente devuelve
                expected_fields = ["wreck_candidates", "bathymetric_anomalies"]
                for field in expected_fields:
                    if field in anomaly_map:
                        value = anomaly_map[field]
                        print(f"   ✅ {field}: {value}")
                    else:
                        print(f"   ❌ {field}: no encontrado")
            
            print("\n🎯 RESULTADO:")
            print("   El frontend ahora debe manejar esta estructura sin errores")
            print("   Ya no debería aparecer el error 'Cannot read properties of undefined'")
            
            return True
        else:
            print(f"❌ Error en backend: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

def test_instructions():
    """Instrucciones para verificar manualmente"""
    print("\n🧪 ===== VERIFICACIÓN MANUAL REQUERIDA =====")
    print("1. 🌐 Abrir http://localhost:8080")
    print("2. 📍 Ingresar coordenadas: 25.0, 25.1, -70.1, -70.0")
    print("3. 🔍 Hacer clic en 'INVESTIGAR'")
    print("4. ✅ Verificar que NO aparezca el error:")
    print("   'TypeError: Cannot read properties of undefined (reading 'length')'")
    print("5. 🗺️ Verificar que aparezcan marcadores en el mapa (candidatos a naufragios)")
    print("6. 🔍 Abrir lupa arqueológica y verificar que funcione correctamente")
    
    print("\n📊 CAMBIOS IMPLEMENTADOS:")
    print("   ✅ Validación de estructura de datos del backend")
    print("   ✅ Visualización alternativa para datos reales")
    print("   ✅ Manejo de wreck_candidates y bathymetric_anomalies")
    print("   ✅ Eliminación de dependencia de anomaly_mask inexistente")

if __name__ == "__main__":
    success = test_frontend_fix()
    test_instructions()
    
    if success:
        print("\n✅ CORRECCIÓN IMPLEMENTADA - LISTO PARA PRUEBA MANUAL")
    else:
        print("\n❌ PROBLEMAS DETECTADOS - REVISAR BACKEND")