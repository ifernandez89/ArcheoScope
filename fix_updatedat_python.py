#!/usr/bin/env python3
"""
Arreglar el campo updatedAt para que tenga default
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

async def fix_updatedat():
    print("Conectando a PostgreSQL...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    print("Ejecutando ALTER TABLE para updatedAt...")
    await conn.execute('''
        ALTER TABLE archaeological_sites 
        ALTER COLUMN "updatedAt" SET DEFAULT CURRENT_TIMESTAMP
    ''')
    
    print("Verificando...")
    result = await conn.fetch('''
        SELECT column_name, column_default 
        FROM information_schema.columns 
        WHERE table_name = 'archaeological_sites' 
        AND column_name IN ('id', 'createdAt', 'updatedAt')
    ''')
    
    print("\nDefaults actuales:")
    for row in result:
        print(f"  {row['column_name']}: {row['column_default']}")
    
    await conn.close()
    print("\nListo! Ahora ejecuta: python scripts/migrate_harvested_to_postgres.py")

if __name__ == "__main__":
    asyncio.run(fix_updatedat())
