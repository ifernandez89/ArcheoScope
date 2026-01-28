#!/usr/bin/env python3
"""Verificar esquema de tabla archaeological_candidate_analyses."""

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
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'archaeological_candidate_analyses'
        ORDER BY ordinal_position
    """)
    
    print("\n📋 ESQUEMA ACTUAL de archaeological_candidate_analyses:")
    print("="*60)
    for r in cols:
        nullable = "NULL" if r['is_nullable'] == 'YES' else "NOT NULL"
        print(f"  {r['column_name']:<30} {r['data_type']:<15} {nullable}")
    
    print("\n" + "="*60)
    print(f"Total columnas: {len(cols)}")
    
    # Verificar si existe anomaly_score
    has_anomaly = any(r['column_name'] == 'anomaly_score' for r in cols)
    print(f"\n❓ ¿Tiene anomaly_score? {'✅ SÍ' if has_anomaly else '❌ NO'}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_schema())
