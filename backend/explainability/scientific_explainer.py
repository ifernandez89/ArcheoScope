#!/usr/bin/env python3
"""
Módulo de explicabilidad científica para ArcheoScope.

Proporciona explicaciones detalladas de por qué cada anomalía fue detectada,
qué capas contribuyeron, y qué explicaciones naturales fueron descartadas.

Esto pone a ArcheoScope por delante metodológicamente de otros sistemas.
"""

import numpy as np
from typing import Dict, List, Any, Tuple
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ContributionType(Enum):
    """Tipo de contribución de una capa al análisis."""
    PRIMARY = "primary"           # Contribución principal
    SUPPORTING = "supporting"     # Contribución de apoyo
    CONTRADICTORY = "contradictory"  # Contradice la hipótesis
    NEUTRAL = "neutral"           # No contribuye significativamente

@dataclass
class LayerContribution:
    """Contribución de una capa específica al análisis."""
    layer_name: str
    contribution_type: ContributionType
    weight: float                 # Peso en la decisión final (0-1)
    confidence: float            # Confianza en esta contribución (0-1)
    evidence_strength: float     # Fuerza de la evidencia (0-1)
    specific_indicators: List[str]  # Indicadores específicos detectados
    natural_alternatives: List[str]  # Explicaciones naturales consideradas

@dataclass
class NaturalExplanation:
    """Explicación natural considerada y descartada."""
    process_name: str
    plausibility_score: float    # Qué tan plausible es (0-1)
    rejection_reason: str        # Por qué fue descartada
    supporting_evidence: List[str]  # Evidencia que la apoyaría
    contradicting_evidence: List[str]  # Evidencia que la contradice

@dataclass
class AnomalyExplanation:
    """Explicación completa de una anomalía detectada."""
    anomaly_id: str
    archaeological_probability: float
    confidence_level: str
    layer_contributions: List[LayerContribution]
    natural_explanations_considered: List[NaturalExplanation]
    decision_rationale: str
    uncertainty_factors: List[str]
    validation_recommendations: List[str]

class ScientificExplainer:
    """
    Explicador científico para análisis arqueológicos.
    
    Proporciona explicaciones detalladas y transparentes de cada
    decisión del sistema, permitiendo validación y reproducibilidad.
    """
    
    def __init__(self):
        """Inicializar explicador científico."""
        self.natural_processes_db = self._load_natural_processes_database()
        logger.info("ScientificExplainer inicializado")
    
    def _load_natural_processes_database(self) -> Dict[str, Dict[str, Any]]:
        """Cargar base de datos de procesos naturales conocidos."""
        
        return {
            'erosion_patterns': {
                'description': 'Patrones de erosión natural',
                'typical_indicators': ['gradual_transitions', 'flow_direction_consistency', 'topographic_correlation'],
                'spatial_characteristics': 'smooth_gradients',
                'temporal_behavior': 'gradual_change'
            },
            'vegetation_stress': {
                'description': 'Estrés natural de vegetación',
                'typical_indicators': ['seasonal_variation', 'moisture_correlation', 'soil_type_correlation'],
                'spatial_characteristics': 'environmental_gradients',
                'temporal_behavior': 'seasonal_cycles'
            },
            'geological_features': {
                'description': 'Características geológicas naturales',
                'typical_indicators': ['mineral_composition', 'structural_geology', 'age_consistency'],
                'spatial_characteristics': 'geological_boundaries',
                'temporal_behavior': 'stable_over_time'
            },
            'hydrological_processes': {
                'description': 'Procesos hidrológicos naturales',
                'typical_indicators': ['water_flow_patterns', 'seasonal_flooding', 'drainage_networks'],
                'spatial_characteristics': 'watershed_boundaries',
                'temporal_behavior': 'seasonal_and_event_driven'
            },
            'climatic_variations': {
                'description': 'Variaciones climáticas naturales',
                'typical_indicators': ['temperature_gradients', 'precipitation_patterns', 'wind_effects'],
                'spatial_characteristics': 'regional_gradients',
                'temporal_behavior': 'cyclical_patterns'
            }
        }
    
    def explain_anomaly(self, anomaly_data: Dict[str, Any], 
                       analysis_results: Dict[str, Any]) -> AnomalyExplanation:
        """
        Generar explicación completa de una anomalía detectada.
        
        Args:
            anomaly_data: Datos de la anomalía específica
            analysis_results: Resultados completos del análisis
            
        Returns:
            Explicación científica detallada
        """
        
        anomaly_id = anomaly_data.get('id', 'unknown')
        logger.info(f"Generando explicación para anomalía: {anomaly_id}")
        
        # Analizar contribuciones de cada capa
        layer_contributions = self._analyze_layer_contributions(anomaly_data, analysis_results)
        
        # Evaluar explicaciones naturales alternativas
        natural_explanations = self._evaluate_natural_explanations(anomaly_data, analysis_results)
        
        # Generar rationale de decisión
        decision_rationale = self._generate_decision_rationale(layer_contributions, natural_explanations)
        
        # Identificar factores de incertidumbre
        uncertainty_factors = self._identify_uncertainty_factors(anomaly_data, analysis_results)
        
        # Generar recomendaciones de validación
        validation_recommendations = self._generate_validation_recommendations(
            layer_contributions, natural_explanations, uncertainty_factors
        )
        
        # Determinar nivel de confianza
        confidence_level = self._determine_confidence_level(layer_contributions, natural_explanations)
        
        return AnomalyExplanation(
            anomaly_id=anomaly_id,
            archaeological_probability=anomaly_data.get('archaeological_probability', 0.0),
            confidence_level=confidence_level,
            layer_contributions=layer_contributions,
            natural_explanations_considered=natural_explanations,
            decision_rationale=decision_rationale,
            uncertainty_factors=uncertainty_factors,
            validation_recommendations=validation_recommendations
        )
    
    def _analyze_layer_contributions(self, anomaly_data: Dict[str, Any], 
                                   analysis_results: Dict[str, Any]) -> List[LayerContribution]:
        """Analizar contribución de cada capa al análisis."""
        
        contributions = []
        
        # Obtener evaluaciones por regla
        evaluations = analysis_results.get('physics_results', {}).get('evaluations', {})
        
        for rule_name, evaluation in evaluations.items():
            # Determinar capas involucradas en esta regla
            involved_layers = self._get_layers_for_rule(rule_name)
            
            for layer_name in involved_layers:
                contribution = self._calculate_layer_contribution(
                    layer_name, rule_name, evaluation, anomaly_data
                )
                contributions.append(contribution)
        
        return contributions
    
    def _get_layers_for_rule(self, rule_name: str) -> List[str]:
        """Obtener capas involucradas en una regla específica."""
        
        layer_mapping = {
            'vegetation_topography_decoupling': ['ndvi_vegetation', 'surface_elevation'],
            'thermal_residual_patterns': ['thermal_lst'],
            'sar_geometric_anomalies': ['sar_backscatter'],
            'surface_roughness_analysis': ['surface_roughness'],
            'soil_salinity_patterns': ['soil_salinity'],
            'seismic_resonance_analysis': ['seismic_resonance']
        }
        
        return layer_mapping.get(rule_name, [rule_name])
    
    def _calculate_layer_contribution(self, layer_name: str, rule_name: str, 
                                    evaluation: Dict[str, Any], 
                                    anomaly_data: Dict[str, Any]) -> LayerContribution:
        """Calcular contribución específica de una capa."""
        
        # Extraer métricas de la evaluación
        archaeological_prob = evaluation.get('archaeological_probability', 0.0)
        confidence = evaluation.get('confidence', 0.0)
        geometric_coherence = evaluation.get('geometric_coherence', 0.0)
        
        # Determinar tipo de contribución
        if archaeological_prob > 0.6:
            contribution_type = ContributionType.PRIMARY
        elif archaeological_prob > 0.3:
            contribution_type = ContributionType.SUPPORTING
        elif archaeological_prob < 0.2:
            contribution_type = ContributionType.CONTRADICTORY
        else:
            contribution_type = ContributionType.NEUTRAL
        
        # Calcular peso en la decisión
        weight = self._calculate_contribution_weight(archaeological_prob, confidence, geometric_coherence)
        
        # Identificar indicadores específicos
        specific_indicators = self._identify_specific_indicators(layer_name, evaluation)
        
        # Identificar alternativas naturales para esta capa
        natural_alternatives = self._identify_natural_alternatives_for_layer(layer_name, evaluation)
        
        return LayerContribution(
            layer_name=layer_name,
            contribution_type=contribution_type,
            weight=weight,
            confidence=confidence,
            evidence_strength=geometric_coherence,
            specific_indicators=specific_indicators,
            natural_alternatives=natural_alternatives
        )
    
    def _calculate_contribution_weight(self, prob: float, confidence: float, coherence: float) -> float:
        """Calcular peso de contribución de una capa."""
        
        # Peso combinado basado en probabilidad, confianza y coherencia
        weight = (prob * 0.5 + confidence * 0.3 + coherence * 0.2)
        return min(weight, 1.0)
    
    def _identify_specific_indicators(self, layer_name: str, evaluation: Dict[str, Any]) -> List[str]:
        """Identificar indicadores específicos detectados en una capa."""
        
        indicators = []
        
        # Indicadores por tipo de capa
        if 'vegetation' in layer_name:
            if evaluation.get('geometric_coherence', 0) > 0.5:
                indicators.append('geometric_vegetation_patterns')
            if evaluation.get('archaeological_probability', 0) > 0.6:
                indicators.append('vegetation_topography_decoupling')
        
        elif 'thermal' in layer_name:
            if evaluation.get('archaeological_probability', 0) > 0.5:
                indicators.append('thermal_inertia_anomalies')
            if evaluation.get('geometric_coherence', 0) > 0.4:
                indicators.append('structured_thermal_patterns')
        
        elif 'sar' in layer_name:
            if evaluation.get('geometric_coherence', 0) > 0.6:
                indicators.append('geometric_backscatter_anomalies')
            if evaluation.get('archaeological_probability', 0) > 0.5:
                indicators.append('surface_roughness_inconsistencies')
        
        elif 'roughness' in layer_name:
            if evaluation.get('archaeological_probability', 0) > 0.4:
                indicators.append('compaction_signatures')
            indicators.append('surface_texture_anomalies')
        
        elif 'salinity' in layer_name:
            if evaluation.get('archaeological_probability', 0) > 0.4:
                indicators.append('drainage_pattern_anomalies')
            indicators.append('soil_chemistry_inconsistencies')
        
        elif 'seismic' in layer_name:
            if evaluation.get('archaeological_probability', 0) > 0.5:
                indicators.append('subsurface_cavity_signatures')
            indicators.append('resonance_anomalies')
        
        return indicators
    
    def _identify_natural_alternatives_for_layer(self, layer_name: str, 
                                               evaluation: Dict[str, Any]) -> List[str]:
        """Identificar alternativas naturales consideradas para una capa."""
        
        alternatives = []
        
        if 'vegetation' in layer_name:
            alternatives.extend(['seasonal_stress', 'soil_moisture_variation', 'microclimate_effects'])
        
        elif 'thermal' in layer_name:
            alternatives.extend(['solar_exposure_variation', 'soil_composition_differences', 'moisture_content_variation'])
        
        elif 'sar' in layer_name:
            alternatives.extend(['natural_surface_roughness', 'vegetation_density_variation', 'moisture_effects'])
        
        elif 'roughness' in layer_name:
            alternatives.extend(['natural_compaction', 'erosion_patterns', 'geological_features'])
        
        elif 'salinity' in layer_name:
            alternatives.extend(['natural_drainage', 'evaporation_patterns', 'geological_salt_deposits'])
        
        elif 'seismic' in layer_name:
            alternatives.extend(['natural_cavities', 'geological_structures', 'groundwater_effects'])
        
        return alternatives
    
    def _evaluate_natural_explanations(self, anomaly_data: Dict[str, Any], 
                                     analysis_results: Dict[str, Any]) -> List[NaturalExplanation]:
        """Evaluar explicaciones naturales alternativas."""
        
        explanations = []
        
        for process_name, process_data in self.natural_processes_db.items():
            explanation = self._evaluate_single_natural_explanation(
                process_name, process_data, anomaly_data, analysis_results
            )
            explanations.append(explanation)
        
        return explanations
    
    def _evaluate_single_natural_explanation(self, process_name: str, process_data: Dict[str, Any],
                                           anomaly_data: Dict[str, Any], 
                                           analysis_results: Dict[str, Any]) -> NaturalExplanation:
        """Evaluar una explicación natural específica."""
        
        # Calcular plausibilidad basada en indicadores presentes
        plausibility = self._calculate_natural_plausibility(process_name, process_data, analysis_results)
        
        # Determinar razón de rechazo si aplica
        rejection_reason = self._determine_rejection_reason(process_name, plausibility, analysis_results)
        
        # Identificar evidencia que apoyaría esta explicación
        supporting_evidence = self._identify_supporting_evidence(process_name, process_data)
        
        # Identificar evidencia que la contradice
        contradicting_evidence = self._identify_contradicting_evidence(process_name, analysis_results)
        
        return NaturalExplanation(
            process_name=process_name,
            plausibility_score=plausibility,
            rejection_reason=rejection_reason,
            supporting_evidence=supporting_evidence,
            contradicting_evidence=contradicting_evidence
        )
    
    def _calculate_natural_plausibility(self, process_name: str, process_data: Dict[str, Any],
                                      analysis_results: Dict[str, Any]) -> float:
        """Calcular plausibilidad de una explicación natural."""
        
        # Plausibilidad base por tipo de proceso
        base_plausibility = {
            'erosion_patterns': 0.7,
            'vegetation_stress': 0.6,
            'geological_features': 0.8,
            'hydrological_processes': 0.5,
            'climatic_variations': 0.4
        }
        
        base = base_plausibility.get(process_name, 0.5)
        
        # Ajustar basado en coherencia geométrica (procesos naturales tienden a ser menos geométricos)
        evaluations = analysis_results.get('physics_results', {}).get('evaluations', {})
        mean_geometric_coherence = float(np.mean([
            eval_data.get('geometric_coherence', 0) for eval_data in evaluations.values()
        ]))
        
        # Alta coherencia geométrica reduce plausibilidad de explicaciones naturales
        geometric_penalty = mean_geometric_coherence * 0.5
        
        plausibility = max(0.1, base - geometric_penalty)
        
        return plausibility
    
    def _determine_rejection_reason(self, process_name: str, plausibility: float,
                                  analysis_results: Dict[str, Any]) -> str:
        """Determinar razón de rechazo de explicación natural."""
        
        if plausibility > 0.6:
            return "Explicación natural plausible - requiere análisis adicional"
        elif plausibility > 0.4:
            return "Explicación natural posible pero inconsistente con patrones geométricos observados"
        else:
            return "Explicación natural improbable debido a alta coherencia geométrica y persistencia espacial"
    
    def _identify_supporting_evidence(self, process_name: str, process_data: Dict[str, Any]) -> List[str]:
        """Identificar evidencia que apoyaría una explicación natural."""
        
        return [
            f"Presencia de {indicator}" for indicator in process_data.get('typical_indicators', [])
        ]
    
    def _identify_contradicting_evidence(self, process_name: str, 
                                       analysis_results: Dict[str, Any]) -> List[str]:
        """Identificar evidencia que contradice una explicación natural."""
        
        contradictions = []
        
        evaluations = analysis_results.get('physics_results', {}).get('evaluations', {})
        
        # Coherencia geométrica alta contradice procesos naturales
        for rule_name, evaluation in evaluations.items():
            geometric_coherence = evaluation.get('geometric_coherence', 0)
            if geometric_coherence > 0.5:
                contradictions.append(f"Alta coherencia geométrica en {rule_name}")
        
        return contradictions
    
    def _generate_decision_rationale(self, layer_contributions: List[LayerContribution],
                                   natural_explanations: List[NaturalExplanation]) -> str:
        """Generar rationale de la decisión tomada."""
        
        # Identificar contribuciones principales
        primary_contributions = [c for c in layer_contributions if c.contribution_type == ContributionType.PRIMARY]
        
        # Identificar explicaciones naturales más plausibles
        most_plausible_natural = max(natural_explanations, key=lambda x: x.plausibility_score)
        
        rationale = f"Decisión basada en {len(primary_contributions)} contribuciones principales: "
        rationale += ", ".join([c.layer_name for c in primary_contributions])
        
        rationale += f". Explicación natural más plausible ({most_plausible_natural.process_name}) "
        rationale += f"tiene plausibilidad de {most_plausible_natural.plausibility_score:.2f}. "
        
        if most_plausible_natural.plausibility_score < 0.5:
            rationale += "Explicaciones naturales consideradas insuficientes para explicar patrones observados."
        else:
            rationale += "Explicaciones naturales requieren consideración adicional."
        
        return rationale
    
    def _identify_uncertainty_factors(self, anomaly_data: Dict[str, Any],
                                    analysis_results: Dict[str, Any]) -> List[str]:
        """Identificar factores de incertidumbre en el análisis."""
        
        uncertainty_factors = []
        
        # Baja confianza en evaluaciones
        evaluations = analysis_results.get('physics_results', {}).get('evaluations', {})
        low_confidence_rules = [
            rule_name for rule_name, eval_data in evaluations.items()
            if eval_data.get('confidence', 0) < 0.5
        ]
        
        if low_confidence_rules:
            uncertainty_factors.append(f"Baja confianza en reglas: {', '.join(low_confidence_rules)}")
        
        # Datos sintéticos
        if analysis_results.get('data_source') == 'synthetic':
            uncertainty_factors.append("Análisis basado en datos sintéticos - requiere validación con datos reales")
        
        # Resolución limitada
        resolution = analysis_results.get('region_info', {}).get('resolution_m', 1000)
        if resolution > 1000:
            uncertainty_factors.append(f"Resolución espacial limitada ({resolution}m) puede afectar detección de estructuras pequeñas")
        
        return uncertainty_factors
    
    def _generate_validation_recommendations(self, layer_contributions: List[LayerContribution],
                                           natural_explanations: List[NaturalExplanation],
                                           uncertainty_factors: List[str]) -> List[str]:
        """Generar recomendaciones específicas de validación."""
        
        recommendations = []
        
        # Recomendaciones basadas en contribuciones principales
        primary_layers = [c.layer_name for c in layer_contributions if c.contribution_type == ContributionType.PRIMARY]
        
        if 'ndvi_vegetation' in primary_layers:
            recommendations.append("Análisis multitemporal de vegetación para confirmar persistencia")
        
        if 'thermal_lst' in primary_layers:
            recommendations.append("Mediciones térmicas nocturnas para validar inercia térmica diferencial")
        
        if 'sar_backscatter' in primary_layers:
            recommendations.append("Análisis SAR multi-polarización para confirmar anomalías de textura")
        
        # Recomendaciones generales
        recommendations.extend([
            "Prospección geofísica (GPR, magnetometría) para validación subsuperficial",
            "Análisis de contexto arqueológico regional",
            "Correlación con bases de datos arqueológicas existentes"
        ])
        
        # Recomendaciones específicas por incertidumbre
        if any('resolución' in factor for factor in uncertainty_factors):
            recommendations.append("Adquisición de datos de mayor resolución espacial")
        
        return recommendations
    
    def _determine_confidence_level(self, layer_contributions: List[LayerContribution],
                                  natural_explanations: List[NaturalExplanation]) -> str:
        """Determinar nivel de confianza general."""
        
        # Calcular confianza promedio de contribuciones principales
        primary_contributions = [c for c in layer_contributions if c.contribution_type == ContributionType.PRIMARY]
        
        if not primary_contributions:
            return "BAJA"
        
        mean_confidence = float(np.mean([c.confidence for c in primary_contributions]))
        
        # Ajustar por plausibilidad de explicaciones naturales
        max_natural_plausibility = max([e.plausibility_score for e in natural_explanations])
        
        adjusted_confidence = mean_confidence * (1 - max_natural_plausibility * 0.5)
        
        if adjusted_confidence > 0.7:
            return "ALTA"
        elif adjusted_confidence > 0.5:
            return "MEDIA"
        else:
            return "BAJA"
    
    def generate_explanation_report(self, explanations: List[AnomalyExplanation]) -> Dict[str, Any]:
        """Generar reporte completo de explicabilidad."""
        
        return {
            'total_anomalies_explained': len(explanations),
            'confidence_distribution': self._analyze_confidence_distribution(explanations),
            'most_contributing_layers': self._identify_most_contributing_layers(explanations),
            'natural_explanations_summary': self._summarize_natural_explanations(explanations),
            'validation_priorities': self._prioritize_validation_recommendations(explanations),
            'methodological_transparency': {
                'all_decisions_explained': True,
                'natural_alternatives_considered': True,
                'uncertainty_factors_identified': True,
                'validation_path_provided': True
            }
        }
    
    def _analyze_confidence_distribution(self, explanations: List[AnomalyExplanation]) -> Dict[str, int]:
        """Analizar distribución de niveles de confianza."""
        
        distribution = {'ALTA': 0, 'MEDIA': 0, 'BAJA': 0}
        
        for explanation in explanations:
            distribution[explanation.confidence_level] += 1
        
        return distribution
    
    def _identify_most_contributing_layers(self, explanations: List[AnomalyExplanation]) -> List[str]:
        """Identificar capas que más contribuyen al análisis."""
        
        layer_weights = {}
        
        for explanation in explanations:
            for contribution in explanation.layer_contributions:
                if contribution.layer_name not in layer_weights:
                    layer_weights[contribution.layer_name] = []
                layer_weights[contribution.layer_name].append(contribution.weight)
        
        # Calcular peso promedio por capa
        layer_avg_weights = {
            layer: float(np.mean(weights)) for layer, weights in layer_weights.items()
        }
        
        # Ordenar por peso promedio
        sorted_layers = sorted(layer_avg_weights.items(), key=lambda x: x[1], reverse=True)
        
        return [layer for layer, _ in sorted_layers[:3]]
    
    def _summarize_natural_explanations(self, explanations: List[AnomalyExplanation]) -> Dict[str, Any]:
        """Resumir evaluación de explicaciones naturales."""
        
        all_natural_explanations = []
        for explanation in explanations:
            all_natural_explanations.extend(explanation.natural_explanations_considered)
        
        # Calcular plausibilidad promedio por proceso
        process_plausibilities = {}
        for nat_exp in all_natural_explanations:
            if nat_exp.process_name not in process_plausibilities:
                process_plausibilities[nat_exp.process_name] = []
            process_plausibilities[nat_exp.process_name].append(nat_exp.plausibility_score)
        
        avg_plausibilities = {
            process: float(np.mean(scores)) for process, scores in process_plausibilities.items()
        }
        
        return {
            'most_plausible_natural_process': max(avg_plausibilities.items(), key=lambda x: x[1]),
            'least_plausible_natural_process': min(avg_plausibilities.items(), key=lambda x: x[1]),
            'overall_natural_explanation_strength': float(np.mean(list(avg_plausibilities.values())))
        }
    
    def _prioritize_validation_recommendations(self, explanations: List[AnomalyExplanation]) -> List[str]:
        """Priorizar recomendaciones de validación."""
        
        all_recommendations = []
        for explanation in explanations:
            all_recommendations.extend(explanation.validation_recommendations)
        
        # Contar frecuencia de recomendaciones
        recommendation_counts = {}
        for rec in all_recommendations:
            recommendation_counts[rec] = recommendation_counts.get(rec, 0) + 1
        
        # Ordenar por frecuencia
        sorted_recommendations = sorted(recommendation_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [rec for rec, _ in sorted_recommendations[:5]]