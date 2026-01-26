"""
Procesador Asíncrono de Datos Satelitales
Optimiza velocidad con procesamiento paralelo y caché
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import asdict

from .satellite_connectors import PlanetaryComputerConnector, SatelliteData
from .satellite_cache import satellite_cache

logger = logging.getLogger(__name__)


class AsyncSatelliteProcessor:
    """
    Procesador asíncrono optimizado para datos satelitales
    
    Estrategia de optimización:
    1. Caché primero (< 1 segundo si existe)
    2. Procesamiento paralelo de múltiples fuentes
    3. Timeout para evitar bloqueos
    4. Fallback a simulación si falla
    """
    
    def __init__(self, use_cache: bool = True, timeout_seconds: int = 30):
        self.use_cache = use_cache
        self.timeout_seconds = timeout_seconds
        
        # Inicializar conector
        self.connector = PlanetaryComputerConnector(cache_enabled=use_cache)
        
        logger.info(f"✅ AsyncSatelliteProcessor initialized (cache: {use_cache})")
    
    async def get_all_data(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        max_cloud_cover: float = 20.0
    ) -> Dict[str, Optional[SatelliteData]]:
        """
        Obtener TODOS los datos satelitales en paralelo
        
        Returns:
            {
                'multispectral': SatelliteData,
                'sar': SatelliteData,
                'thermal': SatelliteData
            }
        """
        logger.info(f"🛰️ Fetching all satellite data for bbox [{lat_min}, {lat_max}, {lon_min}, {lon_max}]")
        
        start_time = asyncio.get_event_loop().time()
        
        # Intentar caché primero
        cached_results = {}
        if self.use_cache:
            cached_results = await self._try_cache(
                lat_min, lat_max, lon_min, lon_max, start_date
            )
        
        # Determinar qué datos faltan
        tasks = {}
        
        if 'multispectral' not in cached_results:
            tasks['multispectral'] = self._fetch_with_timeout(
                self.connector.get_multispectral_data,
                lat_min, lat_max, lon_min, lon_max,
                start_date, end_date, max_cloud_cover
            )
        
        if 'sar' not in cached_results:
            tasks['sar'] = self._fetch_with_timeout(
                self.connector.get_sar_data,
                lat_min, lat_max, lon_min, lon_max,
                start_date, end_date
            )
        
        if 'thermal' not in cached_results:
            tasks['thermal'] = self._fetch_with_timeout(
                self.connector.get_thermal_data,
                lat_min, lat_max, lon_min, lon_max,
                start_date, end_date
            )
        
        # Ejecutar en paralelo
        if tasks:
            logger.info(f"⚡ Fetching {len(tasks)} data types in parallel...")
            results = await asyncio.gather(*tasks.values(), return_exceptions=True)
            
            # Combinar resultados
            for i, (data_type, _) in enumerate(tasks.items()):
                result = results[i]
                
                if isinstance(result, Exception):
                    logger.error(f"Error fetching {data_type}: {result}")
                    cached_results[data_type] = None
                else:
                    cached_results[data_type] = result
                    
                    # Cachear si es exitoso
                    if result and self.use_cache:
                        satellite_cache.set(
                            lat_min, lat_max, lon_min, lon_max,
                            data_type, result, result.acquisition_date
                        )
        
        total_time = asyncio.get_event_loop().time() - start_time
        
        # Contar éxitos
        successful = sum(1 for v in cached_results.values() if v is not None)
        
        logger.info(
            f"✅ Satellite data fetched: {successful}/3 successful in {total_time:.2f}s"
        )
        
        return cached_results
    
    async def _try_cache(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        date: Optional[datetime] = None
    ) -> Dict[str, Optional[SatelliteData]]:
        """Intentar obtener datos de caché"""
        results = {}
        
        for data_type in ['multispectral', 'sar', 'thermal']:
            cached = satellite_cache.get(
                lat_min, lat_max, lon_min, lon_max,
                data_type, date
            )
            
            if cached:
                results[data_type] = cached
                logger.info(f"✅ Cache HIT: {data_type}")
        
        return results
    
    async def _fetch_with_timeout(self, fetch_func, *args, **kwargs):
        """Ejecutar fetch con timeout"""
        try:
            return await asyncio.wait_for(
                fetch_func(*args, **kwargs),
                timeout=self.timeout_seconds
            )
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching data from {fetch_func.__name__}")
            return None
        except Exception as e:
            logger.error(f"Error in {fetch_func.__name__}: {e}")
            return None
    
    def convert_to_dict(self, data: Optional[SatelliteData]) -> Optional[Dict[str, Any]]:
        """Convertir SatelliteData a dict serializable (sin arrays numpy)"""
        if data is None:
            return None
        
        result = {
            'source': data.source,
            'acquisition_date': data.acquisition_date.isoformat(),
            'cloud_cover': data.cloud_cover,
            'resolution_m': data.resolution_m,
            'bbox': {
                'lat_min': data.lat_min,
                'lat_max': data.lat_max,
                'lon_min': data.lon_min,
                'lon_max': data.lon_max
            },
            'indices': data.indices,
            'anomaly_score': data.anomaly_score,
            'anomaly_type': data.anomaly_type,
            'confidence': data.confidence,
            'processing_time_s': data.processing_time_s,
            'cached': data.cached
        }
        
        return result
    
    async def get_quick_summary(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float
    ) -> Dict[str, Any]:
        """
        Obtener resumen rápido (solo índices, sin arrays)
        Optimizado para respuesta rápida
        """
        all_data = await self.get_all_data(lat_min, lat_max, lon_min, lon_max)
        
        summary = {
            'bbox': [lat_min, lat_max, lon_min, lon_max],
            'timestamp': datetime.now().isoformat(),
            'data_sources': {}
        }
        
        for data_type, data in all_data.items():
            summary['data_sources'][data_type] = self.convert_to_dict(data)
        
        # Calcular score multi-instrumental
        scores = []
        for data in all_data.values():
            if data:
                scores.append(data.anomaly_score * data.confidence)
        
        if scores:
            summary['multi_instrumental_score'] = sum(scores) / len(scores)
            summary['convergence_count'] = len(scores)
            summary['convergence_ratio'] = len(scores) / 3.0
        else:
            summary['multi_instrumental_score'] = 0.0
            summary['convergence_count'] = 0
            summary['convergence_ratio'] = 0.0
        
        return summary


# Instancia global
async_satellite_processor = AsyncSatelliteProcessor()
