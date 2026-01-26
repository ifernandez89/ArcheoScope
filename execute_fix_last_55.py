#!/usr/bin/env python3
"""
Ejecutar fix_last_55_unknowns.sql para clasificar los últimos 55 registros
"""

import psycopg2

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

def execute_fix():
    """Ejecutar SQL para clasificar últimos 55 registros"""
    
    print("🔧 Ejecutando fix_last_55_unknowns.sql...")
    
    # Leer SQL
    with open('fix_last_55_unknowns.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Conectar y ejecutar
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql)
        rows_updated = cursor.rowcount
        conn.commit()
        
        print(f"✅ {rows_updated} registros actualizados")
        
        # Verificar resultado
        cursor.execute("""
            SELECT COUNT(*) 
            FROM archaeological_sites 
            WHERE "environmentType" = 'UNKNOWN'
        """)
        remaining = cursor.fetchone()[0]
        
        print(f"\n📊 Registros con environmentType = UNKNOWN: {remaining}")
        
        if remaining == 0:
            print("🎉 ¡TODOS LOS REGISTROS CLASIFICADOS!")
        else:
            print(f"⚠️  Aún quedan {remaining} registros sin clasificar")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    execute_fix()
