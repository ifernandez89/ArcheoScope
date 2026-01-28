#!/usr/bin/env python3
"""
Pruebas específicas de las interpretaciones arqueológicas de IA en ArcheoScope.
Evalúa la calidad y precisión de las explicaciones generadas por phi4-mini-reasoning.
"""

import requests
import json
import time
from datetime import datetime

def test_ai_archaeological_interpretations():
    """Probar interpretaciones arqueológicas de IA en diferentes sitios."""
    
    base_url = "http://localhost:8003"
    
    # Sitios con características arqueológicas específicas para evaluar IA
    test_sites = {
        "nazca_geoglyphs": {
            "name": "Nazca - Zona de Geoglifos",
            "lat_min": -14.75, "lat_max": -14.70,
            "lon_min": -75.15, "lon_max": -75.10,
            "expected_features": ["geometric patterns", "linear structures", "ancient roads"],
            "archaeological_context": "Famous for large-scale geoglyphs and lines visible from aerial view",
            "test_focus": "geometric pattern recognition"
        },
        "machu_picchu_terraces": {
            "name": "Machu Picchu - Terrazas Agrícolas", 
            "lat_min": -13.17, "lat_max": -13.16,
            "lon_min": -72.57, "lon_max": -72.56,
            "expected_features": ["agricultural terraces", "stone structures", "water management"],
            "archaeological_context": "Inca agricultural terraces and urban planning",
            "test_focus": "terrace and structure detection"
        },
        "caral_pyramids": {
            "name": "Caral - Complejo Piramidal",
            "lat_min": -10.90, "lat_max": -10.89,
            "lon_min": -77.52, "lon_max": -77.51,
            "expected_features": ["pyramidal structures", "ceremonial plazas", "urban layout"],
            "archaeological_context": "Ancient Caral civilization with monumental architecture",
            "test_focus": "monumental architecture detection"
        }
    }
    
    print("🤖 ARCHEOSCOPE - EVALUACIÓN DE IA ARQUEOLÓGICA")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Modelo: phi4-mini-reasoning")
    print(f"🧠 Sitios para evaluar IA: {len(test_sites)}")
    
    # Verificar disponibilidad de IA
    print(f"\n🔍 Verificando disponibilidad de IA...")
    try:
        response = requests.get(f"{base_url}/status", timeout=10)
        if response.status_code != 200:
            print(f"❌ Sistema no disponible")
            return False
        
        status = response.json()
        ai_status = status.get('ai_status', 'unknown')
        print(f"✅ Estado de IA: {ai_status}")
        
        if ai_status != 'available':
            print(f"❌ IA no disponible para pruebas")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Probar interpretaciones de IA en cada sitio
    ai_results = []
    total_start = time.time()
    
    for site_key, site_data in test_sites.items():
        print(f"\n🏛️  EVALUANDO IA: {site_data['name']}")
        print("-" * 55)
        
        # Análisis con explicabilidad completa
        analysis_request = {
            "lat_min": site_data["lat_min"],
            "lat_max": site_data["lat_max"],
            "lon_min": site_data["lon_min"],
            "lon_max": site_data["lon_max"],
            "region_name": f"{site_data['name']} - AI Test",
            "resolution_m": 500,  # Alta resolución para mejor análisis
            "include_explainability": True,  # ¡Importante para IA!
            "include_validation_metrics": True
        }
        
        print(f"📍 Coordenadas: ({site_data['lat_min']:.3f}, {site_data['lon_min']:.3f}) - ({site_data['lat_max']:.3f}, {site_data['lon_max']:.3f})")
        print(f"🎯 Enfoque: {site_data['test_focus']}")
        print(f"🏺 Contexto: {site_data['archaeological_context']}")
        print("🤖 Ejecutando análisis con IA...")
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/analyze",
                json=analysis_request,
                timeout=180  # 3 minutos para análisis completo con IA
            )
            
            analysis_time = time.time() - start_time
            
            if response.status_code != 200:
                print(f"❌ Error en análisis: {response.status_code}")
                ai_results.append({
                    "site": site_key,
                    "name": site_data["name"],
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "time": analysis_time
                })
                continue
            
            result = response.json()
            
            # Extraer interpretaciones de IA
            ai_explanations = result.get("ai_explanations", {})
            explainability_analysis = result.get("explainability_analysis", {})
            
            # Verificar disponibilidad de IA
            ai_available = ai_explanations.get("ai_available", False)
            
            if not ai_available:
                print(f"❌ IA no disponible en este análisis")
                ai_results.append({
                    "site": site_key,
                    "name": site_data["name"],
                    "success": False,
                    "error": "IA no disponible",
                    "time": analysis_time
                })
                continue
            
            # Extraer interpretaciones
            explanation = ai_explanations.get("explanation", "")
            archaeological_interpretation = ai_explanations.get("archaeological_interpretation", "")
            confidence_notes = ai_explanations.get("confidence_notes", "")
            recommendations = ai_explanations.get("recommendations", [])
            limitations = ai_explanations.get("limitations", "")
            scientific_reasoning = ai_explanations.get("scientific_reasoning", "")
            
            # Mostrar resultados de IA
            print(f"⏱️  Tiempo de análisis: {analysis_time:.1f}s")
            print(f"🤖 IA disponible: ✅")
            
            print(f"\n📝 EXPLICACIÓN GENERAL:")
            if explanation:
                print(f"   {explanation[:150]}{'...' if len(explanation) > 150 else ''}")
            else:
                print(f"   No disponible")
            
            print(f"\n🏛️  INTERPRETACIÓN ARQUEOLÓGICA:")
            if archaeological_interpretation:
                print(f"   {archaeological_interpretation[:200]}{'...' if len(archaeological_interpretation) > 200 else ''}")
            else:
                print(f"   No disponible")
            
            print(f"\n🧠 RAZONAMIENTO CIENTÍFICO:")
            if scientific_reasoning:
                print(f"   {scientific_reasoning[:150]}{'...' if len(scientific_reasoning) > 150 else ''}")
            else:
                print(f"   No disponible")
            
            print(f"\n📊 EVALUACIÓN DE CONFIANZA:")
            if confidence_notes:
                print(f"   {confidence_notes[:100]}{'...' if len(confidence_notes) > 100 else ''}")
            else:
                print(f"   No disponible")
            
            print(f"\n🔬 RECOMENDACIONES:")
            if recommendations:
                for i, rec in enumerate(recommendations[:3], 1):  # Mostrar primeras 3
                    print(f"   {i}. {rec[:80]}{'...' if len(rec) > 80 else ''}")
            else:
                print(f"   No disponibles")
            
            print(f"\n⚠️  LIMITACIONES:")
            if limitations:
                print(f"   {limitations[:100]}{'...' if len(limitations) > 100 else ''}")
            else:
                print(f"   No especificadas")
            
            # Evaluar calidad de interpretación
            quality_score = evaluate_ai_interpretation_quality(
                explanation, archaeological_interpretation, scientific_reasoning,
                confidence_notes, recommendations, site_data
            )
            
            print(f"\n⭐ CALIDAD DE INTERPRETACIÓN IA:")
            print(f"   Puntuación: {quality_score:.1f}/100")
            
            if quality_score >= 80:
                quality_level = "EXCELENTE"
            elif quality_score >= 60:
                quality_level = "BUENA"
            elif quality_score >= 40:
                quality_level = "MODERADA"
            else:
                quality_level = "BAJA"
            
            print(f"   Nivel: {quality_level}")
            
            # Verificar explicabilidad adicional
            explainability_count = explainability_analysis.get("total_explanations", 0) if explainability_analysis else 0
            print(f"   Explicaciones detalladas: {explainability_count}")
            
            ai_results.append({
                "site": site_key,
                "name": site_data["name"],
                "success": True,
                "time": analysis_time,
                "ai_available": ai_available,
                "explanation": explanation,
                "archaeological_interpretation": archaeological_interpretation,
                "scientific_reasoning": scientific_reasoning,
                "confidence_notes": confidence_notes,
                "recommendations": recommendations,
                "limitations": limitations,
                "quality_score": quality_score,
                "quality_level": quality_level,
                "explainability_count": explainability_count,
                "expected_features": site_data["expected_features"],
                "test_focus": site_data["test_focus"]
            })
            
        except Exception as e:
            analysis_time = time.time() - start_time
            print(f"❌ Error durante análisis: {e}")
            ai_results.append({
                "site": site_key,
                "name": site_data["name"],
                "success": False,
                "error": str(e),
                "time": analysis_time
            })
        
        # Pausa entre análisis
        time.sleep(5)
    
    total_time = time.time() - total_start
    
    # Resumen de evaluación de IA
    print(f"\n🧠 RESUMEN DE EVALUACIÓN DE IA")
    print("=" * 55)
    
    successful = [r for r in ai_results if r["success"]]
    failed = [r for r in ai_results if not r["success"]]
    
    print(f"✅ Análisis exitosos: {len(successful)}/{len(ai_results)}")
    print(f"❌ Análisis fallidos: {len(failed)}")
    print(f"⏱️  Tiempo total: {total_time:.1f}s")
    
    if successful:
        avg_quality = sum(r["quality_score"] for r in successful) / len(successful)
        avg_time = sum(r["time"] for r in successful) / len(successful)
        total_explanations = sum(r["explainability_count"] for r in successful)
        
        print(f"📊 Calidad promedio de IA: {avg_quality:.1f}/100")
        print(f"⏱️  Tiempo promedio: {avg_time:.1f}s")
        print(f"📝 Total explicaciones generadas: {total_explanations}")
        
        print(f"\n📋 EVALUACIÓN POR SITIO:")
        for r in successful:
            print(f"   🏛️  {r['name']}: {r['quality_score']:.1f}/100 ({r['quality_level']})")
            print(f"      Enfoque: {r['test_focus']}")
            print(f"      Explicaciones: {r['explainability_count']}")
        
        # Evaluación general de IA
        if avg_quality >= 80:
            ai_evaluation = "🎉 EXCELENTE - IA arqueológica funciona muy bien"
        elif avg_quality >= 60:
            ai_evaluation = "👍 BUENA - IA proporciona interpretaciones útiles"
        elif avg_quality >= 40:
            ai_evaluation = "⚠️  MODERADA - IA requiere mejoras"
        else:
            ai_evaluation = "❌ BAJA - IA necesita desarrollo adicional"
        
        print(f"\n🎯 EVALUACIÓN GENERAL DE IA:")
        print(f"   {ai_evaluation}")
        print(f"   Modelo: phi4-mini-reasoning")
        print(f"   Disponibilidad: 100%")
        print(f"   Calidad interpretativa: {avg_quality:.1f}/100")
    
    if failed:
        print(f"\n❌ ANÁLISIS FALLIDOS:")
        for r in failed:
            print(f"   {r['name']}: {r.get('error', 'Error desconocido')}")
    
    # Guardar resultados de IA
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"archeoscope_ai_evaluation_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "model": "phi4-mini-reasoning",
            "total_time": total_time,
            "ai_results": ai_results,
            "summary": {
                "total_tests": len(ai_results),
                "successful": len(successful),
                "failed": len(failed),
                "average_quality": sum(r["quality_score"] for r in successful) / len(successful) if successful else 0,
                "average_time": sum(r["time"] for r in successful) / len(successful) if successful else 0,
                "total_explanations": sum(r["explainability_count"] for r in successful) if successful else 0
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Evaluación de IA guardada en: {filename}")
    
    return len(successful) == len(ai_results)

def evaluate_ai_interpretation_quality(explanation, archaeological_interpretation, 
                                     scientific_reasoning, confidence_notes, 
                                     recommendations, site_data):
    """Evaluar calidad de interpretación arqueológica de IA."""
    
    score = 0
    
    # Criterio 1: Completitud de explicación (25 puntos)
    if explanation and len(explanation) > 50:
        score += 25
    elif explanation and len(explanation) > 20:
        score += 15
    elif explanation:
        score += 5
    
    # Criterio 2: Interpretación arqueológica específica (30 puntos)
    if archaeological_interpretation and len(archaeological_interpretation) > 100:
        score += 30
        # Bonus por mencionar características esperadas
        expected_features = site_data.get("expected_features", [])
        for feature in expected_features:
            if any(word in archaeological_interpretation.lower() for word in feature.split()):
                score += 5  # Bonus por relevancia
                break
    elif archaeological_interpretation and len(archaeological_interpretation) > 50:
        score += 20
    elif archaeological_interpretation:
        score += 10
    
    # Criterio 3: Razonamiento científico (20 puntos)
    if scientific_reasoning and len(scientific_reasoning) > 50:
        score += 20
    elif scientific_reasoning and len(scientific_reasoning) > 20:
        score += 10
    elif scientific_reasoning:
        score += 5
    
    # Criterio 4: Evaluación de confianza (10 puntos)
    if confidence_notes and len(confidence_notes) > 20:
        score += 10
    elif confidence_notes:
        score += 5
    
    # Criterio 5: Recomendaciones útiles (10 puntos)
    if recommendations and len(recommendations) >= 3:
        score += 10
    elif recommendations and len(recommendations) >= 1:
        score += 5
    
    # Criterio 6: Reconocimiento de limitaciones (5 puntos)
    if "limitaciones" in str(confidence_notes).lower() or "requiere validación" in str(confidence_notes).lower():
        score += 5
    
    return min(score, 100)

if __name__ == "__main__":
    success = test_ai_archaeological_interpretations()
    if success:
        print(f"\n🎉 EVALUACIÓN DE IA COMPLETADA EXITOSAMENTE")
    else:
        print(f"\n⚠️  ALGUNAS EVALUACIONES DE IA FALLARON")