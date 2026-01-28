#!/usr/bin/env python3
"""Verificar cuántos sitios arqueológicos hay en la BD."""

import asyncpg
import asyncio

async def check_count():
    """Contar sitios en la BD."""
    try:
        conn = await asyncpg.connect(
            'postgresql://postgres:postgres@localhost:5432/archeoscope'
        )
        
        # Total de sitios
        total = await conn.fetchval('SELECT COUNT(*) FROM archaeological_sites')
        print(f"📊 Total sitios arqueológicos: {total:,}")
        
        # Por tipo de sitio
        by_type = await conn.fetch("""
            SELECT "siteType", COUNT(*) as count
            FROM archaeological_sites
            GROUP BY "siteType"
            ORDER BY count DESC
        """)
        
        print(f"\n📋 Por tipo de sitio:")
        for row in by_type:
            print(f"   {row['siteType']}: {row['count']:,}")
        
        # Por país (top 10)
        by_country = await conn.fetch("""
            SELECT country, COUNT(*) as count
            FROM archaeological_sites
            WHERE country IS NOT NULL
            GROUP BY country
            ORDER BY count DESC
            LIMIT 10
        """)
        
        print(f"\n🌍 Top 10 países:")
        for row in by_country:
            print(f"   {row['country']}: {row['count']:,}")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_count())
