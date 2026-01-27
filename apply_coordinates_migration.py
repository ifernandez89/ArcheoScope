#!/usr/bin/env python3
"""
Aplicar migración: agregar coordenadas a archaeological_candidate_analyses
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def apply_migration():
    """Aplicar migración SQL."""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL no configurada")
        return False
    
    conn = await asyncpg.connect(database_url)
    
    try:
        print("="*80)
        print("APLICANDO MIGRACIÓN: Agregar coordenadas a analyses")
        print("="*80)
        
        # Leer SQL
        with open('add_coordinates_to_analyses.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Ejecutar
        await conn.execute(sql)
        
        print("\n✅ Migración aplicada exitosamente")
        
        # Verificar columnas
        columns = await conn.fetch("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'archaeological_candidate_analyses'
              AND column_name IN ('latitude', 'longitude', 'lat_min', 'lat_max', 'lon_min', 'lon_max')
            ORDER BY column_name
        """)
        
        print("\n📊 Columnas agregadas:")
        for col in columns:
            print(f"  ✅ {col['column_name']:<15} ({col['data_type']})")
        
        print("\n" + "="*80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error aplicando migración: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await conn.close()

if __name__ == "__main__":
    success = asyncio.run(apply_migration())
    exit(0 if success else 1)
