#!/usr/bin/env python3
"""
Environmental Tomographic Profile (ETP) - Core System
====================================================

REVOLUCIÓN CONCEPTUAL: ArcheoScope pasa de "detector" a "explicador"

ETP transforma el análisis arqueológico mediante:
- Perfiles tomográficos XZ/YZ con profundidad
- ESS volumétrico y temporal
- Narrativas territoriales explicables
- Visualización 3D interactiva

De "¿Hay un sitio?" a "¿Qué cuenta este territorio?"
"""

import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class SliceType(Enum):
    XZ = "longitudinal"
    YZ = "latitudinal" 
    XY = "horizontal"
    TEMPORAL = "temporal"

@dataclass
class BoundingBox:
    """Caja delimitadora 3D."""
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    depth_min: float = 0.0
    depth_max: float = -20.0
    
    @property
    def center_lat(self) -> float:
        return (self.lat_min + self.lat_max) / 2
    
    @property
    def center_lon(self) -> float:
        return (self.lon_min + self.lon_max) / 2
    
    @property
    def area_km2(self) -> float:
        """Calcular área en km²."""
        lat_extent = (self.lat_max - self.lat_min) * 111.32
        lon_extent = (self.lon_max - self.lon_min) * 111.32 * np.cos(np.radians(self.center_lat))
        return lat_extent * lon_extent
    
    @property
    def volume_km3(self) -> float:
        """Calcular volumen en km³."""
        depth_extent = abs(self.depth_max - self.depth_min) / 1000  # metros a km
        return self.area_km2 * depth_extent

@dataclass
class TomographicLayer:
    """Capa tomográfica individual."""
    depth_m: float
    instruments_data: Dict[str, Any] = field(default_factory=dict)
    anomaly_intensity: float = 0.0
    archaeological_probability: float = 0.0

@dataclass
class VolumetricAnomaly:
    """Anomalía volumétrica detectada."""
    center_3d: Tuple[float, float, float]  # x, y, z
    extent_3d: Tuple[float, float, float]  # ancho, largo, profundidad
    intensity: float
    archaeological_type: str
    temporal_range: Tuple[int, int]  # años
    confidence: float
    instruments_supporting: List[str]

@dataclass
class TomographicSlice:
    """Corte tomográfico individual."""
    slice_type: SliceType
    depth_range: Tuple[float, float]
    layers: List[TomographicLayer] = field(default_factory=list)
    anomalies: List[VolumetricAnomaly] = field(default_factory=list)
    slice_ess: float = 0.0
    coherence_score: float = 0.0
    
    def get_max_anomaly_depth(self) -> float:
        """Obtener profundidad máxima de anomalías."""
        if not self.anomalies:
            return 0.0
        return min(anomaly.center_3d[2] for anomaly in self.anomalies)

@dataclass
class OccupationPeriod:
    """Período de ocupación identificado."""
    start_year: int
    end_year: int
    occupation_type: str  # ceremonial, residential, productive
    evidence_strength: float
    description: str

@dataclass
class TerritorialFunction:
    """Función territorial identificada."""
    primary_function: str
    secondary_functions: List[str]
    spatial_organization: str
    confidence: float = 0.5

@dataclass
class LandscapeEvolution:
    """Evolución del paisaje territorial."""
    natural_baseline: str
    human_modifications: List[str]
    abandonment_indicators: List[str]
    current_state: str

@dataclass
class EnvironmentalTomographicProfile:
    """Perfil Tomográfico Ambiental completo - NÚCLEO DEL SISTEMA ETP."""
    
    # Identificación (campos requeridos primero)
    territory_id: str
    bounds: BoundingBox
    resolution_m: float
    
    # Perfiles tomográficos principales (campos requeridos)
    xz_profile: TomographicSlice
    yz_profile: TomographicSlice
    xy_profiles: List[TomographicSlice]
    temporal_profile: Dict[str, Any]
    
    # Métricas ESS evolucionadas (campos requeridos)
    ess_superficial: float
    ess_volumetrico: float
    ess_temporal: float
    
    # Métricas 3D/4D (campos requeridos)
    coherencia_3d: float
    persistencia_temporal: float
    densidad_arqueologica_m3: float
    
    # Campos con valores por defecto
    generation_timestamp: datetime = field(default_factory=datetime.now)
    
    # Cobertura instrumental (NUEVO - separado de ESS)
    instrumental_coverage: Dict[str, Any] = field(default_factory=dict)
    
    # Contexto geológico (campos opcionales) - NOMBRES CORREGIDOS
    geological_context: Any = None
    geological_compatibility: Any = None  # GeologicalCompatibilityScore (no geological_compatibility_score)
    
    # Contexto hidrográfico (campos opcionales) - NOMBRES CORREGIDOS
    hydrographic_features: List[Any] = field(default_factory=list)
    water_availability: Any = None  # WaterAvailabilityScore (no water_availability_score)
    
    # Validación externa (campos opcionales) - NOMBRES CORREGIDOS
    external_sites: List[Any] = field(default_factory=list)  # (no external_archaeological_sites)
    external_consistency: Any = None  # ExternalConsistencyScore (no external_consistency_score)
    
    # Trazas humanas (campos opcionales)
    human_traces: List[Any] = field(default_factory=list)
    territorial_use_profile: Any = None
    
    # Interpretación narrativa (campos opcionales)
    narrative_explanation: str = ""
    occupational_history: List[OccupationPeriod] = field(default_factory=list)
    territorial_function: Optional[TerritorialFunction] = None
    landscape_evolution: Optional[LandscapeEvolution] = None
    
    # Datos de visualización (campos opcionales)
    visualization_data: Dict[str, Any] = field(default_factory=dict)
    
    def get_comprehensive_score(self) -> float:
        """Calcular score comprensivo que integra todas las dimensiones."""
        
        # Score base (ESS temporal)
        base_score = self.ess_temporal
        
        # Factores de contexto
        geological_factor = 1.0
        if self.geological_compatibility:
            geological_factor = 1.0 + (self.geological_compatibility.gcs_score - 0.5) * 0.2
        
        hydrographic_factor = 1.0
        if self.water_availability:
            hydrographic_factor = 1.0 + (self.water_availability.settlement_viability - 0.5) * 0.15
        
        external_factor = 1.0
        if self.external_consistency:
            external_factor = 1.0 + (self.external_consistency.ecs_score - 0.5) * 0.25
        
        human_traces_factor = 1.0
        if self.territorial_use_profile:
            human_traces_factor = 1.0 + (self.territorial_use_profile.settlement_potential - 0.5) * 0.1
        
        # Score comprensivo
        comprehensive_score = (base_score * geological_factor * hydrographic_factor * 
                             external_factor * human_traces_factor)
        
        return min(1.0, comprehensive_score)
    
    def get_confidence_level(self) -> str:
        """Obtener nivel de confianza basado en múltiples factores."""
        
        confidence_factors = []
        
        # Factor de coherencia 3D
        confidence_factors.append(self.coherencia_3d)
        
        # Factor geológico
        if self.geological_compatibility:
            confidence_factors.append(self.geological_compatibility.gcs_score)
        
        # Factor de validación externa
        if self.external_consistency:
            confidence_factors.append(self.external_consistency.ecs_score)
        
        # Factor de persistencia temporal
        confidence_factors.append(self.persistencia_temporal)
        
        avg_confidence = np.mean(confidence_factors) if confidence_factors else 0.5
        
        if avg_confidence > 0.8:
            return "very_high"
        elif avg_confidence > 0.6:
            return "high"
        elif avg_confidence > 0.4:
            return "moderate"
        else:
            return "low"
    
    def get_archaeological_recommendation(self) -> str:
        """Generar recomendación arqueológica basada en análisis integral."""
        
        comprehensive_score = self.get_comprehensive_score()
        confidence = self.get_confidence_level()
        
        if comprehensive_score > 0.8 and confidence in ["high", "very_high"]:
            return "immediate_investigation"
        elif comprehensive_score > 0.6 and confidence in ["moderate", "high", "very_high"]:
            return "detailed_survey"
        elif comprehensive_score > 0.4:
            return "preliminary_assessment"
        else:
            return "monitoring"
    
    def get_summary_metrics(self) -> Dict[str, float]:
        """Obtener métricas resumen para dashboard."""
        return {
            'ess_superficial': self.ess_superficial,
            'ess_volumetrico': self.ess_volumetrico,
            'ess_temporal': self.ess_temporal,
            'coherencia_3d': self.coherencia_3d,
            'persistencia_temporal': self.persistencia_temporal,
            'densidad_arqueologica': self.densidad_arqueologica_m3
        }
    
    def get_dominant_period(self) -> Optional[OccupationPeriod]:
        """Obtener período de ocupación dominante."""
        if not self.occupational_history:
            return None
        return max(self.occupational_history, key=lambda p: p.evidence_strength)
    
    def generate_territorial_summary(self) -> str:
        """Generar resumen territorial de una línea."""
        if not self.territorial_function:
            return f"Territorio con ESS volumétrico {self.ess_volumetrico:.2f}"
        
        dominant_period = self.get_dominant_period()
        period_text = f" ({dominant_period.occupation_type}, {dominant_period.start_year}-{dominant_period.end_year})" if dominant_period else ""
        
        return f"{self.territorial_function.primary_function.title()} territory{period_text} - ESS: {self.ess_volumetrico:.2f}"

@dataclass
class LandscapeEvolution:
    """Evolución del paisaje en el tiempo."""
    natural_baseline: str
    human_modifications: List[str]
    abandonment_indicators: List[str]
    current_state: str
