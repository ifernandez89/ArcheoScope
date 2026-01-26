#!/usr/bin/env python3
"""
ArcheoScope - Site Confidence System
Sistema de pesos probabilísticos para sitios arqueológicos

NO tratamos sitios como verdad absoluta
SÍ los usamos como evidencia probabilística
"""

import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SiteSource(Enum):
    """Fuentes de datos de sitios"""
    EXCAVATED = "excavated"           # Excavado académicamente
    UNESCO = "unesco"                 # UNESCO World Heritage
    NATIONAL_REGISTRY = "national"    # Registro nacional oficial
    WIKIDATA = "wikidata"            # Wikidata
    OSM = "osm"                      # OpenStreetMap
    UNKNOWN = "unknown"              # Fuente desconocida


@dataclass
class SiteConfidence:
    """Confianza de un sitio arqueológico"""
    
    site_id: str
    name: str
    source: SiteSource
    
    # Confianza base por fuente (0.0 - 1.0)
    base_confidence: float
    
    # Factores que modifican confianza
    has_excavation: bool = False
    has_academic_publication: bool = False
    has_precise_coordinates: bool = False
    has_known_period: bool = False
    has_multiple_sources: bool = False
    
    # Precisión geométrica (metros)
    geometry_accuracy_m: float = 1000.0
    
    # Período conocido
    period: Optional[str] = None
    
    # Confianza final calculada
    final_confidence: float = 0.0
    
    def calculate_final_confidence(self) -> float:
        """
        Calcular confianza final basada en factores
        
        Base + bonificaciones - penalizaciones
        """
        
        confidence = self.base_confidence
        
        # BONIFICACIONES
        if self.has_excavation:
            confidence += 0.15
        
        if self.has_academic_publication:
            confidence += 0.10
        
        if self.has_precise_coordinates:
            confidence += 0.05
        
        if self.has_known_period:
            confidence += 0.05
        
        if self.has_multiple_sources:
            confidence += 0.10
        
        # PENALIZACIONES
        # Geometría imprecisa
        if self.geometry_accuracy_m > 500:
            confidence -= 0.10
        elif self.geometry_accuracy_m > 100:
            confidence -= 0.05
        
        # Limitar a rango válido
        self.final_confidence = np.clip(confidence, 0.0, 1.0)
        
        return self.final_confidence


class SiteConfidenceSystem:
    """
    Sistema de confianza para sitios arqueológicos
    
    Convierte sitios conocidos en:
    - Prior cultural
    - Mapa de probabilidad humana
    - Superficie de densidad
    
    NO los usa como verdad absoluta
    """
    
    # Pesos base por fuente
    SOURCE_WEIGHTS = {
        SiteSource.EXCAVATED: 0.95,
        SiteSource.UNESCO: 0.95,
        SiteSource.NATIONAL_REGISTRY: 0.80,
        SiteSource.WIKIDATA: 0.60,
        SiteSource.OSM: 0.40,
        SiteSource.UNKNOWN: 0.20
    }
    
    def __init__(self):
        self.sites_cache: Dict[str, SiteConfidence] = {}
        logger.info("SiteConfidenceSystem inicializado")
    
    def get_base_confidence(self, source: str) -> float:
        """Obtener confianza base por fuente"""
        
        # Mapear string a enum
        source_map = {
            'excavated': SiteSource.EXCAVATED,
            'unesco': SiteSource.UNESCO,
            'national': SiteSource.NATIONAL_REGISTRY,
            'wikidata': SiteSource.WIKIDATA,
            'osm': SiteSource.OSM,
            'openstreetmap': SiteSource.OSM
        }
        
        source_enum = source_map.get(source.lower(), SiteSource.UNKNOWN)
        return self.SOURCE_WEIGHTS.get(source_enum, 0.20)
    
    def calculate_site_confidence(
        self,
        site_data: Dict[str, Any]
    ) -> SiteConfidence:
        """
        Calcular confianza de un sitio desde datos
        
        Args:
            site_data: Diccionario con datos del sitio
        
        Returns:
            SiteConfidence con confianza calculada
        """
        
        # Extraer fuente
        source_str = site_data.get('source', 'unknown')
        source_enum = SiteSource.UNKNOWN
        
        for src in SiteSource:
            if src.value in source_str.lower():
                source_enum = src
                break
        
        # Crear objeto de confianza
        confidence = SiteConfidence(
            site_id=site_data.get('id', 'unknown'),
            name=site_data.get('name', 'Unknown Site'),
            source=source_enum,
            base_confidence=self.get_base_confidence(source_str),
            has_excavation=site_data.get('excavated', False),
            has_academic_publication=bool(site_data.get('references')),
            has_precise_coordinates=site_data.get('geometry_accuracy_m', 1000) < 100,
            has_known_period=bool(site_data.get('period')),
            has_multiple_sources=site_data.get('source_count', 1) > 1,
            geometry_accuracy_m=site_data.get('geometry_accuracy_m', 1000.0),
            period=site_data.get('period')
        )
        
        # Calcular confianza final
        confidence.calculate_final_confidence()
        
        # Cachear
        self.sites_cache[confidence.site_id] = confidence
        
        return confidence
    
    def adjust_anomaly_score(
        self,
        anomaly_score: float,
        nearby_sites: List[Dict[str, Any]],
        distance_km: float
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Ajustar score de anomalía basado en sitios cercanos
        
        NO descarta automáticamente
        SÍ ajusta score probabilísticamente
        
        Args:
            anomaly_score: Score inicial de anomalía (0-1)
            nearby_sites: Lista de sitios cercanos
            distance_km: Distancia al sitio más cercano
        
        Returns:
            (adjusted_score, adjustment_details)
        """
        
        if not nearby_sites:
            return anomaly_score, {
                'adjustment': 0.0,
                'reason': 'no_nearby_sites',
                'nearby_count': 0
            }
        
        # Calcular ajuste basado en sitios cercanos
        total_adjustment = 0.0
        site_details = []
        
        for site in nearby_sites:
            # Calcular confianza del sitio
            site_conf = self.calculate_site_confidence(site)
            
            # Distancia al sitio
            site_distance = site.get('distance_km', distance_km)
            
            # Factor de distancia (decae con distancia)
            # Buffer pequeño: 0-1km = factor 1.0, >5km = factor 0.0
            distance_factor = max(0.0, 1.0 - (site_distance / 5.0))
            
            # Ajuste = confianza * factor_distancia * peso
            site_adjustment = site_conf.final_confidence * distance_factor * 0.2
            
            total_adjustment += site_adjustment
            
            site_details.append({
                'name': site_conf.name,
                'source': site_conf.source.value,
                'confidence': site_conf.final_confidence,
                'distance_km': site_distance,
                'adjustment': site_adjustment
            })
        
        # Limitar ajuste máximo a -0.3 (nunca descarta completamente)
        total_adjustment = min(total_adjustment, 0.3)
        
        # Aplicar ajuste
        adjusted_score = max(0.0, anomaly_score - total_adjustment)
        
        return adjusted_score, {
            'adjustment': -total_adjustment,
            'reason': 'nearby_known_sites',
            'nearby_count': len(nearby_sites),
            'sites': site_details,
            'original_score': anomaly_score,
            'adjusted_score': adjusted_score
        }
    
    def create_cultural_prior_map(
        self,
        sites: List[Dict[str, Any]],
        grid_size: Tuple[int, int] = (100, 100),
        bounds: Tuple[float, float, float, float] = None
    ) -> np.ndarray:
        """
        Crear mapa de prior cultural (kernel density)
        
        Convierte sitios discretos en superficie continua de probabilidad
        
        Args:
            sites: Lista de sitios con coordenadas
            grid_size: Tamaño de grid (filas, columnas)
            bounds: (lat_min, lat_max, lon_min, lon_max)
        
        Returns:
            Array 2D con densidad cultural (0-1)
        """
        
        if not sites or bounds is None:
            return np.zeros(grid_size)
        
        lat_min, lat_max, lon_min, lon_max = bounds
        
        # Crear grid
        lats = np.linspace(lat_min, lat_max, grid_size[0])
        lons = np.linspace(lon_min, lon_max, grid_size[1])
        
        # Mapa de densidad
        density_map = np.zeros(grid_size)
        
        # Para cada sitio, agregar kernel gaussiano
        for site in sites:
            lat = site.get('latitude')
            lon = site.get('longitude')
            
            if lat is None or lon is None:
                continue
            
            # Calcular confianza del sitio
            site_conf = self.calculate_site_confidence(site)
            
            # Encontrar posición en grid
            lat_idx = int((lat - lat_min) / (lat_max - lat_min) * (grid_size[0] - 1))
            lon_idx = int((lon - lon_min) / (lon_max - lon_min) * (grid_size[1] - 1))
            
            if 0 <= lat_idx < grid_size[0] and 0 <= lon_idx < grid_size[1]:
                # Kernel gaussiano (sigma = 5 pixels)
                sigma = 5
                for i in range(max(0, lat_idx - 3*sigma), min(grid_size[0], lat_idx + 3*sigma)):
                    for j in range(max(0, lon_idx - 3*sigma), min(grid_size[1], lon_idx + 3*sigma)):
                        dist_sq = (i - lat_idx)**2 + (j - lon_idx)**2
                        kernel_val = np.exp(-dist_sq / (2 * sigma**2))
                        density_map[i, j] += kernel_val * site_conf.final_confidence
        
        # Normalizar a rango 0-1
        if density_map.max() > 0:
            density_map = density_map / density_map.max()
        
        return density_map
    
    def detect_cultural_gaps(
        self,
        cultural_prior: np.ndarray,
        threshold: float = 0.1
    ) -> List[Tuple[int, int]]:
        """
        Detectar huecos improbables en mapa cultural
        
        Áreas con baja densidad cultural rodeadas de alta densidad
        = potencialmente interesante
        
        Args:
            cultural_prior: Mapa de densidad cultural
            threshold: Umbral para considerar "hueco"
        
        Returns:
            Lista de coordenadas (i, j) de huecos
        """
        
        from scipy import ndimage
        
        # Suavizar mapa
        smoothed = ndimage.gaussian_filter(cultural_prior, sigma=2)
        
        # Detectar huecos: baja densidad local pero alta densidad en vecindad
        local_low = smoothed < threshold
        
        # Densidad en vecindad (radio 10 pixels)
        neighborhood = ndimage.uniform_filter(smoothed, size=10)
        neighborhood_high = neighborhood > 0.5
        
        # Huecos = local bajo + vecindad alta
        gaps = local_low & neighborhood_high
        
        # Extraer coordenadas
        gap_coords = np.argwhere(gaps)
        
        return [(int(i), int(j)) for i, j in gap_coords]
    
    def get_site_signature(
        self,
        site_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Obtener firma esperada de un sitio conocido
        
        Los sitios conocidos también generan anomalías:
        - Compactación
        - Humedad residual
        - Vegetación distintiva
        
        Esto sirve como validación del modelo
        
        Args:
            site_data: Datos del sitio
        
        Returns:
            Firma esperada (NDVI, LST, SAR, etc.)
        """
        
        # Firma típica de sitio arqueológico
        # (valores aproximados, deberían calibrarse con datos reales)
        
        signature = {
            'ndvi_anomaly': -0.05,      # Vegetación ligeramente reducida
            'lst_anomaly': +1.5,         # Temperatura ligeramente elevada
            'sar_anomaly': +2.0,         # Backscatter aumentado (compactación)
            'ndwi_anomaly': -0.02,       # Humedad ligeramente reducida
            'roughness_anomaly': -5.0    # Superficie más lisa
        }
        
        # Ajustar por tipo de sitio
        site_type = site_data.get('site_type', 'unknown')
        
        if 'urban' in site_type.lower():
            signature['sar_anomaly'] = +4.0  # Más compactación
            signature['roughness_anomaly'] = -10.0
        
        elif 'burial' in site_type.lower():
            signature['ndvi_anomaly'] = -0.10  # Más vegetación afectada
            signature['lst_anomaly'] = +0.5
        
        return signature


# Instancia global
site_confidence_system = SiteConfidenceSystem()
