#!/usr/bin/env python3
"""
Módulo de Normalización - Pipeline Científico
============================================

FASE A: Normalizar mediciones por instrumento.

Cada sensor vive en su universo:
- LiDAR → metros / pendiente
- SAR → backscatter
- Espectral → reflectancia
- Térmico → Kelvin

Transformamos a features comparables usando:
- z-score
- percentiles locales
- diferencias contra entorno inmediato
"""

import numpy as np
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class NormalizedFeatures:
    """Features normalizadas por instrumento."""
    candidate_id: str
    features: Dict[str, float]
    raw_measurements: Dict[str, float]
    normalization_method: str
    local_context: Dict[str, Any]

def normalize_data(raw_measurements: Dict[str, Any], 
                  local_buffer_m: int = 200) -> NormalizedFeatures:
    """
    FASE A: Normalizar mediciones por instrumento.
    
    Args:
        raw_measurements: Mediciones crudas por instrumento
        local_buffer_m: Buffer local para contexto
    
    Returns:
        NormalizedFeatures con datos normalizados
    """
    print("[FASE A] Normalizando mediciones por instrumento...", flush=True)
    
    features = {}
    local_context = {
        "buffer_m": local_buffer_m,
        "normalization_timestamp": datetime.now().isoformat()
    }
    
    # Normalizar cada tipo de medición
    # SKIP metadata keys que no son mediciones reales
    skip_keys = ['candidate_id', 'region_name', 'center_lat', 'center_lon', 
                 'environment_type', 'instruments_available', 'instrumental_measurements',
                 'previous_analyses']
    
    for instrument, measurement in raw_measurements.items():
        # Skip metadata keys
        if instrument in skip_keys:
            continue
        
        if not isinstance(measurement, dict):
            continue
        
        value = measurement.get('value', 0.0)
        threshold = measurement.get('threshold', 1.0)
        
        # Calcular z-score local (simulado - en producción usar buffer real)
        if threshold > 0:
            z_score = (value - threshold) / (threshold * 0.3)  # 30% std estimado
        else:
            z_score = 0.0
        
        # Guardar feature normalizada
        feature_name = f"{instrument.lower().replace(' ', '_')}_zscore"
        features[feature_name] = float(np.clip(z_score, -3, 3))  # Clip a ±3σ
        
        print(f"  - {instrument}: value={value:.3f}, threshold={threshold:.3f}, z-score={z_score:.3f}", flush=True)
    
    # Calcular features derivadas
    if len(features) > 0:
        features['mean_deviation'] = float(np.mean(list(features.values())))
        features['max_deviation'] = float(np.max(list(features.values())))
        features['convergence_ratio'] = sum(1 for v in features.values() if v > 1.0) / len(features)
    
    candidate_id = raw_measurements.get('candidate_id', 'UNKNOWN')
    
    # MEJORA 1: Diferenciar ausencia de no aplicable
    if len(features) == 0:
        local_context['features_status'] = 'not_applicable'
        local_context['reason'] = 'no instrument coverage'
        print(f"[FASE A] ⚠️ No hay features (no instrument coverage)", flush=True)
    else:
        local_context['features_status'] = 'available'
        print(f"[FASE A] Normalizadas {len(features)} features", flush=True)
    
    return NormalizedFeatures(
        candidate_id=candidate_id,
        features=features,
        raw_measurements=raw_measurements,
        normalization_method="z-score_local",
        local_context=local_context
    )