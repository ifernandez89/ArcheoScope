#!/usr/bin/env python3
"""
Buscar sitios específicamente en la región amazónica
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'backend'))

from database import db

async def find_amazonia():
    """Buscar sitios en diferentes regiones amazónicas"""
    
    print("🌳 Buscando sitios en la región amazónica")
    print("=" * 80)
    
    await db.connect()
    
    # Diferentes regiones de la Amazonía
    regions = [
        {"name": "Amazonía Occidental (Brasil)", "lat_min": -5, "lat_max": -3, "lon_min": -62, "lon_max": -60},
        {"name": "Amazonía Central (Brasil)", "lat_min": -4, "lat_max": -2, "lon_min": -61, "lon_max": -59},
        {"name": "Acre (Brasil) - Geoglifos", "lat_min": -11, "lat_max": -9, "lon_min": -70, "lon_max": -68},
        {"name": "Rondônia (Brasil)", "lat_min": -12, "lat_max": -8, "lon_min": -64, "lon_max": -60},
        {"name": "Pará (Brasil)", "lat_min": -8, "lat_max": -1, "lon_min": -56, "lon_max": -48},
        {"name": "Amazonía Peruana", "lat_min": -13, "lat_max": -3, "lon_min": -76, "lon_max": -70},
        {"name": "Amazonía Colombiana", "lat_min": -4, "lat_max": 4, "lon_min": -75, "lon_max": -67},
        {"name": "Amazonía Ecuatoriana", "lat_min": -5, "lat_max": 0, "lon_min": -78, "lon_max": -75},
    ]
    
    async with db.pool.acquire() as conn:
        for region in regions:
            count = await conn.fetchval('''
                SELECT COUNT(*)
                FROM archaeological_sites
                WHERE latitude BETWEEN $1 AND $2
                AND longitude BETWEEN $3 AND $4
            ''', region['lat_min'], region['lat_max'], region['lon_min'], region['lon_max'])
            
            print(f"\n📍 {region['name']}")
            print(f"   Coordenadas: {region['lat_min']} a {region['lat_max']} lat, {region['lon_min']} a {region['lon_max']} lon")
            print(f"   Sitios encontrados: {count}")
            
            if count > 0:
                # Mostrar ejemplos
                sites = await conn.fetch('''
                    SELECT name, latitude, longitude, country, "siteType"
                    FROM archaeological_sites
                    WHERE latitude BETWEEN $1 AND $2
                    AND longitude BETWEEN $3 AND $4
                    LIMIT 5
                ''', region['lat_min'], region['lat_max'], region['lon_min'], region['lon_max'])
                
                print(f"   Ejemplos:")
                for site in sites:
                    print(f"   - {site['name']} ({site['latitude']:.4f}, {site['longitude']:.4f})")
    
    # Buscar sitios con nombres relacionados a Amazonía
    print("\n" + "=" * 80)
    print("🔍 Buscando por nombres relacionados...")
    
    keywords = ['Amazon', 'Amazonia', 'Acre', 'Geoglyph', 'Terra Preta', 'Tapajos', 
                'Xingu', 'Marajó', 'Santarém', 'Manaus']
    
    async with db.pool.acquire() as conn:
        for keyword in keywords:
            count = await conn.fetchval('''
                SELECT COUNT(*)
                FROM archaeological_sites
                WHERE name ILIKE $1
            ''', f'%{keyword}%')
            
            if count > 0:
                print(f"\n   '{keyword}': {count} sitios")
                
                sites = await conn.fetch('''
                    SELECT name, latitude, longitude, country
                    FROM archaeological_sites
                    WHERE name ILIKE $1
                    LIMIT 3
                ''', f'%{keyword}%')
                
                for site in sites:
                    print(f"   - {site['name']} ({site['latitude']:.4f}, {site['longitude']:.4f})")
    
    await db.close()
    
    print("\n" + "=" * 80)
    print("💡 Conclusión:")
    print("   Si no hay sitios en estas regiones, el problema es del harvesting")
    print("   Necesitamos agregar sitios amazónicos manualmente o mejorar el harvesting")

if __name__ == "__main__":
    asyncio.run(find_amazonia())
