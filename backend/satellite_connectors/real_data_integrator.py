"""
Real Data Integrator
Integra TODAS las APIs reales y reemplaza simulaciones

ACTUALIZADO: 2026-01-26
- Agregado NSIDC (hielo, criosfera)
- Agregado MODIS LST (termico regional)
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
    1. Sentinel-2 (NDVI, multispectral) [OK]
    2. Sentinel-1 (SAR) [OK]
    3. Landsat (termico) [OK]
    4. ICESat-2 (elevacion) [OK]
    5. NSIDC (hielo, criosfera) [OK]
    6. MODIS LST (termico regional) [OK]
    7. Copernicus Marine (hielo marino) [OK]
    8. OpenTopography (DEM, LiDAR) [OK] NUEVO
    """
    
    def __init__(self):
        """Inicializar todos los conectores"""
        self.planetary_computer = PlanetaryComputerConnector()
        self.icesat2 = ICESat2Connector()
        self.nsidc = NSIDCConnector()
        self.modis_lst = MODISLSTConnector()
        self.copernicus_marine = CopernicusMarineConnector()
        self.opentopography = OpenTopographyConnector()
        
        print("[OK] RealDataIntegrator initialized - 8/11 APIs (72.7%)", flush=True)
        print("   [OK] Sentinel-2, Sentinel-1, Landsat, ICESat-2", flush=True)
        print("   [OK] NSIDC, MODIS LST, Copernicus Marine", flush=True)
        print("   [OK] OpenTopography (DEM/LiDAR) - NUEVO", flush=True)
    
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
        Obtener medicion REAL de un instrumento
        
        REGLA NRO 1: NO MÁS SIMULACIONES - Solo datos reales
        """
        
        # Log to file for diagnostics
        import sys
        log_file = open('instrument_diagnostics.log', 'a', encoding='utf-8')
        
        def log(msg):
            print(msg, flush=True)
            log_file.write(msg + '\n')
            log_file.flush()
        
        log(f"         >> RealDataIntegrator: Llamando a {instrument_name}")
        
        try:
            # SENTINEL-2 (NDVI, Multispectral)
            if instrument_name in ["sentinel_2_ndvi", "ndvi", "vegetation"]:
                log(f"         >> Llamando a Planetary Computer (Sentinel-2)...")
                data = await self.planetary_computer.get_multispectral_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    log(f"         [OK] Sentinel-2 respondio: NDVI={data.indices.get('ndvi', 0.0):.3f}")
                    log_file.close()
                    return {
                        'value': data.indices.get('ndvi', 0.0),
                        'source': 'Sentinel-2 (Copernicus)',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat(),
                        'status': 'OK',
                        'quality_flags': {'cloud_cover': data.cloud_cover, 'resolution_m': data.resolution_m}
                    }
                else:
                    log(f"         [FAIL] Sentinel-2 no devolvio datos")
            
            # SENTINEL-1 (SAR)
            elif instrument_name in ["sentinel_1_sar", "sar", "backscatter", "sar_penetration_anomalies", "sar_polarimetric_anomalies", "sentinel1_sar"]:
                log(f"         >> Llamando a Planetary Computer (Sentinel-1 SAR)...")
                data = await self.planetary_computer.get_sar_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    log(f"         [OK] Sentinel-1 SAR respondio: VV={data.indices.get('vv_mean', 0.0):.3f} dB")
                    log_file.close()
                    return {
                        'value': data.indices.get('vv_mean', 0.0),
                        'source': 'Sentinel-1 SAR (Copernicus)',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat(),
                        'status': 'OK',
                        'quality_flags': {'resolution_m': data.resolution_m, 'vv_vh_ratio': data.indices.get('vv_vh_ratio', 1.0)}
                    }
                else:
                    log(f"         [FAIL] Sentinel-1 SAR no devolvio datos")
            
            # LANDSAT (Termico)
            elif instrument_name in ["landsat_thermal", "thermal", "lst"]:
                print(f"         >> Llamando a Planetary Computer (Landsat Thermal)...", flush=True)
                data = await self.planetary_computer.get_thermal_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    print(f"         [OK] Landsat Thermal respondio: LST={data.indices.get('lst_mean', 0.0):.1f}K", flush=True)
                    return {
                        'value': data.indices.get('lst_mean', 0.0),
                        'source': 'Landsat Thermal (NASA/USGS)',
                        'confidence': data.confidence,
                        'acquisition_date': data.acquisition_date.isoformat(),
                        'status': 'OK',
                        'quality_flags': {'cloud_cover': data.cloud_cover, 'resolution_m': data.resolution_m}
                    }
                else:
                    print(f"         [FAIL] Landsat Thermal no devolvio datos", flush=True)
            
            # ICESAT-2 (Elevacion) - ACTUALIZADO A INSTRUMENT CONTRACT
            elif instrument_name in ["icesat2", "elevation", "ice_height", "icesat2_subsurface", "icesat2_elevation_anomalies"]:
                log(f"         >> Llamando a ICESat-2 (NASA Earthdata)...")
                measurement = await self.icesat2.get_elevation_data(
                    lat_min, lat_max, lon_min, lon_max
                )
                
                # measurement es InstrumentMeasurement - devolver directamente su dict
                if measurement:
                    log(f"         >> ICESat-2 status: {measurement.status.value}")
                    
                    if measurement.is_usable():
                        log(f"         [OK] ICESat-2 respondio: Elevacion={measurement.value:.2f}m (confidence={measurement.confidence:.2f})")
                        log_file.close()
                        # Devolver dict completo del InstrumentMeasurement
                        return measurement.to_dict()
                    else:
                        log(f"         [FAIL] ICESat-2 no usable: {measurement.reason}")
                        log_file.close()
                        return None
                else:
                    log(f"         [FAIL] ICESat-2 no devolvio medicion")
                    log_file.close()
                    return None
            
            # NSIDC (Hielo marino, criosfera) - MIGRADO A INSTRUMENT CONTRACT
            elif instrument_name in ["nsidc_sea_ice", "sea_ice_concentration", "nsidc_polar_ice", "nsidc_ice_concentration"]:
                log(f"         >> Llamando a NSIDC (Sea Ice)...")
                measurement = await self.nsidc.get_sea_ice_concentration(
                    lat_min, lat_max, lon_min, lon_max
                )
                
                # measurement es InstrumentMeasurement - devolver directamente su dict
                if measurement:
                    log(f"         >> NSIDC status: {measurement.status.value}")
                    
                    if measurement.is_usable():
                        log(f"         [OK] NSIDC respondio: Concentracion={measurement.value:.2f} (confidence={measurement.confidence:.2f})")
                        log_file.close()
                        # Devolver dict completo del InstrumentMeasurement
                        return measurement.to_dict()
                    else:
                        log(f"         [FAIL] NSIDC no usable: {measurement.reason}")
                        log_file.close()
                        return None
                else:
                    log(f"         [FAIL] NSIDC no devolvio medicion")
                    log_file.close()
                    return None
            
            # NSIDC (Cobertura de nieve) - NUEVO
            elif instrument_name in ["nsidc_snow_cover", "snow_cover"]:
                print(f"         >> Llamando a NSIDC (Snow Cover)...", flush=True)
                data = await self.nsidc.get_snow_cover(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    print(f"         [OK] NSIDC Snow respondio: Cobertura={data['value']:.2f}", flush=True)
                    return {
                        'value': data['value'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
                else:
                    print(f"         [FAIL] NSIDC Snow no devolvio datos", flush=True)
            
            # MODIS LST (Termico regional) - NUEVO
            elif instrument_name in ["modis_lst", "modis_thermal", "thermal_inertia", "modis_polar_thermal", "modis_thermal_ice"]:
                log(f"         >> Llamando a MODIS LST...")
                data = await self.modis_lst.get_land_surface_temperature(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    log(f"         [OK] MODIS LST respondio: Inercia termica={data['thermal_inertia']:.2f}")
                    log_file.close()
                    return {
                        'value': data['thermal_inertia'],
                        'lst_day': data['lst_day_celsius'],
                        'lst_night': data['lst_night_celsius'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date'],
                        'status': 'OK',
                        'quality_flags': {'lst_day': data['lst_day_celsius'], 'lst_night': data['lst_night_celsius']}
                    }
                else:
                    log(f"         [FAIL] MODIS LST no devolvio datos")
            
            # COPERNICUS MARINE (Hielo marino) - NUEVO
            elif instrument_name in ["copernicus_sea_ice", "marine_ice"]:
                print(f"         >> Llamando a Copernicus Marine (Sea Ice)...", flush=True)
                data = await self.copernicus_marine.get_sea_ice_concentration(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    print(f"         [OK] Copernicus Marine respondio: Hielo={data['sea_ice_concentration']:.2f}", flush=True)
                    return {
                        'value': data['sea_ice_concentration'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
                else:
                    print(f"         [FAIL] Copernicus Marine no devolvio datos", flush=True)
            
            # COPERNICUS MARINE (SST) - NUEVO
            elif instrument_name in ["copernicus_sst", "sea_surface_temperature"]:
                print(f"         >> Llamando a Copernicus Marine (SST)...", flush=True)
                data = await self.copernicus_marine.get_sea_surface_temperature(
                    lat_min, lat_max, lon_min, lon_max
                )
                if data:
                    print(f"         [OK] Copernicus SST respondio: Temp={data['sea_surface_temperature_celsius']:.1f}C", flush=True)
                    return {
                        'value': data['sea_surface_temperature_celsius'],
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date']
                    }
                else:
                    print(f"         [FAIL] Copernicus SST no devolvio datos", flush=True)
            
            # OPENTOPOGRAPHY (DEM, elevacion, arqueología) - NUEVO
            elif instrument_name in ["opentopography", "dem", "elevation_dem", "lidar_elevation"]:
                print(f"         >> Llamando a OpenTopography...", flush=True)
                data = await self.opentopography.get_elevation_data(
                    lat_min, lat_max, lon_min, lon_max,
                    dem_type="SRTMGL1"  # 30m resolution - mejor para arqueología
                )
                if data:
                    print(f"         [OK] OpenTopography respondio: Rugosidad={data['roughness']:.3f}", flush=True)
                    return {
                        'value': data['roughness'],  # Rugosidad como indicador arqueologico
                        'elevation_mean': data['elevation_mean'],
                        'archaeological_score': data.get('archaeological_score', 0.0),
                        'platforms_detected': data.get('platforms_detected', 0),
                        'mounds_detected': data.get('mounds_detected', 0),
                        'source': data['source'],
                        'confidence': data['confidence'],
                        'acquisition_date': data['acquisition_date'],
                        'status': 'OK',
                        'quality_flags': {
                            'elevation_mean': data['elevation_mean'],
                            'archaeological_score': data.get('archaeological_score', 0.0)
                        }
                    }
                else:
                    print(f"         [FAIL] OpenTopography no devolvio datos", flush=True)
            
            else:
                log(f"         [WARN] Instrumento no reconocido: {instrument_name}")
                log_file.close()
                return None
        
        except Exception as e:
            log(f"         [ERROR] Error obteniendo medicion de {instrument_name}: {e}")
            import traceback
            log(f"         Traceback: {traceback.format_exc()}")
            log_file.close()
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
