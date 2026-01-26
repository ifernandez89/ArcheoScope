#!/usr/bin/env python3
"""
Verificar qué países tienen sitios en la base de datos
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'backend'))

from database import db

async def check_countries():
    """Verificar distribución de sitios por país"""
    
    print("🌍 Verificando distribución de sitios por país")
    print("=" * 80)
    
    await db.connect()
    
    # Query para obtener países
    async with db.pool.acquire() as conn:
        countries = await conn.fetch('''
            SELECT 
                country,
                COUNT(*) as count
            FROM archaeological_sites
            WHERE country IS NOT NULL AND country != ''
            GROUP BY country
            ORDER BY count DESC
            LIMIT 50
        ''')
        
        print(f"\n📊 Top 50 países con más sitios:")
        print("-" * 80)
        
        total_with_country = 0
        for i, row in enumerate(countries):
            print(f"{i+1:3}. {row['country']:30} {row['count']:>6,} sitios")
            total_with_country += row['count']
        
        # Sitios sin país
        no_country = await conn.fetchval('''
            SELECT COUNT(*)
            FROM archaeological_sites
            WHERE country IS NULL OR country = ''
        ''')
        
        total = await conn.fetchval('SELECT COUNT(*) FROM archaeological_sites')
        
        print("\n" + "=" * 80)
        print(f"📊 Resumen:")
        print(f"   Total sitios: {total:,}")
        print(f"   Con país asignado: {total_with_country:,} ({total_with_country/total*100:.1f}%)")
        print(f"   Sin país: {no_country:,} ({no_country/total*100:.1f}%)")
        
        # Buscar sitios sudamericanos
        print("\n" + "=" * 80)
        print("🌎 Buscando sitios sudamericanos...")
        
        south_american_countries = ['Brazil', 'Brasil', 'Peru', 'Perú', 'Colombia', 
                                   'Ecuador', 'Bolivia', 'Chile', 'Argentina', 
                                   'Venezuela', 'Guyana', 'Suriname']
        
        for country in south_american_countries:
            count = await conn.fetchval('''
                SELECT COUNT(*)
                FROM archaeological_sites
                WHERE country ILIKE $1
            ''', f'%{country}%')
            
            if count > 0:
                print(f"   {country}: {count:,} sitios")
        
        # Buscar por coordenadas (Sudamérica: lat -60 a 15, lon -82 a -34)
        print("\n" + "=" * 80)
        print("📍 Buscando por coordenadas (Sudamérica)...")
        
        south_america_sites = await conn.fetchval('''
            SELECT COUNT(*)
            FROM archaeological_sites
            WHERE latitude BETWEEN -60 AND 15
            AND longitude BETWEEN -82 AND -34
        ''')
        
        print(f"   Sitios en rango de coordenadas sudamericanas: {south_america_sites:,}")
        
        if south_america_sites > 0:
            # Mostrar algunos ejemplos
            examples = await conn.fetch('''
                SELECT name, latitude, longitude, country, "siteType"
                FROM archaeological_sites
                WHERE latitude BETWEEN -60 AND 15
                AND longitude BETWEEN -82 AND -34
                LIMIT 20
            ''')
            
            print(f"\n   Ejemplos de sitios sudamericanos:")
            for site in examples:
                print(f"   - {site['name']} ({site['latitude']:.2f}, {site['longitude']:.2f}) - {site['country'] or 'Sin país'}")
    
    await db.close()
    
    print("\n" + "=" * 80)
    if south_america_sites == 0:
        print("❌ PROBLEMA CRÍTICO: No hay sitios sudamericanos en la base de datos")
        print("\n💡 Solución:")
        print("   El harvesting debe incluir sitios de Wikidata/OSM de Sudamérica")
        print("   Especialmente importantes:")
        print("   - Geoglifos del Acre (Brasil)")
        print("   - Sitios de terra preta (Amazonía)")
        print("   - Machu Picchu y sitios incas (Perú)")
        print("   - Tiwanaku (Bolivia)")
        print("   - Líneas de Nazca (Perú)")
    else:
        print(f"✅ Hay {south_america_sites:,} sitios sudamericanos")
        print("   Pero pueden no estar en la región específica de Amazonía brasileña")

if __name__ == "__main__":
    asyncio.run(check_countries())
