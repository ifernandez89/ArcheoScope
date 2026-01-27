#!/usr/bin/env python3
import asyncpg
import asyncio

async def clean():
    conn = await asyncpg.connect(
        host='localhost',
        port=5433,
        user='postgres',
        password='1464',
        database='archeoscope_db'
    )
    
    print("Limpiando tablas...")
    
    # Limpiar measurements
    result = await conn.execute('DELETE FROM measurements')
    print(f"  measurements: {result}")
    
    # Limpiar archaeological_candidates
    result = await conn.execute('DELETE FROM archaeological_candidates')
    print(f"  archaeological_candidates: {result}")
    
    # Limpiar archaeological_candidate_analyses
    result = await conn.execute('DELETE FROM archaeological_candidate_analyses')
    print(f"  archaeological_candidate_analyses: {result}")
    
    # Verificar
    count_m = await conn.fetchval('SELECT COUNT(*) FROM measurements')
    count_c = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidates')
    count_a = await conn.fetchval('SELECT COUNT(*) FROM archaeological_candidate_analyses')
    
    print("\nVerificación:")
    print(f"  measurements: {count_m} registros")
    print(f"  archaeological_candidates: {count_c} registros")
    print(f"  archaeological_candidate_analyses: {count_a} registros")
    
    print("\n[OK] Tablas limpiadas - listo para empezar de 0")
    
    await conn.close()

asyncio.run(clean())
