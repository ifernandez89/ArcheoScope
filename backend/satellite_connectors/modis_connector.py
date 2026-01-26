"""
MODIS Connector - NASA AppEEARS
Térmico regional y NDVI
"""

import logging
from datetime import datetime
from typing import Optional
import os

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class MODISConnector(SatelliteConnector):
    """
    Conector a MODIS via AppEEARS
    
    Productos:
    - MOD11A1: LST Daily (1km)
    - MOD13A1: NDVI 16-day (250m)
    
    API: https://appeears.earthdatacloud.nasa.gov/api/
    Gratuita con NASA Earthdata
    """
    
    API_URL = "https://appeears.earthdatacloud.nasa.gov/api/"
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "MODIS"
        self.username = os.getenv("EARTHDATA_USERNAME")
        self.password = os.getenv("EARTHDATA_PASSWORD")
        
        if not self.username or not self.password:
            logger.warning("MODIS requires EARTHDATA_USERNAME and EARTHDATA_PASSWORD")
            self.available = False
        else:
            self.available = True
            logger.info("✅ MODIS connector initialized")
    
    async def get_lst_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Optional[SatelliteData]:
        """Obtener LST de MODIS"""
        # TODO: Implementar con AppEEARS API
        # Por ahora retornar None para usar fallback
        logger.warning("MODIS LST not yet implemented - using fallback")
        return None
