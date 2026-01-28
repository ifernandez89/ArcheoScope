#!/usr/bin/env python3
"""
Test mínimo para verificar que la corrección funcione sin romper UI
"""

import requests

def test_minimal_fix():
    """Test que la corrección mínima funcione"""
    print("🔧 ===== TEST DE CORRECCIÓN MÍNIMA =====")
    
    coords = {
        "lat_min": 25.0,
        "lat_max": 25.1,
        "lon_min": -70.1,
        "lon_max": -70.0
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=coords,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend responde correctamente")
            
            # Verificar estructura
            has_anomaly_map = 'anomaly_map' in data
            has_anomaly_mask = has_anomaly_map and 'anomaly_mask' in data['anomaly_map']
            
            print(f"📊 anomaly_map presente: {has_anomaly_map}")
            print(f"🗺️ anomaly_mask presente: {has_anomaly_mask}")
            
            if not has_anomaly_mask:
                print("⚠️ anomaly_mask no encontrado - validación debe activarse")
                print("✅ Frontend debe manejar esto sin error ahora")
            
            return True
        else:
            print(f"❌ Error en backend: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

def main():
    print("🛡️ Verificando corrección mínima y segura")
    
    success = test_minimal_fix()
    
    print("\n🧪 ===== VERIFICACIÓN MANUAL REQUERIDA =====")
    print("1. 🌐 Abrir http://localhost:8080")
    print("2. 📍 Ingresar coordenadas cualquiera")
    print("3. 🔧 Hacer clic en 'Calibrar' (opcional)")
    print("4. 🔍 Hacer clic en 'INVESTIGAR'")
    print("5. ✅ Verificar que NO aparezca:")
    print("   'Cannot read properties of undefined (reading 'length')'")
    print("6. ✅ Verificar que UI NO se desplace hacia arriba")
    print("7. ✅ Verificar que aparezca mensaje de advertencia en consola")
    
    if success:
        print("\n✅ CORRECCIÓN MÍNIMA APLICADA - PROBAR MANUALMENTE")
    else:
        print("\n❌ PROBLEMAS DETECTADOS - REVISAR BACKEND")

if __name__ == "__main__":
    main()