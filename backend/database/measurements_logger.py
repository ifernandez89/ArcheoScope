"""
Measurements Logger - Registro de TODAS las mediciones instrumentales
=====================================================================

REGLA CRÍTICA: CADA medición de CADA instrumento DEBE registrarse en la BD
para trazabilidad científica completa.

NO omitir NINGUNA medición, exitosa o fallida.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json
from decimal import Decimal

logger = logging.getLogger(__name__)


class MeasurementsLogger:
    """
    Logger de mediciones instrumentales
    
    Registra CADA medición en la base de datos para:
    - Trazabilidad científica completa
    - Auditoría de datos
    - Análisis histórico
    - Validación de resultados
    - Reproducibilidad
    """
    
    def __init__(self, database_connection):
        """
        Inicializar logger de mediciones
        
        Args:
            database_connection: Conexión a PostgreSQL
        """
        self.db = database_connection
        logger.info("✅ MeasurementsLogger inicializado")
    
    async def log_measurement(
        self,
        instrument_name: str,
        measurement_type: str,
        value: float,
        unit: str,
        latitude: float,
        longitude: float,
        source: str,
        data_mode: str,
        confidence: float = 0.0,
        lat_min: Optional[float] = None,
        lat_max: Optional[float] = None,
        lon_min: Optional[float] = None,
        lon_max: Optional[float] = None,
        region_name: Optional[str] = None,
        analysis_id: Optional[str] = None,
        acquisition_date: Optional[str] = None,
        resolution_m: Optional[int] = None,
        environment_type: Optional[str] = None,
        environment_confidence: Optional[float] = None,
        threshold: Optional[float] = None,
        exceeds_threshold: Optional[bool] = None,
        anomaly_detected: Optional[bool] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Registrar una medición instrumental en la base de datos
        
        Args:
            instrument_name: Nombre del instrumento (sentinel_2_ndvi, icesat2, etc.)
            measurement_type: Tipo de medición (ndvi, elevation, thermal, etc.)
            value: Valor medido
            unit: Unidad de medida (m, K, dB, NDVI, etc.)
            latitude: Latitud central
            longitude: Longitud central
            source: Fuente del dato (ej: "Sentinel-2 (Copernicus)")
            data_mode: REAL, DERIVED, INFERRED, SIMULATED
            confidence: Confianza de la medición (0.0 - 1.0)
            ... (otros parámetros opcionales)
        
        Returns:
            UUID de la medición registrada, o None si falla
        """
        
        try:
            # Preparar datos adicionales como JSON
            additional_json = json.dumps(additional_data) if additional_data else None
            
            # Convertir acquisition_date a timestamp si es string
            acq_timestamp = None
            if acquisition_date:
                if isinstance(acquisition_date, str):
                    try:
                        acq_timestamp = datetime.fromisoformat(acquisition_date.replace('Z', '+00:00'))
                    except:
                        acq_timestamp = None
                else:
                    acq_timestamp = acquisition_date
            
            # Insertar en base de datos
            query = """
                INSERT INTO measurements (
                    measurement_timestamp,
                    analysis_id,
                    latitude,
                    longitude,
                    lat_min,
                    lat_max,
                    lon_min,
                    lon_max,
                    region_name,
                    instrument_name,
                    measurement_type,
                    value,
                    unit,
                    source,
                    acquisition_date,
                    resolution_m,
                    confidence,
                    data_mode,
                    environment_type,
                    environment_confidence,
                    threshold,
                    exceeds_threshold,
                    anomaly_detected,
                    additional_data
                ) VALUES (
                    NOW(),
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23
                )
                RETURNING id
            """
            
            result = await self.db.fetchrow(
                query,
                analysis_id,
                latitude,
                longitude,
                lat_min,
                lat_max,
                lon_min,
                lon_max,
                region_name,
                instrument_name,
                measurement_type,
                value,
                unit,
                source,
                acq_timestamp,
                resolution_m,
                confidence,
                data_mode,
                environment_type,
                environment_confidence,
                threshold,
                exceeds_threshold,
                anomaly_detected,
                additional_json
            )
            
            measurement_id = str(result['id'])
            
            logger.info(f"✅ Medición registrada: {instrument_name} = {value} {unit}")
            logger.debug(f"   ID: {measurement_id}")
            logger.debug(f"   Fuente: {source}")
            logger.debug(f"   Data mode: {data_mode}")
            
            return measurement_id
        
        except Exception as e:
            logger.error(f"❌ Error registrando medición de {instrument_name}: {e}")
            return None
    
    async def log_measurement_from_dict(
        self,
        measurement_data: Dict[str, Any],
        latitude: float,
        longitude: float,
        instrument_name: str,
        measurement_type: str,
        lat_min: Optional[float] = None,
        lat_max: Optional[float] = None,
        lon_min: Optional[float] = None,
        lon_max: Optional[float] = None,
        region_name: Optional[str] = None,
        analysis_id: Optional[str] = None,
        environment_type: Optional[str] = None,
        environment_confidence: Optional[float] = None,
        threshold: Optional[float] = None,
        exceeds_threshold: Optional[bool] = None,
        anomaly_detected: Optional[bool] = None
    ) -> Optional[str]:
        """
        Registrar medición desde un diccionario (formato de RealDataIntegrator)
        
        Args:
            measurement_data: Dict con 'value', 'source', 'confidence', etc.
            ... (otros parámetros de contexto)
        
        Returns:
            UUID de la medición registrada
        """
        
        if not measurement_data:
            return None
        
        # Extraer datos del diccionario
        value = measurement_data.get('value', 0.0)
        source = measurement_data.get('source', 'Unknown')
        confidence = measurement_data.get('confidence', 0.0)
        acquisition_date = measurement_data.get('acquisition_date')
        
        # Determinar unidad basada en tipo de medición
        unit = self._infer_unit(measurement_type, measurement_data)
        
        # Determinar data_mode
        data_mode = measurement_data.get('data_mode', 'REAL')
        
        # Extraer datos adicionales (todo lo que no sea estándar)
        standard_keys = {'value', 'source', 'confidence', 'acquisition_date', 'data_mode'}
        additional_data = {k: v for k, v in measurement_data.items() if k not in standard_keys}
        
        return await self.log_measurement(
            instrument_name=instrument_name,
            measurement_type=measurement_type,
            value=value,
            unit=unit,
            latitude=latitude,
            longitude=longitude,
            source=source,
            data_mode=data_mode,
            confidence=confidence,
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            region_name=region_name,
            analysis_id=analysis_id,
            acquisition_date=acquisition_date,
            environment_type=environment_type,
            environment_confidence=environment_confidence,
            threshold=threshold,
            exceeds_threshold=exceeds_threshold,
            anomaly_detected=anomaly_detected,
            additional_data=additional_data if additional_data else None
        )
    
    def _infer_unit(self, measurement_type: str, data: Dict[str, Any]) -> str:
        """Inferir unidad de medida basada en el tipo"""
        
        # Mapeo de tipos a unidades
        unit_map = {
            'ndvi': 'NDVI',
            'elevation': 'm',
            'thermal': 'K',
            'lst': 'K',
            'sar': 'dB',
            'backscatter': 'dB',
            'ice_concentration': '%',
            'snow_cover': '%',
            'sst': '°C',
            'roughness': 'units',
            'slope': 'degrees'
        }
        
        return unit_map.get(measurement_type, 'units')
    
    async def get_measurements_for_region(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        limit: int = 100
    ) -> list:
        """
        Obtener mediciones históricas para una región
        
        Útil para:
        - Análisis temporal
        - Validación de consistencia
        - Detección de cambios
        """
        
        try:
            query = """
                SELECT *
                FROM measurements
                WHERE latitude BETWEEN $1 AND $2
                  AND longitude BETWEEN $3 AND $4
                ORDER BY measurement_timestamp DESC
                LIMIT $5
            """
            
            results = await self.db.fetch(query, lat_min, lat_max, lon_min, lon_max, limit)
            
            return [dict(row) for row in results]
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo mediciones históricas: {e}")
            return []
    
    async def get_measurement_statistics(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de mediciones registradas
        
        Returns:
            Dict con estadísticas generales
        """
        
        try:
            query = """
                SELECT
                    COUNT(*) as total_measurements,
                    COUNT(DISTINCT instrument_name) as unique_instruments,
                    COUNT(DISTINCT DATE(measurement_timestamp)) as days_with_data,
                    COUNT(*) FILTER (WHERE anomaly_detected = true) as anomalies_detected,
                    COUNT(*) FILTER (WHERE data_mode = 'REAL') as real_data_count,
                    COUNT(*) FILTER (WHERE data_mode = 'DERIVED') as derived_data_count,
                    MIN(measurement_timestamp) as first_measurement,
                    MAX(measurement_timestamp) as last_measurement
                FROM measurements
            """
            
            result = await self.db.fetchrow(query)
            
            return dict(result) if result else {}
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas: {e}")
            return {}
