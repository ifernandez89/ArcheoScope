#!/usr/bin/env python3
"""
ArcheoScope Data Sanitizer - Blindaje Global contra inf/nan
===========================================================

CRÍTICO: Sanitizador central para evitar errores de serialización JSON
por valores inf/nan que vienen de instrumentos satelitales.

Este módulo implementa el blindaje global recomendado para transformar
ArcheoScope de 12.5% a ~60% operativo.
"""

import math
import numpy as np
from typing import Any, Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)

def safe_float(value: Any) -> Optional[float]:
    """
    Sanitizar un valor float para evitar inf/nan en JSON.
    
    Args:
        value: Valor a sanitizar (puede ser None, float, int, numpy types, etc.)
    
    Returns:
        float válido o None si el valor es inválido
    """
    if value is None:
        return None
    
    try:
        # Convertir a float si es posible
        if isinstance(value, (np.integer, np.floating)):
            value = float(value)
        elif not isinstance(value, (int, float)):
            # Intentar conversión para strings, etc.
            value = float(value)
        
        # Verificar si es finito
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        
        return float(value)
        
    except (ValueError, TypeError, OverflowError):
        return None

def safe_int(value: Any) -> Optional[int]:
    """
    Sanitizar un valor int para evitar problemas de serialización.
    
    Args:
        value: Valor a sanitizar
    
    Returns:
        int válido o None si el valor es inválido
    """
    if value is None:
        return None
    
    try:
        # Manejar tipos numpy
        if isinstance(value, (np.integer, np.floating)):
            value = float(value)
        
        # Verificar si es finito antes de convertir a int
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        
        return int(value)
        
    except (ValueError, TypeError, OverflowError):
        return None

def sanitize_measurement_dict(measurement: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizar un diccionario de medición instrumental.
    
    Args:
        measurement: Diccionario con datos de medición
    
    Returns:
        Diccionario sanitizado sin inf/nan
    """
    if not isinstance(measurement, dict):
        return {}
    
    sanitized = {}
    
    # Campos numéricos que necesitan sanitización
    float_fields = [
        'value', 'confidence', 'threshold', 'mean', 'std', 'min', 'max',
        'elevation', 'ndvi', 'lst', 'sar_backscatter', 'temperature',
        'ice_concentration', 'snow_cover', 'sst', 'latitude', 'longitude',
        'archaeological_probability', 'environment_confidence'
    ]
    
    int_fields = [
        'affected_pixels', 'valid_pixels', 'total_pixels', 'count',
        'instruments_converging', 'minimum_required'
    ]
    
    # Sanitizar campos float
    for field in float_fields:
        if field in measurement:
            sanitized[field] = safe_float(measurement[field])
    
    # Sanitizar campos int
    for field in int_fields:
        if field in measurement:
            sanitized[field] = safe_int(measurement[field])
    
    # Copiar campos no numéricos sin modificar
    for key, value in measurement.items():
        if key not in float_fields and key not in int_fields:
            if isinstance(value, (str, bool, type(None))):
                sanitized[key] = value
            elif isinstance(value, (list, dict)):
                # Recursivamente sanitizar estructuras anidadas
                sanitized[key] = sanitize_nested_structure(value)
            else:
                # Intentar convertir a string como fallback
                try:
                    sanitized[key] = str(value)
                except:
                    sanitized[key] = None
    
    return sanitized

def sanitize_nested_structure(data: Union[List, Dict, Any]) -> Any:
    """
    Sanitizar estructuras de datos anidadas (listas, diccionarios).
    
    Args:
        data: Estructura de datos a sanitizar
    
    Returns:
        Estructura sanitizada
    """
    if isinstance(data, dict):
        return {key: sanitize_nested_structure(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_nested_structure(item) for item in data]
    elif isinstance(data, (int, float)):
        return safe_float(data)
    else:
        return data

def sanitize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizar respuesta completa de ArcheoScope antes de JSON.
    
    Este es el punto de entrada principal para el blindaje global.
    
    Args:
        response: Diccionario de respuesta completo
    
    Returns:
        Respuesta sanitizada lista para JSON
    """
    logger.debug("Iniciando sanitización global de respuesta")
    
    try:
        # Sanitizar campos principales
        sanitized = {
            "analysis_id": response.get("analysis_id"),
            "region_name": response.get("region_name"),
            "timestamp": response.get("timestamp"),
            "status": response.get("status", "unknown")
        }
        
        # Sanitizar contexto espacial
        if "spatial_context" in response:
            spatial = response["spatial_context"]
            sanitized["spatial_context"] = {
                "area_km2": safe_float(spatial.get("area_km2")),
                "analysis_mode": spatial.get("analysis_mode"),
                "resolution_m": safe_int(spatial.get("resolution_m")),
                "lat_min": safe_float(spatial.get("lat_min")),
                "lat_max": safe_float(spatial.get("lat_max")),
                "lon_min": safe_float(spatial.get("lon_min")),
                "lon_max": safe_float(spatial.get("lon_max"))
            }
        
        # Sanitizar resultados arqueológicos
        if "archaeological_results" in response:
            arch = response["archaeological_results"]
            sanitized["archaeological_results"] = {
                "result_type": arch.get("result_type"),
                "confidence": safe_float(arch.get("confidence")),
                "archaeological_probability": safe_float(arch.get("archaeological_probability")),
                "affected_pixels": safe_int(arch.get("affected_pixels")),
                "anomaly_detected": arch.get("anomaly_detected"),
                "confidence_level": arch.get("confidence_level")
            }
        
        # Sanitizar mediciones instrumentales
        if "measurements" in response:
            measurements = response["measurements"]
            if isinstance(measurements, list):
                sanitized["measurements"] = [
                    sanitize_measurement_dict(m) for m in measurements
                ]
            elif isinstance(measurements, dict):
                sanitized["measurements"] = sanitize_measurement_dict(measurements)
        
        # Sanitizar capas de evidencia
        if "evidence_layers" in response:
            layers = response["evidence_layers"]
            if isinstance(layers, list):
                sanitized["evidence_layers"] = [
                    sanitize_measurement_dict(layer) for layer in layers
                ]
        
        # Sanitizar explicaciones de IA
        if "ai_explanations" in response:
            ai = response["ai_explanations"]
            sanitized["ai_explanations"] = {
                "ai_available": ai.get("ai_available", False),
                "explanation": ai.get("explanation"),
                "confidence": safe_float(ai.get("confidence")),
                "reasoning": ai.get("reasoning", [])
            }
        
        # Sanitizar métricas de validación
        if "validation_metrics" in response:
            validation = response["validation_metrics"]
            sanitized["validation_metrics"] = sanitize_measurement_dict(validation)
        
        # Sanitizar información de sitios conocidos
        if "known_site_nearby" in response:
            sanitized["known_site_nearby"] = response["known_site_nearby"]
        if "known_site_name" in response:
            sanitized["known_site_name"] = response["known_site_name"]
        if "known_site_distance_km" in response:
            sanitized["known_site_distance_km"] = safe_float(response["known_site_distance_km"])
        
        # Copiar campos de texto sin modificar
        text_fields = [
            "explanation", "detection_reasoning", "false_positive_risks",
            "recommended_validation", "environment_type", "notes", "source"
        ]
        
        for field in text_fields:
            if field in response:
                sanitized[field] = response[field]
        
        # Sanitizar cualquier campo restante
        for key, value in response.items():
            if key not in sanitized:
                sanitized[key] = sanitize_nested_structure(value)
        
        logger.debug("Sanitización global completada exitosamente")
        return sanitized
        
    except Exception as e:
        logger.error(f"Error en sanitización global: {e}")
        # Fallback: devolver respuesta mínima válida
        return {
            "analysis_id": response.get("analysis_id"),
            "status": "error",
            "error": "Sanitization failed",
            "archaeological_results": {
                "result_type": "error",
                "confidence": 0.0,
                "archaeological_probability": 0.0,
                "anomaly_detected": False
            }
        }

def validate_json_serializable(data: Any) -> bool:
    """
    Validar que los datos son serializables a JSON.
    
    Args:
        data: Datos a validar
    
    Returns:
        True si son serializables, False si no
    """
    try:
        import json
        json.dumps(data)
        return True
    except (TypeError, ValueError, OverflowError):
        return False

def log_sanitization_stats(original: Dict[str, Any], sanitized: Dict[str, Any]) -> None:
    """
    Registrar estadísticas de sanitización para debugging.
    
    Args:
        original: Datos originales
        sanitized: Datos sanitizados
    """
    try:
        original_fields = len(original) if isinstance(original, dict) else 0
        sanitized_fields = len(sanitized) if isinstance(sanitized, dict) else 0
        
        logger.info(f"Sanitización: {original_fields} → {sanitized_fields} campos")
        
        # Contar valores None introducidos
        none_count = 0
        if isinstance(sanitized, dict):
            for value in sanitized.values():
                if value is None:
                    none_count += 1
        
        if none_count > 0:
            logger.warning(f"Sanitización introdujo {none_count} valores None (inf/nan eliminados)")
        
    except Exception as e:
        logger.debug(f"Error en estadísticas de sanitización: {e}")

# Funciones de conveniencia para instrumentos específicos

def sanitize_icesat2_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitizar datos específicos de ICESat-2."""
    return {
        "value": safe_float(data.get("value")),
        "confidence": safe_float(data.get("confidence", 0.0)),
        "valid_points": safe_int(data.get("valid_points", 0)),
        "total_points": safe_int(data.get("total_points", 0)),
        "elevation_std": safe_float(data.get("elevation_std")),
        "source": data.get("source", "ICESat-2"),
        "acquisition_date": data.get("acquisition_date"),
        "reason": data.get("reason")
    }

def sanitize_sentinel_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitizar datos específicos de Sentinel."""
    return {
        "value": safe_float(data.get("value")),
        "confidence": safe_float(data.get("confidence", 0.0)),
        "mean": safe_float(data.get("mean")),
        "std": safe_float(data.get("std")),
        "valid_pixels": safe_int(data.get("valid_pixels", 0)),
        "total_pixels": safe_int(data.get("total_pixels", 0)),
        "source": data.get("source", "Sentinel"),
        "acquisition_date": data.get("acquisition_date"),
        "cloud_cover": safe_float(data.get("cloud_cover"))
    }

def sanitize_modis_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitizar datos específicos de MODIS."""
    return {
        "value": safe_float(data.get("value")),
        "confidence": safe_float(data.get("confidence", 0.0)),
        "temperature_k": safe_float(data.get("temperature_k")),
        "quality_flag": safe_int(data.get("quality_flag", 0)),
        "valid_pixels": safe_int(data.get("valid_pixels", 0)),
        "source": data.get("source", "MODIS"),
        "acquisition_date": data.get("acquisition_date")
    }

# Decorador para sanitización automática
def sanitize_output(func):
    """
    Decorador para sanitizar automáticamente la salida de funciones.
    
    Usage:
        @sanitize_output
        def my_function():
            return {"value": float('inf')}  # Será sanitizado automáticamente
    """
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if isinstance(result, dict):
                return sanitize_response(result)
            return result
        except Exception as e:
            logger.error(f"Error en función decorada {func.__name__}: {e}")
            return {
                "status": "error",
                "error": str(e),
                "archaeological_results": {
                    "result_type": "error",
                    "confidence": 0.0,
                    "archaeological_probability": 0.0,
                    "anomaly_detected": False
                }
            }
    return wrapper

if __name__ == "__main__":
    # Test del sanitizador
    test_data = {
        "value": float('inf'),
        "confidence": float('nan'),
        "elevation": 1234.56,
        "valid_pixels": np.int64(100),
        "nested": {
            "temperature": float('-inf'),
            "list_data": [1.0, float('nan'), 3.0]
        }
    }
    
    print("Datos originales:", test_data)
    sanitized = sanitize_response(test_data)
    print("Datos sanitizados:", sanitized)
    print("JSON serializable:", validate_json_serializable(sanitized))