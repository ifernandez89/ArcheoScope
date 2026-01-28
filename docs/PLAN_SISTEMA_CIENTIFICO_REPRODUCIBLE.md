# Plan: ArcheoScope Sistema Científico Reproducible

## 🎯 OBJETIVO ESTRATÉGICO

**TRANSFORMACIÓN**: De "pipeline frágil dependiente de APIs" → "sistema científico reproducible"

**PRINCIPIO CLAVE**: Separar captura de datos de análisis

## 📋 PLAN DE IMPLEMENTACIÓN

### FASE 1: CAPTURA DE DATOS (AHORA - Esta Tarde)

#### 1.1 Modelo de Datos Robusto

**Tabla: `raw_measurements`**
```sql
CREATE TABLE raw_measurements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identificación del candidato
    candidate_id VARCHAR(100) NOT NULL,
    candidate_name VARCHAR(200),
    terrain_type VARCHAR(50) NOT NULL, -- forest, desert, mountain, coastal, etc.
    
    -- Coordenadas
    lat_min DECIMAL(10,7) NOT NULL,
    lat_max DECIMAL(10,7) NOT NULL,
    lon_min DECIMAL(10,7) NOT NULL,
    lon_max DECIMAL(10,7) NOT NULL,
    
    -- Instrumento y medición
    instrument VARCHAR(100) NOT NULL, -- "Sentinel-2 NDVI", "ICESat-2 Elevation"
    measurement_type VARCHAR(100) NOT NULL, -- "ndvi", "elevation", "sar_backscatter"
    
    -- Valor y calidad
    value DECIMAL(15,6), -- NULL si no hay datos
    unit VARCHAR(20), -- "index", "m", "dB", "K"
    confidence DECIMAL(4,3), -- 0.000 - 1.000
    status VARCHAR(20) NOT NULL, -- OK, DEGRADED, NO_DATA, TIMEOUT, ERROR
    
    -- Metadatos de fuente
    source VARCHAR(100), -- "PlanetaryComputer", "ICESat-2 NASA", etc.
    api_response_raw JSONB, -- Respuesta completa de la API
    
    -- Temporal y versionado
    measured_at TIMESTAMP WITH TIME ZONE NOT NULL,
    analysis_version VARCHAR(20) NOT NULL DEFAULT 'v2.1',
    
    -- Diagnóstico
    reason TEXT, -- Razón si status != OK
    processing_time_seconds DECIMAL(8,3),
    
    -- Índices
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para consultas eficientes
CREATE INDEX idx_raw_measurements_candidate ON raw_measurements(candidate_id);
CREATE INDEX idx_raw_measurements_terrain ON raw_measurements(terrain_type);
CREATE INDEX idx_raw_measurements_instrument ON raw_measurements(instrument);
CREATE INDEX idx_raw_measurements_status ON raw_measurements(status);
CREATE INDEX idx_raw_measurements_measured_at ON raw_measurements(measured_at);
```

**Tabla: `analysis_candidates`**
```sql
CREATE TABLE analysis_candidates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identificación
    candidate_id VARCHAR(100) UNIQUE NOT NULL,
    candidate_name VARCHAR(200) NOT NULL,
    terrain_type VARCHAR(50) NOT NULL,
    
    -- Coordenadas
    lat_min DECIMAL(10,7) NOT NULL,
    lat_max DECIMAL(10,7) NOT NULL,
    lon_min DECIMAL(10,7) NOT NULL,
    lon_max DECIMAL(10,7) NOT NULL,
    
    -- Estado del análisis
    analysis_status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, IN_PROGRESS, COMPLETED, FAILED
    measurements_count INTEGER DEFAULT 0,
    successful_measurements INTEGER DEFAULT 0,
    coverage_score DECIMAL(4,3), -- 0.000 - 1.000
    
    -- Metadatos
    country VARCHAR(100),
    region VARCHAR(200),
    notes TEXT,
    
    -- Temporal
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    analyzed_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### 1.2 Selección de Candidatos por Terreno

**5 candidatos por terreno** (total: 25 candidatos)

```python
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
```

#### 1.3 Script de Captura Robusto

**Archivo**: `capture_scientific_dataset.py`

```python
#!/usr/bin/env python3
"""
ArcheoScope Scientific Dataset Capture
=====================================

Captura datos de 25 candidatos (5 por terreno) para crear
dataset científico reproducible.

REGLAS:
- Nunca abortar por un candidato
- Guardar TODO (éxitos y fallos)
- Logging detallado
- Persistencia robusta
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor

# Importar sistema robusto
from backend.satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
from backend.data_sanitizer import sanitize_response

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'scientific_capture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScientificDatasetCapture:
    """Capturador de dataset científico."""
    
    def __init__(self):
        self.integrator = RealDataIntegratorV2()
        self.db_conn = None
        self.analysis_version = "v2.1"
        
        # Conectar a BD
        self._connect_database()
    
    def _connect_database(self):
        """Conectar a PostgreSQL."""
        try:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            db_url = os.getenv("DATABASE_URL")
            if not db_url:
                raise ValueError("DATABASE_URL not configured")
            
            self.db_conn = psycopg2.connect(db_url)
            logger.info("✅ Database connected")
            
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    def setup_tables(self):
        """Crear tablas si no existen."""
        try:
            with self.db_conn.cursor() as cur:
                # Crear tabla de candidatos
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
                        region VARCHAR(200),
                        notes TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        analyzed_at TIMESTAMP WITH TIME ZONE,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                """)
                
                # Crear tabla de mediciones
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
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                    );
                """)
                
                # Crear índices
                cur.execute("CREATE INDEX IF NOT EXISTS idx_raw_measurements_candidate ON raw_measurements(candidate_id);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_raw_measurements_terrain ON raw_measurements(terrain_type);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_raw_measurements_instrument ON raw_measurements(instrument);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_raw_measurements_status ON raw_measurements(status);")
                
                self.db_conn.commit()
                logger.info("✅ Database tables ready")
                
        except Exception as e:
            logger.error(f"❌ Database setup failed: {e}")
            raise
    
    def insert_candidate(self, candidate: Dict[str, Any]) -> str:
        """Insertar candidato en BD."""
        try:
            candidate_id = f"{candidate['terrain']}_{candidate['name'].lower().replace(' ', '_')}"
            
            with self.db_conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO analysis_candidates 
                    (candidate_id, candidate_name, terrain_type, lat_min, lat_max, lon_min, lon_max, country)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (candidate_id) DO UPDATE SET
                        updated_at = NOW()
                    RETURNING candidate_id;
                """, (
                    candidate_id, candidate['name'], candidate['terrain'],
                    candidate['lat_min'], candidate['lat_max'],
                    candidate['lon_min'], candidate['lon_max'],
                    candidate.get('country', 'Unknown')
                ))
                
                result = cur.fetchone()
                self.db_conn.commit()
                
                return result[0] if result else candidate_id
                
        except Exception as e:
            logger.error(f"❌ Failed to insert candidate {candidate['name']}: {e}")
            return candidate_id
    
    def save_measurements(self, candidate_id: str, candidate: Dict[str, Any], 
                         batch_results: Dict[str, Any]):
        """Guardar mediciones en BD."""
        try:
            measurements_saved = 0
            successful_measurements = 0
            
            with self.db_conn.cursor() as cur:
                for instrument_data in batch_results.get('instruments', []):
                    # Sanitizar datos antes de guardar
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
                
                # Actualizar candidato
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
                
                logger.info(f"✅ Saved {measurements_saved} measurements for {candidate['name']}")
                logger.info(f"   Successful: {successful_measurements}, Coverage: {batch_results.get('coverage_score', 0.0):.1%}")
                
        except Exception as e:
            logger.error(f"❌ Failed to save measurements for {candidate['name']}: {e}")
            self.db_conn.rollback()
    
    async def capture_candidate(self, terrain: str, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Capturar datos de un candidato."""
        
        candidate_full = {**candidate, 'terrain': terrain}
        candidate_id = self.insert_candidate(candidate_full)
        
        logger.info(f"\n🔍 Capturing: {candidate['name']} ({terrain})")
        logger.info(f"   Coordinates: [{candidate['lat_min']:.4f}, {candidate['lat_max']:.4f}] x [{candidate['lon_min']:.4f}, {candidate['lon_max']:.4f}]")
        
        # Instrumentos por terreno
        terrain_instruments = {
            'desert': ['sentinel_2_ndvi', 'landsat_thermal', 'sar_backscatter', 'icesat2'],
            'forest': ['sentinel_2_ndvi', 'icesat2', 'sar_backscatter', 'modis_lst'],
            'mountain': ['icesat2', 'sentinel_2_ndvi', 'sar_backscatter', 'opentopography'],
            'coastal': ['sentinel_2_ndvi', 'sar_backscatter', 'modis_lst', 'copernicus_sst'],
            'polar': ['icesat2', 'sar_backscatter', 'nsidc_sea_ice', 'modis_lst']
        }
        
        instruments = terrain_instruments.get(terrain, ['sentinel_2_ndvi', 'icesat2', 'modis_lst'])
        
        try:
            # Marcar como en progreso
            with self.db_conn.cursor() as cur:
                cur.execute("""
                    UPDATE analysis_candidates SET 
                        analysis_status = 'IN_PROGRESS',
                        updated_at = NOW()
                    WHERE candidate_id = %s;
                """, (candidate_id,))
                self.db_conn.commit()
            
            # Capturar mediciones
            batch = await self.integrator.get_batch_measurements(
                instruments,
                candidate['lat_min'], candidate['lat_max'],
                candidate['lon_min'], candidate['lon_max']
            )
            
            # Generar reporte
            batch_results = batch.generate_report()
            
            # Guardar en BD
            self.save_measurements(candidate_id, candidate_full, batch_results)
            
            logger.info(f"✅ {candidate['name']}: Coverage {batch_results['coverage_score']:.1%}")
            
            return {
                'candidate_id': candidate_id,
                'success': True,
                'coverage_score': batch_results['coverage_score'],
                'measurements': batch_results['total_instruments'],
                'successful': batch_results['usable_instruments']
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to capture {candidate['name']}: {e}")
            
            # Marcar como fallido
            try:
                with self.db_conn.cursor() as cur:
                    cur.execute("""
                        UPDATE analysis_candidates SET 
                            analysis_status = 'FAILED',
                            notes = %s,
                            updated_at = NOW()
                        WHERE candidate_id = %s;
                    """, (str(e)[:500], candidate_id))
                    self.db_conn.commit()
            except:
                pass
            
            return {
                'candidate_id': candidate_id,
                'success': False,
                'error': str(e)
            }
    
    async def capture_all_terrains(self) -> Dict[str, Any]:
        """Capturar todos los terrenos."""
        
        logger.info("🚀 Starting Scientific Dataset Capture")
        logger.info("=" * 60)
        
        results = {
            'total_candidates': 0,
            'successful_candidates': 0,
            'failed_candidates': 0,
            'terrain_results': {},
            'start_time': datetime.now(),
            'end_time': None
        }
        
        for terrain, candidates in TERRAIN_CANDIDATES.items():
            logger.info(f"\n🌍 TERRAIN: {terrain.upper()}")
            logger.info("-" * 40)
            
            terrain_results = {
                'candidates': len(candidates),
                'successful': 0,
                'failed': 0,
                'coverage_scores': []
            }
            
            for candidate in candidates:
                result = await self.capture_candidate(terrain, candidate)
                
                results['total_candidates'] += 1
                
                if result['success']:
                    results['successful_candidates'] += 1
                    terrain_results['successful'] += 1
                    terrain_results['coverage_scores'].append(result['coverage_score'])
                else:
                    results['failed_candidates'] += 1
                    terrain_results['failed'] += 1
                
                # Pausa entre candidatos para no saturar APIs
                await asyncio.sleep(2)
            
            # Calcular estadísticas del terreno
            if terrain_results['coverage_scores']:
                terrain_results['avg_coverage'] = sum(terrain_results['coverage_scores']) / len(terrain_results['coverage_scores'])
            else:
                terrain_results['avg_coverage'] = 0.0
            
            results['terrain_results'][terrain] = terrain_results
            
            logger.info(f"   {terrain}: {terrain_results['successful']}/{terrain_results['candidates']} successful")
            logger.info(f"   Average coverage: {terrain_results['avg_coverage']:.1%}")
        
        results['end_time'] = datetime.now()
        results['duration_minutes'] = (results['end_time'] - results['start_time']).total_seconds() / 60
        
        # Guardar reporte final
        report_file = f"scientific_dataset_capture_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 FINAL RESULTS")
        logger.info("=" * 60)
        logger.info(f"Total candidates: {results['total_candidates']}")
        logger.info(f"Successful: {results['successful_candidates']}")
        logger.info(f"Failed: {results['failed_candidates']}")
        logger.info(f"Success rate: {results['successful_candidates']/results['total_candidates']*100:.1f}%")
        logger.info(f"Duration: {results['duration_minutes']:.1f} minutes")
        logger.info(f"Report saved: {report_file}")
        
        return results

# Datos de candidatos
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

async def main():
    """Función principal."""
    try:
        capture = ScientificDatasetCapture()
        capture.setup_tables()
        
        results = await capture.capture_all_terrains()
        
        if results['successful_candidates'] >= results['total_candidates'] * 0.6:
            print("\n🎉 SCIENTIFIC DATASET CAPTURE SUCCESSFUL!")
            print("ArcheoScope is now a reproducible scientific system!")
        else:
            print("\n⚠️ PARTIAL SUCCESS - Some candidates failed")
            print("But we have data to work with!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Capture failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
```

### FASE 2: ANÁLISIS OFFLINE (DESPUÉS)

#### 2.1 Análisis Estadístico

**Archivo**: `analyze_scientific_dataset.py`

```python
#!/usr/bin/env python3
"""
ArcheoScope Scientific Dataset Analysis
======================================

Análisis offline de datos capturados para:
- Normalización por terreno
- Detección de outliers
- Correlaciones cruzadas
- Ranking arqueológico
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class ScientificDatasetAnalyzer:
    """Analizador de dataset científico."""
    
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.measurements_df = None
        self.candidates_df = None
    
    def load_data(self):
        """Cargar datos desde BD."""
        # Cargar mediciones
        self.measurements_df = pd.read_sql("""
            SELECT * FROM raw_measurements 
            WHERE status IN ('SUCCESS', 'DEGRADED')
            ORDER BY candidate_id, instrument;
        """, self.db_conn)
        
        # Cargar candidatos
        self.candidates_df = pd.read_sql("""
            SELECT * FROM analysis_candidates 
            WHERE analysis_status = 'COMPLETED'
            ORDER BY terrain_type, candidate_name;
        """, self.db_conn)
    
    def normalize_by_terrain(self):
        """Normalizar valores por terreno."""
        normalized_data = []
        
        for terrain in self.measurements_df['terrain_type'].unique():
            terrain_data = self.measurements_df[
                self.measurements_df['terrain_type'] == terrain
            ].copy()
            
            for instrument in terrain_data['instrument'].unique():
                instrument_data = terrain_data[
                    terrain_data['instrument'] == instrument
                ]
                
                if len(instrument_data) > 1:
                    # Z-score normalization por terreno e instrumento
                    mean_val = instrument_data['value'].mean()
                    std_val = instrument_data['value'].std()
                    
                    if std_val > 0:
                        terrain_data.loc[
                            terrain_data['instrument'] == instrument, 
                            'normalized_value'
                        ] = (instrument_data['value'] - mean_val) / std_val
            
            normalized_data.append(terrain_data)
        
        return pd.concat(normalized_data, ignore_index=True)
    
    def detect_outliers(self, data):
        """Detectar outliers por terreno e instrumento."""
        outliers = []
        
        for terrain in data['terrain_type'].unique():
            for instrument in data['instrument'].unique():
                subset = data[
                    (data['terrain_type'] == terrain) & 
                    (data['instrument'] == instrument)
                ]
                
                if len(subset) >= 3:
                    z_scores = np.abs(stats.zscore(subset['value'].dropna()))
                    outlier_mask = z_scores > 2.5
                    
                    if outlier_mask.any():
                        outlier_data = subset[outlier_mask].copy()
                        outlier_data['outlier_score'] = z_scores[outlier_mask]
                        outliers.append(outlier_data)
        
        return pd.concat(outliers, ignore_index=True) if outliers else pd.DataFrame()
    
    def calculate_correlations(self, data):
        """Calcular correlaciones entre instrumentos."""
        # Pivot para tener instrumentos como columnas
        pivot_data = data.pivot_table(
            index=['candidate_id', 'terrain_type'],
            columns='instrument',
            values='value',
            aggfunc='mean'
        )
        
        # Correlaciones por terreno
        correlations = {}
        for terrain in pivot_data.index.get_level_values('terrain_type').unique():
            terrain_data = pivot_data[
                pivot_data.index.get_level_values('terrain_type') == terrain
            ]
            
            if len(terrain_data) > 2:
                corr_matrix = terrain_data.corr()
                correlations[terrain] = corr_matrix
        
        return correlations
    
    def generate_archaeological_ranking(self, data):
        """Generar ranking arqueológico basado en anomalías."""
        # Calcular score de anomalía por candidato
        candidate_scores = []
        
        for candidate_id in data['candidate_id'].unique():
            candidate_data = data[data['candidate_id'] == candidate_id]
            
            # Score basado en desviaciones de la norma del terreno
            anomaly_score = 0.0
            weight_sum = 0.0
            
            for _, row in candidate_data.iterrows():
                if pd.notna(row['normalized_value']):
                    # Peso por confianza del instrumento
                    weight = row['confidence'] if pd.notna(row['confidence']) else 0.5
                    
                    # Contribución de anomalía (valores extremos = más arqueológico)
                    anomaly_contribution = abs(row['normalized_value']) * weight
                    
                    anomaly_score += anomaly_contribution
                    weight_sum += weight
            
            if weight_sum > 0:
                final_score = anomaly_score / weight_sum
            else:
                final_score = 0.0
            
            candidate_info = self.candidates_df[
                self.candidates_df['candidate_id'] == candidate_id
            ].iloc[0]
            
            candidate_scores.append({
                'candidate_id': candidate_id,
                'candidate_name': candidate_info['candidate_name'],
                'terrain_type': candidate_info['terrain_type'],
                'country': candidate_info['country'],
                'anomaly_score': final_score,
                'coverage_score': candidate_info['coverage_score'],
                'measurements_count': len(candidate_data)
            })
        
        ranking_df = pd.DataFrame(candidate_scores)
        ranking_df = ranking_df.sort_values('anomaly_score', ascending=False)
        
        return ranking_df
    
    def generate_report(self):
        """Generar reporte completo."""
        print("📊 ArcheoScope Scientific Dataset Analysis Report")
        print("=" * 60)
        
        # Estadísticas generales
        print(f"Total measurements: {len(self.measurements_df)}")
        print(f"Total candidates: {len(self.candidates_df)}")
        print(f"Terrains analyzed: {self.candidates_df['terrain_type'].nunique()}")
        print(f"Instruments used: {self.measurements_df['instrument'].nunique()}")
        
        # Normalizar datos
        normalized_data = self.normalize_by_terrain()
        
        # Detectar outliers
        outliers = self.detect_outliers(normalized_data)
        print(f"\nOutliers detected: {len(outliers)}")
        
        # Correlaciones
        correlations = self.calculate_correlations(normalized_data)
        print(f"Terrain correlations calculated: {len(correlations)}")
        
        # Ranking arqueológico
        ranking = self.generate_archaeological_ranking(normalized_data)
        
        print("\n🏆 TOP 10 ARCHAEOLOGICAL CANDIDATES:")
        print("-" * 50)
        for i, row in ranking.head(10).iterrows():
            print(f"{i+1:2d}. {row['candidate_name']:20} ({row['terrain_type']:8}) "
                  f"Score: {row['anomaly_score']:.3f}")
        
        return {
            'normalized_data': normalized_data,
            'outliers': outliers,
            'correlations': correlations,
            'ranking': ranking
        }
```

## 🚀 EJECUCIÓN DEL PLAN

### Comandos para Esta Tarde:

```bash
# 1. Preparar entorno
pip install -r requirements-cds.txt

# 2. Configurar base de datos (si no está)
python setup_database_quick.py

# 3. Ejecutar captura científica
python capture_scientific_dataset.py

# 4. Monitorear progreso
tail -f scientific_capture_*.log
```

### Cronograma Estimado:

- **Setup inicial**: 10 minutos
- **Captura por terreno**: 15-20 minutos cada uno
- **Total estimado**: 90-120 minutos
- **Datos esperados**: ~125 mediciones (25 candidatos × ~5 instrumentos)

## 📈 BENEFICIOS INMEDIATOS

### 1. **Reproducibilidad Científica**
- Datos congelados en BD
- Versionado de análisis
- Trazabilidad completa

### 2. **Robustez del Sistema**
- Nunca aborta por un fallo
- Estados explícitos
- Coverage score visible

### 3. **Capacidad de Investigación**
- Análisis offline rápido
- Comparaciones entre terrenos
- Detección de patrones

### 4. **Base para Publicación**
- Dataset científico válido
- Metodología reproducible
- Resultados verificables

## 🎯 PRÓXIMOS PASOS POST-CAPTURA

1. **Análisis Estadístico** (1-2 días)
2. **Refinamiento de Algoritmos** (1 semana)
3. **Validación Cruzada** (2 semanas)
4. **Preparación de Paper** (1 mes)

---

**¡Este plan transforma ArcheoScope en un sistema científico de clase mundial!** 🏆