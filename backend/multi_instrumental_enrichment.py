#!/usr/bin/env python3
"""
ArcheoScope - Multi-Instrumental Enrichment System
Sistema de enriquecimiento multi-instrumental para candidatas arqueológicas

🧠 REGLA DE ORO:
LiDAR responde a: FORMA
Otros sistemas responden a: MATERIAL, HUMEDAD, TEMPERATURA, COMPACTACIÓN, QUÍMICA, DINÁMICA TEMPORAL

👉 La magia está en SUPERPOSICIÓN, no en reemplazo
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class InstrumentType(Enum):
    """Tipos de instrumentos disponibles"""
    LIDAR = "lidar"                          # Forma
    SAR = "sar"                              # Compactación, textura, humedad
    INSAR = "insar"                          # Microdeformaciones
    MULTISPECTRAL = "multispectral"          # Estrés vegetal, química suelo
    THERMAL = "thermal"                      # Inercia térmica, materiales
    HYPERSPECTRAL = "hyperspectral"          # Firmas minerales, suelos alterados
    GRAVIMETRY = "gravimetry"                # Anomalías de densidad
    MAGNETOMETRY = "magnetometry"            # Hornos, metalurgia, suelos quemados
    HISTORICAL_PHOTOGRAMMETRY = "historical" # Fotos aéreas antiguas
    MULTITEMPORAL = "multitemporal"          # Persistencia temporal


@dataclass
class InstrumentSignal:
    """Señal de un instrumento específico"""
    
    instrument: InstrumentType
    detected: bool
    confidence: float  # 0-1
    
    # Valores específicos del instrumento
    values: Dict[str, float]
    
    # Metadata
    source: str
    acquisition_date: Optional[str] = None
    resolution_m: Optional[float] = None
    
    # Interpretación
    interpretation: Optional[str] = None


@dataclass
class MultiInstrumentalCandidate:
    """Candidata enriquecida con múltiples instrumentos"""
    
    candidate_id: str
    zone_id: str
    
    # Ubicación
    center_lat: float
    center_lon: float
    area_km2: float
    
    # Señales instrumentales
    signals: Dict[InstrumentType, InstrumentSignal]
    
    # Score multi-instrumental
    multi_instrumental_score: float  # 0-1
    
    # Convergencia (cuántos instrumentos detectan anomalía)
    convergence_count: int
    convergence_ratio: float  # 0-1
    
    # Recomendación
    recommended_action: str  # field_validation, detailed_analysis, monitor, discard
    
    # Persistencia temporal
    temporal_persistence: Optional[bool] = None
    temporal_years: Optional[int] = None


class MultiInstrumentalEnrichment:
    """
    Sistema de enriquecimiento multi-instrumental
    
    Combina señales de múltiples instrumentos para generar candidatas robustas
    """
    
    # Pesos por instrumento (basado en confiabilidad arqueológica)
    INSTRUMENT_WEIGHTS = {
        InstrumentType.LIDAR: 0.20,              # Forma
        InstrumentType.SAR: 0.18,                # Compactación (CLAVE)
        InstrumentType.THERMAL: 0.15,            # Inercia térmica (SUBUTILIZADO)
        InstrumentType.MULTISPECTRAL: 0.12,      # Estrés vegetal
        InstrumentType.MULTITEMPORAL: 0.15,      # Persistencia (CRÍTICO)
        InstrumentType.INSAR: 0.08,              # Microdeformaciones
        InstrumentType.HYPERSPECTRAL: 0.05,      # Firmas minerales (raro)
        InstrumentType.GRAVIMETRY: 0.04,         # Contexto
        InstrumentType.MAGNETOMETRY: 0.02,       # Actividad humana
        InstrumentType.HISTORICAL_PHOTOGRAMMETRY: 0.01  # Validación histórica
    }
    
    # Combos ganadores (instrumentos que se refuerzan mutuamente)
    WINNING_COMBOS = [
        # Combo mínimo pero potente
        {InstrumentType.LIDAR, InstrumentType.SAR, InstrumentType.MULTISPECTRAL, 
         InstrumentType.THERMAL, InstrumentType.MULTITEMPORAL},
        
        # Combo sin LiDAR (bosques densos)
        {InstrumentType.SAR, InstrumentType.THERMAL, InstrumentType.MULTISPECTRAL,
         InstrumentType.MULTITEMPORAL},
        
        # Combo agua
        {InstrumentType.SAR, InstrumentType.THERMAL, InstrumentType.MULTISPECTRAL},
        
        # Combo desierto
        {InstrumentType.MULTISPECTRAL, InstrumentType.THERMAL, InstrumentType.SAR}
    ]
    
    def __init__(self):
        logger.info("MultiInstrumentalEnrichment inicializado")
    
    def enrich_candidate(
        self,
        zone: Dict[str, Any],
        available_data: Dict[str, Any]
    ) -> MultiInstrumentalCandidate:
        """
        Enriquecer candidata con señales multi-instrumentales
        
        Args:
            zone: Zona prioritaria base
            available_data: Datos disponibles de instrumentos
        
        Returns:
            Candidata enriquecida
        """
        
        candidate_id = f"CND_{zone['zone_id']}"
        
        # Recolectar señales de cada instrumento
        signals = {}
        
        # 1. LiDAR (si disponible)
        if 'lidar' in available_data:
            signals[InstrumentType.LIDAR] = self._process_lidar_signal(
                available_data['lidar']
            )
        
        # 2. SAR (compactación)
        if 'sar' in available_data:
            signals[InstrumentType.SAR] = self._process_sar_signal(
                available_data['sar']
            )
        
        # 3. Térmico (inercia térmica)
        if 'thermal' in available_data:
            signals[InstrumentType.THERMAL] = self._process_thermal_signal(
                available_data['thermal']
            )
        
        # 4. Multiespectral (estrés vegetal)
        if 'multispectral' in available_data:
            signals[InstrumentType.MULTISPECTRAL] = self._process_multispectral_signal(
                available_data['multispectral']
            )
        
        # 5. Multitemporal (persistencia)
        if 'multitemporal' in available_data:
            signals[InstrumentType.MULTITEMPORAL] = self._process_multitemporal_signal(
                available_data['multitemporal']
            )
        
        # Calcular score multi-instrumental
        multi_score = self._calculate_multi_instrumental_score(signals)
        
        # Calcular convergencia
        convergence_count = sum(1 for s in signals.values() if s.detected)
        convergence_ratio = convergence_count / len(signals) if signals else 0.0
        
        # Determinar acción recomendada
        recommended_action = self._determine_recommended_action(
            multi_score, convergence_ratio, signals
        )
        
        # Verificar persistencia temporal
        temporal_persistence = None
        temporal_years = None
        if InstrumentType.MULTITEMPORAL in signals:
            mt_signal = signals[InstrumentType.MULTITEMPORAL]
            temporal_persistence = mt_signal.detected
            temporal_years = mt_signal.values.get('years_persistent', 0)
        
        return MultiInstrumentalCandidate(
            candidate_id=candidate_id,
            zone_id=zone['zone_id'],
            center_lat=zone['center']['lat'],
            center_lon=zone['center']['lon'],
            area_km2=zone['area_km2'],
            signals=signals,
            multi_instrumental_score=multi_score,
            convergence_count=convergence_count,
            convergence_ratio=convergence_ratio,
            recommended_action=recommended_action,
            temporal_persistence=temporal_persistence,
            temporal_years=temporal_years
        )
    
    def _process_lidar_signal(self, lidar_data: Dict[str, Any]) -> InstrumentSignal:
        """Procesar señal LiDAR (forma)"""
        
        # LiDAR detecta forma geométrica
        shape_detected = lidar_data.get('shape_detected', False)
        confidence = lidar_data.get('confidence', 0.0)
        
        values = {
            'shape_score': lidar_data.get('shape_score', 0.0),
            'geometric_regularity': lidar_data.get('geometric_regularity', 0.0),
            'elevation_anomaly': lidar_data.get('elevation_anomaly', 0.0)
        }
        
        interpretation = None
        if shape_detected:
            if values['geometric_regularity'] > 0.7:
                interpretation = "Geometric structure detected (platform, terrace, or linear feature)"
            else:
                interpretation = "Irregular elevation anomaly (possible mound or depression)"
        
        return InstrumentSignal(
            instrument=InstrumentType.LIDAR,
            detected=shape_detected,
            confidence=confidence,
            values=values,
            source=lidar_data.get('source', 'unknown'),
            acquisition_date=lidar_data.get('acquisition_date'),
            resolution_m=lidar_data.get('resolution_m'),
            interpretation=interpretation
        )
    
    def _process_sar_signal(self, sar_data: Dict[str, Any]) -> InstrumentSignal:
        """
        Procesar señal SAR (compactación, textura, humedad)
        
        🔥 CLAVE: SAR atraviesa vegetación y nubes
        Detecta: caminos, plataformas, muros enterrados
        """
        
        compaction_detected = sar_data.get('compaction_detected', False)
        confidence = sar_data.get('confidence', 0.0)
        
        values = {
            'backscatter_anomaly': sar_data.get('backscatter_anomaly', 0.0),
            'texture_score': sar_data.get('texture_score', 0.0),
            'coherence': sar_data.get('coherence', 0.0),
            'humidity_anomaly': sar_data.get('humidity_anomaly', 0.0)
        }
        
        interpretation = None
        if compaction_detected:
            if values['backscatter_anomaly'] > 2.0:
                interpretation = "High compaction detected (roads, platforms, walls)"
            elif values['texture_score'] > 0.6:
                interpretation = "Textural anomaly (possible buried structures)"
            else:
                interpretation = "Moderate compaction (historical traffic or construction)"
        
        return InstrumentSignal(
            instrument=InstrumentType.SAR,
            detected=compaction_detected,
            confidence=confidence,
            values=values,
            source=sar_data.get('source', 'Sentinel-1'),
            acquisition_date=sar_data.get('acquisition_date'),
            resolution_m=sar_data.get('resolution_m', 10.0),
            interpretation=interpretation
        )
    
    def _process_thermal_signal(self, thermal_data: Dict[str, Any]) -> InstrumentSignal:
        """
        Procesar señal térmica (inercia térmica, materiales)
        
        🔥 SUBUTILIZADO en arqueología
        Muros enterrados: más calientes de noche, más fríos de día
        """
        
        thermal_anomaly_detected = thermal_data.get('thermal_anomaly_detected', False)
        confidence = thermal_data.get('confidence', 0.0)
        
        values = {
            'lst_day_anomaly': thermal_data.get('lst_day_anomaly', 0.0),
            'lst_night_anomaly': thermal_data.get('lst_night_anomaly', 0.0),
            'thermal_inertia': thermal_data.get('thermal_inertia', 0.0),
            'diurnal_range_anomaly': thermal_data.get('diurnal_range_anomaly', 0.0)
        }
        
        interpretation = None
        if thermal_anomaly_detected:
            if values['lst_night_anomaly'] > 1.0 and values['lst_day_anomaly'] < -0.5:
                interpretation = "Buried structures detected (warmer at night, cooler at day)"
            elif values['thermal_inertia'] > 0.7:
                interpretation = "High thermal inertia (stone, compacted soil, or fill)"
            else:
                interpretation = "Thermal anomaly (material or moisture difference)"
        
        return InstrumentSignal(
            instrument=InstrumentType.THERMAL,
            detected=thermal_anomaly_detected,
            confidence=confidence,
            values=values,
            source=thermal_data.get('source', 'Landsat-8'),
            acquisition_date=thermal_data.get('acquisition_date'),
            resolution_m=thermal_data.get('resolution_m', 100.0),
            interpretation=interpretation
        )
    
    def _process_multispectral_signal(self, ms_data: Dict[str, Any]) -> InstrumentSignal:
        """
        Procesar señal multiespectral (estrés vegetal, química suelo)
        
        Las ciudades antiguas siguen afectando la vegetación siglos después
        """
        
        vegetation_anomaly_detected = ms_data.get('vegetation_anomaly_detected', False)
        confidence = ms_data.get('confidence', 0.0)
        
        values = {
            'ndvi_anomaly': ms_data.get('ndvi_anomaly', 0.0),
            'red_edge_anomaly': ms_data.get('red_edge_anomaly', 0.0),
            'ndwi_anomaly': ms_data.get('ndwi_anomaly', 0.0),
            'savi_anomaly': ms_data.get('savi_anomaly', 0.0)
        }
        
        interpretation = None
        if vegetation_anomaly_detected:
            if values['ndvi_anomaly'] < -0.05:
                interpretation = "Vegetation stress detected (altered soil chemistry or compaction)"
            elif values['ndwi_anomaly'] < -0.02:
                interpretation = "Moisture anomaly (drainage or soil composition change)"
            else:
                interpretation = "Spectral anomaly (possible ancient agriculture or occupation)"
        
        return InstrumentSignal(
            instrument=InstrumentType.MULTISPECTRAL,
            detected=vegetation_anomaly_detected,
            confidence=confidence,
            values=values,
            source=ms_data.get('source', 'Sentinel-2'),
            acquisition_date=ms_data.get('acquisition_date'),
            resolution_m=ms_data.get('resolution_m', 10.0),
            interpretation=interpretation
        )
    
    def _process_multitemporal_signal(self, mt_data: Dict[str, Any]) -> InstrumentSignal:
        """
        Procesar señal multitemporal (persistencia)
        
        🔥 CRÍTICO: Lo humano persiste, lo natural fluctúa
        """
        
        persistence_detected = mt_data.get('persistence_detected', False)
        confidence = mt_data.get('confidence', 0.0)
        
        values = {
            'years_persistent': mt_data.get('years_persistent', 0),
            'seasonal_stability': mt_data.get('seasonal_stability', 0.0),
            'change_resistance': mt_data.get('change_resistance', 0.0),
            'temporal_consistency': mt_data.get('temporal_consistency', 0.0)
        }
        
        interpretation = None
        if persistence_detected:
            years = values['years_persistent']
            if years >= 10:
                interpretation = f"High persistence ({years} years) - NOT natural fluctuation"
            elif years >= 5:
                interpretation = f"Moderate persistence ({years} years) - likely anthropogenic"
            else:
                interpretation = f"Short persistence ({years} years) - requires validation"
        
        return InstrumentSignal(
            instrument=InstrumentType.MULTITEMPORAL,
            detected=persistence_detected,
            confidence=confidence,
            values=values,
            source=mt_data.get('source', 'Landsat/Sentinel archive'),
            acquisition_date=mt_data.get('date_range'),
            interpretation=interpretation
        )
    
    def _calculate_multi_instrumental_score(
        self,
        signals: Dict[InstrumentType, InstrumentSignal]
    ) -> float:
        """
        Calcular score multi-instrumental ponderado
        
        Score = Σ (weight_i × confidence_i × detected_i)
        """
        
        if not signals:
            return 0.0
        
        total_score = 0.0
        total_weight = 0.0
        
        for instrument_type, signal in signals.items():
            weight = self.INSTRUMENT_WEIGHTS.get(instrument_type, 0.0)
            contribution = weight * signal.confidence * (1.0 if signal.detected else 0.0)
            
            total_score += contribution
            total_weight += weight
        
        # Normalizar por peso total disponible
        if total_weight > 0:
            return total_score / total_weight
        else:
            return 0.0
    
    def _determine_recommended_action(
        self,
        multi_score: float,
        convergence_ratio: float,
        signals: Dict[InstrumentType, InstrumentSignal]
    ) -> str:
        """
        Determinar acción recomendada basada en score y convergencia
        
        Returns:
            - field_validation: Alta prioridad para validación de campo
            - detailed_analysis: Requiere análisis más detallado
            - monitor: Monitorear cambios temporales
            - discard: Baja probabilidad, descartar
        """
        
        # FIELD VALIDATION: Score alto + convergencia alta
        if multi_score > 0.75 and convergence_ratio > 0.6:
            return "field_validation"
        
        # FIELD VALIDATION: Persistencia temporal confirmada
        if InstrumentType.MULTITEMPORAL in signals:
            mt_signal = signals[InstrumentType.MULTITEMPORAL]
            if mt_signal.detected and mt_signal.values.get('years_persistent', 0) >= 10:
                return "field_validation"
        
        # DETAILED ANALYSIS: Score moderado-alto
        if multi_score > 0.55:
            return "detailed_analysis"
        
        # MONITOR: Score moderado pero con alguna señal fuerte
        if multi_score > 0.35:
            strong_signals = [s for s in signals.values() if s.detected and s.confidence > 0.7]
            if strong_signals:
                return "monitor"
        
        # DISCARD: Score bajo
        return "discard"
    
    def generate_enriched_zones_geojson(
        self,
        zones: List[Dict[str, Any]],
        available_data_provider: Any = None
    ) -> Dict[str, Any]:
        """
        Generar GeoJSON enriquecido con señales multi-instrumentales
        
        Args:
            zones: Lista de zonas prioritarias
            available_data_provider: Proveedor de datos instrumentales
        
        Returns:
            GeoJSON FeatureCollection enriquecido
        """
        
        features = []
        
        for zone in zones:
            # Obtener datos disponibles para esta zona
            if available_data_provider:
                available_data = available_data_provider.get_data_for_zone(zone)
            else:
                # Simular datos para testing
                available_data = self._simulate_instrumental_data(zone)
            
            # Enriquecer candidata
            candidate = self.enrich_candidate(zone, available_data)
            
            # Crear feature GeoJSON
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [candidate.center_lon, candidate.center_lat]
                },
                'properties': {
                    'candidate_id': candidate.candidate_id,
                    'zone_id': candidate.zone_id,
                    'multi_instrumental_score': round(candidate.multi_instrumental_score, 3),
                    'convergence_count': candidate.convergence_count,
                    'convergence_ratio': round(candidate.convergence_ratio, 3),
                    'recommended_action': candidate.recommended_action,
                    'temporal_persistence': candidate.temporal_persistence,
                    'temporal_years': candidate.temporal_years,
                    'signals': {
                        inst.value: {
                            'detected': sig.detected,
                            'confidence': round(sig.confidence, 3),
                            'interpretation': sig.interpretation
                        }
                        for inst, sig in candidate.signals.items()
                    }
                }
            }
            
            features.append(feature)
        
        return {
            'type': 'FeatureCollection',
            'features': features,
            'metadata': {
                'total_candidates': len(features),
                'field_validation_priority': sum(1 for f in features 
                    if f['properties']['recommended_action'] == 'field_validation'),
                'instruments_used': list(set(
                    inst for f in features 
                    for inst in f['properties']['signals'].keys()
                ))
            }
        }
    
    def _simulate_instrumental_data(self, zone: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simular datos instrumentales para testing
        
        En producción, esto se reemplazaría con datos reales de APIs
        """
        
        # Simular basado en prioridad de la zona
        priority = zone.get('priority', 'low_priority')
        lidar_available = zone.get('lidar_available', False)
        
        # Score base según prioridad
        if priority == 'high_priority':
            base_confidence = 0.7
        elif priority == 'medium_priority':
            base_confidence = 0.5
        else:
            base_confidence = 0.3
        
        # Agregar ruido
        noise = np.random.uniform(-0.1, 0.1)
        confidence = np.clip(base_confidence + noise, 0.0, 1.0)
        
        simulated_data = {}
        
        # LiDAR (si disponible)
        if lidar_available:
            simulated_data['lidar'] = {
                'shape_detected': confidence > 0.5,
                'confidence': confidence,
                'shape_score': confidence * 0.9,
                'geometric_regularity': confidence * 0.8,
                'elevation_anomaly': np.random.uniform(0.5, 2.0),
                'source': 'Simulated ALS',
                'resolution_m': 0.5
            }
        
        # SAR (siempre disponible - Sentinel-1)
        simulated_data['sar'] = {
            'compaction_detected': confidence > 0.4,
            'confidence': confidence * 0.9,
            'backscatter_anomaly': np.random.uniform(1.0, 4.0) if confidence > 0.4 else 0.5,
            'texture_score': confidence * 0.7,
            'coherence': np.random.uniform(0.5, 0.9),
            'humidity_anomaly': np.random.uniform(-0.1, 0.1),
            'source': 'Sentinel-1',
            'resolution_m': 10.0
        }
        
        # Térmico (Landsat-8)
        simulated_data['thermal'] = {
            'thermal_anomaly_detected': confidence > 0.45,
            'confidence': confidence * 0.85,
            'lst_day_anomaly': np.random.uniform(-1.0, 0.5) if confidence > 0.45 else 0.0,
            'lst_night_anomaly': np.random.uniform(0.5, 2.0) if confidence > 0.45 else 0.0,
            'thermal_inertia': confidence * 0.8,
            'diurnal_range_anomaly': np.random.uniform(0.5, 1.5),
            'source': 'Landsat-8',
            'resolution_m': 100.0
        }
        
        # Multiespectral (Sentinel-2)
        simulated_data['multispectral'] = {
            'vegetation_anomaly_detected': confidence > 0.4,
            'confidence': confidence * 0.8,
            'ndvi_anomaly': np.random.uniform(-0.1, -0.02) if confidence > 0.4 else 0.0,
            'red_edge_anomaly': np.random.uniform(-0.05, 0.05),
            'ndwi_anomaly': np.random.uniform(-0.05, 0.0),
            'savi_anomaly': np.random.uniform(-0.08, 0.0),
            'source': 'Sentinel-2',
            'resolution_m': 10.0
        }
        
        # Multitemporal (archivo Landsat/Sentinel)
        years_persistent = int(confidence * 15) if confidence > 0.5 else 0
        simulated_data['multitemporal'] = {
            'persistence_detected': years_persistent >= 5,
            'confidence': confidence,
            'years_persistent': years_persistent,
            'seasonal_stability': confidence * 0.9,
            'change_resistance': confidence * 0.85,
            'temporal_consistency': confidence * 0.8,
            'source': 'Landsat/Sentinel archive',
            'date_range': f'2010-2025 ({years_persistent} years)'
        }
        
        return simulated_data


# Instancia global
multi_instrumental_enrichment = MultiInstrumentalEnrichment()
