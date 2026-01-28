#!/usr/bin/env python3
"""
Aplicar migración: agregar analysis_id a measurements
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
        print("APLICANDO MIGRACIÓN: Agregar analysis_id a measurements")
        print("="*80)
        
        # Leer SQL
        with open('add_analysis_id_to_measurements.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Ejecutar
        await conn.execute(sql)
        
        print("\n✅ Migración aplicada exitosamente")
        
        # Verificar columna
        columns = await conn.fetch("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'measurements'
              AND column_name = 'analysis_id'
        """)
        
        if columns:
            print(f"\n📊 Columna agregada:")
            for col in columns:
                print(f"  ✅ {col['column_name']:<20} ({col['data_type']})")
        
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
