#!/usr/bin/env python3
"""
Script para crear tablas TIMT en la base de datos.
"""

import asyncio
import asyncpg
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

async def setup_timt_tables():
    """Crear tablas TIMT en la base de datos."""
    
    database_url = os.getenv("DATABASE_URL")
    
    # Limpiar comillas si existen
    if database_url:
        database_url = database_url.strip('"').strip("'")
    
    if not database_url:
        print("❌ DATABASE_URL no configurada")
        print(f"   Buscando en: {env_path}")
        return False
    
    print(f"📡 Conectando a: {database_url[:30]}...")
    
    try:
        # Conectar a BD
        conn = await asyncpg.connect(database_url)
        print("✅ Conectado a la base de datos")
        
        # Leer script SQL
        sql_file = Path(__file__).parent / "create_timt_tables.sql"
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar script
        print("📝 Ejecutando script SQL...")
        await conn.execute(sql_script)
        
        print("✅ Tablas TIMT creadas exitosamente")
        
        # Verificar tablas creadas
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND (table_name LIKE '%timt%' OR table_name LIKE '%tcp%' OR table_name LIKE '%etp%')
            ORDER BY table_name
        """)
        
        print(f"\n📊 Tablas TIMT creadas ({len(tables)}):")
        for table in tables:
            print(f"   ✓ {table['table_name']}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(setup_timt_tables())
    exit(0 if success else 1)
