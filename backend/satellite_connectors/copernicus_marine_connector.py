"""
Copernicus Marine Connector
Hielo marino con series temporales 1993-2023+
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import numpy as np
import os

try:
    import copernicusmarine
    COPERNICUS_MARINE_AVAILABLE = True
except ImportError:
    COPERNICUS_MARINE_AVAILABLE = False

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class CopernicusMarineConnector(SatelliteConnector):
    """
    Conector a Copernicus Marine Service
    
    Productos:
    - SEAICE_GLO_SEAICE_L4_NRT_OBSERVATIONS: Hielo marino global
    - Variables: concentración, tipo, borde, deriva
    
    Resolución: Diaria/Semanal
    Cobertura: Global (Ártico + Antártico) desde 1993
    API: Copernicus Marine (gratuita con registro)
    """
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "CopernicusMarine"
        self.username = os.getenv("COPERNICUS_MARINE_USERNAME")
        self.password = os.getenv("COPERNICUS_MARINE_PASSWORD")
        
        if not COPERNICUS_MARINE_AVAILABLE:
            logger.warning(
                "Copernicus Marine not available. "
                "Install with: pip install copernicusmarine"
            )
            self.available = False
        elif not self.username or not self.password:
            logger.warning(
                "Copernicus Marine credentials not found. "
                "Set COPERNICUS_MARINE_USERNAME and COPERNICUS_MARINE_PASSWORD in .env.local"
            )
            self.available = False
        else:
            self.available = True
            logger.info("✅ Copernicus Marine connector initialized")
    
    async def get_sea_ice_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[SatelliteData]:
        """
        Obtener datos de hielo marino
        
        Variables:
        - ice_concentration: Concentración de hielo (0-100%)
        - ice_type: Tipo de hielo
        - ice_edge: Borde del hielo
        - ice_drift: Deriva del hielo
        """
        if not self.available:
            logger.error("Copernicus Marine not available")
            return None
        
        try:
            # Fechas por defecto: últimos 30 días
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                start_date = end_date - timedelta(days=30)
            
            logger.info(f"🛰️ Requesting Copernicus Marine sea ice data")
            
            # Dataset ID para hielo marino
            dataset_id = "SEAICE_GLO_SEAICE_L4_NRT_OBSERVATIONS_011_001"
            
            # Descargar datos
            data = copernicusmarine.open_dataset(
                dataset_id=dataset_id,
                username=self.username,
                password=self.password,
                minimum_longitude=lon_min,
                maximum_longitude=lon_max,
                minimum_latitude=lat_min,
                maximum_latitude=lat_max,
                start_datetime=start_date.isoformat(),
                end_datetime=end_date.isoformat(),
                variables=["ice_concentration", "ice_type"]
            )
            
            # Extraer concentración de hielo
            ice_conc = data['ice_concentration'].values
            
            # Calcular estadísticas
            indices = {
                'ice_concentration_mean': float(np.nanmean(ice_conc)),
                'ice_concentration_std': float(np.nanstd(ice_conc)),
                'ice_concentration_max': float(np.nanmax(ice_conc)),
                'ice_coverage_percent': float(np.sum(ice_conc > 15) / ice_conc.size * 100),
                'temporal_variability': float(np.nanstd(np.nanmean(ice_conc, axis=(1,2))))
            }
            
            # Detectar anomalías de hielo
            mean_conc = np.nanmean(ice_conc)
            anomaly_score = mean_conc / 100.0  # Normalizar a 0-1
            confidence = "high"
            
            # Tipo de anomalía
            if mean_conc > 80:
                anomaly_type = 'heavy_ice_cover'
            elif mean_conc > 50:
                anomaly_type = 'moderate_ice_cover'
            elif mean_conc > 15:
                anomaly_type = 'light_ice_cover'
            else:
                anomaly_type = 'ice_free'
            
            logger.info(f"✅ Copernicus Marine processed: {ice_conc.shape}")
            
            return SatelliteData(
                source='copernicus-marine-seaice',
                acquisition_date=end_date,
                cloud_cover=0.0,
                resolution_m=10000.0,  # ~10km
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                bands={'ice_concentration': ice_conc},
                indices=indices,
                anomaly_score=anomaly_score,
                anomaly_type=anomaly_type,
                confidence=confidence,
                processing_time_s=0.0,
                cached=False
            )
            
        except Exception as e:
            logger.error(f"Error fetching Copernicus Marine data: {e}", exc_info=True)
            return None
    
    async def get_ice_timeseries(
        self,
        lat: float,
        lon: float,
        start_year: int = 1993,
        end_year: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Obtener serie temporal de hielo marino (1993-presente)
        
        Returns:
            Dict con series temporales de concentración, tendencia, estacionalidad
        """
        if not self.available:
            logger.error("Copernicus Marine not available")
            return None
        
        try:
            if end_year is None:
                end_year = datetime.now().year
            
            logger.info(f"🛰️ Requesting ice timeseries {start_year}-{end_year}")
            
            # Dataset de reanálisis (histórico)
            dataset_id = "SEAICE_GLO_SEAICE_L4_REP_OBSERVATIONS_011_009"
            
            start_date = datetime(start_year, 1, 1)
            end_date = datetime(end_year, 12, 31)
            
            # Descargar serie temporal
            data = copernicusmarine.open_dataset(
                dataset_id=dataset_id,
                username=self.username,
                password=self.password,
                minimum_longitude=lon - 0.5,
                maximum_longitude=lon + 0.5,
                minimum_latitude=lat - 0.5,
                maximum_latitude=lat + 0.5,
                start_datetime=start_date.isoformat(),
                end_datetime=end_date.isoformat(),
                variables=["ice_concentration"]
            )
            
            # Extraer serie temporal
            ice_conc_series = data['ice_concentration'].mean(dim=['latitude', 'longitude']).values
            times = data['time'].values
            
            # Calcular tendencia
            from scipy import stats
            x = np.arange(len(ice_conc_series))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, ice_conc_series)
            
            # Detectar estacionalidad
            monthly_mean = []
            for month in range(1, 13):
                month_mask = [t.month == month for t in times]
                monthly_mean.append(float(np.nanmean(ice_conc_series[month_mask])))
            
            timeseries = {
                'years': list(range(start_year, end_year + 1)),
                'ice_concentration': ice_conc_series.tolist(),
                'trend_slope': float(slope),
                'trend_r2': float(r_value**2),
                'trend_p_value': float(p_value),
                'monthly_climatology': monthly_mean,
                'mean_concentration': float(np.nanmean(ice_conc_series)),
                'std_concentration': float(np.nanstd(ice_conc_series))
            }
            
            logger.info(f"✅ Ice timeseries processed: {len(ice_conc_series)} points")
            
            return timeseries
            
        except Exception as e:
            logger.error(f"Error fetching ice timeseries: {e}", exc_info=True)
            return None
