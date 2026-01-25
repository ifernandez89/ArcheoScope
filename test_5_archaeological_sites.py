#!/usr/bin/env python3
"""
Test de 5 Sitios Arqueológicos Diversos
========================================

Prueba el sistema ArcheoScope con 5 sitios arqueológicos reales
de diferentes ambientes y épocas.
"""

import requests
import json
from datetime import datetime
from typing import Dict, Any

API_BASE_URL = "http://localhost:8002"

# 5 SITIOS ARQUEOLÓGICOS DE PRUEBA
TEST_SITES = {
    "giza": {
        "name": "Giza Pyramids Complex",
        "environment": "desert",
        "coordinates": {"lat": 29.9792, "lon": 31.1342},
        "country": "Egypt",
        "period": "Old Kingdom (2580-2560 BCE)",
        "expected_detection": True,
        "notes": "Pirámides masivas - debería detectarse fácilmente"
    },
    "angkor": {
        "name": "Angkor Wat Temple Complex",
        "environment": "forest",
        "coordinates": {"lat": 13.4125, "lon": 103.8670},
        "country": "Cambodia",
        "period": "Khmer Empire (12th century CE)",
        "expected_detection": True,
        "notes": "Templos bajo vegetación densa - requiere LiDAR"
    },
    "machu_picchu": {
        "name": "Machu Picchu",
        "environment": "mountain",
        "coordinates": {"lat": -13.1631, "lon": -72.5450},
        "country": "Peru",
        "period": "Inca Empire (1450 CE)",
        "expected_detection": True,
        "notes": "Ciudad en montaña - topografía compleja"
    },
    "petra": {
        "name": "Petra",
        "environment": "desert",
        "coordinates": {"lat": 30.3285, "lon": 35.4444},
        "country": "Jordan",
        "period": "Nabataean Kingdom (300 BCE)",
        "expected_detection": True,
        "notes": "Ciudad tallada en roca - cañón desértico"
    },
    "stonehenge": {
        "name": "Stonehenge",
        "environment": "grassland",
        "coordinates": {"lat": 51.1789, "lon": -1.8262},
        "country": "United Kingdom",
        "period": "Neolithic (3000-2000 BCE)",
        "expected_detection": True,
        "notes": "Monumento megalítico - campo abierto"
    }
}

def analyze_site(site_id: str, site_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analizar un sitio arqueológico"""
    
    print(f"\n{'='*80}")
    print(f"🏛️  ANALIZANDO: {site_data['name']}")
    print(f"{'='*80}")
    print(f"📍 Ubicación: {site_data['country']}")
    print(f"🌍 Ambiente: {site_data['environment']}")
    print(f"📅 Período: {site_data['period']}")
    print(f"💡 Notas: {site_data['notes']}")
    
    # Preparar request
    lat = site_data['coordinates']['lat']
    lon = site_data['coordinates']['lon']
    
    request_data = {
        "lat_min": lat - 0.01,
        "lat_max": lat + 0.01,
        "lon_min": lon - 0.01,
        "lon_max": lon + 0.01,
        "region_name": site_data['name'],
        "resolution_m": 1000
    }
    
    try:
        print(f"\n🔬 Ejecutando análisis...")
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=request_data,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"❌ ERROR: HTTP {response.status_code}")
            return {
                "site_id": site_id,
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }
        
        result = response.json()
        
        # Extraer información clave
        env_detected = result.get("environment_classification", {}).get("environment_type", "unknown")
        env_confidence = result.get("environment_classification", {}).get("confidence", 0.0)
        
        arch_result = result.get("archaeological_results", {}).get("result_type", "unknown")
        arch_prob = result.get("archaeological_results", {}).get("archaeological_probability", 0.0)
        confidence = result.get("archaeological_results", {}).get("confidence", "unknown")
        
        site_recognized = result.get("archaeological_results", {}).get("site_recognized", False)
        
        convergence = result.get("convergence_analysis", {})
        instruments_converging = convergence.get("instruments_converging", 0)
        minimum_required = convergence.get("minimum_required", 0)
        
        measurements = result.get("instrumental_measurements", [])
        
        # Mostrar resultados
        print(f"\n📊 RESULTADOS:")
        print(f"   Ambiente detectado: {env_detected} (confianza: {env_confidence:.2f})")
        print(f"   Resultado arqueológico: {arch_result}")
        print(f"   Probabilidad arqueológica: {arch_prob:.2%}")
        print(f"   Nivel de confianza: {confidence}")
        print(f"   Sitio reconocido: {'✅ SÍ' if site_recognized else '❌ NO'}")
        print(f"   Instrumentos convergentes: {instruments_converging}/{minimum_required}")
        
        print(f"\n🔬 MEDICIONES INSTRUMENTALES:")
        for m in measurements:
            exceeds = "✅" if m.get("exceeds_threshold") else "❌"
            print(f"   {exceeds} {m.get('instrument')}: {m.get('value'):.2f} {m.get('unit')} "
                  f"(umbral: {m.get('threshold'):.2f}) - {m.get('confidence')}")
        
        # Evaluación
        detected = arch_prob > 0.5
        expected = site_data['expected_detection']
        
        if detected == expected:
            if detected:
                print(f"\n✅ ÉXITO: Sitio arqueológico DETECTADO correctamente")
            else:
                print(f"\n✅ ÉXITO: Correctamente NO detectado")
            status = "success"
        else:
            if expected and not detected:
                print(f"\n❌ FALSO NEGATIVO: Debería detectarse pero no se detectó")
                status = "false_negative"
            else:
                print(f"\n❌ FALSO POSITIVO: No debería detectarse pero se detectó")
                status = "false_positive"
        
        return {
            "site_id": site_id,
            "site_name": site_data['name'],
            "status": status,
            "environment_detected": env_detected,
            "environment_confidence": env_confidence,
            "archaeological_probability": arch_prob,
            "confidence_level": confidence,
            "site_recognized": site_recognized,
            "instruments_converging": instruments_converging,
            "minimum_required": minimum_required,
            "measurements_count": len(measurements),
            "detected": detected,
            "expected": expected,
            "full_result": result
        }
        
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT: Análisis tardó demasiado")
        return {
            "site_id": site_id,
            "status": "timeout",
            "error": "Request timeout"
        }
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}")
        return {
            "site_id": site_id,
            "status": "error",
            "error": str(e)
        }

def generate_report(results: list) -> None:
    """Generar reporte final"""
    
    print(f"\n{'='*80}")
    print(f"📊 REPORTE FINAL - TEST DE 5 SITIOS ARQUEOLÓGICOS")
    print(f"{'='*80}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API: {API_BASE_URL}")
    
    # Estadísticas
    total = len(results)
    success = sum(1 for r in results if r.get("status") == "success")
    false_neg = sum(1 for r in results if r.get("status") == "false_negative")
    false_pos = sum(1 for r in results if r.get("status") == "false_positive")
    errors = sum(1 for r in results if r.get("status") in ["error", "timeout"])
    
    print(f"\n📈 ESTADÍSTICAS GENERALES:")
    print(f"   Total sitios analizados: {total}")
    print(f"   ✅ Éxitos: {success}/{total} ({success/total*100:.1f}%)")
    print(f"   ❌ Falsos negativos: {false_neg}/{total}")
    print(f"   ❌ Falsos positivos: {false_pos}/{total}")
    print(f"   ⚠️  Errores: {errors}/{total}")
    
    # Detalles por sitio
    print(f"\n🏛️  RESULTADOS POR SITIO:")
    for r in results:
        if r.get("status") in ["error", "timeout"]:
            print(f"\n   ⚠️  {r.get('site_id')}: ERROR - {r.get('error')}")
            continue
        
        status_icon = "✅" if r.get("status") == "success" else "❌"
        print(f"\n   {status_icon} {r.get('site_name')}")
        print(f"      Ambiente: {r.get('environment_detected')} (conf: {r.get('environment_confidence', 0):.2f})")
        print(f"      Probabilidad: {r.get('archaeological_probability', 0):.2%}")
        print(f"      Confianza: {r.get('confidence_level')}")
        print(f"      Reconocido: {'✅' if r.get('site_recognized') else '❌'}")
        print(f"      Instrumentos: {r.get('instruments_converging')}/{r.get('minimum_required')}")
        print(f"      Estado: {r.get('status')}")
    
    # Análisis de convergencia instrumental
    print(f"\n🔬 ANÁLISIS DE CONVERGENCIA INSTRUMENTAL:")
    for r in results:
        if r.get("status") not in ["error", "timeout"]:
            converging = r.get('instruments_converging', 0)
            required = r.get('minimum_required', 0)
            met = converging >= required
            icon = "✅" if met else "❌"
            print(f"   {icon} {r.get('site_name')}: {converging}/{required} instrumentos")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    if false_neg > 0:
        print(f"   ⚠️  {false_neg} falsos negativos detectados")
        print(f"      → Ajustar umbrales de detección")
        print(f"      → Mejorar simulación de mediciones")
        print(f"      → Calibrar con sitios conocidos")
    
    if false_pos > 0:
        print(f"   ⚠️  {false_pos} falsos positivos detectados")
        print(f"      → Aumentar requisitos de convergencia")
        print(f"      → Ajustar umbrales más conservadores")
    
    if success == total:
        print(f"   ✅ ¡EXCELENTE! Todos los sitios detectados correctamente")
        print(f"      → Sistema calibrado adecuadamente")
        print(f"      → Listo para análisis en producción")
    
    # Calificación final
    score = (success / total) * 100 if total > 0 else 0
    print(f"\n🎯 CALIFICACIÓN FINAL: {score:.1f}%")
    
    if score >= 80:
        print(f"   ✅ EXCELENTE - Sistema bien calibrado")
    elif score >= 60:
        print(f"   ⚠️  BUENO - Necesita ajustes menores")
    elif score >= 40:
        print(f"   ⚠️  REGULAR - Requiere calibración")
    else:
        print(f"   ❌ POBRE - Necesita revisión completa")
    
    print(f"\n{'='*80}")

def main():
    """Ejecutar test completo"""
    
    print(f"\n{'='*80}")
    print(f"🧪 TEST DE 5 SITIOS ARQUEOLÓGICOS DIVERSOS")
    print(f"{'='*80}")
    print(f"\nProbando ArcheoScope con sitios de diferentes ambientes y épocas:")
    for site_id, site_data in TEST_SITES.items():
        print(f"  • {site_data['name']} ({site_data['environment']})")
    
    # Verificar backend
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        if response.status_code == 200:
            print(f"\n✅ Backend operacional")
        else:
            print(f"\n❌ Backend no responde correctamente")
            return
    except Exception as e:
        print(f"\n❌ ERROR: Backend no está corriendo ({e})")
        print(f"   Inicia el backend: python run_archeoscope.py")
        return
    
    # Analizar cada sitio
    results = []
    for site_id, site_data in TEST_SITES.items():
        result = analyze_site(site_id, site_data)
        results.append(result)
    
    # Generar reporte
    generate_report(results)
    
    # Guardar resultados
    output_file = f"test_5_sites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_date": datetime.now().isoformat(),
            "api_url": API_BASE_URL,
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
