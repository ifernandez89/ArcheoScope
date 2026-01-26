#!/usr/bin/env python3
"""
Clasificar los últimos 55 registros con UNKNOWN
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from environment_classifier import EnvironmentClassifier
from terrain_classifier import TerrainClassifier

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

def classify_remaining():
    """Clasificar los últimos registros UNKNOWN"""
    
    print("🔧 CLASIFICANDO ÚLTIMOS REGISTROS UNKNOWN")
    print("=" * 100)
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Inicializar clasificadores
    env_classifier = EnvironmentClassifier()
    terrain_classifier = TerrainClassifier()
    
    # 1. Clasificar environmentType UNKNOWN
    print("\n1️⃣ Clasificando environmentType UNKNOWN...")
    
    cursor.execute("""
        SELECT id, latitude, longitude, name
        FROM archaeological_sites
        WHERE "environmentType" = 'UNKNOWN'
    """)
    
    unknown_env = cursor.fetchall()
    print(f"   Encontrados: {len(unknown_env)} registros")
    
    for site in unknown_env:
        try:
            result = env_classifier.classify_environment(site['latitude'], site['longitude'])
            env_type = result['environment_type']
            
            cursor.execute("""
                UPDATE archaeological_sites
                SET "environmentType" = %s
                WHERE id = %s
            """, (env_type, site['id']))
            
            print(f"   ✅ {site['name'][:50]:50s} → {env_type}")
            
        except Exception as e:
            print(f"   ❌ Error en {site['id']}: {e}")
    
    conn.commit()
    
    # 2. Clasificar siteType UNKNOWN
    print("\n2️⃣ Clasificando siteType UNKNOWN...")
    
    cursor.execute("""
        SELECT id, latitude, longitude, name, "environmentType"
        FROM archaeological_sites
        WHERE "siteType" = 'UNKNOWN'
    """)
    
    unknown_site = cursor.fetchall()
    print(f"   Encontrados: {len(unknown_site)} registros")
    
    for site in unknown_site:
        try:
            # Clasificar por nombre primero
            name_lower = site['name'].lower() if site['name'] else ''
            
            site_type = 'CEREMONIAL_CENTER'  # Default
            
            if any(word in name_lower for word in ['temple', 'church', 'cathedral']):
                site_type = 'TEMPLE_COMPLEX'
            elif any(word in name_lower for word in ['fort', 'castle', 'fortress']):
                site_type = 'FORTIFICATION'
            elif any(word in name_lower for word in ['tomb', 'cemetery', 'burial']):
                site_type = 'BURIAL_SITE'
            elif any(word in name_lower for word in ['city', 'town', 'settlement']):
                site_type = 'URBAN_SETTLEMENT'
            elif site['environmentType'] == 'FOREST':
                site_type = 'URBAN_SETTLEMENT'
            elif site['environmentType'] == 'DESERT':
                site_type = 'CEREMONIAL_CENTER'
            elif site['environmentType'] == 'MOUNTAIN':
                site_type = 'MOUNTAIN_CITADEL'
            
            cursor.execute("""
                UPDATE archaeological_sites
                SET "siteType" = %s
                WHERE id = %s
            """, (site_type, site['id']))
            
            print(f"   ✅ {site['name'][:50]:50s} → {site_type}")
            
        except Exception as e:
            print(f"   ❌ Error en {site['id']}: {e}")
    
    conn.commit()
    
    # 3. Verificar resultado final
    print("\n3️⃣ Verificando resultado final...")
    
    cursor.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE "environmentType" = 'UNKNOWN') as env_unknown,
            COUNT(*) FILTER (WHERE "siteType" = 'UNKNOWN') as site_unknown,
            COUNT(*) FILTER (WHERE country IS NULL OR country = '') as no_country,
            COUNT(*) as total
        FROM archaeological_sites
    """)
    
    result = cursor.fetchone()
    
    print(f"\n📊 RESULTADO FINAL:")
    print(f"   Total registros: {result['total']:,}")
    print(f"   environmentType UNKNOWN: {result['env_unknown']}")
    print(f"   siteType UNKNOWN: {result['site_unknown']}")
    print(f"   Sin país: {result['no_country']}")
    
    if result['env_unknown'] == 0 and result['site_unknown'] == 0 and result['no_country'] == 0:
        print("\n🎉 ¡TODOS LOS REGISTROS ESTÁN COMPLETAMENTE CLASIFICADOS!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        classify_remaining()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
