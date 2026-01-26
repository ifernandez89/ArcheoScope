"""
Planetary Computer Connector
Microsoft Planetary Computer - Acceso gratuito a Sentinel-2, Sentinel-1, Landsat
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import numpy as np
import os
from pathlib import Path

# FIX CRÍTICO: Configurar PROJ_LIB ANTES de importar rasterio
# PostgreSQL conflictúa con rasterio - forzar uso de PROJ de rasterio
def _configure_proj():
    """Configurar PROJ para evitar conflicto con PostgreSQL"""
    try:
        import rasterio
        proj_path = Path(rasterio.__file__).parent / 'proj_data'
        if proj_path.exists():
            os.environ['PROJ_LIB'] = str(proj_path)
            os.environ['PROJ_DATA'] = str(proj_path)
            print(f"PROJ configurado: {proj_path}")
            return True
    except Exception as e:
        print(f"No se pudo configurar PROJ: {e}")
    return False

# Configurar PROJ antes de cualquier import de rasterio
_configure_proj()

try:
    import pystac_client
    import planetary_computer
    import rasterio
    from rasterio.warp import transform_bounds
    # import stackstac  # DESHABILITADO - requiere pyproj que tiene problemas de DLL
    PLANETARY_COMPUTER_AVAILABLE = True
    STACKSTAC_AVAILABLE = False  # Deshabilitado temporalmente
except ImportError as e:
    PLANETARY_COMPUTER_AVAILABLE = False
    STACKSTAC_AVAILABLE = False
    logger.warning(f"Import error: {e}")

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class PlanetaryComputerConnector(SatelliteConnector):
    """
    Conector a Microsoft Planetary Computer
    
    Acceso gratuito a:
    - Sentinel-2 (multispectral, 10m)
    - Sentinel-1 (SAR, 10m)
    - Landsat-8/9 (térmico, 30m)
    
    Docs: https://planetarycomputer.microsoft.com/
    """
    
    STAC_API_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "PlanetaryComputer"
        
        if not PLANETARY_COMPUTER_AVAILABLE:
            logger.warning(
                "Planetary Computer libraries not available. "
                "Install with: pip install pystac-client planetary-computer stackstac rasterio"
            )
            self.available = False
        else:
            self.available = True
            self.catalog = pystac_client.Client.open(
                self.STAC_API_URL,
                modifier=planetary_computer.sign_inplace
            )
            logger.info("✅ Planetary Computer connector initialized")
    
    async def get_multispectral_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        max_cloud_cover: float = 20.0
    ) -> Optional[SatelliteData]:
        """
        Obtener datos Sentinel-2 (multispectral)
        
        Bandas: Blue, Green, Red, NIR, SWIR
        Resolución: 10m
        """
        if not self.available:
            logger.error("Planetary Computer not available")
            return None
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Fechas por defecto: últimos 30 días
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                start_date = end_date - timedelta(days=30)
            
            # Buscar escenas Sentinel-2
            bbox = [lon_min, lat_min, lon_max, lat_max]
            
            logger.info(f"🛰️ Buscando Sentinel-2 en bbox {bbox}")
            
            search = self.catalog.search(
                collections=["sentinel-2-l2a"],
                bbox=bbox,
                datetime=f"{start_date.isoformat()}/{end_date.isoformat()}",
                query={
                    "eo:cloud_cover": {"lt": max_cloud_cover}
                },
                limit=5
            )
            
            items = list(search.items())
            
            if not items:
                logger.warning(f"No Sentinel-2 scenes found for bbox {bbox}")
                return None
            
            logger.info(f"✅ Found {len(items)} Sentinel-2 scenes")
            
            # Usar la escena más reciente con menor cobertura de nubes
            best_item = min(items, key=lambda x: x.properties.get('eo:cloud_cover', 100))
            
            cloud_cover = best_item.properties.get('eo:cloud_cover', 0)
            acquisition_date = datetime.fromisoformat(
                best_item.properties['datetime'].replace('Z', '+00:00')
            )
            
            logger.info(f"📅 Using scene from {acquisition_date}, cloud cover: {cloud_cover}%")
            
            # Cargar bandas necesarias
            bands_to_load = ['B02', 'B03', 'B04', 'B08', 'B11']  # Blue, Green, Red, NIR, SWIR
            
            # Usar stackstac para cargar datos
            stack = stackstac.stack(
                [best_item],
                assets=bands_to_load,
                bounds_latlon=bbox,
                epsg=4326,  # WGS84
                resolution=10  # 10m resolution
            )
            
            # Computar (esto descarga los datos)
            data = stack.compute()
            
            # Extraer bandas
            bands = {}
            for i, band_name in enumerate(bands_to_load):
                band_data = data[0, i, :, :].values
                bands[band_name] = band_data
            
            # Calcular índices
            blue = bands['B02']
            green = bands['B03']
            red = bands['B04']
            nir = bands['B08']
            swir = bands['B11']
            
            ndvi = self.calculate_ndvi(red, nir)
            ndwi = self.calculate_ndwi(green, nir)
            ndbi = self.calculate_ndbi(swir, nir)
            
            # Calcular valores promedio
            indices = {
                'ndvi': float(np.nanmean(ndvi)),
                'ndwi': float(np.nanmean(ndwi)),
                'ndbi': float(np.nanmean(ndbi)),
                'red_mean': float(np.nanmean(red)),
                'nir_mean': float(np.nanmean(nir)),
                'swir_mean': float(np.nanmean(swir))
            }
            
            # Detectar anomalías en NDVI
            anomaly_score, confidence = self.detect_anomaly(ndvi)
            
            # Determinar tipo de anomalía
            if indices['ndvi'] < 0.2:
                anomaly_type = 'low_vegetation'
            elif indices['ndvi'] > 0.7:
                anomaly_type = 'high_vegetation'
            elif indices['ndbi'] > 0.1:
                anomaly_type = 'built_up_area'
            else:
                anomaly_type = 'vegetation_stress'
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            logger.info(f"✅ Sentinel-2 processed in {processing_time:.2f}s")
            
            return SatelliteData(
                source='sentinel-2-l2a',
                acquisition_date=acquisition_date,
                cloud_cover=cloud_cover,
                resolution_m=10.0,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                bands=bands,
                indices=indices,
                anomaly_score=anomaly_score,
                anomaly_type=anomaly_type,
                confidence=confidence,
                processing_time_s=processing_time,
                cached=False
            )
            
        except Exception as e:
            logger.error(f"Error fetching Sentinel-2 data: {e}", exc_info=True)
            return None
    
    async def get_sar_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[SatelliteData]:
        """
        Obtener datos Sentinel-1 (SAR)
        
        Bandas: VV, VH polarization
        Resolución: 10m
        
        MODOS AUTOMÁTICOS:
        - IW (Interferometric Wide): latitudes <75° (250km swath)
        - EW (Extra Wide): latitudes ≥75° (400km swath, diseñado para polos)
        
        MEJORAS 2026-01-26:
        - Ventana temporal ampliada: 30 → 90 días
        - Fallback a colección sentinel-1-grd
        - Logging detallado a archivo
        """
        if not self.available:
            logger.error("Planetary Computer not available")
            return None
        
        start_time = asyncio.get_event_loop().time()
        
        # Logging a archivo para diagnóstico
        log_file = None
        try:
            log_file = open('instrument_diagnostics.log', 'a', encoding='utf-8')
            
            def log(msg):
                print(msg, flush=True)
                if log_file:
                    log_file.write(msg + '\n')
                    log_file.flush()
            
            # Fechas por defecto: últimos 90 días (AMPLIADO desde 30)
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                start_date = end_date - timedelta(days=90)  # MEJORA: 90 días para mejor cobertura
            
            bbox = [lon_min, lat_min, lon_max, lat_max]
            
            # DETECCIÓN AUTOMÁTICA DE MODO SEGÚN LATITUD
            avg_lat = (lat_min + lat_max) / 2
            is_polar = abs(avg_lat) >= 75
            
            if is_polar:
                instrument_mode = "EW"  # Extra Wide para regiones polares
                log(f"[SAR] Region polar detectada ({avg_lat:.1f}) - usando modo EW")
            else:
                instrument_mode = "IW"  # Interferometric Wide para resto
                log(f"[SAR] Region no-polar ({avg_lat:.1f}) - usando modo IW")
            
            log(f"[SAR] Buscando Sentinel-1 en bbox {bbox}")
            log(f"[SAR] Ventana temporal: {start_date.date()} a {end_date.date()} (90 dias)")
            
            # INTENTO 1: sentinel-1-rtc con modo apropiado
            log(f"[SAR] Intento 1: sentinel-1-rtc modo {instrument_mode}")
            search = self.catalog.search(
                collections=["sentinel-1-rtc"],
                bbox=bbox,
                datetime=f"{start_date.isoformat()}/{end_date.isoformat()}",
                query={
                    "sar:instrument_mode": {"eq": instrument_mode}
                },
                limit=5
            )
            
            items = list(search.items())
            log(f"[SAR] Resultado: {len(items)} escenas encontradas")
            
            if not items:
                # FALLBACK 1: intentar con el otro modo
                fallback_mode = "IW" if instrument_mode == "EW" else "EW"
                log(f"[SAR] Intento 2: sentinel-1-rtc modo {fallback_mode}")
                
                search = self.catalog.search(
                    collections=["sentinel-1-rtc"],
                    bbox=bbox,
                    datetime=f"{start_date.isoformat()}/{end_date.isoformat()}",
                    query={
                        "sar:instrument_mode": {"eq": fallback_mode}
                    },
                    limit=5
                )
                
                items = list(search.items())
                log(f"[SAR] Resultado: {len(items)} escenas encontradas")
                
                if not items:
                    # FALLBACK 2: intentar colección sentinel-1-grd (Ground Range Detected)
                    log(f"[SAR] Intento 3: sentinel-1-grd (sin filtro de modo)")
                    
                    search = self.catalog.search(
                        collections=["sentinel-1-grd"],
                        bbox=bbox,
                        datetime=f"{start_date.isoformat()}/{end_date.isoformat()}",
                        limit=5
                    )
                    
                    items = list(search.items())
                    log(f"[SAR] Resultado: {len(items)} escenas encontradas")
                    
                    if not items:
                        log(f"[SAR] FALLO TOTAL: No se encontraron imagenes SAR")
                        log(f"[SAR] Intentos: rtc-{instrument_mode}, rtc-{fallback_mode}, grd")
                        log(f"[SAR] Conclusion: Planetary Computer no tiene cobertura en esta region")
                        if log_file:
                            log_file.close()
                        return None
                    else:
                        log(f"[SAR] EXITO con sentinel-1-grd")
                else:
                    log(f"[SAR] EXITO con sentinel-1-rtc modo {fallback_mode}")
            else:
                log(f"[SAR] EXITO con sentinel-1-rtc modo {instrument_mode}")
            
            log(f"[SAR] Total escenas encontradas: {len(items)}")
            
            # Usar la escena más reciente
            best_item = items[0]
            
            acquisition_date = datetime.fromisoformat(
                best_item.properties['datetime'].replace('Z', '+00:00')
            )
            
            log(f"[SAR] Usando escena de {acquisition_date.date()}")
            
            # Cargar bandas VV y VH usando rasterio (sin stackstac)
            log(f"[SAR] Cargando bandas VV y VH con rasterio...")
            
            try:
                # Obtener URLs firmadas de los assets
                vh_asset = best_item.assets.get('vh')
                vv_asset = best_item.assets.get('vv')
                
                if not vh_asset or not vv_asset:
                    log(f"[SAR] ERROR: Assets VH o VV no encontrados")
                    if log_file:
                        log_file.close()
                    return None
                
                # Firmar URLs con Planetary Computer
                vh_url = planetary_computer.sign(vh_asset.href)
                vv_url = planetary_computer.sign(vv_asset.href)
                
                log(f"[SAR] URLs firmadas obtenidas")
                
                # Leer bandas con rasterio (leer todo el raster, luego recortar)
                with rasterio.open(vh_url) as src:
                    # Transformar bbox a coordenadas del raster
                    from rasterio.warp import transform_bounds
                    
                    # Leer toda la banda (los COGs de Planetary Computer son optimizados)
                    vh = src.read(1)
                    log(f"[SAR] Banda VH cargada: {vh.shape}")
                
                with rasterio.open(vv_url) as src:
                    vv = src.read(1)
                    log(f"[SAR] Banda VV cargada: {vv.shape}")
                
                # Verificar que no estén vacías
                if vh.size == 0 or vv.size == 0:
                    log(f"[SAR] ERROR: Bandas vacías (VH: {vh.shape}, VV: {vv.shape})")
                    if log_file:
                        log_file.close()
                    return None
                
                log(f"[SAR] Bandas cargadas correctamente")
                
            except Exception as e:
                log(f"[SAR] ERROR cargando bandas: {e}")
                import traceback
                log(f"[SAR] Traceback: {traceback.format_exc()}")
                if log_file:
                    log_file.close()
                return None
            
            bands = {
                'vh': vh,
                'vv': vv
            }
            
            # Calcular ratio VV/VH (indicador de rugosidad/compactación)
            with np.errstate(divide='ignore', invalid='ignore'):
                vv_vh_ratio = vv / vh
                vv_vh_ratio = np.nan_to_num(vv_vh_ratio, nan=1.0)
            
            indices = {
                'vv_mean': float(np.nanmean(vv)),
                'vh_mean': float(np.nanmean(vh)),
                'vv_vh_ratio': float(np.nanmean(vv_vh_ratio)),
                'backscatter_std': float(np.nanstd(vv))
            }
            
            log(f"[SAR] Indices calculados: VV={indices['vv_mean']:.2f} dB")
            
            # Detectar anomalías en backscatter
            anomaly_score, confidence = self.detect_anomaly(vv)
            
            # Tipo de anomalía basado en backscatter
            if indices['vv_mean'] > -5:
                anomaly_type = 'high_backscatter_compaction'
            elif indices['vv_mean'] < -15:
                anomaly_type = 'low_backscatter_water'
            else:
                anomaly_type = 'moderate_backscatter'
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            log(f"[SAR] Procesamiento completado en {processing_time:.2f}s")
            log(f"[SAR] EXITO TOTAL - Datos SAR obtenidos correctamente")
            
            if log_file:
                log_file.close()
            
            logger.info(f"✅ Sentinel-1 processed in {processing_time:.2f}s")
            
            return SatelliteData(
                source='sentinel-1-rtc',
                acquisition_date=acquisition_date,
                cloud_cover=0.0,  # SAR no afectado por nubes
                resolution_m=10.0,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                bands=bands,
                indices=indices,
                anomaly_score=anomaly_score,
                anomaly_type=anomaly_type,
                confidence=confidence,
                processing_time_s=processing_time,
                cached=False
            )
            
        except Exception as e:
            if log_file:
                log_file.write(f"[SAR] ERROR: {e}\n")
                log_file.close()
            logger.error(f"Error fetching Sentinel-1 data: {e}", exc_info=True)
            return None
    
    async def get_thermal_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Optional[SatelliteData]:
        """
        Obtener datos térmicos Landsat-8/9
        
        Banda: Thermal Infrared (TIRS)
        Resolución: 30m
        """
        if not self.available:
            logger.error("Planetary Computer not available")
            return None
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Fechas por defecto: últimos 30 días
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                start_date = end_date - timedelta(days=30)
            
            bbox = [lon_min, lat_min, lon_max, lat_max]
            
            logger.info(f"🛰️ Buscando Landsat-9 en bbox {bbox}")
            
            search = self.catalog.search(
                collections=["landsat-c2-l2"],
                bbox=bbox,
                datetime=f"{start_date.isoformat()}/{end_date.isoformat()}",
                query={
                    "eo:cloud_cover": {"lt": 30}
                },
                limit=5
            )
            
            items = list(search.items())
            
            if not items:
                logger.warning(f"No Landsat scenes found for bbox {bbox}")
                return None
            
            logger.info(f"✅ Found {len(items)} Landsat scenes")
            
            # Usar la escena más reciente
            best_item = min(items, key=lambda x: x.properties.get('eo:cloud_cover', 100))
            
            cloud_cover = best_item.properties.get('eo:cloud_cover', 0)
            acquisition_date = datetime.fromisoformat(
                best_item.properties['datetime'].replace('Z', '+00:00')
            )
            
            logger.info(f"📅 Using Landsat scene from {acquisition_date}")
            
            # Cargar banda térmica (ST_B10)
            stack = stackstac.stack(
                [best_item],
                assets=['lwir11'],  # Thermal band
                bounds_latlon=bbox,
                epsg=4326,  # WGS84
                resolution=30
            )
            
            data = stack.compute()
            
            # Extraer banda térmica
            thermal = data[0, 0, :, :].values
            
            # Convertir a temperatura Celsius (Landsat viene en Kelvin * 0.00341802 + 149.0)
            thermal_celsius = thermal * 0.00341802 + 149.0 - 273.15
            
            bands = {
                'thermal': thermal_celsius
            }
            
            indices = {
                'lst_mean': float(np.nanmean(thermal_celsius)),
                'lst_std': float(np.nanstd(thermal_celsius)),
                'lst_min': float(np.nanmin(thermal_celsius)),
                'lst_max': float(np.nanmax(thermal_celsius))
            }
            
            # Detectar anomalías térmicas
            anomaly_score, confidence = self.detect_anomaly(thermal_celsius)
            
            # Tipo de anomalía basado en temperatura
            if indices['lst_mean'] > 35:
                anomaly_type = 'high_thermal_inertia'
            elif indices['lst_mean'] < 15:
                anomaly_type = 'low_thermal_inertia'
            else:
                anomaly_type = 'moderate_thermal'
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            logger.info(f"✅ Landsat thermal processed in {processing_time:.2f}s")
            
            return SatelliteData(
                source='landsat-c2-l2',
                acquisition_date=acquisition_date,
                cloud_cover=cloud_cover,
                resolution_m=30.0,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                bands=bands,
                indices=indices,
                anomaly_score=anomaly_score,
                anomaly_type=anomaly_type,
                confidence=confidence,
                processing_time_s=processing_time,
                cached=False
            )
            
        except Exception as e:
            logger.error(f"Error fetching Landsat thermal data: {e}", exc_info=True)
            return None
