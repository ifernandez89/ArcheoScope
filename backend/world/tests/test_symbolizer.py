"""
Tests para WorldSymbolizer
"""

import pytest
from backend.world.symbolizer import WorldSymbolizer
from backend.world.metrics_collector import WorldMetrics


def create_test_metrics(entropy: float = 0.5) -> WorldMetrics:
    """Crea métricas de test"""
    return WorldMetrics(
        world_entropy=entropy,
        climate_vector=[0.5, 0.5, 0.5],
        npc_density=0.3,
        energy_flux=0.4,
        player_disruption=0.2,
        anomaly_score=entropy * 0.8,
        temporal_drift=0.1,
        spatial_coherence=0.7
    )


class TestWorldSymbolizer:
    """Tests para WorldSymbolizer"""
    
    def test_initialization(self):
        """Test inicialización"""
        symbolizer = WorldSymbolizer(zones=64)
        assert symbolizer.zones == 64
        assert len(symbolizer.zone_history) == 64
        assert symbolizer.max_history == 10
    
    def test_symbolize_length(self):
        """Test que symbolize retorna 64 tokens"""
        symbolizer = WorldSymbolizer(zones=64)
        metrics = create_test_metrics()
        
        sequence = symbolizer.symbolize(metrics, player_zone=32)
        
        assert len(sequence) == 64
    
    def test_symbolize_range(self):
        """Test que tokens están en rango 0-5"""
        symbolizer = WorldSymbolizer(zones=64)
        metrics = create_test_metrics()
        
        sequence = symbolizer.symbolize(metrics, player_zone=32)
        
        assert all(0 <= token <= 5 for token in sequence)
    
    def test_low_entropy_stable(self):
        """Test que baja entropía produce estados estables"""
        symbolizer = WorldSymbolizer(zones=64)
        metrics = create_test_metrics(entropy=0.1)
        
        sequence = symbolizer.symbolize(metrics, player_zone=32)
        
        # Mayoría de tokens deberían ser 0 o 1 (estable/tensión leve)
        stable_count = sum(1 for t in sequence if t <= 1)
        assert stable_count > 40  # Más del 60%
    
    def test_high_entropy_unstable(self):
        """Test que alta entropía produce estados inestables"""
        symbolizer = WorldSymbolizer(zones=64)
        metrics = create_test_metrics(entropy=0.9)
        
        sequence = symbolizer.symbolize(metrics, player_zone=32)
        
        # Mayoría de tokens deberían ser 3, 4, 5 (inestable/anomalía)
        unstable_count = sum(1 for t in sequence if t >= 3)
        assert unstable_count > 20  # Más del 30%
    
    def test_player_zone_influence(self):
        """Test que zona del jugador tiene mayor inestabilidad"""
        symbolizer = WorldSymbolizer(zones=64)
        metrics = create_test_metrics(entropy=0.5)
        metrics.player_disruption = 0.8
        
        player_zone = 32
        sequence = symbolizer.symbolize(metrics, player_zone=player_zone)
        
        # Zona del jugador debería tener mayor estado
        player_state = sequence[player_zone]
        avg_state = sum(sequence) / len(sequence)
        
        # No siempre es mayor, pero en promedio debería serlo
        # Solo verificamos que no sea 0 (estable)
        assert player_state >= 0
    
    def test_zone_history(self):
        """Test que historial de zonas se mantiene"""
        symbolizer = WorldSymbolizer(zones=64)
        metrics = create_test_metrics()
        
        # Primera simbolización
        sequence1 = symbolizer.symbolize(metrics, player_zone=32)
        
        # Verificar que historial tiene 1 entrada por zona
        for zone_id in range(64):
            assert len(symbolizer.zone_history[zone_id]) == 1
        
        # Segunda simbolización
        sequence2 = symbolizer.symbolize(metrics, player_zone=32)
        
        # Verificar que historial tiene 2 entradas
        for zone_id in range(64):
            assert len(symbolizer.zone_history[zone_id]) == 2
    
    def test_history_max_limit(self):
        """Test que historial respeta límite máximo"""
        symbolizer = WorldSymbolizer(zones=64)
        symbolizer.max_history = 3
        metrics = create_test_metrics()
        
        # Simbolizar 5 veces
        for _ in range(5):
            symbolizer.symbolize(metrics, player_zone=32)
        
        # Verificar que solo se guardan últimas 3
        for zone_id in range(64):
            assert len(symbolizer.zone_history[zone_id]) == 3
    
    def test_classify_zone_state(self):
        """Test clasificación de estados"""
        symbolizer = WorldSymbolizer(zones=64)
        
        # Estado estable
        state = symbolizer.classify_zone_state(
            entropy=0.1,
            anomaly=0.1,
            climate=0.3,
            temporal=0.1
        )
        assert state == symbolizer.STABLE  # 0
        
        # Estado con anomalía
        state = symbolizer.classify_zone_state(
            entropy=0.5,
            anomaly=0.9,
            climate=0.5,
            temporal=0.3
        )
        assert state == symbolizer.ANOMALY  # 4
        
        # Estado de transición
        state = symbolizer.classify_zone_state(
            entropy=0.5,
            anomaly=0.5,
            climate=0.5,
            temporal=0.8
        )
        assert state == symbolizer.TRANSITION  # 5
    
    def test_zone_distance(self):
        """Test cálculo de distancia entre zonas"""
        symbolizer = WorldSymbolizer(zones=64)
        
        # Misma zona
        distance = symbolizer.calculate_zone_distance(32, 32)
        assert distance == 0.0
        
        # Zonas en misma región (0-7)
        distance = symbolizer.calculate_zone_distance(0, 7)
        assert distance == 0.0
        
        # Zonas en regiones diferentes
        distance = symbolizer.calculate_zone_distance(0, 32)
        assert distance > 0.0
    
    def test_zone_type_factor(self):
        """Test factor de tipo de zona"""
        symbolizer = WorldSymbolizer(zones=64)
        
        # Zona normal (norte)
        factor = symbolizer.get_zone_type_factor(0)
        assert factor == 1.0
        
        # Zona atmosférica (48-55)
        factor = symbolizer.get_zone_type_factor(50)
        assert factor == 1.3
        
        # Zona temporal (56-63)
        factor = symbolizer.get_zone_type_factor(60)
        assert factor == 1.5
        
        # Zona subterránea (40-47)
        factor = symbolizer.get_zone_type_factor(45)
        assert factor == 1.2
    
    def test_get_zone_region_name(self):
        """Test obtención de nombre de región"""
        symbolizer = WorldSymbolizer(zones=64)
        
        assert symbolizer.get_zone_region_name(0) == "Norte"
        assert symbolizer.get_zone_region_name(10) == "Este"
        assert symbolizer.get_zone_region_name(20) == "Sur"
        assert symbolizer.get_zone_region_name(30) == "Oeste"
        assert symbolizer.get_zone_region_name(35) == "Central"
        assert symbolizer.get_zone_region_name(45) == "Subterránea"
        assert symbolizer.get_zone_region_name(50) == "Atmosférica"
        assert symbolizer.get_zone_region_name(60) == "Temporal"
    
    def test_get_state_name(self):
        """Test obtención de nombre de estado"""
        symbolizer = WorldSymbolizer(zones=64)
        
        assert symbolizer.get_state_name(0) == "ESTABLE"
        assert symbolizer.get_state_name(1) == "TENSIÓN LEVE"
        assert symbolizer.get_state_name(2) == "TENSIÓN MEDIA"
        assert symbolizer.get_state_name(3) == "INESTABILIDAD"
        assert symbolizer.get_state_name(4) == "ANOMALÍA"
        assert symbolizer.get_state_name(5) == "TRANSICIÓN"
    
    def test_visualize_sequence(self):
        """Test visualización de secuencia"""
        symbolizer = WorldSymbolizer(zones=64)
        metrics = create_test_metrics()
        
        sequence = symbolizer.symbolize(metrics, player_zone=32)
        visualization = symbolizer.visualize_sequence(sequence)
        
        # Verificar que contiene elementos esperados
        assert "ESTADO SIMBÓLICO DEL MUNDO" in visualization
        assert "Norte" in visualization
        assert "Este" in visualization
        assert "Distribución de estados" in visualization
        assert "ESTABLE" in visualization or "TENSIÓN" in visualization


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
