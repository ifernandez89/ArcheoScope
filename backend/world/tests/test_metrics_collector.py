"""
Tests para WorldMetricsCollector
"""

import pytest
import numpy as np
from backend.world.metrics_collector import WorldMetricsCollector, WorldState


def create_test_world_state(
    entropy_level: str = "low"
) -> WorldState:
    """Crea estado de mundo para tests"""
    
    if entropy_level == "low":
        climate = {'temperature': 0.5, 'humidity': 0.5, 'pressure': 0.5}
        npcs = []
        anomalies = []
        velocity = (0.0, 0.0, 0.0)
        weather = 0.1
    elif entropy_level == "medium":
        climate = {'temperature': 0.6, 'humidity': 0.7, 'pressure': 0.4}
        npcs = [{'position': [10, 0, 10]}] * 3
        anomalies = [{'intensity': 0.5}]
        velocity = (2.0, 0.0, 2.0)
        weather = 0.5
    else:  # high
        climate = {'temperature': 0.9, 'humidity': 0.3, 'pressure': 0.8}
        npcs = [{'position': [i*5, 0, i*5]} for i in range(10)]
        anomalies = [{'intensity': 0.8}, {'intensity': 0.9}]
        velocity = (5.0, 0.0, 5.0)
        weather = 0.9
    
    return WorldState(
        player_position=(0.0, 0.0, 0.0),
        player_velocity=velocity,
        climate_state=climate,
        biome_type="desert",
        time_of_day=12.0,
        active_npcs=npcs,
        active_anomalies=anomalies,
        terrain_elevation=100.0,
        weather_intensity=weather
    )


class TestWorldMetricsCollector:
    """Tests para WorldMetricsCollector"""
    
    def test_initialization(self):
        """Test inicialización"""
        collector = WorldMetricsCollector()
        assert collector.history == []
        assert collector.max_history == 100
    
    def test_collect_low_entropy(self):
        """Test recopilación con baja entropía"""
        collector = WorldMetricsCollector()
        state = create_test_world_state("low")
        
        metrics = collector.collect(state)
        
        # Verificar que entropía es baja
        assert 0.0 <= metrics.world_entropy <= 0.4
        assert len(metrics.climate_vector) == 3
        assert metrics.npc_density < 0.3
        assert metrics.anomaly_score < 0.3
    
    def test_collect_high_entropy(self):
        """Test recopilación con alta entropía"""
        collector = WorldMetricsCollector()
        state = create_test_world_state("high")
        
        metrics = collector.collect(state)
        
        # Verificar que entropía es alta
        assert metrics.world_entropy > 0.5
        assert metrics.npc_density > 0.5
        assert metrics.anomaly_score > 0.5
        assert metrics.player_disruption > 0.3
    
    def test_climate_vector(self):
        """Test vector climático"""
        collector = WorldMetricsCollector()
        state = create_test_world_state("medium")
        
        metrics = collector.collect(state)
        
        # Verificar vector climático
        assert len(metrics.climate_vector) == 3
        assert all(0.0 <= v <= 1.0 for v in metrics.climate_vector)
    
    def test_npc_density(self):
        """Test densidad de NPCs"""
        collector = WorldMetricsCollector()
        
        # Sin NPCs
        state = create_test_world_state("low")
        metrics = collector.collect(state)
        assert metrics.npc_density == 0.0
        
        # Con NPCs
        state = create_test_world_state("high")
        metrics = collector.collect(state)
        assert metrics.npc_density > 0.0
    
    def test_anomaly_score(self):
        """Test score de anomalías"""
        collector = WorldMetricsCollector()
        
        # Sin anomalías
        state = create_test_world_state("low")
        metrics = collector.collect(state)
        assert metrics.anomaly_score == 0.0
        
        # Con anomalías
        state = create_test_world_state("high")
        metrics = collector.collect(state)
        assert metrics.anomaly_score > 0.5
    
    def test_temporal_drift(self):
        """Test deriva temporal"""
        collector = WorldMetricsCollector()
        
        # Primera medición
        state1 = create_test_world_state("low")
        metrics1 = collector.collect(state1)
        assert metrics1.temporal_drift == 0.0  # Sin historial
        
        # Segunda medición (cambio grande)
        state2 = create_test_world_state("high")
        metrics2 = collector.collect(state2)
        assert metrics2.temporal_drift > 0.0  # Hay cambio
    
    def test_history_management(self):
        """Test manejo de historial"""
        collector = WorldMetricsCollector()
        collector.max_history = 5
        
        # Agregar más métricas que el máximo
        for i in range(10):
            state = create_test_world_state("low")
            collector.collect(state)
        
        # Verificar que solo se guardan las últimas 5
        assert len(collector.history) == 5
    
    def test_history_summary(self):
        """Test resumen de historial"""
        collector = WorldMetricsCollector()
        
        # Sin historial
        summary = collector.get_history_summary()
        assert summary == {}
        
        # Con historial
        for i in range(5):
            state = create_test_world_state("medium")
            collector.collect(state)
        
        summary = collector.get_history_summary()
        assert 'avg_entropy' in summary
        assert 'max_entropy' in summary
        assert 'avg_anomaly' in summary
        assert 'trend' in summary
    
    def test_metrics_bounds(self):
        """Test que todas las métricas están en rango 0-1"""
        collector = WorldMetricsCollector()
        
        # Probar con diferentes estados
        for entropy_level in ["low", "medium", "high"]:
            state = create_test_world_state(entropy_level)
            metrics = collector.collect(state)
            
            # Verificar bounds
            assert 0.0 <= metrics.world_entropy <= 1.0
            assert 0.0 <= metrics.npc_density <= 1.0
            assert 0.0 <= metrics.energy_flux <= 1.0
            assert 0.0 <= metrics.player_disruption <= 1.0
            assert 0.0 <= metrics.anomaly_score <= 1.0
            assert 0.0 <= metrics.temporal_drift <= 1.0
            assert 0.0 <= metrics.spatial_coherence <= 1.0
            assert all(0.0 <= v <= 1.0 for v in metrics.climate_vector)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
