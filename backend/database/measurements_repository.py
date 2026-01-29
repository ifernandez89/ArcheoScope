#!/usr/bin/env python3
"""
Measurements Repository - Persistencia de mediciones instrumentales
===================================================================

PRIORIDAD 1: Guardar TODAS las mediciones crudas.

Propósito:
- Persistir evidencia instrumental (no solo scores)
- Permitir re-análisis sin re-procesar
- Transparencia científica total
"""

import asyncpg
import json
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MeasurementsRepository:
    """Repositorio para mediciones instrumentales."""
    
    def __init__(self, db_pool: asyncpg.Pool):
        """
        Inicializar repositorio.
        
        Args:
            db_pool: Pool de conexiones PostgreSQL
        """
        self.db = db_pool
    
    async def save_measurement(
        self,
        site_id: UUID,
        instrument_name: str,
        measurement_type: str,
        value: float,
        unit: str,
        confidence: float,
        quality_flags: Dict[str, Any],
        raw_measurements: Dict[str, Any],
        acquisition_date: Optional[datetime] = None,
        source: Optional[str] = None,
        processing_notes: Optional[str] = None
    ) -> UUID:
        """
        Guardar medición instrumental cruda.
        
        Args:
            site_id: ID del sitio arqueológico
            instrument_name: Nombre del instrumento (sentinel_2_ndvi, etc.)
            measurement_type: Tipo de medición (vegetation, thermal, etc.)
            value: Valor principal
            unit: Unidad (NDVI, K, dB, m, etc.)
            confidence: Confianza [0-1]
            quality_flags: Flags de calidad (cloud_cover, pixel_count, etc.)
            raw_measurements: Mediciones detalladas (mean, std, min, max, etc.)
            acquisition_date: Fecha de adquisición del dato
            source: Fuente (Sentinel-2 L2A, Landsat 8 TIRS, etc.)
            processing_notes: Notas de procesamiento
        
        Returns:
            UUID de la medición guardada
        """
        
        query = """
        INSERT INTO instrument_measurements (
            site_id, instrument_name, measurement_type,
            value, unit, confidence, quality_flags, raw_measurements,
            acquisition_date, source, processing_notes
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        RETURNING id
        """
        
        try:
            measurement_id = await self.db.fetchval(
                query,
                site_id,
                instrument_name,
                measurement_type,
                value,
                unit,
                confidence,
                json.dumps(quality_flags),
                json.dumps(raw_measurements),
                acquisition_date,
                source,
                processing_notes
            )
            
            logger.info(f"✅ Medición guardada: {instrument_name} para sitio {site_id}")
            return measurement_id
            
        except Exception as e:
            logger.error(f"❌ Error guardando medición: {e}")
            raise
    
    async def save_batch_measurements(
        self,
        site_id: UUID,
        measurements: List[Dict[str, Any]]
    ) -> List[UUID]:
        """
        Guardar múltiples mediciones en batch.
        
        Args:
            site_id: ID del sitio
            measurements: Lista de mediciones
        
        Returns:
            Lista de UUIDs guardados
        """
        
        measurement_ids = []
        
        async with self.db.acquire() as conn:
            async with conn.transaction():
                for measurement in measurements:
                    measurement_id = await self.save_measurement(
                        site_id=site_id,
                        instrument_name=measurement['instrument_name'],
                        measurement_type=measurement['measurement_type'],
                        value=measurement['value'],
                        unit=measurement['unit'],
                        confidence=measurement['confidence'],
                        quality_flags=measurement.get('quality_flags', {}),
                        raw_measurements=measurement.get('raw_measurements', {}),
                        acquisition_date=measurement.get('acquisition_date'),
                        source=measurement.get('source'),
                        processing_notes=measurement.get('processing_notes')
                    )
                    measurement_ids.append(measurement_id)
        
        logger.info(f"✅ Batch guardado: {len(measurement_ids)} mediciones para sitio {site_id}")
        return measurement_ids
    
    async def get_site_measurements(
        self,
        site_id: UUID,
        instrument_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtener todas las mediciones de un sitio.
        
        Args:
            site_id: ID del sitio
            instrument_name: Filtrar por instrumento (opcional)
        
        Returns:
            Lista de mediciones
        """
        
        if instrument_name:
            query = """
            SELECT * FROM instrument_measurements
            WHERE site_id = $1 AND instrument_name = $2
            ORDER BY acquisition_date DESC, created_at DESC
            """
            rows = await self.db.fetch(query, site_id, instrument_name)
        else:
            query = """
            SELECT * FROM instrument_measurements
            WHERE site_id = $1
            ORDER BY acquisition_date DESC, created_at DESC
            """
            rows = await self.db.fetch(query, site_id)
        
        return [dict(row) for row in rows]
    
    async def get_measurement_summary(self, site_id: UUID) -> Dict[str, Any]:
        """
        Obtener resumen de mediciones de un sitio.
        
        Args:
            site_id: ID del sitio
        
        Returns:
            Resumen con conteo por instrumento y calidad promedio
        """
        
        query = """
        SELECT 
            instrument_name,
            COUNT(*) as measurement_count,
            AVG(confidence) as avg_confidence,
            MAX(acquisition_date) as latest_acquisition
        FROM instrument_measurements
        WHERE site_id = $1
        GROUP BY instrument_name
        ORDER BY measurement_count DESC
        """
        
        rows = await self.db.fetch(query, site_id)
        
        summary = {
            'total_measurements': sum(row['measurement_count'] for row in rows),
            'instruments': {}
        }
        
        for row in rows:
            summary['instruments'][row['instrument_name']] = {
                'count': row['measurement_count'],
                'avg_confidence': float(row['avg_confidence']),
                'latest_acquisition': row['latest_acquisition'].isoformat() if row['latest_acquisition'] else None
            }
        
        return summary
    
    async def delete_site_measurements(self, site_id: UUID) -> int:
        """
        Eliminar todas las mediciones de un sitio.
        
        Args:
            site_id: ID del sitio
        
        Returns:
            Número de mediciones eliminadas
        """
        
        query = "DELETE FROM instrument_measurements WHERE site_id = $1"
        result = await self.db.execute(query, site_id)
        
        # Extraer número de filas eliminadas
        deleted_count = int(result.split()[-1])
        logger.info(f"🗑️ Eliminadas {deleted_count} mediciones del sitio {site_id}")
        
        return deleted_count


# Función helper para convertir InstrumentMeasurement a dict
def instrument_measurement_to_dict(measurement) -> Dict[str, Any]:
    """
    Convertir InstrumentMeasurement a dict para guardar en BD.
    
    Args:
        measurement: InstrumentMeasurement object
    
    Returns:
        Dict con estructura para MeasurementsRepository
    """
    
    return {
        'instrument_name': measurement.instrument_name,
        'measurement_type': measurement.measurement_type,
        'value': measurement.value,
        'unit': measurement.unit,
        'confidence': measurement.confidence,
        'quality_flags': measurement.quality_flags or {},
        'raw_measurements': {
            'value': measurement.value,
            'unit': measurement.unit,
            'status': measurement.status.value if hasattr(measurement, 'status') else 'unknown'
        },
        'acquisition_date': datetime.fromisoformat(measurement.acquisition_date) if measurement.acquisition_date else None,
        'source': measurement.source,
        'processing_notes': measurement.processing_notes
    }


if __name__ == "__main__":
    # Test básico
    import asyncio
    
    async def test_repository():
        """Test del repositorio."""
        
        # USAR VARIABLES DE ENTORNO
        import os
        db_password = os.getenv("POSTGRES_PASSWORD", "postgres")
        
        # Conectar a BD
        db_pool = await asyncpg.create_pool(
            host="localhost",
            port=5433,
            database="archeoscope",
            user="postgres",
            password=db_password
        )
        
        repo = MeasurementsRepository(db_pool)
        
        # Test: Guardar medición
        site_id = UUID('00000000-0000-0000-0000-000000000001')  # UUID de prueba
        
        measurement_id = await repo.save_measurement(
            site_id=site_id,
            instrument_name='sentinel_2_ndvi',
            measurement_type='vegetation',
            value=0.45,
            unit='NDVI',
            confidence=0.95,
            quality_flags={'cloud_cover': 5.2, 'pixel_count': 1024},
            raw_measurements={
                'ndvi_mean': 0.45,
                'ndvi_std': 0.12,
                'ndvi_min': 0.15,
                'ndvi_max': 0.75
            },
            source='Sentinel-2 L2A',
            processing_notes='Test measurement'
        )
        
        print(f"✅ Medición guardada: {measurement_id}")
        
        # Test: Obtener mediciones
        measurements = await repo.get_site_measurements(site_id)
        print(f"📊 Mediciones encontradas: {len(measurements)}")
        
        # Test: Resumen
        summary = await repo.get_measurement_summary(site_id)
        print(f"📈 Resumen: {summary}")
        
        await db_pool.close()
    
    asyncio.run(test_repository())
