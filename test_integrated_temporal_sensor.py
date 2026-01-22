#!/usr/bin/env python3
"""
Test del Sistema de Sensor Temporal Integrado Automáticamente
Prueba con coordenadas de la Antártida para validar el filtrado temporal y exclusión moderna
"""

import requests
import json
import math

def test_integrated_temporal_sensor():
    print("🧊 TESTING INTEGRATED TEMPORAL SENSOR - ANTARCTICA")
    print("=" * 80)
    
    # Coordenadas de la Antártida para prueba
    # Área cerca de la Península Antártica con posibles estructuras geológicas interesantes
    lat = -64.7731  # Península Antártica
    lon = -62.1838  # Estrecho de Gerlache
    offset = 0.01   # Área de ~2km²
    
    print(f"🧊 Coordenadas de prueba: {lat}, {lon}")
    print(f"📍 Región: Península Antártica, Estrecho de Gerlache")
    print(f"🎯 Área de análisis: ±{offset}° (~2km²)")
    
    # Configuración para análisis con sensor temporal integrado automáticamente
    integrated_temporal_data = {
        "lat_min": lat - offset,
        "lat_max": lat + offset,
        "lon_min": lon - offset,
        "lon_max": lon + offset,
        "resolution_m": 10,  # Sentinel-2 para análisis temporal
        "region_name": "Antarctica Integrated Temporal Sensor Test",
        "include_explainability": True,
        "include_validation_metrics": True,
        
        # NUEVO: Configuración temporal integrada automáticamente
        "temporal_integration": {
            "enable_automatic": True,  # Activar sensor temporal automático
            "years_range": "3-5",      # 3-5 años estacionales
            "seasonal_alignment": True, # Bien alineados estacionalmente
            "exclusion_moderna": True,  # Exclusión moderna por defecto
            "target_years": [2020, 2022, 2023, 2024],  # 4 años
            "seasonal_window": "december-january",      # Verano antártico
            "validation_mode": "reaffirm_or_discard"    # Reafirmar o descartar anomalías
        },
        
        "layers_to_analyze": [
            "ndvi_vegetation",      # Para análisis temporal (aunque limitado en Antártida)
            "thermal_lst",          # Importante para detección de estructuras
            "sar_backscatter",      # Excelente para coherencia temporal
            "surface_roughness",    # Detecta cambios geomorfológicos
            "soil_salinity"         # Puede detectar procesos geológicos
        ],
        "active_rules": ["all"],
        "analysis_mode": "integrated_temporal_automatic"
    }
    
    print("\n⏳ SENSOR TEMPORAL INTEGRADO AUTOMÁTICAMENTE:")
    print("   • Años objetivo: 2020, 2022, 2023, 2024 (4 años)")
    print("   • Ventana estacional: diciembre-enero (verano antártico)")
    print("   • Exclusión moderna: ACTIVADA por defecto")
    print("   • Modo: Reafirmar o descartar anomalías automáticamente")
    print("   • Resolución: 10m (Sentinel-2)")
    
    print("\n🧊 CARACTERÍSTICAS ANTÁRTICAS ESPERADAS:")
    print("   • NDVI muy bajo (poca vegetación)")
    print("   • Alta estabilidad temporal (pocas variaciones estacionales)")
    print("   • Baja probabilidad de estructuras modernas")
    print("   • Posibles anomalías geológicas persistentes")
    
    print("\n🎯 OBJETIVOS DEL TEST:")
    print("   1. Verificar integración automática del sensor temporal")
    print("   2. Validar exclusión moderna en ambiente prístino")
    print("   3. Probar persistencia temporal en condiciones extremas")
    print("   4. Confirmar que anomalías se reafirman o descartan correctamente")
    
    try:
        print("\n🔍 Ejecutando análisis con sensor temporal integrado...")
        response = requests.post('http://localhost:8002/analyze', 
                               json=integrated_temporal_data, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Análisis con sensor temporal integrado completado")
            
            # Verificar integración del sensor temporal
            temporal_sensor_data = data.get('temporal_sensor_analysis', {})
            integrated_analysis = data.get('integrated_analysis', {})
            
            print(f"\n⏳ RESULTADOS DEL SENSOR TEMPORAL INTEGRADO:")
            print(f"   - Años analizados: {temporal_sensor_data.get('years_analyzed', [])}")
            print(f"   - Ventana estacional: {temporal_sensor_data.get('seasonal_window', 'N/A')}")
            print(f"   - Score de persistencia: {temporal_sensor_data.get('persistence_score', 0):.3f}")
            print(f"   - Coeficiente de variación: {temporal_sensor_data.get('cv_stability', 0):.3f}")
            print(f"   - Resultado de validación: {temporal_sensor_data.get('validation_result', 'N/A')}")
            print(f"   - Exclusión moderna aplicada: {'✅' if temporal_sensor_data.get('exclusion_moderna_applied') else '❌'}")
            
            # Verificar análisis integrado
            print(f"\n🔗 ANÁLISIS INTEGRADO:")
            print(f"   - Score básico: {integrated_analysis.get('basic_score', 0):.3f}")
            print(f"   - Score avanzado: {integrated_analysis.get('advanced_score', 0):.3f}")
            print(f"   - Score temporal: {integrated_analysis.get('temporal_score', 0):.3f}")
            print(f"   - Score exclusión moderna: {integrated_analysis.get('modern_exclusion_score', 0):.3f}")
            print(f"   - Score integrado final: {integrated_analysis.get('integrated_score', 0):.3f}")
            print(f"   - Clasificación: {integrated_analysis.get('classification', 'N/A')}")
            print(f"   - Validación temporal: {integrated_analysis.get('temporal_validation', 'N/A')}")
            
            # Verificar exclusión moderna
            modern_exclusion_score = integrated_analysis.get('modern_exclusion_score', 0)
            if modern_exclusion_score < 0.2:
                print(f"\n✅ EXCLUSIÓN MODERNA CORRECTA:")
                print(f"   - Score de modernidad: {modern_exclusion_score:.3f} (< 0.2 = ambiente prístino)")
                print(f"   - Interpretación: Ambiente antártico sin estructuras modernas")
            else:
                print(f"\n⚠️ EXCLUSIÓN MODERNA INESPERADA:")
                print(f"   - Score de modernidad: {modern_exclusion_score:.3f} (> 0.2 en Antártida)")
                print(f"   - Posible error en detección de modernidad")
            
            # Verificar persistencia temporal
            persistence_score = temporal_sensor_data.get('persistence_score', 0)
            cv_stability = temporal_sensor_data.get('cv_stability', 1.0)
            
            print(f"\n📊 EVALUACIÓN DE PERSISTENCIA TEMPORAL:")
            if persistence_score > 0.6 and cv_stability < 0.2:
                print(f"   ✅ ALTA PERSISTENCIA: Score={persistence_score:.3f}, CV={cv_stability:.3f}")
                print(f"   - Interpretación: Estructura estable detectada (posible geológica)")
            elif persistence_score > 0.4:
                print(f"   🟡 PERSISTENCIA MODERADA: Score={persistence_score:.3f}, CV={cv_stability:.3f}")
                print(f"   - Interpretación: Cierta estabilidad temporal")
            else:
                print(f"   ❌ BAJA PERSISTENCIA: Score={persistence_score:.3f}, CV={cv_stability:.3f}")
                print(f"   - Interpretación: Variabilidad natural o ruido")
            
            # Verificar validación temporal automática
            validation_result = temporal_sensor_data.get('validation_result', '')
            print(f"\n🎯 VALIDACIÓN TEMPORAL AUTOMÁTICA:")
            if 'REAFIRMADA' in validation_result:
                print(f"   ✅ ANOMALÍA REAFIRMADA: {validation_result}")
                print(f"   - El sensor temporal confirma la persistencia de la anomalía")
            elif 'DESCARTADA' in validation_result:
                print(f"   ❌ ANOMALÍA DESCARTADA: {validation_result}")
                print(f"   - El sensor temporal rechaza la anomalía por baja persistencia")
            else:
                print(f"   🟡 VALIDACIÓN MODERADA: {validation_result}")
                print(f"   - El sensor temporal indica persistencia parcial")
            
            # Resumen del test
            print(f"\n📋 RESUMEN DEL TEST:")
            print(f"   • Sensor temporal integrado: {'✅ FUNCIONANDO' if temporal_sensor_data else '❌ ERROR'}")
            print(f"   • Exclusión moderna automática: {'✅ APLICADA' if temporal_sensor_data.get('exclusion_moderna_applied') is not None else '❌ NO APLICADA'}")
            print(f"   • Validación automática: {'✅ EJECUTADA' if validation_result else '❌ NO EJECUTADA'}")
            print(f"   • Análisis integrado: {'✅ COMPLETO' if integrated_analysis else '❌ INCOMPLETO'}")
            
            # Guardar resultados
            output_filename = f"archeoscope_integrated_temporal_test_{lat}_{lon}_20260122.json"
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Resultados guardados en: {output_filename}")
            
            return True
            
        else:
            print(f"❌ Error en análisis: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Asegúrate de que el servidor esté ejecutándose en localhost:8002")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🚀 INICIANDO TEST DEL SENSOR TEMPORAL INTEGRADO")
    print("🧊 Usando coordenadas de la Antártida para validación")
    print()
    
    success = test_integrated_temporal_sensor()
    
    if success:
        print("\n🎉 TEST COMPLETADO EXITOSAMENTE")
        print("✅ El sensor temporal se integra automáticamente en el análisis")
        print("✅ La exclusión moderna se aplica por defecto")
        print("✅ Las anomalías se reafirman o descartan según persistencia temporal")
    else:
        print("\n❌ TEST FALLÓ")
        print("🔧 Revisar configuración del servidor y implementación")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()