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
        Análisis arqueológico submarino completo
        
        Args:
            water_context: Contexto del cuerpo de agua
            bounds: Límites del área (lat_min, lat_max, lon_min, lon_max)
            
        Returns:
            Resultados del análisis submarino
        """
        try:
            logger.info(f"🌊 Iniciando análisis arqueológico submarino")
            logger.info(f"   Tipo de agua: {water_context.water_type.value if water_context.water_type else 'unknown'}")
            logger.info(f"   Profundidad estimada: {water_context.estimated_depth_m}m")
            logger.info(f"   Potencial arqueológico: {water_context.archaeological_potential}")
            
            # 1. Seleccionar instrumentos según contexto
            selected_instruments = self._select_instruments_for_context(water_context)
            
            # 2. Generar datos sintéticos de instrumentos submarinos
            instrument_data = self._generate_submarine_sensor_data(water_context, bounds, selected_instruments)
            
            # 3. Detectar anomalías volumétricas submarinas
            volumetric_anomalies = self._detect_submarine_volumetric_anomalies(instrument_data, water_context)
            
            # 4. Analizar firmas acústicas
            acoustic_signatures = self._analyze_acoustic_signatures(instrument_data, volumetric_anomalies)
            
            # 5. Correlacionar con datos históricos
            historical_correlation = self._correlate_historical_data(water_context, volumetric_anomalies)
            
            # 6. Clasificar candidatos a naufragios
            wreck_candidates = self._classify_wreck_candidates(
                volumetric_anomalies, acoustic_signatures, historical_correlation
            )
            
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
        """Generar datos batimétricos sintéticos"""
        
        base_depth = water_context.estimated_depth_m or 100
        
        # Crear topografía del fondo marino
        bathymetry = np.random.normal(base_depth, base_depth * 0.1, (grid_size, grid_size))
        
        # Añadir características del fondo según tipo de agua
        if water_context.water_type == WaterBodyType.RIVER:
            # Canales de río
            center = grid_size // 2
            bathymetry[center-5:center+5, :] += np.random.uniform(2, 10)
            
        elif water_context.water_type == WaterBodyType.COASTAL:
            # Pendiente costera
            for i in range(grid_size):
                bathymetry[i, :] += i * (base_depth * 0.02)
        
        # Añadir anomalías potenciales (naufragios simulados)
        # Para aguas con rutas históricas o naufragios conocidos, garantizar anomalías
        if (water_context.historical_shipping_routes or 
            water_context.known_wrecks_nearby or 
            water_context.archaeological_potential in ["high", "medium"]):
            num_anomalies = np.random.randint(1, 3)  # Garantizar al menos 1 anomalía
        else:
            num_anomalies = np.random.randint(0, 2)  # Posibles anomalías
            
        for _ in range(num_anomalies):
            x, y = np.random.randint(10, grid_size-10, 2)
            # Anomalía tipo naufragio con dimensiones realistas basadas en profundidad
            
            # Ajustar tamaño según profundidad del agua
            if base_depth > 3000:  # Aguas muy profundas - naufragios grandes
                wreck_length = np.random.uniform(150, 350)  # 150-350m longitud
                wreck_width = np.random.uniform(20, 50)     # 20-50m anchura
            elif base_depth > 1000:  # Aguas profundas - naufragios medianos
                wreck_length = np.random.uniform(100, 250)  # 100-250m longitud
                wreck_width = np.random.uniform(15, 35)     # 15-35m anchura
            else:  # Aguas someras - naufragios variados
                wreck_length = np.random.uniform(50, 200)   # 50-200m longitud
                wreck_width = np.random.uniform(8, 30)      # 8-30m anchura
            
            wreck_height = np.random.uniform(8, 30)    # 8-30m altura
            
            # Crear depresión con forma de barco
            length_pixels = max(3, int(wreck_length / 10))  # Conversión aproximada a píxeles
            width_pixels = max(2, int(wreck_width / 10))
            
            x_start = max(0, x - length_pixels//2)
            x_end = min(grid_size, x + length_pixels//2)
            y_start = max(0, y - width_pixels//2)
            y_end = min(grid_size, y + width_pixels//2)
            
            # Crear depresión más pronunciada
            depth_change = np.random.uniform(wreck_height/2, wreck_height)
            bathymetry[x_start:x_end, y_start:y_end] -= depth_change
        
        return bathymetry
    
    def _generate_acoustic_image_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar imágenes acústicas sintéticas"""
        
        # Imagen base del fondo
        acoustic_image = np.random.uniform(0.2, 0.8, (grid_size, grid_size))
        
        # Añadir características según tipo de sedimento
        if water_context.sediment_type == "sand_gravel":
            acoustic_image += np.random.uniform(0, 0.3, (grid_size, grid_size))
        elif water_context.sediment_type == "silt_clay":
            acoustic_image *= 0.7  # Menor reflectancia
        
        # Añadir anomalías con alta reflectancia (objetos metálicos)
        num_targets = np.random.randint(0, 3)
        for _ in range(num_targets):
            x, y = np.random.randint(5, grid_size-5, 2)
            # Firma acústica de objeto metálico
            acoustic_image[x-2:x+2, y-5:y+5] = np.random.uniform(0.8, 1.0)
        
        return acoustic_image
    
    def _generate_sediment_profile_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar perfiles de sedimento sintéticos"""
        
        # Capas de sedimento
        sediment_layers = np.random.uniform(0.1, 0.9, (grid_size, grid_size, 10))  # 10 capas
        
        # Añadir objetos enterrados
        num_buried = np.random.randint(0, 2)
        for _ in range(num_buried):
            x, y = np.random.randint(5, grid_size-5, 2)
            depth_layer = np.random.randint(2, 8)
            # Objeto enterrado
            sediment_layers[x-1:x+1, y-3:y+3, depth_layer] = 0.95
        
        return sediment_layers
    
    def _generate_magnetic_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar datos magnéticos sintéticos"""
        
        # Campo magnético base
        magnetic_field = np.random.normal(50000, 100, (grid_size, grid_size))  # nT
        
        # Añadir anomalías magnéticas (objetos ferrosos)
        num_anomalies = np.random.randint(0, 3)
        for _ in range(num_anomalies):
            x, y = np.random.randint(5, grid_size-5, 2)
            # Anomalía magnética dipolar
            anomaly_strength = np.random.uniform(100, 1000)
            magnetic_field[x-2:x+2, y-2:y+2] += anomaly_strength
        
        return magnetic_field
    
    def _generate_acoustic_reflectance_data(self, water_context: WaterContext, grid_size: int) -> np.ndarray:
        """Generar datos de reflectancia acústica sintéticos"""
        
        # Reflectancia base según tipo de fondo
        if water_context.sediment_type == "sand_gravel":
            base_reflectance = np.random.uniform(0.4, 0.7, (grid_size, grid_size))
        elif water_context.sediment_type == "silt_clay":
            base_reflectance = np.random.uniform(0.1, 0.4, (grid_size, grid_size))
        else:
            base_reflectance = np.random.uniform(0.2, 0.6, (grid_size, grid_size))
        
        return base_reflectance
    
    def _detect_submarine_volumetric_anomalies(self, sensor_data: Dict[str, np.ndarray], water_context: WaterContext) -> List[Dict[str, Any]]:
        """Detectar anomalías volumétricas submarinas"""
        
        anomalies = []
        
        if 'bathymetry' in sensor_data:
            bathymetry = sensor_data['bathymetry']
            
            # Detectar depresiones (posibles naufragios)
            mean_depth = np.mean(bathymetry)
            std_depth = np.std(bathymetry)
            
            # Buscar áreas significativamente más profundas (umbral más sensible)
            anomaly_mask = bathymetry < (mean_depth - 1.5 * std_depth)  # Reducido de 2 a 1.5
            
            # Encontrar regiones conectadas (implementación simplificada sin scipy)
            anomaly_positions = np.where(anomaly_mask)
            
            if len(anomaly_positions[0]) > 0:
                # Agrupar píxeles cercanos en regiones
                regions = []
                processed = set()
                
                for i in range(len(anomaly_positions[0])):
                    pos = (anomaly_positions[0][i], anomaly_positions[1][i])
                    if pos not in processed:
                        # Crear nueva región
                        region_pixels = [pos]
                        processed.add(pos)
                        
                        # Buscar píxeles conectados (simplificado)
                        for j in range(i+1, len(anomaly_positions[0])):
                            other_pos = (anomaly_positions[0][j], anomaly_positions[1][j])
                            if other_pos not in processed:
                                # Verificar si está cerca (distancia < 5 píxeles)
                                dist = np.sqrt((pos[0] - other_pos[0])**2 + (pos[1] - other_pos[1])**2)
                                if dist < 5:
                                    region_pixels.append(other_pos)
                                    processed.add(other_pos)
                        
                        if len(region_pixels) > 5:  # Reducido de 10 a 5 píxeles mínimos
                            regions.append(region_pixels)
                
                # Procesar regiones encontradas
                for i, region_pixels in enumerate(regions, 1):
                    coords_y = [p[0] for p in region_pixels]
                    coords_x = [p[1] for p in region_pixels]
                    
                    center_y, center_x = np.mean(coords_y), np.mean(coords_x)
                    
                    # Estimar dimensiones con escalado adaptativo
                    length_pixels = max(coords_y) - min(coords_y)
                    width_pixels = max(coords_x) - min(coords_x)
                    
                    # Escalado adaptativo basado en profundidad y tipo de agua
                    if water_context.estimated_depth_m:
                        if water_context.estimated_depth_m > 3000:  # Aguas muy profundas
                            # Resolución menor, objetos parecen más pequeños
                            scale_factor = 8  # Reducido de 15 a 8 metros por píxel
                        elif water_context.estimated_depth_m > 1000:  # Aguas profundas
                            scale_factor = 6  # Reducido de 12 a 6
                        elif water_context.estimated_depth_m > 200:  # Aguas medias
                            scale_factor = 4  # Reducido de 8 a 4
                        else:  # Aguas someras
                            scale_factor = 2  # Reducido de 5 a 2 - Mayor resolución
                    else:
                        scale_factor = 5  # Factor por defecto reducido de 10 a 5
                    
                    # Ajuste adicional basado en tipo de agua
                    if water_context.water_type:
                        if 'deep_ocean' in water_context.water_type.value:
                            scale_factor *= 1.2  # Océano profundo = objetos más grandes
                        elif 'coastal' in water_context.water_type.value:
                            scale_factor *= 0.8  # Aguas costeras = mejor resolución
                        elif 'river' in water_context.water_type.value:
                            scale_factor *= 0.6  # Ríos = muy buena resolución
                    
                    # Calcular dimensiones finales con escalado adaptativo mejorado
                    length_m = length_pixels * scale_factor
                    width_m = width_pixels * scale_factor
                    
                    # Aplicar escalado adaptativo adicional basado en múltiples factores
                    adaptive_scale = self._calculate_adaptive_scale_factor(water_context, length_pixels, width_pixels)
                    length_m *= adaptive_scale
                    width_m *= adaptive_scale
                    
                    # Aplicar límites realistas basados en contexto mejorado
                    length_m, width_m = self._apply_realistic_dimensional_limits(
                        length_m, width_m, water_context
                    )
                    
                    # Verificar y ajustar proporciones realistas (aspect ratio)
                    length_m, width_m = self._adjust_aspect_ratio(length_m, width_m)
                    
                    # Calcular profundidad de la anomalía
                    region_depths = [bathymetry[p[0], p[1]] for p in region_pixels]
                    depth_anomaly = mean_depth - np.mean(region_depths)
                    
                    # Calcular coherencia geométrica basada en la forma de la anomalía
                    aspect_ratio = length_m / width_m if width_m > 0 else 1.0
                    geometric_coherence = min(1.0, 1.0 / (1.0 + abs(aspect_ratio - 8.0) / 8.0))  # Óptimo alrededor de 8:1
                    
                    anomaly = {
                        'id': f'submarine_anomaly_{i}',
                        'center_coordinates': (float(center_y), float(center_x)),
                        'dimensions': {
                            'length_m': float(length_m),  # Dimensiones calibradas
                            'width_m': float(width_m),
                            'depth_m': float(depth_anomaly)
                        },
                        'area_pixels': len(region_pixels),
                        'confidence': min(1.0, depth_anomaly / std_depth) if std_depth > 0 else 0.5,
                        'geometric_coherence': geometric_coherence
                    }
                    
                    anomalies.append(anomaly)
        
        return anomalies
    
    def _analyze_acoustic_signatures(self, sensor_data: Dict[str, np.ndarray], 
                                   anomalies: List[Dict[str, Any]]) -> List[SubmarineAnomalySignature]:
        """Analizar firmas acústicas de las anomalías"""
        
        signatures = []
        
        for anomaly in anomalies:
            center_y, center_x = anomaly['center_coordinates']
            center_y, center_x = int(center_y), int(center_x)
            
            # Extraer datos acústicos en la región de la anomalía
            acoustic_reflectance = 0.5
            backscatter_intensity = 0.6
            
            if 'acoustic_image' in sensor_data:
                acoustic_data = sensor_data['acoustic_image']
                region_size = 5
                y_start = max(0, center_y - region_size)
                y_end = min(acoustic_data.shape[0], center_y + region_size)
                x_start = max(0, center_x - region_size)
                x_end = min(acoustic_data.shape[1], center_x + region_size)
                
                region_data = acoustic_data[y_start:y_end, x_start:x_end]
                acoustic_reflectance = np.mean(region_data)
                backscatter_intensity = np.std(region_data)
            
            # Calcular sombra acústica (indicador de altura del objeto)
            sonar_shadow_length = anomaly['dimensions']['length_m'] * 1.5
            
            # Estimar profundidad de enterramiento
            burial_depth = np.random.uniform(0, 3)  # 0-3m típico
            
            # Anomalía magnética si hay datos
            magnetic_anomaly = 0
            if 'magnetic_anomalies' in sensor_data:
                magnetic_data = sensor_data['magnetic_anomalies']
                if 0 <= center_y < magnetic_data.shape[0] and 0 <= center_x < magnetic_data.shape[1]:
                    magnetic_anomaly = magnetic_data[center_y, center_x] - np.mean(magnetic_data)
            
            signature = SubmarineAnomalySignature(
                length_m=anomaly['dimensions']['length_m'],
                width_m=anomaly['dimensions']['width_m'],
                height_m=anomaly['dimensions']['depth_m'],
                orientation_degrees=np.random.uniform(0, 360),
                acoustic_reflectance=acoustic_reflectance,
                sonar_shadow_length_m=sonar_shadow_length,
                backscatter_intensity=backscatter_intensity,
                burial_depth_m=burial_depth,
                sediment_penetration=burial_depth / 5.0,  # Normalizado
                magnetic_anomaly_nt=magnetic_anomaly,
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