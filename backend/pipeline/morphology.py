#!/usr/bin/env python3
"""
Módulo de Análisis Morfológico - Pipeline Científico
===================================================

FASE C: Análisis morfológico explícito.

Métricas clave:
- simetría radial
- regularidad de bordes
- pendiente constante
- curvatura artificial

Esto EXPLICA el sistema, no solo predice.
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from .normalization import NormalizedFeatures
from .anomaly_detection import AnomalyResult

@dataclass
class MorphologyResult:
    """Resultado de análisis morfológico."""
    symmetry_score: float
    edge_regularity: float
    planarity: float
    artificial_indicators: List[str]
    geomorphology_hint: str = "unknown"  # NUEVO: contexto geológico
    paleo_signature: Optional[Dict[str, Any]] = None  # NUEVO: firma de paleocauce u otras estructuras lineales

def _infer_geomorphology(environment_type: str,
                        symmetry: float,
                        planarity: float,
                        edge_regularity: float,
                        raw_measurements: Dict[str, Any] = None) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    MEJORA 2: Inferir contexto geomorfológico (NO arqueología).
    
    Esto permite:
    - Entrenar anti-patrones
    - Filtrar automáticamente regiones glaciares
    - Justificar descartes masivos
    - NUEVO: Detectar paleocauces y otras firmas lineales
    
    Returns:
        Tuple[str, Optional[Dict]]: (geomorphology_hint, paleo_signature)
    """
    
    paleo_signature = None
    
    # DETECTOR DE PALEOCAUCES (desiertos con anomalía lineal)
    if environment_type in ['desert', 'semi_arid'] and raw_measurements:
        # Buscar firma de paleocauce: térmica alta + NDVI lineal
        thermal_value = 0.0
        ndvi_value = 0.0
        
        # Extraer mediciones térmicas y NDVI
        for key, measurement in raw_measurements.items():
            if isinstance(measurement, dict):
                if 'thermal' in key.lower():
                    thermal_value = measurement.get('value', 0.0)
                elif 'ndvi' in key.lower():
                    ndvi_value = measurement.get('value', 0.0)
        
        # Firma de paleocauce: térmica alta (>15) + NDVI bajo pero presente (0.05-0.15)
        if thermal_value > 15 and 0.05 < ndvi_value < 0.15:
            # Calcular probabilidad de paleocauce
            thermal_score = min(1.0, thermal_value / 25.0)  # Normalizar a 0-1
            ndvi_score = ndvi_value / 0.15  # Normalizar a 0-1
            
            # Indicadores de linealidad (simulado - en producción usar geometría real)
            linearity_score = 0.6 if symmetry < 0.5 else 0.3  # Baja simetría = más lineal
            
            paleo_probability = (thermal_score * 0.4 + ndvi_score * 0.3 + linearity_score * 0.3)
            
            if paleo_probability > 0.5:
                paleo_signature = {
                    'type': 'paleo_channel',
                    'probability': float(paleo_probability),
                    'indicators': [
                        f'thermal_inertia (value={thermal_value:.2f})',
                        f'NDVI_linear_anomaly (value={ndvi_value:.3f})',
                        f'low_symmetry (score={symmetry:.2f})'
                    ],
                    'confidence': 'medium' if paleo_probability > 0.7 else 'low'
                }
                print(f"[MORFOLOGÍA] 🏜️ PALEOCAUCE DETECTADO: prob={paleo_probability:.2f}", flush=True)
                return "paleo_channel_signature", paleo_signature
    
    # Ambientes glaciares
    if environment_type in ['polar_ice', 'glacier', 'permafrost']:
        if planarity > 0.7:
            return "glacial_outwash_or_ablation_plain", paleo_signature
        elif symmetry > 0.6:
            return "glacial_cirque_or_moraine", paleo_signature
        else:
            return "glacial_terrain_general", paleo_signature
    
    # Ambientes desérticos
    elif environment_type in ['desert', 'arid', 'semi_arid']:
        # 🔴 AJUSTE QUIRÚRGICO 1: Detectar patrones superficiales (Nazca-like)
        # Evitar clasificar como volcán cuando hay trazos superficiales
        
        ndvi_near_zero = False
        dem_rugosity_low = False
        
        if raw_measurements:
            for key, measurement in raw_measurements.items():
                if isinstance(measurement, dict):
                    if 'ndvi' in key.lower():
                        value = measurement.get('value', 0.0)
                        # NDVI muy bajo (< 0.05) = estado basal del desierto
                        if abs(value) < 0.05:
                            ndvi_near_zero = True
                    elif 'dem' in key.lower() or 'topography' in key.lower():
                        value = measurement.get('value', 0.0)
                        # Baja rugosidad = superficie plana
                        if abs(value) < 1.0:
                            dem_rugosity_low = True
        
        # REGLA: IF NDVI ≈ 0 AND DEM.rugosity low AND symmetry high AND planarity high
        # THEN surface_pattern_anthropic_possible
        if ndvi_near_zero and dem_rugosity_low and symmetry > 0.6 and planarity > 0.6:
            print(f"[MORFOLOGÍA] 🏜️ PATRÓN SUPERFICIAL: posible trazo antropogénico (no volcán)", flush=True)
            print(f"  - NDVI ≈ 0 (estado basal desierto)", flush=True)
            print(f"  - DEM rugosity: low (superficie plana)", flush=True)
            print(f"  - Symmetry: {symmetry:.2f}", flush=True)
            print(f"  - Planarity: {planarity:.2f}", flush=True)
            return "surface_pattern_anthropic_possible", paleo_signature
        
        # Clasificación normal si no hay override
        if symmetry < 0.3 and edge_regularity < 0.3:
            return "aeolian_dune_field", paleo_signature
        elif planarity > 0.7:
            return "desert_pavement_or_playa", paleo_signature
        else:
            return "desert_terrain_general", paleo_signature
    
    # Ambientes costeros/marinos
    elif environment_type in ['coastal', 'shallow_sea']:
        if planarity > 0.6:
            return "tidal_flat_or_beach", paleo_signature
        else:
            return "coastal_terrain_general", paleo_signature
    
    # Ambientes montañosos
    elif environment_type in ['mountain', 'highland']:
        # 🔴 AFINADO 1: Override para arquitectura lítica en montaña
        # Evitar falso positivo "volcán" cuando hay evidencia de terrazas/arquitectura
        
        # Buscar rugosidad del DEM (indicador de terrazas)
        dem_rugosity_high = False
        ndvi_missing = False
        
        if raw_measurements:
            # Verificar si hay DEM con alta variabilidad (terrazas)
            for key, measurement in raw_measurements.items():
                if isinstance(measurement, dict):
                    if 'dem' in key.lower() or 'topography' in key.lower():
                        value = measurement.get('value', 0.0)
                        if abs(value) > 1.5:  # Alta variabilidad topográfica
                            dem_rugosity_high = True
                    elif 'ndvi' in key.lower():
                        data_mode = measurement.get('data_mode', 'OK')
                        if data_mode == 'NO_DATA':
                            ndvi_missing = True
        
        # REGLA DE OVERRIDE CONTEXTUAL:
        # IF mountain AND DEM.rugosity high AND symmetry high AND NDVI missing
        # THEN candidate = anthropogenic_terracing_possible
        if dem_rugosity_high and symmetry > 0.6 and ndvi_missing:
            print(f"[MORFOLOGÍA] 🏛️ OVERRIDE: Arquitectura lítica posible (no volcán)", flush=True)
            print(f"  - DEM rugosity: high", flush=True)
            print(f"  - Symmetry: {symmetry:.2f}", flush=True)
            print(f"  - NDVI: missing", flush=True)
            return "anthropogenic_terracing_possible", paleo_signature
        
        # Clasificación normal si no hay override
        if symmetry > 0.7:
            return "volcanic_cone_or_crater", paleo_signature
        elif planarity < 0.3:
            return "steep_mountain_terrain", paleo_signature
        else:
            return "mountain_terrain_general", paleo_signature
    
    # Ambientes de bosque/selva
    elif environment_type in ['forest', 'jungle']:
        return "forested_terrain", paleo_signature
    
    # Default
    else:
        return "terrain_general", paleo_signature

def analyze_morphology(normalized: NormalizedFeatures,
                      anomaly: AnomalyResult) -> MorphologyResult:
    """
    FASE C: Análisis morfológico explícito.
    
    Args:
        normalized: Features normalizadas
        anomaly: Resultado de detección de anomalías
    
    Returns:
        MorphologyResult con métricas morfológicas
    """
    print("[FASE C] Analizando morfología explícita...", flush=True)
    
    features = normalized.features
    
    # Calcular métricas morfológicas (simuladas - en producción usar geometría real)
    
    # Simetría: basada en uniformidad de features
    feature_values = [v for v in features.values() if isinstance(v, (int, float))]
    if len(feature_values) > 1:
        symmetry_score = 1.0 - (np.std(feature_values) / (np.mean(np.abs(feature_values)) + 0.1))
        symmetry_score = float(np.clip(symmetry_score, 0, 1))
    else:
        symmetry_score = 0.5
    
    # Regularidad de bordes: basada en convergencia
    edge_regularity = features.get('convergence_ratio', 0.0)
    
    # Planaridad: basada en estabilidad de mediciones
    planarity = 1.0 - abs(features.get('mean_deviation', 0.0)) / 3.0
    planarity = float(np.clip(planarity, 0, 1))
    
    # Indicadores artificiales
    artificial_indicators = []
    if symmetry_score > 0.7:
        artificial_indicators.append("alta_simetria")
    if edge_regularity > 0.6:
        artificial_indicators.append("bordes_regulares")
    if planarity > 0.7:
        artificial_indicators.append("superficie_plana")
    
    # MEJORA 2: Etiqueta geomorfológica explícita (contexto geológico, NO arqueología)
    geomorphology_hint, paleo_signature = _infer_geomorphology(
        normalized.raw_measurements.get('environment_type', 'unknown'),
        symmetry_score,
        planarity,
        edge_regularity,
        normalized.raw_measurements
    )
    
    print(f"[FASE C] Simetría: {symmetry_score:.3f}, Regularidad: {edge_regularity:.3f}, Planaridad: {planarity:.3f}", flush=True)
    print(f"[FASE C] Indicadores artificiales: {artificial_indicators}", flush=True)
    print(f"[FASE C] Geomorfología inferida: {geomorphology_hint}", flush=True)
    
    if paleo_signature:
        print(f"[FASE C] 🏜️ Firma paleocauce detectada:", flush=True)
        print(f"  - Tipo: {paleo_signature['type']}", flush=True)
        print(f"  - Probabilidad: {paleo_signature['probability']:.2f}", flush=True)
        print(f"  - Indicadores: {', '.join(paleo_signature['indicators'])}", flush=True)
        print(f"  - Confianza: {paleo_signature['confidence']}", flush=True)
    
    return MorphologyResult(
        symmetry_score=symmetry_score,
        edge_regularity=edge_regularity,
        planarity=planarity,
        artificial_indicators=artificial_indicators,
        geomorphology_hint=geomorphology_hint,
        paleo_signature=paleo_signature  # NUEVO
    )