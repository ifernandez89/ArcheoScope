#!/usr/bin/env python3
"""
Test análisis de coordenadas de Giza
"""

import requests
import json

# Coordenadas de Giza (Pirámides)
lat = 29.975
lon = 31.138

# Crear región pequeña alrededor del punto
data = {
    "lat_min": lat - 0.01,
    "lat_max": lat + 0.01,
    "lon_min": lon - 0.01,
    "lon_max": lon + 0.01,
    "region_name": "Giza Pyramids Test"
}

print("=" * 60)
print("ANÁLISIS DE COORDENADAS DE GIZA")
print("=" * 60)
print(f"Coordenadas centrales: {lat}, {lon}")
print(f"Región: Pirámides de Giza, Egipto")
print(f"Área: ~2.5 km²")
print("")
print("Esta es una de las zonas arqueológicas más importantes del mundo.")
print("Debería detectar:")
print("  - Estructuras monumentales conocidas")
print("  - Contexto arqueológico bien documentado")
print("  - Datos de alta calidad disponibles")
print("")
print("Enviando solicitud al backend...")
print("=" * 60)

try:
    response = requests.post(
        'http://localhost:8002/analyze',
        json=data,
        timeout=60
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n✅ ANÁLISIS COMPLETADO")
        print("=" * 60)
        
        # Mostrar información clave
        region_info = result.get('region_info', {})
        print(f"\nTipo de análisis: {region_info.get('analysis_type', 'N/A')}")
        
        # Verificar si hay contexto de agua/hielo
        if 'water_context' in region_info:
            print("\n⚠️ PROBLEMA: Sistema detectó AGUA")
            print(f"Tipo: {region_info['water_context'].get('water_type')}")
            print("Esto es INCORRECTO para Giza (zona desértica)")
            
        if 'ice_context' in region_info:
            print("\n⚠️ PROBLEMA: Sistema detectó HIELO")
            print("Esto es INCORRECTO para Giza (zona desértica)")
        
        # Mostrar resultados estadísticos
        stats = result.get('statistical_results', {})
        print(f"\nAnomalías detectadas: {stats.get('total_anomalies', 'N/A')}")
        
        # Verificar validación arqueológica
        if 'real_archaeological_validation' in result:
            validation = result['real_archaeological_validation']
            overlapping = validation.get('overlapping_known_sites', [])
            nearby = validation.get('nearby_known_sites', [])
            
            print(f"\n📍 Sitios conocidos solapados: {len(overlapping)}")
            print(f"📍 Sitios conocidos cercanos: {len(nearby)}")
            
            if overlapping:
                print("\nSitios solapados:")
                for site in overlapping[:3]:
                    print(f"  - {site.get('name')}")
        
        # Guardar resultado completo
        with open('giza_analysis_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("\n💾 Resultado completo guardado en: giza_analysis_result.json")
        
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ EXCEPCIÓN: {e}")
    import traceback
    traceback.print_exc()
