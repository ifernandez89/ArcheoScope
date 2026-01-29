#!/usr/bin/env python3
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_schema():
    database_url = os.getenv('DATABASE_URL')
    pool = await asyncpg.create_pool(database_url)
    
    async with pool.acquire() as conn:
        columns = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'archaeological_candidate_analyses'
            ORDER BY ordinal_position
        """)
        
        print("\n📋 ESQUEMA DE archaeological_candidate_analyses:")
        print("="*80)
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"  {col['column_name']:30} {col['data_type']:20} {nullable:10}{default}")
        print("="*80)
    
    await pool.close()

asyncio.run(check_schema())
