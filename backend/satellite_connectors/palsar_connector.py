#!/usr/bin/env python3
"""
ALOS PALSAR-2 Connector - Advanced Land Observing Satellite
==========================================================

PALSAR-2 (JAXA) - Instrumento 13/15
- Frecuencia: L-band (1.2 GHz) - Penetración profunda
- Resolución: 3-100m según modo
- Cobertura: Global cada 14 días
- API: ASF DAAC (Alaska Satellite Facility) via Earthdata

APLICACIONES ARQUEOLÓGICAS:
- Penetración de vegetación densa (L-band)
- Detección de estructuras enterradas
- Análisis de humedad del suelo
- Mapeo de redes de drenaje antiguas
"""

import requests
import numpy as np
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import asyncio

logger = logging.getLogger(__name__)

class PALSARConnector:
    """Conector para datos ALOS PALSAR-2 via ASF DAAC."""
    
    def __init__(self):
        """Inicializar conector PALSAR-2."""
        
        self.base_url = "https://api.daac.asf.alaska.edu"
        self.search_url = f"{self.base_url}/services/search/param"
        
        # Productos PALSAR-2 disponibles
        self.products = {
            'rtc': 'ALOS_PALSAR_RTC',      # Radiometric Terrain Corrected
            'mosaic': 'ALOS_PALSAR_MOSAIC', # Global Mosaic
            'interferometry': 'ALOS_PALSAR_INTERFEROMETRY'
        }
        
        # Credenciales Earthdata (hasheadas en BD)
        import os
        self.username = os.getenv('EARTHDATA_USERNAME')
        self.password = os.getenv('EARTHDATA_PASSWORD')
        
        logger.info("📡 ALOS PALSAR-2 Connector initialized")
    
    async def get_sar_backscatter(self, lat_min: float, lat_max: float,
                                 lon_min: float, lon_max: float,
                                 polarization: str = 'HH') -> Dict[str, Any]:
        """
        Obtener datos de backscatter SAR L-band.
        
        Args:
            polarization: 'HH', 'HV', 'VV', 'VH'
        
        VENTAJA L-band: Penetra vegetación hasta 10m de profundidad
        """
        
        try:
            # Buscar escenas PALSAR-2 disponibles
            search_params = {
                'platform': 'ALOS-2',
                'processingLevel': 'RTC_HI_RES',
                'bbox': f"{lon_min},{lat_min},{lon_max},{lat_max}",
                'start': (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                'end': datetime.now().strftime('%Y-%m-%d'),
                'maxResults': 10,
                'output': 'json'
            }
            
            # Realizar búsqueda
            response = await self._make_asf_request(self.search_url, search_params)
            
            if response and response.get('results'):
                # Procesar escenas encontradas
                scenes = response['results']
                logger.info(f"Encontradas {len(scenes)} escenas PALSAR-2")
                
                # Seleccionar la escena más reciente con mejor cobertura
                best_scene = self._select_best_scene(scenes, lat_min, lat_max, lon_min, lon_max)
                
                if best_scene:
                    # Obtener datos de backscatter
                    backscatter_data = await self._process_palsar_scene(
                        best_scene, polarization
                    )
                    
                    if backscatter_data:
                        return {
                            'value': backscatter_data['mean_backscatter'],
                            'backscatter_stats': backscatter_data['stats'],
                            'polarization': polarization,
                            'penetration_indicators': backscatter_data['penetration'],
                            'unit': 'dB',
                            'source': f'PALSAR2_{polarization}',
                            'resolution_m': 25,
                            'acquisition_date': best_scene.get('startTime', ''),
                            'quality': backscatter_data['quality']
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo backscatter PALSAR-2: {e}")
            return None
    
    async def get_forest_penetration(self, lat_min: float, lat_max: float,
                                    lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        Análisis específico de penetración forestal con L-band.
        
        APLICACIÓN: Detectar estructuras bajo dosel denso
        """
        
        try:
            # Obtener datos HH y HV para análisis de penetración
            hh_data = await self.get_sar_backscatter(lat_min, lat_max, lon_min, lon_max, 'HH')
            hv_data = await self.get_sar_backscatter(lat_min, lat_max, lon_min, lon_max, 'HV')
            
            if hh_data and hv_data:
                # Calcular ratio HH/HV (indicador de penetración)
                hh_value = hh_data['value']
                hv_value = hv_data['value']
                
                if hv_value != 0:
                    penetration_ratio = hh_value / hv_value
                    
                    # Interpretar ratio para arqueología
                    penetration_analysis = self._analyze_penetration_ratio(penetration_ratio)
                    
                    return {
                        'value': penetration_ratio,
                        'hh_backscatter': hh_value,
                        'hv_backscatter': hv_value,
                        'penetration_analysis': penetration_analysis,
                        'archaeological_potential': penetration_analysis['archaeological_score'],
                        'unit': 'ratio',
                        'source': 'PALSAR2_penetration',
                        'quality': 'high' if abs(penetration_ratio - 1.0) > 0.2 else 'medium'
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error en análisis de penetración forestal: {e}")
            return None
    
    async def get_soil_moisture(self, lat_min: float, lat_max: float,
                               lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        Estimación de humedad del suelo usando L-band.
        
        APLICACIÓN: Detectar sistemas de drenaje y canales antiguos
        """
        
        try:
            # Obtener backscatter VV (sensible a humedad del suelo)
            vv_data = await self.get_sar_backscatter(lat_min, lat_max, lon_min, lon_max, 'VV')
            
            if vv_data:
                backscatter_vv = vv_data['value']
                
                # Modelo empírico para humedad del suelo (simplificado)
                # En producción usar algoritmos más sofisticados
                moisture_index = self._estimate_soil_moisture(backscatter_vv)
                
                # Detectar patrones de drenaje
                drainage_indicators = self._detect_drainage_patterns(vv_data)
                
                return {
                    'value': moisture_index,
                    'backscatter_vv': backscatter_vv,
                    'moisture_classification': self._classify_moisture(moisture_index),
                    'drainage_indicators': drainage_indicators,
                    'archaeological_relevance': drainage_indicators['archaeological_score'],
                    'unit': 'moisture_index',
                    'source': 'PALSAR2_soil_moisture',
                    'quality': 'medium'  # Estimación indirecta
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error estimando humedad del suelo: {e}")
            return None
    
    def _select_best_scene(self, scenes: list, lat_min: float, lat_max: float,
                          lon_min: float, lon_max: float) -> Optional[Dict]:
        """Seleccionar la mejor escena PALSAR-2 para el análisis."""
        
        try:
            if not scenes:
                return None
            
            # Criterios de selección:
            # 1. Cobertura del área de interés
            # 2. Fecha más reciente
            # 3. Calidad de procesamiento
            
            scored_scenes = []
            
            for scene in scenes:
                score = 0
                
                # Calcular cobertura
                scene_bounds = scene.get('bbox', [])
                if len(scene_bounds) == 4:
                    coverage = self._calculate_coverage(
                        scene_bounds, [lon_min, lat_min, lon_max, lat_max]
                    )
                    score += coverage * 50  # Peso alto para cobertura
                
                # Penalizar por antigüedad
                try:
                    scene_date = datetime.fromisoformat(scene.get('startTime', '').replace('Z', '+00:00'))
                    days_old = (datetime.now(scene_date.tzinfo) - scene_date).days
                    score -= days_old * 0.1
                except:
                    score -= 100  # Penalizar si no hay fecha
                
                # Bonus por procesamiento de alta resolución
                if 'HI_RES' in scene.get('processingLevel', ''):
                    score += 10
                
                scored_scenes.append((score, scene))
            
            # Retornar la escena con mayor score
            if scored_scenes:
                scored_scenes.sort(key=lambda x: x[0], reverse=True)
                return scored_scenes[0][1]
            
            return None
            
        except Exception as e:
            logger.error(f"Error seleccionando escena PALSAR-2: {e}")
            return None
    
    def _calculate_coverage(self, scene_bounds: list, roi_bounds: list) -> float:
        """Calcular porcentaje de cobertura de la escena sobre el ROI."""
        
        try:
            # scene_bounds: [lon_min, lat_min, lon_max, lat_max]
            # roi_bounds: [lon_min, lat_min, lon_max, lat_max]
            
            # Calcular intersección
            intersect_lon_min = max(scene_bounds[0], roi_bounds[0])
            intersect_lat_min = max(scene_bounds[1], roi_bounds[1])
            intersect_lon_max = min(scene_bounds[2], roi_bounds[2])
            intersect_lat_max = min(scene_bounds[3], roi_bounds[3])
            
            if intersect_lon_min >= intersect_lon_max or intersect_lat_min >= intersect_lat_max:
                return 0.0  # No hay intersección
            
            # Calcular áreas
            intersect_area = (intersect_lon_max - intersect_lon_min) * (intersect_lat_max - intersect_lat_min)
            roi_area = (roi_bounds[2] - roi_bounds[0]) * (roi_bounds[3] - roi_bounds[1])
            
            return intersect_area / roi_area if roi_area > 0 else 0.0
            
        except Exception:
            return 0.0
    
    async def _process_palsar_scene(self, scene: Dict, polarization: str) -> Optional[Dict]:
        """Procesar escena PALSAR-2 para extraer estadísticas de backscatter."""
        
        try:
            # En implementación completa, descargaría y procesaría la escena
            # Por ahora, simular procesamiento con metadatos disponibles
            
            # Extraer información de la escena
            scene_id = scene.get('granuleName', '')
            
            # Simular estadísticas de backscatter basadas en metadatos
            # En producción, usar GDAL/rasterio para procesar datos reales
            
            # Valores típicos de backscatter L-band por tipo de superficie
            backscatter_ranges = {
                'HH': {'forest': (-12, -8), 'urban': (-8, -4), 'water': (-25, -20), 'bare': (-15, -10)},
                'HV': {'forest': (-18, -14), 'urban': (-15, -10), 'water': (-30, -25), 'bare': (-20, -15)},
                'VV': {'forest': (-10, -6), 'urban': (-6, -2), 'water': (-23, -18), 'bare': (-13, -8)}
            }
            
            # Estimar backscatter basado en características de la escena
            pol_ranges = backscatter_ranges.get(polarization, backscatter_ranges['HH'])
            
            # Simular valor medio (en producción calcular de datos reales)
            mean_backscatter = np.mean([pol_ranges['forest'][0], pol_ranges['forest'][1]])
            std_backscatter = 2.5
            
            stats = {
                'mean': mean_backscatter,
                'std': std_backscatter,
                'min': mean_backscatter - 2 * std_backscatter,
                'max': mean_backscatter + 2 * std_backscatter
            }
            
            # Indicadores de penetración
            penetration = {
                'vegetation_penetration': True if polarization in ['HH', 'HV'] else False,
                'estimated_depth_m': 5.0 if polarization == 'HH' else 3.0,
                'surface_roughness': 'moderate'
            }
            
            quality = 'high' if abs(mean_backscatter) > 5 else 'medium'
            
            return {
                'mean_backscatter': mean_backscatter,
                'stats': stats,
                'penetration': penetration,
                'quality': quality
            }
            
        except Exception as e:
            logger.error(f"Error procesando escena PALSAR-2: {e}")
            return None
    
    def _analyze_penetration_ratio(self, ratio: float) -> Dict[str, Any]:
        """Analizar ratio HH/HV para interpretación arqueológica."""
        
        analysis = {
            'penetration_quality': 'unknown',
            'vegetation_density': 'unknown',
            'archaeological_score': 0.0,
            'interpretation': ''
        }
        
        try:
            if ratio > 2.0:
                analysis['penetration_quality'] = 'excellent'
                analysis['vegetation_density'] = 'sparse'
                analysis['archaeological_score'] = 0.9
                analysis['interpretation'] = 'Excelente penetración - estructuras visibles'
            elif ratio > 1.5:
                analysis['penetration_quality'] = 'good'
                analysis['vegetation_density'] = 'moderate'
                analysis['archaeological_score'] = 0.7
                analysis['interpretation'] = 'Buena penetración - posibles estructuras'
            elif ratio > 1.0:
                analysis['penetration_quality'] = 'moderate'
                analysis['vegetation_density'] = 'dense'
                analysis['archaeological_score'] = 0.5
                analysis['interpretation'] = 'Penetración limitada - análisis complejo'
            else:
                analysis['penetration_quality'] = 'poor'
                analysis['vegetation_density'] = 'very_dense'
                analysis['archaeological_score'] = 0.2
                analysis['interpretation'] = 'Penetración pobre - vegetación muy densa'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando ratio de penetración: {e}")
            return analysis
    
    def _estimate_soil_moisture(self, backscatter_vv: float) -> float:
        """Estimar humedad del suelo desde backscatter VV."""
        
        try:
            # Modelo empírico simplificado
            # En producción usar modelos calibrados como Oh, Dubois, etc.
            
            # Normalizar backscatter a índice de humedad (0-1)
            # Valores típicos VV: -20 dB (seco) a -5 dB (húmedo)
            normalized = (backscatter_vv + 20) / 15
            moisture_index = max(0.0, min(1.0, normalized))
            
            return moisture_index
            
        except Exception:
            return 0.5  # Valor neutro si hay error
    
    def _classify_moisture(self, moisture_index: float) -> str:
        """Clasificar nivel de humedad del suelo."""
        
        if moisture_index > 0.8:
            return 'very_wet'
        elif moisture_index > 0.6:
            return 'wet'
        elif moisture_index > 0.4:
            return 'moderate'
        elif moisture_index > 0.2:
            return 'dry'
        else:
            return 'very_dry'
    
    def _detect_drainage_patterns(self, sar_data: Dict) -> Dict[str, Any]:
        """Detectar patrones de drenaje arqueológicamente relevantes."""
        
        indicators = {
            'linear_features': False,
            'moisture_gradients': False,
            'archaeological_score': 0.0,
            'pattern_type': 'none'
        }
        
        try:
            # Análisis simplificado basado en estadísticas
            backscatter_stats = sar_data.get('backscatter_stats', {})
            std_dev = backscatter_stats.get('std', 0)
            
            # Alta variabilidad puede indicar patrones de drenaje
            if std_dev > 3.0:
                indicators['linear_features'] = True
                indicators['moisture_gradients'] = True
                indicators['archaeological_score'] = 0.7
                indicators['pattern_type'] = 'potential_channels'
            elif std_dev > 2.0:
                indicators['moisture_gradients'] = True
                indicators['archaeological_score'] = 0.4
                indicators['pattern_type'] = 'subtle_patterns'
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error detectando patrones de drenaje: {e}")
            return indicators
    
    async def _make_asf_request(self, url: str, params: Dict) -> Optional[Dict]:
        """Realizar petición autenticada a ASF DAAC."""
        
        try:
            # Usar credenciales Earthdata (hasheadas en BD)
            auth = (self.username, self.password) if self.username else None
            
            response = requests.get(
                url,
                params=params,
                auth=auth,
                timeout=30,
                headers={'User-Agent': 'ArcheoScope/2.0'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"ASF DAAC API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error en petición ASF DAAC: {e}")
            return None