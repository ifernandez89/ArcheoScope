#!/usr/bin/env python3
"""
ArcheoScope Regional Calibration System
======================================

MEJORAS CRÍTICAS IMPLEMENTADAS:
1. Calibración regional por eco-regiones (Köppen + ecorregiones)
2. Matriz de sensores ponderada dinámicamente
3. Sistema de convergencia explicable y auditable
4. Persistencia relativa vs absoluta

FILOSOFÍA:
- Reglas físicas base + Ajustes eco-regionales → ML
- Matriz no rígida, sino ponderada por contexto
- Score explicable y defendible científicamente
- Persistencia relativa para robustez temporal
"""

import json
import logging
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class EcoRegion(Enum):
    """Eco-regiones para calibración específica"""
    # Desiertos
    SAHARA = "sahara"
    ATACAMA = "atacama" 
    ARABIAN = "arabian"
    GOBI = "gobi"
    SONORAN = "sonoran"
    
    # Selvas
    AMAZON_HUMID = "amazon_humid"
    AMAZON_DRY = "amazon_dry"
    CONGO_HUMID = "congo_humid"
    SOUTHEAST_ASIA_HUMID = "southeast_asia_humid"
    
    # Montañas
    ANDES_TROPICAL = "andes_tropical"
    ANDES_TEMPERATE = "andes_temperate"
    HIMALAYA = "himalaya"
    ALPS = "alps"
    ROCKIES = "rockies"
    
    # Polares
    ANTARCTICA_COASTAL = "antarctica_coastal"
    ANTARCTICA_INTERIOR = "antarctica_interior"
    GREENLAND = "greenland"
    ARCTIC_TUNDRA = "arctic_tundra"
    
    # Marinos
    CARIBBEAN_SHALLOW = "caribbean_shallow"
    MEDITERRANEAN = "mediterranean"
    NORTH_SEA = "north_sea"
    PACIFIC_TROPICAL = "pacific_tropical"
    
    # Fallback
    UNKNOWN = "unknown"

@dataclass
class RegionalCalibration:
    """Calibración específica por eco-región"""
    eco_region: EcoRegion
    base_environment: str  # desert, forest, etc.
    
    # Factores de ajuste por sensor (multiplicadores)
    sensor_weight_adjustments: Dict[str, float]
    
    # Umbrales ajustados regionalmente
    threshold_adjustments: Dict[str, float]
    
    # Contexto climático específico
    climate_context: Dict[str, Any]
    
    # Factores de confianza regional
    confidence_factors: Dict[str, float]
    
    # Notas científicas
    scientific_rationale: str

@dataclass
class ConvergenceScore:
    """Score de convergencia explicable y auditable"""
    total_score: float  # 0.0 - 1.0
    
    # Componentes del score (ponderados)
    forma_score: float      # w1 * forma (LiDAR/DEM)
    compactacion_score: float  # w2 * compactación (SAR)
    termico_score: float    # w3 * térmico
    espectral_score: float  # w4 * espectral
    
    # Pesos utilizados
    weights: Dict[str, float]
    
    # Explicación detallada
    explanation: str
    convergence_reason: str
    
    # Instrumentos que contribuyen
    contributing_instruments: List[str]
    
    # Nivel de confianza
    confidence_level: str  # "high", "moderate", "low"

@dataclass
class PersistenceAnalysis:
    """Análisis de persistencia relativa vs absoluta"""
    temporal_window_years: int
    
    # Persistencia absoluta (tradicional)
    absolute_persistence: bool
    absolute_duration_years: float
    
    # Persistencia relativa (nueva)
    relative_persistence_score: float  # 0.0 - 1.0
    geometric_stability_score: float   # 0.0 - 1.0
    volatility_score: float           # 0.0 - 1.0 (menor es mejor)
    
    # Clasificación final
    persistence_classification: str  # "persistent", "intermittent_stable", "volatile"
    
    # Explicación
    persistence_explanation: str

class RegionalCalibrationSystem:
    """
    Sistema de calibración regional avanzado
    
    FUNCIONALIDADES:
    1. Detecta eco-región específica
    2. Ajusta pesos de sensores dinámicamente
    3. Calcula score de convergencia explicable
    4. Analiza persistencia relativa
    """
    
    def __init__(self):
        """Inicializar sistema de calibración regional"""
        self.regional_calibrations = self._load_regional_calibrations()
        self.eco_region_boundaries = self._load_eco_region_boundaries()
        
        logger.info("RegionalCalibrationSystem inicializado")
        print("[OK] Sistema de calibración regional activado", flush=True)
        print("[OK] Eco-regiones cargadas:", len(self.regional_calibrations), flush=True)
    
    def detect_eco_region(self, lat: float, lon: float, environment_type: str) -> EcoRegion:
        """
        Detectar eco-región específica basada en coordenadas y ambiente
        
        MEJORA CLAVE: No solo ambiente, sino eco-región específica
        """
        
        # Desiertos con calibración específica
        if environment_type == "desert":
            # Sahara
            if 15 <= lat <= 35 and -17 <= lon <= 35:
                return EcoRegion.SAHARA
            # Atacama
            elif -27 <= lat <= -18 and -71 <= lon <= -68:
                return EcoRegion.ATACAMA
            # Arábigo
            elif 12 <= lat <= 32 and 35 <= lon <= 60:
                return EcoRegion.ARABIAN
            # Gobi
            elif 38 <= lat <= 47 and 90 <= lon <= 110:
                return EcoRegion.GOBI
            # Sonoran (México/Arizona)
            elif 25 <= lat <= 35 and -117 <= lon <= -107:
                return EcoRegion.SONORAN
        
        # Selvas con diferenciación húmeda/seca
        elif environment_type == "forest":
            # Amazonas húmeda (norte)
            if -5 <= lat <= 5 and -75 <= lon <= -45:
                return EcoRegion.AMAZON_HUMID
            # Amazonas seca (sur)
            elif -15 <= lat <= -5 and -70 <= lon <= -50:
                return EcoRegion.AMAZON_DRY
            # Congo húmeda
            elif -5 <= lat <= 5 and 10 <= lon <= 30:
                return EcoRegion.CONGO_HUMID
            # Sudeste asiático húmedo
            elif -10 <= lat <= 20 and 95 <= lon <= 140:
                return EcoRegion.SOUTHEAST_ASIA_HUMID
        
        # Montañas con contexto climático
        elif environment_type == "mountain":
            # Andes tropicales
            if -20 <= lat <= 10 and -82 <= lon <= -63:
                return EcoRegion.ANDES_TROPICAL
            # Andes templados
            elif -45 <= lat <= -20 and -75 <= lon <= -65:
                return EcoRegion.ANDES_TEMPERATE
            # Himalaya
            elif 27 <= lat <= 36 and 70 <= lon <= 95:
                return EcoRegion.HIMALAYA
            # Alpes
            elif 43 <= lat <= 48 and 5 <= lon <= 14:
                return EcoRegion.ALPS
            # Rocosas
            elif 31 <= lat <= 60 and -120 <= lon <= -102:
                return EcoRegion.ROCKIES
        
        # Regiones polares
        elif environment_type in ["polar_ice", "glacier"]:
            # Antártida costera
            if -70 <= lat <= -60:
                return EcoRegion.ANTARCTICA_COASTAL
            # Antártida interior
            elif lat < -70:
                return EcoRegion.ANTARCTICA_INTERIOR
            # Groenlandia
            elif 60 <= lat <= 84 and -75 <= lon <= -10:
                return EcoRegion.GREENLAND
            # Tundra ártica
            elif 66.5 <= lat <= 75:
                return EcoRegion.ARCTIC_TUNDRA
        
        # Ambientes marinos
        elif environment_type == "shallow_sea":
            # Caribe
            if 10 <= lat <= 25 and -85 <= lon <= -60:
                return EcoRegion.CARIBBEAN_SHALLOW
            # Mediterráneo
            elif 30 <= lat <= 46 and -6 <= lon <= 37:
                return EcoRegion.MEDITERRANEAN
            # Mar del Norte
            elif 51 <= lat <= 62 and -4 <= lon <= 9:
                return EcoRegion.NORTH_SEA
            # Pacífico tropical
            elif -20 <= lat <= 20 and 120 <= lon <= -80:
                return EcoRegion.PACIFIC_TROPICAL
        
        return EcoRegion.UNKNOWN
    
    def get_regional_calibration(self, eco_region: EcoRegion) -> RegionalCalibration:
        """Obtener calibración específica para eco-región"""
        return self.regional_calibrations.get(eco_region, self._get_default_calibration())
    
    def calculate_weighted_sensor_matrix(self, eco_region: EcoRegion, 
                                       environment_context: Any,
                                       measurements: List[Any]) -> Dict[str, float]:
        """
        MEJORA CLAVE: Matriz de sensores ponderada dinámicamente
        
        No rígida, sino adaptativa según:
        - Eco-región específica
        - Condiciones ambientales actuales
        - Confianza inicial de mediciones
        """
        
        calibration = self.get_regional_calibration(eco_region)
        base_weights = self._get_base_sensor_weights(environment_context.environment_type.value)
        
        # Aplicar ajustes regionales
        adjusted_weights = {}
        for sensor, base_weight in base_weights.items():
            regional_adjustment = calibration.sensor_weight_adjustments.get(sensor, 1.0)
            adjusted_weights[sensor] = base_weight * regional_adjustment
        
        # Ajustar por condiciones actuales
        for measurement in measurements:
            sensor_name = measurement.instrument_name
            if sensor_name in adjusted_weights:
                
                # Ejemplo: Selva + baja nubosidad → subir óptico
                if (environment_context.environment_type.value == "forest" and 
                    "sentinel2" in sensor_name and 
                    measurement.confidence == "high"):
                    adjusted_weights[sensor_name] *= 1.3
                
                # Ejemplo: Selva + alta humedad → subir L-band
                elif (environment_context.environment_type.value == "forest" and 
                      "sar" in sensor_name and 
                      eco_region in [EcoRegion.AMAZON_HUMID, EcoRegion.CONGO_HUMID]):
                    adjusted_weights[sensor_name] *= 1.4
                
                # Desierto + día claro → subir térmico
                elif (environment_context.environment_type.value == "desert" and 
                      "thermal" in sensor_name and 
                      measurement.confidence == "high"):
                    adjusted_weights[sensor_name] *= 1.2
        
        # Normalizar pesos
        total_weight = sum(adjusted_weights.values())
        if total_weight > 0:
            adjusted_weights = {k: v/total_weight for k, v in adjusted_weights.items()}
        
        return adjusted_weights
    
    def calculate_convergence_score(self, measurements: List[Any], 
                                  sensor_weights: Dict[str, float],
                                  eco_region: EcoRegion) -> ConvergenceScore:
        """
        MEJORA CRÍTICA: Score de convergencia explicable y auditable
        
        Score total = w1 * forma + w2 * compactación + w3 * térmico + w4 * espectral
        """
        
        # Inicializar componentes
        forma_score = 0.0
        compactacion_score = 0.0
        termico_score = 0.0
        espectral_score = 0.0
        
        contributing_instruments = []
        explanations = []
        
        # Procesar cada medición
        for measurement in measurements:
            if not measurement.exceeds_threshold:
                continue
                
            instrument = measurement.instrument_name
            weight = sensor_weights.get(instrument, 0.0)
            confidence_multiplier = self._get_confidence_multiplier(measurement.confidence)
            
            # Clasificar por tipo de sensor y acumular scores
            if any(keyword in instrument.lower() for keyword in ['lidar', 'icesat2', 'dem', 'elevation']):
                # Forma (LiDAR/DEM)
                forma_score += weight * confidence_multiplier * (measurement.value / measurement.threshold)
                contributing_instruments.append(f"{instrument} (forma)")
                explanations.append(f"Forma: {instrument} detectó anomalía de {measurement.value:.2f} {measurement.unit}")
                
            elif any(keyword in instrument.lower() for keyword in ['sar', 'coherence', 'backscatter']):
                # Compactación (SAR)
                compactacion_score += weight * confidence_multiplier * (measurement.value / measurement.threshold)
                contributing_instruments.append(f"{instrument} (compactación)")
                explanations.append(f"Compactación: {instrument} mostró {measurement.value:.2f} {measurement.unit}")
                
            elif any(keyword in instrument.lower() for keyword in ['thermal', 'lst', 'temperature']):
                # Térmico
                termico_score += weight * confidence_multiplier * (measurement.value / measurement.threshold)
                contributing_instruments.append(f"{instrument} (térmico)")
                explanations.append(f"Térmico: {instrument} registró {measurement.value:.2f} {measurement.unit}")
                
            elif any(keyword in instrument.lower() for keyword in ['ndvi', 'sentinel2', 'landsat', 'spectral']):
                # Espectral
                espectral_score += weight * confidence_multiplier * (measurement.value / measurement.threshold)
                contributing_instruments.append(f"{instrument} (espectral)")
                explanations.append(f"Espectral: {instrument} indicó {measurement.value:.2f} {measurement.unit}")
        
        # Normalizar scores (máximo 1.0 cada uno)
        forma_score = min(forma_score, 1.0)
        compactacion_score = min(compactacion_score, 1.0)
        termico_score = min(termico_score, 1.0)
        espectral_score = min(espectral_score, 1.0)
        
        # Pesos por tipo de análisis (ajustables por eco-región)
        weights = self._get_analysis_weights(eco_region)
        
        # Calcular score total
        total_score = (
            weights['forma'] * forma_score +
            weights['compactacion'] * compactacion_score +
            weights['termico'] * termico_score +
            weights['espectral'] * espectral_score
        )
        
        # Generar explicación de convergencia
        convergence_reason = self._generate_convergence_explanation(
            forma_score, compactacion_score, termico_score, espectral_score, weights
        )
        
        # Determinar nivel de confianza
        confidence_level = self._determine_confidence_level(total_score, len(contributing_instruments))
        
        return ConvergenceScore(
            total_score=total_score,
            forma_score=forma_score,
            compactacion_score=compactacion_score,
            termico_score=termico_score,
            espectral_score=espectral_score,
            weights=weights,
            explanation=" | ".join(explanations),
            convergence_reason=convergence_reason,
            contributing_instruments=contributing_instruments,
            confidence_level=confidence_level
        )
    
    def analyze_temporal_persistence(self, historical_measurements: List[Dict[str, Any]], 
                                   current_measurement: Dict[str, Any],
                                   temporal_window_years: int = 5) -> PersistenceAnalysis:
        """
        MEJORA CRÍTICA: Persistencia relativa vs absoluta
        
        Evita problemas de:
        - Zonas de abandono reciente
        - Cambios de uso de suelo históricos
        """
        
        # Persistencia absoluta (método tradicional)
        absolute_persistence = len(historical_measurements) >= temporal_window_years
        absolute_duration = len(historical_measurements)
        
        # Persistencia relativa (método mejorado)
        if len(historical_measurements) < 2:
            # Datos insuficientes
            return PersistenceAnalysis(
                temporal_window_years=temporal_window_years,
                absolute_persistence=False,
                absolute_duration_years=0.0,
                relative_persistence_score=0.0,
                geometric_stability_score=0.0,
                volatility_score=1.0,
                persistence_classification="insufficient_data",
                persistence_explanation="Datos históricos insuficientes para análisis de persistencia"
            )
        
        # Calcular persistencia relativa
        relative_score = self._calculate_relative_persistence(historical_measurements, current_measurement)
        
        # Calcular estabilidad geométrica
        geometric_stability = self._calculate_geometric_stability(historical_measurements)
        
        # Calcular volatilidad
        volatility = self._calculate_volatility(historical_measurements)
        
        # Clasificar persistencia
        if relative_score > 0.8 and geometric_stability > 0.7:
            classification = "persistent"
            explanation = "Anomalía persistente y geométricamente estable"
        elif relative_score > 0.6 and geometric_stability > 0.5:
            classification = "intermittent_stable"
            explanation = "Intermitente pero geométricamente estable"
        elif volatility > 0.7:
            classification = "volatile"
            explanation = "Señal volátil - posible falso positivo"
        else:
            classification = "uncertain"
            explanation = "Persistencia incierta - requiere más datos"
        
        return PersistenceAnalysis(
            temporal_window_years=temporal_window_years,
            absolute_persistence=absolute_persistence,
            absolute_duration_years=absolute_duration,
            relative_persistence_score=relative_score,
            geometric_stability_score=geometric_stability,
            volatility_score=volatility,
            persistence_classification=classification,
            persistence_explanation=explanation
        )
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _load_regional_calibrations(self) -> Dict[EcoRegion, RegionalCalibration]:
        """Cargar calibraciones regionales desde configuración"""
        
        calibrations = {}
        
        # Sahara - desierto con excelente visibilidad térmica
        calibrations[EcoRegion.SAHARA] = RegionalCalibration(
            eco_region=EcoRegion.SAHARA,
            base_environment="desert",
            sensor_weight_adjustments={
                "landsat_thermal": 1.3,  # Excelente para Sahara
                "modis_lst": 1.2,
                "sentinel2": 1.1,
                "sar": 0.9  # Menos crítico en desierto
            },
            threshold_adjustments={
                "thermal_delta_k": 0.8,  # Más sensible en Sahara
                "ndvi_delta": 1.2  # Menos vegetación = umbral más alto
            },
            climate_context={
                "aridity_index": 0.95,
                "temperature_range": (5, 50),
                "precipitation_mm": 25
            },
            confidence_factors={
                "thermal": 1.2,
                "optical": 1.1,
                "sar": 0.9
            },
            scientific_rationale="Sahara: excelente visibilidad térmica, mínima vegetación, alta preservación"
        )
        
        # Atacama - desierto extremadamente árido
        calibrations[EcoRegion.ATACAMA] = RegionalCalibration(
            eco_region=EcoRegion.ATACAMA,
            base_environment="desert",
            sensor_weight_adjustments={
                "landsat_thermal": 1.4,  # Extremadamente bueno
                "modis_lst": 1.3,
                "sentinel2": 1.2,
                "sar": 0.8
            },
            threshold_adjustments={
                "thermal_delta_k": 0.7,  # Muy sensible
                "ndvi_delta": 1.5  # Casi sin vegetación
            },
            climate_context={
                "aridity_index": 0.98,
                "temperature_range": (0, 30),
                "precipitation_mm": 15
            },
            confidence_factors={
                "thermal": 1.3,
                "optical": 1.2,
                "sar": 0.8
            },
            scientific_rationale="Atacama: desierto más árido del mundo, preservación excepcional"
        )
        
        # Amazonas húmeda - requiere penetración
        calibrations[EcoRegion.AMAZON_HUMID] = RegionalCalibration(
            eco_region=EcoRegion.AMAZON_HUMID,
            base_environment="forest",
            sensor_weight_adjustments={
                "lidar": 1.5,  # Crítico para penetrar dosel
                "sar": 1.4,    # L-band penetra vegetación
                "sentinel2": 0.7,  # Limitado por nubes
                "landsat": 0.6
            },
            threshold_adjustments={
                "lidar_height_m": 0.8,  # Más sensible
                "ndvi_delta": 1.3,  # Vegetación densa = umbral alto
                "sar_coherence": 0.9  # Más estricto
            },
            climate_context={
                "humidity_index": 0.9,
                "cloud_cover": 0.8,
                "precipitation_mm": 3000
            },
            confidence_factors={
                "lidar": 1.4,
                "sar": 1.3,
                "optical": 0.6
            },
            scientific_rationale="Amazonas húmeda: dosel denso requiere LiDAR y SAR L-band"
        )
        
        # Antártida - condiciones extremas
        calibrations[EcoRegion.ANTARCTICA_INTERIOR] = RegionalCalibration(
            eco_region=EcoRegion.ANTARCTICA_INTERIOR,
            base_environment="polar_ice",
            sensor_weight_adjustments={
                "icesat2": 1.5,  # Único sensor confiable
                "sar": 1.2,      # Penetra hielo seco
                "modis_lst": 0.8,  # Limitado por nubes
                "nsidc": 1.1
            },
            threshold_adjustments={
                "elevation_delta_m": 1.2,  # Más estricto
                "thermal_delta_k": 1.5,    # Difícil detectar
                "ice_concentration": 0.9   # Muy estricto
            },
            climate_context={
                "temperature_range": (-60, -10),
                "ice_thickness_m": 2000,
                "accessibility": "extreme"
            },
            confidence_factors={
                "icesat2": 1.4,
                "sar": 1.1,
                "thermal": 0.7
            },
            scientific_rationale="Antártida interior: condiciones extremas, ICESat-2 crítico"
        )
        
        return calibrations
    
    def _get_default_calibration(self) -> RegionalCalibration:
        """Calibración por defecto para eco-regiones desconocidas"""
        return RegionalCalibration(
            eco_region=EcoRegion.UNKNOWN,
            base_environment="unknown",
            sensor_weight_adjustments={},  # Sin ajustes
            threshold_adjustments={},
            climate_context={},
            confidence_factors={},
            scientific_rationale="Eco-región desconocida - usar calibración base"
        )
    
    def _get_base_sensor_weights(self, environment_type: str) -> Dict[str, float]:
        """Pesos base por tipo de ambiente"""
        
        weights = {
            "desert": {
                "landsat_thermal": 0.3,
                "modis_lst": 0.25,
                "sentinel2": 0.2,
                "sar": 0.15,
                "icesat2": 0.1
            },
            "forest": {
                "lidar": 0.4,
                "sar": 0.3,
                "sentinel2": 0.2,
                "landsat": 0.1
            },
            "polar_ice": {
                "icesat2": 0.4,
                "sar": 0.3,
                "nsidc": 0.2,
                "modis_lst": 0.1
            },
            "shallow_sea": {
                "copernicus_sst": 0.3,
                "sar": 0.3,
                "copernicus_sea_ice": 0.2,
                "bathymetry": 0.2
            }
        }
        
        return weights.get(environment_type, {
            "sentinel2": 0.3,
            "landsat": 0.25,
            "sar": 0.25,
            "modis": 0.2
        })
    
    def _get_confidence_multiplier(self, confidence: str) -> float:
        """Multiplicador por nivel de confianza"""
        return {
            "high": 1.0,
            "moderate": 0.7,
            "low": 0.4,
            "none": 0.0
        }.get(confidence, 0.5)
    
    def _get_analysis_weights(self, eco_region: EcoRegion) -> Dict[str, float]:
        """Pesos por tipo de análisis según eco-región"""
        
        # Pesos por defecto
        default_weights = {
            "forma": 0.3,
            "compactacion": 0.25,
            "termico": 0.25,
            "espectral": 0.2
        }
        
        # Ajustes específicos por eco-región
        if eco_region in [EcoRegion.SAHARA, EcoRegion.ATACAMA]:
            # Desiertos: térmico más importante
            return {"forma": 0.25, "compactacion": 0.2, "termico": 0.35, "espectral": 0.2}
        
        elif eco_region in [EcoRegion.AMAZON_HUMID, EcoRegion.CONGO_HUMID]:
            # Selvas: forma (LiDAR) más importante
            return {"forma": 0.4, "compactacion": 0.3, "termico": 0.15, "espectral": 0.15}
        
        elif eco_region in [EcoRegion.ANTARCTICA_INTERIOR, EcoRegion.GREENLAND]:
            # Polar: forma (ICESat-2) crítico
            return {"forma": 0.45, "compactacion": 0.25, "termico": 0.15, "espectral": 0.15}
        
        return default_weights
    
    def _generate_convergence_explanation(self, forma: float, compactacion: float, 
                                        termico: float, espectral: float,
                                        weights: Dict[str, float]) -> str:
        """Generar explicación de por qué convergen los instrumentos"""
        
        explanations = []
        
        if forma > 0.5:
            explanations.append(f"forma geométrica detectada (score: {forma:.2f})")
        if compactacion > 0.5:
            explanations.append(f"compactación anómala (score: {compactacion:.2f})")
        if termico > 0.5:
            explanations.append(f"anomalía térmica (score: {termico:.2f})")
        if espectral > 0.5:
            explanations.append(f"firma espectral anómala (score: {espectral:.2f})")
        
        if len(explanations) >= 2:
            return f"Convergencia detectada: {' + '.join(explanations)}"
        elif len(explanations) == 1:
            return f"Anomalía detectada: {explanations[0]}"
        else:
            return "Sin convergencia significativa detectada"
    
    def _determine_confidence_level(self, total_score: float, num_instruments: int) -> str:
        """Determinar nivel de confianza basado en score y número de instrumentos"""
        
        if total_score > 0.7 and num_instruments >= 3:
            return "high"
        elif total_score > 0.5 and num_instruments >= 2:
            return "moderate"
        elif total_score > 0.3:
            return "low"
        else:
            return "none"
    
    def _calculate_relative_persistence(self, historical: List[Dict], current: Dict) -> float:
        """Calcular persistencia relativa (no absoluta)"""
        
        if not historical:
            return 0.0
        
        # Comparar con mediciones históricas
        consistent_measurements = 0
        total_comparisons = len(historical)
        
        for hist_measurement in historical:
            # Verificar si la medición actual es consistente con histórica
            if self._measurements_consistent(hist_measurement, current):
                consistent_measurements += 1
        
        return consistent_measurements / total_comparisons if total_comparisons > 0 else 0.0
    
    def _calculate_geometric_stability(self, historical: List[Dict]) -> float:
        """Calcular estabilidad geométrica a lo largo del tiempo"""
        
        if len(historical) < 2:
            return 0.0
        
        # Analizar variabilidad en forma/geometría
        geometric_variations = []
        
        for i in range(1, len(historical)):
            prev = historical[i-1]
            curr = historical[i]
            
            # Calcular variación geométrica (simplificado)
            variation = abs(curr.get('geometric_score', 0.5) - prev.get('geometric_score', 0.5))
            geometric_variations.append(variation)
        
        # Estabilidad = 1 - variabilidad promedio
        avg_variation = np.mean(geometric_variations) if geometric_variations else 0.5
        return max(0.0, 1.0 - avg_variation)
    
    def _calculate_volatility(self, historical: List[Dict]) -> float:
        """Calcular volatilidad de la señal"""
        
        if len(historical) < 3:
            return 0.5  # Volatilidad media por defecto
        
        # Extraer valores de intensidad
        intensities = [m.get('intensity', 0.5) for m in historical]
        
        # Calcular desviación estándar normalizada
        std_dev = np.std(intensities)
        mean_intensity = np.mean(intensities)
        
        # Volatilidad = desviación estándar / media (normalizada)
        if mean_intensity > 0:
            volatility = std_dev / mean_intensity
            return min(volatility, 1.0)  # Limitar a 1.0
        
        return 0.5
    
    def _measurements_consistent(self, hist: Dict, current: Dict) -> bool:
        """Verificar si dos mediciones son consistentes"""
        
        # Tolerancia para considerar mediciones consistentes
        tolerance = 0.3
        
        hist_intensity = hist.get('intensity', 0.5)
        curr_intensity = current.get('intensity', 0.5)
        
        return abs(hist_intensity - curr_intensity) <= tolerance
    
    def _load_eco_region_boundaries(self) -> Dict:
        """Cargar límites de eco-regiones (placeholder)"""
        return {}
