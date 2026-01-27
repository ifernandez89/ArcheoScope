#!/usr/bin/env python3
"""
Analysis Router - Endpoints principales de análisis arqueológico
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
import traceback

from ..models import RegionRequest, AnalysisResponse
from ..dependencies import get_system_components
from ..utils import convert_numpy_types

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_region(
    request: RegionRequest,
    components: Dict = Depends(get_system_components)
):
    """
    ## Análisis Arqueológico de Región
    
    Realiza análisis completo de una región geográfica para detectar
    anomalías espaciales potencialmente arqueológicas.
    
    ### Flujo de análisis:
    1. Clasificación de ambiente
    2. Mediciones instrumentales
    3. Detección de anomalías
    4. Validación arqueológica
    5. Explicación IA (opcional)
    """
    
    try:
        # Obtener detector principal
        detector = components.get('core_anomaly_detector')
        if not detector:
            raise HTTPException(
                status_code=503, 
                detail="Detector principal no disponible"
            )
        
        # Validar coordenadas
        if request.lat_min >= request.lat_max:
            raise HTTPException(
                status_code=400,
                detail="lat_min debe ser menor que lat_max"
            )
        
        if request.lon_min >= request.lon_max:
            raise HTTPException(
                status_code=400,
                detail="lon_min debe ser menor que lon_max"
            )
        
        # Calcular coordenadas centrales
        lat_center = (request.lat_min + request.lat_max) / 2
        lon_center = (request.lon_min + request.lon_max) / 2
        
        logger.info(f"Iniciando análisis: {request.region_name} en {lat_center:.4f}, {lon_center:.4f}")
        
        # Ejecutar análisis principal
        result = await detector.detect_anomaly(
            lat=lat_center,
            lon=lon_center,
            lat_min=request.lat_min,
            lat_max=request.lat_max,
            lon_min=request.lon_min,
            lon_max=request.lon_max,
            region_name=request.region_name
        )
        
        # Construir respuesta
        response_data = {
            'region_info': {
                'name': request.region_name,
                'coordinates': {
                    'lat_min': request.lat_min,
                    'lat_max': request.lat_max,
                    'lon_min': request.lon_min,
                    'lon_max': request.lon_max,
                    'center_lat': lat_center,
                    'center_lon': lon_center
                },
                'area_km2': _calculate_area_km2(request),
                'analysis_timestamp': result.explanation  # Temporal, mejorar estructura
            },
            'environment_analysis': {
                'environment_type': result.environment_type,
                'confidence': result.environment_confidence,
                'archaeological_visibility': getattr(result, 'archaeological_visibility', 'unknown'),
                'preservation_potential': getattr(result, 'preservation_potential', 'unknown')
            },
            'anomaly_detection': {
                'anomaly_detected': result.anomaly_detected,
                'confidence_level': result.confidence_level,
                'archaeological_probability': result.archaeological_probability,
                'instruments_converging': result.instruments_converging,
                'minimum_required': result.minimum_required
            },
            'validation_results': {
                'known_site_nearby': result.known_site_nearby,
                'known_site_name': result.known_site_name,
                'known_site_distance_km': result.known_site_distance_km
            },
            'explanation': result.explanation,
            'detection_reasoning': result.detection_reasoning,
            'recommended_validation': result.recommended_validation
        }
        
        # Agregar explicación IA si está disponible
        if request.include_ai_analysis:
            ai_assistant = components.get('ai_assistant')
            if ai_assistant:
                try:
                    ai_explanation = await _get_ai_explanation(ai_assistant, result, request)
                    response_data['ai_analysis'] = ai_explanation
                except Exception as e:
                    logger.warning(f"Error en análisis IA: {e}")
                    response_data['ai_analysis'] = {
                        'available': False,
                        'error': 'IA temporalmente no disponible'
                    }
        
        # Convertir tipos numpy
        response_data = convert_numpy_types(response_data)
        
        logger.info(f"Análisis completado: {request.region_name}")
        return AnalysisResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error interno durante el análisis: {str(e)}"
        )

@router.post("/quick-analyze")
async def quick_analyze_region(
    request: RegionRequest,
    components: Dict = Depends(get_system_components)
):
    """
    Análisis rápido sin IA ni validaciones extensas.
    Optimizado para respuesta rápida.
    """
    
    try:
        # Forzar análisis sin IA
        request.include_ai_analysis = False
        request.include_validation_metrics = False
        
        # Usar el endpoint principal pero optimizado
        return await analyze_region(request, components)
        
    except Exception as e:
        logger.error(f"Error en análisis rápido: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/environments")
async def get_supported_environments():
    """Lista de ambientes soportados y sus características."""
    
    environments = {
        'desert': {
            'description': 'Desiertos áridos con alta visibilidad',
            'primary_sensors': ['thermal', 'optical', 'sar'],
            'archaeological_potential': 'high',
            'examples': ['Sahara', 'Atacama', 'Arabian Desert']
        },
        'forest': {
            'description': 'Bosques y selvas densas',
            'primary_sensors': ['lidar', 'sar', 'optical'],
            'archaeological_potential': 'medium',
            'examples': ['Amazon', 'Congo Basin', 'Southeast Asia']
        },
        'glacier': {
            'description': 'Glaciares de montaña',
            'primary_sensors': ['icesat2', 'sar', 'thermal'],
            'archaeological_potential': 'low',
            'examples': ['Alps', 'Himalayas', 'Andes']
        },
        'shallow_sea': {
            'description': 'Aguas poco profundas (<200m)',
            'primary_sensors': ['sonar', 'sar', 'sst'],
            'archaeological_potential': 'medium',
            'examples': ['Caribbean', 'Mediterranean', 'North Sea']
        },
        'polar_ice': {
            'description': 'Capas de hielo polares',
            'primary_sensors': ['icesat2', 'sar', 'nsidc'],
            'archaeological_potential': 'very_low',
            'examples': ['Antarctica', 'Greenland']
        },
        'mountain': {
            'description': 'Regiones montañosas',
            'primary_sensors': ['dem', 'optical', 'sar'],
            'archaeological_potential': 'high',
            'examples': ['Andes', 'Himalayas', 'Rockies']
        }
    }
    
    return {
        'supported_environments': environments,
        'total_count': len(environments),
        'note': 'Cada ambiente usa sensores específicos optimizados'
    }

# Funciones auxiliares
def _calculate_area_km2(request: RegionRequest) -> float:
    """Calcular área aproximada en km²."""
    lat_diff = abs(request.lat_max - request.lat_min)
    lon_diff = abs(request.lon_max - request.lon_min)
    
    # Aproximación simple (no considera curvatura terrestre)
    lat_km = lat_diff * 111.0  # 1 grado lat ≈ 111 km
    lon_km = lon_diff * 111.0 * abs(cos(radians((request.lat_min + request.lat_max) / 2)))
    
    return lat_km * lon_km

async def _get_ai_explanation(ai_assistant, result, request):
    """Obtener explicación IA del resultado."""
    
    try:
        # Preparar contexto para IA
        context = {
            'region': request.region_name,
            'environment': result.environment_type,
            'anomaly_detected': result.anomaly_detected,
            'confidence': result.confidence_level,
            'probability': result.archaeological_probability
        }
        
        # Solicitar explicación
        explanation = await ai_assistant.explain_analysis(context)
        
        return {
            'available': True,
            'explanation': explanation.get('explanation', ''),
            'confidence': explanation.get('confidence', 0.0),
            'reasoning': explanation.get('reasoning', [])
        }
        
    except Exception as e:
        logger.error(f"Error generando explicación IA: {e}")
        return {
            'available': False,
            'error': str(e)
        }

# Importar funciones matemáticas necesarias
from math import cos, radians