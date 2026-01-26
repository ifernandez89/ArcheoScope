#!/usr/bin/env python3
"""
Asignar países a sitios usando reverse geocoding
Usa una librería offline para no depender de APIs externas
"""

import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

def get_country_from_coordinates(lat: float, lon: float) -> str:
    """
    Determinar país basándose en coordenadas
    Usa rangos geográficos aproximados
    """
    
    # Rangos geográficos aproximados por país/región
    # Esto es una aproximación simple, no 100% precisa
    
    # Europa
    if 35 < lat < 72 and -10 < lon < 40:
        if 41 < lat < 47 and 6 < lon < 19:
            return 'Italy' if 12 < lon < 19 else 'France'
        if 47 < lat < 55 and 5 < lon < 15:
            return 'Germany'
        if 36 < lat < 42 and 19 < lon < 28:
            return 'Greece'
        if 49 < lat < 61 and -8 < lon < 2:
            return 'United Kingdom'
        if 36 < lat < 44 and -10 < lon < 4:
            return 'Spain'
        if 55 < lat < 70 and 10 < lon < 25:
            return 'Sweden'
        if 60 < lat < 70 and 20 < lon < 32:
            return 'Finland'
        if 54 < lat < 58 and 8 < lon < 13:
            return 'Denmark'
        if 50 < lat < 54 and 3 < lon < 7:
            return 'Netherlands'
        if 50 < lat < 54 and 12 < lon < 24:
            return 'Poland'
        return 'Europe'  # Genérico
    
    # Medio Oriente
    if 12 < lat < 42 and 25 < lon < 65:
        if 22 < lat < 32 and 25 < lon < 37:
            return 'Egypt'
        if 29 < lat < 38 and 34 < lon < 45:
            return 'Iraq'
        if 36 < lat < 42 and 26 < lon < 45:
            return 'Turkey'
        if 29 < lat < 34 and 34 < lon < 39:
            return 'Jordan'
        if 29 < lat < 34 and 34 < lon < 36:
            return 'Israel'
        if 25 < lat < 40 and 44 < lon < 64:
            return 'Iran'
        return 'Middle East'
    
    # Asia
    if -10 < lat < 55 and 60 < lon < 150:
        if 8 < lat < 38 and 68 < lon < 98:
            return 'India'
        if 23 < lat < 28 and 60 < lon < 78:
            return 'Pakistan'
        if 18 < lat < 54 and 73 < lon < 135:
            return 'China'
        if 30 < lat < 46 and 128 < lon < 146:
            return 'Japan'
        if 10 < lat < 21 and 99 < lon < 106:
            return 'Thailand'
        if 10 < lat < 15 and 102 < lon < 108:
            return 'Cambodia'
        if 16 < lat < 29 and 92 < lon < 102:
            return 'Myanmar'
        if -11 < lat < 6 and 95 < lon < 141:
            return 'Indonesia'
        return 'Asia'
    
    # América del Norte
    if 15 < lat < 72 and -170 < lon < -50:
        if 14 < lat < 33 and -118 < lon < -86:
            return 'Mexico'
        if 25 < lat < 50 and -125 < lon < -66:
            return 'United States'
        if 42 < lat < 72 and -141 < lon < -52:
            return 'Canada'
        return 'North America'
    
    # América Central
    if 7 < lat < 18 and -93 < lon < -77:
        if 13 < lat < 18 and -93 < lon < -88:
            return 'Guatemala'
        if 12 < lat < 16 and -90 < lon < -83:
            return 'Honduras'
        if 8 < lat < 12 and -86 < lon < -82:
            return 'Costa Rica'
        return 'Central America'
    
    # América del Sur
    if -56 < lat < 13 and -82 < lon < -34:
        if -18 < lat < -3 and -82 < lon < -68:
            return 'Peru'
        if -34 < lat < -22 and -70 < lon < -53:
            return 'Argentina'
        if -34 < lat < 6 and -74 < lon < -34:
            return 'Brazil'
        if -5 < lat < 13 and -80 < lon < -66:
            return 'Colombia'
        if -23 < lat < -10 and -70 < lon < -57:
            return 'Bolivia'
        if -56 < lat < -17 and -76 < lon < -66:
            return 'Chile'
        if -5 < lat < 2 and -81 < lon < -75:
            return 'Ecuador'
        return 'South America'
    
    # África
    if -35 < lat < 38 and -20 < lon < 52:
        if 22 < lat < 32 and 25 < lon < 37:
            return 'Egypt'
        if 12 < lat < 23 and 22 < lon < 39:
            return 'Sudan'
        if 3 < lat < 15 and 33 < lon < 48:
            return 'Ethiopia'
        if -23 < lat < -15 and 25 < lon < 33:
            return 'Zimbabwe'
        if -35 < lat < -22 and 16 < lon < 33:
            return 'South Africa'
        return 'Africa'
    
    # Oceanía
    if -50 < lat < -10 and 110 < lon < 180:
        return 'Australia'
    
    if -48 < lat < -34 and 166 < lon < 179:
        return 'New Zealand'
    
    # Isla de Pascua
    if -28 < lat < -27 and -110 < lon < -109:
        return 'Chile'
    
    return 'Unknown'

def assign_countries():
    """Asignar países a todos los sitios sin país"""
    
    print("🌍 ASIGNACIÓN DE PAÍSES POR REVERSE GEOCODING")
    print("=" * 100)
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Contar sitios sin país
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM archaeological_sites
        WHERE country IS NULL OR country = ''
    """)
    total_without_country = cursor.fetchone()['total']
    
    print(f"\n📊 Sitios sin país: {total_without_country:,}")
    
    # Procesar en lotes
    batch_size = 5000
    offset = 0
    assigned_count = 0
    
    while offset < total_without_country:
        print(f"\n🔄 Procesando lote {offset//batch_size + 1} ({offset:,} - {min(offset+batch_size, total_without_country):,})")
        
        # Obtener lote
        cursor.execute("""
            SELECT id, latitude, longitude
            FROM archaeological_sites
            WHERE country IS NULL OR country = ''
            ORDER BY id
            LIMIT %s OFFSET %s
        """, (batch_size, offset))
        
        sites = cursor.fetchall()
        
        if not sites:
            break
        
        # Asignar países
        updates = []
        for site in sites:
            country = get_country_from_coordinates(site['latitude'], site['longitude'])
            updates.append((country, site['id']))
            assigned_count += 1
        
        # Actualizar en batch
        execute_batch(cursor, """
            UPDATE archaeological_sites
            SET country = %s
            WHERE id = %s
        """, updates, page_size=1000)
        conn.commit()
        
        print(f"   ✅ {len(updates)} países asignados")
        
        offset += batch_size
        
        # Mostrar progreso
        progress = (assigned_count / total_without_country * 100)
        print(f"   📈 Progreso: {assigned_count:,}/{total_without_country:,} ({progress:.1f}%)")
    
    # Verificar resultado
    print("\n📊 Verificando resultado...")
    
    cursor.execute("""
        SELECT country, COUNT(*) as count
        FROM archaeological_sites
        GROUP BY country
        ORDER BY count DESC
        LIMIT 20
    """)
    
    results = cursor.fetchall()
    print("\nTop 20 países:")
    for row in results:
        print(f"   {row['country']:30s}: {row['count']:6,} sitios")
    
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM archaeological_sites
        WHERE country IS NULL OR country = '' OR country = 'Unknown'
    """)
    
    still_unknown = cursor.fetchone()['count']
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 100)
    print("✅ ASIGNACIÓN COMPLETADA")
    print(f"\n📊 Total asignados: {assigned_count:,}")
    print(f"⚠️  Aún sin país: {still_unknown:,}")

if __name__ == "__main__":
    try:
        assign_countries()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
