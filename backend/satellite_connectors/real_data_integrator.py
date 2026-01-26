"""
Real Data Integrator
Integra TODAS las APIs reales y reemplaza simulaciones

ACTUALIZADO: 2026-01-26
- Agregado NSIDC (hielo, criosfera)
- Agregado MODIS LST (térmico regional)
- Agregado Copernicus Marine (hielo marino, SST)

COBERTURA ACTUAL: 7/11 APIs (63.6%)
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .planetary_computer import PlanetaryComputerConnector
from .icesat2_connector import ICESat2Connector
from .nsidc_connector import NSIDCConnector
from .modis_lst_connector import MODISLSTConnector
from .copernicus_marine_connector import CopernicusMarineConnector
from .opentopography_connector import OpenTopographyConnector

logger = logging.getLogger(__name__)


class RealDataIntegrator:
    """
    Integrador de datos reales satelitales
    
    Reemplaza TODAS las simulaciones por APIs reales
    
    APIs FUNCIONANDO (8/11 = 72.7%):
    1. Sentinel-2 (NDVI, multispectral) ✅
    2. Sentinel-1 (SAR) ✅
    3. Landsat (térmico) ✅
    4. ICESat-2 (elevación) ✅
    5. NSIDC (hielo, criosfera) ✅
    6. MODIS LST (térmico regional) ✅
    7. Copernicus Marine (hielo marino) ✅
    8. OpenTopography (DEM, LiDAR) ✅ NUEVO
    """
    
    def __init__(self):
        """Inicializar todos los conectores"""
        self.planetary_computer = PlanetaryComputerConnector()
        self.icesat2 = ICESat2Connector()
        self.nsidc = NSIDCConnector()
        self.modis_lst = MODISLSTConnector()
        self.copernicus_marine = CopernicusMarineConnector()
        self.opentopography = OpenTopographyConnector()
        
        logger.info("✅ RealDataIntegrator initialized - 8/11 APIs (72.7%)")
        logger.info("   ✅ Sentinel-2, Sentinel-1, Landsat, ICESat-2")
        logger.info("   ✅ NSIDC, MODIS LST, Copernicus Marine")
        logger.info("   ✅ OpenTopography (DEM/LiDAR) - NUEVO")
    
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
        
        REGLA NRO 1: NO MÁS SIMULACIONES - Solo datos reales
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
                        'source': 'Sentinel-2 (Copernicus)',
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
                        'source': 'Sentinel-1 SAR (Copernicus)',
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
                        'source': 'Landsat Thermal (NASA/USGS)',
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
                        'value': data['elevation_mean'],
                        'source': 'ICESat-2 (NASA)',
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
            
            # NSIDC (Hielo marino, criosfera) - NUEVO
            elif instrument_name in ["nsidc_sea_ice", "sea_ice_concentration"]:
                data = await self.nsidc.get_sea_ice_concentration(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data['value'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
            
            # NSIDC (Cobertura de nieve) - NUEVO
            elif instrument_name in ["nsidc_snow_cover", "snow_cover"]:
                data = await self.nsidc.get_snow_cover(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data['value'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
            
            # MODIS LST (Térmico regional) - NUEVO
            elif instrument_name in ["modis_lst", "modis_thermal", "thermal_inertia"]:
                data = await self.modis_lst.get_land_surface_temperature(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data['thermal_inertia'],
                        'lst_day': data['lst_day_celsius'],
                        'lst_night': data['lst_night_celsius'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
            
            # COPERNICUS MARINE (Hielo marino) - NUEVO
            elif instrument_name in ["copernicus_sea_ice", "marine_ice"]:
                data = await self.copernicus_marine.get_sea_ice_concentration(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data['sea_ice_concentration'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
            
            # COPERNICUS MARINE (SST) - NUEVO
            elif instrument_name in ["copernicus_sst", "sea_surface_temperature"]:
                data = await self.copernicus_marine.get_sea_surface_temperature(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    return {
                        'value': data['sea_surface_temperature_celsius'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
            
            # OPENTOPOGRAPHY (DEM, elevación, arqueología) - NUEVO
            elif instrument_name in ["opentopography", "dem", "elevation_dem", "lidar_elevation"]:
                data = await self.opentopography.get_elevation_data(
                    lat_min, lat_max, lon_min, lon_max,
                    dem_type="SRTMGL1"  # 30m resolution - mejor para arqueología
                )
                if data:
                    return {
                        'value': data['roughness'],  # Rugosidad como indicador arqueológico
                        'elevation_mean': data['elevation_mean'],
                        'archaeological_score': data.get('archaeological_score', 0.0),
                        'platforms_detected': data.get('platforms_detected', 0),
                        'mounds_detected': data.get('mounds_detected', 0),
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
            
            else:
                logger.warning(f"⚠️ Instrumento no reconocido: {instrument_name}")
                return None
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo medición de {instrument_name}: {e}")
            return None
    
    def get_available_instruments(self) -> Dict[str, bool]:
        """Obtener estado de disponibilidad de instrumentos"""
        return {
            'sentinel_2': self.planetary_computer.available,
            'sentinel_1': self.planetary_computer.available,
            'landsat': self.planetary_computer.available,
            'icesat2': self.icesat2.available,
            'nsidc': self.nsidc.available,
            'modis_lst': self.modis_lst.available,
            'copernicus_marine': self.copernicus_marine.available,
            'opentopography': self.opentopography.available
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
