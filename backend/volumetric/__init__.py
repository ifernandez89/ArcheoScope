#!/usr/bin/env python3
"""
ArcheoScope Volumetric Inference System

Sistema completo de inferencia volumétrica probabilística para arqueología remota.

PARADIGMA EPISTEMOLÓGICO:
"ArcheoScope no reconstruye estructuras: reconstruye espacios de posibilidad 
geométrica consistentes con firmas físicas persistentes."

COMPONENTES:
- GeometricInferenceEngine: Pipeline completo de inferencia volumétrica
- Phi4GeometricEvaluator: Evaluación de consistencia con phi4-mini-reasoning
- VolumetricIntegrator: Integración con API principal de ArcheoScope

NIVEL DE RECONSTRUCCIÓN: I/II (Geométrica Volumétrica Inferida)
- Forma aproximada con escala correcta
- Relaciones espaciales coherentes
- Incertidumbre explícita
- NO detalles arquitectónicos, función cultural o afirmaciones históricas
"""

from .geometric_inference_engine import (
    GeometricInferenceEngine,
    SpatialSignature,
    VolumetricField,
    GeometricModel,
    MorphologicalClass,
    InferenceLevel
)

from .phi4_geometric_evaluator import (
    Phi4GeometricEvaluator,
    GeometricConsistencyReport
)

__all__ = [
    'GeometricInferenceEngine',
    'Phi4GeometricEvaluator',
    'SpatialSignature',
    'VolumetricField', 
    'GeometricModel',
    'GeometricConsistencyReport',
    'MorphologicalClass',
    'InferenceLevel'
]