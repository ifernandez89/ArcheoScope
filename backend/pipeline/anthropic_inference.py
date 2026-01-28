#!/usr/bin/env python3
"""
Módulo de Inferencia Antropogénica - Pipeline Científico
=======================================================

FASE D: Clasificador antropogénico (CON FRENO DE MANO).

Este modelo NO decide, solo sugiere.

Inputs:
- anomaly_score
- morfología
- contexto (agua, altitud, rutas)

Modelo explicable: Random Forest / Gradient Boosting simulado

AJUSTES IMPLEMENTADOS:
- Penalización explícita por cobertura instrumental (AJUSTE 2)
- Umbral dinámico por región arqueológica (AJUSTE 3)
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from .normalization import NormalizedFeatures
from .anomaly_detection import AnomalyResult
from .morphology import MorphologyResult

@dataclass
class AnthropicInference:
    """Inferencia antropogénica (con freno de mano)."""
    anthropic_probability: float
    confidence: str
    confidence_interval: Tuple[float, float]
    reasoning: List[str]
    model_used: str
    # Métricas de cobertura instrumental
    coverage_raw: float = 0.0  # Instrumentos presentes / disponibles
    coverage_effective: float = 0.0  # Cobertura ponderada
    instruments_measured: int = 0
    instruments_available: int = 0
    # 🟠 AFINADO 2: Separar probabilidad de incertidumbre
    epistemic_uncertainty: float = 0.0  # Incertidumbre por falta de datos (0-1)
    uncertainty_sources: List[str] = None  # Fuentes de incertidumbre
    # 🔬 EXPLANATORY STRANGENESS: Capturar "algo extraño" sin sensacionalismo
    explanatory_strangeness: str = "none"  # none, low, medium, high, very_high
    strangeness_score: float = 0.0  # Score numérico (0-1)
    strangeness_reasons: List[str] = None  # Razones específicas
    # 🎯 SEPARACIÓN CIENTÍFICA EXPLÍCITA (estado del arte)
    anthropic_origin_probability: float = 0.0  # ¿Fue creado por humanos? (0-1)
    anthropic_activity_probability: float = 0.0  # ¿Hay actividad humana actual? (0-1)
    instrumental_anomaly_probability: float = 0.0  # Probabilidad de anomalía instrumental (0-1)
    model_inference_confidence: str = "unknown"  # Confianza del modelo (low, medium, high)

def _calculate_explanatory_strangeness(anomaly_score: float,
                                     anthropic_probability: float,
                                     symmetry: float,
                                     planarity: float,
                                     edge_regularity: float,
                                     epistemic_uncertainty: float,
                                     geomorphology_hint: str,
                                     environment_type: str) -> Tuple[str, float, List[str]]:
    """
    🔬 EXPLANATORY STRANGENESS SCORE (ESS)
    
    Captura "algo extraño" sin sensacionalismo.
    Se activa cuando hay patrones que no encajan en explicaciones naturales simples.
    
    Args:
        anomaly_score: Score de anomalía (0-1)
        anthropic_probability: Probabilidad antropogénica (0-1)
        symmetry: Score de simetría (0-1)
        planarity: Score de planaridad (0-1)
        edge_regularity: Score de regularidad de bordes (0-1)
        epistemic_uncertainty: Incertidumbre epistemológica (0-1)
        geomorphology_hint: Pista geomorfológica
        environment_type: Tipo de ambiente
    
    Returns:
        Tuple[str, float, List[str]]: (strangeness_level, score, reasons)
    """
    
    strangeness_reasons = []
    strangeness_score = 0.0
    
    # 1. ANOMALÍA SIN EXPLICACIÓN GEOMORFOLÓGICA CLARA
    if anomaly_score > 0.6 and geomorphology_hint in ['terrain_general', 'unknown']:
        strangeness_score += 0.3
        strangeness_reasons.append(f"anomalía alta sin explicación geomorfológica (score={anomaly_score:.2f})")
    
    # 2. SIMETRÍA EXTREMA EN AMBIENTES CAÓTICOS
    if symmetry > 0.8 and environment_type in ['mountain', 'desert', 'forest']:
        strangeness_score += 0.25
        strangeness_reasons.append(f"simetría extrema en ambiente caótico ({environment_type})")
    
    # 3. PLANARIDAD PERFECTA EN TERRENO RUGOSO
    if planarity > 0.9 and environment_type in ['mountain', 'highland']:
        strangeness_score += 0.2
        strangeness_reasons.append("planaridad perfecta en terreno montañoso")
    
    # 4. REGULARIDAD GEOMÉTRICA INEXPLICABLE
    if edge_regularity > 0.8 and symmetry > 0.7:
        strangeness_score += 0.2
        strangeness_reasons.append("regularidad geométrica combinada")
    
    # 5. PATRÓN ANTROPOGÉNICO POSIBLE (override geomorfológico)
    if geomorphology_hint in ['surface_pattern_anthropic_possible', 'anthropogenic_terracing_possible']:
        strangeness_score += 0.4
        strangeness_reasons.append(f"patrón geomorfológico antropogénico: {geomorphology_hint}")
    
    # 6. PALEOCAUCE CON ANOMALÍA ADICIONAL
    if geomorphology_hint == 'paleo_channel_signature' and anomaly_score > 0.4:
        strangeness_score += 0.15
        strangeness_reasons.append("paleocauce con anomalía adicional inexplicada")
    
    # 7. CONVERGENCIA DE MÚLTIPLES INDICADORES
    indicator_count = sum([
        1 if anomaly_score > 0.5 else 0,
        1 if symmetry > 0.7 else 0,
        1 if planarity > 0.7 else 0,
        1 if edge_regularity > 0.6 else 0,
        1 if anthropic_probability > 0.6 else 0
    ])
    
    if indicator_count >= 4:
        strangeness_score += 0.3
        strangeness_reasons.append(f"convergencia de {indicator_count} indicadores independientes")
    elif indicator_count >= 3:
        strangeness_score += 0.15
        strangeness_reasons.append(f"convergencia de {indicator_count} indicadores")
    
    # 8. PENALIZACIÓN POR ALTA INCERTIDUMBRE EPISTEMOLÓGICA
    if epistemic_uncertainty > 0.6:
        strangeness_score *= 0.7  # Reducir por falta de datos
        strangeness_reasons.append("ajustado por alta incertidumbre epistemológica")
    
    # Normalizar score
    strangeness_score = float(np.clip(strangeness_score, 0, 1))
    
    # Determinar nivel categórico
    if strangeness_score >= 0.8:
        strangeness_level = "very_high"
    elif strangeness_score >= 0.6:
        strangeness_level = "high"
    elif strangeness_score >= 0.4:
        strangeness_level = "medium"
    elif strangeness_score >= 0.2:
        strangeness_level = "low"
    else:
        strangeness_level = "none"
    
    print(f"[ESS] 🔬 Explanatory Strangeness: {strangeness_level} (score={strangeness_score:.2f})", flush=True)
    if strangeness_reasons:
        print(f"[ESS] Razones: {'; '.join(strangeness_reasons)}", flush=True)
    
    return strangeness_level, strangeness_score, strangeness_reasons

def infer_anthropic_probability(normalized: NormalizedFeatures,
                               anomaly: AnomalyResult,
                               morphology: MorphologyResult) -> AnthropicInference:
    """
    FASE D: Clasificador antropogénico (CON FRENO DE MANO).
    
    Args:
        normalized: Features normalizadas
        anomaly: Resultado de detección de anomalías
        morphology: Resultado de análisis morfológico
    
    Returns:
        AnthropicInference con probabilidad y métricas
    """
    print("[FASE D] Inferencia antropogénica (con freno de mano)...", flush=True)
    
    # Calcular probabilidad antropogénica LEGACY
    # Pesos: anomalía (40%), morfología (40%), contexto (20%)
    
    anomaly_weight = anomaly.anomaly_score * 0.4
    
    morphology_weight = (
        morphology.symmetry_score * 0.15 +
        morphology.edge_regularity * 0.15 +
        morphology.planarity * 0.10
    )
    
    # Contexto (simulado - en producción usar datos reales)
    context_weight = 0.1  # Placeholder
    
    anthropic_probability = anomaly_weight + morphology_weight + context_weight
    anthropic_probability = float(np.clip(anthropic_probability, 0, 1))
    
    # Razonamiento (inicializar antes de usar)
    reasoning = []
    
    # AJUSTE 2: PENALIZACIÓN EXPLÍCITA POR COBERTURA INSTRUMENTAL
    # Sistema de ponderación por peso de instrumento (context-aware)
    
    # Definir pesos por tipo de instrumento y ambiente
    instrument_weights = {
        # Ambientes terrestres
        'terrestrial': {
            'landsat_thermal': 0.15,
            'modis_lst': 0.10,
            'sentinel_2_ndvi': 0.15,
            'sentinel_1_sar': 0.20,
            'opentopography': 0.15,
            'icesat2': 0.10,
            'lidar': 0.10,
            'srtm_dem': 0.05
        },
        # 🟠 AJUSTE QUIRÚRGICO 2: Ambientes desérticos (NDVI no discriminativo)
        'desert': {
            'landsat_thermal': 0.25,  # Más peso a térmicos
            'modis_lst': 0.20,
            'sentinel_1_sar': 0.25,   # SAR crítico en desierto
            'opentopography': 0.20,   # DEM crítico
            'sentinel_2_ndvi': 0.05,  # NDVI casi no discrimina (estado basal)
            'icesat2': 0.03,
            'srtm_dem': 0.02
        },
        # Ambientes marinos/acuáticos
        'marine': {
            'multibeam_sonar': 0.30,
            'side_scan_sonar': 0.25,
            'magnetometer': 0.20,
            'sub_bottom_profiler': 0.15,
            'landsat_thermal': 0.02,
            'modis_lst': 0.02,
            'sentinel_1_sar': 0.03,
            'sentinel_2_ndvi': 0.01,
            'opentopography': 0.01,
            'icesat2': 0.01
        },
        # Ambientes glaciares
        'glacial': {
            'icesat2': 0.25,
            'sentinel_1_sar': 0.25,
            'palsar': 0.20,
            'modis_thermal': 0.15,
            'landsat_thermal': 0.10,
            'opentopography': 0.03,
            'sentinel_2_ndvi': 0.02
        }
    }
    
    # Determinar categoría de ambiente
    environment_type = normalized.raw_measurements.get('environment_type', 'unknown')
    if environment_type in ['deep_ocean', 'shallow_sea', 'coastal', 'lake', 'river']:
        env_category = 'marine'
    elif environment_type in ['polar_ice', 'glacier', 'permafrost']:
        env_category = 'glacial'
    elif environment_type in ['desert', 'arid', 'semi_arid']:
        env_category = 'desert'  # 🟠 AJUSTE 2: Categoría específica para desierto
    else:
        env_category = 'terrestrial'
    
    weights = instrument_weights.get(env_category, instrument_weights['terrestrial'])
    
    # Calcular cobertura ponderada
    total_weight_available = sum(weights.values())
    effective_coverage = 0.0
    raw_instrument_count = 0
    
    # Contar instrumentos que REALMENTE midieron (tienen zscore)
    # EXCLUIR features derivadas (mean_deviation, max_deviation, convergence_ratio)
    derived_features = ['mean_deviation', 'max_deviation', 'convergence_ratio']
    
    for key in normalized.features.keys():
        if 'zscore' in key and key not in derived_features:
            raw_instrument_count += 1  # CORREGIDO: contar cada instrumento
            # Extraer nombre del instrumento
            instrument_name = key.replace('_zscore', '')
            # Buscar peso del instrumento
            for inst_key, weight in weights.items():
                if inst_key.lower().replace('_', '') in instrument_name.lower().replace('_', ''):
                    effective_coverage += weight
                    break
    
    coverage_ratio = effective_coverage / total_weight_available if total_weight_available > 0 else 0
    instrument_count = len([k for k in normalized.features.keys() if 'zscore' in k])
    
    # 🟠 AJUSTE QUIRÚRGICO 2: Detectar NDVI no discriminativo en desierto
    ndvi_non_discriminative = False
    if env_category == 'desert':
        # Verificar si NDVI está presente pero con valor muy bajo (estado basal)
        for key in normalized.features.keys():
            if 'ndvi' in key.lower() and 'zscore' in key:
                # NDVI presente pero no discrimina (peso bajo en desierto)
                ndvi_non_discriminative = True
                print(f"[FASE D] 🏜️ NDVI detectado en desierto: marcado como non_discriminative", flush=True)
                print(f"[FASE D]    Razón: NDVI bajo es estado basal del desierto", flush=True)
                print(f"[FASE D]    Peso ajustado: 5% (vs 15% en terrestre)", flush=True)
                break
    
    # 🟠 AFINADO 2: SEPARAR PROBABILIDAD DE INCERTIDUMBRE
    # En lugar de penalizar probabilidad, calcular incertidumbre epistemológica
    
    uncertainty_sources = []
    epistemic_uncertainty = 0.0
    
    # Calcular incertidumbre por falta de instrumentos críticos
    if coverage_ratio < 0.3:  # Menos del 30% de cobertura efectiva
        epistemic_uncertainty = 0.7  # Alta incertidumbre
        uncertainty_sources.append(f"cobertura crítica ({coverage_ratio*100:.0f}% effective)")
        reasoning.append(f"⚠️ Alta incertidumbre: cobertura {coverage_ratio*100:.0f}% (instrumentos críticos faltantes)")
        print(f"[FASE D] ⚠️ ALTA INCERTIDUMBRE EPISTEMOLÓGICA: {epistemic_uncertainty:.1%}", flush=True)
        print(f"[FASE D]    Coverage effective: {coverage_ratio*100:.0f}% (weighted by instrument importance)", flush=True)
        print(f"[FASE D]    Coverage raw: {raw_instrument_count} instruments present", flush=True)
        print(f"[FASE D]    Environment category: {env_category}", flush=True)
        print(f"[FASE D]    Interpretación: NO sabemos (no = es natural)", flush=True)
    elif coverage_ratio < 0.5:  # Entre 30-50%
        epistemic_uncertainty = 0.5  # Incertidumbre moderada
        uncertainty_sources.append(f"cobertura moderada ({coverage_ratio*100:.0f}% effective)")
        reasoning.append(f"⚠️ Incertidumbre moderada: cobertura {coverage_ratio*100:.0f}%")
        print(f"[FASE D] ⚠️ INCERTIDUMBRE MODERADA: {epistemic_uncertainty:.1%}", flush=True)
        print(f"[FASE D]    Coverage effective: {coverage_ratio*100:.0f}% (weighted by instrument importance)", flush=True)
        print(f"[FASE D]    Coverage raw: {raw_instrument_count} instruments present", flush=True)
        print(f"[FASE D]    Environment category: {env_category}", flush=True)
    elif coverage_ratio < 0.75:  # Entre 50-75%
        epistemic_uncertainty = 0.3  # Incertidumbre baja
        uncertainty_sources.append(f"cobertura aceptable ({coverage_ratio*100:.0f}% effective)")
        reasoning.append(f"⚠️ Incertidumbre baja: cobertura {coverage_ratio*100:.0f}%")
        print(f"[FASE D] ⚠️ INCERTIDUMBRE BAJA: {epistemic_uncertainty:.1%}", flush=True)
        print(f"[FASE D]    Coverage effective: {coverage_ratio*100:.0f}% (weighted by instrument importance)", flush=True)
        print(f"[FASE D]    Coverage raw: {raw_instrument_count} instruments present", flush=True)
    else:
        epistemic_uncertainty = 0.1  # Incertidumbre mínima
        print(f"[FASE D] ✅ Cobertura instrumental adecuada: {coverage_ratio*100:.0f}% effective", flush=True)
        print(f"[FASE D]    Incertidumbre epistemológica: {epistemic_uncertainty:.1%}", flush=True)
        print(f"[FASE D]    Coverage raw: {raw_instrument_count} instruments present", flush=True)
        print(f"[FASE D]    Environment category: {env_category}", flush=True)
    
    # MEJORA 3: Regla de freno contextual
    # Reduce probabilidad en ambientes con baja cobertura instrumental
    environment_type = normalized.raw_measurements.get('environment_type', 'unknown')
    
    if environment_type in ['polar_ice', 'glacier', 'permafrost'] and instrument_count < 2:
        anthropic_probability *= 0.7
        reasoning.append(f"ajuste contextual: ambiente glaciar con baja cobertura ({instrument_count} instrumentos)")
        print(f"[FASE D] Aplicado freno contextual: glaciar con {instrument_count} instrumentos → -30%", flush=True)
    
    elif environment_type in ['deep_ocean', 'shallow_sea'] and instrument_count < 2:
        anthropic_probability *= 0.8
        reasoning.append(f"ajuste contextual: ambiente marino con baja cobertura ({instrument_count} instrumentos)")
        print(f"[FASE D] Aplicado freno contextual: marino con {instrument_count} instrumentos → -20%", flush=True)
    
    anthropic_probability = float(np.clip(anthropic_probability, 0, 1))
    
    # Intervalo de confianza (±10%)
    confidence_interval = (
        max(0.0, anthropic_probability - 0.1),
        min(1.0, anthropic_probability + 0.1)
    )
    
    # Razonamiento adicional
    if anomaly.anomaly_score > 0.5:
        reasoning.append(f"anomalía significativa (score={anomaly.anomaly_score:.2f})")
    if morphology.symmetry_score > 0.7:
        reasoning.append("alta simetría")
    if morphology.planarity > 0.7:
        reasoning.append("superficie plana no erosiva")
    if len(morphology.artificial_indicators) > 0:
        reasoning.append(f"indicadores: {', '.join(morphology.artificial_indicators)}")
    
    if len(reasoning) == 0:
        reasoning.append("sin indicadores antropogénicos claros")
    
    # 🟡 AJUSTE QUIRÚRGICO 3: Separar inference confidence de system confidence
    # Inference confidence: confianza en la inferencia (basada en evidencia)
    # System confidence: confianza en el sistema (reproducibilidad, determinismo)
    
    # INFERENCE CONFIDENCE (basada en evidencia y cobertura)
    inference_confidence = "low"  # Por defecto
    if anthropic_probability > 0.7 and len(reasoning) >= 3 and coverage_ratio > 0.7:
        inference_confidence = "high"
    elif anthropic_probability > 0.5 and coverage_ratio > 0.5:
        inference_confidence = "medium"
    elif anthropic_probability > 0.4:
        inference_confidence = "medium_low"
    else:
        inference_confidence = "low"
    
    # Usar inference_confidence como confidence principal
    confidence = inference_confidence
    
    print(f"[FASE D] Probabilidad antropogénica: {anthropic_probability:.3f} [{confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}]", flush=True)
    print(f"[FASE D] 🟡 Inference confidence: {inference_confidence} (basada en evidencia)", flush=True)
    print(f"[FASE D] 🟡 System confidence: high (deterministic, reproducible)", flush=True)
    print(f"[FASE D] Razonamiento: {reasoning}", flush=True)
    
    # Calcular métricas de cobertura para output
    # Usar el número REAL de instrumentos disponibles (pasado desde el endpoint)
    instruments_available_count = normalized.raw_measurements.get('instruments_available', len(weights))
    coverage_raw_value = raw_instrument_count / instruments_available_count if instruments_available_count > 0 else 0.0
    
    print(f"[FASE D] 📊 Métricas de cobertura:", flush=True)
    print(f"[FASE D]    Raw: {raw_instrument_count}/{instruments_available_count} = {coverage_raw_value:.1%}", flush=True)
    print(f"[FASE D]    Effective: {coverage_ratio:.1%}", flush=True)
    
    # 🔬 CALCULAR EXPLANATORY STRANGENESS SCORE (ESS)
    # Se activa cuando hay "algo extraño" sin anomalía instrumental
    explanatory_strangeness, strangeness_score, strangeness_reasons = _calculate_explanatory_strangeness(
        anomaly_score=anomaly.anomaly_score,
        anthropic_probability=anthropic_probability,
        symmetry=morphology.symmetry_score,
        planarity=morphology.planarity,
        edge_regularity=morphology.edge_regularity,
        epistemic_uncertainty=epistemic_uncertainty,
        geomorphology_hint=morphology.geomorphology_hint,
        environment_type=environment_type
    )
    
    # 🎯 SEPARACIÓN CIENTÍFICA EXPLÍCITA DE MÉTRICAS (estado del arte)
    # Separar ORIGEN vs ACTIVIDAD antropogénica
    print("[FASE D] 🎯 Calculando métricas separadas (origen vs actividad)...", flush=True)
    
    # 1. ANTHROPIC ORIGIN PROBABILITY: ¿Fue creado por humanos?
    # Basado en: morfología + ESS + sitios conocidos + contexto histórico
    anthropic_origin_probability = 0.0
    
    # Base: morfología (simetría, planaridad, regularidad)
    morphology_score = (
        morphology.symmetry_score * 0.4 +
        morphology.planarity * 0.3 +
        morphology.edge_regularity * 0.3
    )
    
    # Boost por ESS (si hay "algo extraño") - AUMENTADO para dar más peso
    ess_boost = 0.0
    if explanatory_strangeness == "very_high":
        ess_boost = 0.40  # Aumentado de 0.30 a 0.40
    elif explanatory_strangeness == "high":
        ess_boost = 0.30  # Aumentado de 0.20 a 0.30
    elif explanatory_strangeness == "medium":
        ess_boost = 0.15  # Aumentado de 0.10 a 0.15
    
    # Boost por sitios conocidos cercanos (si hay validación histórica)
    known_site_boost = 0.0
    if normalized.raw_measurements.get('is_known_archaeological_site', False):
        known_site_boost = 0.40  # Sitio conocido documentado
        print(f"[FASE D] 🏛️ Sitio arqueológico conocido detectado → +40% origen", flush=True)
    
    # Calcular probabilidad de origen
    anthropic_origin_probability = min(1.0, morphology_score + ess_boost + known_site_boost)
    
    # Ajustar por cobertura (si hay poca cobertura, reducir certeza pero no tanto)
    if coverage_ratio < 0.5:
        # Penalizar menos cuando hay ESS alto
        if explanatory_strangeness in ['high', 'very_high']:
            anthropic_origin_probability *= (0.7 + coverage_ratio * 0.3)  # Penalizar menos
        else:
            anthropic_origin_probability *= (0.5 + coverage_ratio)  # Penalizar más
    
    anthropic_origin_probability = float(np.clip(anthropic_origin_probability, 0, 1))
    
    # 2. ANTHROPIC ACTIVITY PROBABILITY: ¿Hay actividad humana actual?
    # Basado en: anomaly_score + señales térmicas + NDVI alto + cambios temporales
    anthropic_activity_probability = 0.0
    
    # Base: anomaly score (actividad genera anomalías)
    anthropic_activity_probability = anomaly.anomaly_score * 0.6
    
    # Boost por señales térmicas altas (actividad genera calor)
    thermal_boost = 0.0
    for key in normalized.features.keys():
        if 'thermal' in key.lower() or 'lst' in key.lower():
            thermal_value = abs(normalized.features.get(key, 0.0))
            if thermal_value > 2.0:  # Más de 2σ
                thermal_boost = min(0.2, thermal_value / 10.0)
                break
    
    # Boost por NDVI alto (vegetación activa)
    ndvi_boost = 0.0
    for key in normalized.features.keys():
        if 'ndvi' in key.lower():
            ndvi_value = abs(normalized.features.get(key, 0.0))
            if ndvi_value > 1.5:  # NDVI anormalmente alto
                ndvi_boost = min(0.15, ndvi_value / 10.0)
                break
    
    anthropic_activity_probability += thermal_boost + ndvi_boost
    anthropic_activity_probability = float(np.clip(anthropic_activity_probability, 0, 1))
    
    # 3. INSTRUMENTAL ANOMALY PROBABILITY: Probabilidad de anomalía instrumental
    # Simplemente = anomaly_score (ya calculado en FASE B)
    instrumental_anomaly_probability = float(anomaly.anomaly_score)
    
    # 4. MODEL INFERENCE CONFIDENCE: Confianza del modelo
    # Basado en: cobertura + convergencia + evidencia
    if coverage_ratio > 0.75 and len(reasoning) >= 3:
        model_inference_confidence = "high"
    elif coverage_ratio > 0.5 and len(reasoning) >= 2:
        model_inference_confidence = "medium"
    else:
        model_inference_confidence = "low"
    
    print(f"[FASE D] 🎯 Métricas separadas calculadas:", flush=True)
    print(f"[FASE D]    Origen antropogénico: {anthropic_origin_probability:.2%}", flush=True)
    print(f"[FASE D]    Actividad antropogénica: {anthropic_activity_probability:.2%}", flush=True)
    print(f"[FASE D]    Anomalía instrumental: {instrumental_anomaly_probability:.2%}", flush=True)
    print(f"[FASE D]    Confianza del modelo: {model_inference_confidence}", flush=True)
    
    # 🔧 AJUSTE CRÍTICO: Actualizar probabilidad legacy para sitios históricos
    # Si detectamos origen alto + anomalía baja = sitio histórico integrado
    if anthropic_origin_probability >= 0.70 and instrumental_anomaly_probability < 0.05:
        # Usar origen como probabilidad legacy (más representativo)
        anthropic_probability_adjusted = anthropic_origin_probability
        print(f"[FASE D] 🏛️ SITIO HISTÓRICO detectado:", flush=True)
        print(f"[FASE D]    Probabilidad legacy ajustada: {anthropic_probability:.2%} → {anthropic_probability_adjusted:.2%}", flush=True)
        anthropic_probability = anthropic_probability_adjusted
        reasoning.append("sitio histórico: origen alto sin anomalía actual")
    
    return AnthropicInference(
        anthropic_probability=anthropic_probability,
        confidence=confidence,
        confidence_interval=confidence_interval,
        reasoning=reasoning,
        model_used="weighted_ensemble_v1",
        coverage_raw=coverage_raw_value,
        coverage_effective=coverage_ratio,
        instruments_measured=raw_instrument_count,
        instruments_available=instruments_available_count,
        epistemic_uncertainty=epistemic_uncertainty,
        uncertainty_sources=uncertainty_sources if uncertainty_sources else [],
        explanatory_strangeness=explanatory_strangeness,
        strangeness_score=strangeness_score,
        strangeness_reasons=strangeness_reasons,
        # 🎯 MÉTRICAS SEPARADAS (estado del arte)
        anthropic_origin_probability=anthropic_origin_probability,
        anthropic_activity_probability=anthropic_activity_probability,
        instrumental_anomaly_probability=instrumental_anomaly_probability,
        model_inference_confidence=model_inference_confidence
    )