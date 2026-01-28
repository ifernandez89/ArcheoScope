#!/usr/bin/env python3
"""
Test: Generar candidatas arqueológicas en los Andes Peruanos
"""

import requests
import json

API_BASE = "http://localhost:8002"

# Regiones peruanas para probar
PERU_REGIONS = [
    {
        'name': 'Cusco - Valle Sagrado',
        'lat_min': -14, 'lat_max': -13,
        'lon_min': -73, 'lon_max': -71
    },
    {
        'name': 'Lima - Costa Central',
        'lat_min': -13, 'lat_max': -11,
        'lon_min': -78, 'lon_max': -76
    },
    {
        'name': 'Nazca - Líneas',
        'lat_min': -15.5, 'lat_max': -14,
        'lon_min': -76, 'lon_max': -74
    },
]

print("🇵🇪 TEST: CANDIDATAS ARQUEOLÓGICAS EN PERÚ")
print("=" * 100)

for region in PERU_REGIONS:
    print(f"\n{'='*100}")
    print(f"📍 {region['name']}")
    print(f"   Coordenadas: {region['lat_min']} a {region['lat_max']} lat, {region['lon_min']} a {region['lon_max']} lon")
    print(f"{'='*100}")
    
    url = f"{API_BASE}/archaeological-sites/enriched-candidates"
    params = {
        'lat_min': region['lat_min'],
        'lat_max': region['lat_max'],
        'lon_min': region['lon_min'],
        'lon_max': region['lon_max'],
        'strategy': 'buffer',
        'max_zones': 20,
        'lidar_priority': True,
        'min_convergence': 0.4,
        'save_to_database': False  # No guardar en este test
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n✅ Status: {response.status_code}")
            print(f"📊 Total candidatas: {data.get('total_candidates', 0)}")
            
            if data.get('total_candidates', 0) > 0:
                candidates = data.get('candidates', [])
                
                # Estadísticas
                actions = {}
                for c in candidates:
                    action = c.get('recommended_action', 'unknown')
                    actions[action] = actions.get(action, 0) + 1
                
                print(f"\n🎯 Acciones recomendadas:")
                for action, count in actions.items():
                    print(f"   {action}: {count}")
                
                # Top 3 candidatas
                print(f"\n🔥 Top 3 Candidatas:")
                for i, c in enumerate(candidates[:3], 1):
                    print(f"\n   {i}. {c.get('candidate_id')}")
                    print(f"      Score: {c.get('multi_instrumental_score', 0):.3f}")
                    print(f"      Convergencia: {c.get('convergence', {}).get('count', 0)}/{c.get('convergence', {}).get('total_instruments', 0)}")
                    print(f"      Acción: {c.get('recommended_action')}")
                    if c.get('temporal_persistence', {}).get('detected'):
                        print(f"      Persistencia: {c.get('temporal_persistence', {}).get('years', 0)} años")
            else:
                print(f"\n⚠️  No se generaron candidatas (puede ser normal si no hay sitios conocidos cerca)")
        
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"   {response.text[:200]}")
    
    except Exception as e:
        print(f"\n❌ Exception: {e}")

print("\n" + "=" * 100)
print("✅ TEST COMPLETADO")
