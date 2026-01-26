#!/usr/bin/env python3
"""
Verificar el estado de clasificación de los 80,000+ registros
"""

import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

def check_classification_status():
    """Verificar estado de clasificación de todos los registros"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    print("🔍 VERIFICACIÓN: Estado de Clasificación de 80,000+ Registros")
    print("=" * 100)
    
    # Total de registros
    cursor.execute("SELECT COUNT(*) as total FROM archaeological_sites")
    total = cursor.fetchone()['total']
    print(f"\n📊 TOTAL REGISTROS: {total:,}")
    
    # Verificar campos críticos
    print("\n" + "=" * 100)
    print("🏷️ CAMPOS DE CLASIFICACIÓN")
    print("=" * 100)
    
    # 1. environmentType
    print("\n1️⃣ ENVIRONMENT TYPE:")
    cursor.execute("""
        SELECT "environmentType", COUNT(*) as count
        FROM archaeological_sites
        GROUP BY "environmentType"
        ORDER BY count DESC
    """)
    
    env_types = cursor.fetchall()
    for row in env_types:
        pct = (row['count'] / total * 100)
        print(f"   {row['environmentType']:20s}: {row['count']:6,} ({pct:5.1f}%)")
    
    # 2. siteType
    print("\n2️⃣ SITE TYPE:")
    cursor.execute("""
        SELECT "siteType", COUNT(*) as count
        FROM archaeological_sites
        GROUP BY "siteType"
        ORDER BY count DESC
    """)
    
    site_types = cursor.fetchall()
    for row in site_types:
        pct = (row['count'] / total * 100)
        print(f"   {row['siteType']:30s}: {row['count']:6,} ({pct:5.1f}%)")
    
    # 3. confidenceLevel
    print("\n3️⃣ CONFIDENCE LEVEL:")
    cursor.execute("""
        SELECT "confidenceLevel", COUNT(*) as count
        FROM archaeological_sites
        GROUP BY "confidenceLevel"
        ORDER BY count DESC
    """)
    
    conf_levels = cursor.fetchall()
    for row in conf_levels:
        pct = (row['count'] / total * 100)
        print(f"   {row['confidenceLevel']:20s}: {row['count']:6,} ({pct:5.1f}%)")
    
    # 4. País
    print("\n4️⃣ PAÍS:")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN country IS NULL OR country = '' THEN 'SIN PAÍS'
                ELSE country
            END as country_status,
            COUNT(*) as count
        FROM archaeological_sites
        GROUP BY country_status
        ORDER BY count DESC
        LIMIT 10
    """)
    
    countries = cursor.fetchall()
    for row in countries:
        pct = (row['count'] / total * 100)
        print(f"   {row['country_status']:30s}: {row['count']:6,} ({pct:5.1f}%)")
    
    # Verificar registros sin clasificar
    print("\n" + "=" * 100)
    print("⚠️  REGISTROS SIN CLASIFICAR")
    print("=" * 100)
    
    # environmentType = UNKNOWN
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM archaeological_sites
        WHERE "environmentType" = 'UNKNOWN'
    """)
    unknown_env = cursor.fetchone()['count']
    unknown_env_pct = (unknown_env / total * 100)
    print(f"\n❌ environmentType = UNKNOWN: {unknown_env:,} ({unknown_env_pct:.1f}%)")
    
    # siteType = UNKNOWN
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM archaeological_sites
        WHERE "siteType" = 'UNKNOWN'
    """)
    unknown_site = cursor.fetchone()['count']
    unknown_site_pct = (unknown_site / total * 100)
    print(f"❌ siteType = UNKNOWN: {unknown_site:,} ({unknown_site_pct:.1f}%)")
    
    # Sin país
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM archaeological_sites
        WHERE country IS NULL OR country = ''
    """)
    no_country = cursor.fetchone()['count']
    no_country_pct = (no_country / total * 100)
    print(f"❌ Sin país: {no_country:,} ({no_country_pct:.1f}%)")
    
    # Verificar registros BIEN clasificados
    print("\n" + "=" * 100)
    print("✅ REGISTROS BIEN CLASIFICADOS")
    print("=" * 100)
    
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM archaeological_sites
        WHERE "environmentType" != 'UNKNOWN'
          AND "siteType" != 'UNKNOWN'
          AND country IS NOT NULL
          AND country != ''
    """)
    well_classified = cursor.fetchone()['count']
    well_classified_pct = (well_classified / total * 100)
    print(f"\n✅ Completamente clasificados: {well_classified:,} ({well_classified_pct:.1f}%)")
    
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM archaeological_sites
        WHERE "environmentType" != 'UNKNOWN'
          AND "siteType" != 'UNKNOWN'
    """)
    partial_classified = cursor.fetchone()['count']
    partial_classified_pct = (partial_classified / total * 100)
    print(f"⚠️  Parcialmente clasificados (sin país): {partial_classified:,} ({partial_classified_pct:.1f}%)")
    
    # Resumen final
    print("\n" + "=" * 100)
    print("📊 RESUMEN FINAL")
    print("=" * 100)
    
    print(f"\nTotal registros: {total:,}")
    print(f"\n✅ Bien clasificados: {well_classified:,} ({well_classified_pct:.1f}%)")
    print(f"⚠️  Parcialmente clasificados: {partial_classified - well_classified:,} ({(partial_classified - well_classified)/total*100:.1f}%)")
    print(f"❌ Mal clasificados (UNKNOWN): {total - partial_classified:,} ({(total - partial_classified)/total*100:.1f}%)")
    
    # Recomendaciones
    print("\n" + "=" * 100)
    print("💡 RECOMENDACIONES")
    print("=" * 100)
    
    if unknown_env_pct > 50:
        print("\n🔴 CRÍTICO: >50% de registros con environmentType = UNKNOWN")
        print("   Acción: Ejecutar clasificador de ambientes en toda la BD")
    
    if unknown_site_pct > 50:
        print("\n🔴 CRÍTICO: >50% de registros con siteType = UNKNOWN")
        print("   Acción: Mejorar clasificación de tipos de sitio")
    
    if no_country_pct > 80:
        print("\n🔴 CRÍTICO: >80% de registros sin país")
        print("   Acción: Ejecutar reverse geocoding para asignar países")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        check_classification_status()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
