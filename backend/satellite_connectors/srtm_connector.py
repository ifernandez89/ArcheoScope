#!/usr/bin/env python3
"""
SRTM DEM Connector - Shuttle Radar Topography Mission
====================================================

SRTM (NASA) - Instrumento 12/15
- Resolución: 30m (SRTM-GL1) y 90m (SRTM-GL3)
- Cobertura: 60°N - 56°S (99% de superficie terrestre habitada)
- Producto: Modelo Digital de Elevación
- API: NASA Earthdata + OpenTopography

APLICACIONES ARQUEOLÓGICAS:
- Detección de montículos artificiales
- Análisis de terrazas y estructuras
- Modelado de visibilidad y accesibilidad
- Detección de anomalías topográficas
"""

import requests
import numpy as np
import logging
from typing import Dict, Any, Optional, Tuple
import json
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
import tempfile
import os

logger = logging.getLogger(__name__)

class SRTMConnector:
    """Conector para datos SRTM DEM via múltiples fuentes."""
    
    def __init__(self):
        """Inicializar conector SRTM."""
        
        # URLs de diferentes fuentes SRTM
        self.sources = {
            'opentopography': 'https://cloud.sdsc.edu/v1/raster',
            'earthdata': 'https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003',
            'usgs': 'https://elevation-api.io/api/elevation'
        }
        
        # Credenciales Earthdata (hasheadas en BD)
        import os
        self.earthdata_token = os.getenv('EARTHDATA_TOKEN')
        
        logger.info("🏔️ SRTM DEM Connector initialized")
    
    async def get_elevation_data(self, lat_min: float, lat_max: float,
                                lon_min: float, lon_max: float,
                                resolution: str = '30m') -> Dict[str, Any]:
        """
        Obtener datos de elevación SRTM.
        
        Args:
            resolution: '30m' (SRTM-GL1) o '90m' (SRTM-GL3)
        """
        
        try:
            # Intentar diferentes fuentes en orden de preferencia
            sources_to_try = [
                ('opentopography', self._get_srtm_opentopography),
                ('usgs_api', self._get_srtm_usgs_api),
                ('earthdata', self._get_srtm_earthdata)
            ]
            
            for source_name, source_func in sources_to_try:
                try:
                    result = await source_func(lat_min, lat_max, lon_min, lon_max, resolution)
                    if result:
                        result['source'] = f'SRTM_{source_name}'
                        return result
                except Exception as e:
                    logger.warning(f"SRTM {source_name} failed: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo datos SRTM: {e}")
            return None
    
    async def _get_srtm_opentopography(self, lat_min: float, lat_max: float,
                                      lon_min: float, lon_max: float,
                                      resolution: str) -> Optional[Dict[str, Any]]:
        """Obtener SRTM via OpenTopography API."""
        
        try:
            # Mapear resolución a dataset OpenTopography
            dataset_map = {
                '30m': 'SRTMGL1',
                '90m': 'SRTMGL3'
            }
            
            dataset = dataset_map.get(resolution, 'SRTMGL1')
            
            params = {
                'demtype': dataset,
                'south': lat_min,
                'north': lat_max,
                'west': lon_min,
                'east': lon_max,
                'outputFormat': 'GTiff',
                'API_Key': os.getenv('OPENTOPOGRAPHY_API_KEY')
            }
            
            response = requests.get(
                f"{self.sources['opentopography']}/globaldem",
                params=params,
                timeout=60
            )
            
            if response.status_code == 200:
                # Guardar temporalmente el GeoTIFF
                with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_path = tmp_file.name
                
                try:
                    # Leer con rasterio
                    with rasterio.open(tmp_path) as dataset:
                        # Leer datos de elevación
                        elevation_data = dataset.read(1)
                        
                        # Filtrar valores NoData
                        valid_mask = elevation_data != dataset.nodata
                        valid_elevations = elevation_data[valid_mask]
                        
                        if len(valid_elevations) > 0:
                            stats = {
                                'mean_elevation': float(np.mean(valid_elevations)),
                                'min_elevation': float(np.min(valid_elevations)),
                                'max_elevation': float(np.max(valid_elevations)),
                                'std_elevation': float(np.std(valid_elevations)),
                                'elevation_range': float(np.max(valid_elevations) - np.min(valid_elevations))
                            }
                            
                            # Detectar anomalías topográficas
                            anomalies = self._detect_topographic_anomalies(elevation_data, valid_mask)
                            
                            return {
                                'value': stats['mean_elevation'],
                                'elevation_stats': stats,
                                'topographic_anomalies': anomalies,
                                'pixel_count': int(np.sum(valid_mask)),
                                'unit': 'meters',
                                'resolution_m': 30 if resolution == '30m' else 90,
                                'quality': 'high' if len(valid_elevations) > 100 else 'medium'
                            }
                
                finally:
                    # Limpiar archivo temporal
                    os.unlink(tmp_path)
            
            return None
            
        except Exception as e:
            logger.error(f"Error OpenTopography SRTM: {e}")
            return None
    
    async def _get_srtm_usgs_api(self, lat_min: float, lat_max: float,
                                lon_min: float, lon_max: float,
                                resolution: str) -> Optional[Dict[str, Any]]:
        """Obtener SRTM via USGS Elevation API."""
        
        try:
            # Crear grid de puntos para muestreo
            lat_points = np.linspace(lat_min, lat_max, 10)
            lon_points = np.linspace(lon_min, lon_max, 10)
            
            elevations = []
            
            for lat in lat_points:
                for lon in lon_points:
                    try:
                        response = requests.get(
                            f"{self.sources['usgs']}/point",
                            params={
                                'lat': lat,
                                'lon': lon,
                                'dataset': 'srtm30m' if resolution == '30m' else 'srtm90m'
                            },
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            if 'elevation' in data and data['elevation'] is not None:
                                elevations.append(data['elevation'])
                    
                    except Exception:
                        continue
            
            if elevations:
                return {
                    'value': float(np.mean(elevations)),
                    'elevation_stats': {
                        'mean_elevation': float(np.mean(elevations)),
                        'min_elevation': float(np.min(elevations)),
                        'max_elevation': float(np.max(elevations)),
                        'std_elevation': float(np.std(elevations)),
                        'elevation_range': float(np.max(elevations) - np.min(elevations))
                    },
                    'pixel_count': len(elevations),
                    'unit': 'meters',
                    'resolution_m': 30 if resolution == '30m' else 90,
                    'quality': 'medium'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error USGS SRTM API: {e}")
            return None
    
    async def _get_srtm_earthdata(self, lat_min: float, lat_max: float,
                                 lon_min: float, lon_max: float,
                                 resolution: str) -> Optional[Dict[str, Any]]:
        """Obtener SRTM via NASA Earthdata (requiere autenticación)."""
        
        try:
            if not self.earthdata_token:
                return None
            
            # Implementación simplificada - en producción usar CMR API
            # Por ahora retornar None para usar otras fuentes
            return None
            
        except Exception as e:
            logger.error(f"Error Earthdata SRTM: {e}")
            return None
    
    def _detect_topographic_anomalies(self, elevation_data: np.ndarray, 
                                     valid_mask: np.ndarray) -> Dict[str, Any]:
        """
        Detectar anomalías topográficas que podrían ser arqueológicas.
        
        ALGORITMOS:
        - Detección de montículos (elevaciones locales)
        - Detección de terrazas (cambios abruptos de pendiente)
        - Análisis de rugosidad superficial
        """
        
        try:
            # Calcular gradientes (pendientes)
            grad_y, grad_x = np.gradient(elevation_data)
            slope = np.sqrt(grad_x**2 + grad_y**2)
            
            # Detectar montículos (máximos locales)
            from scipy import ndimage
            local_maxima = ndimage.maximum_filter(elevation_data, size=3) == elevation_data
            significant_maxima = local_maxima & (elevation_data > np.percentile(elevation_data[valid_mask], 75))
            
            # Detectar terrazas (cambios abruptos de pendiente)
            slope_changes = np.abs(np.gradient(slope))
            terraces = slope_changes > np.percentile(slope_changes[valid_mask], 90)
            
            # Calcular rugosidad
            roughness = ndimage.standard_deviation(elevation_data, size=3)
            
            anomalies = {
                'mound_count': int(np.sum(significant_maxima & valid_mask)),
                'terrace_pixels': int(np.sum(terraces & valid_mask)),
                'mean_slope': float(np.mean(slope[valid_mask])),
                'max_slope': float(np.max(slope[valid_mask])),
                'mean_roughness': float(np.mean(roughness[valid_mask])),
                'topographic_complexity': float(np.std(elevation_data[valid_mask]) / np.mean(elevation_data[valid_mask]))
            }
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detectando anomalías topográficas: {e}")
            return {}
    
    async def get_slope_analysis(self, lat_min: float, lat_max: float,
                                lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        Análisis específico de pendientes para arqueología.
        
        APLICACIÓN: Detectar terrazas artificiales y modificaciones del terreno
        """
        
        try:
            elevation_data = await self.get_elevation_data(lat_min, lat_max, lon_min, lon_max)
            
            if not elevation_data:
                return None
            
            # Análisis de pendientes específico para arqueología
            stats = elevation_data.get('elevation_stats', {})
            anomalies = elevation_data.get('topographic_anomalies', {})
            
            # Clasificar pendientes arqueológicamente relevantes
            slope_classification = {
                'flat_areas': 0,      # < 2° - posibles plazas, patios
                'gentle_slopes': 0,   # 2-8° - terrazas agrícolas
                'moderate_slopes': 0, # 8-15° - estructuras defensivas
                'steep_slopes': 0     # > 15° - muros, acantilados
            }
            
            mean_slope = anomalies.get('mean_slope', 0)
            if mean_slope < 2:
                slope_classification['flat_areas'] = 1
            elif mean_slope < 8:
                slope_classification['gentle_slopes'] = 1
            elif mean_slope < 15:
                slope_classification['moderate_slopes'] = 1
            else:
                slope_classification['steep_slopes'] = 1
            
            return {
                'value': mean_slope,
                'slope_classification': slope_classification,
                'archaeological_indicators': {
                    'potential_terraces': anomalies.get('terrace_pixels', 0) > 10,
                    'potential_mounds': anomalies.get('mound_count', 0) > 0,
                    'terrain_modification_score': anomalies.get('topographic_complexity', 0)
                },
                'unit': 'degrees',
                'source': 'SRTM_slope_analysis',
                'quality': 'high' if elevation_data.get('pixel_count', 0) > 100 else 'medium'
            }
            
        except Exception as e:
            logger.error(f"Error en análisis de pendientes: {e}")
            return None