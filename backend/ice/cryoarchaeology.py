#!/usr/bin/env python3
"""
ArcheoScope CryoArchaeology Module - CryoScope
Instrumentos especializados para arqueología en ambientes de hielo y permafrost
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

from .ice_detector import IceContext, IceEnvironmentType, SeasonalPhase

logger = logging.getLogger(__name__)

class CryoInstrument(Enum):
    """Instrumentos especializados para ambientes de hielo"""
    ICESAT2_ATL06 = "icesat2_atl06"                    # Perfiles de elevación sobre hielo
    ICESAT2_ATL08 = "icesat2_atl08"                    # Detección de depresiones y densidad
    IRIS_SEISMIC = "iris_seismic"                      # Cavidades y resonancias bajo hielo
    SENTINEL1_SAR = "sentinel1_sar"                    # Fracturas en hielo, coherencia superficial
    PALSAR_L_BAND = "palsar_l_band"                    # Penetración en hielo fino y vegetación
    MODIS_THERMAL = "modis_thermal"                    # Contexto térmico y cambios estacionales
    LANDSAT_MULTISPECTRAL = "landsat_multispectral"   # Análisis de superficie y nieve
    SENTINEL2_OPTICAL = "sentinel2_optical"            # Contexto óptico de alta resolución
    SMOS_SOIL_MOISTURE = "smos_soil_moisture"          # Humedad y densidad del hielo
    SMAP_PERMAFROST = "smap_permafrost"                # Caracterización de permafrost
    GPR_ICE_PENETRATING = "gpr_ice_penetrating"        # Radar penetrante de hielo
    THERMAL_IMAGING = "thermal_imaging"                # Imágenes térmicas de alta resolución

@dataclass
class CryoAnomalySignature:
    """Firma de anomalía en ambiente de hielo"""
    # Características de elevación
    elevation_depression_m: float
    surface_roughness: float
    ice_thickness_variation_m: float
    
    # Características térmicas
    thermal_anomaly_c: float
    seasonal_thermal_pattern: str
    melt_pattern_anomaly: float
    
    # Características estructurales
    subsurface_cavity_volume_m3: float
    ice_density_anomaly: float
    fracture_pattern_coherence: float
    
    # Características temporales
    seasonal_persistence: float
    multi_year_stability: float
    melt_freeze_cycle_anomaly: float
    
    # Metadatos de confianza
    detection_confidence: float
    instrument_convergence: float
    temporal_consistency: float

@dataclass
class CryoArchaeologicalCandidate:
    """Candidato arqueológico en ambiente de hielo"""
    anomaly_id: str
    coordinates: Tuple[float, float]
    signature: CryoAnomalySignature
    
    # Clasificación arqueológica
    site_type_probability: Dict[str, float]  # "shelter", "cache", "settlement", etc.
    cultural_period: Optional[str]           # "paleolithic", "historic", "modern"
    preservation_state: str                  # "frozen", "partially_thawed", "degraded"
    
    # Validación
    archaeological_priority: str             # "high", "medium", "low"
    recommended_investigation: List[str]     # Métodos recomendados
    seasonal_accessibility: Dict[str, str]  # Accesibilidad por estación
    risk_assessment: Dict[str, str]         # Riesgos y consideraciones

class CryoArchaeologyEngine:
    """
    Motor de crioarqueología para ArcheoScope
    
    Adapta la metodología ArcheoScope para detección de sitios arqueológicos
    en ambientes de hielo, glaciares y permafrost
    """
    
    def __init__(self):
        self.instrument_config = self._initialize_instruments()
        self.ice_site_database = self._load_ice_site_database()
        self.cultural_signatures = self._load_cultural_signatures()
        
        logger.info("CryoArchaeologyEngine inicializado con instrumentos crioarqueológicos")
    
    def analyze_cryo_area(self, ice_context: IceContext, 
                         bounds: Tuple[float, float, float, float]) -> Dict[str, Any]:
        """
        Análisis crioarqueológico completo
        
        Args:
            ice_context: Contexto del ambiente de hielo
            bounds: Límites del área (lat_min, lat_max, lon_min, lon_max)
            
        Returns:
            Resultados del análisis crioarqueológico
        """
        try:
            logger.info(f"❄️ Iniciando análisis crioarqueológico")
            logger.info(f"   Tipo de hielo: {ice_context.ice_type.value if ice_context.ice_type else 'unknown'}")
            logger.info(f"   Espesor estimado: {ice_context.estimated_thickness_m}m")
            logger.info(f"   Potencial arqueológico: {ice_context.archaeological_potential}")
            logger.info(f"   Fase estacional: {ice_context.seasonal_phase.value if ice_context.seasonal_phase else 'unknown'}")
            
            # 1. Seleccionar instrumentos según contexto de hielo
            selected_instruments = self._select_instruments_for_ice_context(ice_context)
            
            # 2. Generar datos sintéticos de instrumentos crioarqueológicos
            instrument_data = self._generate_cryo_sensor_data(ice_context, bounds, selected_instruments)
            
            # 3. Detectar anomalías de elevación (ICESat-2)
            elevation_anomalies = self._detect_elevation_anomalies(instrument_data)
            
            # 4. Confirmar anomalías sub-superficiales (IRIS Seismic)
            subsurface_confirmation = self._analyze_subsurface_features(instrument_data, elevation_anomalies)
            
            # 5. Análisis temporal y estacional
            temporal_analysis = self._perform_temporal_seasonal_analysis(instrument_data, ice_context)
            
            # 6. Integración multi-sensor
            integrated_anomalies = self._integrate_multi_sensor_data(
                elevation_anomalies, subsurface_confirmation, temporal_analysis
            )
            
            # 7. Clasificar candidatos crioarqueológicos
            cryo_candidates = self._classify_cryo_candidates(
                integrated_anomalies, ice_context, temporal_analysis
            )
            
            # 8. Generar plan de investigación estacional
            investigation_plan = self._generate_seasonal_investigation_plan(cryo_candidates, ice_context)
            
            results = {
                "analysis_type": "cryoarchaeology",
                "ice_context": {
                    "ice_type": ice_context.ice_type.value if ice_context.ice_type else None,
                    "estimated_thickness_m": ice_context.estimated_thickness_m,
                    "surface_temperature_c": ice_context.surface_temperature_c,
                    "seasonal_phase": ice_context.seasonal_phase.value if ice_context.seasonal_phase else None,
                    "archaeological_potential": ice_context.archaeological_potential,
                    "preservation_quality": ice_context.preservation_quality,
                    "accessibility": ice_context.accessibility,
                    "historical_activity": ice_context.historical_activity
                },
                "instruments_used": [instr.value for instr in selected_instruments],
                "elevation_anomalies": len(elevation_anomalies),
                "subsurface_confirmations": len(subsurface_confirmation),
                "cryo_candidates": [
                    {
                        "anomaly_id": candidate.anomaly_id,
                        "coordinates": candidate.coordinates,
                        "signature": {
                            "elevation_depression_m": candidate.signature.elevation_depression_m,
                            "thermal_anomaly_c": candidate.signature.thermal_anomaly_c,
                            "subsurface_cavity_volume_m3": candidate.signature.subsurface_cavity_volume_m3,
                            "seasonal_persistence": candidate.signature.seasonal_persistence,
                            "detection_confidence": candidate.signature.detection_confidence
                        },
                        "site_type_probability": candidate.site_type_probability,
                        "cultural_period": candidate.cultural_period,
                        "preservation_state": candidate.preservation_state,
                        "archaeological_priority": candidate.archaeological_priority,
                        "recommended_investigation": candidate.recommended_investigation,
                        "seasonal_accessibility": candidate.seasonal_accessibility
                    }
                    for candidate in cryo_candidates
                ],
                "investigation_plan": investigation_plan,
                "temporal_analysis": temporal_analysis,
                "summary": {
                    "high_priority_targets": len([c for c in cryo_candidates if c.archaeological_priority == "high"]),
                    "total_anomalies": len(integrated_anomalies),
                    "optimal_investigation_season": investigation_plan.get("optimal_season", "unknown"),
                    "recommended_next_steps": investigation_plan.get("immediate_actions", [])
                }
            }
            
            logger.info(f"✅ Análisis crioarqueológico completado:")
            logger.info(f"   - Anomalías de elevación: {len(elevation_anomalies)}")
            logger.info(f"   - Confirmaciones sub-superficiales: {len(subsurface_confirmation)}")
            logger.info(f"   - Candidatos crioarqueológicos: {len(cryo_candidates)}")
            logger.info(f"   - Objetivos de alta prioridad: {results['summary']['high_priority_targets']}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error en análisis crioarqueológico: {e}")
            raise
    
    def _select_instruments_for_ice_context(self, ice_context: IceContext) -> List[CryoInstrument]:
        """Seleccionar instrumentos según el contexto de hielo"""
        
        instruments = []
        
        # Instrumentos base para todos los ambientes de hielo
        instruments.extend([
            CryoInstrument.ICESAT2_ATL06,
            CryoInstrument.MODIS_THERMAL,
            CryoInstrument.SENTINEL1_SAR
        ])
        
        # Instrumentos específicos según tipo de hielo
        if ice_context.ice_type == IceEnvironmentType.GLACIER:
            instruments.extend([
                CryoInstrument.ICESAT2_ATL08,
                CryoInstrument.GPR_ICE_PENETRATING,
                CryoInstrument.THERMAL_IMAGING
            ])
        
        elif ice_context.ice_type == IceEnvironmentType.PERMAFROST:
            instruments.extend([
                CryoInstrument.IRIS_SEISMIC,
                CryoInstrument.SMAP_PERMAFROST,
                CryoInstrument.SMOS_SOIL_MOISTURE
            ])
        
        elif ice_context.ice_type == IceEnvironmentType.ALPINE_ICE:
            instruments.extend([
                CryoInstrument.SENTINEL2_OPTICAL,
                CryoInstrument.LANDSAT_MULTISPECTRAL,
                CryoInstrument.THERMAL_IMAGING
            ])
        
        elif ice_context.ice_type == IceEnvironmentType.SEASONAL_SNOW:
            instruments.extend([
                CryoInstrument.PALSAR_L_BAND,
                CryoInstrument.SENTINEL2_OPTICAL
            ])
        
        # Instrumentos según espesor
        if ice_context.estimated_thickness_m:
            if ice_context.estimated_thickness_m > 100:  # Hielo espeso
                instruments.append(CryoInstrument.IRIS_SEISMIC)
            elif ice_context.estimated_thickness_m < 50:  # Hielo fino
                instruments.append(CryoInstrument.PALSAR_L_BAND)
        
        return list(set(instruments))  # Eliminar duplicados
    
    def _generate_cryo_sensor_data(self, ice_context: IceContext, 
                                  bounds: Tuple[float, float, float, float],
                                  instruments: List[CryoInstrument]) -> Dict[str, np.ndarray]:
        """Generar datos sintéticos de sensores crioarqueológicos"""
        
        lat_min, lat_max, lon_min, lon_max = bounds
        
        # Tamaño del grid basado en tipo de hielo y resolución de instrumentos
        if ice_context.ice_type in [IceEnvironmentType.ICE_SHEET, IceEnvironmentType.GLACIER]:
            grid_size = 200  # Alta resolución para glaciares
        else:
            grid_size = 150  # Resolución media para otros tipos
        
        sensor_data = {}
        
        for instrument in instruments:
            if instrument == CryoInstrument.ICESAT2_ATL06:
                # Perfiles de elevación de alta precisión
                elevation_data = self._generate_icesat2_elevation_data(ice_context, grid_size)
                sensor_data['elevation_profiles'] = elevation_data
                
            elif instrument == CryoInstrument.ICESAT2_ATL08:
                # Detección de depresiones y cambios de densidad
                density_data = self._generate_icesat2_density_data(ice_context, grid_size)
                sensor_data['ice_density_variations'] = density_data
                
            elif instrument == CryoInstrument.IRIS_SEISMIC:
                # Datos sísmicos para cavidades sub-superficiales
                seismic_data = self._generate_seismic_data(ice_context, grid_size)
                sensor_data['seismic_resonance'] = seismic_data
                
            elif instrument == CryoInstrument.SENTINEL1_SAR:
                # Coherencia SAR y fracturas en hielo
                sar_coherence = self._generate_sar_coherence_data(ice_context, grid_size)
                sensor_data['sar_coherence'] = sar_coherence
                
            elif instrument == CryoInstrument.PALSAR_L_BAND:
                # Penetración en hielo fino
                penetration_data = self._generate_palsar_penetration_data(ice_context, grid_size)
                sensor_data['ice_penetration'] = penetration_data
                
            elif instrument == CryoInstrument.MODIS_THERMAL:
                # Datos térmicos y cambios estacionales
                thermal_data = self._generate_thermal_data(ice_context, grid_size)
                sensor_data['thermal_patterns'] = thermal_data
                
            elif instrument == CryoInstrument.SMOS_SOIL_MOISTURE:
                # Humedad del suelo y características del permafrost
                moisture_data = self._generate_soil_moisture_data(ice_context, grid_size)
                sensor_data['soil_moisture'] = moisture_data
        
        return sensor_data
    
    def _generate_icesat2_elevation_data(self, ice_context: IceContext, grid_size: int) -> np.ndarray:
        """Generar datos de elevación sobre hielo 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        # Elevación base según tipo de hielo
        base_elevation = 1000 if ice_context.ice_type == IceEnvironmentType.ALPINE_ICE else 100
        
        # Hash determinístico de coordenadas SIN np.random
        lat, lon = ice_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Crear superficie base DETERMINÍSTICA con variaciones naturales
        elevation = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Variación determinista basada en coordenadas y posición
                variation = ((coord_hash + i * 3 + j * 7) % int(base_elevation * 0.1)) - int(base_elevation * 0.05)
                elevation[i, j] = base_elevation + variation
        
        # Añadir características según tipo de hielo
        if ice_context.ice_type == IceEnvironmentType.GLACIER:
            # Crevasses y características glaciales
            for i in range(grid_size):
                elevation[i, :] += np.sin(i * 0.1) * 10
        
        # Añadir anomalías arqueológicas DETERMINÍSTICAMENTE (depresiones artificiales)
        num_anomalies = 1 + (coord_hash % 3)  # Siempre 1-3 para mismas coords
        for i in range(num_anomalies):
            # Posición DETERMINÍSTICA basada en hash
            position_hash = coord_hash + i * 1000
            x = 10 + (position_hash % (grid_size - 20))
            y = 10 + ((position_hash // 100) % (grid_size - 20))
            
            # Depresión circular DETERMINÍSTICA (posible refugio o estructura)
            radius_hash = coord_hash + i * 500
            radius = 5 + (radius_hash % 10)  # 5-14, sin random
            
            depth_hash = coord_hash + i * 300
            depth = 2 + (depth_hash % 8)  # 2-9, sin random
            
            for i in range(max(0, x-radius), min(grid_size, x+radius)):
                for j in range(max(0, y-radius), min(grid_size, y+radius)):
                    dist = np.sqrt((i-x)**2 + (j-y)**2)
                    if dist <= radius:
                        elevation[i, j] -= depth * (1 - dist/radius)
        
        return elevation
    
    def _generate_icesat2_density_data(self, ice_context: IceContext, grid_size: int) -> np.ndarray:
        """Generar datos de densidad de hielo 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        base_density = ice_context.ice_density_kg_m3 or 900.0
        
        # Hash determinístico SIN np.random
        lat, lon = ice_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Variaciones de densidad DETERMINÍSTICAS
        density = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Variación determinista de densidad
                variation = ((coord_hash + i * 5 + j * 11) % int(base_density * 0.04)) - int(base_density * 0.02)
                density[i, j] = base_density + variation
        
        # Añadir anomalías de densidad DETERMINÍSTICAMENTE (cavidades de aire, materiales orgánicos)
        num_anomalies = coord_hash % 3  # Siempre 0-2 para mismas coords
        for i in range(num_anomalies):
            # Posición DETERMINÍSTICA
            position_hash = coord_hash + i * 700
            x = 5 + (position_hash % (grid_size - 10))
            y = 5 + ((position_hash // 100) % (grid_size - 10))
            # Zona de menor densidad DETERMINÍSTICA
            density[x-3:x+3, y-3:y+3] *= 0.7  # 30% menos denso
        
        return density
    
    def _generate_seismic_data(self, ice_context: IceContext, grid_size: int) -> np.ndarray:
        """Generar datos sísmicos 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        # Velocidad sísmica base según tipo de hielo
        if ice_context.ice_type == IceEnvironmentType.PERMAFROST:
            base_velocity = 3500  # m/s en permafrost
        else:
            base_velocity = 3800  # m/s en hielo glacial
        
        # Hash determinístico SIN np.random
        lat, lon = ice_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Velocidad sísmica DETERMINÍSTICA
        seismic_velocity = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Variación determinista de velocidad sísmica
                variation = ((coord_hash + i * 7 + j * 13) % int(base_velocity * 0.1)) - int(base_velocity * 0.05)
                seismic_velocity[i, j] = base_velocity + variation
        
        # Añadir anomalías sísmicas DETERMINÍSTICAMENTE (cavidades, materiales diferentes)
        num_cavities = coord_hash % 2  # Siempre 0-1 para mismas coords
        for i in range(num_cavities):
            # Posición DETERMINÍSTICA
            position_hash = coord_hash + i * 900
            x = 5 + (position_hash % (grid_size - 10))
            y = 5 + ((position_hash // 100) % (grid_size - 10))
            # Cavidad (velocidad muy baja) - DETERMINÍSTICA
            seismic_velocity[x-2:x+2, y-2:y+2] = 1500  # Velocidad del aire/agua
        
        return seismic_velocity
    
    def _generate_sar_coherence_data(self, ice_context: IceContext, grid_size: int) -> np.ndarray:
        """Generar datos de coherencia SAR 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        # Coherencia base según estabilidad del hielo
        if ice_context.seasonal_phase == SeasonalPhase.WINTER_ACCUMULATION:
            base_coherence = 0.8  # Alta coherencia en invierno
        else:
            base_coherence = 0.6  # Menor coherencia durante deshielo
        
        # Hash determinístico SIN np.random
        lat, lon = ice_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Coherencia DETERMINÍSTICA
        coherence = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Variación determinista de coherencia
                variation = ((coord_hash + i * 9 + j * 17) % 20) / 100.0 - 0.1  # -0.1 a 0.1
                coherence[i, j] = max(0.0, min(1.0, base_coherence + variation))
        
        # Añadir fracturas y características estructurales DETERMINÍSTICAMENTE
        num_fractures = 1 + (coord_hash % 2)  # Siempre 1-2 para mismas coords
        for i in range(num_fractures):
            # Fractura lineal DETERMINÍSTICA
            position_hash = coord_hash + i * 1100
            start_x = (position_hash % grid_size)
            start_y = ((position_hash // 100) % grid_size)
            end_hash = position_hash + 500
            end_x = (end_hash % grid_size)
            end_y = ((end_hash // 100) % grid_size)
            
            # Crear línea de baja coherencia
            steps = max(abs(end_x - start_x), abs(end_y - start_y))
            if steps > 0:
                x_step = (end_x - start_x) / steps
                y_step = (end_y - start_y) / steps
                
                for i in range(steps):
                    x = int(start_x + i * x_step)
                    y = int(start_y + i * y_step)
                    if 0 <= x < grid_size and 0 <= y < grid_size:
                        coherence[x, y] *= 0.3  # Baja coherencia en fractura
        
        return coherence
    
    def _generate_palsar_penetration_data(self, ice_context: IceContext, grid_size: int) -> np.ndarray:
        """Generar datos de penetración PALSAR 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        # Penetración base según espesor de hielo
        max_penetration = min(50, ice_context.estimated_thickness_m or 10)
        
        # Hash determinístico SIN np.random
        lat, lon = ice_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Penetración DETERMINÍSTICA
        penetration = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Factor de penetración determinista 0.5-1.0
                factor = 0.5 + ((coord_hash + i * 11 + j * 19) % 50) / 100.0
                penetration[i, j] = factor * max_penetration
        
        # Áreas con menor penetración DETERMINÍSTICAMENTE (objetos enterrados)
        num_objects = coord_hash % 2  # Siempre 0-1 para mismas coords
        for i in range(num_objects):
            # Posición DETERMINÍSTICA
            position_hash = coord_hash + i * 1300
            x = 5 + (position_hash % (grid_size - 10))
            y = 5 + ((position_hash // 100) % (grid_size - 10))
            # Objeto que bloquea penetración - DETERMINÍSTICO
            penetration[x-2:x+2, y-2:y+2] *= 0.2
        
        return penetration
    
    def _generate_thermal_data(self, ice_context: IceContext, grid_size: int) -> np.ndarray:
        """Generar datos térmicos 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        base_temp = ice_context.surface_temperature_c or -10.0
        
        # Hash determinístico SIN np.random
        lat, lon = ice_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Variaciones térmicas naturales DETERMINÍSTICAS
        thermal = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Variación determinista de temperatura (±2.0°C)
                variation = ((coord_hash + i * 13 + j * 23) % 40) / 10.0 - 2.0  # -2.0 a 2.0
                thermal[i, j] = base_temp + variation
        
        # Anomalías térmicas DETERMINÍSTICAMENTE (refugios, actividad geotérmica)
        num_anomalies = coord_hash % 2  # Siempre 0-1 para mismas coords
        for i in range(num_anomalies):
            # Posición DETERMINÍSTICA
            position_hash = coord_hash + i * 1500
            x = 5 + (position_hash % (grid_size - 10))
            y = 5 + ((position_hash // 100) % (grid_size - 10))
            # Anomalía cálida DETERMINÍSTICA
            anomaly_hash = coord_hash + i * 700
            thermal_increase = 2 + (anomaly_hash % 6)  # 2-7°C, sin random
            thermal[x-3:x+3, y-3:y+3] += thermal_increase
        
        return thermal
    
    def _generate_soil_moisture_data(self, ice_context: IceContext, grid_size: int) -> np.ndarray:
        """Generar datos de humedad del suelo 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        # Humedad base según tipo de permafrost
        if ice_context.ice_type == IceEnvironmentType.PERMAFROST:
            base_moisture = 0.3  # 30% humedad en permafrost
        else:
            base_moisture = 0.1  # Baja humedad en hielo
        
        # Hash determinístico SIN np.random
        lat, lon = ice_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Humedad DETERMINÍSTICA
        moisture = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Variación determinista de humedad ±0.05
                variation = ((coord_hash + i * 17 + j * 29) % 10) / 100.0 - 0.05  # -0.05 a 0.05
                moisture[i, j] = max(0.0, min(1.0, base_moisture + variation))
        
        return moisture
    
    def _detect_elevation_anomalies(self, sensor_data: Dict[str, np.ndarray]) -> List[Dict[str, Any]]:
        """Detectar anomalías de elevación usando ICESat-2"""
        
        anomalies = []
        
        if 'elevation_profiles' in sensor_data:
            elevation = sensor_data['elevation_profiles']
            
            # Detectar depresiones significativas
            mean_elevation = np.mean(elevation)
            std_elevation = np.std(elevation)
            
            # Buscar áreas significativamente más bajas
            depression_mask = elevation < (mean_elevation - 2 * std_elevation)
            
            # Encontrar regiones conectadas (implementación simplificada)
            depression_positions = np.where(depression_mask)
            
            if len(depression_positions[0]) > 0:
                # Agrupar píxeles cercanos en regiones
                regions = []
                processed = set()
                
                for i in range(len(depression_positions[0])):
                    pos = (depression_positions[0][i], depression_positions[1][i])
                    if pos not in processed:
                        # Crear nueva región
                        region_pixels = [pos]
                        processed.add(pos)
                        
                        # Buscar píxeles conectados
                        for j in range(i+1, len(depression_positions[0])):
                            other_pos = (depression_positions[0][j], depression_positions[1][j])
                            if other_pos not in processed:
                                # Verificar si está cerca
                                dist = np.sqrt((pos[0] - other_pos[0])**2 + (pos[1] - other_pos[1])**2)
                                if dist < 8:  # Radio de conexión
                                    region_pixels.append(other_pos)
                                    processed.add(other_pos)
                        
                        if len(region_pixels) > 15:  # Mínimo 15 píxeles
                            regions.append(region_pixels)
                
                # Procesar regiones encontradas
                for i, region_pixels in enumerate(regions, 1):
                    coords_y = [p[0] for p in region_pixels]
                    coords_x = [p[1] for p in region_pixels]
                    
                    center_y, center_x = np.mean(coords_y), np.mean(coords_x)
                    
                    # Calcular propiedades de la depresión
                    region_elevations = [elevation[p[0], p[1]] for p in region_pixels]
                    depression_depth = mean_elevation - np.mean(region_elevations)
                    
                    # Estimar dimensiones
                    length = (max(coords_y) - min(coords_y)) * 10  # Conversión a metros
                    width = (max(coords_x) - min(coords_x)) * 10
                    
                    anomaly = {
                        'id': f'elevation_anomaly_{i}',
                        'center_coordinates': (float(center_y), float(center_x)),
                        'depression_depth_m': float(depression_depth),
                        'dimensions': {
                            'length_m': float(length),
                            'width_m': float(width)
                        },
                        'area_pixels': len(region_pixels),
                        'confidence': min(1.0, depression_depth / std_elevation) if std_elevation > 0 else 0.5
                    }
                    
                    anomalies.append(anomaly)
        
        return anomalies
    
    def _analyze_subsurface_features(self, sensor_data: Dict[str, np.ndarray], 
                                   elevation_anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analizar características sub-superficiales usando datos sísmicos"""
        
        confirmations = []
        
        if 'seismic_resonance' in sensor_data and elevation_anomalies:
            seismic_data = sensor_data['seismic_resonance']
            
            for anomaly in elevation_anomalies:
                center_y, center_x = anomaly['center_coordinates']
                center_y, center_x = int(center_y), int(center_x)
                
                # Extraer datos sísmicos en la región de la anomalía
                region_size = 5
                y_start = max(0, center_y - region_size)
                y_end = min(seismic_data.shape[0], center_y + region_size)
                x_start = max(0, center_x - region_size)
                x_end = min(seismic_data.shape[1], center_x + region_size)
                
                region_seismic = seismic_data[y_start:y_end, x_start:x_end]
                
                # Detectar cavidades (velocidades sísmicas muy bajas)
                mean_velocity = np.mean(seismic_data)
                region_mean = np.mean(region_seismic)
                
                if region_mean < mean_velocity * 0.7:  # 30% menor velocidad
                    # Posible cavidad sub-superficial
                    cavity_volume = anomaly['area_pixels'] * anomaly['depression_depth_m']
                    
                    confirmation = {
                        'anomaly_id': anomaly['id'],
                        'subsurface_confirmed': True,
                        'cavity_type': 'void_space',
                        'estimated_volume_m3': cavity_volume,
                        'seismic_velocity_ratio': region_mean / mean_velocity,
                        'confidence': anomaly['confidence'] * 0.8  # Reducir confianza ligeramente
                    }
                    
                    confirmations.append(confirmation)
        
        return confirmations
    
    def _perform_temporal_seasonal_analysis(self, sensor_data: Dict[str, np.ndarray], 
                                          ice_context: IceContext) -> Dict[str, Any]:
        """Realizar análisis temporal y estacional"""
        
        analysis = {
            'current_season': ice_context.seasonal_phase.value if ice_context.seasonal_phase else 'unknown',
            'thermal_stability': 'stable',
            'seasonal_accessibility': {},
            'melt_freeze_patterns': {},
            'multi_year_persistence': 0.8  # Simulado
        }
        
        # Análisis de accesibilidad estacional
        if ice_context.ice_type == IceEnvironmentType.ALPINE_ICE:
            analysis['seasonal_accessibility'] = {
                'winter': 'difficult',
                'spring': 'moderate',
                'summer': 'accessible',
                'autumn': 'moderate'
            }
        elif ice_context.ice_type == IceEnvironmentType.PERMAFROST:
            analysis['seasonal_accessibility'] = {
                'winter': 'accessible',
                'spring': 'difficult',  # Deshielo
                'summer': 'accessible',
                'autumn': 'moderate'
            }
        else:
            analysis['seasonal_accessibility'] = {
                'winter': 'extreme',
                'spring': 'difficult',
                'summer': 'difficult',
                'autumn': 'difficult'
            }
        
        # Patrones de deshielo/congelación
        if 'thermal_patterns' in sensor_data:
            thermal_data = sensor_data['thermal_patterns']
            analysis['melt_freeze_patterns'] = {
                'thermal_range_c': float(np.max(thermal_data) - np.min(thermal_data)),
                'mean_temperature_c': float(np.mean(thermal_data)),
                'thermal_anomalies': int(np.sum(thermal_data > np.mean(thermal_data) + 2*np.std(thermal_data)))
            }
        
        return analysis
    
    def _integrate_multi_sensor_data(self, elevation_anomalies: List[Dict[str, Any]], 
                                   subsurface_confirmations: List[Dict[str, Any]],
                                   temporal_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Integrar datos de múltiples sensores"""
        
        integrated_anomalies = []
        
        # Combinar anomalías de elevación con confirmaciones sub-superficiales
        for elevation_anomaly in elevation_anomalies:
            # Buscar confirmación sub-superficial correspondiente
            subsurface_match = None
            for confirmation in subsurface_confirmations:
                if confirmation['anomaly_id'] == elevation_anomaly['id']:
                    subsurface_match = confirmation
                    break
            
            # Crear anomalía integrada
            integrated_anomaly = {
                'id': elevation_anomaly['id'],
                'coordinates': elevation_anomaly['center_coordinates'],
                'elevation_data': elevation_anomaly,
                'subsurface_data': subsurface_match,
                'temporal_data': temporal_analysis,
                'integrated_confidence': elevation_anomaly['confidence']
            }
            
            # Aumentar confianza si hay confirmación sub-superficial
            if subsurface_match:
                integrated_anomaly['integrated_confidence'] *= 1.3
                integrated_anomaly['integrated_confidence'] = min(1.0, integrated_anomaly['integrated_confidence'])
            
            integrated_anomalies.append(integrated_anomaly)
        
        return integrated_anomalies
    
    def _classify_cryo_candidates(self, integrated_anomalies: List[Dict[str, Any]], 
                                ice_context: IceContext,
                                temporal_analysis: Dict[str, Any]) -> List[CryoArchaeologicalCandidate]:
        """Clasificar candidatos crioarqueológicos"""
        
        candidates = []
        
        for anomaly in integrated_anomalies:
            # Crear firma crioarqueológica
            elevation_data = anomaly['elevation_data']
            subsurface_data = anomaly.get('subsurface_data')
            
            signature = CryoAnomalySignature(
                elevation_depression_m=elevation_data['depression_depth_m'],
                surface_roughness=0.5,  # Simulado
                ice_thickness_variation_m=elevation_data['depression_depth_m'] * 0.5,
                thermal_anomaly_c=temporal_analysis['melt_freeze_patterns'].get('thermal_range_c', 5.0),
                seasonal_thermal_pattern='stable',
                melt_pattern_anomaly=0.3,
                subsurface_cavity_volume_m3=subsurface_data['estimated_volume_m3'] if subsurface_data else 0,
                ice_density_anomaly=0.1,
                fracture_pattern_coherence=0.7,
                seasonal_persistence=temporal_analysis['multi_year_persistence'],
                multi_year_stability=0.8,
                melt_freeze_cycle_anomaly=0.2,
                detection_confidence=anomaly['integrated_confidence'],
                instrument_convergence=0.8 if subsurface_data else 0.6,
                temporal_consistency=0.7
            )
            
            # Clasificar tipo de sitio
            site_type_prob = self._classify_site_type(signature, ice_context)
            
            # Determinar período cultural
            cultural_period = self._estimate_cultural_period(signature, ice_context)
            
            # Evaluar estado de preservación
            preservation_state = self._assess_cryo_preservation_state(signature, ice_context)
            
            # Calcular prioridad arqueológica
            archaeological_priority = self._calculate_cryo_priority(signature, ice_context)
            
            # Generar recomendaciones de investigación
            recommended_investigation = self._recommend_cryo_investigation_methods(signature, ice_context)
            
            # Evaluar accesibilidad estacional
            seasonal_accessibility = temporal_analysis['seasonal_accessibility']
            
            # Evaluación de riesgos
            risk_assessment = self._assess_cryo_investigation_risks(signature, ice_context)
            
            candidate = CryoArchaeologicalCandidate(
                anomaly_id=anomaly['id'],
                coordinates=anomaly['coordinates'],
                signature=signature,
                site_type_probability=site_type_prob,
                cultural_period=cultural_period,
                preservation_state=preservation_state,
                archaeological_priority=archaeological_priority,
                recommended_investigation=recommended_investigation,
                seasonal_accessibility=seasonal_accessibility,
                risk_assessment=risk_assessment
            )
            
            candidates.append(candidate)
        
        return candidates
    
    def _classify_site_type(self, signature: CryoAnomalySignature, ice_context: IceContext) -> Dict[str, float]:
        """Clasificar tipo de sitio arqueológico"""
        
        probabilities = {}
        
        # Basado en tamaño y características de la depresión
        if signature.elevation_depression_m > 5:  # Depresión grande
            if ice_context.ice_type == IceEnvironmentType.ALPINE_ICE:
                probabilities['mountain_shelter'] = 0.6
                probabilities['seasonal_camp'] = 0.3
                probabilities['cache_site'] = 0.1
            elif ice_context.ice_type == IceEnvironmentType.PERMAFROST:
                probabilities['winter_dwelling'] = 0.5
                probabilities['storage_pit'] = 0.3
                probabilities['ceremonial_site'] = 0.2
        
        elif 2 < signature.elevation_depression_m <= 5:  # Depresión media
            probabilities['temporary_shelter'] = 0.4
            probabilities['cache_site'] = 0.4
            probabilities['hearth_area'] = 0.2
        
        else:  # Depresión pequeña
            probabilities['cache_site'] = 0.5
            probabilities['hearth_area'] = 0.3
            probabilities['tool_cache'] = 0.2
        
        # Ajustar según cavidad sub-superficial
        if signature.subsurface_cavity_volume_m3 > 50:
            # Cavidad grande sugiere refugio o almacenamiento
            if 'mountain_shelter' in probabilities:
                probabilities['mountain_shelter'] *= 1.5
            if 'winter_dwelling' in probabilities:
                probabilities['winter_dwelling'] *= 1.5
        
        # Normalizar probabilidades
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {k: v/total for k, v in probabilities.items()}
        
        return probabilities
    
    def _estimate_cultural_period(self, signature: CryoAnomalySignature, ice_context: IceContext) -> Optional[str]:
        """Estimar período cultural"""
        
        # Basado en ubicación y características
        if ice_context.historical_activity:
            if ice_context.coordinates[0] >= 60:  # Latitudes árticas
                return "historic_arctic"  # Inuit, pueblos árticos históricos
            else:
                return "historic_alpine"  # Actividad histórica en montañas
        
        # Sin actividad histórica conocida
        if signature.seasonal_persistence > 0.8:
            return "prehistoric"  # Sitio muy persistente, posiblemente antiguo
        else:
            return "recent"  # Sitio menos persistente
    
    def _assess_cryo_preservation_state(self, signature: CryoAnomalySignature, ice_context: IceContext) -> str:
        """Evaluar estado de preservación en ambiente de hielo"""
        
        # El hielo generalmente preserva muy bien
        if ice_context.ice_type == IceEnvironmentType.PERMAFROST:
            return "frozen"  # Preservación excepcional en permafrost
        
        elif ice_context.ice_type in [IceEnvironmentType.GLACIER, IceEnvironmentType.ICE_SHEET]:
            if signature.multi_year_stability > 0.7:
                return "frozen"
            else:
                return "partially_thawed"
        
        elif ice_context.ice_type == IceEnvironmentType.SEASONAL_SNOW:
            return "partially_thawed"  # Ciclos de congelación/deshielo
        
        else:
            return "degraded"
    
    def _calculate_cryo_priority(self, signature: CryoAnomalySignature, ice_context: IceContext) -> str:
        """Calcular prioridad arqueológica crioarqueológica"""
        
        score = 0
        
        # Tamaño significativo
        if signature.elevation_depression_m > 5:
            score += 3
        elif signature.elevation_depression_m > 2:
            score += 2
        else:
            score += 1
        
        # Alta confianza en detección
        if signature.detection_confidence > 0.8:
            score += 3
        elif signature.detection_confidence > 0.6:
            score += 2
        else:
            score += 1
        
        # Confirmación sub-superficial
        if signature.subsurface_cavity_volume_m3 > 0:
            score += 2
        
        # Buena preservación
        if ice_context.preservation_quality == "excellent":
            score += 2
        elif ice_context.preservation_quality == "good":
            score += 1
        
        # Actividad histórica conocida
        if ice_context.historical_activity:
            score += 2
        
        # Accesibilidad
        if ice_context.accessibility == "accessible":
            score += 1
        
        if score >= 8:
            return "high"
        elif score >= 5:
            return "medium"
        else:
            return "low"
    
    def _recommend_cryo_investigation_methods(self, signature: CryoAnomalySignature, ice_context: IceContext) -> List[str]:
        """Recomendar métodos de investigación crioarqueológica"""
        
        methods = []
        
        # Métodos base
        methods.append("high_resolution_gpr_survey")
        methods.append("thermal_imaging_analysis")
        
        # Según tipo de hielo
        if ice_context.ice_type == IceEnvironmentType.PERMAFROST:
            methods.extend(["permafrost_coring", "geochemical_analysis"])
        
        elif ice_context.ice_type in [IceEnvironmentType.GLACIER, IceEnvironmentType.ALPINE_ICE]:
            methods.extend(["ice_core_sampling", "photogrammetric_mapping"])
        
        # Según tamaño de anomalía
        if signature.elevation_depression_m > 5:
            methods.append("systematic_archaeological_excavation")
        
        # Según cavidad sub-superficial
        if signature.subsurface_cavity_volume_m3 > 20:
            methods.extend(["cavity_exploration", "3d_subsurface_mapping"])
        
        # Según accesibilidad
        if ice_context.accessibility == "accessible":
            methods.append("field_survey_and_sampling")
        else:
            methods.append("remote_sensing_analysis_only")
        
        return methods
    
    def _assess_cryo_investigation_risks(self, signature: CryoAnomalySignature, ice_context: IceContext) -> Dict[str, str]:
        """Evaluar riesgos de investigación crioarqueológica"""
        
        risks = {}
        
        # Riesgo climático
        if ice_context.ice_type in [IceEnvironmentType.GLACIER, IceEnvironmentType.ICE_SHEET]:
            risks['climate_risk'] = "high"
        else:
            risks['climate_risk'] = "moderate"
        
        # Riesgo de acceso
        if ice_context.accessibility == "extreme":
            risks['access_risk'] = "extreme"
        elif ice_context.accessibility == "difficult":
            risks['access_risk'] = "high"
        else:
            risks['access_risk'] = "moderate"
        
        # Riesgo de preservación
        if ice_context.seasonal_phase == SeasonalPhase.SPRING_MELT:
            risks['preservation_risk'] = "high"
        else:
            risks['preservation_risk'] = "low"
        
        # Consideraciones logísticas
        risks['logistical_complexity'] = "high"
        risks['equipment_requirements'] = "specialized_cold_weather"
        
        return risks
    
    def _generate_seasonal_investigation_plan(self, candidates: List[CryoArchaeologicalCandidate], 
                                            ice_context: IceContext) -> Dict[str, Any]:
        """Generar plan de investigación estacional"""
        
        high_priority = [c for c in candidates if c.archaeological_priority == "high"]
        
        plan = {
            "optimal_season": "summer",
            "immediate_actions": [],
            "seasonal_phases": {},
            "resource_requirements": {},
            "risk_mitigation": []
        }
        
        # Determinar estación óptima
        if ice_context.ice_type == IceEnvironmentType.PERMAFROST:
            plan["optimal_season"] = "summer"  # Acceso más fácil
        elif ice_context.ice_type == IceEnvironmentType.ALPINE_ICE:
            plan["optimal_season"] = "late_summer"  # Menos nieve
        else:
            plan["optimal_season"] = "winter"  # Hielo más estable
        
        if high_priority:
            plan["immediate_actions"] = [
                "detailed_remote_sensing_analysis",
                "seasonal_accessibility_assessment",
                "specialized_equipment_procurement",
                "cold_weather_team_preparation"
            ]
            
            plan["seasonal_phases"] = {
                "winter": ["remote_sensing", "planning", "equipment_testing"],
                "spring": ["site_monitoring", "access_route_planning"],
                "summer": ["field_investigation", "excavation", "sampling"],
                "autumn": ["data_analysis", "preservation_measures"]
            }
        
        # Recursos necesarios
        plan["resource_requirements"] = {
            "team_size": len(candidates) * 2 + 3,  # Arqueólogos + apoyo
            "duration_weeks": len(candidates) * 2,
            "specialized_equipment": [
                "cold_weather_gear", "ice_penetrating_radar", 
                "thermal_imaging_camera", "permafrost_drilling_equipment"
            ],
            "logistical_support": ["helicopter_access", "base_camp", "emergency_equipment"]
        }
        
        # Mitigación de riesgos
        plan["risk_mitigation"] = [
            "weather_monitoring_system",
            "emergency_evacuation_plan",
            "specialized_cold_weather_training",
            "redundant_communication_systems"
        ]
        
        return plan
    
    def _initialize_instruments(self) -> Dict[str, Any]:
        """Inicializar configuración de instrumentos"""
        return {"initialized": True}
    
    def _load_ice_site_database(self) -> Dict[str, Any]:
        """Cargar base de datos de sitios arqueológicos en hielo"""
        return {"loaded": True}
    
    def _load_cultural_signatures(self) -> Dict[str, Any]:
        """Cargar firmas culturales para ambientes de hielo"""
        return {"loaded": True}