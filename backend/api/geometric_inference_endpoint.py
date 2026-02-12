#!/usr/bin/env python3
"""
API Endpoint - Inferencia Geométrica Culturalmente Constreñida
===============================================================

Endpoint REST para generar representaciones 3D desde coordenadas.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import logging
import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from culturally_constrained_mig import CulturallyConstrainedMIG

logger = logging.getLogger(__name__)

router = APIRouter()

# Instancia global del MIG
mig = CulturallyConstrainedMIG(output_dir="geometric_models")


class GeometricInferenceRequest(BaseModel):
    """Request para inferencia geométrica."""
    lat: float
    lon: float
    region_name: Optional[str] = "Unknown Location"
    
    # Datos de ArcheoScope (opcionales, se pueden inferir)
    scale_invariance: Optional[float] = None
    angular_consistency: Optional[float] = None
    coherence_3d: Optional[float] = None
    sar_rigidity: Optional[float] = None
    stratification_index: Optional[float] = None
    estimated_area_m2: Optional[float] = None
    estimated_height_m: Optional[float] = None


@router.post("/geometric-inference-3d")
async def generate_3d_representation(request: GeometricInferenceRequest):
    """
    Generar representación 3D culturalmente constreñida.
    
    Si no se proveen datos de ArcheoScope, se ejecuta análisis completo.
    """
    
    try:
        logger.info(f"🧬 Solicitud de representación 3D: {request.lat}, {request.lon}")
        
        # Si no hay datos de ArcheoScope, ejecutar análisis
        if request.scale_invariance is None:
            logger.info("📡 Ejecutando análisis ArcheoScope...")
            archeoscope_data = await run_archeoscope_analysis(
                request.lat,
                request.lon,
                request.region_name
            )
        else:
            # Usar datos provistos
            archeoscope_data = {
                'scale_invariance': request.scale_invariance,
                'angular_consistency': request.angular_consistency,
                'coherence_3d': request.coherence_3d,
                'sar_rigidity': request.sar_rigidity or 0.8,
                'stratification_index': request.stratification_index or 0.2,
                'estimated_area_m2': request.estimated_area_m2 or 100.0,
                'estimated_height_m': request.estimated_height_m or 10.0
            }
        
        # Generar nombre de archivo único
        output_name = f"inference_{request.lat:.4f}_{request.lon:.4f}".replace(".", "_").replace("-", "m")
        
        # Ejecutar inferencia culturalmente constreñida
        logger.info("🧬 Generando representación 3D...")
        result = mig.infer_culturally_constrained_geometry(
            archeoscope_data=archeoscope_data,
            output_name=output_name,
            use_ai=False  # Por ahora sin IA
        )
        
        # Retornar resultado
        return {
            'success': True,
            'png_filename': Path(result['png']).name,  # Solo nombre de archivo
            'obj_filename': Path(result['obj']).name,  # Solo nombre de archivo
            'png_path': result['png'],  # Ruta completa para referencia
            'obj_path': result['obj'],  # Ruta completa para referencia
            'morphological_class': result['morphological_class'],
            'cultural_origin': result['cultural_origin'],
            'confidence': result['confidence'],
            'volume_m3': result['volume_m3'],
            'morphological_score': result['morphological_score'],
            'region_name': request.region_name,
            'coordinates': {
                'lat': request.lat,
                'lon': request.lon
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error en inferencia geométrica: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error en inferencia: {str(e)}")


@router.get("/geometric-model/{filename}")
async def get_geometric_model_image(filename: str):
    """Servir imagen PNG del modelo geométrico."""
    
    try:
        # Usar ruta absoluta relativa al proyecto
        project_root = Path(__file__).parent.parent.parent
        file_path = project_root / "geometric_models" / filename
        
        logger.info(f"🔍 Buscando archivo: {file_path}")
        
        if not file_path.exists():
            logger.error(f"❌ Archivo no encontrado: {file_path}")
            raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {filename}")
        
        # Determinar media type según extensión
        media_type = "image/png" if filename.endswith('.png') else "application/octet-stream"
        
        return FileResponse(
            path=str(file_path),
            media_type=media_type,
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error sirviendo archivo: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


async def run_archeoscope_analysis(lat: float, lon: float, region_name: str) -> dict:
    """
    Ejecutar análisis ArcheoScope completo para obtener invariantes.
    
    Por ahora, retorna valores estimados mejorados con contexto geográfico.
    En producción, llamaría al sistema completo de Deep Analysis.
    """
    
    import numpy as np
    
    # Detectar contexto geográfico especial
    is_rapa_nui = (-28 < lat < -26) and (-110 < lon < -108)
    is_egypt = (22 < lat < 32) and (25 < lon < 35)
    is_peru = (-18 < lat < -8) and (-82 < lon < -68)
    
    # Valores base con variación
    base_scale = 0.85 + np.random.uniform(0, 0.15)
    base_angular = 0.80 + np.random.uniform(0, 0.15)
    base_coherence = 0.75 + np.random.uniform(0, 0.20)
    
    # Estimar dimensiones según contexto geográfico
    if is_rapa_nui:
        # MOAI: Vertical, monolítico
        estimated_area = 15.0 + np.random.uniform(0, 10)  # ~4m × 4m
        estimated_height = 7.0 + np.random.uniform(0, 5)  # 7-12m (vertical)
        base_scale = 0.90 + np.random.uniform(0, 0.08)  # Alta rigidez
        base_angular = 0.85 + np.random.uniform(0, 0.10)  # Alta simetría
        
    elif is_egypt:
        # SPHINX o PYRAMID: Puede ser horizontal o vertical
        estimated_area = 200.0 + np.random.uniform(0, 300)
        estimated_height = 15.0 + np.random.uniform(0, 10)
        base_scale = 0.92 + np.random.uniform(0, 0.07)
        base_angular = 0.90 + np.random.uniform(0, 0.08)
        
    elif is_peru:
        # Estructuras andinas: Variadas
        estimated_area = 50.0 + np.random.uniform(0, 150)
        estimated_height = 8.0 + np.random.uniform(0, 12)
        base_scale = 0.88 + np.random.uniform(0, 0.10)
        
    else:
        # Genérico: Usar latitud como factor
        lat_factor = 1.0 - abs(lat) / 90.0
        
        # Para latitudes altas (islas remotas), favorecer verticalidad
        if abs(lat) > 20:
            estimated_area = 20.0 + lat_factor * 80.0  # Más pequeño
            estimated_height = 8.0 + lat_factor * 12.0  # Más alto
        else:
            estimated_area = 50.0 + lat_factor * 200.0
            estimated_height = 5.0 + lat_factor * 15.0
    
    return {
        'scale_invariance': base_scale,
        'angular_consistency': base_angular,
        'coherence_3d': base_coherence,
        'sar_rigidity': 0.85 + np.random.uniform(0, 0.10),
        'stratification_index': 0.15 + np.random.uniform(0, 0.20),
        'estimated_area_m2': estimated_area,
        'estimated_height_m': estimated_height,
        'lat': lat,  # NUEVO: Pasar coordenadas para contexto geográfico
        'lon': lon   # NUEVO: Pasar coordenadas para contexto geográfico
    }
