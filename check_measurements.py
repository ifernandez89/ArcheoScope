#!/usr/bin/env python3
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check():
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    measurements = await conn.fetch("""
        SELECT instrument_name, value, data_mode 
        FROM measurements 
        ORDER BY measurement_timestamp DESC 
        LIMIT 10
    """)
    
    print('\n🔬 ÚLTIMAS MEDICIONES:')
    print('='*60)
    for m in measurements:
        status = '✅' if m['data_mode'] != 'NO_DATA' else '❌'
        print(f"  {status} {m['instrument_name']:<30} = {m['value']:.3f} ({m['data_mode']})")
    
    await conn.close()

asyncio.run(check())
