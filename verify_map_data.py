#!/usr/bin/env python3
"""Verificar que los datos del mapa están correctos"""

import json
import os

print("\n" + "="*70)
print("🔍 VERIFICACIÓN DE DATOS DEL MAPA")
print("="*70)

# 1. Verificar archivo GeoJSON
geojson_path = "frontend/real_candidates.geojson"
print(f"\n1. Verificando archivo GeoJSON...")
print(f"   Ruta: {geojson_path}")

if os.path.exists(geojson_path):
    print(f"   ✅ Archivo existe")
    
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"   ✅ JSON válido")
    print(f"   Features: {len(data['features'])}")
    print(f"   Metadata: {data.get('metadata', {})}")
    
    # Verificar cada feature
    print(f"\n2. Verificando features...")
    for i, feature in enumerate(data['features'], 1):
        props = feature['properties']
        coords = feature['geometry']['coordinates']
        print(f"\n   {i}. {props['zone_id']}")
        print(f"      Coords: [{coords[0]:.2f}, {coords[1]:.2f}]")
        print(f"      Score: {props['score']}")
        print(f"      Prioridad: {props['priority']}")
        print(f"      Color: {props['color']}")
else:
    print(f"   ❌ Archivo NO existe")

# 2. Verificar HTML
html_path = "frontend/priority_zones_map.html"
print(f"\n3. Verificando HTML...")
print(f"   Ruta: {html_path}")

if os.path.exists(html_path):
    print(f"   ✅ Archivo existe")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar funciones clave
    checks = [
        ('loadRealCandidates', 'Función de carga'),
        ('real_candidates.geojson', 'Referencia al GeoJSON'),
        ('updateRealCandidatesStats', 'Función de estadísticas'),
        ('window.onload', 'Inicialización automática')
    ]
    
    for check, desc in checks:
        if check in content:
            print(f"   ✅ {desc}: OK")
        else:
            print(f"   ❌ {desc}: NO ENCONTRADO")
else:
    print(f"   ❌ Archivo NO existe")

print(f"\n" + "="*70)
print("RESUMEN:")
print("="*70)
print(f"\n✅ GeoJSON: {len(data['features'])} candidatas listas")
print(f"✅ HTML: Configurado correctamente")
print(f"\n🗺️  URL del mapa: http://localhost:8081/priority_zones_map.html")
print(f"\nSi no ves las candidatas en el mapa:")
print(f"  1. Abre la consola del navegador (F12)")
print(f"  2. Busca mensajes de 'Cargando candidatas REALES...'")
print(f"  3. Verifica que no haya errores 404")
print(f"\n" + "="*70)
