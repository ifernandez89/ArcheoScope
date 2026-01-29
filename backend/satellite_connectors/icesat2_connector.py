"""
ICESat-2 Connector - NASA Earthdata
Elevación de precisión centimétrica para hielo y terreno
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import numpy as np

try:
    import earthaccess
    import h5py
    ICESAT2_AVAILABLE = True
except ImportError:
    ICESAT2_AVAILABLE = False

from .base_connector import SatelliteConnector, SatelliteData

logger = logging.getLogger(__name__)


class ICESat2Connector(SatelliteConnector):
    """
    Conector a ICESat-2 (NASA)
    
    Productos:
    - ATL06: Land Ice Height (precisión centimétrica)
    - ATL08: Land/Vegetation Height
    
    Resolución: 17m along-track
    Cobertura: Global desde 2018
    API: NASA Earthdata (gratuita con registro)
    """
    
    def __init__(self, cache_enabled: bool = True):
        super().__init__(cache_enabled)
        self.name = "ICESat2"
        
        if not ICESAT2_AVAILABLE:
            logger.warning(
                "ICESat-2 libraries not available. "
                "Install with: pip install earthaccess h5py"
            )
            self.available = False
        else:
            self.available = True
            # Autenticar con NASA Earthdata usando credenciales de BD
            try:
                import sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent.parent))
                from credentials_manager import CredentialsManager
                
                creds_manager = CredentialsManager()
                
                # Obtener credenciales desde BD
                username = creds_manager.get_credential("earthdata", "username")
                password = creds_manager.get_credential("earthdata", "password")
                
                if username and password:
                    # Configurar variables de entorno para earthaccess
                    os.environ['EARTHDATA_USERNAME'] = username
                    os.environ['EARTHDATA_PASSWORD'] = password
                    
                    earthaccess.login(strategy="environment")
                    logger.info("ICESat-2 connector initialized (NASA Earthdata desde BD)")
                else:
                    logger.warning("Credenciales Earthdata no encontradas en BD")
                    self.available = False
                    
            except Exception as e:
                logger.warning(f"ICESat-2 authentication failed: {e}")
                logger.info("Configura credenciales con: python backend/credentials_manager.py")
                self.available = False
    
    async def get_elevation_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        product: str = "ATL06"
    ):
        """
        Obtener datos de elevación ICESat-2 con Instrument Contract
        
        Args:
            product: "ATL06" (Land Ice) o "ATL08" (Land/Vegetation)
            
        Returns:
            InstrumentMeasurement con estado robusto
        """
        # Importar contrato
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from instrument_contract import InstrumentMeasurement, InstrumentStatus
        
        if not self.available:
            return InstrumentMeasurement.create_error(
                instrument_name="ICESat-2",
                measurement_type="elevation",
                error_msg="ICESat-2 not available - credentials not configured",
                source="NASA Earthdata"
            )
        
        try:
            # Fechas por defecto: últimos 6 meses
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                start_date = end_date - timedelta(days=180)
            
            bbox = (lon_min, lat_min, lon_max, lat_max)
            
            logger.info(f"Buscando ICESat-2 {product} en bbox {bbox}")
            
            # Buscar granules
            results = earthaccess.search_data(
                short_name=product,
                bounding_box=bbox,
                temporal=(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")),
                count=5
            )
            
            if not results:
                logger.info(f"ICESat-2: coverage=false (no granules in region) - NORMAL, not error")
                return InstrumentMeasurement.create_no_data(
                    instrument_name="ICESat-2",
                    measurement_type="elevation",
                    reason=f"No {product} granules found - limited orbital coverage (expected)",
                    source="NASA Earthdata"
                )
            
            logger.info(f"Found {len(results)} ICESat-2 granules")
            
            # Descargar el granule más reciente
            granule = results[0]
            acquisition_date = granule['umm']['TemporalExtent']['RangeDateTime']['BeginningDateTime']
            
            files = earthaccess.download(granule, local_path="./cache/icesat2")
            
            if not files:
                return InstrumentMeasurement.create_error(
                    instrument_name="ICESat-2",
                    measurement_type="elevation",
                    error_msg="Failed to download granule",
                    source="NASA Earthdata"
                )
            
            # Leer datos HDF5
            h5_file = files[0]
            elevations = []
            quality_flags = []
            
            with h5py.File(h5_file, 'r') as f:
                # ATL06 tiene 3 beams (gt1l, gt1r, gt2l, gt2r, gt3l, gt3r)
                for beam in ['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r']:
                    try:
                        if product == "ATL06":
                            path = f'{beam}/land_ice_segments'
                            h_li = f[path]['h_li'][:]  # Altura sobre elipsoide
                            lat = f[path]['latitude'][:]
                            lon = f[path]['longitude'][:]
                            # CRÍTICO: Leer quality flags
                            try:
                                atl06_quality = f[path]['atl06_quality_summary'][:]
                            except:
                                atl06_quality = np.zeros_like(h_li)
                        else:  # ATL08
                            path = f'{beam}/land_segments'
                            h_li = f[path]['terrain']['h_te_mean'][:]
                            lat = f[path]['latitude'][:]
                            lon = f[path]['longitude'][:]
                            atl06_quality = np.zeros_like(h_li)
                        
                        # Filtrar por bbox
                        mask = (
                            (lat >= lat_min) & (lat <= lat_max) &
                            (lon >= lon_min) & (lon <= lon_max)
                        )
                        
                        elevations.extend(h_li[mask])
                        quality_flags.extend(atl06_quality[mask])
                        
                    except KeyError:
                        continue
            
            if not elevations:
                return InstrumentMeasurement.create_no_data(
                    instrument_name="ICESat-2",
                    measurement_type="elevation",
                    reason="No elevation data in bbox after filtering",
                    source="NASA Earthdata"
                )
            
            elevations = np.array(elevations)
            quality_flags = np.array(quality_flags)
            
            # CRÍTICO: Filtrar por calidad Y valores finitos
            valid_mask = (
                (quality_flags == 0) &  # Quality flag 0 = good
                np.isfinite(elevations)  # No inf/nan
            )
            
            valid_elevations = elevations[valid_mask]
            
            # CRÍTICO: Validar mínimo de puntos
            # AJUSTADO: 5 puntos mínimo (antes 10) para regiones glaciares con cobertura escasa
            MIN_POINTS = 5
            if len(valid_elevations) < MIN_POINTS:
                return InstrumentMeasurement.create_invalid(
                    instrument_name="ICESat-2",
                    measurement_type="elevation",
                    reason=f"insufficient_valid_points - only {len(valid_elevations)} points after quality filtering (minimum: {MIN_POINTS})",
                    source="NASA Earthdata",
                    unit="meters"
                )
            
            # Calcular elevación promedio
            elevation_mean = float(np.mean(valid_elevations))
            elevation_std = float(np.std(valid_elevations))
            
            # Calcular confianza basada en cantidad y dispersión
            if len(valid_elevations) > 100 and elevation_std < 50:
                confidence = 0.95
            elif len(valid_elevations) > 50:
                confidence = 0.85
            else:
                confidence = 0.70
            
            logger.info(f"ICESat-2 processed: {len(valid_elevations)} valid points, mean={elevation_mean:.2f}m")
            
            return InstrumentMeasurement(
                instrument_name="ICESat-2",
                measurement_type="elevation",
                value=elevation_mean,
                unit="meters",
                status=InstrumentStatus.OK,
                confidence=confidence,
                reason=None,
                quality_flags={
                    'valid_points': len(valid_elevations),
                    'total_points': len(elevations),
                    'quality_filtered': int(np.sum(quality_flags != 0)),
                    'elevation_std': elevation_std
                },
                source="NASA Earthdata",
                acquisition_date=acquisition_date[:10],
                processing_notes=f"Filtered by quality flags (atl06_quality_summary==0) and finite values. {len(valid_elevations)}/{len(elevations)} points valid."
            )
            
        except Exception as e:
            logger.error(f"Error fetching ICESat-2 data: {e}", exc_info=True)
            return InstrumentMeasurement.create_error(
                instrument_name="ICESat-2",
                measurement_type="elevation",
                error_msg=str(e),
                source="NASA Earthdata"
            )
