import asyncpg, asyncio

async def check():
    c = await asyncpg.connect(host='localhost', port=5433, user='postgres', password='1464', database='archeoscope_db')
    cols = await c.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = 'measurements' ORDER BY ordinal_position")
    print("Columnas en measurements:")
    for col in cols:
        print(f"  - {col['column_name']}")
    await c.close()

asyncio.run(check())
