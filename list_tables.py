#!/usr/bin/env python3
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def list_tables():
    database_url = os.getenv('DATABASE_URL')
    pool = await asyncpg.create_pool(database_url)
    
    async with pool.acquire() as conn:
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        print("\n📋 TABLAS EN LA BASE DE DATOS:")
        print("="*60)
        for row in tables:
            print(f"  - {row['table_name']}")
        print("="*60)
    
    await pool.close()

asyncio.run(list_tables())
