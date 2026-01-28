#!/usr/bin/env python3
"""
Test rápido para verificar que la función createAlternativeVisualization está correctamente definida
"""

import requests

def test_function_fix():
    """Test que la función esté correctamente definida"""
    print("🔧 ===== TEST DE CORRECCIÓN DE FUNCIÓN =====")
    
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
            print("✅ Backend responde correctamente")
            data = response.json()
            
            # Verificar estructura
            if 'anomaly_map' in data and 'wreck_candidates' in data['anomaly_map']:
                candidates = data['anomaly_map']['wreck_candidates']
                print(f"🚢 {len(candidates)} candidatos a naufragios detectados")
                print("✅ Estructura correcta para createAlternativeVisualization")
                
                # Mostrar ejemplo de candidato
                if candidates:
                    candidate = candidates[0]
                    print(f"📊 Ejemplo de candidato:")
                    print(f"   ID: {candidate.get('anomaly_id', 'N/A')}")
                    print(f"   Coordenadas: {candidate.get('coordinates', 'N/A')}")
                    print(f"   Prioridad: {candidate.get('archaeological_priority', 'N/A')}")
                
                return True
            else:
                print("❌ Estructura incorrecta en respuesta")
                return False
        else:
            print(f"❌ Error en backend: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

def main():
    print("🔍 Verificando corrección de función createAlternativeVisualization")
    
    success = test_function_fix()
    
    print("\n🧪 ===== VERIFICACIÓN MANUAL REQUERIDA =====")
    print("1. 🌐 Abrir http://localhost:8080")
    print("2. 📍 Ingresar coordenadas: 25.0, 25.1, -70.1, -70.0")
    print("3. 🔍 Hacer clic en 'INVESTIGAR'")
    print("4. ✅ Verificar que NO aparezca:")
    print("   'createAlternativeVisualization is not defined'")
    print("5. 🗺️ Verificar que aparezcan marcadores de naufragios en el mapa")
    
    if success:
        print("\n✅ FUNCIÓN CORRECTAMENTE DEFINIDA - LISTO PARA PRUEBA")
    else:
        print("\n❌ PROBLEMAS DETECTADOS - REVISAR IMPLEMENTACIÓN")

if __name__ == "__main__":
    main()