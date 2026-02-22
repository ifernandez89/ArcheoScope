"""
Field System - Campo Base + Campo Dinámico

Arquitectura de 2 capas:
- Campo Base: Determinista, siempre igual para mismas coords/fecha
- Campo Dinámico: Evolutivo, con memoria acumulativa ligera

Author: Kiro AI Assistant
Date: 22 Feb 2026
"""

import numpy as np
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BaseField:
    """
    Campo Base - SIEMPRE determinista
    
    Se calcula desde:
    - Coordenadas + radio
    - DEM (elevación)
    - Posición solar
    - Fecha/hora
    
    → Discretización 8x8 → tokens 0-5
    
    Este campo:
    - Siempre será igual para mismas coords y fecha/hora
    - No se guarda
    - Se recalcula cada vez
    - Es el "estado físico estructural"
    """
    
    def __init__(self):
        self.grid_size = 8  # 8x8 = 64 celdas
    
    def compute(
        self,
        lat: float,
        lon: float,
        radius_km: float,
        dem_data: Optional[np.ndarray] = None,
        timestamp: Optional[datetime] = None
    ) -> np.ndarray:
        """
        Calcula campo base determinista
        
        Returns:
            np.ndarray: Array 8x8 con valores 0-5
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Inicializar grid
        field = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        
        # 1. Componente geográfica (lat/lon)
        geo_component = self._compute_geographic_component(lat, lon)
        
        # 2. Componente topográfica (DEM)
        topo_component = self._compute_topographic_component(dem_data) if dem_data is not None else 0
        
        # 3. Componente solar (posición del sol)
        solar_component = self._compute_solar_component(lat, lon, timestamp)
        
        # 4. Componente temporal (hora del día, estación)
        temporal_component = self._compute_temporal_component(timestamp)
        
        # Combinar componentes
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Índice normalizado (0-1)
                ni = i / self.grid_size
                nj = j / self.grid_size
                
                # Combinar componentes con pesos
                value = (
                    geo_component * 0.3 +
                    topo_component * 0.3 +
                    solar_component * 0.2 +
                    temporal_component * 0.2
                )
                
                # Añadir variación espacial determinista
                spatial_hash = self._spatial_hash(lat, lon, i, j)
                value += spatial_hash * 0.1
                
                # Discretizar a 0-5
                field[i, j] = int(np.clip(value * 6, 0, 5))
        
        return field
    
    def _compute_geographic_component(self, lat: float, lon: float) -> float:
        """Componente basada en coordenadas geográficas"""
        # Latitud: más cerca del ecuador = más energía
        lat_factor = 1.0 - abs(lat) / 90.0
        
        # Longitud: patrón sinusoidal
        lon_factor = (np.sin(np.radians(lon)) + 1) / 2
        
        return (lat_factor + lon_factor) / 2
    
    def _compute_topographic_component(self, dem_data: np.ndarray) -> float:
        """Componente basada en elevación"""
        if dem_data is None or dem_data.size == 0:
            return 0.5
        
        # Normalizar elevación
        elevation_mean = np.mean(dem_data)
        elevation_std = np.std(dem_data)
        
        # Más variación topográfica = más energía
        return np.clip(elevation_std / 1000.0, 0, 1)
    
    def _compute_solar_component(self, lat: float, lon: float, timestamp: datetime) -> float:
        """Componente basada en posición solar"""
        # Calcular ángulo solar simplificado
        day_of_year = timestamp.timetuple().tm_yday
        hour = timestamp.hour + timestamp.minute / 60.0
        
        # Declinación solar
        declination = 23.45 * np.sin(np.radians((360 / 365) * (day_of_year - 81)))
        
        # Ángulo horario
        hour_angle = 15 * (hour - 12)
        
        # Altura solar
        altitude = np.arcsin(
            np.sin(np.radians(lat)) * np.sin(np.radians(declination)) +
            np.cos(np.radians(lat)) * np.cos(np.radians(declination)) * np.cos(np.radians(hour_angle))
        )
        
        # Normalizar (0 = noche, 1 = mediodía)
        return np.clip((np.degrees(altitude) + 90) / 180, 0, 1)
    
    def _compute_temporal_component(self, timestamp: datetime) -> float:
        """Componente basada en tiempo"""
        # Hora del día (0-1)
        hour_factor = timestamp.hour / 24.0
        
        # Día del año (estación)
        day_of_year = timestamp.timetuple().tm_yday
        season_factor = (np.sin(2 * np.pi * day_of_year / 365) + 1) / 2
        
        return (hour_factor + season_factor) / 2
    
    def _spatial_hash(self, lat: float, lon: float, i: int, j: int) -> float:
        """Hash espacial determinista para variación local"""
        # Crear hash determinista basado en coordenadas y posición en grid
        hash_input = f"{lat:.4f}_{lon:.4f}_{i}_{j}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest()[:8], 16)
        
        # Normalizar a 0-1
        return (hash_value % 1000) / 1000.0


class DynamicField:
    """
    Campo Dinámico - Evolutivo con memoria
    
    Se guarda en: /world_cache/{lat_lon_hash}.json
    
    Contiene:
    - energy_modifier: [64 valores 0-5]
    - last_update: timestamp
    - weather_bias: acumulación de clima
    - instability_score: nivel de inestabilidad
    - interaction_count: número de interacciones
    
    Este campo:
    - Cambia por acciones del usuario
    - Cambia por clima activado
    - Evoluciona con HRM
    - Tiene memoria acumulativa
    """
    
    def __init__(self, cache_dir: str = 'backend/world_cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.grid_size = 8
    
    def load(self, lat: float, lon: float) -> Dict:
        """
        Carga campo dinámico desde caché
        
        Si no existe, crea uno nuevo (ceros)
        """
        tile_id = self._generate_tile_id(lat, lon)
        cache_file = self.cache_dir / f"{tile_id}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                
                logger.info(f"✅ Dynamic field loaded: {tile_id}")
                return data
            except Exception as e:
                logger.error(f"Error loading dynamic field: {e}")
        
        # Crear campo nuevo (ceros)
        return self._create_empty_field()
    
    def save(self, lat: float, lon: float, field_data: Dict) -> None:
        """Guarda campo dinámico en caché"""
        tile_id = self._generate_tile_id(lat, lon)
        cache_file = self.cache_dir / f"{tile_id}.json"
        
        try:
            # Actualizar timestamp
            field_data['last_update'] = datetime.now().isoformat()
            
            with open(cache_file, 'w') as f:
                json.dump(field_data, f, indent=2)
            
            logger.info(f"💾 Dynamic field saved: {tile_id}")
        except Exception as e:
            logger.error(f"Error saving dynamic field: {e}")
    
    def evolve_offline(self, field_data: Dict, current_time: datetime) -> Dict:
        """
        Evoluciona el campo según tiempo transcurrido
        
        Simula evolución offline (cuando el usuario no estaba)
        """
        last_update = datetime.fromisoformat(field_data['last_update'])
        dt = (current_time - last_update).total_seconds() / 3600  # horas
        
        if dt < 1:
            return field_data  # Menos de 1 hora, no evolucionar
        
        # Calcular número de ciclos HRM a simular
        # 1 ciclo por cada 6 horas
        cycles = int(dt / 6)
        cycles = min(cycles, 10)  # Máximo 10 ciclos (60 horas)
        
        if cycles > 0:
            logger.info(f"⏰ Evolving field offline: {cycles} cycles ({dt:.1f} hours)")
            
            # Simular decaimiento natural
            energy_modifier = np.array(field_data['energy_modifier']).reshape(8, 8)
            
            for _ in range(cycles):
                # Decaimiento exponencial hacia 0
                energy_modifier = energy_modifier * 0.9
                
                # Difusión espacial (suavizado)
                energy_modifier = self._spatial_diffusion(energy_modifier)
            
            field_data['energy_modifier'] = energy_modifier.flatten().tolist()
            field_data['instability_score'] *= 0.8  # Reducir inestabilidad
        
        return field_data
    
    def apply_weather_perturbation(
        self,
        field_data: Dict,
        weather_type: str,
        intensity: float = 1.0
    ) -> Dict:
        """
        Aplica perturbación climática al campo dinámico
        
        No cambia directamente el mundo, modifica el dynamic_field
        """
        energy_modifier = np.array(field_data['energy_modifier']).reshape(8, 8)
        
        if weather_type == 'rain':
            # Añadir ruido en celdas cerca de agua (bordes)
            for i in range(8):
                for j in range(8):
                    if i == 0 or i == 7 or j == 0 or j == 7:
                        energy_modifier[i, j] += np.random.randint(0, 2) * intensity
        
        elif weather_type == 'storm':
            # Aumentar inestabilidad en clusters
            center_i, center_j = np.random.randint(2, 6, size=2)
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    i, j = center_i + di, center_j + dj
                    if 0 <= i < 8 and 0 <= j < 8:
                        energy_modifier[i, j] += np.random.randint(1, 3) * intensity
            
            field_data['instability_score'] += 0.1 * intensity
        
        elif weather_type == 'wind':
            # Desplazamiento direccional
            energy_modifier = np.roll(energy_modifier, 1, axis=1)
        
        # Actualizar bias climático
        field_data['weather_bias'] += 1
        
        # Clamp a 0-5
        energy_modifier = np.clip(energy_modifier, 0, 5)
        field_data['energy_modifier'] = energy_modifier.flatten().tolist()
        
        logger.info(f"🌩️ Weather perturbation applied: {weather_type} (intensity={intensity})")
        
        return field_data
    
    def apply_user_interaction(self, field_data: Dict, cell_i: int, cell_j: int, delta: int) -> Dict:
        """Aplica interacción del usuario en una celda específica"""
        energy_modifier = np.array(field_data['energy_modifier']).reshape(8, 8)
        
        # Modificar celda
        energy_modifier[cell_i, cell_j] += delta
        energy_modifier = np.clip(energy_modifier, 0, 5)
        
        # Incrementar contador de interacciones
        field_data['interaction_count'] += 1
        field_data['energy_modifier'] = energy_modifier.flatten().tolist()
        
        logger.info(f"👆 User interaction: cell ({cell_i},{cell_j}) delta={delta}")
        
        return field_data
    
    def _create_empty_field(self) -> Dict:
        """Crea campo dinámico vacío (ceros)"""
        return {
            'energy_modifier': [0] * 64,  # 8x8 = 64 celdas
            'last_update': datetime.now().isoformat(),
            'weather_bias': 0,
            'instability_score': 0.0,
            'interaction_count': 0
        }
    
    def _generate_tile_id(self, lat: float, lon: float) -> str:
        """Genera ID único para tile (lat_lon redondeado a 4 decimales)"""
        return f"{lat:.4f}_{lon:.4f}"
    
    def _spatial_diffusion(self, field: np.ndarray) -> np.ndarray:
        """Aplica difusión espacial (suavizado)"""
        from scipy.ndimage import gaussian_filter
        return gaussian_filter(field, sigma=0.5)
    
    def cleanup_old_tiles(self, days: int = 30) -> int:
        """
        Limpia tiles no usados en X días
        
        Returns:
            int: Número de tiles eliminados
        """
        cutoff = datetime.now() - timedelta(days=days)
        deleted = 0
        
        for cache_file in self.cache_dir.glob('*.json'):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                
                last_update = datetime.fromisoformat(data['last_update'])
                
                if last_update < cutoff:
                    cache_file.unlink()
                    deleted += 1
            except Exception as e:
                logger.error(f"Error cleaning up {cache_file}: {e}")
        
        logger.info(f"🗑️ Cleaned up {deleted} old tiles (>{days} days)")
        return deleted


class FieldCombiner:
    """
    Combina Campo Base + Campo Dinámico
    
    combined_state = base_field + dynamic_field
    combined_state = clamp_0_5(combined_state)
    """
    
    @staticmethod
    def combine(base_field: np.ndarray, dynamic_field_data: Dict) -> np.ndarray:
        """
        Combina campos base y dinámico
        
        Returns:
            np.ndarray: Campo combinado 8x8 con valores 0-5
        """
        # Convertir dynamic field a array
        dynamic_modifier = np.array(dynamic_field_data['energy_modifier']).reshape(8, 8)
        
        # Combinar
        combined = base_field + dynamic_modifier
        
        # Clamp a 0-5
        combined = np.clip(combined, 0, 5).astype(np.int32)
        
        return combined
    
    @staticmethod
    def to_sequence(field: np.ndarray) -> List[int]:
        """Convierte campo 8x8 a secuencia de 64 tokens"""
        return field.flatten().tolist()


# Instancias globales
base_field_system = BaseField()
dynamic_field_system = DynamicField()
field_combiner = FieldCombiner()
