#!/usr/bin/env python3
"""
Motor de reglas arqueológicas para ArcheoScope.

Implementa reglas científicas para detectar persistencias espaciales
no explicables por procesos naturales actuales.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import logging
from dataclasses import dataclass
from scipy import ndimage, stats
# from sklearn.feature_extraction import image  # Comentado temporalmente
# import cv2  # Comentado temporalmente

logger = logging.getLogger(__name__)

class ArchaeologicalResult(Enum):
    """Resultado de evaluación arqueológica."""
    CONSISTENT = "consistent"                    # Explicable por procesos naturales
    ANOMALOUS = "anomalous"                     # Anomalía detectada
    ARCHAEOLOGICAL = "archaeological"            # Firma arqueológica probable
    LANDSCAPE_MODIFIED_NON_STRUCTURAL = "landscape_modified_non_structural"  # NUEVA: Paisaje modificado no estructural
    INCONCLUSIVE = "inconclusive"               # Datos insuficientes

@dataclass
class ArchaeologicalEvaluation:
    """Resultado de evaluación de regla arqueológica."""
    result: ArchaeologicalResult
    confidence: float                      # 0.0 - 1.0
    archaeological_probability: float      # 0.0 - 1.0
    affected_pixels: int
    geometric_coherence: float
    temporal_persistence: float
    natural_explanation_score: float       # Qué tan bien lo explican procesos naturales
    evidence_details: Dict[str, Any]
    rule_violations: List[str]
    resolution_penalty: float = 0.0        # NUEVA: Penalización por resolución gruesa
    geophysical_validation_required: bool = False  # NUEVA: Requiere validación geofísica

class ArchaeologicalRule:
    """Regla base para evaluación arqueológica."""
    
    def __init__(self, name: str, description: str, weight: float = 1.0):
        self.name = name
        self.description = description
        self.weight = weight
    
    def evaluate(self, datasets: Dict[str, Any]) -> ArchaeologicalEvaluation:
        """Evaluar regla arqueológica."""
        raise NotImplementedError("Subclasses must implement evaluate method")

class VegetationTopographyDecouplingRule(ArchaeologicalRule):
    """
    Regla: Desacople Vegetación-Topografía
    
    Detecta vegetación anómalamente vigorosa o débil donde no debería,
    indicativo de estructuras enterradas o alteración del suelo.
    """
    
    def __init__(self):
        super().__init__(
            "vegetation_topography_decoupling",
            "Detecta desacople entre vigor de vegetación y condiciones topográficas esperadas"
        )
    
    def evaluate(self, datasets: Dict[str, Any]) -> ArchaeologicalEvaluation:
        """Evaluar desacople vegetación-topografía."""
        
        if 'ndvi_vegetation' not in datasets:
            return self._inconclusive_result("NDVI data not available")
        
        ndvi_data = datasets['ndvi_vegetation'].values
        
        # Calcular gradientes topográficos si hay DEM
        if 'surface_elevation' in datasets:
            elevation = datasets['surface_elevation'].values
            slope = self._calculate_slope(elevation)
            aspect = self._calculate_aspect(elevation)
        else:
            # Usar gradientes sintéticos
            slope = np.ones_like(ndvi_data) * 0.1
            aspect = np.zeros_like(ndvi_data)
        
        # Modelo esperado: NDVI vs topografía
        expected_ndvi = self._model_expected_vegetation(slope, aspect)
        
        # Calcular desacople
        vegetation_anomaly = ndvi_data - expected_ndvi
        anomaly_magnitude = np.abs(vegetation_anomaly)
        
        # Detectar patrones geométricos en las anomalías
        geometric_score = self._detect_geometric_patterns(vegetation_anomaly)
        
        # Evaluar persistencia espacial
        persistence_score = self._evaluate_spatial_persistence(anomaly_magnitude)
        
        # Calcular probabilidad arqueológica
        archaeological_prob = self._calculate_archaeological_probability(
            anomaly_magnitude, geometric_score, persistence_score
        )
        
        # Calcular penalización por resolución
        resolution_m = datasets.get('resolution_m', 500)  # Resolución en metros
        resolution_penalty = self._calculate_resolution_penalty(resolution_m, anomaly_magnitude)
        
        # Determinar si requiere validación geofísica
        geophysical_required = self._requires_geophysical_validation(
            archaeological_prob, geometric_score, resolution_m
        )
        
        # Determinar resultado con nueva clasificación
        result = self._classify_archaeological_result(
            archaeological_prob, geometric_score, persistence_score, 
            resolution_penalty, anomaly_magnitude
        )
        
        # Aplicar penalización por resolución al score final
        final_archaeological_prob = max(0.0, archaeological_prob - resolution_penalty)
        
        # Contar píxeles afectados
        affected_pixels = int(np.sum(anomaly_magnitude > 0.15))
        
        # Calcular explicación natural
        natural_explanation = 1.0 - archaeological_prob
        
        return ArchaeologicalEvaluation(
            result=result,
            confidence=min(final_archaeological_prob * 1.2, 1.0),
            archaeological_probability=final_archaeological_prob,
            affected_pixels=affected_pixels,
            geometric_coherence=geometric_score,
            temporal_persistence=persistence_score,
            natural_explanation_score=1.0 - final_archaeological_prob,
            evidence_details={
                'max_vegetation_anomaly': float(np.max(anomaly_magnitude)),
                'mean_vegetation_anomaly': float(np.mean(anomaly_magnitude)),
                'anomaly_pattern_type': self._classify_anomaly_pattern(vegetation_anomaly),
                'suspected_features': self._identify_suspected_features(vegetation_anomaly),
                'resolution_context': f"Análisis a {resolution_m}m - {'Adecuado' if resolution_m <= 100 else 'Grueso' if resolution_m <= 500 else 'Muy grueso'}"
            },
            rule_violations=self._identify_violations(vegetation_anomaly, geometric_score),
            resolution_penalty=resolution_penalty,
            geophysical_validation_required=geophysical_required
        )
    
    def _calculate_slope(self, elevation: np.ndarray) -> np.ndarray:
        """Calcular pendiente del terreno."""
        gy, gx = np.gradient(elevation)
        slope = np.sqrt(gx**2 + gy**2)
        return slope
    
    def _calculate_aspect(self, elevation: np.ndarray) -> np.ndarray:
        """Calcular orientación del terreno."""
        gy, gx = np.gradient(elevation)
        aspect = np.arctan2(gy, gx)
        return aspect
    
    def _model_expected_vegetation(self, slope: np.ndarray, aspect: np.ndarray) -> np.ndarray:
        """Modelar vegetación esperada basada en topografía."""
        
        # Modelo simple: vegetación decrece con pendiente, varía con orientación
        base_ndvi = 0.6
        slope_effect = -0.3 * np.clip(slope, 0, 1)  # Pendiente reduce vegetación
        aspect_effect = 0.1 * np.cos(aspect)        # Orientación sur favorece vegetación
        
        expected = base_ndvi + slope_effect + aspect_effect
        return np.clip(expected, 0.1, 0.9)
    
    def _detect_geometric_patterns(self, anomaly: np.ndarray) -> float:
        """Detectar patrones geométricos no naturales."""
        
        # Binarizar anomalías significativas
        binary_anomaly = np.abs(anomaly) > 0.2
        
        if np.sum(binary_anomaly) < 10:
            return 0.0
        
        # Detectar líneas rectas usando gradientes (sin OpenCV)
        gy, gx = np.gradient(binary_anomaly.astype(float))
        
        # Detectar líneas horizontales y verticales
        horizontal_lines = np.sum(np.abs(gy) > 0.5)
        vertical_lines = np.sum(np.abs(gx) > 0.5)
        
        line_score = min((horizontal_lines + vertical_lines) / (binary_anomaly.size * 0.1), 1.0)
        
        # Detectar formas geométricas usando connected components
        labeled, num_features = ndimage.label(binary_anomaly)
        
        geometric_score = 0.0
        for i in range(1, num_features + 1):
            region = (labeled == i)
            if np.sum(region) > 10:
                # Calcular compacidad como proxy de geometría regular
                coords = np.where(region)
                if len(coords[0]) > 0:
                    height = np.max(coords[0]) - np.min(coords[0]) + 1
                    width = np.max(coords[1]) - np.min(coords[1]) + 1
                    area = np.sum(region)
                    
                    # Compacidad: área / (perímetro aproximado)
                    perimeter_approx = 2 * (height + width)
                    if perimeter_approx > 0:
                        compactness = area / perimeter_approx
                        if 0.2 < compactness < 0.8:  # Formas regulares
                            geometric_score += 0.2
        
        return min(line_score + geometric_score, 1.0)
    
    def _evaluate_spatial_persistence(self, anomaly_magnitude: np.ndarray) -> float:
        """Evaluar persistencia espacial de anomalías."""
        
        # Calcular autocorrelación espacial
        from scipy.spatial.distance import pdist, squareform
        
        # Submuestrear para eficiencia
        h, w = anomaly_magnitude.shape
        step = max(1, min(h, w) // 50)
        
        sample_anomaly = anomaly_magnitude[::step, ::step]
        sample_coords = [(i, j) for i in range(0, h, step) for j in range(0, w, step)]
        
        if len(sample_coords) < 10:
            return 0.0
        
        # Calcular correlación espacial
        values = sample_anomaly.flatten()
        coords = np.array(sample_coords)
        
        # Moran's I simplificado
        distances = squareform(pdist(coords))
        weights = 1.0 / (distances + 1e-6)  # Pesos inversamente proporcionales a distancia
        np.fill_diagonal(weights, 0)
        
        # Normalizar pesos
        row_sums = weights.sum(axis=1)
        weights = weights / (row_sums.reshape(-1, 1) + 1e-6)
        
        # Calcular Moran's I
        n = len(values)
        mean_val = np.mean(values)
        
        numerator = np.sum(weights * np.outer(values - mean_val, values - mean_val))
        denominator = np.sum((values - mean_val)**2)
        
        if denominator > 0:
            morans_i = numerator / denominator
            persistence_score = max(0, min(morans_i, 1.0))
        else:
            persistence_score = 0.0
        
        return persistence_score
    
    def _calculate_archaeological_probability(self, anomaly_magnitude: np.ndarray,
                                           geometric_score: float,
                                           persistence_score: float) -> float:
        """Calcular probabilidad arqueológica combinada."""
        
        # Factores ponderados
        anomaly_factor = min(np.mean(anomaly_magnitude) / 0.3, 1.0)  # Normalizar por umbral
        geometric_factor = geometric_score
        persistence_factor = persistence_score
        
        # Combinación ponderada
        archaeological_prob = (
            0.4 * anomaly_factor +
            0.4 * geometric_factor +
            0.2 * persistence_factor
        )
        
        return min(archaeological_prob, 1.0)
    
    def _classify_anomaly_pattern(self, vegetation_anomaly: np.ndarray) -> str:
        """Clasificar tipo de patrón de anomalía."""
        
        positive_anomalies = np.sum(vegetation_anomaly > 0.15)
        negative_anomalies = np.sum(vegetation_anomaly < -0.15)
        
        if positive_anomalies > negative_anomalies * 2:
            return "enhanced_vegetation"  # Posible drenaje mejorado
        elif negative_anomalies > positive_anomalies * 2:
            return "suppressed_vegetation"  # Posibles estructuras enterradas
        else:
            return "mixed_pattern"  # Patrón complejo
    
    def _identify_suspected_features(self, vegetation_anomaly: np.ndarray) -> List[str]:
        """Identificar características arqueológicas sospechosas."""
        
        features = []
        
        # Detectar líneas de vegetación suprimida (posibles muros)
        suppressed = vegetation_anomaly < -0.2
        if np.sum(suppressed) > 0:
            # Buscar patrones lineales
            kernel_h = np.ones((1, 10))  # Línea horizontal
            kernel_v = np.ones((10, 1))  # Línea vertical
            
            conv_h = ndimage.convolve(suppressed.astype(float), kernel_h)
            conv_v = ndimage.convolve(suppressed.astype(float), kernel_v)
            
            if np.max(conv_h) > 7:
                features.append("horizontal_wall_signature")
            if np.max(conv_v) > 7:
                features.append("vertical_wall_signature")
        
        # Detectar líneas de vegetación mejorada (posibles caminos/drenajes)
        enhanced = vegetation_anomaly > 0.2
        if np.sum(enhanced) > 0:
            # Similar análisis para vegetación mejorada
            conv_h = ndimage.convolve(enhanced.astype(float), kernel_h)
            conv_v = ndimage.convolve(enhanced.astype(float), kernel_v)
            
            if np.max(conv_h) > 7:
                features.append("horizontal_drainage_signature")
            if np.max(conv_v) > 7:
                features.append("vertical_drainage_signature")
        
        # Detectar patrones rectangulares
        binary_anomaly = np.abs(vegetation_anomaly) > 0.15
        labeled, num_features = ndimage.label(binary_anomaly)
        
        for i in range(1, num_features + 1):
            region = (labeled == i)
            if np.sum(region) > 50:  # Región significativa
                # Calcular ratio de aspecto del bounding box
                coords = np.where(region)
                height = np.max(coords[0]) - np.min(coords[0])
                width = np.max(coords[1]) - np.min(coords[1])
                
                if height > 0 and width > 0:
                    aspect_ratio = max(height, width) / min(height, width)
                    if 1.2 < aspect_ratio < 5:  # Rectangular pero no extremo
                        features.append("rectangular_structure_signature")
        
        return features
    
    def _identify_violations(self, vegetation_anomaly: np.ndarray, 
                           geometric_score: float) -> List[str]:
        """Identificar violaciones de procesos naturales."""
        
        violations = []
        
        # Violación 1: Patrones demasiado geométricos para ser naturales
        if geometric_score > 0.6:
            violations.append("excessive_geometric_regularity")
        
        # Violación 2: Anomalías de vegetación sin explicación topográfica
        extreme_anomalies = np.sum(np.abs(vegetation_anomaly) > 0.3)
        if extreme_anomalies > vegetation_anomaly.size * 0.05:  # >5% de píxeles
            violations.append("unexplained_vegetation_patterns")
        
        # Violación 3: Patrones lineales persistentes
        if "wall_signature" in str(self._identify_suspected_features(vegetation_anomaly)):
            violations.append("persistent_linear_patterns")
        
        return violations
    
    def _calculate_resolution_penalty(self, resolution_m: float, anomaly_data: np.ndarray) -> float:
        """
        Calcular penalización por resolución gruesa.
        
        Penaliza cuando el píxel es mayor que el tamaño esperado de estructuras.
        """
        # Tamaños típicos de estructuras arqueológicas
        typical_structure_sizes = {
            'walls': 1.0,           # 1m ancho típico
            'foundations': 5.0,     # 5m estructura típica
            'buildings': 15.0,      # 15m edificio típico
            'complexes': 50.0       # 50m complejo típico
        }
        
        # Calcular penalización basada en resolución vs estructura esperada
        penalty = 0.0
        
        if resolution_m > 100:  # Muy grueso
            penalty += 0.3
        elif resolution_m > 50:  # Grueso
            penalty += 0.2
        elif resolution_m > 20:  # Moderadamente grueso
            penalty += 0.1
        
        # Penalización adicional si la anomalía es muy pequeña para la resolución
        anomaly_extent = np.sum(anomaly_data > 0.1)  # Píxeles con anomalía
        if anomaly_extent < 4:  # Menos de 4 píxeles
            penalty += 0.15
        
        return min(penalty, 0.5)  # Máximo 50% de penalización
    
    def _requires_geophysical_validation(self, archaeological_prob: float, 
                                       geometric_score: float, resolution_m: float) -> bool:
        """
        Determinar si requiere validación geofísica.
        
        Criterios académicos para requerir GPR/magnetometría.
        """
        # Siempre requiere validación si:
        if archaeological_prob > 0.4 and resolution_m > 50:
            return bool(True)
        
        # Requiere si hay alta geometría pero resolución gruesa
        if geometric_score > 0.6 and resolution_m > 100:
            return bool(True)
        
        # Requiere si la probabilidad es moderada-alta
        if archaeological_prob > 0.5:
            return bool(True)
        
        return bool(False)
    
    def _classify_archaeological_result(self, archaeological_prob: float, 
                                      geometric_score: float, persistence_score: float,
                                      resolution_penalty: float, anomaly_data: np.ndarray) -> ArchaeologicalResult:
        """
        Clasificar resultado arqueológico con nueva categoría intermedia.
        
        Evita el binarismo natural/arqueológico agregando categoría intermedia.
        """
        # Aplicar penalización por resolución
        adjusted_prob = max(0.0, archaeological_prob - resolution_penalty)
        
        # Detectar si es paisaje modificado no estructural
        is_landscape_modified = self._detect_landscape_modification(
            anomaly_data, geometric_score, persistence_score
        )
        
        # Clasificación mejorada
        if adjusted_prob > 0.75 and geometric_score > 0.6:
            return ArchaeologicalResult.ARCHAEOLOGICAL
        elif is_landscape_modified and 0.3 < adjusted_prob < 0.7:
            return ArchaeologicalResult.LANDSCAPE_MODIFIED_NON_STRUCTURAL
        elif adjusted_prob > 0.4:
            return ArchaeologicalResult.ANOMALOUS
        else:
            return ArchaeologicalResult.CONSISTENT
    
    def _detect_landscape_modification(self, anomaly_data: np.ndarray, 
                                     geometric_score: float, persistence_score: float) -> bool:
        """
        Detectar si es paisaje modificado no estructural.
        
        Características:
        - Anomalías persistentes pero no muy geométricas
        - Patrones difusos o extensos
        - Modificación del paisaje sin estructuras claras
        """
        # Criterios para paisaje modificado
        anomaly_extent = np.sum(anomaly_data > 0.1) / anomaly_data.size
        
        # Es paisaje modificado si:
        # 1. Extensión moderada (5-30% del área)
        # 2. Persistencia alta pero geometría moderada
        # 3. Patrones difusos
        
        if (0.05 < anomaly_extent < 0.3 and 
            persistence_score > 0.5 and 
            0.2 < geometric_score < 0.6):
            return bool(True)
        
        return bool(False)
    
    def _inconclusive_result(self, reason: str) -> ArchaeologicalEvaluation:
        """Generar resultado inconcluso."""
        return ArchaeologicalEvaluation(
            result=ArchaeologicalResult.INCONCLUSIVE,
            confidence=0.0,
            archaeological_probability=0.0,
            affected_pixels=0,
            geometric_coherence=0.0,
            temporal_persistence=0.0,
            natural_explanation_score=1.0,
            evidence_details={'reason': reason},
            rule_violations=[]
        )

class ThermalResidualPatternsRule(ArchaeologicalRule):
    """
    Regla: Patrones Térmicos Residuales
    
    Detecta patrones térmicos persistentes indicativos de estructuras
    enterradas con diferente inercia térmica.
    """
    
    def __init__(self):
        super().__init__(
            "thermal_residual_patterns",
            "Detecta patrones térmicos residuales de estructuras enterradas"
        )
    
    def evaluate(self, datasets: Dict[str, Any]) -> ArchaeologicalEvaluation:
        """Evaluar patrones térmicos residuales."""
        
        if 'thermal_lst' not in datasets:
            return self._inconclusive_result("Thermal data not available")
        
        thermal_data = datasets['thermal_lst'].values
        
        # Calcular anomalías térmicas
        thermal_mean = np.mean(thermal_data)
        thermal_std = np.std(thermal_data)
        thermal_anomaly = (thermal_data - thermal_mean) / (thermal_std + 1e-6)
        
        # Detectar patrones geométricos en anomalías térmicas
        geometric_score = self._detect_thermal_geometric_patterns(thermal_anomaly)
        
        # Evaluar persistencia de patrones térmicos
        persistence_score = self._evaluate_thermal_persistence(thermal_anomaly)
        
        # Detectar firmas de diferentes materiales
        material_signatures = self._detect_material_signatures(thermal_data)
        
        # Calcular probabilidad arqueológica
        archaeological_prob = self._calculate_thermal_archaeological_probability(
            thermal_anomaly, geometric_score, persistence_score, material_signatures
        )
        
        # Determinar resultado
        if archaeological_prob > 0.7:
            result = ArchaeologicalResult.ARCHAEOLOGICAL
        elif archaeological_prob > 0.4:
            result = ArchaeologicalResult.ANOMALOUS
        else:
            result = ArchaeologicalResult.CONSISTENT
        
        affected_pixels = int(np.sum(np.abs(thermal_anomaly) > 1.5))
        
        return ArchaeologicalEvaluation(
            result=result,
            confidence=min(archaeological_prob * 1.1, 1.0),
            archaeological_probability=archaeological_prob,
            affected_pixels=affected_pixels,
            geometric_coherence=geometric_score,
            temporal_persistence=persistence_score,
            natural_explanation_score=1.0 - archaeological_prob,
            evidence_details={
                'max_thermal_anomaly': float(np.max(np.abs(thermal_anomaly))),
                'material_signatures': material_signatures,
                'thermal_pattern_type': self._classify_thermal_pattern(thermal_anomaly)
            },
            rule_violations=self._identify_thermal_violations(thermal_anomaly, geometric_score)
        )
    
    def _detect_thermal_geometric_patterns(self, thermal_anomaly: np.ndarray) -> float:
        """Detectar patrones geométricos en datos térmicos."""
        
        # Similar a vegetación pero adaptado para térmico
        binary_hot = thermal_anomaly > 1.5   # Anomalías calientes
        binary_cold = thermal_anomaly < -1.5  # Anomalías frías
        
        geometric_score = 0.0
        
        for binary_data, label in [(binary_hot, "hot"), (binary_cold, "cold")]:
            if np.sum(binary_data) > 10:
                # Detectar líneas usando gradientes
                gy, gx = np.gradient(binary_data.astype(float))
                
                # Contar líneas horizontales y verticales
                horizontal_lines = np.sum(np.abs(gy) > 0.5)
                vertical_lines = np.sum(np.abs(gx) > 0.5)
                
                if horizontal_lines + vertical_lines > binary_data.size * 0.05:
                    geometric_score += 0.25
        
        return min(geometric_score, 1.0)
    
    def _evaluate_thermal_persistence(self, thermal_anomaly: np.ndarray) -> float:
        """Evaluar persistencia de patrones térmicos."""
        
        # Calcular coherencia espacial de anomalías térmicas
        significant_anomalies = np.abs(thermal_anomaly) > 1.0
        
        if np.sum(significant_anomalies) < 10:
            return 0.0
        
        # Usar filtro de coherencia espacial
        coherence_kernel = np.ones((5, 5)) / 25
        coherence_map = ndimage.convolve(significant_anomalies.astype(float), coherence_kernel)
        
        # Persistencia = proporción de píxeles con alta coherencia local
        high_coherence = coherence_map > 0.6
        persistence_score = np.sum(high_coherence) / np.sum(significant_anomalies)
        
        return min(persistence_score, 1.0)
    
    def _detect_material_signatures(self, thermal_data: np.ndarray) -> Dict[str, float]:
        """Detectar firmas de diferentes materiales."""
        
        signatures = {}
        
        # Detectar zonas de alta inercia térmica (piedra, estructuras)
        high_inertia = thermal_data > np.percentile(thermal_data, 85)
        signatures['high_thermal_inertia'] = np.sum(high_inertia) / thermal_data.size
        
        # Detectar zonas de baja inercia térmica (tierra removida)
        low_inertia = thermal_data < np.percentile(thermal_data, 15)
        signatures['low_thermal_inertia'] = np.sum(low_inertia) / thermal_data.size
        
        # Detectar patrones de contraste térmico (bordes de estructuras)
        thermal_gradient = np.gradient(thermal_data)
        high_gradient = np.sqrt(thermal_gradient[0]**2 + thermal_gradient[1]**2)
        signatures['thermal_edges'] = np.sum(high_gradient > np.percentile(high_gradient, 90)) / thermal_data.size
        
        return signatures
    
    def _calculate_thermal_archaeological_probability(self, thermal_anomaly: np.ndarray,
                                                   geometric_score: float,
                                                   persistence_score: float,
                                                   material_signatures: Dict[str, float]) -> float:
        """Calcular probabilidad arqueológica basada en datos térmicos."""
        
        # Factor de anomalía térmica
        anomaly_factor = min(np.mean(np.abs(thermal_anomaly)) / 2.0, 1.0)
        
        # Factor de firmas de materiales
        material_factor = (
            material_signatures.get('high_thermal_inertia', 0) * 2 +
            material_signatures.get('thermal_edges', 0) * 1.5
        )
        material_factor = min(material_factor, 1.0)
        
        # Combinación ponderada
        archaeological_prob = (
            0.3 * anomaly_factor +
            0.3 * geometric_score +
            0.2 * persistence_score +
            0.2 * material_factor
        )
        
        return min(archaeological_prob, 1.0)
    
    def _classify_thermal_pattern(self, thermal_anomaly: np.ndarray) -> str:
        """Clasificar tipo de patrón térmico."""
        
        hot_anomalies = np.sum(thermal_anomaly > 1.5)
        cold_anomalies = np.sum(thermal_anomaly < -1.5)
        
        if hot_anomalies > cold_anomalies * 2:
            return "high_thermal_inertia_pattern"  # Posibles estructuras de piedra
        elif cold_anomalies > hot_anomalies * 2:
            return "low_thermal_inertia_pattern"   # Posible tierra removida
        else:
            return "mixed_thermal_pattern"         # Patrón complejo
    
    def _identify_thermal_violations(self, thermal_anomaly: np.ndarray,
                                   geometric_score: float) -> List[str]:
        """Identificar violaciones térmicas de procesos naturales."""
        
        violations = []
        
        if geometric_score > 0.5:
            violations.append("geometric_thermal_patterns")
        
        extreme_thermal = np.sum(np.abs(thermal_anomaly) > 2.0)
        if extreme_thermal > thermal_anomaly.size * 0.03:
            violations.append("unexplained_thermal_extremes")
        
        return violations
    
    def _inconclusive_result(self, reason: str) -> ArchaeologicalEvaluation:
        """Generar resultado inconcluso."""
        return ArchaeologicalEvaluation(
            result=ArchaeologicalResult.INCONCLUSIVE,
            confidence=0.0,
            archaeological_probability=0.0,
            affected_pixels=0,
            geometric_coherence=0.0,
            temporal_persistence=0.0,
            natural_explanation_score=1.0,
            evidence_details={'reason': reason},
            rule_violations=[]
        )

class ArchaeologicalRulesEngine:
    """
    Motor de reglas arqueológicas para ArcheoScope.
    
    Coordina la evaluación de múltiples reglas arqueológicas
    y genera un análisis integrado.
    """
    
    def __init__(self):
        """Inicializar motor de reglas arqueológicas."""
        
        self.rules = [
            VegetationTopographyDecouplingRule(),
            ThermalResidualPatternsRule(),
            # Aquí se pueden añadir más reglas:
            # GeometricAnomalyRule(),
            # SeismicResonanceRule(),
            # SalinityDrainageRule(),
            # etc.
        ]
        
        logger.info(f"ArchaeologicalRulesEngine inicializado con {len(self.rules)} reglas")
    
    def evaluate_all_rules(self, datasets: Dict[str, Any]) -> Dict[str, ArchaeologicalEvaluation]:
        """
        Evaluar todas las reglas arqueológicas.
        
        Args:
            datasets: Diccionario de datasets arqueológicos
            
        Returns:
            Diccionario de evaluaciones por regla
        """
        
        evaluations = {}
        
        for rule in self.rules:
            try:
                evaluation = rule.evaluate(datasets)
                evaluations[rule.name] = evaluation
                
                logger.info(f"Regla {rule.name}: {evaluation.result.value} "
                           f"(prob={evaluation.archaeological_probability:.3f}, "
                           f"conf={evaluation.confidence:.3f})")
                
            except Exception as e:
                logger.error(f"Error evaluando regla {rule.name}: {e}")
                evaluations[rule.name] = ArchaeologicalEvaluation(
                    result=ArchaeologicalResult.INCONCLUSIVE,
                    confidence=0.0,
                    archaeological_probability=0.0,
                    affected_pixels=0,
                    geometric_coherence=0.0,
                    temporal_persistence=0.0,
                    natural_explanation_score=1.0,
                    evidence_details={'error': str(e)},
                    rule_violations=[]
                )
        
        return evaluations
    
    def get_integrated_assessment(self, evaluations: Dict[str, ArchaeologicalEvaluation]) -> Dict[str, Any]:
        """
        Generar evaluación arqueológica integrada.
        
        Args:
            evaluations: Evaluaciones individuales por regla
            
        Returns:
            Evaluación arqueológica integrada
        """
        
        # Calcular métricas agregadas
        total_rules = len(evaluations)
        archaeological_rules = sum(1 for e in evaluations.values() 
                                 if e.result == ArchaeologicalResult.ARCHAEOLOGICAL)
        anomalous_rules = sum(1 for e in evaluations.values() 
                            if e.result == ArchaeologicalResult.ANOMALOUS)
        
        # Probabilidad arqueológica ponderada
        weighted_prob = 0.0
        total_weight = 0.0
        
        for rule_name, evaluation in evaluations.items():
            rule = next(r for r in self.rules if r.name == rule_name)
            weighted_prob += evaluation.archaeological_probability * rule.weight
            total_weight += rule.weight
        
        if total_weight > 0:
            integrated_probability = weighted_prob / total_weight
        else:
            integrated_probability = 0.0
        
        # Confianza integrada
        confidences = [e.confidence for e in evaluations.values() if e.confidence > 0]
        integrated_confidence = np.mean(confidences) if confidences else 0.0
        
        # Coherencia geométrica promedio
        geometric_coherences = [e.geometric_coherence for e in evaluations.values()]
        avg_geometric_coherence = np.mean(geometric_coherences) if geometric_coherences else 0.0
        
        # Persistencia temporal promedio
        temporal_persistences = [e.temporal_persistence for e in evaluations.values()]
        avg_temporal_persistence = np.mean(temporal_persistences) if temporal_persistences else 0.0
        
        # Clasificación integrada
        if integrated_probability > 0.7 and archaeological_rules >= 2:
            classification = "high_archaeological_potential"
        elif integrated_probability > 0.5 and (archaeological_rules >= 1 or anomalous_rules >= 2):
            classification = "moderate_archaeological_potential"
        elif integrated_probability > 0.3 or anomalous_rules >= 1:
            classification = "low_archaeological_potential"
        else:
            classification = "natural_processes_sufficient"
        
        # Recopilar todas las violaciones
        all_violations = []
        for evaluation in evaluations.values():
            all_violations.extend(evaluation.rule_violations)
        
        # Recopilar evidencia
        evidence_summary = {}
        for rule_name, evaluation in evaluations.items():
            if evaluation.evidence_details:
                evidence_summary[rule_name] = evaluation.evidence_details
        
        return {
            'classification': classification,
            'integrated_probability': integrated_probability,
            'integrated_confidence': integrated_confidence,
            'geometric_coherence': avg_geometric_coherence,
            'temporal_persistence': avg_temporal_persistence,
            'rules_summary': {
                'total_rules': total_rules,
                'archaeological_rules': archaeological_rules,
                'anomalous_rules': anomalous_rules,
                'consistent_rules': total_rules - archaeological_rules - anomalous_rules
            },
            'violations': all_violations,
            'evidence_summary': evidence_summary,
            'recommendation': self._generate_recommendation(classification, integrated_probability)
        }
    
    def _generate_recommendation(self, classification: str, probability: float) -> str:
        """Generar recomendación basada en la evaluación."""
        
        if classification == "high_archaeological_potential":
            return ("Área con alta probabilidad de intervención humana antigua. "
                   "Recomendado: investigación arqueológica detallada con métodos geofísicos.")
        
        elif classification == "moderate_archaeological_potential":
            return ("Área con indicios moderados de actividad humana antigua. "
                   "Recomendado: análisis adicional con datos de mayor resolución.")
        
        elif classification == "low_archaeological_potential":
            return ("Área con algunos indicios anómalos que podrían ser arqueológicos. "
                   "Recomendado: monitoreo con datos multitemporales.")
        
        else:
            return ("Área consistente con procesos naturales. "
                   "No se requiere investigación arqueológica adicional.")
    
    def get_summary(self) -> Dict[str, Any]:
        """Obtener resumen del motor de reglas."""
        
        return {
            'total_rules': len(self.rules),
            'rule_names': [rule.name for rule in self.rules],
            'rule_descriptions': {rule.name: rule.description for rule in self.rules},
            'engine_type': 'archaeological',
            'paradigm': 'spatial_persistence_detection'
        }
    def _calculate_resolution_penalty(self, resolution_m: float, anomaly_data: np.ndarray) -> float:
        """
        Calcular penalización por resolución gruesa.
        
        Penaliza cuando el píxel es mayor que el tamaño esperado de estructuras.
        """
        # Tamaños típicos de estructuras arqueológicas
        typical_structure_sizes = {
            'walls': 1.0,           # 1m ancho típico
            'foundations': 5.0,     # 5m estructura típica
            'buildings': 15.0,      # 15m edificio típico
            'complexes': 50.0       # 50m complejo típico
        }
        
        # Calcular penalización basada en resolución vs estructura esperada
        penalty = 0.0
        
        if resolution_m > 100:  # Muy grueso
            penalty += 0.3
        elif resolution_m > 50:  # Grueso
            penalty += 0.2
        elif resolution_m > 20:  # Moderadamente grueso
            penalty += 0.1
        
        # Penalización adicional si la anomalía es muy pequeña para la resolución
        anomaly_extent = np.sum(anomaly_data > 0.1)  # Píxeles con anomalía
        if anomaly_extent < 4:  # Menos de 4 píxeles
            penalty += 0.15
        
        return min(penalty, 0.5)  # Máximo 50% de penalización
    
    def _requires_geophysical_validation(self, archaeological_prob: float, 
                                       geometric_score: float, resolution_m: float) -> bool:
        """
        Determinar si requiere validación geofísica.
        
        Criterios académicos para requerir GPR/magnetometría.
        """
        # Siempre requiere validación si:
        if archaeological_prob > 0.4 and resolution_m > 50:
            return bool(True)
        
        # Requiere si hay alta geometría pero resolución gruesa
        if geometric_score > 0.6 and resolution_m > 100:
            return bool(True)
        
        # Requiere si la probabilidad es moderada-alta
        if archaeological_prob > 0.5:
            return bool(True)
        
        return bool(False)
    
    def _classify_archaeological_result(self, archaeological_prob: float, 
                                      geometric_score: float, persistence_score: float,
                                      resolution_penalty: float, anomaly_data: np.ndarray) -> ArchaeologicalResult:
        """
        Clasificar resultado arqueológico con nueva categoría intermedia.
        
        Evita el binarismo natural/arqueológico agregando categoría intermedia.
        """
        # Aplicar penalización por resolución
        adjusted_prob = max(0.0, archaeological_prob - resolution_penalty)
        
        # Detectar si es paisaje modificado no estructural
        is_landscape_modified = self._detect_landscape_modification(
            anomaly_data, geometric_score, persistence_score
        )
        
        # Clasificación mejorada
        if adjusted_prob > 0.75 and geometric_score > 0.6:
            return ArchaeologicalResult.ARCHAEOLOGICAL
        elif is_landscape_modified and 0.3 < adjusted_prob < 0.7:
            return ArchaeologicalResult.LANDSCAPE_MODIFIED_NON_STRUCTURAL
        elif adjusted_prob > 0.4:
            return ArchaeologicalResult.ANOMALOUS
        else:
            return ArchaeologicalResult.CONSISTENT
    
    def _detect_landscape_modification(self, anomaly_data: np.ndarray, 
                                     geometric_score: float, persistence_score: float) -> bool:
        """
        Detectar si es paisaje modificado no estructural.
        
        Características:
        - Anomalías persistentes pero no muy geométricas
        - Patrones difusos o extensos
        - Modificación del paisaje sin estructuras claras
        """
        # Criterios para paisaje modificado
        anomaly_extent = np.sum(anomaly_data > 0.1) / anomaly_data.size
        
        # Es paisaje modificado si:
        # 1. Extensión moderada (5-30% del área)
        # 2. Persistencia alta pero geometría moderada
        # 3. Patrones difusos
        
        if (0.05 < anomaly_extent < 0.3 and 
            persistence_score > 0.5 and 
            0.2 < geometric_score < 0.6):
            return bool(True)
        
        return bool(False)