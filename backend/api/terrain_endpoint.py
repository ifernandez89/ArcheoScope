"""
Terrain Data API Endpoint

Sirve datos DEM (Digital Elevation Model) para el frontend con sistema de caché inteligente.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional
import numpy as np
import logging

# Importar servicio de terreno
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from terrain_data_service import terrain_service, prefetch_common_sites

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/terrain")


class TerrainRequest(BaseModel):
    """Solicitud de datos de terreno"""
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    resolution: int = 256  # Resolución del heightmap


class TerrainResponse(BaseModel):
    """Respuesta con datos de terreno"""
    tile_id: str
    bounds: Dict[str, float]
    resolution: float  # metros por píxel
    source: str
    data_shape: List[int]
    elevation_range: List[float]
    data: List[List[float]]  # Heightmap 2D


class CacheStatsResponse(BaseModel):
    """Estadísticas del caché"""
    memory_tiles: int
    disk_tiles: int
    disk_size_mb: float
    cache_dir: str


@router.post("/data", response_model=TerrainResponse)
async def get_terrain_data(request: TerrainRequest):
    """
    Obtiene datos DEM para un área específica
    
    Estrategia de caché:
    1. Buscar en memoria
    2. Buscar en disco
    3. Descargar de fuente remota
    4. Generar sintético como fallback
    """
    try:
        logger.info(f"📥 Terrain request: {request.lat_min:.4f},{request.lon_min:.4f} to {request.lat_max:.4f},{request.lon_max:.4f}")
        
        # Obtener tile del servicio
        tile = terrain_service.get_terrain_data(
            lat_min=request.lat_min,
            lat_max=request.lat_max,
            lon_min=request.lon_min,
            lon_max=request.lon_max,
            resolution=request.resolution
        )
        
        if not tile:
            raise HTTPException(status_code=500, detail="No se pudo obtener datos de terreno")
        
        # Convertir numpy array a lista para JSON
        data_list = tile.data.tolist()
        
        response = TerrainResponse(
            tile_id=tile.tile_id,
            bounds=tile.bounds,
            resolution=tile.resolution,
            source=tile.source,
            data_shape=list(tile.data.shape),
            elevation_range=[float(tile.data.min()), float(tile.data.max())],
            data=data_list
        )
        
        logger.info(f"✅ Terrain data served: {tile.tile_id} ({tile.source})")
        
        return response
    
    except Exception as e:
        logger.error(f"❌ Error getting terrain data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/stats", response_model=CacheStatsResponse)
async def get_cache_stats():
    """Obtiene estadísticas del caché de terreno"""
    try:
        stats = terrain_service.get_cache_stats()
        
        return CacheStatsResponse(
            memory_tiles=stats['memory_tiles'],
            disk_tiles=stats['disk_tiles'],
            disk_size_mb=stats['disk_size_mb'],
            cache_dir=stats['cache_dir']
        )
    
    except Exception as e:
        logger.error(f"❌ Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/clear")
async def clear_cache(older_than_days: int = Query(30, ge=1, le=365)):
    """Limpia caché antiguo"""
    try:
        cleared = terrain_service.clear_cache(older_than_days=older_than_days)
        
        return {
            "status": "success",
            "cleared_tiles": cleared,
            "message": f"Cleared {cleared} tiles older than {older_than_days} days"
        }
    
    except Exception as e:
        logger.error(f"❌ Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/prefetch/common-sites")
async def prefetch_common_archaeological_sites():
    """Pre-descarga tiles para sitios arqueológicos comunes"""
    try:
        prefetch_common_sites()
        
        return {
            "status": "success",
            "message": "Prefetch initiated for common archaeological sites"
        }
    
    except Exception as e:
        logger.error(f"❌ Error prefetching sites: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_terrain_info():
    """Información sobre el sistema de terreno"""
    return {
        "name": "Terrain Data Service",
        "version": "1.0.0",
        "sources": {
            "opentopography": {
                "resolution": "30m",
                "coverage": "global",
                "status": "available" if terrain_service.sources['opentopography']['api_key'] else "requires_api_key"
            },
            "copernicus": {
                "resolution": "30m",
                "coverage": "global",
                "status": "available"
            },
            "srtm": {
                "resolution": "90m",
                "coverage": "60N-56S",
                "status": "available"
            },
            "synthetic": {
                "resolution": "variable",
                "coverage": "global",
                "status": "fallback"
            }
        },
        "cache": terrain_service.get_cache_stats()
    }
