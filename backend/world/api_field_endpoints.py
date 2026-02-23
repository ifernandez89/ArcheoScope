"""
Field System API Endpoints

Endpoints para el nuevo sistema de campos (Base + Dinámico)

Author: Kiro AI Assistant
Date: 22 Feb 2026
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import logging

from .world_orchestrator import world_orchestrator, initialize_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/world/fields", tags=["world-fields"])


# Modelos Pydantic
class LocationRequest(BaseModel):
    """Request para procesar una ubicación"""
    lat: float
    lon: float
    radius_km: float = 10.0
    weather_active: Optional[str] = None  # 'rain', 'storm', 'wind', etc.
    weather_intensity: float = 1.0
    hrm_cycles: int = 1
    generate_narrative: bool = True


class UserActionRequest(BaseModel):
    """Request para acción del usuario"""
    lat: float
    lon: float
    action_type: str  # 'add_energy', 'remove_energy'
    cell_i: int  # 0-7
    cell_j: int  # 0-7
    intensity: int = 1


class WorldStateRequest(BaseModel):
    """Request para obtener estado del mundo"""
    lat: float
    lon: float


@router.post("/process")
async def process_location(request: LocationRequest) -> Dict:
    """
    Procesa una ubicación completa
    
    Pipeline:
    1. Compute Base Field (determinista)
    2. Load Dynamic Field (json)
    3. Evolve offline if needed
    4. Apply weather if active
    5. Combine fields
    6. Run HRM
    7. Update Dynamic Field
    8. Save
    9. Generate narrative
    """
    if not world_orchestrator:
        raise HTTPException(status_code=500, detail="World Orchestrator not initialized")
    
    try:
        result = world_orchestrator.process_location(
            lat=request.lat,
            lon=request.lon,
            radius_km=request.radius_km,
            weather_active=request.weather_active,
            weather_intensity=request.weather_intensity,
            hrm_cycles=request.hrm_cycles,
            generate_narrative=request.generate_narrative
        )
        
        return result
    
    except Exception as e:
        logger.error(f"Error processing location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/user-action")
async def apply_user_action(request: UserActionRequest) -> Dict:
    """
    Aplica acción del usuario en una celda específica
    
    Modifica el campo dinámico directamente
    """
    if not world_orchestrator:
        raise HTTPException(status_code=500, detail="World Orchestrator not initialized")
    
    try:
        result = world_orchestrator.apply_user_action(
            lat=request.lat,
            lon=request.lon,
            action_type=request.action_type,
            cell_i=request.cell_i,
            cell_j=request.cell_j,
            intensity=request.intensity
        )
        
        return {
            "status": "success",
            "dynamic_field": result
        }
    
    except Exception as e:
        logger.error(f"Error applying user action: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state")
async def get_world_state(lat: float, lon: float) -> Dict:
    """
    Obtiene estado actual del mundo en una ubicación
    
    Sin ejecutar HRM, solo retorna campos actuales
    """
    if not world_orchestrator:
        raise HTTPException(status_code=500, detail="World Orchestrator not initialized")
    
    try:
        result = world_orchestrator.get_world_state(lat, lon)
        return result
    
    except Exception as e:
        logger.error(f"Error getting world state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/stats")
async def get_cache_stats() -> Dict:
    """Obtiene estadísticas del caché de campos dinámicos"""
    if not world_orchestrator:
        raise HTTPException(status_code=500, detail="World Orchestrator not initialized")
    
    try:
        stats = world_orchestrator.get_cache_stats()
        return stats
    
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/cleanup")
async def cleanup_cache(days: int = 30) -> Dict:
    """
    Limpia caché de campos dinámicos antiguos
    
    Args:
        days: Eliminar tiles no usados en X días
    """
    if not world_orchestrator:
        raise HTTPException(status_code=500, detail="World Orchestrator not initialized")
    
    try:
        deleted = world_orchestrator.cleanup_cache(days)
        
        return {
            "status": "success",
            "deleted_tiles": deleted,
            "days_threshold": days
        }
    
    except Exception as e:
        logger.error(f"Error cleaning up cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_system_info() -> Dict:
    """Información del sistema de campos"""
    return {
        "name": "Field System (Base + Dynamic)",
        "version": "1.0.0",
        "architecture": {
            "base_field": {
                "type": "deterministic",
                "inputs": ["coordinates", "DEM", "solar_position", "timestamp"],
                "grid_size": "8x8",
                "token_range": "0-5",
                "persistence": "none (recalculated)"
            },
            "dynamic_field": {
                "type": "evolutionary",
                "storage": "JSON cache",
                "grid_size": "8x8",
                "token_range": "0-5",
                "persistence": "disk",
                "features": [
                    "offline_evolution",
                    "weather_perturbation",
                    "user_interaction",
                    "memory_accumulation"
                ]
            },
            "combination": "base_field + dynamic_field → clamp(0-5)",
            "hrm": "physics_engine",
            "llm": "narrative_interface"
        },
        "pipeline": [
            "1. User selects coord",
            "2. Compute Base Field (deterministic)",
            "3. Load Dynamic Field (json)",
            "4. Evolve offline if needed",
            "5. Apply weather if active",
            "6. Combine fields",
            "7. Run HRM (1-3 cycles)",
            "8. Update Dynamic Field",
            "9. Save JSON",
            "10. LLM narrates if needed"
        ],
        "cache_management": {
            "format": "JSON",
            "location": "backend/world_cache/",
            "naming": "{lat:.4f}_{lon:.4f}.json",
            "cleanup": "automatic (30 days)",
            "max_size": "~1KB per tile"
        }
    }


# Función de inicialización
def init_field_system(
    hrm_checkpoint_path: str,
    llm_model: str = "qwen2.5:3b",
    ollama_url: str = "http://localhost:11434"
):
    """Inicializa el sistema de campos"""
    initialize_orchestrator(
        hrm_checkpoint_path=hrm_checkpoint_path,
        llm_model=llm_model,
        ollama_url=ollama_url
    )
    logger.info("✅ Field System initialized")
