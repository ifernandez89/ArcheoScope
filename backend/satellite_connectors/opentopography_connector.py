"""
OpenTopography Connector
DEM de alta resolución (SRTM, ALOS, COP30)
"""

import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional
import numpy as np
import os

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class OpenTopographyConnector(SatelliteConnector):
    """
    Conector a OpenTopography
    
    Productos:
    - SRTM 30m (Global)
    - ALOS 30m (Global)
    - COP30 (Copernicus 30m)
    
    API: https://portal.opentopography.org/API
    Gratuita con API key
    """
    
    API_URL = "https://portal.opentopography.org/API/globaldem"
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "OpenTopography"
        self.api_key = os.getenv("OPENTOPOGRAPHY_API_KEY")
        
        if not self.api_key:
            logger.warning(
                "OpenTopography API key not found. "
                "Set OPENTOPOGRAPHY_API_KEY in .env.local"
            )
            self.available = False
        else:
            self.available = True
            logger.info("✅ OpenTopography connector initialized")
    
    async def get_dem_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        dem_type: str = "SRTMGL1"
    ) -> Optional[SatelliteData]:
        """
        Obtener DEM de OpenTopography
        
        Args:
            dem_type: "SRTMGL1" (30m), "SRTMGL3" (90m), "AW3D30" (ALOS 30m), "COP30" (Copernicus 30m)
        """
        if not self.available:
            logger.error("OpenTopography not available")
            return None
        
        try:
            logger.info(f"🛰️ Requesting {dem_type} DEM from OpenTopography")
            
            params = {
                'demtype': dem_type,
                'south': lat_min,
                'north': lat_max,
                'west': lon_min,
                'east': lon_max,
                'outputFormat': 'GTiff',
                'API_Key': self.api_key
            }
            
            response = requests.get(self.API_URL, params=params, timeout=60)
            
            if response.status_code != 200:
                logger.error(f"OpenTopography API error: {response.status_code}")
                return None
            
            # Guardar GeoTIFF temporalmente
            temp_file = f"./cache/opentopography/dem_{lat_min}_{lon_min}.tif"
            os.makedirs(os.path.dirname(temp_file), exist_ok=True)
            
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            
            # Leer con rasterio
            try:
                import rasterio
                with rasterio.open(temp_file) as src:
                    dem = src.read(1)
                    
                    # Calcular estadísticas
                    indices = {
                        'elevation_mean': float(np.nanmean(dem)),
                        'elevation_std': float(np.nanstd(dem)),
                        'elevation_min': float(np.nanmin(dem)),
                        'elevation_max': float(np.nanmax(dem)),
                        'slope_mean': self._calculate_slope(dem),
                        'roughness': float(np.nanstd(dem))
                    }
                    
                    # Detectar anomalías topográficas
                    mean_elev = np.nanmean(dem)
                    std_elev = np.nanstd(dem)
                    anomalies = np.abs(dem - mean_elev) > (2 * std_elev)
                    
                    anomaly_score = float(np.sum(anomalies) / dem.size)
                    confidence = "high"
                    
                    # Tipo de anomalía
                    if indices['slope_mean'] > 15:
                        anomaly_type = 'steep_terrain'
                    elif indices['roughness'] > 50:
                        anomaly_type = 'rough_terrain'
                    elif anomaly_score > 0.1:
                        anomaly_type = 'topographic_anomaly'
                    else:
                        anomaly_type = 'flat_terrain'
                    
                    logger.info(f"✅ OpenTopography DEM processed: {dem.shape}")
                    
                    return SatelliteData(
                        source=f'opentopography-{dem_type.lower()}',
                        acquisition_date=datetime.now(),
                        cloud_cover=0.0,
                        resolution_m=30.0,
                        lat_min=lat_min,
                        lat_max=lat_max,
                        lon_min=lon_min,
                        lon_max=lon_max,
                        bands={'elevation': dem},
                        indices=indices,
                        anomaly_score=anomaly_score,
                        anomaly_type=anomaly_type,
                        confidence=confidence,
                        processing_time_s=0.0,
                        cached=False
                    )
            
            except ImportError:
                logger.error("rasterio not installed. Install with: pip install rasterio")
                return None
            
        except Exception as e:
            logger.error(f"Error fetching OpenTopography data: {e}", exc_info=True)
            return None
    
    def _calculate_slope(self, dem: np.ndarray) -> float:
        """Calcular pendiente promedio"""
        try:
            from scipy.ndimage import sobel
            sx = sobel(dem, axis=0, mode='constant')
            sy = sobel(dem, axis=1, mode='constant')
            slope = np.sqrt(sx**2 + sy**2)
            return float(np.nanmean(slope))
        except:
            return 0.0
