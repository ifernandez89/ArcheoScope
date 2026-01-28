#!/usr/bin/env python3
import asyncpg
import asyncio

async def check():
    conn = await asyncpg.connect(
        host='localhost',
        port=5433,
        user='postgres',
        password='1464',
        database='archeoscope_db'
    )
    
    tables = await conn.fetch("""
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        ORDER BY tablename
    """)
    
    print("="*70)
    print("TABLAS EN archeoscope_db")
    print("="*70)
    
    for t in tables:
        table_name = t['tablename']
        count = await conn.fetchval(f'SELECT COUNT(*) FROM "{table_name}"')
        print(f"{table_name}: {count} registros")
    
    print("\n" + "="*70)
    print("VERIFICANDO TABLAS CLAVE")
    print("="*70)
    
    # Verificar measurements
    if 'measurements' in [t['tablename'] for t in tables]:
        print("\n[OK] Tabla 'measurements' existe")
        cols = await conn.fetch("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'measurements' 
            ORDER BY ordinal_position LIMIT 10
        """)
        print("  Columnas:", [c['column_name'] for c in cols])
    else:
        print("\n[FALTA] Tabla 'measurements' NO existe")
    
    # Verificar archaeological_candidates
    if 'archaeological_candidates' in [t['tablename'] for t in tables]:
        print("\n[OK] Tabla 'archaeological_candidates' existe")
        cols = await conn.fetch("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'archaeological_candidates' 
            ORDER BY ordinal_position LIMIT 10
        """)
        print("  Columnas:", [c['column_name'] for c in cols])
    else:
        print("\n[FALTA] Tabla 'archaeological_candidates' NO existe")
    
    await conn.close()

asyncio.run(check())
