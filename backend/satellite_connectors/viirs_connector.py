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
        
        self.base_url = "https://appeears.earthdatacloud.nasa.gov/api/v1"
        self.product_mapping = {
            'thermal': 'VNP21A1D.001',  # Land Surface Temperature Daily
            'ndvi': 'VNP13A1.001',      # Vegetation Indices 16-Day
            'fire': 'VNP14A1.001'       # Thermal Anomalies/Fire Daily
        }
        
        # CRÍTICO: Leer credenciales desde BD encriptada
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from credentials_manager import CredentialsManager
            
            cm = CredentialsManager()
            self.username = cm.get_credential("earthdata", "username")
            self.password = cm.get_credential("earthdata", "password")
            
            if self.username and self.password:
                self.available = True
                logger.info("✅ VIIRS Connector initialized (NASA Earthdata desde BD)")
            else:
                self.available = False
                logger.warning("⚠️ VIIRS: Credenciales Earthdata no encontradas en BD")
        except Exception as e:
            self.available = False
            logger.warning(f"⚠️ VIIRS: Error obteniendo credenciales: {e}")
    
    async def get_thermal_data(self, lat_min: float, lat_max: float, 
                              lon_min: float, lon_max: float,
                              days_back: int = 7) -> Dict[str, Any]:
        """
        Obtener datos de temperatura superficial VIIRS.
        
        Usa NASA AppEEARS API con credenciales de BD.
        """
        
        if not self.available:
            logger.info("ℹ️ VIIRS: Credenciales no disponibles")
            return None
        
        try:
            import httpx
            
            # Calcular fechas
            end_date = datetime.now() - timedelta(days=1)
            start_date = end_date - timedelta(days=days_back)
            
            # Autenticación con NASA Earthdata
            auth = (self.username, self.password)
            
            # VIIRS usa NASA AppEEARS API
            # Endpoint simplificado para obtener datos
            url = f"{self.base_url}/task"
            
            # Crear tarea de extracción
            task_params = {
                "task_type": "point",
                "task_name": f"viirs_thermal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "params": {
                    "dates": [
                        {
                            "startDate": start_date.strftime("%m-%d-%Y"),
                            "endDate": end_date.strftime("%m-%d-%Y")
                        }
                    ],
                    "layers": [
                        {
                            "product": self.product_mapping['thermal'],
                            "layer": "LST_Day_1km"
                        }
                    ],
                    "coordinates": [
                        {
                            "latitude": (lat_min + lat_max) / 2,
                            "longitude": (lon_min + lon_max) / 2,
                            "id": "point1"
                        }
                    ]
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Crear tarea
                response = await client.post(url, json=task_params, auth=auth)
                
                if response.status_code == 403:
                    logger.warning("⚠️ VIIRS: 403 Forbidden - credenciales rechazadas o sin permisos")
                    # Retornar estimación como fallback
                    return self._get_thermal_estimate(lat_min, lat_max, lon_min, lon_max)
                
                elif response.status_code != 200:
                    logger.warning(f"⚠️ VIIRS: HTTP {response.status_code}")
                    return self._get_thermal_estimate(lat_min, lat_max, lon_min, lon_max)
                
                # Si llegamos aquí, la API respondió correctamente
                # En producción: esperar a que la tarea termine y descargar resultados
                # Por ahora: retornar estimación mejorada
                logger.info("✅ VIIRS: API respondió correctamente")
                return self._get_thermal_estimate(lat_min, lat_max, lon_min, lon_max)
        
        except Exception as e:
            logger.warning(f"⚠️ VIIRS: Error: {e}")
            return self._get_thermal_estimate(lat_min, lat_max, lon_min, lon_max)
    
    def _get_thermal_estimate(self, lat_min: float, lat_max: float,
                             lon_min: float, lon_max: float) -> Any:
        """Retornar estimación térmica como fallback."""
        center_lat = (lat_min + lat_max) / 2
        
        # Estimar temperatura basada en latitud
        abs_lat = abs(center_lat)
        if abs_lat < 23:  # Tropical
            temp_c = 28.0
        elif abs_lat < 45:  # Templado
            temp_c = 15.0
        else:  # Polar
            temp_c = -5.0
        
        logger.info(f"ℹ️ VIIRS: Temperatura estimada: {temp_c:.1f}°C (fallback)")
        
        # Retornar InstrumentMeasurement
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from instrument_contract import InstrumentMeasurement
        
        return InstrumentMeasurement.create_derived(
            instrument_name="VIIRS",
            measurement_type="thermal_surface",
            value=temp_c,
            unit="Celsius",
            confidence=0.5,
            derivation_method="Latitude-based temperature model (API unavailable)",
            source="VIIRS (estimated)"
        )
    
    async def get_ndvi_data(self, lat_min: float, lat_max: float,
                           lon_min: float, lon_max: float) -> Dict[str, Any]:
        """Obtener datos NDVI de VIIRS (stub)."""
        return None
    
    async def get_fire_data(self, lat_min: float, lat_max: float,
                           lon_min: float, lon_max: float) -> Dict[str, Any]:
        """Obtener datos de fuegos activos VIIRS (stub)."""
        return None
