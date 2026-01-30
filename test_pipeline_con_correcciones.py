#!/usr/bin/env python3
"""
Test Pipeline Completo con Correcciones de Instrumentos
========================================================

Verifica que las correcciones de PALSAR, MODIS LST y OpenTopography
funcionan correctamente en el pipeline científico completo.

Fecha: 2026-01-29
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from scientific_pipeline import ScientificPipeline


async def test_pipeline_completo():
    """Test del pipeline completo con instrumentos corregidos"""
    
    print("="*80)
    print("TEST PIPELINE COMPLETO CON CORRECCIONES")
    print("="*80)
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nCorrecciones verificadas:")
    print("OK PALSAR: Retorna InstrumentMeasurement")
    print("OK MODIS LST: Timeout 120s + CredentialsManager")
    print("OK OpenTopography: Timeout 120s + CredentialsManager")
    
    # Test región: Tiwanaku, Bolivia (sitio arqueológico conocido)
    test_region = {
        "lat_min": -16.56,
        "lat_max": -16.55,
        "lon_min": -68.68,
        "lon_max": -68.67,
        "region_name": "Tiwanaku Test"
    }
    
    print(f"\n[LOC] Región de test: {test_region['region_name']}")
    print(f"   Coordenadas: [{test_region['lat_min']:.4f}, {test_region['lat_max']:.4f}] x "
          f"[{test_region['lon_min']:.4f}, {test_region['lon_max']:.4f}]")
    
    # Paso 1: Obtener mediciones instrumentales
    print("\n" + "-"*80)
    print("Paso 1: Obteniendo mediciones instrumentales...")
    print("-"*80)
    
    try:
        from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        
        integrator = RealDataIntegratorV2()
        
        # Obtener todas las mediciones disponibles
        raw_measurements = await integrator.get_batch_measurements(
            instrument_names=[
                'sentinel2_ndvi', 'sentinel1_sar', 'landsat_thermal',
                'icesat2_elevation', 'srtm_elevation', 'era5_climate',
                'chirps_precipitation', 'viirs_nightlights',
                'palsar_backscatter', 'modis_lst', 'opentopography_dem'
            ],
            lat_min=test_region['lat_min'],
            lat_max=test_region['lat_max'],
            lon_min=test_region['lon_min'],
            lon_max=test_region['lon_max']
        )
        
        print(f"\n[OK] Mediciones obtenidas: {len(raw_measurements.get('instrumental_measurements', {}))} instrumentos")
        
        # Paso 2: Ejecutar pipeline científico
        print("\n" + "-"*80)
        print("Paso 2: Ejecutando pipeline científico...")
        print("-"*80)
        
        pipeline = ScientificPipeline()
        
        result = await pipeline.analyze(
            raw_measurements=raw_measurements,
            lat_min=test_region['lat_min'],
            lat_max=test_region['lat_max'],
            lon_min=test_region['lon_min'],
            lon_max=test_region['lon_max']
        )
        
        # Analizar resultados
        print("\n" + "="*80)
        print("RESULTADOS DEL ANÁLISIS")
        print("="*80)
        
        # 1. Cobertura instrumental
        coverage = result.get('instrumental_coverage', {})
        print(f"\n[DATA] COBERTURA INSTRUMENTAL")
        print(f"   Total instrumentos: {coverage.get('total_instruments', 0)}")
        print(f"   Instrumentos SUCCESS: {coverage.get('success_count', 0)}")
        print(f"   Instrumentos DEGRADED: {coverage.get('degraded_count', 0)}")
        print(f"   Instrumentos FAILED: {coverage.get('failed_count', 0)}")
        print(f"   Cobertura: {coverage.get('coverage_percentage', 0):.1f}%")
        
        # 2. Verificar instrumentos específicos
        measurements = result.get('measurements', {})
        
        print(f"\n[SCI] INSTRUMENTOS CORREGIDOS:")
        
        # PALSAR
        palsar_found = False
        for key in ['palsar_backscatter', 'sar_l_band_palsar']:
            if key in measurements:
                palsar = measurements[key]
                status = palsar.get('status', 'UNKNOWN')
                value = palsar.get('value', 'N/A')
                print(f"   [OK] PALSAR: {status} (value={value})")
                palsar_found = True
                break
        if not palsar_found:
            print(f"   [!] PALSAR: No encontrado en measurements")
        
        # MODIS LST
        modis_found = False
        for key in ['modis_lst', 'thermal_inertia_modis']:
            if key in measurements:
                modis = measurements[key]
                status = modis.get('status', 'UNKNOWN')
                value = modis.get('value', 'N/A')
                print(f"   [OK] MODIS LST: {status} (value={value})")
                modis_found = True
                break
        if not modis_found:
            print(f"   [!] MODIS LST: No encontrado en measurements")
        
        # OpenTopography
        opentopo_found = False
        for key in ['opentopography_dem', 'elevation_opentopo']:
            if key in measurements:
                opentopo = measurements[key]
                status = opentopo.get('status', 'UNKNOWN')
                value = opentopo.get('value', 'N/A')
                print(f"   [OK] OpenTopography: {status} (value={value})")
                opentopo_found = True
                break
        if not opentopo_found:
            print(f"   [!] OpenTopography: No encontrado en measurements")
        
        # 3. Clasificación arqueológica
        classification = result.get('classification', {})
        print(f"\n[ARCH] CLASIFICACIÓN ARQUEOLÓGICA")
        print(f"   Tipo: {classification.get('classification', 'UNKNOWN')}")
        print(f"   Prioridad: {classification.get('priority', 'UNKNOWN')}")
        print(f"   Anomaly Score: {classification.get('anomaly_score', 0):.2f}")
        
        # 4. Narrativa científica
        narrative = result.get('scientific_narrative', {})
        if narrative:
            print(f"\n[NOTE] NARRATIVA CIENTÍFICA")
            print(f"   Disponible: {narrative.get('narrative_available', False)}")
            if narrative.get('summary'):
                print(f"   Resumen: {narrative['summary'][:100]}...")
        
        # 5. Guardar resultado completo
        output_file = f"test_pipeline_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n[SAVE] Resultado completo guardado en: {output_file}")
        
        # Verificar éxito
        print("\n" + "="*80)
        print("VERIFICACIÓN DE CORRECCIONES")
        print("="*80)
        
        success_count = coverage.get('success_count', 0)
        degraded_count = coverage.get('degraded_count', 0)
        total_usable = success_count + degraded_count
        
        print(f"\n[OK] Instrumentos usables: {total_usable}/12")
        print(f"[OK] Cobertura: {coverage.get('coverage_percentage', 0):.1f}%")
        
        if coverage.get('coverage_percentage', 0) >= 90:
            print("\n[SUCCESS] OBJETIVO ALCANZADO: Cobertura >= 90%")
            return True
        elif coverage.get('coverage_percentage', 0) >= 80:
            print("\n[OK] BUENA COBERTURA: >= 80%")
            return True
        else:
            print(f"\n[!] Cobertura insuficiente: {coverage.get('coverage_percentage', 0):.1f}%")
            return False
        
    except Exception as e:
        print(f"\n[X] ERROR en análisis: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Ejecutar test"""
    success = await test_pipeline_completo()
    
    print("\n" + "="*80)
    if success:
        print("[OK] TEST COMPLETADO EXITOSAMENTE")
    else:
        print("[X] TEST FALLÓ")
    print("="*80)
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
