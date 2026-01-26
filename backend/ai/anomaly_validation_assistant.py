#!/usr/bin/env python3
"""
AI Assistant para Validación de Anomalías Arqueológicas - ArcheoScope

Este módulo implementa un asistente IA especializado en validar anomalías detectadas
por instrumentos, NO como detector primario sino como capa de validación cognitiva.

Arquitectura:
Instrumentos + Algoritmos → detección de anomalías → features numéricas → 
IA (assistant) → score final + explicación

El assistant:
- NO ve píxeles
- NO detecta geometrías  
- SÍ razona sobre resultados
- SÍ detecta inconsistencias lógicas
- SÍ justifica decisiones
- SÍ audita falsos positivos
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

# Importar el asistente base existente
from .archaeological_assistant import ArchaeologicalAssistant

logger = logging.getLogger(__name__)

@dataclass
class AnomalyValidationResult:
    """Resultado de validación de anomalía por IA."""
    is_coherent: bool
    confidence_score: float  # 0.0 - 1.0
    validation_reasoning: str
    detected_inconsistencies: List[str]
    scoring_adjustments: Dict[str, float]
    false_positive_risk: float  # 0.0 - 1.0
    recommended_actions: List[str]
    methodological_notes: str

@dataclass
class InstrumentalFeatures:
    """Features numéricas extraídas de instrumentos para IA."""
    tile_id: str
    terrain_type: str
    signals: Dict[str, float]  # {"sar": 0.81, "thermal": 0.67, "dem": 0.72}
    geometry_score: float
    temporal_persistence: float
    historical_proximity: float
    convergence_count: int
    environment_confidence: float

class AnomalyValidationAssistant:
    """
    Asistente IA para validación cognitiva de anomalías arqueológicas.
    
    NO es un detector primario - es una capa de validación que:
    1. Analiza resultados estructurados de instrumentos
    2. Detecta inconsistencias lógicas en scoring
    3. Revisa pesos y coherencia metodológica
    4. Justifica decisiones de manera reproducible
    5. Audita falsos positivos potenciales
    6. Genera reportes explicables
    """
    
    def __init__(self):
        """Inicializar asistente de validación."""
        # Usar el asistente arqueológico base existente
        self.base_assistant = ArchaeologicalAssistant()
        
        # Configuración específica para validación
        self.validation_threshold = 0.6  # Umbral para validación positiva
        self.inconsistency_threshold = 0.3  # Umbral para detectar inconsistencias
        
        logger.info("AnomalyValidationAssistant inicializado")
        logger.info(f"  - Base AI disponible: {'✅' if self.base_assistant.is_available else '❌'}")
        logger.info(f"  - Validation threshold: {self.validation_threshold}")
        
    @property
    def is_available(self) -> bool:
        """Verificar si el asistente está disponible."""
        return self.base_assistant.is_available
    
    def validate_anomaly(self, 
                        instrumental_features: InstrumentalFeatures,
                        raw_measurements: List[Dict[str, Any]],
                        current_score: float,
                        context: Dict[str, Any]) -> AnomalyValidationResult:
        """
        Validar anomalía detectada usando razonamiento IA.
        
        Args:
            instrumental_features: Features numéricas extraídas
            raw_measurements: Mediciones instrumentales brutas
            current_score: Score actual calculado por algoritmos
            context: Contexto adicional (región, ambiente, etc.)
            
        Returns:
            Resultado de validación con score ajustado y explicación
        """
        
        if not self.is_available:
            return self._fallback_validation(instrumental_features, current_score)
        
        try:
            # 1. Construir prompt de validación
            validation_prompt = self._build_validation_prompt(
                instrumental_features, raw_measurements, current_score, context
            )
            
            # 2. Llamar al modelo IA
            ai_response = self.base_assistant._call_ai_model(validation_prompt)
            
            # 3. Parsear respuesta y generar resultado
            return self._parse_validation_response(
                ai_response, instrumental_features, current_score, context
            )
            
        except Exception as e:
            logger.error(f"Error en validación IA: {e}")
            return self._fallback_validation(instrumental_features, current_score)
    
    def _build_validation_prompt(self,
                                features: InstrumentalFeatures,
                                measurements: List[Dict[str, Any]],
                                current_score: float,
                                context: Dict[str, Any]) -> str:
        """Construir prompt específico para validación de anomalías."""
        
        # Resumen de features numéricas
        signals_summary = ", ".join([
            f"{k}={v:.2f}" for k, v in features.signals.items()
        ])
        
        # Resumen de mediciones
        measurements_summary = []
        for m in measurements[:5]:  # Top 5 mediciones
            name = m.get('instrument', 'unknown')
            value = m.get('value', 0)
            threshold = m.get('threshold', 0)
            exceeds = m.get('exceeds_threshold', False)
            measurements_summary.append(f"{name}: {value:.2f} ({'✓' if exceeds else '✗'} vs {threshold:.2f})")
        
        prompt = f"""Eres un validador IA especializado en anomalías arqueológicas.

DATOS DE ENTRADA:
- Región: {features.tile_id} ({features.terrain_type})
- Señales: {signals_summary}
- Geometría: {features.geometry_score:.2f}
- Persistencia temporal: {features.temporal_persistence:.2f}
- Proximidad histórica: {features.historical_proximity:.2f}
- Instrumentos convergentes: {features.convergence_count}
- Score actual: {current_score:.2f}

MEDICIONES INSTRUMENTALES:
{chr(10).join(measurements_summary)}

TAREA DE VALIDACIÓN:
1. ¿Es coherente el score {current_score:.2f} con las mediciones?
2. ¿Hay inconsistencias lógicas en los datos?
3. ¿Qué ajustes de scoring recomiendas?
4. ¿Cuál es el riesgo de falso positivo?

Responde en formato:
COHERENCIA: [SÍ/NO]
CONFIANZA: [0.0-1.0]
INCONSISTENCIAS: [lista]
AJUSTE_SCORE: [+/-0.XX]
RIESGO_FP: [0.0-1.0]
RAZONAMIENTO: [explicación breve]"""
        
        return prompt
    
    def _parse_validation_response(self,
                                  response: str,
                                  features: InstrumentalFeatures,
                                  current_score: float,
                                  context: Dict[str, Any]) -> AnomalyValidationResult:
        """Parsear respuesta IA en resultado estructurado."""
        
        # Extraer campos estructurados
        is_coherent = "SÍ" in response or "YES" in response.upper()
        
        # Extraer confianza
        confidence_score = self._extract_numeric_field(response, "CONFIANZA", 0.5)
        
        # Extraer ajuste de score
        score_adjustment = self._extract_numeric_field(response, "AJUSTE_SCORE", 0.0)
        
        # Extraer riesgo de falso positivo
        false_positive_risk = self._extract_numeric_field(response, "RIESGO_FP", 0.3)
        
        # Extraer inconsistencias
        inconsistencies = self._extract_list_field(response, "INCONSISTENCIAS")
        
        # Extraer razonamiento
        reasoning = self._extract_text_field(response, "RAZONAMIENTO", 
                                           "Validación basada en coherencia instrumental")
        
        # Generar ajustes de scoring
        scoring_adjustments = {
            "ai_confidence_boost": score_adjustment,
            "coherence_penalty": -0.1 if not is_coherent else 0.0,
            "false_positive_penalty": -false_positive_risk * 0.2
        }
        
        # Generar recomendaciones
        recommended_actions = self._generate_validation_recommendations(
            is_coherent, confidence_score, false_positive_risk, features
        )
        
        return AnomalyValidationResult(
            is_coherent=is_coherent,
            confidence_score=confidence_score,
            validation_reasoning=reasoning,
            detected_inconsistencies=inconsistencies,
            scoring_adjustments=scoring_adjustments,
            false_positive_risk=false_positive_risk,
            recommended_actions=recommended_actions,
            methodological_notes=f"Validación IA sobre {features.convergence_count} instrumentos convergentes"
        )
    
    def _extract_numeric_field(self, text: str, field: str, default: float) -> float:
        """Extraer campo numérico de respuesta IA."""
        try:
            lines = text.split('\n')
            for line in lines:
                if field in line:
                    # Buscar número en la línea
                    import re
                    numbers = re.findall(r'-?\d+\.?\d*', line)
                    if numbers:
                        return float(numbers[0])
            return default
        except:
            return default
    
    def _extract_list_field(self, text: str, field: str) -> List[str]:
        """Extraer campo de lista de respuesta IA."""
        try:
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if field in line:
                    # Buscar elementos en líneas siguientes
                    items = []
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip()
                        if next_line and not any(keyword in next_line for keyword in 
                                               ['AJUSTE', 'RIESGO', 'RAZONAMIENTO', 'CONFIANZA']):
                            items.append(next_line.lstrip('- '))
                        else:
                            break
                    return items
            return []
        except:
            return []
    
    def _extract_text_field(self, text: str, field: str, default: str) -> str:
        """Extraer campo de texto de respuesta IA."""
        try:
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if field in line:
                    # Tomar el resto de la línea o líneas siguientes
                    reasoning_parts = []
                    if ':' in line:
                        reasoning_parts.append(line.split(':', 1)[1].strip())
                    
                    # Buscar líneas adicionales
                    for j in range(i+1, len(lines)):
                        next_line = lines[j].strip()
                        if next_line and not any(keyword in next_line for keyword in 
                                               ['COHERENCIA', 'CONFIANZA', 'INCONSISTENCIAS', 'AJUSTE', 'RIESGO']):
                            reasoning_parts.append(next_line)
                        else:
                            break
                    
                    if reasoning_parts:
                        return ' '.join(reasoning_parts)
            return default
        except:
            return default
    
    def _generate_validation_recommendations(self,
                                           is_coherent: bool,
                                           confidence: float,
                                           fp_risk: float,
                                           features: InstrumentalFeatures) -> List[str]:
        """Generar recomendaciones basadas en validación."""
        
        recommendations = []
        
        if not is_coherent:
            recommendations.append("Revisar calibración de instrumentos - inconsistencias detectadas")
        
        if confidence < 0.5:
            recommendations.append("Adquirir datos adicionales - confianza insuficiente")
        
        if fp_risk > 0.7:
            recommendations.append("Alto riesgo de falso positivo - validación de campo requerida")
        
        if features.convergence_count < 2:
            recommendations.append("Insuficiente convergencia instrumental - añadir sensores")
        
        if features.temporal_persistence < 0.3:
            recommendations.append("Baja persistencia temporal - verificar estabilidad")
        
        if features.geometry_score < 0.4:
            recommendations.append("Geometría poco coherente - revisar patrones espaciales")
        
        # Recomendaciones positivas
        if is_coherent and confidence > 0.7 and fp_risk < 0.3:
            recommendations.append("Anomalía validada - proceder con investigación detallada")
        
        return recommendations
    
    def _fallback_validation(self,
                           features: InstrumentalFeatures,
                           current_score: float) -> AnomalyValidationResult:
        """Validación de respaldo cuando IA no está disponible."""
        
        # Validación determinista básica
        is_coherent = (
            features.convergence_count >= 2 and
            features.geometry_score > 0.3 and
            features.temporal_persistence > 0.2
        )
        
        confidence = min(1.0, (
            features.convergence_count * 0.3 +
            features.geometry_score * 0.4 +
            features.temporal_persistence * 0.3
        ))
        
        false_positive_risk = max(0.0, 1.0 - confidence)
        
        return AnomalyValidationResult(
            is_coherent=is_coherent,
            confidence_score=confidence,
            validation_reasoning="Validación determinista - IA no disponible",
            detected_inconsistencies=[],
            scoring_adjustments={"deterministic_adjustment": 0.0},
            false_positive_risk=false_positive_risk,
            recommended_actions=["Habilitar IA para validación avanzada"],
            methodological_notes="Validación básica sin asistente IA"
        )
    
    def batch_validate_anomalies(self,
                                anomalies: List[Tuple[InstrumentalFeatures, float]],
                                context: Dict[str, Any]) -> List[AnomalyValidationResult]:
        """Validar múltiples anomalías en lote."""
        
        results = []
        for features, score in anomalies:
            result = self.validate_anomaly(features, [], score, context)
            results.append(result)
        
        return results
    
    def generate_validation_report(self,
                                 validation_results: List[AnomalyValidationResult],
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Generar reporte de validación consolidado."""
        
        total_anomalies = len(validation_results)
        coherent_anomalies = sum(1 for r in validation_results if r.is_coherent)
        avg_confidence = sum(r.confidence_score for r in validation_results) / total_anomalies if total_anomalies > 0 else 0
        avg_fp_risk = sum(r.false_positive_risk for r in validation_results) / total_anomalies if total_anomalies > 0 else 0
        
        # Inconsistencias más comunes
        all_inconsistencies = []
        for r in validation_results:
            all_inconsistencies.extend(r.detected_inconsistencies)
        
        inconsistency_counts = {}
        for inc in all_inconsistencies:
            inconsistency_counts[inc] = inconsistency_counts.get(inc, 0) + 1
        
        return {
            "validation_summary": {
                "total_anomalies": total_anomalies,
                "coherent_anomalies": coherent_anomalies,
                "coherence_rate": coherent_anomalies / total_anomalies if total_anomalies > 0 else 0,
                "average_confidence": avg_confidence,
                "average_false_positive_risk": avg_fp_risk
            },
            "quality_assessment": {
                "high_confidence": sum(1 for r in validation_results if r.confidence_score > 0.7),
                "moderate_confidence": sum(1 for r in validation_results if 0.4 <= r.confidence_score <= 0.7),
                "low_confidence": sum(1 for r in validation_results if r.confidence_score < 0.4),
                "high_fp_risk": sum(1 for r in validation_results if r.false_positive_risk > 0.6)
            },
            "common_inconsistencies": dict(sorted(inconsistency_counts.items(), 
                                                key=lambda x: x[1], reverse=True)[:5]),
            "recommendations": self._generate_batch_recommendations(validation_results),
            "timestamp": datetime.now().isoformat(),
            "ai_available": self.is_available
        }
    
    def _generate_batch_recommendations(self,
                                      results: List[AnomalyValidationResult]) -> List[str]:
        """Generar recomendaciones para lote de validaciones."""
        
        recommendations = []
        
        coherence_rate = sum(1 for r in results if r.is_coherent) / len(results) if results else 0
        avg_confidence = sum(r.confidence_score for r in results) / len(results) if results else 0
        avg_fp_risk = sum(r.false_positive_risk for r in results) / len(results) if results else 0
        
        if coherence_rate < 0.6:
            recommendations.append("Baja coherencia general - revisar calibración del sistema")
        
        if avg_confidence < 0.5:
            recommendations.append("Confianza insuficiente - mejorar calidad de datos")
        
        if avg_fp_risk > 0.5:
            recommendations.append("Alto riesgo de falsos positivos - implementar filtros adicionales")
        
        if coherence_rate > 0.8 and avg_confidence > 0.7:
            recommendations.append("Sistema funcionando correctamente - continuar con análisis")
        
        return recommendations