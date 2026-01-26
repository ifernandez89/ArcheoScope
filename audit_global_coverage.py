#!/usr/bin/env python3
"""
Auditoría completa de cobertura geográfica de la base de datos
Identificar regiones arqueológicas importantes sin sitios
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

# Regiones arqueológicas CRÍTICAS del mundo
CRITICAL_ARCHAEOLOGICAL_REGIONS = {
    'AMÉRICA': [
        {'name': 'Perú - Andes/Costa', 'lat_min': -18, 'lat_max': -3, 'lon_min': -82, 'lon_max': -70, 'expected': 100},
        {'name': 'México - Mesoamérica', 'lat_min': 14, 'lat_max': 22, 'lon_min': -106, 'lon_max': -86, 'expected': 200},
        {'name': 'Guatemala - Petén Maya', 'lat_min': 15, 'lat_max': 18, 'lon_min': -92, 'lon_max': -88, 'expected': 100},
        {'name': 'Honduras - Copán', 'lat_min': 14, 'lat_max': 16, 'lon_min': -90, 'lon_max': -86, 'expected': 30},
        {'name': 'Bolivia - Tiwanaku', 'lat_min': -18, 'lat_max': -15, 'lon_min': -70, 'lon_max': -66, 'expected': 30},
        {'name': 'Colombia - San Agustín', 'lat_min': 1, 'lat_max': 3, 'lon_min': -77, 'lon_max': -75, 'expected': 20},
        {'name': 'Ecuador - Andes', 'lat_min': -3, 'lat_max': 1, 'lon_min': -80, 'lon_max': -77, 'expected': 30},
        {'name': 'Brasil - Amazonía Occidental', 'lat_min': -5, 'lat_max': -3, 'lon_min': -62, 'lon_max': -60, 'expected': 10},
        {'name': 'Brasil - Acre (Geoglifos)', 'lat_min': -11, 'lat_max': -9, 'lon_min': -70, 'lon_max': -68, 'expected': 20},
        {'name': 'USA - Suroeste (Anasazi)', 'lat_min': 35, 'lat_max': 38, 'lon_min': -112, 'lon_max': -107, 'expected': 50},
        {'name': 'USA - Mississippi (Cahokia)', 'lat_min': 38, 'lat_max': 40, 'lon_min': -91, 'lon_max': -89, 'expected': 20},
    ],
    'MEDIO ORIENTE': [
        {'name': 'Egipto - Valle del Nilo', 'lat_min': 24, 'lat_max': 31, 'lon_min': 30, 'lon_max': 35, 'expected': 200},
        {'name': 'Irak - Mesopotamia', 'lat_min': 31, 'lat_max': 37, 'lon_min': 42, 'lon_max': 46, 'expected': 150},
        {'name': 'Siria - Palmira/Ebla', 'lat_min': 33, 'lat_max': 37, 'lon_min': 36, 'lon_max': 42, 'expected': 100},
        {'name': 'Jordania - Petra', 'lat_min': 29, 'lat_max': 33, 'lon_min': 35, 'lon_max': 39, 'expected': 50},
        {'name': 'Israel/Palestina', 'lat_min': 29, 'lat_max': 33, 'lon_min': 34, 'lon_max': 36, 'expected': 100},
        {'name': 'Turquía - Anatolia', 'lat_min': 37, 'lat_max': 42, 'lon_min': 26, 'lon_max': 45, 'expected': 200},
        {'name': 'Irán - Persépolis', 'lat_min': 29, 'lat_max': 31, 'lon_min': 52, 'lon_max': 54, 'expected': 30},
    ],
    'ASIA': [
        {'name': 'India - Valle del Indo', 'lat_min': 24, 'lat_max': 32, 'lon_min': 68, 'lon_max': 78, 'expected': 100},
        {'name': 'Pakistán - Mohenjo-daro', 'lat_min': 26, 'lat_max': 28, 'lon_min': 67, 'lon_max': 69, 'expected': 20},
        {'name': 'China - Valle del Río Amarillo', 'lat_min': 34, 'lat_max': 38, 'lon_min': 108, 'lon_max': 116, 'expected': 150},
        {'name': 'China - Xian (Terracota)', 'lat_min': 34, 'lat_max': 35, 'lon_min': 108, 'lon_max': 109, 'expected': 30},
        {'name': 'Camboya - Angkor', 'lat_min': 13, 'lat_max': 14, 'lon_min': 103, 'lon_max': 104, 'expected': 50},
        {'name': 'Tailandia - Ayutthaya', 'lat_min': 14, 'lat_max': 15, 'lon_min': 100, 'lon_max': 101, 'expected': 30},
        {'name': 'Myanmar - Bagan', 'lat_min': 21, 'lat_max': 22, 'lon_min': 94, 'lon_max': 95, 'expected': 30},
        {'name': 'Indonesia - Borobudur', 'lat_min': -8, 'lat_max': -7, 'lon_min': 110, 'lon_max': 111, 'expected': 20},
        {'name': 'Japón - Nara/Kyoto', 'lat_min': 34, 'lat_max': 36, 'lon_min': 135, 'lon_max': 136, 'expected': 50},
    ],
    'EUROPA': [
        {'name': 'Grecia - Atenas/Peloponeso', 'lat_min': 37, 'lat_max': 39, 'lon_min': 21, 'lon_max': 24, 'expected': 150},
        {'name': 'Italia - Roma/Lacio', 'lat_min': 41, 'lat_max': 42, 'lon_min': 12, 'lon_max': 13, 'expected': 200},
        {'name': 'Italia - Pompeya', 'lat_min': 40, 'lat_max': 41, 'lon_min': 14, 'lon_max': 15, 'expected': 50},
        {'name': 'Reino Unido - Stonehenge', 'lat_min': 51, 'lat_max': 52, 'lon_min': -2, 'lon_max': -1, 'expected': 30},
        {'name': 'Francia - Lascaux/Dordoña', 'lat_min': 44, 'lat_max': 46, 'lon_min': 0, 'lon_max': 2, 'expected': 50},
        {'name': 'España - Altamira', 'lat_min': 43, 'lat_max': 44, 'lon_min': -5, 'lon_max': -3, 'expected': 30},
        {'name': 'Alemania - Renania', 'lat_min': 49, 'lat_max': 51, 'lon_min': 6, 'lon_max': 8, 'expected': 100},
    ],
    'ÁFRICA': [
        {'name': 'Egipto - Giza/Saqqara', 'lat_min': 29, 'lat_max': 30, 'lon_min': 31, 'lon_max': 32, 'expected': 50},
        {'name': 'Sudán - Nubia/Meroe', 'lat_min': 16, 'lat_max': 18, 'lon_min': 33, 'lon_max': 34, 'expected': 30},
        {'name': 'Etiopía - Aksum', 'lat_min': 14, 'lat_max': 15, 'lon_min': 38, 'lon_max': 39, 'expected': 20},
        {'name': 'Zimbabwe - Gran Zimbabwe', 'lat_min': -21, 'lat_max': -20, 'lon_min': 30, 'lon_max': 31, 'expected': 10},
        {'name': 'Malí - Tombuctú', 'lat_min': 16, 'lat_max': 17, 'lon_min': -4, 'lon_max': -2, 'expected': 10},
    ],
    'OCEANÍA': [
        {'name': 'Isla de Pascua - Moai', 'lat_min': -28, 'lat_max': -27, 'lon_min': -110, 'lon_max': -109, 'expected': 10},
        {'name': 'Australia - Arte Rupestre', 'lat_min': -18, 'lat_max': -12, 'lon_min': 130, 'lon_max': 136, 'expected': 20},
    ]
}

def audit_global_coverage():
    """Auditar cobertura global de sitios arqueológicos"""
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    print("🌍 AUDITORÍA GLOBAL DE COBERTURA ARQUEOLÓGICA")
    print("=" * 100)
    
    # Estadísticas generales
    cursor.execute("SELECT COUNT(*) as total FROM archaeological_sites")
    total_sites = cursor.fetchone()['total']
    print(f"\n📊 TOTAL SITIOS EN BASE DE DATOS: {total_sites:,}")
    
    # Distribución por continente (aproximada)
    print("\n" + "=" * 100)
    print("📍 DISTRIBUCIÓN POR CONTINENTE (aproximada)")
    print("=" * 100)
    
    continents = [
        ('Europa', 35, 72, -10, 40),
        ('Asia', -10, 55, 25, 150),
        ('África', -35, 38, -20, 52),
        ('América del Norte', 15, 72, -170, -50),
        ('América del Sur', -56, 15, -82, -34),
        ('Oceanía', -50, -10, 110, 180),
    ]
    
    for continent, lat_min, lat_max, lon_min, lon_max in continents:
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM archaeological_sites
            WHERE latitude BETWEEN %s AND %s
              AND longitude BETWEEN %s AND %s
        """, (lat_min, lat_max, lon_min, lon_max))
        
        count = cursor.fetchone()['total']
        percentage = (count / total_sites * 100) if total_sites > 0 else 0
        print(f"   {continent:25s}: {count:6,} sitios ({percentage:5.1f}%)")
    
    # Análisis detallado por región crítica
    print("\n" + "=" * 100)
    print("🔍 ANÁLISIS DETALLADO DE REGIONES ARQUEOLÓGICAS CRÍTICAS")
    print("=" * 100)
    
    problems = []
    
    for continent, regions in CRITICAL_ARCHAEOLOGICAL_REGIONS.items():
        print(f"\n{'='*100}")
        print(f"🌎 {continent}")
        print(f"{'='*100}")
        
        for region in regions:
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM archaeological_sites
                WHERE latitude BETWEEN %s AND %s
                  AND longitude BETWEEN %s AND %s
            """, (region['lat_min'], region['lat_max'], region['lon_min'], region['lon_max']))
            
            count = cursor.fetchone()['total']
            expected = region['expected']
            
            # Calcular estado
            if count == 0:
                status = "🔴 CRÍTICO"
                problems.append({
                    'region': region['name'],
                    'continent': continent,
                    'count': count,
                    'expected': expected,
                    'severity': 'CRITICAL',
                    'coords': (region['lat_min'], region['lat_max'], region['lon_min'], region['lon_max'])
                })
            elif count < expected * 0.2:
                status = "🟠 MUY BAJO"
                problems.append({
                    'region': region['name'],
                    'continent': continent,
                    'count': count,
                    'expected': expected,
                    'severity': 'HIGH',
                    'coords': (region['lat_min'], region['lat_max'], region['lon_min'], region['lon_max'])
                })
            elif count < expected * 0.5:
                status = "🟡 BAJO"
                problems.append({
                    'region': region['name'],
                    'continent': continent,
                    'count': count,
                    'expected': expected,
                    'severity': 'MEDIUM',
                    'coords': (region['lat_min'], region['lat_max'], region['lon_min'], region['lon_max'])
                })
            else:
                status = "✅ OK"
            
            coverage = (count / expected * 100) if expected > 0 else 0
            
            print(f"\n   {status} {region['name']}")
            print(f"      Sitios: {count:4d} / {expected:4d} esperados ({coverage:5.1f}% cobertura)")
            print(f"      Coords: {region['lat_min']} a {region['lat_max']} lat, {region['lon_min']} a {region['lon_max']} lon")
            
            # Mostrar ejemplos si hay sitios
            if count > 0 and count < 5:
                cursor.execute("""
                    SELECT name, latitude, longitude, country
                    FROM archaeological_sites
                    WHERE latitude BETWEEN %s AND %s
                      AND longitude BETWEEN %s AND %s
                    LIMIT 3
                """, (region['lat_min'], region['lat_max'], region['lon_min'], region['lon_max']))
                
                examples = cursor.fetchall()
                print(f"      Ejemplos:")
                for site in examples:
                    print(f"         - {site['name']} ({site['latitude']:.4f}, {site['longitude']:.4f})")
    
    # Resumen de problemas
    print("\n" + "=" * 100)
    print("⚠️  RESUMEN DE PROBLEMAS DETECTADOS")
    print("=" * 100)
    
    critical = [p for p in problems if p['severity'] == 'CRITICAL']
    high = [p for p in problems if p['severity'] == 'HIGH']
    medium = [p for p in problems if p['severity'] == 'MEDIUM']
    
    print(f"\n🔴 CRÍTICO (0 sitios): {len(critical)} regiones")
    for p in critical:
        print(f"   - {p['region']} ({p['continent']})")
    
    print(f"\n🟠 MUY BAJO (<20% esperado): {len(high)} regiones")
    for p in high:
        print(f"   - {p['region']} ({p['continent']}): {p['count']}/{p['expected']} sitios")
    
    print(f"\n🟡 BAJO (<50% esperado): {len(medium)} regiones")
    for p in medium:
        print(f"   - {p['region']} ({p['continent']}): {p['count']}/{p['expected']} sitios")
    
    # Análisis de países
    print("\n" + "=" * 100)
    print("🌍 ANÁLISIS DE PAÍSES")
    print("=" * 100)
    
    cursor.execute("""
        SELECT 
            COALESCE(country, 'SIN PAÍS') as country,
            COUNT(*) as total
        FROM archaeological_sites
        GROUP BY country
        ORDER BY total DESC
        LIMIT 30
    """)
    
    countries = cursor.fetchall()
    
    print("\nTop 30 países por número de sitios:")
    for i, row in enumerate(countries, 1):
        percentage = (row['total'] / total_sites * 100) if total_sites > 0 else 0
        print(f"   {i:2d}. {row['country']:30s}: {row['total']:6,} sitios ({percentage:5.1f}%)")
    
    # Sitios sin país
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM archaeological_sites
        WHERE country IS NULL OR country = ''
    """)
    
    no_country = cursor.fetchone()['total']
    no_country_pct = (no_country / total_sites * 100) if total_sites > 0 else 0
    
    print(f"\n⚠️  Sitios SIN PAÍS asignado: {no_country:,} ({no_country_pct:.1f}%)")
    
    cursor.close()
    conn.close()
    
    # Guardar reporte
    print("\n" + "=" * 100)
    print("💾 GUARDANDO REPORTE...")
    
    with open('GLOBAL_COVERAGE_AUDIT_REPORT.md', 'w', encoding='utf-8') as f:
        f.write("# 🌍 Reporte de Auditoría de Cobertura Global\n\n")
        f.write(f"**Fecha**: 2026-01-26\n")
        f.write(f"**Total sitios**: {total_sites:,}\n\n")
        
        f.write("## 🔴 REGIONES CRÍTICAS (0 sitios)\n\n")
        for p in critical:
            f.write(f"### {p['region']} ({p['continent']})\n")
            f.write(f"- **Esperado**: {p['expected']} sitios\n")
            f.write(f"- **Actual**: 0 sitios\n")
            f.write(f"- **Coordenadas**: {p['coords'][0]} a {p['coords'][1]} lat, {p['coords'][2]} a {p['coords'][3]} lon\n")
            f.write(f"- **Acción**: AGREGAR SITIOS MANUALMENTE\n\n")
        
        f.write("## 🟠 REGIONES MUY BAJAS (<20% esperado)\n\n")
        for p in high:
            f.write(f"### {p['region']} ({p['continent']})\n")
            f.write(f"- **Esperado**: {p['expected']} sitios\n")
            f.write(f"- **Actual**: {p['count']} sitios ({p['count']/p['expected']*100:.1f}%)\n")
            f.write(f"- **Coordenadas**: {p['coords'][0]} a {p['coords'][1]} lat, {p['coords'][2]} a {p['coords'][3]} lon\n")
            f.write(f"- **Acción**: MEJORAR HARVESTING\n\n")
        
        f.write("## 🟡 REGIONES BAJAS (<50% esperado)\n\n")
        for p in medium:
            f.write(f"### {p['region']} ({p['continent']})\n")
            f.write(f"- **Esperado**: {p['expected']} sitios\n")
            f.write(f"- **Actual**: {p['count']} sitios ({p['count']/p['expected']*100:.1f}%)\n")
            f.write(f"- **Coordenadas**: {p['coords'][0]} a {p['coords'][1]} lat, {p['coords'][2]} a {p['coords'][3]} lon\n")
            f.write(f"- **Acción**: MEJORAR HARVESTING\n\n")
    
    print("✅ Reporte guardado en: GLOBAL_COVERAGE_AUDIT_REPORT.md")
    
    print("\n" + "=" * 100)
    print("✅ AUDITORÍA COMPLETADA")
    print(f"\n📊 RESUMEN:")
    print(f"   Total sitios: {total_sites:,}")
    print(f"   Regiones críticas (0 sitios): {len(critical)}")
    print(f"   Regiones muy bajas (<20%): {len(high)}")
    print(f"   Regiones bajas (<50%): {len(medium)}")
    print(f"   Sitios sin país: {no_country:,} ({no_country_pct:.1f}%)")

if __name__ == "__main__":
    try:
        audit_global_coverage()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
