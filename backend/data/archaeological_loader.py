#!/usr/bin/env python3
"""
Cargador de datos arqueológicos para ArcheoScope.

Integra múltiples fuentes de datos satelitales y geofísicos
optimizados para detección de intervención humana antigua.
"""

import numpy as np
import xarray as xr
from typing import Dict, List, Tuple, Any, Optional
import logging
from datetime import datetime, timedelta
import requests
from pathlib import Path
from .enhanced_archaeological_apis import EnhancedArchaeologicalAPIs, integrate_enhanced_apis

logger = logging.getLogger(__name__)

class ArchaeologicalDataLoader:
    """
    Cargador especializado para datos arqueológicos remotos.
    
    Integra:
    - Datos ópticos multiespectrales (Sentinel-2, Landsat)
    - Datos térmicos (MODIS LST, Landsat thermal)
    - Datos SAR (Sentinel-1 backscatter)
    - Datos sísmicos pasivos (IRIS)
    - Scatterometer (ASCAT rugosidad)
    - Salinidad superficial (SMOS/SMAP)
    """
    
    def __init__(self, cache_dir: str = "data/cache"):
        """
        Inicializar cargador arqueológico.
        
        Args:
            cache_dir: Directorio para cache de datos descargados
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # URLs de APIs públicas base
        self.apis = {
            'iris_seismic': 'http://service.iris.edu/fdsnws/dataselect/1/',
            'esa_scihub': 'https://scihub.copernicus.eu/dhus/',
            'usgs_landsat': 'https://earthexplorer.usgs.gov/api/api/json/v1.4.0/',
            'modis_thermal': 'https://modis.gsfc.nasa.gov/data/',
            'smos_salinity': 'https://smos-diss.eo.esa.int/socat-sl/'
        }
        
        # Integrar APIs arqueológicas mejoradas
        self.enhanced_apis = EnhancedArchaeologicalAPIs()
        integrate_enhanced_apis(self)
        
        logger.info("ArchaeologicalDataLoader inicializado con APIs mejoradas")
        logger.info(f"APIs base: {len(self.apis)}, APIs mejoradas: {len(self.enhanced_apis.enhanced_apis)}")
    
    def create_synthetic_archaeological_data(self, region_name: str, 
                                           data_type: str, 
                                           region_size: Tuple[int, int],
                                           bounds: Dict[str, float]) -> xr.DataArray:
        """
        Crear datos sintéticos arqueológicos REALISTAS según ubicación geográfica.
        
        Args:
            region_name: Nombre de la región
            data_type: Tipo de dato arqueológico
            region_size: Tamaño de la región (height, width)
            bounds: Límites geográficos
            
        Returns:
            DataArray con datos sintéticos realistas según ubicación
        """
        height, width = region_size
        
        # NUEVO: Determinar tipo de ambiente según coordenadas
        environment_type = self._classify_environment(bounds)
        archaeological_potential = self._assess_archaeological_potential(bounds, environment_type)
        
        logger.info(f"🌍 Ambiente detectado: {environment_type}, Potencial arqueológico: {archaeological_potential}")
        
        # Generar datos base según el tipo Y la ubicación geográfica
        if data_type == 'ndvi_vegetation':
            data = self._generate_ndvi_realistic(height, width, environment_type, archaeological_potential)
            units = 'NDVI'
            description = f'NDVI realista para {environment_type}'
            
        elif data_type == 'thermal_lst':
            data = self._generate_thermal_realistic(height, width, environment_type, archaeological_potential)
            units = 'Kelvin'
            description = f'Temperatura realista para {environment_type}'
            
        elif data_type == 'sar_backscatter':
            data = self._generate_sar_realistic(height, width, environment_type, archaeological_potential)
            units = 'dB'
            description = f'SAR realista para {environment_type}'
            
        elif data_type == 'surface_roughness':
            data = self._generate_roughness_realistic(height, width, environment_type, archaeological_potential)
            units = 'roughness_index'
            description = f'Rugosidad realista para {environment_type}'
            
        elif data_type == 'soil_salinity':
            data = self._generate_salinity_realistic(height, width, environment_type, archaeological_potential)
            units = 'psu'
            description = f'Salinidad realista para {environment_type}'
            
        elif data_type == 'seismic_resonance':
            data = self._generate_seismic_realistic(height, width, environment_type, archaeological_potential)
            units = 'resonance_factor'
            description = f'Resonancia realista para {environment_type}'
            
        # NUEVAS CAPAS AVANZADAS PARA VISUALIZACIÓN IMPACTANTE
        elif data_type == 'lidar_fullwave':
            data = self.enhanced_apis.get_lidar_fullwave_data(bounds)
            if data is not None:
                return data  # Ya viene como DataArray completo
            else:
                data = self._generate_generic_realistic(height, width, environment_type)
                units = 'meters'
                description = f'LiDAR Full-Waveform sintético para {environment_type}'
            
        elif data_type == 'dem_multiscale':
            data = self.enhanced_apis.get_dem_multiscale_fusion(bounds)
            if data is not None:
                return data  # Ya viene como DataArray completo
            else:
                data = self._generate_generic_realistic(height, width, environment_type)
                units = 'meters'
                description = f'DEM Multiescala sintético para {environment_type}'
            
        elif data_type == 'spectral_roughness':
            data = self.enhanced_apis.get_spectral_roughness_analysis(bounds)
            if data is not None:
                return data  # Ya viene como DataArray completo
            else:
                data = self._generate_generic_realistic(height, width, environment_type)
                units = 'log_power_spectrum'
                description = f'Rugosidad Espectral sintética para {environment_type}'
            
        elif data_type == 'pseudo_lidar_ai':
            data = self.enhanced_apis.get_pseudo_lidar_ai(bounds)
            if data is not None:
                return data  # Ya viene como DataArray completo
            else:
                data = self._generate_generic_realistic(height, width, environment_type)
                units = 'meters_inferred'
                description = f'Pseudo-LiDAR IA sintético para {environment_type}'
            
        elif data_type == 'multitemporal_topo':
            data = self.enhanced_apis.get_multitemporal_topography(bounds)
            if data is not None:
                return data  # Ya viene como DataArray completo
            else:
                data = self._generate_generic_realistic(height, width, environment_type)
                units = 'meters_change'
                description = f'Topografía Multitemporal sintética para {environment_type}'
            
        else:
            # Datos genéricos realistas
            data = self._generate_generic_realistic(height, width, environment_type)
            units = 'generic'
            description = f'Datos realistas para {environment_type}: {data_type}'
        
        # Crear coordenadas geográficas
        lats = np.linspace(bounds['lat_min'], bounds['lat_max'], height)
        lons = np.linspace(bounds['lon_min'], bounds['lon_max'], width)
        
        # Crear DataArray
        data_array = xr.DataArray(
            data,
            coords={'lat': lats, 'lon': lons},
            dims=['lat', 'lon'],
            name=region_name,
            attrs={
                'data_type': data_type,
                'units': units,
                'description': description,
                'environment_type': environment_type,
                'archaeological_potential': archaeological_potential,
                'creation_date': datetime.now().isoformat(),
                'bounds': bounds,
                'synthetic': True,
                'realistic_for_location': True
            }
        )
        
        logger.info(f"Datos realistas creados: {data_type} para {environment_type} "
                   f"({height}x{width}) - Potencial: {archaeological_potential}")
        
        return data_array
    
    def _classify_environment(self, bounds: Dict[str, float]) -> str:
        """Clasificar tipo de ambiente según coordenadas geográficas."""
        
        lat_center = (bounds['lat_min'] + bounds['lat_max']) / 2
        lon_center = (bounds['lon_min'] + bounds['lon_max']) / 2
        
        # Océanos (coordenadas en agua)
        if (abs(lat_center) < 60 and 
            ((lon_center < -120 and lon_center > -180) or  # Pacífico
             (lon_center > 120 and lon_center < 180))):    # Pacífico Oeste
            return "ocean"
        
        # Desiertos
        if ((lat_center > 15 and lat_center < 35 and lon_center > -10 and lon_center < 40) or  # Sahara
            (lat_center > 25 and lat_center < 45 and lon_center > -125 and lon_center < -100)):  # Desierto SW USA
            return "desert"
        
        # Bosques boreales
        if lat_center > 50 and lat_center < 70:
            if lon_center > -130 and lon_center < -100:  # Canadá
                return "boreal_forest"
            elif lon_center > 20 and lon_center < 180:   # Siberia
                return "boreal_forest"
        
        # Selva tropical africana
        if (lat_center > -10 and lat_center < 10 and 
            lon_center > 10 and lon_center < 40):
            return "african_rainforest"
        
        # Amazonía
        if (lat_center > -15 and lat_center < 5 and 
            lon_center > -80 and lon_center < -45):
            return "amazon_rainforest"
        
        # Manglares (costas tropicales)
        if (abs(lat_center) < 30 and 
            ((lon_center > 140 and lon_center < 150) or  # Australia
             (lon_center > -90 and lon_center < -80))):   # Golfo México
            return "mangrove"
        
        # Por defecto: templado
        return "temperate"
    
    def _assess_archaeological_potential(self, bounds: Dict[str, float], environment: str) -> str:
        """Evaluar potencial arqueológico realista según ubicación y ambiente."""
        
        lat_center = (bounds['lat_min'] + bounds['lat_max']) / 2
        lon_center = (bounds['lon_min'] + bounds['lon_max']) / 2
        
        # Océanos: sin potencial arqueológico
        if environment == "ocean":
            return "none"
        
        # Desiertos extremos: muy bajo
        if environment == "desert":
            return "very_low"
        
        # Bosques boreales: bajo (poblamiento tardío)
        if environment == "boreal_forest":
            return "low"
        
        # Selva africana: bajo a moderado (poblamiento disperso)
        if environment == "african_rainforest":
            return "low"
        
        # Amazonía: ALTO (hipótesis antropogénica)
        if environment == "amazon_rainforest":
            # Tapajós-Xingu específicamente
            if (lat_center > -7 and lat_center < -6 and 
                lon_center > -56 and lon_center < -54):
                return "very_high"  # Zona de interés específica
            else:
                return "moderate"   # Amazonía general
        
        # Manglares: bajo (ambientes dinámicos)
        if environment == "mangrove":
            return "low"
        
        # Templado: moderado a alto
        return "moderate"
    
    def _generate_ndvi_realistic(self, height: int, width: int, environment: str, potential: str) -> np.ndarray:
        """Generar NDVI realista según ambiente y potencial arqueológico."""
        
        if environment == "ocean":
            # Océano: NDVI muy bajo, sin patrones
            return np.random.normal(0.05, 0.02, (height, width)).clip(0, 0.1)
        
        elif environment == "desert":
            # Desierto: NDVI muy bajo, sin patrones arqueológicos
            base = np.random.normal(0.15, 0.05, (height, width)).clip(0.05, 0.3)
            return base
        
        elif environment == "boreal_forest":
            # Bosque boreal: NDVI moderado, patrones naturales
            base = np.random.normal(0.4, 0.1, (height, width)).clip(0.2, 0.7)
            return base
        
        elif environment == "african_rainforest":
            # Selva africana: NDVI alto, sin patrones arqueológicos significativos
            base = np.random.normal(0.75, 0.1, (height, width)).clip(0.5, 0.9)
            return base
        
        elif environment == "amazon_rainforest":
            # Amazonía: NDVI alto, CON patrones si potencial es alto
            base = np.random.normal(0.8, 0.08, (height, width)).clip(0.6, 0.95)
            
            if potential == "very_high":
                # Añadir patrones sutiles de manejo (Tapajós-Xingu)
                # Patrones lineales sutiles (manejo de bosque)
                for i in range(0, height, 15):
                    if i < height - 3:
                        base[i:i+2, :] *= 0.95  # Líneas sutiles de manejo
                
                # Parches de diversidad manejada
                patch_size = 8
                for y in range(0, height-patch_size, 20):
                    for x in range(0, width-patch_size, 25):
                        base[y:y+patch_size, x:x+patch_size] *= 1.05  # Parches más verdes
            
            return base
        
        elif environment == "mangrove":
            # Manglar: NDVI moderado, patrones naturales dinámicos
            base = np.random.normal(0.6, 0.15, (height, width)).clip(0.3, 0.8)
            return base
        
        else:  # temperate
            # Templado: NDVI moderado, puede tener patrones arqueológicos
            base = np.random.normal(0.5, 0.12, (height, width)).clip(0.2, 0.8)
            
            if potential in ["high", "very_high"]:
                # Añadir patrones arqueológicos sutiles
                base = self._add_subtle_archaeological_patterns(base)
            
            return base
    
    def _generate_thermal_realistic(self, height: int, width: int, environment: str, potential: str) -> np.ndarray:
        """Generar datos térmicos realistas según ambiente."""
        
        if environment == "ocean":
            # Océano: temperatura estable, sin anomalías
            return np.random.normal(288, 2, (height, width))  # ~15°C
        
        elif environment == "desert":
            # Desierto: temperatura alta, variación natural
            return np.random.normal(310, 8, (height, width))  # ~37°C
        
        elif environment == "boreal_forest":
            # Bosque boreal: temperatura baja
            return np.random.normal(275, 5, (height, width))  # ~2°C
        
        elif environment in ["african_rainforest", "amazon_rainforest"]:
            # Selvas tropicales: temperatura moderada-alta
            base = np.random.normal(298, 3, (height, width))  # ~25°C
            
            if environment == "amazon_rainforest" and potential == "very_high":
                # Añadir anomalías térmicas sutiles (suelos manejados)
                base = self._add_subtle_thermal_anomalies(base)
            
            return base
        
        elif environment == "mangrove":
            # Manglar: temperatura moderada, húmedo
            return np.random.normal(295, 4, (height, width))  # ~22°C
        
        else:  # temperate
            # Templado: temperatura moderada
            base = np.random.normal(290, 6, (height, width))  # ~17°C
            
            if potential in ["high", "very_high"]:
                base = self._add_subtle_thermal_anomalies(base)
            
            return base
    
    def _generate_sar_realistic(self, height: int, width: int, environment: str, potential: str) -> np.ndarray:
        """Generar SAR realista según ambiente."""
        
        if environment == "ocean":
            # Océano: backscatter muy bajo y uniforme
            return np.random.normal(-25, 2, (height, width))
        
        elif environment == "desert":
            # Desierto: backscatter moderado, textura natural
            return np.random.normal(-8, 3, (height, width))
        
        elif environment == "boreal_forest":
            # Bosque boreal: backscatter moderado-alto
            return np.random.normal(-10, 4, (height, width))
        
        elif environment in ["african_rainforest", "amazon_rainforest"]:
            # Selvas: backscatter alto (vegetación densa)
            base = np.random.normal(-6, 3, (height, width))
            
            if environment == "amazon_rainforest" and potential == "very_high":
                # Añadir patrones sutiles de estructura
                base = self._add_subtle_sar_patterns(base)
            
            return base
        
        elif environment == "mangrove":
            # Manglar: backscatter variable (agua + vegetación)
            return np.random.normal(-12, 5, (height, width))
        
        else:  # temperate
            base = np.random.normal(-12, 4, (height, width))
            
            if potential in ["high", "very_high"]:
                base = self._add_subtle_sar_patterns(base)
            
            return base
    
    def _generate_roughness_realistic(self, height: int, width: int, environment: str, potential: str) -> np.ndarray:
        """Generar rugosidad realista según ambiente."""
        
        if environment == "ocean":
            # Océano: rugosidad muy baja (superficie de agua)
            return np.random.exponential(0.05, (height, width)).clip(0, 0.2)
        
        elif environment == "desert":
            # Desierto: rugosidad variable (dunas, rocas)
            return np.random.exponential(0.4, (height, width)).clip(0, 2.0)
        
        elif environment == "boreal_forest":
            # Bosque boreal: rugosidad moderada
            return np.random.exponential(0.3, (height, width)).clip(0, 1.5)
        
        elif environment in ["african_rainforest", "amazon_rainforest"]:
            # Selvas: rugosidad alta (vegetación densa)
            base = np.random.exponential(0.5, (height, width)).clip(0, 2.5)
            
            if environment == "amazon_rainforest" and potential == "very_high":
                # Patrones sutiles de manejo (senderos, claros)
                base = self._add_subtle_roughness_patterns(base)
            
            return base
        
        elif environment == "mangrove":
            # Manglar: rugosidad moderada-alta
            return np.random.exponential(0.4, (height, width)).clip(0, 2.0)
        
        else:  # temperate
            base = np.random.exponential(0.3, (height, width)).clip(0, 1.8)
            
            if potential in ["high", "very_high"]:
                base = self._add_subtle_roughness_patterns(base)
            
            return base
    
    def _generate_salinity_realistic(self, height: int, width: int, environment: str, potential: str) -> np.ndarray:
        """Generar salinidad realista según ambiente."""
        
        if environment == "ocean":
            # Océano: salinidad alta y uniforme
            return np.random.normal(35, 2, (height, width)).clip(30, 40)  # psu oceánica
        
        elif environment == "desert":
            # Desierto: salinidad variable (evaporación)
            return np.random.exponential(1.5, (height, width)).clip(0.1, 8.0)
        
        elif environment == "boreal_forest":
            # Bosque boreal: salinidad muy baja
            return np.random.exponential(0.2, (height, width)).clip(0.05, 1.0)
        
        elif environment in ["african_rainforest", "amazon_rainforest"]:
            # Selvas: salinidad baja (alta precipitación)
            base = np.random.exponential(0.3, (height, width)).clip(0.1, 1.5)
            
            if environment == "amazon_rainforest" and potential == "very_high":
                # Patrones de drenaje manejado
                base = self._add_subtle_salinity_patterns(base)
            
            return base
        
        elif environment == "mangrove":
            # Manglar: salinidad moderada-alta (influencia marina)
            return np.random.normal(15, 5, (height, width)).clip(5, 30)
        
        else:  # temperate
            base = np.random.exponential(0.5, (height, width)).clip(0.1, 3.0)
            
            if potential in ["high", "very_high"]:
                base = self._add_subtle_salinity_patterns(base)
            
            return base
    
    def _generate_seismic_realistic(self, height: int, width: int, environment: str, potential: str) -> np.ndarray:
        """Generar resonancia sísmica realista según ambiente."""
        
        # Base realista según ambiente
        if environment == "ocean":
            return np.random.normal(0.8, 0.1, (height, width)).clip(0.5, 1.2)
        elif environment == "desert":
            return np.random.normal(1.2, 0.2, (height, width)).clip(0.8, 2.0)
        elif environment in ["african_rainforest", "amazon_rainforest"]:
            base = np.random.normal(1.0, 0.15, (height, width)).clip(0.6, 1.8)
            
            if environment == "amazon_rainforest" and potential == "very_high":
                # Anomalías sísmicas sutiles (terra preta, estructuras)
                base = self._add_subtle_seismic_anomalies(base)
            
            return base
        else:
            base = np.random.normal(1.0, 0.2, (height, width)).clip(0.5, 2.0)
            
            if potential in ["high", "very_high"]:
                base = self._add_subtle_seismic_anomalies(base)
            
            return base
    
    def _generate_generic_realistic(self, height: int, width: int, environment: str) -> np.ndarray:
        """Generar datos genéricos realistas según ambiente."""
        
        if environment == "ocean":
            return np.random.normal(0.2, 0.05, (height, width)).clip(0, 0.5)
        elif environment == "desert":
            return np.random.normal(0.3, 0.1, (height, width)).clip(0, 0.8)
        else:
            return np.random.normal(0.5, 0.15, (height, width)).clip(0, 1.0)
    
    def _add_subtle_archaeological_patterns(self, base_data: np.ndarray) -> np.ndarray:
        """Añadir patrones arqueológicos sutiles y realistas."""
        
        height, width = base_data.shape
        
        # Patrones muy sutiles (no obvios como antes)
        
        # 1. Línea sutil (camino antiguo)
        if height > 20 and width > 20:
            line_y = height // 2 + np.random.randint(-5, 6)
            line_thickness = 2
            if line_y + line_thickness < height:
                base_data[line_y:line_y+line_thickness, width//4:3*width//4] *= 0.95
        
        # 2. Patrón rectangular muy sutil
        if height > 30 and width > 30:
            rect_y = height // 3 + np.random.randint(-3, 4)
            rect_x = width // 3 + np.random.randint(-3, 4)
            rect_h, rect_w = 8, 12
            
            if rect_y + rect_h < height and rect_x + rect_w < width:
                base_data[rect_y:rect_y+rect_h, rect_x:rect_x+rect_w] *= 0.97
        
        return base_data
    
    def _add_subtle_thermal_anomalies(self, base_data: np.ndarray) -> np.ndarray:
        """Añadir anomalías térmicas sutiles."""
        
        height, width = base_data.shape
        
        # Anomalía térmica sutil (diferencia de inercia térmica)
        if height > 15 and width > 15:
            anomaly_y = height // 2 + np.random.randint(-3, 4)
            anomaly_x = width // 2 + np.random.randint(-3, 4)
            anomaly_size = 6
            
            if (anomaly_y + anomaly_size < height and 
                anomaly_x + anomaly_size < width):
                base_data[anomaly_y:anomaly_y+anomaly_size, 
                         anomaly_x:anomaly_x+anomaly_size] += 0.5  # Anomalía muy sutil
        
        return base_data
    
    def _add_subtle_sar_patterns(self, base_data: np.ndarray) -> np.ndarray:
        """Añadir patrones SAR sutiles."""
        
        height, width = base_data.shape
        
        # Línea de reflectividad sutil
        if height > 20:
            line_y = height // 2 + np.random.randint(-2, 3)
            if line_y + 1 < height:
                base_data[line_y:line_y+1, width//5:4*width//5] += 1.0  # Sutil
        
        return base_data
    
    def _add_subtle_roughness_patterns(self, base_data: np.ndarray) -> np.ndarray:
        """Añadir patrones de rugosidad sutiles."""
        
        height, width = base_data.shape
        
        # Zona ligeramente más lisa (compactación antigua)
        if height > 15 and width > 15:
            smooth_y = height // 3 + np.random.randint(-2, 3)
            smooth_x = width // 3 + np.random.randint(-2, 3)
            smooth_size = 8
            
            if (smooth_y + smooth_size < height and 
                smooth_x + smooth_size < width):
                base_data[smooth_y:smooth_y+smooth_size, 
                         smooth_x:smooth_x+smooth_size] *= 0.8  # Más liso
        
        return base_data
    
    def _add_subtle_salinity_patterns(self, base_data: np.ndarray) -> np.ndarray:
        """Añadir patrones de salinidad sutiles."""
        
        height, width = base_data.shape
        
        # Línea de drenaje sutil
        if width > 20:
            drain_x = width // 2 + np.random.randint(-2, 3)
            if drain_x + 1 < width:
                base_data[height//4:3*height//4, drain_x:drain_x+1] *= 0.7  # Menos salino
        
        return base_data
    
    def _add_subtle_seismic_anomalies(self, base_data: np.ndarray) -> np.ndarray:
        """Añadir anomalías sísmicas sutiles."""
        
        height, width = base_data.shape
        
        # Anomalía sísmica sutil (cavidad pequeña)
        if height > 12 and width > 12:
            anomaly_y = height // 2 + np.random.randint(-2, 3)
            anomaly_x = width // 2 + np.random.randint(-2, 3)
            anomaly_size = 4
            
            if (anomaly_y + anomaly_size < height and 
                anomaly_x + anomaly_size < width):
                base_data[anomaly_y:anomaly_y+anomaly_size, 
                         anomaly_x:anomaly_x+anomaly_size] *= 1.2  # Resonancia sutil
        
        return base_data
    
    def _generate_ndvi_with_archaeological_signatures(self, height: int, width: int) -> np.ndarray:
        """Generar NDVI con firmas arqueológicas típicas."""
        
        # Base de vegetación natural
        base_ndvi = np.random.normal(0.6, 0.15, (height, width))
        base_ndvi = np.clip(base_ndvi, 0.1, 0.9)
        
        # Añadir firmas arqueológicas
        
        # 1. Muros enterrados (vegetación débil en líneas)
        wall_y = height // 3
        wall_thickness = 3
        base_ndvi[wall_y:wall_y+wall_thickness, width//4:3*width//4] *= 0.6  # Vegetación débil
        
        # 2. Camino antiguo (vegetación vigorosa por mejor drenaje)
        road_x = width // 2
        road_width = 5
        base_ndvi[height//4:3*height//4, road_x:road_x+road_width] *= 1.3  # Vegetación vigorosa
        
        # 3. Estructura rectangular enterrada (patrón geométrico)
        struct_y1, struct_y2 = height//2, height//2 + 20
        struct_x1, struct_x2 = width//3, width//3 + 30
        base_ndvi[struct_y1:struct_y2, struct_x1:struct_x2] *= 0.7  # Vegetación moderadamente afectada
        
        # 4. Añadir ruido natural pero preservar patrones geométricos
        noise = np.random.normal(0, 0.05, (height, width))
        base_ndvi += noise
        
        return np.clip(base_ndvi, 0.0, 1.0)
    
    def _generate_thermal_with_buried_structures(self, height: int, width: int) -> np.ndarray:
        """Generar datos térmicos con patrones de estructuras enterradas."""
        
        # Temperatura base (variación natural)
        base_temp = np.random.normal(295, 5, (height, width))  # ~22°C base
        
        # Añadir gradiente topográfico natural
        y_gradient = np.linspace(-2, 2, height).reshape(-1, 1)
        base_temp += y_gradient
        
        # Firmas térmicas arqueológicas
        
        # 1. Fundación de piedra (alta inercia térmica - se enfría lento)
        foundation_y1, foundation_y2 = height//4, height//4 + 15
        foundation_x1, foundation_x2 = width//4, width//4 + 25
        base_temp[foundation_y1:foundation_y2, foundation_x1:foundation_x2] += 3  # Más caliente de noche
        
        # 2. Calzada compactada (respuesta térmica diferente)
        road_y = 2*height//3
        road_thickness = 4
        base_temp[road_y:road_y+road_thickness, width//6:5*width//6] += 1.5
        
        # 3. Zona de tierra removida (baja inercia térmica)
        disturbed_y1, disturbed_y2 = height//2, height//2 + 12
        disturbed_x1, disturbed_x2 = 2*width//3, 2*width//3 + 18
        base_temp[disturbed_y1:disturbed_y2, disturbed_x1:disturbed_x2] -= 2  # Se enfría rápido
        
        return base_temp
    
    def _generate_sar_with_geometric_anomalies(self, height: int, width: int) -> np.ndarray:
        """Generar backscatter SAR con anomalías geométricas."""
        
        # Backscatter base natural
        base_sar = np.random.normal(-12, 3, (height, width))  # dB típicos
        
        # Añadir textura natural
        from scipy import ndimage
        base_sar = ndimage.gaussian_filter(base_sar, sigma=1.5)
        
        # Anomalías geométricas arqueológicas
        
        # 1. Líneas rectas (caminos, muros) - alta reflectividad
        line_y = height // 2
        base_sar[line_y-1:line_y+2, width//5:4*width//5] += 8  # Línea brillante
        
        # 2. Patrón rectangular (estructura enterrada)
        rect_y1, rect_y2 = height//3, height//3 + 18
        rect_x1, rect_x2 = width//2, width//2 + 22
        base_sar[rect_y1:rect_y2, rect_x1:rect_x2] += 4  # Reflectividad moderada
        
        # 3. Intersección ortogonal (esquinas de estructuras)
        intersection_y, intersection_x = 2*height//3, width//3
        base_sar[intersection_y-2:intersection_y+3, intersection_x-10:intersection_x+11] += 6
        base_sar[intersection_y-10:intersection_y+11, intersection_x-2:intersection_x+3] += 6
        
        return base_sar
    
    def _generate_roughness_with_compaction(self, height: int, width: int) -> np.ndarray:
        """Generar rugosidad superficial con zonas compactadas."""
        
        # Rugosidad base natural
        base_roughness = np.random.exponential(0.3, (height, width))
        
        # Zonas compactadas (baja rugosidad)
        
        # 1. Camino compactado
        road_y1, road_y2 = height//4, height//4 + 6
        base_roughness[road_y1:road_y2, width//6:5*width//6] *= 0.3  # Muy liso
        
        # 2. Plaza o área ceremonial
        plaza_y1, plaza_y2 = 2*height//3, 2*height//3 + 25
        plaza_x1, plaza_x2 = width//3, width//3 + 30
        base_roughness[plaza_y1:plaza_y2, plaza_x1:plaza_x2] *= 0.4  # Compactado
        
        # 3. Bordes de estructuras (rugosidad intermedia)
        border_y = height // 2
        base_roughness[border_y-3:border_y+4, width//4:3*width//4] *= 0.7
        
        return base_roughness
    
    def _generate_salinity_with_drainage_patterns(self, height: int, width: int) -> np.ndarray:
        """Generar salinidad con patrones de drenaje anómalos."""
        
        # Salinidad base
        base_salinity = np.random.normal(0.5, 0.2, (height, width))
        base_salinity = np.clip(base_salinity, 0.1, 2.0)
        
        # Patrones de drenaje arqueológicos
        
        # 1. Canal de drenaje antiguo (baja salinidad)
        channel_x = width // 3
        channel_width = 4
        base_salinity[height//5:4*height//5, channel_x:channel_x+channel_width] *= 0.4
        
        # 2. Zona impermeabilizada (alta salinidad por acumulación)
        imperm_y1, imperm_y2 = height//2, height//2 + 20
        imperm_x1, imperm_x2 = 2*width//3, 2*width//3 + 25
        base_salinity[imperm_y1:imperm_y2, imperm_x1:imperm_x2] *= 1.8
        
        # 3. Red de drenaje ortogonal (patrón geométrico)
        # Líneas horizontales
        for y in [height//4, height//2, 3*height//4]:
            base_salinity[y-1:y+2, width//6:5*width//6] *= 0.6
        
        # Líneas verticales
        for x in [width//4, width//2, 3*width//4]:
            base_salinity[height//6:5*height//6, x-1:x+2] *= 0.6
        
        return base_salinity
    
    def _generate_seismic_with_cavities(self, height: int, width: int) -> np.ndarray:
        """Generar resonancia sísmica con indicios de cavidades."""
        
        # Resonancia base (suelo sólido)
        base_resonance = np.random.normal(1.0, 0.1, (height, width))
        
        # Anomalías sísmicas arqueológicas
        
        # 1. Cavidad subterránea (alta resonancia)
        cavity_y1, cavity_y2 = height//3, height//3 + 15
        cavity_x1, cavity_x2 = width//2, width//2 + 20
        base_resonance[cavity_y1:cavity_y2, cavity_x1:cavity_x2] *= 2.5  # Resonancia alta
        
        # 2. Túnel o galería (resonancia lineal)
        tunnel_y = 2*height//3
        tunnel_thickness = 3
        base_resonance[tunnel_y:tunnel_y+tunnel_thickness, width//4:3*width//4] *= 1.8
        
        # 3. Cimentación sólida (baja resonancia)
        foundation_y1, foundation_y2 = height//4, height//4 + 12
        foundation_x1, foundation_x2 = width//4, width//4 + 18
        base_resonance[foundation_y1:foundation_y2, foundation_x1:foundation_x2] *= 0.4
        
        return base_resonance
    
    def get_available_datasets(self, region_bounds: Dict[str, float]) -> List[str]:
        """
        Obtener lista de datasets disponibles para una región.
        
        Args:
            region_bounds: Límites geográficos de la región
            
        Returns:
            Lista de datasets arqueológicos disponibles (base + mejorados)
        """
        base_datasets = [
            'ndvi_vegetation',
            'thermal_lst', 
            'sar_backscatter',
            'surface_roughness',
            'soil_salinity',
            'seismic_resonance'
        ]
        
        enhanced_datasets = [
            'elevation_dem',           # OpenTopography
            'sar_l_band',             # ASF DAAC PALSAR
            'icesat2_profiles',       # ICESat-2 ATL08
            'vegetation_height',      # GEDI
            'soil_moisture',          # SMAP
            
            # NUEVAS CAPAS AVANZADAS PARA VISUALIZACIÓN IMPACTANTE
            'lidar_fullwave',         # LiDAR full-waveform
            'dem_multiscale',         # DEM multiescala fusionado
            'spectral_roughness',     # Rugosidad espectral (Fourier/Wavelets)
            'pseudo_lidar_ai',        # Pseudo-LiDAR por IA
            'multitemporal_topo'      # Topografía multitemporal
        ]
        
        return base_datasets + enhanced_datasets
    
    def validate_archaeological_data(self, data: xr.DataArray) -> Dict[str, Any]:
        """
        Validar calidad de datos arqueológicos.
        
        Args:
            data: DataArray a validar
            
        Returns:
            Reporte de validación
        """
        validation = {
            'valid': True,
            'issues': [],
            'quality_score': 1.0,
            'archaeological_potential': 'high'
        }
        
        # Verificar rango de valores
        if data.min() < 0 and data.attrs.get('data_type') == 'ndvi_vegetation':
            validation['issues'].append('NDVI values below 0 detected')
            validation['quality_score'] *= 0.9
        
        # Verificar patrones geométricos (indicativo de firmas arqueológicas)
        data_std = float(data.std())
        if data_std < 0.05:
            validation['issues'].append('Very low variation - may lack archaeological signatures')
            validation['archaeological_potential'] = 'low'
        elif data_std > 0.5:
            validation['issues'].append('Very high variation - may be too noisy')
            validation['quality_score'] *= 0.8
        
        # Verificar cobertura espacial
        if data.shape[0] < 50 or data.shape[1] < 50:
            validation['issues'].append('Low spatial resolution for archaeological analysis')
            validation['quality_score'] *= 0.7
        
        logger.info(f"Validación arqueológica: calidad={validation['quality_score']:.2f}, "
                   f"potencial={validation['archaeological_potential']}")
        
        return validation