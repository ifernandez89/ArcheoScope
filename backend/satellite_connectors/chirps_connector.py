#!/usr/bin/env python3
"""
CHIRPS Connector - Climate Hazards Group InfraRed Precipitation
==============================================================

CHIRPS (USGS/UCSB) - Instrumento 15/15
- Resolución: 0.05° (~5km) diaria/mensual
- Cobertura: 50°S-50°N desde 1981
- Producto: Precipitación satelital + estaciones
- API: USGS/NASA Giovanni + Direct FTP

APLICACIONES ARQUEOLÓGICAS:
- Análisis de patrones de precipitación histórica
- Identificación de períodos de sequía/abundancia
- Correlación con ocupación/abandono de sitios
- Análisis de sistemas de manejo de agua antiguos
"""

import requests
import numpy as np
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
import ftplib
import tempfile
import os
import xarray as xr

logger = logging.getLogger(__name__)

class CHIRPSConnector:
    """Conector para datos CHIRPS de precipitación."""
    
    def __init__(self):
        """Inicializar conector CHIRPS."""
        
        # URLs de diferentes fuentes CHIRPS
        self.sources = {
            'giovanni': 'https://giovanni.gsfc.nasa.gov/giovanni/daac-bin/service_manager.pl',
            'iridl': 'https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.daily-improved/.global/.0p05deg/.prcp',
            'ftp': 'ftp.chg.ucsb.edu',
            'api': 'https://climateserv.servirglobal.net/chirps'
        }
        
        # Productos CHIRPS disponibles
        self.products = {
            'daily': 'chirps-v2.0.daily',
            'pentad': 'chirps-v2.0.pentads',
            'monthly': 'chirps-v2.0.monthly',
            'annual': 'chirps-v2.0.annual'
        }
        
        logger.info("🌧️ CHIRPS Connector initialized")
    
    async def get_precipitation_history(self, lat_min: float, lat_max: float,
                                       lon_min: float, lon_max: float,
                                       years_back: int = 20) -> Dict[str, Any]:
        """
        Obtener historial de precipitación CHIRPS.
        
        Args:
            years_back: Años hacia atrás para análisis histórico
        """
        
        try:
            # STUB: Retornar estimación basada en latitud
            # En producción: conectar a API real
            
            # Estimar precipitación anual basada en latitud
            annual_precip = self._estimate_precipitation(lat_min, lat_max, lon_min, lon_max)
            
            logger.info(f"🌧️ CHIRPS: Precipitación estimada: {annual_precip:.1f} mm/año")
            
            # Retornar InstrumentMeasurement
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent.parent))
            from instrument_contract import InstrumentMeasurement
            
            return InstrumentMeasurement.create_derived(
                instrument_name="CHIRPS",
                measurement_type="precipitation_annual",
                value=annual_precip,
                unit="mm/year",
                confidence=0.6,
                derivation_method="Latitude-based precipitation model (stub)",
                source="CHIRPS (estimated)"
            )
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo historial CHIRPS: {e}")
            return None
    
    async def get_drought_analysis(self, lat_min: float, lat_max: float,
                                  lon_min: float, lon_max: float,
                                  reference_period: int = 30) -> Dict[str, Any]:
        """
        Análisis de sequías usando CHIRPS.
        
        APLICACIÓN: Correlacionar períodos de sequía con abandono de sitios
        """
        
        try:
            # Obtener datos de precipitación
            precip_data = await self.get_precipitation_history(
                lat_min, lat_max, lon_min, lon_max, reference_period
            )
            
            if not precip_data:
                return None
            
            precipitation = precip_data['precipitation_data']
            
            # Calcular índices de sequía
            drought_indices = self._calculate_drought_indices(precipitation)
            
            # Identificar eventos de sequía significativos
            drought_events = self._identify_drought_events(drought_indices)
            
            # Analizar implicaciones arqueológicas
            archaeological_implications = self._analyze_drought_archaeology(drought_events)
            
            return {
                'value': drought_indices['spi_mean'],  # Standardized Precipitation Index
                'drought_indices': drought_indices,
                'drought_events': drought_events,
                'archaeological_implications': archaeological_implications,
                'severity_classification': self._classify_drought_severity(drought_indices['spi_mean']),
                'unit': 'spi_index',
                'source': 'CHIRPS_drought_analysis',
                'quality': 'high'
            }
            
        except Exception as e:
            logger.error(f"Error en análisis de sequías: {e}")
            return None
    
    async def get_seasonal_patterns(self, lat_min: float, lat_max: float,
                                   lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        Analizar patrones estacionales de precipitación.
        
        APLICACIÓN: Entender ciclos agrícolas y ocupación estacional
        """
        
        try:
            # Obtener datos mensuales de los últimos 10 años
            precip_data = await self.get_precipitation_history(
                lat_min, lat_max, lon_min, lon_max, 10
            )
            
            if not precip_data:
                return None
            
            # Analizar patrones estacionales
            seasonal_analysis = self._analyze_seasonal_patterns(
                precip_data['precipitation_data']
            )
            
            # Identificar temporadas agrícolas
            agricultural_seasons = self._identify_agricultural_seasons(seasonal_analysis)
            
            return {
                'value': seasonal_analysis['seasonality_index'],
                'seasonal_patterns': seasonal_analysis,
                'agricultural_seasons': agricultural_seasons,
                'archaeological_relevance': self._assess_seasonal_archaeology(seasonal_analysis),
                'unit': 'seasonality_index',
                'source': 'CHIRPS_seasonal_analysis',
                'quality': 'high'
            }
            
        except Exception as e:
            logger.error(f"Error analizando patrones estacionales: {e}")
            return None
    
    async def get_water_management_indicators(self, lat_min: float, lat_max: float,
                                             lon_min: float, lon_max: float) -> Dict[str, Any]:
        """
        Indicadores para sistemas de manejo de agua antiguos.
        
        APLICACIÓN: Detectar necesidad histórica de sistemas de irrigación/drenaje
        """
        
        try:
            # Obtener análisis de sequías y patrones estacionales
            drought_analysis = await self.get_drought_analysis(lat_min, lat_max, lon_min, lon_max)
            seasonal_patterns = await self.get_seasonal_patterns(lat_min, lat_max, lon_min, lon_max)
            
            if not drought_analysis or not seasonal_patterns:
                return None
            
            # Calcular indicadores de manejo de agua
            water_management = self._calculate_water_management_indicators(
                drought_analysis, seasonal_patterns
            )
            
            return {
                'value': water_management['management_necessity_score'],
                'water_management_indicators': water_management,
                'archaeological_predictions': self._predict_water_systems(water_management),
                'unit': 'management_score',
                'source': 'CHIRPS_water_management',
                'quality': 'high'
            }
            
        except Exception as e:
            logger.error(f"Error analizando manejo de agua: {e}")
            return None
    
    async def _get_chirps_api(self, lat_min: float, lat_max: float,
                             lon_min: float, lon_max: float,
                             start_date: datetime, end_date: datetime) -> Optional[Dict]:
        """Obtener datos CHIRPS via API ClimateSERV."""
        
        try:
            # Parámetros para API ClimateSERV
            params = {
                'datatype': 'chirps',
                'begintime': start_date.strftime('%m/%d/%Y'),
                'endtime': end_date.strftime('%m/%d/%Y'),
                'intervaltype': 'monthly',
                'operationtype': 'average',
                'callback': 'successCallback',
                'dateType_Category': 'default',
                'isZip_CurrentDataType': 'false',
                'geometry': json.dumps({
                    'type': 'Polygon',
                    'coordinates': [[
                        [lon_min, lat_min],
                        [lon_max, lat_min],
                        [lon_max, lat_max],
                        [lon_min, lat_max],
                        [lon_min, lat_min]
                    ]]
                })
            }
            
            response = requests.get(
                self.sources['api'],
                params=params,
                timeout=60
            )
            
            if response.status_code == 200:
                # Procesar respuesta JSONP
                content = response.text
                if content.startswith('successCallback('):
                    json_str = content[16:-1]  # Remover callback wrapper
                    data = json.loads(json_str)
                    
                    if 'data' in data:
                        # Procesar datos de precipitación
                        precip_values = []
                        dates = []
                        
                        for item in data['data']:
                            if 'value' in item and item['value'] is not None:
                                precip_values.append(item['value'])
                                dates.append(item.get('date', ''))
                        
                        if precip_values:
                            return {
                                'values': precip_values,
                                'dates': dates,
                                'statistics': {
                                    'mean': np.mean(precip_values),
                                    'std': np.std(precip_values),
                                    'min': np.min(precip_values),
                                    'max': np.max(precip_values),
                                    'total': np.sum(precip_values)
                                }
                            }
            
            return None
            
        except Exception as e:
            logger.error(f"Error API CHIRPS: {e}")
            return None
    
    async def _get_chirps_giovanni(self, lat_min: float, lat_max: float,
                                  lon_min: float, lon_max: float,
                                  start_date: datetime, end_date: datetime) -> Optional[Dict]:
        """Obtener datos CHIRPS via NASA Giovanni."""
        
        try:
            # Implementación simplificada - Giovanni requiere configuración compleja
            # En producción implementar cliente Giovanni completo
            return None
            
        except Exception as e:
            logger.error(f"Error Giovanni CHIRPS: {e}")
            return None
    
    async def _get_chirps_iridl(self, lat_min: float, lat_max: float,
                               lon_min: float, lon_max: float,
                               start_date: datetime, end_date: datetime) -> Optional[Dict]:
        """Obtener datos CHIRPS via IRI Data Library."""
        
        try:
            # Construir URL IRI/LDEO
            url = (f"{self.sources['iridl']}/X/{lon_min}/{lon_max}/RANGE/"
                   f"Y/{lat_min}/{lat_max}/RANGE/"
                   f"T/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}/RANGE/"
                   "data.nc")
            
            response = requests.get(url, timeout=60)
            
            if response.status_code == 200:
                # Guardar temporalmente el NetCDF
                with tempfile.NamedTemporaryFile(suffix='.nc', delete=False) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_path = tmp_file.name
                
                try:
                    # Leer con xarray
                    with xr.open_dataset(tmp_path) as ds:
                        if 'prcp' in ds.variables:
                            precip_data = ds['prcp']
                            
                            # Calcular estadísticas espaciales y temporales
                            spatial_mean = precip_data.mean(dim=['X', 'Y'])
                            values = spatial_mean.values
                            
                            return {
                                'values': values.tolist(),
                                'dates': [str(t) for t in ds.T.values],
                                'statistics': {
                                    'mean': float(np.mean(values)),
                                    'std': float(np.std(values)),
                                    'min': float(np.min(values)),
                                    'max': float(np.max(values)),
                                    'total': float(np.sum(values))
                                }
                            }
                
                finally:
                    os.unlink(tmp_path)
            
            return None
            
        except Exception as e:
            logger.error(f"Error IRI CHIRPS: {e}")
            return None
    
    def _analyze_precipitation_archaeology(self, precip_data: Dict) -> Dict[str, Any]:
        """Analizar precipitación desde perspectiva arqueológica."""
        
        analysis = {
            'climate_stability': 'unknown',
            'agricultural_viability': 'unknown',
            'water_stress_periods': [],
            'optimal_occupation_periods': []
        }
        
        try:
            values = precip_data['values']
            stats = precip_data['statistics']
            
            # Estabilidad climática (baja variabilidad = más estable)
            cv = stats['std'] / stats['mean'] if stats['mean'] > 0 else 1.0
            
            if cv < 0.2:
                analysis['climate_stability'] = 'very_stable'
            elif cv < 0.4:
                analysis['climate_stability'] = 'stable'
            elif cv < 0.6:
                analysis['climate_stability'] = 'moderate'
            else:
                analysis['climate_stability'] = 'unstable'
            
            # Viabilidad agrícola
            mean_annual = stats['mean'] * 12  # Aproximación anual
            
            if mean_annual > 1000:
                analysis['agricultural_viability'] = 'excellent'
            elif mean_annual > 600:
                analysis['agricultural_viability'] = 'good'
            elif mean_annual > 300:
                analysis['agricultural_viability'] = 'marginal'
            else:
                analysis['agricultural_viability'] = 'poor'
            
            # Identificar períodos de estrés hídrico
            threshold = stats['mean'] - stats['std']
            stress_periods = [i for i, v in enumerate(values) if v < threshold]
            analysis['water_stress_periods'] = stress_periods
            
            # Períodos óptimos (precipitación abundante pero no excesiva)
            optimal_threshold_low = stats['mean']
            optimal_threshold_high = stats['mean'] + stats['std']
            optimal_periods = [i for i, v in enumerate(values) 
                             if optimal_threshold_low <= v <= optimal_threshold_high]
            analysis['optimal_occupation_periods'] = optimal_periods
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando precipitación arqueológica: {e}")
            return analysis
    
    def _calculate_drought_indices(self, precip_data: Dict) -> Dict[str, float]:
        """Calcular índices de sequía."""
        
        indices = {
            'spi_mean': 0.0,
            'drought_frequency': 0.0,
            'max_drought_duration': 0,
            'drought_intensity': 0.0
        }
        
        try:
            values = np.array(precip_data['values'])
            stats = precip_data['statistics']
            
            # Standardized Precipitation Index (SPI) simplificado
            if stats['std'] > 0:
                spi_values = (values - stats['mean']) / stats['std']
                indices['spi_mean'] = float(np.mean(spi_values))
                
                # Frecuencia de sequía (SPI < -1)
                drought_months = np.sum(spi_values < -1)
                indices['drought_frequency'] = drought_months / len(values)
                
                # Duración máxima de sequía
                drought_periods = []
                current_drought = 0
                
                for spi in spi_values:
                    if spi < -1:
                        current_drought += 1
                    else:
                        if current_drought > 0:
                            drought_periods.append(current_drought)
                        current_drought = 0
                
                if current_drought > 0:
                    drought_periods.append(current_drought)
                
                indices['max_drought_duration'] = max(drought_periods) if drought_periods else 0
                
                # Intensidad promedio de sequía
                drought_spi = spi_values[spi_values < -1]
                indices['drought_intensity'] = float(np.mean(np.abs(drought_spi))) if len(drought_spi) > 0 else 0.0
            
            return indices
            
        except Exception as e:
            logger.error(f"Error calculando índices de sequía: {e}")
            return indices
    
    def _identify_drought_events(self, drought_indices: Dict) -> List[Dict]:
        """Identificar eventos de sequía significativos."""
        
        events = []
        
        try:
            # Crear eventos basados en índices
            if drought_indices['max_drought_duration'] > 6:  # Sequías > 6 meses
                events.append({
                    'type': 'severe_drought',
                    'duration_months': drought_indices['max_drought_duration'],
                    'intensity': drought_indices['drought_intensity'],
                    'archaeological_impact': 'high'
                })
            
            if drought_indices['drought_frequency'] > 0.3:  # >30% del tiempo en sequía
                events.append({
                    'type': 'chronic_drought',
                    'frequency': drought_indices['drought_frequency'],
                    'archaeological_impact': 'moderate'
                })
            
            return events
            
        except Exception as e:
            logger.error(f"Error identificando eventos de sequía: {e}")
            return events
    
    def _analyze_drought_archaeology(self, drought_events: List[Dict]) -> Dict[str, Any]:
        """Analizar implicaciones arqueológicas de sequías."""
        
        implications = {
            'site_abandonment_risk': 'low',
            'water_management_necessity': 'low',
            'agricultural_adaptation_required': False,
            'population_stress_indicators': []
        }
        
        try:
            severe_droughts = [e for e in drought_events if e['type'] == 'severe_drought']
            chronic_droughts = [e for e in drought_events if e['type'] == 'chronic_drought']
            
            if severe_droughts:
                implications['site_abandonment_risk'] = 'high'
                implications['water_management_necessity'] = 'critical'
                implications['agricultural_adaptation_required'] = True
                implications['population_stress_indicators'].append('Sequías severas documentadas')
            
            if chronic_droughts:
                implications['water_management_necessity'] = 'high'
                implications['agricultural_adaptation_required'] = True
                implications['population_stress_indicators'].append('Estrés hídrico crónico')
            
            return implications
            
        except Exception as e:
            logger.error(f"Error analizando arqueología de sequías: {e}")
            return implications
    
    def _classify_drought_severity(self, spi_mean: float) -> str:
        """Clasificar severidad de sequía basada en SPI."""
        
        if spi_mean <= -2.0:
            return 'extreme_drought'
        elif spi_mean <= -1.5:
            return 'severe_drought'
        elif spi_mean <= -1.0:
            return 'moderate_drought'
        elif spi_mean <= -0.5:
            return 'mild_drought'
        elif spi_mean >= 2.0:
            return 'extreme_wet'
        elif spi_mean >= 1.5:
            return 'severe_wet'
        elif spi_mean >= 1.0:
            return 'moderate_wet'
        elif spi_mean >= 0.5:
            return 'mild_wet'
        else:
            return 'normal'
    
    def _analyze_seasonal_patterns(self, precip_data: Dict) -> Dict[str, Any]:
        """Analizar patrones estacionales de precipitación."""
        
        patterns = {
            'seasonality_index': 0.0,
            'wet_season_months': [],
            'dry_season_months': [],
            'peak_precipitation_month': 1,
            'precipitation_regime': 'unknown'
        }
        
        try:
            values = precip_data['values']
            
            # Calcular promedios mensuales (asumiendo datos mensuales)
            if len(values) >= 12:
                # Agrupar por mes
                monthly_means = []
                for month in range(12):
                    month_values = [values[i] for i in range(month, len(values), 12)]
                    monthly_means.append(np.mean(month_values))
                
                # Índice de estacionalidad
                patterns['seasonality_index'] = np.std(monthly_means) / np.mean(monthly_means)
                
                # Identificar estaciones
                mean_precip = np.mean(monthly_means)
                wet_months = [i+1 for i, p in enumerate(monthly_means) if p > mean_precip]
                dry_months = [i+1 for i, p in enumerate(monthly_means) if p <= mean_precip]
                
                patterns['wet_season_months'] = wet_months
                patterns['dry_season_months'] = dry_months
                patterns['peak_precipitation_month'] = int(np.argmax(monthly_means) + 1)
                
                # Clasificar régimen de precipitación
                patterns['precipitation_regime'] = self._classify_precipitation_regime(monthly_means)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analizando patrones estacionales: {e}")
            return patterns
    
    def _classify_precipitation_regime(self, monthly_means: List[float]) -> str:
        """Clasificar régimen de precipitación."""
        
        try:
            # Encontrar picos de precipitación
            max_month = np.argmax(monthly_means)
            min_month = np.argmin(monthly_means)
            
            # Clasificar según distribución temporal
            if max_month in [5, 6, 7, 8]:  # Jun-Sep (NH summer)
                return 'summer_monsoon'
            elif max_month in [11, 0, 1, 2]:  # Dec-Mar (NH winter)
                return 'winter_precipitation'
            elif len([m for m in monthly_means if m > np.mean(monthly_means)]) > 8:
                return 'year_round'
            else:
                return 'seasonal'
                
        except Exception:
            return 'unknown'
    
    def _identify_agricultural_seasons(self, seasonal_analysis: Dict) -> Dict[str, Any]:
        """Identificar temporadas agrícolas basadas en precipitación."""
        
        seasons = {
            'planting_season': [],
            'growing_season': [],
            'harvest_season': [],
            'agricultural_viability': 'unknown'
        }
        
        try:
            wet_months = seasonal_analysis['wet_season_months']
            dry_months = seasonal_analysis['dry_season_months']
            
            if wet_months:
                # Temporada de siembra al inicio de lluvias
                seasons['planting_season'] = [min(wet_months)]
                
                # Temporada de crecimiento durante lluvias
                seasons['growing_season'] = wet_months
                
                # Cosecha al final de lluvias/inicio de secas
                if dry_months:
                    harvest_candidates = [m for m in dry_months if m > max(wet_months)]
                    if harvest_candidates:
                        seasons['harvest_season'] = [min(harvest_candidates)]
                    else:
                        seasons['harvest_season'] = [max(wet_months)]
            
            # Evaluar viabilidad agrícola
            if len(wet_months) >= 4:
                seasons['agricultural_viability'] = 'good'
            elif len(wet_months) >= 2:
                seasons['agricultural_viability'] = 'marginal'
            else:
                seasons['agricultural_viability'] = 'poor'
            
            return seasons
            
        except Exception as e:
            logger.error(f"Error identificando temporadas agrícolas: {e}")
            return seasons
    
    def _assess_seasonal_archaeology(self, seasonal_analysis: Dict) -> Dict[str, Any]:
        """Evaluar relevancia arqueológica de patrones estacionales."""
        
        relevance = {
            'settlement_patterns': 'unknown',
            'agricultural_indicators': [],
            'seasonal_mobility': 'unknown',
            'water_storage_necessity': 'unknown'
        }
        
        try:
            seasonality = seasonal_analysis['seasonality_index']
            wet_months = len(seasonal_analysis['wet_season_months'])
            dry_months = len(seasonal_analysis['dry_season_months'])
            
            # Patrones de asentamiento
            if seasonality > 1.0:  # Alta estacionalidad
                relevance['settlement_patterns'] = 'seasonal_occupation_likely'
                relevance['seasonal_mobility'] = 'high'
            else:
                relevance['settlement_patterns'] = 'permanent_occupation_viable'
                relevance['seasonal_mobility'] = 'low'
            
            # Indicadores agrícolas
            if wet_months >= 4:
                relevance['agricultural_indicators'].append('Agricultura de temporal viable')
            if dry_months >= 6:
                relevance['agricultural_indicators'].append('Necesidad de irrigación')
                relevance['water_storage_necessity'] = 'high'
            
            return relevance
            
        except Exception as e:
            logger.error(f"Error evaluando arqueología estacional: {e}")
            return relevance
    
    def _calculate_water_management_indicators(self, drought_analysis: Dict, 
                                             seasonal_patterns: Dict) -> Dict[str, Any]:
        """Calcular indicadores de necesidad de manejo de agua."""
        
        indicators = {
            'management_necessity_score': 0.0,
            'irrigation_necessity': False,
            'storage_necessity': False,
            'drainage_necessity': False,
            'system_complexity_required': 'none'
        }
        
        try:
            # Factores de sequía
            drought_score = 0.0
            if drought_analysis['drought_indices']['drought_frequency'] > 0.2:
                drought_score += 0.3
            if drought_analysis['drought_indices']['max_drought_duration'] > 3:
                drought_score += 0.3
            
            # Factores estacionales
            seasonal_score = 0.0
            seasonality = seasonal_patterns['seasonal_patterns']['seasonality_index']
            if seasonality > 0.8:
                seasonal_score += 0.4
            
            # Score total
            indicators['management_necessity_score'] = drought_score + seasonal_score
            
            # Necesidades específicas
            if indicators['management_necessity_score'] > 0.6:
                indicators['irrigation_necessity'] = True
                indicators['storage_necessity'] = True
                indicators['system_complexity_required'] = 'complex'
            elif indicators['management_necessity_score'] > 0.3:
                indicators['storage_necessity'] = True
                indicators['system_complexity_required'] = 'moderate'
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error calculando indicadores de manejo de agua: {e}")
            return indicators
    
    def _predict_water_systems(self, water_management: Dict) -> Dict[str, Any]:
        """Predecir tipos de sistemas de agua esperables."""
        
        predictions = {
            'expected_systems': [],
            'archaeological_signatures': [],
            'detection_methods': []
        }
        
        try:
            necessity_score = water_management['management_necessity_score']
            
            if water_management['irrigation_necessity']:
                predictions['expected_systems'].append('Canales de irrigación')
                predictions['archaeological_signatures'].append('Canales lineales, compuertas')
                predictions['detection_methods'].append('SAR L-band, análisis topográfico')
            
            if water_management['storage_necessity']:
                predictions['expected_systems'].append('Reservorios, cisternas')
                predictions['archaeological_signatures'].append('Depresiones artificiales, muros de contención')
                predictions['detection_methods'].append('LiDAR, análisis de elevación')
            
            if necessity_score > 0.7:
                predictions['expected_systems'].append('Sistemas de drenaje')
                predictions['archaeological_signatures'].append('Redes de drenaje, terrazas')
                predictions['detection_methods'].append('Análisis de pendientes, SAR')
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error prediciendo sistemas de agua: {e}")
            return predictions

    
    def _estimate_precipitation(self, lat_min: float, lat_max: float, 
                               lon_min: float, lon_max: float) -> float:
        """Estimar precipitación anual basada en latitud."""
        
        center_lat = (lat_min + lat_max) / 2
        
        # Modelo simple basado en latitud
        abs_lat = abs(center_lat)
        
        if abs_lat < 10:  # Tropical
            return 2000.0
        elif abs_lat < 23:  # Subtropical
            return 800.0
        elif abs_lat < 35:  # Templado seco
            return 500.0
        elif abs_lat < 50:  # Templado húmedo
            return 1000.0
        else:  # Polar
            return 300.0
