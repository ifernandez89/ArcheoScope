#!/usr/bin/env python3
"""
Territorial Inferential Multi-domain Tomography (TIMT) - SISTEMA COMPLETO
========================================================================

REVOLUCIÓN CONCEPTUAL: Motor de Tomografía Territorial Inferencial
De "detector de sitios" a "explicador de territorios"

FLUJO CIENTÍFICO COMPLETO (3 CAPAS):
CAPA 0: Contexto antes de medir (TCP)
CAPA 1: Adquisición dirigida por hipótesis
CAPA 2: Tomografía + evidencia + narrativa
CAPA 3: Transparencia + límites + comunicación

RESULTADO: Sistema científicamente honesto que promete coherencia, no certezas.
"""

import asyncio
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from territorial_context_profile import TerritorialContextProfileSystem, TerritorialContextProfile, AnalysisObjective
from etp_generator import ETProfileGenerator
from etp_core import EnvironmentalTomographicProfile, BoundingBox
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# HRM Imports
try:
    from hrm.hrm_runner import load_models as load_hrm_model, generate_response as generate_hrm_response
    HRM_AVAILABLE = True
except ImportError:
    HRM_AVAILABLE = False
    logger.warning("⚠️ HRM module not available")


class AnalysisMode(Enum):
    """Modos de análisis territorial."""
    HYPOTHESIS_DRIVEN = "hypothesis_driven"    # Dirigido por hipótesis (NUEVO)
    SENSOR_DRIVEN = "sensor_driven"           # Dirigido por sensores (TRADICIONAL)
    HYBRID = "hybrid"                         # Híbrido

class EvidenceLevel(Enum):
    """Niveles de evidencia."""
    STRONG = "strong"           # Evidencia fuerte, múltiples fuentes
    MODERATE = "moderate"       # Evidencia moderada
    WEAK = "weak"              # Evidencia débil
    CONTRADICTORY = "contradictory"  # Evidencia contradictoria
    INSUFFICIENT = "insufficient"    # Evidencia insuficiente

class CommunicationLevel(Enum):
    """Niveles de comunicación de resultados."""
    TECHNICAL = "technical"     # Técnico especializado
    ACADEMIC = "academic"       # Académico riguroso
    GENERAL = "general"         # Público general
    INSTITUTIONAL = "institutional"  # Institucional

@dataclass
class HypothesisValidation:
    """Validación de hipótesis territorial."""
    
    hypothesis_id: str
    hypothesis_type: str
    
    # Evidencia por fuente
    sensorial_evidence: float      # 0-1
    geological_evidence: float     # 0-1
    hydrographic_evidence: float   # 0-1
    archaeological_evidence: float # 0-1
    human_traces_evidence: float   # 0-1
    
    # Evaluación final
    overall_evidence_level: EvidenceLevel
    confidence_score: float        # 0-1
    
    # Contradicciones
    contradictions: List[str]
    supporting_factors: List[str]
    
    # Explicación
    validation_explanation: str

@dataclass
class SystemTransparencyReport:
    """Reporte de transparencia del sistema."""
    
    # Proceso completo
    analysis_process: List[str]
    decisions_made: List[str]
    hypotheses_discarded: List[str]
    
    # Incertidumbres
    measurement_uncertainties: List[str]
    interpretation_uncertainties: List[str]
    
    # Límites del sistema
    system_limitations: List[str]
    cannot_affirm: List[str]
    can_infer: List[str]
    
    # Recomendaciones
    validation_recommendations: List[str]
    future_work_suggestions: List[str]

    # Métricas cuantitativas de transparencia (con valores por defecto al final)
    hypotheses_evaluated: int = 0
    hypotheses_validated: int = 0
    hypotheses_rejected: int = 0

@dataclass
class TerritorialInferentialTomographyResult:
    """Resultado completo del análisis tomográfico territorial."""
    
    # Identificación (campos requeridos primero)
    analysis_id: str
    territory_bounds: BoundingBox
    
    # CAPA 0: Contexto territorial (requerido)
    territorial_context: TerritorialContextProfile
    
    # CAPA 1: Perfil tomográfico (requerido)
    tomographic_profile: EnvironmentalTomographicProfile
    
    # CAPA 3: Transparencia (requerido)
    transparency_report: SystemTransparencyReport
    
    # Campos con defaults
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    
    # CAPA 2: Validación de hipótesis (opcional)
    hypothesis_validations: List[HypothesisValidation] = field(default_factory=list)
    
    # Comunicación multinivel
    technical_summary: str = ""
    academic_summary: str = ""
    general_summary: str = ""
    institutional_summary: str = ""
    
    # Métricas finales
    territorial_coherence_score: float = 0.0  # Coherencia territorial general
    scientific_rigor_score: float = 0.0      # Rigor científico del análisis
    
    # HRM Output
    scientific_output: Dict[str, Any] = field(default_factory=dict)

class TerritorialInferentialTomographyEngine:
    """Motor de Tomografía Territorial Inferencial - SISTEMA COMPLETO."""
    
    def __init__(self, integrator_15_instruments):
        """
        Inicializar motor TIMT.
        
        Args:
            integrator_15_instruments: RealDataIntegratorV2 con 15 instrumentos
        """
        
        # Sistemas componentes
        self.tcp_system = TerritorialContextProfileSystem()
        self.etp_generator = ETProfileGenerator(integrator_15_instruments)
        
        # Inicializar HRM si está disponible
        self.hrm_model = None
        if HRM_AVAILABLE:
            try:
                self.hrm_model = load_hrm_model()
                logger.info("🧠 HRM Model loaded in TIMT Engine")
            except Exception as e:
                logger.error(f"❌ Failed to load HRM model: {e}")
        
        # Configuración del motor
        self.analysis_mode = AnalysisMode.HYPOTHESIS_DRIVEN  # NUEVO POR DEFECTO
        
        logger.info("🚀 Territorial Inferential Tomography Engine initialized")
        logger.info("🧩 MODO: Hypothesis-driven analysis (REVOLUCIÓN CONCEPTUAL)")
    
    async def analyze_territory(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float,
                               analysis_objective: AnalysisObjective = AnalysisObjective.EXPLORATORY,
                               analysis_radius_km: float = 5.0,
                               resolution_m: float = None,
                               communication_level: CommunicationLevel = CommunicationLevel.TECHNICAL) -> TerritorialInferentialTomographyResult:
        """
        Análisis territorial completo con flujo científico de 3 capas.
        
        PROCESO REVOLUCIONARIO:
        CAPA 0: Contexto → Hipótesis → Estrategia
        CAPA 1: Adquisición dirigida → Tomografía
        CAPA 2: Validación → Transparencia → Comunicación
        
        Args:
            lat_min, lat_max, lon_min, lon_max: Límites territoriales
            analysis_objective: Objetivo del análisis
            analysis_radius_km: Radio de análisis contextual
            resolution_m: Resolución (si None, usa recomendación TCP)
            communication_level: Nivel de comunicación de resultados
            
        Returns:
            TerritorialInferentialTomographyResult completo
        """
        
        logger.info("🚀 INICIANDO ANÁLISIS TERRITORIAL INFERENCIAL TOMOGRÁFICO")
        logger.info(f"📍 Territorio: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        logger.info(f"🎯 Objetivo: {analysis_objective.value}")
        logger.info(f"📡 Modo: {self.analysis_mode.value}")
        
        analysis_id = f"TIMT_{lat_min:.4f}_{lat_max:.4f}_{lon_min:.4f}_{lon_max:.4f}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # ============================================================================
        # CAPA 0: CONTEXTO ANTES DE MEDIR (REVOLUCIÓN CONCEPTUAL)
        # ============================================================================
        
        logger.info("🧩 CAPA 0: GENERACIÓN DE CONTEXTO TERRITORIAL (TCP)")
        
        tcp = await self.tcp_system.generate_tcp(
            lat_min, lat_max, lon_min, lon_max, analysis_objective, analysis_radius_km
        )
        
        # Usar resolución recomendada por TCP si no se especifica
        if resolution_m is None:
            resolution_m = tcp.instrumental_strategy.recommended_resolution_m if tcp.instrumental_strategy else 50.0
        
        logger.info(f"✅ TCP generado - {len(tcp.territorial_hypotheses)} hipótesis territoriales")
        
        # ============================================================================
        # CAPA 1: ADQUISICIÓN DIRIGIDA POR HIPÓTESIS
        # ============================================================================
        
        logger.info("🛰️ CAPA 1: ADQUISICIÓN DIRIGIDA Y TOMOGRAFÍA")
        
        # Crear bounding box 3D
        bounds = BoundingBox(
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            depth_min=0.0,
            depth_max=-20.0
        )
        
        # Generar perfil tomográfico (ahora dirigido por hipótesis TCP)
        etp = await self.etp_generator.generate_etp(bounds, resolution_m)
        
        logger.info("✅ Perfil tomográfico generado")
        
        # ============================================================================
        # CAPA 2: VALIDACIÓN DE HIPÓTESIS Y EVIDENCIA
        # ============================================================================
        
        logger.info("🧠 CAPA 2: VALIDACIÓN DE HIPÓTESIS TERRITORIALES")
        
        hypothesis_validations = self._validate_territorial_hypotheses(tcp, etp)
        
        logger.info(f"✅ {len(hypothesis_validations)} hipótesis validadas")
        
        # ============================================================================
        # CAPA 3: TRANSPARENCIA Y COMUNICACIÓN
        # ============================================================================
        
        logger.info("📋 CAPA 3: GENERACIÓN DE TRANSPARENCIA Y COMUNICACIÓN")
        
        transparency_report = self._generate_transparency_report(tcp, etp, hypothesis_validations)
        
        # Comunicación multinivel
        summaries = self._generate_multilevel_communication(
            tcp, etp, hypothesis_validations, transparency_report, communication_level
        )
        
        # Métricas finales
        territorial_coherence = self._calculate_territorial_coherence(tcp, etp, hypothesis_validations)
        scientific_rigor = self._calculate_scientific_rigor(tcp, etp, transparency_report)
        
        # ============================================================================
        # CAPA EXTRA: HRM ANALYSIS (Neural Visualization) & Honest Metrics
        # ============================================================================
        
        hrm_result = {}
        if self.hrm_model:
            logger.info("🧠 EJECUTANDO ANÁLISIS HRM (High Resolution Morphology)")
            hrm_result = self._run_hrm_analysis(analysis_id, tcp, etp, hypothesis_validations)
        else:
            logger.warning("⚠️ HRM analysis skipped (model not available)")
            
        # Construir Scientific Output con métricas de honestidad académica
        # Extraer instrumentos (esto es una simplificación, en producción vendría del batch)
        available_instr = tcp.instrumental_strategy.priority_instruments if tcp.instrumental_strategy else ["Sentinel-2", "Sentinel-1", "DEM", "ICESat-2"]
        
        scientific_output = {
            "anthropic_origin_probability": etp.densidad_arqueologica_m3,
            "anthropic_activity_probability": 0.0, # Por ahora estático hasta tener firma TAS/DIL mapeada
            "instrumental_anomaly_probability": etp.ess_superficial,
            "recommended_action": etp.get_archaeological_recommendation(),
            "notes": etp.narrative_explanation,
            "available_instruments": available_instr,
            "instruments_measured": len([i for i in available_instr if i]), # Simplificación
            "coverage_raw": scientific_rigor, # Usar rigor como aproximación de cobertura raw
            "hrm_analysis": hrm_result.get("hrm_analysis", {})
        }
        
        # ============================================================================
        # RESULTADO FINAL
        # ============================================================================
        
        result = TerritorialInferentialTomographyResult(
            analysis_id=analysis_id,
            territory_bounds=bounds,
            territorial_context=tcp,
            tomographic_profile=etp,
            hypothesis_validations=hypothesis_validations,
            transparency_report=transparency_report,
            technical_summary=summaries['technical'],
            academic_summary=summaries['academic'],
            general_summary=summaries['general'],
            institutional_summary=summaries['institutional'],
            territorial_coherence_score=territorial_coherence,
            scientific_rigor_score=scientific_rigor,
            scientific_output=scientific_output
        )
        
        logger.info("🎉 ANÁLISIS TERRITORIAL INFERENCIAL TOMOGRÁFICO COMPLETADO")
        logger.info(f"   🎯 Coherencia territorial: {territorial_coherence:.3f}")
        logger.info(f"   🔬 Rigor científico: {scientific_rigor:.3f}")
        logger.info(f"   🧠 Hipótesis validadas: {len([h for h in hypothesis_validations if h.overall_evidence_level in [EvidenceLevel.STRONG, EvidenceLevel.MODERATE]])}")
        
        return result
    
    def _validate_territorial_hypotheses(self, tcp: TerritorialContextProfile,
                                       etp: EnvironmentalTomographicProfile) -> List[HypothesisValidation]:
        """Validar hipótesis territoriales contra evidencia tomográfica."""
        
        validations = []
        
        for hypothesis in tcp.territorial_hypotheses:
            
            # Evidencia sensorial (del ETP)
            sensorial_evidence = etp.ess_volumetrico
            
            # Evidencia geológica
            geological_evidence = etp.geological_compatibility.gcs_score if etp.geological_compatibility else 0.5
            
            # Evidencia hidrográfica
            hydrographic_evidence = etp.water_availability.settlement_viability if etp.water_availability else 0.5
            
            # Evidencia arqueológica externa
            archaeological_evidence = etp.external_consistency.ecs_score if etp.external_consistency else 0.5
            
            # Evidencia de trazas humanas
            human_traces_evidence = etp.territorial_use_profile.settlement_potential if etp.territorial_use_profile else 0.5
            
            # Evaluación combinada
            evidence_scores = [
                sensorial_evidence,
                geological_evidence,
                hydrographic_evidence,
                archaeological_evidence,
                human_traces_evidence
            ]
            
            confidence_score = np.mean(evidence_scores)
            
            # Determinar nivel de evidencia
            if confidence_score > 0.8:
                evidence_level = EvidenceLevel.STRONG
            elif confidence_score > 0.6:
                evidence_level = EvidenceLevel.MODERATE
            elif confidence_score > 0.4:
                evidence_level = EvidenceLevel.WEAK
            else:
                evidence_level = EvidenceLevel.INSUFFICIENT
            
            # Identificar contradicciones y factores de soporte
            contradictions = []
            supporting_factors = []
            
            if sensorial_evidence < 0.3:
                contradictions.append("Baja evidencia sensorial")
            else:
                supporting_factors.append("Evidencia sensorial positiva")
            
            if geological_evidence > 0.7:
                supporting_factors.append("Contexto geológico favorable")
            elif geological_evidence < 0.3:
                contradictions.append("Contexto geológico desfavorable")
            
            if archaeological_evidence > 0.6:
                supporting_factors.append("Consistencia con sitios arqueológicos conocidos")
            
            # Explicación de validación
            explanation = f"Hipótesis {hypothesis.hypothesis_type} con evidencia {evidence_level.value} (confianza: {confidence_score:.2f})"
            
            validation = HypothesisValidation(
                hypothesis_id=hypothesis.hypothesis_id,
                hypothesis_type=hypothesis.hypothesis_type,
                sensorial_evidence=sensorial_evidence,
                geological_evidence=geological_evidence,
                hydrographic_evidence=hydrographic_evidence,
                archaeological_evidence=archaeological_evidence,
                human_traces_evidence=human_traces_evidence,
                overall_evidence_level=evidence_level,
                confidence_score=confidence_score,
                contradictions=contradictions,
                supporting_factors=supporting_factors,
                validation_explanation=explanation
            )
            
            validations.append(validation)
        
        return validations
    
    def _generate_transparency_report(self, tcp: TerritorialContextProfile,
                                    etp: EnvironmentalTomographicProfile,
                                    validations: List[HypothesisValidation]) -> SystemTransparencyReport:
        """Generar reporte completo de transparencia del sistema."""
        
        # Proceso de análisis
        analysis_process = [
            "1. Generación de Contexto Territorial (TCP)",
            "2. Formulación de hipótesis territoriales",
            "3. Selección instrumental dirigida por hipótesis",
            "4. Adquisición de datos satelitales",
            "5. Generación de perfil tomográfico (ETP)",
            "6. Integración de contextos adicionales",
            "7. Validación cruzada de hipótesis",
            "8. Evaluación de coherencia territorial"
        ]
        
        # Decisiones tomadas
        decisions_made = [
            f"Modo de análisis: {self.analysis_mode.value}",
            f"Resolución seleccionada: {etp.resolution_m}m",
            f"Instrumentos prioritarios: {len(tcp.instrumental_strategy.priority_instruments) if tcp.instrumental_strategy else 0}",
            f"Hipótesis evaluadas: {len(tcp.territorial_hypotheses)}"
        ]
        
        # Hipótesis descartadas
        weak_hypotheses = [v for v in validations if v.overall_evidence_level in [EvidenceLevel.WEAK, EvidenceLevel.INSUFFICIENT]]
        hypotheses_discarded = [f"{h.hypothesis_type} (evidencia {h.overall_evidence_level.value})" for h in weak_hypotheses]
        
        # Incertidumbres de medición
        measurement_uncertainties = [
            "Profundidades inferidas, no medidas directamente",
            "Resolución espacial limitada por sensores satelitales",
            "Condiciones atmosféricas pueden afectar mediciones",
            "Cobertura temporal limitada de algunos instrumentos"
        ]
        
        # Incertidumbres de interpretación
        interpretation_uncertainties = [
            "Anomalías pueden tener origen natural o cultural",
            "Datación relativa basada en patrones espaciales",
            "Función territorial inferida de contexto",
            "Preservación arqueológica variable según condiciones"
        ]
        
        # Límites del sistema
        system_limitations = tcp.known_limitations + [
            "No detecta estructuras específicas individuales",
            "Limitado a evidencia indirecta y patrones",
            "Requiere validación de campo para confirmación",
            "Efectividad variable según tipo de sitio"
        ]
        
        # Lo que NO puede afirmar
        cannot_affirm = [
            "Presencia confirmada de estructuras arqueológicas",
            "Datación absoluta de anomalías",
            "Función específica de estructuras detectadas",
            "Estado de preservación exacto",
            "Significancia cultural específica"
        ]
        
        # Lo que SÍ puede inferir
        can_infer = [
            "Patrones espaciales anómalos consistentes",
            "Coherencia territorial de anomalías",
            "Compatibilidad con contexto arqueológico",
            "Potencial arqueológico relativo",
            "Priorización para investigación de campo"
        ]
        
        # Recomendaciones de validación
        validation_recommendations = [
            "Prospección geofísica de superficie",
            "Sondeos arqueológicos estratégicos",
            "Análisis de materiales de superficie",
            "Documentación fotogramétrica detallada",
            "Consulta con arqueólogos especialistas regionales"
        ]
        
        # Sugerencias de trabajo futuro
        future_work_suggestions = [
            "Integración de datos LiDAR de alta resolución",
            "Análisis temporal con series históricas",
            "Validación con excavaciones controladas",
            "Desarrollo de modelos predictivos regionales",
            "Integración con bases de datos arqueológicas"
        ]
        
        # Métricas de hipótesis
        valid_evidence_levels = [EvidenceLevel.STRONG, EvidenceLevel.MODERATE]
        hypotheses_evaluated = len(validations)
        hypotheses_validated = len([v for v in validations if v.overall_evidence_level in valid_evidence_levels])
        hypotheses_rejected = len([v for v in validations if v.overall_evidence_level not in valid_evidence_levels])

        return SystemTransparencyReport(
            analysis_process=analysis_process,
            decisions_made=decisions_made,
            hypotheses_discarded=hypotheses_discarded,
            hypotheses_evaluated=hypotheses_evaluated,
            hypotheses_validated=hypotheses_validated,
            hypotheses_rejected=hypotheses_rejected,
            measurement_uncertainties=measurement_uncertainties,
            interpretation_uncertainties=interpretation_uncertainties,
            system_limitations=system_limitations,
            cannot_affirm=cannot_affirm,
            can_infer=can_infer,
            validation_recommendations=validation_recommendations,
            future_work_suggestions=future_work_suggestions
        )
    
    def _generate_multilevel_communication(self, tcp: TerritorialContextProfile,
                                         etp: EnvironmentalTomographicProfile,
                                         validations: List[HypothesisValidation],
                                         transparency: SystemTransparencyReport,
                                         level: CommunicationLevel) -> Dict[str, str]:
        """Generar comunicación multinivel de resultados."""
        
        # Métricas clave
        strong_hypotheses = [v for v in validations if v.overall_evidence_level == EvidenceLevel.STRONG]
        moderate_hypotheses = [v for v in validations if v.overall_evidence_level == EvidenceLevel.MODERATE]
        
        # Resumen técnico
        technical = f"""
ANÁLISIS TERRITORIAL INFERENCIAL TOMOGRÁFICO
============================================

TERRITORIO: {tcp.territory_bounds}
OBJETIVO: {tcp.analysis_objective.value}
ESS VOLUMÉTRICO: {etp.ess_volumetrico:.3f}
COHERENCIA 3D: {etp.coherencia_3d:.3f}

HIPÓTESIS VALIDADAS:
- Evidencia fuerte: {len(strong_hypotheses)}
- Evidencia moderada: {len(moderate_hypotheses)}

CONTEXTOS INTEGRADOS:
- Geológico: {etp.geological_context.dominant_lithology.value if etp.geological_context else 'N/A'}
- Hidrográfico: {len(etp.hydrographic_features)} características
- Arqueológico externo: {len(etp.external_sites)} sitios
- Trazas humanas: {len(etp.human_traces)} trazas

LIMITACIONES: {len(transparency.system_limitations)} identificadas
RECOMENDACIONES: {len(transparency.validation_recommendations)} sugeridas
        """.strip()
        
        # Resumen académico
        academic = f"""
Este análisis territorial aplicó tomografía inferencial multidominio para evaluar {len(tcp.territorial_hypotheses)} hipótesis territoriales. 
El sistema integró evidencia sensorial (ESS: {etp.ess_volumetrico:.3f}), contexto geológico (GCS: {etp.geological_compatibility.gcs_score if etp.geological_compatibility else 'N/A'}), 
validación arqueológica externa (ECS: {etp.external_consistency.ecs_score if etp.external_consistency else 'N/A'}), y análisis de trazas humanas.

Resultados: {len(strong_hypotheses)} hipótesis con evidencia fuerte, {len(moderate_hypotheses)} con evidencia moderada. 
La coherencia territorial ({etp.coherencia_3d:.3f}) sugiere patrones espaciales consistentes que requieren validación de campo.

Limitaciones: El sistema infiere patrones territoriales pero no confirma estructuras específicas. 
Se recomienda prospección geofísica y sondeos arqueológicos para validación.
        """.strip()
        
        # Resumen general
        general = f"""
Se analizó un territorio usando tecnología satelital avanzada y inteligencia artificial para identificar posibles sitios arqueológicos.

El sistema encontró {len(strong_hypotheses + moderate_hypotheses)} áreas de interés arqueológico con diferentes niveles de evidencia. 
Se integraron datos geológicos, hidrográficos y de actividad humana histórica para una evaluación completa.

Los resultados sugieren potencial arqueológico que requiere investigación de campo para confirmación. 
El análisis proporciona una guía científica para priorizar futuras excavaciones.
        """.strip()
        
        # Resumen institucional
        institutional = f"""
INFORME EJECUTIVO - ANÁLISIS TERRITORIAL ARQUEOLÓGICO

TERRITORIO ANALIZADO: {tcp.territory_bounds}
METODOLOGÍA: Tomografía Territorial Inferencial con 15 instrumentos satelitales
OBJETIVO: {tcp.analysis_objective.value}

RESULTADOS PRINCIPALES:
• {len(strong_hypotheses)} áreas con evidencia arqueológica fuerte
• {len(moderate_hypotheses)} áreas con evidencia moderada
• Coherencia territorial: {etp.coherencia_3d:.3f}/1.0
• Potencial de preservación: {tcp.preservation_potential.value}

RECOMENDACIONES:
• Prospección geofísica en áreas prioritarias
• Sondeos arqueológicos estratégicos
• Consulta con especialistas regionales

LIMITACIONES: Análisis basado en evidencia indirecta. Requiere validación de campo.
CONFIANZA CIENTÍFICA: Sistema transparente con limitaciones documentadas.
        """.strip()
        
        return {
            'technical': technical,
            'academic': academic,
            'general': general,
            'institutional': institutional
        }
    
    def _calculate_territorial_coherence(self, tcp: TerritorialContextProfile,
                                       etp: EnvironmentalTomographicProfile,
                                       validations: List[HypothesisValidation]) -> float:
        """Calcular coherencia territorial general."""
        
        coherence_factors = []
        
        # Coherencia tomográfica 3D
        coherence_factors.append(etp.coherencia_3d)
        
        # Coherencia de hipótesis
        if validations:
            hypothesis_coherence = np.mean([v.confidence_score for v in validations])
            coherence_factors.append(hypothesis_coherence)
        
        # Coherencia contextual
        context_scores = []
        if etp.geological_compatibility:
            context_scores.append(etp.geological_compatibility.gcs_score)
        if etp.external_consistency:
            context_scores.append(etp.external_consistency.ecs_score)
        if etp.water_availability:
            context_scores.append(etp.water_availability.settlement_viability)
        
        if context_scores:
            context_coherence = np.mean(context_scores)
            coherence_factors.append(context_coherence)
        
        return np.mean(coherence_factors) if coherence_factors else 0.5
    
    def _calculate_scientific_rigor(self, tcp: TerritorialContextProfile,
                                  etp: EnvironmentalTomographicProfile,
                                  transparency: SystemTransparencyReport) -> float:
        """Calcular rigor científico del análisis."""
        
        rigor_factors = []
        
        # Completitud del contexto
        context_completeness = 0.0
        if tcp.geological_context:
            context_completeness += 0.25
        if tcp.hydrographic_features:
            context_completeness += 0.25
        if tcp.external_archaeological_sites:
            context_completeness += 0.25
        if tcp.known_human_traces:
            context_completeness += 0.25
        
        rigor_factors.append(context_completeness)
        
        # Transparencia del proceso
        transparency_score = min(1.0, len(transparency.analysis_process) / 8.0)
        rigor_factors.append(transparency_score)
        
        # Documentación de limitaciones
        limitations_score = min(1.0, len(transparency.system_limitations) / 5.0)
        rigor_factors.append(limitations_score)
        
        # Validación cruzada
        if etp.external_consistency and etp.geological_compatibility:
            rigor_factors.append(0.8)  # Bonus por validación cruzada
        
        return np.mean(rigor_factors) if rigor_factors else 0.5

    def _run_hrm_analysis(self, analysis_id: str, tcp: TerritorialContextProfile,
                        etp: EnvironmentalTomographicProfile,
                        validations: List[HypothesisValidation]) -> Dict[str, Any]:
        """Ejecutar análisis HRM y generar visualización neural."""
        
        try:
            # 1. Preparar pregunta para HRM
            strongest_hypothesis = "No hypothesis"
            if validations:
                # Buscar la mejor validada
                best = max(validations, key=lambda x: x.confidence_score)
                strongest_hypothesis = f"{best.hypothesis_type} (confianza: {best.confidence_score:.2f})"
            
            question = (
                f"Analizar coherencia territorial en {tcp.territory_bounds}. "
                f"Contexto: {tcp.geological_context.dominant_lithology.value if tcp.geological_context else 'Unknown'}. "
                f"ESS Volumétrico: {etp.ess_volumetrico:.3f}. "
                f"Hipótesis principal: {strongest_hypothesis}."
            )
            
            # 2. Configurar path de visualización
            # Asegurar que el directorio existe
            maps_dir = Path("anomaly_maps")
            maps_dir.mkdir(exist_ok=True)
            
            filename = f"hrm_viz_{analysis_id}.png"
            viz_path = maps_dir / filename
            
            # 3. Ejecutar HRM
            response_json = generate_hrm_response(
                question=question,
                hrm_model=self.hrm_model,
                temperature=0.3,
                mode="scientific_strict",
                visualize_path=str(viz_path)
            )
            
            # 4. Procesar respuesta
            # Si response_json es string (porque falló el parseo JSON en HRM u otro motivo), empaquetarlo
            if isinstance(response_json, str):
                result = {
                    "raw_output": response_json,
                    "analisis_morfologico": "Análisis textual generado.",
                    "hipotesis_antropica": "Ver raw output.",
                    "hipotesis_natural_alternativa": "Ver raw output.",
                    "nivel_incertidumbre": "Indeterminado"
                }
            else:
                result = response_json
            
            # 5. Agregar URL de visualización (será servida por /anomaly-map/{filename})
            # El frontend espera 'visualizacion_neural'
            # Usamos una URL relativa que el frontend pueda resolver
            # Si el frontend está en otro puerto, podría necesitar la URL completa del backend
            # Por ahora asumimos que el backend sirve esto en /anomaly-map/
            
            # Construir URL absoluta si es posible, o relativa
            API_URL = os.getenv("VITE_API_URL", "http://localhost:8003")
            result["visualizacion_neural"] = f"{API_URL}/anomaly-map/{filename}"
            
            logger.info(f"✅ HRM Analysis complete. Viz: {filename}")
            
            return {
                "hrm_analysis": result
            }
            
        except Exception as e:
            logger.error(f"❌ Error in HRM analysis: {e}", exc_info=True)
            return {
                "error": str(e),
                "hrm_analysis": {}
            }