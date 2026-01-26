"""
ArcheoScope - Satellite Data Connectors
Conectores a APIs satelitales reales para datos multi-instrumentales
"""

from .planetary_computer import PlanetaryComputerConnector
from .base_connector import SatelliteConnector, SatelliteData

__all__ = [
    'PlanetaryComputerConnector',
    'SatelliteConnector',
    'SatelliteData'
]
