#!/usr/bin/env python3
"""
Coverage Assessment - Separar Cobertura de Señal
================================================

PROBLEMA CRÍTICO:
- Menos sensores ⇒ menos features ⇒ score más plano
- Usuario ve ⚠️⚠️⚠️ ⇒ desconfianza cognitiva
- Confunde ausencia de datos con ausencia de señal

SOLUCIÓN:
1. data_coverage_score ∈ [0,1] - Qué tan completa es la cobertura
2. confidence_level - Qué tan confiable es el análisis
3. signal_strength - Qué tan fuerte es la señal detectada

SEPARACIÓN CLAVE:
- Cobertura baja + señal fuerte = Candidato válido con datos limitados
- Cobertura alta + señal débil = Zona bien cubierta pero sin interés
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class CoverageQuality(Enum):
    """Calidad de cobertura instrumental."""
    FULL = "full"           # ≥80% instrumentos disponibles
    GOOD = "good"           # 60-80%
    PARTIAL = "partial"     # 40-60%
    MINIMAL = "minimal"     # 20-40%
    INSUFFICIENT = "insufficient"  # <20%


class InstrumentCategory(Enum):
    """Categorías de instrumentos por importancia."""
    CORE = "core"           # Esenciales (Sentinel-2, Sentinel-1, DEM, Thermal)
    IMPORTANT = "important" # Importantes (ICESat-2, MODIS, ERA5)
    OPTIONAL = "optional"   # Opcionales (VIIRS, CHIRPS, PALSAR)


@dataclass
class CoverageAssessment:
    """Evaluación de cobertura instrumental."""
    coverage_score: float  # 0-1
    coverage_quality: CoverageQuality
    instruments_available: int
    instruments_total: int
    core_coverage: float  # 0-1 (solo CORE)
    missing_instruments: List[str]
    missing_categories: Dict[str, List[str]]
    confidence_penalty: float  # 0-1 (penalización por falta de datos)
    message: str  # Mensaje UX


# Definir instrumentos por categoría
INSTRUMENT_CATEGORIES = {
    # CORE: Esenciales para cualquier análisis
    InstrumentCategory.CORE: [
        'sentinel_2_ndvi',
        'sentinel_1_sar',
        'landsat_thermal',
        'srtm_elevation',
    ],
    
    # IMPORTANT: Mejoran significativamente el análisis
    InstrumentCategory.IMPORTANT: [
        'icesat2',
        'modis_lst',
        'era5_climate',
        'opentopography',
    ],
    
    # OPTIONAL: Contexto adicional
    InstrumentCategory.OPTIONAL: [
        'viirs_thermal',
        'chirps_precipitation',
        'palsar_backscatter',
        'nsidc_sea_ice',
        'copernicus_sst',
    ]
}


def calculate_coverage_score(
    instruments_available: List[str],
    instruments_total: Optional[List[str]] = None
) -> CoverageAssessment:
    """
    Calcular score de cobertura instrumental.
    
    Args:
        instruments_available: Lista de instrumentos con datos válidos
        instruments_total: Lista de todos los instrumentos posibles
    
    Returns:
        CoverageAssessment con métricas detalladas
    """
    
    # Normalizar nombres de instrumentos
    available_normalized = [inst.lower().replace(' ', '_') for inst in instruments_available]
    
    # Contar por categoría
    core_available = 0
    core_total = len(INSTRUMENT_CATEGORIES[InstrumentCategory.CORE])
    
    important_available = 0
    important_total = len(INSTRUMENT_CATEGORIES[InstrumentCategory.IMPORTANT])
    
    optional_available = 0
    optional_total = len(INSTRUMENT_CATEGORIES[InstrumentCategory.OPTIONAL])
    
    missing_by_category = {
        'core': [],
        'important': [],
        'optional': []
    }
    
    # Verificar CORE
    for inst in INSTRUMENT_CATEGORIES[InstrumentCategory.CORE]:
        if any(inst in avail for avail in available_normalized):
            core_available += 1
        else:
            missing_by_category['core'].append(inst)
    
    # Verificar IMPORTANT
    for inst in INSTRUMENT_CATEGORIES[InstrumentCategory.IMPORTANT]:
        if any(inst in avail for avail in available_normalized):
            important_available += 1
        else:
            missing_by_category['important'].append(inst)
    
    # Verificar OPTIONAL
    for inst in INSTRUMENT_CATEGORIES[InstrumentCategory.OPTIONAL]:
        if any(inst in avail for avail in available_normalized):
            optional_available += 1
        else:
            missing_by_category['optional'].append(inst)
    
    # Calcular coverage score ponderado
    core_coverage = core_available / core_total if core_total > 0 else 0
    important_coverage = important_available / important_total if important_total > 0 else 0
    optional_coverage = optional_available / optional_total if optional_total > 0 else 0
    
    # Pesos: CORE 60%, IMPORTANT 30%, OPTIONAL 10%
    coverage_score = (
        core_coverage * 0.60 +
        important_coverage * 0.30 +
        optional_coverage * 0.10
    )
    
    # Determinar calidad
    if coverage_score >= 0.80:
        quality = CoverageQuality.FULL
    elif coverage_score >= 0.60:
        quality = CoverageQuality.GOOD
    elif coverage_score >= 0.40:
        quality = CoverageQuality.PARTIAL
    elif coverage_score >= 0.20:
        quality = CoverageQuality.MINIMAL
    else:
        quality = CoverageQuality.INSUFFICIENT
    
    # Calcular penalización por confianza
    # Si CORE está completo (≥75%), no penalizar
    if core_coverage >= 0.75:
        confidence_penalty = 0.0
    else:
        # Penalizar proporcionalmente a CORE faltante
        confidence_penalty = (1.0 - core_coverage) * 0.3  # Máximo 30% penalización
    
    # Generar mensaje UX
    message = _generate_coverage_message(
        quality, core_coverage, core_available, core_total,
        important_available, optional_available,
        missing_by_category
    )
    
    total_available = core_available + important_available + optional_available
    total_instruments = core_total + important_total + optional_total
    
    logger.info(f"📊 Coverage Assessment:")
    logger.info(f"   Score: {coverage_score:.2f} ({quality.value})")
    logger.info(f"   CORE: {core_available}/{core_total} ({core_coverage:.0%})")
    logger.info(f"   IMPORTANT: {important_available}/{important_total}")
    logger.info(f"   OPTIONAL: {optional_available}/{optional_total}")
    logger.info(f"   Confidence penalty: {confidence_penalty:.2f}")
    
    return CoverageAssessment(
        coverage_score=coverage_score,
        coverage_quality=quality,
        instruments_available=total_available,
        instruments_total=total_instruments,
        core_coverage=core_coverage,
        missing_instruments=missing_by_category['core'] + missing_by_category['important'],
        missing_categories=missing_by_category,
        confidence_penalty=confidence_penalty,
        message=message
    )


def _generate_coverage_message(
    quality: CoverageQuality,
    core_coverage: float,
    core_available: int,
    core_total: int,
    important_available: int,
    optional_available: int,
    missing_by_category: Dict[str, List[str]]
) -> str:
    """Generar mensaje UX sobre cobertura."""
    
    if quality == CoverageQuality.FULL:
        return f"Cobertura completa ({core_available}/{core_total} sensores CORE). Análisis de alta confianza."
    
    elif quality == CoverageQuality.GOOD:
        return f"Cobertura buena ({core_available}/{core_total} sensores CORE, +{important_available} adicionales). Análisis confiable."
    
    elif quality == CoverageQuality.PARTIAL:
        if core_coverage >= 0.75:
            # CORE completo pero faltan IMPORTANT
            return f"Cobertura parcial pero sensores CORE completos ({core_available}/{core_total}). Señales detectadas son confiables."
        else:
            # Faltan algunos CORE
            missing_core = ', '.join(missing_by_category['core'][:2])
            return f"Cobertura parcial ({core_available}/{core_total} sensores CORE). Faltan: {missing_core}. Señales detectadas requieren validación."
    
    elif quality == CoverageQuality.MINIMAL:
        missing_core = ', '.join(missing_by_category['core'][:3])
        return f"Cobertura mínima ({core_available}/{core_total} sensores CORE). Faltan: {missing_core}. Análisis preliminar únicamente."
    
    else:  # INSUFFICIENT
        return f"Cobertura insuficiente ({core_available}/{core_total} sensores CORE). Análisis no confiable."


def separate_confidence_and_signal(
    measurements: List[Dict[str, Any]],
    coverage_assessment: CoverageAssessment
) -> Dict[str, float]:
    """
    Separar confianza de fuerza de señal.
    
    CLAVE: No confundir "pocos datos" con "señal débil"
    
    Args:
        measurements: Lista de mediciones instrumentales
        coverage_assessment: Evaluación de cobertura
    
    Returns:
        Dict con confidence_level y signal_strength separados
    """
    
    # 1. Calcular fuerza de señal (independiente de cobertura)
    signal_values = []
    for m in measurements:
        if isinstance(m, dict) and 'value' in m:
            value = m.get('value', 0)
            threshold = m.get('threshold', 1.0)
            
            if threshold > 0:
                # Señal normalizada (cuánto se desvía del umbral)
                signal_strength = abs(value - threshold) / threshold
                signal_values.append(signal_strength)
    
    if signal_values:
        # Fuerza de señal = máxima desviación detectada
        signal_strength = min(1.0, max(signal_values))
    else:
        signal_strength = 0.0
    
    # 2. Calcular nivel de confianza (depende de cobertura)
    base_confidence = 0.5  # Confianza base
    
    # Aumentar confianza si CORE está completo
    if coverage_assessment.core_coverage >= 0.75:
        base_confidence += 0.3
    
    # Aumentar confianza si hay múltiples sensores convergiendo
    if len(signal_values) >= 3:
        base_confidence += 0.2
    
    # Aplicar penalización por cobertura
    confidence_level = base_confidence * (1.0 - coverage_assessment.confidence_penalty)
    confidence_level = min(1.0, max(0.0, confidence_level))
    
    logger.info(f"📊 Confidence vs Signal:")
    logger.info(f"   Confidence level: {confidence_level:.2f} (qué tan confiable)")
    logger.info(f"   Signal strength: {signal_strength:.2f} (qué tan fuerte)")
    logger.info(f"   Coverage factor: {1.0 - coverage_assessment.confidence_penalty:.2f}")
    
    return {
        'confidence_level': confidence_level,
        'signal_strength': signal_strength,
        'coverage_factor': 1.0 - coverage_assessment.confidence_penalty,
        'interpretation': _interpret_confidence_signal(confidence_level, signal_strength)
    }


def _interpret_confidence_signal(confidence: float, signal: float) -> str:
    """Interpretar combinación de confianza y señal."""
    
    if confidence >= 0.7 and signal >= 0.6:
        return "🟢 Alta confianza + señal fuerte - Candidato prioritario"
    
    elif confidence >= 0.5 and signal >= 0.6:
        return "🟡 Confianza moderada + señal fuerte - Candidato válido con datos limitados"
    
    elif confidence >= 0.7 and signal < 0.4:
        return "🔵 Alta confianza + señal débil - Zona bien cubierta sin interés arqueológico"
    
    elif confidence < 0.5 and signal >= 0.6:
        return "🟠 Baja confianza + señal fuerte - Requiere más datos para validar"
    
    else:
        return "⚪ Confianza y señal bajas - No concluyente"


if __name__ == "__main__":
    # Test
    print("🧪 Coverage Assessment - Test")
    print("=" * 80)
    
    # Test 1: Cobertura completa
    print("\n1. Test: Cobertura completa")
    instruments = [
        'sentinel_2_ndvi',
        'sentinel_1_sar',
        'landsat_thermal',
        'srtm_elevation',
        'icesat2',
        'modis_lst'
    ]
    
    assessment = calculate_coverage_score(instruments)
    print(f"   Score: {assessment.coverage_score:.2f}")
    print(f"   Quality: {assessment.coverage_quality.value}")
    print(f"   Message: {assessment.message}")
    
    # Test 2: Cobertura parcial pero CORE completo
    print("\n2. Test: Cobertura parcial (CORE completo)")
    instruments = [
        'sentinel_2_ndvi',
        'sentinel_1_sar',
        'landsat_thermal',
        'srtm_elevation'
    ]
    
    assessment = calculate_coverage_score(instruments)
    print(f"   Score: {assessment.coverage_score:.2f}")
    print(f"   Quality: {assessment.coverage_quality.value}")
    print(f"   Message: {assessment.message}")
    print(f"   Confidence penalty: {assessment.confidence_penalty:.2f}")
    
    # Test 3: Separar confianza y señal
    print("\n3. Test: Confianza vs Señal")
    measurements = [
        {'value': 0.8, 'threshold': 0.5},  # Señal fuerte
        {'value': 0.7, 'threshold': 0.5},  # Señal fuerte
        {'value': 0.6, 'threshold': 0.5},  # Señal moderada
    ]
    
    result = separate_confidence_and_signal(measurements, assessment)
    print(f"   Confidence: {result['confidence_level']:.2f}")
    print(f"   Signal: {result['signal_strength']:.2f}")
    print(f"   {result['interpretation']}")
    
    print("\n" + "=" * 80)
    print("✅ Test completado")
