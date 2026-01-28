#!/usr/bin/env python3
"""
Test del sistema de registro de mediciones
"""

import asyncio
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
import asyncpg

load_dotenv()

from database.measurements_logger import MeasurementsLogger

async def test_measurements_logger():
    """Test completo del logger de mediciones"""
    
    print("="*70)
    print("TEST MEASUREMENTS LOGGER")
    print("="*70)
    print()
    
    # Conectar a BD
    database_url = os.getenv("DATABASE_URL")
    conn = await asyncpg.connect(database_url)
    
    # Inicializar logger
    logger = MeasurementsLogger(conn)
    
    print("Logger inicializado")
    print()
    
    # Test 1: Registrar medición de Sentinel-2
    print("Test 1: Registrando medición de Sentinel-2 NDVI...")
    measurement_id = await logger.log_measurement(
        instrument_name="sentinel_2_ndvi",
        measurement_type="ndvi",
        value=0.75,
        unit="NDVI",
        latitude=17.22,
        longitude=-89.62,
        lat_min=17.20,
        lat_max=17.25,
        lon_min=-89.65,
        lon_max=-89.60,
        region_name="Tikal, Guatemala",
        source="Sentinel-2 (Copernicus)",
        data_mode="REAL",
        confidence=0.95,
        acquisition_date="2024-01-15T10:30:00Z",
        resolution_m=10,
        environment_type="forest",
        environment_confidence=0.92,
        threshold=0.6,
        exceeds_threshold=True,
        anomaly_detected=True
    )
    
    if measurement_id:
        print(f"  EXITO: Medicion registrada con ID: {measurement_id}")
    else:
        print("  ERROR: No se pudo registrar")
        return False
    
    print()
    
    # Test 2: Registrar medición de OpenTopography
    print("Test 2: Registrando medición de OpenTopography...")
    measurement_id2 = await logger.log_measurement(
        instrument_name="opentopography",
        measurement_type="elevation",
        value=271.2,
        unit="m",
        latitude=17.22,
        longitude=-89.62,
        lat_min=17.20,
        lat_max=17.25,
        lon_min=-89.65,
        lon_max=-89.60,
        region_name="Tikal, Guatemala",
        source="OpenTopography SRTMGL1",
        data_mode="REAL",
        confidence=0.95,
        resolution_m=30,
        environment_type="forest",
        threshold=None,
        exceeds_threshold=False,
        anomaly_detected=False,
        additional_data={
            "elevation_min": 226.0,
            "elevation_max": 334.0,
            "roughness": 1.553,
            "archaeological_score": 0.039,
            "platforms_detected": 0,
            "mounds_detected": 3,
            "terraces_detected": 9
        }
    )
    
    if measurement_id2:
        print(f"  EXITO: Medicion registrada con ID: {measurement_id2}")
    else:
        print("  ERROR: No se pudo registrar")
        return False
    
    print()
    
    # Test 3: Registrar desde diccionario (formato RealDataIntegrator)
    print("Test 3: Registrando desde diccionario...")
    measurement_data = {
        'value': 285.5,
        'source': 'ICESat-2 (NASA)',
        'confidence': 0.88,
        'acquisition_date': '2024-01-20T14:00:00Z'
    }
    
    measurement_id3 = await logger.log_measurement_from_dict(
        measurement_data=measurement_data,
        latitude=17.22,
        longitude=-89.62,
        instrument_name="icesat2",
        measurement_type="elevation",
        lat_min=17.20,
        lat_max=17.25,
        lon_min=-89.65,
        lon_max=-89.60,
        region_name="Tikal, Guatemala",
        environment_type="forest",
        environment_confidence=0.92
    )
    
    if measurement_id3:
        print(f"  EXITO: Medicion registrada con ID: {measurement_id3}")
    else:
        print("  ERROR: No se pudo registrar")
        return False
    
    print()
    
    # Test 4: Obtener mediciones históricas
    print("Test 4: Obteniendo mediciones historicas para la region...")
    measurements = await logger.get_measurements_for_region(
        lat_min=17.15,
        lat_max=17.30,
        lon_min=-89.70,
        lon_max=-89.55,
        limit=10
    )
    
    print(f"  Mediciones encontradas: {len(measurements)}")
    for m in measurements[:3]:
        print(f"    - {m['instrument_name']}: {m['value']} {m['unit']} ({m['data_mode']})")
    
    print()
    
    # Test 5: Estadísticas
    print("Test 5: Obteniendo estadisticas...")
    stats = await logger.get_measurement_statistics()
    
    print(f"  Total mediciones: {stats.get('total_measurements', 0)}")
    print(f"  Instrumentos unicos: {stats.get('unique_instruments', 0)}")
    print(f"  Dias con datos: {stats.get('days_with_data', 0)}")
    print(f"  Anomalias detectadas: {stats.get('anomalies_detected', 0)}")
    print(f"  Datos REALES: {stats.get('real_data_count', 0)}")
    print(f"  Datos DERIVADOS: {stats.get('derived_data_count', 0)}")
    
    await conn.close()
    
    print()
    print("="*70)
    print("TODOS LOS TESTS EXITOSOS")
    print("="*70)
    print()
    print("Sistema de registro de mediciones funcionando correctamente")
    print("CADA medicion instrumental sera registrada en la BD")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_measurements_logger())
    exit(0 if success else 1)
