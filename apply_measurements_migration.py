#!/usr/bin/env python3
"""
Apply Measurements Migration - Aplicar migración de tabla de mediciones
=======================================================================

Crea la tabla instrument_measurements en la BD.
"""

import asyncio
import asyncpg
import os
from pathlib import Path


async def apply_migration():
    """Aplicar migración de measurements."""
    
    print("="*80)
    print("APLICANDO MIGRACIÓN: instrument_measurements")
    print("="*80)
    
    # Conectar a BD
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5433,
            database="archeoscope",
            user="postgres",
            password="postgres"
        )
        
        print("✅ Conectado a BD")
        
        # Leer SQL de migración
        migration_path = Path("prisma/migrations/20260129_add_instrument_measurements.sql")
        
        if not migration_path.exists():
            print(f"❌ Archivo de migración no encontrado: {migration_path}")
            return False
        
        with open(migration_path, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        print(f"📄 Leyendo migración: {migration_path}")
        
        # Ejecutar migración
        print("🔄 Ejecutando migración...")
        
        await conn.execute(migration_sql)
        
        print("✅ Migración aplicada exitosamente")
        
        # Verificar tabla
        result = await conn.fetchval("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'instrument_measurements'
        """)
        
        if result > 0:
            print("✅ Tabla instrument_measurements creada")
            
            # Verificar índices
            indices = await conn.fetch("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'instrument_measurements'
            """)
            
            print(f"✅ {len(indices)} índices creados:")
            for idx in indices:
                print(f"   - {idx['indexname']}")
        else:
            print("❌ Tabla no encontrada después de migración")
            return False
        
        await conn.close()
        
        print("\n" + "="*80)
        print("✅ MIGRACIÓN COMPLETADA")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando migración: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(apply_migration())
    exit(0 if success else 1)
