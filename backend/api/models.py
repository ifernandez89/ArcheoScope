#!/usr/bin/env python3
"""
Modelos Pydantic centralizados para ArcheoScope API
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

# ========== MODELOS DE REQUEST ==========

class RegionRequest(BaseModel):
    """Solicitud de análisis arqueológico de región"""
    lat_min: float = Field(..., ge=-90, le=90, description="Latitud mínima")
    lat_max: float = Field(..., ge=-90, le=90, description="Latitud máxima")
    lon_min: float = Field(..., ge=-180, le=180, description="Longitud mínima")
    lon_max: float = Field(..., ge=-180, le=180, description="Longitud máxima")
    region_name: str = Field(..., min_length=1, max_length=200, description="Nombre de la región")
    
    # Opciones de análisis
    include_ai_analysis: Optional[bool] = Field(True, description="Incluir análisis de IA")
    include_validation_metrics: Optional[bool] = Field(False, description="Incluir métricas de validación")
    resolution_preference: Optional[str] = Field("auto", description="Preferencia de resolución: auto, high, medium, low")

# ========== MODELOS DE RESPONSE ==========

class RegionInfo(BaseModel):
    """Información de la región analizada"""
    name: str
    coordinates: Dict[str, float]
    area_km2: float
    analysis_timestamp: str

class EnvironmentAnalysis(BaseModel):
    """Análisis del ambiente detectado"""
    environment_type: str
    confidence: float
    archaeological_visibility: Optional[str] = None
    preservation_potential: Optional[str] = None

class AnomalyDetection(BaseModel):
    """Resultados de detección de anomalías"""
    anomaly_detected: bool
    confidence_level: str
    archaeological_probability: float
    instruments_converging: int
    minimum_required: int

class ValidationResults(BaseModel):
    """Resultados de validación arqueológica"""
    known_site_nearby: bool
    known_site_name: Optional[str] = None
    known_site_distance_km: Optional[float] = None

class AIAnalysis(BaseModel):
    """Análisis de IA opcional"""
    available: bool
    explanation: Optional[str] = None
    confidence: Optional[float] = None
    reasoning: Optional[List[str]] = None
    error: Optional[str] = None

class AnalysisResponse(BaseModel):
    """Respuesta completa del análisis arqueológico"""
    region_info: RegionInfo
    environment_analysis: EnvironmentAnalysis
    anomaly_detection: AnomalyDetection
    validation_results: ValidationResults
    explanation: str
    detection_reasoning: List[str]
    recommended_validation: List[str]
    
    # Análisis opcionales
    ai_analysis: Optional[AIAnalysis] = None
    validation_metrics: Optional[Dict[str, Any]] = None
    integrated_analysis: Optional[Dict[str, Any]] = None

# ========== MODELOS DE SISTEMA ==========

class SystemStatus(BaseModel):
    """Estado del sistema arqueológico"""
    backend_status: str = Field(..., description="Estado del backend: operational, degraded, error")
    database_status: str = Field(..., description="Estado de la base de datos")
    ai_status: str = Field(..., description="Estado del sistema de IA")
    active_instruments: int = Field(..., description="Número de instrumentos activos")
    last_update: str = Field(..., description="Última actualización del estado")
    version: str = Field(..., description="Versión del sistema")

class InstrumentStatus(BaseModel):
    """Estado de un instrumento específico"""
    name: str
    status: str  # available, degraded, unavailable
    description: str
    last_check: str
    error_message: Optional[str] = None

class ComponentStatus(BaseModel):
    """Estado de un componente del sistema"""
    name: str
    status: str  # loaded, not_loaded, error
    type: Optional[str] = None
    error: Optional[str] = None

# ========== MODELOS DE CATÁLOGO ==========

class ArchaeologicalSite(BaseModel):
    """Sitio arqueológico en el catálogo"""
    id: str
    name: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    site_type: str
    confidence_level: str
    environment: Optional[str] = None
    source: Optional[str] = None
    period: Optional[str] = None
    description: Optional[str] = None

class SitesCatalog(BaseModel):
    """Catálogo de sitios arqueológicos"""
    sites: List[ArchaeologicalSite]
    pagination: Dict[str, int]
    filters_applied: Dict[str, Optional[str]]
    total_count: Optional[int] = None

class DataSource(BaseModel):
    """Fuente de datos satelitales o arqueológicos"""
    name: str
    description: str
    provider: str
    coverage: str
    resolution: Optional[str] = None
    update_frequency: Optional[str] = None
    parameters: Optional[List[str]] = None

class ValidationSite(BaseModel):
    """Sitio de validación para calibración"""
    name: str
    location: Dict[str, float]
    environment: str
    expected_detection: bool
    confidence: str
    validation_purpose: str
    known_parameters: Optional[Dict[str, Any]] = None

# ========== MODELOS VOLUMÉTRICOS ==========

class VolumetricAnalysis(BaseModel):
    """Análisis volumétrico 3D"""
    elevation_analysis: Dict[str, Any]
    geometric_features: Dict[str, Any]
    archaeological_indicators: Dict[str, Any]
    confidence_metrics: Dict[str, Any]

class LidarCapabilities(BaseModel):
    """Capacidades de análisis LiDAR"""
    sensors: Dict[str, Dict[str, str]]
    analysis_types: Dict[str, str]
    environments: Dict[str, str]

class VolumetricBenchmark(BaseModel):
    """Benchmark volumétrico de sitio de referencia"""
    site_name: str
    expected_height_m: float
    geometric_complexity: float
    archaeological_features_detected: int
    additional_metrics: Optional[Dict[str, Any]] = None

# ========== MODELOS DE ERROR ==========

class ErrorResponse(BaseModel):
    """Respuesta de error estándar"""
    error: str
    detail: str
    timestamp: str
    request_id: Optional[str] = None

class ValidationError(BaseModel):
    """Error de validación de datos"""
    field: str
    message: str
    invalid_value: Any

# ========== MODELOS DE CONFIGURACIÓN ==========

class AnalysisConfig(BaseModel):
    """Configuración de análisis"""
    environment_detection: bool = True
    ai_explanation: bool = True
    validation_check: bool = True
    instrument_timeout_seconds: int = 30
    max_area_km2: float = 1000.0

class SystemConfig(BaseModel):
    """Configuración del sistema"""
    lazy_loading: bool = True
    cache_enabled: bool = True
    debug_mode: bool = False
    max_concurrent_analyses: int = 10