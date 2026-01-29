#!/usr/bin/env python3
"""
VIIRS Connector - Visible Infrared Imaging Radiometer Suite
==========================================================

VIIRS (NASA/NOAA) - Instrumento 11/15
- Resolución: 375m-750m
- Cobertura: Global diaria
- Productos: Temperatura superficial, NDVI, fuegos activos
- API: NASA Earthdata (ya hasheada en BD)

APLICACIONES ARQUEOLÓGICAS:
- Detección de anomalías térmicas nocturnas
- Monitoreo de vegetación de alta frecuencia
- Detección de actividad humana (fuegos)
"""

import requests
import numpy as np
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class VIIRSConnector:
    """Conector para datos VIIRS via NASA Earthdata."""
    
    def __init__(self):
        """Inicializar conector VIIRS."""
        
        # DESACTIVADO: 403 Forbidden constante
        self.available = False
        self.disabled_reason = "VIIRS temporarily unavailable (403 Forbidden - API access restricted)"
        
        logger.info(f"⚠️ VIIRS: {self.disabled_reason}")
        
        self.base_url = "https://appeears.earthdatacloud.nasa.gov/api/v1"
        self.product_mapping = {
            'thermal': 'VNP21A1D.001',  # Land Surface Temperature Daily
            'ndvi': 'VNP13A1.001',      # Vegetation Indices 16-Day
            'fire': 'VNP14A1.001'       # Thermal Anomalies/Fire Daily
        }
        
        # Credenciales desde variables de entorno (hasheadas en BD)
        import os
        self.username = os.getenv('EARTHDATA_USERNAME')
        self.password = os.getenv('EARTHDATA_PASSWORD')
    
    async def get_thermal_data(self, lat_min: float, lat_max: float, 
                              lon_min: float, lon_max: float,
                              days_back: int = 7) -> Dict[str, Any]:
        """
        Obtener datos de temperatura superficial VIIRS.
        
        DESACTIVADO: API devuelve 403 Forbidden constantemente.
        """
        
        if not self.available:
            logger.info("ℹ️ VIIRS: Skipped (temporarily unavailable)")
            return None
        
        VENTAJA vs MODIS: Mayor resolución espacial (375m vs 1km)
        """
        
        try:
            # Calcular fechas
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Parámetros de consulta
            params = {
                'product': self.product_mapping['thermal'],
                'layer': 'LST_Day_1km',
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'bbox': f"{lon_min},{lat_min},{lon_max},{lat_max}",
                'format': 'json'
            }
            
            # Realizar consulta
            response = await self._make_earthdata_request(
                f"{self.base_url}/task", params
            )
            
            if response and 'data' in response:
                # Procesar datos térmicos
                thermal_values = []
                for pixel in response['data']:
                    if pixel.get('LST_Day_1km') and pixel['LST_Day_1km'] > 0:
                        # Convertir de Kelvin a Celsius
                        temp_c = pixel['LST_Day_1km'] * 0.02 - 273.15
                        thermal_values.append(temp_c)
                
                if thermal_values:
                    mean_temp = np.mean(thermal_values)
                    temp_std = np.std(thermal_values)
                    
                    return {
                        'value': float(mean_temp),
                        'std_dev': float(temp_std),
                        'pixel_count': len(thermal_values),
                        'unit': 'celsius',
                        'source': 'VIIRS_VNP21A1D',
                        'resolution_m': 1000,
                        'acquisition_date': end_date.isoformat(),
                        'quality': 'high' if len(thermal_values) > 10 else 'medium'
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo datos térmicos VIIRS: {e}")
            return None
    
    async def get_ndvi_data(self, lat_min: float, lat_max: float,
                           lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        Obtener datos NDVI de VIIRS.
        
        VENTAJA: Frecuencia diaria vs 16 días de MODIS
        """
        
        try:
            # Fechas recientes (últimos 16 días para composite)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=16)
            
            params = {
                'product': self.product_mapping['ndvi'],
                'layer': 'NDVI',
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'bbox': f"{lon_min},{lat_min},{lon_max},{lat_max}",
                'format': 'json'
            }
            
            response = await self._make_earthdata_request(
                f"{self.base_url}/task", params
            )
            
            if response and 'data' in response:
                ndvi_values = []
                for pixel in response['data']:
                    if pixel.get('NDVI') and pixel['NDVI'] > -1:
                        # VIIRS NDVI ya está en escala -1 a 1
                        ndvi_values.append(pixel['NDVI'] * 0.0001)
                
                if ndvi_values:
                    mean_ndvi = np.mean(ndvi_values)
                    ndvi_std = np.std(ndvi_values)
                    
                    return {
                        'value': float(mean_ndvi),
                        'std_dev': float(ndvi_std),
                        'pixel_count': len(ndvi_values),
                        'unit': 'ndvi',
                        'source': 'VIIRS_VNP13A1',
                        'resolution_m': 500,
                        'acquisition_date': end_date.isoformat(),
                        'quality': 'high' if mean_ndvi > -0.5 else 'medium'
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo NDVI VIIRS: {e}")
            return None
    
    async def get_fire_data(self, lat_min: float, lat_max: float,
                           lon_min: float, lon_max: float,
                           days_back: int = 30) -> Dict[str, Any]:
        """
        Obtener datos de anomalías térmicas/fuegos VIIRS.
        
        APLICACIÓN ARQUEOLÓGICA: Detectar actividad humana reciente
        """
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            params = {
                'product': self.product_mapping['fire'],
                'layer': 'FRP',  # Fire Radiative Power
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'bbox': f"{lon_min},{lat_min},{lon_max},{lat_max}",
                'format': 'json'
            }
            
            response = await self._make_earthdata_request(
                f"{self.base_url}/task", params
            )
            
            if response and 'data' in response:
                fire_detections = []
                total_frp = 0
                
                for pixel in response['data']:
                    if pixel.get('FRP') and pixel['FRP'] > 0:
                        fire_detections.append(pixel['FRP'])
                        total_frp += pixel['FRP']
                
                fire_density = len(fire_detections) / ((lat_max - lat_min) * (lon_max - lon_min))
                
                return {
                    'value': float(fire_density),
                    'total_frp': float(total_frp),
                    'detection_count': len(fire_detections),
                    'unit': 'detections_per_degree2',
                    'source': 'VIIRS_VNP14A1',
                    'resolution_m': 375,
                    'acquisition_date': end_date.isoformat(),
                    'quality': 'high' if len(fire_detections) > 0 else 'low'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de fuego VIIRS: {e}")
            return None
    
    async def _make_earthdata_request(self, url: str, params: Dict) -> Optional[Dict]:
        """Realizar petición autenticada a NASA Earthdata."""
        
        try:
            # Usar credenciales hasheadas en BD
            auth = (self.username, self.password) if self.username else None
            
            response = requests.get(
                url,
                params=params,
                auth=auth,
                timeout=30,
                headers={'User-Agent': 'ArcheoScope/2.0'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"VIIRS API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error en petición VIIRS: {e}")
            return None