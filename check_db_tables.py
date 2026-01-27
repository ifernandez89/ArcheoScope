#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def check():
    from database import ArcheoScopeDB
    
    db = ArcheoScopeDB()
    await db.connect()
    
    # Listar todas las tablas
    tables = await db.pool.fetch("""
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        ORDER BY tablename
    """)
    
    print("="*70)
    print("TABLAS EN BASE DE DATOS")
    print("="*70)
    
    for t in tables:
        table_name = t['tablename']
        
        # Contar registros
        count_result = await db.pool.fetchrow(f'SELECT COUNT(*) as count FROM "{table_name}"')
        count = count_result['count']
        
        print(f"\n{table_name}: {count} registros")
        
        # Mostrar estructura si es tabla relevante
        if table_name in ['measurements', 'archaeological_candidates', 'archaeological_sites']:
            columns = await db.pool.fetch(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            print("  Columnas:")
            for col in columns[:10]:  # Primeras 10 columnas
                print(f"    - {col['column_name']}: {col['data_type']}")
    
    await db.close()
    
    print("\n" + "="*70)

asyncio.run(check())
