"""
ArcheoScope Satellite Connectors
Conectores a APIs reales gratuitas de datos satelitales
"""

from .base_connector import SatelliteConnector, SatelliteData
from .planetary_computer import PlanetaryComputerConnector
from .icesat2_connector import ICESat2Connector
from .opentopography_connector import OpenTopographyConnector
from .copernicus_marine_connector import CopernicusMarineConnector
from .modis_connector import MODISConnector
from .palsar_connector import PALSARConnector
from .smos_connector import SMOSConnector
from .smap_connector import SMAPConnector
from .nsidc_connector import NSIDCConnector

__all__ = [
    'SatelliteConnector',
    'SatelliteData',
    'PlanetaryComputerConnector',
    'ICESat2Connector',
    'OpenTopographyConnector',
    'CopernicusMarineConnector',
    'MODISConnector',
    'PALSARConnector',
    'SMOSConnector',
    'SMAPConnector',
    'NSIDCConnector',
]
