"""
ArcheoScope - Reglas Arqueológicas Avanzadas
Implementación de firmas temporales, índices no estándar y filtros anti-modernos
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class AdvancedArchaeologicalResult(Enum):
    """Resultados de análisis arqueológico avanzado"""
    ARCHAEOLOGICAL_TEMPORAL = "archaeological_temporal"
    ARCHAEOLOGICAL_SPECTRAL = "archaeological_spectral"
    MODERN_ANTHROPOGENIC = "modern_anthropogenic"
    NATURAL_PROCESS = "natural_process"
    INCONCLUSIVE = "inconclusive"

@dataclass
class TemporalSignature:
    """Firma temporal arqueológica"""
    ndvi_temporal_lag: float
    thermal_phase_shift: float
    sar_seasonal_stability: float
    moisture_response_delay: float
    temporal_coherence_score: float

@dataclass
class NonStandardIndices:
    """Índices espectrales no estándar"""
    ndre_stress: float  # Red Edge stress
    msi_anomaly: float  # Moisture Stress Index anomaly
    intra_pixel_variability: float
    spectral_heterogeneity: float
    vegetation_stress_differential: float

@dataclass
class ModernAnthropogenicFilter:
    """Filtro para estructuras modernas"""
    agricultural_drainage_probability: float
    power_line_probability: float
    modern_road_probability: float
    recent_terrace_probability: float
    cadastral_alignment_score: float

class AdvancedArchaeologicalRulesEngine:
    """Motor de reglas arqueológicas avanzadas"""
    
    def __init__(self):
        self.temporal_thresholds = {
            'ndvi_lag_min': 0.15,  # Retraso mínimo en respuesta NDVI
            'thermal_phase_min': 0.2,  # Desfase térmico mínimo
            'sar_stability_min': 0.8,  # Estabilidad SAR mínima
            'moisture_delay_min': 0.1,  # Retraso en respuesta a humedad
            'temporal_coherence_min': 0.6  # Coherencia temporal mínima
        }
        
        self.spectral_thresholds = {
            'ndre_stress_min': 0.1,  # Estrés Red Edge mínimo
            'msi_anomaly_min': 0.15,  # Anomalía MSI mínima
            'variability_max': 0.3,  # Variabilidad intra-píxel máxima
            'heterogeneity_min': 0.2,  # Heterogeneidad mínima
            'stress_differential_min': 0.1  # Diferencial de estrés mínimo
        }
        
        self.modern_filter_thresholds = {
            'agricultural_max': 0.3,  # Probabilidad agrícola máxima
            'power_line_max': 0.2,  # Probabilidad línea eléctrica máxima
            'modern_road_max': 0.25,  # Probabilidad camino moderno máxima
            'recent_terrace_max': 0.2,  # Probabilidad terraza reciente máxima
            'cadastral_alignment_max': 0.4  # Alineación catastral máxima
        }

    def analyze_temporal_archaeological_signature(self, 
                                                spectral_data: Dict[str, np.ndarray],
                                                temporal_series: Dict[str, List[float]]) -> TemporalSignature:
        """
        Analiza la firma temporal arqueológica
        
        Detecta:
        - Desfase sistemático en respuestas espectrales
        - Amortiguación anómala de señales estacionales
        - Respuestas retardadas a eventos climáticos
        - Inercia temporal característica de estructuras enterradas
        """
        try:
            # 1. Análisis de retraso en respuesta NDVI
            ndvi_series = temporal_series.get('ndvi', [])
            ndvi_temporal_lag = self._calculate_temporal_lag(ndvi_series)
            
            # 2. Análisis de desfase térmico día/noche
            thermal_series = temporal_series.get('thermal', [])
            thermal_phase_shift = self._calculate_thermal_phase_shift(thermal_series)
            
            # 3. Estabilidad SAR estacional
            sar_series = temporal_series.get('sar', [])
            sar_seasonal_stability = self._calculate_sar_stability(sar_series)
            
            # 4. Retraso en respuesta a humedad
            moisture_response_delay = self._calculate_moisture_response_delay(
                ndvi_series, temporal_series.get('precipitation', [])
            )
            
            # 5. Score de coherencia temporal integrado
            temporal_coherence_score = self._calculate_temporal_coherence(
                ndvi_temporal_lag, thermal_phase_shift, sar_seasonal_stability
            )
            
            return TemporalSignature(
                ndvi_temporal_lag=ndvi_temporal_lag,
                thermal_phase_shift=thermal_phase_shift,
                sar_seasonal_stability=sar_seasonal_stability,
                moisture_response_delay=moisture_response_delay,
                temporal_coherence_score=temporal_coherence_score
            )
            
        except Exception as e:
            logger.error(f"Error en análisis de firma temporal: {e}")
            return TemporalSignature(0.0, 0.0, 0.0, 0.0, 0.0)

    def analyze_non_standard_vegetation_indices(self, 
                                              spectral_data: Dict[str, np.ndarray]) -> NonStandardIndices:
        """
        Calcula índices espectrales no estándar para detectar estrés vegetal diferencial
        
        Detecta:
        - Estrés vegetal localizado dentro de parcelas homogéneas
        - Heterogeneidad vegetal no explicable por topografía
        - Variabilidad intra-píxel característica de estructuras enterradas
        """
        try:
            # Extraer bandas espectrales
            red = spectral_data.get('red', np.zeros((100, 100)))
            nir = spectral_data.get('nir', np.zeros((100, 100)))
            red_edge = spectral_data.get('red_edge', np.zeros((100, 100)))
            swir = spectral_data.get('swir', np.zeros((100, 100)))
            
            # 1. NDRE (Normalized Difference Red Edge) - Estrés vegetal sutil
            ndre = (nir - red_edge) / (nir + red_edge + 1e-10)
            ndre_stress = self._calculate_stress_anomaly(ndre)
            
            # 2. MSI (Moisture Stress Index) - Estrés hídrico
            msi = swir / (nir + 1e-10)  # Evitar división por cero
            msi_anomaly = self._calculate_moisture_anomaly(msi)
            
            # 3. Variabilidad intra-píxel
            intra_pixel_variability = self._calculate_intra_pixel_variability(
                red, nir, red_edge
            )
            
            # 4. Heterogeneidad espectral
            spectral_heterogeneity = self._calculate_spectral_heterogeneity(
                spectral_data
            )
            
            # 5. Diferencial de estrés vegetal
            vegetation_stress_differential = self._calculate_stress_differential(
                ndre_stress, msi_anomaly
            )
            
            return NonStandardIndices(
                ndre_stress=ndre_stress,
                msi_anomaly=msi_anomaly,
                intra_pixel_variability=intra_pixel_variability,
                spectral_heterogeneity=spectral_heterogeneity,
                vegetation_stress_differential=vegetation_stress_differential
            )
            
        except Exception as e:
            logger.error(f"Error en análisis de índices no estándar: {e}")
            return NonStandardIndices(0.0, 0.0, 0.0, 0.0, 0.0)

    def apply_modern_anthropogenic_filter(self, 
                                        spectral_data: Dict[str, np.ndarray],
                                        geometric_features: Dict[str, float]) -> ModernAnthropogenicFilter:
        """
        Filtra estructuras antropogénicas modernas
        
        Detecta y excluye:
        - Drenajes agrícolas
        - Líneas eléctricas
        - Caminos modernos
        - Terrazas recientes
        - Alineaciones catastrales
        """
        try:
            # 1. Probabilidad de drenaje agrícola
            agricultural_drainage_probability = self._detect_agricultural_drainage(
                spectral_data, geometric_features
            )
            
            # 2. Probabilidad de línea eléctrica
            power_line_probability = self._detect_power_lines(
                geometric_features
            )
            
            # 3. Probabilidad de camino moderno
            modern_road_probability = self._detect_modern_roads(
                spectral_data, geometric_features
            )
            
            # 4. Probabilidad de terraza reciente
            recent_terrace_probability = self._detect_recent_terraces(
                spectral_data
            )
            
            # 5. Score de alineación catastral
            cadastral_alignment_score = self._calculate_cadastral_alignment(
                geometric_features
            )
            
            return ModernAnthropogenicFilter(
                agricultural_drainage_probability=agricultural_drainage_probability,
                power_line_probability=power_line_probability,
                modern_road_probability=modern_road_probability,
                recent_terrace_probability=recent_terrace_probability,
                cadastral_alignment_score=cadastral_alignment_score
            )
            
        except Exception as e:
            logger.error(f"Error en filtro antropogénico moderno: {e}")
            return ModernAnthropogenicFilter(0.0, 0.0, 0.0, 0.0, 0.0)

    def evaluate_advanced_archaeological_potential(self,
                                                 temporal_signature: TemporalSignature,
                                                 non_standard_indices: NonStandardIndices,
                                                 modern_filter: ModernAnthropogenicFilter) -> Dict:
        """
        Evalúa el potencial arqueológico usando análisis avanzados
        """
        try:
            # 1. Evaluar firma temporal arqueológica
            temporal_score = self._evaluate_temporal_signature(temporal_signature)
            
            # 2. Evaluar índices espectrales no estándar
            spectral_score = self._evaluate_non_standard_indices(non_standard_indices)
            
            # 3. Aplicar filtro anti-moderno
            modern_exclusion_score = self._evaluate_modern_filter(modern_filter)
            
            # 4. Score integrado con pesos explicables
            integrated_score = self._calculate_integrated_advanced_score(
                temporal_score, spectral_score, modern_exclusion_score
            )
            
            # 5. Clasificación final
            classification = self._classify_advanced_result(integrated_score, modern_exclusion_score)
            
            return {
                'temporal_archaeological_signature': {
                    'score': temporal_score,
                    'ndvi_lag': temporal_signature.ndvi_temporal_lag,
                    'thermal_phase': temporal_signature.thermal_phase_shift,
                    'sar_stability': temporal_signature.sar_seasonal_stability,
                    'coherence': temporal_signature.temporal_coherence_score
                },
                'non_standard_spectral_analysis': {
                    'score': spectral_score,
                    'ndre_stress': non_standard_indices.ndre_stress,
                    'msi_anomaly': non_standard_indices.msi_anomaly,
                    'heterogeneity': non_standard_indices.spectral_heterogeneity,
                    'stress_differential': non_standard_indices.vegetation_stress_differential
                },
                'modern_anthropogenic_filter': {
                    'exclusion_score': modern_exclusion_score,
                    'agricultural_probability': modern_filter.agricultural_drainage_probability,
                    'power_line_probability': modern_filter.power_line_probability,
                    'modern_road_probability': modern_filter.modern_road_probability,
                    'cadastral_alignment': modern_filter.cadastral_alignment_score
                },
                'integrated_advanced_analysis': {
                    'score': integrated_score,
                    'classification': classification,
                    'confidence_level': self._calculate_confidence_level(integrated_score),
                    'explanation': self._generate_explanation(
                        temporal_score, spectral_score, modern_exclusion_score
                    )
                }
            }
            
        except Exception as e:
            logger.error(f"Error en evaluación arqueológica avanzada: {e}")
            return {'error': str(e)}

    # Métodos auxiliares para cálculos específicos
    
    def _calculate_temporal_lag(self, ndvi_series: List[float]) -> float:
        """Calcula el retraso temporal en respuesta NDVI"""
        if len(ndvi_series) < 12:  # Mínimo 1 año de datos
            return 0.0
        
        # Simular análisis de autocorrelación temporal
        # En implementación real: análisis de Fourier, autocorrelación
        temporal_variance = np.var(ndvi_series)
        seasonal_amplitude = np.ptp(ndvi_series)  # Peak-to-peak
        
        # Estructuras enterradas amortiguan variaciones estacionales
        lag_indicator = 1.0 - (temporal_variance / (seasonal_amplitude + 1e-10))
        return max(0.0, min(1.0, lag_indicator))

    def _calculate_thermal_phase_shift(self, thermal_series: List[float]) -> float:
        """Calcula el desfase térmico día/noche"""
        if len(thermal_series) < 24:  # Mínimo datos diarios
            return 0.0
        
        # Simular análisis de fase térmica
        thermal_range = np.ptp(thermal_series)
        thermal_std = np.std(thermal_series)
        
        # Estructuras con masa térmica tienen desfase característico
        phase_shift = thermal_std / (thermal_range + 1e-10)
        return max(0.0, min(1.0, phase_shift))

    def _calculate_sar_stability(self, sar_series: List[float]) -> float:
        """Calcula la estabilidad SAR estacional"""
        if len(sar_series) < 12:
            return 0.0
        
        # Estructuras rígidas tienen alta estabilidad SAR
        sar_stability = 1.0 - (np.std(sar_series) / (np.mean(sar_series) + 1e-10))
        return max(0.0, min(1.0, sar_stability))

    def _calculate_moisture_response_delay(self, ndvi_series: List[float], 
                                         precipitation_series: List[float]) -> float:
        """Calcula el retraso en respuesta a eventos de humedad"""
        if len(ndvi_series) != len(precipitation_series) or len(ndvi_series) < 12:
            return 0.0
        
        # Simular análisis de correlación cruzada
        # Estructuras enterradas retrasan respuesta vegetal a lluvia
        correlation = np.corrcoef(ndvi_series, precipitation_series)[0, 1]
        delay_indicator = 1.0 - abs(correlation)  # Menor correlación = mayor retraso
        return max(0.0, min(1.0, delay_indicator))

    def _calculate_temporal_coherence(self, ndvi_lag: float, thermal_phase: float, 
                                    sar_stability: float) -> float:
        """Calcula coherencia temporal integrada"""
        return (ndvi_lag + thermal_phase + sar_stability) / 3.0

    def _calculate_stress_anomaly(self, ndre: np.ndarray) -> float:
        """Calcula anomalía de estrés vegetal usando NDRE"""
        ndre_mean = np.mean(ndre)
        ndre_std = np.std(ndre)
        
        # Detectar estrés localizado (valores bajos de NDRE)
        stress_threshold = ndre_mean - ndre_std
        stress_pixels = np.sum(ndre < stress_threshold)
        stress_ratio = stress_pixels / ndre.size
        
        return min(1.0, stress_ratio * 2.0)  # Normalizar

    def _calculate_moisture_anomaly(self, msi: np.ndarray) -> float:
        """Calcula anomalía de estrés hídrico usando MSI"""
        msi_mean = np.mean(msi)
        msi_std = np.std(msi)
        
        # Detectar estrés hídrico (valores altos de MSI)
        stress_threshold = msi_mean + msi_std
        stress_pixels = np.sum(msi > stress_threshold)
        stress_ratio = stress_pixels / msi.size
        
        return min(1.0, stress_ratio * 2.0)

    def _calculate_intra_pixel_variability(self, red: np.ndarray, 
                                         nir: np.ndarray, red_edge: np.ndarray) -> float:
        """Calcula variabilidad intra-píxel"""
        # Usar ventana deslizante para analizar variabilidad local
        variability_scores = []
        
        for i in range(1, red.shape[0]-1):
            for j in range(1, red.shape[1]-1):
                # Ventana 3x3
                window_red = red[i-1:i+2, j-1:j+2]
                window_nir = nir[i-1:i+2, j-1:j+2]
                window_re = red_edge[i-1:i+2, j-1:j+2]
                
                # Calcular variabilidad como CV (coeficiente de variación)
                cv_red = np.std(window_red) / (np.mean(window_red) + 1e-10)
                cv_nir = np.std(window_nir) / (np.mean(window_nir) + 1e-10)
                cv_re = np.std(window_re) / (np.mean(window_re) + 1e-10)
                
                variability_scores.append((cv_red + cv_nir + cv_re) / 3.0)
        
        return np.mean(variability_scores) if variability_scores else 0.0

    def _calculate_spectral_heterogeneity(self, spectral_data: Dict[str, np.ndarray]) -> float:
        """Calcula heterogeneidad espectral general"""
        heterogeneity_scores = []
        
        for band_name, band_data in spectral_data.items():
            if band_data.size > 0:
                band_cv = np.std(band_data) / (np.mean(band_data) + 1e-10)
                heterogeneity_scores.append(band_cv)
        
        return np.mean(heterogeneity_scores) if heterogeneity_scores else 0.0

    def _calculate_stress_differential(self, ndre_stress: float, msi_anomaly: float) -> float:
        """Calcula diferencial de estrés vegetal"""
        return abs(ndre_stress - msi_anomaly)

    def _detect_agricultural_drainage(self, spectral_data: Dict[str, np.ndarray], 
                                    geometric_features: Dict[str, float]) -> float:
        """Detecta patrones de drenaje agrícola"""
        # Características típicas de drenajes agrícolas:
        # - Líneas rectas muy regulares
        # - Espaciado uniforme
        # - Alineación con parcelas catastrales
        
        linearity = geometric_features.get('linearity', 0.0)
        regularity = geometric_features.get('regularity', 0.0)
        
        # Drenajes son muy lineales y regulares
        agricultural_score = (linearity + regularity) / 2.0
        
        # Si es demasiado perfecto, probablemente es moderno
        if agricultural_score > 0.9:
            return 0.8  # Alta probabilidad de ser drenaje agrícola
        
        return agricultural_score * 0.5

    def _detect_power_lines(self, geometric_features: Dict[str, float]) -> float:
        """Detecta líneas eléctricas"""
        # Características de líneas eléctricas:
        # - Perfectamente rectas
        # - Muy largas
        # - Ancho constante muy estrecho
        
        linearity = geometric_features.get('linearity', 0.0)
        length = geometric_features.get('length_m', 0.0)
        width = geometric_features.get('width_m', 0.0)
        
        # Líneas eléctricas: muy lineales, largas y estrechas
        if linearity > 0.95 and length > 1000 and width < 10:
            return 0.9  # Muy probable línea eléctrica
        
        return 0.0

    def _detect_modern_roads(self, spectral_data: Dict[str, np.ndarray], 
                           geometric_features: Dict[str, float]) -> float:
        """Detecta caminos modernos"""
        # Características de caminos modernos:
        # - Superficie asfáltica (baja reflectancia)
        # - Ancho estándar (3-12m)
        # - Muy lineales
        
        linearity = geometric_features.get('linearity', 0.0)
        width = geometric_features.get('width_m', 0.0)
        
        # Reflectancia promedio (asfalto tiene baja reflectancia)
        if 'red' in spectral_data:
            avg_reflectance = np.mean(spectral_data['red'])
        else:
            avg_reflectance = 0.5
        
        # Caminos modernos: lineales, ancho estándar, baja reflectancia
        if linearity > 0.8 and 3 <= width <= 12 and avg_reflectance < 0.3:
            return 0.7  # Probable camino moderno
        
        return 0.0

    def _detect_recent_terraces(self, spectral_data: Dict[str, np.ndarray]) -> float:
        """Detecta terrazas agrícolas recientes"""
        # Terrazas recientes tienen vegetación muy homogénea
        if 'nir' in spectral_data and 'red' in spectral_data:
            ndvi = (spectral_data['nir'] - spectral_data['red']) / \
                   (spectral_data['nir'] + spectral_data['red'] + 1e-10)
            
            ndvi_std = np.std(ndvi)
            
            # Terrazas recientes: NDVI muy homogéneo
            if ndvi_std < 0.05:  # Muy poca variabilidad
                return 0.6
        
        return 0.0

    def _calculate_cadastral_alignment(self, geometric_features: Dict[str, float]) -> float:
        """Calcula alineación con catastro moderno"""
        # Simular alineación con parcelas catastrales
        # En implementación real: comparar con datos catastrales
        
        orientation = geometric_features.get('orientation_degrees', 0.0)
        
        # Orientaciones típicas catastrales: N-S (0°), E-W (90°)
        cadastral_orientations = [0, 45, 90, 135, 180]
        
        min_deviation = min(abs(orientation - co) for co in cadastral_orientations)
        
        # Si está muy alineado con catastro, probable estructura moderna
        if min_deviation < 5:  # Menos de 5° de desviación
            return 0.8
        elif min_deviation < 15:
            return 0.4
        
        return 0.1

    def _evaluate_temporal_signature(self, temporal_signature: TemporalSignature) -> float:
        """Evalúa la firma temporal arqueológica"""
        score = 0.0
        
        if temporal_signature.ndvi_temporal_lag > self.temporal_thresholds['ndvi_lag_min']:
            score += 0.25
        
        if temporal_signature.thermal_phase_shift > self.temporal_thresholds['thermal_phase_min']:
            score += 0.25
        
        if temporal_signature.sar_seasonal_stability > self.temporal_thresholds['sar_stability_min']:
            score += 0.25
        
        if temporal_signature.temporal_coherence_score > self.temporal_thresholds['temporal_coherence_min']:
            score += 0.25
        
        return score

    def _evaluate_non_standard_indices(self, non_standard_indices: NonStandardIndices) -> float:
        """Evalúa los índices espectrales no estándar"""
        score = 0.0
        
        if non_standard_indices.ndre_stress > self.spectral_thresholds['ndre_stress_min']:
            score += 0.3
        
        if non_standard_indices.msi_anomaly > self.spectral_thresholds['msi_anomaly_min']:
            score += 0.3
        
        if non_standard_indices.spectral_heterogeneity > self.spectral_thresholds['heterogeneity_min']:
            score += 0.2
        
        if non_standard_indices.vegetation_stress_differential > self.spectral_thresholds['stress_differential_min']:
            score += 0.2
        
        return score

    def _evaluate_modern_filter(self, modern_filter: ModernAnthropogenicFilter) -> float:
        """Evalúa el filtro de estructuras modernas (score alto = probable moderno)"""
        modern_score = 0.0
        
        if modern_filter.agricultural_drainage_probability > self.modern_filter_thresholds['agricultural_max']:
            modern_score += 0.3
        
        if modern_filter.power_line_probability > self.modern_filter_thresholds['power_line_max']:
            modern_score += 0.3
        
        if modern_filter.modern_road_probability > self.modern_filter_thresholds['modern_road_max']:
            modern_score += 0.2
        
        if modern_filter.cadastral_alignment_score > self.modern_filter_thresholds['cadastral_alignment_max']:
            modern_score += 0.2
        
        return modern_score

    def _calculate_integrated_advanced_score(self, temporal_score: float, 
                                           spectral_score: float, 
                                           modern_exclusion_score: float) -> float:
        """Calcula score integrado con pesos explicables"""
        # Pesos bayesianos ligeros
        temporal_weight = 0.4  # Firma temporal es muy diagnóstica
        spectral_weight = 0.4  # Índices no estándar son clave
        modern_penalty = 0.8   # Penalización fuerte por ser moderno
        
        base_score = (temporal_score * temporal_weight + 
                     spectral_score * spectral_weight)
        
        # Aplicar penalización por estructuras modernas
        final_score = base_score * (1.0 - modern_exclusion_score * modern_penalty)
        
        return max(0.0, min(1.0, final_score))

    def _classify_advanced_result(self, integrated_score: float, 
                                modern_exclusion_score: float) -> AdvancedArchaeologicalResult:
        """Clasifica el resultado del análisis avanzado"""
        if modern_exclusion_score > 0.6:
            return AdvancedArchaeologicalResult.MODERN_ANTHROPOGENIC
        elif integrated_score > 0.7:
            return AdvancedArchaeologicalResult.ARCHAEOLOGICAL_TEMPORAL
        elif integrated_score > 0.5:
            return AdvancedArchaeologicalResult.ARCHAEOLOGICAL_SPECTRAL
        elif integrated_score > 0.3:
            return AdvancedArchaeologicalResult.INCONCLUSIVE
        else:
            return AdvancedArchaeologicalResult.NATURAL_PROCESS

    def _calculate_confidence_level(self, integrated_score: float) -> str:
        """Calcula nivel de confianza"""
        if integrated_score > 0.8:
            return "Muy Alta"
        elif integrated_score > 0.6:
            return "Alta"
        elif integrated_score > 0.4:
            return "Media"
        elif integrated_score > 0.2:
            return "Baja"
        else:
            return "Muy Baja"

    def _generate_explanation(self, temporal_score: float, 
                            spectral_score: float, 
                            modern_exclusion_score: float) -> str:
        """Genera explicación del resultado"""
        explanations = []
        
        if temporal_score > 0.5:
            explanations.append("Firma temporal arqueológica detectada")
        
        if spectral_score > 0.5:
            explanations.append("Índices espectrales no estándar indican estrés vegetal anómalo")
        
        if modern_exclusion_score > 0.5:
            explanations.append("Características compatibles con estructuras antropogénicas modernas")
        
        if not explanations:
            explanations.append("Patrones compatibles con procesos naturales")
        
        return "; ".join(explanations)