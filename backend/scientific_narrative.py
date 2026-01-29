#!/usr/bin/env python3
"""
Scientific Narrative Generator - Conclusión Explícita
====================================================

PROBLEMA:
- Sistema sabe que es interesante pero habla con miedo
- Falta conclusión explícita y accionable
- Usuario queda sin saber qué hacer

SOLUCIÓN:
- Narrativa científica clara y justificada
- Recomendaciones accionables
- Nivel de confianza explícito

EJEMPLO:
"Candidato arqueológico de baja visibilidad superficial. 
Alta estabilidad térmica multidecadal (0.93) sugiere estructuras 
enterradas o uso humano prolongado no monumental. 
Recomendado para análisis focalizado SAR + térmico de alta resolución."
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SiteClassification(Enum):
    """Clasificación de sitio arqueológico."""
    HIGH_CONFIDENCE = "high_confidence"           # Alta confianza
    MODERATE_CANDIDATE = "moderate_candidate"     # Candidato moderado
    LOW_VISIBILITY = "low_visibility"             # Baja visibilidad superficial
    THERMAL_ANCHOR = "thermal_anchor"             # Zona de anclaje térmico
    STRUCTURAL_ANOMALY = "structural_anomaly"     # Anomalía estructural
    MONITORING_ZONE = "monitoring_zone"           # Zona de monitoreo
    INSUFFICIENT_DATA = "insufficient_data"       # Datos insuficientes
    NO_INTEREST = "no_interest"                   # Sin interés arqueológico


@dataclass
class ArchaeologicalNarrative:
    """Narrativa arqueológica completa."""
    classification: SiteClassification
    confidence: float  # 0-1
    main_statement: str  # Declaración principal
    evidence: List[str]  # Lista de evidencias
    interpretation: str  # Interpretación científica
    recommendations: List[str]  # Recomendaciones accionables
    priority: str  # HIGH, MEDIUM, LOW
    full_narrative: str  # Narrativa completa


def generate_archaeological_narrative(
    thermal_stability: float,
    sar_structural_index: float,
    icesat2_rugosity: Optional[float],
    ndvi_persistence: float,
    tas_score: float,
    coverage_score: float,
    environment_type: str,
    flags: List[str]
) -> ArchaeologicalNarrative:
    """
    Generar narrativa arqueológica explícita y accionable.
    
    Args:
        thermal_stability: Estabilidad térmica (0-1)
        sar_structural_index: Índice estructural SAR (0-1)
        icesat2_rugosity: Rugosidad ICESat-2 (metros, opcional)
        ndvi_persistence: Persistencia NDVI (0-1)
        tas_score: Score TAS (0-1)
        coverage_score: Score de cobertura (0-1)
        environment_type: Tipo de ambiente
        flags: Flags especiales (THERMAL_ANCHOR_ZONE, etc.)
    
    Returns:
        ArchaeologicalNarrative completa
    """
    
    logger.info("📝 Generando narrativa arqueológica...")
    
    # 1. Determinar clasificación principal
    classification = _determine_classification(
        thermal_stability, sar_structural_index, tas_score, flags
    )
    
    # 2. Calcular confianza
    confidence = _calculate_narrative_confidence(
        thermal_stability, sar_structural_index, coverage_score, tas_score
    )
    
    # 3. Generar declaración principal
    main_statement = _generate_main_statement(
        classification, thermal_stability, environment_type
    )
    
    # 4. Recopilar evidencias
    evidence = _collect_evidence(
        thermal_stability, sar_structural_index, icesat2_rugosity,
        ndvi_persistence, tas_score, environment_type
    )
    
    # 5. Generar interpretación
    interpretation = _generate_interpretation(
        classification, thermal_stability, sar_structural_index,
        environment_type, flags
    )
    
    # 6. Generar recomendaciones accionables
    recommendations = _generate_recommendations(
        classification, thermal_stability, sar_structural_index,
        icesat2_rugosity, coverage_score
    )
    
    # 7. Determinar prioridad
    priority = _determine_priority(
        classification, thermal_stability, sar_structural_index, confidence
    )
    
    # 8. Ensamblar narrativa completa
    full_narrative = _assemble_full_narrative(
        main_statement, evidence, interpretation, recommendations, priority
    )
    
    logger.info(f"   Clasificación: {classification.value}")
    logger.info(f"   Confianza: {confidence:.2f}")
    logger.info(f"   Prioridad: {priority}")
    
    return ArchaeologicalNarrative(
        classification=classification,
        confidence=confidence,
        main_statement=main_statement,
        evidence=evidence,
        interpretation=interpretation,
        recommendations=recommendations,
        priority=priority,
        full_narrative=full_narrative
    )


def _determine_classification(
    thermal_stability: float,
    sar_structural_index: float,
    tas_score: float,
    flags: List[str]
) -> SiteClassification:
    """Determinar clasificación principal del sitio."""
    
    if 'THERMAL_ANCHOR_ZONE' in flags:
        return SiteClassification.THERMAL_ANCHOR
    
    if thermal_stability > 0.9 or sar_structural_index > 0.7:
        return SiteClassification.HIGH_CONFIDENCE
    
    if thermal_stability > 0.7 or sar_structural_index > 0.5:
        if tas_score > 0.5:
            return SiteClassification.MODERATE_CANDIDATE
        else:
            return SiteClassification.LOW_VISIBILITY
    
    if sar_structural_index > 0.4:
        return SiteClassification.STRUCTURAL_ANOMALY
    
    if tas_score > 0.4:
        return SiteClassification.MONITORING_ZONE
    
    return SiteClassification.NO_INTEREST


def _calculate_narrative_confidence(
    thermal_stability: float,
    sar_structural_index: float,
    coverage_score: float,
    tas_score: float
) -> float:
    """Calcular confianza de la narrativa."""
    
    # Confianza basada en señales fuertes
    signal_confidence = (thermal_stability * 0.4 + sar_structural_index * 0.4 + tas_score * 0.2)
    
    # Ajustar por cobertura
    coverage_factor = min(1.0, coverage_score + 0.3)  # Mínimo 30% incluso con baja cobertura
    
    confidence = signal_confidence * coverage_factor
    
    return min(1.0, confidence)


def _generate_main_statement(
    classification: SiteClassification,
    thermal_stability: float,
    environment_type: str
) -> str:
    """Generar declaración principal."""
    
    if classification == SiteClassification.THERMAL_ANCHOR:
        return f"Zona de anclaje térmico detectada (estabilidad {thermal_stability:.2f})"
    
    elif classification == SiteClassification.HIGH_CONFIDENCE:
        return "Candidato arqueológico de alta confianza"
    
    elif classification == SiteClassification.MODERATE_CANDIDATE:
        return "Candidato arqueológico moderado"
    
    elif classification == SiteClassification.LOW_VISIBILITY:
        if environment_type == "arid":
            return "Candidato arqueológico de baja visibilidad superficial (ambiente árido)"
        else:
            return "Candidato arqueológico de baja visibilidad superficial"
    
    elif classification == SiteClassification.STRUCTURAL_ANOMALY:
        return "Anomalía estructural detectada"
    
    elif classification == SiteClassification.MONITORING_ZONE:
        return "Zona de interés para monitoreo continuo"
    
    else:
        return "Sin evidencia arqueológica significativa"


def _collect_evidence(
    thermal_stability: float,
    sar_structural_index: float,
    icesat2_rugosity: Optional[float],
    ndvi_persistence: float,
    tas_score: float,
    environment_type: str
) -> List[str]:
    """Recopilar evidencias detectadas."""
    
    evidence = []
    
    if thermal_stability > 0.9:
        evidence.append(
            f"Alta estabilidad térmica multidecadal ({thermal_stability:.2f}) "
            "sugiere estructuras enterradas o uso humano prolongado"
        )
    elif thermal_stability > 0.7:
        evidence.append(
            f"Estabilidad térmica significativa ({thermal_stability:.2f}) "
            "indica posible masa enterrada"
        )
    
    if sar_structural_index > 0.5:
        evidence.append(
            f"Anomalías estructurales SAR ({sar_structural_index:.2f}) "
            "indican heterogeneidad subsuperficial coherente"
        )
    
    if icesat2_rugosity and icesat2_rugosity > 10:
        evidence.append(
            f"Rugosidad superficial elevada ({icesat2_rugosity:.1f}m) "
            "sugiere irregularidades del terreno (posibles estructuras erosionadas)"
        )
    
    if ndvi_persistence < 0.1 and environment_type == "arid":
        evidence.append(
            "NDVI muy bajo (suelo desnudo) - Detección basada en señales térmicas y SAR"
        )
    
    if tas_score > 0.5:
        evidence.append(
            f"Firma arqueológica temporal (TAS {tas_score:.2f}) "
            "indica persistencia de anomalías"
        )
    
    if not evidence:
        evidence.append("Señales arqueológicas débiles o ausentes")
    
    return evidence


def _generate_interpretation(
    classification: SiteClassification,
    thermal_stability: float,
    sar_structural_index: float,
    environment_type: str,
    flags: List[str]
) -> str:
    """Generar interpretación científica."""
    
    if classification == SiteClassification.THERMAL_ANCHOR:
        return (
            "La alta estabilidad térmica es consistente con estructuras enterradas "
            "o uso humano prolongado no monumental. Típico de ocupaciones antiguas "
            "con arquitectura erosionada o rellenos artificiales."
        )
    
    elif classification == SiteClassification.HIGH_CONFIDENCE:
        return (
            "Múltiples señales convergentes (térmica + estructural) indican "
            "alta probabilidad de presencia arqueológica. Requiere validación "
            "de campo para caracterización precisa."
        )
    
    elif classification == SiteClassification.LOW_VISIBILITY:
        return (
            "Señales subsuperficiales detectadas sin evidencia superficial clara. "
            "Consistente con estructuras erosionadas, enterradas o uso humano "
            "prolongado sin arquitectura monumental."
        )
    
    elif classification == SiteClassification.STRUCTURAL_ANOMALY:
        return (
            "Anomalías estructurales SAR sugieren heterogeneidad subsuperficial. "
            "Puede indicar estructuras enterradas, rellenos o modificación antrópica del terreno."
        )
    
    else:
        return "Señales insuficientes para interpretación arqueológica concluyente."


def _generate_recommendations(
    classification: SiteClassification,
    thermal_stability: float,
    sar_structural_index: float,
    icesat2_rugosity: Optional[float],
    coverage_score: float
) -> List[str]:
    """Generar recomendaciones accionables."""
    
    recommendations = []
    
    # Recomendaciones por señal detectada
    if thermal_stability > 0.8:
        recommendations.append("Análisis térmico de alta resolución (día/noche)")
        recommendations.append("GPR (Ground Penetrating Radar) para validación subsuperficial")
    
    if sar_structural_index > 0.5:
        recommendations.append("SAR multi-temporal (series largas para coherencia)")
        recommendations.append("SAR multi-ángulo (diferentes geometrías de adquisición)")
    
    if icesat2_rugosity and icesat2_rugosity > 10:
        recommendations.append("LIDAR aéreo de alta densidad (<1m resolución)")
        recommendations.append("Análisis microtopográfico fino")
    
    # Recomendaciones por clasificación
    if classification in [SiteClassification.HIGH_CONFIDENCE, SiteClassification.THERMAL_ANCHOR]:
        recommendations.append("Magnetometría para detectar estructuras de combustión")
        recommendations.append("Prospección de campo prioritaria")
    
    # Si cobertura baja, recomendar más datos
    if coverage_score < 0.5:
        recommendations.append("Adquirir datos adicionales (ICESat-2, MODIS, ERA5)")
    
    if not recommendations:
        recommendations.append("Monitoreo continuo con sensores disponibles")
    
    return recommendations


def _determine_priority(
    classification: SiteClassification,
    thermal_stability: float,
    sar_structural_index: float,
    confidence: float
) -> str:
    """Determinar prioridad de investigación."""
    
    if classification == SiteClassification.THERMAL_ANCHOR:
        return "HIGH"
    
    if classification == SiteClassification.HIGH_CONFIDENCE:
        return "HIGH"
    
    if thermal_stability > 0.8 or sar_structural_index > 0.6:
        return "HIGH"
    
    if confidence > 0.6:
        return "MEDIUM"
    
    return "LOW"


def _assemble_full_narrative(
    main_statement: str,
    evidence: List[str],
    interpretation: str,
    recommendations: List[str],
    priority: str
) -> str:
    """Ensamblar narrativa completa."""
    
    parts = []
    
    # 1. Declaración principal
    parts.append(main_statement + ".")
    
    # 2. Evidencias
    if evidence:
        parts.append("\n\nEvidencias detectadas:")
        for i, ev in enumerate(evidence, 1):
            parts.append(f"  {i}. {ev}")
    
    # 3. Interpretación
    parts.append(f"\n\nInterpretación: {interpretation}")
    
    # 4. Recomendaciones
    if recommendations:
        parts.append("\n\nRecomendaciones:")
        for i, rec in enumerate(recommendations, 1):
            parts.append(f"  {i}. {rec}")
    
    # 5. Prioridad
    priority_emoji = "🔴" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢"
    parts.append(f"\n\nPrioridad: {priority_emoji} {priority}")
    
    return "".join(parts)


if __name__ == "__main__":
    # Test
    print("🧪 Scientific Narrative Generator - Test")
    print("=" * 80)
    
    # Test 1: Thermal Anchor Zone
    print("\n1. Test: Thermal Anchor Zone")
    narrative = generate_archaeological_narrative(
        thermal_stability=0.93,
        sar_structural_index=0.52,
        icesat2_rugosity=15.7,
        ndvi_persistence=0.06,
        tas_score=0.58,
        coverage_score=0.65,
        environment_type="arid",
        flags=['THERMAL_ANCHOR_ZONE']
    )
    
    print(f"\nClasificación: {narrative.classification.value}")
    print(f"Confianza: {narrative.confidence:.2f}")
    print(f"Prioridad: {narrative.priority}")
    print(f"\n{narrative.full_narrative}")
    
    print("\n" + "=" * 80)
    print("✅ Test completado")
