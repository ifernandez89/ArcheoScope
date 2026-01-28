#!/usr/bin/env python3
"""
Enriquecer BD con análisis de sitios arqueológicos icónicos.

SITIOS A ANALIZAR:
1. 🗿 Machu Picchu, Perú
2. 🐪 Giza/Esfinge, Egipto
3. 🌀 Nazca, Perú
4. 🏛️ Angkor Wat, Camboya
5. 🏺 Petra, Jordania
6. 🗼 Teotihuacán, México
7. 🏰 Stonehenge, UK
8. 🌋 Pompeya, Italia
9. 🏛️ Acrópolis, Grecia
10. 🏜️ Chichén Itzá, México

Objetivo: Poblar BD con análisis científicos completos usando:
- Pipeline científico refinado
- Explanatory Strangeness Score
- Ajustes quirúrgicos implementados
"""

import requests
import json
import time
from typing import Dict, List

# Configuración
API_BASE_URL = "http://localhost:8002"

# Sitios arqueológicos icónicos con coordenadas reales
ICONIC_SITES = [
    {
        "name": "Machu Picchu",
        "country": "Perú",
        "lat": -13.1631,
        "lon": -72.5450,
        "environment": "mountain",
        "description": "Ciudad inca del siglo XV en los Andes peruanos",
        "expected_ess": "very_high"
    },
    {
        "name": "Pirámides de Giza",
        "country": "Egipto",
        "lat": 29.9792,
        "lon": 31.1342,
        "environment": "desert",
        "description": "Complejo de pirámides del Antiguo Egipto",
        "expected_ess": "high"
    },
    {
        "name": "Líneas de Nazca",
        "country": "Perú",
        "lat": -14.7390,
        "lon": -75.1300,
        "environment": "desert",
        "description": "Geoglifos precolombinos en el desierto de Nazca",
        "expected_ess": "very_high"
    },
    {
        "name": "Angkor Wat",
        "country": "Camboya",
        "lat": 13.4125,
        "lon": 103.8670,
        "environment": "tropical_forest",
        "description": "Complejo de templos jemer del siglo XII",
        "expected_ess": "high"
    },
    {
        "name": "Petra",
        "country": "Jordania",
        "lat": 30.3285,
        "lon": 35.4444,
        "environment": "desert",
        "description": "Ciudad nabatea tallada en roca",
        "expected_ess": "high"
    },
    {
        "name": "Teotihuacán",
        "country": "México",
        "lat": 19.6925,
        "lon": -98.8438,
        "environment": "highland",
        "description": "Ciudad mesoamericana con pirámides monumentales",
        "expected_ess": "high"
    },
    {
        "name": "Stonehenge",
        "country": "Reino Unido",
        "lat": 51.1789,
        "lon": -1.8262,
        "environment": "grassland",
        "description": "Monumento megalítico neolítico",
        "expected_ess": "medium"
    },
    {
        "name": "Pompeya",
        "country": "Italia",
        "lat": 40.7489,
        "lon": 14.4839,
        "environment": "urban",
        "description": "Ciudad romana sepultada por erupción del Vesubio",
        "expected_ess": "medium"
    },
    {
        "name": "Acrópolis de Atenas",
        "country": "Grecia",
        "lat": 37.9715,
        "lon": 23.7257,
        "environment": "urban",
        "description": "Ciudadela de la antigua Atenas",
        "expected_ess": "high"
    },
    {
        "name": "Chichén Itzá",
        "country": "México",
        "lat": 20.6843,
        "lon": -88.5678,
        "environment": "tropical_forest",
        "description": "Ciudad maya con pirámide de Kukulkán",
        "expected_ess": "high"
    }
]

def analyze_site(site: Dict) -> Dict:
    """
    Analizar un sitio arqueológico usando el endpoint científico.
    
    Args:
        site: Diccionario con datos del sitio
    
    Returns:
        Resultado del análisis o None si falla
    """
    
    print(f"\n{'='*70}")
    print(f"🏛️ ANALIZANDO: {site['name']}, {site['country']}")
    print(f"{'='*70}")
    print(f"📍 Coordenadas: ({site['lat']:.4f}, {site['lon']:.4f})")
    print(f"🌍 Ambiente: {site['environment']}")
    print(f"📝 Descripción: {site['description']}")
    print(f"🔬 ESS esperado: {site['expected_ess'].upper()}")
    
    # Preparar request
    # Usar un área pequeña alrededor del sitio (0.01 grados ≈ 1km)
    request_data = {
        "lat_min": site['lat'] - 0.01,
        "lat_max": site['lat'] + 0.01,
        "lon_min": site['lon'] - 0.01,
        "lon_max": site['lon'] + 0.01,
        "region_name": f"{site['name']}, {site['country']}"
    }
    
    try:
        print(f"\n🔄 Enviando request al backend...")
        response = requests.post(
            f"{API_BASE_URL}/api/scientific/analyze",
            json=request_data,
            timeout=120  # 2 minutos timeout
        )
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
        
        result = response.json()
        
        # Extraer métricas clave
        sci_output = result.get('scientific_output', {})
        
        print(f"\n✅ ANÁLISIS COMPLETADO")
        print(f"\n📊 RESULTADOS:")
        print(f"   🆔 Analysis ID: {sci_output.get('analysis_id')}")
        print(f"   📍 Candidate Name: {sci_output.get('candidate_name')}")
        print(f"   🌍 Region: {sci_output.get('region')}")
        print(f"   🏞️ Environment: {sci_output.get('environment_type')}")
        
        print(f"\n🔬 MÉTRICAS CIENTÍFICAS:")
        print(f"   📉 Anomaly Score: {sci_output.get('anomaly_score', 0):.3f}")
        print(f"   🧬 Anthropic Probability: {sci_output.get('anthropic_probability', 0):.3f}")
        print(f"   📊 Confidence Interval: [{sci_output.get('confidence_interval', [0,0])[0]:.2f}, {sci_output.get('confidence_interval', [0,0])[1]:.2f}]")
        print(f"   🎯 Result Type: {sci_output.get('result_type')}")
        print(f"   ⚡ Recommended Action: {sci_output.get('recommended_action')}")
        
        print(f"\n📡 COBERTURA INSTRUMENTAL:")
        print(f"   Raw: {sci_output.get('coverage_raw', 0):.1%} ({sci_output.get('instruments_measured', 0)}/{sci_output.get('instruments_available', 0)})")
        print(f"   Effective: {sci_output.get('coverage_effective', 0):.1%}")
        
        print(f"\n🔬 EXPLANATORY STRANGENESS:")
        ess_level = sci_output.get('explanatory_strangeness', 'none')
        ess_score = sci_output.get('strangeness_score', 0)
        ess_reasons = sci_output.get('strangeness_reasons', [])
        
        print(f"   Level: {ess_level.upper()} (score={ess_score:.3f})")
        if ess_reasons:
            print(f"   Razones:")
            for reason in ess_reasons:
                print(f"      • {reason}")
        
        # Verificar si ESS coincide con expectativa
        if ess_level in ['high', 'very_high'] and site['expected_ess'] in ['high', 'very_high']:
            print(f"\n   ✅ ESS coincide con expectativa ({site['expected_ess']})")
        elif ess_level == site['expected_ess']:
            print(f"\n   ✅ ESS coincide exactamente con expectativa")
        else:
            print(f"\n   ⚠️ ESS difiere de expectativa (esperado: {site['expected_ess']}, obtenido: {ess_level})")
        
        print(f"\n📝 EXPLICACIÓN:")
        explanation = sci_output.get('scientific_explanation', 'N/A')
        print(f"   {explanation[:200]}...")
        
        return result
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout esperando respuesta del backend")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Analizar todos los sitios icónicos y poblar la BD."""
    
    print("\n" + "="*70)
    print("🏛️ ENRIQUECIMIENTO DE BASE DE DATOS")
    print("="*70)
    print(f"\nSitios a analizar: {len(ICONIC_SITES)}")
    print(f"API: {API_BASE_URL}")
    print("\n⚠️ IMPORTANTE: Asegúrate de que el backend esté corriendo")
    print("   Comando: python run_archeoscope.py")
    
    input("\n▶️ Presiona Enter para comenzar...")
    
    results = []
    successful = 0
    failed = 0
    
    for i, site in enumerate(ICONIC_SITES, 1):
        print(f"\n\n{'#'*70}")
        print(f"# SITIO {i}/{len(ICONIC_SITES)}")
        print(f"{'#'*70}")
        
        result = analyze_site(site)
        
        if result:
            results.append({
                'site': site,
                'result': result,
                'success': True
            })
            successful += 1
        else:
            results.append({
                'site': site,
                'result': None,
                'success': False
            })
            failed += 1
        
        # Pausa entre requests para no saturar el backend
        if i < len(ICONIC_SITES):
            print(f"\n⏳ Esperando 3 segundos antes del siguiente análisis...")
            time.sleep(3)
    
    # Resumen final
    print("\n\n" + "="*70)
    print("📊 RESUMEN FINAL")
    print("="*70)
    print(f"\n✅ Exitosos: {successful}/{len(ICONIC_SITES)}")
    print(f"❌ Fallidos: {failed}/{len(ICONIC_SITES)}")
    
    if successful > 0:
        print(f"\n🎉 Base de datos enriquecida con {successful} sitios arqueológicos icónicos")
        
        # Mostrar tabla resumen
        print(f"\n📋 TABLA RESUMEN:")
        print(f"{'Sitio':<25} {'País':<15} {'ESS':<12} {'Anomaly':<10} {'Prob':<10}")
        print("-" * 70)
        
        for r in results:
            if r['success']:
                site = r['site']
                sci = r['result'].get('scientific_output', {})
                ess = sci.get('explanatory_strangeness', 'none')
                anomaly = sci.get('anomaly_score', 0)
                prob = sci.get('anthropic_probability', 0)
                
                print(f"{site['name']:<25} {site['country']:<15} {ess.upper():<12} {anomaly:<10.3f} {prob:<10.3f}")
    
    # Guardar resultados en JSON
    output_file = "iconic_sites_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    
    print("\n" + "="*70)
    print("✅ ENRIQUECIMIENTO COMPLETADO")
    print("="*70)


if __name__ == "__main__":
    main()
