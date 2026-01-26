"""
Real Data Integrator
Integra TODAS las APIs reales y reemplaza simulaciones
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .planetary_computer import PlanetaryComputerConnector
from .icesat2_connector import ICESat2Connector
from .opentopography_connector import OpenTopographyConnector
from .copernicus_marine_connector import CopernicusMarineConnector
from .modis_connector import MODISConnector
from .palsar_connector import PALSARConnector
from .smos_connector import SMOSConnector
from .smap_connector import SMAPConnector
from .nsidc_connector import NSIDCConnector

logger = logging.getLogger(__name__)


class RealDataIntegrator:
    """
    Integrador de datos reales satelitales
    
    Reemplaza TODAS las simulaciones por APIs reales gratuitas
    """
    
    def __init__(self):
        """Inicializar todos los conectores"""
        self.planetary_computer = PlanetaryComputerConnector()
        self.icesat2 = ICESat2Connector()
        self.opentopography = OpenTopographyConnector()
        self.copernicus_marine = CopernicusMarineConnector()
        self.modis = MODISConnector()
        self.palsar = PALSARConnector()
        self.smos = SMOSConnector()
        self.smap = SMAPConnector()
        self.nsidc = NSIDCConnector()
        
        logger.info("✅ RealDataIntegrator initialized with all connectors")
    
    async def get_instrument_measurement(
        self,
        instrument_name: str,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Obtener medición REAL de un instrumento
        
        NO MÁS SIMULACIONES - Solo datos reales
        """
        
        try:
            # SENTINEL-2 (NDVI, Multispectral)
            if instrument_name in ["sentinel_2_ndvi", "ndvi", "vegetation"]:
                data = await self.planetary_computer.get_multispectral_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('ndvi', 0.0),
                        'source': 'sentinel-2-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # SENTINEL-1 (SAR)
            elif instrument_name in ["sentinel_1_sar", "sar", "backscatter"]:
                data = await self.planetary_computer.get_sar_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('vv_mean', 0.0),
                        'source': 'sentinel-1-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # LANDSAT (Térmico)
            elif instrument_name in ["landsat_thermal", "thermal", "lst"]:
                data = await self.planetary_computer.get_thermal_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('lst_mean', 0.0),
                        'source': 'landsat-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # ICESAT-2 (Elevación)
            elif instrument_name in ["icesat2", "elevation", "ice_height"]:
                data = await self.icesat2.get_elevation_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('elevation_mean', 0.0),
                        'source': 'icesat2-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # OPENTOPOGRAPHY (DEM)
            elif instrument_name in ["opentopography", "dem", "srtm"]:
                data = await self.opentopography.get_dem_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('elevation_mean', 0.0),
                        'source': 'opentopography-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # COPERNICUS MARINE (Hielo marino)
            elif instrument_name in ["copernicus_marine", "sea_ice", "ice_concentration"]:
                data = await self.copernicus_marine.get_sea_ice_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('ice_concentration_mean', 0.0),
                        'source': 'copernicus-marine-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # MODIS (Térmico regional)
            elif instrument_name in ["modis", "modis_thermal"]:
                data = await self.modis.get_lst_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('lst_mean', 0.0),
                        'source': 'modis-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # PALSAR (L-band)
            elif instrument_name in ["palsar", "lband"]:
                data = await self.palsar.get_lband_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('backscatter_mean', 0.0),
                        'source': 'palsar-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # SMOS (Salinidad)
            elif instrument_name in ["smos", "salinity"]:
                data = await self.smos.get_soil_moisture(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('soil_moisture', 0.0),
                        'source': 'smos-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            # SMAP (Humedad)
            elif instrument_name in ["smap", "soil_moisture"]:
                data = await self.smap.get_soil_moisture(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data.indices.get('soil_moisture', 0.0),
                        'source': 'smap-real',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat()
                    }
            
            else:
                logger.warning(f"Unknown instrument: {instrument_name}")
                return None
        
        except Exception as e:
            logger.error(f"Error getting real data for {instrument_name}: {e}")
            return None
    
    def get_available_instruments(self) -> Dict[str, bool]:
        """Obtener estado de disponibilidad de instrumentos"""
        return {
            'sentinel_2': self.planetary_computer.available,
            'sentinel_1': self.planetary_computer.available,
            'landsat': self.planetary_computer.available,
            'icesat2': self.icesat2.available,
            'opentopography': self.opentopography.available,
            'copernicus_marine': self.copernicus_marine.available,
            'modis': self.modis.available,
            'palsar': self.palsar.available,
            'smos': self.smos.available,
            'smap': self.smap.available,
            'nsidc': self.nsidc.available
        }
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generar reporte de estado de APIs reales"""
        available = self.get_available_instruments()
        
        total = len(available)
        active = sum(1 for v in available.values() if v)
        
        return {
            'total_instruments': total,
            'active_instruments': active,
            'coverage_percent': (active / total * 100) if total > 0 else 0,
            'instruments': available,
            'all_real_data': active == total,
            'no_simulations': active > 0
        }
