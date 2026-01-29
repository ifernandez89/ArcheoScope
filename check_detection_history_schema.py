#!/usr/bin/env python3
"""Verificar esquema de la tabla detection_history."""

import asyncio
import asyncpg


async def check_schema():
    """Verificar esquema de detection_history."""
    
    try:
        conn = await asyncpg.connect(
            'postgresql://postgres:1464@localhost:5433/archeoscope_db'
        )
        print("✅ Conectado a BD")
        print()
        
        # Obtener columnas de detection_history
        columns = await conn.fetch("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'detection_history'
            ORDER BY ordinal_position
        """)
        
        print("📊 ESQUEMA DE detection_history:")
        print("="*80)
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            print(f"  {col['column_name']:30} {col['data_type']:20} {nullable}")
        
        print()
        print(f"Total columnas: {len(columns)}")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(check_schema())
