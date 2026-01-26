"""
SMOS Connector - Copernicus CDS
Salinidad y humedad del suelo
"""

import logging
from typing import Optional
import os

try:
    import cdsapi
    SMOS_AVAILABLE = True
except ImportError:
    SMOS_AVAILABLE = False

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class SMOSConnector(SatelliteConnector):
    """
    Conector a SMOS via Copernicus CDS
    
    Producto: SMOS L3 Soil Moisture
    Resolución: 25km
    API: Copernicus CDS (gratuita con registro)
    """
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "SMOS"
        self.api_key = os.getenv("CDS_API_KEY")
        
        if not SMOS_AVAILABLE:
            logger.warning("SMOS requires: pip install cdsapi")
            self.available = False
        elif not self.api_key:
            logger.warning("SMOS requires CDS_API_KEY in .env.local")
            self.available = False
        else:
            self.available = True
            logger.info("✅ SMOS connector initialized")
    
    async def get_soil_moisture(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Optional[SatelliteData]:
        """Obtener humedad del suelo"""
        # TODO: Implementar con CDS API
        logger.warning("SMOS not yet implemented - using fallback")
        return None
