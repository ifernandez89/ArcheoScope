#!/usr/bin/env python3
"""
Test de endpoints de sitios arqueológicos.

Endpoints a probar:
1. GET /api/scientific/sites/stats - Estadísticas generales
2. GET /api/scientific/sites/all - Listar todos los sitios (paginado)
"""

import requests
import json

API_BASE_URL = "http://localhost:8002"

def test_sites_statistics():
    """Test endpoint de estadísticas."""
    
    print("📊 TEST 1: Estadísticas de Sitios Arqueológicos")
    print("=" * 70)
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/scientific/sites/stats",
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        stats = response.json()
        
        print(f"\n✅ ESTADÍSTICAS OBTENIDAS")
        print(f"\n📈 TOTALES:")
        print(f"   Total sitios: {stats['total_sites']:,}")
        print(f"   Sitios de control: {stats['control_sites']:,}")
        print(f"   Adiciones recientes (7 días): {stats['recent_additions']:,}")
        
        print(f"\n🌍 TOP 10 PAÍSES:")
        for item in stats['by_country'][:10]:
            print(f"   {item['country']:<30} {item['count']:>8,}")
        
        print(f"\n🏛️ POR TIPO DE SITIO:")
        for item in stats['by_site_type']:
            print(f"   {item['site_type']:<30} {item['count']:>8,}")
        
        print(f"\n🌲 POR AMBIENTE:")
        for item in stats['by_environment']:
            print(f"   {item['environment_type']:<30} {item['count']:>8,}")
        
        print(f"\n🎯 POR CONFIANZA:")
        for item in stats['by_confidence']:
            print(f"   {item['confidence_level']:<30} {item['count']:>8,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_list_sites():
    """Test endpoint de listado de sitios."""
    
    print("\n\n📋 TEST 2: Listar Sitios Arqueológicos (Paginado)")
    print("=" * 70)
    
    try:
        # Test 1: Primera página sin filtros
        print("\n🔍 Test 2.1: Primera página (100 sitios)")
        response = requests.get(
            f"{API_BASE_URL}/api/scientific/sites/all?page=1&page_size=100",
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code}")
            return False
        
        data = response.json()
        
        print(f"   Total sitios: {data['total']:,}")
        print(f"   Página: {data['page']}/{data['total_pages']}")
        print(f"   Sitios en esta página: {len(data['sites'])}")
        
        if len(data['sites']) > 0:
            print(f"\n   📍 Primeros 5 sitios:")
            for site in data['sites'][:5]:
                coords = site['coordinates']
                loc = site['location']
                print(f"      • {site['name']}")
                print(f"        Tipo: {site['site_type']}, Ambiente: {site['environment_type']}")
                print(f"        Ubicación: {loc['country']}, {loc['region']}")
                print(f"        Coords: ({coords['latitude']:.4f}, {coords['longitude']:.4f})")
        
        # Test 2: Filtrar por país
        print(f"\n🔍 Test 2.2: Filtrar por país (México)")
        response = requests.get(
            f"{API_BASE_URL}/api/scientific/sites/all?country=México&page_size=10",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Sitios en México: {data['total']:,}")
            if len(data['sites']) > 0:
                print(f"   Primeros sitios:")
                for site in data['sites'][:3]:
                    print(f"      • {site['name']}")
        
        # Test 3: Búsqueda por nombre
        print(f"\n🔍 Test 2.3: Búsqueda por nombre (Machu)")
        response = requests.get(
            f"{API_BASE_URL}/api/scientific/sites/all?search=Machu&page_size=10",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Resultados encontrados: {data['total']}")
            if len(data['sites']) > 0:
                print(f"   Sitios:")
                for site in data['sites']:
                    print(f"      • {site['name']} ({site['location']['country']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Ejecutar todos los tests."""
    
    print("\n" + "="*70)
    print("🧪 TEST DE ENDPOINTS DE SITIOS ARQUEOLÓGICOS")
    print("="*70)
    print(f"\nAPI: {API_BASE_URL}")
    print("\n⚠️ Asegúrate de que el backend esté corriendo")
    
    results = []
    
    # Test 1: Estadísticas
    results.append(test_sites_statistics())
    
    # Test 2: Listado
    results.append(test_list_sites())
    
    # Resumen
    print("\n\n" + "="*70)
    print(f"📊 RESUMEN: {sum(results)}/{len(results)} tests pasaron")
    print("="*70)
    
    if all(results):
        print("\n✅ TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE")
    else:
        print("\n⚠️ Algunos tests fallaron")


if __name__ == "__main__":
    main()
