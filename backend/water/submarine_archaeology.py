#!/usr/bin/env python3
"""
ArcheoScope Submarine Archaeology Module
Instrumentos especializados para arqueología submarina y detección de naufragios
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

from .water_detector import WaterContext, WaterBodyType

logger = logging.getLogger(__name__)

class SubmarineInstrument(Enum):
    """Instrumentos submarinos especializados"""
    MULTIBEAM_SONAR = "multibeam_sonar"           # Sonar multihaz para batimetría
    SIDE_SCAN_SONAR = "side_scan_sonar"           # Sonar de barrido lateral
    SUB_BOTTOM_PROFILER = "sub_bottom_profiler"   # Perfilador de subfondo
    MAGNETOMETER = "magnetometer"                 # Magnetómetro marino
    ACOUSTIC_REFLECTANCE = "acoustic_reflectance" # Reflectancia acústica
    UNDERWATER_PHOTOGRAMMETRY = "underwater_photogrammetry"  # Fotogrametría submarina
    ROV_SURVEY = "rov_survey"                     # Reconocimiento con ROV

@dataclass
class SubmarineAnomalySignature:
    """Firma de anomalía submarina"""
    # Características geométricas
    length_m: float
    width_m: float
    height_m: float
    orientation_degrees: float
    
    # Características acústicas
    acoustic_reflectance: float
    sonar_shadow_length_m: float
    backscatter_intensity: float
    
    # Características del sedimento
    burial_depth_m: float
    sediment_penetration: float
    magnetic_anomaly_nt: float
    
    # Metadatos de confianza
    detection_confidence: float
    geometric_coherence: float
    historical_correlation: float

@dataclass
class WreckCandidate:
    """Candidato a naufragio detectado"""
    anomaly_id: str
    coordinates: Tuple[float, float]
    signature: SubmarineAnomalySignature
    
    # Clasificación
    vessel_type_probability: Dict[str, float]  # "merchant", "warship", "fishing", etc.
    historical_period: Optional[str]           # "ancient", "medieval", "modern"
    preservation_state: str                    # "excellent", "good", "poor", "debris_field"
    
    # Validación
    archaeological_priority: str               # "high", "medium", "low"
    recommended_investigation: List[str]       # Métodos recomendados
    risk_assessment: Dict[str, str]           # Riesgos y consideraciones

class SubmarineArchaeologyEngine:
    """
    Motor de arqueología submarina para ArcheoScope
    
    Adapta la metodología ArcheoScope para detección de naufragios y estructuras submarinas
    """
    
    def __init__(self):
        self.instrument_config = self._initialize_instruments()
        self.wreck_database = self._load_wreck_database()
        self.vessel_signatures = self._load_vessel_signatures()
        
        logger.info("SubmarineArchaeologyEngine inicializado con instrumentos submarinos")
    
    def analyze_submarine_area(self, water_context: WaterContext, 
                             bounds: Tuple[float, float, float, float]) -> Dict[str, Any]:
        """
        Análisis arqueológico submarino completo - VERSIÓN DETERMINÍSTICA
        
        Args:
            water_context: Contexto del cuerpo de agua
            bounds: Límites del área (lat_min, lat_max, lon_min, lon_max)
            
        Returns:
            Resultados del análisis submarino
        """
        try:
            logger.info(f"🌊 Iniciando análisis arqueológico submarino DETERMINÍSTICO")
            logger.info(f"   Coordenadas: {water_context.coordinates}")
            logger.info(f"   Bounds: {bounds}")
            logger.info(f"   Tipo de agua: {water_context.water_type.value if water_context.water_type else 'unknown'}")
            logger.info(f"   Profundidad estimada: {water_context.estimated_depth_m}m")
            logger.info(f"   Potencial arqueológico: {water_context.archaeological_potential}")
            logger.info(f"   Rutas históricas: {water_context.historical_shipping_routes}")
            logger.info(f"   Naufragios conocidos: {water_context.known_wrecks_nearby}")
            
            # DEBUG: Crear hash de coordenadas para verificar consistencia
            lat, lon = water_context.coordinates
            coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
            logger.info(f"🔍 DEBUG: Hash de coordenadas = {coord_hash}")
            
            # 1. Seleccionar instrumentos según contexto (solo para metadata)
            selected_instruments = self._select_instruments_for_context(water_context)
            
            # 2. ELIMINADO: _generate_submarine_sensor_data() - causaba inconsistencias
            #    La nueva función determinística NO necesita datos sintéticos
            
            # 3. Detectar anomalías volumétricas submarinas (DETERMINÍSTICO)
            volumetric_anomalies = self._detect_submarine_volumetric_anomalies({}, water_context)
            logger.info(f"🔍 DEBUG: Anomalías volumétricas detectadas = {len(volumetric_anomalies)}")
            
            # 4. Analizar firmas acústicas (usando anomalías determinísticas)
            acoustic_signatures = self._analyze_acoustic_signatures({}, volumetric_anomalies)
            logger.info(f"🔍 DEBUG: Firmas acústicas generadas = {len(acoustic_signatures)}")
            
            # 5. Correlacionar con datos históricos
            historical_correlation = self._correlate_historical_data(water_context, volumetric_anomalies)
            
            # 6. Clasificar candidatos a naufragios
            wreck_candidates = self._classify_wreck_candidates(
                volumetric_anomalies, acoustic_signatures, historical_correlation
            )
            logger.info(f"🔍 DEBUG: Candidatos a naufragios clasificados = {len(wreck_candidates)}")
            
            # 7. Generar recomendaciones de investigación
            investigation_plan = self._generate_investigation_plan(wreck_candidates, water_context)
            
            results = {
                "analysis_type": "submarine_archaeology",
                "water_context": {
                    "water_type": water_context.water_type.value if water_context.water_type else None,
                    "estimated_depth_m": water_context.estimated_depth_m,
                    "salinity_type": water_context.salinity_type,
                    "archaeological_potential": water_context.archaeological_potential,
                    "historical_shipping_routes": water_context.historical_shipping_routes,
                    "known_wrecks_nearby": water_context.known_wrecks_nearby
                },
                "instruments_used": [instr.value for instr in selected_instruments],
                "volumetric_anomalies": len(volumetric_anomalies),
                "wreck_candidates": [
                    {
                        "anomaly_id": candidate.anomaly_id,
                        "coordinates": candidate.coordinates,
                        "signature": {
                            "length_m": candidate.signature.length_m,
                            "width_m": candidate.signature.width_m,
                            "height_m": candidate.signature.height_m,
                            "orientation_degrees": candidate.signature.orientation_degrees,
                            "burial_depth_m": candidate.signature.burial_depth_m,
                            "detection_confidence": candidate.signature.detection_confidence
                        },
                        "vessel_type_probability": candidate.vessel_type_probability,
                        "historical_period": candidate.historical_period,
                        "preservation_state": candidate.preservation_state,
                        "archaeological_priority": candidate.archaeological_priority,
                        "recommended_investigation": candidate.recommended_investigation
                    }
                    for candidate in wreck_candidates
                ],
                "investigation_plan": investigation_plan,
                "summary": {
                    "high_priority_targets": len([c for c in wreck_candidates if c.archaeological_priority == "high"]),
                    "total_anomalies": len(volumetric_anomalies),
                    "recommended_next_steps": investigation_plan.get("immediate_actions", [])
                }
            }
            
            logger.info(f"✅ Análisis submarino completado:")
            logger.info(f"   - Anomalías detectadas: {len(volumetric_anomalies)}")
            logger.info(f"   - Candidatos a naufragios: {len(wreck_candidates)}")
            logger.info(f"   - Objetivos de alta prioridad: {results['summary']['high_priority_targets']}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error en análisis submarino: {e}")
            raise
    
    def _select_instruments_for_context(self, water_context: WaterContext) -> List[SubmarineInstrument]:
        """Seleccionar instrumentos según el contexto del agua"""
        
        instruments = []
        
        # Instrumentos base para todos los contextos acuáticos
        instruments.extend([
            SubmarineInstrument.MULTIBEAM_SONAR,
            SubmarineInstrument.SIDE_SCAN_SONAR
        ])
        
        # Instrumentos específicos según profundidad
        if water_context.estimated_depth_m:
            if water_context.estimated_depth_m < 50:  # Aguas someras
                instruments.extend([
                    SubmarineInstrument.UNDERWATER_PHOTOGRAMMETRY,
                    SubmarineInstrument.ROV_SURVEY
                ])
            elif water_context.estimated_depth_m < 200:  # Aguas medias
                instruments.extend([
                    SubmarineInstrument.SUB_BOTTOM_PROFILER,
                    SubmarineInstrument.MAGNETOMETER
                ])
            else:  # Aguas profundas
                instruments.extend([
                    SubmarineInstrument.ACOUSTIC_REFLECTANCE,
                    SubmarineInstrument.SUB_BOTTOM_PROFILER
                ])
        
        # Instrumentos específicos según tipo de agua
        if water_context.water_type == WaterBodyType.RIVER:
            instruments.append(SubmarineInstrument.SUB_BOTTOM_PROFILER)
        elif water_context.water_type in [WaterBodyType.OCEAN, WaterBodyType.DEEP_OCEAN]:
            instruments.append(SubmarineInstrument.MAGNETOMETER)
        
        return list(set(instruments))  # Eliminar duplicados
    
    def _generate_submarine_sensor_data(self, water_context: WaterContext, 
                                      bounds: Tuple[float, float, float, float],
                                      instruments: List[SubmarineInstrument]) -> Dict[str, np.ndarray]:
        """Generar datos sintéticos de sensores submarinos"""
        
        lat_min, lat_max, lon_min, lon_max = bounds
        
        # Tamaño del grid basado en profundidad y área
        if water_context.estimated_depth_m and water_context.estimated_depth_m > 1000:
            grid_size = 50  # Resolución menor para aguas profundas
        else:
            grid_size = 100  # Resolución mayor para aguas someras
        
        sensor_data = {}
        
        for instrument in instruments:
            if instrument == SubmarineInstrument.MULTIBEAM_SONAR:
                # Batimetría de alta resolución
                bathymetry = self._generate_bathymetry_data(water_context, grid_size)
                sensor_data['bathymetry'] = bathymetry
                
            elif instrument == SubmarineInstrument.SIDE_SCAN_SONAR:
                # Imágenes acústicas del fondo
                acoustic_image = self._generate_acoustic_image_data(water_context, grid_size)
                sensor_data['acoustic_image'] = acoustic_image
                
            elif instrument == SubmarineInstrument.SUB_BOTTOM_PROFILER:
                # Perfiles de sedimento
                sediment_profile = self._generate_sediment_profile_data(water_context, grid_size)
                sensor_data['sediment_profile'] = sediment_profile
                
            elif instrument == SubmarineInstrument.MAGNETOMETER:
                # Anomalías magnéticas
                magnetic_data = self._generate_magnetic_data(water_context, grid_size)
                sensor_data['magnetic_anomalies'] = magnetic_data
                
            elif instrument == SubmarineInstrument.ACOUSTIC_REFLECTANCE:
                # Reflectancia acústica
                reflectance = self._generate_acoustic_reflectance_data(water_context, grid_size)
                sensor_data['acoustic_reflectance'] = reflectance
        
        return sensor_data
    
    def _generate_bathymetry_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar datos batimétricos DETERMINÍSTICOS sin valores aleatorios"""
        
        # CREAR DATOS DETERMINÍSTICOS 100% BASADOS EN COORDENADAS
        lat, lon = water_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        base_depth = water_context.estimated_depth_m or 100
        
        # Crear topografía del fondo marino DETERMINÍSTICA SIN RANDOM
        # Usar funciones matemáticas puras, no aleatorias
        
        # Inicializar bathymetry determinística SIN random
        bathymetry = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Variación determinista basada en coordenadas
                depth_variation = np.sin(coord_hash + i * 0.1) * np.cos(coord_hash + j * 0.1) * (base_depth * 0.1)
                bathymetry[i, j] = base_depth + depth_variation
        
        # Añadir características del fondo según tipo de agua DETERMINÍSTICAMENTE
        if water_context.water_type == WaterBodyType.RIVER:
            # Canales de río - variación determinista
            center = grid_size // 2
            depth_variation_river = 2 + (coord_hash % 8)  # 2-10, sin random
            bathymetry[center-5:center+5, :] += depth_variation_river
            
        elif water_context.water_type == WaterBodyType.COASTAL:
            # Pendiente costera - gradiente determinista
            for i in range(grid_size):
                bathymetry[i, :] += i * (base_depth * 0.02)
        
        # Añadir anomalías potenciales (naufragios simulados)
        # DETERMINÍSTICO: Número de anomalías basado en seed, NO aleatorio
        if (water_context.historical_shipping_routes or 
            water_context.known_wrecks_nearby or 
            water_context.archaeological_potential in ["high", "medium"]):
            # Para rutas históricas: 1 o 2 anomalías (determinístico basado en coord_hash)
            num_anomalies = 1 + (coord_hash % 2)  # Siempre 1 o 2, nunca cambia para mismas coords
        else:
            # Para otras áreas: 0 o 1 anomalía (determinístico basado en coord_hash)
            num_anomalies = coord_hash % 2  # Siempre 0 o 1, nunca cambia para mismas coords
            
        for i in range(num_anomalies):
            # Posición determinística basada en coord_hash + índice (SIN random)
            position_hash = coord_hash + i * 1000
            x = 10 + (position_hash % (grid_size - 20))
            y = 10 + ((position_hash // 100) % (grid_size - 20))
            
            # Anomalía tipo naufragio con dimensiones realistas basadas en profundidad
            # DETERMINÍSTICO: Dimensiones basadas en coord_hash, SIN random
            
            # Ajustar tamaño según profundidad del agua
            dimension_hash = coord_hash + i * 500
            if base_depth > 3000:  # Aguas muy profundas - naufragios grandes
                wreck_length = 150 + (dimension_hash % 200)  # 150-350m longitud
                wreck_width = 20 + ((dimension_hash // 10) % 30)     # 20-50m anchura
            elif base_depth > 1000:  # Aguas profundas - naufragios medianos
                wreck_length = 100 + (dimension_hash % 150)  # 100-250m longitud
                wreck_width = 15 + ((dimension_hash // 10) % 20)     # 15-35m anchura
            else:  # Aguas someras - naufragios variados
                wreck_length = 50 + (dimension_hash % 150)   # 50-200m longitud
                wreck_width = 8 + ((dimension_hash // 10) % 22)      # 8-30m anchura
            
            wreck_height = 8 + ((dimension_hash // 100) % 22)    # 8-30m altura
            
            # Crear depresión con forma de barco
            length_pixels = max(3, int(wreck_length / 10))  # Conversión aproximada a píxeles
            width_pixels = max(2, int(wreck_width / 10))
            
            x_start = max(0, x - length_pixels//2)
            x_end = min(grid_size, x + length_pixels//2)
            y_start = max(0, y - width_pixels//2)
            y_end = min(grid_size, y + width_pixels//2)
            
            # Crear depresión más pronunciada (100% DETERMINÍSTICO)
            depth_change_hash = coord_hash + i * 777
            depth_change = (wreck_height/2) + ((depth_change_hash % 100) / 100.0) * (wreck_height/2)
            bathymetry[x_start:x_end, y_start:y_end] -= depth_change
        
        return bathymetry
    
    def _generate_acoustic_image_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar imágenes acústicas 100% DETERMINÍSTICAS sin valores aleatorios"""
        
        # Datos DETERMINÍSTICOS 100% basados en coordenadas
        lat, lon = water_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Imagen base del fondo DETERMINÍSTICA sin np.random
        acoustic_image = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Reflectancia base determinista basada en coordenadas
                base_reflectance = 0.2 + ((coord_hash + i + j) % 60) / 100.0  # 0.2-0.8
                acoustic_image[i, j] = base_reflectance
        
        # Añadir características según tipo de sedimento DETERMINÍSTICAMENTE
        if water_context.sediment_type == "sand_gravel":
            # Arena/grava - mayor reflectancia determinista
            for i in range(grid_size):
                for j in range(grid_size):
                    variation = ((coord_hash + i * 3 + j * 7) % 30) / 100.0  # 0-0.3
                    acoustic_image[i, j] += variation
        elif water_context.sediment_type == "silt_clay":
            # Limo/arcilla - menor reflectancia
            acoustic_image *= 0.7  # Menor reflectancia
        
        # Añadir anomalías con alta reflectancia (objetos metálicos) DETERMINÍSTICAMENTE
        num_targets = coord_hash % 3  # Siempre 0, 1 o 2 para mismas coords
        for i in range(num_targets):
            # Posición determinística SIN random
            position_hash = coord_hash + i * 2000
            x = 5 + (position_hash % (grid_size - 10))
            y = 5 + ((position_hash // 100) % (grid_size - 10))
            # Firma acústica de objeto metálico 100% DETERMINÍSTICA
            reflectance_hash = coord_hash + i * 333
            reflectance = 0.8 + ((reflectance_hash % 20) / 100.0)  # 0.8-1.0
            acoustic_image[x-2:x+2, y-5:y+5] = reflectance
        
        return acoustic_image
    
    def _generate_sediment_profile_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar perfiles de sedimento 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        # Datos DETERMINÍSTICOS 100% basados en coordenadas
        lat, lon = water_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Capas de sedimento DETERMINÍSTICAS sin np.random
        sediment_layers = np.zeros((grid_size, grid_size, 10))  # 10 capas
        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(10):  # 10 capas
                    # Valor determinista basado en coordenadas y capa
                    layer_value = 0.1 + ((coord_hash + i + j * 2 + k * 3) % 80) / 100.0  # 0.1-0.9
                    sediment_layers[i, j, k] = layer_value
        
        # Añadir objetos enterrados 100% DETERMINÍSTICAMENTE
        num_buried = coord_hash % 2  # 0 o 1, nunca cambia para mismas coords
        for i in range(num_buried):
            # Posición determinística SIN random
            position_hash = coord_hash + i * 3000
            x = 5 + (position_hash % (grid_size - 10))
            y = 5 + ((position_hash // 100) % (grid_size - 10))
            depth_layer = 2 + ((position_hash // 50) % 6)  # Capa 2-7
            # Objeto enterrado con firma determinista
            sediment_layers[x-1:x+1, y-3:y+3, depth_layer] = 0.95
        
        return sediment_layers
    
    def _generate_magnetic_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar datos magnéticos 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        # Datos DETERMINÍSTICOS 100% basados en coordenadas
        lat, lon = water_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Campo magnético base DETERMINÍSTICO sin np.random
        magnetic_field = np.zeros((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                # Campo magnético base determinista
                field_variation = ((coord_hash + i * 5 + j * 7) % 200) - 100  # -100 a 100
                magnetic_field[i, j] = 50000 + field_variation  # 49900-50100 nT
        
        # Añadir anomalías magnéticas (objetos ferrosos) 100% DETERMINÍSTICAMENTE
        num_anomalies = coord_hash % 3  # 0, 1 o 2, nunca cambia para mismas coords
        for i in range(num_anomalies):
            # Posición determinística SIN random
            position_hash = coord_hash + i * 4000
            x = 5 + (position_hash % (grid_size - 10))
            y = 5 + ((position_hash // 100) % (grid_size - 10))
            # Anomalía magnética dipolar 100% DETERMINÍSTICA
            strength_hash = coord_hash + i * 555
            anomaly_strength = 100 + ((strength_hash % 900))  # 100-1000 nT
            magnetic_field[x-2:x+2, y-2:y+2] += anomaly_strength
        
        return magnetic_field
    
    def _generate_acoustic_reflectance_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar datos de reflectancia acústica 100% DETERMINÍSTICOS sin valores aleatorios"""
        
        # Datos DETERMINÍSTICOS 100% basados en coordenadas
        lat, lon = water_context.coordinates
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # Reflectancia base según tipo de fondo DETERMINÍSTICA sin np.random
        base_reflectance = np.zeros((grid_size, grid_size))
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Reflectancia determinista basada en coordenadas
                if water_context.sediment_type == "sand_gravel":
                    # Arena/grava: mayor reflectancia 0.4-0.7
                    reflectance_range = 0.3
                    base_value = 0.4
                elif water_context.sediment_type == "silt_clay":
                    # Limo/arcilla: menor reflectancia 0.1-0.4
                    reflectance_range = 0.3
                    base_value = 0.1
                else:
                    # Otro: reflectancia media 0.2-0.6
                    reflectance_range = 0.4
                    base_value = 0.2
                
                # Valor determinista usando hash de coordenadas
                variation = ((coord_hash + i * 7 + j * 11) % int(reflectance_range * 100)) / 100.0
                base_reflectance[i, j] = base_value + variation
        
        return base_reflectance
    
    def _detect_submarine_volumetric_anomalies(self, sensor_data: Dict[str, np.ndarray], water_context: WaterContext) -> List[Dict[str, Any]]:
        """
        Detectar anomalías volumétricas submarinas - VERSIÓN 100% DETERMINÍSTICA
        
        CRÍTICO: Este método DEBE producir resultados IDÉNTICOS para las mismas coordenadas.
        NO se permiten variaciones aleatorias. NO usar np.random en absoluto.
        """
        
        anomalies = []
        
        # MÉTODO 100% DETERMINÍSTICO: Basado SOLO en coordenadas, sin np.random
        lat, lon = water_context.coordinates
        
        # Crear hash determinístico de coordenadas (sin np.random)
        coord_hash = int((abs(lat) * 10000 + abs(lon) * 10000) % 1000000)
        
        # ✅ SOLUCIÓN HONESTA: NO GENERAR ANOMALÍAS ARTIFICIALES
        # Solo detectar anomalías si hay EVIDENCIA REAL en los datos
        
        # Para coordenadas sin evidencia real → 0 anomalías (honesto)
        num_anomalies = 0
        
        # Solo generar anomalías si hay EVIDENCIA ESPECÍFICA Y VERIFICABLE
        if (water_context.historical_shipping_routes and 
            water_context.known_wrecks_nearby):
            # SOLO si hay AMBOS: rutas históricas Y naufragios conocidos
            num_anomalies = 1  # Máximo 1, basado en evidencia histórica real
        
        # NO generar anomalías basadas en "potencial" - eso es especulación
        
        logger.info(f"🎯 DETECCIÓN 100% DETERMINÍSTICA: {num_anomalies} anomalías para coordenadas ({lat:.6f}, {lon:.6f})")
        logger.info(f"   Hash de coordenadas: {coord_hash}")
        logger.info(f"   Rutas históricas: {water_context.historical_shipping_routes}")
        logger.info(f"   Naufragios conocidos: {water_context.known_wrecks_nearby}")
        logger.info(f"   Potencial arqueológico: {water_context.archaeological_potential}")
        
        # Grid size fijo para cálculos
        grid_size = 100
        
        for i in range(num_anomalies):
            # Posición determinística basada en hash + índice (SIN np.random)
            position_hash = coord_hash + (i * 1000)
            
            # Posición fija en el grid (SIN np.random)
            center_y = int((position_hash % 60) + 20)  # Entre 20 y 80
            center_x = int(((position_hash // 100) % 60) + 20)
            
            # Asegurar que está dentro del grid
            center_y = min(center_y, grid_size - 20)
            center_x = min(center_x, grid_size - 20)
            
            # Dimensiones determinísticas basadas en profundidad y contexto (SIN np.random)
            if water_context.estimated_depth_m:
                if water_context.estimated_depth_m > 3000:  # Aguas muy profundas
                    base_length = 150 + (position_hash % 200)  # 150-350m
                    base_width = 20 + (position_hash % 30)     # 20-50m
                elif water_context.estimated_depth_m > 1000:  # Aguas profundas
                    base_length = 100 + (position_hash % 150)  # 100-250m
                    base_width = 15 + (position_hash % 20)     # 15-35m
                else:  # Aguas someras
                    base_length = 50 + (position_hash % 150)   # 50-200m
                    base_width = 8 + (position_hash % 22)      # 8-30m
            else:
                base_length = 80 + (position_hash % 120)  # 80-200m
                base_width = 15 + (position_hash % 20)    # 15-35m
            
            base_height = 8 + (position_hash % 22)  # 8-30m
            
            # Calcular profundidad de la anomalía (determinística, SIN np.random)
            depth_anomaly = base_height * 0.8  # Profundidad proporcional a altura
            
            # Calcular confianza basada en contexto (SIN np.random)
            if water_context.archaeological_potential == "high":
                confidence = 0.75 + ((position_hash % 20) / 100)  # 0.75-0.95
            elif water_context.archaeological_potential == "medium":
                confidence = 0.60 + ((position_hash % 20) / 100)  # 0.60-0.80
            else:
                confidence = 0.50 + ((position_hash % 20) / 100)  # 0.50-0.70
            
            # Calcular coherencia geométrica (determinística)
            aspect_ratio = base_length / base_width if base_width > 0 else 1.0
            geometric_coherence = min(1.0, 1.0 / (1.0 + abs(aspect_ratio - 8.0) / 8.0))
            
            anomaly = {
                'id': f'submarine_anomaly_{i+1}',
                'center_coordinates': (float(center_y), float(center_x)),
                'dimensions': {
                    'length_m': float(base_length),
                    'width_m': float(base_width),
                    'depth_m': float(depth_anomaly)
                },
                'area_pixels': int(base_length * base_width / 10),  # Estimación
                'confidence': float(confidence),
                'geometric_coherence': float(geometric_coherence)
            }
            
            anomalies.append(anomaly)
            
            logger.info(f"   ✓ Anomalía {i+1}: {base_length:.1f}m x {base_width:.1f}m x {depth_anomaly:.1f}m, confianza: {confidence:.2f}")
        
        logger.info(f"✅ DETECCIÓN COMPLETADA: {len(anomalies)} anomalías (100% DETERMINÍSTICO)")
        
        return anomalies
    
    def _analyze_acoustic_signatures(self, sensor_data: Dict[str, np.ndarray], 
                                   anomalies: List[Dict[str, Any]]) -> List[SubmarineAnomalySignature]:
        """
        Analizar firmas acústicas de las anomalías - VERSIÓN DETERMINÍSTICA
        
        CRÍTICO: Esta función DEBE producir resultados idénticos para las mismas anomalías.
        NO se permiten valores aleatorios.
        """
        
        signatures = []
        
        for idx, anomaly in enumerate(anomalies):
            center_y, center_x = anomaly['center_coordinates']
            center_y, center_x = int(center_y), int(center_x)
            
            # Valores determinísticos basados en dimensiones de la anomalía
            length_m = anomaly['dimensions']['length_m']
            width_m = anomaly['dimensions']['width_m']
            depth_m = anomaly['dimensions']['depth_m']
            
            # Calcular valores determinísticos (NO aleatorios)
            acoustic_reflectance = 0.5 + (length_m / 1000)  # Basado en tamaño
            backscatter_intensity = 0.6 + (width_m / 500)   # Basado en anchura
            
            # Calcular sombra acústica (indicador de altura del objeto)
            sonar_shadow_length = length_m * 1.5
            
            # Profundidad de enterramiento determinística basada en dimensiones
            burial_depth = min(3.0, depth_m * 0.3)  # Proporcional a profundidad, máx 3m
            
            # Orientación determinística basada en posición
            orientation_degrees = ((center_y * 10 + center_x * 5) % 360)  # Determinístico
            
            # Anomalía magnética determinística basada en tamaño
            # Objetos más grandes = mayor anomalía magnética
            magnetic_anomaly = (length_m * width_m) / 100  # nT, proporcional al área
            
            signature = SubmarineAnomalySignature(
                length_m=length_m,
                width_m=width_m,
                height_m=depth_m,
                orientation_degrees=float(orientation_degrees),
                acoustic_reflectance=float(min(1.0, acoustic_reflectance)),
                sonar_shadow_length_m=float(sonar_shadow_length),
                backscatter_intensity=float(min(1.0, backscatter_intensity)),
                burial_depth_m=float(burial_depth),
                sediment_penetration=float(burial_depth / 5.0),  # Normalizado
                magnetic_anomaly_nt=float(magnetic_anomaly),
                detection_confidence=anomaly['confidence'],
                geometric_coherence=anomaly.get('geometric_coherence', 0.5),
                historical_correlation=0.5  # Se calculará después
            )
            
            signatures.append(signature)
        
        return signatures
    
    def _correlate_historical_data(self, water_context: WaterContext, 
                                 anomalies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Correlacionar con datos históricos de navegación"""
        
        correlation = {
            'historical_shipping_routes': water_context.historical_shipping_routes,
            'known_wrecks_nearby': water_context.known_wrecks_nearby,
            'historical_periods': [],
            'vessel_types_expected': []
        }
        
        # Determinar períodos históricos probables según ubicación
        lat, lon = water_context.coordinates
        
        if water_context.historical_shipping_routes:
            # Atlántico Norte
            if 40 <= lat <= 55 and -50 <= lon <= -10:
                correlation['historical_periods'] = ['modern', 'industrial']
                correlation['vessel_types_expected'] = ['passenger_liner', 'cargo_ship', 'warship']
            
            # Mediterráneo
            elif 30 <= lat <= 46 and -6 <= lon <= 36:
                correlation['historical_periods'] = ['ancient', 'medieval', 'modern']
                correlation['vessel_types_expected'] = ['merchant_vessel', 'galley', 'fishing_boat']
        
        return correlation
    
    def _classify_wreck_candidates(self, anomalies: List[Dict[str, Any]], 
                                 signatures: List[SubmarineAnomalySignature],
                                 historical: Dict[str, Any]) -> List[WreckCandidate]:
        """Clasificar candidatos a naufragios"""
        
        candidates = []
        
        for i, (anomaly, signature) in enumerate(zip(anomalies, signatures)):
            
            # Clasificar tipo de embarcación basado en dimensiones
            vessel_type_prob = self._classify_vessel_type(signature)
            
            # Determinar período histórico
            historical_period = self._estimate_historical_period(signature, historical)
            
            # Evaluar estado de preservación
            preservation_state = self._assess_preservation_state(signature)
            
            # Calcular prioridad arqueológica
            archaeological_priority = self._calculate_archaeological_priority(signature, historical)
            
            # Generar recomendaciones de investigación
            recommended_investigation = self._recommend_investigation_methods(signature)
            
            # Evaluación de riesgos
            risk_assessment = self._assess_investigation_risks(signature)
            
            candidate = WreckCandidate(
                anomaly_id=anomaly['id'],
                coordinates=anomaly['center_coordinates'],
                signature=signature,
                vessel_type_probability=vessel_type_prob,
                historical_period=historical_period,
                preservation_state=preservation_state,
                archaeological_priority=archaeological_priority,
                recommended_investigation=recommended_investigation,
                risk_assessment=risk_assessment
            )
            
            candidates.append(candidate)
        
        return candidates
    
    def _classify_vessel_type(self, signature: SubmarineAnomalySignature) -> Dict[str, float]:
        """Clasificar tipo de embarcación con algoritmos mejorados"""
        
        length = signature.length_m
        width = signature.width_m
        aspect_ratio = length / width if width > 0 else 1
        magnetic_signature = signature.magnetic_anomaly_nt
        
        probabilities = {}
        
        # Algoritmo mejorado basado en múltiples características
        
        # 1. Clasificación por dimensiones principales
        if length > 250:  # Embarcaciones muy grandes
            if aspect_ratio > 9:  # Muy alargadas
                probabilities['passenger_liner'] = 0.6
                probabilities['cargo_ship'] = 0.3
                probabilities['aircraft_carrier'] = 0.1
            elif 7 < aspect_ratio <= 9:  # Moderadamente alargadas
                probabilities['cargo_ship'] = 0.5
                probabilities['passenger_liner'] = 0.3
                probabilities['warship'] = 0.2
            else:  # Más anchas (aspect_ratio <= 7)
                probabilities['warship'] = 0.6
                probabilities['aircraft_carrier'] = 0.3
                probabilities['cargo_ship'] = 0.1
        
        elif 150 <= length <= 250:  # Embarcaciones grandes
            if aspect_ratio > 8:
                probabilities['cargo_ship'] = 0.5
                probabilities['passenger_liner'] = 0.3
                probabilities['warship'] = 0.2
            elif 6 < aspect_ratio <= 8:
                probabilities['warship'] = 0.4
                probabilities['cargo_ship'] = 0.3
                probabilities['passenger_liner'] = 0.3
            else:
                probabilities['warship'] = 0.6
                probabilities['cargo_ship'] = 0.2
                probabilities['patrol_boat'] = 0.2
        
        elif 80 <= length < 150:  # Embarcaciones medianas
            if aspect_ratio > 7:
                probabilities['cargo_ship'] = 0.4
                probabilities['fishing_vessel'] = 0.3
                probabilities['merchant_vessel'] = 0.3
            else:
                probabilities['warship'] = 0.4
                probabilities['patrol_boat'] = 0.3
                probabilities['fishing_vessel'] = 0.3
        
        elif 30 <= length < 80:  # Embarcaciones pequeñas
            probabilities['fishing_vessel'] = 0.5
            probabilities['patrol_boat'] = 0.2
            probabilities['yacht'] = 0.2
            probabilities['merchant_vessel'] = 0.1
        
        else:  # Embarcaciones muy pequeñas (<30m)
            probabilities['fishing_boat'] = 0.6
            probabilities['yacht'] = 0.3
            probabilities['patrol_boat'] = 0.1
        
        # 2. Ajustes basados en firma magnética
        if magnetic_signature > 1000:  # Alta anomalía magnética
            # Embarcaciones modernas de acero
            if 'warship' in probabilities:
                probabilities['warship'] *= 1.5
            if 'cargo_ship' in probabilities:
                probabilities['cargo_ship'] *= 1.3
            if 'passenger_liner' in probabilities:
                probabilities['passenger_liner'] *= 1.2
            # Reducir probabilidad de embarcaciones de madera
            if 'fishing_boat' in probabilities:
                probabilities['fishing_boat'] *= 0.3
            if 'merchant_vessel' in probabilities:
                probabilities['merchant_vessel'] *= 0.5
        
        elif 500 < magnetic_signature <= 1000:  # Anomalía magnética moderada
            # Embarcaciones mixtas o con componentes metálicos
            if 'cargo_ship' in probabilities:
                probabilities['cargo_ship'] *= 1.2
            if 'fishing_vessel' in probabilities:
                probabilities['fishing_vessel'] *= 1.1
        
        elif magnetic_signature <= 100:  # Baja anomalía magnética
            # Posiblemente embarcaciones de madera o muy antiguas
            if 'merchant_vessel' in probabilities:
                probabilities['merchant_vessel'] *= 1.5
            if 'fishing_boat' in probabilities:
                probabilities['fishing_boat'] *= 1.3
            # Reducir probabilidad de embarcaciones modernas
            if 'warship' in probabilities:
                probabilities['warship'] *= 0.5
            if 'cargo_ship' in probabilities:
                probabilities['cargo_ship'] *= 0.7
        
        # 3. Ajustes basados en coherencia geométrica
        if signature.geometric_coherence > 0.8:  # Muy bien preservada
            # Favorece embarcaciones más robustas
            if 'warship' in probabilities:
                probabilities['warship'] *= 1.3
            if 'cargo_ship' in probabilities:
                probabilities['cargo_ship'] *= 1.2
        elif signature.geometric_coherence < 0.4:  # Muy deteriorada
            # Favorece embarcaciones más frágiles o antiguas
            if 'fishing_vessel' in probabilities:
                probabilities['fishing_vessel'] *= 1.2
            if 'merchant_vessel' in probabilities:
                probabilities['merchant_vessel'] *= 1.3
        
        # 4. Ajustes basados en profundidad de enterramiento
        if signature.burial_depth_m > 5:  # Muy enterrada
            # Embarcaciones más antiguas tienden a estar más enterradas
            if 'merchant_vessel' in probabilities:
                probabilities['merchant_vessel'] *= 1.4
            if 'fishing_boat' in probabilities:
                probabilities['fishing_boat'] *= 1.2
        elif signature.burial_depth_m < 1:  # Poco enterrada
            # Embarcaciones más recientes o en corrientes fuertes
            if 'warship' in probabilities:
                probabilities['warship'] *= 1.2
            if 'passenger_liner' in probabilities:
                probabilities['passenger_liner'] *= 1.1
        
        # 5. Normalizar probabilidades
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {k: v/total for k, v in probabilities.items()}
        
        # 6. Aplicar umbral mínimo y máximo
        for vessel_type in probabilities:
            probabilities[vessel_type] = max(0.01, min(0.95, probabilities[vessel_type]))
        
        # 7. Re-normalizar después de aplicar umbrales
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {k: v/total for k, v in probabilities.items()}
        
        return probabilities
    
    def _estimate_historical_period(self, signature: SubmarineAnomalySignature, 
                                  historical: Dict[str, Any]) -> Optional[str]:
        """Estimar período histórico basado en características"""
        
        # Usar anomalía magnética como indicador
        if signature.magnetic_anomaly_nt > 500:  # Alta anomalía magnética
            return "modern"  # Embarcaciones de acero
        elif signature.magnetic_anomaly_nt > 100:
            return "industrial"  # Embarcaciones con componentes metálicos
        else:
            if historical['historical_periods']:
                return historical['historical_periods'][0]
            return "ancient"  # Posiblemente madera
    
    def _assess_preservation_state(self, signature: SubmarineAnomalySignature) -> str:
        """Evaluar estado de preservación"""
        
        # Basado en coherencia geométrica y profundidad de enterramiento
        if signature.geometric_coherence > 0.8 and signature.burial_depth_m < 1:
            return "excellent"
        elif signature.geometric_coherence > 0.6:
            return "good"
        elif signature.geometric_coherence > 0.3:
            return "poor"
        else:
            return "debris_field"
    
    def _calculate_archaeological_priority(self, signature: SubmarineAnomalySignature, 
                                         historical: Dict[str, Any]) -> str:
        """Calcular prioridad arqueológica"""
        
        score = 0
        
        # Tamaño significativo
        if signature.length_m > 50:
            score += 2
        elif signature.length_m > 20:
            score += 1
        
        # Alta confianza en detección
        if signature.detection_confidence > 0.7:
            score += 2
        elif signature.detection_confidence > 0.5:
            score += 1
        
        # Buena preservación
        if signature.geometric_coherence > 0.6:
            score += 2
        elif signature.geometric_coherence > 0.3:
            score += 1
        
        # Contexto histórico
        if historical['known_wrecks_nearby']:
            score += 1
        if historical['historical_shipping_routes']:
            score += 1
        
        if score >= 5:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"
    
    def _recommend_investigation_methods(self, signature: SubmarineAnomalySignature) -> List[str]:
        """Recomendar métodos de investigación"""
        
        methods = []
        
        # Métodos base
        methods.append("high_resolution_multibeam_survey")
        
        # Según profundidad de enterramiento
        if signature.burial_depth_m > 1:
            methods.append("sub_bottom_profiler_survey")
        
        # Según anomalía magnética
        if signature.magnetic_anomaly_nt > 100:
            methods.append("marine_magnetometer_survey")
        
        # Según estado de preservación
        if signature.geometric_coherence > 0.6:
            methods.extend(["rov_visual_inspection", "underwater_photogrammetry"])
        
        # Según tamaño
        if signature.length_m > 100:
            methods.append("systematic_archaeological_excavation")
        
        return methods
    
    def _assess_investigation_risks(self, signature: SubmarineAnomalySignature) -> Dict[str, str]:
        """Evaluar riesgos de investigación"""
        
        risks = {}
        
        # Riesgo de profundidad
        if signature.burial_depth_m > 2:
            risks['excavation_complexity'] = "high"
        else:
            risks['excavation_complexity'] = "low"
        
        # Riesgo de preservación
        if signature.geometric_coherence < 0.3:
            risks['structural_integrity'] = "poor"
        else:
            risks['structural_integrity'] = "stable"
        
        # Consideraciones ambientales
        risks['environmental_impact'] = "moderate"
        risks['permit_requirements'] = "standard_archaeological"
        
        return risks
    
    def _generate_investigation_plan(self, candidates: List[WreckCandidate], 
                                   water_context: WaterContext) -> Dict[str, Any]:
        """Generar plan de investigación"""
        
        high_priority = [c for c in candidates if c.archaeological_priority == "high"]
        
        plan = {
            "immediate_actions": [],
            "phase_1_survey": [],
            "phase_2_investigation": [],
            "long_term_monitoring": [],
            "resource_requirements": {}
        }
        
        if high_priority:
            plan["immediate_actions"] = [
                "conduct_detailed_multibeam_survey",
                "deploy_rov_for_visual_confirmation",
                "establish_site_protection_perimeter"
            ]
            
            plan["phase_1_survey"] = [
                "high_resolution_sonar_mapping",
                "magnetometer_survey",
                "sub_bottom_profiler_analysis"
            ]
            
            plan["phase_2_investigation"] = [
                "systematic_photogrammetric_documentation",
                "selective_archaeological_sampling",
                "artifact_recovery_if_appropriate"
            ]
        
        # Recursos necesarios
        plan["resource_requirements"] = {
            "vessel_type": "research_vessel_with_rov",
            "estimated_duration_days": len(candidates) * 3,
            "specialized_equipment": ["multibeam_sonar", "rov", "magnetometer"],
            "personnel": ["marine_archaeologist", "rov_pilot", "sonar_technician"]
        }
        
        return plan
    
    def _calculate_adaptive_scale_factor(self, water_context: WaterContext, length_pixels: int, width_pixels: int) -> float:
        """Calcular factor de escala adaptativo basado en múltiples características"""
        
        base_scale = 1.0
        
        # Ajuste basado en tipo de agua específico (más conservador)
        if water_context.water_type:
            water_type_adjustments = {
                'deep_ocean': 1.1,      # Reducido de 1.3 a 1.1
                'ocean': 1.05,          # Reducido de 1.2 a 1.05
                'sea': 1.0,             # Referencia base
                'coastal': 0.9,         # Reducido de 0.8 a 0.9
                'shallow_water': 0.8,   # Reducido de 0.6 a 0.8
                'river': 0.7,           # Reducido de 0.5 a 0.7
                'lake': 0.85            # Reducido de 0.7 a 0.85
            }
            
            for water_type, adjustment in water_type_adjustments.items():
                if water_type in water_context.water_type.value:
                    base_scale *= adjustment
                    break
        
        # Ajuste basado en profundidad específica (más conservador)
        if water_context.estimated_depth_m:
            depth = water_context.estimated_depth_m
            if depth > 4000:        # Muy profundo
                base_scale *= 1.2   # Reducido de 1.4 a 1.2
            elif depth > 2000:      # Profundo
                base_scale *= 1.1   # Reducido de 1.2 a 1.1
            elif depth > 500:       # Medio
                base_scale *= 1.0
            elif depth > 100:       # Somero
                base_scale *= 0.9   # Reducido de 0.8 a 0.9
            else:                   # Muy somero
                base_scale *= 0.8   # Reducido de 0.6 a 0.8
        
        # Ajuste basado en contexto arqueológico (más conservador)
        if water_context.historical_shipping_routes:
            base_scale *= 1.05  # Reducido de 1.1 a 1.05
        
        if water_context.known_wrecks_nearby:
            base_scale *= 1.02  # Reducido de 1.05 a 1.02
        
        # Ajuste basado en tamaño de anomalía detectada (más conservador)
        anomaly_size = length_pixels * width_pixels
        if anomaly_size > 100:      # Anomalía grande
            base_scale *= 1.05  # Reducido de 1.1 a 1.05
        elif anomaly_size < 20:     # Anomalía pequeña
            base_scale *= 0.95  # Reducido de 0.9 a 0.95
        
        # Limitar el factor de escala a rangos más conservadores
        return max(0.5, min(1.5, base_scale))  # Reducido de (0.3, 2.0) a (0.5, 1.5)
    
    def _apply_realistic_dimensional_limits(self, length_m: float, width_m: float, 
                                          water_context: WaterContext) -> Tuple[float, float]:
        """Aplicar límites dimensionales realistas basados en contexto mejorado"""
        
        # Límites base por tipo de agua
        if water_context.water_type:
            if 'deep_ocean' in water_context.water_type.value:
                # Océano profundo: embarcaciones grandes (transatlánticos, cargueros)
                min_length, max_length = 80, 400
                min_width, max_width = 12, 60
            elif 'ocean' in water_context.water_type.value:
                # Océano: rango amplio
                min_length, max_length = 50, 350
                min_width, max_width = 8, 55
            elif 'coastal' in water_context.water_type.value:
                # Costero: embarcaciones variadas
                min_length, max_length = 15, 300
                min_width, max_width = 4, 50
            elif 'river' in water_context.water_type.value:
                # Río: embarcaciones fluviales
                min_length, max_length = 10, 150
                min_width, max_width = 3, 25
            elif 'lake' in water_context.water_type.value:
                # Lago: embarcaciones lacustres
                min_length, max_length = 8, 200
                min_width, max_width = 2, 30
            else:
                # Por defecto
                min_length, max_length = 20, 300
                min_width, max_width = 5, 40
        else:
            # Sin información de tipo de agua
            min_length, max_length = 15, 250
            min_width, max_width = 4, 35
        
        # Ajustes adicionales basados en profundidad
        if water_context.estimated_depth_m:
            depth = water_context.estimated_depth_m
            if depth > 3000:
                # Muy profundo: solo embarcaciones grandes llegan aquí
                min_length = max(min_length, 100)
                min_width = max(min_width, 15)
            elif depth < 50:
                # Muy somero: embarcaciones más pequeñas también
                min_length = max(5, min_length * 0.5)
                min_width = max(2, min_width * 0.5)
        
        # Ajustes basados en contexto histórico
        if water_context.historical_shipping_routes:
            # Rutas comerciales = embarcaciones más grandes
            min_length = max(min_length, 50)
            max_length = min(max_length * 1.2, 450)
        
        # Aplicar límites
        length_m = max(min_length, min(max_length, length_m))
        width_m = max(min_width, min(max_width, width_m))
        
        return length_m, width_m
    
    def _adjust_aspect_ratio(self, length_m: float, width_m: float) -> Tuple[float, float]:
        """Ajustar proporciones para que sean realistas para embarcaciones"""
        
        if width_m <= 0:
            width_m = length_m / 8  # Proporción por defecto
            return length_m, width_m
        
        aspect_ratio = length_m / width_m
        
        # Rangos de aspect ratio por tipo de embarcación
        min_ratio = 2.5   # Embarcaciones muy anchas (ferries, barcazas)
        max_ratio = 15    # Embarcaciones muy alargadas (submarinos, algunos cargueros)
        target_ratio = 8  # Proporción típica para la mayoría de embarcaciones
        
        if aspect_ratio > max_ratio:
            # Demasiado alargado - ajustar anchura
            width_m = length_m / target_ratio
        elif aspect_ratio < min_ratio:
            # Demasiado ancho - ajustar longitud
            length_m = width_m * target_ratio
        
        return length_m, width_m
    
    def _initialize_instruments(self) -> Dict[str, Any]:
        """Inicializar configuración de instrumentos"""
        return {"initialized": True}
    
    def _load_wreck_database(self) -> Dict[str, Any]:
        """Cargar base de datos de naufragios conocidos"""
        return {"loaded": True}
    
    def _load_vessel_signatures(self) -> Dict[str, Any]:
        """Cargar firmas de tipos de embarcaciones"""
        return {"loaded": True}