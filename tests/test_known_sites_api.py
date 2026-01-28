#!/usr/bin/env python3
"""Test de API de sitios conocidos"""

import requests
import json

API_BASE = "http://localhost:8002/api"

def test_regions():
    """Test endpoint de regiones"""
    print("=" * 80)
    print("TEST: /known-sites/regions")
    print("=" * 80)
    
    response = requests.get(f"{API_BASE}/known-sites/regions")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total regiones: {data['total_regions']}")
        print(f"\nTop 5 regiones:")
        for region in data['regions'][:5]:
            print(f"  - {region['country']}: {region['count']} sitios")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        return False

def test_known_sites():
    """Test endpoint de sitios conocidos"""
    print("\n" + "=" * 80)
    print("TEST: /known-sites (España)")
    print("=" * 80)
    
    response = requests.get(f"{API_BASE}/known-sites?country=Spain&limit=10")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total sitios: {data['total']}")
        print(f"\nPrimeros 3 sitios:")
        for site in data['sites'][:3]:
            print(f"  - {site['name']}")
            print(f"    {site['lat']:.4f}, {site['lon']:.4f}")
            print(f"    País: {site['country']}")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        return False

def test_nearby():
    """Test endpoint de sitios cercanos"""
    print("\n" + "=" * 80)
    print("TEST: /known-sites/nearby (Roma)")
    print("=" * 80)
    
    # Roma: 41.9028, 12.4964
    response = requests.get(f"{API_BASE}/known-sites/nearby/41.9028/12.4964?radius_km=50")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sitios cercanos: {data['total']}")
        print(f"Radio: {data['radius_km']}km")
        print(f"\nPrimeros 3 sitios:")
        for site in data['sites'][:3]:
            print(f"  - {site['name']}")
            print(f"    Distancia: {site['distance_km']}km")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        return False

if __name__ == "__main__":
    print("\n🧪 TESTING API DE SITIOS CONOCIDOS\n")
    
    results = []
    results.append(test_regions())
    results.append(test_known_sites())
    results.append(test_nearby())
    
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Tests pasados: {sum(results)}/{len(results)}")
    
    if all(results):
        print("✅ Todos los tests pasaron")
    else:
        print("❌ Algunos tests fallaron")
    
    exit(0 if all(results) else 1)
