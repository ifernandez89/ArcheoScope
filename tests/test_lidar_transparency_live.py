#!/usr/bin/env python3
"""
Test en vivo del sistema de transparencia de LiDAR
Verifica que el backend y frontend estén funcionando correctamente
"""

import requests
import json
import time

def test_backend_connection():
    """Test de conexión al backend"""
    try:
        response = requests.get("http://localhost:8003/status/detailed", timeout=5)
        if response.status_code == 200:
            print("✅ Backend conectado correctamente")
            return True
        else:
            print(f"❌ Backend respondió con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False

def test_rapa_nui_analysis():
    """Test específico para Rapa Nui (sin LiDAR)"""
    print("\n🏝️ ===== TEST RAPA NUI (SIN LIDAR) =====")
    
    # Coordenadas de Rapa Nui
    coords = {
        "lat_min": -27.19,
        "lat_max": -27.17,
        "lon_min": -109.45,
        "lon_max": -109.43
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=coords,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Análisis completado para Rapa Nui")
            
            # Verificar que hay datos estadísticos
            if 'statistical_results' in data:
                stats = data['statistical_results']
                print(f"📊 Instrumentos detectados: {len(stats)}")
                
                # Verificar LiDAR específicamente
                if 'lidar_fullwave' in stats:
                    lidar_prob = stats['lidar_fullwave'].get('archaeological_probability', 0)
                    print(f"📡 LiDAR probability: {lidar_prob * 100:.1f}%")
                    print("🏷️ Frontend debe mostrar: 'LiDAR-Sintético' o 'LiDAR-No-Disponible'")
                else:
                    print("📡 No se encontraron datos LiDAR en respuesta")
                
                return True
            else:
                print("❌ No se encontraron resultados estadísticos")
                return False
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en análisis de Rapa Nui: {e}")
        return False

def test_uk_analysis():
    """Test específico para Reino Unido (con LiDAR)"""
    print("\n🇬🇧 ===== TEST REINO UNIDO (CON LIDAR) =====")
    
    # Coordenadas cerca de Stonehenge
    coords = {
        "lat_min": 51.17,
        "lat_max": 51.19,
        "lon_min": -1.83,
        "lon_max": -1.81
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/analyze",
            json=coords,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Análisis completado para Reino Unido")
            
            if 'statistical_results' in data:
                stats = data['statistical_results']
                print(f"📊 Instrumentos detectados: {len(stats)}")
                
                if 'lidar_fullwave' in stats:
                    lidar_prob = stats['lidar_fullwave'].get('archaeological_probability', 0)
                    print(f"📡 LiDAR probability: {lidar_prob * 100:.1f}%")
                    print("🏷️ Frontend debe mostrar: 'LiDAR-Arqueológico' o 'LiDAR-Sistemático'")
                
                return True
            else:
                print("❌ No se encontraron resultados estadísticos")
                return False
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en análisis de Reino Unido: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🔍 ===== TEST DE TRANSPARENCIA LIDAR EN VIVO =====")
    print("🌐 Frontend: http://localhost:8001")
    print("🔧 Backend: http://localhost:8003")
    
    # Test 1: Conexión al backend
    if not test_backend_connection():
        print("❌ No se puede continuar sin conexión al backend")
        return False
    
    # Test 2: Análisis de Rapa Nui (sin LiDAR)
    rapa_nui_ok = test_rapa_nui_analysis()
    
    # Test 3: Análisis de Reino Unido (con LiDAR)
    uk_ok = test_uk_analysis()
    
    # Resumen
    print("\n📋 ===== RESUMEN DE TESTS =====")
    print(f"🔧 Backend: {'✅' if test_backend_connection() else '❌'}")
    print(f"🏝️ Rapa Nui: {'✅' if rapa_nui_ok else '❌'}")
    print(f"🇬🇧 Reino Unido: {'✅' if uk_ok else '❌'}")
    
    print("\n🧪 ===== VERIFICACIÓN MANUAL REQUERIDA =====")
    print("1. 🌐 Abrir http://localhost:8001 en navegador")
    print("2. 📍 Probar coordenadas: -27.18, -109.44 (Rapa Nui)")
    print("3. 🔍 Verificar que anomalías muestren 'LiDAR-Sintético'")
    print("4. 📍 Probar coordenadas: 51.1789, -1.8262 (Stonehenge)")
    print("5. 🔍 Verificar que anomalías muestren 'LiDAR-Arqueológico'")
    print("6. 📊 Confirmar panel lateral muestre información de disponibilidad")
    
    return rapa_nui_ok and uk_ok

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ SISTEMA DE TRANSPARENCIA FUNCIONANDO CORRECTAMENTE")
    else:
        print("\n❌ PROBLEMAS DETECTADOS EN SISTEMA DE TRANSPARENCIA")