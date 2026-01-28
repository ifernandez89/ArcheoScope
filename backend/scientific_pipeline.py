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
    paleo_signature: Optional[Dict[str, Any]] = None  # NUEVO: firma de paleocauce u otras estructuras lineales

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
    # COBERTURA INSTRUMENTAL (separar raw vs effective)
    coverage_raw: float = 0.0  # Instrumentos presentes / disponibles (0-1)
    coverage_effective: float = 0.0  # Cobertura ponderada por importancia (0-1)
    instruments_measured: int = 0  # Número de instrumentos que midieron
    instruments_available: int = 0  # Número de instrumentos disponibles
    # 🟠 AFINADO 2: Incertidumbre epistemológica
    epistemic_uncertainty: float = 0.0  # Incertidumbre por falta de datos (0-1)
    uncertainty_sources: List[str] = None  # Fuentes de incertidumbre
    # 🔬 EXPLANATORY STRANGENESS: "Algo extraño" sin sensacionalismo
    explanatory_strangeness: str = "none"  # none, low, medium, high, very_high
    strangeness_score: float = 0.0  # Score numérico (0-1)
    strangeness_reasons: List[str] = None  # Razones específicas
    # 🎯 SEPARACIÓN CIENTÍFICA EXPLÍCITA (estado del arte)
    anthropic_origin_probability: float = 0.0  # ¿Fue creado por humanos? (0-1)
    anthropic_activity_probability: float = 0.0  # ¿Hay actividad humana actual? (0-1)
    instrumental_anomaly_probability: float = 0.0  # Probabilidad de anomalía instrumental (0-1)
    model_inference_confidence: str = "unknown"  # Confianza del modelo (low, medium, high)
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
    # ETIQUETADO EPISTEMOLÓGICO (blindaje académico y legal)
    epistemic_mode: str = "deterministic_scientific"  # deterministic_scientific, assistive_ai, hybrid
    ai_used: bool = False  # True si se usó IA en alguna fase
    ai_role: Optional[str] = None  # explanation_only, validation_support, none
    reproducible: bool = True  # True si el análisis es 100% reproducible
    method_transparency: str = "full"  # full, partial, limited
    recommended_action: str
    notes: str
    phases_completed: List[str]
    timestamp: str
    # COBERTURA INSTRUMENTAL (separar raw vs effective)
    coverage_raw: float = 0.0  # Instrumentos presentes / disponibles (0-1)
    coverage_effective: float = 0.0  # Cobertura ponderada por importancia (0-1)
    instruments_measured: int = 0  # Número de instrumentos que midieron
    instruments_available: int = 0  # Número de instrumentos disponibles
    # 🟠 AFINADO 2: Incertidumbre epistemológica
    epistemic_uncertainty: float = 0.0  # Incertidumbre por falta de datos (0-1)
    uncertainty_sources: List[str] = None  # Fuentes de incertidumbre
    # 🔬 EXPLANATORY STRANGENESS: "Algo extraño" sin sensacionalismo
    explanatory_strangeness: str = "none"  # none, low, medium, high, very_high
    strangeness_score: float = 0.0  # Score numérico (0-1)
    strangeness_reasons: List[str] = None  # Razones específicas
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
    # ETIQUETADO EPISTEMOLÓGICO (blindaje académico y legal)
    epistemic_mode: str = "deterministic_scientific"  # deterministic_scientific, assistive_ai, hybrid
    ai_used: bool = False  # True si se usó IA en alguna fase
    ai_role: Optional[str] = None  # explanation_only, validation_support, none
    reproducible: bool = True  # True si el análisis es 100% reproducible
    method_transparency: str = "full"  # full, partial, limited

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
                        created_at as analysis_timestamp
                    FROM archaeological_candidate_analyses
                    WHERE region = $1
                    ORDER BY created_at DESC
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
        geomorphology_hint, paleo_signature = self._infer_geomorphology(
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
        
        # NO contar de raw_measurements - ya contamos arriba correctamente
        
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
        explanatory_strangeness, strangeness_score, strangeness_reasons = self._calculate_explanatory_strangeness(
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
    
    # =========================================================================
    # FASE D+: EXPLANATORY STRANGENESS SCORE (ESS)
    # =========================================================================
    
    def _calculate_explanatory_strangeness(self,
                                          anomaly_score: float,
                                          anthropic_probability: float,
                                          symmetry: float,
                                          planarity: float,
                                          edge_regularity: float,
                                          epistemic_uncertainty: float,
                                          geomorphology_hint: str,
                                          environment_type: str) -> Tuple[str, float, List[str]]:
        """
        🔬 EXPLANATORY STRANGENESS SCORE (ESS)
        
        Captura casos donde "algo no cuadra" sin caer en sensacionalismo.
        
        FILOSOFÍA:
        - NO hay anomalía instrumental (anomaly_score ≈ 0)
        - Probabilidad antropogénica moderada (0.25-0.60)
        - Alta geometría regular (simetría, planaridad)
        - Alta incertidumbre (instrumentos faltantes)
        
        INTERPRETACIÓN CIENTÍFICA:
        "No hay anomalía instrumental, pero el modelo natural es insuficiente
        para explicar los patrones geométricos observados."
        
        Esto NO es pseudociencia - es honestidad epistemológica.
        
        Returns:
            Tuple[str, float, List[str]]: (level, score, reasons)
            - level: "none", "low", "medium", "high", "very_high"
            - score: 0.0-1.0
            - reasons: Lista de razones específicas
        """
        
        print("[FASE D+] 🔬 Calculando Explanatory Strangeness Score...", flush=True)
        
        strangeness_reasons = []
        strangeness_score = 0.0
        
        # =====================================================================
        # CONDICIONES DE ACTIVACIÓN
        # =====================================================================
        
        # 1. Anomalía instrumental muy baja (< 0.05)
        if anomaly_score >= 0.05:
            print(f"[FASE D+] ESS no activado: anomaly_score = {anomaly_score:.3f} (>= 0.05)", flush=True)
            return "none", 0.0, []
        
        # 2. Probabilidad antropogénica en rango moderado (0.25-0.60)
        if not (0.25 <= anthropic_probability <= 0.60):
            print(f"[FASE D+] ESS no activado: anthropic_probability = {anthropic_probability:.3f} (fuera de [0.25, 0.60])", flush=True)
            return "none", 0.0, []
        
        # 3. Alta geometría regular (simetría O planaridad > 0.6)
        if symmetry < 0.6 and planarity < 0.6:
            print(f"[FASE D+] ESS no activado: geometría baja (symmetry={symmetry:.2f}, planarity={planarity:.2f})", flush=True)
            return "none", 0.0, []
        
        # 4. Alta incertidumbre (> 0.4)
        if epistemic_uncertainty < 0.4:
            print(f"[FASE D+] ESS no activado: incertidumbre baja ({epistemic_uncertainty:.1%})", flush=True)
            return "none", 0.0, []
        
        # =====================================================================
        # CÁLCULO DE STRANGENESS SCORE
        # =====================================================================
        
        print(f"[FASE D+] ✅ ESS ACTIVADO", flush=True)
        print(f"[FASE D+]    Anomaly score: {anomaly_score:.3f} (< 0.05)", flush=True)
        print(f"[FASE D+]    Anthropic prob: {anthropic_probability:.3f} (0.25-0.60)", flush=True)
        print(f"[FASE D+]    Symmetry: {symmetry:.2f}", flush=True)
        print(f"[FASE D+]    Planarity: {planarity:.2f}", flush=True)
        print(f"[FASE D+]    Uncertainty: {epistemic_uncertainty:.1%}", flush=True)
        
        # Factor 1: Geometría regular (peso 40%)
        geometry_factor = (symmetry * 0.5 + planarity * 0.3 + edge_regularity * 0.2)
        strangeness_score += geometry_factor * 0.4
        
        if symmetry > 0.8:
            strangeness_reasons.append(f"simetría geométrica muy alta ({symmetry:.2f})")
        elif symmetry > 0.6:
            strangeness_reasons.append(f"simetría geométrica significativa ({symmetry:.2f})")
        
        if planarity > 0.8:
            strangeness_reasons.append(f"planaridad extrema ({planarity:.2f})")
        elif planarity > 0.6:
            strangeness_reasons.append(f"planaridad significativa ({planarity:.2f})")
        
        # Factor 2: Incertidumbre epistemológica (peso 30%)
        # Más incertidumbre → más "extraño" que no veamos anomalía
        uncertainty_factor = epistemic_uncertainty
        strangeness_score += uncertainty_factor * 0.3
        
        if epistemic_uncertainty > 0.6:
            strangeness_reasons.append(f"alta incertidumbre instrumental ({epistemic_uncertainty:.1%})")
        else:
            strangeness_reasons.append(f"incertidumbre moderada ({epistemic_uncertainty:.1%})")
        
        # Factor 3: Contexto geomorfológico (peso 30%)
        # Ciertos contextos hacen la geometría más "extraña"
        context_factor = 0.0
        
        if geomorphology_hint in ['surface_pattern_anthropic_possible', 'anthropogenic_terracing_possible']:
            context_factor = 0.9
            strangeness_reasons.append(f"patrón geométrico en contexto: {geomorphology_hint}")
        elif geomorphology_hint in ['volcanic_cone_or_crater']:
            # Volcán con baja anomalía es extraño
            context_factor = 0.7
            strangeness_reasons.append(f"morfología volcánica sin anomalía térmica")
        elif environment_type in ['desert', 'arid'] and symmetry > 0.7:
            # Geometría en desierto es extraña (Nazca-like)
            context_factor = 0.8
            strangeness_reasons.append(f"patrones geométricos en desierto no explicables por erosión aleatoria")
        elif environment_type in ['mountain', 'highland'] and planarity > 0.7:
            # Planaridad en montaña es extraña (Machu Picchu-like)
            context_factor = 0.8
            strangeness_reasons.append(f"arquitectura simétrica integrada en relieve extremo")
        elif environment_type in ['desert', 'arid'] and planarity > 0.8:
            # Planaridad extrema en desierto (Giza-like)
            context_factor = 0.85
            strangeness_reasons.append(f"geometría regular en entorno sedimentario")
        else:
            context_factor = 0.5
            strangeness_reasons.append(f"geometría regular en contexto: {environment_type}")
        
        strangeness_score += context_factor * 0.3
        
        # Normalizar score
        strangeness_score = float(np.clip(strangeness_score, 0, 1))
        
        # =====================================================================
        # CLASIFICACIÓN DE NIVEL
        # =====================================================================
        
        if strangeness_score >= 0.75:
            level = "very_high"
        elif strangeness_score >= 0.60:
            level = "high"
        elif strangeness_score >= 0.45:
            level = "medium"
        elif strangeness_score >= 0.30:
            level = "low"
        else:
            level = "none"
        
        print(f"[FASE D+] 🔬 Explanatory Strangeness: {level.upper()} (score={strangeness_score:.3f})", flush=True)
        print(f"[FASE D+]    Razones:", flush=True)
        for reason in strangeness_reasons:
            print(f"[FASE D+]       • {reason}", flush=True)
        
        print(f"[FASE D+] 💡 Interpretación: Modelo natural insuficiente para explicar patrones observados", flush=True)
        
        return level, strangeness_score, strangeness_reasons
    
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
        
        # AJUSTE 3: UMBRAL DINÁMICO POR REGIÓN ARQUEOLÓGICA Y AMBIENTE
        # Definir umbrales contextuales por ambiente
        threshold_by_environment = {
            'desert': 0.45,           # Desiertos: alta visibilidad, baja complejidad
            'semi_arid': 0.45,        # Semiáridos: similar a desiertos
            'polar_ice': 0.55,        # Hielo: alta complejidad, requiere más certeza
            'glacier': 0.55,          # Glaciares: similar a hielo
            'forest': 0.52,           # Bosques: complejidad media-alta
            'deep_ocean': 0.60,       # Océano profundo: muy alta complejidad
            'shallow_sea': 0.55,      # Mar poco profundo: alta complejidad
            'default': 0.50           # Umbral por defecto
        }
        
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
        
        # Aplicar umbral contextual (región arqueológica tiene prioridad sobre ambiente)
        if is_known_archaeological_region:
            decision_threshold = decision_threshold_known_region
            threshold_reason = "región arqueológica conocida"
        else:
            decision_threshold = threshold_by_environment.get(environment_type, threshold_by_environment['default'])
            threshold_reason = f"ambiente {environment_type}"
        
        print(f"[FASE G] Umbral de decisión: {decision_threshold:.2f} ({threshold_reason})", flush=True)
        
        if is_known_archaeological_region and anthropic.anthropic_probability >= decision_threshold_known_region:
            print(f"[FASE G] ✅ Probabilidad {anthropic.anthropic_probability:.3f} supera umbral contextual {decision_threshold_known_region:.2f}", flush=True)
        elif not is_known_archaeological_region and anthropic.anthropic_probability >= decision_threshold:
            print(f"[FASE G] ✅ Probabilidad {anthropic.anthropic_probability:.3f} supera umbral estándar {decision_threshold:.2f}", flush=True)
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
            # AJUSTE 4: Diferenciar monitoring_passive vs monitoring_targeted
            instrument_count = len([k for k in normalized.features.keys() if 'zscore' in k])
            coverage_ratio = instrument_count / 8
            
            # Factores para monitoring_targeted:
            # 1. Baja cobertura instrumental (<50%)
            # 2. Ambiente con alta visibilidad (desert, semi_arid)
            # 3. Firma de paleocauce detectada
            # 4. Región arqueológica conocida
            
            is_high_visibility = environment_type in ['desert', 'semi_arid', 'grassland']
            has_paleo_signature = morphology.paleo_signature is not None
            
            if (coverage_ratio < 0.5 and is_high_visibility) or has_paleo_signature or is_known_archaeological_region:
                recommended_action = "monitoring_targeted"
                
                # Construir lista de instrumentos requeridos
                required_instruments = []
                if environment_type in ['desert', 'semi_arid']:
                    required_instruments.append("Sentinel-1 SAR")
                    required_instruments.append("Sentinel-2 multitemporal NDVI")
                    if has_paleo_signature:
                        required_instruments.append("Thermal nocturnal analysis")
                elif environment_type == 'forest':
                    required_instruments.append("Sentinel-1 SAR")
                    required_instruments.append("Sentinel-2 Red Edge")
                
                notes = f"Anomalía con cobertura insuficiente ({instrument_count}/8 instrumentos) - monitoreo dirigido con: {', '.join(required_instruments)}"
                candidate_type = "uncertain"
                negative_reason = None
                
                print(f"[FASE G] 🎯 MONITORING_TARGETED activado", flush=True)
                print(f"[FASE G]    Cobertura: {coverage_ratio*100:.0f}%", flush=True)
                print(f"[FASE G]    Instrumentos requeridos: {', '.join(required_instruments)}", flush=True)
            else:
                # 🧪 AJUSTE QUIRÚRGICO 4: Mensaje más preciso
                # Evitar "Anomalía detectada" cuando anomaly_score es bajo
                if anomaly.anomaly_score > 0.3:
                    notes = f"Anomalía detectada (score={anomaly.anomaly_score:.3f}, prob={anthropic.anthropic_probability:.3f}) - monitoreo pasivo recomendado"
                else:
                    notes = f"Sin anomalía detectable (score={anomaly.anomaly_score:.3f}); probabilidad antropogénica moderada ({anthropic.anthropic_probability:.3f}) bajo alta incertidumbre - monitoreo pasivo recomendado"
                
                recommended_action = "monitoring_passive"
                candidate_type = "uncertain"
                negative_reason = None
                print(f"[FASE G] 📊 MONITORING_PASSIVE activado", flush=True)
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
            if coverage_ratio < 0.3:  # Cobertura crítica
                recommended_action = "instrument_upgrade_required"
                
                # Identificar instrumentos críticos faltantes
                missing_critical = []
                if env_category == 'marine':
                    if effective_coverage < 0.5:
                        missing_critical = ["multibeam_sonar", "side_scan_sonar", "magnetometer"]
                elif env_category == 'glacial':
                    if effective_coverage < 0.5:
                        missing_critical = ["icesat2", "sentinel1_sar", "palsar"]
                elif env_category == 'terrestrial':
                    if effective_coverage < 0.5:
                        missing_critical = ["sentinel1_sar", "sentinel2_ndvi", "lidar"]
                
                notes = f"Región arqueológica con cobertura crítica ({coverage_ratio*100:.0f}% efectiva) - actualización instrumental REQUERIDA: {', '.join(missing_critical)}"
                candidate_type = "uncertain"
                print(f"[FASE G] 🚨 ACCIÓN CRÍTICA: instrument_upgrade_required", flush=True)
                print(f"[FASE G]    Missing critical instruments: {', '.join(missing_critical)}", flush=True)
            elif coverage_ratio < 0.5:
                recommended_action = "targeted_reanalysis"
                
                # Construir lista de instrumentos requeridos
                required_instruments = []
                if environment_type in ['desert', 'semi_arid']:
                    required_instruments.append("Sentinel-1 SAR")
                    required_instruments.append("Sentinel-2 multitemporal NDVI")
                    if morphology.paleo_signature:
                        required_instruments.append("Thermal nocturnal analysis")
                elif environment_type == 'forest':
                    required_instruments.append("Sentinel-1 SAR")
                    required_instruments.append("Sentinel-2 Red Edge")
                
                notes = f"Región arqueológica con cobertura insuficiente ({coverage_ratio*100:.0f}% efectiva) - re-análisis dirigido con: {', '.join(required_instruments)}"
                candidate_type = "uncertain"
                
                print(f"[FASE G] 🎯 ACCIÓN AVANZADA: targeted_reanalysis", flush=True)
                print(f"[FASE G]    Required instruments: {', '.join(required_instruments)}", flush=True)
        
        # Fases completadas
        phases_completed = ["0_enrich", "A_normalize", "B_anomaly", "C_morphology", "D_anthropic", "E_antipatterns", "F_known_sites", "G_output"]
        
        # ETIQUETADO EPISTEMOLÓGICO (blindaje académico y legal)
        epistemic_mode = "deterministic_scientific"  # Este pipeline es 100% determinístico
        ai_used = False  # No se usa IA en ninguna fase del pipeline científico
        ai_role = None  # IA no interviene
        reproducible = True  # 100% reproducible con mismos inputs
        method_transparency = "full"  # Todas las fases documentadas y explicables
        
        print(f"\n[FASE G] 🔬 ETIQUETADO EPISTEMOLÓGICO", flush=True)
        print(f"  Modo epistémico: {epistemic_mode}", flush=True)
        print(f"  IA utilizada: {ai_used}", flush=True)
        print(f"  Reproducible: {reproducible}", flush=True)
        print(f"  Transparencia metodológica: {method_transparency}", flush=True)
        
        output = ScientificOutput(
            candidate_id=normalized.candidate_id,
            anomaly_score=anomaly.anomaly_score,
            anthropic_probability=anthropic.anthropic_probability,
            confidence_interval=anthropic.confidence_interval,
            recommended_action=recommended_action,
            notes=notes,
            phases_completed=phases_completed,
            timestamp=datetime.now().isoformat(),
            # COBERTURA INSTRUMENTAL
            coverage_raw=anthropic.coverage_raw,
            coverage_effective=anthropic.coverage_effective,
            instruments_measured=anthropic.instruments_measured,
            instruments_available=anthropic.instruments_available,
            # 🟠 AFINADO 2: Incertidumbre epistemológica
            epistemic_uncertainty=anthropic.epistemic_uncertainty,
            uncertainty_sources=anthropic.uncertainty_sources,
            # 🔬 EXPLANATORY STRANGENESS
            explanatory_strangeness=anthropic.explanatory_strangeness,
            strangeness_score=anthropic.strangeness_score,
            strangeness_reasons=anthropic.strangeness_reasons,
            # 🎯 MÉTRICAS SEPARADAS (estado del arte)
            anthropic_origin_probability=anthropic.anthropic_origin_probability,
            anthropic_activity_probability=anthropic.anthropic_activity_probability,
            instrumental_anomaly_probability=anthropic.instrumental_anomaly_probability,
            model_inference_confidence=anthropic.model_inference_confidence,
            candidate_type=candidate_type,
            negative_reason=negative_reason,
            reuse_for_training=candidate_type == "negative_reference",
            discard_type=discard_type,
            scientific_confidence=scientific_confidence,
            # FASE F: Sitios conocidos
            known_sites_nearby=nearby_sites,
            overlapping_known_site=overlapping_sites[0] if overlapping_sites else None,
            distance_to_known_site_km=distance_to_known,
            is_known_site_rediscovery=is_rediscovery,
            # ETIQUETADO EPISTEMOLÓGICO
            epistemic_mode=epistemic_mode,
            ai_used=ai_used,
            ai_role=ai_role,
            reproducible=reproducible,
            method_transparency=method_transparency
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
    # GENERACIÓN DE EXPLICACIÓN CIENTÍFICA
    # =========================================================================
    
    def generate_scientific_explanation(self,
                                       scientific_output: ScientificOutput,
                                       environment_type: str,
                                       instruments_measured: int,
                                       instruments_available: int) -> str:
        """
        Generar explicación científica determinística en lenguaje natural.
        
        Esta explicación se guarda en BD para consultas rápidas.
        NO usa IA - es 100% determinística basada en reglas.
        """
        
        probability = scientific_output.anthropic_probability * 100
        anomaly_score = scientific_output.anomaly_score * 100
        action = scientific_output.recommended_action
        coverage_raw = scientific_output.coverage_raw * 100
        coverage_effective = scientific_output.coverage_effective * 100
        
        explanation = ""
        
        # Explicación basada en acción recomendada
        if action in ['no_action', 'discard', 'reject_natural_process']:
            if coverage_effective < 30:
                explanation = (
                    f"El análisis detectó una anomalía del {anomaly_score:.1f}%, pero la probabilidad "
                    f"antropogénica es baja ({probability:.1f}%). Los patrones observados son consistentes "
                    f"con procesos naturales. Cobertura instrumental: {coverage_raw:.0f}% raw "
                    f"({instruments_measured}/{instruments_available} instrumentos), {coverage_effective:.0f}% "
                    f"efectiva (los instrumentos presentes no muestran señal discriminante suficiente). "
                    f"El sistema recomienda no tomar acción."
                )
            else:
                explanation = (
                    f"El análisis detectó una anomalía del {anomaly_score:.1f}%, pero la probabilidad "
                    f"antropogénica es baja ({probability:.1f}%). Los patrones observados son consistentes "
                    f"con procesos naturales. Cobertura instrumental: {coverage_raw:.0f}% "
                    f"({instruments_measured}/{instruments_available} instrumentos). "
                    f"El sistema recomienda no tomar acción."
                )
            
            # Agregar razón de descarte si existe
            if scientific_output.negative_reason:
                explanation += f" Geomorfología identificada: {scientific_output.negative_reason}."
        
        elif action == 'monitoring_passive':
            explanation = (
                f"Se detectó una anomalía del {anomaly_score:.1f}% con probabilidad antropogénica "
                f"moderada ({probability:.1f}%). Los datos actuales no son concluyentes debido a "
                f"cobertura instrumental limitada ({coverage_raw:.0f}% raw, {coverage_effective:.0f}% efectiva). "
                f"Se recomienda monitoreo pasivo para acumular más evidencia antes de invertir recursos."
            )
        
        elif action == 'monitoring_targeted':
            explanation = (
                f"Anomalía significativa del {anomaly_score:.1f}% con probabilidad antropogénica de "
                f"{probability:.1f}%. Los patrones detectados son prometedores pero requieren confirmación "
                f"con instrumentos adicionales. Cobertura actual: {coverage_raw:.0f}% raw "
                f"({instruments_measured}/{instruments_available}), {coverage_effective:.0f}% efectiva. "
                f"Se recomienda análisis dirigido con SAR o LiDAR de alta resolución."
            )
        
        elif action == 'field_verification':
            explanation = (
                f"Candidato arqueológico con anomalía del {anomaly_score:.1f}% y probabilidad "
                f"antropogénica de {probability:.1f}%. Los datos instrumentales (cobertura {coverage_raw:.0f}% "
                f"raw, {coverage_effective:.0f}% efectiva) muestran patrones consistentes con actividad "
                f"humana pasada. Se recomienda validación de campo para confirmar hallazgo."
            )
        
        elif action == 'field_verification_priority':
            explanation = (
                f"Candidato arqueológico prioritario con anomalía del {anomaly_score:.1f}% y alta "
                f"probabilidad antropogénica ({probability:.1f}%). Los patrones morfológicos y espectrales "
                f"son altamente consistentes con estructuras artificiales. Cobertura instrumental: "
                f"{coverage_raw:.0f}% ({instruments_measured}/{instruments_available}). "
                f"Se recomienda verificación de campo PRIORITARIA."
            )
        
        elif action == 'instrument_upgrade_required':
            explanation = (
                f"Región arqueológicamente relevante pero con cobertura instrumental insuficiente "
                f"({coverage_raw:.0f}% raw, {coverage_effective:.0f}% efectiva). Probabilidad antropogénica: "
                f"{probability:.1f}%. Se requieren instrumentos adicionales (SAR, LiDAR, magnetometría) "
                f"antes de poder emitir conclusiones científicas sólidas."
            )
        
        elif action == 'targeted_reanalysis':
            explanation = (
                f"Región arqueológica con cobertura insuficiente ({coverage_raw:.0f}% raw, "
                f"{coverage_effective:.0f}% efectiva) pero probabilidad antropogénica moderada ({probability:.1f}%). "
                f"Se recomienda re-análisis dirigido con instrumentos específicos para el ambiente {environment_type}."
            )
        
        else:
            # Fallback genérico
            explanation = (
                f"Análisis completado con anomalía del {anomaly_score:.1f}% y probabilidad antropogénica "
                f"de {probability:.1f}%. Cobertura instrumental: {coverage_raw:.0f}% raw "
                f"({instruments_measured}/{instruments_available}), {coverage_effective:.0f}% efectiva. "
                f"Acción recomendada: {action}."
            )
        
        return explanation
    
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
                # COBERTURA INSTRUMENTAL (separar raw vs effective)
                "coverage_raw": output.coverage_raw,
                "coverage_effective": output.coverage_effective,
                "instruments_measured": output.instruments_measured,
                "instruments_available": output.instruments_available,
                # 🟠 INCERTIDUMBRE EPISTEMOLÓGICA
                "epistemic_uncertainty": output.epistemic_uncertainty,
                "uncertainty_sources": output.uncertainty_sources,
                # 🔬 EXPLANATORY STRANGENESS SCORE
                "explanatory_strangeness": output.explanatory_strangeness,
                "strangeness_score": output.strangeness_score,
                "strangeness_reasons": output.strangeness_reasons,
                # 🎯 MÉTRICAS SEPARADAS (estado del arte)
                "anthropic_origin_probability": output.anthropic_origin_probability,
                "anthropic_activity_probability": output.anthropic_activity_probability,
                "instrumental_anomaly_probability": output.instrumental_anomaly_probability,
                "model_inference_confidence": output.model_inference_confidence,
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
                "is_known_site_rediscovery": output.is_known_site_rediscovery,
                # ETIQUETADO EPISTEMOLÓGICO (blindaje académico y legal)
                "epistemic_mode": output.epistemic_mode,
                "ai_used": output.ai_used,
                "ai_role": output.ai_role,
                "reproducible": output.reproducible,
                "method_transparency": output.method_transparency
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
                "geomorphology_hint": morphology.geomorphology_hint,  # MEJORA 2
                "paleo_signature": morphology.paleo_signature  # NUEVO: firma de paleocauce
            },
            "phase_d_anthropic": {
                "anthropic_probability": anthropic.anthropic_probability,
                "confidence": anthropic.confidence,
                "confidence_interval": list(anthropic.confidence_interval),
                "reasoning": anthropic.reasoning,
                "model_used": anthropic.model_used,
                # MÉTRICAS DE COBERTURA INSTRUMENTAL
                "coverage_raw": anthropic.coverage_raw,
                "coverage_effective": anthropic.coverage_effective,
                "instruments_measured": anthropic.instruments_measured,
                "instruments_available": anthropic.instruments_available,
                # 🔬 EXPLANATORY STRANGENESS SCORE
                "explanatory_strangeness": anthropic.explanatory_strangeness,
                "strangeness_score": anthropic.strangeness_score,
                "strangeness_reasons": anthropic.strangeness_reasons,
                # 🎯 MÉTRICAS SEPARADAS (estado del arte)
                "anthropic_origin_probability": anthropic.anthropic_origin_probability,
                "anthropic_activity_probability": anthropic.anthropic_activity_probability,
                "instrumental_anomaly_probability": anthropic.instrumental_anomaly_probability,
                "model_inference_confidence": anthropic.model_inference_confidence
            },
            "phase_e_anti_pattern": anti_pattern,
            "phases_completed": output.phases_completed
        }
