#!/usr/bin/env python3
"""
Actualizar base de datos PostgreSQL con datos enriquecidos
"""

import json
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Agregar backend al path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from database import db

async def update_enriched_data(enriched_file: Path):
    """Actualizar base de datos con datos enriquecidos"""
    
    print("="*60)
    print("📊 ACTUALIZACIÓN DE BASE DE DATOS CON DATOS ENRIQUECIDOS")
    print("="*60)
    
    # Cargar datos enriquecidos
    print(f"\n📂 Cargando {enriched_file.name}...")
    
    with open(enriched_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sites = data.get('sites', [])
    print(f"✅ Cargados {len(sites):,} sitios enriquecidos")
    
    # Conectar a base de datos
    print("\n🔌 Conectando a PostgreSQL...")
    await db.connect()
    print("✅ Conectado")
    
    # Actualizar sitios
    updated = 0
    errors = 0
    
    print(f"\n🔄 Actualizando {len(sites):,} sitios...")
    
    for i, site in enumerate(sites, 1):
        try:
            # Buscar sitio por coordenadas (aproximadas)
            lat = site.get('latitude')
            lon = site.get('longitude')
            
            if not lat or not lon:
                continue
            
            # Query para encontrar sitio existente
            query = """
                UPDATE archaeological_sites
                SET 
                    period = COALESCE($1, period),
                    culture = $2,
                    "dateRangeStart" = $3,
                    "imageUrl" = $4,
                    "heritageDesignation" = $5,
                    "wikipediaUrl" = $6,
                    "wikidataEnriched" = $7,
                    "unescoStatus" = $8,
                    "enrichedAt" = $9
                WHERE 
                    latitude BETWEEN $10 - 0.001 AND $10 + 0.001
                    AND longitude BETWEEN $11 - 0.001 AND $11 + 0.001
                    AND name = $12
                RETURNING id
            """
            
            async with db.pool.acquire() as conn:
                result = await conn.fetchrow(
                    query,
                    site.get('period_detailed'),
                    site.get('culture'),
                    site.get('date_established'),
                    site.get('image_url'),
                    site.get('heritage_designation'),
                    site.get('wikipedia_url'),
                    site.get('wikidata_enriched', False),
                    site.get('unesco_status', 'not_listed'),
                    site.get('enriched_at'),
                    lat,
                    lon,
                    site.get('name')
                )
                
                if result:
                    updated += 1
                    
                    if updated % 10 == 0:
                        print(f"  Actualizados: {updated}/{len(sites)}")
        
        except Exception as e:
            errors += 1
            if errors <= 5:  # Mostrar solo primeros 5 errores
                print(f"  ⚠️ Error actualizando {site.get('name')}: {e}")
    
    # Cerrar conexión
    await db.close()
    
    # Resultados
    print("\n" + "="*60)
    print("📊 RESULTADOS DE ACTUALIZACIÓN")
    print("="*60)
    print(f"Sitios procesados: {len(sites):,}")
    print(f"Sitios actualizados: {updated:,}")
    print(f"Errores: {errors:,}")
    print("="*60)
    
    return updated > 0


async def main():
    """Función principal"""
    
    # Buscar archivo más reciente de datos enriquecidos
    enriched_files = list(Path(__file__).parent.parent.glob("enriched_sites_*.json"))
    
    if not enriched_files:
        print("❌ No se encontraron archivos de datos enriquecidos")
        print("\nEjecuta primero: python scripts/enrich_archaeological_data.py")
        return 1
    
    # Usar el más reciente
    enriched_file = max(enriched_files, key=lambda p: p.stat().st_mtime)
    
    print(f"📂 Usando archivo: {enriched_file.name}")
    
    success = await update_enriched_data(enriched_file)
    
    if success:
        print("\n✅ ACTUALIZACIÓN COMPLETADA")
        return 0
    else:
        print("\n❌ ACTUALIZACIÓN FALLÓ")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
