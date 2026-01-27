"""
ICESat-2 Connector - NASA Earthdata
Elevación de precisión centimétrica para hielo y terreno
"""

import logging
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
    ) -> Optional[SatelliteData]:
        """
        Obtener datos de elevación ICESat-2
        
        Args:
            product: "ATL06" (Land Ice) o "ATL08" (Land/Vegetation)
        """
        if not self.available:
            logger.error("ICESat-2 not available")
            return None
        
        try:
            # Fechas por defecto: últimos 6 meses
            if end_date is None:
                end_date = datetime.now()
            if start_date is None:
                start_date = end_date - timedelta(days=180)
            
            bbox = (lon_min, lat_min, lon_max, lat_max)
            
            logger.info(f"🛰️ Buscando ICESat-2 {product} en bbox {bbox}")
            
            # Buscar granules
            results = earthaccess.search_data(
                short_name=product,
                bounding_box=bbox,
                temporal=(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")),
                count=5
            )
            
            if not results:
                logger.warning(f"No ICESat-2 {product} data found for bbox {bbox}")
                return None
            
            logger.info(f"✅ Found {len(results)} ICESat-2 granules")
            
            # Descargar el granule más reciente
            granule = results[0]
            files = earthaccess.download(granule, local_path="./cache/icesat2")
            
            if not files:
                logger.error("Failed to download ICESat-2 data")
                return None
            
            # Leer datos HDF5
            h5_file = files[0]
            elevations = []
            lats = []
            lons = []
            
            with h5py.File(h5_file, 'r') as f:
                # ATL06 tiene 3 beams (gt1l, gt1r, gt2l, gt2r, gt3l, gt3r)
                for beam in ['gt1l', 'gt1r', 'gt2l', 'gt2r', 'gt3l', 'gt3r']:
                    try:
                        if product == "ATL06":
                            path = f'{beam}/land_ice_segments'
                            h_li = f[path]['h_li'][:]  # Altura sobre elipsoide
                            lat = f[path]['latitude'][:]
                            lon = f[path]['longitude'][:]
                        else:  # ATL08
                            path = f'{beam}/land_segments'
                            h_li = f[path]['terrain']['h_te_mean'][:]
                            lat = f[path]['latitude'][:]
                            lon = f[path]['longitude'][:]
                        
                        # Filtrar por bbox
                        mask = (
                            (lat >= lat_min) & (lat <= lat_max) &
                            (lon >= lon_min) & (lon <= lon_max)
                        )
                        
                        elevations.extend(h_li[mask])
                        lats.extend(lat[mask])
                        lons.extend(lon[mask])
                        
                    except KeyError:
                        continue
            
            if not elevations:
                logger.warning("No elevation data in bbox")
                return None
            
            elevations = np.array(elevations)
            lats = np.array(lats)
            lons = np.array(lons)
            
            # CRÍTICO: Filtros de calidad robustos para ICESat-2
            # 1. Eliminar valores finitos (inf/nan)
            valid = elevations[np.isfinite(elevations)]
            
            # 2. Eliminar outliers absurdos (ICESat a veces devuelve locuras)
            valid = valid[(valid > -500) & (valid < 9000)]  # Rango terrestre razonable
            
            # 3. Verificar cantidad mínima de puntos válidos
            if valid.size < 10:
                logger.warning(f"ICESat-2: Insuficientes puntos válidos ({valid.size}/10 mínimo)")
                return SatelliteData(
                    source=f'icesat2-{product.lower()}',
                    acquisition_date=datetime.now(),
                    cloud_cover=0.0,
                    resolution_m=17.0,
                    lat_min=lat_min,
                    lat_max=lat_max,
                    lon_min=lon_min,
                    lon_max=lon_max,
                    bands={},
                    indices={
                        'elevation_mean': None,
                        'elevation_std': None,
                        'points_count': len(elevations),
                        'valid_points': valid.size
                    },
                    anomaly_score=0.0,
                    anomaly_type='insufficient_data',
                    confidence=0.0,
                    processing_time_s=0.0,
                    cached=False
                )
            
            # 4. Calcular estadísticas SOLO con datos válidos
            mean_elev = float(np.mean(valid))
            std_elev = float(np.std(valid))
            
            indices = {
                'elevation_mean': mean_elev,
                'elevation_std': std_elev,
                'elevation_min': float(np.min(valid)),
                'elevation_max': float(np.max(valid)),
                'elevation_range': float(np.max(valid) - np.min(valid)),
                'points_count': len(elevations),
                'valid_points': valid.size,
                'quality_ratio': float(valid.size / len(elevations)) if len(elevations) > 0 else 0.0
            }
            
            # 5. Detectar depresiones con datos válidos
            depressions = valid < (mean_elev - 2 * std_elev)
            anomaly_score = float(np.sum(depressions) / len(valid)) if len(valid) > 0 else 0.0
            
            # 6. Confianza basada en calidad de datos
            quality_ratio = valid.size / len(elevations) if len(elevations) > 0 else 0.0
            
            if quality_ratio > 0.8 and valid.size > 100:
                confidence = 0.9
            elif quality_ratio > 0.6 and valid.size > 50:
                confidence = 0.7
            elif quality_ratio > 0.4 and valid.size > 20:
                confidence = 0.5
            else:
                confidence = 0.3
            
            # Tipo de anomalía
            if indices['elevation_range'] > 50:
                anomaly_type = 'high_relief'
            elif anomaly_score > 0.1:
                anomaly_type = 'depression_detected'
            else:
                anomaly_type = 'flat_terrain'
            
            logger.info(f"✅ ICESat-2 processed: {len(elevations)} points")
            
            return SatelliteData(
                source=f'icesat2-{product.lower()}',
                acquisition_date=datetime.now(),
                cloud_cover=0.0,
                resolution_m=17.0,
                lat_min=lat_min,
                lat_max=lat_max,
                lon_min=lon_min,
                lon_max=lon_max,
                bands={'elevation': elevations, 'latitude': lats, 'longitude': lons},
                indices=indices,
                anomaly_score=anomaly_score,
                anomaly_type=anomaly_type,
                confidence=confidence,
                processing_time_s=0.0,
                cached=False
            )
            
        except Exception as e:
            logger.error(f"Error fetching ICESat-2 data: {e}", exc_info=True)
            return None
