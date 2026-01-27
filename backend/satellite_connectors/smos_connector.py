"""
SMOS Connector - Copernicus CDS
Salinidad y humedad del suelo
"""

import logging
from typing import Optional
import os
import sys
from pathlib import Path

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
    
    ACTUALIZADO: 2026-01-26 - Lee credenciales desde BD encriptadas
    """
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "SMOS"
        
        # Cargar credenciales desde BD
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from credentials_manager import CredentialsManager
            
            creds_manager = CredentialsManager()
            self.cds_url = creds_manager.get_credential("copernicus_cds", "url")
            self.cds_api_key = creds_manager.get_credential("copernicus_cds", "api_key")
        except Exception as e:
            logger.warning(f"Error cargando credenciales CDS desde BD: {e}")
            self.cds_url = None
            self.cds_api_key = None
        
        if not SMOS_AVAILABLE:
            logger.warning("SMOS requires: pip install cdsapi")
            self.available = False
        elif not self.cds_api_key:
            logger.warning("SMOS requires Copernicus CDS credentials in BD")
            logger.info("Configure with: python backend/credentials_manager.py")
            self.available = False
        else:
            self.available = True
            logger.info("✅ SMOS connector initialized (CDS credentials from BD)")
    
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
