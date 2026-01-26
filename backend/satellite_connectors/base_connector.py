"""
Base Connector para APIs Satelitales
Define interfaz común para todos los conectores
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
import numpy as np


@dataclass
class SatelliteData:
    """Datos satelitales procesados"""
    
    # Metadata
    source: str  # 'sentinel-2', 'sentinel-1', 'landsat-8', etc.
    acquisition_date: datetime
    cloud_cover: float  # 0-100%
    resolution_m: float
    
    # Coordenadas
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    
    # Datos procesados
    bands: Dict[str, np.ndarray]  # {'red': array, 'nir': array, ...}
    indices: Dict[str, float]  # {'ndvi': 0.45, 'ndwi': 0.23, ...}
    
    # Anomalías detectadas
    anomaly_score: float  # 0-1
    anomaly_type: str  # 'vegetation_stress', 'thermal_anomaly', etc.
    confidence: float  # 0-1
    
    # Metadata adicional
    processing_time_s: float
    cached: bool = False


class SatelliteConnector(ABC):
    """Clase base para conectores satelitales"""
    
    def __init__(self, cache_enabled: bool = True):
        self.cache_enabled = cache_enabled
        self.name = "BaseConnector"
    
    @abstractmethod
    async def get_multispectral_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        max_cloud_cover: float = 20.0
    ) -> Optional[SatelliteData]:
        """
        Obtener datos multiespectrales (Sentinel-2, Landsat)
        
        Returns:
            SatelliteData con bandas RGB, NIR, SWIR y índices calculados
        """
        pass
    
    @abstractmethod
    async def get_sar_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[SatelliteData]:
        """
        Obtener datos SAR (Sentinel-1)
        
        Returns:
            SatelliteData con backscatter VV, VH y coherencia
        """
        pass
    
    @abstractmethod
    async def get_thermal_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[SatelliteData]:
        """
        Obtener datos térmicos (Landsat-8/9)
        
        Returns:
            SatelliteData con temperatura superficial (LST)
        """
        pass
    
    def calculate_ndvi(self, red: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """Calcular NDVI (Normalized Difference Vegetation Index)"""
        with np.errstate(divide='ignore', invalid='ignore'):
            ndvi = (nir - red) / (nir + red)
            ndvi = np.nan_to_num(ndvi, nan=0.0)
        return ndvi
    
    def calculate_ndwi(self, green: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """Calcular NDWI (Normalized Difference Water Index)"""
        with np.errstate(divide='ignore', invalid='ignore'):
            ndwi = (green - nir) / (green + nir)
            ndwi = np.nan_to_num(ndwi, nan=0.0)
        return ndwi
    
    def calculate_ndbi(self, swir: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """Calcular NDBI (Normalized Difference Built-up Index)"""
        with np.errstate(divide='ignore', invalid='ignore'):
            ndbi = (swir - nir) / (swir + nir)
            ndbi = np.nan_to_num(ndbi, nan=0.0)
        return ndbi
    
    def detect_anomaly(
        self,
        data: np.ndarray,
        threshold_std: float = 2.0
    ) -> tuple[float, float]:
        """
        Detectar anomalías estadísticas en datos
        
        Returns:
            (anomaly_score, confidence)
        """
        if data.size == 0:
            return 0.0, 0.0
        
        mean = np.mean(data)
        std = np.std(data)
        
        if std == 0:
            return 0.0, 0.0
        
        # Calcular z-scores
        z_scores = np.abs((data - mean) / std)
        
        # Porcentaje de píxeles anómalos
        anomalous_pixels = np.sum(z_scores > threshold_std)
        anomaly_ratio = anomalous_pixels / data.size
        
        # Score basado en ratio y magnitud
        anomaly_score = min(anomaly_ratio * 2.0, 1.0)
        
        # Confianza basada en cantidad de datos
        confidence = min(data.size / 10000.0, 1.0)
        
        return float(anomaly_score), float(confidence)
