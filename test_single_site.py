#!/usr/bin/env python3
"""
Test simple de un sitio arqueológico para verificar funcionamiento.
"""

import requests
import json
import time

def test_nazca_lines():
    """Probar análisis de las Líneas de Nazca."""
    
    base_url = "http://localhost:8003"
    
    print("🏛️  ARCHEOSCOPE - PRUEBA DE NAZCA LINES")
    print("=" * 50)
    
    # Verificar sistema
    print("🔍 Verificando sistema...")
    try:
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code != 200:
            print(f"❌ Sistema no disponible: {response.status_code}")
            return False
        
        status = response.json()
        print(f"✅ Backend: {status['backend_status']}")
        print(f"✅ IA: {status['ai_status']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Análisis de Nazca
    print(f"\n🏛️  ANALIZANDO: Nazca Lines")
    print("-" * 40)
    
    analysis_request = {
        "lat_min": -14.8,
        "lat_max": -14.6, 
        "lon_min": -75.2,
        "lon_max": -75.0,
        "region_name": "Nazca Lines Test",
        "resolution_m": 1000,
        "include_explainability": False,  # Sin explicabilidad para ser más rápido
        "include_validation_metrics": False
    }
    
    print(f"📍 Coordenadas: ({analysis_request['lat_min']}, {analysis_request['lon_min']}) - ({analysis_request['lat_max']}, {analysis_request['lon_max']})")
    print("⏳ Ejecutando análisis...")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/analyze",
            json=analysis_request,
            timeout=120  # Aumentar timeout a 2 minutos
        )
        
        analysis_time = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ Error en análisis: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}...")
            return False
        
        result = response.json()
        
        # Mostrar resultados
        print(f"\n📊 RESULTADOS:")
        print(f"⏱️  Tiempo: {analysis_time:.1f}s")
        print(f"📏 Área: {result['region_info']['area_km2']:.1f} km²")
        
        # Anomalías
        anomaly_map = result.get('anomaly_map', {})
        stats = anomaly_map.get('statistics', {})
        
        print(f"\n🎯 DETECCIÓN:")
        print(f"   🔴 Firmas arqueológicas: {stats.get('archaeological_signature_percentage', 0):.1f}%")
        print(f"   🟡 Anomalías espaciales: {stats.get('spatial_anomaly_percentage', 0):.1f}%")
        print(f"   🟢 Procesos naturales: {stats.get('natural_percentage', 0):.1f}%")
        
        # Reglas
        physics_results = result.get('physics_results', {})
        evaluations = physics_results.get('evaluations', {})
        
        print(f"\n🧪 REGLAS ARQUEOLÓGICAS:")
        for rule_name, evaluation in evaluations.items():
            prob = evaluation.get('archaeological_probability', 0)
            result_type = evaluation.get('result', 'unknown')
            print(f"   {rule_name}: {result_type} (prob: {prob:.2f})")
        
        # IA
        ai_explanations = result.get('ai_explanations', {})
        ai_available = ai_explanations.get('ai_available', False)
        
        print(f"\n🤖 IA: {'Disponible' if ai_available else 'No disponible'}")
        if ai_available:
            interpretation = ai_explanations.get('archaeological_interpretation', '')
            if interpretation and interpretation != 'No disponible':
                print(f"   Interpretación: {interpretation[:100]}...")
        
        # Evaluación
        archaeological_sig = stats.get('archaeological_signature_percentage', 0)
        spatial_anomalies = stats.get('spatial_anomaly_percentage', 0)
        
        total_score = archaeological_sig * 3 + spatial_anomalies * 1.5
        
        print(f"\n⭐ EVALUACIÓN:")
        print(f"   Puntuación: {total_score:.1f}/100")
        
        if total_score > 50:
            print(f"   ✅ BUENA DETECCIÓN - Nazca muestra firmas arqueológicas significativas")
        elif total_score > 20:
            print(f"   🟡 DETECCIÓN MODERADA - Algunas anomalías detectadas")
        else:
            print(f"   ❌ DETECCIÓN BAJA - Pocas anomalías arqueológicas")
        
        return True
        
    except Exception as e:
        analysis_time = time.time() - start_time
        print(f"❌ Error durante análisis: {e}")
        print(f"⏱️  Tiempo transcurrido: {analysis_time:.1f}s")
        return False

if __name__ == "__main__":
    success = test_nazca_lines()
    if success:
        print(f"\n🎉 PRUEBA EXITOSA")
    else:
        print(f"\n⚠️  PRUEBA FALLIDA")