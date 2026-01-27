#!/usr/bin/env python3
"""
ArcheoScope Scientific Dataset Capture
=====================================

Captura datos de 25 candidatos (5 por terreno) para crear
dataset científico reproducible.

TRANSFORMACIÓN: "pipeline frágil dependiente de APIs" → "sistema científico reproducible"

REGLAS:
- Nunca abortar por un candidato
- Guardar TODO (éxitos y fallos)
- Logging detallado
- Persistencia robusta
- Estados explícitos por instrumento
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠️ psycopg2 not available - install with: pip install psycopg2-binary")

# Importar sistema robusto
try:
    from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
    from data_sanitizer import sanitize_response
    INTEGRATOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Integrator not available: {e}")
    INTEGRATOR_AVAILABLE = False

# Configurar logging
log_filename = f'scientific_capture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Datos de candidatos por terreno (5 por terreno = 25 total)
TERRAIN_CANDIDATES = {
    "desert": [
        {"name": "Giza Plateau", "lat_min": 29.97, "lat_max": 29.98, "lon_min": 31.13, "lon_max": 31.14, "country": "Egypt"},
        {"name": "Petra Jordan", "lat_min": 30.32, "lat_max": 30.33, "lon_min": 35.44, "lon_max": 35.45, "country": "Jordan"},
        {"name": "Nazca Lines", "lat_min": -14.74, "lat_max": -14.73, "lon_min": -75.13, "lon_max": -75.12, "country": "Peru"},
        {"name": "Sahara Morocco", "lat_min": 31.63, "lat_max": 31.64, "lon_min": -8.01, "lon_max": -8.00, "country": "Morocco"},
        {"name": "Atacama Chile", "lat_min": -24.50, "lat_max": -24.49, "lon_min": -69.25, "lon_max": -69.24, "country": "Chile"}
    ],
    "forest": [
        {"name": "Angkor Cambodia", "lat_min": 13.41, "lat_max": 13.42, "lon_min": 103.86, "lon_max": 103.87, "country": "Cambodia"},
        {"name": "Amazon Brazil", "lat_min": -3.12, "lat_max": -3.11, "lon_min": -60.02, "lon_max": -60.01, "country": "Brazil"},
        {"name": "Maya Guatemala", "lat_min": 17.22, "lat_max": 17.23, "lon_min": -89.62, "lon_max": -89.61, "country": "Guatemala"},
        {"name": "Boreal Canada", "lat_min": 54.73, "lat_max": 54.74, "lon_min": -101.88, "lon_max": -101.87, "country": "Canada"},
        {"name": "Congo DRC", "lat_min": -4.32, "lat_max": -4.31, "lon_min": 15.31, "lon_max": 15.32, "country": "DRC"}
    ],
    "mountain": [
        {"name": "Machu Picchu", "lat_min": -13.16, "lat_max": -13.15, "lon_min": -72.55, "lon_max": -72.54, "country": "Peru"},
        {"name": "Alps Austria", "lat_min": 47.07, "lat_max": 47.08, "lon_min": 10.84, "lon_max": 10.85, "country": "Austria"},
        {"name": "Himalayas Nepal", "lat_min": 27.98, "lat_max": 27.99, "lon_min": 86.92, "lon_max": 86.93, "country": "Nepal"},
        {"name": "Andes Colombia", "lat_min": 4.60, "lat_max": 4.61, "lon_min": -74.08, "lon_max": -74.07, "country": "Colombia"},
        {"name": "Rocky Mountains USA", "lat_min": 40.34, "lat_max": 40.35, "lon_min": -105.69, "lon_max": -105.68, "country": "USA"}
    ],
    "coastal": [
        {"name": "Mediterranean Greece", "lat_min": 37.97, "lat_max": 37.98, "lon_min": 23.72, "lon_max": 23.73, "country": "Greece"},
        {"name": "Pacific Chile", "lat_min": -33.45, "lat_max": -33.44, "lon_min": -70.65, "lon_max": -70.64, "country": "Chile"},
        {"name": "Atlantic Portugal", "lat_min": 38.71, "lat_max": 38.72, "lon_min": -9.14, "lon_max": -9.13, "country": "Portugal"},
        {"name": "North Sea Denmark", "lat_min": 55.68, "lat_max": 55.69, "lon_min": 12.58, "lon_max": 12.59, "country": "Denmark"},
        {"name": "Caribbean Mexico", "lat_min": 20.68, "lat_max": 20.69, "lon_min": -87.46, "lon_max": -87.45, "country": "Mexico"}
    ],
    "polar": [
        {"name": "Antarctica West", "lat_min": -75.70, "lat_max": -75.69, "lon_min": -111.36, "lon_max": -111.35, "country": "Antarctica"},
        {"name": "Greenland Ice", "lat_min": 72.58, "lat_max": 72.59, "lon_min": -38.46, "lon_max": -38.45, "country": "Greenland"},
        {"name": "Svalbard Norway", "lat_min": 78.92, "lat_max": 78.93, "lon_min": 11.93, "lon_max": 11.94, "country": "Norway"},
        {"name": "Alaska Tundra", "lat_min": 68.77, "lat_max": 68.78, "lon_min": -166.05, "lon_max": -166.04, "country": "USA"},
        {"name": "Siberia Russia", "lat_min": 67.50, "lat_max": 67.51, "lon_min": 64.05, "lon_max": 64.06, "country": "Russia"}
    ]
}

class ScientificDatasetCapture:
    """Capturador de dataset científico robusto."""
    
    def __init__(self):
        self.integrator = None
        self.db_conn = None
        self.analysis_version = "v2.1"
        self.results_file = f"scientific_dataset_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Inicializar componentes
        self._initialize_integrator()
        self._initialize_database()
    
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
    
    def _initialize_database(self):
        """Inicializar conexión a base de datos."""
        if not POSTGRES_AVAILABLE:
            logger.warning("⚠️ PostgreSQL not available - will save to JSON only")
            return
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            db_url = os.getenv("DATABASE_URL")
            if not db_url:
                logger.warning("⚠️ DATABASE_URL not configured - will save to JSON only")
                return
            
            self.db_conn = psycopg2.connect(db_url)
            logger.info("✅ Database connected")
            
            # Crear tablas si no existen
            self._setup_tables()
            
        except Exception as e:
            logger.warning(f"⚠️ Database connection failed: {e} - will save to JSON only")
            self.db_conn = None
    
    def _setup_tables(self):
        """Crear tablas si no existen."""
        if not self.db_conn:
            return
        
        try:
            with self.db_conn.cursor() as cur:
                # Tabla de candidatos
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS analysis_candidates (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        candidate_id VARCHAR(100) UNIQUE NOT NULL,
                        candidate_name VARCHAR(200) NOT NULL,
                        terrain_type VARCHAR(50) NOT NULL,
                        lat_min DECIMAL(10,7) NOT NULL,
                        lat_max DECIMAL(10,7) NOT NULL,
                        lon_min DECIMAL(10,7) NOT NULL,
                        lon_max DECIMAL(10,7) NOT NULL,
                        analysis_status VARCHAR(20) DEFAULT 'PENDING',
                        measurements_count INTEGER DEFAULT 0,
                        successful_measurements INTEGER DEFAULT 0,
                        coverage_score DECIMAL(4,3),
                        country VARCHAR(100),
                        notes TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        analyzed_at TIMESTAMP WITH TIME ZONE,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                """)
                
                # Tabla de mediciones
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS raw_measurements (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        candidate_id VARCHAR(100) NOT NULL,
                        candidate_name VARCHAR(200),
                        terrain_type VARCHAR(50) NOT NULL,
                        lat_min DECIMAL(10,7) NOT NULL,
                        lat_max DECIMAL(10,7) NOT NULL,
                        lon_min DECIMAL(10,7) NOT NULL,
                        lon_max DECIMAL(10,7) NOT NULL,
                        instrument VARCHAR(100) NOT NULL,
                        measurement_type VARCHAR(100) NOT NULL,
                        value DECIMAL(15,6),
                        unit VARCHAR(20),
                        confidence DECIMAL(4,3),
                        status VARCHAR(20) NOT NULL,
                        source VARCHAR(100),
                        api_response_raw JSONB,
                        measured_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        analysis_version VARCHAR(20) NOT NULL DEFAULT 'v2.1',
                        reason TEXT,
                        processing_time_seconds DECIMAL(8,3),
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                """)
                
                # Índices
                cur.execute("CREATE INDEX IF NOT EXISTS idx_raw_measurements_candidate ON raw_measurements(candidate_id);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_raw_measurements_terrain ON raw_measurements(terrain_type);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_raw_measurements_instrument ON raw_measurements(instrument);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_raw_measurements_status ON raw_measurements(status);")
                
                self.db_conn.commit()
                logger.info("✅ Database tables ready")
                
        except Exception as e:
            logger.error(f"❌ Database setup failed: {e}")
            self.db_conn = None
    
    def _save_to_database(self, candidate_id: str, candidate: Dict[str, Any], 
                         batch_results: Dict[str, Any]):
        """Guardar resultados en base de datos."""
        if not self.db_conn:
            return
        
        try:
            measurements_saved = 0
            successful_measurements = 0
            
            with self.db_conn.cursor() as cur:
                # Insertar/actualizar candidato
                cur.execute("""
                    INSERT INTO analysis_candidates 
                    (candidate_id, candidate_name, terrain_type, lat_min, lat_max, lon_min, lon_max, country)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (candidate_id) DO UPDATE SET
                        analysis_status = 'IN_PROGRESS',
                        updated_at = NOW();
                """, (
                    candidate_id, candidate['name'], candidate['terrain'],
                    candidate['lat_min'], candidate['lat_max'],
                    candidate['lon_min'], candidate['lon_max'],
                    candidate.get('country', 'Unknown')
                ))
                
                # Insertar mediciones
                for instrument_data in batch_results.get('instruments', []):
                    sanitized_data = sanitize_response(instrument_data)
                    
                    cur.execute("""
                        INSERT INTO raw_measurements 
                        (candidate_id, candidate_name, terrain_type, lat_min, lat_max, lon_min, lon_max,
                         instrument, measurement_type, value, unit, confidence, status, source,
                         api_response_raw, measured_at, analysis_version, reason, processing_time_seconds)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        candidate_id, candidate['name'], candidate['terrain'],
                        candidate['lat_min'], candidate['lat_max'],
                        candidate['lon_min'], candidate['lon_max'],
                        sanitized_data.get('instrument', 'unknown'),
                        sanitized_data.get('measurement_type', 'unknown'),
                        sanitized_data.get('value'),
                        sanitized_data.get('unit'),
                        sanitized_data.get('confidence'),
                        sanitized_data.get('status', 'UNKNOWN'),
                        sanitized_data.get('source'),
                        json.dumps(sanitized_data),
                        datetime.now(),
                        self.analysis_version,
                        sanitized_data.get('reason'),
                        sanitized_data.get('processing_time_s')
                    ))
                    
                    measurements_saved += 1
                    if sanitized_data.get('status') in ['SUCCESS', 'DEGRADED']:
                        successful_measurements += 1
                
                # Actualizar candidato con resultados
                cur.execute("""
                    UPDATE analysis_candidates SET
                        analysis_status = 'COMPLETED',
                        measurements_count = %s,
                        successful_measurements = %s,
                        coverage_score = %s,
                        analyzed_at = NOW(),
                        updated_at = NOW()
                    WHERE candidate_id = %s;
                """, (
                    measurements_saved,
                    successful_measurements,
                    batch_results.get('coverage_score', 0.0),
                    candidate_id
                ))
                
                self.db_conn.commit()
                logger.info(f"✅ Saved to database: {measurements_saved} measurements")
                
        except Exception as e:
            logger.error(f"❌ Database save failed: {e}")
            if self.db_conn:
                self.db_conn.rollback()
    
    def _save_to_json(self, all_results: Dict[str, Any]):
        """Guardar resultados en JSON como backup."""
        try:
            with open(self.results_file, 'w') as f:
                json.dump(all_results, f, indent=2, default=str)
            logger.info(f"✅ Results saved to: {self.results_file}")
        except Exception as e:
            logger.error(f"❌ JSON save failed: {e}")
    
    async def capture_candidate(self, terrain: str, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Capturar datos de un candidato específico."""
        
        candidate_full = {**candidate, 'terrain': terrain}
        candidate_id = f"{terrain}_{candidate['name'].lower().replace(' ', '_')}"
        
        logger.info(f"\n🔍 CAPTURING: {candidate['name']} ({terrain.upper()})")
        logger.info(f"   Coordinates: [{candidate['lat_min']:.4f}, {candidate['lat_max']:.4f}] x [{candidate['lon_min']:.4f}, {candidate['lon_max']:.4f}]")
        logger.info(f"   Country: {candidate.get('country', 'Unknown')}")
        
        # Instrumentos específicos por terreno
        terrain_instruments = {
            'desert': ['sentinel_2_ndvi', 'landsat_thermal', 'sar_backscatter', 'icesat2'],
            'forest': ['sentinel_2_ndvi', 'icesat2', 'sar_backscatter', 'modis_lst'],
            'mountain': ['icesat2', 'sentinel_2_ndvi', 'sar_backscatter', 'opentopography'],
            'coastal': ['sentinel_2_ndvi', 'sar_backscatter', 'modis_lst', 'copernicus_sst'],
            'polar': ['icesat2', 'sar_backscatter', 'nsidc_sea_ice', 'modis_lst']
        }
        
        instruments = terrain_instruments.get(terrain, ['sentinel_2_ndvi', 'icesat2', 'modis_lst'])
        
        logger.info(f"   Instruments: {', '.join(instruments)}")
        
        try:
            if not self.integrator:
                raise Exception("Integrator not available")
            
            # Capturar mediciones con timeout por candidato
            batch = await asyncio.wait_for(
                self.integrator.get_batch_measurements(
                    instruments,
                    candidate['lat_min'], candidate['lat_max'],
                    candidate['lon_min'], candidate['lon_max']
                ),
                timeout=300.0  # 5 minutos por candidato
            )
            
            # Generar reporte
            batch_results = batch.generate_report()
            
            # Guardar en BD si está disponible
            self._save_to_database(candidate_id, candidate_full, batch_results)
            
            result = {
                'candidate_id': candidate_id,
                'candidate_name': candidate['name'],
                'terrain': terrain,
                'country': candidate.get('country', 'Unknown'),
                'coordinates': {
                    'lat_min': candidate['lat_min'],
                    'lat_max': candidate['lat_max'],
                    'lon_min': candidate['lon_min'],
                    'lon_max': candidate['lon_max']
                },
                'success': True,
                'coverage_score': batch_results['coverage_score'],
                'total_instruments': batch_results['total_instruments'],
                'usable_instruments': batch_results['usable_instruments'],
                'status_summary': batch_results['status_summary'],
                'measurements': batch_results['instruments'],
                'captured_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ {candidate['name']}: Coverage {batch_results['coverage_score']:.1%} "
                       f"({batch_results['usable_instruments']}/{batch_results['total_instruments']} instruments)")
            
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"⏰ {candidate['name']}: Timeout after 5 minutes")
            return {
                'candidate_id': candidate_id,
                'candidate_name': candidate['name'],
                'terrain': terrain,
                'success': False,
                'error': 'TIMEOUT_5MIN',
                'captured_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ {candidate['name']}: Failed - {e}")
            return {
                'candidate_id': candidate_id,
                'candidate_name': candidate['name'],
                'terrain': terrain,
                'success': False,
                'error': str(e)[:200],
                'captured_at': datetime.now().isoformat()
            }
    
    async def capture_all_terrains(self) -> Dict[str, Any]:
        """Capturar todos los terrenos y candidatos."""
        
        logger.info("🚀 ARCHEOSCOPE SCIENTIFIC DATASET CAPTURE")
        logger.info("=" * 60)
        logger.info("TRANSFORMING: 'fragile API pipeline' → 'reproducible scientific system'")
        logger.info("=" * 60)
        
        start_time = datetime.now()
        
        results = {
            'metadata': {
                'capture_version': self.analysis_version,
                'start_time': start_time.isoformat(),
                'end_time': None,
                'duration_minutes': None,
                'log_file': log_filename,
                'results_file': self.results_file
            },
            'summary': {
                'total_candidates': 0,
                'successful_candidates': 0,
                'failed_candidates': 0,
                'total_measurements': 0,
                'successful_measurements': 0,
                'overall_coverage_score': 0.0
            },
            'terrain_results': {},
            'candidate_details': []
        }
        
        total_coverage_scores = []
        
        for terrain, candidates in TERRAIN_CANDIDATES.items():
            logger.info(f"\n🌍 TERRAIN: {terrain.upper()}")
            logger.info("-" * 40)
            
            terrain_results = {
                'terrain': terrain,
                'total_candidates': len(candidates),
                'successful_candidates': 0,
                'failed_candidates': 0,
                'coverage_scores': [],
                'avg_coverage_score': 0.0,
                'candidates': []
            }
            
            for i, candidate in enumerate(candidates, 1):
                logger.info(f"\n[{i}/{len(candidates)}] Processing {candidate['name']}...")
                
                result = await self.capture_candidate(terrain, candidate)
                
                terrain_results['candidates'].append(result)
                results['candidate_details'].append(result)
                results['summary']['total_candidates'] += 1
                
                if result['success']:
                    results['summary']['successful_candidates'] += 1
                    terrain_results['successful_candidates'] += 1
                    
                    coverage_score = result['coverage_score']
                    terrain_results['coverage_scores'].append(coverage_score)
                    total_coverage_scores.append(coverage_score)
                    
                    results['summary']['total_measurements'] += result['total_instruments']
                    results['summary']['successful_measurements'] += result['usable_instruments']
                    
                else:
                    results['summary']['failed_candidates'] += 1
                    terrain_results['failed_candidates'] += 1
                
                # Pausa entre candidatos para no saturar APIs
                if i < len(candidates):  # No pausar después del último
                    logger.info("   ⏳ Pausing 3 seconds before next candidate...")
                    await asyncio.sleep(3)
            
            # Calcular estadísticas del terreno
            if terrain_results['coverage_scores']:
                terrain_results['avg_coverage_score'] = sum(terrain_results['coverage_scores']) / len(terrain_results['coverage_scores'])
            
            results['terrain_results'][terrain] = terrain_results
            
            logger.info(f"\n📊 {terrain.upper()} SUMMARY:")
            logger.info(f"   Successful: {terrain_results['successful_candidates']}/{terrain_results['total_candidates']}")
            logger.info(f"   Avg Coverage: {terrain_results['avg_coverage_score']:.1%}")
            
            # Pausa entre terrenos
            if terrain != list(TERRAIN_CANDIDATES.keys())[-1]:  # No pausar después del último terreno
                logger.info("   ⏳ Pausing 5 seconds before next terrain...")
                await asyncio.sleep(5)
        
        # Calcular estadísticas finales
        end_time = datetime.now()
        duration = end_time - start_time
        
        results['metadata']['end_time'] = end_time.isoformat()
        results['metadata']['duration_minutes'] = duration.total_seconds() / 60
        
        if total_coverage_scores:
            results['summary']['overall_coverage_score'] = sum(total_coverage_scores) / len(total_coverage_scores)
        
        # Guardar resultados
        self._save_to_json(results)
        
        # Mostrar resumen final
        self._print_final_summary(results)
        
        return results
    
    def _print_final_summary(self, results: Dict[str, Any]):
        """Imprimir resumen final."""
        
        summary = results['summary']
        metadata = results['metadata']
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 FINAL SCIENTIFIC DATASET CAPTURE RESULTS")
        logger.info("=" * 60)
        
        logger.info(f"🎯 TRANSFORMATION STATUS:")
        logger.info(f"   From: 'fragile API pipeline'")
        logger.info(f"   To:   'reproducible scientific system'")
        
        logger.info(f"\n📈 CAPTURE STATISTICS:")
        logger.info(f"   Total Candidates: {summary['total_candidates']}")
        logger.info(f"   Successful: {summary['successful_candidates']}")
        logger.info(f"   Failed: {summary['failed_candidates']}")
        logger.info(f"   Success Rate: {summary['successful_candidates']/summary['total_candidates']*100:.1f}%")
        
        logger.info(f"\n🔬 MEASUREMENT STATISTICS:")
        logger.info(f"   Total Measurements: {summary['total_measurements']}")
        logger.info(f"   Successful Measurements: {summary['successful_measurements']}")
        logger.info(f"   Overall Coverage Score: {summary['overall_coverage_score']:.1%}")
        
        logger.info(f"\n⏱️  TIMING:")
        logger.info(f"   Duration: {metadata['duration_minutes']:.1f} minutes")
        logger.info(f"   Avg per candidate: {metadata['duration_minutes']/summary['total_candidates']:.1f} min")
        
        logger.info(f"\n🌍 TERRAIN BREAKDOWN:")
        for terrain, terrain_data in results['terrain_results'].items():
            success_rate = terrain_data['successful_candidates'] / terrain_data['total_candidates'] * 100
            logger.info(f"   {terrain:8}: {terrain_data['successful_candidates']}/{terrain_data['total_candidates']} "
                       f"({success_rate:4.1f}%) - Avg Coverage: {terrain_data['avg_coverage_score']:.1%}")
        
        logger.info(f"\n📁 OUTPUT FILES:")
        logger.info(f"   Results: {metadata['results_file']}")
        logger.info(f"   Log: {metadata['log_file']}")
        if self.db_conn:
            logger.info(f"   Database: ✅ Saved to PostgreSQL")
        else:
            logger.info(f"   Database: ⚠️ Not available - JSON only")
        
        # Evaluación del éxito
        success_threshold = 0.6  # 60% de candidatos exitosos
        coverage_threshold = 0.4  # 40% de coverage promedio
        
        overall_success_rate = summary['successful_candidates'] / summary['total_candidates']
        
        if (overall_success_rate >= success_threshold and 
            summary['overall_coverage_score'] >= coverage_threshold):
            logger.info(f"\n🎉 SCIENTIFIC DATASET CAPTURE: SUCCESS!")
            logger.info(f"   ArcheoScope is now a reproducible scientific system!")
            logger.info(f"   Ready for offline analysis and algorithm refinement.")
        elif overall_success_rate >= 0.4:
            logger.info(f"\n✅ SCIENTIFIC DATASET CAPTURE: PARTIAL SUCCESS")
            logger.info(f"   Sufficient data captured for initial analysis.")
            logger.info(f"   Can proceed with dataset analysis.")
        else:
            logger.info(f"\n⚠️ SCIENTIFIC DATASET CAPTURE: LIMITED SUCCESS")
            logger.info(f"   Some data captured but may need troubleshooting.")
            logger.info(f"   Check failed candidates and retry if needed.")
        
        logger.info("\n🚀 NEXT STEPS:")
        logger.info("   1. Run: python analyze_scientific_dataset.py")
        logger.info("   2. Review terrain-specific patterns")
        logger.info("   3. Refine algorithms based on real data")
        logger.info("   4. Prepare scientific publication")
        
        logger.info("=" * 60)

async def main():
    """Función principal."""
    
    print("🚀 ArcheoScope Scientific Dataset Capture")
    print("Transforming: 'fragile API pipeline' → 'reproducible scientific system'")
    print()
    
    # Verificar dependencias
    if not INTEGRATOR_AVAILABLE:
        print("❌ Critical error: RealDataIntegratorV2 not available")
        print("   Make sure backend modules are properly installed")
        return False
    
    try:
        # Crear capturador
        capture = ScientificDatasetCapture()
        
        # Ejecutar captura completa
        results = await capture.capture_all_terrains()
        
        # Evaluar éxito
        success_rate = results['summary']['successful_candidates'] / results['summary']['total_candidates']
        
        if success_rate >= 0.6:
            print("\n🎉 MISSION ACCOMPLISHED!")
            print("ArcheoScope scientific dataset successfully captured!")
            return True
        elif success_rate >= 0.4:
            print("\n✅ PARTIAL SUCCESS!")
            print("Sufficient data for analysis captured!")
            return True
        else:
            print("\n⚠️ LIMITED SUCCESS")
            print("Some data captured but review needed")
            return False
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Capture interrupted by user")
        print("\n⚠️ Capture interrupted - partial results may be available")
        return False
        
    except Exception as e:
        logger.error(f"\n❌ Capture failed: {e}")
        print(f"\n❌ Capture failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting ArcheoScope Scientific Dataset Capture...")
    print("This will capture data from 25 candidates across 5 terrains")
    print("Estimated time: 90-120 minutes")
    print()
    
    # Confirmar ejecución
    try:
        response = input("Continue? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Capture cancelled by user")
            exit(0)
    except KeyboardInterrupt:
        print("\nCapture cancelled by user")
        exit(0)
    
    # Ejecutar captura
    success = asyncio.run(main())
    exit(0 if success else 1)