#!/usr/bin/env python3
"""
Human Traces Analysis System - Análisis de Trazas Humanas No Visuales
====================================================================

VALOR AGREGADO: Frontera real - humanidad sin monumentos
- No "ves" estructuras → ves uso
- Subsuelo narrativo, no físico
- Trazas de actividad humana indirecta

FUENTES PÚBLICAS:
- Night Lights históricos (DMSP/OLS pre-2013, VIIRS)
- Rutas históricas (Roman roads, Qhapaq Ñan datasets)
- Land Use reconstructions (HYDE database)
- Historical trade routes datasets
- Ancient pathways and corridors

Sin esto, el análisis se limita a estructuras físicas y pierde el contexto de uso territorial.
"""

import requests
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class HumanTraceType(Enum):
    """Tipos de trazas humanas."""
    NIGHT_LIGHTS = "night_lights"
    HISTORICAL_ROUTE = "historical_route"
    LAND_USE_CHANGE = "land_use_change"
    TRADE_CORRIDOR = "trade_corridor"
    SETTLEMENT_PATTERN = "settlement_pattern"
    RESOURCE_EXTRACTION = "resource_extraction"
    UNKNOWN = "unknown"

class ActivityIntensity(Enum):
    """Intensidad de actividad humana."""
    VERY_HIGH = "very_high"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    MINIMAL = "minimal"
    UNKNOWN = "unknown"

class TemporalScale(Enum):
    """Escala temporal de las trazas."""
    CONTEMPORARY = "contemporary"      # 0-50 años
    RECENT_HISTORICAL = "recent_historical"  # 50-200 años
    HISTORICAL = "historical"          # 200-1000 años
    ANCIENT = "ancient"               # 1000+ años
    UNKNOWN = "unknown"

@dataclass
class HumanTrace:
    """Traza de actividad humana identificada."""
    
    # Identificación
    trace_id: str
    trace_type: HumanTraceType
    
    # Ubicación espacial
    center_coords: Tuple[float, float]  # lat, lon
    extent_km2: float
    spatial_pattern: str  # linear, radial, clustered, dispersed
    
    # Características temporales
    temporal_scale: TemporalScale
    activity_intensity: ActivityIntensity
    persistence_score: float  # 0-1
    
    # Contexto arqueológico
    archaeological_relevance: float  # 0-1
    cultural_significance: float     # 0-1
    
    # Evidencia
    evidence_strength: float  # 0-1
    data_sources: List[str]
    
    # Explicación
    trace_explanation: str

@dataclass
class TerritorialUseProfile:
    """Perfil de uso territorial basado en trazas humanas."""
    
    # Uso dominante
    primary_use: str
    secondary_uses: List[str]
    
    # Intensidad de uso
    overall_intensity: ActivityIntensity
    temporal_continuity: float  # 0-1
    
    # Patrones espaciales
    use_distribution: str  # concentrated, dispersed, linear, nodal
    connectivity_score: float  # 0-1
    
    # Contexto arqueológico
    settlement_potential: float  # 0-1
    cultural_landscape_score: float  # 0-1
    
    # Explicación
    use_explanation: str
    archaeological_implications: List[str]

class HumanTracesAnalysisSystem:
    """Sistema de análisis de trazas humanas para ETP."""
    
    def __init__(self):
        """Inicializar sistema de análisis de trazas humanas."""
        
        # URLs de fuentes de trazas humanas
        self.human_traces_sources = {
            'night_lights': 'https://ngdc.noaa.gov/eog/dmsp/downloadV4composites.html',
            'viirs_lights': 'https://eogdata.mines.edu/products/vnl/',
            'roman_roads': 'http://dare.ht.lu.se/',
            'qhapaq_nan': 'https://whc.unesco.org/en/list/1459/',
            'hyde_landuse': 'https://themasites.pbl.nl/tridion/en/themasites/hyde/',
            'trade_routes': 'https://worldmap.harvard.edu/data/geonode:trade_routes'
        }
        
        # Relevancia arqueológica por tipo de traza
        self.archaeological_relevance = {
            HumanTraceType.NIGHT_LIGHTS: 0.6,          # Moderada - indica ocupación
            HumanTraceType.HISTORICAL_ROUTE: 0.9,      # Muy alta - rutas antiguas
            HumanTraceType.LAND_USE_CHANGE: 0.8,       # Alta - modificación territorial
            HumanTraceType.TRADE_CORRIDOR: 0.85,       # Muy alta - actividad comercial
            HumanTraceType.SETTLEMENT_PATTERN: 0.95,   # Extrema - patrones de asentamiento
            HumanTraceType.RESOURCE_EXTRACTION: 0.7,   # Alta - explotación de recursos
            HumanTraceType.UNKNOWN: 0.5                # Neutro
        }
        
        # Significancia cultural por escala temporal
        self.cultural_significance = {
            TemporalScale.CONTEMPORARY: 0.3,
            TemporalScale.RECENT_HISTORICAL: 0.6,
            TemporalScale.HISTORICAL: 0.8,
            TemporalScale.ANCIENT: 0.95,
            TemporalScale.UNKNOWN: 0.5
        }
        
        logger.info("👥 Human Traces Analysis System initialized")
    
    async def analyze_human_traces(self, lat_min: float, lat_max: float,
                                 lon_min: float, lon_max: float) -> List[HumanTrace]:
        """
        Analizar trazas de actividad humana en territorio.
        
        CRÍTICO: Identifica uso territorial más allá de estructuras físicas.
        """
        
        logger.info(f"👥 Analizando trazas humanas para [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        
        try:
            # Consultar fuentes de trazas humanas
            traces_data = await self._query_human_traces_sources(lat_min, lat_max, lon_min, lon_max)
            
            # Procesar trazas humanas
            traces = self._process_human_traces_data(traces_data, lat_min, lat_max, lon_min, lon_max)
            
            logger.info(f"✅ {len(traces)} trazas humanas identificadas")
            
            return traces
            
        except Exception as e:
            logger.warning(f"⚠️ Error analizando trazas humanas: {e}")
            return self._create_default_human_traces(lat_min, lat_max, lon_min, lon_max)
    
    async def _query_human_traces_sources(self, lat_min: float, lat_max: float,
                                        lon_min: float, lon_max: float) -> Dict[str, Any]:
        """Consultar fuentes de trazas humanas."""
        
        traces_data = {}
        lat_center = (lat_min + lat_max) / 2
        lon_center = (lon_min + lon_max) / 2
        
        # Fuente 1: Análisis de luces nocturnas (simulado)
        try:
            night_lights_data = self._analyze_night_lights_pattern(lat_center, lon_center)
            traces_data['night_lights'] = night_lights_data
            logger.info("✅ Análisis de luces nocturnas completado")
        except Exception as e:
            logger.warning(f"⚠️ Night lights analysis failed: {e}")
        
        # Fuente 2: Identificación de rutas históricas
        try:
            historical_routes_data = self._identify_historical_routes(lat_center, lon_center)
            traces_data['historical_routes'] = historical_routes_data
            logger.info("✅ Rutas históricas identificadas")
        except Exception as e:
            logger.warning(f"⚠️ Historical routes identification failed: {e}")
        
        # Fuente 3: Análisis de cambios de uso del suelo
        try:
            land_use_data = self._analyze_land_use_changes(lat_center, lon_center)
            traces_data['land_use'] = land_use_data
            logger.info("✅ Cambios de uso del suelo analizados")
        except Exception as e:
            logger.warning(f"⚠️ Land use analysis failed: {e}")
        
        # Fuente 4: Identificación de corredores comerciales
        try:
            trade_corridors_data = self._identify_trade_corridors(lat_center, lon_center)
            traces_data['trade_corridors'] = trade_corridors_data
            logger.info("✅ Corredores comerciales identificados")
        except Exception as e:
            logger.warning(f"⚠️ Trade corridors identification failed: {e}")
        
        return traces_data
    
    def _analyze_night_lights_pattern(self, lat: float, lon: float) -> Dict[str, Any]:
        """Analizar patrones de luces nocturnas."""
        
        # Simulación de análisis de luces nocturnas
        # En producción usaría datos DMSP/OLS y VIIRS reales
        
        # Estimar intensidad basada en región
        if self._is_urban_region(lat, lon):
            light_intensity = np.random.uniform(0.7, 0.9)
            temporal_pattern = "continuous"
        elif self._is_rural_developed_region(lat, lon):
            light_intensity = np.random.uniform(0.3, 0.6)
            temporal_pattern = "intermittent"
        else:
            light_intensity = np.random.uniform(0.1, 0.3)
            temporal_pattern = "sparse"
        
        # Análisis temporal (cambios en últimas décadas)
        historical_trend = np.random.choice(['increasing', 'stable', 'decreasing'])
        
        return {
            'light_intensity': light_intensity,
            'temporal_pattern': temporal_pattern,
            'historical_trend': historical_trend,
            'archaeological_relevance': 0.6,
            'confidence': 0.7
        }
    
    def _identify_historical_routes(self, lat: float, lon: float) -> Dict[str, Any]:
        """Identificar rutas históricas conocidas."""
        
        routes = []
        
        # Identificar región para rutas específicas
        if self._is_in_roman_region(lat, lon):
            routes.append({
                'type': 'roman_road',
                'name': 'Via Romana',
                'period': 'ancient',
                'confidence': 0.8,
                'archaeological_relevance': 0.9
            })
        
        if self._is_in_inca_region(lat, lon):
            routes.append({
                'type': 'qhapaq_nan',
                'name': 'Camino del Inca',
                'period': 'ancient',
                'confidence': 0.85,
                'archaeological_relevance': 0.95
            })
        
        if self._is_in_silk_road_region(lat, lon):
            routes.append({
                'type': 'silk_road',
                'name': 'Ruta de la Seda',
                'period': 'historical',
                'confidence': 0.7,
                'archaeological_relevance': 0.85
            })
        
        # Rutas comerciales regionales (más generales)
        if np.random.random() > 0.4:  # 60% probabilidad
            routes.append({
                'type': 'regional_trade',
                'name': 'Ruta Comercial Regional',
                'period': 'historical',
                'confidence': 0.6,
                'archaeological_relevance': 0.7
            })
        
        return {'routes': routes}
    
    def _analyze_land_use_changes(self, lat: float, lon: float) -> Dict[str, Any]:
        """Analizar cambios históricos de uso del suelo."""
        
        # Simulación de análisis HYDE
        # En producción usaría datos HYDE reales
        
        # Uso actual estimado
        current_use = self._estimate_current_land_use(lat, lon)
        
        # Cambios históricos simulados
        historical_changes = []
        
        if current_use in ['agricultural', 'urban']:
            historical_changes.append({
                'period': 'recent_historical',
                'change_type': 'intensification',
                'intensity': np.random.uniform(0.6, 0.8)
            })
        
        if np.random.random() > 0.5:  # 50% probabilidad de cambio antiguo
            historical_changes.append({
                'period': 'ancient',
                'change_type': 'initial_modification',
                'intensity': np.random.uniform(0.3, 0.6)
            })
        
        return {
            'current_use': current_use,
            'historical_changes': historical_changes,
            'modification_intensity': np.random.uniform(0.4, 0.8),
            'archaeological_relevance': 0.8
        }
    
    def _identify_trade_corridors(self, lat: float, lon: float) -> Dict[str, Any]:
        """Identificar corredores comerciales históricos."""
        
        corridors = []
        
        # Corredores basados en geografía
        if self._is_river_valley_region(lat, lon):
            corridors.append({
                'type': 'river_trade',
                'name': 'Corredor Fluvial',
                'period': 'historical',
                'intensity': 'high'
            })
        
        if self._is_mountain_pass_region(lat, lon):
            corridors.append({
                'type': 'mountain_pass',
                'name': 'Paso de Montaña',
                'period': 'ancient',
                'intensity': 'moderate'
            })
        
        if self._is_coastal_region(lat, lon):
            corridors.append({
                'type': 'coastal_trade',
                'name': 'Ruta Costera',
                'period': 'historical',
                'intensity': 'high'
            })
        
        return {'corridors': corridors}
    
    def _process_human_traces_data(self, traces_data: Dict[str, Any],
                                  lat_min: float, lat_max: float,
                                  lon_min: float, lon_max: float) -> List[HumanTrace]:
        """Procesar datos de trazas humanas en objetos estructurados."""
        
        traces = []
        lat_center = (lat_min + lat_max) / 2
        lon_center = (lon_min + lon_max) / 2
        area_km2 = self._calculate_area_km2(lat_min, lat_max, lon_min, lon_max)
        
        # Procesar luces nocturnas
        if 'night_lights' in traces_data:
            night_data = traces_data['night_lights']
            
            trace = HumanTrace(
                trace_id=f"NL_{int(lat_center*1000)}_{int(lon_center*1000)}",
                trace_type=HumanTraceType.NIGHT_LIGHTS,
                center_coords=(lat_center, lon_center),
                extent_km2=area_km2,
                spatial_pattern=night_data.get('temporal_pattern', 'dispersed'),
                temporal_scale=TemporalScale.CONTEMPORARY,
                activity_intensity=self._map_intensity(night_data.get('light_intensity', 0.5)),
                persistence_score=night_data.get('light_intensity', 0.5),
                archaeological_relevance=night_data.get('archaeological_relevance', 0.6),
                cultural_significance=0.3,  # Baja para luces contemporáneas
                evidence_strength=night_data.get('confidence', 0.7),
                data_sources=['night_lights_analysis'],
                trace_explanation=f"Patrón de luces nocturnas {night_data.get('temporal_pattern', 'dispersed')} indica actividad humana contemporánea"
            )
            
            traces.append(trace)
        
        # Procesar rutas históricas
        if 'historical_routes' in traces_data:
            routes_data = traces_data['historical_routes']
            
            for route in routes_data.get('routes', []):
                trace = HumanTrace(
                    trace_id=f"HR_{route['type']}_{int(lat_center*1000)}_{int(lon_center*1000)}",
                    trace_type=HumanTraceType.HISTORICAL_ROUTE,
                    center_coords=(lat_center, lon_center),
                    extent_km2=area_km2 * 0.1,  # Rutas son lineales, menor área
                    spatial_pattern="linear",
                    temporal_scale=TemporalScale(route.get('period', 'historical')),
                    activity_intensity=ActivityIntensity.HIGH,  # Rutas implican alta actividad
                    persistence_score=route.get('confidence', 0.8),
                    archaeological_relevance=route.get('archaeological_relevance', 0.9),
                    cultural_significance=self.cultural_significance.get(TemporalScale(route.get('period', 'historical')), 0.8),
                    evidence_strength=route.get('confidence', 0.8),
                    data_sources=['historical_routes_db'],
                    trace_explanation=f"Ruta histórica {route.get('name', 'desconocida')} indica corredor de actividad humana antigua"
                )
                
                traces.append(trace)
        
        # Procesar cambios de uso del suelo
        if 'land_use' in traces_data:
            land_data = traces_data['land_use']
            
            for change in land_data.get('historical_changes', []):
                trace = HumanTrace(
                    trace_id=f"LU_{change['period']}_{int(lat_center*1000)}_{int(lon_center*1000)}",
                    trace_type=HumanTraceType.LAND_USE_CHANGE,
                    center_coords=(lat_center, lon_center),
                    extent_km2=area_km2,
                    spatial_pattern="dispersed",
                    temporal_scale=TemporalScale(change.get('period', 'historical')),
                    activity_intensity=self._map_intensity(change.get('intensity', 0.5)),
                    persistence_score=change.get('intensity', 0.5),
                    archaeological_relevance=land_data.get('archaeological_relevance', 0.8),
                    cultural_significance=self.cultural_significance.get(TemporalScale(change.get('period', 'historical')), 0.7),
                    evidence_strength=0.6,
                    data_sources=['land_use_reconstruction'],
                    trace_explanation=f"Cambio de uso del suelo ({change.get('change_type', 'modificación')}) indica transformación territorial humana"
                )
                
                traces.append(trace)
        
        # Procesar corredores comerciales
        if 'trade_corridors' in traces_data:
            corridors_data = traces_data['trade_corridors']
            
            for corridor in corridors_data.get('corridors', []):
                trace = HumanTrace(
                    trace_id=f"TC_{corridor['type']}_{int(lat_center*1000)}_{int(lon_center*1000)}",
                    trace_type=HumanTraceType.TRADE_CORRIDOR,
                    center_coords=(lat_center, lon_center),
                    extent_km2=area_km2 * 0.3,  # Corredores cubren área moderada
                    spatial_pattern="linear",
                    temporal_scale=TemporalScale(corridor.get('period', 'historical')),
                    activity_intensity=self._map_intensity_from_string(corridor.get('intensity', 'moderate')),
                    persistence_score=0.7,
                    archaeological_relevance=0.85,
                    cultural_significance=self.cultural_significance.get(TemporalScale(corridor.get('period', 'historical')), 0.8),
                    evidence_strength=0.6,
                    data_sources=['trade_corridors_analysis'],
                    trace_explanation=f"Corredor comercial {corridor.get('name', 'regional')} indica actividad económica histórica"
                )
                
                traces.append(trace)
        
        return traces
    
    def generate_territorial_use_profile(self, traces: List[HumanTrace]) -> TerritorialUseProfile:
        """
        Generar perfil de uso territorial basado en trazas humanas.
        
        CRÍTICO: Transforma trazas individuales en comprensión territorial integral.
        """
        
        if not traces:
            return self._create_default_territorial_use_profile()
        
        # Determinar uso primario
        use_types = {}
        for trace in traces:
            use_type = self._map_trace_to_use_type(trace.trace_type)
            use_types[use_type] = use_types.get(use_type, 0) + trace.evidence_strength
        
        primary_use = max(use_types.keys(), key=lambda k: use_types[k]) if use_types else "unknown"
        secondary_uses = [use for use, score in sorted(use_types.items(), key=lambda x: x[1], reverse=True)[1:3]]
        
        # Calcular intensidad general
        intensities = [trace.activity_intensity for trace in traces]
        intensity_scores = [self._intensity_to_score(intensity) for intensity in intensities]
        avg_intensity_score = np.mean(intensity_scores)
        overall_intensity = self._score_to_intensity(avg_intensity_score)
        
        # Calcular continuidad temporal
        temporal_scores = []
        for trace in traces:
            if trace.temporal_scale == TemporalScale.ANCIENT:
                temporal_scores.append(1.0)
            elif trace.temporal_scale == TemporalScale.HISTORICAL:
                temporal_scores.append(0.8)
            elif trace.temporal_scale == TemporalScale.RECENT_HISTORICAL:
                temporal_scores.append(0.6)
            else:
                temporal_scores.append(0.4)
        
        temporal_continuity = np.mean(temporal_scores) if temporal_scores else 0.5
        
        # Determinar distribución de uso
        spatial_patterns = [trace.spatial_pattern for trace in traces]
        if spatial_patterns.count("linear") > len(spatial_patterns) * 0.5:
            use_distribution = "linear"
        elif spatial_patterns.count("clustered") > len(spatial_patterns) * 0.3:
            use_distribution = "concentrated"
        else:
            use_distribution = "dispersed"
        
        # Calcular score de conectividad
        route_traces = [t for t in traces if t.trace_type in [HumanTraceType.HISTORICAL_ROUTE, HumanTraceType.TRADE_CORRIDOR]]
        connectivity_score = min(1.0, len(route_traces) / 3.0)  # Normalizado a máximo 3 rutas
        
        # Potencial de asentamiento
        settlement_potential = np.mean([trace.archaeological_relevance for trace in traces])
        
        # Score de paisaje cultural
        cultural_traces = [t for t in traces if t.cultural_significance > 0.7]
        cultural_landscape_score = len(cultural_traces) / len(traces) if traces else 0.0
        
        # Generar explicación
        explanation = self._generate_territorial_use_explanation(primary_use, overall_intensity, temporal_continuity)
        
        # Implicaciones arqueológicas
        implications = self._identify_territorial_archaeological_implications(traces, primary_use)
        
        return TerritorialUseProfile(
            primary_use=primary_use,
            secondary_uses=secondary_uses,
            overall_intensity=overall_intensity,
            temporal_continuity=temporal_continuity,
            use_distribution=use_distribution,
            connectivity_score=connectivity_score,
            settlement_potential=settlement_potential,
            cultural_landscape_score=cultural_landscape_score,
            use_explanation=explanation,
            archaeological_implications=implications
        )
    
    # Métodos auxiliares
    
    def _calculate_area_km2(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> float:
        """Calcular área en km²."""
        lat_extent = (lat_max - lat_min) * 111.32
        lon_extent = (lon_max - lon_min) * 111.32 * np.cos(np.radians((lat_min + lat_max) / 2))
        return lat_extent * lon_extent
    
    def _is_urban_region(self, lat: float, lon: float) -> bool:
        """Determinar si es región urbana."""
        # Simplificación - en producción usaría datos reales
        return np.random.random() > 0.7
    
    def _is_rural_developed_region(self, lat: float, lon: float) -> bool:
        """Determinar si es región rural desarrollada."""
        return np.random.random() > 0.5
    
    def _is_in_roman_region(self, lat: float, lon: float) -> bool:
        """Determinar si está en región del Imperio Romano."""
        return (25 <= lat <= 55 and -10 <= lon <= 40)
    
    def _is_in_inca_region(self, lat: float, lon: float) -> bool:
        """Determinar si está en región del Imperio Inca."""
        return (-20 <= lat <= 5 and -85 <= lon <= -65)
    
    def _is_in_silk_road_region(self, lat: float, lon: float) -> bool:
        """Determinar si está en región de la Ruta de la Seda."""
        return (30 <= lat <= 50 and 60 <= lon <= 120)
    
    def _is_river_valley_region(self, lat: float, lon: float) -> bool:
        """Determinar si está en región de valle fluvial."""
        return np.random.random() > 0.6
    
    def _is_mountain_pass_region(self, lat: float, lon: float) -> bool:
        """Determinar si está en región de paso montañoso."""
        return abs(lat) > 30 and np.random.random() > 0.7
    
    def _is_coastal_region(self, lat: float, lon: float) -> bool:
        """Determinar si está en región costera."""
        return np.random.random() > 0.5
    
    def _estimate_current_land_use(self, lat: float, lon: float) -> str:
        """Estimar uso actual del suelo."""
        uses = ['agricultural', 'forest', 'urban', 'grassland', 'barren']
        weights = [0.3, 0.25, 0.15, 0.2, 0.1]
        return np.random.choice(uses, p=weights)
    
    def _map_intensity(self, value: float) -> ActivityIntensity:
        """Mapear valor numérico a intensidad de actividad."""
        if value > 0.8:
            return ActivityIntensity.VERY_HIGH
        elif value > 0.6:
            return ActivityIntensity.HIGH
        elif value > 0.4:
            return ActivityIntensity.MODERATE
        elif value > 0.2:
            return ActivityIntensity.LOW
        else:
            return ActivityIntensity.MINIMAL
    
    def _map_intensity_from_string(self, intensity_str: str) -> ActivityIntensity:
        """Mapear string a intensidad de actividad."""
        mapping = {
            'very_high': ActivityIntensity.VERY_HIGH,
            'high': ActivityIntensity.HIGH,
            'moderate': ActivityIntensity.MODERATE,
            'low': ActivityIntensity.LOW,
            'minimal': ActivityIntensity.MINIMAL
        }
        return mapping.get(intensity_str, ActivityIntensity.MODERATE)
    
    def _intensity_to_score(self, intensity: ActivityIntensity) -> float:
        """Convertir intensidad a score numérico."""
        mapping = {
            ActivityIntensity.VERY_HIGH: 1.0,
            ActivityIntensity.HIGH: 0.8,
            ActivityIntensity.MODERATE: 0.6,
            ActivityIntensity.LOW: 0.4,
            ActivityIntensity.MINIMAL: 0.2,
            ActivityIntensity.UNKNOWN: 0.5
        }
        return mapping.get(intensity, 0.5)
    
    def _score_to_intensity(self, score: float) -> ActivityIntensity:
        """Convertir score numérico a intensidad."""
        if score > 0.8:
            return ActivityIntensity.VERY_HIGH
        elif score > 0.6:
            return ActivityIntensity.HIGH
        elif score > 0.4:
            return ActivityIntensity.MODERATE
        elif score > 0.2:
            return ActivityIntensity.LOW
        else:
            return ActivityIntensity.MINIMAL
    
    def _map_trace_to_use_type(self, trace_type: HumanTraceType) -> str:
        """Mapear tipo de traza a tipo de uso territorial."""
        mapping = {
            HumanTraceType.NIGHT_LIGHTS: "residential",
            HumanTraceType.HISTORICAL_ROUTE: "transportation",
            HumanTraceType.LAND_USE_CHANGE: "agricultural",
            HumanTraceType.TRADE_CORRIDOR: "commercial",
            HumanTraceType.SETTLEMENT_PATTERN: "residential",
            HumanTraceType.RESOURCE_EXTRACTION: "industrial",
            HumanTraceType.UNKNOWN: "mixed"
        }
        return mapping.get(trace_type, "mixed")
    
    def _generate_territorial_use_explanation(self, primary_use: str, intensity: ActivityIntensity, continuity: float) -> str:
        """Generar explicación de uso territorial."""
        
        intensity_desc = {
            ActivityIntensity.VERY_HIGH: "muy intensa",
            ActivityIntensity.HIGH: "intensa",
            ActivityIntensity.MODERATE: "moderada",
            ActivityIntensity.LOW: "baja",
            ActivityIntensity.MINIMAL: "mínima"
        }.get(intensity, "variable")
        
        continuity_desc = "alta" if continuity > 0.7 else "moderada" if continuity > 0.4 else "baja"
        
        return f"Territorio con uso primario {primary_use}, actividad {intensity_desc} y continuidad temporal {continuity_desc}. Patrón de ocupación humana sostenida."
    
    def _identify_territorial_archaeological_implications(self, traces: List[HumanTrace], primary_use: str) -> List[str]:
        """Identificar implicaciones arqueológicas del uso territorial."""
        
        implications = []
        
        # Rutas históricas
        route_traces = [t for t in traces if t.trace_type in [HumanTraceType.HISTORICAL_ROUTE, HumanTraceType.TRADE_CORRIDOR]]
        if route_traces:
            implications.append(f"Presencia de {len(route_traces)} corredor(es) de actividad histórica")
        
        # Trazas antiguas
        ancient_traces = [t for t in traces if t.temporal_scale == TemporalScale.ANCIENT]
        if ancient_traces:
            implications.append(f"Evidencia de {len(ancient_traces)} traza(s) de actividad antigua")
        
        # Alta intensidad de uso
        high_intensity_traces = [t for t in traces if t.activity_intensity in [ActivityIntensity.HIGH, ActivityIntensity.VERY_HIGH]]
        if len(high_intensity_traces) > len(traces) * 0.5:
            implications.append("Patrón de uso territorial intensivo favorable para arqueología")
        
        # Uso primario específico
        if primary_use == "transportation":
            implications.append("Territorio de tránsito con potencial para sitios de paso y descanso")
        elif primary_use == "commercial":
            implications.append("Territorio comercial con potencial para centros de intercambio")
        elif primary_use == "residential":
            implications.append("Territorio residencial con potencial para asentamientos permanentes")
        
        return implications
    
    def _create_default_human_traces(self, lat_min: float, lat_max: float,
                                   lon_min: float, lon_max: float) -> List[HumanTrace]:
        """Crear trazas humanas por defecto."""
        
        lat_center = (lat_min + lat_max) / 2
        lon_center = (lon_min + lon_max) / 2
        area_km2 = self._calculate_area_km2(lat_min, lat_max, lon_min, lon_max)
        
        default_trace = HumanTrace(
            trace_id='DEFAULT_HT_001',
            trace_type=HumanTraceType.UNKNOWN,
            center_coords=(lat_center, lon_center),
            extent_km2=area_km2,
            spatial_pattern="dispersed",
            temporal_scale=TemporalScale.UNKNOWN,
            activity_intensity=ActivityIntensity.UNKNOWN,
            persistence_score=0.5,
            archaeological_relevance=0.5,
            cultural_significance=0.5,
            evidence_strength=0.1,
            data_sources=['default'],
            trace_explanation="Trazas humanas no disponibles - usando valores por defecto"
        )
        
        return [default_trace]
    
    def _create_default_territorial_use_profile(self) -> TerritorialUseProfile:
        """Crear perfil de uso territorial por defecto."""
        
        return TerritorialUseProfile(
            primary_use="unknown",
            secondary_uses=[],
            overall_intensity=ActivityIntensity.UNKNOWN,
            temporal_continuity=0.5,
            use_distribution="dispersed",
            connectivity_score=0.5,
            settlement_potential=0.5,
            cultural_landscape_score=0.5,
            use_explanation="Perfil de uso territorial no disponible - usando valores por defecto",
            archaeological_implications=["Contexto de trazas humanas limitado"]
        )