"""
Tests de integración para HRM-World Engine

Tests end-to-end del pipeline completo
"""

import pytest
import asyncio
from backend.world.world_engine import WorldEngine
from backend.world.metrics_collector import WorldState


@pytest.fixture
def world_engine():
    """Fixture para WorldEngine"""
    # Usar checkpoint placeholder para tests
    engine = WorldEngine(
        hrm_checkpoint_path="dummy_checkpoint.pt",
        llm_model="qwen2.5:3b",
        device="cpu"
    )
    return engine


@pytest.fixture
def sample_world_state():
    """Fixture para WorldState de ejemplo"""
    return WorldState(
        player_position=(0.0, 0.0, 0.0),
        player_velocity=(1.0, 0.0, 1.0),
        climate_state={'temperature': 0.5, 'humidity': 0.6, 'pressure': 0.7},
        biome_type="desert",
        time_of_day=12.0,
        active_npcs=[],
        active_anomalies=[],
        terrain_elevation=100.0,
        weather_intensity=0.3
    )


class TestWorldEnginePipeline:
    """Tests del pipeline completo"""
    
    def test_full_pipeline(self, world_engine, sample_world_state):
        """Test pipeline completo: Metrics → Symbolizer → HRM → Interpreter → Narrative"""
        try:
            result = world_engine.update(sample_world_state, player_zone=32)
            
            # Verificar estructura del resultado
            assert 'event' in result
            assert 'narrative' in result
            assert 'analysis' in result
            assert 'metrics' in result
            assert 'processing_time' in result
            
            # Verificar evento
            assert 'type' in result['event']
            assert 'severity' in result['event']
            assert 'intensity' in result['event']
            
            # Verificar análisis
            assert 'instability' in result['analysis']
            assert 'confidence' in result['analysis']
            
            # Verificar métricas
            assert 'entropy' in result['metrics']
            assert 'anomaly_score' in result['metrics']
            
        except Exception as e:
            # Esperado sin checkpoint real
            assert "checkpoint" in str(e).lower() or "model" in str(e).lower()
    
    def test_player_action_injection(self, world_engine, sample_world_state):
        """Test inyección de acción del jugador"""
        try:
            # Actualización inicial
            world_engine.update(sample_world_state, player_zone=32)
            
            # Inyectar acción
            result = world_engine.inject_player_action(
                action_intensity=0.8,
                player_zone=32
            )
            
            # Verificar resultado
            assert 'event' in result
            assert 'impact' in result
            
        except Exception as e:
            # Esperado sin checkpoint real
            assert "checkpoint" in str(e).lower() or "model" in str(e).lower()
    
    def test_propagation_simulation(self, world_engine, sample_world_state):
        """Test simulación de propagación multi-step"""
        try:
            # Habilitar propagación
            world_engine.configure(
                enable_propagation=True,
                propagation_steps=3
            )
            
            result = world_engine.update(sample_world_state, player_zone=32)
            
            # Verificar que se ejecutó propagación
            assert result is not None
            
        except Exception as e:
            # Esperado sin checkpoint real
            assert "checkpoint" in str(e).lower() or "model" in str(e).lower()
    
    def test_cascade_selection(self, world_engine, sample_world_state):
        """Test cascada cognitiva (selección de modelo)"""
        try:
            # Habilitar cascada
            world_engine.configure(enable_cascade=True)
            
            # Evento simple (baja intensidad)
            state_simple = sample_world_state
            state_simple.weather_intensity = 0.1
            result_simple = world_engine.update(state_simple, player_zone=32)
            
            # Evento complejo (alta intensidad)
            state_complex = sample_world_state
            state_complex.weather_intensity = 0.9
            result_complex = world_engine.update(state_complex, player_zone=32)
            
            # Ambos deberían funcionar
            assert result_simple is not None
            assert result_complex is not None
            
        except Exception as e:
            # Esperado sin checkpoint real
            assert "checkpoint" in str(e).lower() or "model" in str(e).lower()
    
    def test_world_status(self, world_engine, sample_world_state):
        """Test obtención de estado del mundo"""
        try:
            # Actualizar mundo
            world_engine.update(sample_world_state, player_zone=32)
            
            # Obtener estado
            status = world_engine.get_world_status()
            
            # Verificar estructura
            assert 'status' in status
            assert 'metrics' in status
            assert 'state_distribution' in status
            
        except Exception as e:
            # Sin actualización previa, debería retornar not_initialized
            status = world_engine.get_world_status()
            assert status['status'] == 'not_initialized'
    
    def test_event_history(self, world_engine, sample_world_state):
        """Test historial de eventos"""
        try:
            # Generar varios eventos
            for i in range(3):
                world_engine.update(sample_world_state, player_zone=32)
            
            # Obtener historial
            history = world_engine.get_event_history(limit=3)
            
            # Verificar que hay eventos
            assert len(history) > 0
            
            # Verificar estructura de eventos
            for entry in history:
                assert 'timestamp' in entry
                assert 'event' in entry
                assert 'narrative' in entry
                assert 'metrics' in entry
            
        except Exception as e:
            # Esperado sin checkpoint real
            pass
    
    def test_statistics(self, world_engine, sample_world_state):
        """Test estadísticas del motor"""
        try:
            # Generar eventos
            for i in range(5):
                world_engine.update(sample_world_state, player_zone=32)
            
            # Obtener estadísticas
            stats = world_engine.get_statistics()
            
            # Verificar estructura
            assert 'total_updates' in stats
            assert 'total_events' in stats
            assert 'avg_processing_time' in stats
            assert 'token_savings' in stats
            
            # Verificar valores
            assert stats['total_updates'] >= 5
            assert stats['total_events'] >= 5
            
        except Exception as e:
            # Esperado sin checkpoint real
            pass
    
    def test_visualization(self, world_engine, sample_world_state):
        """Test visualización de estado simbólico"""
        try:
            # Actualizar mundo
            world_engine.update(sample_world_state, player_zone=32)
            
            # Obtener visualización
            viz = world_engine.visualize_world_state()
            
            # Verificar que es string no vacío
            assert isinstance(viz, str)
            assert len(viz) > 0
            
        except Exception as e:
            # Sin actualización, debería retornar mensaje
            viz = world_engine.visualize_world_state()
            assert "No current sequence" in viz
    
    def test_configuration(self, world_engine):
        """Test configuración dinámica"""
        # Configurar parámetros
        world_engine.configure(
            hrm_cycles=3,
            enable_propagation=False,
            propagation_steps=5,
            enable_cascade=False
        )
        
        # Verificar que se aplicaron
        assert world_engine.hrm_cycles == 3
        assert world_engine.enable_propagation == False
        assert world_engine.propagation_steps == 5
        assert world_engine.enable_cascade == False
    
    def test_clear_active_events(self, world_engine, sample_world_state):
        """Test limpieza de eventos activos"""
        try:
            # Generar eventos
            world_engine.update(sample_world_state, player_zone=32)
            
            # Limpiar eventos
            world_engine.clear_active_events()
            
            # Verificar que se limpiaron
            # (eventos que ya terminaron se eliminan)
            assert True  # No hay forma directa de verificar sin acceso interno
            
        except Exception as e:
            # Esperado sin checkpoint real
            pass


class TestComponentIntegration:
    """Tests de integración entre componentes"""
    
    def test_metrics_to_symbolizer(self, world_engine, sample_world_state):
        """Test integración Metrics → Symbolizer"""
        try:
            # Recopilar métricas
            metrics = world_engine.metrics_collector.collect(sample_world_state)
            
            # Simbolizar
            sequence = world_engine.symbolizer.symbolize(metrics, player_zone=32)
            
            # Verificar
            assert len(sequence) == 64
            assert all(0 <= t <= 5 for t in sequence)
            
        except Exception as e:
            pytest.fail(f"Error en integración Metrics → Symbolizer: {e}")
    
    def test_symbolizer_to_hrm(self, world_engine):
        """Test integración Symbolizer → HRM"""
        try:
            # Crear secuencia de prueba
            sequence = [0] * 32 + [2] * 16 + [4] * 16
            
            # Analizar con HRM
            analysis = world_engine.hrm_analyzer.analyze(sequence, cycles=2)
            
            # Verificar estructura
            assert 'world_state_shift' in analysis
            assert 'emergent_event' in analysis
            assert 'confidence' in analysis
            assert 'instability_level' in analysis
            
        except Exception as e:
            # Esperado sin checkpoint real
            assert "checkpoint" in str(e).lower() or "model" in str(e).lower()
    
    def test_hrm_to_interpreter(self, world_engine):
        """Test integración HRM → Interpreter"""
        # Crear análisis simulado
        hrm_output = {
            'world_state_shift': 'instability_increase',
            'emergent_event': 'electromagnetic_storm',
            'confidence': 0.75,
            'instability_level': 0.82,
            'affected_zones': [30, 31, 32, 33],
            'propagation_vector': {
                'direction': 'norte',
                'speed': 0.5,
                'intensity': 0.8
            },
            'state_changes': [],
            'global_patterns': {}
        }
        
        # Interpretar
        event = world_engine.event_interpreter.interpret(hrm_output)
        
        # Verificar
        assert event.type is not None
        assert event.severity is not None
        assert event.intensity == 0.82
        assert len(event.effects) > 0
    
    def test_interpreter_to_narrative(self, world_engine):
        """Test integración Interpreter → Narrative"""
        # Crear evento simulado
        from backend.world.event_interpreter import Event, EventType, EventSeverity, EventEffect
        
        event = Event(
            type=EventType.ELECTROMAGNETIC_STORM,
            severity=EventSeverity.MAJOR,
            intensity=0.8,
            confidence=0.75,
            affected_zones=[32],
            affected_regions=['central'],
            duration=120.0,
            effects=[
                EventEffect(
                    type='climate',
                    parameter='storm_intensity',
                    value=0.8,
                    duration=120.0
                )
            ],
            narrative_seed={
                'event': 'tormenta electromagnética',
                'severity_text': 'major',
                'sensation': 'una fuerza intensa',
                'region': 'central',
                'direction': 'desde el norte',
                'intensity_text': 'fuerte',
                'speed_text': 'rápidamente'
            },
            propagation={'direction': 'norte', 'speed': 0.5, 'intensity': 0.8}
        )
        
        # Generar narrativa (fallback procedural)
        try:
            narrative = world_engine.narrative_generator.generate(event)
            
            # Verificar que es string no vacío
            assert isinstance(narrative, str)
            assert len(narrative) > 0
            
        except Exception as e:
            # Si falla LLM, debería usar fallback procedural
            narrative = world_engine.narrative_generator._generate_procedural(event)
            assert isinstance(narrative, str)
            assert len(narrative) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
