#!/usr/bin/env python3
"""
Aplicar migración: agregar campo de explicación científica
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
        print("APLICANDO MIGRACIÓN: Agregar explicación científica")
        print("="*80)
        
        # Leer SQL
        with open('add_explanation_to_analyses.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Ejecutar
        await conn.execute(sql)
        
        print("\n✅ Migración aplicada exitosamente")
        
        # Verificar columnas
        columns = await conn.fetch("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_name = 'archaeological_candidate_analyses'
              AND column_name IN ('scientific_explanation', 'explanation_type')
            ORDER BY column_name
        """)
        
        print("\n📊 Columnas agregadas:")
        for col in columns:
            default = col['column_default'] or 'NULL'
            print(f"  ✅ {col['column_name']:<30} ({col['data_type']:<20}) DEFAULT {default}")
        
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
