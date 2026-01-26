"""
SMAP Connector - NASA Earthdata
Humedad del suelo para permafrost
"""

import logging
from typing import Optional
import os

try:
    import earthaccess
    SMAP_AVAILABLE = True
except ImportError:
    SMAP_AVAILABLE = False

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class SMAPConnector(SatelliteConnector):
    """
    Conector a SMAP via NASA Earthdata
    
    Producto: SMAP L3 Soil Moisture
    Resolución: 36km
    API: NASA Earthdata (gratuita con registro)
    """
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "SMAP"
        
        if not SMAP_AVAILABLE:
            logger.warning("SMAP requires: pip install earthaccess")
            self.available = False
        else:
            self.available = True
            logger.info("✅ SMAP connector initialized")
    
    async def get_soil_moisture(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Optional[SatelliteData]:
        """Obtener humedad del suelo"""
        # TODO: Implementar con NASA Earthdata
        logger.warning("SMAP not yet implemented - using fallback")
        return None
