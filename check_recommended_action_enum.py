import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect('postgresql://postgres:1464@localhost:5433/archeoscope_db')
    result = await conn.fetch("SELECT unnest(enum_range(NULL::recommended_action))::text as value")
    print('Valores válidos para recommended_action:')
    for r in result:
        print(f'  - {r["value"]}')
    await conn.close()

asyncio.run(check())
