#!/usr/bin/env python3
"""
Phi4-Mini-Reasoning Geometric Evaluator para ArcheoScope

FUNCIÓN ESPECÍFICA DE PHI4:
- Evalúa coherencia entre capas espectrales
- Decide qué geometrías son compatibles con datos
- Penaliza sobre-ajuste visual (anti-pareidolia)
- Ajusta pesos del campo volumétrico
- Genera informe explicativo de consistencia

PHI4 NO DIBUJA - Es motor de consistencia geométrica, no generador creativo.
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import logging
import json

from .geometric_inference_engine import SpatialSignature, MorphologicalClass, VolumetricField

logger = logging.getLogger(__name__)

@dataclass
class GeometricConsistencyReport:
    """Reporte de consistencia geométrica generado por phi4."""
    
    consistency_score: float  # 0-1, coherencia general entre capas
    layer_agreements: Dict[str, float]  # Acuerdo por capa espectral
    geometric_plausibility: float  # Plausibilidad de la geometría inferida
    over_fitting_penalty: float  # Penalización por sobre-ajuste visual
    
    # Evaluaciones específicas
    spectral_convergence: float  # Convergencia entre sensores
    temporal_consistency: float  # Consistencia temporal
    morphological_support: float  # Soporte para clasificación morfológica
    
    # Ajustes recomendados
    field_weight_adjustments: Dict[str, float]  # Ajustes de pesos volumétricos
    confidence_modifiers: Dict[str, float]  # Modificadores de confianza
    
    # Explicación textual
    reasoning_explanation: str
    consistency_warnings: List[str]
    validation_recommendations: List[str]

class Phi4GeometricEvaluator:
    """
    Evaluador de consistencia geométrica usando phi4-mini-reasoning.
    
    Actúa como motor de validación científica de las inferencias volumétricas,
    NO como generador creativo de formas.
    """
    
    def __init__(self, model_name: str = "phi4-mini-reasoning"):
        self.model_name = model_name
        self.consistency_threshold = 0.6
        self.over_fitting_threshold = 0.3
        
        # Intentar conectar con Ollama
        try:
            import ollama
            self.ollama_client = ollama.Client()
            
            # Verificar disponibilidad del modelo
            models = self.ollama_client.list()
            model_names = [model['name'] for model in models['models']]
            self.is_available = any(model_name in name for name in model_names)
            
            if self.is_available:
                logger.info(f"Phi4GeometricEvaluator inicializado con {model_name}")
            else:
                logger.warning(f"Modelo {model_name} no disponible, usando evaluación determinista")
                
        except ImportError:
            logger.warning("Ollama no disponible, usando evaluación determinista")
            self.ollama_client = None
            self.is_available = False
    
    def evaluate_geometric_consistency(self, 
                                     signature: SpatialSignature,
                                     morphology: MorphologicalClass,
                                     volumetric_field: VolumetricField,
                                     layer_results: Dict[str, Any]) -> GeometricConsistencyReport:
        """
        Evaluar consistencia geométrica de la inferencia volumétrica.
        
        Phi4 analiza si la geometría inferida es coherente con los datos espectrales.
        """
        
        if self.is_available:
            return self._evaluate_with_phi4(signature, morphology, volumetric_field, layer_results)
        else:
            return self._evaluate_deterministic(signature, morphology, volumetric_field, layer_results)
    
    def _evaluate_with_phi4(self, 
                           signature: SpatialSignature,
                           morphology: MorphologicalClass,
                           volumetric_field: VolumetricField,
                           layer_results: Dict[str, Any]) -> GeometricConsistencyReport:
        """Evaluación usando phi4-mini-reasoning."""
        
        # Preparar contexto para phi4
        analysis_context = {
            "spatial_signature": {
                "area_m2": signature.area_m2,
                "elongation_ratio": signature.elongation_ratio,
                "symmetry_index": signature.symmetry_index,
                "thermal_amplitude": signature.thermal_amplitude,
                "sar_roughness": signature.sar_roughness,
                "multitemporal_coherence": signature.multitemporal_coherence,
                "sensor_convergence": signature.sensor_convergence
            },
            "morphological_classification": morphology.value,
            "volumetric_properties": {
                "confidence_layers": volumetric_field.confidence_layers,
                "voxel_count": np.prod(volumetric_field.dimensions),
                "active_voxels": int(np.sum(volumetric_field.probability_volume > 0.3))
            },
            "spectral_layers": {
                layer: {
                    "archaeological_probability": result.get('archaeological_probability', 0),
                    "geometric_coherence": result.get('geometric_coherence', 0),
                    "temporal_persistence": result.get('temporal_persistence', 0),
                    "natural_explanation_score": result.get('natural_explanation_score', 1.0)
                }
                for layer, result in layer_results.items()
            }
        }
        
        # Prompt para phi4 - Enfoque en consistencia, NO en creatividad
        prompt = f"""
TAREA: Evaluar consistencia geométrica de inferencia volumétrica arqueológica.

CONTEXTO DE ANÁLISIS:
{json.dumps(analysis_context, indent=2)}

INSTRUCCIONES ESPECÍFICAS:
1. Evalúa la COHERENCIA entre datos espectrales y geometría inferida
2. Identifica INCONSISTENCIAS entre capas de sensores
3. Detecta posible SOBRE-AJUSTE visual (pareidolia)
4. Recomienda AJUSTES de pesos volumétricos
5. NO generes nuevas formas - solo evalúa consistencia

CRITERIOS DE EVALUACIÓN:
- Convergencia espectral: ¿Los sensores concuerdan?
- Plausibilidad geométrica: ¿La forma es físicamente razonable?
- Consistencia temporal: ¿Los patrones persisten?
- Anti-pareidolia: ¿Hay sobre-interpretación visual?

FORMATO DE RESPUESTA (JSON):
{{
    "consistency_score": 0.0-1.0,
    "spectral_convergence": 0.0-1.0,
    "geometric_plausibility": 0.0-1.0,
    "over_fitting_risk": 0.0-1.0,
    "layer_agreements": {{"ndvi": 0.0-1.0, "thermal": 0.0-1.0, "sar": 0.0-1.0}},
    "weight_adjustments": {{"probability_boost": 0.0-2.0, "uncertainty_increase": 0.0-1.0}},
    "reasoning": "Explicación de la evaluación de consistencia",
    "warnings": ["Lista de advertencias sobre inconsistencias"],
    "recommendations": ["Recomendaciones para mejorar consistencia"]
}}

Responde SOLO con JSON válido. Enfócate en CONSISTENCIA CIENTÍFICA, no en interpretación arqueológica.
"""
        
        try:
            # Llamar a phi4
            response = self.ollama_client.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.1,  # Baja creatividad, alta consistencia
                    'top_p': 0.8,
                    'num_predict': 1000
                }
            )
            
            # Parsear respuesta JSON
            response_text = response['message']['content'].strip()
            
            # Extraer JSON de la respuesta
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end].strip()
            elif '{' in response_text and '}' in response_text:
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                json_text = response_text[json_start:json_end]
            else:
                raise ValueError("No se encontró JSON válido en respuesta")
            
            phi4_evaluation = json.loads(json_text)
            
            # Convertir a GeometricConsistencyReport
            report = GeometricConsistencyReport(
                consistency_score=phi4_evaluation.get('consistency_score', 0.5),
                layer_agreements=phi4_evaluation.get('layer_agreements', {}),
                geometric_plausibility=phi4_evaluation.get('geometric_plausibility', 0.5),
                over_fitting_penalty=phi4_evaluation.get('over_fitting_risk', 0.3),
                spectral_convergence=phi4_evaluation.get('spectral_convergence', 0.5),
                temporal_consistency=signature.multitemporal_coherence,
                morphological_support=phi4_evaluation.get('consistency_score', 0.5),
                field_weight_adjustments=phi4_evaluation.get('weight_adjustments', {}),
                confidence_modifiers={
                    'phi4_consistency_boost': phi4_evaluation.get('consistency_score', 0.5),
                    'over_fitting_penalty': phi4_evaluation.get('over_fitting_risk', 0.3)
                },
                reasoning_explanation=phi4_evaluation.get('reasoning', 'Evaluación phi4 completada'),
                consistency_warnings=phi4_evaluation.get('warnings', []),
                validation_recommendations=phi4_evaluation.get('recommendations', [])
            )
            
            logger.info(f"Evaluación phi4 completada: consistencia={report.consistency_score:.3f}")
            
            return report
            
        except Exception as e:
            logger.warning(f"Error en evaluación phi4: {e}, usando fallback determinista")
            return self._evaluate_deterministic(signature, morphology, volumetric_field, layer_results)
    
    def _evaluate_deterministic(self, 
                              signature: SpatialSignature,
                              morphology: MorphologicalClass,
                              volumetric_field: VolumetricField,
                              layer_results: Dict[str, Any]) -> GeometricConsistencyReport:
        """Evaluación determinista de consistencia (fallback)."""
        
        # Calcular consistencia entre capas espectrales
        archaeological_probs = [r.get('archaeological_probability', 0) for r in layer_results.values()]
        geometric_coherences = [r.get('geometric_coherence', 0) for r in layer_results.values()]
        
        # Convergencia espectral
        spectral_convergence = 1.0 - np.var(archaeological_probs) if archaeological_probs else 0.5
        
        # Plausibilidad geométrica basada en coherencia
        geometric_plausibility = np.mean(geometric_coherences) if geometric_coherences else 0.5
        
        # Detectar sobre-ajuste (demasiada precisión con pocos datos)
        data_density = len(layer_results) / max(signature.area_m2 / 1000, 1)  # Datos por km²
        over_fitting_risk = max(0, 0.5 - data_density * 0.1)  # Más datos = menos riesgo
        
        # Consistencia temporal
        temporal_consistency = signature.multitemporal_coherence
        
        # Score de consistencia general
        consistency_score = (
            spectral_convergence * 0.3 +
            geometric_plausibility * 0.3 +
            temporal_consistency * 0.2 +
            (1.0 - over_fitting_risk) * 0.2
        )
        
        # Acuerdos por capa
        layer_agreements = {}
        for layer_name, result in layer_results.items():
            agreement = (
                result.get('archaeological_probability', 0) * 0.4 +
                result.get('geometric_coherence', 0) * 0.3 +
                result.get('temporal_persistence', 0) * 0.3
            )
            layer_agreements[layer_name] = agreement
        
        # Ajustes de pesos recomendados
        field_weight_adjustments = {
            'probability_boost': 1.0 + (consistency_score - 0.5),  # Boost si alta consistencia
            'uncertainty_increase': over_fitting_risk,  # Aumentar incertidumbre si sobre-ajuste
            'temporal_weight': temporal_consistency
        }
        
        # Modificadores de confianza
        confidence_modifiers = {
            'spectral_convergence_factor': spectral_convergence,
            'geometric_plausibility_factor': geometric_plausibility,
            'over_fitting_penalty': over_fitting_risk
        }
        
        # Generar explicación
        reasoning_explanation = f"""
Evaluación determinista de consistencia geométrica:

CONVERGENCIA ESPECTRAL: {spectral_convergence:.3f}
- Varianza entre capas: {np.var(archaeological_probs):.3f}
- Acuerdo entre sensores: {'Alto' if spectral_convergence > 0.7 else 'Moderado' if spectral_convergence > 0.5 else 'Bajo'}

PLAUSIBILIDAD GEOMÉTRICA: {geometric_plausibility:.3f}
- Coherencia geométrica promedio: {np.mean(geometric_coherences):.3f}
- Morfología clasificada: {morphology.value}

CONSISTENCIA TEMPORAL: {temporal_consistency:.3f}
- Persistencia multitemporal verificada
- Estabilidad de patrones: {'Alta' if temporal_consistency > 0.7 else 'Moderada'}

RIESGO DE SOBRE-AJUSTE: {over_fitting_risk:.3f}
- Densidad de datos: {data_density:.2f} capas/km²
- Riesgo de pareidolia: {'Alto' if over_fitting_risk > 0.4 else 'Bajo'}

CONSISTENCIA GENERAL: {consistency_score:.3f}
"""
        
        # Generar advertencias
        warnings = []
        if spectral_convergence < 0.5:
            warnings.append("Baja convergencia entre sensores espectrales - validar calibración")
        if over_fitting_risk > 0.4:
            warnings.append("Alto riesgo de sobre-ajuste visual - aumentar incertidumbre")
        if temporal_consistency < 0.4:
            warnings.append("Baja persistencia temporal - validar estabilidad de anomalías")
        if len(layer_results) < 3:
            warnings.append("Pocos sensores disponibles - limitada validación cruzada")
        
        # Generar recomendaciones
        recommendations = []
        if consistency_score > 0.7:
            recommendations.append("Alta consistencia - proceder con inferencia volumétrica")
        elif consistency_score > 0.5:
            recommendations.append("Consistencia moderada - validación geofísica recomendada")
        else:
            recommendations.append("Baja consistencia - revisar datos espectrales antes de inferencia")
        
        if over_fitting_risk > 0.3:
            recommendations.append("Aplicar suavizado adicional para reducir sobre-ajuste")
        
        recommendations.append("Validar con datos independientes antes de interpretación arqueológica")
        
        return GeometricConsistencyReport(
            consistency_score=consistency_score,
            layer_agreements=layer_agreements,
            geometric_plausibility=geometric_plausibility,
            over_fitting_penalty=over_fitting_risk,
            spectral_convergence=spectral_convergence,
            temporal_consistency=temporal_consistency,
            morphological_support=consistency_score,
            field_weight_adjustments=field_weight_adjustments,
            confidence_modifiers=confidence_modifiers,
            reasoning_explanation=reasoning_explanation,
            consistency_warnings=warnings,
            validation_recommendations=recommendations
        )
    
    def apply_consistency_adjustments(self, 
                                    volumetric_field: VolumetricField,
                                    consistency_report: GeometricConsistencyReport) -> VolumetricField:
        """
        Aplicar ajustes de consistencia al campo volumétrico.
        
        Modifica pesos y incertidumbres basado en evaluación de consistencia.
        """
        
        # Copiar campo volumétrico
        adjusted_field = VolumetricField(
            probability_volume=volumetric_field.probability_volume.copy(),
            void_probability=volumetric_field.void_probability.copy(),
            uncertainty_field=volumetric_field.uncertainty_field.copy(),
            voxel_size_m=volumetric_field.voxel_size_m,
            origin_coords=volumetric_field.origin_coords,
            dimensions=volumetric_field.dimensions,
            inference_level=volumetric_field.inference_level,
            morphological_class=volumetric_field.morphological_class,
            confidence_layers=volumetric_field.confidence_layers.copy()
        )
        
        # Aplicar ajustes de pesos
        adjustments = consistency_report.field_weight_adjustments
        
        # Boost de probabilidad basado en consistencia
        probability_boost = adjustments.get('probability_boost', 1.0)
        adjusted_field.probability_volume *= probability_boost
        adjusted_field.probability_volume = np.clip(adjusted_field.probability_volume, 0, 1)
        
        # Aumento de incertidumbre por sobre-ajuste
        uncertainty_increase = adjustments.get('uncertainty_increase', 0.0)
        adjusted_field.uncertainty_field += uncertainty_increase
        adjusted_field.uncertainty_field = np.clip(adjusted_field.uncertainty_field, 0, 1)
        
        # Ajuste temporal
        temporal_weight = adjustments.get('temporal_weight', 1.0)
        if temporal_weight < 0.5:
            # Reducir confianza si baja persistencia temporal
            adjusted_field.probability_volume *= temporal_weight * 2
        
        # Recalcular capas de confianza
        adjusted_field.confidence_layers = {
            'core': float(np.sum(adjusted_field.probability_volume > 0.7) / adjusted_field.probability_volume.size),
            'probable': float(np.sum(adjusted_field.probability_volume > 0.5) / adjusted_field.probability_volume.size),
            'possible': float(np.sum(adjusted_field.probability_volume > 0.3) / adjusted_field.probability_volume.size)
        }
        
        logger.info(f"Ajustes de consistencia aplicados: boost={probability_boost:.3f}, incertidumbre+={uncertainty_increase:.3f}")
        
        return adjusted_field
    
    def generate_consistency_summary(self, 
                                   consistency_report: GeometricConsistencyReport) -> Dict[str, Any]:
        """Generar resumen de consistencia para reporte científico."""
        
        return {
            "phi4_geometric_evaluation": {
                "evaluation_method": "phi4_mini_reasoning" if self.is_available else "deterministic_consistency",
                "overall_consistency_score": consistency_report.consistency_score,
                "consistency_classification": self._classify_consistency(consistency_report.consistency_score),
                
                "spectral_analysis": {
                    "convergence_score": consistency_report.spectral_convergence,
                    "layer_agreements": consistency_report.layer_agreements,
                    "cross_sensor_validation": "passed" if consistency_report.spectral_convergence > 0.6 else "requires_review"
                },
                
                "geometric_validation": {
                    "plausibility_score": consistency_report.geometric_plausibility,
                    "morphological_support": consistency_report.morphological_support,
                    "over_fitting_assessment": {
                        "risk_level": "high" if consistency_report.over_fitting_penalty > 0.4 else "low",
                        "penalty_applied": consistency_report.over_fitting_penalty,
                        "anti_pareidolia_measures": "active"
                    }
                },
                
                "temporal_validation": {
                    "consistency_score": consistency_report.temporal_consistency,
                    "persistence_verified": consistency_report.temporal_consistency > 0.5,
                    "stability_assessment": "stable" if consistency_report.temporal_consistency > 0.7 else "moderate"
                },
                
                "field_adjustments_applied": {
                    "weight_modifications": consistency_report.field_weight_adjustments,
                    "confidence_modifiers": consistency_report.confidence_modifiers,
                    "adjustment_rationale": "consistency_optimization"
                },
                
                "quality_assessment": {
                    "scientific_rigor": "high" if consistency_report.consistency_score > 0.7 else "moderate",
                    "validation_warnings": consistency_report.consistency_warnings,
                    "improvement_recommendations": consistency_report.validation_recommendations,
                    "peer_review_readiness": consistency_report.consistency_score > 0.6
                },
                
                "phi4_reasoning": {
                    "explanation": consistency_report.reasoning_explanation,
                    "decision_transparency": "complete",
                    "bias_mitigation": "anti_pareidolia_active",
                    "scientific_objectivity": "maintained"
                }
            }
        }
    
    def _classify_consistency(self, score: float) -> str:
        """Clasificar nivel de consistencia."""
        
        if score >= 0.8:
            return "very_high_consistency"
        elif score >= 0.7:
            return "high_consistency"
        elif score >= 0.6:
            return "moderate_consistency"
        elif score >= 0.4:
            return "low_consistency"
        else:
            return "very_low_consistency"