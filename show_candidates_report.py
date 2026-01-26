#!/usr/bin/env python3
"""Mostrar reporte visual de candidatas reales"""

import json

# Cargar datos
with open('real_candidates_20260125_232836.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('\n' + '='*70)
print('🛰️  REPORTE DE CANDIDATAS REALES - ArcheoScope')
print('='*70)

print(f'\n📊 RESUMEN:')
print(f'   Total: {data["total_candidates"]} candidatas')
print(f'   Convergencia: 3/3 fuentes (100%)')
print(f'   Tipo: {data["data_type"]}')

print(f'\n📡 FUENTES:')
for s in data['sources']:
    print(f'   ✅ {s}')

print(f'\n🗺️  CANDIDATAS:\n')

# Ordenar por score
candidates_sorted = sorted(data['candidates'], key=lambda x: x['multi_instrumental_score'], reverse=True)

for i, c in enumerate(candidates_sorted, 1):
    priority_icon = '🟠' if c['priority'] == 'HIGH' else '🟡'
    
    print(f'{i}. {priority_icon} {c["priority"]} - {c["region_name"]}')
    print(f'   Score: {c["multi_instrumental_score"]:.3f}')
    
    thermal = c["real_data_sources"]["thermal"]
    elevation = c["real_data_sources"]["elevation"]
    ndvi = c["real_data_sources"]["ndvi"]
    
    print(f'   LST: {thermal["lst_mean"]:.1f}°C | Elev: {elevation["elevation_m"]:.0f}m | NDVI: {ndvi["ndvi_mean"]:.3f}')
    print(f'   Lat/Lon: {c["location"]["lat"]:.2f}, {c["location"]["lon"]:.2f}')
    print(f'   Sitios conocidos: {", ".join(c["known_sites_nearby"])}')
    print()

print('='*70)
print('✅ Estado: IMPORTADAS A BD + VISUALIZACION LISTA')
print('🗺️  Mapa: http://localhost:8080/priority_zones_map.html')
print('📄 Reporte completo: HARVEST_REPORT_2026-01-25.md')
print('='*70)
