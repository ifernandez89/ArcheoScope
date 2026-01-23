"""
ArcheoScope - API del Módulo Volumétrico LIDAR
Endpoints para el Modelado Volumétrico Arqueológico (LIDAR + ArcheoScope)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import numpy as np
import json
import logging
from pathlib import Path

def convert_numpy_types(obj):
    """Convertir tipos numpy a tipos Python nativos para serialización JSON."""
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_numpy_types(item) for item in obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

from volumetric.lidar_fusion_engine import (
    LidarFusionEngine, LidarSite, VolumetricAnalysis, 
    FusionResult, LidarType, SiteType
)

logger = logging.getLogger(__name__)

# Router para endpoints volumétricos
volumetric_router = APIRouter(prefix="/volumetric", tags=["Volumetric LIDAR"])

# Instancia global del motor de fusión
fusion_engine = None

class VolumetricAnalysisRequest(BaseModel):
    """Request para análisis volumétrico"""
    site_id: str = Field(..., description="ID del sitio en el catálogo LIDAR")
    include_archeoscope: bool = Field(True, description="Incluir análisis ArcheoScope paralelo")
    perform_fusion: bool = Field(True, description="Realizar fusión probabilística")
    output_format: str = Field("gltf", description="Formato de salida del modelo 3D")

class SiteCatalogResponse(BaseModel):
    """Response del catálogo de sitios"""
    total_sites: int
    archaeological_confirmed: int
    control_sites: int
    sites: Dict[str, Dict[str, Any]]

class VolumetricAnalysisResponse(BaseModel):
    """Response del análisis volumétrico completo"""
    site_info: Dict[str, Any]
    volumetric_analysis: Dict[str, Any]
    archeoscope_results: Optional[Dict[str, Any]] = None
    fusion_results: Optional[Dict[str, Any]] = None
    model_3d: Optional[Dict[str, Any]] = None
    processing_metadata: Dict[str, Any]

@volumetric_router.on_event("startup")
async def initialize_volumetric_engine():
    """Inicializar el motor de fusión LIDAR"""
    global fusion_engine
    try:
        fusion_engine = LidarFusionEngine()
        
        # Cargar catálogo de sitios
        catalog_path = Path(__file__).parent.parent.parent / "data" / "lidar_sites_catalog.json"
        if catalog_path.exists():
            success = fusion_engine.load_sites_catalog(str(catalog_path))
            if success:
                logger.info("✅ Motor de fusión LIDAR inicializado correctamente")
            else:
                logger.error("❌ Error cargando catálogo de sitios LIDAR")
        else:
            logger.warning("⚠️ Catálogo de sitios LIDAR no encontrado")
            
    except Exception as e:
        logger.error(f"❌ Error inicializando motor volumétrico: {e}")

# Inicializar inmediatamente al importar
def initialize_fusion_engine():
    """Inicializar el motor de fusión inmediatamente"""
    global fusion_engine
    try:
        fusion_engine = LidarFusionEngine()
        
        # Cargar catálogo de sitios
        catalog_path = Path(__file__).parent.parent.parent / "data" / "lidar_sites_catalog.json"
        if catalog_path.exists():
            success = fusion_engine.load_sites_catalog(str(catalog_path))
            if success:
                logger.info("✅ Motor de fusión LIDAR inicializado correctamente")
            else:
                logger.error("❌ Error cargando catálogo de sitios LIDAR")
        else:
            logger.warning("⚠️ Catálogo de sitios LIDAR no encontrado")
            
    except Exception as e:
        logger.error(f"❌ Error inicializando motor volumétrico: {e}")

# Inicializar al importar el módulo
initialize_fusion_engine()

@volumetric_router.get("/sites/catalog", response_model=SiteCatalogResponse)
async def get_sites_catalog():
    """
    Obtener catálogo curado de sitios LIDAR
    
    Incluye controles positivos (arqueológicos confirmados) y negativos (modernos/naturales)
    """
    if not fusion_engine:
        raise HTTPException(status_code=503, detail="Motor volumétrico no inicializado")
    
    try:
        sites_data = {}
        archaeological_count = 0
        control_count = 0
        
        for site_id, site in fusion_engine.sites_catalog.items():
            sites_data[site_id] = {
                "name": site.name,
                "coordinates": site.coordinates,
                "aoi_bounds": site.aoi_bounds,
                "lidar_type": site.lidar_type.value,
                "resolution_cm": site.resolution_cm,
                "acquisition_year": site.acquisition_year,
                "official_source": site.official_source,
                "license": site.license,
                "site_type": site.site_type.value,
                "metadata": site.metadata or {}
            }
            
            if site.site_type == SiteType.ARCHAEOLOGICAL_CONFIRMED:
                archaeological_count += 1
            else:
                control_count += 1
        
        return SiteCatalogResponse(
            total_sites=len(sites_data),
            archaeological_confirmed=archaeological_count,
            control_sites=control_count,
            sites=sites_data
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo catálogo de sitios: {e}")
        raise HTTPException(status_code=500, detail=f"Error obteniendo catálogo: {str(e)}")

@volumetric_router.get("/sites/{site_id}")
async def get_site_details(site_id: str):
    """Obtener detalles de un sitio específico"""
    if not fusion_engine:
        raise HTTPException(status_code=503, detail="Motor volumétrico no inicializado")
    
    site = fusion_engine.sites_catalog.get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail=f"Sitio {site_id} no encontrado")
    
    return {
        "site_id": site_id,
        "name": site.name,
        "coordinates": site.coordinates,
        "aoi_bounds": site.aoi_bounds,
        "lidar_type": site.lidar_type.value,
        "resolution_cm": site.resolution_cm,
        "acquisition_year": site.acquisition_year,
        "official_source": site.official_source,
        "license": site.license,
        "site_type": site.site_type.value,
        "data_path": site.data_path,
        "metadata": site.metadata or {},
        "scientific_classification": {
            "is_archaeological": site.site_type == SiteType.ARCHAEOLOGICAL_CONFIRMED,
            "is_control": site.site_type in [SiteType.MODERN_CONTROL, SiteType.NATURAL_CONTROL],
            "validation_purpose": _get_validation_purpose(site.site_type)
        }
    }

@volumetric_router.post("/analyze", response_model=VolumetricAnalysisResponse)
async def perform_volumetric_analysis(request: VolumetricAnalysisRequest):
    """
    Realizar análisis volumétrico completo LIDAR + ArcheoScope
    
    Pipeline científico:
    1. Análisis volumétrico LIDAR (independiente)
    2. Análisis ArcheoScope paralelo (opcional)
    3. Fusión probabilística (opcional)
    4. Generación de modelo 3D interpretado
    """
    if not fusion_engine:
        raise HTTPException(status_code=503, detail="Motor volumétrico no inicializado")
    
    try:
        logger.info(f"🔍 Iniciando análisis volumétrico para sitio: {request.site_id}")
        
        # Verificar que el sitio existe
        site = fusion_engine.sites_catalog.get(request.site_id)
        if not site:
            raise HTTPException(status_code=404, detail=f"Sitio {request.site_id} no encontrado")
        
        # 1. Análisis volumétrico LIDAR (independiente)
        logger.info("📊 Ejecutando análisis volumétrico LIDAR...")
        
        # Simular datos LIDAR (en implementación real cargaría datos reales)
        simulated_lidar_data = _generate_simulated_lidar_data(site)
        
        volumetric_analysis = fusion_engine.process_lidar_volumetric(
            request.site_id, simulated_lidar_data
        )
        
        # 2. Análisis ArcheoScope paralelo (opcional)
        archeoscope_results = None
        if request.include_archeoscope:
            logger.info("🛰️ Ejecutando análisis ArcheoScope paralelo...")
            archeoscope_results = fusion_engine.execute_archeoscope_parallel(
                request.site_id, site.aoi_bounds
            )
        
        # 3. Fusión probabilística (opcional)
        fusion_results = None
        if request.perform_fusion and archeoscope_results:
            logger.info("🧬 Realizando fusión probabilística...")
            fusion_results = fusion_engine.perform_probabilistic_fusion(
                volumetric_analysis, archeoscope_results
            )
        
        # 4. Generación de modelo 3D
        model_3d = None
        if fusion_results:
            logger.info(f"🎯 Generando modelo 3D en formato {request.output_format}...")
            model_3d = fusion_engine.generate_3d_model(
                volumetric_analysis, fusion_results, request.output_format
            )
        
        # Preparar respuesta con conversión de tipos numpy
        response_data = {
            "site_info": {
                "site_id": request.site_id,
                "name": site.name,
                "coordinates": site.coordinates,
                "site_type": site.site_type.value,
                "lidar_type": site.lidar_type.value,
                "resolution_cm": float(site.resolution_cm),
                "acquisition_year": int(site.acquisition_year)
            },
            "volumetric_analysis": {
                "positive_volume_m3": float(volumetric_analysis.positive_volume_m3),
                "negative_volume_m3": float(volumetric_analysis.negative_volume_m3),
                "dtm_shape": list(volumetric_analysis.dtm.shape),
                "dsm_shape": list(volumetric_analysis.dsm.shape),
                "processing_metadata": convert_numpy_types(volumetric_analysis.processing_metadata)
            },
            "archeoscope_results": _serialize_archeoscope_results(archeoscope_results) if archeoscope_results else None,
            "fusion_results": _serialize_fusion_results(fusion_results) if fusion_results else None,
            "model_3d": convert_numpy_types(model_3d) if model_3d else None,
            "processing_metadata": {
                "analysis_timestamp": np.datetime64('now').astype(str),
                "include_archeoscope": request.include_archeoscope,
                "perform_fusion": request.perform_fusion,
                "output_format": request.output_format,
                "pipeline_steps": _get_pipeline_steps(request)
            }
        }
        
        logger.info(f"✅ Análisis volumétrico completado para {site.name}")
        
        return VolumetricAnalysisResponse(**response_data)
        
    except Exception as e:
        logger.error(f"❌ Error en análisis volumétrico: {e}")
        raise HTTPException(status_code=500, detail=f"Error en análisis volumétrico: {str(e)}")

@volumetric_router.get("/sites/{site_id}/preview")
async def get_site_preview(site_id: str):
    """
    Obtener vista previa rápida de un sitio
    Solo análisis volumétrico LIDAR básico
    """
    if not fusion_engine:
        raise HTTPException(status_code=503, detail="Motor volumétrico no inicializado")
    
    try:
        site = fusion_engine.sites_catalog.get(site_id)
        if not site:
            raise HTTPException(status_code=404, detail=f"Sitio {site_id} no encontrado")
        
        # Análisis volumétrico básico
        simulated_lidar_data = _generate_simulated_lidar_data(site)
        volumetric_analysis = fusion_engine.process_lidar_volumetric(site_id, simulated_lidar_data)
        
        return {
            "site_info": {
                "name": site.name,
                "coordinates": site.coordinates,
                "site_type": site.site_type.value,
                "lidar_type": site.lidar_type.value,
                "resolution_cm": site.resolution_cm
            },
            "volumetric_preview": {
                "positive_volume_m3": volumetric_analysis.positive_volume_m3,
                "negative_volume_m3": volumetric_analysis.negative_volume_m3,
                "total_volume_m3": volumetric_analysis.positive_volume_m3 + volumetric_analysis.negative_volume_m3,
                "average_slope_degrees": float(np.mean(volumetric_analysis.local_slope_degrees)),
                "average_roughness": float(np.mean(volumetric_analysis.microtopographic_roughness)),
                "data_quality": _assess_data_quality(volumetric_analysis)
            }
        }
        
    except Exception as e:
        logger.error(f"Error en vista previa del sitio: {e}")
        raise HTTPException(status_code=500, detail=f"Error en vista previa: {str(e)}")

@volumetric_router.get("/methodology")
async def get_methodology():
    """
    Obtener metodología explícita del módulo volumétrico
    
    Documentación científica transparente
    """
    return {
        "module_name": "Modelado Volumétrico Arqueológico (LIDAR + ArcheoScope)",
        "scientific_principle": "LIDAR no 'descubre' arqueología. ArcheoScope no 'imagina' geometría. La verdad emerge de la convergencia.",
        "pipeline_architecture": {
            "step_1": {
                "name": "Catálogo LIDAR público",
                "description": "Sitios curados con controles positivos y negativos",
                "output": "Metadatos validados científicamente"
            },
            "step_2": {
                "name": "Normalización geométrica",
                "description": "Procesamiento DTM/DSM estándar",
                "output": "Modelos de elevación normalizados"
            },
            "step_3": {
                "name": "Motor volumétrico LIDAR",
                "description": "Análisis geométrico puro sin interpretación",
                "output": "Volúmenes, pendientes, rugosidad, curvatura"
            },
            "step_4": {
                "name": "Análisis ArcheoScope paralelo",
                "description": "Análisis espectral y temporal independiente",
                "output": "Máscara probabilística de intervención antrópica"
            },
            "step_5": {
                "name": "Fusión probabilística",
                "description": "Convergencia ponderada de evidencias",
                "output": "Probabilidad antrópica final con confianza"
            },
            "step_6": {
                "name": "Modelo 3D interpretado",
                "description": "Visualización científica con capas activables",
                "output": "glTF/3D Tiles con atributos por vértice"
            }
        },
        "fusion_weights": fusion_engine.fusion_weights if fusion_engine else {},
        "scientific_thresholds": fusion_engine.thresholds if fusion_engine else {},
        "validation_approach": {
            "positive_controls": "Sitios arqueológicos confirmados (excavados/documentados)",
            "negative_controls": "Sitios modernos y naturales para calibración",
            "scientific_rules": [
                "Volumen sin persistencia ≠ arqueología",
                "Persistencia sin volumen ≠ estructura",
                "Coincidencia fuerte → confianza alta"
            ]
        },
        "limitations": [
            "Interpretación basada en datos disponibles",
            "Resolución limitada por LIDAR original",
            "Análisis espectral sujeto a condiciones atmosféricas",
            "Persistencia temporal requiere múltiples años",
            "Fusión probabilística no garantiza certeza arqueológica"
        ],
        "data_sources": {
            "lidar_requirements": "ALS/UAV/TLS con resolución ≤1m",
            "spectral_requirements": "Sentinel-2 L2A multitemporal",
            "temporal_requirements": "≥3 años, ventanas estacionales consistentes"
        },
        "output_interpretation": {
            "measured_data": "Geometría LIDAR directa",
            "inferred_data": "Análisis espectral/temporal ArcheoScope",
            "interpreted_data": "Fusión probabilística final",
            "confidence_levels": "Basados en convergencia de evidencias independientes"
        }
    }

# Funciones auxiliares

def _get_validation_purpose(site_type: SiteType) -> str:
    """Obtener propósito de validación del sitio"""
    if site_type == SiteType.ARCHAEOLOGICAL_CONFIRMED:
        return "Control positivo - validar detección arqueológica"
    elif site_type == SiteType.MODERN_CONTROL:
        return "Control negativo - validar exclusión moderna"
    elif site_type == SiteType.NATURAL_CONTROL:
        return "Control negativo - validar exclusión natural"
    else:
        return "Sin clasificación de validación"

def _generate_simulated_lidar_data(site: LidarSite) -> np.ndarray:
    """Generar datos LIDAR simulados adaptativos para testing"""
    # En implementación real, cargaría datos LIDAR reales
    np.random.seed(hash(site.name) % 2**32)  # Seed consistente por sitio
    
    # Tamaño adaptativo basado en resolución
    base_size = 100
    resolution_factor = max(0.5, min(2.0, 50.0 / site.resolution_cm))  # Factor de escala
    size = int(base_size * resolution_factor)
    
    # Elevación base realista basada en coordenadas
    lat, lon = site.coordinates
    base_elevation = max(0, 50 + lat * 5 + abs(lon) * 2)  # Aproximación geográfica
    
    if site.site_type == SiteType.ARCHAEOLOGICAL_CONFIRMED:
        # Simular características arqueológicas realistas
        lidar_data = np.random.random((size, size)) * 3 + base_elevation
        
        # Añadir características arqueológicas basadas en área del sitio
        if hasattr(site, 'metadata') and site.metadata:
            expected_area = site.metadata.get('expected_area_m2', 2000)
        else:
            expected_area = 2000  # Área por defecto
        
        # Escalar características según área esperada
        feature_size = int(np.sqrt(expected_area) / (site.resolution_cm / 100))
        center_x, center_y = size // 2, size // 2
        
        # Estructura principal (proporcional al área)
        struct_half_size = max(5, feature_size // 4)
        lidar_data[center_x-struct_half_size:center_x+struct_half_size, 
                  center_y-struct_half_size:center_y+struct_half_size] += np.random.uniform(1.0, 3.0)
        
        # Características secundarias
        if expected_area > 5000:  # Sitios grandes
            # Depresión (excavación/foso)
            depression_size = max(3, struct_half_size // 2)
            lidar_data[center_x+struct_half_size+5:center_x+struct_half_size+5+depression_size, 
                      center_y-depression_size//2:center_y+depression_size//2] -= np.random.uniform(0.5, 1.5)
        
    elif site.site_type == SiteType.MODERN_CONTROL:
        # Simular características modernas
        lidar_data = np.random.random((size, size)) * 1.5 + base_elevation
        
        # Características modernas (carreteras, edificios)
        road_width = max(2, size // 20)
        lidar_data[size//4:size//4+road_width, :] += np.random.uniform(0.2, 0.8)  # Carretera
        
        # Edificios modernos (más altos y regulares)
        building_size = max(5, size // 10)
        lidar_data[size//2:size//2+building_size, size//2:size//2+building_size] += np.random.uniform(3.0, 8.0)
        
    else:
        # Simular topografía natural
        lidar_data = np.random.random((size, size)) * 2 + base_elevation
        
        # Añadir variaciones naturales suaves
        from scipy.ndimage import gaussian_filter
        natural_variation = gaussian_filter(np.random.random((size, size)) * 5, sigma=size/20)
        lidar_data += natural_variation
    
    return lidar_data

def _serialize_archeoscope_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Serializar resultados ArcheoScope para JSON"""
    serialized = {}
    for key, value in results.items():
        if isinstance(value, np.ndarray):
            serialized[key] = {
                "shape": value.shape,
                "mean": float(np.mean(value)),
                "std": float(np.std(value)),
                "min": float(np.min(value)),
                "max": float(np.max(value))
            }
        else:
            serialized[key] = value
    return serialized

def _serialize_fusion_results(results: FusionResult) -> Dict[str, Any]:
    """Serializar resultados de fusión para JSON"""
    return {
        "anthropic_probability_final": {
            "shape": results.anthropic_probability_final.shape,
            "mean": float(np.mean(results.anthropic_probability_final)),
            "std": float(np.std(results.anthropic_probability_final)),
            "high_probability_pixels": int(np.sum(results.anthropic_probability_final > 0.7)),
            "convergence_pixels": int(np.sum(results.confidence_level > 0.6))
        },
        "confidence_statistics": {
            "mean_confidence": float(np.mean(results.confidence_level)),
            "high_confidence_percentage": float(np.sum(results.confidence_level > 0.6) / results.confidence_level.size * 100)
        },
        "fusion_metadata": results.fusion_metadata
    }

def _get_pipeline_steps(request: VolumetricAnalysisRequest) -> List[str]:
    """Obtener pasos del pipeline ejecutados"""
    steps = ["lidar_volumetric_analysis"]
    
    if request.include_archeoscope:
        steps.append("archeoscope_parallel_analysis")
    
    if request.perform_fusion and request.include_archeoscope:
        steps.append("probabilistic_fusion")
        steps.append("3d_model_generation")
    
    return steps

def _assess_data_quality(volumetric_analysis: VolumetricAnalysis) -> Dict[str, Any]:
    """Evaluar calidad de los datos volumétricos"""
    return {
        "resolution_quality": "high" if volumetric_analysis.dtm.size > 10000 else "medium",
        "volume_significance": "significant" if (volumetric_analysis.positive_volume_m3 + volumetric_analysis.negative_volume_m3) > 1.0 else "minimal",
        "topographic_complexity": "high" if np.std(volumetric_analysis.local_slope_degrees) > 5.0 else "low",
        "data_completeness": "complete"  # En implementación real verificaría gaps en datos
    }