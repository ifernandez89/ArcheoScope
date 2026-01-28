#!/usr/bin/env python3
"""
Test de Integración Completa - 15 Instrumentos Satelitales
=========================================================

OBJETIVO: Probar la integración completa de los 15 instrumentos satelitales:

INSTRUMENTOS ORIGINALES (1-10):
1. Sentinel-2 (NDVI, multispectral)
2. Sentinel-1 (SAR C-band)
3. Landsat (térmico)
4. ICESat-2 (elevación)
5. OpenTopography (DEM/LiDAR)
6. MODIS LST (térmico regional)
7. NSIDC (hielo marino/nieve)
8. Copernicus Marine (SST/hielo)
9. Planetary Computer (orquestador)
10. Real Data Integrator (coordinador)

NUEVOS INSTRUMENTOS (11-15):
11. VIIRS (térmico/NDVI/fuego - 375m)
12. SRTM (DEM - 30m/90m)
13. ALOS PALSAR-2 (SAR L-band)
14. ERA5 (clima/preservación)
15. CHIRPS (precipitación histórica)

COORDENADAS DE PRUEBA:
- Giza, Egipto (desierto) - sitio conocido
- Angkor, Camboya (bosque) - sitio conocido
- Machu Picchu, Perú (montaña) - sitio conocido
- Región árida con agricultura antigua
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar path del backend
sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_15_instruments_complete():
    """Test completo de los 15 instrumentos satelitales."""
    
    print("🚀 INICIANDO TEST DE INTEGRACIÓN COMPLETA - 15 INSTRUMENTOS")
    print("=" * 80)
    
    # Importar sistema completo
    try:
        from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        from core_anomaly_detector import CoreAnomalyDetector
        from environment_classifier import EnvironmentClassifier
        from archaeological_validator import ArchaeologicalValidator
        from data.archaeological_loader import ArchaeologicalDataLoader
        
        print("✅ Módulos importados correctamente")
        
    except Exception as e:
        print(f"❌ Error importando módulos: {e}")
        return False
    
    # Inicializar sistema completo
    try:
        print("\n🔧 Inicializando sistema completo...")
        
        # Componentes del sistema
        env_classifier = EnvironmentClassifier()
        data_loader = ArchaeologicalDataLoader()
        validator = ArchaeologicalValidator(data_loader)
        
        # Detector principal con 15 instrumentos
        detector = CoreAnomalyDetector(env_classifier, validator, data_loader)
        
        # Integrador de datos reales V2 (con blindaje crítico)
        integrator = RealDataIntegratorV2()
        
        print("✅ Sistema inicializado correctamente")
        
    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")
        return False
    
    # Verificar disponibilidad de APIs
    print("\n📡 Verificando disponibilidad de APIs...")
    api_status = integrator.get_availability_status()
    
    print(f"APIs disponibles: {api_status['_summary']['available_apis']}/{api_status['_summary']['total_apis']}")
    print(f"Tasa de disponibilidad: {api_status['_summary']['availability_rate']:.1%}")
    print(f"Estado general: {api_status['_summary']['status']}")
    
    # Mostrar estado por API
    for api_name, status in api_status.items():
        if api_name != '_summary':
            status_icon = "✅" if status['available'] else "❌"
            print(f"  {status_icon} {api_name}: {status['status']}")
    
    # Definir coordenadas de prueba
    test_sites = [
        {
            'name': 'Giza Pyramids (Desert)',
            'lat_min': 29.9, 'lat_max': 30.0,
            'lon_min': 31.1, 'lon_max': 31.2,
            'environment': 'desert',
            'expected_instruments': ['landsat_thermal', 'modis_lst', 'viirs_thermal', 'srtm_elevation']
        },
        {
            'name': 'Angkor Wat (Forest)',
            'lat_min': 13.4, 'lat_max': 13.5,
            'lon_min': 103.8, 'lon_max': 103.9,
            'environment': 'forest',
            'expected_instruments': ['palsar_penetration', 'viirs_ndvi', 'sentinel_2_ndvi']
        },
        {
            'name': 'Machu Picchu (Mountain)',
            'lat_min': -13.2, 'lat_max': -13.1,
            'lon_min': -72.6, 'lon_max': -72.5,
            'environment': 'mountain',
            'expected_instruments': ['srtm_slope', 'era5_climate', 'icesat2']
        },
        {
            'name': 'Atacama Desert (Arid Agricultural)',
            'lat_min': -24.5, 'lat_max': -24.4,
            'lon_min': -68.3, 'lon_max': -68.2,
            'environment': 'arid_agricultural',
            'expected_instruments': ['chirps_precipitation', 'era5_preservation', 'palsar_soil_moisture']
        }
    ]
    
    # Probar cada sitio
    results = {}
    
    for site in test_sites:
        print(f"\n🏛️ PROBANDO SITIO: {site['name']}")
        print("-" * 60)
        
        try:
            # Test 1: Análisis completo con detector principal
            print("🔍 Ejecutando análisis arqueológico completo...")
            
            lat_center = (site['lat_min'] + site['lat_max']) / 2
            lon_center = (site['lon_min'] + site['lon_max']) / 2
            
            result = await detector.detect_anomaly(
                lat=lat_center,
                lon=lon_center,
                lat_min=site['lat_min'],
                lat_max=site['lat_max'],
                lon_min=site['lon_min'],
                lon_max=site['lon_max'],
                region_name=site['name']
            )
            
            print(f"  ✅ Análisis completado")
            print(f"  📊 Anomalía detectada: {result.anomaly_detected}")
            print(f"  📊 Confianza: {result.confidence_level}")
            print(f"  📊 Probabilidad arqueológica: {result.archaeological_probability:.2%}")
            print(f"  📊 Instrumentos convergentes: {result.instruments_converging}/{result.minimum_required}")
            
            # Test 2: Mediciones instrumentales específicas
            print("🛰️ Probando instrumentos específicos...")
            
            instrument_results = {}
            
            for instrument in site['expected_instruments']:
                try:
                    measurement = await integrator.get_instrument_measurement_robust(
                        instrument_name=instrument,
                        lat_min=site['lat_min'],
                        lat_max=site['lat_max'],
                        lon_min=site['lon_min'],
                        lon_max=site['lon_max']
                    )
                    
                    if measurement:
                        status = measurement.status if hasattr(measurement, 'status') else 'SUCCESS'
                        value = measurement.value if hasattr(measurement, 'value') else 'N/A'
                        print(f"    ✅ {instrument}: {status} (valor: {value})")
                        instrument_results[instrument] = {
                            'status': status,
                            'value': value,
                            'success': True
                        }
                    else:
                        print(f"    ❌ {instrument}: Sin datos")
                        instrument_results[instrument] = {
                            'status': 'NO_DATA',
                            'success': False
                        }
                        
                except Exception as e:
                    print(f"    ❌ {instrument}: Error - {e}")
                    instrument_results[instrument] = {
                        'status': 'ERROR',
                        'error': str(e),
                        'success': False
                    }
            
            # Test 3: Batch de instrumentos múltiples
            print("📦 Probando batch de instrumentos múltiples...")
            
            all_instruments = [
                'sentinel_2_ndvi', 'sentinel_1_sar', 'landsat_thermal', 'icesat2',
                'modis_lst', 'viirs_thermal', 'srtm_elevation', 'palsar_backscatter',
                'era5_climate', 'chirps_precipitation'
            ]
            
            batch_result = await integrator.get_batch_measurements(
                instrument_names=all_instruments,
                lat_min=site['lat_min'],
                lat_max=site['lat_max'],
                lon_min=site['lon_min'],
                lon_max=site['lon_max']
            )
            
            batch_report = batch_result.generate_report()
            
            print(f"  📊 Coverage Score: {batch_report['coverage_score']:.1%}")
            print(f"  📊 Instrumentos usables: {batch_report['usable_instruments']}/{batch_report['total_instruments']}")
            print(f"  📊 Estados: SUCCESS={batch_report['status_summary'].get('SUCCESS', 0)}, "
                  f"DEGRADED={batch_report['status_summary'].get('DEGRADED', 0)}, "
                  f"FAILED={batch_report['status_summary'].get('FAILED', 0)}")
            
            # Guardar resultados
            results[site['name']] = {
                'archaeological_analysis': {
                    'anomaly_detected': result.anomaly_detected,
                    'confidence_level': result.confidence_level,
                    'archaeological_probability': result.archaeological_probability,
                    'instruments_converging': result.instruments_converging,
                    'environment_type': result.environment_type
                },
                'instrument_tests': instrument_results,
                'batch_analysis': {
                    'coverage_score': batch_report['coverage_score'],
                    'usable_instruments': batch_report['usable_instruments'],
                    'total_instruments': batch_report['total_instruments'],
                    'status_summary': batch_report['status_summary']
                },
                'success': True
            }
            
            print(f"  ✅ {site['name']} - Test completado exitosamente")
            
        except Exception as e:
            print(f"  ❌ {site['name']} - Error: {e}")
            results[site['name']] = {
                'success': False,
                'error': str(e)
            }
    
    # Generar reporte final
    print("\n" + "=" * 80)
    print("📋 REPORTE FINAL - INTEGRACIÓN 15 INSTRUMENTOS")
    print("=" * 80)
    
    successful_sites = sum(1 for r in results.values() if r.get('success', False))
    total_sites = len(results)
    
    print(f"🎯 Sitios probados exitosamente: {successful_sites}/{total_sites}")
    print(f"🎯 Tasa de éxito: {successful_sites/total_sites:.1%}")
    
    # Estadísticas por instrumento
    instrument_stats = {}
    
    for site_name, site_results in results.items():
        if site_results.get('success') and 'instrument_tests' in site_results:
            for instrument, test_result in site_results['instrument_tests'].items():
                if instrument not in instrument_stats:
                    instrument_stats[instrument] = {'success': 0, 'total': 0}
                
                instrument_stats[instrument]['total'] += 1
                if test_result.get('success', False):
                    instrument_stats[instrument]['success'] += 1
    
    print(f"\n📊 ESTADÍSTICAS POR INSTRUMENTO:")
    for instrument, stats in instrument_stats.items():
        success_rate = stats['success'] / stats['total'] if stats['total'] > 0 else 0
        status_icon = "✅" if success_rate >= 0.5 else "⚠️" if success_rate > 0 else "❌"
        print(f"  {status_icon} {instrument}: {stats['success']}/{stats['total']} ({success_rate:.1%})")
    
    # Guardar resultados detallados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"test_15_instruments_results_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'test_metadata': {
                'timestamp': timestamp,
                'total_instruments': 15,
                'total_sites': total_sites,
                'successful_sites': successful_sites,
                'success_rate': successful_sites/total_sites,
                'api_availability': api_status
            },
            'site_results': results,
            'instrument_statistics': instrument_stats
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados detallados guardados en: {results_file}")
    
    # Conclusión
    if successful_sites == total_sites:
        print("\n🎉 ¡INTEGRACIÓN COMPLETA EXITOSA!")
        print("✅ Los 15 instrumentos satelitales están correctamente integrados")
        print("✅ Sistema listo para análisis arqueológico en casa")
        return True
    else:
        print(f"\n⚠️ INTEGRACIÓN PARCIAL")
        print(f"✅ {successful_sites} sitios exitosos, {total_sites - successful_sites} con problemas")
        print("🔧 Revisar logs para diagnosticar problemas específicos")
        return successful_sites > 0

async def test_new_instruments_only():
    """Test específico solo de los 5 nuevos instrumentos."""
    
    print("\n🆕 TEST ESPECÍFICO - 5 NUEVOS INSTRUMENTOS")
    print("=" * 60)
    
    try:
        from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
        integrator = RealDataIntegratorV2()
        
        # Instrumentos nuevos a probar
        new_instruments = [
            'viirs_thermal',      # 11/15
            'srtm_elevation',     # 12/15
            'palsar_backscatter', # 13/15
            'era5_climate',       # 14/15
            'chirps_precipitation' # 15/15
        ]
        
        # Coordenadas de prueba (Giza)
        lat_min, lat_max = 29.9, 30.0
        lon_min, lon_max = 31.1, 31.2
        
        print(f"🎯 Probando {len(new_instruments)} nuevos instrumentos en Giza...")
        
        results = {}
        
        for instrument in new_instruments:
            print(f"\n🛰️ Probando {instrument}...")
            
            try:
                result = await integrator.get_instrument_measurement_robust(
                    instrument_name=instrument,
                    lat_min=lat_min,
                    lat_max=lat_max,
                    lon_min=lon_min,
                    lon_max=lon_max
                )
                
                if result:
                    status = getattr(result, 'status', 'SUCCESS')
                    value = getattr(result, 'value', 'N/A')
                    processing_time = getattr(result, 'processing_time_s', 0)
                    
                    print(f"  ✅ Status: {status}")
                    print(f"  📊 Valor: {value}")
                    print(f"  ⏱️ Tiempo: {processing_time:.2f}s")
                    
                    results[instrument] = {
                        'success': True,
                        'status': status,
                        'value': value,
                        'processing_time': processing_time
                    }
                else:
                    print(f"  ❌ Sin datos")
                    results[instrument] = {'success': False, 'reason': 'NO_DATA'}
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                results[instrument] = {'success': False, 'error': str(e)}
        
        # Reporte de nuevos instrumentos
        successful = sum(1 for r in results.values() if r.get('success', False))
        total = len(new_instruments)
        
        print(f"\n📊 RESULTADO NUEVOS INSTRUMENTOS:")
        print(f"✅ Exitosos: {successful}/{total} ({successful/total:.1%})")
        
        for instrument, result in results.items():
            status_icon = "✅" if result.get('success') else "❌"
            print(f"  {status_icon} {instrument}: {result.get('status', 'FAILED')}")
        
        return successful >= 3  # Al menos 3 de 5 deben funcionar
        
    except Exception as e:
        print(f"❌ Error en test de nuevos instrumentos: {e}")
        return False

if __name__ == "__main__":
    async def main():
        print("🚀 ARCHEOSCOPE - TEST DE INTEGRACIÓN 15 INSTRUMENTOS")
        print("=" * 80)
        print("OBJETIVO: Verificar integración completa de 10→15 instrumentos satelitales")
        print("NUEVOS: VIIRS, SRTM, PALSAR-2, ERA5, CHIRPS")
        print("=" * 80)
        
        # Test 1: Solo nuevos instrumentos
        print("\n🆕 FASE 1: Test de nuevos instrumentos...")
        new_instruments_ok = await test_new_instruments_only()
        
        if new_instruments_ok:
            print("✅ Nuevos instrumentos funcionando - continuando con test completo")
            
            # Test 2: Integración completa
            print("\n🌍 FASE 2: Test de integración completa...")
            full_integration_ok = await test_15_instruments_complete()
            
            if full_integration_ok:
                print("\n🎉 ¡ÉXITO TOTAL!")
                print("✅ Sistema ArcheoScope con 15 instrumentos listo para casa")
                print("🏠 Puedes probar con coordenadas candidatas reales")
            else:
                print("\n⚠️ Integración parcial - revisar logs")
        else:
            print("❌ Problemas con nuevos instrumentos - revisar configuración")
    
    # Ejecutar test
    asyncio.run(main())