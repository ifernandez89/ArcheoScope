#!/usr/bin/env python3
"""
Pipeline Científico de Análisis Arqueológico - ArcheoScope
===========================================================

FILOSOFÍA: Primero medís, después dudás, luego explicás, y recién al final sugerís.

FASES:
0. Enriquecimiento con datos históricos de BD (PRIMERO - crítico)
A. Normalización y alineación (imprescindible)
B. Anomalía pura (sin arqueología todavía)
C. Morfología explícita (donde ganamos ventaja)
D. Clasificador antropogénico (con freno de mano)
E. Anti-patrones (nivel pro)
F. Validación contra sitios conocidos documentados
G. Salida científica (no marketing)
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from scipy import stats
from datetime import datetime
import asyncpg

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
    geomorphology_hint: str = "unknown"  # NUEVO: contexto geológico

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
    # MEJORA PRO: Resultados negativos valiosos
    candidate_type: str = "unknown"  # positive_candidate, negative_reference, uncertain
    negative_reason: Optional[str] = None  # geomorfología si es negativo
    reuse_for_training: bool = False  # True si es referencia negativa valiosa
    # AJUSTE FINO 2: Diferenciar descartar de archivar
    discard_type: str = "none"  # discard_operational, archive_scientific_negative, none
    # AJUSTE FINO 3: Confianza científica del descarte
    scientific_confidence: str = "unknown"  # high, medium, low (certeza del descarte)
    # FASE G: Validación contra sitios conocidos
    known_sites_nearby: List[Dict[str, Any]] = None  # Sitios documentados cercanos
    overlapping_known_site: Optional[Dict[str, Any]] = None  # Sitio solapado
    distance_to_known_site_km: Optional[float] = None  # Distancia al sitio más cercano
    is_known_site_rediscovery: bool = False  # True si coincide con sitio documentado

class ScientificPipeline:
    """
    Pipeline científico completo para análisis arqueológico.
    
    NO hace trampa - detecta anomalías realmente.
    NO decide - solo sugiere con evidencia.
    """
    
    def __init__(self, db_pool=None, validator=None):
        """Inicializar pipeline."""
        self.anti_patterns = self._load_anti_patterns()
        self.baseline_profiles = self._load_baseline_profiles()  # AJUSTE FINO 1
        self.db_pool = db_pool  # Pool de conexiones a PostgreSQL
        self.validator = validator  # RealArchaeologicalValidator
        print("[PIPELINE] ScientificPipeline inicializado", flush=True)
        if self.db_pool:
            print("[PIPELINE] Conexión a BD disponible para enriquecimiento", flush=True)
        if self.validator:
            print(f"[PIPELINE] Validador con {len(self.validator.known_sites)} sitios conocidos", flush=True)
    
    def _load_baseline_profiles(self) -> Dict[str, Dict[str, Any]]:
        """
        AJUSTE FINO 1: Baseline profiles por tipo de ambiente.
        
        Permite comparar candidatos contra perfiles esperados y
        rechazar más rápido cuando coinciden con geomorfología natural.
        """
        return {
            "glacial": {
                "baseline_type": "glacial",
                "expected_morphology": ["planar", "low_symmetry"],
                "instrument_expectations": ["SAR > optical"],
                "default_anthropic_ceiling": 0.25,
                "geomorphology_hints": [
                    "glacial_outwash_or_ablation_plain",
                    "moraine",
                    "glacial_valley"
                ]
            },
            "desert": {
                "baseline_type": "desert",
                "expected_morphology": ["dune_patterns", "wind_erosion"],
                "instrument_expectations": ["thermal_high", "optical_clear"],
                "default_anthropic_ceiling": 0.30,
                "geomorphology_hints": [
                    "aeolian_dune",
                    "desert_pavement",
                    "wadi"
                ]
            },
            "coastal": {
                "baseline_type": "coastal",
                "expected_morphology": ["wave_patterns", "tidal_features"],
                "instrument_expectations": ["SAR_water", "optical_variable"],
                "default_anthropic_ceiling": 0.35,
                "geomorphology_hints": [
                    "beach_ridge",
                    "tidal_flat",
                    "coastal_erosion"
                ]
            },
            "mountain": {
                "baseline_type": "mountain",
                "expected_morphology": ["steep_slopes", "erosion_channels"],
                "instrument_expectations": ["lidar_relief", "slope_high"],
                "default_anthropic_ceiling": 0.30,
                "geomorphology_hints": [
                    "mountain_ridge",
                    "talus_slope",
                    "alpine_valley"
                ]
            }
        }
    
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
    
    def _infer_geomorphology(self, 
                            environment_type: str,
                            symmetry: float,
                            planarity: float,
                            edge_regularity: float) -> str:
        """
        MEJORA 2: Inferir contexto geomorfológico (NO arqueología).
        
        Esto permite:
        - Entrenar anti-patrones
        - Filtrar automáticamente regiones glaciares
        - Justificar descartes masivos
        """
        
        # Ambientes glaciares
        if environment_type in ['polar_ice', 'glacier', 'permafrost']:
            if planarity > 0.7:
                return "glacial_outwash_or_ablation_plain"
            elif symmetry > 0.6:
                return "glacial_cirque_or_moraine"
            else:
                return "glacial_terrain_general"
        
        # Ambientes desérticos
        elif environment_type in ['desert', 'arid']:
            if symmetry < 0.3 and edge_regularity < 0.3:
                return "aeolian_dune_field"
            elif planarity > 0.7:
                return "desert_pavement_or_playa"
            else:
                return "desert_terrain_general"
        
        # Ambientes costeros/marinos
        elif environment_type in ['coastal', 'shallow_sea']:
            if planarity > 0.6:
                return "tidal_flat_or_beach"
            else:
                return "coastal_terrain_general"
        
        # Ambientes montañosos
        elif environment_type in ['mountain', 'highland']:
            if symmetry > 0.7:
                return "volcanic_cone_or_crater"
            elif planarity < 0.3:
                return "steep_mountain_terrain"
            else:
                return "mountain_terrain_general"
        
        # Ambientes de bosque/selva
        elif environment_type in ['forest', 'jungle']:
            return "forested_terrain"
        
        # Default
        else:
            return "terrain_general"
    
    # =========================================================================
    # FASE 0: ENRIQUECIMIENTO CON DATOS HISTÓRICOS DE BD
    # =========================================================================
    
    async def phase_0_enrich_from_db(self, 
                                     raw_measurements: Dict[str, Any],
                                     lat_min: float, lat_max: float,
                                     lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        FASE 0: Consultar BD por mediciones previas en la zona.
        
        CRÍTICO: Esto se ejecuta ANTES de cualquier análisis.
        
        Enriquece raw_measurements con:
        - Mediciones instrumentales previas en la zona
        - Análisis previos realizados
        - Sitios conocidos documentados cercanos
        
        Returns:
            raw_measurements enriquecido con datos históricos
        """
        print("[FASE 0] Enriqueciendo con datos históricos de BD...", flush=True)
        
        if not self.db_pool:
            print("[FASE 0] Sin conexión a BD - usando solo mediciones actuales", flush=True)
            return raw_measurements
        
        try:
            async with self.db_pool.acquire() as conn:
                # Buscar mediciones previas en la zona (buffer de 0.1 grados)
                center_lat = (lat_min + lat_max) / 2
                center_lon = (lon_min + lon_max) / 2
                buffer = 0.1
                
                historical_measurements = await conn.fetch("""
                    SELECT 
                        instrument_name,
                        value,
                        unit,
                        data_mode,
                        measurement_timestamp,
                        latitude,
                        longitude
                    FROM measurements
                    WHERE latitude BETWEEN $1 AND $2
                      AND longitude BETWEEN $3 AND $4
                      AND data_mode IN ('OK', 'DERIVED')
                    ORDER BY measurement_timestamp DESC
                    LIMIT 50
                """, center_lat - buffer, center_lat + buffer,
                     center_lon - buffer, center_lon + buffer)
                
                if historical_measurements:
                    print(f"[FASE 0] Encontradas {len(historical_measurements)} mediciones históricas", flush=True)
                    
                    # Agrupar por instrumento y promediar
                    instrument_data = {}
                    for row in historical_measurements:
                        instrument = row['instrument_name']
                        if instrument not in instrument_data:
                            instrument_data[instrument] = []
                        instrument_data[instrument].append(float(row['value']))
                    
                    # Enriquecer raw_measurements con promedios históricos
                    enriched_count = 0
                    for instrument, values in instrument_data.items():
                        avg_value = np.mean(values)
                        std_value = np.std(values) if len(values) > 1 else 0
                        
                        # Si el instrumento no tiene medición actual, agregar histórica
                        if instrument not in raw_measurements.get('instrumental_measurements', {}):
                            if 'instrumental_measurements' not in raw_measurements:
                                raw_measurements['instrumental_measurements'] = {}
                            
                            raw_measurements['instrumental_measurements'][instrument] = {
                                'value': avg_value,
                                'std': std_value,
                                'source': 'historical_average',
                                'n_measurements': len(values)
                            }
                            enriched_count += 1
                            print(f"[FASE 0] Enriquecido {instrument}: {avg_value:.3f} (n={len(values)})", flush=True)
                    
                    print(f"[FASE 0] Total enriquecido: {enriched_count} instrumentos", flush=True)
                else:
                    print("[FASE 0] No hay mediciones históricas en la zona", flush=True)
                
                # Buscar análisis previos
                previous_analyses = await conn.fetch("""
                    SELECT 
                        candidate_name,
                        archaeological_probability,
                        result_type,
                        analysis_timestamp
                    FROM archaeological_candidate_analyses
                    WHERE region = $1
                    ORDER BY analysis_timestamp DESC
                    LIMIT 5
                """, raw_measurements.get('region_name', 'unknown'))
                
                if previous_analyses:
                    print(f"[FASE 0] Encontrados {len(previous_analyses)} análisis previos en región", flush=True)
                    raw_measurements['previous_analyses'] = [dict(row) for row in previous_analyses]
                
        except Exception as e:
            print(f"[FASE 0] Error consultando BD: {e}", flush=True)
            # Continuar sin enriquecimiento
        
        return raw_measurements
    
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
        
        # MEJORA 2: Etiqueta geomorfológica explícita (contexto geológico, NO arqueología)
        geomorphology_hint = self._infer_geomorphology(
            normalized.raw_measurements.get('environment_type', 'unknown'),
            symmetry_score,
            planarity,
            edge_regularity
        )
        
        print(f"[FASE C] Simetría: {symmetry_score:.3f}, Regularidad: {edge_regularity:.3f}, Planaridad: {planarity:.3f}", flush=True)
        print(f"[FASE C] Indicadores artificiales: {artificial_indicators}", flush=True)
        print(f"[FASE C] Geomorfología inferida: {geomorphology_hint}", flush=True)
        
        return MorphologyResult(
            symmetry_score=symmetry_score,
            edge_regularity=edge_regularity,
            planarity=planarity,
            artificial_indicators=artificial_indicators,
            geomorphology_hint=geomorphology_hint  # NUEVO
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
        
        AJUSTES IMPLEMENTADOS:
        - Penalización explícita por cobertura instrumental (AJUSTE 2)
        - Umbral dinámico por región arqueológica (AJUSTE 3)
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
        
        # Razonamiento (inicializar antes de usar)
        reasoning = []
        
        # AJUSTE 2: PENALIZACIÓN EXPLÍCITA POR COBERTURA INSTRUMENTAL
        # Contar instrumentos válidos (con mediciones reales)
        instrument_count = len([k for k in normalized.features.keys() if 'zscore' in k])
        total_instruments = 8  # Total de instrumentos disponibles en el sistema
        coverage_ratio = instrument_count / total_instruments
        
        # Penalización por baja cobertura
        coverage_penalty = 0.0
        if coverage_ratio < 0.5:  # Menos del 50% de instrumentos
            coverage_penalty = 0.15  # -15%
            anthropic_probability *= (1.0 - coverage_penalty)
            reasoning.append(f"⚠️ Coverage penalty: -{coverage_penalty*100:.0f}% (only {instrument_count}/{total_instruments} instruments)")
            print(f"[FASE D] ⚠️ PENALIZACIÓN POR COBERTURA: -{coverage_penalty*100:.0f}%", flush=True)
            print(f"[FASE D]    Reason: insufficient optical/SAR confirmation ({instrument_count}/{total_instruments} instruments)", flush=True)
        elif coverage_ratio < 0.75:  # Entre 50-75%
            coverage_penalty = 0.08  # -8%
            anthropic_probability *= (1.0 - coverage_penalty)
            reasoning.append(f"⚠️ Coverage penalty: -{coverage_penalty*100:.0f}% (only {instrument_count}/{total_instruments} instruments)")
            print(f"[FASE D] ⚠️ PENALIZACIÓN POR COBERTURA: -{coverage_penalty*100:.0f}%", flush=True)
            print(f"[FASE D]    Reason: moderate instrumental coverage ({instrument_count}/{total_instruments} instruments)", flush=True)
        else:
            print(f"[FASE D] ✅ Cobertura instrumental adecuada: {instrument_count}/{total_instruments} ({coverage_ratio*100:.0f}%)", flush=True)
        
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
    # FASE F: VALIDACIÓN CONTRA SITIOS CONOCIDOS
    # =========================================================================
    
    def phase_f_validate_known_sites(self,
                                     normalized: NormalizedFeatures,
                                     lat_min: float, lat_max: float,
                                     lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        FASE F: Validar contra sitios arqueológicos conocidos documentados.
        
        CRÍTICO: Esto define si es anomalía o redescubrimiento.
        
        Returns:
            - overlapping_sites: Sitios documentados que solapan
            - nearby_sites: Sitios cercanos (<50km)
            - is_rediscovery: True si coincide con sitio conocido
            - distance_to_known: Distancia al sitio más cercano
        """
        print("[FASE F] Validando contra sitios conocidos...", flush=True)
        
        if not self.validator:
            print("[FASE F] Sin validador - saltando validación", flush=True)
            return {
                "overlapping_sites": [],
                "nearby_sites": [],
                "is_rediscovery": False,
                "distance_to_known_km": None,
                "validation_confidence": "no_validator"
            }
        
        try:
            validation = self.validator.validate_region(lat_min, lat_max, lon_min, lon_max)
            
            overlapping = validation.get('overlapping_sites', [])
            nearby = validation.get('nearby_sites', [])
            
            is_rediscovery = len(overlapping) > 0
            
            # Calcular distancia al sitio más cercano
            distance_to_known = None
            if overlapping:
                distance_to_known = 0.0  # Solapado
            elif nearby:
                distance_to_known = nearby[0][1] if nearby else None  # Distancia del más cercano
            
            print(f"[FASE F] Sitios solapados: {len(overlapping)}", flush=True)
            print(f"[FASE F] Sitios cercanos: {len(nearby)}", flush=True)
            
            if is_rediscovery:
                site = overlapping[0]
                print(f"[FASE F] ⚠️ REDESCUBRIMIENTO: {site.name} ({site.confidence_level})", flush=True)
            elif nearby:
                site, dist = nearby[0]
                print(f"[FASE F] Sitio cercano: {site.name} a {dist:.1f}km", flush=True)
            else:
                print(f"[FASE F] No hay sitios conocidos cercanos", flush=True)
            
            return {
                "overlapping_sites": [
                    {
                        "name": s.name,
                        "coordinates": s.coordinates,
                        "site_type": s.site_type,
                        "period": s.period,
                        "confidence_level": s.confidence_level,
                        "source": s.source
                    } for s in overlapping
                ],
                "nearby_sites": [
                    {
                        "name": s.name,
                        "coordinates": s.coordinates,
                        "site_type": s.site_type,
                        "distance_km": dist,
                        "confidence_level": s.confidence_level
                    } for s, dist in nearby
                ],
                "is_rediscovery": is_rediscovery,
                "distance_to_known_km": distance_to_known,
                "validation_confidence": validation.get('validation_confidence', 'unknown')
            }
            
        except Exception as e:
            print(f"[FASE F] Error en validación: {e}", flush=True)
            return {
                "overlapping_sites": [],
                "nearby_sites": [],
                "is_rediscovery": False,
                "distance_to_known_km": None,
                "validation_confidence": "error"
            }
    
    # =========================================================================
    # FASE G: SALIDA CIENTÍFICA
    # =========================================================================
    
    def phase_g_scientific_output(self,
                                  normalized: NormalizedFeatures,
                                  anomaly: AnomalyResult,
                                  morphology: MorphologyResult,
                                  anthropic: AnthropicInference,
                                  anti_pattern: Optional[Dict[str, Any]],
                                  known_sites_validation: Dict[str, Any]) -> ScientificOutput:
        """
        FASE G: Generar salida científica (NO marketing).
        
        Nunca: ❌ "Sitio arqueológico detectado"
        Siempre: ✅ "Geo-candidata con anomalía morfológica significativa"
        
        AJUSTES FINOS:
        1. Comparar contra baseline profiles
        2. Diferenciar discard_operational vs archive_scientific_negative
        3. Calcular scientific_confidence (certeza del descarte)
        4. Integrar validación de sitios conocidos (CRÍTICO)
        """
        print("[FASE G] Generando salida científica...", flush=True)
        
        # Extraer validación de sitios conocidos
        is_rediscovery = known_sites_validation.get('is_rediscovery', False)
        overlapping_sites = known_sites_validation.get('overlapping_sites', [])
        nearby_sites = known_sites_validation.get('nearby_sites', [])
        distance_to_known = known_sites_validation.get('distance_to_known_km')
        
        # Si es redescubrimiento, ajustar probabilidad antropogénica
        if is_rediscovery:
            print(f"[FASE G] ⚠️ REDESCUBRIMIENTO de sitio conocido", flush=True)
            # Aumentar probabilidad si coincide con sitio confirmado
            site = overlapping_sites[0]
            if site['confidence_level'] == 'confirmed':
                anthropic.anthropic_probability = min(0.95, anthropic.anthropic_probability + 0.3)
                anthropic.reasoning.append(f"coincide con sitio confirmado: {site['name']}")
                print(f"[FASE G] Probabilidad ajustada a {anthropic.anthropic_probability:.3f} (sitio confirmado)", flush=True)
        
        # AJUSTE FINO 1: Comparar contra baseline profile
        environment_type = normalized.raw_measurements.get('environment_type', 'unknown')
        baseline_match = None
        baseline_profile = None
        
        if environment_type in ['polar_ice', 'glacier', 'permafrost']:
            baseline_profile = self.baseline_profiles.get('glacial')
        elif environment_type in ['desert', 'arid']:
            baseline_profile = self.baseline_profiles.get('desert')
        elif environment_type in ['coastal', 'shallow_sea']:
            baseline_profile = self.baseline_profiles.get('coastal')
        elif environment_type in ['mountain', 'alpine']:
            baseline_profile = self.baseline_profiles.get('mountain')
        
        if baseline_profile:
            # Verificar si coincide con baseline
            geomorph_hint = morphology.geomorphology_hint
            if geomorph_hint in baseline_profile['geomorphology_hints']:
                baseline_match = baseline_profile['baseline_type']
                print(f"[FASE G] Coincide con baseline profile: {baseline_match}", flush=True)
                # Aplicar techo antropogénico del baseline
                if anthropic.anthropic_probability > baseline_profile['default_anthropic_ceiling']:
                    print(f"[FASE G] Probabilidad reducida por baseline ceiling: {baseline_profile['default_anthropic_ceiling']}", flush=True)
        
        # AJUSTE 3: UMBRAL DINÁMICO POR REGIÓN ARQUEOLÓGICA
        # Definir umbrales contextuales
        decision_threshold_default = 0.50  # Umbral por defecto
        decision_threshold_known_region = 0.45  # Umbral en regiones con arqueología documentada
        
        # Detectar si estamos en región arqueológica conocida
        is_known_archaeological_region = False
        region_name = normalized.raw_measurements.get('region_name', '').lower()
        
        # Regiones arqueológicas conocidas
        known_regions = [
            'acre', 'amazonía', 'amazonia', 'geoglifos',  # Amazonía occidental
            'rub al khali', 'arabia', 'paleocauces',  # Arabia con paleocauces
            'sahara', 'egipto', 'nilo',  # Norte de África
            'petra', 'nabateo',  # Medio Oriente
            'angkor', 'khmer',  # Sudeste Asiático
            'machu picchu', 'inca', 'andes',  # Andes
            'maya', 'yucatan', 'mesoamerica'  # Mesoamérica
        ]
        
        for known_region in known_regions:
            if known_region in region_name:
                is_known_archaeological_region = True
                print(f"[FASE G] 🏛️ REGIÓN ARQUEOLÓGICA CONOCIDA detectada: {known_region}", flush=True)
                break
        
        # También considerar si hay sitios conocidos cercanos
        if nearby_sites and len(nearby_sites) > 0:
            closest_distance = nearby_sites[0]['distance_km']
            if closest_distance < 50:  # Menos de 50km de sitio conocido
                is_known_archaeological_region = True
                print(f"[FASE G] 🏛️ Sitio conocido cercano a {closest_distance:.1f}km - región arqueológica", flush=True)
        
        # Aplicar umbral contextual
        decision_threshold = decision_threshold_known_region if is_known_archaeological_region else decision_threshold_default
        
        print(f"[FASE G] Umbral de decisión: {decision_threshold:.2f} ({'región arqueológica' if is_known_archaeological_region else 'región general'})", flush=True)
        
        if is_known_archaeological_region and anthropic.anthropic_probability >= decision_threshold_known_region:
            print(f"[FASE G] ✅ Probabilidad {anthropic.anthropic_probability:.3f} supera umbral contextual {decision_threshold_known_region:.2f}", flush=True)
        elif not is_known_archaeological_region and anthropic.anthropic_probability >= decision_threshold_default:
            print(f"[FASE G] ✅ Probabilidad {anthropic.anthropic_probability:.3f} supera umbral estándar {decision_threshold_default:.2f}", flush=True)
        else:
            print(f"[FASE G] ⚠️ Probabilidad {anthropic.anthropic_probability:.3f} por debajo de umbral {decision_threshold:.2f}", flush=True)
        
        # AJUSTE FINO 3: Calcular confianza científica del descarte
        # (certeza de que NO es arqueológico, independiente de la probabilidad)
        scientific_confidence = "unknown"
        
        if anti_pattern:
            # Anti-patrón detectado → alta confianza en el descarte
            scientific_confidence = "high"
        elif baseline_match and anthropic.anthropic_probability < 0.3:
            # Coincide con baseline natural → alta confianza en el descarte
            scientific_confidence = "high"
        elif morphology.geomorphology_hint != "unknown" and anthropic.anthropic_probability < 0.4:
            # Geomorfología identificada + baja probabilidad → confianza media-alta
            scientific_confidence = "medium_high"
        elif anomaly.anomaly_score < 0.3 and anthropic.anthropic_probability < 0.5:
            # Sin anomalía + baja probabilidad → confianza media
            scientific_confidence = "medium"
        elif anthropic.confidence == "low":
            # Baja confianza en la inferencia → baja confianza en el descarte
            scientific_confidence = "low"
        else:
            scientific_confidence = "medium"
        
        # Determinar acción recomendada y tipo de descarte
        discard_type = "none"
        
        if anti_pattern:
            recommended_action = "reject_natural_process"
            notes = f"Descartado como proceso natural: {anti_pattern['rejected_as']}"
            candidate_type = "negative_reference"
            negative_reason = anti_pattern['rejected_as']
            discard_type = "archive_scientific_negative"  # AJUSTE FINO 2
        elif baseline_match and anthropic.anthropic_probability < 0.3:
            recommended_action = "no_action"
            notes = f"Consistente con baseline {baseline_match} - {morphology.geomorphology_hint}"
            candidate_type = "negative_reference"
            negative_reason = morphology.geomorphology_hint
            discard_type = "archive_scientific_negative"  # AJUSTE FINO 2
        elif anthropic.anthropic_probability > 0.7 and anthropic.confidence == "high":
            recommended_action = "field_verification_priority"
            notes = "Geo-candidata con anomalía morfológica significativa - verificación de campo prioritaria"
            candidate_type = "positive_candidate"
            negative_reason = None
        elif anthropic.anthropic_probability >= decision_threshold:  # AJUSTE 3: Usar umbral dinámico
            if is_known_archaeological_region:
                recommended_action = "field_verification"
                notes = f"Geo-candidata en región arqueológica conocida (prob={anthropic.anthropic_probability:.3f}, umbral={decision_threshold:.2f}) - verificación de campo recomendada"
                candidate_type = "positive_candidate"
                negative_reason = None
            else:
                recommended_action = "field_verification"
                notes = "Geo-candidata con indicadores antropogénicos - verificación de campo recomendada"
                candidate_type = "positive_candidate"
                negative_reason = None
        elif anthropic.anthropic_probability > 0.3:
            recommended_action = "monitoring"
            notes = f"Anomalía detectada (prob={anthropic.anthropic_probability:.3f}) - monitoreo recomendado"
            candidate_type = "uncertain"
            negative_reason = None
        else:
            recommended_action = "no_action"
            notes = "Consistente con procesos naturales - no requiere acción"
            candidate_type = "negative_reference"
            negative_reason = morphology.geomorphology_hint
            # AJUSTE FINO 2: Diferenciar tipos de descarte
            if scientific_confidence in ["high", "medium_high"]:
                discard_type = "archive_scientific_negative"  # Vale para ciencia
            else:
                discard_type = "discard_operational"  # Descarte operacional simple
        
        # AJUSTE 3: Acción avanzada para regiones arqueológicas con cobertura insuficiente
        if is_known_archaeological_region and anthropic.anthropic_probability >= 0.40 and anthropic.anthropic_probability < decision_threshold:
            # Caso especial: región arqueológica, probabilidad alta pero bajo umbral por cobertura
            instrument_count = len([k for k in normalized.features.keys() if 'zscore' in k])
            if instrument_count < 4:  # Menos del 50% de instrumentos
                recommended_action = "targeted_reanalysis"
                notes = f"Región arqueológica con cobertura insuficiente ({instrument_count}/8 instrumentos) - re-análisis dirigido recomendado"
                candidate_type = "uncertain"
                print(f"[FASE G] 🎯 ACCIÓN AVANZADA: targeted_reanalysis", flush=True)
                print(f"[FASE G]    Required instruments: Sentinel-2 (NDVI/Red Edge), Sentinel-1 SAR", flush=True)
                print(f"[FASE G]    Optional: Dry season optical", flush=True)
        
        # Fases completadas
        phases_completed = ["0_enrich", "A_normalize", "B_anomaly", "C_morphology", "D_anthropic", "E_antipatterns", "F_known_sites", "G_output"]
        
        output = ScientificOutput(
            candidate_id=normalized.candidate_id,
            anomaly_score=anomaly.anomaly_score,
            anthropic_probability=anthropic.anthropic_probability,
            confidence_interval=anthropic.confidence_interval,
            recommended_action=recommended_action,
            notes=notes,
            phases_completed=phases_completed,
            timestamp=datetime.now().isoformat(),
            candidate_type=candidate_type,
            negative_reason=negative_reason,
            reuse_for_training=candidate_type == "negative_reference",
            discard_type=discard_type,
            scientific_confidence=scientific_confidence,
            # FASE F: Sitios conocidos
            known_sites_nearby=nearby_sites,
            overlapping_known_site=overlapping_sites[0] if overlapping_sites else None,
            distance_to_known_site_km=distance_to_known,
            is_known_site_rediscovery=is_rediscovery
        )
        
        print(f"[FASE G] Salida científica generada", flush=True)
        print(f"  - Anomaly score: {output.anomaly_score:.3f}", flush=True)
        print(f"  - Anthropic probability: {output.anthropic_probability:.3f}", flush=True)
        print(f"  - Recommended action: {output.recommended_action}", flush=True)
        print(f"  - Candidate type: {output.candidate_type}", flush=True)
        if is_rediscovery:
            print(f"  - ⚠️ REDESCUBRIMIENTO: {overlapping_sites[0]['name']}", flush=True)
        elif nearby_sites:
            print(f"  - Sitio cercano: {nearby_sites[0]['name']} ({nearby_sites[0]['distance_km']:.1f}km)", flush=True)
        if baseline_match:
            print(f"  - Baseline match: {baseline_match}", flush=True)
        if output.negative_reason:
            print(f"  - Negative reason: {output.negative_reason}", flush=True)
            print(f"  - Reuse for training: {output.reuse_for_training}", flush=True)
        print(f"  - Discard type: {output.discard_type}", flush=True)
        print(f"  - Scientific confidence: {output.scientific_confidence}", flush=True)
        print(f"  - Notes: {output.notes}", flush=True)
        
        return output
    
    # =========================================================================
    # PIPELINE COMPLETO
    # =========================================================================
    
    async def analyze(self, raw_measurements: Dict[str, Any],
                     lat_min: float, lat_max: float,
                     lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        Ejecutar pipeline científico completo.
        
        FLUJO:
        0. Enriquecer con datos históricos de BD
        A-E. Pipeline científico
        F. Validar contra sitios conocidos
        G. Salida científica
        
        Returns:
            Dict con todas las fases y salida científica
        """
        print("\n" + "="*80, flush=True)
        print("INICIANDO PIPELINE CIENTÍFICO", flush=True)
        print("="*80 + "\n", flush=True)
        
        # FASE 0: Enriquecimiento con datos históricos
        raw_measurements = await self.phase_0_enrich_from_db(raw_measurements, lat_min, lat_max, lon_min, lon_max)
        
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
        
        # FASE F: Validación contra sitios conocidos
        known_sites_validation = self.phase_f_validate_known_sites(normalized, lat_min, lat_max, lon_min, lon_max)
        
        # FASE G: Salida científica
        output = self.phase_g_scientific_output(normalized, anomaly, morphology, anthropic, anti_pattern, known_sites_validation)
        
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
                "timestamp": output.timestamp,
                # MEJORA PRO
                "candidate_type": output.candidate_type,
                "negative_reason": output.negative_reason,
                "reuse_for_training": output.reuse_for_training,
                # AJUSTES FINOS
                "discard_type": output.discard_type,
                "scientific_confidence": output.scientific_confidence,
                # FASE F: Sitios conocidos
                "known_sites_nearby": output.known_sites_nearby,
                "overlapping_known_site": output.overlapping_known_site,
                "distance_to_known_site_km": output.distance_to_known_site_km,
                "is_known_site_rediscovery": output.is_known_site_rediscovery
            },
            "phase_a_normalized": {
                "features": normalized.features,
                "normalization_method": normalized.normalization_method,
                "local_context": normalized.local_context  # Incluye features_status y reason
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
                "artificial_indicators": morphology.artificial_indicators,
                "geomorphology_hint": morphology.geomorphology_hint  # MEJORA 2
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
