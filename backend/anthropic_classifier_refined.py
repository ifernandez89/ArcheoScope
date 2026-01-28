#!/usr/bin/env python3
"""
Clasificador Antropogénico Refinado - ArcheoScope
==================================================

AFINADO CRÍTICO: Separar origen vs actividad antropogénica.

El problema de la Esfinge:
- Origen antropogénico: ~95% (es una estructura humana)
- Actividad antropogénica: ~5% (no hay actividad humana reciente)
- Anomaly Score: 0.0% (no hay anomalía detectable)

Esto NO es contradictorio - es arqueología histórica.

FILOSOFÍA:
- anthropic_origin_probability: ¿Fue creado por humanos?
- anthropic_activity_probability: ¿Hay actividad humana reciente/actual?
- anomaly_score: ¿Hay desviación estadística del entorno?

Una estructura antigua puede tener:
- Alto origen, baja actividad, baja anomalía → ARQUEOLOGÍA HISTÓRICA
- Alto origen, alta actividad, alta anomalía → SITIO ACTIVO
- Bajo origen, baja actividad, alta anomalía → GEOMORFOLOGÍA INUSUAL
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from scipy import stats

@dataclass
class RefinedAnthropicInference:
    """
    Inferencia antropogénica refinada con separación origen/actividad.
    """
    # SEPARACIÓN CRÍTICA
    anthropic_origin_probability: float  # ¿Fue creado por humanos? (0-1)
    anthropic_activity_probability: float  # ¿Hay actividad humana actual? (0-1)
    
    # Intervalos de confianza SEPARADOS
    origin_confidence_interval: Tuple[float, float]
    activity_confidence_interval: Tuple[float, float]
    
    # Confianza general
    confidence: str  # "high", "medium", "low"
    
    # Razonamiento
    origin_reasoning: List[str]
    activity_reasoning: List[str]
    
    # Clasificación de sitio
    site_classification: str  # "historical_structure", "active_site", "natural_formation", "uncertain"
    
    # Métricas de cobertura
    coverage_raw: float = 0.0
    coverage_effective: float = 0.0
    instruments_measured: int = 0
    instruments_available: int = 0
    
    # Modelo usado
    model_used: str = "refined_dual_axis_v1"


class RefinedAnthropicClassifier:
    """
    Clasificador antropogénico refinado que separa origen de actividad.
    
    Resuelve el problema de la Esfinge y estructuras históricas.
    """
    
    def __init__(self):
        """Inicializar clasificador."""
        print("[REFINED CLASSIFIER] Inicializado con separación origen/actividad", flush=True)
    
    def classify(self,
                 anomaly_score: float,
                 morphology: Dict[str, Any],
                 normalized_features: Dict[str, float],
                 raw_measurements: Dict[str, Any],
                 environment_type: str) -> RefinedAnthropicInference:
        """
        Clasificar sitio con separación origen/actividad.
        
        Args:
            anomaly_score: Score de anomalía (0-1)
            morphology: Resultado de análisis morfológico
            normalized_features: Features normalizadas
            raw_measurements: Mediciones crudas
            environment_type: Tipo de ambiente
        
        Returns:
            RefinedAnthropicInference con probabilidades separadas
        """
        print("[REFINED CLASSIFIER] Clasificando con dual-axis...", flush=True)
        
        # =====================================================================
        # EJE 1: ORIGEN ANTROPOGÉNICO (¿Fue creado por humanos?)
        # =====================================================================
        
        origin_reasoning = []
        
        # Factores de ORIGEN (independientes de actividad actual)
        origin_factors = []
        
        # 1. Morfología (crítico para origen)
        symmetry_score = morphology.get('symmetry_score', 0.0)
        edge_regularity = morphology.get('edge_regularity', 0.0)
        planarity = morphology.get('planarity', 0.0)
        
        # Morfología es MUY indicativa de origen antropogénico
        # Si tienes alta simetría + regularidad + planaridad → muy probable origen humano
        morphology_score = (symmetry_score * 0.4 + 
                           edge_regularity * 0.4 + 
                           planarity * 0.2)
        
        # BOOST si múltiples indicadores morfológicos son altos
        if symmetry_score > 0.6 and edge_regularity > 0.6:
            morphology_score = min(1.0, morphology_score * 1.3)  # +30% boost
            origin_reasoning.append(f"morfología altamente regular (simetría {symmetry_score:.2f}, bordes {edge_regularity:.2f})")
        elif symmetry_score > 0.6:
            origin_reasoning.append(f"simetría geométrica ({symmetry_score:.2f})")
        
        if edge_regularity > 0.6:
            origin_reasoning.append(f"regularidad de bordes ({edge_regularity:.2f})")
        if planarity > 0.6:
            origin_reasoning.append(f"planaridad ({planarity:.2f})")
        
        origin_factors.append(morphology_score)
        
        # 2. Indicadores artificiales (MUY importante)
        artificial_indicators = morphology.get('artificial_indicators', [])
        if len(artificial_indicators) > 0:
            # Cada indicador artificial es evidencia fuerte
            indicator_score = min(1.0, 0.5 + len(artificial_indicators) * 0.15)
            origin_factors.append(indicator_score)
            origin_reasoning.append(f"indicadores artificiales: {', '.join(artificial_indicators)}")
        
        # 3. Contexto geomorfológico (NEGATIVO para origen)
        geomorphology_hint = morphology.get('geomorphology_hint', 'unknown')
        natural_formations = [
            'glacial_outwash', 'moraine', 'dune', 'wadi', 
            'lava_flow', 'erosion_pattern', 'natural_terrace'
        ]
        
        if any(nat in geomorphology_hint for nat in natural_formations):
            # Reducir probabilidad de origen antropogénico
            origin_factors.append(-0.3)
            origin_reasoning.append(f"geomorfología natural: {geomorphology_hint}")
        
        # Calcular probabilidad de ORIGEN
        if len(origin_factors) > 0:
            origin_probability = np.mean(origin_factors)
            origin_probability = float(np.clip(origin_probability, 0, 1))
        else:
            origin_probability = 0.3  # Prior neutral
        
        # =====================================================================
        # EJE 2: ACTIVIDAD ANTROPOGÉNICA (¿Hay actividad humana actual?)
        # =====================================================================
        
        activity_reasoning = []
        
        # Factores de ACTIVIDAD (dependen de señales actuales)
        activity_factors = []
        
        # 1. Anomalía (crítico para actividad)
        # Alta anomalía → posible actividad reciente
        activity_factors.append(anomaly_score * 0.6)
        
        if anomaly_score > 0.3:
            activity_reasoning.append(f"anomalía detectable ({anomaly_score:.2f})")
        elif anomaly_score < 0.1:
            activity_reasoning.append(f"sin anomalía significativa ({anomaly_score:.2f})")
        
        # 2. Señales térmicas (actividad reciente)
        thermal_signals = []
        for key, value in normalized_features.items():
            if 'thermal' in key.lower() or 'lst' in key.lower():
                if abs(value) > 1.5:  # Desviación térmica significativa
                    thermal_signals.append(key)
        
        if len(thermal_signals) > 0:
            activity_factors.append(0.4)
            activity_reasoning.append(f"señales térmicas anómalas: {len(thermal_signals)}")
        else:
            activity_factors.append(-0.2)
            activity_reasoning.append("sin señales térmicas anómalas")
        
        # 3. Vegetación (NDVI) - actividad agrícola/manejo
        ndvi_signals = []
        for key, value in normalized_features.items():
            if 'ndvi' in key.lower():
                if abs(value) > 1.5:
                    ndvi_signals.append(key)
        
        if len(ndvi_signals) > 0 and environment_type not in ['desert', 'polar_ice']:
            activity_factors.append(0.3)
            activity_reasoning.append("patrón de vegetación anómalo")
        
        # 4. SAR (estructuras activas, movimiento)
        sar_signals = []
        for key, value in normalized_features.items():
            if 'sar' in key.lower():
                if abs(value) > 2.0:  # Alta desviación SAR
                    sar_signals.append(key)
        
        if len(sar_signals) > 0:
            activity_factors.append(0.3)
            activity_reasoning.append("señal SAR anómala (posible estructura activa)")
        
        # Calcular probabilidad de ACTIVIDAD
        if len(activity_factors) > 0:
            activity_probability = np.mean(activity_factors)
            activity_probability = float(np.clip(activity_probability, 0, 1))
        else:
            activity_probability = 0.1  # Prior bajo (mayoría de sitios son históricos)
        
        # =====================================================================
        # AJUSTES POR COBERTURA INSTRUMENTAL
        # =====================================================================
        
        # Calcular cobertura (mismo método que antes)
        instruments_measured = len([k for k in normalized_features.keys() 
                                   if 'zscore' in k and k not in ['mean_deviation', 'max_deviation', 'convergence_ratio']])
        instruments_available = raw_measurements.get('instruments_available', 5)
        coverage_raw = instruments_measured / instruments_available if instruments_available > 0 else 0.0
        
        # Cobertura efectiva (simplificada)
        coverage_effective = coverage_raw * 0.8  # Placeholder
        
        # Penalización por baja cobertura (afecta MÁS a actividad que a origen)
        if coverage_effective < 0.3:
            # Actividad es más sensible a cobertura
            activity_probability *= 0.7
            activity_reasoning.append(f"⚠️ baja cobertura ({coverage_effective:.1%}) - actividad incierta")
            
            # Origen menos afectado (morfología es más robusta)
            origin_probability *= 0.9
            origin_reasoning.append(f"⚠️ baja cobertura ({coverage_effective:.1%})")
        
        # =====================================================================
        # CLASIFICACIÓN DE SITIO
        # =====================================================================
        
        # Umbrales ajustados para mejor clasificación
        if origin_probability > 0.55 and activity_probability < 0.3:
            site_classification = "historical_structure"
        elif origin_probability > 0.6 and activity_probability > 0.3:
            # Sitio con origen antropogénico y alguna actividad
            site_classification = "active_site"
        elif origin_probability < 0.4 and anomaly_score > 0.5:
            site_classification = "natural_anomaly"
        elif origin_probability < 0.4:
            site_classification = "natural_formation"
        else:
            site_classification = "uncertain"
        
        # =====================================================================
        # INTERVALOS DE CONFIANZA
        # =====================================================================
        
        # Intervalo más amplio si hay baja cobertura
        ci_width = 0.15 if coverage_effective < 0.5 else 0.10
        
        origin_ci = (
            max(0.0, origin_probability - ci_width),
            min(1.0, origin_probability + ci_width)
        )
        
        activity_ci = (
            max(0.0, activity_probability - ci_width),
            min(1.0, activity_probability + ci_width)
        )
        
        # =====================================================================
        # CONFIANZA GENERAL
        # =====================================================================
        
        if coverage_effective > 0.7 and len(origin_reasoning) >= 2:
            confidence = "high"
        elif coverage_effective > 0.4:
            confidence = "medium"
        else:
            confidence = "low"
        
        # =====================================================================
        # LOGGING
        # =====================================================================
        
        print(f"[REFINED CLASSIFIER] 📊 Resultados:", flush=True)
        print(f"  🏛️  Origen antropogénico: {origin_probability:.1%} [{origin_ci[0]:.1%}, {origin_ci[1]:.1%}]", flush=True)
        print(f"  🔥 Actividad antropogénica: {activity_probability:.1%} [{activity_ci[0]:.1%}, {activity_ci[1]:.1%}]", flush=True)
        print(f"  📍 Clasificación: {site_classification}", flush=True)
        print(f"  🎯 Confianza: {confidence}", flush=True)
        print(f"  📡 Cobertura: {coverage_raw:.1%} raw, {coverage_effective:.1%} effective", flush=True)
        
        if len(origin_reasoning) == 0:
            origin_reasoning.append("sin indicadores claros de origen antropogénico")
        if len(activity_reasoning) == 0:
            activity_reasoning.append("sin señales de actividad reciente")
        
        return RefinedAnthropicInference(
            anthropic_origin_probability=origin_probability,
            anthropic_activity_probability=activity_probability,
            origin_confidence_interval=origin_ci,
            activity_confidence_interval=activity_ci,
            confidence=confidence,
            origin_reasoning=origin_reasoning,
            activity_reasoning=activity_reasoning,
            site_classification=site_classification,
            coverage_raw=coverage_raw,
            coverage_effective=coverage_effective,
            instruments_measured=instruments_measured,
            instruments_available=instruments_available,
            model_used="refined_dual_axis_v1"
        )
