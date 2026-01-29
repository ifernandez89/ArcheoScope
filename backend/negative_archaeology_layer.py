#!/usr/bin/env python3
"""
Negative Archaeology Layer (NAL) - SALTO EVOLUTIVO 5
====================================================

Sistema para definir cuándo NO hay nada (con alta confianza).

CONCEPTO CLAVE:
- Un sistema que puede decir "no hay nada aquí" es más valioso
  que uno que siempre encuentra algo
- Poder negativo = credibilidad científica

CRITERIOS DE AUSENCIA CONFIABLE:
1. Territorio estable (ESS < 0.25)
2. Sin ruptura estratigráfica (coherencia > 0.7)
3. Sin memoria temporal (persistencia < 0.3)
4. Buena cobertura instrumental (> 60%)
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class NegativeConfidence(Enum):
    """Niveles de confianza en ausencia."""
    VERY_HIGH = "very_high"  # > 0.85
    HIGH = "high"            # 0.70-0.85
    MEDIUM = "medium"        # 0.50-0.70
    LOW = "low"              # < 0.50


@dataclass
class NegativeArchaeologyAssessment:
    """Evaluación de arqueología negativa."""
    
    # Resultado principal
    is_negative: bool                    # ¿Es territorio negativo?
    negative_confidence: float           # 0-1: Confianza en ausencia
    confidence_level: NegativeConfidence
    
    # Criterios evaluados
    is_stable: bool                      # ESS < 0.25
    no_rupture: bool                     # Coherencia > 0.7
    no_memory: bool                      # Persistencia < 0.3
    good_coverage: bool                  # Cobertura > 60%
    
    # Métricas
    ess_volumetrico: float
    coherencia_3d: float
    persistencia_temporal: float
    cobertura_total: float
    
    # Recomendación
    recommendation: str
    reason: str
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario."""
        return {
            "is_negative": self.is_negative,
            "negative_confidence": self.negative_confidence,
            "confidence_level": self.confidence_level.value,
            "criteria": {
                "is_stable": self.is_stable,
                "no_rupture": self.no_rupture,
                "no_memory": self.no_memory,
                "good_coverage": self.good_coverage
            },
            "metrics": {
                "ess_volumetrico": self.ess_volumetrico,
                "coherencia_3d": self.coherencia_3d,
                "persistencia_temporal": self.persistencia_temporal,
                "cobertura_total": self.cobertura_total
            },
            "recommendation": self.recommendation,
            "reason": self.reason
        }


class NegativeArchaeologyLayerEngine:
    """Motor de arqueología negativa."""
    
    def __init__(self):
        """Inicializar motor NAL."""
        
        # Umbrales de negatividad
        self.stability_threshold = 0.25      # ESS < 0.25 = estable
        self.coherence_threshold = 0.7       # Coherencia > 0.7 = sin ruptura
        self.memory_threshold = 0.3          # Persistencia < 0.3 = sin memoria
        self.coverage_threshold = 0.6        # Cobertura > 60% = buena
        
        logger.info("⚪ NegativeArchaeologyLayerEngine inicializado")
        logger.info("   📊 Método: Criterios de ausencia confiable")
        logger.info("   🎯 Objetivo: Poder negativo = credibilidad científica")
    
    def assess_negative_archaeology(self, etp) -> NegativeArchaeologyAssessment:
        """
        Evaluar si un territorio es arqueológicamente negativo.
        
        Args:
            etp: EnvironmentalTomographicProfile
            
        Returns:
            NegativeArchaeologyAssessment
        """
        
        logger.info("⚪ Evaluando arqueología negativa...")
        
        # Extraer métricas
        ess_volumetrico = etp.ess_volumetrico
        coherencia_3d = etp.coherencia_3d
        persistencia_temporal = etp.persistencia_temporal
        
        # Calcular cobertura total
        coverage = etp.instrumental_coverage
        cobertura_total = (
            coverage.get('superficial', {}).get('percentage', 0) +
            coverage.get('subsuperficial', {}).get('percentage', 0) +
            coverage.get('profundo', {}).get('percentage', 0)
        ) / 3.0 / 100.0  # Normalizar a 0-1
        
        # Evaluar criterios
        is_stable = ess_volumetrico < self.stability_threshold
        no_rupture = coherencia_3d > self.coherence_threshold
        no_memory = persistencia_temporal < self.memory_threshold
        good_coverage = cobertura_total > self.coverage_threshold
        
        logger.info(f"   📊 Criterios:")
        logger.info(f"      Estable (ESS < {self.stability_threshold}): {is_stable} (ESS={ess_volumetrico:.3f})")
        logger.info(f"      Sin ruptura (Coh > {self.coherence_threshold}): {no_rupture} (Coh={coherencia_3d:.3f})")
        logger.info(f"      Sin memoria (Pers < {self.memory_threshold}): {no_memory} (Pers={persistencia_temporal:.3f})")
        logger.info(f"      Buena cobertura (> {self.coverage_threshold}): {good_coverage} (Cob={cobertura_total:.3f})")
        
        # Determinar si es negativo
        criteria_met = sum([is_stable, no_rupture, no_memory, good_coverage])
        is_negative = criteria_met >= 3  # Al menos 3 de 4 criterios
        
        # Calcular confianza en ausencia
        if criteria_met == 4:
            negative_confidence = 0.90
        elif criteria_met == 3:
            negative_confidence = 0.75
        elif criteria_met == 2:
            negative_confidence = 0.55
        else:
            negative_confidence = 0.30
        
        # Ajustar por cobertura (si cobertura baja, reducir confianza)
        if not good_coverage:
            negative_confidence *= 0.7
        
        # Determinar nivel de confianza
        if negative_confidence > 0.85:
            confidence_level = NegativeConfidence.VERY_HIGH
        elif negative_confidence > 0.70:
            confidence_level = NegativeConfidence.HIGH
        elif negative_confidence > 0.50:
            confidence_level = NegativeConfidence.MEDIUM
        else:
            confidence_level = NegativeConfidence.LOW
        
        # Generar recomendación
        if is_negative and negative_confidence > 0.70:
            recommendation = "no_re_analizar"
            reason = "Territorio estable sin evidencia arqueológica. Alta confianza en ausencia."
        elif is_negative and negative_confidence > 0.50:
            recommendation = "monitoreo_pasivo"
            reason = "Territorio probablemente estable. Confianza moderada en ausencia."
        else:
            recommendation = "analisis_adicional"
            reason = "Territorio no concluyente. Se requiere análisis adicional."
        
        # Crear evaluación
        assessment = NegativeArchaeologyAssessment(
            is_negative=is_negative,
            negative_confidence=negative_confidence,
            confidence_level=confidence_level,
            is_stable=is_stable,
            no_rupture=no_rupture,
            no_memory=no_memory,
            good_coverage=good_coverage,
            ess_volumetrico=ess_volumetrico,
            coherencia_3d=coherencia_3d,
            persistencia_temporal=persistencia_temporal,
            cobertura_total=cobertura_total,
            recommendation=recommendation,
            reason=reason
        )
        
        logger.info(f"✅ Evaluación NAL completada:")
        logger.info(f"   ⚪ Es negativo: {is_negative}")
        logger.info(f"   📊 Confianza: {negative_confidence:.3f} ({confidence_level.value})")
        logger.info(f"   📋 Recomendación: {recommendation}")
        
        return assessment
    
    def generate_negative_report(self, assessment: NegativeArchaeologyAssessment) -> str:
        """Generar reporte de arqueología negativa."""
        
        report_lines = []
        
        report_lines.append("="*80)
        report_lines.append("⚪ REPORTE DE ARQUEOLOGÍA NEGATIVA")
        report_lines.append("="*80)
        report_lines.append("")
        
        if assessment.is_negative:
            report_lines.append("✅ TERRITORIO ARQUEOLÓGICAMENTE NEGATIVO")
            report_lines.append(f"   Confianza en ausencia: {assessment.negative_confidence:.1%} ({assessment.confidence_level.value})")
        else:
            report_lines.append("⚠️ TERRITORIO NO CONCLUYENTE")
            report_lines.append(f"   Confianza en ausencia: {assessment.negative_confidence:.1%} (insuficiente)")
        
        report_lines.append("")
        report_lines.append("📊 CRITERIOS EVALUADOS:")
        report_lines.append(f"   {'✅' if assessment.is_stable else '❌'} Territorio estable (ESS < 0.25): {assessment.ess_volumetrico:.3f}")
        report_lines.append(f"   {'✅' if assessment.no_rupture else '❌'} Sin ruptura estratigráfica (Coh > 0.7): {assessment.coherencia_3d:.3f}")
        report_lines.append(f"   {'✅' if assessment.no_memory else '❌'} Sin memoria temporal (Pers < 0.3): {assessment.persistencia_temporal:.3f}")
        report_lines.append(f"   {'✅' if assessment.good_coverage else '❌'} Buena cobertura instrumental (> 60%): {assessment.cobertura_total:.1%}")
        
        report_lines.append("")
        report_lines.append("📋 RECOMENDACIÓN:")
        report_lines.append(f"   {assessment.recommendation.upper()}")
        report_lines.append(f"   Razón: {assessment.reason}")
        
        report_lines.append("")
        report_lines.append("="*80)
        
        return "\n".join(report_lines)


if __name__ == "__main__":
    print("⚪ Negative Archaeology Layer (NAL) - SALTO EVOLUTIVO 5")
    print("=" * 70)
    print()
    print("Sistema de arqueología negativa implementado.")
    print()
    print("Capacidades:")
    print("  ✅ Criterios de ausencia confiable")
    print("  ✅ Confianza en negatividad")
    print("  ✅ Recomendación de no re-analizar")
    print("  ✅ Credibilidad científica (poder negativo)")
    print()
    print("Uso:")
    print("  from negative_archaeology_layer import NegativeArchaeologyLayerEngine")
    print("  nal_engine = NegativeArchaeologyLayerEngine()")
    print("  assessment = nal_engine.assess_negative_archaeology(etp)")
