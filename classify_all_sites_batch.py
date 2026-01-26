#!/usr/bin/env python3
"""
Clasificar TODOS los 80,000+ sitios en la base de datos
Proceso por lotes para no sobrecargar el sistema
"""

import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch
import sys
import os

# Agregar el directorio backend al path
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

def classify_all_sites():
    """Clasificar todos los sitios en lotes"""
    
    print("🚀 CLASIFICACIÓN MASIVA DE 80,000+ SITIOS")
    print("=" * 100)
    
    # Inicializar clasificadores
    print("\n📦 Inicializando clasificadores...")
    env_classifier = EnvironmentClassifier()
    terrain_classifier = TerrainClassifier()
    print("✅ Clasificadores listos")
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    # Contar sitios a clasificar
    cursor.execute("""
        SELECT COUNT(*) as total
        FROM archaeological_sites
        WHERE "siteType" = 'UNKNOWN'
    """)
    total_to_classify = cursor.fetchone()['total']
    
    print(f"\n📊 Sitios a clasificar: {total_to_classify:,}")
    print(f"⏱️  Tiempo estimado: {total_to_classify / 1000:.1f} minutos (1000 sitios/min)")
    
    # Procesar en lotes de 1000
    batch_size = 1000
    offset = 0
    classified_count = 0
    
    while offset < total_to_classify:
        print(f"\n🔄 Procesando lote {offset//batch_size + 1} ({offset:,} - {min(offset+batch_size, total_to_classify):,})")
        
        # Obtener lote de sitios
        cursor.execute("""
            SELECT id, latitude, longitude, name, "siteType"
            FROM archaeological_sites
            WHERE "siteType" = 'UNKNOWN'
            ORDER BY id
            LIMIT %s OFFSET %s
        """, (batch_size, offset))
        
        sites = cursor.fetchall()
        
        if not sites:
            break
        
        # Clasificar cada sitio
        updates = []
        for site in sites:
            try:
                # Clasificar terreno
                terrain_result = terrain_classifier.classify_terrain(
                    site['latitude'],
                    site['longitude']
                )
                
                # Mapear terrain a siteType (heurística simple)
                site_type = map_terrain_to_site_type(terrain_result['terrain_type'], site['name'])
                
                updates.append((
                    site_type,
                    site['id']
                ))
                
                classified_count += 1
                
            except Exception as e:
                print(f"   ⚠️  Error clasificando {site['id']}: {e}")
                continue
        
        # Actualizar en batch
        if updates:
            execute_batch(cursor, """
                UPDATE archaeological_sites
                SET "siteType" = %s
                WHERE id = %s
            """, updates)
            conn.commit()
            
            print(f"   ✅ {len(updates)} sitios clasificados")
        
        offset += batch_size
        
        # Mostrar progreso
        progress = (classified_count / total_to_classify * 100)
        print(f"   📈 Progreso: {classified_count:,}/{total_to_classify:,} ({progress:.1f}%)")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 100)
    print("✅ CLASIFICACIÓN COMPLETADA")
    print(f"\n📊 Total clasificados: {classified_count:,}")
    print(f"⏱️  Tiempo total: {classified_count / 1000:.1f} minutos")

def map_terrain_to_site_type(terrain_type: str, site_name: str) -> str:
    """
    Mapear tipo de terreno a tipo de sitio arqueológico
    Usa heurística basada en terreno y nombre
    """
    
    # Palabras clave en el nombre
    name_lower = site_name.lower() if site_name else ''
    
    # Mapeo por palabras clave
    if any(word in name_lower for word in ['temple', 'church', 'cathedral', 'mosque', 'shrine', 'sanctuary']):
        return 'TEMPLE_COMPLEX'
    
    if any(word in name_lower for word in ['fort', 'castle', 'fortress', 'wall', 'defense']):
        return 'FORTIFICATION'
    
    if any(word in name_lower for word in ['tomb', 'cemetery', 'burial', 'grave', 'necropolis', 'mausoleum']):
        return 'BURIAL_SITE'
    
    if any(word in name_lower for word in ['city', 'town', 'settlement', 'village', 'urban']):
        return 'URBAN_SETTLEMENT'
    
    if any(word in name_lower for word in ['pyramid', 'ziggurat', 'mound', 'tumulus']):
        return 'MONUMENTAL_COMPLEX'
    
    if any(word in name_lower for word in ['stone', 'megalith', 'dolmen', 'menhir', 'cromlech']):
        return 'MEGALITHIC_MONUMENT'
    
    if any(word in name_lower for word in ['farm', 'field', 'terrace', 'irrigation', 'agricultural']):
        return 'AGRICULTURAL_SITE'
    
    # Mapeo por tipo de terreno
    terrain_to_site = {
        'desert': 'CEREMONIAL_CENTER',  # Desiertos suelen tener centros ceremoniales
        'mountain': 'MOUNTAIN_CITADEL',  # Montañas suelen tener ciudadelas
        'forest': 'URBAN_SETTLEMENT',    # Bosques suelen tener asentamientos
        'grassland': 'AGRICULTURAL_SITE', # Praderas suelen tener sitios agrícolas
        'coastal': 'URBAN_SETTLEMENT',   # Costas suelen tener asentamientos
        'glacier': 'UNKNOWN',            # Glaciares son raros
        'water': 'UNKNOWN'               # Agua es raro
    }
    
    return terrain_to_site.get(terrain_type, 'CEREMONIAL_CENTER')

if __name__ == "__main__":
    try:
        response = input("⚠️  Esto clasificará 80,000+ sitios. ¿Continuar? (s/n): ")
        if response.lower() == 's':
            classify_all_sites()
        else:
            print("❌ Cancelado")
    except KeyboardInterrupt:
        print("\n❌ Interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
