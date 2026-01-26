#!/usr/bin/env python3
"""
Ver el esquema real de la tabla archaeological_sites
"""

import psycopg2

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'archaeological_sites'
    ORDER BY ordinal_position
""")

print("📋 ESQUEMA DE LA TABLA archaeological_sites:\n")
for row in cursor.fetchall():
    print(f"   {row[0]:30s} {row[1]:20s} NULL: {row[2]}")

cursor.close()
conn.close()
