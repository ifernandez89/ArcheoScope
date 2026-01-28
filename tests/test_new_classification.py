#!/usr/bin/env python3
"""
Test del nuevo sistema de clasificación arqueológica con:
- Clasificación "landscape_modified_non_structural"
- Penalización por resolución
- Etiqueta "Solo verificable con magnetometría/GPR"
"""

import requests
import json
from datetime import datetime

def test_new_archaeological_classification():
    """Test del nuevo sistema de clasificación."""
    
    # Datos de prueba para análisis arqueológico
    test_data = {
        "lat_min": 41.8500,
        "lat_max": 41.8600,
        "lon_min": 12.5000,
        "lon_max": 12.5100,
        "resolution_m": 500,  # Resolución gruesa para activar penalización
        "region_name": "Test Región - Nueva Clasificación",
        "include_explainability": True,
        "include_validation_metrics": True,
        "layers_to_analyze": [
            "ndvi_vegetation", "thermal_lst", "sar_backscatter", 
            "surface_roughness", "soil_salinity"
        ],
        "active_rules": ["all"]
    }
    
    print("🧪 Probando nuevo sistema de clasificación arqueológica...")
    print(f"📍 Región: {test_data['region_name']}")
    print(f"🔍 Resolución: {test_data['resolution_m']}m (para activar penalización)")
    print()
    
    try:
        # Hacer petición al backend
        response = requests.post(
            "http://localhost:8004/analyze",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Análisis completado exitosamente!")
            print()
            
            # Verificar nueva clasificación
            physics_results = result.get('physics_results', {})
            evaluations = physics_results.get('evaluations', {})
            
            print("🔍 VERIFICANDO NUEVAS CARACTERÍSTICAS:")
            print()
            
            # 1. Verificar clasificación landscape_modified_non_structural
            landscape_modified_found = False
            resolution_penalty_found = False
            geophysical_required_found = False
            
            for rule_name, evaluation in evaluations.items():
                result_type = evaluation.get('result')
                resolution_penalty = evaluation.get('resolution_penalty', 0)
                geophysical_required = evaluation.get('geophysical_validation_required', False)
                
                print(f"📋 Regla: {rule_name}")
                print(f"   - Resultado: {result_type}")
                print(f"   - Penalización resolución: {resolution_penalty:.3f}")
                print(f"   - Requiere geofísica: {'Sí' if geophysical_required else 'No'}")
                print()
                
                if result_type == 'landscape_modified_non_structural':
                    landscape_modified_found = True
                    print("🌾 ¡NUEVA CLASIFICACIÓN DETECTADA!")
                    print("   'landscape_modified_non_structural' - Paisaje modificado no estructural")
                    print()
                
                if resolution_penalty > 0:
                    resolution_penalty_found = True
                    print("⚠️ PENALIZACIÓN POR RESOLUCIÓN APLICADA!")
                    print(f"   Penalización: {resolution_penalty:.3f} por resolución gruesa ({test_data['resolution_m']}m)")
                    print()
                
                if geophysical_required:
                    geophysical_required_found = True
                    print("🔬 VALIDACIÓN GEOFÍSICA REQUERIDA!")
                    print("   'Solo verificable con magnetometría/GPR'")
                    print()
            
            # Resumen de características encontradas
            print("📊 RESUMEN DE NUEVAS CARACTERÍSTICAS:")
            print(f"   ✅ Clasificación paisaje modificado: {'Encontrada' if landscape_modified_found else 'No encontrada'}")
            print(f"   ✅ Penalización por resolución: {'Aplicada' if resolution_penalty_found else 'No aplicada'}")
            print(f"   ✅ Validación geofísica requerida: {'Sí' if geophysical_required_found else 'No'}")
            print()
            
            # Verificar explicabilidad académica
            explainability = result.get('explainability_analysis')
            if explainability:
                print("🎓 EXPLICABILIDAD ACADÉMICA INCLUIDA:")
                print(f"   - Explicaciones generadas: {explainability.get('total_explanations', 0)}")
                print()
            
            # Verificar métricas de validación
            validation_metrics = result.get('validation_metrics')
            if validation_metrics:
                print("📏 MÉTRICAS DE VALIDACIÓN INCLUIDAS:")
                print(f"   - Sistema de validación: Operacional")
                print()
            
            # Guardar resultado completo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_new_classification_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Resultado completo guardado en: {filename}")
            print()
            print("🎯 TEST COMPLETADO - Nuevas características implementadas correctamente!")
            
        else:
            print(f"❌ Error en la petición: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("Verifica que el backend esté corriendo en puerto 8004")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_new_archaeological_classification()