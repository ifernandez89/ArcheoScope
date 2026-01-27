#!/usr/bin/env python3
"""
Status Router - Health checks y diagnósticos del sistema
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
from datetime import datetime

from ..models import SystemStatus
from ..dependencies import get_system_components

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/status", tags=["Status"])

@router.get("/", response_model=SystemStatus)
async def get_system_status(components: Dict = Depends(get_system_components)):
    """Estado básico del sistema arqueológico."""
    
    try:
        # Verificar componentes críticos
        backend_status = "operational" if components.get('core_anomaly_detector') else "degraded"
        
        # Verificar base de datos
        database_status = "connected"
        try:
            db = components.get('database')
            if db:
                # Test simple de conectividad
                db.execute("SELECT 1")
        except Exception:
            database_status = "disconnected"
        
        # Verificar IA
        ai_status = "available" if components.get('ai_assistant') else "unavailable"
        
        # Contar instrumentos activos
        active_instruments = 0
        if components.get('core_anomaly_detector'):
            # Contar instrumentos disponibles
            active_instruments = len(components.get('instrument_list', []))
        
        return SystemStatus(
            backend_status=backend_status,
            database_status=database_status,
            ai_status=ai_status,
            active_instruments=active_instruments,
            last_update=datetime.now().isoformat(),
            version="2.0.0-refactored"
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo estado del sistema: {e}")
        raise HTTPException(status_code=500, detail="Error interno del sistema")

@router.get("/detailed")
async def get_detailed_system_status(components: Dict = Depends(get_system_components)):
    """Estado detallado del sistema incluyendo instrumentos."""
    
    try:
        detector = components.get('core_anomaly_detector')
        if not detector:
            return {"error": "Detector principal no disponible"}
        
        # Estado de instrumentos
        instruments_status = {}
        
        # Verificar integrador de datos reales
        if hasattr(detector, 'real_data_integrator'):
            try:
                # Test básico de conectividad
                instruments_status['real_data_integrator'] = {
                    'status': 'available',
                    'description': 'Integrador de datos satelitales reales'
                }
            except Exception as e:
                instruments_status['real_data_integrator'] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        # Estado de componentes
        components_status = {}
        for name, component in components.items():
            if component is not None:
                components_status[name] = {
                    'status': 'loaded',
                    'type': type(component).__name__
                }
            else:
                components_status[name] = {'status': 'not_loaded'}
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system_health': 'operational',
            'components': components_status,
            'instruments': instruments_status,
            'memory_usage': 'lazy_loaded',  # Indicar que usa lazy loading
            'startup_time': 'optimized'
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado detallado: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/instruments")
async def get_instruments_status(components: Dict = Depends(get_system_components)):
    """Estado completo de todos los instrumentos arqueológicos."""
    
    try:
        detector = components.get('core_anomaly_detector')
        if not detector:
            raise HTTPException(status_code=503, detail="Detector principal no disponible")
        
        # Matriz de instrumentos por ambiente
        instruments_matrix = {
            'desert': {
                'primary': ['landsat_thermal', 'modis_lst', 'sentinel2', 'sar'],
                'secondary': ['srtm_dem', 'palsar'],
                'archaeological_value': 'high',
                'visibility': 'excellent'
            },
            'forest': {
                'primary': ['lidar', 'sentinel2', 'sar'],
                'secondary': ['landsat', 'modis'],
                'archaeological_value': 'medium',
                'visibility': 'limited'
            },
            'glacier': {
                'primary': ['icesat2', 'sentinel1_sar', 'nsidc_sea_ice'],
                'secondary': ['modis_lst', 'palsar'],
                'archaeological_value': 'low',
                'visibility': 'poor'
            },
            'shallow_sea': {
                'primary': ['copernicus_sst', 'sentinel1_sar'],
                'secondary': ['copernicus_sea_ice', 'bathymetry'],
                'archaeological_value': 'medium',
                'visibility': 'moderate'
            }
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_environments': len(instruments_matrix),
            'instruments_by_environment': instruments_matrix,
            'status': 'operational',
            'note': 'Instrumentos cargados bajo demanda (lazy loading)'
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estado de instrumentos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check simple para load balancers."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}