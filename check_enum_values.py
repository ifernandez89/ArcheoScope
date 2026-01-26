#!/usr/bin/env python3
"""
Ver los valores válidos de los enums
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

enums = ['SiteType', 'EnvironmentType', 'ConfidenceLevel', 'ExcavationStatus', 'PreservationStatus']

for enum_name in enums:
    cursor.execute(f"""
        SELECT e.enumlabel
        FROM pg_type t
        JOIN pg_enum e ON t.oid = e.enumtypid
        WHERE t.typname = '{enum_name}'
        ORDER BY e.enumsortorder
    """)
    
    values = [row[0] for row in cursor.fetchall()]
    print(f"\n{enum_name}:")
    for v in values:
        print(f"   - {v}")

cursor.close()
conn.close()
