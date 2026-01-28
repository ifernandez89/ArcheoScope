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
    confidence: float

@dataclass
class LandscapeEvolution:
    """Evolución del paisaje en el tiempo."""
    natural_baseline: str
    human_modifications: List[str]
    abandonment_indicators: List[str]
    current_state: str

@dataclass
class EnvironmentalTomographicProfile:
    """Perfil tomográfico ambiental completo - NÚCLEO DEL SISTEMA."""
    
    # Identificación
    territory_id: str
    bounds: BoundingBox
    resolution_m: float
    generation_timestamp: datetime = field(default_factory=datetime.now)
    
    # Cortes tomográficos
    xz_profile: Optional[TomographicSlice] = None  # Longitudinal
    yz_profile: Optional[TomographicSlice] = None  # Latitudinal
    xy_profiles: List[TomographicSlice] = field(default_factory=list)  # Por profundidad
    temporal_profile: Optional[Dict[str, Any]] = None
    
    # ESS evolucionado - CLAVE DEL CONCEPTO
    ess_superficial: float = 0.0
    ess_volumetrico: float = 0.0
    ess_temporal: float = 0.0
    
    # Métricas 3D
    coherencia_3d: float = 0.0
    persistencia_temporal: float = 0.0
    densidad_arqueologica_m3: float = 0.0
    
    # Interpretación narrativa - REVOLUCIÓN CONCEPTUAL
    narrative_explanation: str = ""
    occupational_history: List[OccupationPeriod] = field(default_factory=list)
    territorial_function: Optional[TerritorialFunction] = None
    landscape_evolution: Optional[LandscapeEvolution] = None
    
    # Datos para visualización
    visualization_data: Dict[str, Any] = field(default_factory=dict)
    
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