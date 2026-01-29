#!/usr/bin/env python3
"""
ArcheoScope GPR (Ground Penetrating Radar) Connector
====================================================

Integración de datos GPR públicos para detección de anomalías subsuperficiales.

🎯 OBJETIVO:
- Usar GPR como evidencia secundaria fuerte
- Detectar cavidades, estructuras enterradas, anomalías de humedad
- Comparar firmas GPR con patrones conocidos

📊 FUENTES DE DATOS:
1. Zenodo - Datasets GPR arqueológicos públicos
2. GPR sintético simulado (gprMax)
3. Patrones de referencia pre-calculados

🔑 CASOS DE USO:
- Zonas áridas/semiáridas: Detectar muros enterrados
- Mesetas rocosas: Identificar cavidades
- Llanuras: Estructuras subsuperficiales

⚠️ LIMITACIONES:
- GPR NO está disponible en tiempo real
- Se usa como validador/prior, no como sensor primario
- Requiere descarga previa de datasets
"""

import os
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import json
from pathlib import Path

from .base_connector import BaseConnector
from ..instrument_status import InstrumentResult, InstrumentStatus

logger = logging.getLogger(__name__)


class GPRSignatureType(Enum):
    """Tipos de firmas GPR detectables."""
    CAVITY = "cavity"                    # Cavidad/hueco
    BURIED_WALL = "buried_wall"          # Muro enterrado
    FOUNDATION = "foundation"            # Fundación
    MOISTURE_ANOMALY = "moisture"        # Anomalía de humedad
    COMPACTION = "compaction"            # Compactación diferencial
    VOID_SPACE = "void_space"            # Espacio vacío
    UNKNOWN = "unknown"


@dataclass
class GPRPattern:
    """Patrón de referencia GPR."""
    signature_type: GPRSignatureType
    depth_range_m: Tuple[float, float]
    amplitude_threshold: float
    frequency_mhz: float
    confidence: float
    archaeological_context: str
    reference_site: Optional[str] = None


class GPRConnector(BaseConnector):
    """
    Conector para datos GPR públicos y sintéticos.
    
    FILOSOFÍA:
    - GPR como validador, no como sensor primario
    - Usar patrones pre-calculados de sitios conocidos
    - Simular firmas cuando no hay datos reales
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Inicializar conector GPR.
        
        Args:
            cache_dir: Directorio para cachear datasets GPR descargados
        """
        super().__init__()
        
        # Directorio de caché para datasets GPR
        if cache_dir is None:
            cache_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'cache', 'gpr_data')
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cargar patrones de referencia
        self.reference_patterns = self._load_reference_patterns()
        
        # Datasets públicos conocidos
        self.public_datasets = {
            'zenodo_archaeological_gpr': {
                'url': 'https://zenodo.org/communities/gpr-archaeology',
                'description': 'Archaeological GPR datasets',
                'format': 'various'
            },
            'gpr_archaeological_prospection': {
                'url': 'https://zenodo.org/record/4589234',
                'description': 'GPR data from archaeological sites',
                'format': 'SEG-Y, DZT'
            }
        }
        
        logger.info(f"GPR Connector initialized with {len(self.reference_patterns)} reference patterns")
    
    def _load_reference_patterns(self) -> List[GPRPattern]:
        """
        Cargar patrones de referencia GPR de sitios conocidos.
        
        Estos patrones se usan para comparación con nuevas anomalías.
        """
        patterns = [
            # Cavidades (prioridad alta para arqueología)
            GPRPattern(
                signature_type=GPRSignatureType.CAVITY,
                depth_range_m=(0.5, 5.0),
                amplitude_threshold=0.7,
                frequency_mhz=400,
                confidence=0.85,
                archaeological_context="Cámaras subterráneas, tumbas, cisternas",
                reference_site="Tell sites, Middle East"
            ),
            
            # Muros enterrados
            GPRPattern(
                signature_type=GPRSignatureType.BURIED_WALL,
                depth_range_m=(0.3, 2.0),
                amplitude_threshold=0.65,
                frequency_mhz=500,
                confidence=0.80,
                archaeological_context="Fundaciones, muros de ciudades antiguas",
                reference_site="Roman urban sites"
            ),
            
            # Fundaciones
            GPRPattern(
                signature_type=GPRSignatureType.FOUNDATION,
                depth_range_m=(0.5, 3.0),
                amplitude_threshold=0.60,
                frequency_mhz=400,
                confidence=0.75,
                archaeological_context="Plataformas ceremoniales, edificios",
                reference_site="Mesoamerican sites"
            ),
            
            # Anomalías de humedad (túneles, sistemas hidráulicos)
            GPRPattern(
                signature_type=GPRSignatureType.MOISTURE_ANOMALY,
                depth_range_m=(1.0, 8.0),
                amplitude_threshold=0.55,
                frequency_mhz=250,
                confidence=0.70,
                archaeological_context="Túneles, acueductos, sistemas de drenaje",
                reference_site="Andean hydraulic systems"
            ),
            
            # Compactación diferencial
            GPRPattern(
                signature_type=GPRSignatureType.COMPACTION,
                depth_range_m=(0.2, 1.5),
                amplitude_threshold=0.50,
                frequency_mhz=600,
                confidence=0.65,
                archaeological_context="Caminos antiguos, plazas",
                reference_site="Inca road network"
            ),
        ]
        
        return patterns
    
    def get_gpr_similarity_score(
        self,
        lat: float,
        lon: float,
        environment_type: str,
        target_depth_m: float = 3.0
    ) -> InstrumentResult:
        """
        Calcular score de similitud GPR basado en patrones conocidos.
        
        Args:
            lat: Latitud
            lon: Longitud
            environment_type: Tipo de ambiente (desert, semi_arid, etc.)
            target_depth_m: Profundidad objetivo de exploración
        
        Returns:
            InstrumentResult con score de similitud GPR
        """
        try:
            # Verificar si hay datos GPR reales en caché para esta región
            cached_data = self._check_cached_gpr_data(lat, lon)
            
            if cached_data:
                return self._process_real_gpr_data(cached_data, lat, lon, environment_type)
            
            # Si no hay datos reales, calcular similitud con patrones
            similarity_score = self._calculate_pattern_similarity(
                lat, lon, environment_type, target_depth_m
            )
            
            return InstrumentResult.create_success(
                instrument_name="GPR_Pattern_Matching",
                measurement_type="subsurface_similarity",
                value=similarity_score,
                unit="similarity_score",
                confidence=0.6,  # Menor confianza porque es basado en patrones
                source="reference_patterns",
                reason=f"Pattern-based similarity for {environment_type} environment"
            )
            
        except Exception as e:
            logger.error(f"Error in GPR similarity calculation: {e}")
            return InstrumentResult.create_failed(
                instrument_name="GPR_Pattern_Matching",
                measurement_type="subsurface_similarity",
                reason=f"GPR_ERROR: {str(e)}"
            )
    
    def _check_cached_gpr_data(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Verificar si hay datos GPR reales en caché para esta región.
        
        Args:
            lat: Latitud
            lon: Longitud
        
        Returns:
            Datos GPR si existen, None si no
        """
        # Buscar archivos en caché que coincidan con la región
        # Formato: gpr_data_{lat}_{lon}.json
        lat_rounded = round(lat, 2)
        lon_rounded = round(lon, 2)
        
        cache_file = self.cache_dir / f"gpr_data_{lat_rounded}_{lon_rounded}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error reading cached GPR data: {e}")
                return None
        
        return None
    
    def _process_real_gpr_data(
        self,
        gpr_data: Dict[str, Any],
        lat: float,
        lon: float,
        environment_type: str
    ) -> InstrumentResult:
        """
        Procesar datos GPR reales descargados.
        
        Args:
            gpr_data: Datos GPR del caché
            lat: Latitud
            lon: Longitud
            environment_type: Tipo de ambiente
        
        Returns:
            InstrumentResult con análisis de datos reales
        """
        # Extraer métricas clave de los datos GPR
        depth_slices = gpr_data.get('depth_slices', [])
        reflectivity_map = gpr_data.get('reflectivity_map', [])
        
        if not depth_slices:
            return InstrumentResult.create_failed(
                instrument_name="GPR_Real_Data",
                measurement_type="subsurface_analysis",
                reason="NO_DEPTH_SLICES"
            )
        
        # Calcular anomalías
        anomaly_score = self._detect_gpr_anomalies(depth_slices, reflectivity_map)
        
        return InstrumentResult.create_success(
            instrument_name="GPR_Real_Data",
            measurement_type="subsurface_anomaly",
            value=anomaly_score,
            unit="anomaly_score",
            confidence=0.9,  # Alta confianza en datos reales
            source=gpr_data.get('source', 'cached_dataset'),
            acquisition_date=gpr_data.get('acquisition_date'),
            reason=f"Real GPR data analysis for {environment_type}"
        )
    
    def _detect_gpr_anomalies(
        self,
        depth_slices: List[Dict[str, Any]],
        reflectivity_map: List[float]
    ) -> float:
        """
        Detectar anomalías en datos GPR reales.
        
        Args:
            depth_slices: Slices de profundidad
            reflectivity_map: Mapa de reflectividad
        
        Returns:
            Score de anomalía (0.0-1.0)
        """
        anomaly_indicators = []
        
        for slice_data in depth_slices:
            depth_m = slice_data.get('depth_m', 0)
            mean_amplitude = slice_data.get('mean_amplitude', 0)
            variance = slice_data.get('variance', 0)
            
            # Detectar anomalías por profundidad
            if 0.5 <= depth_m <= 5.0:  # Rango arqueológico típico
                # Alta amplitud + baja varianza = posible estructura
                if mean_amplitude > 0.6 and variance < 0.2:
                    anomaly_indicators.append(0.8)
                # Alta varianza = posible cavidad
                elif variance > 0.5:
                    anomaly_indicators.append(0.7)
        
        if not anomaly_indicators:
            return 0.0
        
        return np.mean(anomaly_indicators)
    
    def _calculate_pattern_similarity(
        self,
        lat: float,
        lon: float,
        environment_type: str,
        target_depth_m: float
    ) -> float:
        """
        Calcular similitud con patrones de referencia.
        
        Esta función usa contexto geográfico y ambiental para estimar
        la probabilidad de encontrar firmas GPR similares a sitios conocidos.
        
        Args:
            lat: Latitud
            lon: Longitud
            environment_type: Tipo de ambiente
            target_depth_m: Profundidad objetivo
        
        Returns:
            Score de similitud (0.0-1.0)
        """
        # Mapeo de ambientes a tipos de firma más probables
        environment_signature_affinity = {
            'desert': [GPRSignatureType.BURIED_WALL, GPRSignatureType.FOUNDATION],
            'semi_arid': [GPRSignatureType.CAVITY, GPRSignatureType.BURIED_WALL, GPRSignatureType.COMPACTION],
            'grassland': [GPRSignatureType.FOUNDATION, GPRSignatureType.COMPACTION],
            'coastal': [GPRSignatureType.MOISTURE_ANOMALY, GPRSignatureType.BURIED_WALL],
            'mountain': [GPRSignatureType.CAVITY, GPRSignatureType.FOUNDATION],
        }
        
        # Obtener firmas afines al ambiente
        affine_signatures = environment_signature_affinity.get(environment_type, [])
        
        if not affine_signatures:
            return 0.3  # Score base bajo si no hay afinidad conocida
        
        # Filtrar patrones por profundidad objetivo
        relevant_patterns = [
            p for p in self.reference_patterns
            if p.signature_type in affine_signatures
            and p.depth_range_m[0] <= target_depth_m <= p.depth_range_m[1]
        ]
        
        if not relevant_patterns:
            return 0.4  # Score ligeramente mayor si hay afinidad pero no en profundidad
        
        # Calcular score ponderado por confianza de patrones
        weighted_scores = [p.confidence for p in relevant_patterns]
        
        return np.mean(weighted_scores)
    
    def get_recommended_gpr_frequency(self, environment_type: str, target_depth_m: float) -> Dict[str, Any]:
        """
        Recomendar frecuencia GPR óptima según ambiente y profundidad.
        
        Args:
            environment_type: Tipo de ambiente
            target_depth_m: Profundidad objetivo
        
        Returns:
            Recomendación de frecuencia y configuración
        """
        # Reglas generales:
        # - Mayor frecuencia = mayor resolución, menor penetración
        # - Menor frecuencia = menor resolución, mayor penetración
        
        if target_depth_m < 1.0:
            frequency_mhz = 900
            resolution_cm = 5
        elif target_depth_m < 3.0:
            frequency_mhz = 400
            resolution_cm = 10
        elif target_depth_m < 6.0:
            frequency_mhz = 200
            resolution_cm = 20
        else:
            frequency_mhz = 100
            resolution_cm = 40
        
        # Ajustar por tipo de suelo
        soil_attenuation = {
            'desert': 1.0,      # Baja atenuación
            'semi_arid': 1.1,
            'grassland': 1.3,
            'coastal': 1.5,     # Alta atenuación (humedad)
            'mountain': 1.2,
        }
        
        attenuation_factor = soil_attenuation.get(environment_type, 1.2)
        adjusted_frequency = frequency_mhz / attenuation_factor
        
        return {
            'recommended_frequency_mhz': round(adjusted_frequency),
            'expected_resolution_cm': resolution_cm,
            'max_penetration_m': target_depth_m * 1.2,
            'environment_factor': attenuation_factor,
            'notes': f"Optimized for {environment_type} at {target_depth_m}m depth"
        }
    
    def download_public_dataset(self, dataset_name: str, target_region: Optional[Tuple[float, float]] = None) -> bool:
        """
        Descargar dataset GPR público desde Zenodo u otras fuentes.
        
        Args:
            dataset_name: Nombre del dataset
            target_region: Región objetivo (lat, lon) opcional
        
        Returns:
            True si la descarga fue exitosa
        """
        if dataset_name not in self.public_datasets:
            logger.error(f"Unknown dataset: {dataset_name}")
            return False
        
        dataset_info = self.public_datasets[dataset_name]
        
        logger.info(f"Downloading GPR dataset: {dataset_name}")
        logger.info(f"URL: {dataset_info['url']}")
        logger.info(f"Format: {dataset_info['format']}")
        
        # TODO: Implementar descarga real usando requests
        # Por ahora, solo logging
        logger.warning("Dataset download not implemented yet. Manual download required.")
        logger.info(f"Please download from: {dataset_info['url']}")
        logger.info(f"Save to: {self.cache_dir}")
        
        return False
    
    def simulate_gpr_signature(
        self,
        signature_type: GPRSignatureType,
        depth_m: float,
        width_m: float = 2.0
    ) -> Dict[str, Any]:
        """
        Simular firma GPR sintética usando modelo simplificado.
        
        Útil para:
        - Validar hipótesis sin datos reales
        - Entrenar detectores
        - Generar patrones de referencia
        
        Args:
            signature_type: Tipo de firma a simular
            depth_m: Profundidad del objetivo
            width_m: Ancho del objetivo
        
        Returns:
            Datos GPR sintéticos
        """
        # Parámetros de simulación
        time_window_ns = 100  # Ventana de tiempo en nanosegundos
        samples = 512
        
        # Generar eje de tiempo
        time_axis = np.linspace(0, time_window_ns, samples)
        
        # Velocidad típica en suelo (m/ns)
        velocity = 0.1
        
        # Calcular tiempo de llegada
        two_way_time = 2 * depth_m / velocity
        
        # Generar firma según tipo
        if signature_type == GPRSignatureType.CAVITY:
            # Cavidad: reflexión fuerte + reverberaciones
            amplitude = 0.8
            signal = amplitude * np.exp(-((time_axis - two_way_time) ** 2) / (2 * 5 ** 2))
            # Agregar reverberaciones
            signal += 0.3 * np.exp(-((time_axis - two_way_time - 10) ** 2) / (2 * 3 ** 2))
            
        elif signature_type == GPRSignatureType.BURIED_WALL:
            # Muro: reflexión nítida, lineal
            amplitude = 0.7
            signal = amplitude * np.exp(-((time_axis - two_way_time) ** 2) / (2 * 3 ** 2))
            
        elif signature_type == GPRSignatureType.FOUNDATION:
            # Fundación: reflexión moderada, amplia
            amplitude = 0.6
            signal = amplitude * np.exp(-((time_axis - two_way_time) ** 2) / (2 * 8 ** 2))
            
        else:
            # Genérico
            amplitude = 0.5
            signal = amplitude * np.exp(-((time_axis - two_way_time) ** 2) / (2 * 5 ** 2))
        
        # Agregar ruido
        noise = np.random.normal(0, 0.05, samples)
        signal += noise
        
        return {
            'signature_type': signature_type.value,
            'depth_m': depth_m,
            'width_m': width_m,
            'time_axis_ns': time_axis.tolist(),
            'amplitude': signal.tolist(),
            'peak_amplitude': float(np.max(signal)),
            'two_way_time_ns': two_way_time,
            'simulated': True
        }


# Instancia global
gpr_connector = GPRConnector()
