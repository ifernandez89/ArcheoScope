#!/usr/bin/env python3
"""
Verificar esquema de archaeological_candidate_analyses
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_schema():
    """Verificar esquema de la tabla."""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL no configurada")
        return
    
    conn = await asyncpg.connect(database_url)
    
    try:
        # Obtener columnas de la tabla
        columns = await conn.fetch("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'archaeological_candidate_analyses'
            ORDER BY ordinal_position
        """)
        
        print("="*80)
        print("ESQUEMA: archaeological_candidate_analyses")
        print("="*80)
        
        has_coordinates = False
        
        for col in columns:
            print(f"  - {col['column_name']:<30} {col['data_type']:<20} {'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'}")
            if col['column_name'] in ['latitude', 'longitude', 'center_lat', 'center_lon']:
                has_coordinates = True
        
        print("\n" + "="*80)
        if has_coordinates:
            print("✅ La tabla TIENE columnas de coordenadas")
        else:
            print("❌ La tabla NO TIENE columnas de coordenadas")
            print("\n💡 SOLUCIÓN: Agregar columnas latitude, longitude")
        print("="*80)
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(check_schema())
