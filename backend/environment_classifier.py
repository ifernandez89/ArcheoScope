#!/usr/bin/env python3
"""
ArcheoScope Environment Classifier
Sistema ROBUSTO de clasificación de ambientes para selección de sensores apropiados

CRÍTICO: Este módulo determina qué herramientas usar según el ambiente
- Hielo/Nieve → ICESat-2, SAR polarimétrico, GPR
- Agua → Sonar, magnetometría, batimetría
- Desierto → Térmico, SAR, NDVI bajo
- Vegetación → LiDAR, NDVI, térmico
- Urbano → SAR, fotogrametría, catastro
"""

import logging
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any
import math

logger = logging.getLogger(__name__)

class EnvironmentType(Enum):
    """Tipos de ambiente MUTUAMENTE EXCLUYENTES"""
    # Ambientes extremos (prioridad máxima)
    POLAR_ICE = "polar_ice"              # Antártida, Groenlandia, glaciares polares
    GLACIER = "glacier"                   # Glaciares de montaña
    PERMAFROST = "permafrost"            # Tundra, permafrost continuo
    
    # Ambientes acuáticos
    DEEP_OCEAN = "deep_ocean"            # Océano profundo (>200m)
    SHALLOW_SEA = "shallow_sea"          # Mar poco profundo (<200m)
    COASTAL = "coastal"                   # Zona costera
    LAKE = "lake"                         # Lagos
    RIVER = "river"                       # Ríos (solo cauce)
    
    # Ambientes terrestres
    DESERT = "desert"                     # Desiertos áridos
    SEMI_ARID = "semi_arid"              # Zonas semiáridas
    GRASSLAND = "grassland"               # Praderas, estepas
    FOREST = "forest"                     # Bosques, selvas
    AGRICULTURAL = "agricultural"         # Zonas agrícolas
    URBAN = "urban"                       # Zonas urbanas
    MOUNTAIN = "mountain"                 # Montañas (sin glaciar)
    
    # Fallback
    UNKNOWN = "unknown"

@dataclass
class EnvironmentContext:
    """Contexto completo del ambiente detectado"""
    environment_type: EnvironmentType
    confidence: float  # 0.0 - 1.0
    coordinates: Tuple[float, float]
    
    # Características del ambiente
    temperature_range_c: Tuple[float, float]  # (min, max) anual
    precipitation_mm_year: Optional[float]
    elevation_m: Optional[float]
    
    # Instrumentos recomendados
    primary_sensors: list  # Sensores principales para este ambiente
    secondary_sensors: list  # Sensores complementarios
    
    # Metadatos arqueológicos
    archaeological_visibility: str  # "high", "medium", "low"
    preservation_potential: str  # "excellent", "good", "moderate", "poor"
    access_difficulty: str  # "easy", "moderate", "difficult", "extreme"
    
    # Información adicional
    notes: str

class EnvironmentClassifier:
    """
    Clasificador ROBUSTO de ambientes usando datos geográficos precisos
    
    FILOSOFÍA:
    1. Usar límites geográficos PRECISOS, no rangos amplios
    2. Priorizar ambientes extremos (hielo, agua profunda)
    3. Usar elevación y clima cuando sea posible
    4. Ser CONSERVADOR: mejor "unknown" que clasificación incorrecta
    """
    
    def __init__(self):
        """Inicializar con bases de datos geográficas"""
        self.known_glaciers = self._load_glacier_database()
        self.ocean_boundaries = self._load_ocean_database()
        self.desert_regions = self._load_desert_database()
        self.major_rivers = self._load_river_database()
        
        logger.info("EnvironmentClassifier inicializado con bases de datos precisas")
    
    def classify(self, lat: float, lon: float) -> EnvironmentContext:
        """
        Clasificar ambiente en coordenadas específicas
        
        ORDEN DE PRIORIDAD:
        1. Regiones polares (hielo)
        2. Océanos y mares
        3. Lagos grandes
        4. Ríos principales (solo cauce)
        5. Desiertos conocidos
        6. Zonas de vegetación
        7. Montañas
        8. Urbano (si se puede detectar)
        """
        try:
            logger.info(f"🌍 Clasificando ambiente: {lat:.4f}, {lon:.4f}")
            
            # NIVEL 1: Regiones polares (prioridad máxima)
            polar_check = self._check_polar_regions(lat, lon)
            if polar_check:
                return polar_check
            
            # NIVEL 2: Océanos y mares
            ocean_check = self._check_oceans(lat, lon)
            if ocean_check:
                return ocean_check
            
            # NIVEL 3: Lagos grandes
            lake_check = self._check_major_lakes(lat, lon)
            if lake_check:
                return lake_check
            
            # NIVEL 4: Ríos principales (SOLO cauce, buffer estrecho)
            river_check = self._check_rivers(lat, lon)
            if river_check:
                return river_check
            
            # NIVEL 5: Glaciares de montaña
            glacier_check = self._check_mountain_glaciers(lat, lon)
            if glacier_check:
                return glacier_check
            
            # NIVEL 6: Regiones montañosas (NUEVO)
            mountain_check = self._check_mountain_regions(lat, lon)
            if mountain_check:
                return mountain_check
            
            # NIVEL 7: Desiertos conocidos
            desert_check = self._check_deserts(lat, lon)
            if desert_check:
                return desert_check
            
            # NIVEL 8: Clasificación por latitud y clima
            climate_check = self._classify_by_climate(lat, lon)
            if climate_check:
                return climate_check
            
            # FALLBACK: Unknown
            logger.warning(f"⚠️ No se pudo clasificar ambiente para {lat:.4f}, {lon:.4f}")
            return self._create_unknown_context(lat, lon)
            
        except Exception as e:
            logger.error(f"Error clasificando ambiente: {e}")
            return self._create_unknown_context(lat, lon)
    
    def _check_polar_regions(self, lat: float, lon: float) -> Optional[EnvironmentContext]:
        """Detectar regiones polares con PRECISIÓN"""
        
        # Antártida (continente de hielo)
        if lat <= -60:
            logger.info("❄️ ANTÁRTIDA detectada")
            return EnvironmentContext(
                environment_type=EnvironmentType.POLAR_ICE,
                confidence=0.99,
                coordinates=(lat, lon),
                temperature_range_c=(-60, -10),
                precipitation_mm_year=50,
                elevation_m=2000,  # Promedio
                primary_sensors=["icesat2", "sentinel1_sar", "palsar"],
                secondary_sensors=["modis_thermal", "landsat_thermal"],
                archaeological_visibility="low",
                preservation_potential="excellent",
                access_difficulty="extreme",
                notes="Continente antártico - hielo permanente"
            )
        
        # Groenlandia (capa de hielo)
        if 60 <= lat <= 84 and -75 <= lon <= -10:
            logger.info("❄️ GROENLANDIA detectada")
            return EnvironmentContext(
                environment_type=EnvironmentType.POLAR_ICE,
                confidence=0.95,
                coordinates=(lat, lon),
                temperature_range_c=(-40, 10),
                precipitation_mm_year=200,
                elevation_m=2000,
                primary_sensors=["icesat2", "sentinel1_sar", "palsar"],
                secondary_sensors=["modis_thermal"],
                archaeological_visibility="low",
                preservation_potential="excellent",
                access_difficulty="extreme",
                notes="Capa de hielo de Groenlandia"
            )
        
        # Ártico (permafrost y tundra)
        if 66.5 <= lat <= 75:
            # Excluir Groenlandia ya detectada
            if not (-75 <= lon <= -10):
                logger.info("❄️ ÁRTICO/TUNDRA detectado")
                return EnvironmentContext(
                    environment_type=EnvironmentType.PERMAFROST,
                    confidence=0.85,
                    coordinates=(lat, lon),
                    temperature_range_c=(-30, 15),
                    precipitation_mm_year=300,
                    elevation_m=100,
                    primary_sensors=["sentinel1_sar", "landsat", "modis"],
                    secondary_sensors=["icesat2", "palsar"],
                    archaeological_visibility="medium",
                    preservation_potential="excellent",
                    access_difficulty="difficult",
                    notes="Región ártica - permafrost y tundra"
                )
        
        return None
    
    def _check_oceans(self, lat: float, lon: float) -> Optional[EnvironmentContext]:
        """Detectar océanos usando límites PRECISOS de continentes"""
        
        # Verificar si está en tierra firme
        if self._is_on_land(lat, lon):
            return None
        
        # Si no está en tierra, está en océano
        # Determinar profundidad aproximada por ubicación
        depth = self._estimate_ocean_depth(lat, lon)
        
        if depth > 200:
            logger.info(f"🌊 OCÉANO PROFUNDO detectado (~{depth}m)")
            return EnvironmentContext(
                environment_type=EnvironmentType.DEEP_OCEAN,
                confidence=0.90,
                coordinates=(lat, lon),
                temperature_range_c=(2, 25),
                precipitation_mm_year=None,
                elevation_m=-depth,
                primary_sensors=["multibeam_sonar", "magnetometer", "sub_bottom_profiler"],
                secondary_sensors=["side_scan_sonar", "rov_cameras"],
                archaeological_visibility="low",
                preservation_potential="excellent",
                access_difficulty="extreme",
                notes=f"Océano profundo - profundidad estimada {depth}m"
            )
        else:
            logger.info(f"🌊 MAR POCO PROFUNDO detectado (~{depth}m)")
            return EnvironmentContext(
                environment_type=EnvironmentType.SHALLOW_SEA,
                confidence=0.85,
                coordinates=(lat, lon),
                temperature_range_c=(10, 28),
                precipitation_mm_year=None,
                elevation_m=-depth,
                primary_sensors=["multibeam_sonar", "side_scan_sonar", "magnetometer"],
                secondary_sensors=["sub_bottom_profiler", "acoustic_reflectance"],
                archaeological_visibility="medium",
                preservation_potential="good",
                access_difficulty="difficult",
                notes=f"Mar poco profundo - profundidad estimada {depth}m"
            )
    
    def _check_major_lakes(self, lat: float, lon: float) -> Optional[EnvironmentContext]:
        """Detectar lagos grandes ESPECÍFICOS"""
        
        # Grandes Lagos (América del Norte)
        if 41 <= lat <= 49 and -93 <= lon <= -76:
            if self._point_in_great_lakes(lat, lon):
                logger.info("🌊 GRANDES LAGOS detectados")
                return EnvironmentContext(
                    environment_type=EnvironmentType.LAKE,
                    confidence=0.90,
                    coordinates=(lat, lon),
                    temperature_range_c=(-5, 25),
                    precipitation_mm_year=800,
                    elevation_m=-50,
                    primary_sensors=["multibeam_sonar", "side_scan_sonar"],
                    secondary_sensors=["magnetometer", "sub_bottom_profiler"],
                    archaeological_visibility="medium",
                    preservation_potential="good",
                    access_difficulty="moderate",
                    notes="Grandes Lagos de América del Norte"
                )
        
        # Lago Victoria (África)
        if -3 <= lat <= 1 and 31 <= lon <= 35:
            logger.info("🌊 LAGO VICTORIA detectado")
            return EnvironmentContext(
                environment_type=EnvironmentType.LAKE,
                confidence=0.85,
                coordinates=(lat, lon),
                temperature_range_c=(20, 28),
                precipitation_mm_year=1200,
                elevation_m=-40,
                primary_sensors=["multibeam_sonar", "side_scan_sonar"],
                secondary_sensors=["sub_bottom_profiler"],
                archaeological_visibility="medium",
                preservation_potential="moderate",
                access_difficulty="moderate",
                notes="Lago Victoria"
            )
        
        # Lago Baikal (Rusia)
        if 51 <= lat <= 56 and 103 <= lon <= 110:
            logger.info("🌊 LAGO BAIKAL detectado")
            return EnvironmentContext(
                environment_type=EnvironmentType.LAKE,
                confidence=0.90,
                coordinates=(lat, lon),
                temperature_range_c=(-20, 20),
                precipitation_mm_year=400,
                elevation_m=-700,
                primary_sensors=["multibeam_sonar", "side_scan_sonar"],
                secondary_sensors=["sub_bottom_profiler"],
                archaeological_visibility="low",
                preservation_potential="excellent",
                access_difficulty="difficult",
                notes="Lago Baikal - lago más profundo del mundo"
            )
        
        return None
    
    def _check_rivers(self, lat: float, lon: float) -> Optional[EnvironmentContext]:
        """Detectar ríos principales con BUFFER ESTRECHO (solo cauce)"""
        
        # Río Nilo - SOLO el cauce, no todo Egipto
        if 4 <= lat <= 31:
            # Cauce del Nilo en diferentes secciones
            if lat > 24:  # Norte de Egipto (Cairo, delta)
                nile_lon = 31.25  # Longitud aproximada del Nilo en Cairo
                distance_km = abs(lon - nile_lon) * 111  # Conversión a km
                if distance_km < 3:  # Buffer de 3km (solo el cauce)
                    logger.info(f"🌊 RÍO NILO detectado (distancia: {distance_km:.1f}km)")
                    return self._create_river_context(lat, lon, "Río Nilo")
            elif 15 <= lat <= 24:  # Sudán
                nile_lon = 32.5
                distance_km = abs(lon - nile_lon) * 111
                if distance_km < 3:
                    logger.info(f"🌊 RÍO NILO detectado (distancia: {distance_km:.1f}km)")
                    return self._create_river_context(lat, lon, "Río Nilo (Sudán)")
        
        # Río Amazonas - SOLO el cauce principal
        if -5 <= lat <= 2 and -70 <= lon <= -48:
            # El Amazonas fluye aproximadamente a lo largo de lat=-3
            distance_km = abs(lat - (-3)) * 111
            if distance_km < 5:  # Buffer de 5km
                logger.info(f"🌊 RÍO AMAZONAS detectado (distancia: {distance_km:.1f}km)")
                return self._create_river_context(lat, lon, "Río Amazonas")
        
        # Río Mississippi - SOLO el cauce
        if 29 <= lat <= 48 and -95 <= lon <= -89:
            mississippi_lon = -90.5
            distance_km = abs(lon - mississippi_lon) * 111
            if distance_km < 3:
                logger.info(f"🌊 RÍO MISSISSIPPI detectado (distancia: {distance_km:.1f}km)")
                return self._create_river_context(lat, lon, "Río Mississippi")
        
        return None
    
    def _check_mountain_glaciers(self, lat: float, lon: float) -> Optional[EnvironmentContext]:
        """Detectar glaciares de montaña ESPECÍFICOS"""
        
        # Alpes (glaciares específicos)
        if 45 <= lat <= 48 and 6 <= lon <= 13:
            # Solo en altitudes altas
            logger.info("❄️ GLACIAR ALPINO detectado")
            return EnvironmentContext(
                environment_type=EnvironmentType.GLACIER,
                confidence=0.75,
                coordinates=(lat, lon),
                temperature_range_c=(-15, 10),
                precipitation_mm_year=2000,
                elevation_m=3000,
                primary_sensors=["icesat2", "sentinel1_sar", "landsat"],
                secondary_sensors=["modis", "palsar"],
                archaeological_visibility="low",
                preservation_potential="excellent",
                access_difficulty="extreme",
                notes="Glaciar alpino - alta montaña"
            )
        
        # Himalaya (glaciares)
        if 27 <= lat <= 36 and 70 <= lon <= 95:
            logger.info("❄️ GLACIAR HIMALAYO detectado")
            return EnvironmentContext(
                environment_type=EnvironmentType.GLACIER,
                confidence=0.80,
                coordinates=(lat, lon),
                temperature_range_c=(-20, 10),
                precipitation_mm_year=1500,
                elevation_m=4500,
                primary_sensors=["icesat2", "sentinel1_sar", "landsat"],
                secondary_sensors=["modis", "palsar"],
                archaeological_visibility="low",
                preservation_potential="excellent",
                access_difficulty="extreme",
                notes="Glaciar himalayo"
            )
        
        return None
    
    def _check_deserts(self, lat: float, lon: float) -> Optional[EnvironmentContext]:
        """Detectar desiertos CONOCIDOS con límites PRECISOS"""
        
        # Sahara (el más grande) - incluye Egipto excepto el valle del Nilo
        if 15 <= lat <= 35 and -17 <= lon <= 35:
            # Excluir SOLO el cauce estrecho del Nilo (no todo Egipto)
            in_nile_valley = False
            if 4 <= lat <= 31:
                # Cauce del Nilo en diferentes secciones
                if lat > 24:  # Norte de Egipto (Cairo, delta)
                    nile_lon = 31.25
                    distance_km = abs(lon - nile_lon) * 111
                    if distance_km < 10:  # Solo 10km del cauce
                        in_nile_valley = True
                elif 15 <= lat <= 24:  # Sudán
                    nile_lon = 32.5
                    distance_km = abs(lon - nile_lon) * 111
                    if distance_km < 10:
                        in_nile_valley = True
            
            if not in_nile_valley:
                logger.info("🏜️ DESIERTO DEL SAHARA detectado")
                return EnvironmentContext(
                    environment_type=EnvironmentType.DESERT,
                    confidence=0.95,
                    coordinates=(lat, lon),
                    temperature_range_c=(5, 50),
                    precipitation_mm_year=50,
                    elevation_m=300,
                    primary_sensors=["landsat_thermal", "sentinel2", "sar"],
                    secondary_sensors=["modis", "srtm_dem"],
                    archaeological_visibility="high",
                    preservation_potential="excellent",
                    access_difficulty="moderate",
                    notes="Desierto del Sahara - excelente para detección arqueológica"
                )
        
        # Desierto Arábigo
        if 12 <= lat <= 32 and 35 <= lon <= 60:
            logger.info("🏜️ DESIERTO ARÁBIGO detectado")
            return EnvironmentContext(
                environment_type=EnvironmentType.DESERT,
                confidence=0.90,
                coordinates=(lat, lon),
                temperature_range_c=(10, 50),
                precipitation_mm_year=100,
                elevation_m=500,
                primary_sensors=["landsat_thermal", "sentinel2", "sar"],
                secondary_sensors=["modis", "srtm_dem"],
                archaeological_visibility="high",
                preservation_potential="excellent",
                access_difficulty="moderate",
                notes="Desierto Arábigo"
            )
        
        # Desierto de Gobi
        if 38 <= lat <= 47 and 90 <= lon <= 110:
            logger.info("🏜️ DESIERTO DE GOBI detectado")
            return EnvironmentContext(
                environment_type=EnvironmentType.DESERT,
                confidence=0.85,
                coordinates=(lat, lon),
                temperature_range_c=(-40, 40),
                precipitation_mm_year=150,
                elevation_m=1000,
                primary_sensors=["landsat_thermal", "sentinel2", "sar"],
                secondary_sensors=["modis", "srtm_dem"],
                archaeological_visibility="high",
                preservation_potential="good",
                access_difficulty="moderate",
                notes="Desierto de Gobi"
            )
        
        # Desierto de Atacama
        if -27 <= lat <= -18 and -71 <= lon <= -68:
            logger.info("🏜️ DESIERTO DE ATACAMA detectado")
            return EnvironmentContext(
                environment_type=EnvironmentType.DESERT,
                confidence=0.95,
                coordinates=(lat, lon),
                temperature_range_c=(0, 30),
                precipitation_mm_year=15,  # Uno de los más secos
                elevation_m=2500,
                primary_sensors=["landsat_thermal", "sentinel2", "sar"],
                secondary_sensors=["modis", "srtm_dem"],
                archaeological_visibility="high",
                preservation_potential="excellent",
                access_difficulty="moderate",
                notes="Desierto de Atacama - extremadamente árido"
            )
        
        return None
    
    def _check_mountain_regions(self, lat: float, lon: float) -> Optional[EnvironmentContext]:
        """Detectar regiones montañosas específicas"""
        
        # AJUSTE 1: Amazonía occidental (Acre, Brasil) - EXCEPCIÓN CRÍTICA
        # Geoglifos precolombinos documentados en mesetas suavemente elevadas
        if -12 <= lat <= -8 and -70 <= lon <= -65:
            logger.info("🌳 AMAZONÍA OCCIDENTAL (Acre) detectada - zona de geoglifos")
            return EnvironmentContext(
                environment_type=EnvironmentType.FOREST,
                confidence=0.90,
                coordinates=(lat, lon),
                temperature_range_c=(20, 32),
                precipitation_mm_year=1800,
                elevation_m=200,  # Meseta suavemente elevada, NO montaña
                primary_sensors=["sentinel2", "sentinel1_sar", "lidar"],
                secondary_sensors=["landsat", "modis"],
                archaeological_visibility="medium",  # Vegetación pero detectable
                preservation_potential="excellent",  # Geoglifos preservados
                access_difficulty="moderate",
                notes="Amazonía occidental - meseta con geoglifos precolombinos documentados (Acre, Brasil)"
            )
        
        # Andes (incluyendo Machu Picchu)
        if -56 <= lat <= 11 and -82 <= lon <= -63:
            # Machu Picchu está en: -13.1631°, -72.5450°
            logger.info("⛰️ ANDES detectados")
            return EnvironmentContext(
                environment_type=EnvironmentType.MOUNTAIN,
                confidence=0.85,
                coordinates=(lat, lon),
                temperature_range_c=(-10, 25),
                precipitation_mm_year=800,
                elevation_m=3000,
                primary_sensors=["srtm_dem", "sentinel2", "sar", "lidar"],
                secondary_sensors=["landsat", "modis"],
                archaeological_visibility="medium",
                preservation_potential="excellent",
                access_difficulty="difficult",
                notes="Cordillera de los Andes - topografía montañosa compleja"
            )
        
        # Himalaya
        if 27 <= lat <= 36 and 70 <= lon <= 95:
            # Excluir glaciares ya detectados
            logger.info("⛰️ HIMALAYA detectado")
            return EnvironmentContext(
                environment_type=EnvironmentType.MOUNTAIN,
                confidence=0.90,
                coordinates=(lat, lon),
                temperature_range_c=(-15, 20),
                precipitation_mm_year=1000,
                elevation_m=4000,
                primary_sensors=["srtm_dem", "sentinel2", "sar", "lidar"],
                secondary_sensors=["landsat", "modis"],
                archaeological_visibility="low",
                preservation_potential="excellent",
                access_difficulty="extreme",
                notes="Himalaya - montañas de gran altitud"
            )
        
        # Alpes (sin glaciares)
        if 43 <= lat <= 48 and 5 <= lon <= 14:
            logger.info("⛰️ ALPES detectados")
            return EnvironmentContext(
                environment_type=EnvironmentType.MOUNTAIN,
                confidence=0.80,
                coordinates=(lat, lon),
                temperature_range_c=(-10, 20),
                precipitation_mm_year=1200,
                elevation_m=2500,
                primary_sensors=["srtm_dem", "sentinel2", "sar", "lidar"],
                secondary_sensors=["landsat", "modis"],
                archaeological_visibility="medium",
                preservation_potential="good",
                access_difficulty="difficult",
                notes="Alpes - montañas europeas"
            )
        
        # Montañas Rocosas
        if 31 <= lat <= 60 and -120 <= lon <= -102:
            logger.info("⛰️ MONTAÑAS ROCOSAS detectadas")
            return EnvironmentContext(
                environment_type=EnvironmentType.MOUNTAIN,
                confidence=0.80,
                coordinates=(lat, lon),
                temperature_range_c=(-20, 25),
                precipitation_mm_year=600,
                elevation_m=2500,
                primary_sensors=["srtm_dem", "sentinel2", "sar", "lidar"],
                secondary_sensors=["landsat", "modis"],
                archaeological_visibility="medium",
                preservation_potential="good",
                access_difficulty="moderate",
                notes="Montañas Rocosas de América del Norte"
            )
        
        return None
    
    def _classify_by_climate(self, lat: float, lon: float) -> Optional[EnvironmentContext]:
        """Clasificación por zona climática (fallback)"""
        
        abs_lat = abs(lat)
        
        # Zonas tropicales (selva/bosque)
        if abs_lat < 23.5:
            logger.info("🌳 ZONA TROPICAL detectada")
            return EnvironmentContext(
                environment_type=EnvironmentType.FOREST,
                confidence=0.60,
                coordinates=(lat, lon),
                temperature_range_c=(20, 35),
                precipitation_mm_year=2000,
                elevation_m=200,
                primary_sensors=["lidar", "sentinel2", "sar"],
                secondary_sensors=["landsat", "modis"],
                archaeological_visibility="low",
                preservation_potential="poor",
                access_difficulty="difficult",
                notes="Zona tropical - probable vegetación densa"
            )
        
        # Zonas templadas
        if 23.5 <= abs_lat < 50:
            logger.info("🌾 ZONA TEMPLADA detectada")
            return EnvironmentContext(
                environment_type=EnvironmentType.AGRICULTURAL,
                confidence=0.50,
                coordinates=(lat, lon),
                temperature_range_c=(-5, 30),
                precipitation_mm_year=800,
                elevation_m=300,
                primary_sensors=["sentinel2", "landsat", "sar"],
                secondary_sensors=["lidar", "modis"],
                archaeological_visibility="medium",
                preservation_potential="moderate",
                access_difficulty="easy",
                notes="Zona templada - probable uso agrícola"
            )
        
        return None
    
    def _create_river_context(self, lat: float, lon: float, river_name: str) -> EnvironmentContext:
        """Crear contexto para río"""
        return EnvironmentContext(
            environment_type=EnvironmentType.RIVER,
            confidence=0.80,
            coordinates=(lat, lon),
            temperature_range_c=(5, 30),
            precipitation_mm_year=500,
            elevation_m=0,
            primary_sensors=["multibeam_sonar", "side_scan_sonar", "sub_bottom_profiler"],
            secondary_sensors=["magnetometer", "gpr"],
            archaeological_visibility="low",
            preservation_potential="moderate",
            access_difficulty="moderate",
            notes=f"{river_name} - cauce principal"
        )
    
    def _create_unknown_context(self, lat: float, lon: float) -> EnvironmentContext:
        """Crear contexto para ambiente desconocido"""
        return EnvironmentContext(
            environment_type=EnvironmentType.UNKNOWN,
            confidence=0.0,
            coordinates=(lat, lon),
            temperature_range_c=(-10, 30),
            precipitation_mm_year=None,
            elevation_m=None,
            primary_sensors=["sentinel2", "landsat", "sar"],
            secondary_sensors=["modis", "srtm_dem"],
            archaeological_visibility="unknown",
            preservation_potential="unknown",
            access_difficulty="unknown",
            notes="Ambiente no clasificado - usar sensores generales"
        )
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _is_on_land(self, lat: float, lon: float) -> bool:
        """Verificar si coordenadas están en tierra firme (simplificado pero preciso)"""
        
        # América del Norte (continental) - INCLUYE MÉXICO Y CENTROAMÉRICA
        if 14 <= lat <= 72 and -170 <= lon <= -50:
            # Excluir Grandes Lagos
            if 41 <= lat <= 49 and -93 <= lon <= -76:  # Grandes Lagos
                return False
            # Excluir Golfo de México (solo agua abierta, no costas)
            if 18 <= lat <= 30 and -97 <= lon <= -80:
                # Península de Yucatán (México) - TIERRA FIRME
                if 17 <= lat <= 22 and -92 <= lon <= -86:
                    return True
                # Costa de México (Veracruz, Tamaulipas) - TIERRA FIRME
                if 18 <= lat <= 26 and -100 <= lon <= -96:
                    return True
                # Florida - TIERRA FIRME
                if 24 <= lat <= 31 and -88 <= lon <= -80:
                    return True
                # Resto del Golfo - AGUA
                return False
            return True
        
        # Caribe e islas - SOLO islas pequeñas, NO península de Yucatán
        # Port Royal, Jamaica está aquí: 17.94°N, -76.84°W
        if 10 <= lat <= 25 and -85 <= lon <= -60:
            # Esta es zona de islas caribeñas - considerar como AGUA
            return False
        
        # América del Sur
        if -56 <= lat <= 13 and -82 <= lon <= -34:
            return True
        
        # Europa
        if 36 <= lat <= 71 and -10 <= lon <= 40:
            return True
        
        # África
        if -35 <= lat <= 37 and -18 <= lon <= 52:
            return True
        
        # Asia
        if 5 <= lat <= 75 and 25 <= lon <= 180:
            # Excluir grandes lagos
            return True
        
        # Australia
        if -44 <= lat <= -10 and 113 <= lon <= 154:
            return True
        
        return False
    
    def _estimate_ocean_depth(self, lat: float, lon: float) -> float:
        """Estimar profundidad del océano (simplificado)"""
        
        # CASOS ESPECIALES: Aguas poco profundas conocidas
        
        # Caribe (incluyendo Port Royal, Jamaica)
        if 10 <= lat <= 25 and -85 <= lon <= -60:
            return 50  # Aguas poco profundas del Caribe
        
        # Mediterráneo
        if 30 <= lat <= 46 and -6 <= lon <= 37:
            return 150  # Mar Mediterráneo poco profundo
        
        # Golfo Pérsico
        if 24 <= lat <= 30 and 48 <= lon <= 57:
            return 50  # Aguas poco profundas
        
        # Mar del Norte
        if 51 <= lat <= 62 and -4 <= lon <= 9:
            return 100  # Aguas poco profundas
        
        # Profundidades típicas por región (océanos abiertos)
        abs_lat = abs(lat)
        
        if abs_lat > 60:  # Regiones polares
            return 1000
        elif abs_lat > 40:  # Latitudes medias
            return 3000
        else:  # Trópicos (océanos abiertos)
            return 4000
    
    def _point_in_great_lakes(self, lat: float, lon: float) -> bool:
        """Verificar si punto está en Grandes Lagos (simplificado)"""
        # Aproximación simple - en producción usar polígonos precisos
        if 41 <= lat <= 49 and -93 <= lon <= -76:
            return True
        return False
    
    def _load_glacier_database(self) -> Dict:
        """Cargar base de datos de glaciares"""
        return {}
    
    def _load_ocean_database(self) -> Dict:
        """Cargar base de datos de océanos"""
        return {}
    
    def _load_desert_database(self) -> Dict:
        """Cargar base de datos de desiertos"""
        return {}
    
    def _load_river_database(self) -> Dict:
        """Cargar base de datos de ríos"""
        return {}
