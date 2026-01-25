#!/usr/bin/env python3
"""
Verificar valores de environmentType en la base de datos
"""

import asyncio
import sys
from pathlib import Path

# Agregar backend al path
sys.path.append(str(Path(__file__).parent / "backend"))

from database import db

async def check_values():
    """Verificar valores de environmentType"""
    
    print("🔍 Verificando valores de environmentType en la base de datos...")
    
    await db.connect()
    
    # Query para ver valores únicos
    query = '''
        SELECT DISTINCT "environmentType", COUNT(*) as count
        FROM archaeological_sites
        GROUP BY "environmentType"
        ORDER BY count DESC
        LIMIT 20
    '''
    
    async with db.pool.acquire() as conn:
        rows = await conn.fetch(query)
    
    print(f"\nValores encontrados:")
    print("-" * 60)
    for row in rows:
        env_type = row['environmentType'] if row['environmentType'] else 'NULL'
        count = row['count']
        print(f"  {env_type:20s}: {count:,} sitios")
    
    await db.close()

if __name__ == "__main__":
    asyncio.run(check_values())
