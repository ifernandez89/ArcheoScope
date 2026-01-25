#!/usr/bin/env python3
"""
Clasificar todos los sitios arqueológicos por tipo de terreno
Usa el TerrainClassifier de 2 capas (reglas duras + ML)
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from database import db
from terrain_classifier import terrain_classifier, TerrainType

async def classify_all_sites():
    """Clasificar todos los sitios en la base de datos"""
    
    print("="*60)
    print("🗺️ CLASIFICACIÓN DE TERRENO - TODOS LOS SITIOS")
    print("="*60)
    print("\nEnfoque de 2 capas:")
    print("  1. Reglas duras (casos obvios)")
    print("  2. Random Forest / Heurísticas (casos ambiguos)")
    print()
    
    # Conectar a base de datos
    print("🔌 Conectando a PostgreSQL...")
    await db.connect()
    print("✅ Conectado")
    
    # Obtener total de sitios
    total_sites = await db.count_sites()
    print(f"\n📊 Total de sitios a clasificar: {total_sites:,}")
    
    # Preguntar confirmación
    response = input("\n¿Continuar con la clasificación? (s/n): ").strip().lower()
    if response != 's':
        print("❌ Clasificación cancelada")
        await db.close()
        return 1
    
    print("\n🚀 Iniciando clasificación...")
    print("⚠️ Esto puede tomar varios minutos...")
    
    # Estadísticas
    stats = {
        'total': 0,
        'updated': 0,
        'errors': 0,
        'by_terrain': {}
    }
    
    # Procesar en lotes
    batch_size = 1000
    offset = 0
    
    while offset < total_sites:
        # Obtener lote de sitios
        query = '''
            SELECT id, latitude, longitude, name
            FROM archaeological_sites
            ORDER BY id
            LIMIT $1 OFFSET $2
        '''
        
        async with db.pool.acquire() as conn:
            sites = await conn.fetch(query, batch_size, offset)
        
        if not sites:
            break
        
        # Clasificar cada sitio
        for site in sites:
            stats['total'] += 1
            
            try:
                # Clasificar usando coordenadas
                classification = terrain_classifier.classify_from_coordinates(
                    latitude=site['latitude'],
                    longitude=site['longitude']
                )
                
                # Mapear TerrainType a EnvironmentType (enum PostgreSQL)
                terrain_map = {
                    TerrainType.WATER: 'SHALLOW_SEA',
                    TerrainType.DESERT: 'DESERT',
                    TerrainType.VEGETATION: 'FOREST',
                    TerrainType.MOUNTAIN: 'MOUNTAIN',
                    TerrainType.ICE_SNOW: 'GLACIER',
                    TerrainType.WETLAND: 'WETLAND',
                    TerrainType.ANCIENT_URBAN: 'URBAN',
                    TerrainType.UNKNOWN: 'UNKNOWN'
                }
                
                environment_type = terrain_map.get(
                    classification.terrain_type,
                    'UNKNOWN'
                )
                
                # Actualizar en base de datos
                update_query = '''
                    UPDATE archaeological_sites
                    SET 
                        "environmentType" = $1,
                        "updatedAt" = NOW()
                    WHERE id = $2
                '''
                
                async with db.pool.acquire() as conn:
                    await conn.execute(update_query, environment_type, site['id'])
                
                stats['updated'] += 1
                
                # Estadísticas por terreno
                terrain_name = classification.terrain_type.name
                stats['by_terrain'][terrain_name] = stats['by_terrain'].get(terrain_name, 0) + 1
                
                # Progreso cada 100 sitios
                if stats['total'] % 100 == 0:
                    print(f"  Procesados: {stats['total']:,}/{total_sites:,} ({stats['total']/total_sites*100:.1f}%)")
            
            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] <= 5:  # Mostrar solo primeros 5 errores
                    print(f"  ⚠️ Error en sitio {site['name']}: {e}")
        
        offset += batch_size
    
    # Cerrar conexión
    await db.close()
    
    # Resultados
    print("\n" + "="*60)
    print("📊 RESULTADOS DE CLASIFICACIÓN")
    print("="*60)
    print(f"Sitios procesados: {stats['total']:,}")
    print(f"Sitios actualizados: {stats['updated']:,}")
    print(f"Errores: {stats['errors']:,}")
    
    print("\n📈 Distribución por tipo de terreno:")
    for terrain, count in sorted(stats['by_terrain'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"  {terrain:15s}: {count:6,} sitios ({percentage:5.2f}%)")
    
    print("="*60)
    
    print("\n✅ CLASIFICACIÓN COMPLETADA")
    print(f"\nPróximos pasos:")
    print(f"  1. Verificar distribución: python check_environment_values.py")
    print(f"  2. Test endpoints: python test_new_endpoints.py")
    print(f"  3. Ajustar instrumentos según terreno")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(classify_all_sites()))
