#!/usr/bin/env python3
"""
Crear tabla sar_cache en PostgreSQL
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_sar_cache_table():
    """Crear tabla sar_cache"""
    
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("ERROR: DATABASE_URL no configurado")
        return False
    
    try:
        print(f"Conectando a base de datos...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Leer SQL
        with open('create_sar_cache_table.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
        
        print(f"Ejecutando SQL...")
        cur.execute(sql)
        conn.commit()
        
        print(f"✅ Tabla sar_cache creada correctamente")
        
        # Verificar
        cur.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'sar_cache'
        """)
        
        count = cur.fetchone()[0]
        
        if count > 0:
            print(f"✅ Verificación OK - tabla existe")
        else:
            print(f"❌ ERROR - tabla no encontrada")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_sar_cache_table()
    exit(0 if success else 1)
