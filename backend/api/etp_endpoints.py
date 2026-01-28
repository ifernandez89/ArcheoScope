#!/usr/bin/env python3
"""
ETP API Endpoints - Environmental Tomographic Profile
====================================================

Endpoints revolucionarios que transforman ArcheoScope de "detector" a "explicador":

POST /etp/generate - Generar perfil tomográfico completo
GET /etp/{territory_id} - Obtener perfil existente
GET /etp/{territory_id}/visualization - Datos para visualización
POST /etp/compare - Comparar múltiples territorios

REVOLUCIÓN: De "¿Hay un sitio?" a "¿Qué cuenta este territorio?"
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime

from ..etp_generator import ETProfileGenerator
from ..etp_core import BoundingBox, EnvironmentalTomographicProfile
from ..satellite_connectors.real_data_integrator_v2 import RealDataIntegratorV2

logger = logging.getLogger(__name__)

# Router para endpoints ETP
etp_router = APIRouter(prefix="/etp", tags=["Environmental Tomographic Profile"])

# Modelos Pydantic para requests/responses

class ETProfileRequest(BaseModel):
    """Request para generar perfil tomográfico."""
    lat_min: float = Field(..., ge=-90, le=90, description="Latitud mínima")
    lat_max: float = Field(..., ge=-90, le=90, description="Latitud máxima")
    lon_min: float = Field(..., ge=-180, le=180, description="Longitud mínima")
    lon_max: float = Field(..., ge=-180, le=180, description="Longitud máxima")
    depth_min: float = Field(0.0, description="Profundidad mínima (superficie)")
    depth_max: float = Field(-20.0, description="Profundidad máxima en metros")
    resolution_m: float = Field(30.0, gt=0, description="Resolución espacial en metros")
    territory_name: Optional[str] = Field(None, description="Nombre del territorio")

class ETProfileSummary(BaseModel):
    """Resumen de perfil tomográfico."""
    territory_id: str
    territory_name: Optional[str]
    generation_timestamp: datetime
    bounds: Dict[str, float]
    ess_superficial: float
    ess_volumetrico: float
    ess_temporal: float
    coherencia_3d: float
    narrative_summary: str
    anomalies_count: int

class ETProfileVisualization(BaseModel):
    """Datos de visualización tomográfica."""
    territory_id: str
    xz_slice: Dict[str, List[float]]
    yz_slice: Dict[str, List[float]]
    xy_slices: List[Dict[str, Any]]
    depth_layers: List[float]
    metrics: Dict[str, float]

# Dependencia para obtener generador ETP
async def get_etp_generator() -> ETProfileGenerator:
    """Obtener generador ETP inicializado."""
    try:
        integrator = RealDataIntegratorV2()
        generator = ETProfileGenerator(integrator)
        return generator
    except Exception as e:
        logger.error(f"Error inicializando ETP generator: {e}")
        raise HTTPException(status_code=500, detail="Error inicializando sistema ETP")

# Cache simple para perfiles generados (en producción usar Redis)
etp_cache: Dict[str, EnvironmentalTomographicProfile] = {}

@etp_router.post("/generate", response_model=ETProfileSummary)
async def generate_etp_profile(
    request: ETProfileRequest,
    generator: ETProfileGenerator = Depends(get_etp_generator)
):
    """
    Generar perfil tomográfico ambiental completo.
    
    REVOLUCIÓN CONCEPTUAL: Transforma coordenadas en narrativa territorial explicable.
    
    Returns:
        ETProfileSummary con métricas y narrativa del territorio
    """
    
    logger.info(f"🚀 Generando ETP para territorio: {request.territory_name or 'Sin nombre'}")
    logger.info(f"📐 Región: [{request.lat_min:.4f}, {request.lat_max:.4f}] x [{request.lon_min:.4f}, {request.lon_max:.4f}]")
    
    try:
        # Validar bounds
        if request.lat_min >= request.lat_max:
            raise HTTPException(status_code=400, detail="lat_min debe ser menor que lat_max")
        if request.lon_min >= request.lon_max:
            raise HTTPException(status_code=400, detail="lon_min debe ser menor que lon_max")
        if request.depth_min <= request.depth_max:
            raise HTTPException(status_code=400, detail="depth_max debe ser menor que depth_min (valores negativos)")
        
        # Crear bounding box
        bounds = BoundingBox(
            lat_min=request.lat_min,
            lat_max=request.lat_max,
            lon_min=request.lon_min,
            lon_max=request.lon_max,
            depth_min=request.depth_min,
            depth_max=request.depth_max
        )
        
        # Verificar tamaño razonable
        if bounds.area_km2 > 100:  # Límite de 100 km²
            raise HTTPException(
                status_code=400, 
                detail=f"Área demasiado grande: {bounds.area_km2:.2f} km². Máximo: 100 km²"
            )
        
        # Generar perfil tomográfico
        logger.info("🧠 Iniciando generación de perfil tomográfico...")
        etp = await generator.generate_etp(bounds, request.resolution_m)
        
        # Guardar en cache
        etp_cache[etp.territory_id] = etp
        
        # Contar anomalías
        anomalies_count = 0
        if etp.xz_profile:
            anomalies_count += len(etp.xz_profile.anomalies)
        if etp.yz_profile:
            anomalies_count += len(etp.yz_profile.anomalies)
        
        # Generar resumen narrativo
        narrative_summary = etp.generate_territorial_summary()
        
        logger.info(f"✅ ETP generado exitosamente: {etp.territory_id}")
        logger.info(f"📊 ESS Volumétrico: {etp.ess_volumetrico:.3f}")
        logger.info(f"🏛️ Anomalías detectadas: {anomalies_count}")
        
        return ETProfileSummary(
            territory_id=etp.territory_id,
            territory_name=request.territory_name,
            generation_timestamp=etp.generation_timestamp,
            bounds={
                "lat_min": bounds.lat_min,
                "lat_max": bounds.lat_max,
                "lon_min": bounds.lon_min,
                "lon_max": bounds.lon_max,
                "depth_min": bounds.depth_min,
                "depth_max": bounds.depth_max
            },
            ess_superficial=etp.ess_superficial,
            ess_volumetrico=etp.ess_volumetrico,
            ess_temporal=etp.ess_temporal,
            coherencia_3d=etp.coherencia_3d,
            narrative_summary=narrative_summary,
            anomalies_count=anomalies_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error generando ETP: {e}")
        raise HTTPException(status_code=500, detail=f"Error generando perfil tomográfico: {str(e)}")

@etp_router.get("/{territory_id}", response_model=Dict[str, Any])
async def get_etp_profile(territory_id: str):
    """
    Obtener perfil tomográfico completo por ID.
    
    Returns:
        Perfil tomográfico completo con toda la información
    """
    
    if territory_id not in etp_cache:
        raise HTTPException(status_code=404, detail=f"Perfil tomográfico {territory_id} no encontrado")
    
    etp = etp_cache[territory_id]
    
    # Convertir a diccionario serializable
    return {
        "territory_id": etp.territory_id,
        "bounds": {
            "lat_min": etp.bounds.lat_min,
            "lat_max": etp.bounds.lat_max,
            "lon_min": etp.bounds.lon_min,
            "lon_max": etp.bounds.lon_max,
            "depth_min": etp.bounds.depth_min,
            "depth_max": etp.bounds.depth_max
        },
        "resolution_m": etp.resolution_m,
        "generation_timestamp": etp.generation_timestamp.isoformat(),
        "metrics": etp.get_summary_metrics(),
        "narrative_explanation": etp.narrative_explanation,
        "occupational_history": [
            {
                "start_year": period.start_year,
                "end_year": period.end_year,
                "occupation_type": period.occupation_type,
                "evidence_strength": period.evidence_strength,
                "description": period.description
            }
            for period in etp.occupational_history
        ],
        "territorial_function": {
            "primary_function": etp.territorial_function.primary_function,
            "secondary_functions": etp.territorial_function.secondary_functions,
            "spatial_organization": etp.territorial_function.spatial_organization,
            "confidence": etp.territorial_function.confidence
        } if etp.territorial_function else None,
        "landscape_evolution": {
            "natural_baseline": etp.landscape_evolution.natural_baseline,
            "human_modifications": etp.landscape_evolution.human_modifications,
            "abandonment_indicators": etp.landscape_evolution.abandonment_indicators,
            "current_state": etp.landscape_evolution.current_state
        } if etp.landscape_evolution else None
    }

@etp_router.get("/{territory_id}/visualization", response_model=ETProfileVisualization)
async def get_etp_visualization(territory_id: str):
    """
    Obtener datos de visualización tomográfica.
    
    CRÍTICO: Datos específicamente preparados para el frontend tomográfico.
    
    Returns:
        Datos estructurados para visualización 3D/4D
    """
    
    if territory_id not in etp_cache:
        raise HTTPException(status_code=404, detail=f"Perfil tomográfico {territory_id} no encontrado")
    
    etp = etp_cache[territory_id]
    
    return ETProfileVisualization(
        territory_id=etp.territory_id,
        xz_slice=etp.visualization_data.get('xz_slice', {}),
        yz_slice=etp.visualization_data.get('yz_slice', {}),
        xy_slices=etp.visualization_data.get('xy_slices', []),
        depth_layers=etp.visualization_data.get('depth_layers', []),
        metrics=etp.get_summary_metrics()
    )

@etp_router.get("/", response_model=List[ETProfileSummary])
async def list_etp_profiles():
    """
    Listar todos los perfiles tomográficos generados.
    
    Returns:
        Lista de resúmenes de perfiles disponibles
    """
    
    summaries = []
    
    for territory_id, etp in etp_cache.items():
        # Contar anomalías
        anomalies_count = 0
        if etp.xz_profile:
            anomalies_count += len(etp.xz_profile.anomalies)
        if etp.yz_profile:
            anomalies_count += len(etp.yz_profile.anomalies)
        
        summary = ETProfileSummary(
            territory_id=etp.territory_id,
            territory_name=None,  # No almacenamos nombre en cache
            generation_timestamp=etp.generation_timestamp,
            bounds={
                "lat_min": etp.bounds.lat_min,
                "lat_max": etp.bounds.lat_max,
                "lon_min": etp.bounds.lon_min,
                "lon_max": etp.bounds.lon_max,
                "depth_min": etp.bounds.depth_min,
                "depth_max": etp.bounds.depth_max
            },
            ess_superficial=etp.ess_superficial,
            ess_volumetrico=etp.ess_volumetrico,
            ess_temporal=etp.ess_temporal,
            coherencia_3d=etp.coherencia_3d,
            narrative_summary=etp.generate_territorial_summary(),
            anomalies_count=anomalies_count
        )
        
        summaries.append(summary)
    
    # Ordenar por timestamp descendente
    summaries.sort(key=lambda x: x.generation_timestamp, reverse=True)
    
    return summaries

@etp_router.delete("/{territory_id}")
async def delete_etp_profile(territory_id: str):
    """
    Eliminar perfil tomográfico del cache.
    
    Returns:
        Confirmación de eliminación
    """
    
    if territory_id not in etp_cache:
        raise HTTPException(status_code=404, detail=f"Perfil tomográfico {territory_id} no encontrado")
    
    del etp_cache[territory_id]
    
    return {"message": f"Perfil tomográfico {territory_id} eliminado exitosamente"}

@etp_router.post("/compare")
async def compare_etp_profiles(territory_ids: List[str]):
    """
    Comparar múltiples perfiles tomográficos.
    
    FUTURO: Análisis comparativo de territorios para identificar patrones regionales.
    
    Args:
        territory_ids: Lista de IDs de territorios a comparar
        
    Returns:
        Análisis comparativo de territorios
    """
    
    if len(territory_ids) < 2:
        raise HTTPException(status_code=400, detail="Se requieren al menos 2 territorios para comparar")
    
    # Verificar que todos los territorios existen
    missing_territories = [tid for tid in territory_ids if tid not in etp_cache]
    if missing_territories:
        raise HTTPException(
            status_code=404, 
            detail=f"Territorios no encontrados: {', '.join(missing_territories)}"
        )
    
    # Obtener perfiles
    profiles = [etp_cache[tid] for tid in territory_ids]
    
    # Análisis comparativo básico
    comparison = {
        "territories_count": len(profiles),
        "average_ess_volumetrico": sum(p.ess_volumetrico for p in profiles) / len(profiles),
        "average_ess_temporal": sum(p.ess_temporal for p in profiles) / len(profiles),
        "average_coherencia_3d": sum(p.coherencia_3d for p in profiles) / len(profiles),
        "territories": [
            {
                "territory_id": p.territory_id,
                "ess_volumetrico": p.ess_volumetrico,
                "ess_temporal": p.ess_temporal,
                "coherencia_3d": p.coherencia_3d,
                "primary_function": p.territorial_function.primary_function if p.territorial_function else "unknown"
            }
            for p in profiles
        ]
    }
    
    return comparison

# Endpoint de salud para ETP
@etp_router.get("/health")
async def etp_health_check():
    """
    Verificar estado del sistema ETP.
    
    Returns:
        Estado del sistema tomográfico
    """
    
    try:
        # Verificar que el generador se puede inicializar
        generator = await get_etp_generator()
        
        return {
            "status": "healthy",
            "system": "Environmental Tomographic Profile",
            "version": "1.0.0",
            "cached_profiles": len(etp_cache),
            "capabilities": [
                "volumetric_analysis",
                "temporal_analysis", 
                "narrative_generation",
                "3d_visualization",
                "territorial_explanation"
            ]
        }
        
    except Exception as e:
        logger.error(f"ETP health check failed: {e}")
        raise HTTPException(status_code=503, detail="Sistema ETP no disponible")

# Exportar router
__all__ = ["etp_router"]