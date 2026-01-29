#!/usr/bin/env python3
"""Verificar tablas en la base de datos."""

import asyncio
import asyncpg

async def check_tables():
    conn = await asyncpg.connect('postgresql://postgres:Xiphos2024!@localhost:5432/archeoscope')
    
    # Listar tablas
    tables = await conn.fetch("""
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname='public' 
        ORDER BY tablename
    """)
    
    print("📊 Tablas en la base de datos:")
    print()
    for t in tables:
        print(f"  - {t['tablename']}")
    
    print()
    print("🔍 Verificando tabla 'analyses':")
    
    # Verificar si existe tabla analyses
    exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename = 'analyses'
        )
    """)
    
    if exists:
        # Contar registros
        count = await conn.fetchval("SELECT COUNT(*) FROM analyses")
        print(f"  ✅ Tabla 'analyses' existe con {count} registros")
        
        # Mostrar últimos 3
        if count > 0:
            recent = await conn.fetch("""
                SELECT id, region_name, created_at, ess_volumetrico 
                FROM analyses 
                ORDER BY created_at DESC 
                LIMIT 3
            """)
            print()
            print("  Últimos 3 análisis:")
            for r in recent:
                print(f"    - {r['region_name']}: ESS={r['ess_volumetrico']:.3f} ({r['created_at']})")
    else:
        print("  ❌ Tabla 'analyses' NO existe")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_tables())
