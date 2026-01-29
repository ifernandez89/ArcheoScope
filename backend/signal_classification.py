#!/usr/bin/env python3
"""
Signal Classification - Separación clara de señales
===================================================

PRIORIDAD 2: Separar OBSERVED vs INFERRED vs CONTEXTUAL

Propósito:
- Transparencia científica total
- Score paper-ready
- Credibilidad x2
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class SignalType(Enum):
    """Tipo de señal arqueológica."""
    
    OBSERVED = "observed"        # Medición directa de sensor
    INFERRED = "inferred"        # Inferencia de modelo (DIL, TAS, etc.)
    CONTEXTUAL = "contextual"    # Conocimiento previo (clima, geología, etc.)


class EvidenceStrength(Enum):
    """Fuerza de la evidencia."""
    
    STRONG = "strong"      # Confianza > 0.8
    MEDIUM = "medium"      # Confianza 0.5-0.8
    WEAK = "weak"          # Confianza < 0.5
    NONE = "none"          # Sin evidencia


@dataclass
class ArchaeologicalSignal:
    """
    Señal arqueológica clasificada.
    
    Atributos:
        signal_type: Tipo de señal (OBSERVED/INFERRED/CONTEXTUAL)
        instrument: Nombre del instrumento o método
        value: Valor de la señal
        confidence: Confianza [0-1]
        evidence_strength: Fuerza de la evidencia
        description: Descripción de la señal
    """
    
    signal_type: SignalType
    instrument: str
    value: float
    confidence: float
    evidence_strength: EvidenceStrength
    description: str
    
    @classmethod
    def from_instrument_measurement(cls, measurement, signal_type: SignalType):
        """Crear señal desde medición instrumental."""
        
        # Determinar fuerza de evidencia
        if measurement.confidence > 0.8:
            strength = EvidenceStrength.STRONG
        elif measurement.confidence > 0.5:
            strength = EvidenceStrength.MEDIUM
        else:
            strength = EvidenceStrength.WEAK
        
        return cls(
            signal_type=signal_type,
            instrument=measurement.instrument_name,
            value=measurement.value,
            confidence=measurement.confidence,
            evidence_strength=strength,
            description=f"{measurement.measurement_type} from {measurement.source}"
        )


def classify_instrument_signal(instrument_name: str) -> SignalType:
    """
    Clasificar tipo de señal según instrumento.
    
    Args:
        instrument_name: Nombre del instrumento
    
    Returns:
        SignalType correspondiente
    """
    
    # Señales OBSERVADAS (sensores directos)
    observed_instruments = {
        'sentinel_2_ndvi',
        'sentinel_1_sar',
        'landsat_thermal',
        'srtm_elevation',
        'modis_lst',
        'icesat2',
        'viirs_thermal',
        'palsar_backscatter'
    }
    
    # Señales INFERIDAS (modelos)
    inferred_instruments = {
        'dil_analysis',           # Deep Inference Layer
        'tas_analysis',           # Temporal Archaeological Signature
        'etp_analysis',           # Environmental Tomographic Profile
        'void_detection',         # Subsurface Void Detection
        'water_archaeology'       # Water Archaeology Detection
    }
    
    # Señales CONTEXTUALES (conocimiento previo)
    contextual_instruments = {
        'era5_climate',
        'chirps_precipitation',
        'copernicus_sst',
        'geological_context',
        'historical_hydrography'
    }
    
    if instrument_name in observed_instruments:
        return SignalType.OBSERVED
    elif instrument_name in inferred_instruments:
        return SignalType.INFERRED
    elif instrument_name in contextual_instruments:
        return SignalType.CONTEXTUAL
    else:
        # Default: OBSERVED si es un sensor desconocido
        logger.warning(f"Instrumento desconocido: {instrument_name}, clasificando como OBSERVED")
        return SignalType.OBSERVED


def calculate_ess_with_transparency(signals: List[ArchaeologicalSignal]) -> Dict[str, Any]:
    """
    Calcular ESS con transparencia total.
    
    Separa:
    - Señales observadas (sensores reales)
    - Señales inferidas (modelos)
    - Conocimiento contextual
    
    Args:
        signals: Lista de señales arqueológicas
    
    Returns:
        Dict con ESS y breakdown completo
    """
    
    # Separar señales por tipo
    observed_signals = [s for s in signals if s.signal_type == SignalType.OBSERVED]
    inferred_signals = [s for s in signals if s.signal_type == SignalType.INFERRED]
    contextual_signals = [s for s in signals if s.signal_type == SignalType.CONTEXTUAL]
    
    # Score base (solo observados)
    if observed_signals:
        # Promedio ponderado por confianza
        total_weight = sum(s.confidence for s in observed_signals)
        if total_weight > 0:
            base_score = sum(s.value * s.confidence for s in observed_signals) / total_weight
        else:
            base_score = 0.0
    else:
        base_score = 0.0
    
    # Boost por inferencia (máximo 20%)
    if inferred_signals:
        inference_contribution = sum(s.value * s.confidence for s in inferred_signals) / len(inferred_signals)
        inference_boost = min(inference_contribution * 0.2, 0.2)  # Cap at 20%
    else:
        inference_boost = 0.0
    
    # Ajuste contextual (±10%)
    if contextual_signals:
        context_contribution = sum(s.value * s.confidence for s in contextual_signals) / len(contextual_signals)
        # Puede ser positivo o negativo
        context_adjustment = max(-0.1, min(0.1, (context_contribution - 0.5) * 0.2))
    else:
        context_adjustment = 0.0
    
    # Score final
    final_score = max(0.0, min(1.0, base_score + inference_boost + context_adjustment))
    
    # Clasificar evidencia
    strong_observed = sum(1 for s in observed_signals if s.evidence_strength == EvidenceStrength.STRONG)
    medium_observed = sum(1 for s in observed_signals if s.evidence_strength == EvidenceStrength.MEDIUM)
    weak_observed = sum(1 for s in observed_signals if s.evidence_strength == EvidenceStrength.WEAK)
    
    # Interpretación
    if strong_observed >= 3:
        interpretation = f"Score {final_score:.2f} basado en {strong_observed} sensores de alta confianza"
    elif strong_observed + medium_observed >= 2:
        interpretation = f"Score {final_score:.2f} basado en {len(observed_signals)} sensores reales"
    elif len(observed_signals) > 0:
        interpretation = f"Score {final_score:.2f} basado en {len(observed_signals)} sensores (confianza limitada)"
    else:
        interpretation = f"Score {final_score:.2f} basado solo en inferencia (sin sensores directos)"
    
    if len(inferred_signals) > 0:
        interpretation += f" + inferencia {', '.join(s.instrument for s in inferred_signals)}"
    
    return {
        "ess_score": round(final_score, 3),
        "breakdown": {
            "base_score": round(base_score, 3),
            "inference_boost": round(inference_boost, 3),
            "context_adjustment": round(context_adjustment, 3),
            "observed_sensors": len(observed_signals),
            "inferred_components": len(inferred_signals),
            "contextual_factors": len(contextual_signals)
        },
        "evidence_quality": {
            "strong": strong_observed,
            "medium": medium_observed,
            "weak": weak_observed
        },
        "transparency": {
            "observed_instruments": [s.instrument for s in observed_signals],
            "inferred_methods": [s.instrument for s in inferred_signals],
            "contextual_sources": [s.instrument for s in contextual_signals]
        },
        "interpretation": interpretation,
        "paper_ready": len(observed_signals) >= 2 and strong_observed >= 1
    }


def generate_evidence_report(signals: List[ArchaeologicalSignal]) -> str:
    """
    Generar reporte de evidencia en texto.
    
    Args:
        signals: Lista de señales
    
    Returns:
        Reporte en texto
    """
    
    observed = [s for s in signals if s.signal_type == SignalType.OBSERVED]
    inferred = [s for s in signals if s.signal_type == SignalType.INFERRED]
    contextual = [s for s in signals if s.signal_type == SignalType.CONTEXTUAL]
    
    report = []
    
    report.append("=== EVIDENCIA ARQUEOLÓGICA ===\n")
    
    if observed:
        report.append(f"SEÑALES OBSERVADAS ({len(observed)}):")
        for s in observed:
            report.append(f"  • {s.instrument}: {s.value:.3f} (conf: {s.confidence:.2f}, {s.evidence_strength.value})")
    
    if inferred:
        report.append(f"\nSEÑALES INFERIDAS ({len(inferred)}):")
        for s in inferred:
            report.append(f"  • {s.instrument}: {s.value:.3f} (conf: {s.confidence:.2f})")
    
    if contextual:
        report.append(f"\nCONTEXTO ({len(contextual)}):")
        for s in contextual:
            report.append(f"  • {s.instrument}: {s.value:.3f} (conf: {s.confidence:.2f})")
    
    return "\n".join(report)


if __name__ == "__main__":
    # Test
    
    # Crear señales de ejemplo
    signals = [
        ArchaeologicalSignal(
            signal_type=SignalType.OBSERVED,
            instrument="sentinel_2_ndvi",
            value=0.45,
            confidence=0.95,
            evidence_strength=EvidenceStrength.STRONG,
            description="Vegetation anomaly"
        ),
        ArchaeologicalSignal(
            signal_type=SignalType.OBSERVED,
            instrument="sentinel_1_sar",
            value=0.52,
            confidence=0.85,
            evidence_strength=EvidenceStrength.STRONG,
            description="Subsurface anomaly"
        ),
        ArchaeologicalSignal(
            signal_type=SignalType.INFERRED,
            instrument="dil_analysis",
            value=0.38,
            confidence=0.75,
            evidence_strength=EvidenceStrength.MEDIUM,
            description="Deep inference layer"
        ),
        ArchaeologicalSignal(
            signal_type=SignalType.CONTEXTUAL,
            instrument="era5_climate",
            value=0.60,
            confidence=0.90,
            evidence_strength=EvidenceStrength.STRONG,
            description="Favorable preservation"
        )
    ]
    
    # Calcular ESS con transparencia
    result = calculate_ess_with_transparency(signals)
    
    print("ESS Score:", result['ess_score'])
    print("Breakdown:", result['breakdown'])
    print("Interpretation:", result['interpretation'])
    print("Paper-ready:", result['paper_ready'])
    
    print("\n" + generate_evidence_report(signals))
