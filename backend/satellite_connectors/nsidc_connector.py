"""
NSIDC Connector
Hielo histórico 1970s-presente
"""

import logging
import requests
from typing import Optional, Dict, Any
from datetime import datetime

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class NSIDCConnector(SatelliteConnector):
    """
    Conector a NSIDC (National Snow and Ice Data Center)
    
    Productos:
    - Sea Ice Index
    - Ice Age
    
    Series temporales: 1970s-presente
    API: https://nsidc.org/api/
    Gratuita
    """
    
    API_URL = "https://nsidc.org/api/seaiceindex/v1"
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "NSIDC"
        self.available = True
        logger.info("✅ NSIDC connector initialized")
    
    async def get_ice_extent_timeseries(
        self,
        hemisphere: str = "north",
        start_year: int = 1979,
        end_year: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Obtener serie temporal de extensión de hielo
        
        Args:
            hemisphere: "north" o "south"
            start_year: Año inicial (1979+)
            end_year: Año final (None = actual)
        """
        try:
            if end_year is None:
                end_year = datetime.now().year
            
            logger.info(f"🛰️ Requesting NSIDC ice extent {start_year}-{end_year}")
            
            # Endpoint para datos mensuales
            url = f"{self.API_URL}/monthly/{hemisphere}"
            
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                logger.error(f"NSIDC API error: {response.status_code}")
                return None
            
            data = response.json()
            
            # Filtrar por años
            filtered_data = [
                entry for entry in data['data']
                if start_year <= int(entry['year']) <= end_year
            ]
            
            # Extraer series temporales
            years = [int(entry['year']) for entry in filtered_data]
            months = [int(entry['month']) for entry in filtered_data]
            extents = [float(entry['extent']) for entry in filtered_data]
            
            timeseries = {
                'hemisphere': hemisphere,
                'years': years,
                'months': months,
                'ice_extent_million_km2': extents,
                'mean_extent': sum(extents) / len(extents) if extents else 0,
                'min_extent': min(extents) if extents else 0,
                'max_extent': max(extents) if extents else 0,
                'data_points': len(extents)
            }
            
            logger.info(f"✅ NSIDC timeseries: {len(extents)} points")
            
            return timeseries
            
        except Exception as e:
            logger.error(f"Error fetching NSIDC data: {e}", exc_info=True)
            return None
