#!/usr/bin/env python3
"""
Crear tabla de mediciones en la base de datos
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def create_measurements_table():
    """Crear tabla measurements"""
    
    database_url = os.getenv("DATABASE_URL")
    
    print("="*70)
    print("CREANDO TABLA DE MEDICIONES")
    print("="*70)
    print()
    
    try:
        # Conectar a la base de datos
        conn = await asyncpg.connect(database_url)
        
        print("Conectado a la base de datos")
        print()
        
        # Leer SQL
        with open('prisma/migrations/create_measurements_table.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Ejecutar
        print("Ejecutando migracion...")
        await conn.execute(sql)
        
        print("EXITO: Tabla measurements creada")
        print()
        
        # Verificar
        result = await conn.fetchrow("""
            SELECT COUNT(*) as count
            FROM information_schema.tables
            WHERE table_name = 'measurements'
        """)
        
        if result['count'] > 0:
            print("Tabla verificada correctamente")
            
            # Mostrar estructura
            columns = await conn.fetch("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'measurements'
                ORDER BY ordinal_position
            """)
            
            print()
            print("Columnas creadas:")
            for col in columns:
                print(f"  - {col['column_name']}: {col['data_type']}")
        
        await conn.close()
        
        print()
        print("="*70)
        print("TABLA MEASUREMENTS LISTA PARA USAR")
        print("="*70)
        
        return True
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(create_measurements_table())
    exit(0 if success else 1)
