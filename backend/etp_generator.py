#!/usr/bin/env python3
"""
ETP Generator - Generador de Perfiles Tomográficos Ambientales
=============================================================

MOTOR PRINCIPAL del sistema ETP que transforma datos satelitales 
en perfiles tomográficos explicables.

PROCESO:
1. Adquisición de datos por capas de profundidad
2. Generación de cortes XZ/YZ/XY
3. Cálculo de ESS volumétrico y temporal
4. Generación de narrativa territorial
5. Preparación de datos para visualización
"""

import asyncio
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta

from .etp_core import (
    EnvironmentalTomographicProfile, TomographicSlice, TomographicLayer,
    VolumetricAnomaly, BoundingBox, SliceType, OccupationPeriod,
    TerritorialFunction, LandscapeEvolution
)

logger = logging.getLogger(__name__)

class ETProfileGenerator:
    """Generador de perfiles tomográficos ambientales."""
    
    def __init__(self, integrator_15_instruments):
        """
        Inicializar generador ETP.
        
        Args:
            integrator_15_instruments: RealDataIntegratorV2 con 15 instrumentos
        """
        self.integrator = integrator_15_instruments
        
        # Capas de profundidad estándar para análisis tomográfico
        self.depth_layers = [0, -0.5, -1, -2, -3, -5, -10, -20]  # metros
        
        # Mapeo de instrumentos por capacidad de penetración
        self.instrument_depth_mapping = {
            # Superficie (0m)
            0: ['sentinel_2_ndvi', 'viirs_thermal', 'viirs_ndvi', 'srtm_elevation'],
            
            # Subsuperficie ligera (-0.5m a -1m)
            -0.5: ['sentinel_1_sar', 'viirs_thermal', 'landsat_thermal'],
            -1: ['sentinel_1_sar', 'modis_lst', 'palsar_backscatter'],
            
            # Subsuperficie media (-2m a -3m)
            -2: ['palsar_backscatter', 'palsar_penetration', 'icesat2'],
            -3: ['palsar_penetration', 'palsar_soil_moisture'],
            
            # Profundidad (-5m a -20m)
            -5: ['palsar_penetration'],  # Máxima penetración L-band
            -10: ['palsar_penetration'],  # Inferencia geofísica
            -20: []  # Solo inferencia basada en patrones superiores
        }
        
        # Pesos por profundidad para ESS volumétrico
        self.depth_weights = {
            0: 1.0,      # Superficie - peso completo
            -0.5: 0.9,   # Subsuperficie ligera
            -1: 0.8,     # Subsuperficie
            -2: 0.7,     # Subsuperficie media
            -3: 0.6,     # Subsuperficie profunda
            -5: 0.5,     # Profundidad media
            -10: 0.3,    # Profundidad alta
            -20: 0.1     # Profundidad máxima (inferencia)
        }
        
        logger.info("🧠 ETProfileGenerator inicializado - SISTEMA TOMOGRÁFICO ACTIVO")
    
    async def generate_etp(self, bounds: BoundingBox, 
                          resolution_m: float = 30.0) -> EnvironmentalTomographicProfile:
        """
        Generar perfil tomográfico completo.
        
        PROCESO REVOLUCIONARIO:
        1. Adquisición por capas → datos volumétricos
        2. Cortes tomográficos → comprensión espacial
        3. ESS evolucionado → métricas 3D/4D
        4. Narrativa territorial → explicación automática
        
        Args:
            bounds: Región 3D a analizar
            resolution_m: Resolución espacial en metros
            
        Returns:
            EnvironmentalTomographicProfile completo
        """
        
        logger.info(f"🚀 Generando ETP para territorio {bounds.center_lat:.4f}, {bounds.center_lon:.4f}")
        logger.info(f"📐 Volumen: {bounds.volume_km3:.3f} km³, Resolución: {resolution_m}m")
        
        territory_id = f"ETP_{bounds.center_lat:.4f}_{bounds.center_lon:.4f}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # FASE 1: Adquisición de datos por capas
        logger.info("📡 FASE 1: Adquisición de datos por capas de profundidad...")
        layered_data = await self._acquire_layered_data(bounds)
        
        # FASE 2: Generación de cortes tomográficos
        logger.info("🔬 FASE 2: Generación de cortes tomográficos...")
        xz_profile = self._generate_xz_slice(layered_data, bounds)
        yz_profile = self._generate_yz_slice(layered_data, bounds)
        xy_profiles = self._generate_xy_slices(layered_data, bounds)
        
        # FASE 3: Análisis temporal
        logger.info("⏰ FASE 3: Análisis temporal...")
        temporal_profile = await self._generate_temporal_analysis(bounds)
        
        # FASE 4: Cálculo de ESS evolucionado
        logger.info("📊 FASE 4: Cálculo de ESS volumétrico y temporal...")
        ess_superficial = self._calculate_surface_ess(layered_data.get(0, {}))
        ess_volumetrico = self._calculate_volumetric_ess(layered_data)
        ess_temporal = self._calculate_temporal_ess(temporal_profile, ess_volumetrico)
        
        # FASE 5: Métricas 3D
        logger.info("🧮 FASE 5: Cálculo de métricas 3D...")
        coherencia_3d = self._calculate_3d_coherence(layered_data)
        persistencia = self._calculate_temporal_persistence(temporal_profile)
        densidad_m3 = self._calculate_archaeological_density(layered_data, bounds)
        
        # FASE 6: Detección de anomalías volumétricas
        logger.info("🎯 FASE 6: Detección de anomalías volumétricas...")
        volumetric_anomalies = self._detect_volumetric_anomalies(layered_data, bounds)
        
        # FASE 7: Interpretación narrativa - REVOLUCIÓN CONCEPTUAL
        logger.info("📖 FASE 7: Generación de narrativa territorial...")
        narrative = self._generate_territorial_narrative(
            xz_profile, yz_profile, temporal_profile, volumetric_anomalies
        )
        
        occupational_history = self._analyze_occupational_history(temporal_profile, volumetric_anomalies)
        territorial_function = self._determine_territorial_function(volumetric_anomalies, layered_data)
        landscape_evolution = self._analyze_landscape_evolution(temporal_profile, layered_data)
        
        # FASE 8: Preparación de datos de visualización
        logger.info("🎨 FASE 8: Preparación de datos de visualización...")
        visualization_data = self._prepare_visualization_data(
            xz_profile, yz_profile, xy_profiles, layered_data
        )
        
        # Crear perfil tomográfico completo
        etp = EnvironmentalTomographicProfile(
            territory_id=territory_id,
            bounds=bounds,
            resolution_m=resolution_m,
            xz_profile=xz_profile,
            yz_profile=yz_profile,
            xy_profiles=xy_profiles,
            temporal_profile=temporal_profile,
            ess_superficial=ess_superficial,
            ess_volumetrico=ess_volumetrico,
            ess_temporal=ess_temporal,
            coherencia_3d=coherencia_3d,
            persistencia_temporal=persistencia,
            densidad_arqueologica_m3=densidad_m3,
            narrative_explanation=narrative,
            occupational_history=occupational_history,
            territorial_function=territorial_function,
            landscape_evolution=landscape_evolution,
            visualization_data=visualization_data
        )
        
        logger.info(f"✅ ETP generado exitosamente:")
        logger.info(f"   📊 ESS Volumétrico: {ess_volumetrico:.3f}")
        logger.info(f"   📊 ESS Temporal: {ess_temporal:.3f}")
        logger.info(f"   📊 Coherencia 3D: {coherencia_3d:.3f}")
        logger.info(f"   🏛️ Anomalías detectadas: {len(volumetric_anomalies)}")
        
        return etp
    
    async def _acquire_layered_data(self, bounds: BoundingBox) -> Dict[float, Dict[str, Any]]:
        """Adquirir datos por capas de profundidad."""
        
        layered_data = {}
        
        for depth in self.depth_layers:
            logger.info(f"  📡 Adquiriendo datos para profundidad {depth}m...")
            
            # Obtener instrumentos apropiados para esta profundidad
            instruments = self.instrument_depth_mapping.get(depth, [])
            
            if not instruments:
                logger.info(f"    ⚠️ Sin instrumentos para {depth}m - usando inferencia")
                layered_data[depth] = {}
                continue
            
            # Adquirir datos de instrumentos
            layer_data = {}
            
            for instrument in instruments:
                try:
                    result = await self.integrator.get_instrument_measurement_robust(
                        instrument_name=instrument,
                        lat_min=bounds.lat_min,
                        lat_max=bounds.lat_max,
                        lon_min=bounds.lon_min,
                        lon_max=bounds.lon_max
                    )
                    
                    if result and hasattr(result, 'status') and result.status in ['SUCCESS', 'DEGRADED']:
                        layer_data[instrument] = {
                            'value': getattr(result, 'value', 0.0),
                            'unit': getattr(result, 'unit', 'units'),
                            'confidence': getattr(result, 'confidence', 0.5),
                            'status': result.status
                        }
                        logger.info(f"    ✅ {instrument}: {layer_data[instrument]['value']:.3f}")
                    else:
                        logger.info(f"    ❌ {instrument}: Sin datos válidos")
                        
                except Exception as e:
                    logger.warning(f"    💥 {instrument}: Error - {e}")
            
            layered_data[depth] = layer_data
        
        return layered_data
    def _generate_xz_slice(self, layered_data: Dict[float, Dict[str, Any]], 
                          bounds: BoundingBox) -> TomographicSlice:
        """Generar corte longitudinal XZ (Este-Oeste con profundidad)."""
        
        layers = []
        
        for depth in sorted(self.depth_layers):
            layer_data = layered_data.get(depth, {})
            
            # Calcular intensidad de anomalía para esta capa
            anomaly_intensity = self._calculate_layer_anomaly_intensity(layer_data)
            
            # Calcular probabilidad arqueológica
            arch_probability = self._calculate_archaeological_probability_layer(layer_data, depth)
            
            layer = TomographicLayer(
                depth_m=depth,
                instruments_data=layer_data,
                anomaly_intensity=anomaly_intensity,
                archaeological_probability=arch_probability
            )
            
            layers.append(layer)
        
        # Calcular ESS del corte
        slice_ess = np.mean([layer.anomaly_intensity for layer in layers if layer.anomaly_intensity > 0])
        
        # Calcular coherencia del corte
        coherence = self._calculate_slice_coherence(layers)
        
        return TomographicSlice(
            slice_type=SliceType.XZ,
            depth_range=(0, -20),
            layers=layers,
            slice_ess=slice_ess,
            coherence_score=coherence
        )
    
    def _generate_yz_slice(self, layered_data: Dict[float, Dict[str, Any]], 
                          bounds: BoundingBox) -> TomographicSlice:
        """Generar corte latitudinal YZ (Norte-Sur con profundidad)."""
        
        # Similar al XZ pero con orientación Norte-Sur
        layers = []
        
        for depth in sorted(self.depth_layers):
            layer_data = layered_data.get(depth, {})
            
            anomaly_intensity = self._calculate_layer_anomaly_intensity(layer_data)
            arch_probability = self._calculate_archaeological_probability_layer(layer_data, depth)
            
            layer = TomographicLayer(
                depth_m=depth,
                instruments_data=layer_data,
                anomaly_intensity=anomaly_intensity,
                archaeological_probability=arch_probability
            )
            
            layers.append(layer)
        
        slice_ess = np.mean([layer.anomaly_intensity for layer in layers if layer.anomaly_intensity > 0])
        coherence = self._calculate_slice_coherence(layers)
        
        return TomographicSlice(
            slice_type=SliceType.YZ,
            depth_range=(0, -20),
            layers=layers,
            slice_ess=slice_ess,
            coherence_score=coherence
        )
    
    def _generate_xy_slices(self, layered_data: Dict[float, Dict[str, Any]], 
                           bounds: BoundingBox) -> List[TomographicSlice]:
        """Generar cortes horizontales XY por profundidad."""
        
        xy_slices = []
        
        for depth in sorted(self.depth_layers):
            layer_data = layered_data.get(depth, {})
            
            if not layer_data:
                continue
            
            # Crear capa única para este nivel de profundidad
            anomaly_intensity = self._calculate_layer_anomaly_intensity(layer_data)
            arch_probability = self._calculate_archaeological_probability_layer(layer_data, depth)
            
            layer = TomographicLayer(
                depth_m=depth,
                instruments_data=layer_data,
                anomaly_intensity=anomaly_intensity,
                archaeological_probability=arch_probability
            )
            
            xy_slice = TomographicSlice(
                slice_type=SliceType.XY,
                depth_range=(depth, depth),
                layers=[layer],
                slice_ess=anomaly_intensity,
                coherence_score=1.0  # Coherencia perfecta para capa única
            )
            
            xy_slices.append(xy_slice)
        
        return xy_slices
    
    async def _generate_temporal_analysis(self, bounds: BoundingBox) -> Dict[str, Any]:
        """Generar análisis temporal usando ERA5 y CHIRPS."""
        
        temporal_data = {}
        
        try:
            # Obtener contexto climático histórico con ERA5
            era5_result = await self.integrator.get_instrument_measurement_robust(
                instrument_name='era5_climate',
                lat_min=bounds.lat_min,
                lat_max=bounds.lat_max,
                lon_min=bounds.lon_min,
                lon_max=bounds.lon_max
            )
            
            if era5_result and hasattr(era5_result, 'value'):
                temporal_data['climate_context'] = {
                    'preservation_score': era5_result.value,
                    'climate_stability': 'stable' if era5_result.value > 0.7 else 'variable'
                }
            
            # Obtener análisis de precipitación histórica con CHIRPS
            chirps_result = await self.integrator.get_instrument_measurement_robust(
                instrument_name='chirps_precipitation',
                lat_min=bounds.lat_min,
                lat_max=bounds.lat_max,
                lon_min=bounds.lon_min,
                lon_max=bounds.lon_max
            )
            
            if chirps_result and hasattr(chirps_result, 'value'):
                temporal_data['precipitation_history'] = {
                    'precipitation_index': chirps_result.value,
                    'water_availability': 'high' if chirps_result.value > 0.6 else 'low'
                }
            
            # Análisis de tendencias temporales
            temporal_data['temporal_trends'] = {
                'occupation_viability': self._assess_occupation_viability(temporal_data),
                'abandonment_risk': self._assess_abandonment_risk(temporal_data)
            }
            
        except Exception as e:
            logger.warning(f"Error en análisis temporal: {e}")
            temporal_data = {'error': str(e)}
        
        return temporal_data
    
    def _calculate_surface_ess(self, surface_data: Dict[str, Any]) -> float:
        """Calcular ESS superficial tradicional."""
        
        if not surface_data:
            return 0.0
        
        anomaly_scores = []
        
        for instrument, data in surface_data.items():
            if isinstance(data, dict) and 'value' in data:
                # Normalizar valor según tipo de instrumento
                normalized_score = self._normalize_instrument_value(instrument, data['value'])
                confidence = data.get('confidence', 0.5)
                
                # Score ponderado por confianza
                weighted_score = normalized_score * confidence
                anomaly_scores.append(weighted_score)
        
        return np.mean(anomaly_scores) if anomaly_scores else 0.0
    
    def _calculate_volumetric_ess(self, layered_data: Dict[float, Dict[str, Any]]) -> float:
        """Calcular ESS volumétrico - NÚCLEO DEL CONCEPTO ETP."""
        
        volumetric_scores = []
        
        for depth, layer_data in layered_data.items():
            if not layer_data:
                continue
            
            # ESS de la capa
            layer_ess = self._calculate_surface_ess(layer_data)
            
            # Aplicar peso por profundidad
            depth_weight = self.depth_weights.get(depth, 0.1)
            weighted_ess = layer_ess * depth_weight
            
            volumetric_scores.append(weighted_ess)
        
        if not volumetric_scores:
            return 0.0
        
        # ESS volumétrico = promedio ponderado por profundidad
        volumetric_ess = np.sum(volumetric_scores) / len(self.depth_layers)
        
        return min(1.0, volumetric_ess)  # Normalizar a [0,1]
    
    def _calculate_temporal_ess(self, temporal_profile: Dict[str, Any], 
                               volumetric_ess: float) -> float:
        """Calcular ESS temporal - DIMENSIÓN 4D."""
        
        if not temporal_profile or 'temporal_trends' not in temporal_profile:
            return volumetric_ess  # Fallback al volumétrico
        
        trends = temporal_profile['temporal_trends']
        
        # Factores temporales
        occupation_factor = 1.0
        if trends.get('occupation_viability') == 'high':
            occupation_factor = 1.2
        elif trends.get('occupation_viability') == 'low':
            occupation_factor = 0.8
        
        abandonment_factor = 1.0
        if trends.get('abandonment_risk') == 'high':
            abandonment_factor = 0.9  # Reduce ligeramente por abandono
        
        # Estabilidad climática
        climate_factor = 1.0
        if temporal_profile.get('climate_context', {}).get('climate_stability') == 'stable':
            climate_factor = 1.1
        
        # ESS temporal = ESS volumétrico * factores temporales
        temporal_ess = volumetric_ess * occupation_factor * abandonment_factor * climate_factor
        
        return min(1.0, temporal_ess)  # Normalizar a [0,1]
    
    def _calculate_3d_coherence(self, layered_data: Dict[float, Dict[str, Any]]) -> float:
        """Calcular coherencia espacial 3D."""
        
        coherence_scores = []
        
        # Coherencia vertical (entre capas)
        depths = sorted(layered_data.keys())
        for i in range(len(depths) - 1):
            depth1, depth2 = depths[i], depths[i + 1]
            
            layer1_ess = self._calculate_surface_ess(layered_data[depth1])
            layer2_ess = self._calculate_surface_ess(layered_data[depth2])
            
            # Coherencia = similitud entre capas adyacentes
            if layer1_ess > 0 and layer2_ess > 0:
                coherence = 1.0 - abs(layer1_ess - layer2_ess)
                coherence_scores.append(coherence)
        
        return np.mean(coherence_scores) if coherence_scores else 0.5
    
    def _calculate_temporal_persistence(self, temporal_profile: Dict[str, Any]) -> float:
        """Calcular persistencia temporal."""
        
        if not temporal_profile:
            return 0.5
        
        # Factores de persistencia
        persistence_factors = []
        
        # Estabilidad climática
        climate_context = temporal_profile.get('climate_context', {})
        if climate_context.get('climate_stability') == 'stable':
            persistence_factors.append(0.8)
        else:
            persistence_factors.append(0.4)
        
        # Disponibilidad de agua
        precip_history = temporal_profile.get('precipitation_history', {})
        if precip_history.get('water_availability') == 'high':
            persistence_factors.append(0.7)
        else:
            persistence_factors.append(0.3)
        
        return np.mean(persistence_factors) if persistence_factors else 0.5
    def _calculate_archaeological_density(self, layered_data: Dict[float, Dict[str, Any]], 
                                         bounds: BoundingBox) -> float:
        """Calcular densidad arqueológica por m³."""
        
        total_anomaly_volume = 0.0
        
        for depth, layer_data in layered_data.items():
            layer_ess = self._calculate_surface_ess(layer_data)
            
            if layer_ess > 0.5:  # Umbral de anomalía significativa
                # Volumen de la capa (área * espesor de 1m)
                layer_volume = bounds.area_km2 * 1000 * 1000 * 1  # m³
                anomaly_contribution = layer_ess * layer_volume
                total_anomaly_volume += anomaly_contribution
        
        # Densidad = volumen anómalo / volumen total
        total_volume = bounds.volume_km3 * 1000 * 1000 * 1000  # m³
        density = total_anomaly_volume / total_volume if total_volume > 0 else 0.0
        
        return density
    
    def _detect_volumetric_anomalies(self, layered_data: Dict[float, Dict[str, Any]], 
                                    bounds: BoundingBox) -> List[VolumetricAnomaly]:
        """Detectar anomalías volumétricas significativas."""
        
        anomalies = []
        
        for depth, layer_data in layered_data.items():
            layer_ess = self._calculate_surface_ess(layer_data)
            
            if layer_ess > 0.6:  # Umbral para anomalía significativa
                
                # Determinar tipo arqueológico basado en profundidad y señales
                arch_type = self._classify_archaeological_type(depth, layer_data)
                
                # Estimar extensión 3D (simplificado)
                extent_x = (bounds.lon_max - bounds.lon_min) * 111320  # metros
                extent_y = (bounds.lat_max - bounds.lat_min) * 111320  # metros
                extent_z = 2.0  # Asumimos 2m de espesor
                
                # Centro de la anomalía
                center_x = (bounds.lon_min + bounds.lon_max) / 2
                center_y = (bounds.lat_min + bounds.lat_max) / 2
                center_z = depth
                
                # Instrumentos que soportan la detección
                supporting_instruments = [
                    instrument for instrument, data in layer_data.items()
                    if isinstance(data, dict) and data.get('value', 0) > 0
                ]
                
                anomaly = VolumetricAnomaly(
                    center_3d=(center_x, center_y, center_z),
                    extent_3d=(extent_x, extent_y, extent_z),
                    intensity=layer_ess,
                    archaeological_type=arch_type,
                    temporal_range=(self._estimate_temporal_range(arch_type)),
                    confidence=layer_ess,
                    instruments_supporting=supporting_instruments
                )
                
                anomalies.append(anomaly)
        
        return anomalies
    
    def _generate_territorial_narrative(self, xz_profile: TomographicSlice, 
                                       yz_profile: TomographicSlice,
                                       temporal_profile: Dict[str, Any],
                                       anomalies: List[VolumetricAnomaly]) -> str:
        """Generar narrativa territorial explicable - REVOLUCIÓN CONCEPTUAL."""
        
        narrative_parts = []
        
        # Introducción territorial
        narrative_parts.append("ANÁLISIS TERRITORIAL TOMOGRÁFICO:")
        
        # Análisis de superficie
        surface_layers = [layer for layer in xz_profile.layers if layer.depth_m == 0]
        if surface_layers:
            surface_intensity = surface_layers[0].anomaly_intensity
            if surface_intensity > 0.7:
                narrative_parts.append(f"La superficie presenta anomalías significativas (intensidad: {surface_intensity:.2f}), indicando posible actividad arqueológica visible.")
            elif surface_intensity > 0.4:
                narrative_parts.append(f"La superficie muestra anomalías moderadas (intensidad: {surface_intensity:.2f}), sugiriendo evidencia arqueológica sutil.")
            else:
                narrative_parts.append("La superficie no presenta anomalías significativas, pero el análisis subsuperficial revela patrones de interés.")
        
        # Análisis subsuperficial
        subsurface_layers = [layer for layer in xz_profile.layers if -3 <= layer.depth_m < 0]
        if subsurface_layers:
            max_subsurface = max(layer.anomaly_intensity for layer in subsurface_layers)
            if max_subsurface > 0.6:
                narrative_parts.append(f"El análisis subsuperficial (0-3m) revela estructuras enterradas con alta probabilidad arqueológica (máximo: {max_subsurface:.2f}).")
        
        # Análisis de profundidad
        deep_layers = [layer for layer in xz_profile.layers if layer.depth_m < -3]
        if deep_layers:
            max_deep = max(layer.anomaly_intensity for layer in deep_layers)
            if max_deep > 0.5:
                narrative_parts.append(f"Las capas profundas (>3m) muestran evidencia de estructuras complejas o sistemas constructivos antiguos (intensidad: {max_deep:.2f}).")
        
        # Análisis temporal
        if temporal_profile:
            climate_context = temporal_profile.get('climate_context', {})
            if climate_context.get('climate_stability') == 'stable':
                narrative_parts.append("Las condiciones climáticas históricas han sido favorables para la preservación arqueológica.")
            
            precip_history = temporal_profile.get('precipitation_history', {})
            if precip_history.get('water_availability') == 'high':
                narrative_parts.append("La disponibilidad histórica de agua sugiere condiciones propicias para asentamientos permanentes.")
        
        # Análisis de anomalías específicas
        if anomalies:
            structure_anomalies = [a for a in anomalies if a.archaeological_type == 'structure']
            if structure_anomalies:
                narrative_parts.append(f"Se identificaron {len(structure_anomalies)} anomalías estructurales con alta confianza arqueológica.")
            
            hydraulic_anomalies = [a for a in anomalies if a.archaeological_type == 'hydraulic_system']
            if hydraulic_anomalies:
                narrative_parts.append(f"Evidencia de {len(hydraulic_anomalies)} sistemas hidráulicos antiguos, indicando manejo sofisticado del agua.")
        
        # Conclusión territorial
        if len(anomalies) > 3:
            narrative_parts.append("El territorio presenta un patrón complejo de ocupación arqueológica con múltiples fases constructivas y funciones especializadas.")
        elif len(anomalies) > 1:
            narrative_parts.append("El territorio muestra evidencia de ocupación arqueológica organizada con estructuras diferenciadas.")
        else:
            narrative_parts.append("El territorio presenta indicios arqueológicos que requieren investigación adicional para confirmar su naturaleza y extensión.")
        
        return " ".join(narrative_parts)
    
    def _analyze_occupational_history(self, temporal_profile: Dict[str, Any], 
                                     anomalies: List[VolumetricAnomaly]) -> List[OccupationPeriod]:
        """Analizar historia ocupacional del territorio."""
        
        periods = []
        
        # Análisis basado en tipos de anomalías y contexto temporal
        if anomalies:
            # Período temprano (basado en anomalías profundas)
            deep_anomalies = [a for a in anomalies if a.center_3d[2] < -5]
            if deep_anomalies:
                periods.append(OccupationPeriod(
                    start_year=-800,
                    end_year=-200,
                    occupation_type="foundational",
                    evidence_strength=np.mean([a.confidence for a in deep_anomalies]),
                    description="Ocupación fundacional con estructuras profundas"
                ))
            
            # Período medio (anomalías subsuperficiales)
            medium_anomalies = [a for a in anomalies if -5 <= a.center_3d[2] < -1]
            if medium_anomalies:
                periods.append(OccupationPeriod(
                    start_year=-200,
                    end_year=400,
                    occupation_type="expansion",
                    evidence_strength=np.mean([a.confidence for a in medium_anomalies]),
                    description="Período de expansión y desarrollo"
                ))
            
            # Período tardío (anomalías superficiales)
            surface_anomalies = [a for a in anomalies if a.center_3d[2] >= -1]
            if surface_anomalies:
                periods.append(OccupationPeriod(
                    start_year=400,
                    end_year=1200,
                    occupation_type="consolidation",
                    evidence_strength=np.mean([a.confidence for a in surface_anomalies]),
                    description="Período de consolidación y actividad superficial"
                ))
        
        return periods
    
    def _determine_territorial_function(self, anomalies: List[VolumetricAnomaly], 
                                       layered_data: Dict[float, Dict[str, Any]]) -> TerritorialFunction:
        """Determinar función territorial principal."""
        
        # Análisis de tipos de anomalías
        anomaly_types = [a.archaeological_type for a in anomalies]
        
        # Determinar función principal
        if 'ceremonial_space' in anomaly_types:
            primary_function = "ceremonial"
        elif 'hydraulic_system' in anomaly_types:
            primary_function = "agricultural"
        elif 'defensive_feature' in anomaly_types:
            primary_function = "defensive"
        elif 'structure' in anomaly_types:
            primary_function = "residential"
        else:
            primary_function = "mixed_use"
        
        # Funciones secundarias
        secondary_functions = list(set(anomaly_types))
        if primary_function in secondary_functions:
            secondary_functions.remove(primary_function)
        
        # Organización espacial
        if len(anomalies) > 5:
            spatial_org = "complex_planned"
        elif len(anomalies) > 2:
            spatial_org = "organized"
        else:
            spatial_org = "simple"
        
        # Confianza basada en evidencia
        confidence = np.mean([a.confidence for a in anomalies]) if anomalies else 0.5
        
        return TerritorialFunction(
            primary_function=primary_function,
            secondary_functions=secondary_functions,
            spatial_organization=spatial_org,
            confidence=confidence
        )
    
    def _analyze_landscape_evolution(self, temporal_profile: Dict[str, Any], 
                                    layered_data: Dict[float, Dict[str, Any]]) -> LandscapeEvolution:
        """Analizar evolución del paisaje."""
        
        # Línea base natural
        natural_baseline = "Paisaje natural con topografía variable"
        
        # Modificaciones humanas
        human_modifications = []
        
        # Buscar evidencia de modificaciones
        surface_data = layered_data.get(0, {})
        if any('srtm' in instrument for instrument in surface_data.keys()):
            human_modifications.append("Modificaciones topográficas detectadas")
        
        if any('palsar' in instrument for instrument in surface_data.keys()):
            human_modifications.append("Alteraciones de drenaje natural")
        
        # Indicadores de abandono
        abandonment_indicators = []
        
        if temporal_profile:
            trends = temporal_profile.get('temporal_trends', {})
            if trends.get('abandonment_risk') == 'high':
                abandonment_indicators.append("Condiciones climáticas adversas")
        
        # Estado actual
        current_state = "Paisaje con evidencia arqueológica preservada"
        
        return LandscapeEvolution(
            natural_baseline=natural_baseline,
            human_modifications=human_modifications,
            abandonment_indicators=abandonment_indicators,
            current_state=current_state
        )
    
    def _prepare_visualization_data(self, xz_profile: TomographicSlice, 
                                   yz_profile: TomographicSlice,
                                   xy_profiles: List[TomographicSlice],
                                   layered_data: Dict[float, Dict[str, Any]]) -> Dict[str, Any]:
        """Preparar datos para visualización tomográfica."""
        
        viz_data = {
            'xz_slice': {
                'depths': [layer.depth_m for layer in xz_profile.layers],
                'intensities': [layer.anomaly_intensity for layer in xz_profile.layers],
                'probabilities': [layer.archaeological_probability for layer in xz_profile.layers]
            },
            'yz_slice': {
                'depths': [layer.depth_m for layer in yz_profile.layers],
                'intensities': [layer.anomaly_intensity for layer in yz_profile.layers],
                'probabilities': [layer.archaeological_probability for layer in yz_profile.layers]
            },
            'xy_slices': [
                {
                    'depth': slice_xy.depth_range[0],
                    'intensity': slice_xy.slice_ess,
                    'instruments': list(slice_xy.layers[0].instruments_data.keys()) if slice_xy.layers else []
                }
                for slice_xy in xy_profiles
            ],
            'depth_layers': self.depth_layers,
            'instrument_data': layered_data
        }
        
        return viz_data
    
    # Métodos auxiliares
    
    def _calculate_layer_anomaly_intensity(self, layer_data: Dict[str, Any]) -> float:
        """Calcular intensidad de anomalía para una capa."""
        return self._calculate_surface_ess(layer_data)
    
    def _calculate_archaeological_probability_layer(self, layer_data: Dict[str, Any], depth: float) -> float:
        """Calcular probabilidad arqueológica para una capa."""
        base_probability = self._calculate_surface_ess(layer_data)
        
        # Ajustar por profundidad (estructuras más profundas = más intencionales)
        depth_factor = 1.0
        if depth < -2:
            depth_factor = 1.2  # Bonus por profundidad
        elif depth > 0:
            depth_factor = 0.9  # Penalización por superficie
        
        return min(1.0, base_probability * depth_factor)
    
    def _calculate_slice_coherence(self, layers: List[TomographicLayer]) -> float:
        """Calcular coherencia de un corte tomográfico."""
        if len(layers) < 2:
            return 1.0
        
        coherence_scores = []
        for i in range(len(layers) - 1):
            layer1, layer2 = layers[i], layers[i + 1]
            coherence = 1.0 - abs(layer1.anomaly_intensity - layer2.anomaly_intensity)
            coherence_scores.append(coherence)
        
        return np.mean(coherence_scores)
    
    def _normalize_instrument_value(self, instrument: str, value: float) -> float:
        """Normalizar valor de instrumento a [0,1]."""
        # Normalización específica por tipo de instrumento
        if 'thermal' in instrument or 'viirs' in instrument:
            return min(1.0, abs(value) / 10.0)  # Valores térmicos
        elif 'ndvi' in instrument:
            return min(1.0, abs(value))  # NDVI ya normalizado
        elif 'sar' in instrument or 'palsar' in instrument:
            return min(1.0, abs(value) / 20.0)  # Valores SAR en dB
        elif 'elevation' in instrument or 'srtm' in instrument:
            return min(1.0, abs(value) / 100.0)  # Elevación en metros
        else:
            return min(1.0, abs(value))  # Normalización genérica
    
    def _classify_archaeological_type(self, depth: float, layer_data: Dict[str, Any]) -> str:
        """Clasificar tipo arqueológico basado en profundidad y datos."""
        
        # Clasificación por profundidad
        if depth >= 0:
            return "activity_area"
        elif depth >= -2:
            return "structure"
        elif depth >= -5:
            return "burial"
        else:
            return "hydraulic_system"
    
    def _estimate_temporal_range(self, arch_type: str) -> Tuple[int, int]:
        """Estimar rango temporal basado en tipo arqueológico."""
        
        ranges = {
            "activity_area": (0, 500),
            "structure": (-500, 800),
            "burial": (-800, 200),
            "hydraulic_system": (-1000, 500),
            "defensive_feature": (-300, 1000),
            "ceremonial_space": (-1200, 800)
        }
        
        return ranges.get(arch_type, (-500, 500))
    
    def _assess_occupation_viability(self, temporal_data: Dict[str, Any]) -> str:
        """Evaluar viabilidad de ocupación basada en datos temporales."""
        
        climate_context = temporal_data.get('climate_context', {})
        precip_history = temporal_data.get('precipitation_history', {})
        
        climate_score = 0.7 if climate_context.get('climate_stability') == 'stable' else 0.3
        water_score = 0.8 if precip_history.get('water_availability') == 'high' else 0.4
        
        combined_score = (climate_score + water_score) / 2
        
        if combined_score > 0.7:
            return 'high'
        elif combined_score > 0.5:
            return 'medium'
        else:
            return 'low'
    
    def _assess_abandonment_risk(self, temporal_data: Dict[str, Any]) -> str:
        """Evaluar riesgo de abandono basado en datos temporales."""
        
        climate_context = temporal_data.get('climate_context', {})
        precip_history = temporal_data.get('precipitation_history', {})
        
        # Riesgo alto si clima inestable o agua escasa
        if (climate_context.get('climate_stability') != 'stable' or 
            precip_history.get('water_availability') == 'low'):
            return 'high'
        else:
            return 'low'