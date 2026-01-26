#!/usr/bin/env python3
"""
Script para generar raster global de probabilidad cultural
Fase 2: Escalado Global
"""

import sys
import asyncio
import numpy as np
from pathlib import Path
from typing import Tuple
import logging

# Agregar backend al path
sys.path.append(str(Path(__file__).parent.parent))

from backend.database import db
from backend.site_confidence_system import site_confidence_system

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_tile(lat_min: float, lat_max: float, 
                       lon_min: float, lon_max: float,
                       resolution: int = 100) -> np.ndarray:
    """
    Generar tile de prior cultural para una región
    
    Args:
        lat_min, lat_max, lon_min, lon_max: Bounds del tile
        resolution: Resolución del grid (pixels por lado)
    
    Returns:
        Array 2D con densidad cultural (0-1)
    """
    
    logger.info(f"Generando tile: {lat_min:.1f}-{lat_max:.1f}, {lon_min:.1f}-{lon_max:.1f}")
    
    # Buscar sitios en la región
    center_lat = (lat_min + lat_max) / 2
    center_lon = (lon_min + lon_max) / 2
    
    import math
    lat_diff = lat_max - lat_min
    lon_diff = lon_max - lon_min
    radius_km = math.sqrt(lat_diff**2 + lon_diff**2) * 111.32
    
    sites = await db.search_sites(center_lat, center_lon, radius_km, limit=10000)
    
    logger.info(f"  {len(sites)} sitios encontrados")
    
    # Convertir a formato para sistema de confianza
    sites_for_map = []
    for site in sites:
        sites_for_map.append({
            'id': site.get('id'),
            'name': site.get('name'),
            'latitude': site.get('latitude'),
            'longitude': site.get('longitude'),
            'source': 'osm',  # Simplificado
            'site_type': site.get('site_type'),
            'excavated': False,
            'references': None,
            'geometry_accuracy_m': 100.0,
            'period': site.get('period'),
            'source_count': 1
        })
    
    # Generar mapa cultural
    cultural_prior = site_confidence_system.create_cultural_prior_map(
        sites_for_map,
        grid_size=(resolution, resolution),
        bounds=(lat_min, lat_max, lon_min, lon_max)
    )
    
    return cultural_prior


async def generate_global_raster_tiles(output_dir: Path, tile_size: int = 10):
    """
    Generar raster global dividido en tiles
    
    Args:
        output_dir: Directorio de salida
        tile_size: Tamaño de cada tile en grados (default: 10°)
    """
    
    logger.info("="*80)
    logger.info("🌍 GENERACIÓN DE RASTER GLOBAL DE PROBABILIDAD CULTURAL")
    logger.info("="*80)
    logger.info()
    
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Conectar a BD
    await db.connect()
    
    try:
        total_tiles = 0
        completed_tiles = 0
        
        # Iterar por tiles (10° x 10°)
        for lat in range(-90, 90, tile_size):
            for lon in range(-180, 180, tile_size):
                total_tiles += 1
                
                lat_min = lat
                lat_max = min(lat + tile_size, 90)
                lon_min = lon
                lon_max = min(lon + tile_size, 180)
                
                try:
                    # Generar tile
                    tile = await generate_tile(lat_min, lat_max, lon_min, lon_max)
                    
                    # Guardar como numpy array
                    tile_filename = f"cultural_prior_lat{lat:+04d}_lon{lon:+04d}.npy"
                    tile_path = output_dir / tile_filename
                    
                    np.save(tile_path, tile)
                    
                    completed_tiles += 1
                    
                    logger.info(f"✅ Tile guardado: {tile_filename}")
                    logger.info(f"   Progreso: {completed_tiles}/{total_tiles} ({completed_tiles/total_tiles*100:.1f}%)")
                    logger.info()
                
                except Exception as e:
                    logger.error(f"❌ Error generando tile {lat},{lon}: {e}")
        
        logger.info("="*80)
        logger.info(f"✅ COMPLETADO: {completed_tiles}/{total_tiles} tiles generados")
        logger.info("="*80)
        logger.info()
        logger.info(f"Tiles guardados en: {output_dir}")
        logger.info()
        logger.info("Próximos pasos:")
        logger.info("  1. Convertir tiles a GeoTIFF")
        logger.info("  2. Generar pirámide de tiles para visualización")
        logger.info("  3. Servir via tile server (TileServer GL, etc.)")
        logger.info()
    
    finally:
        await db.close()


async def generate_sample_region(output_file: Path):
    """
    Generar raster de muestra para una región (Egipto)
    """
    
    logger.info("="*80)
    logger.info("🗺️ GENERACIÓN DE RASTER DE MUESTRA - EGIPTO")
    logger.info("="*80)
    logger.info()
    
    await db.connect()
    
    try:
        # Región de Egipto
        lat_min, lat_max = 22.0, 32.0
        lon_min, lon_max = 25.0, 35.0
        
        logger.info(f"Región: Egipto")
        logger.info(f"  Bounds: {lat_min}-{lat_max}, {lon_min}-{lon_max}")
        logger.info()
        
        # Generar raster de alta resolución
        tile = await generate_tile(lat_min, lat_max, lon_min, lon_max, resolution=500)
        
        # Guardar
        np.save(output_file, tile)
        
        logger.info(f"✅ Raster guardado: {output_file}")
        logger.info(f"   Resolución: {tile.shape}")
        logger.info(f"   Densidad máxima: {tile.max():.3f}")
        logger.info(f"   Densidad promedio: {tile.mean():.3f}")
        logger.info()
    
    finally:
        await db.close()


def main():
    """Función principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Generar raster global de probabilidad cultural')
    parser.add_argument('--global', dest='generate_global', action='store_true',
                       help='Generar raster global (tiles de 10°)')
    parser.add_argument('--sample', action='store_true',
                       help='Generar raster de muestra (Egipto)')
    parser.add_argument('--output-dir', type=str, default='global_cultural_prior',
                       help='Directorio de salida para tiles')
    
    args = parser.parse_args()
    
    if args.generate_global:
        output_dir = Path(args.output_dir)
        asyncio.run(generate_global_raster_tiles(output_dir))
    elif args.sample:
        output_file = Path('egypt_cultural_prior_sample.npy')
        asyncio.run(generate_sample_region(output_file))
    else:
        print("Uso:")
        print("  python scripts/generate_global_cultural_prior.py --sample")
        print("  python scripts/generate_global_cultural_prior.py --global")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
