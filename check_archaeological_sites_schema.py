#!/usr/bin/env python3
"""Verificar estructura de la tabla archaeological_sites (80k registros)."""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_schema():
    """Verificar estructura completa de archaeological_sites."""
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    # Obtener columnas
    cols = await conn.fetch("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'archaeological_sites'
        ORDER BY ordinal_position
    """)
    
    print("\n📋 ESTRUCTURA DE archaeological_sites (80k registros):")
    print("="*80)
    for r in cols:
        nullable = "NULL" if r['is_nullable'] == 'YES' else "NOT NULL"
        default = f"DEFAULT {r['column_default']}" if r['column_default'] else ""
        print(f"  {r['column_name']:<35} {r['data_type']:<20} {nullable:<10} {default}")
    
    print("\n" + "="*80)
    print(f"Total columnas: {len(cols)}")
    
    # Contar registros
    count = await conn.fetchval("SELECT COUNT(*) FROM archaeological_sites")
    print(f"Total registros: {count:,}")
    
    # Mostrar ejemplo de registro
    sample = await conn.fetchrow("SELECT * FROM archaeological_sites LIMIT 1")
    if sample:
        print("\n📄 EJEMPLO DE REGISTRO:")
        print("="*80)
        for key, value in dict(sample).items():
            print(f"  {key:<35} = {value}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_schema())
