ment, max_signal    max_signal = 0.0
        dominant_instrument = "none"
        
        for instrument, data in self.instruments_data.items():
            if isinstance(data, dict) and 'value' in data:
                signal_strength = abs(data['value'])
                if signal_strength > max_signal:
                    max_signal = signal_strength
                    dominant_instrument = instrument
        
        return dominant_instru_km

@dataclass
class TomographicLayer:
    """Capa individual en corte tomográfico."""
    depth_m: float
    instruments_data: Dict[str, Any] = field(default_factory=dict)
    anomaly_intensity: float = 0.0
    archaeological_probability: float = 0.0
    penetration_quality: str = "unknown"  # excellent, good, poor
    
    def get_dominant_signal(self) -> Tuple[str, float]:
        """Obtener señal dominante en esta capa."""
        if not self.instruments_data:
            return "none", 0.0
        
    -> float:
        return (self.lon_min + self.lon_max) / 2
    
    @property
    def area_km2(self) -> float:
        """Área superficial en km²."""
        lat_diff = abs(self.lat_max - self.lat_min)
        lon_diff = abs(self.lon_max - self.lon_min)
        return lat_diff * lon_diff * 111.32 * 111.32  # Aproximación
    
    @property
    def volume_km3(self) -> float:
        """Volumen total en km³."""
        depth_km = abs(self.depth_max - self.depth_min) / 1000
        return self.area_km2 * depth"hydraulic_system"
    DEFENSIVE_FEATURE = "defensive_feature"
    CEREMONIAL_SPACE = "ceremonial_space"

@dataclass
class BoundingBox:
    """Caja delimitadora 3D para análisis territorial."""
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    depth_min: float = 0.0      # superficie
    depth_max: float = -20.0    # 20m profundidad
    
    @property
    def center_lat(self) -> float:
        return (self.lat_min + self.lat_max) / 2
    
    @property
    def center_lon(self) ArchaeologicalType(Enum):
    """Tipos de anomalías arqueológicas volumétricas."""
    STRUCTURE = "structure"
    BURIAL = "burial"
    ACTIVITY_AREA = "activity_area"
    HYDRAULIC_SYSTEM = import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

logger = logging.getLogger(__name__)

class SliceType(Enum):
    """Tipos de cortes tomográficos."""
    XZ = "longitudinal"  # Este-Oeste con profundidad
    YZ = "latitudinal"   # Norte-Sur con profundidad  
    XY = "horizontal"    # Horizontal por profundidad
    TEMPORAL = "temporal" # Evolución temporal

class =========================================

CONCEPTO REVOLUCIONARIO: Transformar ArcheoScope de "detector de sitios" 
a "explicador de territorios" mediante análisis tomográfico volumétrico.

ETP genera perfiles explicables de territorios arqueológicos con:
- Cortes transversales XZ/YZ con profundidad
- ESS superficial, volumétrico y temporal
- Narrativas territoriales automáticas
- Visualización tomográfica interactiva

ESTO CAMBIA TODO: De detección binaria a comprensión territorial completa.
"""

import asyncio
#!/usr/bin/env python3
"""
Environmental Tomographic Profile (ETP) System
=====