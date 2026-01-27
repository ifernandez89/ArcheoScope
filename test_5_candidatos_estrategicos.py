#!/usr/bin/env python3
"""
Test de 5 Candidatos Estratégicos ArcheoScope
============================================

Captura datos de 5 candidatos de alto valor científico:
1. Groenlandia - márgenes glaciares retraídos (HIELO)
2. Amazonia occidental - selva densa (SELVA) 
3. Desierto de Arabia - Rub' al Khali (DESIERTO)
4. Patagonia austral - estepas + glaciares (MONTAÑA/ESTEPA)
5. Plataforma continental - Mar del Norte (MARINO)

OBJETIVO: Capturar datos instrumentales para análisis posterior en casa
NO guardar en BD ahora - solo JSON para análisis offline
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

try:
    from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
    from data_sanitizer import sanitize_response
    INTEGRATOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Integrator not available: {e}")
    INTEGRATOR_AVAILABLE = False

# Configurar logging
log_filename = f'test_5_candidatos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 5 CANDIDATOS ESTRATÉGICOS DE ALTO VALOR CIENTÍFICO
CANDIDATOS_ESTRATEGICOS = {
    "groenlandia_glaciar": {
        "name": "Groenlandia - Márgenes Glaciares Retraídos",
        "terrain": "polar_ice",
        "lat_min": 72.58, "lat_max": 72.59,
        "lon_min": -38.46, "lon_max": -38.45,
        "country": "Greenland",
        "scientific_value": "ALTÍSIMO",
        "description": "Retroceso glaciar acelerado → superficies nuevas expuestas",
        "target_features": ["alineamientos lineales", "terrazas costeras antiguas", "estructuras fuera del hielo"],
        "advantages": ["bajo ruido moderno", "excavación puntual viable", "series NSIDC desde 1970s"],
        "instruments": ["icesat2", "nsidc_sea_ice", "sar_backscatter", "modis_lst"]
    },
    
    "amazonia_occidental": {
        "name": "Amazonia Occidental - Selva Densa",
        "terrain": "forest",
        "lat_min": -8.12, "lat_max": -8.11,
        "lon_min": -74.02, "lon_max": -74.01,
        "country": "Peru/Brazil",
        "scientific_value": "ALTO",
        "description": "LiDAR fragmentado, análisis sistemático pendiente",
        "target_features": ["patrones geométricos persistentes", "caminos elevados", "manejo hidráulico antiguo"],
        "advantages": ["excavación digital vs física", "NDVI + SAR + humedad", "poco análisis integrado"],
        "instruments": ["sentinel_2_ndvi", "sar_backscatter", "icesat2", "modis_lst"]
    },
    
    "desierto_arabia": {
        "name": "Desierto de Arabia - Rub' al Khali",
        "terrain": "desert",
        "lat_min": 21.50, "lat_max": 21.51,
        "lon_min": 51.00, "lon_max": 51.01,
        "country": "Saudi Arabia",
        "scientific_value": "ALTO",
        "description": "Cambios climáticos pasados documentados, infraestructura mínima",
        "target_features": ["paleocauces", "asentamientos efímeros", "nodos logísticos antiguos"],
        "advantages": ["SAR + térmico + humedad histórica", "mucho por descubrir", "poca cobertura integrada"],
        "instruments": ["landsat_thermal", "sentinel_2_ndvi", "sar_backscatter", "icesat2"]
    },
    
    "patagonia_austral": {
        "name": "Patagonia Austral - Estepas + Glaciares",
        "terrain": "mountain_steppe",
        "lat_min": -50.20, "lat_max": -50.19,
        "lon_min": -72.30, "lon_max": -72.29,
        "country": "Argentina/Chile",
        "scientific_value": "ALTO",
        "description": "Enorme extensión, poca densidad de estudios, acceso difícil",
        "target_features": ["sitios ocupación temprana", "estructuras de abrigo", "patrones de movilidad"],
        "advantages": ["ventaja local + técnica", "glaciares + lagos proglaciares", "ventaja digital vs campo"],
        "instruments": ["icesat2", "sentinel_2_ndvi", "sar_backscatter", "modis_lst"]
    },
    
    "plataforma_continental": {
        "name": "Plataforma Continental - Mar del Norte",
        "terrain": "shallow_marine",
        "lat_min": 55.68, "lat_max": 55.69,
        "lon_min": 2.58, "lon_max": 2.59,
        "country": "North Sea",
        "scientific_value": "MEDIO-ALTO",
        "description": "Zonas inundadas post-glaciación, data dispersa",
        "target_features": ["paleopaisajes", "rutas humanas", "asentamientos costeros sumergidos"],
        "advantages": ["excavación física carísima", "sistema brilla como filtro", "batimetría + térmico"],
        "instruments": ["sar_backscatter", "modis_lst", "copernicus_sst", "sentinel_2_ndvi"]
    }
}

class TestCandidatosEstrategicos:
    """Test de candidatos estratégicos para captura de datos."""
    
    def __init__(self):
        self.integrator = None
        self.results = {
            "metadata": {
                "test_version": "v2.1_estrategicos",
                "test_timestamp": datetime.now().isoformat(),
                "test_duration_minutes": None,
                "log_file": log_filename,
                "objective": "Capturar datos instrumentales para análisis posterior en casa"
            },
            "summary": {
                "total_candidates": len(CANDIDATOS_ESTRATEGICOS),
                "successful_candidates": 0,
                "failed_candidates": 0,
                "total_measurements": 0,
                "successful_measurements": 0,
                "instrument_failures": []
            },
            "candidates": {}
        }
        
        # Inicializar integrador
        self._initialize_integrator()
    
    def _initialize_integrator(self):
        """Inicializar integrador robusto."""
        if not INTEGRATOR_AVAILABLE:
            logger.error("❌ Integrator not available - check imports")
            return
        
        try:
            self.integrator = RealDataIntegratorV2()
            logger.info("✅ RealDataIntegratorV2 initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize integrator: {e}")
    
    async def test_candidato(self, candidato_id: str, candidato_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test un candidato específico."""
        
        logger.info(f"\n🔍 TESTING: {candidato_data['name']}")
        logger.info(f"   Terrain: {candidato_data['terrain']}")
        logger.info(f"   Scientific Value: {candidato_data['scientific_value']}")
        logger.info(f"   Coordinates: [{candidato_data['lat_min']:.4f}, {candidato_data['lat_max']:.4f}] x [{candidato_data['lon_min']:.4f}, {candidato_data['lon_max']:.4f}]")
        logger.info(f"   Target Features: {', '.join(candidato_data['target_features'])}")
        logger.info(f"   Instruments: {', '.join(candidato_data['instruments'])}")
        
        start_time = datetime.now()
        
        try:
            if not self.integrator:
                raise Exception("Integrator not available")
            
            # Capturar mediciones con timeout
            batch = await asyncio.wait_for(
                self.integrator.get_batch_measurements(
                    candidato_data['instruments'],
                    candidato_data['lat_min'], candidato_data['lat_max'],
                    candidato_data['lon_min'], candidato_data['lon_max']
                ),
                timeout=180.0  # 3 minutos por candidato
            )
            
            # Generar reporte
            batch_results = batch.generate_report()
            
            # Procesar mediciones individuales
            measurements = []
            instrument_failures = []
            
            for instrument_data in batch_results.get('instruments', []):
                sanitized_data = sanitize_response(instrument_data)
                
                # Crear medición en formato estándar
                measurement = {
                    "candidate_id": candidato_id,
                    "candidate_name": candidato_data['name'],
                    "terrain": candidato_data['terrain'],
                    "country": candidato_data['country'],
                    "coordinates": {
                        "lat_min": candidato_data['lat_min'],
                        "lat_max": candidato_data['lat_max'],
                        "lon_min": candidato_data['lon_min'],
                        "lon_max": candidato_data['lon_max']
                    },
                    "instrument": sanitized_data.get('instrument', 'unknown'),
                    "measurement_type": sanitized_data.get('measurement_type', 'unknown'),
                    "value": sanitized_data.get('value'),
                    "unit": sanitized_data.get('unit'),
                    "confidence": sanitized_data.get('confidence'),
                    "status": sanitized_data.get('status', 'UNKNOWN'),
                    "source": sanitized_data.get('source'),
                    "measured_at": datetime.now().isoformat(),
                    "analysis_version": "v2.1",
                    "reason": sanitized_data.get('reason'),
                    "processing_time_seconds": sanitized_data.get('processing_time_s'),
                    "raw_response": sanitized_data  # Guardar respuesta completa
                }
                
                measurements.append(measurement)
                
                # Registrar fallos de instrumentos
                if sanitized_data.get('status') not in ['SUCCESS', 'DEGRADED']:
                    instrument_failures.append({
                        "candidate": candidato_id,
                        "instrument": sanitized_data.get('instrument', 'unknown'),
                        "status": sanitized_data.get('status', 'UNKNOWN'),
                        "reason": sanitized_data.get('reason', 'No reason provided'),
                        "error_details": sanitized_data.get('error_details')
                    })
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            result = {
                "candidate_id": candidato_id,
                "candidate_info": candidato_data,
                "success": True,
                "processing_time_seconds": processing_time,
                "coverage_score": batch_results['coverage_score'],
                "total_instruments": batch_results['total_instruments'],
                "usable_instruments": batch_results['usable_instruments'],
                "status_summary": batch_results['status_summary'],
                "measurements": measurements,
                "instrument_failures": instrument_failures,
                "captured_at": end_time.isoformat()
            }
            
            logger.info(f"✅ {candidato_data['name']}: Coverage {batch_results['coverage_score']:.1%} "
                       f"({batch_results['usable_instruments']}/{batch_results['total_instruments']} instruments)")
            
            if instrument_failures:
                logger.warning(f"⚠️ {len(instrument_failures)} instrument failures detected")
                for failure in instrument_failures:
                    logger.warning(f"   - {failure['instrument']}: {failure['status']} - {failure['reason']}")
            
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"⏰ {candidato_data['name']}: Timeout after 3 minutes")
            return {
                "candidate_id": candidato_id,
                "candidate_info": candidato_data,
                "success": False,
                "error": "TIMEOUT_3MIN",
                "processing_time_seconds": 180.0,
                "captured_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ {candidato_data['name']}: Failed - {e}")
            return {
                "candidate_id": candidato_id,
                "candidate_info": candidato_data,
                "success": False,
                "error": str(e)[:200],
                "processing_time_seconds": (datetime.now() - start_time).total_seconds(),
                "captured_at": datetime.now().isoformat()
            }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Ejecutar tests de todos los candidatos."""
        
        logger.info("🚀 ARCHEOSCOPE - TEST 5 CANDIDATOS ESTRATÉGICOS")
        logger.info("=" * 60)
        logger.info("OBJETIVO: Capturar datos instrumentales para análisis posterior")
        logger.info("NO guardar en BD - solo JSON para análisis offline")
        logger.info("=" * 60)
        
        start_time = datetime.now()
        
        for i, (candidato_id, candidato_data) in enumerate(CANDIDATOS_ESTRATEGICOS.items(), 1):
            logger.info(f"\n[{i}/{len(CANDIDATOS_ESTRATEGICOS)}] Processing {candidato_id}...")
            
            result = await self.test_candidato(candidato_id, candidato_data)
            
            self.results['candidates'][candidato_id] = result
            
            if result['success']:
                self.results['summary']['successful_candidates'] += 1
                self.results['summary']['total_measurements'] += len(result.get('measurements', []))
                self.results['summary']['successful_measurements'] += result.get('usable_instruments', 0)
                
                # Agregar fallos de instrumentos al resumen
                if 'instrument_failures' in result:
                    self.results['summary']['instrument_failures'].extend(result['instrument_failures'])
            else:
                self.results['summary']['failed_candidates'] += 1
            
            # Pausa entre candidatos
            if i < len(CANDIDATOS_ESTRATEGICOS):
                logger.info("   ⏳ Pausing 5 seconds before next candidate...")
                await asyncio.sleep(5)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        
        self.results['metadata']['test_duration_minutes'] = duration
        self.results['metadata']['test_completed_at'] = end_time.isoformat()
        
        return self.results
    
    def save_results(self, results: Dict[str, Any]) -> str:
        """Guardar resultados en JSON."""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'candidatos_estrategicos_mediciones_{timestamp}.json'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"✅ Results saved to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ Failed to save results: {e}")
            return ""
    
    def print_summary_report(self, results: Dict[str, Any]):
        """Imprimir reporte resumen."""
        
        summary = results['summary']
        metadata = results['metadata']
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 REPORTE FINAL - 5 CANDIDATOS ESTRATÉGICOS")
        logger.info("=" * 60)
        
        logger.info(f"🎯 OBJETIVO CUMPLIDO:")
        logger.info(f"   Capturar datos instrumentales para análisis posterior en casa")
        logger.info(f"   NO guardar en BD ahora - solo JSON")
        
        logger.info(f"\n📈 ESTADÍSTICAS DE CAPTURA:")
        logger.info(f"   Total Candidatos: {summary['total_candidates']}")
        logger.info(f"   Exitosos: {summary['successful_candidates']}")
        logger.info(f"   Fallidos: {summary['failed_candidates']}")
        logger.info(f"   Tasa de Éxito: {summary['successful_candidates']/summary['total_candidates']*100:.1f}%")
        
        logger.info(f"\n🔬 MEDICIONES CAPTURADAS:")
        logger.info(f"   Total Mediciones: {summary['total_measurements']}")
        logger.info(f"   Mediciones Exitosas: {summary['successful_measurements']}")
        
        logger.info(f"\n⏱️ TIMING:")
        logger.info(f"   Duración Total: {metadata['test_duration_minutes']:.1f} minutos")
        logger.info(f"   Promedio por Candidato: {metadata['test_duration_minutes']/summary['total_candidates']:.1f} min")
        
        logger.info(f"\n🌍 CANDIDATOS POR RESULTADO:")
        for candidato_id, candidato_result in results['candidates'].items():
            candidato_info = candidato_result['candidate_info']
            status = "✅ SUCCESS" if candidato_result['success'] else "❌ FAILED"
            
            if candidato_result['success']:
                coverage = candidato_result['coverage_score']
                instruments = f"{candidato_result['usable_instruments']}/{candidato_result['total_instruments']}"
                logger.info(f"   {candidato_info['name']:35} {status} (Coverage: {coverage:.1%}, Instruments: {instruments})")
            else:
                error = candidato_result.get('error', 'Unknown error')
                logger.info(f"   {candidato_info['name']:35} {status} ({error})")
        
        # Fallos de instrumentos
        if summary['instrument_failures']:
            logger.info(f"\n⚠️ FALLOS DE INSTRUMENTOS ({len(summary['instrument_failures'])}):")
            
            # Agrupar por instrumento
            instrument_failure_counts = {}
            for failure in summary['instrument_failures']:
                instrument = failure['instrument']
                if instrument not in instrument_failure_counts:
                    instrument_failure_counts[instrument] = []
                instrument_failure_counts[instrument].append(failure)
            
            for instrument, failures in instrument_failure_counts.items():
                logger.info(f"   {instrument}: {len(failures)} fallos")
                for failure in failures[:3]:  # Mostrar solo los primeros 3
                    logger.info(f"     - {failure['candidate']}: {failure['status']} - {failure['reason']}")
                if len(failures) > 3:
                    logger.info(f"     ... y {len(failures)-3} más")
        
        logger.info(f"\n📁 ARCHIVOS GENERADOS:")
        logger.info(f"   Mediciones: {metadata.get('results_file', 'candidatos_estrategicos_mediciones_*.json')}")
        logger.info(f"   Log: {metadata['log_file']}")
        
        # Evaluación del éxito
        success_rate = summary['successful_candidates'] / summary['total_candidates']
        
        if success_rate >= 0.8:
            logger.info(f"\n🎉 TEST EXITOSO!")
            logger.info(f"   Datos capturados listos para análisis en casa")
            logger.info(f"   Calidad de datos: EXCELENTE")
        elif success_rate >= 0.6:
            logger.info(f"\n✅ TEST PARCIALMENTE EXITOSO")
            logger.info(f"   Suficientes datos para análisis inicial")
            logger.info(f"   Calidad de datos: BUENA")
        else:
            logger.info(f"\n⚠️ TEST CON LIMITACIONES")
            logger.info(f"   Algunos datos capturados, revisar fallos")
            logger.info(f"   Calidad de datos: LIMITADA")
        
        logger.info(f"\n🚀 PRÓXIMOS PASOS EN CASA:")
        logger.info(f"   1. Cargar JSON en base de datos PostgreSQL")
        logger.info(f"   2. Ejecutar análisis con asistentes IA")
        logger.info(f"   3. Correlacionar con BD arqueológica existente")
        logger.info(f"   4. Generar insights científicos")
        logger.info(f"   5. Refinar algoritmos basado en patrones reales")
        
        logger.info("=" * 60)

async def main():
    """Función principal."""
    
    print("🚀 ArcheoScope - Test 5 Candidatos Estratégicos")
    print("Capturando datos instrumentales para análisis posterior en casa")
    print()
    
    if not INTEGRATOR_AVAILABLE:
        print("❌ Critical error: RealDataIntegratorV2 not available")
        return False
    
    try:
        # Crear tester
        tester = TestCandidatosEstrategicos()
        
        # Ejecutar tests
        results = await tester.run_all_tests()
        
        # Guardar resultados
        results_file = tester.save_results(results)
        results['metadata']['results_file'] = results_file
        
        # Mostrar reporte
        tester.print_summary_report(results)
        
        # Evaluar éxito
        success_rate = results['summary']['successful_candidates'] / results['summary']['total_candidates']
        
        if success_rate >= 0.6:
            print(f"\n🎉 DATOS CAPTURADOS EXITOSAMENTE!")
            print(f"Listos para análisis en casa con BD + IA")
            return True
        else:
            print(f"\n⚠️ CAPTURA PARCIAL")
            print(f"Revisar fallos de instrumentos")
            return False
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Test interrupted by user")
        return False
        
    except Exception as e:
        logger.error(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("Iniciando test de 5 candidatos estratégicos...")
    print("Tiempo estimado: 15-20 minutos")
    print("Objetivo: Capturar datos para análisis posterior")
    print()
    
    # Ejecutar test
    success = asyncio.run(main())
    exit(0 if success else 1)