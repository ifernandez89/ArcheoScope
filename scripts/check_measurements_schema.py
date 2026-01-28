#!/usr/bin/env python3
"""Verificar esquema de tabla measurements."""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_schema():
    """Verificar columnas de la tabla."""
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    # Obtener columnas
    cols = await conn.fetch("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'measurements'
        ORDER BY ordinal_position
    """)
    
    print("\n📋 ESQUEMA ACTUAL de measurements:")
    print("="*80)
    for r in cols:
        nullable = "NULL" if r['is_nullable'] == 'YES' else "NOT NULL"
        default = f"DEFAULT {r['column_default']}" if r['column_default'] else ""
        print(f"  {r['column_name']:<30} {r['data_type']:<20} {nullable:<10} {default}")
    
    print("\n" + "="*80)
    print(f"Total columnas: {len(cols)}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_schema())
