#!/usr/bin/env python3
"""
Verificar el nombre exacto del tipo enum en PostgreSQL
"""

import psycopg2

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

def check_enum():
    """Verificar tipos enum en la base de datos"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Obtener tipos enum
    cursor.execute("""
        SELECT t.typname, e.enumlabel
        FROM pg_type t 
        JOIN pg_enum e ON t.oid = e.enumtypid  
        WHERE t.typname LIKE '%nvironment%'
        ORDER BY t.typname, e.enumsortorder
    """)
    
    print("🔍 Tipos enum relacionados con 'environment':")
    current_type = None
    for row in cursor.fetchall():
        type_name, enum_value = row
        if type_name != current_type:
            print(f"\n📋 Tipo: {type_name}")
            current_type = type_name
        print(f"   - {enum_value}")
    
    # Verificar estructura de la tabla
    cursor.execute("""
        SELECT column_name, data_type, udt_name
        FROM information_schema.columns
        WHERE table_name = 'archaeological_sites'
          AND column_name = 'environmentType'
    """)
    
    print("\n\n🏛️ Columna environmentType:")
    for row in cursor.fetchall():
        print(f"   Nombre: {row[0]}")
        print(f"   Tipo: {row[1]}")
        print(f"   UDT: {row[2]}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    check_enum()
