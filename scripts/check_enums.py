#!/usr/bin/env python3
"""Verificar ENUMs de archaeological_sites."""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_enums():
    """Verificar valores de ENUMs."""
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    # Obtener ENUMs
    enums = await conn.fetch("""
        SELECT t.typname as enum_name, e.enumlabel as enum_value
        FROM pg_type t 
        JOIN pg_enum e ON t.oid = e.enumtypid  
        WHERE t.typname IN ('EnvironmentType', 'SiteType', 'ConfidenceLevel', 'ExcavationStatus', 'PreservationStatus')
        ORDER BY t.typname, e.enumsortorder
    """)
    
    print("\n📋 ENUMS DE archaeological_sites:")
    print("="*80)
    
    current_enum = None
    for r in enums:
        if r['enum_name'] != current_enum:
            current_enum = r['enum_name']
            print(f"\n{current_enum}:")
        print(f"  - {r['enum_value']}")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_enums())
