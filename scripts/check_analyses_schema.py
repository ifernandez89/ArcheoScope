import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect('postgresql://postgres:1464@localhost:5433/archeoscope_db')
    cols = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name='archaeological_candidate_analyses'")
    print('Columnas en archaeological_candidate_analyses:')
    for c in cols:
        print(f'  - {c["column_name"]}')
    await conn.close()

asyncio.run(check())
