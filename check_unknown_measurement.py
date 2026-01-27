#!/usr/bin/env python3
"""Verificar qué es la medición 'unknown'."""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check():
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    # Obtener las últimas 15 mediciones con más detalles
    measurements = await conn.fetch("""
        SELECT 
            instrument_name, 
            value, 
            data_mode,
            source,
            region_name,
            environment_type,
            measurement_timestamp,
            latitude,
            longitude
        FROM measurements 
        ORDER BY measurement_timestamp DESC 
        LIMIT 15
    """)
    
    print('\n🔬 ÚLTIMAS 15 MEDICIONES (con detalles):')
    print('='*100)
    for i, m in enumerate(measurements, 1):
        status = '✅' if m['data_mode'] != 'NO_DATA' else '❌'
        print(f"{i:2d}. {status} {m['instrument_name']:<30} = {m['value']:8.3f} ({m['data_mode']:<10})")
        print(f"     Source: {m['source']}")
        print(f"     Region: {m['region_name']}, Env: {m['environment_type']}")
        print(f"     Coords: ({m['latitude']:.4f}, {m['longitude']:.4f})")
        print(f"     Time: {m['measurement_timestamp']}")
        print()
    
    await conn.close()

asyncio.run(check())
