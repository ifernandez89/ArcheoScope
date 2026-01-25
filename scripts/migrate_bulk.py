#!/usr/bin/env python3
"""
Migración RÁPIDA usando COPY bulk insert
"""

import json
import asyncio
import asyncpg
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

async def migrate_bulk():
    print("Conectando a PostgreSQL...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    print("Cargando datos...")
    json_path = Path("harvested_complete.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sites = data.get('sites', [])
    print(f"Total sitios: {len(sites):,}")
    
    print("\nPreparando datos para bulk insert...")
    records = []
    
    for i, site in enumerate(sites):
        if i % 10000 == 0 and i > 0:
            print(f"  Procesados {i:,}/{len(sites):,}...")
        
        try:
            name = site.get('name', 'Unknown')[:255]
            latitude = float(site.get('latitude', 0))
            longitude = float(site.get('longitude', 0))
            
            if latitude == 0 and longitude == 0:
                continue
            
            # Crear slug simple
            import re
            slug = name.lower()
            slug = re.sub(r'[^a-z0-9\s-]', '', slug)
            slug = re.sub(r'\s+', '-', slug)
            slug = slug[:200]
            site_id = site.get('wikidata_id') or site.get('osm_id') or str(i)
            slug = f"{slug}-{site_id}"[:255]
            
            country = site.get('country', 'Unknown')[:100]
            period = site.get('period', '')[:255] if site.get('period') else None
            description = site.get('description', '')[:1000] if site.get('description') else None
            
            records.append((
                name,
                slug,
                'UNKNOWN',  # environmentType
                'UNKNOWN',  # siteType
                'MODERATE',  # confidenceLevel
                latitude,
                longitude,
                country,
                period,
                description
            ))
            
        except Exception as e:
            continue
    
    print(f"\nRegistros válidos: {len(records):,}")
    print("Insertando en la base de datos (esto puede tardar 1-2 minutos)...")
    
    # Usar COPY para inserción masiva ultra-rápida
    await conn.copy_records_to_table(
        'archaeological_sites',
        records=records,
        columns=[
            'name', 'slug', 
            'environmentType', 'siteType', 'confidenceLevel',
            'latitude', 'longitude',
            'country', 'period', 'description'
        ]
    )
    
    # Verificar
    count = await conn.fetchval('SELECT COUNT(*) FROM archaeological_sites')
    print(f"\nTotal en base de datos: {count:,}")
    
    await conn.close()
    print("\nMIGRACION COMPLETADA!")

if __name__ == "__main__":
    asyncio.run(migrate_bulk())
