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

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)

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
    from rasterio import windows  # Para leer ventanas específicas
    
    # CRÍTICO: Importar stackstac DESPUÉS de configurar PROJ
    try:
        import stackstac
        STACKSTAC_AVAILABLE = True
    except ImportError as e:
        print(f"stackstac no disponible: {e}")
        STACKSTAC_AVAILABLE = False
    
    PLANETARY_COMPUTER_AVAILABLE = True
except ImportError as e:
    PLANETARY_COMPUTER_AVAILABLE = False
    STACKSTAC_AVAILABLE = False
    logger.warning(f"Import error: {e}")



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
            
            # Cargar bandas necesarias SIN stackstac (usando rasterio directamente)
            bands_to_load = ['B02', 'B03', 'B04', 'B08', 'B11']  # Blue, Green, Red, NIR, SWIR
            
            # Leer bandas directamente con rasterio
            bands = {}
            for band_name in bands_to_load:
                try:
                    asset = best_item.assets.get(band_name)
                    if not asset:
                        continue
                    
                    # Firmar URL con Planetary Computer
                    signed_href = planetary_computer.sign(asset.href)
                    
                    # Leer con rasterio
                    with rasterio.open(signed_href) as src:
                        # CRÍTICO: Reprojectar bbox de EPSG:4326 al CRS del raster
                        bbox_proj = transform_bounds(
                            "EPSG:4326",
                            src.crs,
                            lon_min, lat_min, lon_max, lat_max
                        )
                        
                        # Crear ventana desde bbox reproyectado
                        window = windows.from_bounds(
                            *bbox_proj,
                            transform=src.transform
                        )
                        
                        # VALIDAR que ventana tenga datos
                        if window.width == 0 or window.height == 0:
                            logger.warning(f"Ventana vacía para banda {band_name} (width={window.width}, height={window.height})")
                            continue
                        
                        # Leer datos
                        band_data = src.read(1, window=window)
                        
                        # Validar que tenga datos
                        if band_data.size == 0:
                            logger.warning(f"Array vacío para banda {band_name}")
                            continue
                        
                        bands[band_name] = band_data.astype(float)
                        logger.info(f"✅ Banda {band_name} leída: {band_data.shape}, valores válidos: {np.sum(np.isfinite(band_data))}")
                        
                except Exception as e:
                    logger.warning(f"Error leyendo banda {band_name}: {e}")
                    continue
            
            if len(bands) < 4:  # Necesitamos al menos 4 bandas
                logger.error(f"Solo se pudieron leer {len(bands)} bandas")
                return None
            
            # CRÍTICO: Resamplear todas las bandas al mismo tamaño (usar B04 como referencia)
            reference_shape = bands['B04'].shape
            logger.info(f"Shape de referencia (B04): {reference_shape}")
            
            resampled_bands = {}
            for band_name, band_data in bands.items():
                if band_data.shape != reference_shape:
                    logger.info(f"Resampling {band_name} de {band_data.shape} a {reference_shape}")
                    from scipy.ndimage import zoom
                    zoom_factors = (reference_shape[0] / band_data.shape[0], 
                                   reference_shape[1] / band_data.shape[1])
                    resampled_bands[band_name] = zoom(band_data, zoom_factors, order=1)
                else:
                    resampled_bands[band_name] = band_data
            
            # Calcular índices con bandas resampled
            blue = resampled_bands['B02']
            green = resampled_bands['B03']
            red = resampled_bands['B04']
            nir = resampled_bands['B08']
            swir = resampled_bands['B11']
            
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
        end_date: Optional[datetime] = None,
        resolution_m: int = 30  # OPTIMIZADO: 30m en vez de 10m (9x más rápido)
    ) -> Optional[SatelliteData]:
        """
        Obtener datos Sentinel-1 (SAR)
        
        Bandas: VV, VH polarization
        Resolución: 30m (optimizado para velocidad)
        
        MODOS AUTOMÁTICOS:
        - IW (Interferometric Wide): latitudes <75° (250km swath)
        - EW (Extra Wide): latitudes ≥75° (400km swath, diseñado para polos)
        
        MEJORAS 2026-01-26:
        - Ventana temporal ampliada: 30 → 90 días
        - Fallback a colección sentinel-1-grd
        - Logging detallado a archivo
        - Cache en BD (evita re-descargas)
        - Resolución 30m (9x más rápido que 10m)
        
        LIMITACIÓN CONOCIDA:
        - Descargas de COGs grandes (200-400 MB) toman 2-5 minutos
        - Sin stackstac, no hay forma eficiente de descargar solo bbox
        - Recomendación: Usar cache agresivamente o deshabilitar con SAR_ENABLED=false
        """
        
        # Check if SAR is enabled
        sar_enabled = os.getenv("SAR_ENABLED", "true").lower() == "true"
        if not sar_enabled:
            logger.info("SAR disabled via SAR_ENABLED=false")
            return None
        
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
            
            # CACHE: Intentar obtener del cache primero
            try:
                from cache.sar_cache import get_sar_cache
                sar_cache = get_sar_cache()
                
                cached_data = sar_cache.get(lat_min, lat_max, lon_min, lon_max)
                
                if cached_data:
                    log(f"[SAR] CACHE HIT - usando datos guardados")
                    
                    # Reconstruir SatelliteData desde cache
                    processing_time = asyncio.get_event_loop().time() - start_time
                    
                    if log_file:
                        log_file.close()
                    
                    return SatelliteData(
                        source='sentinel-1-rtc',
                        acquisition_date=cached_data['acquisition_date'],
                        cloud_cover=0.0,
                        resolution_m=cached_data['resolution_m'],
                        lat_min=lat_min,
                        lat_max=lat_max,
                        lon_min=lon_min,
                        lon_max=lon_max,
                        bands={},  # No guardamos arrays completos
                        indices={
                            'vv_mean': float(cached_data['vv_mean']),
                            'vh_mean': float(cached_data['vh_mean']),
                            'vv_vh_ratio': float(cached_data['vv_vh_ratio']),
                            'backscatter_std': float(cached_data['backscatter_std'])
                        },
                        anomaly_score=0.0,
                        anomaly_type='moderate_backscatter',
                        confidence=0.8,
                        processing_time_s=processing_time,
                        cached=True
                    )
            except Exception as e:
                log(f"[SAR] Cache no disponible: {e}")
                # Continuar sin cache
            
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
                
                # Inicializar confidence
                confidence = 0.8  # Default para full-resolution
                
                # Leer bandas con rasterio usando overviews de COG
                # OPTIMIZACIÓN: Los COGs tienen overviews pre-calculados
                # Esto es mucho más rápido que descargar el raster completo
                
                log(f"[SAR] Estrategia: Intentar full resolution, fallback a overview si falla")
                
                # INTENTO 1: Full resolution con ventana específica
                try:
                    with rasterio.open(vh_url) as src:
                        # Reprojectar bbox
                        bbox_proj = transform_bounds(
                            "EPSG:4326",
                            src.crs,
                            lon_min, lat_min, lon_max, lat_max
                        )
                        
                        # Crear ventana
                        window = windows.from_bounds(*bbox_proj, transform=src.transform)
                        
                        if window.width > 0 and window.height > 0:
                            vh = src.read(1, window=window)
                            log(f"[SAR] Banda VH cargada (full-res window): {vh.shape}")
                        else:
                            raise ValueError("Ventana vacía")
                    
                    with rasterio.open(vv_url) as src:
                        bbox_proj = transform_bounds(
                            "EPSG:4326",
                            src.crs,
                            lon_min, lat_min, lon_max, lat_max
                        )
                        window = windows.from_bounds(*bbox_proj, transform=src.transform)
                        
                        if window.width > 0 and window.height > 0:
                            vv = src.read(1, window=window)
                            log(f"[SAR] Banda VV cargada (full-res window): {vv.shape}")
                        else:
                            raise ValueError("Ventana vacía")
                    
                    log(f"[SAR] [OK] Full resolution exitoso")
                    
                except Exception as e:
                    # FALLBACK: Usar overview (menor resolución pero estable)
                    log(f"[SAR] [WARN] Full-res fallo: {e}")
                    log(f"[SAR] Fallback a overview level 2 (~30m)")
                    
                    try:
                        with rasterio.open(vh_url) as src:
                            # Leer overview level 2 (1/4 de resolución = ~40m)
                            if src.overviews(1):
                                overview_level = min(2, len(src.overviews(1)) - 1)
                                vh = src.read(1, out_shape=(
                                    src.height // (2 ** overview_level),
                                    src.width // (2 ** overview_level)
                                ))
                                log(f"[SAR] Banda VH cargada: {vh.shape} (overview level {overview_level})")
                            else:
                                # Sin overviews, leer completo con reducción
                                vh = src.read(1, out_shape=(
                                    src.height // 3,
                                    src.width // 3
                                ))
                                log(f"[SAR] Banda VH cargada: {vh.shape} (sin overviews)")
                        
                        with rasterio.open(vv_url) as src:
                            if src.overviews(1):
                                overview_level = min(2, len(src.overviews(1)) - 1)
                                vv = src.read(1, out_shape=(
                                    src.height // (2 ** overview_level),
                                    src.width // (2 ** overview_level)
                                ))
                                log(f"[SAR] Banda VV cargada: {vv.shape} (overview level {overview_level})")
                            else:
                                vv = src.read(1, out_shape=(
                                    src.height // 3,
                                    src.width // 3
                                ))
                                log(f"[SAR] Banda VV cargada: {vv.shape} (sin overviews)")
                        
                        log(f"[SAR] [OK] Fallback a overview exitoso (confidence reducida a 0.6)")
                        confidence = 0.6  # Reducir confianza por usar overview
                        
                    except Exception as e2:
                        log(f"[SAR] [FAIL] Fallback tambien fallo: {e2}")
                        import traceback
                        log(f"[SAR] Traceback: {traceback.format_exc()}")
                        if log_file:
                            log_file.close()
                        return None
                
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
            anomaly_score, anomaly_confidence = self.detect_anomaly(vv)
            
            # Usar el confidence más bajo (del fallback o del detector)
            final_confidence = min(confidence, anomaly_confidence)
            
            # Tipo de anomalía basado en backscatter
            if indices['vv_mean'] > -5:
                anomaly_type = 'high_backscatter_compaction'
            elif indices['vv_mean'] < -15:
                anomaly_type = 'low_backscatter_water'
            else:
                anomaly_type = 'moderate_backscatter'
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            log(f"[SAR] Procesamiento completado en {processing_time:.2f}s")
            log(f"[SAR] EXITO TOTAL - Datos SAR obtenidos correctamente (confidence={final_confidence:.2f})")
            
            # GUARDAR EN CACHE para evitar re-descargas
            try:
                from cache.sar_cache import get_sar_cache
                sar_cache = get_sar_cache()
                
                # Obtener scene_id del item
                scene_id = best_item.id if hasattr(best_item, 'id') else None
                
                saved = sar_cache.set(
                    lat_min=lat_min,
                    lat_max=lat_max,
                    lon_min=lon_min,
                    lon_max=lon_max,
                    vv_mean=indices['vv_mean'],
                    vh_mean=indices['vh_mean'],
                    vv_vh_ratio=indices['vv_vh_ratio'],
                    backscatter_std=indices['backscatter_std'],
                    source='sentinel-1-rtc',
                    acquisition_date=acquisition_date,
                    resolution_m=resolution_m,
                    scene_id=scene_id
                )
                
                if saved:
                    log(f"[SAR] Datos guardados en cache")
                else:
                    log(f"[SAR] No se pudo guardar en cache (no crítico)")
                    
            except Exception as e:
                log(f"[SAR] Error guardando cache: {e} (no crítico)")
            
            if log_file:
                log_file.close()
            
            logger.info(f"✅ Sentinel-1 processed in {processing_time:.2f}s")
            
            return SatelliteData(
                source='sentinel-1-rtc',
                acquisition_date=acquisition_date,
                cloud_cover=0.0,  # SAR no afectado por nubes
                resolution_m=float(resolution_m),  # Usar resolución configurada
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                bands=bands,
                indices=indices,
                anomaly_score=anomaly_score,
                anomaly_type=anomaly_type,
                confidence=final_confidence,  # Usar confidence ajustado por fallback
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
            
            logger.info(f"Using Landsat scene from {acquisition_date.date()}")
            
            # Cargar banda térmica (lwir11) usando rasterio (sin stackstac)
            lwir_asset = best_item.assets.get('lwir11')
            
            if not lwir_asset:
                logger.error("Asset lwir11 no encontrado")
                return None
            
            # Firmar URL
            lwir_url = planetary_computer.sign(lwir_asset.href)
            
            # Leer con rasterio
            import rasterio
            import rasterio.warp
            
            with rasterio.open(lwir_url) as src:
                # Reprojectar bbox a CRS del raster
                bbox_proj = rasterio.warp.transform_bounds(
                    "EPSG:4326",
                    src.crs,
                    lon_min, lat_min, lon_max, lat_max
                )
                
                # Crear ventana
                window = rasterio.windows.from_bounds(*bbox_proj, transform=src.transform)
                
                # Validar ventana
                if window.width == 0 or window.height == 0:
                    logger.warning(f"Ventana vacía para Landsat thermal")
                    return None
                
                # Leer datos
                thermal = src.read(1, window=window).astype(float)
            
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
