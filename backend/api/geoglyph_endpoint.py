#!/usr/bin/env python3
"""
API Endpoint para Detección de Geoglifos
=========================================

Endpoints:
- POST /geoglyph/detect - Detectar geoglifo en coordenadas
- GET /geoglyph/zones/promising - Zonas prometedoras para exploración
- POST /geoglyph/batch-scan - Escaneo batch de región
- GET /geoglyph/types - Tipos de geoglifos conocidos
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path
import logging

# Agregar backend al path
sys.path.append(str(Path(__file__).parent.parent))

from geoglyph_detector import (
    GeoglyphDetector,
    DetectionMode,
    GeoglyphType,
    get_promising_zones
)

logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix="/geoglyph", tags=["Geoglyph Detection"])

# Modelos Pydantic
class GeoglyphDetectionRequest(BaseModel):
    """Solicitud de detección de geoglifo"""
    lat: float = Field(..., description="Latitud central")
    lon: float = Field(..., description="Longitud central")
    lat_min: float = Field(..., description="Latitud mínima del bbox")
    lat_max: float = Field(..., description="Latitud máxima del bbox")
    lon_min: float = Field(..., description="Longitud mínima del bbox")
    lon_max: float = Field(..., description="Longitud máxima del bbox")
    resolution_m: float = Field(1.0, description="Resolución espacial en m/pixel")
    mode: str = Field("scientific", description="Modo: scientific, explorer, cognitive")
    
    class Config:
        schema_extra = {
            "example": {
                "lat": 26.5,
                "lon": 38.5,
                "lat_min": 26.4,
                "lat_max": 26.6,
                "lon_min": 38.4,
                "lon_max": 38.6,
                "resolution_m": 0.5,
                "mode": "scientific"
            }
        }


class BatchScanRequest(BaseModel):
    """Solicitud de escaneo batch"""
    zone_id: str = Field(..., description="ID de zona prometedora")
    grid_size_km: float = Field(5.0, description="Tamaño de celda en km")
    mode: str = Field("explorer", description="Modo de detección")
    
    class Config:
        schema_extra = {
            "example": {
                "zone_id": "harrat_uwayrid_south",
                "grid_size_km": 5.0,
                "mode": "explorer"
            }
        }


# Estado global
detectors = {
    "scientific": GeoglyphDetector(DetectionMode.SCIENTIFIC),
    "explorer": GeoglyphDetector(DetectionMode.EXPLORER),
    "cognitive": GeoglyphDetector(DetectionMode.COGNITIVE)
}


@router.post("/detect")
async def detect_geoglyph(request: GeoglyphDetectionRequest):
    """
    Detectar geoglifo en coordenadas específicas
    
    Pipeline completo:
    1. Verificación de resolución espacial
    2. Análisis de orientación y simetría
    3. Contexto volcánico (harrats)
    4. Paleohidrología (agua antigua)
    5. Alineaciones solares/estelares
    6. Scoring cultural
    7. Clasificación de tipo
    
    Modos:
    - **scientific**: Umbrales estrictos, FP=NO, ideal para papers
    - **explorer**: Más sensibilidad, detecta "rarezas"
    - **cognitive**: Patrones no lineales, solo señalar
    """
    
    try:
        # Validar modo
        if request.mode not in detectors:
            raise HTTPException(
                status_code=400,
                detail=f"Modo inválido. Opciones: {list(detectors.keys())}"
            )
        
        detector = detectors[request.mode]
        
        logger.info(f"🔍 Detectando geoglifo en ({request.lat}, {request.lon})")
        logger.info(f"   Modo: {request.mode}, Resolución: {request.resolution_m}m")
        
        # Detectar
        result = detector.detect_geoglyph(
            lat=request.lat,
            lon=request.lon,
            lat_min=request.lat_min,
            lat_max=request.lat_max,
            lon_min=request.lon_min,
            lon_max=request.lon_max,
            resolution_m=request.resolution_m
        )
        
        # Convertir a dict
        return {
            "status": "success",
            "result": {
                "candidate_id": result.candidate_id,
                "geoglyph_type": result.geoglyph_type.value,
                "type_confidence": result.type_confidence,
                "location": {
                    "lat": result.lat,
                    "lon": result.lon,
                    "bbox": result.bbox
                },
                "orientation": {
                    "azimuth_deg": result.orientation.azimuth_deg,
                    "major_axis_m": result.orientation.major_axis_length_m,
                    "minor_axis_m": result.orientation.minor_axis_length_m,
                    "aspect_ratio": result.orientation.aspect_ratio,
                    "symmetry": 1 - result.orientation.bilateral_symmetry,
                    "is_nw_se": result.orientation.is_nw_se,
                    "is_e_w": result.orientation.is_e_w
                },
                "volcanic_context": {
                    "distance_to_basalt_km": result.volcanic_context.distance_to_basalt_flow_km,
                    "on_stable_surface": result.volcanic_context.on_stable_surface,
                    "on_young_flow": result.volcanic_context.on_young_flow
                } if result.volcanic_context else None,
                "paleo_hydrology": {
                    "distance_to_wadi_km": result.paleo_hydrology.distance_to_wadi_km,
                    "on_sediment_transition": result.paleo_hydrology.on_sediment_transition,
                    "seasonal_water_prob": result.paleo_hydrology.seasonal_water_probability
                } if result.paleo_hydrology else None,
                "celestial_alignment": {
                    "best_solar": result.celestial_alignment.best_solar_alignment,
                    "summer_solstice": result.celestial_alignment.summer_solstice_alignment,
                    "winter_solstice": result.celestial_alignment.winter_solstice_alignment,
                    "equinox": result.celestial_alignment.equinox_alignment
                } if result.celestial_alignment else None,
                "scores": {
                    "cultural": result.cultural_score,
                    "form": result.form_score,
                    "context": result.context_score,
                    "orientation": result.orientation_score,
                    "hydrology": result.hydrology_score
                },
                "validation": {
                    "needs_validation": result.needs_validation,
                    "priority": result.validation_priority,
                    "recommended_resolution_m": result.recommended_resolution_m,
                    "paper_level_discovery": result.paper_level_discovery
                },
                "detection_mode": result.detection_mode.value,
                "timestamp": result.detection_timestamp,
                "reasoning": result.detection_reasoning,
                "fp_risks": result.false_positive_risks
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error en detección: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zones/promising")
async def get_promising_exploration_zones():
    """
    Obtener zonas prometedoras para exploración de geoglifos
    
    Criterios:
    - Basalto antiguo
    - Baja intervención moderna
    - Cercanía a paleorutas
    - Ausencia de papers arqueológicos
    
    Regiones:
    - Sur de Harrat Uwayrid
    - Límite Arabia-Jordania
    - Bordes de Rub' al Khali
    """
    
    zones = get_promising_zones()
    
    return {
        "status": "success",
        "total_zones": len(zones),
        "zones": zones,
        "note": "Zonas no catalogadas con alto potencial de descubrimiento"
    }


@router.post("/batch-scan")
async def batch_scan_zone(request: BatchScanRequest):
    """
    Escaneo batch de zona prometedora
    
    Divide la zona en grid y escanea cada celda.
    Útil para exploración sistemática.
    
    NOTA: Esta es una operación costosa que puede tomar tiempo.
    Se recomienda usar modo 'explorer' o 'cognitive'.
    """
    
    try:
        zones = get_promising_zones()
        
        if request.zone_id not in zones:
            raise HTTPException(
                status_code=404,
                detail=f"Zona no encontrada. Disponibles: {list(zones.keys())}"
            )
        
        zone = zones[request.zone_id]
        lat_min, lat_max, lon_min, lon_max = zone["bbox"]
        
        # Calcular grid
        # TODO: Implementar escaneo real
        # Por ahora, retornar metadata
        
        lat_cells = int((lat_max - lat_min) * 111 / request.grid_size_km)
        lon_cells = int((lon_max - lon_min) * 111 / request.grid_size_km)
        total_cells = lat_cells * lon_cells
        
        return {
            "status": "queued",
            "zone": zone,
            "grid": {
                "lat_cells": lat_cells,
                "lon_cells": lon_cells,
                "total_cells": total_cells,
                "cell_size_km": request.grid_size_km
            },
            "mode": request.mode,
            "estimated_time_hours": total_cells * 0.1,  # ~6 min por celda
            "note": "Escaneo batch en desarrollo. Use /detect para análisis individual."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error en batch scan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/types")
async def get_geoglyph_types():
    """
    Tipos de geoglifos conocidos
    
    Retorna información sobre los tipos de geoglifos que el sistema
    puede detectar y clasificar.
    """
    
    types_info = {
        "gate": {
            "name": "Gate (Puerta)",
            "region": "Arabia",
            "characteristics": [
                "Estructura rectangular o trapezoidal",
                "Aspect ratio 1.5-3.0",
                "Orientación variable"
            ],
            "typical_size_m": "50-200"
        },
        "pendant": {
            "name": "Pendant (Pendiente)",
            "region": "Arabia",
            "characteristics": [
                "Estructura alargada con 'cola'",
                "Aspect ratio > 3.0",
                "Orientación NW-SE o E-W común",
                "Cola apunta a zonas bajas"
            ],
            "typical_size_m": "100-500"
        },
        "wheel": {
            "name": "Wheel (Rueda)",
            "region": "Arabia, Jordania",
            "characteristics": [
                "Estructura circular o radial",
                "Aspect ratio < 1.5",
                "Rayos desde centro"
            ],
            "typical_size_m": "20-100"
        },
        "kite": {
            "name": "Kite (Cometa)",
            "region": "Jordania, Sinaí, Arabia",
            "characteristics": [
                "Forma de cometa",
                "Muros convergentes",
                "Asociado a caza"
            ],
            "typical_size_m": "100-1000"
        },
        "line": {
            "name": "Line (Línea)",
            "region": "Nazca, Perú",
            "characteristics": [
                "Líneas rectas",
                "Longitud variable",
                "Alineaciones astronómicas"
            ],
            "typical_size_m": "100-10000"
        },
        "figure": {
            "name": "Figure (Figura)",
            "region": "Nazca, Perú",
            "characteristics": [
                "Formas zoomorfas o geométricas",
                "Alta complejidad",
                "Simetría variable"
            ],
            "typical_size_m": "50-500"
        }
    }
    
    return {
        "status": "success",
        "total_types": len(types_info),
        "types": types_info,
        "note": "Clasificación basada en literatura arqueológica"
    }


@router.get("/modes")
async def get_detection_modes():
    """
    Modos operativos del detector
    
    Cada modo tiene diferentes umbrales y filosofía.
    """
    
    modes_info = {
        "scientific": {
            "name": "Científico Duro",
            "philosophy": "Umbrales estrictos, FP=NO, ideal para papers",
            "thresholds": {
                "min_cultural_score": 0.75,
                "min_symmetry": 0.70,
                "max_fp_risk": 0.15,
                "min_resolution_m": 1.0
            },
            "use_case": "Publicaciones científicas, validación rigurosa"
        },
        "explorer": {
            "name": "Explorador",
            "philosophy": "Más sensibilidad, detecta 'cosas raras'",
            "thresholds": {
                "min_cultural_score": 0.50,
                "min_symmetry": 0.50,
                "max_fp_risk": 0.35,
                "min_resolution_m": 2.0
            },
            "use_case": "Descubrimientos, exploración de nuevas zonas"
        },
        "cognitive": {
            "name": "Cognitivo / Anómalo",
            "philosophy": "Patrones no lineales, solo señalar, NO afirmar",
            "thresholds": {
                "min_cultural_score": 0.30,
                "min_symmetry": 0.30,
                "max_fp_risk": 0.50,
                "min_resolution_m": 5.0
            },
            "use_case": "Hipótesis nuevas, patrones inusuales"
        }
    }
    
    return {
        "status": "success",
        "total_modes": len(modes_info),
        "modes": modes_info,
        "recommendation": "Usar 'scientific' para papers, 'explorer' para descubrimientos"
    }
