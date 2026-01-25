#!/usr/bin/env python3
"""
Test de nuevos endpoints de sitios arqueológicos
"""

import requests
import json

BASE_URL = "http://localhost:8002"

def test_all_sites():
    """Test endpoint /archaeological-sites/all"""
    
    print("="*60)
    print("TEST 1: Todos los sitios (sin filtros)")
    print("="*60)
    
    url = f"{BASE_URL}/archaeological-sites/all"
    response = requests.get(url, params={'limit': 10})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Total sitios: {data['total']:,}")
        print(f"Sitios retornados: {len(data['sites'])}")
        print(f"Página: {data['page']}/{data['total_pages']}")
        print(f"Filtros aplicados: {data['filters_applied']}")
        
        if data['sites']:
            print(f"\nPrimer sitio:")
            site = data['sites'][0]
            print(f"  - Nombre: {site['name']}")
            print(f"  - País: {site['country']}")
            print(f"  - Ambiente: {site['environment_type']}")
            print(f"  - Coordenadas: ({site['latitude']}, {site['longitude']})")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_filter_by_environment():
    """Test filtro por tipo de ambiente"""
    
    print("\n" + "="*60)
    print("TEST 2: Filtrar por ambiente (desert)")
    print("="*60)
    
    url = f"{BASE_URL}/archaeological-sites/all"
    response = requests.get(url, params={
        'environment_type': 'desert',
        'limit': 10
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Total sitios en desiertos: {data['total']:,}")
        print(f"Sitios retornados: {len(data['sites'])}")
        print(f"Filtros aplicados: {data['filters_applied']}")
        
        if data['sites']:
            print(f"\nPrimeros 3 sitios en desiertos:")
            for i, site in enumerate(data['sites'][:3], 1):
                print(f"  {i}. {site['name']} ({site['country']})")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_by_environment_endpoint():
    """Test endpoint especializado por ambiente"""
    
    print("\n" + "="*60)
    print("TEST 3: Endpoint por ambiente (forest)")
    print("="*60)
    
    url = f"{BASE_URL}/archaeological-sites/by-environment/forest"
    response = requests.get(url, params={'limit': 10})
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Ambiente: {data['environment_type']}")
        print(f"Total sitios: {data['total']:,}")
        print(f"Sitios retornados: {len(data['sites'])}")
        
        print(f"\nInstrumentos recomendados:")
        print(f"  Primarios: {', '.join(data['recommended_instruments']['primary'])}")
        print(f"  Secundarios: {', '.join(data['recommended_instruments']['secondary'])}")
        print(f"  Características: {data['recommended_instruments']['characteristics']}")
        
        if data['sites']:
            print(f"\nPrimeros 3 sitios en bosques:")
            for i, site in enumerate(data['sites'][:3], 1):
                print(f"  {i}. {site['name']} ({site['country']})")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_environment_stats():
    """Test estadísticas de ambientes"""
    
    print("\n" + "="*60)
    print("TEST 4: Estadísticas de ambientes")
    print("="*60)
    
    url = f"{BASE_URL}/archaeological-sites/environments/stats"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Total sitios: {data['total_sites']:,}")
        print(f"Tipos de ambiente: {data['total_environments']}")
        
        print(f"\nDistribución por ambiente:")
        for stat in data['environment_stats'][:10]:
            env = stat['environment_type'] or 'unknown'
            count = stat['count']
            pct = stat['percentage']
            print(f"  - {env:15s}: {count:6,} sitios ({pct:5.2f}%)")
        
        print(f"\nAmbiente más común:")
        summary = data['summary']
        print(f"  - {summary['most_common_environment']}: {summary['most_common_count']:,} sitios")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_filter_by_country():
    """Test filtro por país"""
    
    print("\n" + "="*60)
    print("TEST 5: Filtrar por país (Italy)")
    print("="*60)
    
    url = f"{BASE_URL}/archaeological-sites/all"
    response = requests.get(url, params={
        'country': 'Italy',
        'limit': 10
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Total sitios en Italia: {data['total']:,}")
        print(f"Sitios retornados: {len(data['sites'])}")
        
        if data['sites']:
            print(f"\nPrimeros 5 sitios en Italia:")
            for i, site in enumerate(data['sites'][:5], 1):
                env = site['environment_type'] or 'unknown'
                print(f"  {i}. {site['name']} - Ambiente: {env}")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def test_combined_filters():
    """Test filtros combinados"""
    
    print("\n" + "="*60)
    print("TEST 6: Filtros combinados (forest + France)")
    print("="*60)
    
    url = f"{BASE_URL}/archaeological-sites/all"
    response = requests.get(url, params={
        'environment_type': 'forest',
        'country': 'France',
        'limit': 10
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Total sitios (bosques en Francia): {data['total']:,}")
        print(f"Sitios retornados: {len(data['sites'])}")
        print(f"Filtros aplicados: {data['filters_applied']}")
        
        if data['sites']:
            print(f"\nSitios encontrados:")
            for i, site in enumerate(data['sites'][:5], 1):
                print(f"  {i}. {site['name']}")
        
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def main():
    """Ejecutar todos los tests"""
    
    print("\n🧪 TESTING NUEVOS ENDPOINTS DE SITIOS ARQUEOLÓGICOS")
    print("="*60)
    
    tests = [
        ("Todos los sitios", test_all_sites),
        ("Filtro por ambiente", test_filter_by_environment),
        ("Endpoint por ambiente", test_by_environment_endpoint),
        ("Estadísticas de ambientes", test_environment_stats),
        ("Filtro por país", test_filter_by_country),
        ("Filtros combinados", test_combined_filters)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Error en test '{name}': {e}")
            results.append((name, False))
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE TESTS")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResultado: {passed}/{total} tests pasados")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} tests fallaron")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
