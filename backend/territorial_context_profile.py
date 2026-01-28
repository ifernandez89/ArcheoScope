#!/usr/bin/env python3
"""
Territorial Context Profile (TCP) - CAPA 0: CONTEXTO ANTES DE MEDIR
==================================================================

REVOLUCIÓN CONCEPTUAL: De "medición genérica" a "adquisición dirigida"

FLUJO CIENTÍFICO REAL (NASA, CERN):
1. CONTEXTO → 2. HIPÓTESIS → 3. MEDICIÓN

TCP construye el perfil territorial base (NO sensorial) que define:
- Qué es posible y qué no en ese territorio
- Qué hipótesis son plausibles
- Qué instrumentos son relevantes

COMPONENTES TCP:
- Geología / litología
- Hidrografía histórica  
- Topografía estructural
- Bioma histórico
- Rutas humanas conocidas
- Sitios arqueológicos documentados (externos + internos)
"""

import asyncio
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from .geological_context import GeologicalContextSystem, GeologicalContext
from .historical_hydrography import HistoricalHydrographySystem, HydrographicFeature
from .external_archaeological_validation import ExternalArchaeologicalValidationSystem, ExternalArchaeologicalSite
from .human_traces_analysis import HumanTracesAnalysisSystem, HumanTrace

logger = logging.getLogger(__name__)

class AnalysisObjective(Enum):
    """Objetivos de análisis."""
    EXPLORATORY = "exploratory"      # Exploración general
    VALIDATION = "validation"        # Validación de hipótesis específica
    ACADEMIC = "academic"           # Investigación académica rigurosa
    MONITORING = "monitoring"       # Monitoreo de sitio conocido

class PreservationPotential(Enum):
    """Potencial de preservación arqueológica."""
    EXCELLENT = "excellent"
    GOOD = "good"
    MODERATE = "moderate"
    POOR = "poor"
    UNKNOWN = "unknown"

class BiomeType(Enum):
    """Tipos de bioma histórico."""
    TROPICAL_FOREST = "tropical_forest"
    TEMPERATE_FOREST = "temperate_forest"
    GRASSLAND = "grassland"
    DESERT = "desert"
    MEDITERRANEAN = "mediterranean"
    TUNDRA = "tundra"
    WETLAND = "wetland"
    UNKNOWN = "unknown"

@dataclass
class TerritorialHypothesis:
    """Hipótesis territorial plausible."""
    
    hypothesis_id: str
    hypothesis_type: str  # settlement, ritual, hydraulic, transit, etc.
    plausibility_score: float  # 0-1
    
    # Evidencia de soporte
    geological_support: float
    hydrographic_support: float
    archaeological_support: float
    human_traces_support: float
    
    # Instrumentos recomendados
    recommended_instruments: List[str]
    
    # Explicación
    hypothesis_explanation: str
    contradictions: List[str]

@dataclass
class InstrumentalStrategy:
    """Estrategia instrumental dirigida por hipótesis."""
    
    # Instrumentos por capa
    surface_instruments: List[str]
    subsurface_instruments: List[str]
    climate_instruments: List[str]
    human_context_instruments: List[str]
    
    # Priorización
    priority_instruments: List[str]
    secondary_instruments: List[str]
    
    # Resolución recomendada
    recommended_resolution_m: float
    
    # Explicación de la estrategia
    strategy_explanation: str

@dataclass
class TerritorialContextProfile:
    """Perfil de Contexto Territorial - CAPA 0 del sistema."""
    
    # Identificación
    tcp_id: str
    territory_bounds: Tuple[float, float, float, float]  # lat_min, lat_max, lon_min, lon_max
    analysis_objective: AnalysisObjective
    generation_timestamp: datetime = field(default_factory=datetime.now)
    
    # Contexto geológico
    geological_context: Optional[GeologicalContext] = None
    
    # Contexto hidrográfico
    hydrographic_features: List[HydrographicFeature] = field(default_factory=list)
    
    # Contexto arqueológico externo
    external_archaeological_sites: List[ExternalArchaeologicalSite] = field(default_factory=list)
    
    # Trazas humanas conocidas
    known_human_traces: List[HumanTrace] = field(default_factory=list)
    
    # Contexto ambiental
    historical_biome: BiomeType = BiomeType.UNKNOWN
    topographic_complexity: float = 0.5  # 0-1
    
    # Evaluación de preservación
    preservation_potential: PreservationPotential = PreservationPotential.UNKNOWN
    preservation_factors: List[str] = field(default_factory=list)
    
    # Hipótesis territoriales
    territorial_hypotheses: List[TerritorialHypothesis] = field(default_factory=list)
    
    # Estrategia instrumental
    instrumental_strategy: Optional[InstrumentalStrategy] = None
    
    # Limitaciones conocidas
    known_limitations: List[str] = field(default_factory=list)
    system_boundaries: List[str] = field(default_factory=list)

class TerritorialContextProfileSystem:
    """Sistema de generación de Perfiles de Contexto Territorial."""
    
    def __init__(self):
        """Inicializar sistema TCP."""
        
        # Sistemas de contexto
        self.geological_system = GeologicalContextSystem()
        self.hydrography_system = HistoricalHydrographySystem()
        self.external_validation_system = ExternalArchaeologicalValidationSystem()
        self.human_traces_system = HumanTracesAnalysisSystem()
        
        # Mapeo de biomas por región
        self.regional_biomes = {
            'tropical': BiomeType.TROPICAL_FOREST,
            'temperate': BiomeType.TEMPERATE_FOREST,
            'arid': BiomeType.DESERT,
            'mediterranean': BiomeType.MEDITERRANEAN,
            'polar': BiomeType.TUNDRA,
            'wetland': BiomeType.WETLAND
        }
        
        # Instrumentos por tipo de hipótesis
        self.hypothesis_instruments = {
            'settlement': ['sentinel_2_ndvi', 'sentinel_1_sar', 'srtm_elevation', 'landsat_thermal'],
            'ritual': ['sentinel_2_ndvi', 'viirs_thermal', 'palsar_backscatter', 'icesat2'],
            'hydraulic': ['sentinel_1_sar', 'palsar_penetration', 'srtm_elevation', 'chirps_precipitation'],
            'transit': ['srtm_elevation', 'sentinel_2_ndvi', 'viirs_ndvi', 'era5_climate'],
            'agricultural': ['sentinel_2_ndvi', 'viirs_ndvi', 'chirps_precipitation', 'era5_climate'],
            'defensive': ['srtm_elevation', 'sentinel_1_sar', 'icesat2', 'palsar_backscatter']
        }
        
        logger.info("🧩 Territorial Context Profile System initialized - CAPA 0 ACTIVA")
    
    async def generate_tcp(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float,
                          analysis_objective: AnalysisObjective = AnalysisObjective.EXPLORATORY,
                          analysis_radius_km: float = 5.0) -> TerritorialContextProfile:
        """
        Generar Perfil de Contexto Territorial - CAPA 0.
        
        PROCESO REVOLUCIONARIO:
        1. Contexto antes de medición
        2. Hipótesis territoriales plausibles
        3. Estrategia instrumental dirigida
        
        Args:
            lat_min, lat_max, lon_min, lon_max: Límites territoriales
            analysis_objective: Objetivo del análisis
            analysis_radius_km: Radio de análisis contextual
            
        Returns:
            TerritorialContextProfile completo
        """
        
        logger.info(f"🧩 Generando TCP para territorio [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        logger.info(f"🎯 Objetivo: {analysis_objective.value}")
        
        tcp_id = f"TCP_{lat_min:.4f}_{lat_max:.4f}_{lon_min:.4f}_{lon_max:.4f}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # FASE 1: Contexto geológico
        logger.info("🗿 FASE 1: Adquisición de contexto geológico...")
        geological_context = await self.geological_system.get_geological_context(lat_min, lat_max, lon_min, lon_max)
        
        # FASE 2: Contexto hidrográfico histórico
        logger.info("💧 FASE 2: Adquisición de contexto hidrográfico...")
        hydrographic_features = await self.hydrography_system.get_hydrographic_context(lat_min, lat_max, lon_min, lon_max)
        
        # FASE 3: Contexto arqueológico externo
        logger.info("🏛️ FASE 3: Adquisición de contexto arqueológico externo...")
        external_sites = await self.external_validation_system.get_external_archaeological_context(
            lat_min, lat_max, lon_min, lon_max, analysis_radius_km
        )
        
        # FASE 4: Trazas humanas conocidas
        logger.info("👥 FASE 4: Análisis de trazas humanas conocidas...")
        human_traces = await self.human_traces_system.analyze_human_traces(lat_min, lat_max, lon_min, lon_max)
        
        # FASE 5: Contexto ambiental
        logger.info("🌿 FASE 5: Determinación de contexto ambiental...")
        historical_biome = self._determine_historical_biome(lat_min, lat_max, lon_min, lon_max)
        topographic_complexity = self._assess_topographic_complexity(lat_min, lat_max, lon_min, lon_max)
        
        # FASE 6: Evaluación de potencial de preservación
        logger.info("🛡️ FASE 6: Evaluación de potencial de preservación...")
        preservation_potential, preservation_factors = self._assess_preservation_potential(
            geological_context, hydrographic_features, historical_biome
        )
        
        # FASE 7: Generación de hipótesis territoriales
        logger.info("🧠 FASE 7: Generación de hipótesis territoriales...")
        territorial_hypotheses = self._generate_territorial_hypotheses(
            geological_context, hydrographic_features, external_sites, human_traces, analysis_objective
        )
        
        # FASE 8: Estrategia instrumental dirigida
        logger.info("🛰️ FASE 8: Definición de estrategia instrumental...")
        instrumental_strategy = self._define_instrumental_strategy(
            territorial_hypotheses, geological_context, analysis_objective
        )
        
        # FASE 9: Identificación de limitaciones
        logger.info("⚠️ FASE 9: Identificación de limitaciones del sistema...")
        known_limitations, system_boundaries = self._identify_system_limitations(
            geological_context, analysis_objective, territorial_hypotheses
        )
        
        # Crear TCP completo
        tcp = TerritorialContextProfile(
            tcp_id=tcp_id,
            territory_bounds=(lat_min, lat_max, lon_min, lon_max),
            analysis_objective=analysis_objective,
            geological_context=geological_context,
            hydrographic_features=hydrographic_features,
            external_archaeological_sites=external_sites,
            known_human_traces=human_traces,
            historical_biome=historical_biome,
            topographic_complexity=topographic_complexity,
            preservation_potential=preservation_potential,
            preservation_factors=preservation_factors,
            territorial_hypotheses=territorial_hypotheses,
            instrumental_strategy=instrumental_strategy,
            known_limitations=known_limitations,
            system_boundaries=system_boundaries
        )
        
        logger.info(f"✅ TCP generado exitosamente:")
        logger.info(f"   🗿 Contexto geológico: {geological_context.dominant_lithology.value}")
        logger.info(f"   💧 Características hidrográficas: {len(hydrographic_features)}")
        logger.info(f"   🏛️ Sitios externos: {len(external_sites)}")
        logger.info(f"   👥 Trazas humanas: {len(human_traces)}")
        logger.info(f"   🧠 Hipótesis territoriales: {len(territorial_hypotheses)}")
        logger.info(f"   🛡️ Potencial preservación: {preservation_potential.value}")
        
        return tcp
    
    def _determine_historical_biome(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> BiomeType:
        """Determinar bioma histórico del territorio."""
        
        lat_center = (lat_min + lat_max) / 2
        
        # Clasificación básica por latitud
        if abs(lat_center) < 10:
            return BiomeType.TROPICAL_FOREST
        elif abs(lat_center) < 30:
            # Depende de precipitación - simplificado
            if -20 <= lat_center <= 40 and -10 <= (lon_min + lon_max) / 2 <= 50:
                return BiomeType.DESERT  # Sahara, Arabia
            else:
                return BiomeType.GRASSLAND
        elif abs(lat_center) < 50:
            if 30 <= lat_center <= 45 and -10 <= (lon_min + lon_max) / 2 <= 45:
                return BiomeType.MEDITERRANEAN
            else:
                return BiomeType.TEMPERATE_FOREST
        else:
            return BiomeType.TUNDRA
    
    def _assess_topographic_complexity(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> float:
        """Evaluar complejidad topográfica (0-1)."""
        
        lat_center = (lat_min + lat_max) / 2
        
        # Estimación básica por región
        if abs(lat_center) > 45:  # Regiones montañosas
            return 0.8
        elif 30 <= abs(lat_center) <= 45:  # Regiones templadas
            return 0.6
        else:  # Regiones tropicales/ecuatoriales
            return 0.4
    
    def _assess_preservation_potential(self, geological_context: GeologicalContext,
                                     hydrographic_features: List[HydrographicFeature],
                                     biome: BiomeType) -> Tuple[PreservationPotential, List[str]]:
        """Evaluar potencial de preservación arqueológica."""
        
        factors = []
        scores = []
        
        # Factor geológico
        if geological_context:
            geo_score = geological_context.preservation_potential
            scores.append(geo_score)
            
            if geo_score > 0.8:
                factors.append("Excelente contexto geológico para preservación")
            elif geo_score > 0.6:
                factors.append("Buen contexto geológico")
            else:
                factors.append("Contexto geológico desafiante")
        
        # Factor hidrográfico
        if hydrographic_features:
            hydro_score = np.mean([f.settlement_potential for f in hydrographic_features])
            scores.append(hydro_score)
            
            if hydro_score > 0.7:
                factors.append("Contexto hidrográfico favorable")
            else:
                factors.append("Disponibilidad de agua limitada")
        
        # Factor de bioma
        biome_scores = {
            BiomeType.TEMPERATE_FOREST: 0.8,
            BiomeType.MEDITERRANEAN: 0.9,
            BiomeType.GRASSLAND: 0.7,
            BiomeType.DESERT: 0.6,
            BiomeType.TROPICAL_FOREST: 0.5,
            BiomeType.TUNDRA: 0.3,
            BiomeType.WETLAND: 0.4
        }
        
        biome_score = biome_scores.get(biome, 0.5)
        scores.append(biome_score)
        factors.append(f"Bioma {biome.value} con preservación {['pobre', 'moderada', 'buena', 'excelente'][int(biome_score * 3)]}")
        
        # Evaluación final
        avg_score = np.mean(scores) if scores else 0.5
        
        if avg_score > 0.8:
            potential = PreservationPotential.EXCELLENT
        elif avg_score > 0.6:
            potential = PreservationPotential.GOOD
        elif avg_score > 0.4:
            potential = PreservationPotential.MODERATE
        else:
            potential = PreservationPotential.POOR
        
        return potential, factors
    
    def _generate_territorial_hypotheses(self, geological_context: GeologicalContext,
                                       hydrographic_features: List[HydrographicFeature],
                                       external_sites: List[ExternalArchaeologicalSite],
                                       human_traces: List[HumanTrace],
                                       objective: AnalysisObjective) -> List[TerritorialHypothesis]:
        """Generar hipótesis territoriales plausibles."""
        
        hypotheses = []
        
        # Hipótesis basada en contexto hidrográfico
        if hydrographic_features:
            water_features = [f for f in hydrographic_features if f.archaeological_relevance > 0.7]
            if water_features:
                hypothesis = TerritorialHypothesis(
                    hypothesis_id="H_SETTLEMENT_WATER",
                    hypothesis_type="settlement",
                    plausibility_score=0.8,
                    geological_support=geological_context.archaeological_suitability if geological_context else 0.5,
                    hydrographic_support=np.mean([f.archaeological_relevance for f in water_features]),
                    archaeological_support=0.6,  # Moderado por defecto
                    human_traces_support=0.5,
                    recommended_instruments=self.hypothesis_instruments['settlement'],
                    hypothesis_explanation="Proximidad a fuentes de agua históricas sugiere potencial de asentamiento permanente",
                    contradictions=[]
                )
                hypotheses.append(hypothesis)
        
        # Hipótesis basada en sitios externos
        if external_sites:
            nearby_sites = [s for s in external_sites if s.data_quality > 0.6]
            if nearby_sites:
                site_types = [s.site_type.value for s in nearby_sites]
                dominant_type = max(set(site_types), key=site_types.count)
                
                hypothesis = TerritorialHypothesis(
                    hypothesis_id=f"H_{dominant_type.upper()}_EXTERNAL",
                    hypothesis_type=dominant_type,
                    plausibility_score=0.7,
                    geological_support=geological_context.archaeological_suitability if geological_context else 0.5,
                    hydrographic_support=0.5,
                    archaeological_support=np.mean([s.data_quality for s in nearby_sites]),
                    human_traces_support=0.5,
                    recommended_instruments=self.hypothesis_instruments.get(dominant_type, self.hypothesis_instruments['settlement']),
                    hypothesis_explanation=f"Proximidad a sitios {dominant_type} conocidos sugiere función territorial similar",
                    contradictions=[]
                )
                hypotheses.append(hypothesis)
        
        # Hipótesis basada en trazas humanas
        if human_traces:
            route_traces = [t for t in human_traces if 'route' in t.trace_type.value or 'corridor' in t.trace_type.value]
            if route_traces:
                hypothesis = TerritorialHypothesis(
                    hypothesis_id="H_TRANSIT_ROUTES",
                    hypothesis_type="transit",
                    plausibility_score=0.6,
                    geological_support=geological_context.archaeological_suitability if geological_context else 0.5,
                    hydrographic_support=0.5,
                    archaeological_support=0.5,
                    human_traces_support=np.mean([t.archaeological_relevance for t in route_traces]),
                    recommended_instruments=self.hypothesis_instruments['transit'],
                    hypothesis_explanation="Evidencia de rutas históricas sugiere territorio de tránsito con sitios de paso",
                    contradictions=[]
                )
                hypotheses.append(hypothesis)
        
        # Hipótesis por defecto si no hay evidencia específica
        if not hypotheses:
            hypothesis = TerritorialHypothesis(
                hypothesis_id="H_EXPLORATORY_GENERAL",
                hypothesis_type="settlement",
                plausibility_score=0.5,
                geological_support=geological_context.archaeological_suitability if geological_context else 0.5,
                hydrographic_support=0.5,
                archaeological_support=0.5,
                human_traces_support=0.5,
                recommended_instruments=self.hypothesis_instruments['settlement'],
                hypothesis_explanation="Análisis exploratorio general sin hipótesis específica predominante",
                contradictions=["Contexto territorial limitado para hipótesis específicas"]
            )
            hypotheses.append(hypothesis)
        
        return hypotheses
    
    def _define_instrumental_strategy(self, hypotheses: List[TerritorialHypothesis],
                                    geological_context: GeologicalContext,
                                    objective: AnalysisObjective) -> InstrumentalStrategy:
        """Definir estrategia instrumental dirigida por hipótesis."""
        
        # Recopilar instrumentos recomendados por todas las hipótesis
        all_instruments = []
        for hypothesis in hypotheses:
            all_instruments.extend(hypothesis.recommended_instruments)
        
        # Contar frecuencia de instrumentos
        instrument_counts = {}
        for instrument in all_instruments:
            instrument_counts[instrument] = instrument_counts.get(instrument, 0) + 1
        
        # Priorizar por frecuencia y plausibilidad
        weighted_instruments = {}
        for hypothesis in hypotheses:
            weight = hypothesis.plausibility_score
            for instrument in hypothesis.recommended_instruments:
                weighted_instruments[instrument] = weighted_instruments.get(instrument, 0) + weight
        
        # Ordenar por peso
        sorted_instruments = sorted(weighted_instruments.items(), key=lambda x: x[1], reverse=True)
        
        # Dividir en prioritarios y secundarios
        priority_instruments = [inst for inst, weight in sorted_instruments[:8]]  # Top 8
        secondary_instruments = [inst for inst, weight in sorted_instruments[8:]]
        
        # Categorizar por capa
        surface_instruments = [inst for inst in priority_instruments if any(x in inst for x in ['ndvi', 'thermal', 'elevation'])]
        subsurface_instruments = [inst for inst in priority_instruments if any(x in inst for x in ['sar', 'palsar', 'icesat'])]
        climate_instruments = [inst for inst in priority_instruments if any(x in inst for x in ['era5', 'chirps', 'modis'])]
        human_context_instruments = [inst for inst in priority_instruments if any(x in inst for x in ['viirs', 'landsat'])]
        
        # Resolución recomendada basada en objetivo
        resolution_mapping = {
            AnalysisObjective.EXPLORATORY: 100.0,
            AnalysisObjective.VALIDATION: 30.0,
            AnalysisObjective.ACADEMIC: 10.0,
            AnalysisObjective.MONITORING: 30.0
        }
        recommended_resolution = resolution_mapping.get(objective, 50.0)
        
        # Explicación de la estrategia
        top_hypothesis = max(hypotheses, key=lambda h: h.plausibility_score) if hypotheses else None
        strategy_explanation = f"Estrategia dirigida por hipótesis {top_hypothesis.hypothesis_type if top_hypothesis else 'general'} con {len(priority_instruments)} instrumentos prioritarios"
        
        return InstrumentalStrategy(
            surface_instruments=surface_instruments,
            subsurface_instruments=subsurface_instruments,
            climate_instruments=climate_instruments,
            human_context_instruments=human_context_instruments,
            priority_instruments=priority_instruments,
            secondary_instruments=secondary_instruments,
            recommended_resolution_m=recommended_resolution,
            strategy_explanation=strategy_explanation
        )
    
    def _identify_system_limitations(self, geological_context: GeologicalContext,
                                   objective: AnalysisObjective,
                                   hypotheses: List[TerritorialHypothesis]) -> Tuple[List[str], List[str]]:
        """Identificar limitaciones conocidas y límites del sistema."""
        
        limitations = []
        boundaries = []
        
        # Limitaciones geológicas
        if geological_context:
            if geological_context.lithology_confidence < 0.5:
                limitations.append("Baja confianza en determinación litológica")
            
            if geological_context.archaeological_suitability < 0.4:
                limitations.append("Contexto geológico desafiante para preservación arqueológica")
        
        # Limitaciones por objetivo
        if objective == AnalysisObjective.ACADEMIC:
            boundaries.append("Análisis académico requiere validación de campo adicional")
            boundaries.append("Resultados deben ser contrastados con excavación controlada")
        
        # Limitaciones por hipótesis
        low_confidence_hypotheses = [h for h in hypotheses if h.plausibility_score < 0.6]
        if len(low_confidence_hypotheses) == len(hypotheses):
            limitations.append("Todas las hipótesis territoriales tienen baja confianza")
        
        # Límites generales del sistema
        boundaries.extend([
            "Sistema no detecta estructuras específicas, infiere patrones territoriales",
            "Profundidades inferidas, no medidas directamente",
            "Análisis limitado a evidencia indirecta y patrones espaciales",
            "Requiere validación cruzada con métodos arqueológicos tradicionales"
        ])
        
        return limitations, boundaries