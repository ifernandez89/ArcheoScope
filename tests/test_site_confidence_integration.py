#!/usr/bin/env python3
"""
Test de integración del sistema de confianza de sitios
Valida que el ajuste probabilístico funciona correctamente
"""

import requests
import json
from typing import Dict, Any

API_BASE = "http://localhost:8002"


def test_cultural_prior_map():
    """Test del endpoint de mapa de prior cultural"""
    
    print("="*80)
    print("🗺️ TEST: Mapa de Prior Cultural")
    print("="*80)
    print()
    
    # Región de Giza (debería tener alta densidad cultural)
    test_data = {
        "lat_min": 29.9,
        "lat_max": 30.1,
        "lon_min": 31.0,
        "lon_max": 31.2,
        "grid_size": 50
    }
    
    print(f"📍 Región: Giza, Egipto")
    print(f"   Bounds: {test_data['lat_min']:.2f} - {test_data['lat_max']:.2f}, {test_data['lon_min']:.2f} - {test_data['lon_max']:.2f}")
    print()
    
    try:
        response = requests.post(
            f"{API_BASE}/archaeological-sites/cultural-prior-map",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Mapa generado exitosamente")
            print()
            print(f"📊 Sitios usados: {result['sites_used']}")
            print(f"📊 Huecos detectados: {result['metadata']['gaps_detected']}")
            print(f"📊 Densidad máxima: {result['metadata']['max_density']:.3f}")
            print(f"📊 Densidad promedio: {result['metadata']['mean_density']:.3f}")
            print()
            
            interpretation = result['interpretation']
            print("🔍 Interpretación:")
            print(f"   Áreas alta densidad: {interpretation['high_density_areas']}")
            print(f"   Áreas media densidad: {interpretation['medium_density_areas']}")
            print(f"   Áreas baja densidad: {interpretation['low_density_areas']}")
            print()
            
            if result['metadata']['gaps_detected'] > 0:
                print(f"⚠️ {result['metadata']['gaps_detected']} huecos culturales detectados")
                print("   → Candidatos prioritarios para exploración")
            
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"   {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def test_anomaly_detection_with_confidence():
    """Test de detección de anomalías con ajuste de confianza"""
    
    print("\n" + "="*80)
    print("🎯 TEST: Detección con Ajuste de Confianza")
    print("="*80)
    print()
    
    # Test 1: Región con sitio conocido (Giza)
    print("📍 Test 1: Región con sitio conocido (Giza)")
    print()
    
    giza_data = {
        "lat_min": 29.975,
        "lat_max": 29.980,
        "lon_min": 31.130,
        "lon_max": 31.135,
        "region_name": "Giza Plateau Test"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/analyze",
            json=giza_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Análisis completado")
            print()
            print(f"🏛️ Sitio conocido: {result.get('known_site_name', 'N/A')}")
            print(f"📊 Probabilidad arqueológica: {result.get('archaeological_probability', 0):.2%}")
            print(f"🎯 Confianza: {result.get('confidence_level', 'N/A')}")
            print()
            
            # Verificar que el ajuste se aplicó
            if 'adjustment_details' in result:
                adj = result['adjustment_details']
                print("📉 Ajuste por sitio conocido:")
                print(f"   Score original: {adj.get('original_score', 0):.3f}")
                print(f"   Ajuste aplicado: {adj.get('adjustment', 0):.3f}")
                print(f"   Score ajustado: {adj.get('adjusted_score', 0):.3f}")
                print(f"   Sitios cercanos: {adj.get('nearby_count', 0)}")
            
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def test_confidence_calculation():
    """Test de cálculo de confianza de sitios"""
    
    print("\n" + "="*80)
    print("🔍 TEST: Cálculo de Confianza de Sitios")
    print("="*80)
    print()
    
    try:
        # Obtener algunos sitios de ejemplo
        response = requests.get(
            f"{API_BASE}/archaeological-sites/all",
            params={"limit": 5},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            sites = result.get('sites', [])
            
            print(f"✅ Obtenidos {len(sites)} sitios de ejemplo")
            print()
            
            for site in sites:
                print(f"📍 {site.get('name')}")
                print(f"   País: {site.get('country')}")
                print(f"   Tipo: {site.get('site_type')}")
                print(f"   Nivel confianza BD: {site.get('confidence_level')}")
                print(f"   Ambiente: {site.get('environment_type')}")
                print()
            
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def test_environment_stats():
    """Test de estadísticas por ambiente"""
    
    print("\n" + "="*80)
    print("📊 TEST: Estadísticas por Ambiente")
    print("="*80)
    print()
    
    try:
        response = requests.get(
            f"{API_BASE}/archaeological-sites/environments/stats",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Total de sitios: {result['total_sites']:,}")
            print(f"✅ Tipos de ambiente: {result['total_environments']}")
            print()
            
            print("📊 Distribución por ambiente:")
            for stat in result['environment_stats'][:5]:
                env_type = stat['environment_type']
                count = stat['count']
                percentage = stat['percentage']
                print(f"   {env_type:15s}: {count:6,} sitios ({percentage:5.1f}%)")
            
            print()
            print(f"🏆 Ambiente más común: {result['summary']['most_common_environment']}")
            print(f"   ({result['summary']['most_common_count']:,} sitios)")
            
            return True
        else:
            print(f"❌ Error HTTP {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False


def main():
    """Función principal"""
    
    print("="*80)
    print("🧪 SUITE DE TESTS: Sistema de Confianza de Sitios")
    print("="*80)
    print()
    print("Tests a ejecutar:")
    print("  1. Estadísticas por ambiente")
    print("  2. Cálculo de confianza de sitios")
    print("  3. Mapa de prior cultural")
    print("  4. Detección con ajuste de confianza")
    print()
    
    results = []
    
    # Test 1: Estadísticas
    results.append(("Estadísticas por ambiente", test_environment_stats()))
    
    # Test 2: Confianza
    results.append(("Cálculo de confianza", test_confidence_calculation()))
    
    # Test 3: Mapa cultural
    results.append(("Mapa de prior cultural", test_cultural_prior_map()))
    
    # Test 4: Detección con ajuste
    results.append(("Detección con ajuste", test_anomaly_detection_with_confidence()))
    
    # Resumen
    print("\n" + "="*80)
    print("📋 RESUMEN DE TESTS")
    print("="*80)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Resultado: {passed}/{total} tests pasados ({passed/total*100:.0f}%)")
    print()
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron!")
        return 0
    else:
        print("⚠️ Algunos tests fallaron")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
