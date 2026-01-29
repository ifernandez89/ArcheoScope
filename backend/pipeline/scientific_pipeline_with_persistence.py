#!/usr/bin/env python3
"""
Scientific Pipeline with Persistence - Pipeline con persistencia de mediciones
==============================================================================

INTEGRACIÓN DE LAS 3 PRIORIDADES:
1. ✅ Persistir mediciones crudas
2. ✅ Clasificar señales (OBSERVED/INFERRED/CONTEXTUAL)
3. ✅ Usar Copernicus DEM

Flujo:
1. Obtener mediciones instrumentales
2. Guardar en BD (measurements_repository)
3. Clasificar señales (signal_classification)
4. Calcular ESS con transparencia
5. Retornar resultado paper-ready
"""

import asyncio
import asyncpg
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging

# Importar componentes
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
from satellite_connectors.copernicus_dem_connector import CopernicusDEMConnector
from database.measurements_repository import MeasurementsRepository, instrument_measurement_to_dict
from signal_classification import (
    ArchaeologicalSignal,
    SignalType,
    classify_instrument_signal,
    calculate_ess_with_transparency,
    generate_evidence_report
)

logger = logging.getLogger(__name__)


class ScientificPipelineWithPersistence:
    """
    Pipeline científico con persistencia de mediciones.
    
    Características:
    - Guarda TODAS las mediciones crudas
    - Clasifica señales (OBSERVED/INFERRED/CONTEXTUAL)
    - Calcula ESS con transparencia total
    - Paper-ready
    """
    
    def __init__(self, db_pool: asyncpg.Pool):
        """
        Inicializar pipeline.
        
        Args:
            db_pool: Pool de conexiones PostgreSQL
        """
        self.integrator = RealDataIntegratorV2()
        self.copernicus_dem = CopernicusDEMConnector()
        self.measurements_repo = MeasurementsRepository(db_pool)
        
        logger.info("🔬 Scientific Pipeline with Persistence initialized")
    
    async def analyze_site(
        self,
        site_id: UUID,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        save_measurements: bool = True
    ) -> Dict[str, Any]:
        """
        Analizar sitio con persistencia de mediciones.
        
        Args:
            site_id: ID del sitio arqueológico
            lat_min, lat_max, lon_min, lon_max: Bounding box
            save_measurements: Guardar mediciones en BD
        
        Returns:
            Dict con análisis completo y transparencia total
        """
        
        logger.info(f"🔬 Analizando sitio {site_id}...")
        
        # 1. Obtener mediciones CORE
        core_instruments = [
            'sentinel_2_ndvi',
            'sentinel_1_sar',
            'landsat_thermal',
            'srtm_elevation',
            'era5_climate'
        ]
        
        logger.info(f"   📡 Obteniendo {len(core_instruments)} instrumentos CORE...")
        
        batch = await self.integrator.get_batch_measurements(
            core_instruments,
            lat_min, lat_max, lon_min, lon_max
        )
        
        # 2. Intentar Copernicus DEM (mejor que SRTM)
        logger.info("   🗻 Intentando Copernicus DEM...")
        copernicus_result = await self.copernicus_dem.get_elevation_data(
            lat_min, lat_max, lon_min, lon_max
        )
        
        # 3. Guardar mediciones en BD
        if save_measurements:
            logger.info("   💾 Guardando mediciones en BD...")
            
            measurements_to_save = []
            
            # Convertir batch results a formato BD
            for result in batch.results:
                if result.status.value in ['SUCCESS', 'DEGRADED']:
                    measurement_dict = instrument_measurement_to_dict(result)
                    measurements_to_save.append(measurement_dict)
            
            # Agregar Copernicus DEM si está disponible
            if copernicus_result:
                measurements_to_save.append({
                    'instrument_name': 'copernicus_dem',
                    'measurement_type': 'elevation',
                    'value': copernicus_result['value'],
                    'unit': 'meters',
                    'confidence': 0.95,  # Copernicus es alta confianza
                    'quality_flags': {
                        'dem_status': copernicus_result['dem_status'],
                        'resolution_m': copernicus_result['resolution_m'],
                        'pixel_count': copernicus_result['pixel_count']
                    },
                    'raw_measurements': copernicus_result['elevation_stats'],
                    'acquisition_date': None,
                    'source': copernicus_result['source'],
                    'processing_notes': copernicus_result['processing_notes']
                })
            
            # Guardar batch
            if measurements_to_save:
                await self.measurements_repo.save_batch_measurements(
                    site_id, measurements_to_save
                )
                logger.info(f"   ✅ {len(measurements_to_save)} mediciones guardadas")
        
        # 4. Clasificar señales
        logger.info("   🏷️ Clasificando señales...")
        
        signals = []
        
        for result in batch.results:
            if result.status.value in ['SUCCESS', 'DEGRADED']:
                # Clasificar tipo de señal
                signal_type = classify_instrument_signal(result.instrument_name)
                
                # Crear señal
                signal = ArchaeologicalSignal.from_instrument_measurement(
                    result, signal_type
                )
                signals.append(signal)
        
        # Agregar Copernicus DEM como señal
        if copernicus_result:
            from signal_classification import EvidenceStrength
            signals.append(ArchaeologicalSignal(
                signal_type=SignalType.OBSERVED,
                instrument='copernicus_dem',
                value=copernicus_result['value'] / 1000.0,  # Normalizar a [0-1]
                confidence=0.95,
                evidence_strength=EvidenceStrength.STRONG,
                description=f"High-res DEM from {copernicus_result['source']}"
            ))
        
        # 5. Calcular ESS con transparencia
        logger.info("   📊 Calculando ESS con transparencia...")
        
        ess_result = calculate_ess_with_transparency(signals)
        
        # 6. Generar reporte de evidencia
        evidence_report = generate_evidence_report(signals)
        
        # 7. Resultado final
        result = {
            'site_id': str(site_id),
            'bbox': {
                'lat_min': lat_min,
                'lat_max': lat_max,
                'lon_min': lon_min,
                'lon_max': lon_max
            },
            'ess_analysis': ess_result,
            'evidence_report': evidence_report,
            'measurements': {
                'total': len(signals),
                'observed': len([s for s in signals if s.signal_type == SignalType.OBSERVED]),
                'inferred': len([s for s in signals if s.signal_type == SignalType.INFERRED]),
                'contextual': len([s for s in signals if s.signal_type == SignalType.CONTEXTUAL])
            },
            'coverage': {
                'score': batch.generate_report()['coverage_score'],
                'usable_instruments': batch.generate_report()['usable_instruments']
            },
            'dem_source': copernicus_result['source'] if copernicus_result else 'SRTM_fallback',
            'measurements_saved': save_measurements,
            'paper_ready': ess_result['paper_ready']
        }
        
        logger.info(f"   ✅ Análisis completado: ESS={ess_result['ess_score']:.3f}, Paper-ready={ess_result['paper_ready']}")
        
        return result


async def example_usage():
    """Ejemplo de uso del pipeline."""
    
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
    
    # Crear pipeline
    pipeline = ScientificPipelineWithPersistence(db_pool)
    
    # Analizar sitio (Giza, Egipto)
    site_id = UUID('00000000-0000-0000-0000-000000000001')
    
    result = await pipeline.analyze_site(
        site_id=site_id,
        lat_min=29.95,
        lat_max=30.05,
        lon_min=31.10,
        lon_max=31.20,
        save_measurements=True
    )
    
    print("="*80)
    print("RESULTADO DEL ANÁLISIS")
    print("="*80)
    print(f"\nESS Score: {result['ess_analysis']['ess_score']}")
    print(f"Interpretation: {result['ess_analysis']['interpretation']}")
    print(f"Paper-ready: {result['paper_ready']}")
    print(f"\nBreakdown:")
    print(f"  Base score: {result['ess_analysis']['breakdown']['base_score']}")
    print(f"  Inference boost: {result['ess_analysis']['breakdown']['inference_boost']}")
    print(f"  Context adjustment: {result['ess_analysis']['breakdown']['context_adjustment']}")
    print(f"\nMeasurements:")
    print(f"  Observed: {result['measurements']['observed']}")
    print(f"  Inferred: {result['measurements']['inferred']}")
    print(f"  Contextual: {result['measurements']['contextual']}")
    print(f"\nDEM Source: {result['dem_source']}")
    print(f"\n{result['evidence_report']}")
    print("="*80)
    
    await db_pool.close()


if __name__ == "__main__":
    asyncio.run(example_usage())
