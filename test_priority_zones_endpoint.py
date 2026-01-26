#!/usr/bin/env python3
"""
Test del endpoint de zonas prioritarias GeoJSON
"""

import requests
import json

def test_priority_zones_geojson():
    """Test del endpoint de zonas prioritarias en formato GeoJSON"""
    
    print("🧪 Testing Priority Zones GeoJSON Endpoint")
    print("=" * 80)
    
    # Región de Petén, Guatemala
    url = "http://localhost:8002/archaeological-sites/recommended-zones-geojson"
    params = {
        'lat_min': 16.0,
        'lat_max': 18.0,
        'lon_min': -91.0,
        'lon_max': -89.0,
        'strategy': 'buffer',
        'max_zones': 50,
        'lidar_priority': True
    }
    
    try:
        print(f"\n📡 Llamando a: {url}")
        print(f"   Parámetros: {params}")
        
        response = requests.get(url, params=params, timeout=30)
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Validar estructura GeoJSON
            assert data['type'] == 'FeatureCollection', "Debe ser FeatureCollection"
            assert 'features' in data, "Debe tener features"
            assert 'metadata' in data, "Debe tener metadata"
            
            features = data['features']
            metadata = data['metadata']
            
            print(f"\n📊 Resultados:")
            print(f"   Total zonas: {len(features)}")
            print(f"   Estrategia: {metadata.get('strategy', 'unknown')}")
            print(f"   Sitios analizados: {metadata.get('sites_analyzed', metadata.get('summary', {}).get('sites_analyzed', 'N/A'))}")
            
            if 'summary' in metadata:
                summary = metadata['summary']
                print(f"\n🎯 Resumen de Prioridades:")
                print(f"   CRITICAL: {summary.get('critical_priority_zones', 0)}")
                print(f"   HIGH: {summary.get('high_priority_zones', 0)}")
                print(f"   MEDIUM: {summary.get('medium_priority_zones', 0)}")
                print(f"   🔥 GOLD CLASS: {summary.get('lidar_gold_class', 0)}")
                print(f"   Cobertura: {summary.get('coverage_percentage', 0):.1f}%")
            
            # Mostrar primeras 3 zonas
            print(f"\n🗺️ Primeras 3 zonas:")
            for i, feature in enumerate(features[:3]):
                props = feature['properties']
                print(f"\n   {i+1}. {props['zone_id']}")
                print(f"      Score: {props.get('priority_score', 'N/A')}")
                print(f"      Clase: {props.get('priority_class', 'N/A')}")
                print(f"      LiDAR: {'✅' if props.get('lidar_available') else '❌'}")
                print(f"      Terreno: {props.get('terrain_type', 'unknown')}")
                print(f"      Área: {props.get('area_km2', 0):.2f} km²")
            
            # Validar geometría
            print(f"\n🔍 Validando geometrías...")
            for i, feature in enumerate(features[:5]):
                assert feature['type'] == 'Feature', f"Feature {i} debe ser tipo Feature"
                assert 'geometry' in feature, f"Feature {i} debe tener geometry"
                assert feature['geometry']['type'] == 'Polygon', f"Feature {i} debe ser Polygon"
                assert 'properties' in feature, f"Feature {i} debe tener properties"
            
            print(f"   ✅ Todas las geometrías son válidas")
            
            print(f"\n{'='*80}")
            print(f"✅ TEST EXITOSO - Endpoint funcionando correctamente")
            print(f"{'='*80}")
            
            return True
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_priority_zones_geojson()
    exit(0 if success else 1)
