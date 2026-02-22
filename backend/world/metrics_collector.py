"""
WorldMetricsCollector - Recopila métricas continuas del mundo 3D
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class WorldState:
    """Estado actual del mundo"""
    player_position: Tuple[float, float, float]
    player_velocity: Tuple[float, float, float]
    climate_state: Dict[str, float]  # temp, humidity, pressure
    biome_type: str
    time_of_day: float  # 0-24
    active_npcs: List[Dict]
    active_anomalies: List[Dict]
    terrain_elevation: float
    weather_intensity: float
    
    
@dataclass
class WorldMetrics:
    """Métricas continuas del mundo (0-1)"""
    world_entropy: float  # Entropía acumulativa
    climate_vector: List[float]  # [temp, humidity, pressure]
    npc_density: float  # Densidad de NPCs
    energy_flux: float  # Flujo de energía
    player_disruption: float  # Impacto del jugador
    anomaly_score: float  # Score de anomalías
    temporal_drift: float  # Deriva temporal
    spatial_coherence: float  # Coherencia espacial


class WorldMetricsCollector:
    """
    Recopila y normaliza métricas del mundo 3D
    
    Convierte estado complejo del mundo en métricas continuas 0-1
    que luego serán simbolizadas para el HRM.
    """
    
    def __init__(self):
        self.history: List[WorldMetrics] = []
        self.max_history = 100
        
    def collect(self, world_state: WorldState) -> WorldMetrics:
        """
        Recopila métricas del estado actual del mundo
        
        Args:
            world_state: Estado actual del mundo
            
        Returns:
            WorldMetrics con valores normalizados 0-1
        """
        metrics = WorldMetrics(
            world_entropy=self.calculate_entropy(world_state),
            climate_vector=self.get_climate_vector(world_state),
            npc_density=self.calculate_npc_density(world_state),
            energy_flux=self.calculate_energy_flux(world_state),
            player_disruption=self.calculate_player_impact(world_state),
            anomaly_score=self.calculate_anomaly_score(world_state),
            temporal_drift=self.calculate_temporal_drift(world_state),
            spatial_coherence=self.calculate_spatial_coherence(world_state)
        )
        
        # Guardar en historial
        self.history.append(metrics)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        return metrics
    
    def calculate_entropy(self, state: WorldState) -> float:
        """
        Calcula entropía del mundo (0-1)
        
        Factores:
        - Variabilidad climática
        - Actividad de NPCs
        - Anomalías activas
        - Velocidad del jugador
        """
        # Entropía climática
        climate_entropy = np.std([
            state.climate_state.get('temperature', 0.5),
            state.climate_state.get('humidity', 0.5),
            state.climate_state.get('pressure', 0.5)
        ])
        
        # Entropía de actividad
        npc_entropy = min(1.0, len(state.active_npcs) / 10.0)
        anomaly_entropy = min(1.0, len(state.active_anomalies) / 5.0)
        
        # Entropía de movimiento
        velocity_magnitude = np.linalg.norm(state.player_velocity)
        movement_entropy = min(1.0, velocity_magnitude / 10.0)
        
        # Combinar (promedio ponderado)
        total_entropy = (
            climate_entropy * 0.3 +
            npc_entropy * 0.2 +
            anomaly_entropy * 0.3 +
            movement_entropy * 0.2
        )
        
        return float(np.clip(total_entropy, 0.0, 1.0))
    
    def get_climate_vector(self, state: WorldState) -> List[float]:
        """
        Vector climático normalizado [temp, humidity, pressure]
        """
        return [
            state.climate_state.get('temperature', 0.5),
            state.climate_state.get('humidity', 0.5),
            state.climate_state.get('pressure', 0.5)
        ]
    
    def calculate_npc_density(self, state: WorldState) -> float:
        """
        Densidad de NPCs en área cercana (0-1)
        """
        # Contar NPCs en radio de 50 unidades
        nearby_npcs = 0
        player_pos = np.array(state.player_position)
        
        for npc in state.active_npcs:
            npc_pos = np.array(npc.get('position', [0, 0, 0]))
            distance = np.linalg.norm(player_pos - npc_pos)
            if distance < 50:
                nearby_npcs += 1
        
        # Normalizar (máximo 10 NPCs cercanos)
        return min(1.0, nearby_npcs / 10.0)
    
    def calculate_energy_flux(self, state: WorldState) -> float:
        """
        Flujo de energía del mundo (0-1)
        
        Combina:
        - Intensidad climática
        - Anomalías activas
        - Hora del día
        """
        # Energía climática
        climate_energy = state.weather_intensity
        
        # Energía de anomalías
        anomaly_energy = min(1.0, len(state.active_anomalies) / 5.0)
        
        # Energía temporal (más alta al amanecer/atardecer)
        time_factor = abs(np.sin(state.time_of_day * np.pi / 12))
        
        # Combinar
        total_energy = (
            climate_energy * 0.4 +
            anomaly_energy * 0.4 +
            time_factor * 0.2
        )
        
        return float(np.clip(total_energy, 0.0, 1.0))
    
    def calculate_player_impact(self, state: WorldState) -> float:
        """
        Impacto del jugador en el mundo (0-1)
        
        Basado en:
        - Velocidad de movimiento
        - Interacciones recientes
        - Distancia recorrida
        """
        # Velocidad actual
        velocity_magnitude = np.linalg.norm(state.player_velocity)
        velocity_impact = min(1.0, velocity_magnitude / 10.0)
        
        # TODO: Agregar historial de interacciones
        interaction_impact = 0.0
        
        # Combinar
        total_impact = velocity_impact * 0.7 + interaction_impact * 0.3
        
        return float(np.clip(total_impact, 0.0, 1.0))
    
    def calculate_anomaly_score(self, state: WorldState) -> float:
        """
        Score de anomalías activas (0-1)
        """
        if not state.active_anomalies:
            return 0.0
        
        # Sumar intensidades de anomalías
        total_intensity = sum(
            anomaly.get('intensity', 0.5) 
            for anomaly in state.active_anomalies
        )
        
        # Normalizar
        return min(1.0, total_intensity / 3.0)
    
    def calculate_temporal_drift(self, state: WorldState) -> float:
        """
        Deriva temporal (0-1)
        
        Mide qué tan rápido cambia el mundo
        """
        if len(self.history) < 2:
            return 0.0
        
        # Comparar con estado anterior
        prev_metrics = self.history[-1]
        
        # Calcular diferencias
        entropy_diff = abs(prev_metrics.world_entropy - self.calculate_entropy(state))
        energy_diff = abs(prev_metrics.energy_flux - self.calculate_energy_flux(state))
        
        # Promedio de cambios
        drift = (entropy_diff + energy_diff) / 2.0
        
        return float(np.clip(drift, 0.0, 1.0))
    
    def calculate_spatial_coherence(self, state: WorldState) -> float:
        """
        Coherencia espacial (0-1)
        
        Mide qué tan "ordenado" está el mundo
        """
        # Coherencia climática (variación baja = alta coherencia)
        climate_variance = np.var(self.get_climate_vector(state))
        climate_coherence = 1.0 - min(1.0, climate_variance * 4.0)
        
        # Coherencia de NPCs (distribución uniforme = alta coherencia)
        npc_coherence = 1.0 - self.calculate_npc_density(state)
        
        # Combinar
        total_coherence = (climate_coherence + npc_coherence) / 2.0
        
        return float(np.clip(total_coherence, 0.0, 1.0))
    
    def get_history_summary(self) -> Dict:
        """
        Resumen del historial de métricas
        """
        if not self.history:
            return {}
        
        return {
            'avg_entropy': np.mean([m.world_entropy for m in self.history]),
            'max_entropy': np.max([m.world_entropy for m in self.history]),
            'avg_anomaly': np.mean([m.anomaly_score for m in self.history]),
            'trend': 'increasing' if self.history[-1].world_entropy > self.history[0].world_entropy else 'decreasing'
        }
