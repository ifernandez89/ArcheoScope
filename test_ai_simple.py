#!/usr/bin/env python3
"""
Test simple de IA arqueológica sin explicabilidad completa.
"""

import requests
import json
import time

def test_ai_simple():
    """Probar IA arqueológica de forma simple."""
    
    base_url = "http://localhost:8003"
    
    print("🤖 ARCHEOSCOPE - PRUEBA SIMPLE DE IA ARQUEOLÓGICA")
    print("=" * 55)
    
    # Verificar IA
    print("🔍 Verificando IA...")
    try:
        response = requests.get(f"{base_url}/status", timeout=10)
        if response.status_code != 200:
            print(f"❌ Sistema no disponible")
            return False
        
        status = response.json()
        ai_status = status.get('ai_status', 'unknown')
        print(f"✅ Estado de IA: {ai_status}")
        
        if ai_status != 'available':
            print(f"❌ IA no disponible")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test con Nazca (sin explicabilidad para evitar errores)
    print(f"\n🏛️  PROBANDO IA: Nazca Lines")
    print("-" * 40)
    
    analysis_request = {
        "lat_min": -14.75,
        "lat_max": -14.70,
        "lon_min": -75.15,
        "lon_max": -75.10,
        "region_name": "Nazca IA Test",
        "resolution_m": 1000,
        "include_explainability": False,  # Sin explicabilidad
        "include_validation_metrics": False
    }
    
    print("🤖 Ejecutando análisis con IA...")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/analyze",
            json=analysis_request,
            timeout=120
        )
        
        analysis_time = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            return False
        
        result = response.json()
        
        # Extraer interpretaciones de IA
        ai_explanations = result.get("ai_explanations", {})
        
        print(f"⏱️  Tiempo: {analysis_time:.1f}s")
        
        # Verificar IA
        ai_available = ai_explanations.get("ai_available", False)
        print(f"🤖 IA disponible: {'✅' if ai_available else '❌'}")
        
        if not ai_available:
            print(f"❌ IA no funcionó en este análisis")
            return False
        
        # Mostrar interpretaciones
        explanation = ai_explanations.get("explanation", "")
        archaeological_interpretation = ai_explanations.get("archaeological_interpretation", "")
        confidence_notes = ai_explanations.get("confidence_notes", "")
        recommendations = ai_explanations.get("recommendations", [])
        limitations = ai_explanations.get("limitations", "")
        scientific_reasoning = ai_explanations.get("scientific_reasoning", "")
        
        print(f"\n📝 EXPLICACIÓN GENERAL:")
        if explanation:
            print(f"   {explanation[:200]}{'...' if len(explanation) > 200 else ''}")
        else:
            print(f"   No disponible")
        
        print(f"\n🏛️  INTERPRETACIÓN ARQUEOLÓGICA:")
        if archaeological_interpretation:
            print(f"   {archaeological_interpretation[:250]}{'...' if len(archaeological_interpretation) > 250 else ''}")
        else:
            print(f"   No disponible")
        
        print(f"\n🧠 RAZONAMIENTO CIENTÍFICO:")
        if scientific_reasoning:
            print(f"   {scientific_reasoning[:200]}{'...' if len(scientific_reasoning) > 200 else ''}")
        else:
            print(f"   No disponible")
        
        print(f"\n📊 EVALUACIÓN DE CONFIANZA:")
        if confidence_notes:
            print(f"   {confidence_notes[:150]}{'...' if len(confidence_notes) > 150 else ''}")
        else:
            print(f"   No disponible")
        
        print(f"\n🔬 RECOMENDACIONES:")
        if recommendations:
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec[:100]}{'...' if len(rec) > 100 else ''}")
        else:
            print(f"   No disponibles")
        
        # Evaluar calidad
        quality_score = 0
        
        if explanation and len(explanation) > 50:
            quality_score += 25
        if archaeological_interpretation and len(archaeological_interpretation) > 100:
            quality_score += 30
        if scientific_reasoning and len(scientific_reasoning) > 50:
            quality_score += 20
        if confidence_notes and len(confidence_notes) > 20:
            quality_score += 10
        if recommendations and len(recommendations) >= 3:
            quality_score += 10
        if "nazca" in archaeological_interpretation.lower() or "geoglifo" in archaeological_interpretation.lower():
            quality_score += 5  # Bonus por relevancia
        
        print(f"\n⭐ EVALUACIÓN DE CALIDAD IA:")
        print(f"   Puntuación: {quality_score}/100")
        
        if quality_score >= 80:
            quality_level = "EXCELENTE"
        elif quality_score >= 60:
            quality_level = "BUENA"
        elif quality_score >= 40:
            quality_level = "MODERADA"
        else:
            quality_level = "BAJA"
        
        print(f"   Nivel: {quality_level}")
        
        # Verificar que la IA mencione conceptos arqueológicos relevantes
        archaeological_terms = ["arqueológico", "estructura", "patrón", "intervención", "humana", "antigua", "geoglifo", "línea"]
        terms_found = sum(1 for term in archaeological_terms if term in str(archaeological_interpretation).lower())
        
        print(f"   Términos arqueológicos relevantes: {terms_found}/{len(archaeological_terms)}")
        
        if quality_score >= 50 and terms_found >= 3:
            print(f"\n✅ IA ARQUEOLÓGICA FUNCIONA CORRECTAMENTE")
            print(f"   - Genera interpretaciones relevantes")
            print(f"   - Usa terminología arqueológica apropiada")
            print(f"   - Proporciona razonamiento científico")
            return True
        else:
            print(f"\n⚠️  IA ARQUEOLÓGICA NECESITA MEJORAS")
            print(f"   - Calidad: {quality_level}")
            print(f"   - Relevancia arqueológica limitada")
            return False
        
    except Exception as e:
        analysis_time = time.time() - start_time
        print(f"❌ Error: {e}")
        print(f"⏱️  Tiempo: {analysis_time:.1f}s")
        return False

if __name__ == "__main__":
    success = test_ai_simple()
    if success:
        print(f"\n🎉 IA ARQUEOLÓGICA FUNCIONANDO CORRECTAMENTE")
    else:
        print(f"\n⚠️  IA ARQUEOLÓGICA REQUIERE ATENCIÓN")