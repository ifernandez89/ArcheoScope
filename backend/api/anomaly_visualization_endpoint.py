#!/usr/bin/env python3
"""
Anomaly Visualization Endpoint
==============================

Endpoint para generar y servir mapas de anomalía en tiempo real.

ENDPOINTS:
- POST /api/generate-anomaly-map - Generar mapa desde análisis
- GET /api/anomaly-map/{analysis_id} - Obtener mapa existente
- GET /api/anomaly-map/{analysis_id}/png - Descargar PNG
"""

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path
import base64
import io

# Agregar backend al path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from anomaly_map_generator import AnomalyMapGenerator, AnomalyMap
import numpy as np

router = APIRouter()

# Cache de mapas generados (en producción: usar Redis)
anomaly_maps_cache: Dict[str, AnomalyMap] = {}


class AnomalyMapRequest(BaseModel):
    """Request para generar mapa de anomalía."""
    analysis_id: str
    measurements: Dict[str, Any]
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float
    environment_type: str = 'temperate'
    resolution_m: float = 30.0


class AnomalyMapResponse(BaseModel):
    """Response con mapa de anomalía."""
    analysis_id: str
    anomaly_map_base64: str  # Mapa como base64 (para visualización)
    geometric_features_base64: str  # Features geométricas
    layers_used: List[str]
    resolution_m: float
    bounds: List[float]  # [lat_min, lat_max, lon_min, lon_max]
    environment_type: str
    fusion_weights: Dict[str, float]
    metadata: Dict[str, Any]
    visualization_url: str  # URL para PNG


@router.post("/api/generate-anomaly-map", response_model=AnomalyMapResponse)
async def generate_anomaly_map(request: AnomalyMapRequest):
    """
    Generar mapa de anomalía desde mediciones instrumentales.
    
    Este endpoint se llama automáticamente después de cada análisis
    para generar la visualización en tiempo real.
    """
    
    try:
        # Crear generador
        generator = AnomalyMapGenerator(resolution_m=request.resolution_m)
        
        # Generar mapa
        anomaly_map = generator.generate_anomaly_map(
            measurements=request.measurements,
            lat_min=request.lat_min,
            lat_max=request.lat_max,
            lon_min=request.lon_min,
            lon_max=request.lon_max,
            environment_type=request.environment_type
        )
        
        # Guardar en cache
        anomaly_maps_cache[request.analysis_id] = anomaly_map
        
        # Convertir arrays a base64 para transmisión
        anomaly_map_base64 = _array_to_base64(anomaly_map.anomaly_map)
        geometric_features_base64 = _array_to_base64(anomaly_map.geometric_features)
        
        return AnomalyMapResponse(
            analysis_id=request.analysis_id,
            anomaly_map_base64=anomaly_map_base64,
            geometric_features_base64=geometric_features_base64,
            layers_used=anomaly_map.layers_used,
            resolution_m=anomaly_map.resolution_m,
            bounds=list(anomaly_map.bounds),
            environment_type=anomaly_map.environment_type,
            fusion_weights=anomaly_map.fusion_weights,
            metadata=anomaly_map.metadata,
            visualization_url=f"/api/anomaly-map/{request.analysis_id}/png"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando mapa: {str(e)}")


@router.get("/api/anomaly-map/{analysis_id}")
async def get_anomaly_map(analysis_id: str):
    """Obtener mapa de anomalía existente."""
    
    if analysis_id not in anomaly_maps_cache:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")
    
    anomaly_map = anomaly_maps_cache[analysis_id]
    
    # Convertir a response
    anomaly_map_base64 = _array_to_base64(anomaly_map.anomaly_map)
    geometric_features_base64 = _array_to_base64(anomaly_map.geometric_features)
    
    return AnomalyMapResponse(
        analysis_id=analysis_id,
        anomaly_map_base64=anomaly_map_base64,
        geometric_features_base64=geometric_features_base64,
        layers_used=anomaly_map.layers_used,
        resolution_m=anomaly_map.resolution_m,
        bounds=list(anomaly_map.bounds),
        environment_type=anomaly_map.environment_type,
        fusion_weights=anomaly_map.fusion_weights,
        metadata=anomaly_map.metadata,
        visualization_url=f"/api/anomaly-map/{analysis_id}/png"
    )


@router.get("/api/anomaly-map/{analysis_id}/png")
async def get_anomaly_map_png(analysis_id: str):
    """Descargar mapa como PNG."""
    
    if analysis_id not in anomaly_maps_cache:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")
    
    anomaly_map = anomaly_maps_cache[analysis_id]
    
    try:
        from PIL import Image
        
        # Generar PNG en memoria
        png_bytes = _generate_png_bytes(anomaly_map)
        
        return Response(
            content=png_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f"inline; filename=anomaly_map_{analysis_id}.png"
            }
        )
        
    except ImportError:
        raise HTTPException(status_code=500, detail="PIL no disponible")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PNG: {str(e)}")


def _array_to_base64(array: np.ndarray) -> str:
    """Convertir numpy array a base64 para transmisión."""
    
    # Convertir a bytes
    array_bytes = array.tobytes()
    
    # Codificar a base64
    base64_str = base64.b64encode(array_bytes).decode('utf-8')
    
    # Incluir shape y dtype para reconstrucción
    shape_str = ','.join(map(str, array.shape))
    dtype_str = str(array.dtype)
    
    return f"{shape_str}|{dtype_str}|{base64_str}"


def _base64_to_array(base64_str: str) -> np.ndarray:
    """Reconstruir numpy array desde base64."""
    
    # Parsear metadata
    parts = base64_str.split('|')
    shape = tuple(map(int, parts[0].split(',')))
    dtype = np.dtype(parts[1])
    data = base64.b64decode(parts[2])
    
    # Reconstruir array
    array = np.frombuffer(data, dtype=dtype).reshape(shape)
    
    return array


def _generate_png_bytes(anomaly_map: AnomalyMap) -> bytes:
    """Generar PNG en memoria."""
    
    from PIL import Image
    
    # Crear colormap
    data = anomaly_map.anomaly_map
    data_norm = (data * 255).astype(np.uint8)
    
    # RGB: azul → amarillo → rojo
    rgb = np.zeros((*data.shape, 3), dtype=np.uint8)
    
    # Azul (bajo)
    rgb[:, :, 2] = 255 - data_norm
    
    # Amarillo (medio)
    mask_medium = (data > 0.3) & (data < 0.7)
    rgb[mask_medium, 0] = 255
    rgb[mask_medium, 1] = 255
    
    # Rojo (alto)
    mask_high = data >= 0.7
    rgb[mask_high, 0] = 255
    rgb[mask_high, 1] = 0
    rgb[mask_high, 2] = 0
    
    # Overlay geometric features (blanco)
    geometric_mask = anomaly_map.geometric_features > 0.5
    rgb[geometric_mask] = [255, 255, 255]
    
    # Convertir a PNG en memoria
    img = Image.fromarray(rgb)
    
    # Guardar en BytesIO
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()


# Registrar router en main API
def register_anomaly_visualization_routes(app):
    """Registrar rutas en FastAPI app."""
    app.include_router(router, tags=["Anomaly Visualization"])
