#!/usr/bin/env python3
"""
Script para crear la tabla de candidatas arqueológicas en PostgreSQL
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

async def setup_candidates_table():
    """Crear tabla de candidatas y estructuras relacionadas"""
    
    print("🔧 Configurando tabla de candidatas arqueológicas...")
    print("=" * 80)
    
    try:
        # Conectar a la base de datos
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("✅ Conectado a PostgreSQL")
        
        # Leer el archivo SQL
        with open('create_candidates_table.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        print("\n📄 Ejecutando script SQL...")
        
        # Ejecutar el script
        await conn.execute(sql_script)
        
        print("\n✅ Tabla archaeological_candidates creada exitosamente")
        print("✅ Índices creados para búsquedas eficientes")
        print("✅ Vistas priority_candidates y candidates_statistics disponibles")
        
        # Verificar que la tabla existe
        table_exists = await conn.fetchval('''
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'archaeological_candidates'
            )
        ''')
        
        if table_exists:
            print("\n🎉 Verificación exitosa - Tabla operacional")
            
            # Mostrar estructura de la tabla
            columns = await conn.fetch('''
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'archaeological_candidates'
                ORDER BY ordinal_position
            ''')
            
            print("\n📊 Estructura de la tabla:")
            print("-" * 80)
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                print(f"  {col['column_name']:30} {col['data_type']:20} {nullable}")
            
            # Mostrar índices
            indexes = await conn.fetch('''
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE tablename = 'archaeological_candidates'
            ''')
            
            print(f"\n🔍 Índices creados ({len(indexes)}):")
            print("-" * 80)
            for idx in indexes:
                print(f"  {idx['indexname']}")
        
        else:
            print("\n❌ Error: La tabla no se creó correctamente")
        
        await conn.close()
        
        print("\n" + "=" * 80)
        print("✅ Setup completado exitosamente")
        print("\n💡 Próximos pasos:")
        print("   1. Generar candidatas: GET /archaeological-sites/enriched-candidates")
        print("   2. Ver prioritarias: GET /archaeological-sites/candidates/priority")
        print("   3. Ver estadísticas: GET /archaeological-sites/candidates/statistics")
        
    except Exception as e:
        print(f"\n❌ Error durante setup: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(setup_candidates_table())
    exit(0 if success else 1)
