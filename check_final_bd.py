#!/usr/bin/env python3
"""Verificación final de registros en BD."""

import asyncio
import asyncpg

async def check_bd():
    conn = await asyncpg.connect('postgresql://postgres:1464@localhost:5433/archeoscope_db')
    
    count = await conn.fetchval('SELECT COUNT(*) FROM detection_history')
    print(f'✅ Total registros en BD: {count}')
    print()
    
    records = await conn.fetch('''
        SELECT "regionName", "archaeologicalProbability", "detectionDate", 
               "environmentDetected", "confidenceLevel"
        FROM detection_history 
        ORDER BY "detectionDate" DESC 
        LIMIT 6
    ''')
    
    print('📊 ÚLTIMOS 6 REGISTROS:')
    print('='*80)
    for i, r in enumerate(records, 1):
        print(f'{i}. {r["regionName"]}')
        print(f'   ESS: {r["archaeologicalProbability"]:.3f}')
        print(f'   Ambiente: {r["environmentDetected"]}')
        print(f'   Confianza: {r["confidenceLevel"]}')
        print(f'   Fecha: {r["detectionDate"].strftime("%Y-%m-%d %H:%M")}')
        print()
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(check_bd())
