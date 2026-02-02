#!/usr/bin/env python3
"""
SAR Enhanced Processing - Corrección Normalización Agresiva
===========================================================

PROBLEMA:
- SAR normalizado globalmente → norm=0.003 (casi cero)
- SAR es sensor ESTRELLA para arqueología enterrada
- Valor absoluto no sirve, necesitamos ESTRUCTURA

SOLUCIÓN:
1. Normalización regional (50-100km, no global)
2. Derivados estructurales:
   - Textura (GLCM)
   - Gradiente espacial
   - Coherencia temporal
   - Anomalías locales (z-score por vecindad)

IMPACTO:
- SAR pasa de "ruido" a "señal principal"
- Detecta estructuras sutiles
- No depende de valor absoluto
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from scipy import ndimage
from scipy.stats import zscore
import logging

logger = logging.getLogger(__name__)

def despeckle_sar(img: np.ndarray, window_size: int = 5) -> np.ndarray:
    """
    Apply Lee Filter for SAR de-speckling.
    This reduces granular noise while preserving edges.
    """
    img_mean = ndimage.uniform_filter(img, (window_size, window_size))
    img_sqr_mean = ndimage.uniform_filter(img**2, (window_size, window_size))
    img_variance = img_sqr_mean - img_mean**2

    overall_variance = np.var(img)

    img_weights = img_variance / (img_variance + overall_variance + 1e-10)
    img_output = img_mean + img_weights * (img - img_mean)
    return img_output


def calculate_sar_texture(sar_data: np.ndarray, window_size: int = 3) -> Dict[str, float]:
    """
    Calcular textura SAR usando GLCM simplificado.
    
    Textura detecta:
    - Homogeneidad (estructuras uniformes)
    - Contraste (bordes, límites)
    - Entropía (complejidad)
    
    Args:
        sar_data: Array 2D de backscatter SAR
        window_size: Tamaño de ventana para análisis
    
    Returns:
        Dict con métricas de textura
    """
    
    # Calcular varianza local (proxy de textura)
    variance_map = ndimage.generic_filter(
        sar_data, 
        np.var, 
        size=window_size
    )
    
    # Calcular rango local (contraste)
    def local_range(window):
        return np.max(window) - np.min(window)
    
    range_map = ndimage.generic_filter(
        sar_data,
        local_range,
        size=window_size
    )
    
    # Métricas agregadas
    texture_variance = float(np.mean(variance_map))
    texture_contrast = float(np.mean(range_map))
    texture_homogeneity = float(1.0 / (1.0 + texture_variance))
    
    # Detectar zonas de alta textura (posibles estructuras)
    high_texture_fraction = float(np.sum(variance_map > np.percentile(variance_map, 75)) / variance_map.size)
    
    return {
        'texture_variance': texture_variance,
        'texture_contrast': texture_contrast,
        'texture_homogeneity': texture_homogeneity,
        'high_texture_fraction': high_texture_fraction,
        'texture_index': texture_variance * texture_contrast  # Índice combinado
    }


def calculate_sar_gradient(sar_data: np.ndarray) -> Dict[str, float]:
    """
    Calcular gradiente espacial SAR (bordes, estructuras).
    
    Gradiente detecta:
    - Bordes de estructuras
    - Cambios bruscos de backscatter
    - Límites de ocupación
    
    Args:
        sar_data: Array 2D de backscatter SAR
    
    Returns:
        Dict con métricas de gradiente
    """
    
    # Calcular gradiente con Sobel
    gradient_x = ndimage.sobel(sar_data, axis=0)
    gradient_y = ndimage.sobel(sar_data, axis=1)
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    # Métricas
    gradient_mean = float(np.mean(gradient_magnitude))
    gradient_std = float(np.std(gradient_magnitude))
    gradient_max = float(np.max(gradient_magnitude))
    
    # Detectar bordes fuertes (posibles estructuras)
    edge_threshold = np.percentile(gradient_magnitude, 90)
    edge_density = float(np.sum(gradient_magnitude > edge_threshold) / gradient_magnitude.size)
    
    return {
        'gradient_mean': gradient_mean,
        'gradient_std': gradient_std,
        'gradient_max': gradient_max,
        'edge_density': edge_density,
        'gradient_index': gradient_mean * edge_density  # Índice combinado
    }


def calculate_sar_local_anomalies(sar_data: np.ndarray, window_size: int = 5) -> Dict[str, float]:
    """
    Detectar anomalías locales SAR (z-score por vecindad).
    
    Anomalías locales detectan:
    - Outliers locales (no globales)
    - Estructuras sutiles
    - Patrones no evidentes en valor absoluto
    
    Args:
        sar_data: Array 2D de backscatter SAR
        window_size: Tamaño de ventana para z-score local
    
    Returns:
        Dict con métricas de anomalías
    """
    
    def local_zscore(window):
        """Calcular z-score del pixel central respecto a su vecindad."""
        center_idx = len(window) // 2
        center = window[center_idx]
        mean = np.mean(window)
        std = np.std(window)
        if std == 0:
            return 0
        return (center - mean) / std
    
    # Calcular z-score local para cada pixel
    zscore_map = ndimage.generic_filter(
        sar_data,
        local_zscore,
        size=window_size
    )
    
    # Detectar anomalías (|z| > 2)
    anomalies = np.abs(zscore_map) > 2
    anomaly_fraction = float(np.sum(anomalies) / anomalies.size)
    
    if np.any(anomalies):
        anomaly_mean_zscore = float(np.mean(np.abs(zscore_map[anomalies])))
    else:
        anomaly_mean_zscore = 0.0
    
    # Detectar clusters de anomalías (estructuras coherentes)
    from scipy.ndimage import label
    labeled_anomalies, num_clusters = label(anomalies)
    
    return {
        'anomaly_fraction': anomaly_fraction,
        'anomaly_mean_zscore': anomaly_mean_zscore,
        'anomaly_clusters': float(num_clusters),
        'anomaly_index': anomaly_fraction * anomaly_mean_zscore  # Índice combinado
    }


def normalize_sar_regional(sar_value: float, regional_mean: float, regional_std: float) -> float:
    """
    Normalizar SAR usando estadísticas regionales (no globales).
    
    Args:
        sar_value: Valor SAR del pixel/región
        regional_mean: Media regional (50-100km)
        regional_std: Desviación estándar regional
    
    Returns:
        Z-score regional (no global)
    """
    
    if regional_std == 0:
        return 0.0
    
    z_score_regional = (sar_value - regional_mean) / regional_std
    
    # Clip a ±5σ (más permisivo que ±3σ global)
    return float(np.clip(z_score_regional, -5, 5))


def process_sar_enhanced(sar_value: float, sar_data_2d: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """
    Procesar SAR con métricas mejoradas (no solo valor absoluto).
    
    Args:
        sar_value: Valor SAR puntual (backscatter)
        sar_data_2d: Array 2D opcional para análisis espacial
    
    Returns:
        Dict con métricas SAR mejoradas
    """
    
    result = {
        'sar_value_raw': sar_value,
        'sar_value_normalized': 0.0,
        'sar_texture': {},
        'sar_gradient': {},
        'sar_anomalies': {},
        'sar_structural_index': 0.0,
        'processing_mode': 'point'
    }
    
    # Si tenemos datos 2D, calcular derivados espaciales
    if sar_data_2d is not None and sar_data_2d.size > 0:
        logger.info("   📊 SAR: Aplicando De-speckling (Lee Filter) y calculando derivados...")
        
        # 1. Aplicar De-speckling antes del análisis
        sar_clean = despeckle_sar(sar_data_2d)
        
        # 2. Textura (sobre datos limpios)
        result['sar_texture'] = calculate_sar_texture(sar_clean)
        logger.info(f"      Texture index: {result['sar_texture']['texture_index']:.3f}")
        
        # 3. Gradiente
        result['sar_gradient'] = calculate_sar_gradient(sar_clean)
        logger.info(f"      Gradient index: {result['sar_gradient']['gradient_index']:.3f}")
        
        # Anomalías locales
        result['sar_anomalies'] = calculate_sar_local_anomalies(sar_data_2d)
        logger.info(f"      Anomaly index: {result['sar_anomalies']['anomaly_index']:.3f}")
        
        # Índice estructural combinado
        result['sar_structural_index'] = (
            result['sar_texture']['texture_index'] * 0.4 +
            result['sar_gradient']['gradient_index'] * 0.4 +
            result['sar_anomalies']['anomaly_index'] * 0.2
        )
        
        result['processing_mode'] = 'spatial'
        
        logger.info(f"   ✅ SAR Structural Index: {result['sar_structural_index']:.3f}")
    
    else:
        # Solo valor puntual - normalización regional estimada
        # Estimar estadísticas regionales basadas en ambiente
        # (en producción: consultar buffer real de 50-100km)
        regional_mean = -12.0  # dB típico
        regional_std = 3.0     # Variabilidad típica
        
        result['sar_value_normalized'] = normalize_sar_regional(
            sar_value, regional_mean, regional_std
        )
        
        logger.info(f"   📊 SAR: Normalización regional (z={result['sar_value_normalized']:.2f})")
    
    return result


if __name__ == "__main__":
    # Test
    print("🧪 SAR Enhanced Processing - Test")
    print("=" * 80)
    
    # Test 1: Valor puntual
    print("\n1. Test: Valor puntual SAR")
    sar_value = -8.2  # dB
    result = process_sar_enhanced(sar_value)
    print(f"   Raw: {result['sar_value_raw']:.2f} dB")
    print(f"   Normalized (regional): {result['sar_value_normalized']:.2f}")
    
    # Test 2: Datos 2D (simulados)
    print("\n2. Test: Datos 2D SAR con estructura")
    sar_2d = np.random.normal(-12, 3, (50, 50))
    # Agregar estructura artificial (cuadrado)
    sar_2d[20:30, 20:30] += 5  # Anomalía positiva
    
    result = process_sar_enhanced(-12.0, sar_2d)
    print(f"   Texture index: {result['sar_texture']['texture_index']:.3f}")
    print(f"   Gradient index: {result['sar_gradient']['gradient_index']:.3f}")
    print(f"   Anomaly index: {result['sar_anomalies']['anomaly_index']:.3f}")
    print(f"   ✅ Structural index: {result['sar_structural_index']:.3f}")
    
    print("\n" + "=" * 80)
    print("✅ Test completado")
