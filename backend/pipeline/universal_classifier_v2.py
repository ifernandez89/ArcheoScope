#!/usr/bin/env python3
"""
ArcheoScope Universal Classifier v2.0 - Official Framework
==========================================================

Implementación de la arquitectura de análisis oficial post-unificación:
1.  **Invariantes Geo-Estructurales**: G1 (Geometría), G2 (Estratigrafía/Persistencia), 
    G3 (Anomalía ESS), G4 (Modularidad HRM).
2.  **Material Sensitivity Factor (MSF)**: Ajuste por física del material.
3.  **AMB (Antrópico de Material Blando)**: Nueva clasificación formal.
4.  **Lógica Decisional**: (G1 && G2) || (G1 && G4) || (G2 && G3)
"""

import numpy as np
from typing import Dict, Any, Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ArchaeologicalClassification(Enum):
    NATURAL = "GEOLÓGICO/NATURAL"
    AMB = "ANTRÓPICO DE MATERIAL BLANDO (AMB)"
    ANTHROPIC_STONE = "ANTRÓPICO MONUMENTAL (PIEDRA)"
    CANDIDATE_HIGH = "CANDIDATO DE ALTA PRIORIDAD"
    UNCERTAIN = "INCERTEZA CIENTÍFICA (MONITOREO)"

@dataclass
class UniversalMetrics:
    g1_geometry: float      # Coherencia 3D / Geométrica
    g2_stratigraphy: float  # Persistencia temporal
    g3_anomaly: float       # ESS Superficial / Anomalía pura
    g4_modularity: int      # HRM Peaks / Modularidad
    msf: float = 1.0        # Material Sensitivity Factor

class UniversalClassifierV2:
    """Implementación oficial del Framework ArcheoScope 2026."""
    
    def __init__(self):
        # Umbrales oficiales del framework
        self.THRESHOLDS = {
            "G1_GEOMETRY": 0.915,
            "G2_PERSISTENCE": 0.70,
            "G3_ANOMALY": 0.58,
            "G4_MODULARITY": 120  # Ajuste v2.0: 120 es el punto de ruptura prospectivo
        }
    
    def classify(self, metrics: UniversalMetrics) -> Dict[str, Any]:
        """
        Clasifica un nodo según la lógica (G1&&G2) || (G1&&G4) || (G2&&G3).
        Aplica MSF a G2 para compensar materiales blandos.
        """
        
        # 1. Aplicar MSF (Material Sensitivity Factor)
        # Para materiales blandos (adobe), G2 es naturalmente más bajo.
        # El MSF ajusta la persistencia efectiva.
        # User Suggestion: G2_eff = G2 * MSF. 
        # Pero si MSF es 0.75 para adobe, G2_eff disminuye.
        # Interpretación correcta para "reducir falsos negativos": 
        # Si ES adobe, el umbral G2_persitence debería ser menor.
        # O G2_eff = G2 / MSF. (0.5 / 0.75 = 0.66)
        
        effective_g2 = metrics.g2_stratigraphy / metrics.msf if metrics.msf > 0 else metrics.g2_stratigraphy
        
        # 2. Evaluación de Invariantes
        g1_pass = metrics.g1_geometry >= self.THRESHOLDS["G1_GEOMETRY"]
        g2_pass = effective_g2 >= self.THRESHOLDS["G2_PERSISTENCE"]
        g3_pass = metrics.g3_anomaly >= self.THRESHOLDS["G3_ANOMALY"]
        g4_pass = metrics.g4_modularity >= self.THRESHOLDS["G4_MODULARITY"]
        
        # 3. Lógica Decisional (G1 && G2) || (G1 && G4) || (G2 && G3)
        condition_1 = g1_pass and g2_pass
        condition_2 = g1_pass and g4_pass
        condition_3 = g2_pass and g3_pass
        
        is_anthropic = condition_1 or condition_2 or condition_3
        
        # 4. Determinación de Clase Formal
        veredicto = ArchaeologicalClassification.NATURAL
        
        if is_anthropic:
            if metrics.msf < 1.0:
                veredicto = ArchaeologicalClassification.AMB
            else:
                veredicto = ArchaeologicalClassification.ANTHROPIC_STONE
        elif g1_pass and metrics.g4_modularity > 120:
            # Caso especial Xi'an (Soft Material Anthropic Candidate)
            if metrics.msf < 1.0:
                veredicto = ArchaeologicalClassification.AMB
            else:
                veredicto = ArchaeologicalClassification.CANDIDATE_HIGH
        elif g1_pass or (g2_pass and metrics.g3_anomaly > 0.5):
            veredicto = ArchaeologicalClassification.UNCERTAIN
            
        return {
            "veredicto": veredicto.value,
            "is_anthropic": is_anthropic,
            "metrics_applied": {
                "g1_geometry": metrics.g1_geometry,
                "g2_persistence_eff": effective_g2,
                "g3_anomaly": metrics.g3_anomaly,
                "g4_modularity": metrics.g4_modularity,
                "msf": metrics.msf
            },
            "checks": {
                "G1": g1_pass,
                "G2": g2_pass,
                "G3": g3_pass,
                "G4": g4_pass
            },
            "logic_path": {
                "G1_AND_G2": condition_1,
                "G1_AND_G4": condition_2,
                "G2_AND_G3": condition_3
            }
        }

def estimate_msf(environment: str, geological_context: str) -> float:
    """Estimación automática del MSF basado en contexto."""
    # Piedra / Granito / Basalto
    if "igneous" in geological_context or "metamorphic" in geological_context:
        return 1.0
    # Sedimentary -> Adobe / Tierra apisonada probable en culturas antiguas
    if "sedimentary" in geological_context or environment in ["arid", "desert"]:
        return 0.75
    return 1.0
