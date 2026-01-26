"""
OpenTopography Connector
High-resolution LiDAR and DEM data for archaeological detection

API Docs: https://portal.opentopography.org/apidocs/
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
import httpx
import numpy as np
from scipy.ndimage import generic_filter, gaussian_filter, maximum_filter, minimum_filter

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class OpenTopographyConnector(SatelliteConnector):
    """
    Conector a OpenTopography API
    
    Acceso a:
    - SRTM Global DEM (30m, 90m)
    - ALOS World 3D (30m)
    - COP30/COP90 (Copernicus DEM)
    - LiDAR point clouds (donde disponible)
    
    CRÍTICO para arqueología:
    - Detección de estructuras enterradas
    - Análisis de microtopografía
    - Identificación de patrones geométricos
    """
    
    BASE_URL = "https://portal.opentopography.org/API/globaldem"
    
    def __init__(self, api_key: Optional[str] = None, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "OpenTopography"
        
        # Cargar API key desde environment
        self.api_key = api_key or os.getenv("OPENTOPOGRAPHY_API_KEY")
        
        if not self.api_key:
            logger.warning("⚠️ OpenTopography API key no configurada")
            logger.warning("   Configura OPENTOPOGRAPHY_API_KEY en .env")
            self.available = False
        else:
            logger.info("✅ OpenTopography API key configurada")
            self.available = True
        
        # Timeout configuration
        self.timeout = float(os.getenv("OPENTOPOGRAPHY_TIMEOUT", "30"))  # 30s para descargas
        self.connect_timeout = float(os.getenv("SATELLITE_API_CONNECT_TIMEOUT", "5"))
    
    async def get_elevation_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        dem_type: str = "SRTMGL1"  # SRTMGL1 (30m), SRTMGL3 (90m), AW3D30, COP30
    ) -> Optional[Dict[str, Any]]:
        """
        Obtener datos de elevación de OpenTopography
        
        Args:
            lat_min, lat_max, lon_min, lon_max: Bounding box
            dem_type: Tipo de DEM
                - SRTMGL1: SRTM 30m (mejor para arqueología)
                - SRTMGL3: SRTM 90m
                - AW3D30: ALOS World 3D 30m
                - COP30: Copernicus DEM 30m
        
        Returns:
            Dict con estadísticas de elevación y análisis arqueológico
        """
        
        if not self.available:
            return None
        
        try:
            # Construir URL de request
            params = {
                "demtype": dem_type,
                "south": lat_min,
                "north": lat_max,
                "west": lon_min,
                "east": lon_max,
                "outputFormat": "GTiff",
                "API_Key": self.api_key
            }
            
            logger.info(f"🌍 Solicitando DEM de OpenTopography ({dem_type})...")
            logger.info(f"   Región: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
            
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout, connect=self.connect_timeout)
            ) as client:
                response = await client.get(self.BASE_URL, params=params)
                
                if response.status_code == 200:
                    # Guardar GeoTIFF temporalmente
                    import tempfile
                    import rasterio
                    
                    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
                        tmp.write(response.content)
                        tmp_path = tmp.name
                    
                    try:
                        # Leer con rasterio
                        with rasterio.open(tmp_path) as dataset:
                            elevation = dataset.read(1)
                            
                            # Análisis de elevación
                            stats = self._analyze_elevation(elevation)
                            
                            # Análisis arqueológico
                            archaeological_features = self._detect_archaeological_features(elevation)
                            
                            logger.info(f"✅ DEM obtenido: {elevation.shape}")
                            logger.info(f"   Elevación: {stats['elevation_min']:.1f}m - {stats['elevation_max']:.1f}m")
                            logger.info(f"   Rugosidad: {stats['roughness']:.3f}")
                            
                            return {
                                "source": f"OpenTopography {dem_type}",
                                "acquisition_date": datetime.now().isoformat(),
                                "resolution_m": 30 if "30" in dem_type or "GL1" in dem_type else 90,
                                "confidence": 0.95,  # OpenTopography es muy confiable
                                "data_mode": "REAL",
                                **stats,
                                **archaeological_features
                            }
                    finally:
                        # Limpiar archivo temporal
                        try:
                            os.unlink(tmp_path)
                        except:
                            pass
                
                elif response.status_code == 401:
                    logger.error("❌ OpenTopography: API key inválida")
                    self.available = False
                    return None
                
                elif response.status_code == 400:
                    logger.warning(f"⚠️ OpenTopography: Región no disponible o parámetros inválidos")
                    return None
                
                else:
                    logger.error(f"❌ OpenTopography error: {response.status_code}")
                    return None
        
        except httpx.TimeoutException:
            logger.warning(f"⏱️ OpenTopography timeout después de {self.timeout}s")
            return None
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo DEM de OpenTopography: {e}")
            return None
    
    def _analyze_elevation(self, elevation: np.ndarray) -> Dict[str, float]:
        """
        Analizar estadísticas de elevación
        """
        
        # Filtrar valores inválidos
        valid_elevation = elevation[~np.isnan(elevation)]
        
        if len(valid_elevation) == 0:
            return {
                "elevation_mean": 0.0,
                "elevation_min": 0.0,
                "elevation_max": 0.0,
                "elevation_std": 0.0,
                "roughness": 0.0,
                "slope_mean": 0.0
            }
        
        # Estadísticas básicas
        elev_mean = float(np.mean(valid_elevation))
        elev_min = float(np.min(valid_elevation))
        elev_max = float(np.max(valid_elevation))
        elev_std = float(np.std(valid_elevation))
        
        # Rugosidad (variación local)
        try:
            from scipy.ndimage import generic_filter
            roughness = float(np.nanmean(generic_filter(elevation, np.std, size=3)))
        except:
            roughness = elev_std
        
        # Pendiente aproximada
        try:
            grad_y, grad_x = np.gradient(elevation)
            slope = np.sqrt(grad_x**2 + grad_y**2)
            slope_mean = float(np.nanmean(slope))
        except:
            slope_mean = 0.0
        
        return {
            "elevation_mean": elev_mean,
            "elevation_min": elev_min,
            "elevation_max": elev_max,
            "elevation_std": elev_std,
            "roughness": roughness,
            "slope_mean": slope_mean
        }
    
    def _detect_archaeological_features(self, elevation: np.ndarray) -> Dict[str, Any]:
        """
        Detectar características arqueológicas en DEM
        
        Busca:
        - Plataformas artificiales (áreas planas anómalas)
        - Montículos (elevaciones locales)
        - Terrazas (cambios de pendiente regulares)
        - Patrones geométricos
        """
        
        features = {
            "platforms_detected": 0,
            "mounds_detected": 0,
            "terraces_detected": 0,
            "geometric_anomalies": 0,
            "archaeological_score": 0.0
        }
        
        try:
            from scipy.ndimage import gaussian_filter, maximum_filter, minimum_filter
            
            # Suavizar para reducir ruido
            smoothed = gaussian_filter(elevation, sigma=2)
            
            # Detectar plataformas (áreas planas en terreno irregular)
            local_std = generic_filter(smoothed, np.std, size=5)
            flat_areas = local_std < np.nanpercentile(local_std, 10)
            platforms = np.sum(flat_areas) / flat_areas.size
            
            # Detectar montículos (máximos locales)
            local_max = maximum_filter(smoothed, size=5)
            mounds = np.sum(smoothed == local_max) / smoothed.size
            
            # Detectar terrazas (cambios de pendiente)
            grad_y, grad_x = np.gradient(smoothed)
            slope = np.sqrt(grad_x**2 + grad_y**2)
            slope_changes = np.abs(np.gradient(slope)[0])
            terraces = np.sum(slope_changes > np.nanpercentile(slope_changes, 90)) / slope_changes.size
            
            # Score arqueológico (0-1)
            archaeological_score = (platforms * 0.4 + mounds * 0.3 + terraces * 0.3)
            
            features.update({
                "platforms_detected": int(platforms * 100),
                "mounds_detected": int(mounds * 100),
                "terraces_detected": int(terraces * 100),
                "archaeological_score": float(archaeological_score)
            })
        
        except Exception as e:
            logger.warning(f"⚠️ Error en detección arqueológica: {e}")
        
        return features
    
    async def get_lidar_availability(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Dict[str, Any]:
        """
        Verificar disponibilidad de datos LiDAR en región
        
        Returns:
            Dict con disponibilidad y metadatos
        """
        
        # OpenTopography tiene LiDAR limitado a ciertas regiones
        # Por ahora retornamos disponibilidad de DEM global
        
        return {
            "lidar_available": False,  # Requiere búsqueda específica
            "dem_available": True,
            "recommended_dem": "SRTMGL1",
            "resolution_m": 30
        }
