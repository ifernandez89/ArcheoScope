#!/usr/bin/env python3
"""
Clasificación RÁPIDA de sitios usando environmentType existente
"""

import psycopg2

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

def quick_classify():
    """Clasificar sitios basándose en environmentType y nombre"""
    
    print("🚀 CLASIFICACIÓN RÁPIDA DE SITIOS")
    print("=" * 100)
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # 1. Clasificar por palabras clave en el nombre
    print("\n1️⃣ Clasificando por palabras clave en nombre...")
    
    classifications = [
        ('TEMPLE_COMPLEX', ['temple', 'church', 'cathedral', 'mosque', 'shrine', 'sanctuary', 'basilica']),
        ('FORTIFICATION', ['fort', 'castle', 'fortress', 'wall', 'defense', 'citadel', 'stronghold']),
        ('BURIAL_SITE', ['tomb', 'cemetery', 'burial', 'grave', 'necropolis', 'mausoleum', 'crypt']),
        ('URBAN_SETTLEMENT', ['city', 'town', 'settlement', 'village', 'urban', 'oppidum']),
        ('MONUMENTAL_COMPLEX', ['pyramid', 'ziggurat', 'mound', 'tumulus', 'complex']),
        ('MEGALITHIC_MONUMENT', ['stone', 'megalith', 'dolmen', 'menhir', 'cromlech', 'henge']),
        ('AGRICULTURAL_SITE', ['farm', 'field', 'terrace', 'irrigation', 'agricultural', 'villa']),
    ]
    
    total_classified = 0
    for site_type, keywords in classifications:
        pattern = '|'.join(keywords)
        cursor.execute(f"""
            UPDATE archaeological_sites
            SET "siteType" = %s
            WHERE "siteType" = 'UNKNOWN'
              AND name ~* %s
        """, (site_type, pattern))
        
        count = cursor.rowcount
        total_classified += count
        print(f"   {site_type:30s}: {count:6,} sitios")
    
    conn.commit()
    
    # 2. Clasificar por environmentType
    print("\n2️⃣ Clasificando por environmentType...")
    
    env_mappings = [
        ('DESERT', 'CEREMONIAL_CENTER'),
        ('MOUNTAIN', 'MOUNTAIN_CITADEL'),
        ('FOREST', 'URBAN_SETTLEMENT'),
        ('GRASSLAND', 'AGRICULTURAL_SITE'),
        ('COASTAL', 'URBAN_SETTLEMENT'),
    ]
    
    for env_type, site_type in env_mappings:
        cursor.execute("""
            UPDATE archaeological_sites
            SET "siteType" = %s
            WHERE "siteType" = 'UNKNOWN'
              AND "environmentType" = %s
        """, (site_type, env_type))
        
        count = cursor.rowcount
        total_classified += count
        print(f"   {env_type:20s} → {site_type:30s}: {count:6,} sitios")
    
    conn.commit()
    
    # 3. Verificar resultado
    print("\n3️⃣ Verificando resultado...")
    
    cursor.execute("""
        SELECT "siteType", COUNT(*) as count
        FROM archaeological_sites
        GROUP BY "siteType"
        ORDER BY count DESC
    """)
    
    results = cursor.fetchall()
    print("\n📊 Distribución final:")
    for row in results:
        print(f"   {row[0]:30s}: {row[1]:6,} sitios")
    
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM archaeological_sites
        WHERE "siteType" = 'UNKNOWN'
    """)
    
    still_unknown = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 100)
    print("✅ CLASIFICACIÓN COMPLETADA")
    print(f"\n📊 Total clasificados: {total_classified:,}")
    print(f"⚠️  Aún sin clasificar: {still_unknown:,}")

if __name__ == "__main__":
    try:
        quick_classify()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
