#!/usr/bin/env python3
"""
Verificar sitios arqueológicos en los Andes Peruanos
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de base de datos
DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}

def check_andes_sites():
    """Verificar sitios en los Andes Peruanos"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    print("🔍 INVESTIGACIÓN: Sitios en los Andes Peruanos\n")
    print("=" * 80)
    
    # Región Andes Peruanos (amplia)
    regions = [
        {
            'name': 'Andes Peruanos (Completo)',
            'lat_min': -18, 'lat_max': -3,
            'lon_min': -82, 'lon_max': -70
        },
        {
            'name': 'Cusco - Machu Picchu',
            'lat_min': -14, 'lat_max': -13,
            'lon_min': -73, 'lon_max': -71
        },
        {
            'name': 'Lima - Costa Central',
            'lat_min': -13, 'lat_max': -11,
            'lon_min': -78, 'lon_max': -76
        },
        {
            'name': 'Arequipa - Sur',
            'lat_min': -17, 'lat_max': -15,
            'lon_min': -73, 'lon_max': -71
        },
        {
            'name': 'Cajamarca - Norte',
            'lat_min': -8, 'lat_max': -6,
            'lon_min': -79, 'lon_max': -77
        },
        {
            'name': 'Nazca - Líneas',
            'lat_min': -15.5, 'lat_max': -14,
            'lon_min': -76, 'lon_max': -74
        }
    ]
    
    for region in regions:
        print(f"\n📍 {region['name']}")
        print(f"   Coordenadas: {region['lat_min']} a {region['lat_max']} lat, {region['lon_min']} a {region['lon_max']} lon")
        
        query = """
            SELECT COUNT(*) as total,
                   COUNT(DISTINCT country) as countries,
                   STRING_AGG(DISTINCT country, ', ') as country_list
            FROM archaeological_sites
            WHERE latitude BETWEEN %s AND %s
              AND longitude BETWEEN %s AND %s
        """
        
        cursor.execute(query, (
            region['lat_min'], region['lat_max'],
            region['lon_min'], region['lon_max']
        ))
        
        result = cursor.fetchone()
        print(f"   ✅ Sitios encontrados: {result['total']}")
        print(f"   🌍 Países: {result['country_list'] or 'Sin país asignado'}")
        
        if result['total'] > 0:
            # Mostrar algunos sitios de ejemplo
            query_examples = """
                SELECT name, latitude, longitude, country, site_type
                FROM archaeological_sites
                WHERE latitude BETWEEN %s AND %s
                  AND longitude BETWEEN %s AND %s
                LIMIT 5
            """
            
            cursor.execute(query_examples, (
                region['lat_min'], region['lat_max'],
                region['lon_min'], region['lon_max']
            ))
            
            examples = cursor.fetchall()
            print(f"\n   📋 Ejemplos de sitios:")
            for site in examples:
                print(f"      - {site['name']} ({site['latitude']:.4f}, {site['longitude']:.4f})")
                print(f"        País: {site['country'] or 'N/A'}, Tipo: {site['site_type'] or 'N/A'}")
    
    # Buscar TODOS los sitios en Perú
    print("\n" + "=" * 80)
    print("\n🇵🇪 TODOS LOS SITIOS EN PERÚ (por país)")
    
    query_peru = """
        SELECT COUNT(*) as total
        FROM archaeological_sites
        WHERE country ILIKE '%peru%' OR country ILIKE '%perú%'
    """
    
    cursor.execute(query_peru)
    result = cursor.fetchone()
    print(f"   Sitios con país = 'Peru': {result['total']}")
    
    # Buscar por nombre
    print("\n🔍 SITIOS CON 'PERU' EN EL NOMBRE")
    
    query_name = """
        SELECT COUNT(*) as total
        FROM archaeological_sites
        WHERE name ILIKE '%peru%' OR name ILIKE '%perú%'
           OR name ILIKE '%inca%' OR name ILIKE '%machu%'
           OR name ILIKE '%cusco%' OR name ILIKE '%nazca%'
    """
    
    cursor.execute(query_name)
    result = cursor.fetchone()
    print(f"   Sitios con nombres peruanos: {result['total']}")
    
    if result['total'] > 0:
        query_examples = """
            SELECT name, latitude, longitude, country
            FROM archaeological_sites
            WHERE name ILIKE '%peru%' OR name ILIKE '%perú%'
               OR name ILIKE '%inca%' OR name ILIKE '%machu%'
               OR name ILIKE '%cusco%' OR name ILIKE '%nazca%'
            LIMIT 10
        """
        
        cursor.execute(query_examples)
        examples = cursor.fetchall()
        print(f"\n   📋 Ejemplos:")
        for site in examples:
            print(f"      - {site['name']} ({site['latitude']:.4f}, {site['longitude']:.4f})")
            print(f"        País: {site['country'] or 'N/A'}")
    
    # Distribución general Sudamérica
    print("\n" + "=" * 80)
    print("\n🌎 DISTRIBUCIÓN SUDAMÉRICA")
    
    query_sa = """
        SELECT 
            CASE 
                WHEN latitude BETWEEN -18 AND -3 AND longitude BETWEEN -82 AND -70 THEN 'Andes Peruanos'
                WHEN latitude BETWEEN -35 AND -20 AND longitude BETWEEN -75 AND -65 THEN 'Chile/Argentina'
                WHEN latitude BETWEEN -11 AND -9 AND longitude BETWEEN -70 AND -68 THEN 'Acre (Brasil)'
                WHEN latitude BETWEEN -5 AND 5 AND longitude BETWEEN -75 AND -60 THEN 'Amazonía'
                ELSE 'Otra región'
            END as region,
            COUNT(*) as total
        FROM archaeological_sites
        WHERE latitude BETWEEN -35 AND 5
          AND longitude BETWEEN -82 AND -35
        GROUP BY region
        ORDER BY total DESC
    """
    
    cursor.execute(query_sa)
    results = cursor.fetchall()
    
    for row in results:
        print(f"   {row['region']}: {row['total']} sitios")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        check_andes_sites()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
