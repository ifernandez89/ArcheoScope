#!/usr/bin/env python3
"""
Módulo de Detección de Anomalías - Pipeline Científico
=====================================================

FASE B: Detectar anomalía pura (sin arqueología todavía).

Objetivo: "Esto no se parece a su entorno"

Técnicas:
- Isolation Forest (simulado)
- LOF - Local Outlier Factor (simulado)
- PCA residuals (simulado)
"""

from typing import List
from dataclasses import dataclass
from .normalization import NormalizedFeatures

@dataclass
class AnomalyResult:
    """Resultado de detección de anomalía pura."""
    anomaly_score: float  # 0.0 - 1.0
    outlier_dimensions: List[str]
    method: str
    confidence: str  # "high", "medium", "low"

def detect_anomaly(normalized: NormalizedFeatures) -> AnomalyResult:
    """
    FASE B: Detectar anomalía pura (sin arqueología todavía).
    
    Args:
        normalized: Features normalizadas
    
    Returns:
        AnomalyResult con score y dimensiones outlier
    """
    print("[FASE B] Detectando anomalía pura...", flush=True)
    
    features = normalized.features
    
    # Calcular anomaly score basado en desviaciones
    deviations = [abs(v) for v in features.values() if isinstance(v, (int, float))]
    
    if len(deviations) == 0:
        anomaly_score = 0.0
        outlier_dims = []
        confidence = "none"
    else:
        # Score basado en cuántas features son outliers (>2σ)
        outlier_count = sum(1 for d in deviations if d > 2.0)
        anomaly_score = min(1.0, outlier_count / max(1, len(deviations)))
        
        # Identificar dimensiones outlier
        outlier_dims = [
            k for k, v in features.items() 
            if isinstance(v, (int, float)) and abs(v) > 2.0
        ]
        
        # Confianza basada en convergencia
        if anomaly_score > 0.7:
            confidence = "high"
        elif anomaly_score > 0.4:
            confidence = "medium"
        else:
            confidence = "low"
    
    print(f"[FASE B] Anomaly score: {anomaly_score:.3f}, outliers: {len(outlier_dims)}, confidence: {confidence}", flush=True)
    
    return AnomalyResult(
        anomaly_score=anomaly_score,
        outlier_dimensions=outlier_dims,
        method="deviation_based",
        confidence=confidence
    )