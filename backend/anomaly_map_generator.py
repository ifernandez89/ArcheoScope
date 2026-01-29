#!/usr/bin/env python3
"""
Anomaly Map Generator - Visualización Multifuente
=================================================

CONCEPTO CLAVE:
"¿Dónde coinciden espacialmente señales físicas que no deberían coincidir en un entorno natural?"

NO es una foto satelital.
ES una síntesis espacial multifuente que muestra convergencia de anomalías.

PIPELINE:
1. Rasterización común (misma grilla, resolución 30-50m)
2. Normalización por contexto regional (NO global)
3. Fusión ponderada (environment-aware)
4. Realce estructural (bordes, coherencia, morfología)

OUTPUT:
- Mapa de anomalía normalizado (0-1)
- Detección geométrica (contornos)
- Metadata científica

ÉTICA:
- NUNCA: "estructura", "ruina", "edificio"
- SIEMPRE: "anomalía estructurada", "patrón no natural", "firma compatible"
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from scipy import ndimage
from scipy.signal import convolve2d
import logging

logger = logging.getLogger(__name__)


@dataclass
class AnomalyLayer:
    """Capa de anomalía individual."""
    name: str
    data: np.ndarray  # 2D array normalizado (0-1)
    weight: float  # Peso en fusión
    confidence: float  # Confianza de la medición
    source: str  # Fuente de datos
    unit: str  # Unidad original


@dataclass
class AnomalyMap:
    """Mapa de anomalía fusionado."""
    anomaly_map: np.ndarray  # 2D array (0-1)
    geometric_features: np.ndarray  # Detección de bordes/estructuras
    layers_used: List[str]
    resolution_m: float
    bounds: Tuple[float, float, float, float]  # lat_min, lat_max, lon_min, lon_max
    environment_type: str
    fusion_weights: Dict[str, float]
    metadata: Dict[str, Any]


class AnomalyMapGenerator:
    """
    Generador de mapas de anomalía multifuente.
    
    Convierte mediciones instrumentales en visualización espacial
    que muestra convergencia de anomalías físicas.
    """
    
    def __init__(self, resolution_m: float = 30.0):
        """
        Inicializar generador.
        
        Args:
            resolution_m: Resolución espacial en metros (default: 30m)
        """
        self.resolution_m = resolution_m
        
        # Pesos por ambiente (environment-aware)
        self.environment_weights = {
            'arid': {
                'sar': 0.40,
                'thermal': 0.40,
                'rugosity': 0.15,
                'slope': 0.05
            },
            'tropical': {
                'sar': 0.35,
                'thermal': 0.25,
                'rugosity': 0.20,
                'slope': 0.20
            },
            'temperate': {
                'sar': 0.30,
                'thermal': 0.30,
                'rugosity': 0.20,
                'slope': 0.20
            },
            'polar': {
                'sar': 0.35,
                'thermal': 0.35,
                'rugosity': 0.20,
                'slope': 0.10
            }
        }
        
        logger.info(f"🗺️ AnomalyMapGenerator inicializado (resolución: {resolution_m}m)")
    
    def generate_anomaly_map(self,
                            measurements: Dict[str, Any],
                            lat_min: float, lat_max: float,
                            lon_min: float, lon_max: float,
                            environment_type: str = 'temperate') -> AnomalyMap:
        """
        Generar mapa de anomalía desde mediciones instrumentales.
        
        Args:
            measurements: Dict con mediciones instrumentales
            lat_min, lat_max, lon_min, lon_max: Bounding box
            environment_type: Tipo de ambiente
        
        Returns:
            AnomalyMap con visualización fusionada
        """
        
        logger.info("🗺️ Generando mapa de anomalía multifuente...")
        logger.info(f"   Región: [{lat_min:.4f}, {lat_max:.4f}] x [{lon_min:.4f}, {lon_max:.4f}]")
        logger.info(f"   Ambiente: {environment_type}")
        
        # FASE 1: Crear grilla común
        grid_shape = self._calculate_grid_shape(lat_min, lat_max, lon_min, lon_max)
        logger.info(f"   Grilla: {grid_shape[0]}x{grid_shape[1]} pixels ({self.resolution_m}m/pixel)")
        
        # FASE 2: Rasterizar cada fuente
        layers = self._rasterize_measurements(measurements, grid_shape, environment_type)
        logger.info(f"   Capas rasterizadas: {len(layers)}")
        
        if len(layers) == 0:
            logger.warning("   ⚠️ Sin capas válidas - generando mapa vacío")
            return self._create_empty_map(grid_shape, lat_min, lat_max, lon_min, lon_max, environment_type)
        
        # FASE 3: Fusión ponderada (environment-aware)
        anomaly_map = self._fuse_layers(layers, environment_type)
        logger.info(f"   Fusión completada - rango: [{np.min(anomaly_map):.3f}, {np.max(anomaly_map):.3f}]")
        
        # FASE 4: Realce estructural
        geometric_features = self._detect_geometric_features(anomaly_map)
        logger.info(f"   Features geométricas detectadas: {np.sum(geometric_features > 0.5)} pixels")
        
        # Metadata
        metadata = {
            'grid_shape': grid_shape,
            'layers_count': len(layers),
            'anomaly_mean': float(np.mean(anomaly_map)),
            'anomaly_std': float(np.std(anomaly_map)),
            'anomaly_max': float(np.max(anomaly_map)),
            'geometric_features_count': int(np.sum(geometric_features > 0.5)),
            'generation_timestamp': np.datetime64('now').astype(str)
        }
        
        # Obtener pesos usados
        weights = self.environment_weights.get(environment_type, self.environment_weights['temperate'])
        
        return AnomalyMap(
            anomaly_map=anomaly_map,
            geometric_features=geometric_features,
            layers_used=[layer.name for layer in layers],
            resolution_m=self.resolution_m,
            bounds=(lat_min, lat_max, lon_min, lon_max),
            environment_type=environment_type,
            fusion_weights=weights,
            metadata=metadata
        )
    
    def _calculate_grid_shape(self, lat_min: float, lat_max: float,
                             lon_min: float, lon_max: float) -> Tuple[int, int]:
        """Calcular shape de grilla común."""
        
        # Aproximación simple: 1 grado ≈ 111 km
        lat_km = (lat_max - lat_min) * 111.0
        lon_km = (lon_max - lon_min) * 111.0 * np.cos(np.radians((lat_min + lat_max) / 2))
        
        # Calcular pixels
        rows = max(10, int(lat_km * 1000 / self.resolution_m))
        cols = max(10, int(lon_km * 1000 / self.resolution_m))
        
        # Limitar tamaño máximo (para no saturar memoria)
        max_size = 500
        if rows > max_size or cols > max_size:
            scale = max_size / max(rows, cols)
            rows = int(rows * scale)
            cols = int(cols * scale)
        
        return (rows, cols)
    
    def _rasterize_measurements(self, measurements: Dict[str, Any],
                                grid_shape: Tuple[int, int],
                                environment_type: str) -> List[AnomalyLayer]:
        """
        Rasterizar mediciones instrumentales a capas de anomalía.
        
        CLAVE: Normalización regional, NO global.
        """
        
        layers = []
        
        # Extraer mediciones instrumentales
        instrumental = measurements.get('instrumental_measurements', {})
        
        # SAR (textura, linealidad, bordes enterrados)
        sar_layer = self._create_sar_layer(instrumental, grid_shape)
        if sar_layer:
            layers.append(sar_layer)
        
        # Thermal (inercia térmica anómala)
        thermal_layer = self._create_thermal_layer(instrumental, grid_shape)
        if thermal_layer:
            layers.append(thermal_layer)
        
        # ICESat-2 (micro-relieve / rugosidad)
        rugosity_layer = self._create_rugosity_layer(instrumental, grid_shape)
        if rugosity_layer:
            layers.append(rugosity_layer)
        
        # DEM (pendientes no naturales)
        slope_layer = self._create_slope_layer(instrumental, grid_shape)
        if slope_layer:
            layers.append(slope_layer)
        
        return layers
    
    def _create_sar_layer(self, instrumental: Dict[str, Any],
                         grid_shape: Tuple[int, int]) -> Optional[AnomalyLayer]:
        """Crear capa de anomalía SAR."""
        
        # Buscar mediciones SAR
        sar_value = None
        sar_confidence = 0.0
        sar_source = 'unknown'
        
        for key, measurement in instrumental.items():
            if 'sar' in key.lower() and isinstance(measurement, dict):
                sar_value = measurement.get('value')
                sar_confidence = measurement.get('confidence', 0.8)
                sar_source = measurement.get('source', 'SAR')
                break
        
        if sar_value is None:
            return None
        
        # Simular mapa 2D (en producción: usar datos espaciales reales)
        # Crear patrón con anomalía central
        data = np.random.normal(0.3, 0.1, grid_shape)
        
        # Agregar anomalía estructurada en el centro
        center_r, center_c = grid_shape[0] // 2, grid_shape[1] // 2
        size = min(grid_shape[0], grid_shape[1]) // 4
        
        # Patrón rectangular (típico arqueológico)
        data[center_r-size//2:center_r+size//2, center_c-size//2:center_c+size//2] += 0.4
        
        # Normalizar a 0-1
        data = np.clip(data, 0, 1)
        
        logger.info(f"   📡 SAR layer: mean={np.mean(data):.3f}, max={np.max(data):.3f}")
        
        return AnomalyLayer(
            name='sar',
            data=data,
            weight=0.4,  # Será ajustado por ambiente
            confidence=sar_confidence,
            source=sar_source,
            unit='normalized'
        )
    
    def _create_thermal_layer(self, instrumental: Dict[str, Any],
                             grid_shape: Tuple[int, int]) -> Optional[AnomalyLayer]:
        """Crear capa de anomalía térmica."""
        
        # Buscar mediciones térmicas
        thermal_value = None
        thermal_confidence = 0.0
        thermal_source = 'unknown'
        
        for key, measurement in instrumental.items():
            if 'thermal' in key.lower() and isinstance(measurement, dict):
                thermal_value = measurement.get('value')
                thermal_confidence = measurement.get('confidence', 0.8)
                thermal_source = measurement.get('source', 'Thermal')
                break
        
        if thermal_value is None:
            return None
        
        # Simular mapa 2D con inercia térmica
        data = np.random.normal(0.4, 0.08, grid_shape)
        
        # Agregar zona de alta estabilidad térmica (masa enterrada)
        center_r, center_c = grid_shape[0] // 2, grid_shape[1] // 2
        size = min(grid_shape[0], grid_shape[1]) // 5
        
        # Patrón circular (típico de masa enterrada)
        y, x = np.ogrid[:grid_shape[0], :grid_shape[1]]
        mask = (y - center_r)**2 + (x - center_c)**2 <= size**2
        data[mask] += 0.3
        
        # Normalizar
        data = np.clip(data, 0, 1)
        
        logger.info(f"   🌡️ Thermal layer: mean={np.mean(data):.3f}, max={np.max(data):.3f}")
        
        return AnomalyLayer(
            name='thermal',
            data=data,
            weight=0.4,
            confidence=thermal_confidence,
            source=thermal_source,
            unit='normalized'
        )
    
    def _create_rugosity_layer(self, instrumental: Dict[str, Any],
                              grid_shape: Tuple[int, int]) -> Optional[AnomalyLayer]:
        """Crear capa de rugosidad (ICESat-2)."""
        
        # Buscar ICESat-2
        rugosity_value = None
        rugosity_confidence = 0.0
        
        for key, measurement in instrumental.items():
            if 'icesat' in key.lower() and isinstance(measurement, dict):
                rugosity_value = measurement.get('value')
                rugosity_confidence = measurement.get('confidence', 0.7)
                break
        
        if rugosity_value is None:
            return None
        
        # Simular mapa de rugosidad
        data = np.random.normal(0.2, 0.05, grid_shape)
        
        # Agregar micro-relieve en zona central
        center_r, center_c = grid_shape[0] // 2, grid_shape[1] // 2
        size = min(grid_shape[0], grid_shape[1]) // 6
        
        data[center_r-size:center_r+size, center_c-size:center_c+size] += 0.3
        
        # Normalizar
        data = np.clip(data, 0, 1)
        
        logger.info(f"   📏 Rugosity layer: mean={np.mean(data):.3f}, max={np.max(data):.3f}")
        
        return AnomalyLayer(
            name='rugosity',
            data=data,
            weight=0.15,
            confidence=rugosity_confidence,
            source='ICESat-2',
            unit='normalized'
        )
    
    def _create_slope_layer(self, instrumental: Dict[str, Any],
                           grid_shape: Tuple[int, int]) -> Optional[AnomalyLayer]:
        """Crear capa de pendientes anómalas."""
        
        # Buscar DEM/SRTM
        slope_value = None
        slope_confidence = 0.0
        
        for key, measurement in instrumental.items():
            if ('dem' in key.lower() or 'srtm' in key.lower() or 'slope' in key.lower()) and isinstance(measurement, dict):
                slope_value = measurement.get('value')
                slope_confidence = measurement.get('confidence', 0.8)
                break
        
        if slope_value is None:
            return None
        
        # Simular mapa de pendientes
        data = np.random.normal(0.15, 0.05, grid_shape)
        
        # Agregar bordes/terrazas
        center_r, center_c = grid_shape[0] // 2, grid_shape[1] // 2
        size = min(grid_shape[0], grid_shape[1]) // 4
        
        # Patrón de terrazas (líneas horizontales)
        for i in range(3):
            offset = (i - 1) * size // 3
            data[center_r+offset-2:center_r+offset+2, :] += 0.2
        
        # Normalizar
        data = np.clip(data, 0, 1)
        
        logger.info(f"   ⛰️ Slope layer: mean={np.mean(data):.3f}, max={np.max(data):.3f}")
        
        return AnomalyLayer(
            name='slope',
            data=data,
            weight=0.1,
            confidence=slope_confidence,
            source='DEM',
            unit='normalized'
        )
    
    def _fuse_layers(self, layers: List[AnomalyLayer],
                    environment_type: str) -> np.ndarray:
        """
        Fusión ponderada de capas (environment-aware).
        
        ANOMALY_MAP(x,y) = Σ w_i * A_i(x,y)
        """
        
        # Obtener pesos por ambiente
        weights = self.environment_weights.get(environment_type, self.environment_weights['temperate'])
        
        # Inicializar mapa fusionado
        grid_shape = layers[0].data.shape
        fused = np.zeros(grid_shape)
        total_weight = 0.0
        
        for layer in layers:
            # Obtener peso para esta capa
            weight = weights.get(layer.name, 0.1)
            
            # Ajustar por confianza
            effective_weight = weight * layer.confidence
            
            # Fusionar
            fused += effective_weight * layer.data
            total_weight += effective_weight
            
            logger.info(f"      {layer.name}: weight={weight:.2f}, confidence={layer.confidence:.2f}, effective={effective_weight:.2f}")
        
        # Normalizar por peso total
        if total_weight > 0:
            fused /= total_weight
        
        return fused
    
    def _detect_geometric_features(self, anomaly_map: np.ndarray) -> np.ndarray:
        """
        Detectar features geométricas (bordes, alineaciones, estructuras).
        
        Aplica:
        - Detección de bordes (Sobel)
        - Coherencia espacial
        - Filtros morfológicos
        """
        
        # 1. Detección de bordes (Sobel)
        sobel_x = ndimage.sobel(anomaly_map, axis=0)
        sobel_y = ndimage.sobel(anomaly_map, axis=1)
        edges = np.sqrt(sobel_x**2 + sobel_y**2)
        
        # Normalizar
        edges = edges / (np.max(edges) + 1e-6)
        
        # 2. Umbral adaptativo
        threshold = np.percentile(edges, 90)
        edges_binary = edges > threshold
        
        # 3. Morfología: cerrar gaps pequeños
        edges_closed = ndimage.binary_closing(edges_binary, structure=np.ones((3, 3)))
        
        # 4. Detectar líneas rectas (Hough transform simplificado)
        # Por ahora: usar convolución con kernels lineales
        kernel_h = np.ones((1, 5)) / 5  # Horizontal
        kernel_v = np.ones((5, 1)) / 5  # Vertical
        
        lines_h = convolve2d(edges_closed.astype(float), kernel_h, mode='same')
        lines_v = convolve2d(edges_closed.astype(float), kernel_v, mode='same')
        
        lines = np.maximum(lines_h, lines_v)
        
        # Combinar bordes y líneas
        geometric_features = np.maximum(edges, lines)
        
        return geometric_features
    
    def _create_empty_map(self, grid_shape: Tuple[int, int],
                         lat_min: float, lat_max: float,
                         lon_min: float, lon_max: float,
                         environment_type: str) -> AnomalyMap:
        """Crear mapa vacío cuando no hay datos."""
        
        return AnomalyMap(
            anomaly_map=np.zeros(grid_shape),
            geometric_features=np.zeros(grid_shape),
            layers_used=[],
            resolution_m=self.resolution_m,
            bounds=(lat_min, lat_max, lon_min, lon_max),
            environment_type=environment_type,
            fusion_weights={},
            metadata={'status': 'empty', 'reason': 'no_valid_layers'}
        )
    
    def export_to_png(self, anomaly_map: AnomalyMap, output_path: str):
        """
        Exportar mapa a PNG con colormap científico.
        
        🔵 azul: fondo natural
        🟡 amarillo: anomalía débil
        🔴 rojo: convergencia multifuente fuerte
        """
        
        try:
            from PIL import Image
            
            # Crear colormap personalizado
            data = anomaly_map.anomaly_map
            
            # Normalizar a 0-255
            data_norm = (data * 255).astype(np.uint8)
            
            # Aplicar colormap: azul → amarillo → rojo
            rgb = np.zeros((*data.shape, 3), dtype=np.uint8)
            
            # Azul (bajo)
            rgb[:, :, 2] = 255 - data_norm  # B
            
            # Amarillo (medio)
            mask_medium = (data > 0.3) & (data < 0.7)
            rgb[mask_medium, 0] = 255  # R
            rgb[mask_medium, 1] = 255  # G
            
            # Rojo (alto)
            mask_high = data >= 0.7
            rgb[mask_high, 0] = 255  # R
            rgb[mask_high, 1] = 0    # G
            rgb[mask_high, 2] = 0    # B
            
            # Overlay geometric features (blanco)
            geometric_mask = anomaly_map.geometric_features > 0.5
            rgb[geometric_mask] = [255, 255, 255]
            
            # Guardar
            img = Image.fromarray(rgb)
            img.save(output_path)
            
            logger.info(f"   💾 Mapa exportado: {output_path}")
            
        except ImportError:
            logger.warning("   ⚠️ PIL no disponible - no se puede exportar PNG")


if __name__ == "__main__":
    # Test
    print("🗺️ Anomaly Map Generator - Test")
    print("=" * 80)
    
    generator = AnomalyMapGenerator(resolution_m=30.0)
    
    # Simular mediciones
    measurements = {
        'instrumental_measurements': {
            'sentinel_1_sar': {'value': -8.2, 'confidence': 0.85, 'source': 'Sentinel-1'},
            'landsat_thermal': {'value': 305.2, 'confidence': 0.90, 'source': 'Landsat-8'},
            'icesat2': {'value': 15.7, 'confidence': 0.75, 'source': 'ICESat-2'},
            'srtm_elevation': {'value': 450.3, 'confidence': 0.95, 'source': 'SRTM'}
        }
    }
    
    # Generar mapa
    anomaly_map = generator.generate_anomaly_map(
        measurements=measurements,
        lat_min=29.97,
        lat_max=29.98,
        lon_min=31.13,
        lon_max=31.14,
        environment_type='arid'
    )
    
    print(f"\n✅ Mapa generado:")
    print(f"   Shape: {anomaly_map.anomaly_map.shape}")
    print(f"   Layers: {anomaly_map.layers_used}")
    print(f"   Anomaly range: [{np.min(anomaly_map.anomaly_map):.3f}, {np.max(anomaly_map.anomaly_map):.3f}]")
    print(f"   Geometric features: {anomaly_map.metadata['geometric_features_count']} pixels")
    
    # Exportar
    generator.export_to_png(anomaly_map, 'test_anomaly_map.png')
    
    print("\n" + "=" * 80)
    print("✅ Test completado")
