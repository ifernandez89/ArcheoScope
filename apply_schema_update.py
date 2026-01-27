#!/usr/bin/env python3
"""Aplicar actualización de esquema a archaeological_candidate_analyses."""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def apply_update():
    """Aplicar actualización de esquema."""
    conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
    
    print("\n🔧 APLICANDO ACTUALIZACIÓN DE ESQUEMA")
    print("="*60)
    
    try:
        # Leer SQL
        with open('add_missing_columns_to_analyses.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Ejecutar
        await conn.execute(sql)
        print("✅ Columnas agregadas exitosamente")
        
        # Verificar
        cols = await conn.fetch("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'archaeological_candidate_analyses'
              AND column_name IN ('anomaly_score', 'recommended_action', 'environment_type', 'confidence_level')
            ORDER BY column_name
        """)
        
        print(f"\n📋 Columnas nuevas verificadas: {len(cols)}/4")
        for r in cols:
            print(f"  ✅ {r['column_name']}")
        
        if len(cols) == 4:
            print("\n🎉 Actualización completada exitosamente")
        else:
            print("\n⚠️ Algunas columnas no se agregaron")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(apply_update())
