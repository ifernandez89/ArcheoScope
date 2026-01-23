#!/usr/bin/env python3
"""
ArcheoScope Geometric Inference Engine - Volumetric Reconstruction Framework

PARADIGMA EPISTEMOLÓGICO:
"ArcheoScope no reconstruye estructuras: reconstruye espacios de posibilidad 
geométrica consistentes con firmas físicas persistentes."

Nivel de Reconstrucción: I/II (Geométrica Volumétrica Inferida)
- Forma aproximada con escala correcta
- Relaciones espaciales coherentes  
- Incertidumbre explícita
- NO detalles arquitectónicos
- NO función cultural
- NO afirmaciones históricas
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class MorphologicalClass(Enum):
    """Clases geométricas abstractas (NO tipológicas)."""
    TRUNCATED_PYRAMIDAL = "volumen_troncopiramidal"
    STEPPED_PLATFORM = "plataforma_escalonada"
    LINEAR_COMPACT = "estructura_lineal_compactada"
    CAVITY_VOID = "cavidad_vacio"
    EMBANKMENT_MOUND = "terraplen_monticulo"
    ORTHOGONAL_NETWORK = "red_ortogonal_superficial"
    UNDEFINED_VOLUME = "volumen_indefinido"

class InferenceLevel(Enum):
    """Niveles de inferencia volumétrica."""
    LEVEL_I = "geometrica_basica"      # Forma y escala aproximada
    LEVEL_II = "geometrica_avanzada"   # Relaciones espaciales coherentes
    LEVEL_III = "estructural_detallada" # NO IMPLEMENTADO - requiere LIDAR

@dataclass
class SpatialSignature:
    """Vector de firma física extraído de anomalía."""
    area_m2: float
    elongation_ratio: float
    symmetry_index: float
    anisotropy_factor: float
    thermal_amplitude: float
    sar_roughness: float
    multitemporal_coherence: float
    residual_slope: float
    
    # Metadatos de confianza
    signature_confidence: float
    sensor_convergence: float
    temporal_persistence: float

@dataclass
class VolumetricField:
    """Campo volumétrico de probabilidad (NO mesh sólido)."""
    probability_volume: np.ndarray  # 3D array [x, y, z] -> P(material|datos)
    void_probability: np.ndarray    # 3D array [x, y, z] -> P(vacío|datos)
    uncertainty_field: np.ndarray   # 3D array [x, y, z] -> incertidumbre
    
    # Metadatos espaciales
    voxel_size_m: float
    origin_coords: Tuple[float, float, float]  # (lat, lon, elevation)
    dimensions: Tuple[int, int, int]  # (nx, ny, nz)
    
    # Metadatos de inferencia
    inference_level: InferenceLevel
    morphological_class: MorphologicalClass
    confidence_layers: Dict[str, float]  # core/probable/possible

@dataclass
class GeometricModel:
    """Modelo geométrico 3D mínimo extraído del campo volumétrico."""
    vertices: np.ndarray        # Vértices del modelo low-poly
    faces: np.ndarray          # Caras triangulares
    confidence_zones: Dict[str, List[int]]  # Índices por zona de confianza
    
    # Propiedades geométricas
    estimated_volume_m3: float
    surface_area_m2: float
    max_height_m: float
    footprint_area_m2: float
    
    # Metadatos de reconstrucción
    reconstruction_method: str
    iso_surface_threshold: float
    smoothing_applied: bool
    symmetries_detected: List[str]

class GeometricInferenceEngine:
    """
    Motor de inferencia volumétrica probabilística para ArcheoScope.
    
    Pipeline:
    1. Extracción de firma espacial
    2. Clasificación morfológica blanda
    3. Inferencia volumétrica probabilística
    4. Reconstrucción geométrica mínima
    5. Metadatos y validación
    """
    
    def __init__(self):
        self.inference_level = InferenceLevel.LEVEL_II
        self.voxel_resolution_m = 2.0  # Resolución volumétrica
        self.confidence_threshold = 0.65
        
        logger.info("GeometricInferenceEngine inicializado - Nivel II")
    
    def _default_spatial_signature(self) -> SpatialSignature:
        """Generar firma espacial por defecto para casos de error."""
        return SpatialSignature(
            area_m2=1000.0,
            elongation_ratio=1.5,
            symmetry_index=0.5,
            anisotropy_factor=0.5,
            thermal_amplitude=5.0,
            sar_roughness=0.5,
            multitemporal_coherence=0.5,
            residual_slope=0.5,
            signature_confidence=0.3,
            sensor_convergence=0.5,
            temporal_persistence=0.5
        )
    
    def extract_spatial_signature(self, 
                                anomaly_data: Dict[str, Any],
                                layer_results: Dict[str, Any]) -> SpatialSignature:
        """
        ETAPA 1: Extracción de firma espacial de anomalía detectada.
        
        Convierte datos multi-espectrales en vector de firma física.
        """
        
        try:
            # Validación de entrada
            if not anomaly_data or not layer_results:
                logger.warning("Datos insuficientes para extracción de firma espacial")
                return self._default_spatial_signature()
            
            # Extraer métricas geométricas básicas con valores por defecto
            area_m2 = max(1.0, anomaly_data.get('footprint_area_m2', 1000.0))
            
            # Calcular elongación desde dimensiones
            length = anomaly_data.get('estimated_length_m', np.sqrt(area_m2 * 1.5))
            width = anomaly_data.get('estimated_width_m', np.sqrt(area_m2 / 1.5))
            
            # Evitar división por cero
            min_dimension = max(1.0, min(length, width))
            max_dimension = max(1.0, max(length, width))
            elongation_ratio = max_dimension / min_dimension
            
            # Índice de simetría (basado en coherencia geométrica)
            geometric_coherence = max(0.0, min(1.0, anomaly_data.get('geometric_coherence', 0.5)))
            symmetry_index = min(geometric_coherence * 1.2, 1.0)
            
            # Factor de anisotropía (basado en orientación preferencial)
            orientation_coherence = max(0.0, min(1.0, anomaly_data.get('orientation_coherence', 0.5)))
            anisotropy_factor = orientation_coherence
            
            # Amplitud térmica (diferencia día/noche simulada)
            thermal_data = layer_results.get('thermal_lst', {})
            thermal_prob = max(0.0, min(1.0, thermal_data.get('archaeological_probability', 0.3)))
            thermal_amplitude = thermal_prob * 15.0  # Max 15°C
            
            # Rugosidad SAR
            sar_data = layer_results.get('sar_backscatter', {})
            sar_roughness = max(0.0, min(1.0, sar_data.get('geometric_coherence', 0.5)))
            
            # Coherencia multitemporal
            temporal_values = [
                max(0.0, min(1.0, result.get('temporal_persistence', 0.5))) 
                for result in layer_results.values()
            ]
            multitemporal_coherence = np.mean(temporal_values) if temporal_values else 0.5
            
            # Pendiente residual (desacople topográfico)
            vegetation_data = layer_results.get('ndvi_vegetation', {})
            natural_explanation = max(0.0, min(1.0, vegetation_data.get('natural_explanation_score', 0.5)))
            residual_slope = 1.0 - natural_explanation
            
            # Métricas de confianza
            signature_confidence = max(0.0, min(1.0, anomaly_data.get('confidence_level', 0.5)))
            
            # Convergencia entre sensores
            archaeological_probs = [
                max(0.0, min(1.0, r.get('archaeological_probability', 0))) 
                for r in layer_results.values()
            ]
            if archaeological_probs:
                sensor_convergence = max(0.0, 1.0 - np.var(archaeological_probs))
            else:
                sensor_convergence = 0.5
            
            # Persistencia temporal promedio
            temporal_persistence = multitemporal_coherence
            
            signature = SpatialSignature(
                area_m2=area_m2,
                elongation_ratio=elongation_ratio,
                symmetry_index=symmetry_index,
                anisotropy_factor=anisotropy_factor,
                thermal_amplitude=thermal_amplitude,
                sar_roughness=sar_roughness,
                multitemporal_coherence=multitemporal_coherence,
                residual_slope=residual_slope,
                signature_confidence=signature_confidence,
                sensor_convergence=sensor_convergence,
                temporal_persistence=temporal_persistence
            )
            
            logger.info(f"Firma espacial extraída: área={area_m2:.0f}m², elongación={elongation_ratio:.2f}")
            
            return signature
            
        except Exception as e:
            logger.error(f"Error extrayendo firma espacial: {e}")
            return self._default_spatial_signature()
    
    def classify_morphology(self, signature: SpatialSignature) -> MorphologicalClass:
        """
        ETAPA 2: Clasificación morfológica blanda (NO tipológica).
        
        Clasifica por compatibilidad geométrica, NO por semántica arqueológica.
        """
        
        # Reglas de clasificación geométrica
        
        # Volumen troncopiramidal: alta simetría + área compacta + persistencia alta
        if (signature.symmetry_index > 0.7 and 
            signature.elongation_ratio < 2.0 and
            signature.temporal_persistence > 0.7):
            return MorphologicalClass.TRUNCATED_PYRAMIDAL
        
        # Plataforma escalonada: área grande + baja elongación + alta coherencia SAR
        elif (signature.area_m2 > 2000 and
              signature.elongation_ratio < 1.5 and
              signature.sar_roughness > 0.6):
            return MorphologicalClass.STEPPED_PLATFORM
        
        # Estructura lineal: alta elongación + anisotropía + persistencia
        elif (signature.elongation_ratio > 3.0 and
              signature.anisotropy_factor > 0.6 and
              signature.multitemporal_coherence > 0.6):
            return MorphologicalClass.LINEAR_COMPACT
        
        # Cavidad/vacío: baja rugosidad SAR + alta amplitud térmica
        elif (signature.sar_roughness < 0.4 and
              signature.thermal_amplitude > 8.0):
            return MorphologicalClass.CAVITY_VOID
        
        # Terraplén/montículo: alta rugosidad + pendiente residual + área media
        elif (signature.sar_roughness > 0.7 and
              signature.residual_slope > 0.5 and
              500 < signature.area_m2 < 5000):
            return MorphologicalClass.EMBANKMENT_MOUND
        
        # Red ortogonal: alta anisotropía + simetría + área extensa
        elif (signature.anisotropy_factor > 0.8 and
              signature.symmetry_index > 0.6 and
              signature.area_m2 > 5000):
            return MorphologicalClass.ORTHOGONAL_NETWORK
        
        else:
            return MorphologicalClass.UNDEFINED_VOLUME
    
    def generate_volumetric_field(self, 
                                signature: SpatialSignature,
                                morphology: MorphologicalClass,
                                bounds: Tuple[float, float, float, float]) -> VolumetricField:
        """
        ETAPA 3: Inferencia volumétrica probabilística.
        
        Genera campo volumétrico de probabilidad (NO mesh sólido).
        """
        
        # Calcular dimensiones del volumen
        lat_min, lat_max, lon_min, lon_max = bounds
        
        # Convertir a metros (aproximado)
        width_m = (lon_max - lon_min) * 85000  # ~85km por grado longitud
        height_m = (lat_max - lat_min) * 111000  # ~111km por grado latitud
        
        # Dimensiones del grid volumétrico
        nx = max(10, int(width_m / self.voxel_resolution_m))
        ny = max(10, int(height_m / self.voxel_resolution_m))
        nz = max(5, int(signature.area_m2**0.5 / self.voxel_resolution_m))  # Altura basada en área
        
        # Limitar dimensiones para eficiencia
        nx, ny, nz = min(nx, 100), min(ny, 100), min(nz, 50)
        
        # Inicializar campos volumétricos
        probability_volume = np.zeros((nx, ny, nz))
        void_probability = np.zeros((nx, ny, nz))
        uncertainty_field = np.ones((nx, ny, nz)) * 0.5  # Incertidumbre base 50%
        
        # Generar distribución de probabilidad basada en morfología
        center_x, center_y = nx // 2, ny // 2
        
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    
                    # Distancia desde el centro
                    dx = (i - center_x) / nx
                    dy = (j - center_y) / ny
                    dz = k / nz
                    
                    # Distancia radial normalizada
                    r_horizontal = np.sqrt(dx**2 + dy**2)
                    
                    # Probabilidad base según morfología
                    if morphology == MorphologicalClass.TRUNCATED_PYRAMIDAL:
                        # Pirámide truncada: máxima probabilidad en base, decrece con altura
                        base_prob = max(0, 1.0 - r_horizontal * 2)
                        height_factor = max(0, 1.0 - dz * 1.5)
                        prob = base_prob * height_factor * signature.signature_confidence
                        
                    elif morphology == MorphologicalClass.STEPPED_PLATFORM:
                        # Plataforma: probabilidad uniforme en niveles
                        if r_horizontal < 0.8:
                            level = int(dz * 3)  # 3 niveles
                            prob = 0.8 - level * 0.2 if level < 3 else 0.1
                            prob *= signature.signature_confidence
                        else:
                            prob = 0.1
                            
                    elif morphology == MorphologicalClass.LINEAR_COMPACT:
                        # Estructura lineal: probabilidad a lo largo del eje principal
                        if abs(dx) < 0.2 or abs(dy) < 0.2:  # Eje principal
                            prob = (1.0 - dz * 0.8) * signature.signature_confidence
                        else:
                            prob = 0.1
                            
                    elif morphology == MorphologicalClass.CAVITY_VOID:
                        # Cavidad: alta probabilidad de vacío
                        if r_horizontal < 0.6:
                            void_probability[i, j, k] = 0.8 * signature.signature_confidence
                            prob = 0.2
                        else:
                            prob = 0.1
                            
                    elif morphology == MorphologicalClass.EMBANKMENT_MOUND:
                        # Montículo: distribución gaussiana
                        gauss_factor = np.exp(-(r_horizontal**2 + dz**2) * 3)
                        prob = gauss_factor * signature.signature_confidence
                        
                    elif morphology == MorphologicalClass.ORTHOGONAL_NETWORK:
                        # Red ortogonal: patrones regulares
                        grid_x = abs(np.sin(dx * np.pi * 4))
                        grid_y = abs(np.sin(dy * np.pi * 4))
                        if grid_x > 0.7 or grid_y > 0.7:
                            prob = (1.0 - dz * 0.5) * signature.signature_confidence
                        else:
                            prob = 0.1
                            
                    else:  # UNDEFINED_VOLUME
                        # Distribución uniforme con baja probabilidad
                        prob = 0.3 * signature.signature_confidence * (1.0 - dz)
                    
                    probability_volume[i, j, k] = min(prob, 1.0)
                    
                    # Calcular incertidumbre basada en convergencia de sensores
                    base_uncertainty = 1.0 - signature.sensor_convergence
                    distance_uncertainty = r_horizontal * 0.3 + dz * 0.4
                    uncertainty_field[i, j, k] = min(base_uncertainty + distance_uncertainty, 1.0)
        
        # Aplicar suavizado para evitar pareidolia
        from scipy.ndimage import gaussian_filter
        probability_volume = gaussian_filter(probability_volume, sigma=1.0)
        
        # Calcular capas de confianza
        confidence_layers = {
            'core': np.sum(probability_volume > 0.7) / probability_volume.size,
            'probable': np.sum(probability_volume > 0.5) / probability_volume.size,
            'possible': np.sum(probability_volume > 0.3) / probability_volume.size
        }
        
        volumetric_field = VolumetricField(
            probability_volume=probability_volume,
            void_probability=void_probability,
            uncertainty_field=uncertainty_field,
            voxel_size_m=self.voxel_resolution_m,
            origin_coords=(lat_min, lon_min, 0.0),
            dimensions=(nx, ny, nz),
            inference_level=self.inference_level,
            morphological_class=morphology,
            confidence_layers=confidence_layers
        )
        
        logger.info(f"Campo volumétrico generado: {nx}x{ny}x{nz} voxels, confianza core: {confidence_layers['core']:.3f}")
        
        return volumetric_field
    
    def extract_geometric_model(self, volumetric_field: VolumetricField) -> GeometricModel:
        """
        ETAPA 4: Reconstrucción geométrica mínima.
        
        Extrae modelo 3D low-poly del campo volumétrico.
        """
        
        # Umbral de iso-superficie
        iso_threshold = 0.5
        
        # Extraer iso-superficie usando marching cubes (simplificado)
        prob_vol = volumetric_field.probability_volume
        nx, ny, nz = prob_vol.shape
        
        vertices = []
        faces = []
        
        # Algoritmo simplificado de extracción de superficie
        vertex_map = {}
        vertex_count = 0
        
        for i in range(nx-1):
            for j in range(ny-1):
                for k in range(nz-1):
                    
                    # Verificar si el voxel cruza el umbral
                    values = [
                        prob_vol[i, j, k],
                        prob_vol[i+1, j, k],
                        prob_vol[i, j+1, k],
                        prob_vol[i, j, k+1]
                    ]
                    
                    if min(values) < iso_threshold < max(values):
                        # Crear vértice en el centro del voxel
                        vertex_pos = (
                            i * volumetric_field.voxel_size_m,
                            j * volumetric_field.voxel_size_m,
                            k * volumetric_field.voxel_size_m
                        )
                        
                        vertex_key = (i, j, k)
                        if vertex_key not in vertex_map:
                            vertices.append(vertex_pos)
                            vertex_map[vertex_key] = vertex_count
                            vertex_count += 1
        
        # Generar caras triangulares (simplificado)
        for i in range(0, len(vertices)-2, 3):
            if i+2 < len(vertices):
                faces.append([i, i+1, i+2])
        
        vertices = np.array(vertices) if vertices else np.zeros((0, 3))
        faces = np.array(faces) if faces else np.zeros((0, 3), dtype=int)
        
        # Calcular propiedades geométricas
        if len(vertices) > 0:
            estimated_volume_m3 = np.sum(prob_vol > iso_threshold) * (volumetric_field.voxel_size_m ** 3)
            max_height_m = np.max(vertices[:, 2]) if len(vertices) > 0 else 0
            
            # Proyección 2D para área de huella
            if len(vertices) > 0:
                x_range = np.max(vertices[:, 0]) - np.min(vertices[:, 0])
                y_range = np.max(vertices[:, 1]) - np.min(vertices[:, 1])
                footprint_area_m2 = x_range * y_range
            else:
                footprint_area_m2 = 0
                
            surface_area_m2 = len(faces) * (volumetric_field.voxel_size_m ** 2) * 2  # Aproximación
        else:
            estimated_volume_m3 = 0
            surface_area_m2 = 0
            max_height_m = 0
            footprint_area_m2 = 0
        
        # Detectar simetrías (simplificado)
        symmetries_detected = []
        if volumetric_field.morphological_class in [MorphologicalClass.TRUNCATED_PYRAMIDAL, 
                                                   MorphologicalClass.STEPPED_PLATFORM]:
            symmetries_detected.append("bilateral_approximate")
        
        # Zonas de confianza basadas en probabilidad
        confidence_zones = {
            'high_confidence': list(range(len(vertices) // 3)),
            'medium_confidence': list(range(len(vertices) // 3, 2 * len(vertices) // 3)),
            'low_confidence': list(range(2 * len(vertices) // 3, len(vertices)))
        }
        
        geometric_model = GeometricModel(
            vertices=vertices,
            faces=faces,
            confidence_zones=confidence_zones,
            estimated_volume_m3=estimated_volume_m3,
            surface_area_m2=surface_area_m2,
            max_height_m=max_height_m,
            footprint_area_m2=footprint_area_m2,
            reconstruction_method="probabilistic_iso_surface",
            iso_surface_threshold=iso_threshold,
            smoothing_applied=True,
            symmetries_detected=symmetries_detected
        )
        
        logger.info(f"Modelo geométrico extraído: {len(vertices)} vértices, volumen estimado: {estimated_volume_m3:.1f} m³")
        
        return geometric_model
    
    def generate_metadata_report(self, 
                               signature: SpatialSignature,
                               volumetric_field: VolumetricField,
                               geometric_model: GeometricModel,
                               sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ETAPA 5: Generar metadatos completos y reporte de validación.
        
        CRÍTICO: Acompañar SIEMPRE con metadatos para rigor científico.
        """
        
        return {
            "inference_metadata": {
                "inference_level": volumetric_field.inference_level.value,
                "morphological_classification": volumetric_field.morphological_class.value,
                "reconstruction_method": geometric_model.reconstruction_method,
                "epistemological_framework": "espacios_posibilidad_geometrica_consistentes_firmas_fisicas_persistentes"
            },
            
            "spatial_signature": {
                "area_m2": signature.area_m2,
                "elongation_ratio": signature.elongation_ratio,
                "symmetry_index": signature.symmetry_index,
                "thermal_amplitude_c": signature.thermal_amplitude,
                "multitemporal_coherence": signature.multitemporal_coherence,
                "signature_confidence": signature.signature_confidence,
                "sensor_convergence": signature.sensor_convergence
            },
            
            "volumetric_properties": {
                "voxel_resolution_m": volumetric_field.voxel_size_m,
                "grid_dimensions": volumetric_field.dimensions,
                "confidence_layers": volumetric_field.confidence_layers,
                "total_voxels": np.prod(volumetric_field.dimensions),
                "active_voxels": int(np.sum(volumetric_field.probability_volume > 0.3))
            },
            
            "geometric_properties": {
                "estimated_volume_m3": geometric_model.estimated_volume_m3,
                "max_height_m": geometric_model.max_height_m,
                "footprint_area_m2": geometric_model.footprint_area_m2,
                "surface_area_m2": geometric_model.surface_area_m2,
                "vertex_count": len(geometric_model.vertices),
                "face_count": len(geometric_model.faces),
                "symmetries_detected": geometric_model.symmetries_detected
            },
            
            "uncertainty_analysis": {
                "mean_uncertainty": float(np.mean(volumetric_field.uncertainty_field)),
                "max_uncertainty": float(np.max(volumetric_field.uncertainty_field)),
                "uncertainty_zones": {
                    "high_uncertainty_percentage": float(np.sum(volumetric_field.uncertainty_field > 0.7) / volumetric_field.uncertainty_field.size * 100),
                    "medium_uncertainty_percentage": float(np.sum((volumetric_field.uncertainty_field > 0.4) & (volumetric_field.uncertainty_field <= 0.7)) / volumetric_field.uncertainty_field.size * 100),
                    "low_uncertainty_percentage": float(np.sum(volumetric_field.uncertainty_field <= 0.4) / volumetric_field.uncertainty_field.size * 100)
                }
            },
            
            "sensor_integration": {
                "sensors_involved": list(sensor_data.keys()),
                "sensor_count": len(sensor_data),
                "cross_sensor_correlation": signature.sensor_convergence,
                "temporal_persistence_index": signature.temporal_persistence
            },
            
            "validation_requirements": {
                "recommended_validation": [
                    "geofisica_GPR_magnetometria_area_alta_probabilidad",
                    "LIDAR_alta_resolucion_validacion_geometrica",
                    "analisis_multitemporal_confirmacion_persistencia",
                    "contexto_arqueologico_regional_interpretacion"
                ],
                "field_work_priority": "high" if signature.signature_confidence > 0.7 else "medium",
                "geophysical_methods": self._recommend_geophysical_methods(volumetric_field.morphological_class),
                "excavation_guidance": self._generate_excavation_guidance(geometric_model)
            },
            
            "scientific_disclaimers": {
                "reconstruction_level": "Modelo volumétrico inferido a partir de firmas espaciales multicapas",
                "accuracy_statement": "Forma aproximada con escala correcta - NO detalles arquitectónicos",
                "uncertainty_explicit": f"Incertidumbre promedio: {np.mean(volumetric_field.uncertainty_field):.1%}",
                "validation_required": "Todas las inferencias requieren validación geofísica independiente",
                "epistemological_note": "Sistema produce espacios de posibilidad geométrica, no reconstrucciones definitivas"
            },
            
            "comparative_analysis": {
                "volume_order_of_magnitude": self._classify_volume_magnitude(geometric_model.estimated_volume_m3),
                "morphological_precedents": self._find_morphological_precedents(volumetric_field.morphological_class),
                "regional_context_needed": True,
                "cultural_interpretation_excluded": "Sistema NO proporciona interpretación cultural o cronológica"
            }
        }
    
    def _recommend_geophysical_methods(self, morphology: MorphologicalClass) -> List[str]:
        """Recomendar métodos geofísicos según morfología detectada."""
        
        recommendations = ["GPR_ground_penetrating_radar"]  # Siempre recomendado
        
        if morphology == MorphologicalClass.TRUNCATED_PYRAMIDAL:
            recommendations.extend(["magnetometria", "resistividad_electrica"])
        elif morphology == MorphologicalClass.CAVITY_VOID:
            recommendations.extend(["sísmica_refracción", "gravimetría_microgravedad"])
        elif morphology == MorphologicalClass.LINEAR_COMPACT:
            recommendations.extend(["magnetometria_gradiente", "conductividad_electromagnetica"])
        elif morphology == MorphologicalClass.EMBANKMENT_MOUND:
            recommendations.extend(["resistividad_electrica", "sísmica_refracción"])
        
        return recommendations
    
    def _generate_excavation_guidance(self, model: GeometricModel) -> Dict[str, Any]:
        """Generar guía para excavación basada en modelo geométrico."""
        
        if len(model.vertices) == 0:
            return {"status": "insufficient_data_for_guidance"}
        
        # Identificar zonas de alta confianza para excavación prioritaria
        high_conf_vertices = model.confidence_zones.get('high_confidence', [])
        
        if high_conf_vertices:
            # Calcular centro de masa de zona de alta confianza
            high_conf_coords = model.vertices[high_conf_vertices]
            center_of_mass = np.mean(high_conf_coords, axis=0)
            
            return {
                "priority_excavation_center": {
                    "x_offset_m": float(center_of_mass[0]),
                    "y_offset_m": float(center_of_mass[1]),
                    "suggested_depth_m": min(float(center_of_mass[2]), model.max_height_m * 0.7)
                },
                "excavation_strategy": "systematic_grid_from_high_confidence_center",
                "grid_spacing_m": max(2.0, model.footprint_area_m2**0.5 / 10),
                "maximum_depth_recommendation": model.max_height_m * 1.2,
                "area_priority_zones": len(high_conf_vertices)
            }
        else:
            return {
                "status": "low_confidence_systematic_survey_recommended",
                "survey_method": "regular_grid_geophysical_survey",
                "grid_spacing_m": 5.0
            }
    
    def _classify_volume_magnitude(self, volume_m3: float) -> str:
        """Clasificar orden de magnitud del volumen."""
        
        if volume_m3 < 100:
            return "small_structure_individual_feature"
        elif volume_m3 < 1000:
            return "medium_structure_building_scale"
        elif volume_m3 < 10000:
            return "large_structure_complex_scale"
        else:
            return "massive_structure_monumental_scale"
    
    def _find_morphological_precedents(self, morphology: MorphologicalClass) -> List[str]:
        """Encontrar precedentes morfológicos (NO culturales)."""
        
        precedents = {
            MorphologicalClass.TRUNCATED_PYRAMIDAL: [
                "plataformas_ceremoniales_mesoamericanas",
                "tells_arqueologicos_oriente_medio",
                "montículos_artificiales_norteamerica"
            ],
            MorphologicalClass.STEPPED_PLATFORM: [
                "terrazas_agricolas_andinas",
                "plataformas_escalonadas_asia_sudeste",
                "ziggurats_mesopotamicos"
            ],
            MorphologicalClass.LINEAR_COMPACT: [
                "caminos_antiguos_enterrados",
                "canales_irrigacion_prehistoricos",
                "muros_perimetrales_asentamientos"
            ],
            MorphologicalClass.CAVITY_VOID: [
                "cámaras_subterraneas_artificiales",
                "sistemas_almacenamiento_subterraneo",
                "espacios_rituales_excavados"
            ],
            MorphologicalClass.EMBANKMENT_MOUND: [
                "montículos_funerarios_diversos",
                "terraplenes_defensivos_antiguos",
                "plataformas_habitacionales_elevadas"
            ],
            MorphologicalClass.ORTHOGONAL_NETWORK: [
                "trazados_urbanos_planificados",
                "sistemas_campos_elevados",
                "redes_canales_ortogonales"
            ]
        }
        
        return precedents.get(morphology, ["sin_precedentes_morfologicos_claros"])
    
    def process_anomaly_complete(self, 
                               anomaly_data: Dict[str, Any],
                               layer_results: Dict[str, Any],
                               bounds: Tuple[float, float, float, float]) -> Dict[str, Any]:
        """
        Pipeline completo de inferencia volumétrica para una anomalía.
        
        Ejecuta las 5 etapas del proceso y retorna resultado completo.
        """
        
        logger.info(f"Iniciando inferencia volumétrica completa para anomalía: {anomaly_data.get('id', 'unknown')}")
        
        try:
            # ETAPA 1: Extracción de firma espacial
            signature = self.extract_spatial_signature(anomaly_data, layer_results)
            
            # ETAPA 2: Clasificación morfológica
            morphology = self.classify_morphology(signature)
            
            # ETAPA 3: Inferencia volumétrica probabilística
            volumetric_field = self.generate_volumetric_field(signature, morphology, bounds)
            
            # ETAPA 4: Reconstrucción geométrica mínima
            geometric_model = self.extract_geometric_model(volumetric_field)
            
            # ETAPA 5: Metadatos y validación
            metadata_report = self.generate_metadata_report(
                signature, volumetric_field, geometric_model, layer_results
            )
            
            result = {
                "inference_successful": True,
                "anomaly_id": anomaly_data.get('id', 'unknown'),
                "morphological_class": morphology.value,
                "inference_level": self.inference_level.value,
                "spatial_signature": signature,
                "volumetric_field": volumetric_field,
                "geometric_model": geometric_model,
                "metadata_report": metadata_report,
                "processing_summary": {
                    "pipeline_stages_completed": 5,
                    "total_vertices_generated": len(geometric_model.vertices),
                    "estimated_volume_m3": geometric_model.estimated_volume_m3,
                    "confidence_assessment": signature.signature_confidence,
                    "morphological_classification": morphology.value
                }
            }
            
            logger.info(f"Inferencia volumétrica completada: {morphology.value}, volumen: {geometric_model.estimated_volume_m3:.1f} m³")
            
            return result
            
        except Exception as e:
            logger.error(f"Error en inferencia volumétrica: {e}")
            return {
                "inference_successful": False,
                "error": str(e),
                "anomaly_id": anomaly_data.get('id', 'unknown')
            }