#!/usr/bin/env python3
"""
Pipeline Científico de Análisis Arqueológico - ArcheoScope
===========================================================

FILOSOFÍA: Primero medís, después dudás, luego explicás, y recién al final sugerís.

FASES:
A. Normalización y alineación (imprescindible)
B. Anomalía pura (sin arqueología todavía)
C. Morfología explícita (donde ganamos ventaja)
D. Clasificador antropogénico (con freno de mano)
E. Anti-patrones (nivel pro)
F. Salida científica (no marketing)
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from scipy import stats
from datetime import datetime

@dataclass
class NormalizedFeatures:
    """Features normalizadas por instrumento."""
    candidate_id: str
    features: Dict[str, float]
    raw_measurements: Dict[str, float]
    normalization_method: str
    local_context: Dict[str, Any]

@dataclass
class AnomalyResult:
    """Resultado de detección de anomalía pura."""
    anomaly_score: float  # 0.0 - 1.0
    outlier_dimensions: List[str]
    method: str
    confidence: str  # "high", "medium", "low"

@dataclass
class MorphologyResult:
    """Resultado de análisis morfológico."""
    symmetry_score: float
    edge_regularity: float
    planarity: float
    artificial_indicators: List[str]

@dataclass
class AnthropicInference:
    """Inferencia antropogénica (con freno de mano)."""
    anthropic_probability: float
    confidence: str
    confidence_interval: Tuple[float, float]
    reasoning: List[str]
    model_used: str

@dataclass
class ScientificOutput:
    """Salida científica completa."""
    candidate_id: str
    anomaly_score: float
    anthropic_probability: float
    confidence_interval: Tuple[float, float]
    recommended_action: str
    notes: str
    phases_completed: List[str]
    timestamp: str

class ScientificPipeline:
    """
    Pipeline científico completo para análisis arqueológico.
    
    NO hace trampa - detecta anomalías realmente.
    NO decide - solo sugiere con evidencia.
    """
    
    def __init__(self):
        """Inicializar pipeline."""
        self.anti_patterns = self._load_anti_patterns()
        print("[PIPELINE] ScientificPipeline inicializado", flush=True)
    
    def _load_anti_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Cargar anti-patrones conocidos (volcanes, dunas, etc.)."""
        return {
            "volcanic": {
                "thermal_high": True,
                "symmetry_radial": True,
                "slope_steep": True
            },
            "dune": {
                "thermal_variable": True,
                "symmetry_low": True,
                "slope_gentle": True
            },
            "erosion": {
                "thermal_stable": True,
                "symmetry_low": True,
                "slope_variable": True
            },
            "karst": {
                "thermal_stable": True,
                "symmetry_circular": True,
                "slope_steep": True
            }
        }
    
    # =========================================================================
    # FASE A: NORMALIZACIÓN Y ALINEACIÓN
    # =========================================================================
    
    def phase_a_normalize(self, 
                         raw_measurements: Dict[str, Any],
                         local_buffer_m: int = 200) -> NormalizedFeatures:
        """
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
        print("[FASE A] Normalizando mediciones por instrumento...", flush=True)
        
        features = {}
        local_context = {
            "buffer_m": local_buffer_m,
            "normalization_timestamp": datetime.now().isoformat()
        }
        
        # Normalizar cada tipo de medición
        for instrument, measurement in raw_measurements.items():
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
        
        print(f"[FASE A] Normalizadas {len(features)} features", flush=True)
        
        return NormalizedFeatures(
            candidate_id=candidate_id,
            features=features,
            raw_measurements=raw_measurements,
            normalization_method="z-score_local",
            local_context=local_context
        )
    
    # =========================================================================
    # FASE B: ANOMALÍA PURA
    # =========================================================================
    
    def phase_b_anomaly_detection(self, 
                                  normalized: NormalizedFeatures) -> AnomalyResult:
        """
        FASE B: Detectar anomalía pura (sin arqueología todavía).
        
        Objetivo: "Esto no se parece a su entorno"
        
        Técnicas:
        - Isolation Forest (simulado)
        - LOF - Local Outlier Factor (simulado)
        - PCA residuals (simulado)
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
    
    # =========================================================================
    # FASE C: MORFOLOGÍA EXPLÍCITA
    # =========================================================================
    
    def phase_c_morphology(self,
                          normalized: NormalizedFeatures,
                          anomaly: AnomalyResult) -> MorphologyResult:
        """
        FASE C: Análisis morfológico explícito.
        
        Métricas clave:
        - simetría radial
        - regularidad de bordes
        - pendiente constante
        - curvatura artificial
        
        Esto EXPLICA el sistema, no solo predice.
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
        
        print(f"[FASE C] Simetría: {symmetry_score:.3f}, Regularidad: {edge_regularity:.3f}, Planaridad: {planarity:.3f}", flush=True)
        print(f"[FASE C] Indicadores artificiales: {artificial_indicators}", flush=True)
        
        return MorphologyResult(
            symmetry_score=symmetry_score,
            edge_regularity=edge_regularity,
            planarity=planarity,
            artificial_indicators=artificial_indicators
        )
    
    # =========================================================================
    # FASE D: CLASIFICADOR ANTROPOGÉNICO
    # =========================================================================
    
    def phase_d_anthropic_inference(self,
                                    normalized: NormalizedFeatures,
                                    anomaly: AnomalyResult,
                                    morphology: MorphologyResult) -> AnthropicInference:
        """
        FASE D: Clasificador antropogénico (CON FRENO DE MANO).
        
        Este modelo NO decide, solo sugiere.
        
        Inputs:
        - anomaly_score
        - morfología
        - contexto (agua, altitud, rutas)
        
        Modelo explicable: Random Forest / Gradient Boosting simulado
        """
        print("[FASE D] Inferencia antropogénica (con freno de mano)...", flush=True)
        
        # Calcular probabilidad antropogénica
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
        
        # Intervalo de confianza (±10%)
        confidence_interval = (
            max(0.0, anthropic_probability - 0.1),
            min(1.0, anthropic_probability + 0.1)
        )
        
        # Razonamiento
        reasoning = []
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
        
        # Confianza
        if anthropic_probability > 0.7 and len(reasoning) >= 3:
            confidence = "high"
        elif anthropic_probability > 0.4:
            confidence = "medium"
        else:
            confidence = "low"
        
        print(f"[FASE D] Probabilidad antropogénica: {anthropic_probability:.3f} [{confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}]", flush=True)
        print(f"[FASE D] Confianza: {confidence}", flush=True)
        print(f"[FASE D] Razonamiento: {reasoning}", flush=True)
        
        return AnthropicInference(
            anthropic_probability=anthropic_probability,
            confidence=confidence,
            confidence_interval=confidence_interval,
            reasoning=reasoning,
            model_used="weighted_ensemble_v1"
        )
    
    # =========================================================================
    # FASE E: ANTI-PATRONES
    # =========================================================================
    
    def phase_e_anti_patterns(self,
                             normalized: NormalizedFeatures,
                             morphology: MorphologyResult) -> Optional[Dict[str, Any]]:
        """
        FASE E: Verificar anti-patrones (nivel pro).
        
        Registrar explícitamente:
        - volcanes
        - dunas
        - cárcavas
        - erosión fluvial
        
        Cada descarte entrena al sistema.
        """
        print("[FASE E] Verificando anti-patrones...", flush=True)
        
        features = normalized.features
        
        # Verificar cada anti-patrón
        for pattern_name, pattern_rules in self.anti_patterns.items():
            matches = 0
            total_rules = len(pattern_rules)
            
            # Verificar reglas (simulado - en producción usar lógica real)
            if pattern_rules.get('symmetry_radial') and morphology.symmetry_score > 0.8:
                matches += 1
            if pattern_rules.get('symmetry_low') and morphology.symmetry_score < 0.3:
                matches += 1
            
            # Si coincide >50% de reglas, es anti-patrón
            if matches / total_rules > 0.5:
                print(f"[FASE E] ANTI-PATRÓN DETECTADO: {pattern_name}", flush=True)
                return {
                    "rejected_as": pattern_name,
                    "features_conflict": list(pattern_rules.keys()),
                    "confidence": matches / total_rules
                }
        
        print("[FASE E] No se detectaron anti-patrones", flush=True)
        return None
    
    # =========================================================================
    # FASE F: SALIDA CIENTÍFICA
    # =========================================================================
    
    def phase_f_scientific_output(self,
                                  normalized: NormalizedFeatures,
                                  anomaly: AnomalyResult,
                                  morphology: MorphologyResult,
                                  anthropic: AnthropicInference,
                                  anti_pattern: Optional[Dict[str, Any]]) -> ScientificOutput:
        """
        FASE F: Generar salida científica (NO marketing).
        
        Nunca: ❌ "Sitio arqueológico detectado"
        Siempre: ✅ "Geo-candidata con anomalía morfológica significativa"
        """
        print("[FASE F] Generando salida científica...", flush=True)
        
        # Determinar acción recomendada
        if anti_pattern:
            recommended_action = "reject_natural_process"
            notes = f"Descartado como proceso natural: {anti_pattern['rejected_as']}"
        elif anthropic.anthropic_probability > 0.7 and anthropic.confidence == "high":
            recommended_action = "field_verification_priority"
            notes = "Geo-candidata con anomalía morfológica significativa - verificación de campo prioritaria"
        elif anthropic.anthropic_probability > 0.5:
            recommended_action = "field_verification"
            notes = "Geo-candidata con indicadores antropogénicos - verificación de campo recomendada"
        elif anthropic.anthropic_probability > 0.3:
            recommended_action = "monitoring"
            notes = "Anomalía detectada - monitoreo recomendado"
        else:
            recommended_action = "no_action"
            notes = "Consistente con procesos naturales - no requiere acción"
        
        # Fases completadas
        phases_completed = ["A_normalize", "B_anomaly", "C_morphology", "D_anthropic", "E_antipatterns", "F_output"]
        
        output = ScientificOutput(
            candidate_id=normalized.candidate_id,
            anomaly_score=anomaly.anomaly_score,
            anthropic_probability=anthropic.anthropic_probability,
            confidence_interval=anthropic.confidence_interval,
            recommended_action=recommended_action,
            notes=notes,
            phases_completed=phases_completed,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"[FASE F] Salida científica generada", flush=True)
        print(f"  - Anomaly score: {output.anomaly_score:.3f}", flush=True)
        print(f"  - Anthropic probability: {output.anthropic_probability:.3f}", flush=True)
        print(f"  - Recommended action: {output.recommended_action}", flush=True)
        print(f"  - Notes: {output.notes}", flush=True)
        
        return output
    
    # =========================================================================
    # PIPELINE COMPLETO
    # =========================================================================
    
    def analyze(self, raw_measurements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecutar pipeline científico completo.
        
        Returns:
            Dict con todas las fases y salida científica
        """
        print("\n" + "="*80, flush=True)
        print("INICIANDO PIPELINE CIENTÍFICO", flush=True)
        print("="*80 + "\n", flush=True)
        
        # FASE A: Normalización
        normalized = self.phase_a_normalize(raw_measurements)
        
        # FASE B: Anomalía pura
        anomaly = self.phase_b_anomaly_detection(normalized)
        
        # FASE C: Morfología
        morphology = self.phase_c_morphology(normalized, anomaly)
        
        # FASE D: Inferencia antropogénica
        anthropic = self.phase_d_anthropic_inference(normalized, anomaly, morphology)
        
        # FASE E: Anti-patrones
        anti_pattern = self.phase_e_anti_patterns(normalized, morphology)
        
        # FASE F: Salida científica
        output = self.phase_f_scientific_output(normalized, anomaly, morphology, anthropic, anti_pattern)
        
        print("\n" + "="*80, flush=True)
        print("PIPELINE CIENTÍFICO COMPLETADO", flush=True)
        print("="*80 + "\n", flush=True)
        
        # Retornar resultado completo
        return {
            "scientific_output": {
                "candidate_id": output.candidate_id,
                "anomaly_score": output.anomaly_score,
                "anthropic_probability": output.anthropic_probability,
                "confidence_interval": list(output.confidence_interval),
                "recommended_action": output.recommended_action,
                "notes": output.notes,
                "timestamp": output.timestamp
            },
            "phase_a_normalized": {
                "features": normalized.features,
                "normalization_method": normalized.normalization_method,
                "local_context": normalized.local_context
            },
            "phase_b_anomaly": {
                "anomaly_score": anomaly.anomaly_score,
                "outlier_dimensions": anomaly.outlier_dimensions,
                "method": anomaly.method,
                "confidence": anomaly.confidence
            },
            "phase_c_morphology": {
                "symmetry_score": morphology.symmetry_score,
                "edge_regularity": morphology.edge_regularity,
                "planarity": morphology.planarity,
                "artificial_indicators": morphology.artificial_indicators
            },
            "phase_d_anthropic": {
                "anthropic_probability": anthropic.anthropic_probability,
                "confidence": anthropic.confidence,
                "confidence_interval": list(anthropic.confidence_interval),
                "reasoning": anthropic.reasoning,
                "model_used": anthropic.model_used
            },
            "phase_e_anti_pattern": anti_pattern,
            "phases_completed": output.phases_completed
        }
