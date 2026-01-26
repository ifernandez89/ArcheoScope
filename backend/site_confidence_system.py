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
    
    def identify_priority_zones(
        self,
        cultural_prior: np.ndarray,
        strategy: str = 'buffer'
    ) -> Dict[str, np.ndarray]:
        """
        Identificar zonas prioritarias para análisis de anomalías
        
        ESTRATEGIA CLAVE:
        - NO analizar el centro de hot zones (ya conocido)
        - SÍ analizar anillos, bordes, gradientes, transiciones
        - Ahí aparecen: fases previas, satélites, rutas, estructuras auxiliares
        
        Args:
            cultural_prior: Mapa de densidad cultural (0-1)
            strategy: Estrategia de priorización
                - 'buffer': Anillos alrededor de hot zones (RECOMENDADO)
                - 'gradient': Zonas de transición rápida
                - 'gaps': Huecos culturales (ya implementado)
        
        Returns:
            Dict con máscaras de prioridad:
            {
                'high_priority': array booleano,
                'medium_priority': array booleano,
                'low_priority': array booleano
            }
        """
        
        if strategy == 'buffer':
            # ESTRATEGIA BUFFER: Anillos alrededor de hot zones
            
            # Hot zone core (densidad > 0.7) → BAJA prioridad
            # Ya conocido, documentado
            core = cultural_prior > 0.7
            
            # Buffer 1 (0.3 < densidad < 0.7) → ALTA prioridad
            # Zona de transición, satélites, estructuras auxiliares
            buffer1 = (cultural_prior > 0.3) & (cultural_prior <= 0.7)
            
            # Buffer 2 (0.1 < densidad < 0.3) → MEDIA prioridad
            # Periferia, rutas, asentamientos menores
            buffer2 = (cultural_prior > 0.1) & (cultural_prior <= 0.3)
            
            # Fuera de hot zones (densidad < 0.1) → BAJA prioridad
            # Pero no descartamos completamente
            outside = cultural_prior <= 0.1
            
            return {
                'high_priority': buffer1,
                'medium_priority': buffer2,
                'low_priority': core | outside
            }
        
        elif strategy == 'gradient':
            # ESTRATEGIA GRADIENT: Zonas de cambio rápido
            from scipy import ndimage
            
            # Calcular gradiente (cambio espacial)
            gradient_y, gradient_x = np.gradient(cultural_prior)
            gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
            
            # Normalizar
            if gradient_magnitude.max() > 0:
                gradient_magnitude = gradient_magnitude / gradient_magnitude.max()
            
            # Alta prioridad: gradiente fuerte (transiciones)
            high_priority = gradient_magnitude > 0.3
            
            # Media prioridad: gradiente moderado
            medium_priority = (gradient_magnitude > 0.15) & (gradient_magnitude <= 0.3)
            
            # Baja prioridad: gradiente bajo (zonas homogéneas)
            low_priority = gradient_magnitude <= 0.15
            
            return {
                'high_priority': high_priority,
                'medium_priority': medium_priority,
                'low_priority': low_priority
            }
        
        elif strategy == 'gaps':
            # ESTRATEGIA GAPS: Huecos culturales improbables
            gaps = self.detect_cultural_gaps(cultural_prior, threshold=0.1)
            
            # Crear máscara de huecos
            gaps_mask = np.zeros_like(cultural_prior, dtype=bool)
            for i, j in gaps:
                gaps_mask[i, j] = True
            
            # Expandir huecos ligeramente (buffer de 3 pixels)
            from scipy import ndimage
            gaps_expanded = ndimage.binary_dilation(gaps_mask, iterations=3)
            
            return {
                'high_priority': gaps_expanded,
                'medium_priority': np.zeros_like(cultural_prior, dtype=bool),
                'low_priority': ~gaps_expanded
            }
        
        else:
            raise ValueError(f"Estrategia desconocida: {strategy}")
    
    def generate_recommended_zones(
        self,
        sites: List[Dict[str, Any]],
        bounds: Tuple[float, float, float, float],
        grid_size: int = 100,
        strategy: str = 'buffer',
        max_zones: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Generar zonas recomendadas para análisis de anomalías
        
        OPTIMIZACIÓN BAYESIANA:
        Maximiza: P(discovery | zone) / cost
        
        Args:
            sites: Lista de sitios arqueológicos
            bounds: (lat_min, lat_max, lon_min, lon_max)
            grid_size: Resolución del grid
            strategy: Estrategia de priorización
            max_zones: Máximo número de zonas a retornar
        
        Returns:
            Lista de zonas recomendadas con metadata completa
        """
        
        from scipy import ndimage
        
        lat_min, lat_max, lon_min, lon_max = bounds
        
        logger.info(f"🎯 Generando zonas recomendadas con estrategia '{strategy}'")
        
        # 1. Generar mapa de prior cultural
        cultural_prior = self.create_cultural_prior_map(
            sites, 
            grid_size=(grid_size, grid_size),
            bounds=bounds
        )
        
        # 2. Identificar zonas prioritarias
        priority_zones = self.identify_priority_zones(cultural_prior, strategy)
        
        # 3. Generar bounding boxes para cada zona
        zones = []
        
        for priority_level, zone_mask in priority_zones.items():
            if priority_level == 'low_priority':
                continue  # Saltar zonas de baja prioridad
            
            # Encontrar regiones conectadas
            labeled, num_features = ndimage.label(zone_mask)
            
            logger.info(f"   {priority_level}: {num_features} regiones detectadas")
            
            for zone_id in range(1, num_features + 1):
                zone_pixels = labeled == zone_id
                
                # Filtrar zonas muy pequeñas (< 10 pixels)
                if zone_pixels.sum() < 10:
                    continue
                
                # Calcular bbox
                rows, cols = np.where(zone_pixels)
                lat_min_idx, lat_max_idx = rows.min(), rows.max()
                lon_min_idx, lon_max_idx = cols.min(), cols.max()
                
                # Convertir índices a coordenadas
                zone_lat_min = lat_min + (lat_min_idx / grid_size) * (lat_max - lat_min)
                zone_lat_max = lat_min + ((lat_max_idx + 1) / grid_size) * (lat_max - lat_min)
                zone_lon_min = lon_min + (lon_min_idx / grid_size) * (lon_max - lon_min)
                zone_lon_max = lon_min + ((lon_max_idx + 1) / grid_size) * (lon_max - lon_min)
                
                # Calcular área (aproximada)
                area_km2 = self._calculate_area_km2(
                    zone_lat_min, zone_lat_max, zone_lon_min, zone_lon_max
                )
                
                # Calcular densidad cultural promedio en la zona
                zone_density = cultural_prior[zone_pixels].mean()
                
                # Generar zona
                zone = {
                    'zone_id': f'HZ_{len(zones):06d}',
                    'bbox': {
                        'lat_min': float(zone_lat_min),
                        'lat_max': float(zone_lat_max),
                        'lon_min': float(zone_lon_min),
                        'lon_max': float(zone_lon_max)
                    },
                    'center': {
                        'lat': float((zone_lat_min + zone_lat_max) / 2),
                        'lon': float((zone_lon_min + zone_lon_max) / 2)
                    },
                    'priority': priority_level,
                    'area_km2': float(area_km2),
                    'cultural_density': float(zone_density),
                    'pixels': int(zone_pixels.sum()),
                    'reason': self._generate_zone_reasoning(priority_level, strategy, zone_density),
                    'recommended_instruments': self._recommend_instruments_for_zone(
                        zone_lat_min, zone_lon_min
                    ),
                    'estimated_analysis_time_minutes': self._estimate_analysis_time(area_km2)
                }
                
                zones.append(zone)
        
        # 4. Ordenar por prioridad y score
        priority_order = {'high_priority': 0, 'medium_priority': 1, 'low_priority': 2}
        zones.sort(key=lambda z: (
            priority_order[z['priority']],
            -z['cultural_density']  # Mayor densidad primero dentro de cada prioridad
        ))
        
        logger.info(f"✅ {len(zones)} zonas generadas, retornando top {max_zones}")
        
        return zones[:max_zones]
    
    def _calculate_area_km2(self, lat_min: float, lat_max: float, 
                           lon_min: float, lon_max: float) -> float:
        """Calcular área aproximada en km²"""
        import math
        
        # Aproximación usando fórmula de Haversine
        lat_diff = lat_max - lat_min
        lon_diff = lon_max - lon_min
        
        # Conversión aproximada a km
        lat_km = lat_diff * 111.32  # 1° latitud ≈ 111.32 km
        lon_km = lon_diff * 111.32 * abs(math.cos(math.radians((lat_min + lat_max) / 2)))
        
        return lat_km * lon_km
    
    def _generate_zone_reasoning(self, priority_level: str, strategy: str, 
                                 density: float) -> List[str]:
        """Generar razones para la priorización de una zona"""
        
        reasons = []
        
        if strategy == 'buffer':
            if priority_level == 'high_priority':
                reasons.append("Zona de transición alrededor de hot zone")
                reasons.append("Alta probabilidad de estructuras auxiliares")
                reasons.append("Posibles satélites de asentamientos conocidos")
                if density > 0.5:
                    reasons.append("Densidad cultural significativa")
            elif priority_level == 'medium_priority':
                reasons.append("Periferia de zona cultural")
                reasons.append("Posibles rutas o asentamientos menores")
                reasons.append("Área de expansión histórica probable")
        
        elif strategy == 'gradient':
            if priority_level == 'high_priority':
                reasons.append("Zona de cambio rápido en densidad cultural")
                reasons.append("Transición entre áreas conocidas y desconocidas")
                reasons.append("Posible límite de asentamiento o frontera")
        
        elif strategy == 'gaps':
            if priority_level == 'high_priority':
                reasons.append("Hueco cultural improbable")
                reasons.append("Baja densidad rodeada de alta densidad")
                reasons.append("Candidato prioritario para exploración")
        
        # Razones generales
        if density < 0.2:
            reasons.append("Baja documentación actual")
        
        return reasons
    
    def _recommend_instruments_for_zone(self, lat: float, lon: float) -> List[str]:
        """Recomendar instrumentos basado en ubicación aproximada"""
        
        # Clasificación simple por latitud (aproximación)
        abs_lat = abs(lat)
        
        instruments = []
        
        if abs_lat < 30:  # Tropical/subtropical
            instruments = ['LiDAR', 'L-band SAR', 'Multispectral', 'Thermal']
        elif abs_lat < 60:  # Templado
            instruments = ['Multispectral', 'SAR', 'Thermal', 'LiDAR']
        else:  # Polar
            instruments = ['SAR', 'ICESat-2', 'Thermal']
        
        return instruments
    
    def _estimate_analysis_time(self, area_km2: float) -> int:
        """Estimar tiempo de análisis en minutos"""
        
        # Aproximación: 1 km² = 2 minutos de análisis
        base_time = area_km2 * 2
        
        # Mínimo 5 minutos, máximo 120 minutos
        return int(max(5, min(120, base_time)))
    
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
