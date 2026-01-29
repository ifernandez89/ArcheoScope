#!/usr/bin/env python3
"""
Copernicus DEM Connector - DEM Global 30m GRATIS
================================================

PRIORIDAD 3: Eliminar ruido SRTM/ICESat

Fuente: https://registry.opendata.aws/copernicus-dem/
Resolución: 30m (GLO-30)
Cobertura: Global (-90 a +90)
Costo: GRATIS (AWS Open Data)
API Key: NO REQUERIDA

Ventajas vs SRTM:
- ✅ Gratis (sin autenticación)
- ✅ 30m resolución (vs 90m SRTM)
- ✅ Sin vacíos (mejor corrección)
- ✅ Actualizado (2021 vs 2000)
- ✅ Global completo
"""

import httpx
import rasterio
from rasterio.merge import merge
from rasterio.mask import mask
import numpy as np
import tempfile
import os
from typing import Dict, Any, Optional, List, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CopernicusDEMConnector:
    """
    Conector a Copernicus DEM GLO-30.
    
    DEM global de 30m sin API key requerida.
    """
    
    def __init__(self):
        """Inicializar conector Copernicus DEM."""
        
        self.base_url = "https://copernicus-dem-30m.s3.amazonaws.com"
        self.available = True  # Siempre disponible (sin auth)
        self.resolution_m = 30
        
        logger.info("🗻 Copernicus DEM Connector initialized (30m, gratis)")
    
    async def get_elevation_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Optional[Dict[str, Any]]:
        """
        Obtener datos de elevación Copernicus DEM.
        
        Args:
            lat_min, lat_max: Rango de latitud
            lon_min, lon_max: Rango de longitud
        
        Returns:
            Dict con estadísticas de elevación o None si falla
        """
        
        try:
            logger.info(f"🗻 Copernicus DEM: Obteniendo elevación para bbox [{lat_min:.2f}, {lat_max:.2f}] x [{lon_min:.2f}, {lon_max:.2f}]")
            
            # Calcular tiles necesarios
            tiles = self._calculate_tiles(lat_min, lat_max, lon_min, lon_max)
            
            if not tiles:
                logger.warning("⚠️ No tiles found for bbox")
                return None
            
            logger.info(f"   📦 Descargando {len(tiles)} tiles...")
            
            # Descargar tiles
            tile_paths = []
            for tile_name in tiles:
                tile_path = await self._download_tile(tile_name)
                if tile_path:
                    tile_paths.append(tile_path)
            
            if not tile_paths:
                logger.warning("⚠️ No tiles downloaded successfully")
                return None
            
            logger.info(f"   ✅ {len(tile_paths)} tiles descargados")
            
            # Merge tiles si hay más de uno
            if len(tile_paths) > 1:
                merged_path = self._merge_tiles(tile_paths)
            else:
                merged_path = tile_paths[0]
            
            # Crop a bbox exacto
            elevation_data = self._crop_to_bbox(
                merged_path, lat_min, lat_max, lon_min, lon_max
            )
            
            if elevation_data is None or elevation_data.size == 0:
                logger.warning("⚠️ No elevation data after crop")
                return None
            
            # Filtrar NoData
            valid_mask = elevation_data != -32768  # NoData value
            valid_elevations = elevation_data[valid_mask]
            
            if len(valid_elevations) == 0:
                logger.warning("⚠️ No valid elevations found")
                return None
            
            # Calcular estadísticas
            stats = {
                'mean_elevation': float(np.mean(valid_elevations)),
                'min_elevation': float(np.min(valid_elevations)),
                'max_elevation': float(np.max(valid_elevations)),
                'std_elevation': float(np.std(valid_elevations)),
                'elevation_range': float(np.max(valid_elevations) - np.min(valid_elevations)),
                'median_elevation': float(np.median(valid_elevations))
            }
            
            # Calcular roughness (rugosidad)
            roughness = self._calculate_roughness(elevation_data, valid_mask)
            
            logger.info(f"   ✅ Elevación: {stats['mean_elevation']:.1f}m (±{stats['std_elevation']:.1f}m)")
            
            # Limpiar archivos temporales
            for path in tile_paths:
                try:
                    os.unlink(path)
                except:
                    pass
            
            return {
                'value': stats['mean_elevation'],
                'elevation_stats': stats,
                'roughness': roughness,
                'pixel_count': int(np.sum(valid_mask)),
                'unit': 'meters',
                'source': 'Copernicus_DEM_GLO30',
                'dem_status': 'HIGH_RES',  # ✅ Copernicus es HIGH_RES
                'resolution_m': 30,
                'quality': 'high',
                'acquisition_date': '2021-01-01',  # Copernicus DEM 2021
                'processing_notes': 'Copernicus DEM GLO-30 (30m resolution, free)'
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo Copernicus DEM: {e}")
            return None
    
    def _calculate_tiles(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> List[str]:
        """
        Calcular tiles Copernicus DEM necesarios.
        
        Tiles son 1°x1° con nomenclatura:
        - Latitud: N00-N89, S01-S90
        - Longitud: E000-E179, W001-W180
        
        Ejemplo: N29E031 (29°N, 31°E)
        """
        
        tiles = []
        
        # Redondear a grados enteros
        lat_start = int(np.floor(lat_min))
        lat_end = int(np.floor(lat_max))
        lon_start = int(np.floor(lon_min))
        lon_end = int(np.floor(lon_max))
        
        for lat in range(lat_start, lat_end + 1):
            for lon in range(lon_start, lon_end + 1):
                tile_name = self._format_tile_name(lat, lon)
                tiles.append(tile_name)
        
        return tiles
    
    def _format_tile_name(self, lat: int, lon: int) -> str:
        """
        Formatear nombre de tile Copernicus.
        
        Ejemplos:
        - (29, 31) → "Copernicus_DSM_COG_10_N29_00_E031_00_DEM"
        - (-16, -68) → "Copernicus_DSM_COG_10_S16_00_W068_00_DEM"
        """
        
        # Latitud
        if lat >= 0:
            lat_str = f"N{abs(lat):02d}_00"
        else:
            lat_str = f"S{abs(lat):02d}_00"
        
        # Longitud
        if lon >= 0:
            lon_str = f"E{abs(lon):03d}_00"
        else:
            lon_str = f"W{abs(lon):03d}_00"
        
        return f"Copernicus_DSM_COG_10_{lat_str}_{lon_str}_DEM"
    
    async def _download_tile(self, tile_name: str) -> Optional[str]:
        """
        Descargar tile desde S3 público.
        
        Args:
            tile_name: Nombre del tile
        
        Returns:
            Path al archivo descargado o None si falla
        """
        
        try:
            # URL del tile
            url = f"{self.base_url}/{tile_name}/{tile_name}.tif"
            
            # Descargar
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                
                if response.status_code == 200:
                    # Guardar temporalmente
                    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp_file:
                        tmp_file.write(response.content)
                        return tmp_file.name
                else:
                    logger.warning(f"   ⚠️ Tile {tile_name}: HTTP {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.warning(f"   ⚠️ Error descargando tile {tile_name}: {e}")
            return None
    
    def _merge_tiles(self, tile_paths: List[str]) -> str:
        """
        Merge múltiples tiles en uno solo.
        
        Args:
            tile_paths: Lista de paths a tiles
        
        Returns:
            Path al tile merged
        """
        
        try:
            # Abrir todos los tiles
            src_files = [rasterio.open(path) for path in tile_paths]
            
            # Merge
            mosaic, out_trans = merge(src_files)
            
            # Cerrar archivos
            for src in src_files:
                src.close()
            
            # Guardar merged
            with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp_file:
                merged_path = tmp_file.name
            
            # Escribir merged
            with rasterio.open(
                merged_path,
                'w',
                driver='GTiff',
                height=mosaic.shape[1],
                width=mosaic.shape[2],
                count=1,
                dtype=mosaic.dtype,
                crs=src_files[0].crs,
                transform=out_trans
            ) as dst:
                dst.write(mosaic[0], 1)
            
            return merged_path
            
        except Exception as e:
            logger.error(f"Error merging tiles: {e}")
            return tile_paths[0]  # Fallback al primer tile
    
    def _crop_to_bbox(
        self,
        raster_path: str,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Optional[np.ndarray]:
        """
        Crop raster a bbox exacto.
        
        Args:
            raster_path: Path al raster
            lat_min, lat_max, lon_min, lon_max: Bbox
        
        Returns:
            Array con elevaciones o None
        """
        
        try:
            with rasterio.open(raster_path) as src:
                # Crear geometría bbox
                from shapely.geometry import box
                bbox_geom = box(lon_min, lat_min, lon_max, lat_max)
                
                # Crop
                out_image, out_transform = mask(src, [bbox_geom], crop=True)
                
                return out_image[0]
                
        except Exception as e:
            logger.error(f"Error cropping raster: {e}")
            return None
    
    def _calculate_roughness(
        self,
        elevation_data: np.ndarray,
        valid_mask: np.ndarray
    ) -> float:
        """
        Calcular rugosidad del terreno.
        
        Roughness = std de diferencias locales
        """
        
        try:
            # Aplicar máscara
            masked_data = np.where(valid_mask, elevation_data, np.nan)
            
            # Calcular gradientes
            grad_x = np.gradient(masked_data, axis=1)
            grad_y = np.gradient(masked_data, axis=0)
            
            # Magnitud del gradiente
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            
            # Roughness = std del gradiente
            roughness = float(np.nanstd(gradient_magnitude))
            
            return roughness
            
        except Exception:
            return 0.0


if __name__ == "__main__":
    # Test
    import asyncio
    
    async def test_copernicus_dem():
        """Test del conector."""
        
        print("="*80)
        print("TEST: Copernicus DEM Connector")
        print("="*80)
        
        connector = CopernicusDEMConnector()
        
        # Test: Giza, Egipto
        print("\nTest: Giza, Egipto")
        result = await connector.get_elevation_data(
            lat_min=29.95,
            lat_max=30.05,
            lon_min=31.10,
            lon_max=31.20
        )
        
        if result:
            print(f"✅ Elevación: {result['value']:.1f}m")
            print(f"   Rango: {result['elevation_stats']['min_elevation']:.1f} - {result['elevation_stats']['max_elevation']:.1f}m")
            print(f"   Roughness: {result['roughness']:.3f}")
            print(f"   DEM Status: {result['dem_status']}")
        else:
            print("❌ Failed")
        
        print("\n" + "="*80)
    
    asyncio.run(test_copernicus_dem())
