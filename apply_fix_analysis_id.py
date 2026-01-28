#!/usr/bin/env python3
"""
Corregir tipo de analysis_id
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def apply_fix():
    """Aplicar fix."""
    
    database_url = os.getenv("DATABASE_URL")
    conn = await asyncpg.connect(database_url)
    
    try:
        print("Corrigiendo tipo de analysis_id...")
        
        with open('fix_analysis_id_type.sql', 'r') as f:
            sql = f.read()
        
        await conn.execute(sql)
        
        print("✅ Fix aplicado")
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(apply_fix())
