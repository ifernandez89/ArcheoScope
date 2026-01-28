#!/usr/bin/env python3
"""Verificar datos arqueológicos en BD"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Total y rango
cur.execute('''
    SELECT 
        COUNT(*), 
        MIN(latitude), MAX(latitude), 
        MIN(longitude), MAX(longitude)
    FROM archaeological_sites
''')
total, lat_min, lat_max, lon_min, lon_max = cur.fetchone()

print(f"Total sitios: {total}")
print(f"Rango latitud: {lat_min} a {lat_max}")
print(f"Rango longitud: {lon_min} a {lon_max}")

# Top países
print("\nTop 10 países:")
cur.execute('''
    SELECT country, COUNT(*) 
    FROM archaeological_sites 
    WHERE country IS NOT NULL
    GROUP BY country 
    ORDER BY COUNT(*) DESC 
    LIMIT 10
''')
for country, count in cur.fetchall():
    print(f"  {country}: {count} sitios")

# Clasificación por tipo
print("\nPor clasificación:")
cur.execute('''
    SELECT classification, COUNT(*) 
    FROM archaeological_sites 
    WHERE classification IS NOT NULL
    GROUP BY classification 
    ORDER BY COUNT(*) DESC
''')
for classification, count in cur.fetchall():
    print(f"  {classification}: {count} sitios")

cur.close()
conn.close()
