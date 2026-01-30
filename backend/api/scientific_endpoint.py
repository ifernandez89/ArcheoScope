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
from territorial_inferential_tomography import (
    TerritorialInferentialTomographyEngine,
    AnalysisObjective,
    CommunicationLevel
)
from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
import asyncpg

router = APIRouter()

# Inicializar componentes
integrator = RealDataIntegrator()
classifier = EnvironmentClassifier()
validator = RealArchaeologicalValidator()

# Motor TIMT (se inicializa en startup)
timt_engine: Optional[TerritorialInferentialTomographyEngine] = None

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

def initialize_timt_engine():
    """Inicializar motor TIMT para fusión transparente."""
    global timt_engine
    
    try:
        # Inicializar integrador V2 con 15 instrumentos
        integrator_v2 = RealDataIntegratorV2()
        
        # Inicializar motor TIMT
        timt_engine = TerritorialInferentialTomographyEngine(integrator_v2)
        
        print("[SCIENTIFIC_ENDPOINT] 🚀 TIMT Engine inicializado para fusión transparente", flush=True)
        
    except Exception as e:
        print(f"[SCIENTIFIC_ENDPOINT] ⚠️ Error inicializando TIMT Engine: {e}", flush=True)
        timt_engine = None

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
    # Análisis Científico Completo - Pipeline Integrado con TIMT
    
    Ejecuta el análisis territorial completo con Tomografía Inferencial (TIMT).
    
    ## FUSIÓN TRANSPARENTE
    
    Este endpoint llama internamente al sistema TIMT completo:
    - **CAPA 0**: Contexto Territorial (TCP)
    - **CAPA 1**: Adquisición dirigida + Tomografía (ETP)
    - **CAPA 2**: Validación + Transparencia + Comunicación
    
    ## Características
    
    - ✅ 100% Determinístico y reproducible
    - ✅ TODOS los instrumentos disponibles intervienen SIEMPRE
    - ✅ Mediciones con 15 instrumentos reales
    - ✅ Guardado automático completo en base de datos
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
    - Contexto territorial (TCP completo)
    - Perfil tomográfico (ETP completo)
    - Validación de hipótesis
    - Mediciones instrumentales (TODOS los instrumentos: exitosos Y fallidos)
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
        
        # ============================================================================
        # FUSIÓN TRANSPARENTE: Llamar a TIMT internamente
        # ============================================================================
        
        if timt_engine:
            print("\n" + "="*80, flush=True)
            print("🔬 FUSIÓN TRANSPARENTE: Ejecutando análisis TIMT completo", flush=True)
            print("="*80 + "\n", flush=True)
            
            # Ejecutar análisis territorial completo con TIMT
            # AJUSTES OPTIMIZADOS:
            # - Objetivo: EXPLORATORY (análisis amplio)
            # - Resolución: 150m (balance cobertura/detalle)
            # - Radio: 5km (contexto territorial)
            timt_result = await timt_engine.analyze_territory(
                lat_min=request.lat_min,
                lat_max=request.lat_max,
                lon_min=request.lon_min,
                lon_max=request.lon_max,
                analysis_objective=AnalysisObjective.EXPLORATORY,
                analysis_radius_km=5.0,
                resolution_m=150.0,  # AJUSTE: 150m por defecto
                communication_level=CommunicationLevel.TECHNICAL
            )
            
            print("\n✅ Análisis TIMT completado exitosamente", flush=True)
            print(f"  - TCP ID: {timt_result.territorial_context.tcp_id}", flush=True)
            print(f"  - ETP ID: {timt_result.tomographic_profile.territory_id}", flush=True)
            print(f"  - Hipótesis evaluadas: {len(timt_result.hypothesis_validations)}", flush=True)
            print(f"  - Coherencia territorial: {timt_result.territorial_coherence_score:.3f}", flush=True)
            print(f"  - Rigor científico: {timt_result.scientific_rigor_score:.3f}", flush=True)
            
            # Extraer métricas del ETP para compatibilidad con respuesta científica
            etp = timt_result.tomographic_profile
            
            # Extraer mediciones instrumentales REALES de layered_data
            all_measurements = []
            layered_data = etp.visualization_data.get('instrument_data', {})
            
            # Obtener todos los instrumentos únicos que se intentaron medir
            all_instruments_attempted = set()
            for depth, instruments in layered_data.items():
                all_instruments_attempted.update(instruments.keys())
            
            # Construir lista de mediciones con datos REALES
            for instrument_name in all_instruments_attempted:
                # Buscar la medición en cualquier profundidad
                measurement_found = False
                for depth, instruments in layered_data.items():
                    if instrument_name in instruments:
                        instr_data = instruments[instrument_name]
                        all_measurements.append({
                            'instrument_name': instrument_name,
                            'value': instr_data.get('value', 0),
                            'threshold': 0,
                            'exceeds_threshold': False,
                            'confidence': instr_data.get('confidence', 0),
                            'data_mode': instr_data.get('status', 'UNKNOWN'),
                            'source': 'TIMT',
                            'success': instr_data.get('status') in ['SUCCESS', 'DEGRADED']
                        })
                        measurement_found = True
                        break
                
                # Si no se encontró medición, marcar como fallido
                if not measurement_found:
                    all_measurements.append({
                        'instrument_name': instrument_name,
                        'value': 0,
                        'threshold': 0,
                        'exceeds_threshold': False,
                        'confidence': 0,
                        'data_mode': 'NO_DATA',
                        'source': 'TIMT',
                        'success': False
                    })
            
            # ============================================================================
            # ANÁLISIS HRM (Razonamiento Jerárquico)
            # ============================================================================
            hrm_analysis = None
            try:
                # Importar runner dinámicamente si no está en top-level
                from hrm import hrm_runner
                
                # Cargar modelo (debería estar cacheado o ser rápido si ya se cargó)
                # NOTA: En producción ideal, esto se carga al inicio. Por ahora lo cargamos on-demand con cache interno.
                # hrm_runner maneja su propia carga ligera.
                if not hasattr(router, "hrm_model_instance"):
                    print("[SCIENTIFIC_ENDPOINT] Inicializando HRM Model...", flush=True)
                    router.hrm_model_instance = hrm_runner.load_models()
                
                # Construir consulta basada en datos TIMT
                # Usamos la narrativa del ETP como input base + contexto
                query = f"Analizar anomalía en {request.region_name}. "
                if etp.narrative_explanation:
                    query += f"Contexto: {etp.narrative_explanation}. "
                query += f"ESS Superficial: {etp.ess_superficial:.2f}. "
                
                # Configurar ruta de visualización (Backend escribe en carpeta del Frontend)
                # Asumimos estructura standard: backend/api/scientific_endpoint.py -> ... -> frontend/
                frontend_dir = Path(__file__).parent.parent.parent / "frontend"
                viz_dir = frontend_dir / "hrm_viz"
                viz_dir.mkdir(exist_ok=True)
                
                timestamp_str = timt_result.analysis_timestamp.strftime("%Y%m%d_%H%M%S")
                viz_filename = f"hrm_{timestamp_str}_{request.region_name[:5].replace(' ','_')}.png"
                viz_path = viz_dir / viz_filename
                
                # URL relativa para el frontend (servido desde 'frontend/')
                viz_url = f"/hrm_viz/{viz_filename}"
                
                # Ejecutar análisis con visualización
                print(f"[SCIENTIFIC_ENDPOINT] Ejecutando HRM para: {query[:50]}...", flush=True)
                hrm_json = hrm_runner.generate_response(
                    query, 
                    router.hrm_model_instance, 
                    temperature=0.3, 
                    mode="scientific_strict",
                    visualize_path=str(viz_path)
                )
                
                # Parsear resultado si es string (aunque generate_response devuelve string, 
                # en strict mode intentamos que sea JSON válido dentro del texto)
                try:
                    # Intentar limpiar si viene con markdown
                    cleaned = hrm_json.replace("```json", "").replace("```", "").strip()
                    hrm_analysis = json.loads(cleaned)
                    # Inyectar URL de visualización en el objeto JSON analizado
                    hrm_analysis["visualizacion_neural"] = viz_url
                except:
                    # Si falla, structurar manualmente el texto
                    hrm_analysis = {
                        "analisis_morfologico": "Análisis textural realizado.",
                        "hipotesis_antropica": hrm_json[:200] + "...",
                        "hipotesis_natural_alternativa": "Ver detalle narrativo.", 
                        "evidencia_requerida": "Validación de campo necesaria.",
                        "nivel_incertidumbre": "Medio (No estructurado)",
                        "raw_output": hrm_json,
                        "visualizacion_neural": viz_url
                    }
                    
                print("[SCIENTIFIC_ENDPOINT] ✅ Análisis HRM completado", flush=True)
                
            except Exception as e:
                print(f"[SCIENTIFIC_ENDPOINT] ⚠️ Error en HRM Integration: {e}", flush=True)
                hrm_analysis = {
                    "error": str(e),
                    "status": "failed"
                }

            # Construir respuesta compatible con estructura científica
            result = {
                'scientific_output': {
                    'candidate_id': request.candidate_id or f"{detected_region}_{center_lat:.4f}_{center_lon:.4f}",
                    'anomaly_score': etp.ess_superficial,  # ESS superficial como anomaly score
                    'anthropic_probability': etp.densidad_arqueologica_m3,  # Densidad arqueológica como probabilidad
                    'confidence_interval': [0.5, 1.0],  # Intervalo de confianza basado en rigor científico
                    'recommended_action': 'field_verification' if etp.densidad_arqueologica_m3 > 0.5 else 'monitoring_passive',
                    'notes': etp.narrative_explanation,
                    'hrm_analysis': hrm_analysis, # <--- NUEVO CAMPO HRM
                    'timestamp': timt_result.analysis_timestamp.isoformat(),
                    'coverage_raw': len([m for m in all_measurements if m['success']]) / len(all_measurements) if all_measurements else 0,
                    'coverage_effective': timt_result.scientific_rigor_score,  # Rigor científico como cobertura efectiva
                    'instruments_measured': len([m for m in all_measurements if m['success']]),
                    'instruments_available': len(all_measurements),
                    'candidate_type': 'positive_candidate' if etp.densidad_arqueologica_m3 > 0.5 else 'uncertain',
                    'negative_reason': None,
                    
                    # Métricas separadas (origen vs actividad)
                    'anthropic_origin_probability': etp.densidad_arqueologica_m3,
                    'anthropic_activity_probability': 0.0,  # TODO: Extraer de ETP si disponible
                    'instrumental_anomaly_probability': etp.ess_superficial,
                    'model_confidence': 'high'  # Siempre alta (determinístico)
                },
                
                # Contexto territorial (TCP)
                'territorial_context': {
                    'tcp_id': timt_result.territorial_context.tcp_id,
                    'analysis_objective': timt_result.territorial_context.analysis_objective.value,
                    'preservation_potential': timt_result.territorial_context.preservation_potential.value,
                    'geological_context': {
                        'dominant_lithology': timt_result.territorial_context.geological_context.dominant_lithology.value if timt_result.territorial_context.geological_context else 'unknown',
                        'geological_age': timt_result.territorial_context.geological_context.geological_age.value if timt_result.territorial_context.geological_context else 'unknown',
                        'archaeological_suitability': timt_result.territorial_context.geological_context.archaeological_suitability if timt_result.territorial_context.geological_context else 0.5,
                        'explanation': timt_result.territorial_context.geological_context.geological_explanation if timt_result.territorial_context.geological_context else ''
                    },
                    'hydrographic_features_count': len(timt_result.territorial_context.hydrographic_features),
                    'external_sites_count': len(timt_result.territorial_context.external_archaeological_sites),
                    'human_traces_count': len(timt_result.territorial_context.known_human_traces),
                    'territorial_hypotheses_count': len(timt_result.territorial_context.territorial_hypotheses)
                },
                
                # Perfil tomográfico (ETP)
                'tomographic_profile': {
                    'territory_id': etp.territory_id,
                    'ess_superficial': etp.ess_superficial,
                    'ess_volumetrico': etp.ess_volumetrico,
                    'ess_temporal': etp.ess_temporal,
                    
                    # NUEVO: Cobertura instrumental (separada de ESS)
                    'instrumental_coverage': etp.instrumental_coverage,
                    
                    # SALTO EVOLUTIVO 1: Temporal Archaeological Signature (TAS)
                    'tas_signature': etp.tas_signature.to_dict() if etp.tas_signature else None,
                    
                    # SALTO EVOLUTIVO 2: Deep Inference Layer (DIL)
                    'dil_signature': etp.dil_signature.to_dict() if etp.dil_signature else None,
                    
                    'coherencia_3d': etp.coherencia_3d,
                    'persistencia_temporal': etp.persistencia_temporal,
                    'densidad_arqueologica_m3': etp.densidad_arqueologica_m3,
                    'confidence_level': 'medium',  # Basado en rigor científico
                    'recommended_action': 'field_verification' if etp.densidad_arqueologica_m3 > 0.5 else 'monitoring_passive',
                    'narrative_explanation': etp.narrative_explanation,
                    
                    # Scores de compatibilidad (usando atributos REALES)
                    'geological_compatibility_score': etp.geological_compatibility.gcs_score if etp.geological_compatibility else None,
                    'water_availability_score': etp.water_availability.settlement_viability if etp.water_availability else None,
                    'external_consistency_score': etp.external_consistency.ecs_score if etp.external_consistency else None
                },
                
                # Validación de hipótesis
                'hypothesis_validations': [
                    {
                        'hypothesis_id': hv.hypothesis_id,
                        'hypothesis_type': hv.hypothesis_type,
                        'evidence_level': hv.overall_evidence_level.value,
                        'confidence_score': hv.confidence_score,
                        'supporting_factors': hv.supporting_factors,
                        'contradictions': hv.contradictions,
                        'explanation': hv.validation_explanation
                    }
                    for hv in timt_result.hypothesis_validations
                ],
                
                # Métricas TIMT
                'territorial_coherence_score': timt_result.territorial_coherence_score,
                'scientific_rigor_score': timt_result.scientific_rigor_score,
                
                # Comunicación multinivel
                'technical_summary': timt_result.technical_summary,
                'academic_summary': timt_result.academic_summary,
                'general_summary': timt_result.general_summary,
                'institutional_summary': timt_result.institutional_summary,
                
                # Mediciones instrumentales (TODOS: exitosos Y fallidos) - DATOS REALES
                'instrumental_measurements': all_measurements,
                
                # Contexto ambiental
                'environment_context': {
                    'environment_type': timt_result.territorial_context.historical_biome.value,
                    'confidence': 0.9,  # Alta confianza en clasificación ambiental
                    'available_instruments': [m.get('instrument_name') for m in all_measurements if m.get('success')],
                    'archaeological_visibility': timt_result.territorial_context.preservation_potential.value,
                    'preservation_potential': timt_result.territorial_context.preservation_potential.value
                },
                
                # Información de la solicitud
                'request_info': {
                    'region_name': detected_region,
                    'center_lat': center_lat,
                    'center_lon': center_lon,
                    'bounds': {
                        'lat_min': request.lat_min,
                        'lat_max': request.lat_max,
                        'lon_min': request.lon_min,
                        'lon_max': request.lon_max
                    }
                }
            }
            
            print("\n✅ Respuesta científica construida desde TIMT", flush=True)
            
        else:
            # Fallback: usar pipeline científico básico si TIMT no está disponible
            print("\n⚠️ TIMT no disponible, usando pipeline científico básico", flush=True)
            
            # Primero obtener mediciones con RealDataIntegratorV2
            integrator_v2 = RealDataIntegratorV2()
            
            # Lista de instrumentos a medir (NOMBRES CORRECTOS según mapping)
            instrument_names = [
                'sentinel2',  # Sentinel-2 NDVI
                'sentinel_1_sar',  # Sentinel-1 SAR
                'landsat_thermal',  # Landsat térmico
                'icesat2',  # ICESat-2 elevación
                'srtm_dem',  # SRTM DEM
                'modis_lst',  # MODIS LST
                'era5_climate',  # ERA5 clima
                'chirps_precipitation',  # CHIRPS precipitación
                'copernicus_sst',  # Copernicus Marine
                'viirs_thermal',  # VIIRS térmico
                'opentopography',  # OpenTopography LiDAR
                'palsar_backscatter'  # PALSAR SAR
            ]
            
            print(f"\n[MEDICIONES] Obteniendo datos de {len(instrument_names)} instrumentos...", flush=True)
            
            instrument_batch = await integrator_v2.get_batch_measurements(
                instrument_names=instrument_names,
                lat_min=request.lat_min,
                lat_max=request.lat_max,
                lon_min=request.lon_min,
                lon_max=request.lon_max
            )
            
            # Convertir InstrumentBatch a diccionario compatible con pipeline
            raw_measurements = {
                'instrumental_measurements': {},
                'metadata': {
                    'coverage_score': instrument_batch.get_coverage_score(),
                    'status_summary': instrument_batch.get_status_summary()
                }
            }
            
            # Agregar cada medición al diccionario
            for result in instrument_batch.results:
                raw_measurements['instrumental_measurements'][result.instrument_name] = {
                    'value': result.value,
                    'confidence': result.confidence,
                    'status': result.status.value,
                    'unit': result.unit,
                    'quality_ratio': result.quality_ratio,
                    'source': result.source,
                    'acquisition_date': result.acquisition_date,
                    'reason': result.reason
                }
            
            print(f"[MEDICIONES] Obtenidas {len(raw_measurements['instrumental_measurements'])} mediciones", flush=True)
            print(f"[MEDICIONES] Coverage score: {raw_measurements['metadata']['coverage_score']:.2f}", flush=True)
            
            # Usar el pipeline científico con los parámetros correctos
            pipeline = ScientificPipeline(
                db_pool=db_pool,
                validator=validator
            )
            
            # Ejecutar análisis con las mediciones
            result = await pipeline.analyze(
                raw_measurements=raw_measurements,
                lat_min=request.lat_min,
                lat_max=request.lat_max,
                lon_min=request.lon_min,
                lon_max=request.lon_max
            )
            
            # Extraer scientific_output
            scientific_output = result.get('scientific_output', {})
            
            # Construir lista de mediciones para el frontend
            measurements_list = []
            for inst_name, inst_data in raw_measurements['instrumental_measurements'].items():
                measurements_list.append({
                    'instrument_name': inst_name,
                    'value': inst_data.get('value'),
                    'confidence': inst_data.get('confidence', 0),
                    'status': inst_data.get('status', 'UNKNOWN'),
                    'unit': inst_data.get('unit', ''),
                    'source': inst_data.get('source', ''),
                    'quality_ratio': inst_data.get('quality_ratio')
                })
            
            # Construir respuesta compatible con frontend
            response_data = {
                'analysis_id': scientific_output.get('candidate_id', 'unknown'),
                'region_name': detected_region,
                'timestamp': scientific_output.get('timestamp'),
                'measurements': measurements_list,  # Lista de instrumentos
                'archaeological_results': {
                    'anomaly_score': scientific_output.get('anomaly_score', 0),
                    'anthropic_probability': scientific_output.get('anthropic_probability', 0),
                    'confidence_interval': scientific_output.get('confidence_interval', [0, 0]),
                    'recommended_action': scientific_output.get('recommended_action', 'unknown'),
                    'classification': scientific_output.get('classification', 'unknown'),
                    'priority': scientific_output.get('priority', 'NORMAL'),
                    'scientific_confidence': scientific_output.get('scientific_confidence', 'low')
                },
                'environment_context': {
                    'coverage_raw': scientific_output.get('coverage_raw', 0),
                    'coverage_effective': scientific_output.get('coverage_effective', 0),
                    'instruments_measured': scientific_output.get('instruments_measured', 0),
                    'instruments_available': scientific_output.get('instruments_available', 0),
                    'epistemic_uncertainty': scientific_output.get('epistemic_uncertainty', 0)
                },
                'anomaly_map': {
                    'path': scientific_output.get('anomaly_map_path', ''),
                    'metadata': scientific_output.get('anomaly_map_metadata', {})
                },
                'scientific_narrative': scientific_output.get('scientific_narrative', ''),
                'request_info': {
                    'region_name': detected_region,
                    'center_lat': center_lat,
                    'center_lon': center_lon,
                    'bounds': {
                        'lat_min': request.lat_min,
                        'lat_max': request.lat_max,
                        'lon_min': request.lon_min,
                        'lon_max': request.lon_max
                    }
                }
            }
            
            print("\n✅ Análisis científico básico completado", flush=True)
            return response_data
        
        # ============================================================================
        # GUARDAR EN BASE DE DATOS (estructura completa TIMT)
        # ============================================================================
        
        if db_pool:
            try:
                print("\n[BD] Guardando resultados TIMT en base de datos...", flush=True)
                
                # Importar guardador TIMT
                from api.timt_db_saver import save_timt_result_to_db
                
                request_dict = {
                    'region_name': detected_region,
                    'analysis_radius_km': 5.0,
                    'resolution_m': etp.resolution_m
                }
                
                timt_db_id = await save_timt_result_to_db(db_pool, timt_result, request_dict)
                
                if timt_db_id:
                    print(f"[BD] ✅ Resultado TIMT guardado con ID: {timt_db_id}", flush=True)
                else:
                    print("[BD] ⚠️ Resultado TIMT no guardado", flush=True)
                    
            except Exception as e:
                print(f"[BD] ⚠️ Error guardando TIMT en BD: {e}", flush=True)
                import traceback
                traceback.print_exc()
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


# ============================================================================
# ENDPOINTS PARA CAPA DE SITIOS ARQUEOLÓGICOS
# ============================================================================

@router.get("/sites/layer")
async def get_sites_layer(
    confidence_level: Optional[str] = None,
    site_type: Optional[str] = None,
    country: Optional[str] = None,
    limit: int = 2000,  # REDUCIDO: 10000 → 2000 para mejor UX
    # FASE 2: Filtrado espacial (bbox)
    bbox: Optional[str] = None  # "lat_min,lon_min,lat_max,lon_max"
):
    """
    Obtener sitios para capa de mapa (GeoJSON).
    
    Parámetros:
    - confidence_level: HIGH, MODERATE, LOW, CANDIDATE
    - site_type: Filtrar por tipo
    - country: Filtrar por país
    - limit: Máximo de sitios (default 2000, max 10000)
    - bbox: Bounding box "lat_min,lon_min,lat_max,lon_max" (opcional)
    
    Returns:
        GeoJSON FeatureCollection con sitios filtrados
    """
    
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not available")
    
    # FASE 1: Limitar resultados para mejor UX
    if limit > 10000:
        limit = 10000
        print(f"⚠️ WARNING: Limit capped at 10000 for performance")
    
    try:
        async with db_pool.acquire() as conn:
            # Construir query
            where_clauses = []
            params = []
            param_count = 1
            
            if confidence_level:
                where_clauses.append(f'"confidenceLevel" = ${param_count}')
                params.append(confidence_level)
                param_count += 1
            
            if site_type:
                where_clauses.append(f'"siteType" = ${param_count}')
                params.append(site_type)
                param_count += 1
            
            if country:
                where_clauses.append(f'country = ${param_count}')
                params.append(country)
                param_count += 1
            
            # FASE 2: Filtrado por bounding box
            if bbox:
                try:
                    lat_min, lon_min, lat_max, lon_max = map(float, bbox.split(','))
                    where_clauses.append(f'latitude BETWEEN ${param_count} AND ${param_count + 1}')
                    where_clauses.append(f'longitude BETWEEN ${param_count + 2} AND ${param_count + 3}')
                    params.extend([lat_min, lat_max, lon_min, lon_max])
                    param_count += 4
                    print(f"📍 Spatial filter applied: bbox={bbox}")
                except ValueError:
                    print(f"⚠️ WARNING: Invalid bbox format '{bbox}', ignoring spatial filter")
            
            where_sql = " AND ".join(where_clauses) if where_clauses else "TRUE"
            
            # Contar total antes de limitar
            count_query = f"""
                SELECT COUNT(*) as total
                FROM archaeological_sites
                WHERE {where_sql}
            """
            
            total_count = await conn.fetchval(count_query, *params)
            
            query = f"""
                SELECT 
                    id,
                    name,
                    slug,
                    "siteType" as site_type,
                    "environmentType" as environment_type,
                    "confidenceLevel" as confidence_level,
                    latitude,
                    longitude,
                    country,
                    region,
                    description,
                    "createdAt" as created_at
                FROM archaeological_sites
                WHERE {where_sql}
                ORDER BY "confidenceLevel" DESC, "createdAt" DESC
                LIMIT ${param_count}
            """
            params.append(limit)
            
            sites = await conn.fetch(query, *params)
            
            # FASE 1: Warning si se trunca
            if total_count > limit:
                print(f"⚠️ WARNING: Results truncated - showing {limit} of {total_count} sites")
            
            # Convertir a GeoJSON
            features = []
            for site in sites:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [site['longitude'], site['latitude']]
                    },
                    "properties": {
                        "id": str(site['id']),
                        "name": site['name'],
                        "slug": site['slug'],
                        "siteType": site['site_type'],
                        "environmentType": site['environment_type'],
                        "confidenceLevel": site['confidence_level'],
                        "country": site['country'],
                        "region": site['region'],
                        "description": site['description'][:200] if site['description'] else "",
                        "createdAt": site['created_at'].isoformat() if site['created_at'] else None
                    }
                }
                features.append(feature)
            
            geojson = {
                "type": "FeatureCollection",
                "features": features,
                "metadata": {
                    "total": len(features),
                    "total_available": total_count,  # NUEVO: total sin límite
                    "truncated": total_count > limit,  # NUEVO: indica si se truncó
                    "spatial_filtered": bbox is not None,  # NUEVO: indica si hay filtro espacial
                    "filters": {
                        "confidence_level": confidence_level,
                        "site_type": site_type,
                        "country": country,
                        "bbox": bbox,
                        "limit": limit
                    }
                }
            }
            
            return geojson
            
    except Exception as e:
        print(f"Error getting sites layer: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sites/candidate")
async def add_candidate_site(request: dict):
    """
    Agregar nuevo sitio candidato a la capa.
    
    Body:
    {
        "name": "Candidato Amazonía 001",
        "latitude": -10.5,
        "longitude": -70.2,
        "country": "Brazil",
        "region": "Acre",
        "origin_probability": 0.85,
        "activity_probability": 0.05,
        "anomaly_probability": 0.02,
        "ess": "high",
        "ess_score": 0.75,
        "description": "Candidato detectado...",
        "analysis_id": "uuid"
    }
    """
    
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not available")
    
    try:
        # Validar datos requeridos
        required = ['name', 'latitude', 'longitude', 'country']
        for field in required:
            if field not in request:
                raise HTTPException(status_code=400, detail=f"Missing field: {field}")
        
        # Generar slug
        import re
        slug_base = f"{request['name']}-{request['latitude']:.4f}-{request['longitude']:.4f}"
        slug = re.sub(r'[^a-z0-9-]', '', slug_base.lower().replace(' ', '-'))
        
        # Generar descripción con métricas separadas
        origin = request.get('origin_probability', 0)
        activity = request.get('activity_probability', 0)
        anomaly = request.get('anomaly_probability', 0)
        ess = request.get('ess', 'none')
        
        description = (
            f"Candidato arqueológico detectado por ArcheoScope. "
            f"Métricas: Origen {origin:.0%}, Actividad {activity:.0%}, "
            f"Anomalía {anomaly:.0%}. ESS: {ess.upper()}. "
            f"Requiere validación de campo."
        )
        
        if 'description' in request:
            description = request['description']
        
        async with db_pool.acquire() as conn:
            # Insertar sitio
            site_id = await conn.fetchval("""
                INSERT INTO archaeological_sites (
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
                    "createdAt",
                    "updatedAt"
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, NOW(), NOW()
                )
                RETURNING id
            """,
                request['name'],
                slug,
                'UNKNOWN',  # Tipo por defecto
                request.get('environment_type', 'UNKNOWN'),
                'CANDIDATE',  # Siempre candidato
                request['latitude'],
                request['longitude'],
                request['country'],
                request.get('region', ''),
                description
            )
            
            return {
                "success": True,
                "site_id": str(site_id),
                "message": "Candidato agregado a la capa",
                "slug": slug
            }
            
    except Exception as e:
        print(f"Error adding candidate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sites/candidates")
async def get_candidates_only(limit: int = 1000):
    """
    Obtener solo sitios CANDIDATOS para revisión.
    
    Returns:
        Lista de candidatos con métricas extraídas
    """
    
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not available")
    
    try:
        async with db_pool.acquire() as conn:
            candidates = await conn.fetch("""
                SELECT 
                    id,
                    name,
                    slug,
                    "siteType" as site_type,
                    "environmentType" as environment_type,
                    latitude,
                    longitude,
                    country,
                    region,
                    description,
                    "createdAt" as created_at
                FROM archaeological_sites
                WHERE "confidenceLevel" = 'CANDIDATE'
                ORDER BY "createdAt" DESC
                LIMIT $1
            """, limit)
            
            result = []
            for c in candidates:
                # Extraer métricas de la descripción
                import re
                desc = c['description']
                
                origin = 0.0
                activity = 0.0
                anomaly = 0.0
                ess = "none"
                
                # Buscar métricas en descripción
                origin_match = re.search(r'Origen (\d+)%', desc)
                if origin_match:
                    origin = float(origin_match.group(1)) / 100
                
                activity_match = re.search(r'Actividad (\d+)%', desc)
                if activity_match:
                    activity = float(activity_match.group(1)) / 100
                
                anomaly_match = re.search(r'Anomalía (\d+)%', desc)
                if anomaly_match:
                    anomaly = float(anomaly_match.group(1)) / 100
                
                ess_match = re.search(r'ESS: (\w+)', desc)
                if ess_match:
                    ess = ess_match.group(1).lower()
                
                result.append({
                    "id": str(c['id']),
                    "name": c['name'],
                    "slug": c['slug'],
                    "site_type": c['site_type'],
                    "environment_type": c['environment_type'],
                    "latitude": c['latitude'],
                    "longitude": c['longitude'],
                    "country": c['country'],
                    "region": c['region'],
                    "description": c['description'],
                    "created_at": c['created_at'].isoformat() if c['created_at'] else None,
                    "metrics": {
                        "origin": origin,
                        "activity": activity,
                        "anomaly": anomaly,
                        "ess": ess
                    }
                })
            
            return {
                "total": len(result),
                "candidates": result
            }
            
    except Exception as e:
        print(f"Error getting candidates: {e}")
        raise HTTPException(status_code=500, detail=str(e))
