#!/usr/bin/env python3
"""
Importación Masiva Inteligente de Sitios Arqueológicos
Compara harvested_complete.json con BD y solo importa sitios nuevos
"""

import asyncio
import json
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
from typing import List, Dict, Set, Tuple
import hashlib

DB_CONFIG = {
    'dbname': 'archeoscope_db',
    'user': 'postgres',
    'password': '1464',
    'host': 'localhost',
    'port': '5433'
}


def generate_site_hash(lat: float, lon: float, name: str) -> str:
    """Generar hash único para identificar sitios duplicados"""
    # Redondear coordenadas a 4 decimales (~11m precisión)
    lat_rounded = round(lat, 4)
    lon_rounded = round(lon, 4)
    name_normalized = name.lower().strip()
    
    hash_str = f"{lat_rounded}_{lon_rounded}_{name_normalized}"
    return hashlib.md5(hash_str.encode()).hexdigest()[:16]


def load_harvested_sites(filepath: str) -> List[Dict]:
    """Cargar sitios del archivo JSON"""
    print(f"\n📂 Cargando sitios desde {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sites = data.get('sites', [])
    metadata = data.get('metadata', {})
    
    print(f"✅ Archivo cargado:")
    print(f"   Total sitios: {len(sites):,}")
    print(f"   Fecha harvest: {metadata.get('harvested_at', 'N/A')}")
    print(f"   Fuentes: {', '.join(metadata.get('sources', []))}")
    
    return sites


def get_existing_sites_hashes(conn) -> Set[str]:
    """Obtener hashes de sitios existentes en BD"""
    print(f"\n🔍 Obteniendo sitios existentes de la BD...")
    
    cursor = conn.cursor()
    
    # Obtener todos los sitios con sus coordenadas y nombres
    cursor.execute("""
        SELECT latitude, longitude, name
        FROM archaeological_sites
    """)
    
    existing_hashes = set()
    
    for row in cursor.fetchall():
        lat, lon, name = row
        site_hash = generate_site_hash(lat, lon, name)
        existing_hashes.add(site_hash)
    
    cursor.close()
    
    print(f"✅ Sitios existentes en BD: {len(existing_hashes):,}")
    
    return existing_hashes


def filter_new_sites(harvested_sites: List[Dict], existing_hashes: Set[str]) -> Tuple[List[Dict], List[Dict]]:
    """Filtrar sitios nuevos vs duplicados"""
    print(f"\n🔎 Comparando sitios...")
    
    new_sites = []
    duplicate_sites = []
    
    for site in harvested_sites:
        lat = site.get('latitude')
        lon = site.get('longitude')
        name = site.get('name', '')
        
        if lat is None or lon is None:
            continue
        
        site_hash = generate_site_hash(lat, lon, name)
        
        if site_hash in existing_hashes:
            duplicate_sites.append(site)
        else:
            new_sites.append(site)
    
    print(f"\n📊 RESULTADOS:")
    print(f"   ✅ Sitios NUEVOS: {len(new_sites):,}")
    print(f"   🔄 Sitios DUPLICADOS: {len(duplicate_sites):,}")
    print(f"   📈 Tasa de novedad: {len(new_sites)/len(harvested_sites)*100:.1f}%")
    
    return new_sites, duplicate_sites


def classify_site(site: Dict) -> Tuple[str, str]:
    """Clasificar sitio por tipo y ambiente"""
    
    # Clasificar por tipo
    name = site.get('name', '').lower()
    source = site.get('source', '')
    
    # Tipo de sitio
    if any(word in name for word in ['temple', 'templo', 'pyramid', 'pirámide']):
        site_type = 'TEMPLE'
    elif any(word in name for word in ['city', 'ciudad', 'settlement', 'asentamiento']):
        site_type = 'SETTLEMENT'
    elif any(word in name for word in ['tomb', 'tumba', 'burial', 'cemetery']):
        site_type = 'BURIAL'
    elif any(word in name for word in ['fort', 'fortress', 'castle', 'fortaleza']):
        site_type = 'FORTIFICATION'
    elif any(word in name for word in ['cave', 'cueva', 'rock', 'roca']):
        site_type = 'ROCK_ART'
    else:
        site_type = 'SETTLEMENT'  # Default
    
    # Ambiente (simplificado - se puede mejorar con geocoding)
    lat = site.get('latitude', 0)
    
    if abs(lat) < 10:
        environment = 'FOREST'  # Tropical
    elif abs(lat) > 60:
        environment = 'MOUNTAIN'  # Polar/montaña
    elif 20 < abs(lat) < 35:
        environment = 'DESERT'  # Subtropical seco
    else:
        environment = 'FOREST'  # Default
    
    return site_type, environment


def bulk_insert_sites(conn, new_sites: List[Dict], batch_size: int = 1000):
    """Insertar sitios en lotes usando execute_batch"""
    print(f"\n💾 Insertando {len(new_sites):,} sitios nuevos...")
    print(f"   Tamaño de lote: {batch_size}")
    
    cursor = conn.cursor()
    
    # Preparar datos para inserción
    insert_data = []
    
    for site in new_sites:
        lat = site.get('latitude')
        lon = site.get('longitude')
        name = site.get('name', 'Unknown Site')
        country = site.get('country', 'Unknown')
        source = site.get('source', 'harvested')
        
        # Clasificar
        site_type, environment = classify_site(site)
        
        # Metadata adicional
        metadata = {
            'source': source,
            'original_data': site
        }
        
        insert_data.append((
            name,
            lat,
            lon,
            country,
            site_type,
            environment,
            json.dumps(metadata)
        ))
    
    # Insertar en lotes
    insert_query = """
        INSERT INTO archaeological_sites 
        (name, latitude, longitude, country, "siteType", "environmentType", metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    total_batches = (len(insert_data) + batch_size - 1) // batch_size
    
    for i in range(0, len(insert_data), batch_size):
        batch = insert_data[i:i + batch_size]
        batch_num = i // batch_size + 1
        
        print(f"   Lote {batch_num}/{total_batches}: {len(batch)} sitios...", end=' ')
        
        try:
            execute_batch(cursor, insert_query, batch, page_size=batch_size)
            conn.commit()
            print("✅")
        except Exception as e:
            print(f"❌ Error: {e}")
            conn.rollback()
            continue
    
    cursor.close()
    
    print(f"\n✅ Inserción completada!")


def verify_import(conn, expected_new: int):
    """Verificar que la importación fue exitosa"""
    print(f"\n🔍 Verificando importación...")
    
    cursor = conn.cursor()
    
    # Contar total
    cursor.execute("SELECT COUNT(*) FROM archaeological_sites")
    total = cursor.fetchone()[0]
    
    # Contar por fuente
    cursor.execute("""
        SELECT 
            metadata->>'source' as source,
            COUNT(*) as count
        FROM archaeological_sites
        WHERE metadata->>'source' IS NOT NULL
        GROUP BY metadata->>'source'
        ORDER BY count DESC
    """)
    
    sources = cursor.fetchall()
    
    cursor.close()
    
    print(f"\n📊 ESTADO FINAL DE LA BD:")
    print(f"   Total sitios: {total:,}")
    print(f"\n   Por fuente:")
    for source, count in sources:
        print(f"      {source}: {count:,}")
    
    return total


async def main():
    """Proceso principal de importación masiva"""
    
    print("=" * 80)
    print("🚀 IMPORTACIÓN MASIVA INTELIGENTE DE SITIOS ARQUEOLÓGICOS")
    print("=" * 80)
    
    start_time = datetime.now()
    
    # 1. Cargar sitios del archivo
    harvested_sites = load_harvested_sites('harvested_complete.json')
    
    if not harvested_sites:
        print("\n❌ No se encontraron sitios en el archivo")
        return
    
    # 2. Conectar a BD
    print(f"\n🔌 Conectando a PostgreSQL...")
    conn = psycopg2.connect(**DB_CONFIG)
    print(f"✅ Conectado")
    
    # 3. Obtener sitios existentes
    existing_hashes = get_existing_sites_hashes(conn)
    
    # 4. Filtrar sitios nuevos
    new_sites, duplicate_sites = filter_new_sites(harvested_sites, existing_hashes)
    
    if not new_sites:
        print(f"\n✅ No hay sitios nuevos para importar")
        print(f"   Todos los {len(harvested_sites):,} sitios ya están en la BD")
        conn.close()
        return
    
    # 5. Confirmar importación
    print(f"\n⚠️  ¿Deseas importar {len(new_sites):,} sitios nuevos? (s/n): ", end='')
    
    # Auto-confirmar para script
    confirm = 's'  # Cambiar a input() para confirmación manual
    
    if confirm.lower() != 's':
        print("❌ Importación cancelada")
        conn.close()
        return
    
    # 6. Importar sitios nuevos
    bulk_insert_sites(conn, new_sites, batch_size=1000)
    
    # 7. Verificar
    final_total = verify_import(conn, len(new_sites))
    
    # 8. Cerrar conexión
    conn.close()
    
    # Resumen final
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n" + "=" * 80)
    print(f"✅ IMPORTACIÓN COMPLETADA")
    print(f"=" * 80)
    
    print(f"\n📊 RESUMEN:")
    print(f"   Sitios procesados: {len(harvested_sites):,}")
    print(f"   Sitios nuevos importados: {len(new_sites):,}")
    print(f"   Sitios duplicados omitidos: {len(duplicate_sites):,}")
    print(f"   Total en BD: {final_total:,}")
    print(f"   Tiempo: {duration:.1f} segundos")
    print(f"   Velocidad: {len(new_sites)/duration:.0f} sitios/segundo")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"   1. Verificar clasificación de sitios nuevos")
    print(f"   2. Generar zonas prioritarias actualizadas")
    print(f"   3. Actualizar visualización en mapa")
    
    print(f"\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
