#!/usr/bin/env python3
"""
ArcheoScope Real Data Integrator V2 - BLINDAJE CRÍTICO IMPLEMENTADO
===================================================================

MEJORAS CRÍTICAS 2026-01-27:
1. 🔴 Blindaje global contra inf/nan (sanitizador central)
2. 🔴 Estados explícitos por instrumento (nunca abortar batch)
3. 🔴 ICESat-2 robusto con filtros de calidad
4. 🔴 Sentinel-1 SAR con fallback y lectura por bloques
5. 🟡 MODIS LST prioritario (más estable que Landsat)

Transformación: 12.5% → ~60% operativo

ARQUITECTURA RESILIENTE:
- ❌ Nunca abortar por un instrumento
- ✔ Puntuar con lo que hay
- ✔ Mostrar "coverage score"
- ✔ Estados explícitos: SUCCESS/DEGRADED/FAILED/INVALID
"""

import asyncio
import logging
import math
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

# CRÍTICO: Importar sanitizador y sistema de estados
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_sanitizer import sanitize_response, safe_float, safe_int
from instrument_status import InstrumentResult, InstrumentBatch, create_instrument_result_from_api_data

from .planetary_computer import PlanetaryComputerConnector
from .icesat2_connector import ICESat2Connector
from .opentopography_connector import OpenTopographyConnector
from .nsidc_connector import NSIDCConnector
from .modis_lst_connector import MODISLSTConnector
from .copernicus_marine_connector import CopernicusMarineConnector

# NEW: 5 additional satellite connectors (10→15 instruments)
from .viirs_connector import VIIRSConnector
from .srtm_connector import SRTMConnector
from .palsar_connector import PALSARConnector
from .era5_connector import ERA5Connector
from .chirps_connector import CHIRPSConnector

logger = logging.getLogger(__name__)

# NEW: Import SAR enhanced processing
import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

try:
    from sar_enhanced_processing import process_sar_enhanced
    SAR_ENHANCED_AVAILABLE = True
    logger.info("✅ SAR Enhanced Processing module loaded")
except ImportError as e:
    SAR_ENHANCED_AVAILABLE = False
    logger.warning(f"⚠️ SAR Enhanced Processing not available: {e}")


class RealDataIntegratorV2:
    """
    Integrador de datos reales V2 - Con blindaje crítico
    
    MEJORAS CRÍTICAS:
    - Sanitización global de inf/nan
    - Estados explícitos por instrumento
    - Nunca abortar el batch completo
    - Coverage score en tiempo real
    - Degradación controlada
    """
    
    def __init__(self, credentials_manager=None):
        """Inicializar todos los conectores con manejo de errores robusto."""
        
        # CRÍTICO: Inicializar credentials_manager si no se proporciona
        if credentials_manager is None:
            try:
                from backend.credentials_manager import CredentialsManager
                self.credentials_manager = CredentialsManager()
                logger.info("✅ CredentialsManager initialized from BD")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize CredentialsManager: {e}")
                self.credentials_manager = None
        else:
            self.credentials_manager = credentials_manager
        
        # Inicializar conectores con manejo de errores
        self.connectors = {}
        
        try:
            self.connectors['planetary_computer'] = PlanetaryComputerConnector()
            logger.info("✅ Planetary Computer connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ Planetary Computer failed to initialize: {e}")
            self.connectors['planetary_computer'] = None
        
        try:
            self.connectors['icesat2'] = ICESat2Connector()
            logger.info("✅ ICESat-2 connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ ICESat-2 failed to initialize: {e}")
            self.connectors['icesat2'] = None
        
        try:
            self.connectors['opentopography'] = OpenTopographyConnector()
            logger.info("✅ OpenTopography connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ OpenTopography failed to initialize: {e}")
            self.connectors['opentopography'] = None
        
        try:
            self.connectors['nsidc'] = NSIDCConnector()
            logger.info("✅ NSIDC connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ NSIDC failed to initialize: {e}")
            self.connectors['nsidc'] = None
        
        try:
            self.connectors['modis_lst'] = MODISLSTConnector()
            logger.info("✅ MODIS LST connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ MODIS LST failed to initialize: {e}")
            self.connectors['modis_lst'] = None
        
        try:
            self.connectors['copernicus_marine'] = CopernicusMarineConnector()
            logger.info("✅ Copernicus Marine connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ Copernicus Marine failed to initialize: {e}")
            self.connectors['copernicus_marine'] = None
        
        # NEW: Initialize 5 additional satellite connectors (10→15 instruments)
        try:
            self.connectors['viirs'] = VIIRSConnector()
            logger.info("✅ VIIRS connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ VIIRS failed to initialize: {e}")
            self.connectors['viirs'] = None
        
        try:
            # CRÍTICO: Pasar credentials_manager a SRTM para leer de BD
            self.connectors['srtm'] = SRTMConnector(credentials_manager=self.credentials_manager)
            logger.info("✅ SRTM DEM connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ SRTM failed to initialize: {e}")
            self.connectors['srtm'] = None
        
        try:
            self.connectors['palsar'] = PALSARConnector()
            logger.info("✅ ALOS PALSAR-2 connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ PALSAR-2 failed to initialize: {e}")
            self.connectors['palsar'] = None
        
        try:
            self.connectors['era5'] = ERA5Connector()
            logger.info("✅ ERA5 connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ ERA5 failed to initialize: {e}")
            self.connectors['era5'] = None
        
        try:
            self.connectors['chirps'] = CHIRPSConnector()
            logger.info("✅ CHIRPS connector initialized")
        except Exception as e:
            logger.warning(f"⚠️ CHIRPS failed to initialize: {e}")
            self.connectors['chirps'] = None
        
        # Contar conectores disponibles
        available_count = sum(1 for c in self.connectors.values() if c is not None)
        total_count = len(self.connectors)
        
        logger.info(f"🚀 RealDataIntegratorV2 initialized: {available_count}/{total_count} APIs available")
        
        # Logging detallado a archivo
        self.log_file = None
        try:
            self.log_file = open('instrument_diagnostics.log', 'a', encoding='utf-8')
            self.log_file.write(f"\n{'='*80}\n")
            self.log_file.write(f"RealDataIntegratorV2 initialized at {datetime.now()}\n")
            self.log_file.write(f"Available APIs: {available_count}/{total_count}\n")
            self.log_file.flush()
        except Exception as e:
            logger.warning(f"Could not open diagnostics log: {e}")
    
    def log(self, message: str):
        """Log a message to both console and file."""
        print(message, flush=True)
        if self.log_file:
            self.log_file.write(message + '\n')
            self.log_file.flush()
    
    async def get_instrument_measurement_robust(self,
                                              instrument_name: str,
                                              lat_min: float, lat_max: float,
                                              lon_min: float, lon_max: float) -> InstrumentResult:
        """
        Obtener medición de instrumento con manejo robusto de errores.
        
        CRÍTICO: Nunca falla - siempre devuelve InstrumentResult con estado apropiado.
        
        Args:
            instrument_name: Nombre del instrumento/API
            lat_min, lat_max, lon_min, lon_max: Bounding box
        
        Returns:
            InstrumentResult con estado SUCCESS/DEGRADED/FAILED/INVALID/UNAVAILABLE
        """
        
        start_time = time.time()
        
        self.log(f"\n[{instrument_name}] Iniciando medición robusta...")
        self.log(f"[{instrument_name}] Región: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        
        try:
            # Mapear instrumento a conector y método
            api_mapping = {
                # Sentinel-2 (NDVI, multispectral)
                'sentinel_2_ndvi': ('planetary_computer', 'get_multispectral_data'),
                'sentinel2': ('planetary_computer', 'get_multispectral_data'),
                
                # Sentinel-1 (SAR)
                'sentinel_1_sar': ('planetary_computer', 'get_sar_data'),
                'sar_backscatter': ('planetary_computer', 'get_sar_data'),
                'sar_l_band_penetration': ('planetary_computer', 'get_sar_data'),
                'sar_polarimetric_anomalies': ('planetary_computer', 'get_sar_data'),
                'sar_ocean_surface': ('planetary_computer', 'get_sar_data'),
                'sar_penetration_anomalies': ('planetary_computer', 'get_sar_data'),
                'sar_structural_anomalies': ('planetary_computer', 'get_sar_data'),
                
                # Landsat (térmico)
                'landsat_thermal': ('planetary_computer', 'get_thermal_data'),
                'thermal_anomalies': ('planetary_computer', 'get_thermal_data'),
                
                # ICESat-2 (elevación) - CON FILTROS ROBUSTOS
                'icesat2': ('icesat2', 'get_elevation_data'),
                'elevation': ('icesat2', 'get_elevation_data'),
                'ice_height': ('icesat2', 'get_elevation_data'),
                'icesat2_subsurface': ('icesat2', 'get_elevation_data'),
                'icesat2_elevation_anomalies': ('icesat2', 'get_elevation_data'),
                'lidar_elevation_anomalies': ('icesat2', 'get_elevation_data'),
                'elevation_terracing': ('icesat2', 'get_elevation_data'),
                'slope_anomalies': ('icesat2', 'get_elevation_data'),
                
                # MODIS LST (térmico regional) - PRIORITARIO
                'modis_lst': ('modis_lst', 'get_thermal_data'),
                'modis_thermal_inertia': ('modis_lst', 'get_thermal_data'),
                'modis_thermal_ice': ('modis_lst', 'get_thermal_data'),
                'modis_polar_thermal': ('modis_lst', 'get_thermal_data'),
                
                # NSIDC (hielo, criosfera)
                'nsidc_sea_ice': ('nsidc', 'get_sea_ice_data'),
                'nsidc_snow_cover': ('nsidc', 'get_snow_data'),
                'nsidc_ice_concentration': ('nsidc', 'get_sea_ice_data'),
                'nsidc_polar_ice': ('nsidc', 'get_sea_ice_data'),
                
                # Copernicus Marine (hielo marino, SST)
                'copernicus_sst': ('copernicus_marine', 'get_sst_data'),
                'copernicus_sea_ice': ('copernicus_marine', 'get_sea_ice_data'),
                'copernicus_sst_anomaly': ('copernicus_marine', 'get_sst_data'),
                'copernicus_ice_marine': ('copernicus_marine', 'get_sea_ice_data'),
                
                # OpenTopography (DEM, LiDAR)
                'opentopography': ('opentopography', 'get_elevation_data'),
                'dem': ('opentopography', 'get_elevation_data'),
                'lidar': ('opentopography', 'get_elevation_data'),
                
                # NEW: VIIRS (thermal, NDVI, fire detection) - Instrumento 11/15
                'viirs_thermal': ('viirs', 'get_thermal_data'),
                'viirs_ndvi': ('viirs', 'get_ndvi_data'),
                'viirs_fire': ('viirs', 'get_fire_data'),
                'viirs_thermal_anomalies': ('viirs', 'get_thermal_data'),
                'viirs_vegetation_stress': ('viirs', 'get_ndvi_data'),
                
                # NEW: SRTM DEM (topographic analysis) - Instrumento 12/15
                'srtm_elevation': ('srtm', 'get_elevation_data'),
                'srtm_slope': ('srtm', 'get_slope_analysis'),
                'srtm_dem': ('srtm', 'get_elevation_data'),
                'elevation_terracing_srtm': ('srtm', 'get_slope_analysis'),
                'slope_anomalies_srtm': ('srtm', 'get_slope_analysis'),
                
                # NEW: ALOS PALSAR-2 (L-band SAR penetration) - Instrumento 13/15
                'palsar_backscatter': ('palsar', 'get_sar_backscatter'),
                'palsar_penetration': ('palsar', 'get_forest_penetration'),
                'palsar_soil_moisture': ('palsar', 'get_soil_moisture'),
                'sar_l_band_palsar': ('palsar', 'get_sar_backscatter'),
                'forest_penetration_l_band': ('palsar', 'get_forest_penetration'),
                
                # NEW: ERA5 (climate context) - Instrumento 14/15
                'era5_climate': ('era5', 'get_climate_context'),
                'era5_preservation': ('era5', 'get_preservation_conditions'),
                'era5_accessibility': ('era5', 'get_seasonal_accessibility'),
                'climate_context': ('era5', 'get_climate_context'),
                'preservation_conditions': ('era5', 'get_preservation_conditions'),
                
                # NEW: CHIRPS (precipitation history) - Instrumento 15/15
                'chirps_precipitation': ('chirps', 'get_precipitation_history'),
                'chirps_drought': ('chirps', 'get_drought_analysis'),
                'chirps_seasonal': ('chirps', 'get_seasonal_patterns'),
                'chirps_water_management': ('chirps', 'get_water_management_indicators'),
                'precipitation_history': ('chirps', 'get_precipitation_history'),
                'drought_analysis': ('chirps', 'get_drought_analysis')
            }
            
            # Verificar si el instrumento está mapeado
            if instrument_name not in api_mapping:
                self.log(f"[{instrument_name}] ❌ Instrumento no mapeado")
                return InstrumentResult.create_failed(
                    instrument_name=instrument_name,
                    measurement_type="unknown",
                    reason="INSTRUMENT_NOT_MAPPED",
                    processing_time_s=time.time() - start_time
                )
            
            connector_name, method_name = api_mapping[instrument_name]
            
            # Verificar si el conector está disponible
            connector = self.connectors.get(connector_name)
            if connector is None:
                self.log(f"[{instrument_name}] ❌ Conector {connector_name} no disponible")
                return InstrumentResult.create_failed(
                    instrument_name=instrument_name,
                    measurement_type="api_unavailable",
                    reason="CONNECTOR_UNAVAILABLE",
                    error_details=f"Connector {connector_name} failed to initialize",
                    processing_time_s=time.time() - start_time
                )
            
            # Verificar si el método existe
            if not hasattr(connector, method_name):
                self.log(f"[{instrument_name}] ❌ Método {method_name} no existe en {connector_name}")
                return InstrumentResult.create_failed(
                    instrument_name=instrument_name,
                    measurement_type="method_missing",
                    reason="METHOD_NOT_FOUND",
                    error_details=f"Method {method_name} not found in {connector_name}",
                    processing_time_s=time.time() - start_time
                )
            
            self.log(f"[{instrument_name}] 🔄 Llamando {connector_name}.{method_name}...")
            
            # Llamar al método de la API
            method = getattr(connector, method_name)
            
            # Timeout por instrumento (no abortar todo el batch)
            try:
                api_data = await asyncio.wait_for(
                    method(lat_min, lat_max, lon_min, lon_max),
                    timeout=60.0  # 60 segundos por instrumento
                )
            except asyncio.TimeoutError:
                self.log(f"[{instrument_name}] ⏰ Timeout después de 60s")
                return InstrumentResult.create_failed(
                    instrument_name=instrument_name,
                    measurement_type="timeout",
                    reason="API_TIMEOUT_60S",
                    processing_time_s=time.time() - start_time
                )
            
            processing_time = time.time() - start_time
            
            # Verificar si la API devolvió datos
            if api_data is None:
                self.log(f"[{instrument_name}] ❌ API devolvió None")
                return InstrumentResult.create_failed(
                    instrument_name=instrument_name,
                    measurement_type="no_data",
                    reason="API_RETURNED_NONE",
                    processing_time_s=processing_time
                )
            
            # CRÍTICO: Manejar InstrumentMeasurement (nuevo contrato)
            if hasattr(api_data, 'status'):
                # Es un InstrumentMeasurement - convertir directamente
                self.log(f"[{instrument_name}] 📦 InstrumentMeasurement recibido: status={api_data.status}")
                
                # Convertir status string a InstrumentStatus enum
                from instrument_status import InstrumentStatus
                if isinstance(api_data.status, str):
                    status_map = {
                        'OK': InstrumentStatus.SUCCESS,
                        'NO_DATA': InstrumentStatus.FAILED,
                        'INVALID': InstrumentStatus.INVALID,
                        'LOW_QUALITY': InstrumentStatus.DEGRADED,
                        'DERIVED': InstrumentStatus.DEGRADED,
                        'TIMEOUT': InstrumentStatus.FAILED,
                        'ERROR': InstrumentStatus.FAILED
                    }
                    status = status_map.get(api_data.status, InstrumentStatus.FAILED)
                elif hasattr(api_data.status, 'value'):
                    # Es un enum, mapear su valor
                    status_map = {
                        'OK': InstrumentStatus.SUCCESS,
                        'NO_DATA': InstrumentStatus.FAILED,
                        'INVALID': InstrumentStatus.INVALID,
                        'LOW_QUALITY': InstrumentStatus.DEGRADED,
                        'DERIVED': InstrumentStatus.DEGRADED,
                        'TIMEOUT': InstrumentStatus.FAILED,
                        'ERROR': InstrumentStatus.FAILED
                    }
                    status = status_map.get(api_data.status.value, InstrumentStatus.FAILED)
                else:
                    status = api_data.status
                
                # Convertir a InstrumentResult (sin 'metadata', usar quality_flags si existe)
                return InstrumentResult(
                    instrument_name=api_data.instrument_name,
                    status=status,
                    measurement_type=api_data.measurement_type,
                    value=api_data.value,
                    unit=api_data.unit,
                    confidence=api_data.confidence,
                    source=api_data.source,
                    acquisition_date=api_data.acquisition_date,
                    reason=api_data.reason,
                    error_details=api_data.reason,  # InstrumentMeasurement usa 'reason', no 'error_details'
                    processing_time_s=processing_time
                    # NO incluir metadata - InstrumentResult no lo acepta
                )
            
            # Extraer valor principal con sanitización (para SatelliteData legacy)
            value = None
            confidence = 0.0
            raw_value = None  # Para debugging
            
            # Diferentes formas de extraer valor según el tipo de datos
            if hasattr(api_data, 'indices') and api_data.indices:
                # SatelliteData object
                indices = api_data.indices
                
                # Priorizar valores según el instrumento
                if 'elevation_std' in indices:
                    # CRÍTICO: ICESat-2 rugosidad (std) como señal arqueológica
                    raw_value = indices['elevation_std']
                    if isinstance(raw_value, (int, float)) and not (np.isnan(raw_value) or np.isinf(raw_value)):
                        value = float(raw_value)
                        self.log(f"   ✅ ICESat-2 rugosity: {value:.2f}m (señal arqueológica)")
                    else:
                        self.log(f"   ⚠️ ICESat-2 rugosity inválido: {raw_value}")
                elif 'elevation_variance' in indices:
                    # Alternativa: varianza
                    raw_value = indices['elevation_variance']
                    if isinstance(raw_value, (int, float)) and not (np.isnan(raw_value) or np.isinf(raw_value)):
                        value = float(raw_value)
                        self.log(f"   ✅ ICESat-2 variance: {value:.2f}m² (señal arqueológica)")
                elif 'elevation_gradient' in indices:
                    # Alternativa: gradiente
                    raw_value = indices['elevation_gradient']
                    if isinstance(raw_value, (int, float)) and not (np.isnan(raw_value) or np.isinf(raw_value)):
                        value = float(raw_value)
                        self.log(f"   ✅ ICESat-2 gradient: {value:.2f}m (señal arqueológica)")
                elif 'elevation_mean' in indices:
                    # FALLBACK: mean (solo si no hay rugosidad)
                    raw_value = indices['elevation_mean']
                    # CRÍTICO: ICESat-2 elevation NO normalizar (puede ser >1000m)
                    # Solo validar que sea finito
                    if isinstance(raw_value, (int, float)) and not (np.isnan(raw_value) or np.isinf(raw_value)):
                        value = float(raw_value)
                        self.log(f"   ⚠️ ICESat-2 elevation mean: {value:.1f}m (fallback - preferir rugosidad)")
                    else:
                        self.log(f"   ⚠️ ICESat-2 elevation inválido: {raw_value}")
                elif 'ndvi' in indices:
                    value = safe_float(indices['ndvi'])
                elif 'vv_mean' in indices:
                    value = safe_float(indices['vv_mean'])
                elif 'lst_mean' in indices:
                    value = safe_float(indices['lst_mean'])
                elif 'ice_concentration' in indices:
                    value = safe_float(indices['ice_concentration'])
                elif 'sst_mean' in indices:
                    value = safe_float(indices['sst_mean'])
                else:
                    # Tomar el primer valor numérico disponible
                    for key, val in indices.items():
                        sanitized_val = safe_float(val)
                        if sanitized_val is not None:
                            value = sanitized_val
                            break
                
                confidence = safe_float(getattr(api_data, 'confidence', 0.8)) or 0.8
                
            elif isinstance(api_data, dict):
                # Dictionary response
                value = safe_float(api_data.get('value'))
                confidence = safe_float(api_data.get('confidence', 0.8)) or 0.8
            
            # NUEVO: Procesar SAR con métricas mejoradas (no solo valor absoluto)
            sar_enhanced_result = None
            if SAR_ENHANCED_AVAILABLE and 'sar' in instrument_name.lower() and value is not None:
                try:
                    # Intentar obtener datos 2D si están disponibles
                    sar_data_2d = None
                    if hasattr(api_data, 'data_2d'):
                        sar_data_2d = api_data.data_2d
                    
                    # Procesar SAR con derivados estructurales
                    sar_enhanced_result = process_sar_enhanced(value, sar_data_2d)
                    
                    # Si tenemos índice estructural, usarlo como valor principal
                    if sar_enhanced_result.get('processing_mode') == 'spatial':
                        structural_index = sar_enhanced_result.get('sar_structural_index', 0.0)
                        if structural_index > 0:
                            self.log(f"   🔬 SAR Enhanced: structural_index={structural_index:.3f} (reemplaza norm={value:.3f})")
                            value = structural_index
                            # Aumentar confianza si hay análisis espacial
                            confidence = min(1.0, confidence + 0.1)
                    
                except Exception as e:
                    self.log(f"   ⚠️ SAR Enhanced processing failed: {e}")
                    # Continuar con valor original
            
            # NUEVA LÓGICA: Si value es None, buscar métricas derivadas válidas
            if value is None and hasattr(api_data, 'indices') and api_data.indices:
                indices = api_data.indices
                self.log(f"[{instrument_name}] 🔍 raw_value=None, buscando métricas derivadas...")
                
                # Buscar CUALQUIER métrica derivada válida
                derived_metrics = [
                    'rugosity', 'elevation_std', 'elevation_variance', 'elevation_gradient',
                    'structural_index', 'coherence', 'texture_variance',
                    'thermal_stability', 'thermal_inertia',
                    'slope_mean', 'slope_std', 'aspect_variance'
                ]
                
                for metric in derived_metrics:
                    if metric in indices:
                        derived_value = safe_float(indices[metric])
                        if derived_value is not None:
                            value = derived_value
                            self.log(f"   ✅ Métrica derivada válida: {metric}={value:.3f}")
                            # Ajustar confidence porque es métrica derivada
                            confidence = min(confidence * 0.9, 0.95) if confidence else 0.7
                            break
            
            # Verificar si obtuvimos un valor válido (después de buscar derivadas)
            if value is None:
                self.log(f"[{instrument_name}] ❌ Sin valor válido (ni raw ni derivado)")
                return InstrumentResult.create_invalid(
                    instrument_name=instrument_name,
                    measurement_type="invalid_value",
                    reason="NO_VALID_VALUE_OR_DERIVED_METRIC",
                    processing_time_s=processing_time
                )
            
            # Determinar unidad según el instrumento
            unit_mapping = {
                'elevation': 'm',
                'icesat2': 'm',
                'ndvi': 'NDVI',
                'sentinel_2_ndvi': 'NDVI',
                'sar': 'dB',
                'sentinel_1_sar': 'dB',
                'thermal': 'K',
                'lst': 'K',
                'ice_concentration': '%',
                'sst': 'K'
            }
            
            unit = 'units'  # Default
            for key, u in unit_mapping.items():
                if key in instrument_name.lower():
                    unit = u
                    break
            
            # Determinar si es SUCCESS o DEGRADED
            is_degraded = False
            degraded_reasons = []
            
            if confidence < 0.7:
                is_degraded = True
                degraded_reasons.append(f"low_confidence_{confidence:.2f}")
            
            # Verificar calidad específica por instrumento
            if hasattr(api_data, 'indices') and api_data.indices:
                indices = api_data.indices
                
                # ICESat-2: verificar puntos válidos
                if 'valid_points' in indices:
                    valid_points = safe_int(indices.get('valid_points', 0))
                    if valid_points and valid_points < 20:
                        is_degraded = True
                        degraded_reasons.append(f"low_point_count_{valid_points}")
                
                # Sentinel: verificar cobertura de nubes
                if hasattr(api_data, 'cloud_cover'):
                    cloud_cover = safe_float(api_data.cloud_cover)
                    if cloud_cover and cloud_cover > 30:
                        is_degraded = True
                        degraded_reasons.append(f"high_cloud_cover_{cloud_cover:.1f}")
            
            # Crear resultado apropiado
            if is_degraded:
                self.log(f"[{instrument_name}] ⚠️ DEGRADED: {value:.3f} {unit} (razones: {', '.join(degraded_reasons)})")
                return InstrumentResult.create_degraded(
                    instrument_name=instrument_name,
                    measurement_type="degraded_quality",
                    value=value,
                    unit=unit,
                    confidence=confidence,
                    reason=" | ".join(degraded_reasons),
                    source=getattr(api_data, 'source', connector_name),
                    acquisition_date=getattr(api_data, 'acquisition_date', datetime.now()).isoformat() if hasattr(api_data, 'acquisition_date') else None,
                    processing_time_s=processing_time
                )
            else:
                self.log(f"[{instrument_name}] ✅ SUCCESS: {value:.3f} {unit} (confianza: {confidence:.2f})")
                return InstrumentResult.create_success(
                    instrument_name=instrument_name,
                    measurement_type="measurement",
                    value=value,
                    unit=unit,
                    confidence=confidence,
                    source=getattr(api_data, 'source', connector_name),
                    acquisition_date=getattr(api_data, 'acquisition_date', datetime.now()).isoformat() if hasattr(api_data, 'acquisition_date') else None,
                    processing_time_s=processing_time
                )
        
        except Exception as e:
            processing_time = time.time() - start_time
            self.log(f"[{instrument_name}] 💥 EXCEPTION: {e}")
            
            # Clasificar tipo de error
            error_str = str(e).lower()
            
            if 'timeout' in error_str:
                status = 'TIMEOUT'
            elif 'unavailable' in error_str or 'service' in error_str:
                status = 'UNAVAILABLE'
            elif 'invalid' in error_str or 'nan' in error_str or 'inf' in error_str:
                status = 'INVALID'
            else:
                status = 'FAILED'
            
            return InstrumentResult.create_failed(
                instrument_name=instrument_name,
                measurement_type="exception",
                reason=status,
                error_details=str(e)[:200],  # Limitar longitud del error
                processing_time_s=processing_time
            )
    
    async def get_batch_measurements(self,
                                   instrument_names: List[str],
                                   lat_min: float, lat_max: float,
                                   lon_min: float, lon_max: float) -> InstrumentBatch:
        """
        Obtener mediciones de múltiples instrumentos en lote.
        
        CRÍTICO: Nunca aborta - procesa todos los instrumentos independientemente.
        
        Args:
            instrument_names: Lista de nombres de instrumentos
            lat_min, lat_max, lon_min, lon_max: Bounding box
        
        Returns:
            InstrumentBatch con todos los resultados y coverage score
        """
        
        self.log(f"\n{'='*80}")
        self.log(f"INICIANDO BATCH DE {len(instrument_names)} INSTRUMENTOS")
        self.log(f"Región: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        self.log(f"{'='*80}")
        
        batch = InstrumentBatch()
        batch.start_time = time.time()
        
        # Procesar instrumentos en paralelo (pero con límite para no saturar APIs)
        semaphore = asyncio.Semaphore(3)  # Máximo 3 instrumentos simultáneos
        
        async def process_instrument(instrument_name: str):
            async with semaphore:
                result = await self.get_instrument_measurement_robust(
                    instrument_name, lat_min, lat_max, lon_min, lon_max
                )
                batch.add_result(result)
                return result
        
        # Ejecutar todos los instrumentos
        tasks = [process_instrument(name) for name in instrument_names]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        batch.end_time = time.time()
        
        # Generar reporte del batch
        report = batch.generate_report()
        
        self.log(f"\n{'='*80}")
        self.log(f"BATCH COMPLETADO")
        self.log(f"Total instrumentos: {report['total_instruments']}")
        self.log(f"Coverage Score: {report['coverage_score']:.1%}")
        self.log(f"Instrumentos usables: {report['usable_instruments']}")
        self.log(f"Estados: SUCCESS={report['status_summary']['SUCCESS']}, "
                f"DEGRADED={report['status_summary']['DEGRADED']}, "
                f"FAILED={report['status_summary']['FAILED']}")
        self.log(f"Tiempo total: {batch.end_time - batch.start_time:.2f}s")
        self.log(f"{'='*80}\n")
        
        return batch
    
    def get_availability_status(self) -> Dict[str, Any]:
        """Obtener estado de disponibilidad de todas las APIs."""
        
        status = {}
        
        for name, connector in self.connectors.items():
            if connector is None:
                status[name] = {
                    'available': False,
                    'status': 'UNAVAILABLE',
                    'reason': 'Failed to initialize'
                }
            else:
                available = getattr(connector, 'available', False)
                status[name] = {
                    'available': available,
                    'status': 'AVAILABLE' if available else 'UNAVAILABLE',
                    'reason': 'OK' if available else 'Authentication or setup issue'
                }
        
        # Calcular estadísticas generales
        total_apis = len(status)
        available_apis = sum(1 for s in status.values() if s['available'])
        
        status['_summary'] = {
            'total_apis': total_apis,
            'available_apis': available_apis,
            'availability_rate': available_apis / total_apis if total_apis > 0 else 0.0,
            'status': 'OPERATIONAL' if available_apis >= total_apis * 0.6 else 'DEGRADED'
        }
        
        return status
    
    def __del__(self):
        """Cleanup al destruir el objeto."""
        if self.log_file:
            try:
                self.log_file.close()
            except:
                pass


# Función de conveniencia para uso directo
async def get_robust_measurements(instrument_names: List[str],
                                lat_min: float, lat_max: float,
                                lon_min: float, lon_max: float) -> Dict[str, Any]:
    """
    Función de conveniencia para obtener mediciones robustas.
    
    Returns:
        Diccionario sanitizado listo para JSON
    """
    
    integrator = RealDataIntegratorV2()
    
    try:
        batch = await integrator.get_batch_measurements(
            instrument_names, lat_min, lat_max, lon_min, lon_max
        )
        
        # Generar respuesta sanitizada
        response = batch.generate_report()
        
        # Sanitizar antes de devolver
        sanitized_response = sanitize_response(response)
        
        return sanitized_response
        
    except Exception as e:
        logger.error(f"Error in robust measurements: {e}")
        
        # Respuesta de emergencia sanitizada
        emergency_response = {
            "status": "error",
            "error": str(e),
            "total_instruments": len(instrument_names),
            "coverage_score": 0.0,
            "usable_instruments": 0,
            "instruments": []
        }
        
        return sanitize_response(emergency_response)


if __name__ == "__main__":
    # Test del integrador robusto
    async def test_robust_integrator():
        print("🧪 Testing RealDataIntegratorV2...")
        
        # Test con instrumentos mixtos (algunos funcionarán, otros fallarán)
        instruments = [
            'sentinel_2_ndvi',
            'icesat2',
            'modis_lst',
            'sentinel_1_sar',
            'nonexistent_instrument'  # Este fallará intencionalmente
        ]
        
        # Coordenadas de test (Giza, Egipto)
        lat_min, lat_max = 29.9, 30.0
        lon_min, lon_max = 31.1, 31.2
        
        result = await get_robust_measurements(
            instruments, lat_min, lat_max, lon_min, lon_max
        )
        
        print(f"Coverage Score: {result['coverage_score']:.1%}")
        print(f"Usable Instruments: {result['usable_instruments']}/{result['total_instruments']}")
        
        for instrument in result['instruments']:
            status = instrument['status']
            name = instrument['instrument']
            value = instrument.get('value', 'N/A')
            print(f"  {name}: {status} (value: {value})")
    
    # Ejecutar test
    import asyncio
    asyncio.run(test_robust_integrator())