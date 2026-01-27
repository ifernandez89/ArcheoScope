#!/usr/bin/env python3
"""
Utilidades compartidas para ArcheoScope API
"""

import numpy as np
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

def convert_numpy_types(obj: Any) -> Any:
    """
    Convertir tipos numpy a tipos Python nativos para serialización JSON.
    
    Función crítica para evitar errores de serialización en FastAPI.
    """
    if isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def validate_coordinates(lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> Dict[str, Any]:
    """
    Validar coordenadas geográficas y calcular métricas básicas.
    
    Returns:
        Dict con información de validación y métricas calculadas
    """
    
    errors = []
    warnings = []
    
    # Validaciones básicas
    if not (-90 <= lat_min <= 90):
        errors.append(f"lat_min fuera de rango: {lat_min}")
    if not (-90 <= lat_max <= 90):
        errors.append(f"lat_max fuera de rango: {lat_max}")
    if not (-180 <= lon_min <= 180):
        errors.append(f"lon_min fuera de rango: {lon_min}")
    if not (-180 <= lon_max <= 180):
        errors.append(f"lon_max fuera de rango: {lon_max}")
    
    if lat_min >= lat_max:
        errors.append("lat_min debe ser menor que lat_max")
    if lon_min >= lon_max:
        errors.append("lon_min debe ser menor que lon_max")
    
    # Calcular métricas si las coordenadas son válidas
    metrics = {}
    if not errors:
        # Área aproximada
        lat_diff = lat_max - lat_min
        lon_diff = lon_max - lon_min
        
        # Conversión aproximada a km (no considera curvatura terrestre)
        lat_km = lat_diff * 111.0
        lon_km = lon_diff * 111.0 * abs(np.cos(np.radians((lat_min + lat_max) / 2)))
        area_km2 = lat_km * lon_km
        
        metrics = {
            'area_km2': area_km2,
            'lat_span_km': lat_km,
            'lon_span_km': lon_km,
            'center_lat': (lat_min + lat_max) / 2,
            'center_lon': (lon_min + lon_max) / 2
        }
        
        # Warnings por área
        if area_km2 > 10000:
            warnings.append(f"Área muy grande: {area_km2:.1f} km² - puede afectar rendimiento")
        elif area_km2 < 0.01:
            warnings.append(f"Área muy pequeña: {area_km2:.4f} km² - puede no detectar estructuras")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'metrics': metrics
    }

def format_analysis_response(raw_result: Any, request_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formatear resultado de análisis para respuesta API consistente.
    """
    
    try:
        # Estructura base de respuesta
        formatted = {
            'region_info': {
                'name': request_info.get('region_name', 'Unknown Region'),
                'coordinates': {
                    'lat_min': request_info.get('lat_min'),
                    'lat_max': request_info.get('lat_max'),
                    'lon_min': request_info.get('lon_min'),
                    'lon_max': request_info.get('lon_max'),
                    'center_lat': (request_info.get('lat_min', 0) + request_info.get('lat_max', 0)) / 2,
                    'center_lon': (request_info.get('lon_min', 0) + request_info.get('lon_max', 0)) / 2
                },
                'area_km2': _calculate_area_km2(request_info),
                'analysis_timestamp': _get_current_timestamp()
            }
        }
        
        # Agregar datos del resultado si están disponibles
        if hasattr(raw_result, 'environment_type'):
            formatted['environment_analysis'] = {
                'environment_type': raw_result.environment_type,
                'confidence': getattr(raw_result, 'environment_confidence', 0.0)
            }
        
        if hasattr(raw_result, 'anomaly_detected'):
            formatted['anomaly_detection'] = {
                'anomaly_detected': raw_result.anomaly_detected,
                'confidence_level': getattr(raw_result, 'confidence_level', 'unknown'),
                'archaeological_probability': getattr(raw_result, 'archaeological_probability', 0.0)
            }
        
        # Convertir tipos numpy
        formatted = convert_numpy_types(formatted)
        
        return formatted
        
    except Exception as e:
        logger.error(f"Error formateando respuesta: {e}")
        return {
            'error': 'Error interno formateando respuesta',
            'raw_error': str(e)
        }

def _calculate_area_km2(coords: Dict[str, float]) -> float:
    """Calcular área aproximada en km²."""
    
    try:
        lat_min = coords.get('lat_min', 0)
        lat_max = coords.get('lat_max', 0)
        lon_min = coords.get('lon_min', 0)
        lon_max = coords.get('lon_max', 0)
        
        lat_diff = abs(lat_max - lat_min)
        lon_diff = abs(lon_max - lon_min)
        
        lat_km = lat_diff * 111.0
        lon_km = lon_diff * 111.0 * abs(np.cos(np.radians((lat_min + lat_max) / 2)))
        
        return lat_km * lon_km
        
    except Exception:
        return 0.0

def _get_current_timestamp() -> str:
    """Obtener timestamp actual en formato ISO."""
    from datetime import datetime
    return datetime.now().isoformat()

def log_analysis_request(request_data: Dict[str, Any]) -> str:
    """
    Registrar solicitud de análisis para auditoría.
    
    Returns:
        Request ID para trazabilidad
    """
    
    import uuid
    
    request_id = str(uuid.uuid4())[:8]
    
    logger.info(f"[{request_id}] Análisis solicitado: {request_data.get('region_name', 'Unknown')}")
    logger.info(f"[{request_id}] Coordenadas: {request_data.get('lat_min')}, {request_data.get('lon_min')} -> {request_data.get('lat_max')}, {request_data.get('lon_max')}")
    
    return request_id

def log_analysis_result(request_id: str, result: Any, duration_seconds: float):
    """Registrar resultado de análisis."""
    
    try:
        anomaly_detected = getattr(result, 'anomaly_detected', False)
        confidence = getattr(result, 'confidence_level', 'unknown')
        probability = getattr(result, 'archaeological_probability', 0.0)
        
        logger.info(f"[{request_id}] Análisis completado en {duration_seconds:.2f}s")
        logger.info(f"[{request_id}] Resultado: anomalía={anomaly_detected}, confianza={confidence}, prob={probability:.2%}")
        
    except Exception as e:
        logger.warning(f"[{request_id}] Error registrando resultado: {e}")

def sanitize_region_name(name: str) -> str:
    """Sanitizar nombre de región para uso seguro."""
    
    import re
    
    # Remover caracteres peligrosos
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    
    # Limitar longitud
    sanitized = sanitized[:200]
    
    # Asegurar que no esté vacío
    if not sanitized.strip():
        sanitized = "Unknown_Region"
    
    return sanitized.strip()

def get_memory_usage() -> Dict[str, Any]:
    """Obtener información de uso de memoria (para debugging)."""
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'percent': process.memory_percent(),
            'available_mb': psutil.virtual_memory().available / 1024 / 1024
        }
        
    except ImportError:
        return {'error': 'psutil no disponible'}
    except Exception as e:
        return {'error': str(e)}

def validate_analysis_area(area_km2: float) -> Dict[str, Any]:
    """
    Validar que el área de análisis sea apropiada.
    
    Diferentes límites según el tipo de análisis.
    """
    
    validation = {
        'valid': True,
        'warnings': [],
        'recommendations': []
    }
    
    if area_km2 > 5000:
        validation['valid'] = False
        validation['warnings'].append(f"Área demasiado grande: {area_km2:.1f} km²")
        validation['recommendations'].append("Reducir área a menos de 5000 km²")
    
    elif area_km2 > 1000:
        validation['warnings'].append(f"Área grande: {area_km2:.1f} km² - análisis puede ser lento")
        validation['recommendations'].append("Considerar dividir en regiones más pequeñas")
    
    elif area_km2 < 0.1:
        validation['warnings'].append(f"Área muy pequeña: {area_km2:.3f} km²")
        validation['recommendations'].append("Estructuras arqueológicas pueden no ser detectables")
    
    return validation