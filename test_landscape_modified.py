#!/usr/bin/env python3
"""
Test específico para activar la nueva clasificación "landscape_modified_non_structural"
y las penalizaciones por resolución.
"""

import requests
import json
from datetime import datetime

def test_landscape_modified_classification():
    """Test específico para la nueva clasificación."""
    
    # Datos diseñados para activar la nueva clasificación
    test_data = {
        "lat_min": 41.8500,
        "lat_max": 41.8600,
        "lon_min": 12.5000,
        "lon_max": 12.5100,
        "resolution_m": 1000,  # Resolución muy gruesa para activar penalización
        "region_name": "Test Paisaje Modificado - Resolución Gruesa",
        "include_explainability": True,
        "include_validation_metrics": True,
        "layers_to_analyze": [
            "ndvi_vegetation", "thermal_lst", "sar_backscatter", 
            "surface_roughness", "soil_salinity", "seismic_resonance"
        ],
        "active_rules": ["all"]
    }
    
    print("🌾 Probando clasificación 'Paisaje Modificado No Estructural'...")
    print(f"📍 Región: {test_data['region_name']}")
    print(f"🔍 Resolución: {test_data['resolution_m']}m (muy gruesa para penalización)")
    print()
    
    try:
        response = requests.post(
            "http://localhost:8004/analyze",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Análisis completado exitosamente!")
            print()
            
            # Analizar resultados detalladamente
            physics_results = result.get('physics_results', {})
            evaluations = physics_results.get('evaluations', {})
            
            print("🔍 ANÁLISIS DETALLADO DE CLASIFICACIONES:")
            print()
            
            features_found = {
                'landscape_modified': False,
                'resolution_penalty': False,
                'geophysical_required': False,
                'high_archaeological_prob': False
            }
            
            for rule_name, evaluation in evaluations.items():
                result_type = evaluation.get('result')
                archaeological_prob = evaluation.get('archaeological_probability', 0)
                resolution_penalty = evaluation.get('resolution_penalty', 0)
                geophysical_required = evaluation.get('geophysical_validation_required', False)
                confidence = evaluation.get('confidence', 0)
                
                print(f"📋 Regla: {rule_name}")
                print(f"   🎯 Resultado: {result_type}")
                print(f"   📊 Probabilidad arqueológica: {archaeological_prob:.3f}")
                print(f"   ⚠️ Penalización resolución: {resolution_penalty:.3f}")
                print(f"   🔬 Requiere geofísica: {'Sí' if geophysical_required else 'No'}")
                print(f"   🎚️ Confianza: {confidence:.3f}")
                
                # Mostrar detalles de evidencia
                evidence = evaluation.get('evidence_details', {})
                if evidence:
                    print(f"   📝 Evidencia:")
                    for key, value in evidence.items():
                        if isinstance(value, (int, float)):
                            print(f"      - {key}: {value:.3f}")
                        else:
                            print(f"      - {key}: {value}")
                
                print()
                
                # Verificar características específicas
                if result_type == 'landscape_modified_non_structural':
                    features_found['landscape_modified'] = True
                    print("🌾 ¡CLASIFICACIÓN PAISAJE MODIFICADO DETECTADA!")
                    print("   Esta es la nueva clasificación intermedia entre natural y arqueológico")
                    print()
                
                if resolution_penalty > 0:
                    features_found['resolution_penalty'] = True
                    print("⚠️ ¡PENALIZACIÓN POR RESOLUCIÓN APLICADA!")
                    print(f"   Penalización: {resolution_penalty:.3f}")
                    print(f"   Razón: Resolución {test_data['resolution_m']}m es muy gruesa")
                    print()
                
                if geophysical_required:
                    features_found['geophysical_required'] = True
                    print("🔬 ¡VALIDACIÓN GEOFÍSICA REQUERIDA!")
                    print("   Etiqueta: 'Solo verificable con magnetometría/GPR'")
                    print()
                
                if archaeological_prob > 0.5:
                    features_found['high_archaeological_prob'] = True
                    print("📈 ¡ALTA PROBABILIDAD ARQUEOLÓGICA!")
                    print(f"   Probabilidad: {archaeological_prob:.3f}")
                    print()
            
            # Resumen final
            print("=" * 60)
            print("📊 RESUMEN DE NUEVAS CARACTERÍSTICAS IMPLEMENTADAS:")
            print("=" * 60)
            
            for feature, found in features_found.items():
                status = "✅ ENCONTRADA" if found else "❌ No encontrada"
                feature_names = {
                    'landscape_modified': 'Clasificación Paisaje Modificado No Estructural',
                    'resolution_penalty': 'Penalización por Resolución Gruesa',
                    'geophysical_required': 'Validación Geofísica Requerida',
                    'high_archaeological_prob': 'Alta Probabilidad Arqueológica'
                }
                print(f"   {feature_names[feature]}: {status}")
            
            print()
            
            # Verificar análisis integrado
            integrated_analysis = physics_results.get('integrated_assessment', {})
            if integrated_analysis:
                print("🔗 ANÁLISIS INTEGRADO:")
                classification = integrated_analysis.get('classification', 'unknown')
                probability = integrated_analysis.get('integrated_probability', 0)
                print(f"   Clasificación final: {classification}")
                print(f"   Probabilidad integrada: {probability:.3f}")
                print()
            
            # Guardar resultado
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_landscape_modified_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Resultado completo guardado en: {filename}")
            print()
            
            if any(features_found.values()):
                print("🎉 ¡ÉXITO! Nuevas características arqueológicas funcionando correctamente")
            else:
                print("⚠️ Las nuevas características no se activaron con estos datos")
                print("   Esto puede ser normal si los datos no cumplen los criterios específicos")
            
        else:
            print(f"❌ Error en la petición: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("Verifica que el backend esté corriendo en puerto 8004")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_landscape_modified_classification()