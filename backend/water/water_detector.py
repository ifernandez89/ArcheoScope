#!/usr/bin/env python3
"""
ArcheoScope Water Detection Module
Detecta automáticamente si las coordenadas están sobre agua y determina el tipo de cuerpo de agua
"""

import numpy as np
import requests
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class WaterBodyType(Enum):
    """Tipos de cuerpos de agua"""
    OCEAN = "ocean"
    SEA = "sea"
    LAKE = "lake"
    RIVER = "river"
    COASTAL = "coastal"
    DEEP_OCEAN = "deep_ocean"
    SHALLOW_WATER = "shallow_water"
    UNKNOWN_WATER = "unknown_water"

@dataclass
class WaterContext:
    """Contexto del cuerpo de agua detectado"""
    is_water: bool
    water_type: Optional[WaterBodyType]
    estimated_depth_m: Optional[float]
    salinity_type: str  # "saltwater", "freshwater", "brackish"
    coordinates: Tuple[float, float]
    confidence: float
    
    # Metadatos para arqueología submarina
    archaeological_potential: str  # "high", "medium", "low"
    historical_shipping_routes: bool
    known_wrecks_nearby: bool
    sediment_type: Optional[str]
    current_strength: Optional[str]  # "low", "medium", "high"

class WaterDetector:
    """
    Detector de agua y clasificador de contexto acuático
    
    Utiliza múltiples fuentes para determinar si las coordenadas están sobre agua
    y caracterizar el ambiente submarino para arqueología
    """
    
    def __init__(self):
        self.ocean_boundaries = self._load_ocean_boundaries()
        self.major_rivers = self._load_major_rivers()
        self.known_wreck_sites = self._load_known_wreck_sites()
        
        logger.info("WaterDetector inicializado con bases de datos geográficas")
    
    def detect_water_context(self, lat: float, lon: float) -> WaterContext:
        """
        Detectar si las coordenadas están sobre agua y caracterizar el contexto
        
        Args:
            lat: Latitud
            lon: Longitud
            
        Returns:
            WaterContext con información completa del cuerpo de agua
        """
        try:
            logger.info(f"Detectando contexto de agua para coordenadas: {lat:.4f}, {lon:.4f}")
            
            # 1. Verificación básica de océanos
            ocean_check = self._check_ocean_boundaries(lat, lon)
            
            # 2. Verificación de mares y lagos grandes
            water_body_check = self._check_water_bodies(lat, lon)
            
            # 3. Verificación de ríos principales
            river_check = self._check_major_rivers(lat, lon)
            
            # 4. Estimación de profundidad
            estimated_depth = self._estimate_depth(lat, lon)
            
            # 5. Determinar tipo de agua
            water_type, salinity = self._determine_water_type(lat, lon, ocean_check, water_body_check, river_check)
            
            # 6. Evaluar potencial arqueológico
            archaeological_potential = self._assess_archaeological_potential(lat, lon, water_type, estimated_depth)
            
            # 7. Verificar rutas históricas de navegación
            shipping_routes = self._check_historical_shipping_routes(lat, lon)
            
            # 8. Verificar naufragios conocidos cercanos
            known_wrecks = self._check_known_wrecks_nearby(lat, lon)
            
            # 9. Caracterizar sedimentos y corrientes
            sediment_type = self._estimate_sediment_type(lat, lon, water_type)
            current_strength = self._estimate_current_strength(lat, lon, water_type)
            
            is_water = any([ocean_check, water_body_check, river_check])
            confidence = self._calculate_confidence(ocean_check, water_body_check, river_check, estimated_depth)
            
            context = WaterContext(
                is_water=is_water,
                water_type=water_type,
                estimated_depth_m=estimated_depth,
                salinity_type=salinity,
                coordinates=(lat, lon),
                confidence=confidence,
                archaeological_potential=archaeological_potential,
                historical_shipping_routes=shipping_routes,
                known_wrecks_nearby=known_wrecks,
                sediment_type=sediment_type,
                current_strength=current_strength
            )
            
            if is_water:
                logger.info(f"✅ Agua detectada: {water_type.value if water_type else 'unknown'}, profundidad: {estimated_depth}m")
                logger.info(f"   Potencial arqueológico: {archaeological_potential}")
            else:
                logger.info("🏔️ Coordenadas sobre tierra firme")
            
            return context
            
        except Exception as e:
            logger.error(f"Error detectando contexto de agua: {e}")
            return WaterContext(
                is_water=False,
                water_type=None,
                estimated_depth_m=None,
                salinity_type="unknown",
                coordinates=(lat, lon),
                confidence=0.0,
                archaeological_potential="unknown",
                historical_shipping_routes=False,
                known_wrecks_nearby=False,
                sediment_type=None,
                current_strength=None
            )
    
    def _check_ocean_boundaries(self, lat: float, lon: float) -> bool:
        """Verificar si está en océano usando límites geográficos"""
        
        # Océano Atlántico
        if -80 <= lon <= 20 and -60 <= lat <= 70:
            # Excluir masas de tierra principales
            if not self._is_land_mass(lat, lon):
                return True
        
        # Océano Pacífico
        if (lon >= 120 or lon <= -60) and -60 <= lat <= 70:
            if not self._is_land_mass(lat, lon):
                return True
        
        # Océano Índico
        if 20 <= lon <= 120 and -60 <= lat <= 30:
            if not self._is_land_mass(lat, lon):
                return True
        
        # Océano Ártico
        if lat >= 66.5:
            if not self._is_land_mass(lat, lon):
                return True
        
        # Océano Antártico
        if lat <= -60:
            return True
        
        return False
    
    def _check_water_bodies(self, lat: float, lon: float) -> bool:
        """Verificar mares, lagos grandes y cuerpos de agua específicos"""
        
        # Mar Mediterráneo
        if 30 <= lat <= 46 and -6 <= lon <= 36:
            return True
        
        # Mar Negro
        if 40.5 <= lat <= 47 and 27 <= lon <= 42:
            return True
        
        # Mar Caspio
        if 36 <= lat <= 47 and 46 <= lon <= 55:
            return True
        
        # Grandes Lagos (América del Norte)
        if 41 <= lat <= 49 and -93 <= lon <= -76:
            return True
        
        # Mar Báltico
        if 53 <= lat <= 66 and 9 <= lon <= 31:
            return True
        
        # Golfo de México
        if 18 <= lat <= 31 and -98 <= lon <= -80:
            return True
        
        # Mar Rojo
        if 12 <= lat <= 30 and 32 <= lon <= 43:
            return True
        
        return False
    
    def _check_major_rivers(self, lat: float, lon: float) -> bool:
        """Verificar ríos principales (simplificado)"""
        
        # Río Amazonas
        if -5 <= lat <= 2 and -70 <= lon <= -48:
            return True
        
        # Río Nilo
        if 4 <= lat <= 31 and 24 <= lon <= 35:
            return True
        
        # Río Mississippi
        if 29 <= lat <= 48 and -95 <= lon <= -89:
            return True
        
        # Río Yangtsé
        if 25 <= lat <= 35 and 90 <= lon <= 122:
            return True
        
        return False
    
    def _is_land_mass(self, lat: float, lon: float) -> bool:
        """Verificar si está sobre una masa de tierra principal (simplificado)"""
        
        # América del Norte
        if 25 <= lat <= 70 and -170 <= lon <= -50:
            return True
        
        # América del Sur
        if -55 <= lat <= 15 and -82 <= lon <= -35:
            return True
        
        # Europa
        if 35 <= lat <= 72 and -10 <= lon <= 40:
            return True
        
        # África
        if -35 <= lat <= 37 and -18 <= lon <= 52:
            return True
        
        # Asia
        if 5 <= lat <= 75 and 25 <= lon <= 180:
            return True
        
        # Australia
        if -45 <= lat <= -10 and 110 <= lon <= 155:
            return True
        
        return False
    
    def _estimate_depth(self, lat: float, lon: float) -> Optional[float]:
        """Estimar profundidad del agua (simulado - en implementación real usaría batimetría)"""
        
        if not self._check_ocean_boundaries(lat, lon) and not self._check_water_bodies(lat, lon):
            if self._check_major_rivers(lat, lon):
                return np.random.uniform(2, 50)  # Ríos: 2-50m
            return None
        
        # Océano profundo
        if abs(lat) < 60:  # Latitudes tropicales/templadas
            return np.random.uniform(1000, 6000)  # 1-6km profundidad
        else:  # Latitudes polares
            return np.random.uniform(500, 3000)   # 0.5-3km profundidad
    
    def _determine_water_type(self, lat: float, lon: float, ocean: bool, water_body: bool, river: bool) -> Tuple[Optional[WaterBodyType], str]:
        """Determinar tipo de cuerpo de agua y salinidad"""
        
        if river:
            return WaterBodyType.RIVER, "freshwater"
        
        if ocean:
            depth = self._estimate_depth(lat, lon)
            if depth and depth > 200:
                return WaterBodyType.DEEP_OCEAN, "saltwater"
            else:
                return WaterBodyType.COASTAL, "saltwater"
        
        if water_body:
            # Determinar tipo específico basado en ubicación
            if 30 <= lat <= 46 and -6 <= lon <= 36:  # Mediterráneo
                return WaterBodyType.SEA, "saltwater"
            elif 36 <= lat <= 47 and 46 <= lon <= 55:  # Caspio
                return WaterBodyType.LAKE, "brackish"
            elif 41 <= lat <= 49 and -93 <= lon <= -76:  # Grandes Lagos
                return WaterBodyType.LAKE, "freshwater"
            else:
                return WaterBodyType.SEA, "saltwater"
        
        return None, "unknown"
    
    def _assess_archaeological_potential(self, lat: float, lon: float, water_type: Optional[WaterBodyType], depth: Optional[float]) -> str:
        """Evaluar potencial arqueológico submarino"""
        
        if not water_type:
            return "none"
        
        # Ríos: alto potencial para asentamientos ribereños
        if water_type == WaterBodyType.RIVER:
            return "high"
        
        # Aguas costeras: alto potencial para naufragios
        if water_type == WaterBodyType.COASTAL:
            return "high"
        
        # Mares cerrados: alto potencial histórico
        if water_type == WaterBodyType.SEA:
            return "high"
        
        # Lagos: potencial medio
        if water_type == WaterBodyType.LAKE:
            return "medium"
        
        # Océano profundo: evaluar rutas históricas y naufragios conocidos
        if water_type == WaterBodyType.DEEP_OCEAN:
            # Verificar si está en rutas históricas importantes
            if self._check_historical_shipping_routes(lat, lon):
                return "high"  # Rutas históricas = alto potencial
            elif depth and depth < 6000:  # Accesible para ROVs modernos
                return "medium"
            else:
                return "low"
        
        return "low"
    
    def _check_historical_shipping_routes(self, lat: float, lon: float) -> bool:
        """Verificar si está en rutas históricas de navegación"""
        
        # Atlántico Norte (ruta del Titanic)
        if 40 <= lat <= 55 and -50 <= lon <= -10:
            return True
        
        # Mediterráneo (rutas comerciales antiguas)
        if 30 <= lat <= 46 and -6 <= lon <= 36:
            return True
        
        # Ruta del Cabo (África)
        if -40 <= lat <= -30 and 15 <= lon <= 25:
            return True
        
        # Estrecho de Malaca
        if 1 <= lat <= 6 and 100 <= lon <= 105:
            return True
        
        return False
    
    def _check_known_wrecks_nearby(self, lat: float, lon: float, radius_km: float = 50) -> bool:
        """Verificar naufragios conocidos en el área (simulado)"""
        
        # Titanic
        if 41.5 <= lat <= 42 and -50 <= lon <= -49:
            return True
        
        # Lusitania
        if 51 <= lat <= 52 and -9 <= lon <= -8:
            return True
        
        # Área del Mediterráneo (muchos naufragios antiguos)
        if 35 <= lat <= 42 and 10 <= lon <= 25:
            return True
        
        return False
    
    def _estimate_sediment_type(self, lat: float, lon: float, water_type: Optional[WaterBodyType]) -> Optional[str]:
        """Estimar tipo de sedimento del fondo"""
        
        if not water_type:
            return None
        
        if water_type == WaterBodyType.RIVER:
            return "silt_clay"
        elif water_type == WaterBodyType.COASTAL:
            return "sand_gravel"
        elif water_type == WaterBodyType.DEEP_OCEAN:
            return "deep_sea_clay"
        elif water_type == WaterBodyType.SEA:
            return "mixed_sediment"
        else:
            return "unknown_sediment"
    
    def _estimate_current_strength(self, lat: float, lon: float, water_type: Optional[WaterBodyType]) -> Optional[str]:
        """Estimar fuerza de corrientes"""
        
        if not water_type:
            return None
        
        # Corrientes oceánicas fuertes
        if water_type == WaterBodyType.DEEP_OCEAN:
            if 30 <= abs(lat) <= 60:  # Latitudes medias
                return "high"
            else:
                return "medium"
        
        # Aguas costeras: variable
        elif water_type == WaterBodyType.COASTAL:
            return "medium"
        
        # Ríos: depende del tamaño
        elif water_type == WaterBodyType.RIVER:
            return "medium"
        
        # Mares cerrados: generalmente bajas
        elif water_type == WaterBodyType.SEA:
            return "low"
        
        else:
            return "low"
    
    def _calculate_confidence(self, ocean: bool, water_body: bool, river: bool, depth: Optional[float]) -> float:
        """Calcular confianza en la detección"""
        
        confidence = 0.0
        
        if ocean:
            confidence += 0.8
        if water_body:
            confidence += 0.7
        if river:
            confidence += 0.6
        if depth:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _load_ocean_boundaries(self) -> Dict[str, Any]:
        """Cargar límites de océanos (simulado)"""
        return {"loaded": True}
    
    def _load_major_rivers(self) -> Dict[str, Any]:
        """Cargar base de datos de ríos principales (simulado)"""
        return {"loaded": True}
    
    def _load_known_wreck_sites(self) -> Dict[str, Any]:
        """Cargar base de datos de naufragios conocidos (simulado)"""
        return {"loaded": True}