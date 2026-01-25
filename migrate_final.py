#!/usr/bin/env python3
"""
Migración final con manejo de duplicados
"""

import json
import asyncio
import asyncpg
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

async def migrate():
    print("Conectando...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    print("Limpiando tabla...")
    await conn.execute('TRUNCATE TABLE archaeological_sites CASCADE')
    
    print("Cargando datos...")
    with open("harvested_complete.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sites = data['sites']
    print(f"Total: {len(sites):,}")
    
    print("\nInsertando en lotes de 1000...")
    inserted = 0
    skipped = 0
    
    for i in range(0, len(sites), 1000):
        batch = sites[i:i+1000]
        batch_num = (i // 1000) + 1
        total_batches = (len(sites) + 999) // 1000
        
        for site in batch:
            try:
                name = site.get('name', 'Unknown')[:255]
                lat = float(site.get('latitude', 0))
                lon = float(site.get('longitude', 0))
                
                if lat == 0 and lon == 0:
                    skipped += 1
                    continue
                
                import re
                slug = name.lower()
                slug = re.sub(r'[^a-z0-9\s-]', '', slug)
                slug = re.sub(r'\s+', '-', slug)[:200]
                site_id = site.get('wikidata_id') or site.get('osm_id') or str(inserted)
                slug = f"{slug}-{site_id}-{inserted}"[:255]
                
                country = site.get('country', 'Unknown')[:100]
                period = site.get('period', '')[:255] if site.get('period') else None
                desc = site.get('description', '')[:1000] if site.get('description') else None
                
                await conn.execute('''
                    INSERT INTO archaeological_sites 
                    (name, slug, "environmentType", "siteType", "confidenceLevel",
                     latitude, longitude, country, period, description)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    ON CONFLICT (slug) DO NOTHING
                ''', name, slug, 'UNKNOWN', 'UNKNOWN', 'MODERATE',
                     lat, lon, country, period, desc)
                
                inserted += 1
                
            except:
                skipped += 1
        
        print(f"  Lote {batch_num}/{total_batches} - Insertados: {inserted:,}, Omitidos: {skipped:,}")
    
    count = await conn.fetchval('SELECT COUNT(*) FROM archaeological_sites')
    await conn.close()
    
    print(f"\nCOMPLETADO!")
    print(f"Total en DB: {count:,}")

if __name__ == "__main__":
    asyncio.run(migrate())
