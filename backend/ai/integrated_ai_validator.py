#!/usr/bin/env python3
"""
Integrador IA para Validación de Anomalías - ArcheoScope

Este módulo integra el AI Validator con el pipeline existente de ArcheoScope,
implementando la arquitectura ganadora:

Instrumentos + Algoritmos → detección de anomalías → features numéricas → 
IA (assistant) → score final + explicación

Integración con:
- CoreAnomalyDetector (detector base)
- ArchaeologicalAssistant (explicaciones)
- AnomalyValidationAssistant (validación cognitiva)
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np
from datetime import datetime

from .anomaly_validation_assistant import (
    AnomalyValidationAssistant, 
    InstrumentalFeatures, 
    AnomalyValidationResult
)

logger = logging.getLogger(__name__)

@dataclass
class IntegratedAnalysisResult:
    """Resultado de análisis integrado con validación IA."""
    # Resultados base del detector
    base_detection: Dict[str, Any]
    
    # Validación IA
    ai_validation: Optional[AnomalyValidationResult]
    
    # Score final ajustado
    final_score: float
    original_score: float
    
    # Explicación integrada
    integrated_explanation: str
    
    # Métricas de calidad
    quality_metrics: Dict[str, Any]
    
    # Recomendaciones finales
    final_recommendations: List[str]

class IntegratedAIValidator:
    """
    Integrador que combina detección instrumental con validación IA.
    
    Pipeline completo:
    1. CoreAnomalyDetector → detección base
    2. Extracción de features numéricas
    3. AnomalyValidationAssistant → validación cognitiva
    4. Score final ajustado + explicación integrada
    """
    
    def __init__(self, core_detector, archaeological_assistant=None):
        """
        Inicializar integrador IA.
        
        Args:
            core_detector: CoreAnomalyDetector existente
            archaeological_assistant: ArchaeologicalAssistant opcional
        """
        self.core_detector = core_detector
        self.archaeological_assistant = archaeological_assistant
        self.ai_validator = AnomalyValidationAssistant()
        
        logger.info("IntegratedAIValidator inicializado")
        logger.info(f"  - Core detector: {'✅' if core_detector else '❌'}")
        logger.info(f"  - Archaeological assistant: {'✅' if archaeological_assistant else '❌'}")
        logger.info(f"  - AI validator: {'✅' if self.ai_validator.is_available else '❌'}")
    
    @property
    def is_available(self) -> bool:
        """Verificar si el validador integrado está disponible."""
        return (
            self.core_detector is not None and
            self.ai_validator.is_available
        )
    
    async def analyze_with_ai_validation(self,
                                  lat: float, lon: float,
                                  lat_min: float, lat_max: float,
                                  lon_min: float, lon_max: float,
                                  region_name: str,
                                  context: Optional[Dict[str, Any]] = None) -> IntegratedAnalysisResult:
        """
        Ejecutar análisis completo con validación IA OPCIONAL.
        
        ARQUITECTURA RESILIENTE:
        [ Sensores + Algoritmos ]  ← núcleo autónomo
                    ↓ 
        [ Detección de anomalías ] ← núcleo autónomo
                    ↓ 
        [ Pre-score numérico ]     ← núcleo autónomo
                    ↓ 
        [ MCP Assistant ]          ← OPCIONAL (puede fallar)
                    ↓ 
        [ Score final + BD ]       ← siempre funciona
        
        Args:
            lat, lon: Coordenadas centrales
            lat_min, lat_max, lon_min, lon_max: Bounds de región
            region_name: Nombre de la región
            context: Contexto adicional
            
        Returns:
            Resultado integrado - SIEMPRE exitoso, con o sin IA
        """
        
        if not self.core_detector:
            raise ValueError("Core detector no disponible")
        
        context = context or {}
        
        try:
            # 1. DETECCIÓN BASE con Core Detector (NÚCLEO AUTÓNOMO)
            logger.info(f"🔍 Paso 1: Detección base para {region_name}")
            
            base_result = await self.core_detector.detect_anomaly(
                lat, lon, lat_min, lat_max, lon_min, lon_max, region_name
            )
            
            original_score = base_result.archaeological_probability
            logger.info(f"   Score base: {original_score:.3f}")
            
            # 2. EXTRACCIÓN DE FEATURES (NÚCLEO AUTÓNOMO)
            logger.info("📊 Paso 2: Extracción de features numéricas")
            
            instrumental_features = self._extract_instrumental_features(
                base_result, region_name, context
            )
            
            # 3. VALIDACIÓN IA (OPCIONAL - PUEDE FALLAR SIN AFECTAR EL ANÁLISIS)
            ai_validation = None
            assistant_score = 0.0
            assistant_status = "SKIPPED"
            assistant_version = "none"
            final_score = original_score  # Score base como fallback
            
            if self.ai_validator.is_available:
                logger.info("🤖 Paso 3: Validación cognitiva IA (OPCIONAL)")
                
                try:
                    # Intentar validación IA con timeout
                    ai_validation = self.ai_validator.validate_anomaly(
                        instrumental_features=instrumental_features,
                        raw_measurements=[
                            {
                                'instrument': m.instrument_name,
                                'value': m.value,
                                'threshold': m.threshold,
                                'exceeds_threshold': m.exceeds_threshold,
                                'confidence': m.confidence
                            }
                            for m in base_result.measurements
                        ],
                        current_score=original_score,
                        context=context
                    )
                    
                    # Aplicar ajustes de scoring
                    score_adjustments = sum(ai_validation.scoring_adjustments.values())
                    assistant_score = score_adjustments
                    final_score = max(0.0, min(1.0, original_score + score_adjustments))
                    assistant_status = "OK"
                    assistant_version = "integrated_ai_validator@1.0.0"
                    
                    logger.info(f"   ✅ IA validación exitosa:")
                    logger.info(f"      Coherente: {'✅' if ai_validation.is_coherent else '❌'}")
                    logger.info(f"      Confianza IA: {ai_validation.confidence_score:.3f}")
                    logger.info(f"      Ajuste score: {score_adjustments:+.3f}")
                    logger.info(f"      Score final: {final_score:.3f}")
                    
                except Exception as e:
                    # IA falló - continuar sin ella (RESILIENTE)
                    logger.warning(f"⚠️ IA no disponible: {e}")
                    logger.info("   📊 Continuando con score base (análisis autónomo)")
                    assistant_status = "ERROR"
                    assistant_score = 0.0
                    final_score = original_score
            else:
                logger.info("⚠️ IA no disponible - usando análisis autónomo")
                logger.info("   📊 Score base mantenido sin ajustes IA")
            
            # 4. EXPLICACIÓN INTEGRADA (SIEMPRE DISPONIBLE)
            logger.info("📝 Paso 4: Generación de explicación integrada")
            
            integrated_explanation = self._generate_integrated_explanation(
                base_result, ai_validation, original_score, final_score, assistant_status
            )
            
            # 5. MÉTRICAS DE CALIDAD (SIEMPRE DISPONIBLES)
            quality_metrics = self._calculate_quality_metrics(
                base_result, ai_validation, original_score, final_score, assistant_status
            )
            
            # 6. RECOMENDACIONES FINALES (SIEMPRE DISPONIBLES)
            final_recommendations = self._generate_final_recommendations(
                base_result, ai_validation, quality_metrics, assistant_status
            )
            
            # 7. CONSTRUIR RESULTADO INTEGRADO (SIEMPRE EXITOSO)
            result = IntegratedAnalysisResult(
                base_detection={
                    "archaeological_probability": original_score,
                    "environment_type": base_result.environment_type,
                    "confidence_level": base_result.confidence_level,
                    "instruments_converging": base_result.instruments_converging,
                    "known_site_nearby": base_result.known_site_nearby,
                    "measurements": [
                        {
                            "instrument": m.instrument_name,
                            "value": m.value,
                            "exceeds_threshold": m.exceeds_threshold,
                            "confidence": m.confidence
                        }
                        for m in base_result.measurements
                    ],
                    # TRAZABILIDAD CRÍTICA para BD
                    "assistant_metadata": {
                        "base_score": original_score,
                        "assistant_score": assistant_score,
                        "final_score": final_score,
                        "assistant_status": assistant_status,  # OK | SKIPPED | ERROR
                        "assistant_version": assistant_version
                    }
                },
                ai_validation=ai_validation,
                final_score=final_score,
                original_score=original_score,
                integrated_explanation=integrated_explanation,
                quality_metrics=quality_metrics,
                final_recommendations=final_recommendations
            )
            
            logger.info(f"✅ Análisis integrado completado para {region_name}")
            logger.info(f"   Score: {original_score:.3f} → {final_score:.3f}")
            logger.info(f"   IA Status: {assistant_status}")
            logger.info(f"   Calidad: {quality_metrics.get('overall_quality', 'unknown')}")
            
            return result
            
        except Exception as e:
            # ERROR CRÍTICO en núcleo - esto SÍ debe fallar
            logger.error(f"❌ Error CRÍTICO en análisis base (núcleo): {e}")
            raise  # Re-lanzar porque el núcleo debe funcionar
    
    def _extract_instrumental_features(self,
                                     base_result,
                                     region_name: str,
                                     context: Dict[str, Any]) -> InstrumentalFeatures:
        """Extraer features numéricas para IA."""
        
        # Extraer señales de instrumentos
        signals = {}
        for measurement in base_result.measurements:
            instrument_key = measurement.instrument_name.lower().replace(' ', '_')
            # Normalizar valor entre 0-1 basado en threshold
            if measurement.threshold > 0:
                normalized_value = min(1.0, abs(measurement.value) / measurement.threshold)
            else:
                normalized_value = min(1.0, abs(measurement.value))
            signals[instrument_key] = normalized_value
        
        # Calcular geometry score basado en convergencia
        geometry_score = min(1.0, base_result.instruments_converging / 5.0)
        
        # Temporal persistence (placeholder - podría venir de contexto)
        temporal_persistence = context.get('temporal_score', 0.5)
        
        # Historical proximity basado en sitios conocidos
        historical_proximity = 0.8 if base_result.known_site_nearby else 0.1
        
        return InstrumentalFeatures(
            tile_id=region_name,
            terrain_type=base_result.environment_type,
            signals=signals,
            geometry_score=geometry_score,
            temporal_persistence=temporal_persistence,
            historical_proximity=historical_proximity,
            convergence_count=base_result.instruments_converging,
            environment_confidence=base_result.environment_confidence
        )
    
    def _generate_integrated_explanation(self,
                                       base_result,
                                       ai_validation: Optional[AnomalyValidationResult],
                                       original_score: float,
                                       final_score: float,
                                       assistant_status: str) -> str:
        """Generar explicación integrada combinando detección base + IA (resiliente)."""
        
        explanation_parts = []
        
        # Explicación base (SIEMPRE disponible)
        explanation_parts.append(f"DETECCIÓN INSTRUMENTAL (NÚCLEO AUTÓNOMO):")
        explanation_parts.append(f"- {base_result.instruments_converging} instrumentos convergentes")
        explanation_parts.append(f"- Probabilidad arqueológica base: {original_score:.3f}")
        explanation_parts.append(f"- Ambiente: {base_result.environment_type}")
        
        if base_result.known_site_nearby:
            explanation_parts.append(f"- Sitio conocido cercano: {base_result.known_site_name}")
        
        # Validación IA (OPCIONAL - puede no estar)
        if assistant_status == "OK" and ai_validation:
            explanation_parts.append(f"\nVALIDACIÓN IA (OPCIONAL):")
            explanation_parts.append(f"- Estado: ✅ Exitosa")
            explanation_parts.append(f"- Coherencia: {'✅' if ai_validation.is_coherent else '❌'}")
            explanation_parts.append(f"- Confianza IA: {ai_validation.confidence_score:.3f}")
            explanation_parts.append(f"- Riesgo falso positivo: {ai_validation.false_positive_risk:.3f}")
            
            if ai_validation.detected_inconsistencies:
                explanation_parts.append(f"- Inconsistencias: {', '.join(ai_validation.detected_inconsistencies[:3])}")
            
            explanation_parts.append(f"- Razonamiento: {ai_validation.validation_reasoning}")
        elif assistant_status == "SKIPPED":
            explanation_parts.append(f"\nVALIDACIÓN IA (OPCIONAL):")
            explanation_parts.append(f"- Estado: ⚠️ No disponible")
            explanation_parts.append(f"- Análisis continúa con núcleo autónomo")
        elif assistant_status == "ERROR":
            explanation_parts.append(f"\nVALIDACIÓN IA (OPCIONAL):")
            explanation_parts.append(f"- Estado: ❌ Error temporal")
            explanation_parts.append(f"- Análisis continúa con núcleo autónomo")
            explanation_parts.append(f"- Candidata marcada para revalidación futura")
        
        # Score final (SIEMPRE disponible)
        score_change = final_score - original_score
        if abs(score_change) > 0.01:
            explanation_parts.append(f"\nSCORE FINAL:")
            explanation_parts.append(f"- Score ajustado: {original_score:.3f} → {final_score:.3f} ({score_change:+.3f})")
        else:
            explanation_parts.append(f"\nSCORE FINAL:")
            explanation_parts.append(f"- Score mantenido: {final_score:.3f} (sin ajustes IA)")
        
        return "\n".join(explanation_parts)
    
    def _calculate_quality_metrics(self,
                                 base_result,
                                 ai_validation: Optional[AnomalyValidationResult],
                                 original_score: float,
                                 final_score: float,
                                 assistant_status: str) -> Dict[str, Any]:
        """Calcular métricas de calidad del análisis."""
        
        metrics = {
            "instrumental_quality": {
                "convergence_count": base_result.instruments_converging,
                "environment_confidence": base_result.environment_confidence,
                "measurement_quality": sum(1 for m in base_result.measurements if m.confidence == "high") / len(base_result.measurements) if base_result.measurements else 0
            },
            "ai_quality": {
                "ai_available": assistant_status == "OK",
                "assistant_status": assistant_status,  # OK | SKIPPED | ERROR
                "coherence": ai_validation.is_coherent if ai_validation else None,
                "confidence": ai_validation.confidence_score if ai_validation else None,
                "false_positive_risk": ai_validation.false_positive_risk if ai_validation else None
            },
            "integrated_quality": {
                "score_stability": 1.0 - abs(final_score - original_score),
                "overall_confidence": final_score * (ai_validation.confidence_score if ai_validation else 0.7),
                "validation_agreement": ai_validation.is_coherent if ai_validation else True
            }
        }
        
        # Calcular calidad general
        instrumental_quality = min(1.0, base_result.instruments_converging / 3.0)
        ai_quality = ai_validation.confidence_score if ai_validation else 0.5
        overall_quality = (instrumental_quality + ai_quality) / 2.0
        
        if overall_quality > 0.8:
            quality_level = "excellent"
        elif overall_quality > 0.6:
            quality_level = "good"
        elif overall_quality > 0.4:
            quality_level = "moderate"
        else:
            quality_level = "low"
        
        metrics["overall_quality"] = quality_level
        metrics["overall_score"] = overall_quality
        
        return metrics
    
    def _generate_final_recommendations(self,
                                      base_result,
                                      ai_validation: Optional[AnomalyValidationResult],
                                      quality_metrics: Dict[str, Any]) -> List[str]:
        """Generar recomendaciones finales integradas."""
        
        recommendations = []
        
        # Recomendaciones basadas en calidad instrumental
        if base_result.instruments_converging < 2:
            recommendations.append("Insuficiente convergencia instrumental - añadir sensores")
        
        if base_result.environment_confidence < 0.6:
            recommendations.append("Baja confianza en clasificación de ambiente")
        
        # Recomendaciones basadas en validación IA
        if ai_validation:
            recommendations.extend(ai_validation.recommended_actions)
            
            if not ai_validation.is_coherent:
                recommendations.append("IA detectó inconsistencias - revisar calibración")
            
            if ai_validation.false_positive_risk > 0.7:
                recommendations.append("Alto riesgo de falso positivo según IA")
        else:
            recommendations.append("Habilitar IA para validación avanzada")
        
        # Recomendaciones basadas en calidad general
        overall_quality = quality_metrics.get("overall_quality", "unknown")
        
        if overall_quality == "excellent":
            recommendations.append("Análisis de alta calidad - proceder con investigación")
        elif overall_quality == "good":
            recommendations.append("Análisis confiable - considerar validación adicional")
        elif overall_quality == "moderate":
            recommendations.append("Calidad moderada - mejorar datos antes de proceder")
        else:
            recommendations.append("Calidad insuficiente - revisar metodología")
        
        # Eliminar duplicados y limitar
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:8]  # Máximo 8 recomendaciones
    
    async def batch_analyze_with_validation(self,
                                    regions: List[Dict[str, Any]],
                                    context: Optional[Dict[str, Any]] = None) -> List[IntegratedAnalysisResult]:
        """Analizar múltiples regiones con validación IA."""
        
        results = []
        
        for region in regions:
            try:
                result = await self.analyze_with_ai_validation(
                    lat=region['lat'],
                    lon=region['lon'],
                    lat_min=region['lat_min'],
                    lat_max=region['lat_max'],
                    lon_min=region['lon_min'],
                    lon_max=region['lon_max'],
                    region_name=region.get('name', 'Unknown'),
                    context=context
                )
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error analizando región {region.get('name', 'Unknown')}: {e}")
                continue
        
        return results
    
    def generate_validation_summary(self,
                                  results: List[IntegratedAnalysisResult]) -> Dict[str, Any]:
        """Generar resumen de validación para múltiples análisis."""
        
        if not results:
            return {"error": "No results to summarize"}
        
        # Estadísticas generales
        total_analyses = len(results)
        ai_validated = sum(1 for r in results if r.ai_validation is not None)
        coherent_analyses = sum(1 for r in results if r.ai_validation and r.ai_validation.is_coherent)
        
        # Scores
        original_scores = [r.original_score for r in results]
        final_scores = [r.final_score for r in results]
        
        avg_original = sum(original_scores) / len(original_scores)
        avg_final = sum(final_scores) / len(final_scores)
        avg_adjustment = avg_final - avg_original
        
        # Calidad
        quality_levels = [r.quality_metrics.get("overall_quality", "unknown") for r in results]
        quality_counts = {level: quality_levels.count(level) for level in set(quality_levels)}
        
        return {
            "summary": {
                "total_analyses": total_analyses,
                "ai_validated": ai_validated,
                "ai_validation_rate": ai_validated / total_analyses,
                "coherent_analyses": coherent_analyses,
                "coherence_rate": coherent_analyses / ai_validated if ai_validated > 0 else 0
            },
            "scoring": {
                "average_original_score": avg_original,
                "average_final_score": avg_final,
                "average_adjustment": avg_adjustment,
                "score_improvement": avg_adjustment > 0.01,
                "significant_adjustments": sum(1 for r in results if abs(r.final_score - r.original_score) > 0.05)
            },
            "quality_distribution": quality_counts,
            "recommendations": {
                "system_performance": "excellent" if coherent_analyses / ai_validated > 0.8 else "needs_improvement" if ai_validated > 0 else "enable_ai",
                "data_quality": "good" if avg_original > 0.5 else "improve_instruments",
                "ai_effectiveness": "high" if abs(avg_adjustment) > 0.02 else "moderate"
            },
            "timestamp": datetime.now().isoformat()
        }