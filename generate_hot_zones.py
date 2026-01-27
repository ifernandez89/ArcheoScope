#!/usr/bin/env python3
"""
Generar zonas calientes (hot zones) basadas en densidad de sitios arqueológicos
"""

import psycopg2
import os
import json
from dotenv import load_dotenv
from collections import defaultdict
import math

load_dotenv()

def calculate_grid_density(sites, grid_size=1.0):
    """
    Calcular densidad de sitios en una grilla
    
    Args:
        sites: Lista de (lat, lon)
        grid_size: Tamaño de celda en grados (default: 1° ≈ 111km)
    
    Returns:
        Dict con celdas y sus densidades
    """
    grid = defaultdict(int)
    
    for lat, lon in sites:
        # Redondear a la grilla
        grid_lat = math.floor(lat / grid_size) * grid_size
        grid_lon = math.floor(lon / grid_size) * grid_size
        
        grid[(grid_lat, grid_lon)] += 1
    
    return grid

def generate_hot_zones():
    """Generar zonas calientes desde la BD"""
    
    print("Conectando a BD...")
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    
    # Obtener todos los sitios
    print("Obteniendo sitios...")
    cur.execute('''
        SELECT latitude, longitude, name, country
        FROM archaeological_sites
        WHERE latitude IS NOT NULL 
          AND longitude IS NOT NULL
    ''')
    
    sites = cur.fetchall()
    print(f"Total sitios: {len(sites)}")
    
    # Calcular densidad en grilla de 1°
    print("Calculando densidad...")
    coords = [(lat, lon) for lat, lon, _, _ in sites]
    grid = calculate_grid_density(coords, grid_size=1.0)
    
    # Convertir a lista ordenada por densidad
    hot_zones = []
    for (grid_lat, grid_lon), count in grid.items():
        if count >= 10:  # Mínimo 10 sitios por celda
            hot_zones.append({
                'lat': grid_lat + 0.5,  # Centro de la celda
                'lon': grid_lon + 0.5,
                'density': count,
                'grid_size': 1.0,
                'priority': 'high' if count >= 100 else 'medium' if count >= 50 else 'low'
            })
    
    # Ordenar por densidad
    hot_zones.sort(key=lambda x: x['density'], reverse=True)
    
    print(f"\nZonas calientes generadas: {len(hot_zones)}")
    print(f"Top 10 zonas:")
    for i, zone in enumerate(hot_zones[:10], 1):
        print(f"  {i}. Lat: {zone['lat']:.1f}, Lon: {zone['lon']:.1f} - {zone['density']} sitios ({zone['priority']})")
    
    # Guardar a JSON
    output_file = 'hot_zones.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generated_at': '2026-01-26',
            'total_sites': len(sites),
            'total_zones': len(hot_zones),
            'grid_size_degrees': 1.0,
            'min_sites_per_zone': 10,
            'zones': hot_zones
        }, f, indent=2)
    
    print(f"\n✅ Zonas guardadas en: {output_file}")
    
    # Estadísticas por prioridad
    high = sum(1 for z in hot_zones if z['priority'] == 'high')
    medium = sum(1 for z in hot_zones if z['priority'] == 'medium')
    low = sum(1 for z in hot_zones if z['priority'] == 'low')
    
    print(f"\nPor prioridad:")
    print(f"  Alta (≥100 sitios): {high} zonas")
    print(f"  Media (50-99 sitios): {medium} zonas")
    print(f"  Baja (10-49 sitios): {low} zonas")
    
    cur.close()
    conn.close()
    
    return hot_zones

if __name__ == "__main__":
    hot_zones = generate_hot_zones()
