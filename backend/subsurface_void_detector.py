#!/usr/bin/env python3
"""
ArcheoScope - Subsurface Void Detector
======================================

Detector CIENTÍFICO de subestructuras huecas usando datos satelitales.

🎯 FILOSOFÍA:
- Un vacío NO se ve directamente
- Se infiere por CONTRADICCIONES FÍSICAS persistentes
- Solo en tierra continental ESTABLE

🔬 MÉTODO CIENTÍFICO:
1. Filtro duro: ¿Tierra estable?
2. Señales SAR + Térmico + Humedad + Micro-hundimiento
3. Score compuesto ponderado
4. Clasificación artificial vs natural
5. Conclusión científica rigurosa

⚠️ NO BUSCAR EN:
- Hielo/glaciares
- Agua
- Sedimentos activos
- Dunas móviles
- Volcanes activos
- Pendientes >15°
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class VoidProbability(Enum):
    """Niveles de probabilidad de vacío"""
    NATURAL = "natural"                    # < 0.4
    AMBIGUOUS = "ambiguous"                # 0.4 - 0.6
    PROBABLE_CAVITY = "probable_cavity"    # 0.6 - 0.75
    STRONG_VOID = "strong_void"            # > 0.75


class VoidClassification(Enum):
    """Clasificación de origen del vacío"""
    ARTIFICIAL_CANDIDATE = "artificial_candidate"
    NATURAL_CAVITY = "natural_cavity"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


@dataclass
class StabilityCheck:
    """Resultado del filtro de estabilidad"""
    is_stable: bool
    surface_type: str
    is_ice: bool
    is_water: bool
    slope_degrees: float
    ndvi_mean: float
    thermal_variance: float
    rejection_reason: Optional[str] = None


@dataclass
class VoidSignals:
    """Señales individuales de vacío"""
    # SAR (35% peso)
    sar_score: float
    sar_low_backscatter: bool
    sar_coherence_drop: bool
    sar_spatial_symmetry: bool
    
    # Térmico (25% peso)
    thermal_score: float
    thermal_night_anomaly: float
    thermal_day_night_decoupling: bool
    thermal_temporal_stable: bool
    
    # Humedad (20% peso)
    humidity_score: float
    humidity_ndvi_low: bool
    humidity_ndvi_stable: bool
    humidity_persistent: bool
    
    # Micro-hundimiento (20% peso)
    subsidence_score: float
    subsidence_depression: bool
    subsidence_symmetric: bool
    subsidence_not_erosion: bool


@dataclass
class VoidDetectionResult:
    """Resultado completo de detección de vacío"""
    # Estabilidad
    stability: StabilityCheck
    
    # Señales
    signals: Optional[VoidSignals]
    
    # Score compuesto
    void_probability_score: float
    void_probability_level: VoidProbability
    
    # Clasificación
    classification: VoidClassification
    
    # Indicadores de artificialidad
    geometric_symmetry: float
    right_angles: bool
    orientation_bias: bool
    modular_repetition: bool
    
    # Conclusión científica
    scientific_conclusion: str
    measurement_confidence: float          # Calidad de datos (sensores)
    epistemic_confidence: float            # Solidez inferencial (convergencia)
    
    # Metadata
    analyzed_at: str
    coordinates: Tuple[float, float]


class SubsurfaceVoidDetector:
    """
    Detector de subestructuras huecas usando datos satelitales.
    
    REGLA DE ORO: Solo analizar en tierra continental ESTABLE.
    """
    
    # Umbrales científicos
    STABILITY_THRESHOLDS = {
        'max_slope_degrees': 15.0,
        'max_ndvi_for_void': 0.25,
        'max_thermal_variance': 5.0,  # °C
    }
    
    VOID_SCORE_THRESHOLDS = {
        'natural': 0.4,
        'ambiguous': 0.6,
        'probable': 0.75,
    }
    
    SIGNAL_WEIGHTS = {
        'sar': 0.35,
        'thermal': 0.25,
        'humidity': 0.20,
        'subsidence': 0.20,
    }
    
    def __init__(self):
        logger.info("SubsurfaceVoidDetector initialized")
    
    def detect_void(
        self,
        lat: float,
        lon: float,
        environment_context: Any,
        satellite_data: Dict[str, Any]
    ) -> VoidDetectionResult:
        """
        Detectar subestructura hueca en coordenadas específicas.
        
        Args:
            lat: Latitud
            lon: Longitud
            environment_context: Contexto ambiental (de environment_classifier)
            satellite_data: Datos satelitales procesados
        
        Returns:
            VoidDetectionResult con análisis completo
        """
        from datetime import datetime
        
        # PASO 1: Filtro duro de estabilidad
        stability = self._check_stability(environment_context, satellite_data)
        
        if not stability.is_stable:
            logger.info(f"❌ Coordenadas {lat:.4f}, {lon:.4f} rechazadas: {stability.rejection_reason}")
            return VoidDetectionResult(
                stability=stability,
                signals=None,
                void_probability_score=0.0,
                void_probability_level=VoidProbability.NATURAL,
                classification=VoidClassification.NOT_APPLICABLE,
                geometric_symmetry=0.0,
                right_angles=False,
                orientation_bias=False,
                modular_repetition=False,
                scientific_conclusion=f"Análisis no aplicable: {stability.rejection_reason}",
                measurement_confidence=0.0,
                epistemic_confidence=0.0,
                analyzed_at=datetime.utcnow().isoformat(),
                coordinates=(lat, lon)
            )
        
        logger.info(f"✅ Coordenadas {lat:.4f}, {lon:.4f} pasan filtro de estabilidad")
        
        # PASO 2: Analizar señales de vacío
        signals = self._analyze_void_signals(satellite_data)
        
        # PASO 3: Calcular score compuesto
        void_score = self._calculate_void_probability(signals)
        void_level = self._classify_void_probability(void_score)
        
        # PASO 4: Clasificar artificial vs natural
        classification, symmetry, right_angles, orientation, modular = \
            self._classify_void_origin(signals, satellite_data)
        
        # PASO 5: Generar conclusión científica
        conclusion = self._generate_scientific_conclusion(
            stability, signals, void_score, classification
        )
        
        # PASO 6: Calcular confianza (separada en medida y epistémica)
        measurement_conf, epistemic_conf = self._calculate_confidence_metrics(signals, satellite_data)
        
        return VoidDetectionResult(
            stability=stability,
            signals=signals,
            void_probability_score=void_score,
            void_probability_level=void_level,
            classification=classification,
            geometric_symmetry=symmetry,
            right_angles=right_angles,
            orientation_bias=orientation,
            modular_repetition=modular,
            scientific_conclusion=conclusion,
            measurement_confidence=measurement_conf,
            epistemic_confidence=epistemic_conf,
            analyzed_at=datetime.utcnow().isoformat(),
            coordinates=(lat, lon)
        )
    
    def _check_stability(
        self,
        environment_context: Any,
        satellite_data: Dict[str, Any]
    ) -> StabilityCheck:
        """
        FILTRO DURO: Verificar si es tierra continental estable.
        
        Rechazar:
        - Hielo/glaciares
        - Agua
        - Sedimentos activos
        - Dunas móviles
        - Volcanes activos
        - Pendientes >15°
        """
        from .environment_classifier import EnvironmentType
        
        env_type = environment_context.environment_type
        
        # Verificar tipo de superficie
        is_ice = env_type in [
            EnvironmentType.POLAR_ICE,
            EnvironmentType.GLACIER,
            EnvironmentType.PERMAFROST
        ]
        
        is_water = env_type in [
            EnvironmentType.DEEP_OCEAN,
            EnvironmentType.SHALLOW_SEA,
            EnvironmentType.COASTAL,
            EnvironmentType.LAKE,
            EnvironmentType.RIVER
        ]
        
        surface_type = "land" if not (is_ice or is_water) else "non_land"
        
        # Extraer métricas
        slope = satellite_data.get('slope_degrees', 0.0)
        ndvi_mean = satellite_data.get('ndvi_mean', 0.0)
        thermal_variance = satellite_data.get('thermal_variance', 0.0)
        
        # Aplicar filtros
        rejection_reason = None
        
        if is_ice:
            rejection_reason = "Superficie de hielo/glaciar (no estable)"
        elif is_water:
            rejection_reason = "Cuerpo de agua (no aplicable)"
        elif slope > self.STABILITY_THRESHOLDS['max_slope_degrees']:
            rejection_reason = f"Pendiente {slope:.1f}° > {self.STABILITY_THRESHOLDS['max_slope_degrees']}° (ladera inestable)"
        elif ndvi_mean > self.STABILITY_THRESHOLDS['max_ndvi_for_void']:
            rejection_reason = f"NDVI {ndvi_mean:.2f} > {self.STABILITY_THRESHOLDS['max_ndvi_for_void']} (vegetación densa)"
        elif thermal_variance > self.STABILITY_THRESHOLDS['max_thermal_variance']:
            rejection_reason = f"Varianza térmica {thermal_variance:.1f}°C (actividad volcánica posible)"
        
        is_stable = rejection_reason is None
        
        return StabilityCheck(
            is_stable=is_stable,
            surface_type=surface_type,
            is_ice=is_ice,
            is_water=is_water,
            slope_degrees=slope,
            ndvi_mean=ndvi_mean,
            thermal_variance=thermal_variance,
            rejection_reason=rejection_reason
        )
    
    def _analyze_void_signals(self, satellite_data: Dict[str, Any]) -> VoidSignals:
        """
        Analizar señales individuales de vacío.
        
        A. SAR: Pérdida de coherencia + baja retrodispersión
        B. Térmico: Enfriamiento nocturno + desacople día/noche
        C. Humedad: NDVI bajo pero estable
        D. Micro-hundimiento: Depresión simétrica
        """
        # A. SAR (35% peso)
        sar_backscatter = satellite_data.get('sar_backscatter_db', 0.0)
        sar_coherence = satellite_data.get('sar_coherence', 1.0)
        sar_symmetry = satellite_data.get('sar_spatial_symmetry', 0.0)
        
        sar_low_backscatter = sar_backscatter < -15.0  # dB
        sar_coherence_drop = sar_coherence < 0.5
        sar_spatial_symmetry = sar_symmetry > 0.6
        
        sar_score = 0.0
        if sar_low_backscatter:
            sar_score += 0.4
        if sar_coherence_drop:
            sar_score += 0.4
        if sar_spatial_symmetry:
            sar_score += 0.2
        
        # B. Térmico (25% peso)
        lst_night = satellite_data.get('lst_night_celsius', 20.0)
        lst_day = satellite_data.get('lst_day_celsius', 30.0)
        expected_night_temp = satellite_data.get('expected_night_temp', 20.0)
        thermal_temporal_variance = satellite_data.get('thermal_temporal_variance', 0.0)
        
        thermal_night_anomaly = expected_night_temp - lst_night
        thermal_day_night_decoupling = abs(lst_day - lst_night) < 5.0  # Menor rango = menor inercia
        thermal_temporal_stable = thermal_temporal_variance < 2.0
        
        thermal_score = 0.0
        if thermal_night_anomaly > 2.0:  # Más frío de noche
            thermal_score += 0.5
        if thermal_day_night_decoupling:
            thermal_score += 0.3
        if thermal_temporal_stable:
            thermal_score += 0.2
        
        # C. Humedad (20% peso)
        ndvi_mean = satellite_data.get('ndvi_mean', 0.0)
        ndvi_variance = satellite_data.get('ndvi_variance', 0.0)
        ndvi_temporal_stability = satellite_data.get('ndvi_temporal_stability', 0.0)
        
        humidity_ndvi_low = ndvi_mean < 0.2
        humidity_ndvi_stable = ndvi_variance < 0.05
        humidity_persistent = ndvi_temporal_stability > 0.7
        
        humidity_score = 0.0
        if humidity_ndvi_low:
            humidity_score += 0.4
        if humidity_ndvi_stable:
            humidity_score += 0.3
        if humidity_persistent:
            humidity_score += 0.3
        
        # D. Micro-hundimiento (20% peso)
        elevation_anomaly = satellite_data.get('elevation_anomaly', 0.0)
        depression_symmetry = satellite_data.get('depression_symmetry', 0.0)
        erosion_likelihood = satellite_data.get('erosion_likelihood', 0.5)
        
        subsidence_depression = elevation_anomaly < -0.5  # metros
        subsidence_symmetric = depression_symmetry > 0.6
        subsidence_not_erosion = erosion_likelihood < 0.3
        
        subsidence_score = 0.0
        if subsidence_depression:
            subsidence_score += 0.4
        if subsidence_symmetric:
            subsidence_score += 0.4
        if subsidence_not_erosion:
            subsidence_score += 0.2
        
        return VoidSignals(
            sar_score=sar_score,
            sar_low_backscatter=sar_low_backscatter,
            sar_coherence_drop=sar_coherence_drop,
            sar_spatial_symmetry=sar_spatial_symmetry,
            thermal_score=thermal_score,
            thermal_night_anomaly=thermal_night_anomaly,
            thermal_day_night_decoupling=thermal_day_night_decoupling,
            thermal_temporal_stable=thermal_temporal_stable,
            humidity_score=humidity_score,
            humidity_ndvi_low=humidity_ndvi_low,
            humidity_ndvi_stable=humidity_ndvi_stable,
            humidity_persistent=humidity_persistent,
            subsidence_score=subsidence_score,
            subsidence_depression=subsidence_depression,
            subsidence_symmetric=subsidence_symmetric,
            subsidence_not_erosion=subsidence_not_erosion
        )
    
    def _calculate_void_probability(self, signals: VoidSignals) -> float:
        """
        Calcular score compuesto de probabilidad de vacío.
        
        void_probability = weighted_sum({
            "sar": 0.35,
            "thermal": 0.25,
            "humidity": 0.20,
            "subsidence": 0.20
        })
        """
        void_score = (
            signals.sar_score * self.SIGNAL_WEIGHTS['sar'] +
            signals.thermal_score * self.SIGNAL_WEIGHTS['thermal'] +
            signals.humidity_score * self.SIGNAL_WEIGHTS['humidity'] +
            signals.subsidence_score * self.SIGNAL_WEIGHTS['subsidence']
        )
        
        return float(np.clip(void_score, 0.0, 1.0))
    
    def _classify_void_probability(self, score: float) -> VoidProbability:
        """
        Clasificar nivel de probabilidad de vacío.
        
        < 0.4: Natural
        0.4 - 0.6: Ambiguo
        0.6 - 0.75: Cavidad probable
        > 0.75: Subestructura hueca fuerte
        """
        if score < self.VOID_SCORE_THRESHOLDS['natural']:
            return VoidProbability.NATURAL
        elif score < self.VOID_SCORE_THRESHOLDS['ambiguous']:
            return VoidProbability.AMBIGUOUS
        elif score < self.VOID_SCORE_THRESHOLDS['probable']:
            return VoidProbability.PROBABLE_CAVITY
        else:
            return VoidProbability.STRONG_VOID
    
    def _classify_void_origin(
        self,
        signals: VoidSignals,
        satellite_data: Dict[str, Any]
    ) -> Tuple[VoidClassification, float, bool, bool, bool]:
        """
        Clasificar si el vacío es artificial o natural.
        
        Indicadores de artificialidad:
        - Simetría geométrica
        - Ángulos rectos
        - Orientación no geomorfológica
        - Repetición modular
        """
        # Extraer indicadores geométricos
        symmetry = satellite_data.get('geometric_symmetry', 0.0)
        has_right_angles = satellite_data.get('right_angles_detected', False)
        orientation_bias = satellite_data.get('orientation_bias', 0.0) > 0.6
        modular_repetition = satellite_data.get('modular_repetition', False)
        
        # Clasificar
        if symmetry > 0.7 and (has_right_angles or orientation_bias):
            classification = VoidClassification.ARTIFICIAL_CANDIDATE
        elif symmetry < 0.3:
            classification = VoidClassification.NATURAL_CAVITY
        else:
            classification = VoidClassification.UNKNOWN
        
        return classification, symmetry, has_right_angles, orientation_bias, modular_repetition
    
    def _generate_scientific_conclusion(
        self,
        stability: StabilityCheck,
        signals: VoidSignals,
        void_score: float,
        classification: VoidClassification
    ) -> str:
        """
        Generar conclusión científica rigurosa y defendible.
        """
        if not stability.is_stable:
            return f"Análisis no aplicable: {stability.rejection_reason}"
        
        # Construir conclusión basada en señales detectadas
        detected_signals = []
        
        if signals.sar_coherence_drop:
            detected_signals.append("pérdida persistente de coherencia SAR")
        
        if signals.thermal_night_anomaly > 2.0:
            detected_signals.append("anomalía térmica nocturna desacoplada de la topografía")
        
        if signals.humidity_persistent:
            detected_signals.append("humedad sub-superficial estable")
        
        if signals.subsidence_symmetric:
            detected_signals.append("micro-hundimiento simétrico")
        
        if not detected_signals:
            return "No se detectaron señales significativas de subestructura hueca."
        
        signals_text = ", ".join(detected_signals)
        
        # Interpretación según score
        if void_score > 0.75:
            interpretation = "consistentes con la presencia de una subestructura hueca"
        elif void_score > 0.6:
            interpretation = "sugieren la posible presencia de una cavidad subsuperficial"
        elif void_score > 0.4:
            interpretation = "presentan características ambiguas que requieren validación adicional"
        else:
            interpretation = "no son suficientes para inferir una estructura hueca"
        
        # Clasificación artificial/natural
        if classification == VoidClassification.ARTIFICIAL_CANDIDATE:
            origin_note = " La geometría regular y orientación sugieren posible origen antrópico."
        elif classification == VoidClassification.NATURAL_CAVITY:
            origin_note = " Las características geométricas son consistentes con formación natural."
        else:
            origin_note = ""
        
        conclusion = (
            f"La región analizada presenta {signals_text}. "
            f"Estos indicadores combinados {interpretation} "
            f"en terreno continental estable.{origin_note}"
        )
        
        return conclusion
    
    def _calculate_confidence_metrics(
        self,
        signals: VoidSignals,
        satellite_data: Dict[str, Any]
    ) -> Tuple[float, float]:
        """
        Calcular métricas de confianza.
        
        Returns:
            (measurement_confidence, epistemic_confidence)
        """
        # 1. Measurement Confidence (Calidad de datos de sensores)
        # Basado en la calidad reportada por los conectores
        measurement_confidence = satellite_data.get('data_quality_score', 0.7)
        
        # 2. Epistemic Confidence (Solidez de la inferencia)
        # Basado en la convergencia de señales independientes
        signal_count = sum([
            signals.sar_coherence_drop,
            signals.thermal_night_anomaly > 2.0,
            signals.humidity_persistent,
            signals.subsidence_symmetric
        ])
        
        # Convergencia: cuantas más señales coincidan, más sólida es la inferencia
        epistemic_confidence = min(signal_count / 4.0, 1.0)
        
        return (
            float(np.clip(measurement_confidence, 0.0, 1.0)),
            float(np.clip(epistemic_confidence, 0.0, 1.0))
        )


# Instancia global
subsurface_void_detector = SubsurfaceVoidDetector()
