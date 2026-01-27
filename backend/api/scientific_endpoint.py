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

@router.post("/analyze-scientific")
async def analyze_scientific(request: ScientificAnalysisRequest):
    """
    Análisis científico completo con pipeline de 7 fases.
    
    FASES:
    0. Enriquecimiento con datos históricos de BD
    A. Normalización por instrumento
    B. Detección de anomalía pura
    C. Análisis morfológico explícito
    D. Inferencia antropogénica (con freno de mano)
    E. Verificación de anti-patrones
    F. Validación contra sitios conocidos
    G. Salida científica
    
    Returns:
        Resultado científico completo con todas las fases
    """
    
    print("\n" + "="*80, flush=True)
    print("ENDPOINT /analyze-scientific ALCANZADO", flush=True)
    print(f"Región: {request.region_name}", flush=True)
    print(f"Bounds: [{request.lat_min}, {request.lat_max}] x [{request.lon_min}, {request.lon_max}]", flush=True)
    print("="*80 + "\n", flush=True)
    
    try:
        # Inicializar pipeline con BD y validator
        pipeline = ScientificPipeline(db_pool=db_pool, validator=validator)
        
        # Calcular centro
        center_lat = (request.lat_min + request.lat_max) / 2
        center_lon = (request.lon_min + request.lon_max) / 2
        
        # 1. Clasificar ambiente
        print("[STEP 1] Clasificando ambiente...", flush=True)
        env_context = classifier.classify(center_lat, center_lon)
        print(f"  Ambiente: {env_context.environment_type.value}", flush=True)
        print(f"  Confianza: {env_context.confidence:.2f}", flush=True)
        
        # 2. Medir con instrumentos reales
        print("[STEP 2] Midiendo con instrumentos reales...", flush=True)
        
        # Obtener lista de instrumentos apropiados para el ambiente
        instrument_names = env_context.primary_sensors
        
        measurements = []
        for instrument_name in instrument_names:
            try:
                measurement = await integrator.get_instrument_measurement(
                    instrument_name=instrument_name,
                    lat_min=request.lat_min,
                    lat_max=request.lat_max,
                    lon_min=request.lon_min,
                    lon_max=request.lon_max
                )
                measurements.append(measurement)
            except Exception as e:
                print(f"  [WARNING] Error en {instrument_name}: {e}", flush=True)
                continue
        
        print(f"  Mediciones obtenidas: {len(measurements)}", flush=True)
        for m in measurements:
            print(f"    - {m.instrument_name}: {m.value:.3f} ({m.data_mode})", flush=True)
        
        # 3. Preparar datos para pipeline
        raw_measurements = {
            'candidate_id': request.candidate_id or f"{request.region_name}_{center_lat:.4f}_{center_lon:.4f}",
            'region_name': request.region_name,
            'center_lat': center_lat,
            'center_lon': center_lon,
            'environment_type': env_context.environment_type.value
        }
        
        # Añadir mediciones
        for m in measurements:
            raw_measurements[m.instrument_name] = {
                'value': m.value,
                'threshold': m.threshold,
                'exceeds_threshold': m.exceeds_threshold,
                'confidence': m.confidence,
                'data_mode': m.data_mode,
                'source': m.source
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
            'primary_sensors': env_context.primary_sensors,
            'archaeological_visibility': env_context.archaeological_visibility,
            'preservation_potential': env_context.preservation_potential
        }
        
        result['instrumental_measurements'] = [
            {
                'instrument_name': m.instrument_name,
                'value': m.value,
                'threshold': m.threshold,
                'exceeds_threshold': m.exceeds_threshold,
                'confidence': m.confidence,
                'data_mode': m.data_mode,
                'source': m.source
            }
            for m in measurements
        ]
        
        result['request_info'] = {
            'region_name': request.region_name,
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
        
        return result
        
    except Exception as e:
        print(f"\n[ERROR] Error en análisis científico: {e}", flush=True)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en análisis científico: {str(e)}")
