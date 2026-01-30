#!/usr/bin/env python3
"""
TIMT API Endpoints - Territorial Inferential Multi-domain Tomography
===================================================================

Endpoints para el sistema revolucionario de Tomografía Territorial Inferencial.

ENDPOINTS PRINCIPALES:
- /timt/analyze - Análisis territorial completo (3 capas)
- /timt/tcp - Solo generación de Contexto Territorial (Capa 0)
- /timt/hypotheses - Validación de hipótesis específicas
- /timt/transparency - Reporte de transparencia detallado
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from territorial_inferential_tomography import (
    TerritorialInferentialTomographyEngine, 
    TerritorialInferentialTomographyResult,
    AnalysisObjective,
    CommunicationLevel
)
from territorial_context_profile import TerritorialContextProfile
from satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2
import asyncpg
import os

logger = logging.getLogger(__name__)

# Router para endpoints TIMT
timt_router = APIRouter(prefix="/timt", tags=["Territorial Inferential Tomography"])

# Inicializar motor TIMT (se hará en startup)
timt_engine: Optional[TerritorialInferentialTomographyEngine] = None

# Pool de conexiones a BD
db_pool = None

async def init_timt_db_pool():
    """Inicializar pool de conexiones a BD para TIMT."""
    global db_pool
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        database_url = database_url.strip('"').strip("'")
        try:
            db_pool = await asyncpg.create_pool(database_url, min_size=2, max_size=10)
            logger.info("✅ TIMT DB Pool initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing TIMT DB pool: {e}")
            db_pool = None
    else:
        logger.warning("⚠️ DATABASE_URL not configured for TIMT")

def initialize_timt_engine():
    """Inicializar motor TIMT con integrador de 15 instrumentos."""
    global timt_engine
    
    try:
        # Inicializar integrador con 15 instrumentos
        integrator = RealDataIntegratorV2()
        
        # Inicializar motor TIMT
        timt_engine = TerritorialInferentialTomographyEngine(integrator)
        
        logger.info("🚀 TIMT Engine initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize TIMT Engine: {e}")
        raise

# Modelos Pydantic para requests/responses

class TIMTAnalysisRequest(BaseModel):
    """Request para análisis territorial completo."""
    
    lat_min: float = Field(..., ge=-90, le=90, description="Latitud mínima")
    lat_max: float = Field(..., ge=-90, le=90, description="Latitud máxima")
    lon_min: float = Field(..., ge=-180, le=180, description="Longitud mínima")
    lon_max: float = Field(..., ge=-180, le=180, description="Longitud máxima")
    
    analysis_objective: str = Field(
        default="exploratory",
        description="Objetivo del análisis: exploratory, validation, academic, monitoring"
    )
    
    analysis_radius_km: float = Field(
        default=5.0,
        ge=1.0,
        le=50.0,
        description="Radio de análisis contextual en km"
    )
    
    resolution_m: Optional[float] = Field(
        default=None,
        ge=1.0,
        le=1000.0,
        description="Resolución en metros (si None, usa recomendación TCP)"
    )
    
    communication_level: str = Field(
        default="technical",
        description="Nivel de comunicación: technical, academic, general, institutional"
    )

class TCPRequest(BaseModel):
    """Request para generación de Contexto Territorial."""
    
    lat_min: float = Field(..., ge=-90, le=90)
    lat_max: float = Field(..., ge=-90, le=90)
    lon_min: float = Field(..., ge=-180, le=180)
    lon_max: float = Field(..., ge=-180, le=180)
    
    analysis_objective: str = Field(default="exploratory")
    analysis_radius_km: float = Field(default=5.0, ge=1.0, le=50.0)

class TIMTAnalysisResponse(BaseModel):
    """Response del análisis territorial completo."""
    
    analysis_id: str
    status: str
    timestamp: datetime
    
    # Métricas principales
    territorial_coherence_score: float
    scientific_rigor_score: float
    
    # Resúmenes por nivel
    technical_summary: str
    academic_summary: str
    general_summary: str
    institutional_summary: str
    
    # Contexto territorial
    tcp_summary: Dict[str, Any]
    
    # Perfil tomográfico
    etp_summary: Dict[str, Any]
    
    # Validación de hipótesis
    hypothesis_validations: List[Dict[str, Any]]
    
    # Transparencia
    transparency_summary: Dict[str, Any]
    
    # Salida Científica (HRM)
    scientific_output: Dict[str, Any] = Field(default_factory=dict)

class TCPResponse(BaseModel):
    """Response del Contexto Territorial."""
    
    tcp_id: str
    status: str
    timestamp: datetime
    
    # Contexto territorial
    geological_context: Dict[str, Any]
    hydrographic_features: List[Dict[str, Any]]
    external_sites: List[Dict[str, Any]]
    human_traces: List[Dict[str, Any]]
    
    # Hipótesis territoriales
    territorial_hypotheses: List[Dict[str, Any]]
    
    # Estrategia instrumental
    instrumental_strategy: Dict[str, Any]
    
    # Limitaciones
    known_limitations: List[str]
    system_boundaries: List[str]

# Endpoints

@timt_router.post("/analyze", response_model=TIMTAnalysisResponse)
async def analyze_territory_complete(request: TIMTAnalysisRequest):
    """
    Análisis territorial completo con Tomografía Inferencial (3 capas).
    
    PROCESO:
    - CAPA 0: Contexto Territorial (TCP)
    - CAPA 1: Adquisición dirigida + Tomografía (ETP)
    - CAPA 2: Validación + Transparencia + Comunicación
    
    Returns:
        Resultado completo con análisis territorial, validación de hipótesis y transparencia.
    """
    
    if not timt_engine:
        raise HTTPException(status_code=500, detail="TIMT Engine not initialized")
    
    try:
        logger.info(f"🚀 Starting TIMT analysis for territory [{request.lat_min:.4f}, {request.lat_max:.4f}] x [{request.lon_min:.4f}, {request.lon_max:.4f}]")
        
        # Validar coordenadas
        if request.lat_min >= request.lat_max or request.lon_min >= request.lon_max:
            raise HTTPException(status_code=400, detail="Invalid coordinate bounds")
        
        # Mapear enums
        try:
            objective = AnalysisObjective(request.analysis_objective)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid analysis_objective: {request.analysis_objective}")
        
        try:
            comm_level = CommunicationLevel(request.communication_level)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid communication_level: {request.communication_level}")
        
        # Ejecutar análisis territorial completo
        result = await timt_engine.analyze_territory(
            lat_min=request.lat_min,
            lat_max=request.lat_max,
            lon_min=request.lon_min,
            lon_max=request.lon_max,
            analysis_objective=objective,
            analysis_radius_km=request.analysis_radius_km,
            resolution_m=request.resolution_m,
            communication_level=comm_level
        )
        
        # Preparar response
        response = TIMTAnalysisResponse(
            analysis_id=result.analysis_id,
            status="success",
            timestamp=result.analysis_timestamp,
            territorial_coherence_score=result.territorial_coherence_score,
            scientific_rigor_score=result.scientific_rigor_score,
            technical_summary=result.technical_summary,
            academic_summary=result.academic_summary,
            general_summary=result.general_summary,
            institutional_summary=result.institutional_summary,
            tcp_summary={
                "tcp_id": result.territorial_context.tcp_id,
                "analysis_objective": result.territorial_context.analysis_objective.value,
                "preservation_potential": result.territorial_context.preservation_potential.value,
                "hypotheses_count": len(result.territorial_context.territorial_hypotheses),
                "geological_context": result.territorial_context.geological_context.dominant_lithology.value if result.territorial_context.geological_context else "unknown",
                "hydrographic_features_count": len(result.territorial_context.hydrographic_features),
                "external_sites_count": len(result.territorial_context.external_archaeological_sites),
                "human_traces_count": len(result.territorial_context.known_human_traces)
            },
            etp_summary={
                "territory_id": result.tomographic_profile.territory_id,
                "ess_superficial": result.tomographic_profile.ess_superficial,
                "ess_volumetrico": result.tomographic_profile.ess_volumetrico,
                "ess_temporal": result.tomographic_profile.ess_temporal,
                "coherencia_3d": result.tomographic_profile.coherencia_3d,
                "persistencia_temporal": result.tomographic_profile.persistencia_temporal,
                "densidad_arqueologica_m3": result.tomographic_profile.densidad_arqueologica_m3,
                "narrative_explanation": result.tomographic_profile.narrative_explanation
            },
            hypothesis_validations=[
                {
                    "hypothesis_id": hv.hypothesis_id,
                    "hypothesis_type": hv.hypothesis_type,
                    "evidence_level": hv.overall_evidence_level.value,
                    "confidence_score": hv.confidence_score,
                    "supporting_factors": hv.supporting_factors,
                    "contradictions": hv.contradictions,
                    "explanation": hv.validation_explanation
                }
                for hv in result.hypothesis_validations
            ],
            transparency_summary={
                "analysis_process_steps": len(result.transparency_report.analysis_process),
                "decisions_made_count": len(result.transparency_report.decisions_made),
                "hypotheses_discarded_count": len(result.transparency_report.hypotheses_discarded),
                "system_limitations_count": len(result.transparency_report.system_limitations),
                "validation_recommendations_count": len(result.transparency_report.validation_recommendations),
                "cannot_affirm": result.transparency_report.cannot_affirm[:3],  # Primeros 3
                "can_infer": result.transparency_report.can_infer[:3]  # Primeros 3
            },
            scientific_output=result.scientific_output
        )
        
        logger.info(f"✅ TIMT analysis completed successfully: {result.analysis_id}")
        
        # Guardar en base de datos
        try:
            from api.timt_db_saver import save_timt_result_to_db
            
            request_dict = {
                'region_name': request.region_name,
                'analysis_radius_km': request.analysis_radius_km,
                'resolution_m': request.resolution_m
            }
            
            timt_db_id = await save_timt_result_to_db(db_pool, result, request_dict)
            if timt_db_id:
                logger.info(f"✅ TIMT result saved to DB with ID: {timt_db_id}")
            else:
                logger.warning("⚠️ TIMT result not saved to DB")
        except Exception as e:
            logger.error(f"❌ Error saving TIMT to DB: {e}")
            # No fallar el análisis si falla el guardado
        
        return response
        
    except Exception as e:
        logger.error(f"❌ TIMT analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@timt_router.post("/tcp", response_model=TCPResponse)
async def generate_territorial_context(request: TCPRequest):
    """
    Generar solo el Contexto Territorial (TCP) - CAPA 0.
    
    Útil para:
    - Evaluación rápida de potencial territorial
    - Planificación de estrategia instrumental
    - Identificación de hipótesis territoriales
    
    Returns:
        Contexto territorial con hipótesis y estrategia instrumental.
    """
    
    if not timt_engine:
        raise HTTPException(status_code=500, detail="TIMT Engine not initialized")
    
    try:
        logger.info(f"🧩 Generating TCP for territory [{request.lat_min:.4f}, {request.lat_max:.4f}] x [{request.lon_min:.4f}, {request.lon_max:.4f}]")
        
        # Validar coordenadas
        if request.lat_min >= request.lat_max or request.lon_min >= request.lon_max:
            raise HTTPException(status_code=400, detail="Invalid coordinate bounds")
        
        # Mapear enum
        try:
            objective = AnalysisObjective(request.analysis_objective)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid analysis_objective: {request.analysis_objective}")
        
        # Generar TCP
        tcp = await timt_engine.tcp_system.generate_tcp(
            lat_min=request.lat_min,
            lat_max=request.lat_max,
            lon_min=request.lon_min,
            lon_max=request.lon_max,
            analysis_objective=objective,
            analysis_radius_km=request.analysis_radius_km
        )
        
        # Preparar response
        response = TCPResponse(
            tcp_id=tcp.tcp_id,
            status="success",
            timestamp=tcp.generation_timestamp,
            geological_context={
                "dominant_lithology": tcp.geological_context.dominant_lithology.value if tcp.geological_context else "unknown",
                "geological_age": tcp.geological_context.geological_age.value if tcp.geological_context else "unknown",
                "archaeological_suitability": tcp.geological_context.archaeological_suitability if tcp.geological_context else 0.5,
                "preservation_potential": tcp.geological_context.preservation_potential if tcp.geological_context else 0.5,
                "explanation": tcp.geological_context.geological_explanation if tcp.geological_context else "No disponible"
            },
            hydrographic_features=[
                {
                    "type": hf.watercourse_type.value,
                    "period": hf.hydrographic_period.value,
                    "archaeological_relevance": hf.archaeological_relevance,
                    "settlement_potential": hf.settlement_potential,
                    "coords": hf.center_coords,
                    "explanation": hf.hydrographic_explanation
                }
                for hf in tcp.hydrographic_features
            ],
            external_sites=[
                {
                    "site_id": es.site_id,
                    "name": es.site_name,
                    "type": es.site_type.value,
                    "coords": [es.latitude, es.longitude],
                    "data_quality": es.data_quality,
                    "source": es.data_source.value,
                    "institutional_validation": es.institutional_validation
                }
                for es in tcp.external_archaeological_sites
            ],
            human_traces=[
                {
                    "trace_id": ht.trace_id,
                    "type": ht.trace_type.value,
                    "intensity": ht.activity_intensity.value,
                    "temporal_scale": ht.temporal_scale.value,
                    "archaeological_relevance": ht.archaeological_relevance,
                    "coords": ht.center_coords,
                    "explanation": ht.trace_explanation
                }
                for ht in tcp.known_human_traces
            ],
            territorial_hypotheses=[
                {
                    "hypothesis_id": th.hypothesis_id,
                    "type": th.hypothesis_type,
                    "plausibility_score": th.plausibility_score,
                    "geological_support": th.geological_support,
                    "hydrographic_support": th.hydrographic_support,
                    "archaeological_support": th.archaeological_support,
                    "human_traces_support": th.human_traces_support,
                    "recommended_instruments": th.recommended_instruments,
                    "explanation": th.hypothesis_explanation,
                    "contradictions": th.contradictions
                }
                for th in tcp.territorial_hypotheses
            ],
            instrumental_strategy={
                "surface_instruments": tcp.instrumental_strategy.surface_instruments if tcp.instrumental_strategy else [],
                "subsurface_instruments": tcp.instrumental_strategy.subsurface_instruments if tcp.instrumental_strategy else [],
                "climate_instruments": tcp.instrumental_strategy.climate_instruments if tcp.instrumental_strategy else [],
                "human_context_instruments": tcp.instrumental_strategy.human_context_instruments if tcp.instrumental_strategy else [],
                "priority_instruments": tcp.instrumental_strategy.priority_instruments if tcp.instrumental_strategy else [],
                "secondary_instruments": tcp.instrumental_strategy.secondary_instruments if tcp.instrumental_strategy else [],
                "recommended_resolution_m": tcp.instrumental_strategy.recommended_resolution_m if tcp.instrumental_strategy else 50.0,
                "explanation": tcp.instrumental_strategy.strategy_explanation if tcp.instrumental_strategy else "No disponible"
            },
            known_limitations=tcp.known_limitations,
            system_boundaries=tcp.system_boundaries
        )
        
        logger.info(f"✅ TCP generated successfully: {tcp.tcp_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ TCP generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"TCP generation failed: {str(e)}")

@timt_router.get("/status")
async def get_timt_status():
    """
    Obtener estado del sistema TIMT.
    
    Returns:
        Estado del motor TIMT y sistemas componentes.
    """
    
    try:
        status = {
            "timt_engine_initialized": timt_engine is not None,
            "timestamp": datetime.now(),
            "system_components": {
                "tcp_system": timt_engine.tcp_system is not None if timt_engine else False,
                "etp_generator": timt_engine.etp_generator is not None if timt_engine else False,
                "geological_system": True,  # Siempre disponible
                "hydrography_system": True,  # Siempre disponible
                "external_validation_system": True,  # Siempre disponible
                "human_traces_system": True  # Siempre disponible
            },
            "analysis_modes": [mode.value for mode in AnalysisObjective],
            "communication_levels": [level.value for level in CommunicationLevel]
        }
        
        return status
        
    except Exception as e:
        logger.error(f"❌ Status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@timt_router.get("/capabilities")
async def get_timt_capabilities():
    """
    Obtener capacidades del sistema TIMT.
    
    Returns:
        Descripción completa de capacidades del sistema.
    """
    
    capabilities = {
        "system_name": "Territorial Inferential Multi-domain Tomography (TIMT)",
        "version": "1.0.0",
        "description": "Sistema revolucionario de análisis territorial arqueológico",
        
        "analysis_layers": {
            "layer_0": {
                "name": "Territorial Context Profile (TCP)",
                "description": "Contexto territorial antes de medición",
                "components": [
                    "Contexto geológico",
                    "Hidrografía histórica",
                    "Sitios arqueológicos externos",
                    "Trazas humanas conocidas",
                    "Hipótesis territoriales",
                    "Estrategia instrumental"
                ]
            },
            "layer_1": {
                "name": "Hypothesis-Driven Acquisition",
                "description": "Adquisición dirigida por hipótesis",
                "components": [
                    "15 instrumentos satelitales",
                    "Tomografía 3D (XZ/YZ/XY)",
                    "ESS volumétrico y temporal",
                    "Análisis multidominio"
                ]
            },
            "layer_2": {
                "name": "Validation & Transparency",
                "description": "Validación de hipótesis y transparencia",
                "components": [
                    "Validación cruzada de hipótesis",
                    "Reporte de transparencia completo",
                    "Comunicación multinivel",
                    "Documentación de limitaciones"
                ]
            }
        },
        
        "scientific_approach": {
            "methodology": "Hypothesis-driven territorial analysis",
            "evidence_integration": "Multi-domain cross-validation",
            "transparency": "Complete process documentation",
            "limitations": "Explicitly documented and communicated"
        },
        
        "output_formats": {
            "technical": "Detailed technical analysis",
            "academic": "Academic research format",
            "general": "Public-friendly summary",
            "institutional": "Executive report format"
        },
        
        "validation_metrics": [
            "Territorial Coherence Score",
            "Scientific Rigor Score",
            "External Consistency Score (ECS)",
            "Geological Compatibility Score (GCS)",
            "Hypothesis Evidence Levels"
        ]
    }
    
    return capabilities

# Función de inicialización para ser llamada en startup
def setup_timt_endpoints():
    """Setup TIMT endpoints - llamar en startup de la aplicación."""
    initialize_timt_engine()
    return timt_router