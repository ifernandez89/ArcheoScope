#!/usr/bin/env python3
"""
ArcheoScope Modern Activity Detector (Anti-Signals)
====================================================

PROBLEMA CRÍTICO:
El sistema puede detectar anomalías que NO son arqueológicas sino actividad moderna:
- Minería moderna
- Caminos recientes
- Drenajes agrícolas
- Obras hidráulicas contemporáneas
- Infraestructura industrial

SOLUCIÓN:
Sistema de anti-señales que DESCARTA falsos positivos explícitamente.

FILOSOFÍA:
Cada anti-señal tiene un antiScore ∈ [0,1] que RESTA peso al score arqueológico.
Si antiScore es alto, la anomalía es probablemente moderna, no arqueológica.
"""

import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class ModernActivityType(Enum):
    """Tipos de actividad moderna detectables"""
    MINING = "mining"  # Minería moderna
    ROADS = "roads"  # Caminos recientes
    AGRICULTURE = "agriculture"  # Drenajes agrícolas
    HYDRAULIC = "hydraulic"  # Obras hidráulicas modernas
    INDUSTRIAL = "industrial"  # Infraestructura industrial
    URBAN_EXPANSION = "urban_expansion"  # Expansión urbana
    DEFORESTATION = "deforestation"  # Deforestación reciente
    QUARRYING = "quarrying"  # Canteras
    MILITARY = "military"  # Instalaciones militares
    UNKNOWN = "unknown"

@dataclass
class AntiSignal:
    """Una anti-señal detectada"""
    activity_type: ModernActivityType
    confidence: float  # 0.0 - 1.0
    anti_score: float  # 0.0 - 1.0 (cuánto resta al score arqueológico)
    evidence: List[str]
    temporal_signature: Optional[str]  # "recent", "modern", "contemporary"
    spatial_extent_km2: Optional[float]
    detection_method: str
    notes: str

@dataclass
class ModernActivityAnalysis:
    """Resultado del análisis de actividad moderna"""
    modern_activity_detected: bool
    total_anti_score: float  # Suma de todos los anti-scores
    detected_activities: List[AntiSignal]
    archaeological_score_adjustment: float  # Factor multiplicador (0.0 - 1.0)
    confidence: float
    explanation: str
    recommended_actions: List[str]

class ModernActivityDetector:
    """
    Detector de actividad moderna (anti-señales).
    
    INTEGRACIÓN:
    Este módulo se integra con CoreAnomalyDetector para:
    1. Detectar actividad moderna
    2. Calcular anti-scores
    3. Ajustar score arqueológico final
    
    FÓRMULA:
    finalArchaeologicalScore = baseScore * (1.0 - totalAntiScore)
    """
    
    def __init__(self):
        """Inicializar detector de actividad moderna"""
        self.detection_thresholds = self._initialize_thresholds()
        logger.info("ModernActivityDetector inicializado")
    
    def _initialize_thresholds(self) -> Dict[str, Any]:
        """Inicializar umbrales de detección para cada tipo de actividad"""
        return {
            'mining': {
                'spectral_signature_threshold': 0.7,
                'geometric_regularity_threshold': 0.8,
                'temporal_change_threshold': 0.6,
                'typical_scale_km2': (0.1, 50.0)
            },
            'roads': {
                'linearity_threshold': 0.85,
                'width_consistency_threshold': 0.75,
                'surface_material_modern': 0.7,
                'typical_width_m': (3.0, 30.0)
            },
            'agriculture': {
                'drainage_pattern_regularity': 0.8,
                'field_geometry_modern': 0.75,
                'irrigation_signature': 0.7,
                'typical_field_size_ha': (1.0, 100.0)
            },
            'hydraulic': {
                'concrete_signature': 0.8,
                'geometric_precision': 0.85,
                'modern_materials': 0.75,
                'typical_scale_m': (10.0, 1000.0)
            },
            'industrial': {
                'metal_signature': 0.8,
                'thermal_signature': 0.7,
                'geometric_complexity': 0.75,
                'typical_scale_m': (50.0, 5000.0)
            },
            'urban_expansion': {
                'building_density_increase': 0.7,
                'road_network_expansion': 0.75,
                'temporal_growth_rate': 0.6,
                'typical_scale_km2': (0.5, 100.0)
            },
            'deforestation': {
                'ndvi_decrease_rate': 0.7,
                'clear_cut_pattern': 0.8,
                'temporal_signature_recent': 0.75,
                'typical_scale_km2': (0.1, 50.0)
            },
            'quarrying': {
                'excavation_pattern': 0.8,
                'material_extraction_signature': 0.75,
                'geometric_terracing': 0.7,
                'typical_scale_m': (50.0, 2000.0)
            }
        }
    
    def detect_modern_activity(self,
                              measurements: List[Dict[str, Any]],
                              environment_type: str,
                              coordinates: Tuple[float, float],
                              temporal_data: Optional[Dict[str, Any]] = None,
                              context: Optional[Dict[str, Any]] = None) -> ModernActivityAnalysis:
        """
        Detectar actividad moderna en la región analizada.
        
        Args:
            measurements: Mediciones instrumentales del CoreAnomalyDetector
            environment_type: Tipo de ambiente
            coordinates: (lat, lon)
            temporal_data: Datos temporales si disponibles
            context: Contexto adicional
            
        Returns:
            ModernActivityAnalysis con anti-señales detectadas
        """
        
        context = context or {}
        temporal_data = temporal_data or {}
        
        logger.info(f"🔍 Detectando actividad moderna en {coordinates}")
        
        detected_activities = []
        
        # 1. DETECTAR MINERÍA MODERNA
        mining_signal = self._detect_mining(measurements, environment_type, context)
        if mining_signal:
            detected_activities.append(mining_signal)
        
        # 2. DETECTAR CAMINOS MODERNOS
        roads_signal = self._detect_modern_roads(measurements, temporal_data, context)
        if roads_signal:
            detected_activities.append(roads_signal)
        
        # 3. DETECTAR AGRICULTURA MODERNA
        agriculture_signal = self._detect_modern_agriculture(measurements, environment_type, context)
        if agriculture_signal:
            detected_activities.append(agriculture_signal)
        
        # 4. DETECTAR OBRAS HIDRÁULICAS MODERNAS
        hydraulic_signal = self._detect_modern_hydraulic(measurements, context)
        if hydraulic_signal:
            detected_activities.append(hydraulic_signal)
        
        # 5. DETECTAR INFRAESTRUCTURA INDUSTRIAL
        industrial_signal = self._detect_industrial(measurements, context)
        if industrial_signal:
            detected_activities.append(industrial_signal)
        
        # 6. DETECTAR EXPANSIÓN URBANA
        urban_signal = self._detect_urban_expansion(measurements, temporal_data, context)
        if urban_signal:
            detected_activities.append(urban_signal)
        
        # 7. DETECTAR DEFORESTACIÓN RECIENTE
        deforestation_signal = self._detect_deforestation(measurements, temporal_data, environment_type, context)
        if deforestation_signal:
            detected_activities.append(deforestation_signal)
        
        # 8. DETECTAR CANTERAS
        quarrying_signal = self._detect_quarrying(measurements, environment_type, context)
        if quarrying_signal:
            detected_activities.append(quarrying_signal)
        
        # CALCULAR ANTI-SCORE TOTAL
        total_anti_score = self._calculate_total_anti_score(detected_activities)
        
        # CALCULAR AJUSTE AL SCORE ARQUEOLÓGICO
        archaeological_adjustment = self._calculate_archaeological_adjustment(total_anti_score)
        
        # DETERMINAR SI HAY ACTIVIDAD MODERNA SIGNIFICATIVA
        modern_activity_detected = total_anti_score > 0.3
        
        # CALCULAR CONFIANZA
        confidence = self._calculate_confidence(detected_activities)
        
        # GENERAR EXPLICACIÓN
        explanation = self._generate_explanation(
            detected_activities, total_anti_score, archaeological_adjustment
        )
        
        # GENERAR RECOMENDACIONES
        recommended_actions = self._generate_recommendations(
            detected_activities, total_anti_score
        )
        
        logger.info(f"   Actividades detectadas: {len(detected_activities)}")
        logger.info(f"   Anti-score total: {total_anti_score:.3f}")
        logger.info(f"   Ajuste arqueológico: {archaeological_adjustment:.3f}x")
        
        return ModernActivityAnalysis(
            modern_activity_detected=modern_activity_detected,
            total_anti_score=total_anti_score,
            detected_activities=detected_activities,
            archaeological_score_adjustment=archaeological_adjustment,
            confidence=confidence,
            explanation=explanation,
            recommended_actions=recommended_actions
        )
    
    def _detect_mining(self,
                      measurements: List[Dict[str, Any]],
                      environment_type: str,
                      context: Dict[str, Any]) -> Optional[AntiSignal]:
        """Detectar minería moderna"""
        
        evidence = []
        confidence = 0.0
        
        # Buscar firmas espectrales de minería
        for m in measurements:
            instrument = m.get('instrument', '').lower()
            value = m.get('value', 0.0)
            
            # Firmas típicas de minería:
            # - Alteración espectral extrema
            # - Geometría muy regular (terrazas, pozos)
            # - Ausencia de vegetación
            # - Materiales expuestos
            
            if 'spectral' in instrument or 'ndvi' in instrument:
                if value > 0.8:  # Alteración extrema
                    evidence.append(f"Alteración espectral extrema: {value:.2f}")
                    confidence += 0.3
            
            if 'geometric' in instrument or 'regularity' in instrument:
                if value > 0.85:  # Geometría muy regular
                    evidence.append(f"Geometría extremadamente regular: {value:.2f}")
                    confidence += 0.3
            
            if 'thermal' in instrument:
                if value > 0.75:  # Actividad térmica (maquinaria)
                    evidence.append(f"Firma térmica de maquinaria: {value:.2f}")
                    confidence += 0.2
        
        # Contexto adicional
        if context.get('known_mining_region', False):
            evidence.append("Región conocida de minería activa")
            confidence += 0.2
        
        if confidence > 0.5 and evidence:
            anti_score = min(confidence, 0.9)  # Máximo 0.9
            
            return AntiSignal(
                activity_type=ModernActivityType.MINING,
                confidence=confidence,
                anti_score=anti_score,
                evidence=evidence,
                temporal_signature="modern",
                spatial_extent_km2=context.get('mining_extent_km2'),
                detection_method="spectral_geometric_thermal",
                notes="Minería moderna detectada - alta probabilidad de falso positivo arqueológico"
            )
        
        return None
    
    def _detect_modern_roads(self,
                            measurements: List[Dict[str, Any]],
                            temporal_data: Dict[str, Any],
                            context: Dict[str, Any]) -> Optional[AntiSignal]:
        """Detectar caminos modernos"""
        
        evidence = []
        confidence = 0.0
        
        for m in measurements:
            instrument = m.get('instrument', '').lower()
            value = m.get('value', 0.0)
            
            # Firmas de caminos modernos:
            # - Linealidad extrema
            # - Ancho consistente
            # - Material de superficie moderno (asfalto, concreto)
            # - Conexión con red vial moderna
            
            if 'linear' in instrument or 'geometry' in instrument:
                if value > 0.9:  # Linealidad extrema
                    evidence.append(f"Linealidad extrema: {value:.2f}")
                    confidence += 0.3
            
            if 'sar' in instrument or 'backscatter' in instrument:
                if value > 0.8:  # Firma de superficie pavimentada
                    evidence.append(f"Firma de pavimento moderno: {value:.2f}")
                    confidence += 0.3
        
        # Datos temporales
        if temporal_data.get('construction_date'):
            construction_year = temporal_data.get('construction_date')
            if construction_year > 1950:
                evidence.append(f"Construcción moderna: {construction_year}")
                confidence += 0.4
        
        if confidence > 0.5 and evidence:
            anti_score = min(confidence, 0.85)
            
            return AntiSignal(
                activity_type=ModernActivityType.ROADS,
                confidence=confidence,
                anti_score=anti_score,
                evidence=evidence,
                temporal_signature="modern",
                spatial_extent_km2=None,
                detection_method="geometric_spectral_temporal",
                notes="Camino moderno detectado - no es estructura arqueológica"
            )
        
        return None
    
    def _detect_modern_agriculture(self,
                                  measurements: List[Dict[str, Any]],
                                  environment_type: str,
                                  context: Dict[str, Any]) -> Optional[AntiSignal]:
        """Detectar agricultura moderna (drenajes, irrigación)"""
        
        evidence = []
        confidence = 0.0
        
        for m in measurements:
            instrument = m.get('instrument', '').lower()
            value = m.get('value', 0.0)
            
            # Firmas de agricultura moderna:
            # - Patrones de drenaje muy regulares
            # - Geometría de campos moderna (rectangular perfecta)
            # - Sistemas de irrigación mecánicos
            
            if 'drainage' in instrument or 'hydraulic' in instrument:
                if value > 0.8:  # Patrón muy regular
                    evidence.append(f"Patrón de drenaje moderno: {value:.2f}")
                    confidence += 0.3
            
            if 'field_geometry' in instrument:
                if value > 0.85:  # Geometría perfectamente rectangular
                    evidence.append(f"Geometría de campo moderna: {value:.2f}")
                    confidence += 0.3
        
        # Contexto ambiental
        if environment_type == 'agricultural':
            evidence.append("Zona agrícola activa")
            confidence += 0.2
        
        if confidence > 0.5 and evidence:
            anti_score = min(confidence, 0.75)
            
            return AntiSignal(
                activity_type=ModernActivityType.AGRICULTURE,
                confidence=confidence,
                anti_score=anti_score,
                evidence=evidence,
                temporal_signature="modern",
                spatial_extent_km2=context.get('field_size_km2'),
                detection_method="geometric_hydraulic",
                notes="Agricultura moderna detectada - drenajes no son canales arqueológicos"
            )
        
        return None
    
    def _detect_modern_hydraulic(self,
                                measurements: List[Dict[str, Any]],
                                context: Dict[str, Any]) -> Optional[AntiSignal]:
        """Detectar obras hidráulicas modernas"""
        
        evidence = []
        confidence = 0.0
        
        for m in measurements:
            instrument = m.get('instrument', '').lower()
            value = m.get('value', 0.0)
            
            # Firmas de obras hidráulicas modernas:
            # - Firma de concreto
            # - Precisión geométrica extrema
            # - Materiales modernos
            
            if 'concrete' in instrument or 'material' in instrument:
                if value > 0.8:
                    evidence.append(f"Firma de concreto moderno: {value:.2f}")
                    confidence += 0.4
            
            if 'geometric_precision' in instrument:
                if value > 0.9:
                    evidence.append(f"Precisión geométrica moderna: {value:.2f}")
                    confidence += 0.3
        
        if confidence > 0.5 and evidence:
            anti_score = min(confidence, 0.85)
            
            return AntiSignal(
                activity_type=ModernActivityType.HYDRAULIC,
                confidence=confidence,
                anti_score=anti_score,
                evidence=evidence,
                temporal_signature="contemporary",
                spatial_extent_km2=None,
                detection_method="material_geometric",
                notes="Obra hidráulica moderna - no es acueducto arqueológico"
            )
        
        return None
    
    def _detect_industrial(self,
                          measurements: List[Dict[str, Any]],
                          context: Dict[str, Any]) -> Optional[AntiSignal]:
        """Detectar infraestructura industrial"""
        
        evidence = []
        confidence = 0.0
        
        for m in measurements:
            instrument = m.get('instrument', '').lower()
            value = m.get('value', 0.0)
            
            # Firmas industriales:
            # - Firma de metal
            # - Actividad térmica
            # - Geometría compleja moderna
            
            if 'metal' in instrument or 'magnetometer' in instrument:
                if value > 0.8:
                    evidence.append(f"Firma metálica industrial: {value:.2f}")
                    confidence += 0.4
            
            if 'thermal' in instrument:
                if value > 0.75:
                    evidence.append(f"Actividad térmica industrial: {value:.2f}")
                    confidence += 0.3
        
        if confidence > 0.5 and evidence:
            anti_score = min(confidence, 0.9)
            
            return AntiSignal(
                activity_type=ModernActivityType.INDUSTRIAL,
                confidence=confidence,
                anti_score=anti_score,
                evidence=evidence,
                temporal_signature="contemporary",
                spatial_extent_km2=None,
                detection_method="metal_thermal",
                notes="Infraestructura industrial - no es sitio arqueológico"
            )
        
        return None
    
    def _detect_urban_expansion(self,
                               measurements: List[Dict[str, Any]],
                               temporal_data: Dict[str, Any],
                               context: Dict[str, Any]) -> Optional[AntiSignal]:
        """Detectar expansión urbana reciente"""
        
        evidence = []
        confidence = 0.0
        
        # Analizar cambio temporal
        if temporal_data.get('building_density_change'):
            change = temporal_data['building_density_change']
            if change > 0.5:  # Aumento significativo
                evidence.append(f"Aumento de densidad de edificios: {change:.2f}")
                confidence += 0.4
        
        if temporal_data.get('road_network_expansion'):
            expansion = temporal_data['road_network_expansion']
            if expansion > 0.4:
                evidence.append(f"Expansión de red vial: {expansion:.2f}")
                confidence += 0.3
        
        if confidence > 0.5 and evidence:
            anti_score = min(confidence, 0.8)
            
            return AntiSignal(
                activity_type=ModernActivityType.URBAN_EXPANSION,
                confidence=confidence,
                anti_score=anti_score,
                evidence=evidence,
                temporal_signature="recent",
                spatial_extent_km2=context.get('expansion_area_km2'),
                detection_method="temporal_change",
                notes="Expansión urbana reciente - no es asentamiento arqueológico"
            )
        
        return None
    
    def _detect_deforestation(self,
                             measurements: List[Dict[str, Any]],
                             temporal_data: Dict[str, Any]],
                             environment_type: str,
                             context: Dict[str, Any]) -> Optional[AntiSignal]:
        """Detectar deforestación reciente"""
        
        evidence = []
        confidence = 0.0
        
        # Solo relevante en ambientes forestales
        if environment_type not in ['forest', 'grassland']:
            return None
        
        for m in measurements:
            instrument = m.get('instrument', '').lower()
            value = m.get('value', 0.0)
            
            if 'ndvi' in instrument:
                # NDVI bajo puede indicar deforestación
                if value < 0.3:
                    evidence.append(f"NDVI bajo (deforestación): {value:.2f}")
                    confidence += 0.3
        
        # Datos temporales
        if temporal_data.get('ndvi_decrease_rate'):
            rate = temporal_data['ndvi_decrease_rate']
            if rate > 0.5:  # Disminución rápida
                evidence.append(f"Disminución rápida de NDVI: {rate:.2f}")
                confidence += 0.4
        
        if confidence > 0.5 and evidence:
            anti_score = min(confidence, 0.7)
            
            return AntiSignal(
                activity_type=ModernActivityType.DEFORESTATION,
                confidence=confidence,
                anti_score=anti_score,
                evidence=evidence,
                temporal_signature="recent",
                spatial_extent_km2=context.get('deforestation_area_km2'),
                detection_method="ndvi_temporal",
                notes="Deforestación reciente - puede generar falsos positivos"
            )
        
        return None
    
    def _detect_quarrying(self,
                         measurements: List[Dict[str, Any]],
                         environment_type: str,
                         context: Dict[str, Any]) -> Optional[AntiSignal]:
        """Detectar canteras modernas"""
        
        evidence = []
        confidence = 0.0
        
        for m in measurements:
            instrument = m.get('instrument', '').lower()
            value = m.get('value', 0.0)
            
            # Firmas de canteras:
            # - Patrón de excavación
            # - Terrazas geométricas
            # - Extracción de material
            
            if 'excavation' in instrument or 'elevation' in instrument:
                if value > 0.8:
                    evidence.append(f"Patrón de excavación: {value:.2f}")
                    confidence += 0.3
            
            if 'terracing' in instrument:
                if value > 0.85:
                    evidence.append(f"Terrazas geométricas modernas: {value:.2f}")
                    confidence += 0.3
        
        if confidence > 0.5 and evidence:
            anti_score = min(confidence, 0.85)
            
            return AntiSignal(
                activity_type=ModernActivityType.QUARRYING,
                confidence=confidence,
                anti_score=anti_score,
                evidence=evidence,
                temporal_signature="modern",
                spatial_extent_km2=None,
                detection_method="geometric_excavation",
                notes="Cantera moderna - no es sitio arqueológico"
            )
        
        return None
    
    def _calculate_total_anti_score(self, activities: List[AntiSignal]) -> float:
        """
        Calcular anti-score total.
        
        IMPORTANTE: No es suma simple, sino combinación ponderada
        para evitar sobre-penalización.
        """
        
        if not activities:
            return 0.0
        
        # Ordenar por anti-score descendente
        sorted_activities = sorted(activities, key=lambda x: x.anti_score, reverse=True)
        
        # Tomar el más alto + fracción de los demás
        total = sorted_activities[0].anti_score
        
        for activity in sorted_activities[1:]:
            # Cada actividad adicional aporta menos (ley de rendimientos decrecientes)
            total += activity.anti_score * 0.3
        
        # Limitar a 0.95 (nunca descartar completamente)
        return min(total, 0.95)
    
    def _calculate_archaeological_adjustment(self, total_anti_score: float) -> float:
        """
        Calcular factor de ajuste para score arqueológico.
        
        FÓRMULA:
        adjustment = 1.0 - total_anti_score
        
        Ejemplos:
        - anti_score = 0.0 → adjustment = 1.0 (sin cambio)
        - anti_score = 0.5 → adjustment = 0.5 (reduce a la mitad)
        - anti_score = 0.9 → adjustment = 0.1 (reduce drásticamente)
        """
        
        return max(0.05, 1.0 - total_anti_score)  # Mínimo 0.05 (nunca cero absoluto)
    
    def _calculate_confidence(self, activities: List[AntiSignal]) -> float:
        """Calcular confianza general de la detección"""
        
        if not activities:
            return 1.0  # Alta confianza de que NO hay actividad moderna
        
        # Promedio ponderado de confianzas
        total_confidence = sum(a.confidence * a.anti_score for a in activities)
        total_weight = sum(a.anti_score for a in activities)
        
        if total_weight > 0:
            return total_confidence / total_weight
        else:
            return 0.5
    
    def _generate_explanation(self,
                            activities: List[AntiSignal],
                            total_anti_score: float,
                            archaeological_adjustment: float) -> str:
        """Generar explicación de anti-señales detectadas"""
        
        if not activities:
            return "No se detectó actividad moderna significativa. Score arqueológico sin ajuste."
        
        parts = []
        
        parts.append(f"ACTIVIDAD MODERNA DETECTADA ({len(activities)} señales):")
        
        for activity in activities:
            parts.append(f"- {activity.activity_type.value}: anti-score {activity.anti_score:.2f} (confianza {activity.confidence:.2f})")
            parts.append(f"  Evidencia: {', '.join(activity.evidence[:2])}")
        
        parts.append(f"\nANTI-SCORE TOTAL: {total_anti_score:.3f}")
        parts.append(f"AJUSTE ARQUEOLÓGICO: {archaeological_adjustment:.3f}x")
        
        if archaeological_adjustment < 0.3:
            parts.append("⚠️ ALTA probabilidad de falso positivo - actividad moderna dominante")
        elif archaeological_adjustment < 0.6:
            parts.append("⚠️ MODERADA probabilidad de falso positivo - revisar evidencia")
        else:
            parts.append("✓ Actividad moderna presente pero no dominante")
        
        return "\n".join(parts)
    
    def _generate_recommendations(self,
                                 activities: List[AntiSignal],
                                 total_anti_score: float) -> List[str]:
        """Generar recomendaciones basadas en anti-señales"""
        
        recommendations = []
        
        if total_anti_score > 0.7:
            recommendations.append("DESCARTAR como sitio arqueológico - actividad moderna dominante")
            recommendations.append("Verificar con imágenes de alta resolución recientes")
        elif total_anti_score > 0.4:
            recommendations.append("REVISAR cuidadosamente - posible falso positivo")
            recommendations.append("Comparar con imágenes históricas para confirmar antigüedad")
        else:
            recommendations.append("Actividad moderna presente pero no descarta arqueología")
            recommendations.append("Proceder con análisis arqueológico estándar")
        
        # Recomendaciones específicas por tipo
        activity_types = {a.activity_type for a in activities}
        
        if ModernActivityType.MINING in activity_types:
            recommendations.append("Verificar registros de concesiones mineras")
        
        if ModernActivityType.ROADS in activity_types:
            recommendations.append("Consultar mapas viales históricos")
        
        if ModernActivityType.AGRICULTURE in activity_types:
            recommendations.append("Verificar con registros catastrales agrícolas")
        
        if ModernActivityType.INDUSTRIAL in activity_types:
            recommendations.append("Consultar registros industriales y permisos de construcción")
        
        return recommendations
