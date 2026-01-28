#!/usr/bin/env python3
"""
Test del Sistema de Validación IA - ArcheoScope

Este script demuestra la nueva funcionalidad de validación IA implementada:

Arquitectura GANADORA:
Instrumentos + Algoritmos → detección de anomalías → features numéricas → 
IA (assistant) → score final + explicación

El assistant:
- NO ve píxeles
- NO detecta geometrías  
- SÍ razona sobre resultados
- SÍ detecta inconsistencias lógicas
- SÍ justifica decisiones
- SÍ audita falsos positivos
"""

import requests
import json
import time
from typing import Dict, Any, List

def test_ai_validation_status():
    """Test del estado del sistema de validación IA."""
    
    print("🔍 TEST 1: Estado del Sistema de Validación IA")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:8002/ai-validation/status", timeout=10)
        
        if response.status_code == 200:
            status = response.json()
            
            print("✅ Sistema de validación IA:")
            print(f"   - AI Validator disponible: {'✅' if status['ai_validator_available'] else '❌'}")
            print(f"   - Core Detector disponible: {'✅' if status['core_detector_available'] else '❌'}")
            print(f"   - Assistant arqueológico: {'✅' if status['archaeological_assistant_available'] else '❌'}")
            print(f"   - Estado integración: {status['integration_status']}")
            
            print("\n🎯 Capacidades disponibles:")
            for capability, available in status['capabilities'].items():
                print(f"   - {capability}: {'✅' if available else '❌'}")
            
            print(f"\n⚙️ Configuración:")
            print(f"   - Umbral validación: {status['configuration']['validation_threshold']}")
            print(f"   - Umbral inconsistencias: {status['configuration']['inconsistency_threshold']}")
            
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return False

def test_single_ai_validation():
    """Test de análisis individual con validación IA."""
    
    print("\n🔍 TEST 2: Análisis Individual con Validación IA")
    print("=" * 60)
    
    # Coordenadas de Giza (sitio conocido)
    test_data = {
        "lat_min": 29.97,
        "lat_max": 29.99,
        "lon_min": 31.12,
        "lon_max": 31.14,
        "region_name": "Giza Pyramids - AI Validation Test",
        "include_explanation": True,
        "include_quality_metrics": True
    }
    
    try:
        print(f"📍 Analizando: {test_data['region_name']}")
        print(f"   Coordenadas: {test_data['lat_min']:.3f}-{test_data['lat_max']:.3f}, {test_data['lon_min']:.3f}-{test_data['lon_max']:.3f}")
        
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8002/ai-validation/analyze",
            json=test_data,
            timeout=60
        )
        
        analysis_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Análisis completado en {analysis_time:.2f}s")
            print(f"\n📊 RESULTADOS:")
            print(f"   - Score original: {result['original_score']:.3f}")
            print(f"   - Score final: {result['final_score']:.3f}")
            print(f"   - Ajuste IA: {result['score_adjustment']:+.3f}")
            print(f"   - IA disponible: {'✅' if result['ai_available'] else '❌'}")
            
            if result['ai_available']:
                print(f"   - IA coherente: {'✅' if result['ai_coherent'] else '❌'}")
                print(f"   - Confianza IA: {result['ai_confidence']:.3f}")
                print(f"   - Riesgo falso positivo: {result['false_positive_risk']:.3f}")
            
            print(f"   - Nivel de calidad: {result['quality_level']}")
            
            print(f"\n🤖 EXPLICACIÓN INTEGRADA:")
            explanation_lines = result['integrated_explanation'].split('\n')
            for line in explanation_lines[:10]:  # Primeras 10 líneas
                print(f"   {line}")
            if len(explanation_lines) > 10:
                print(f"   ... ({len(explanation_lines) - 10} líneas más)")
            
            print(f"\n💡 RECOMENDACIONES:")
            for i, rec in enumerate(result['recommendations'][:5], 1):
                print(f"   {i}. {rec}")
            
            # Guardar resultado detallado
            with open(f"ai_validation_test_{int(time.time())}.json", 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        return False

def test_batch_ai_validation():
    """Test de análisis en lote con validación IA."""
    
    print("\n🔍 TEST 3: Análisis en Lote con Validación IA")
    print("=" * 60)
    
    # Múltiples sitios para comparar
    test_regions = [
        {
            "lat": 29.98, "lon": 31.13,
            "lat_min": 29.97, "lat_max": 29.99,
            "lon_min": 31.12, "lon_max": 31.14,
            "name": "Giza Pyramids"
        },
        {
            "lat": 13.41, "lon": 103.87,
            "lat_min": 13.40, "lat_max": 13.42,
            "lon_min": 103.86, "lon_max": 103.88,
            "name": "Angkor Wat"
        },
        {
            "lat": 30.33, "lon": 35.44,
            "lat_min": 30.32, "lat_max": 30.34,
            "lon_min": 35.43, "lon_max": 35.45,
            "name": "Petra"
        }
    ]
    
    batch_data = {
        "regions": test_regions,
        "context": {
            "batch_id": "ai_validation_test_batch",
            "test_purpose": "Demostrar validación IA en lote"
        }
    }
    
    try:
        print(f"📍 Analizando {len(test_regions)} regiones en lote:")
        for region in test_regions:
            print(f"   - {region['name']}")
        
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8002/ai-validation/batch-analyze",
            json=batch_data,
            timeout=120
        )
        
        analysis_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Análisis en lote completado en {analysis_time:.2f}s")
            
            # Resumen del lote
            summary = result['summary']
            print(f"\n📊 RESUMEN DEL LOTE:")
            print(f"   - Total análisis: {summary['summary']['total_analyses']}")
            print(f"   - Validados por IA: {summary['summary']['ai_validated']}")
            print(f"   - Tasa validación IA: {summary['summary']['ai_validation_rate']:.1%}")
            print(f"   - Análisis coherentes: {summary['summary']['coherent_analyses']}")
            print(f"   - Tasa coherencia: {summary['summary']['coherence_rate']:.1%}")
            
            print(f"\n🎯 SCORING:")
            scoring = summary['scoring']
            print(f"   - Score promedio original: {scoring['average_original_score']:.3f}")
            print(f"   - Score promedio final: {scoring['average_final_score']:.3f}")
            print(f"   - Ajuste promedio: {scoring['average_adjustment']:+.3f}")
            print(f"   - Mejora de score: {'✅' if scoring['score_improvement'] else '❌'}")
            
            print(f"\n🏆 DISTRIBUCIÓN DE CALIDAD:")
            quality_dist = summary['quality_distribution']
            for quality, count in quality_dist.items():
                print(f"   - {quality}: {count}")
            
            # Resultados individuales
            print(f"\n📋 RESULTADOS INDIVIDUALES:")
            for i, res in enumerate(result['results'], 1):
                print(f"   {i}. {res['region_name']}:")
                print(f"      Score: {res['original_score']:.3f} → {res['final_score']:.3f} ({res['score_adjustment']:+.3f})")
                print(f"      IA: {'✅' if res['ai_coherent'] else '❌'} | Calidad: {res['quality_level']}")
            
            # Guardar resultado detallado
            with open(f"ai_validation_batch_test_{int(time.time())}.json", 'w') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en análisis en lote: {e}")
        return False

def test_validation_report():
    """Test del reporte de validación IA."""
    
    print("\n🔍 TEST 4: Reporte de Validación IA")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:8002/ai-validation/validation-report", timeout=10)
        
        if response.status_code == 200:
            report = response.json()
            
            print("✅ Reporte de validación generado:")
            
            print(f"\n🖥️ ESTADO DEL SISTEMA:")
            system_status = report['system_status']
            for key, value in system_status.items():
                print(f"   - {key}: {'✅' if value else '❌'}")
            
            print(f"\n⚙️ CONFIGURACIÓN:")
            config = report['configuration']
            for key, value in config.items():
                print(f"   - {key}: {value}")
            
            print(f"\n🎯 CAPACIDADES:")
            capabilities = report['capabilities']
            for capability, available in capabilities.items():
                print(f"   - {capability}: {'✅' if available else '❌'}")
            
            print(f"\n💡 RECOMENDACIONES:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"   {i}. {rec}")
            
            print(f"\n📖 INSTRUCCIONES DE USO:")
            usage = report['usage_instructions']
            for endpoint, description in usage.items():
                print(f"   - {endpoint}: {description}")
            
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error obteniendo reporte: {e}")
        return False

def test_examples_endpoint():
    """Test del endpoint de ejemplos."""
    
    print("\n🔍 TEST 5: Ejemplos de Uso")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:8002/ai-validation/examples", timeout=10)
        
        if response.status_code == 200:
            examples = response.json()
            
            print("✅ Ejemplos de uso obtenidos:")
            
            print(f"\n📝 EJEMPLO ANÁLISIS INDIVIDUAL:")
            single_example = examples['single_analysis_example']
            print(f"   Endpoint: {single_example['endpoint']}")
            print(f"   Descripción: {single_example['description']}")
            
            print(f"\n📝 EJEMPLO ANÁLISIS EN LOTE:")
            batch_example = examples['batch_analysis_example']
            print(f"   Endpoint: {batch_example['endpoint']}")
            print(f"   Descripción: {batch_example['description']}")
            
            print(f"\n📖 GUÍA DE INTERPRETACIÓN:")
            guide = examples['interpretation_guide']
            
            print(f"   Interpretación de scores:")
            for field, description in guide['score_interpretation'].items():
                print(f"     - {field}: {description}")
            
            print(f"   Niveles de calidad:")
            for level, description in guide['quality_levels'].items():
                print(f"     - {level}: {description}")
            
            return True
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error obteniendo ejemplos: {e}")
        return False

def main():
    """Ejecutar todos los tests del sistema de validación IA."""
    
    print("🧠 SISTEMA DE VALIDACIÓN IA - ARCHEOSCOPE")
    print("=" * 80)
    print("Arquitectura GANADORA:")
    print("Instrumentos + Algoritmos → detección → features → IA → score + explicación")
    print("=" * 80)
    
    # Verificar que el backend esté corriendo
    try:
        response = requests.get("http://localhost:8002/status", timeout=5)
        if response.status_code != 200:
            print("❌ Backend no está corriendo en http://localhost:8002")
            print("   Ejecuta: python run_archeoscope.py")
            return
    except:
        print("❌ No se puede conectar al backend")
        print("   Ejecuta: python run_archeoscope.py")
        return
    
    # Ejecutar tests
    tests = [
        ("Estado del Sistema", test_ai_validation_status),
        ("Análisis Individual", test_single_ai_validation),
        ("Análisis en Lote", test_batch_ai_validation),
        ("Reporte de Validación", test_validation_report),
        ("Ejemplos de Uso", test_examples_endpoint)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error en test {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE TESTS")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} tests exitosos ({passed/total:.1%})")
    
    if passed == total:
        print("🎉 ¡SISTEMA DE VALIDACIÓN IA FUNCIONANDO PERFECTAMENTE!")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Integrar con frontend para UI de validación IA")
        print("   2. Configurar alertas para inconsistencias detectadas")
        print("   3. Implementar métricas de rendimiento en tiempo real")
        print("   4. Añadir validación IA a pipeline de producción")
    else:
        print("⚠️ Algunos tests fallaron - revisar configuración")
        print("\n🔧 POSIBLES SOLUCIONES:")
        print("   1. Verificar que OPENROUTER_API_KEY esté configurada")
        print("   2. Verificar que Ollama esté corriendo (alternativa)")
        print("   3. Revisar logs del backend para errores específicos")

if __name__ == "__main__":
    main()