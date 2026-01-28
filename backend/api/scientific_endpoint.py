#!/usr/bin/env python3
"""
Endpoint Científico de Análisis - ArcheoScope
==============================================

Implementa el pipeline científico completo de 7 fases (0, A-F, G).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path
import os

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scientific_pipeline import ScientificPipeline
from satellite_connectors.real_data_integrator import RealDataIntegrator
from environment_classifier import EnvironmentClassifier
from validation.real_archaeological_validator import RealArchaeologicalValidator
import asyncpg

router = APIRouter()

# Inicializar componentes
integrator = RealDataIntegrator()
classifier = EnvironmentClassifier()
validator = RealArchaeologicalValidator()

# Pool de conexiones a BD (se inicializa en startup)
db_pool = None

async def init_db_pool():
    """Inicializar pool de conexiones a BD."""
    global db_pool
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        try:
            db_pool = await asyncpg.create_pool(database_url, min_size=2, max_size=10)
            print("[SCIENTIFIC_ENDPOINT] Pool de BD inicializado", flush=True)
        except Exception as e:
            print(f"[SCIENTIFIC_ENDPOINT] Error inicializando pool: {e}", flush=True)
            db_pool = None
    else:
        print("[SCIENTIFIC_ENDPOINT] DATABASE_URL no configurada", flush=True)

class ScientificAnalysisRequest(BaseModel):
    """Solicitud de análisis científico."""
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    region_name: str
    candidate_id: Optional[str] = None

@router.post("/analyze")
async def analyze_scientific(request: ScientificAnalysisRequest):
    """
    # Análisis Científico Completo - Pipeline de 7 Fases
    
    Ejecuta el pipeline científico determinístico completo para análisis arqueológico remoto.
    
    ## Fases del Pipeline
    
    - **Fase 0**: Enriquecimiento con datos históricos de BD
    - **Fase A**: Normalización por instrumento
    - **Fase B**: Detección de anomalía pura
    - **Fase C**: Análisis morfológico explícito
    - **Fase D**: Inferencia antropogénica (con freno de mano)
    - **Fase E**: Verificación de anti-patrones
    - **Fase F**: Validación contra sitios conocidos
    - **Fase G**: Salida científica
    
    ## Características
    
    - ✅ 100% Determinístico y reproducible
    - ✅ Mediciones con instrumentos reales (Sentinel, Landsat, ICESat-2, etc.)
    - ✅ Guardado automático en base de datos
    - ✅ Etiquetado epistemológico completo
    - ✅ Sin uso de IA en decisiones científicas
    
    ## Parámetros
    
    - `lat_min`, `lat_max`: Rango de latitud (grados decimales)
    - `lon_min`, `lon_max`: Rango de longitud (grados decimales)
    - `region_name`: Nombre descriptivo de la región
    - `candidate_id` (opcional): ID personalizado del candidato
    
    ## Respuesta
    
    Retorna análisis completo con:
    - Salida científica (probabilidad antropogénica, anomaly score, acción recomendada)
    - Contexto ambiental (tipo de ambiente, visibilidad arqueológica)
    - Mediciones instrumentales (valores, fuentes, modos de datos)
    - Información de la solicitud (coordenadas, región)
    
    ## Ejemplo
    
    ```json
    {
      "lat_min": 64.19,
      "lat_max": 64.21,
      "lon_min": -51.71,
      "lon_max": -51.69,
      "region_name": "Groenlandia Test"
    }
    ```
    """
    
    print("\n" + "="*80, flush=True)
    print("ENDPOINT /analyze-scientific ALCANZADO", flush=True)
    print(f"Región solicitada: {request.region_name}", flush=True)
    print(f"Bounds: [{request.lat_min}, {request.lat_max}] x [{request.lon_min}, {request.lon_max}]", flush=True)
    print("="*80 + "\n", flush=True)
    
    try:
        # Inicializar pipeline con BD y validator
        pipeline = ScientificPipeline(db_pool=db_pool, validator=validator)
        
        # Calcular centro
        center_lat = (request.lat_min + request.lat_max) / 2
        center_lon = (request.lon_min + request.lon_max) / 2
        
        # DETECTAR REGIÓN AUTOMÁTICAMENTE si no se proporcionó o es genérica
        detected_region = request.region_name
        if not request.region_name or request.region_name in ['Test Region', 'Interactive Analysis', 'Unknown']:
            print("[STEP 0] Detectando región automáticamente...", flush=True)
            from site_name_generator import site_name_generator
            
            # Usar geocoding reverso para obtener la región
            location_info = site_name_generator._reverse_geocode(center_lat, center_lon)
            if location_info:
                # Construir nombre de región descriptivo
                parts = []
                if location_info.get('state'):
                    parts.append(location_info['state'])
                if location_info.get('country'):
                    parts.append(location_info['country'])
                
                if parts:
                    detected_region = ' - '.join(parts)
                    print(f"  ✅ Región detectada: {detected_region}", flush=True)
                else:
                    detected_region = f"Lat {center_lat:.2f}, Lon {center_lon:.2f}"
                    print(f"  ⚠️ Región no identificada, usando coordenadas", flush=True)
            else:
                detected_region = f"Lat {center_lat:.2f}, Lon {center_lon:.2f}"
                print(f"  ⚠️ Geocoding falló, usando coordenadas", flush=True)
        else:
            print(f"[STEP 0] Usando región proporcionada: {detected_region}", flush=True)
        
        # 1. Clasificar ambiente
        print("[STEP 1] Clasificando ambiente...", flush=True)
        env_context = classifier.classify(center_lat, center_lon)
        print(f"  Ambiente: {env_context.environment_type.value}", flush=True)
        print(f"  Confianza: {env_context.confidence:.2f}", flush=True)
        
        # 2. Medir con instrumentos reales
        print("[STEP 2] Midiendo con TODOS los instrumentos disponibles para el ambiente...", flush=True)
        
        # USAR TODOS LOS INSTRUMENTOS DISPONIBLES (primarios + secundarios)
        # No hay jerarquía - todos son igualmente importantes
        all_instruments = list(set(env_context.primary_sensors + env_context.secondary_sensors))
        print(f"  Total instrumentos disponibles para {env_context.environment_type.value}: {len(all_instruments)}", flush=True)
        print(f"  Instrumentos: {', '.join(all_instruments)}", flush=True)
        
        measurements = []
        for instrument_name in all_instruments:
            try:
                measurement = await integrator.get_instrument_measurement(
                    instrument_name=instrument_name,
                    lat_min=request.lat_min,
                    lat_max=request.lat_max,
                    lon_min=request.lon_min,
                    lon_max=request.lon_max
                )
                # Solo agregar si la medición es válida (no None)
                if measurement is not None:
                    measurements.append(measurement)
                    print(f"  ✅ {instrument_name}: {measurement.get('value', 0):.3f}", flush=True)
                else:
                    print(f"  ❌ {instrument_name}: Sin datos", flush=True)
            except Exception as e:
                print(f"  ❌ {instrument_name}: Error - {e}", flush=True)
                continue
        
        print(f"\n  📊 RESUMEN: {len(measurements)}/{len(all_instruments)} instrumentos midieron exitosamente", flush=True)
        if len(measurements) > 0:
            print(f"  Instrumentos exitosos:", flush=True)
            for m in measurements:
                if m is not None:
                    print(f"    - {m.get('instrument_name', 'unknown')}: {m.get('value', 0):.3f} ({m.get('data_mode', 'unknown')})", flush=True)
        
        # 3. Preparar datos para pipeline
        raw_measurements = {
            'candidate_id': request.candidate_id or f"{detected_region}_{center_lat:.4f}_{center_lon:.4f}",
            'region_name': detected_region,  # Usar región detectada
            'center_lat': center_lat,
            'center_lon': center_lon,
            'environment_type': env_context.environment_type.value,
            'instruments_available': len(all_instruments)  # AGREGADO: número real de instrumentos disponibles
        }
        
        # Añadir mediciones (measurements son diccionarios)
        for m in measurements:
            if m is not None:
                instrument_name = m.get('instrument_name', 'unknown')
                raw_measurements[instrument_name] = {
                    'value': m.get('value', 0),
                    'threshold': m.get('threshold', 0),
                    'exceeds_threshold': m.get('exceeds_threshold', False),
                    'confidence': m.get('confidence', 0),
                    'data_mode': m.get('data_mode', 'unknown'),
                    'source': m.get('source', 'unknown')
                }
        
        # 4. Ejecutar pipeline científico (ASYNC con enriquecimiento de BD)
        print("[STEP 3] Ejecutando pipeline científico...", flush=True)
        result = await pipeline.analyze(
            raw_measurements,
            request.lat_min, request.lat_max,
            request.lon_min, request.lon_max
        )
        
        # 5. Añadir contexto adicional
        result['environment_context'] = {
            'environment_type': env_context.environment_type.value,
            'confidence': env_context.confidence,
            'available_instruments': list(set(env_context.primary_sensors + env_context.secondary_sensors)),  # TODOS los disponibles
            'archaeological_visibility': env_context.archaeological_visibility,
            'preservation_potential': env_context.preservation_potential
        }
        
        result['instrumental_measurements'] = [
            {
                'instrument_name': m.get('instrument_name', 'unknown'),
                'value': m.get('value', 0),
                'threshold': m.get('threshold', 0),
                'exceeds_threshold': m.get('exceeds_threshold', False),
                'confidence': m.get('confidence', 0),
                'data_mode': m.get('data_mode', 'unknown'),
                'source': m.get('source', 'unknown')
            }
            for m in measurements if m is not None  # Filtrar None
        ]
        
        result['request_info'] = {
            'region_name': detected_region,  # Usar región detectada
            'center_lat': center_lat,
            'center_lon': center_lon,
            'bounds': {
                'lat_min': request.lat_min,
                'lat_max': request.lat_max,
                'lon_min': request.lon_min,
                'lon_max': request.lon_max
            }
        }
        
        print("\n[SUCCESS] Análisis científico completado", flush=True)
        print(f"  Anomaly score: {result['scientific_output']['anomaly_score']:.3f}", flush=True)
        print(f"  Anthropic probability: {result['scientific_output']['anthropic_probability']:.3f}", flush=True)
        print(f"  Recommended action: {result['scientific_output']['recommended_action']}", flush=True)
        
        # 6. GUARDAR RESULTADOS EN BD (ESTRUCTURA COMPLETA)
        if db_pool:
            try:
                print("\n[BD] Guardando resultados en base de datos...", flush=True)
                
                # Importar generador de nombres
                from site_name_generator import site_name_generator
                
                # Generar nombre descriptivo del sitio
                site_info = site_name_generator.generate_name(
                    center_lat, 
                    center_lon, 
                    env_context.environment_type.value
                )
                
                print(f"[BD] Nombre generado: {site_info['name']}", flush=True)
                print(f"[BD] País: {site_info['country']}, Región: {site_info['region']}", flush=True)
                
                # Mapear environment type a ENUM de BD
                env_type_mapping = {
                    'desert': 'DESERT',
                    'semi_arid': 'SEMI_ARID',
                    'forest': 'FOREST',
                    'tropical_forest': 'FOREST',
                    'grassland': 'GRASSLAND',
                    'mountain': 'MOUNTAIN',
                    'glacier': 'GLACIER',
                    'polar_ice': 'POLAR_ICE',
                    'permafrost': 'PERMAFROST',
                    'shallow_sea': 'SHALLOW_SEA',
                    'deep_ocean': 'DEEP_OCEAN',
                    'coastal': 'COASTAL',
                    'lake': 'LAKE',
                    'river': 'RIVER',
                    'agricultural': 'AGRICULTURAL',
                    'urban': 'URBAN',
                    'unknown': 'UNKNOWN'
                }
                
                env_type_db = env_type_mapping.get(
                    env_context.environment_type.value, 
                    'UNKNOWN'
                )
                
                async with db_pool.acquire() as conn:
                    # 1. GUARDAR EN archaeological_sites (MISMA ESTRUCTURA QUE LOS 80K)
                    site_id = await conn.fetchval("""
                        INSERT INTO archaeological_sites 
                        (name, slug, "environmentType", "siteType", "confidenceLevel", 
                         "excavationStatus", "preservationStatus", latitude, longitude,
                         country, region, description, "scientificSignificance",
                         "isReferencesite", "isControlSite", "discoveryDate")
                        VALUES ($1, $2, $3::text::"EnvironmentType", $4::text::"SiteType", 
                                $5::text::"ConfidenceLevel", $6::text::"ExcavationStatus", 
                                $7::text::"PreservationStatus", $8, $9, $10, $11, $12, $13, $14, $15, NOW())
                        RETURNING id
                    """,
                        site_info['name'],
                        site_info['slug'],
                        env_type_db,
                        'UNKNOWN',  # siteType: UNKNOWN hasta clasificación
                        'CANDIDATE',  # confidenceLevel: CANDIDATE para nuevos sitios
                        'UNEXCAVATED',  # excavationStatus
                        'UNKNOWN',  # preservationStatus
                        center_lat,
                        center_lon,
                        site_info['country'],
                        site_info['region'],
                        f"Candidato detectado por ArcheoScope. Probabilidad antropogénica: {result['scientific_output']['anthropic_probability']:.3f}",
                        f"Anomaly score: {result['scientific_output']['anomaly_score']:.3f}. "
                        f"Instrumentos: {len(measurements)}/{len(all_instruments)}. "
                        f"Acción recomendada: {result['scientific_output']['recommended_action']}",
                        False,  # isReferencesite
                        result['scientific_output']['candidate_type'] == 'negative_reference'  # isControlSite
                    )
                    
                    print(f"[BD] ✅ Sitio guardado con ID: {site_id}", flush=True)
                    
                    # Generar explicación científica determinística
                    # Crear objeto ScientificOutput temporal para la explicación
                    from scientific_pipeline import ScientificOutput
                    
                    temp_output = ScientificOutput(
                        candidate_id=site_id,
                        anomaly_score=result['scientific_output']['anomaly_score'],
                        anthropic_probability=result['scientific_output']['anthropic_probability'],
                        confidence_interval=tuple(result['scientific_output']['confidence_interval']),
                        recommended_action=result['scientific_output']['recommended_action'],
                        notes=result['scientific_output']['notes'],
                        phases_completed=[],  # No necesario para la explicación
                        timestamp=result['scientific_output']['timestamp'],
                        coverage_raw=result['scientific_output']['coverage_raw'],
                        coverage_effective=result['scientific_output']['coverage_effective'],
                        instruments_measured=result['scientific_output']['instruments_measured'],
                        instruments_available=result['scientific_output']['instruments_available'],
                        candidate_type=result['scientific_output']['candidate_type'],
                        negative_reason=result['scientific_output'].get('negative_reason')
                    )
                    
                    scientific_explanation = pipeline.generate_scientific_explanation(
                        temp_output,
                        env_context.environment_type.value,
                        len(measurements),
                        len(all_instruments)
                    )
                    
                    print(f"[BD] 📝 Explicación generada: {scientific_explanation[:100]}...", flush=True)
                    
                    # 2. GUARDAR EN archaeological_candidate_analyses (análisis detallado)
                    analysis_id = await conn.fetchval("""
                        INSERT INTO archaeological_candidate_analyses 
                        (candidate_id, candidate_name, region, archaeological_probability, anomaly_score, 
                         result_type, recommended_action, environment_type, confidence_level,
                         instruments_measuring, instruments_total,
                         latitude, longitude, lat_min, lat_max, lon_min, lon_max,
                         scientific_explanation, explanation_type)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19)
                        RETURNING id
                    """, 
                        site_id,  # Usar ID del sitio
                        site_info['name'],
                        detected_region,  # Usar región detectada
                        result['scientific_output']['anthropic_probability'],
                        result['scientific_output']['anomaly_score'],
                        result['scientific_output']['candidate_type'],
                        result['scientific_output']['recommended_action'],
                        env_context.environment_type.value,
                        result['scientific_output']['confidence_interval'][0],  # Lower bound
                        len(measurements),  # Instrumentos que midieron
                        len(all_instruments),  # Total instrumentos disponibles
                        center_lat,  # Coordenadas del centro
                        center_lon,
                        request.lat_min,  # Bounding box
                        request.lat_max,
                        request.lon_min,
                        request.lon_max,
                        scientific_explanation,  # Explicación en lenguaje natural
                        'deterministic'  # Tipo de explicación
                    )
                    
                    print(f"[BD] ✅ Análisis guardado con ID: {analysis_id}", flush=True)
                    
                    # 3. GUARDAR MEDICIONES INSTRUMENTALES (exitosas)
                    for m in measurements:
                        if m is not None:
                            await conn.execute("""
                                INSERT INTO measurements 
                                (instrument_name, measurement_type, value, unit, data_mode, source, 
                                 latitude, longitude, region_name, environment_type, analysis_id)
                                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                            """,
                                m.get('instrument_name', 'unknown'),
                                'remote_sensing',
                                m.get('value', 0),
                                'various',
                                m.get('data_mode', 'unknown'),
                                m.get('source', 'unknown'),
                                center_lat,
                                center_lon,
                                detected_region,  # Usar región detectada
                                env_context.environment_type.value,
                                analysis_id  # Vincular con el análisis
                            )
                    
                    # 4. GUARDAR INSTRUMENTOS FALLIDOS (los que no midieron)
                    failed_instruments = set(all_instruments) - set([m.get('instrument_name') for m in measurements if m])
                    for instrument_name in failed_instruments:
                        await conn.execute("""
                            INSERT INTO measurements 
                            (instrument_name, measurement_type, value, unit, data_mode, source,
                             latitude, longitude, region_name, environment_type, analysis_id)
                            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                        """,
                            instrument_name,
                            'remote_sensing',
                            0.0,  # Valor 0 para fallidos
                            'none',
                            'NO_DATA',  # Marcar como sin datos
                            'failed',
                            center_lat,
                            center_lon,
                            detected_region,  # Usar región detectada
                            env_context.environment_type.value,
                            analysis_id  # Vincular con el análisis
                        )
                    
                    print(f"[BD] ✅ Guardado completo:", flush=True)
                    print(f"     - 1 sitio arqueológico (ID: {site_id})", flush=True)
                    print(f"     - 1 análisis científico", flush=True)
                    print(f"     - {len(measurements)} mediciones exitosas", flush=True)
                    print(f"     - {len(failed_instruments)} instrumentos fallidos registrados", flush=True)
                    
            except Exception as e:
                print(f"[BD] ⚠️ Error guardando en BD: {e}", flush=True)
                import traceback
                traceback.print_exc()
                # No fallar el análisis si falla el guardado
                # No fallar el análisis si falla el guardado
        else:
            print("[BD] ⚠️ Sin conexión a BD - resultados no persistidos", flush=True)
        
        return result
        
    except Exception as e:
        print(f"\n[ERROR] Error en análisis científico: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en análisis científico: {str(e)}")


@router.get("/analyses/recent", summary="Obtener análisis recientes")
async def get_recent_analyses(limit: int = 10):
    """
    # Consultar Análisis Recientes
    
    Retorna los últimos N análisis realizados, ordenados por fecha (más reciente primero).
    
    ## Parámetros
    
    - `limit` (opcional): Número máximo de análisis a retornar (default: 10, máximo: 100)
    
    ## Respuesta
    
    Lista de análisis con:
    - ID único del análisis
    - Nombre del candidato
    - Región analizada
    - Probabilidad antropogénica
    - Anomaly score
    - Tipo de resultado (positive_candidate, negative_reference, uncertain)
    - Acción recomendada
    - Tipo de ambiente
    - Nivel de confianza
    - Fecha de creación
    
    ## Uso
    
    Útil para:
    - Ver historial de análisis
    - Monitorear actividad del sistema
    - Identificar patrones en resultados
    """
    if not db_pool:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    
    try:
        async with db_pool.acquire() as conn:
            analyses = await conn.fetch("""
                SELECT 
                    id,
                    candidate_name,
                    region,
                    archaeological_probability,
                    anomaly_score,
                    result_type,
                    recommended_action,
                    environment_type,
                    confidence_level,
                    latitude,
                    longitude,
                    scientific_explanation,
                    explanation_type,
                    created_at
                FROM archaeological_candidate_analyses
                ORDER BY created_at DESC
                LIMIT $1
            """, limit)
            
            return {
                "total": len(analyses),
                "analyses": [
                    {
                        "id": row['id'],
                        "candidate_name": row['candidate_name'],
                        "region": row['region'],
                        "archaeological_probability": float(row['archaeological_probability']),
                        "anomaly_score": float(row['anomaly_score']),
                        "result_type": row['result_type'],
                        "recommended_action": row['recommended_action'],
                        "environment_type": row['environment_type'],
                        "confidence_level": float(row['confidence_level']),
                        "latitude": float(row['latitude']) if row['latitude'] is not None else None,
                        "longitude": float(row['longitude']) if row['longitude'] is not None else None,
                        "scientific_explanation": row['scientific_explanation'],
                        "explanation_type": row['explanation_type'],
                        "created_at": row['created_at'].isoformat()
                    }
                    for row in analyses
                ]
            }
    except Exception as e:
        print(f"[ERROR] Error consultando análisis: {e}", flush=True)
        raise HTTPException(status_code=500, detail=f"Error consultando análisis: {str(e)}")

@router.get("/analyses/{analysis_id}", summary="Obtener análisis por ID")
async def get_analysis_by_id(analysis_id: int):
    """
    # Consultar Análisis Específico
    
    Retorna un análisis completo por su ID, incluyendo todas las mediciones instrumentales asociadas.
    
    ## Parámetros
    
    - `analysis_id` (requerido): ID único del análisis
    
    ## Respuesta
    
    Objeto con tres secciones:
    
    ### 1. Analysis
    - Datos completos del análisis científico
    - Probabilidades, scores, acciones recomendadas
    - Metadatos (ambiente, confianza, fecha)
    - **Instrumentos usados** (instruments_measured/instruments_total)
    
    ### 2. Measurements
    - Lista de mediciones instrumentales EXITOSAS
    - Nombre del instrumento, valor, unidad, modo de datos
    
    ### 3. Failed Instruments
    - Lista de instrumentos que NO midieron
    - Útil para entender cobertura incompleta
    
    ## Errores
    
    - `404`: Análisis no encontrado
    - `503`: Base de datos no disponible
    """
    if not db_pool:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    
    try:
        async with db_pool.acquire() as conn:
            # Obtener análisis
            analysis = await conn.fetchrow("""
                SELECT 
                    id,
                    candidate_name,
                    region,
                    archaeological_probability,
                    anomaly_score,
                    result_type,
                    recommended_action,
                    environment_type,
                    confidence_level,
                    instruments_measuring,
                    instruments_total,
                    latitude,
                    longitude,
                    lat_min,
                    lat_max,
                    lon_min,
                    lon_max,
                    scientific_explanation,
                    explanation_type,
                    created_at
                FROM archaeological_candidate_analyses
                WHERE id = $1
            """, analysis_id)
            
            if not analysis:
                raise HTTPException(status_code=404, detail=f"Análisis {analysis_id} no encontrado")
            
            # Obtener mediciones EXITOSAS (data_mode != NO_DATA)
            # Usar analysis_id para obtener exactamente las mediciones de este análisis
            measurements = await conn.fetch("""
                SELECT 
                    instrument_name,
                    value,
                    unit,
                    data_mode,
                    source,
                    latitude,
                    longitude,
                    measurement_timestamp
                FROM measurements
                WHERE analysis_id = $1
                  AND data_mode != 'NO_DATA'
                ORDER BY measurement_timestamp DESC
            """, analysis_id)
            
            # Obtener instrumentos FALLIDOS (data_mode = NO_DATA)
            failed_instruments = await conn.fetch("""
                SELECT 
                    instrument_name,
                    source,
                    measurement_timestamp
                FROM measurements
                WHERE analysis_id = $1
                  AND data_mode = 'NO_DATA'
                ORDER BY measurement_timestamp DESC
            """, analysis_id)
            
            return {
                "analysis": {
                    "id": analysis['id'],
                    "candidate_name": analysis['candidate_name'],
                    "region": analysis['region'],
                    "archaeological_probability": float(analysis['archaeological_probability']),
                    "anomaly_score": float(analysis['anomaly_score']),
                    "result_type": analysis['result_type'],
                    "recommended_action": analysis['recommended_action'],
                    "environment_type": analysis['environment_type'],
                    "confidence_level": float(analysis['confidence_level']),
                    "instruments_measured": analysis['instruments_measuring'],
                    "instruments_total": analysis['instruments_total'],
                    "coordinates": {
                        "center": {
                            "latitude": float(analysis['latitude']) if analysis['latitude'] is not None else None,
                            "longitude": float(analysis['longitude']) if analysis['longitude'] is not None else None
                        },
                        "bounds": {
                            "lat_min": float(analysis['lat_min']) if analysis['lat_min'] is not None else None,
                            "lat_max": float(analysis['lat_max']) if analysis['lat_max'] is not None else None,
                            "lon_min": float(analysis['lon_min']) if analysis['lon_min'] is not None else None,
                            "lon_max": float(analysis['lon_max']) if analysis['lon_max'] is not None else None
                        }
                    },
                    "scientific_explanation": analysis['scientific_explanation'],
                    "explanation_type": analysis['explanation_type'],
                    "created_at": analysis['created_at'].isoformat()
                },
                "measurements": [
                    {
                        "instrument_name": row['instrument_name'],
                        "value": float(row['value']),
                        "unit": row['unit'],
                        "data_mode": row['data_mode'],
                        "source": row['source'],
                        "latitude": float(row['latitude']),
                        "longitude": float(row['longitude']),
                        "timestamp": row['measurement_timestamp'].isoformat()
                    }
                    for row in measurements
                ],
                "failed_instruments": [
                    {
                        "instrument_name": row['instrument_name'],
                        "reason": "NO_DATA",
                        "source": row['source'],
                        "timestamp": row['measurement_timestamp'].isoformat()
                    }
                    for row in failed_instruments
                ]
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error consultando análisis {analysis_id}: {e}", flush=True)
        raise HTTPException(status_code=500, detail=f"Error consultando análisis: {str(e)}")

@router.get("/analyses/by-region/{region_name}", summary="Obtener análisis por región")
async def get_analyses_by_region(region_name: str, limit: int = 10):
    """
    # Consultar Análisis por Región
    
    Retorna todos los análisis realizados en una región específica.
    
    ## Parámetros
    
    - `region_name` (requerido): Nombre de la región (ej: "Groenlandia Test", "Sahara Norte")
    - `limit` (opcional): Número máximo de análisis a retornar (default: 10)
    
    ## Respuesta
    
    Objeto con:
    - `region`: Nombre de la región consultada
    - `total`: Número de análisis encontrados
    - `analyses`: Lista de análisis ordenados por fecha
    
    ## Uso
    
    Útil para:
    - Comparar múltiples análisis de la misma región
    - Evaluar cambios temporales
    - Validar consistencia de resultados
    - Análisis de series temporales
    
    ## Ejemplo
    
    ```
    GET /api/scientific/analyses/by-region/Groenlandia%20Test?limit=5
    ```
    """
    if not db_pool:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    
    try:
        async with db_pool.acquire() as conn:
            analyses = await conn.fetch("""
                SELECT 
                    id,
                    candidate_name,
                    region,
                    archaeological_probability,
                    anomaly_score,
                    result_type,
                    recommended_action,
                    environment_type,
                    confidence_level,
                    created_at
                FROM archaeological_candidate_analyses
                WHERE region = $1
                ORDER BY created_at DESC
                LIMIT $2
            """, region_name, limit)
            
            return {
                "region": region_name,
                "total": len(analyses),
                "analyses": [
                    {
                        "id": row['id'],
                        "candidate_name": row['candidate_name'],
                        "archaeological_probability": float(row['archaeological_probability']),
                        "anomaly_score": float(row['anomaly_score']),
                        "result_type": row['result_type'],
                        "recommended_action": row['recommended_action'],
                        "environment_type": row['environment_type'],
                        "confidence_level": float(row['confidence_level']),
                        "created_at": row['created_at'].isoformat()
                    }
                    for row in analyses
                ]
            }
    except Exception as e:
        print(f"[ERROR] Error consultando análisis de región {region_name}: {e}", flush=True)
        raise HTTPException(status_code=500, detail=f"Error consultando análisis: {str(e)}")


@router.get("/sites/all", summary="Listar todos los sitios arqueológicos")
async def get_all_archaeological_sites(
    page: int = 1,
    page_size: int = 100,
    country: Optional[str] = None,
    site_type: Optional[str] = None,
    environment_type: Optional[str] = None,
    confidence_level: Optional[str] = None,
    search: Optional[str] = None
):
    """
    # Listar Todos los Sitios Arqueológicos
    
    Retorna todos los sitios arqueológicos de la base de datos con paginación y filtros.
    
    ## Parámetros de Paginación
    
    - `page`: Número de página (default: 1)
    - `page_size`: Tamaño de página (default: 100, max: 1000)
    
    ## Filtros Opcionales
    
    - `country`: Filtrar por país (ej: "México", "Perú")
    - `site_type`: Filtrar por tipo de sitio (SETTLEMENT, MONUMENT, BURIAL, etc.)
    - `environment_type`: Filtrar por ambiente (DESERT, MOUNTAIN, FOREST, etc.)
    - `confidence_level`: Filtrar por nivel de confianza (CONFIRMED, PROBABLE, POSSIBLE)
    - `search`: Búsqueda por nombre (case-insensitive)
    
    ## Respuesta
    
    Retorna:
    - `total`: Total de sitios en la BD
    - `page`: Página actual
    - `page_size`: Tamaño de página
    - `total_pages`: Total de páginas
    - `sites`: Array de sitios con información completa
    
    ## Ejemplo
    
    ```
    GET /api/scientific/sites/all?page=1&page_size=50&country=México
    ```
    """
    
    if not db_pool:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    
    # Validar page_size
    if page_size > 1000:
        page_size = 1000
    if page_size < 1:
        page_size = 100
    
    if page < 1:
        page = 1
    
    try:
        async with db_pool.acquire() as conn:
            # Construir query con filtros
            where_clauses = []
            params = []
            param_count = 1
            
            if country:
                where_clauses.append(f"country = ${param_count}")
                params.append(country)
                param_count += 1
            
            if site_type:
                where_clauses.append(f'"siteType" = ${param_count}')
                params.append(site_type)
                param_count += 1
            
            if environment_type:
                where_clauses.append(f'"environmentType" = ${param_count}')
                params.append(environment_type)
                param_count += 1
            
            if confidence_level:
                where_clauses.append(f'"confidenceLevel" = ${param_count}')
                params.append(confidence_level)
                param_count += 1
            
            if search:
                where_clauses.append(f"name ILIKE ${param_count}")
                params.append(f"%{search}%")
                param_count += 1
            
            where_sql = " AND ".join(where_clauses) if where_clauses else "TRUE"
            
            # Contar total de sitios (con filtros)
            count_query = f"SELECT COUNT(*) FROM archaeological_sites WHERE {where_sql}"
            total = await conn.fetchval(count_query, *params)
            
            # Calcular offset
            offset = (page - 1) * page_size
            
            # Obtener sitios paginados
            sites_query = f"""
                SELECT 
                    id,
                    name,
                    slug,
                    "siteType",
                    "environmentType",
                    "confidenceLevel",
                    latitude,
                    longitude,
                    country,
                    region,
                    description,
                    "scientificSignificance",
                    "isControlSite",
                    "discoveryDate",
                    "createdAt",
                    "updatedAt"
                FROM archaeological_sites
                WHERE {where_sql}
                ORDER BY "createdAt" DESC
                LIMIT ${param_count} OFFSET ${param_count + 1}
            """
            params.extend([page_size, offset])
            
            sites = await conn.fetch(sites_query, *params)
            
            # Calcular total de páginas
            total_pages = (total + page_size - 1) // page_size
            
            return {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "filters": {
                    "country": country,
                    "site_type": site_type,
                    "environment_type": environment_type,
                    "confidence_level": confidence_level,
                    "search": search
                },
                "sites": [
                    {
                        "id": str(row['id']),
                        "name": row['name'],
                        "slug": row['slug'],
                        "site_type": row['siteType'],
                        "environment_type": row['environmentType'],
                        "confidence_level": row['confidenceLevel'],
                        "coordinates": {
                            "latitude": float(row['latitude']) if row['latitude'] is not None else None,
                            "longitude": float(row['longitude']) if row['longitude'] is not None else None
                        },
                        "location": {
                            "country": row['country'],
                            "region": row['region']
                        },
                        "description": row['description'],
                        "scientific_significance": row['scientificSignificance'],
                        "is_control_site": row['isControlSite'],
                        "discovery_date": row['discoveryDate'].isoformat() if row['discoveryDate'] else None,
                        "created_at": row['createdAt'].isoformat() if row['createdAt'] else None,
                        "updated_at": row['updatedAt'].isoformat() if row['updatedAt'] else None
                    }
                    for row in sites
                ]
            }
            
    except Exception as e:
        print(f"[ERROR] Error listando sitios: {e}", flush=True)
        raise HTTPException(status_code=500, detail=f"Error listando sitios: {str(e)}")


@router.get("/sites/stats", summary="Estadísticas de sitios arqueológicos")
async def get_sites_statistics():
    """
    # Estadísticas de Sitios Arqueológicos
    
    Retorna estadísticas agregadas de todos los sitios en la base de datos.
    
    ## Respuesta
    
    Retorna:
    - `total_sites`: Total de sitios en la BD
    - `by_country`: Distribución por país (top 20)
    - `by_site_type`: Distribución por tipo de sitio
    - `by_environment`: Distribución por tipo de ambiente
    - `by_confidence`: Distribución por nivel de confianza
    - `control_sites`: Número de sitios de control
    - `recent_additions`: Sitios agregados en los últimos 7 días
    """
    
    if not db_pool:
        raise HTTPException(status_code=503, detail="Base de datos no disponible")
    
    try:
        async with db_pool.acquire() as conn:
            # Total de sitios
            total = await conn.fetchval('SELECT COUNT(*) FROM archaeological_sites')
            
            # Por país (top 20)
            by_country = await conn.fetch("""
                SELECT country, COUNT(*) as count
                FROM archaeological_sites
                WHERE country IS NOT NULL
                GROUP BY country
                ORDER BY count DESC
                LIMIT 20
            """)
            
            # Por tipo de sitio
            by_site_type = await conn.fetch("""
                SELECT "siteType", COUNT(*) as count
                FROM archaeological_sites
                GROUP BY "siteType"
                ORDER BY count DESC
            """)
            
            # Por ambiente
            by_environment = await conn.fetch("""
                SELECT "environmentType", COUNT(*) as count
                FROM archaeological_sites
                GROUP BY "environmentType"
                ORDER BY count DESC
            """)
            
            # Por confianza
            by_confidence = await conn.fetch("""
                SELECT "confidenceLevel", COUNT(*) as count
                FROM archaeological_sites
                GROUP BY "confidenceLevel"
                ORDER BY count DESC
            """)
            
            # Sitios de control
            control_sites = await conn.fetchval("""
                SELECT COUNT(*) FROM archaeological_sites
                WHERE "isControlSite" = TRUE
            """)
            
            # Adiciones recientes (últimos 7 días)
            recent = await conn.fetchval("""
                SELECT COUNT(*) FROM archaeological_sites
                WHERE "createdAt" >= NOW() - INTERVAL '7 days'
            """)
            
            return {
                "total_sites": total,
                "by_country": [
                    {"country": row['country'], "count": row['count']}
                    for row in by_country
                ],
                "by_site_type": [
                    {"site_type": row['siteType'], "count": row['count']}
                    for row in by_site_type
                ],
                "by_environment": [
                    {"environment_type": row['environmentType'], "count": row['count']}
                    for row in by_environment
                ],
                "by_confidence": [
                    {"confidence_level": row['confidenceLevel'], "count": row['count']}
                    for row in by_confidence
                ],
                "control_sites": control_sites,
                "recent_additions": recent
            }
            
    except Exception as e:
        print(f"[ERROR] Error obteniendo estadísticas: {e}", flush=True)
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")
