#!/usr/bin/env python3
"""
Test del backend volumétrico de ArcheoScope
"""

import requests
import json
import sys

def test_backend_status():
    """Test del estado del backend"""
    try:
        response = requests.get("http://localhost:8002/status/detailed", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend disponible")
            print(f"   - Estado volumétrico: {data.get('volumetric_engine', 'N/A')}")
            print(f"   - Estado IA: {data.get('ai_status', 'N/A')}")
            return True
        else:
            print(f"❌ Backend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False

def test_volumetric_analysis():
    """Test del análisis volumétrico"""
    try:
        # Datos de prueba para Giza
        test_data = {
            "lat_min": 29.9750,
            "lat_max": 29.9800,
            "lon_min": 31.1300,
            "lon_max": 31.1350,
            "resolution_m": 500,
            "layers_to_analyze": [
                "ndvi_vegetation", 
                "thermal_lst", 
                "sar_backscatter"
            ],
            "active_rules": ["all"],
            "region_name": "Giza Plateau Test",
            "include_explainability": False,
            "include_validation_metrics": False
        }
        
        print("🔍 Ejecutando análisis de prueba...")
        response = requests.post(
            "http://localhost:8002/analyze", 
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Análisis completado")
            
            # Verificar datos volumétricos
            volumetric_data = data.get('scientific_report', {}).get('volumetric_geometric_inference')
            if volumetric_data:
                print("✅ Datos volumétricos generados:")
                summary = volumetric_data.get('analysis_summary', {})
                print(f"   - Volumen estimado: {summary.get('total_estimated_volume_m3', 'N/A')} m³")
                print(f"   - Altura máxima: {summary.get('max_estimated_height_m', 'N/A')} m")
                print(f"   - Confianza promedio: {summary.get('average_confidence', 'N/A')}")
                
                # Verificar si el modelo está disponible
                model_available = volumetric_data.get('volumetric_model_available', False)
                print(f"   - Modelo 3D disponible: {model_available}")
                
                if model_available:
                    print("✅ El modelo volumétrico 3D debería funcionar en el frontend")
                else:
                    print("⚠️ Modelo volumétrico no disponible")
                    reason = volumetric_data.get('reason', 'Razón no especificada')
                    print(f"   - Razón: {reason}")
                
                return True
            else:
                print("❌ No se generaron datos volumétricos")
                return False
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            print(f"   - Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en análisis volumétrico: {e}")
        return False

def main():
    print("🏺 TEST DEL BACKEND VOLUMÉTRICO ARCHEOSCOPE")
    print("=" * 50)
    
    # Test 1: Estado del backend
    if not test_backend_status():
        print("\n❌ Backend no disponible. Asegúrate de que esté ejecutándose.")
        sys.exit(1)
    
    print()
    
    # Test 2: Análisis volumétrico
    if test_volumetric_analysis():
        print("\n✅ TODOS LOS TESTS PASARON")
        print("El modelo volumétrico 3D debería funcionar correctamente en el frontend.")
    else:
        print("\n❌ TESTS FALLARON")
        print("Revisa los logs del backend para más detalles.")

if __name__ == "__main__":
    main()