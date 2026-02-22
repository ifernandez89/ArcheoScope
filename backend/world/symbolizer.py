"""
WorldSymbolizer - Convierte métricas continuas en secuencia discreta 0-5

Reinterpreta los 6 tokens del checkpoint Maze para representar dinámica del mundo:
0 = ESTABLE
1 = TENSIÓN LEVE
2 = TENSIÓN MEDIA
3 = INESTABILIDAD ACTIVA
4 = ANOMALÍA
5 = TRANSICIÓN / COLAPSO
"""

from typing import List, Dict, Tuple
import numpy as np
from .metrics_collector import WorldMetrics


class WorldSymbolizer:
    """
    Convierte métricas continuas del mundo en secuencia discreta de 64 tokens (0-5)
    
    El mundo se divide en 64 zonas conceptuales:
    - Zona 0-7: Región Norte
    - Zona 8-15: Región Este
    - Zona 16-23: Región Sur
    - Zona 24-31: Región Oeste
    - Zona 32-39: Región Central
    - Zona 40-47: Región Subterránea
    - Zona 48-55: Región Atmosférica
    - Zona 56-63: Región Temporal
    """
    
    # Definición de estados
    STABLE = 0
    TENSION_LOW = 1
    TENSION_MEDIUM = 2
    INSTABILITY = 3
    ANOMALY = 4
    TRANSITION = 5
    
    def __init__(self, zones: int = 64):
        self.zones = zones
        self.zone_history: Dict[int, List[int]] = {i: [] for i in range(zones)}
        self.max_history = 10
        
    def symbolize(self, metrics: WorldMetrics, player_zone: int = 32) -> List[int]:
        """
        Convierte métricas continuas en secuencia de 64 tokens (0-5)
        
        Args:
            metrics: Métricas del mundo
            player_zone: Zona donde está el jugador (0-63)
            
        Returns:
            Lista de 64 tokens (0-5)
        """
        sequence = []
        
        for zone_id in range(self.zones):
            # Calcular estado de la zona
            zone_state = self.calculate_zone_state(
                metrics, 
                zone_id, 
                player_zone
            )
            
            # Guardar en historial
            self.zone_history[zone_id].append(zone_state)
            if len(self.zone_history[zone_id]) > self.max_history:
                self.zone_history[zone_id].pop(0)
            
            sequence.append(zone_state)
        
        return sequence
    
    def calculate_zone_state(
        self, 
        metrics: WorldMetrics, 
        zone_id: int, 
        player_zone: int
    ) -> int:
        """
        Calcula estado de una zona específica (0-5)
        
        Factores:
        - Entropía global
        - Anomalías
        - Distancia al jugador
        - Clima
        - Historial de la zona
        """
        # Calcular factores base
        zone_entropy = self.get_zone_entropy(metrics, zone_id, player_zone)
        zone_anomaly = self.get_zone_anomaly(metrics, zone_id)
        zone_climate = self.get_zone_climate(metrics, zone_id)
        zone_temporal = self.get_zone_temporal(metrics, zone_id)
        
        # Clasificar en 0-5
        return self.classify_zone_state(
            zone_entropy,
            zone_anomaly,
            zone_climate,
            zone_temporal
        )
    
    def get_zone_entropy(
        self, 
        metrics: WorldMetrics, 
        zone_id: int, 
        player_zone: int
    ) -> float:
        """
        Entropía de la zona (0-1)
        
        Más alta cerca del jugador y en zonas con historial inestable
        """
        # Entropía base del mundo
        base_entropy = metrics.world_entropy
        
        # Factor de distancia al jugador
        distance_factor = self.calculate_zone_distance(zone_id, player_zone)
        player_influence = metrics.player_disruption * (1.0 - distance_factor)
        
        # Factor de historial
        history_factor = self.calculate_history_instability(zone_id)
        
        # Combinar
        zone_entropy = (
            base_entropy * 0.4 +
            player_influence * 0.3 +
            history_factor * 0.3
        )
        
        return float(np.clip(zone_entropy, 0.0, 1.0))
    
    def get_zone_anomaly(self, metrics: WorldMetrics, zone_id: int) -> float:
        """
        Score de anomalía de la zona (0-1)
        
        Más alto en zonas atmosféricas y temporales
        """
        # Anomalía base
        base_anomaly = metrics.anomaly_score
        
        # Factor de tipo de zona
        zone_type_factor = self.get_zone_type_factor(zone_id)
        
        # Combinar
        zone_anomaly = base_anomaly * zone_type_factor
        
        return float(np.clip(zone_anomaly, 0.0, 1.0))
    
    def get_zone_climate(self, metrics: WorldMetrics, zone_id: int) -> float:
        """
        Intensidad climática de la zona (0-1)
        
        Más alta en zonas atmosféricas
        """
        # Clima base
        climate_intensity = np.mean(metrics.climate_vector)
        
        # Factor de zona atmosférica (48-55)
        if 48 <= zone_id <= 55:
            climate_intensity *= 1.5
        
        return float(np.clip(climate_intensity, 0.0, 1.0))
    
    def get_zone_temporal(self, metrics: WorldMetrics, zone_id: int) -> float:
        """
        Deriva temporal de la zona (0-1)
        
        Más alta en zonas temporales (56-63)
        """
        # Deriva base
        temporal_drift = metrics.temporal_drift
        
        # Factor de zona temporal
        if 56 <= zone_id <= 63:
            temporal_drift *= 1.5
        
        return float(np.clip(temporal_drift, 0.0, 1.0))
    
    def classify_zone_state(
        self,
        entropy: float,
        anomaly: float,
        climate: float,
        temporal: float
    ) -> int:
        """
        Clasifica estado de la zona en 0-5
        
        Lógica de clasificación:
        - ESTABLE (0): Baja entropía, sin anomalías
        - TENSIÓN LEVE (1): Entropía moderada
        - TENSIÓN MEDIA (2): Entropía alta o clima inestable
        - INESTABILIDAD (3): Entropía muy alta o anomalías detectables
        - ANOMALÍA (4): Anomalías fuertes
        - TRANSICIÓN (5): Deriva temporal alta o cambio de estado
        """
        # Calcular score combinado
        combined_score = (
            entropy * 0.4 +
            anomaly * 0.3 +
            climate * 0.2 +
            temporal * 0.1
        )
        
        # Clasificar
        if anomaly > 0.8:
            return self.ANOMALY  # 4
        elif temporal > 0.7:
            return self.TRANSITION  # 5
        elif combined_score < 0.3:
            return self.STABLE  # 0
        elif combined_score < 0.5:
            return self.TENSION_LOW  # 1
        elif combined_score < 0.7:
            return self.TENSION_MEDIUM  # 2
        else:
            return self.INSTABILITY  # 3
    
    def calculate_zone_distance(self, zone_a: int, zone_b: int) -> float:
        """
        Calcula distancia normalizada entre dos zonas (0-1)
        
        Zonas se organizan en regiones de 8 zonas cada una
        """
        region_a = zone_a // 8
        region_b = zone_b // 8
        
        # Distancia entre regiones
        region_distance = abs(region_a - region_b)
        
        # Normalizar (máximo 7 regiones de distancia)
        return min(1.0, region_distance / 7.0)
    
    def get_zone_type_factor(self, zone_id: int) -> float:
        """
        Factor de tipo de zona para anomalías
        
        Zonas atmosféricas y temporales tienen más anomalías
        """
        if 48 <= zone_id <= 55:  # Atmosférica
            return 1.3
        elif 56 <= zone_id <= 63:  # Temporal
            return 1.5
        elif 40 <= zone_id <= 47:  # Subterránea
            return 1.2
        else:
            return 1.0
    
    def calculate_history_instability(self, zone_id: int) -> float:
        """
        Calcula inestabilidad basada en historial de la zona (0-1)
        
        Zonas con cambios frecuentes tienen mayor inestabilidad
        """
        history = self.zone_history[zone_id]
        
        if len(history) < 2:
            return 0.0
        
        # Contar cambios de estado
        changes = sum(
            1 for i in range(len(history) - 1)
            if history[i] != history[i + 1]
        )
        
        # Normalizar
        instability = changes / (len(history) - 1)
        
        return float(np.clip(instability, 0.0, 1.0))
    
    def get_zone_region_name(self, zone_id: int) -> str:
        """
        Obtiene nombre de la región de la zona
        """
        if 0 <= zone_id <= 7:
            return "Norte"
        elif 8 <= zone_id <= 15:
            return "Este"
        elif 16 <= zone_id <= 23:
            return "Sur"
        elif 24 <= zone_id <= 31:
            return "Oeste"
        elif 32 <= zone_id <= 39:
            return "Central"
        elif 40 <= zone_id <= 47:
            return "Subterránea"
        elif 48 <= zone_id <= 55:
            return "Atmosférica"
        elif 56 <= zone_id <= 63:
            return "Temporal"
        else:
            return "Desconocida"
    
    def get_state_name(self, state: int) -> str:
        """
        Obtiene nombre del estado
        """
        names = {
            0: "ESTABLE",
            1: "TENSIÓN LEVE",
            2: "TENSIÓN MEDIA",
            3: "INESTABILIDAD",
            4: "ANOMALÍA",
            5: "TRANSICIÓN"
        }
        return names.get(state, "DESCONOCIDO")
    
    def visualize_sequence(self, sequence: List[int]) -> str:
        """
        Visualiza secuencia simbólica en formato legible
        """
        lines = []
        lines.append("=" * 60)
        lines.append("ESTADO SIMBÓLICO DEL MUNDO (64 zonas)")
        lines.append("=" * 60)
        
        for region_start in range(0, 64, 8):
            region_end = region_start + 8
            region_name = self.get_zone_region_name(region_start)
            region_states = sequence[region_start:region_end]
            
            # Visualizar región
            state_str = " ".join(str(s) for s in region_states)
            lines.append(f"{region_name:15} [{state_str}]")
        
        lines.append("=" * 60)
        
        # Estadísticas
        state_counts = {i: sequence.count(i) for i in range(6)}
        lines.append("\nDistribución de estados:")
        for state, count in state_counts.items():
            percentage = (count / 64) * 100
            lines.append(f"  {self.get_state_name(state):20} {count:2} ({percentage:5.1f}%)")
        
        return "\n".join(lines)
