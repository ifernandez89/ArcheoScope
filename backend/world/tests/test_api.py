"""
Tests para API endpoints de HRM-World

Tests de API REST y WebSocket
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json


# Mock del WorldEngine para tests sin checkpoint real
@pytest.fixture
def mock_world_engine():
    """Mock de WorldEngine para tests"""
    mock_engine = Mock()
    
    # Mock update
    mock_engine.update.return_value = {
        'event': {
            'type': 'electromagnetic_storm',
            'severity': 'major',
            'intensity': 0.82,
            'confidence': 0.75,
            'affected_zones': [32, 33],
            'affected_regions': ['central'],
            'duration': 120.0,
            'effects': [],
            'narrative_seed': {},
            'propagation': {}
        },
        'narrative': 'Una tormenta electromagnética se aproxima desde el norte.',
        'analysis': {
            'instability': 0.82,
            'confidence': 0.75,
            'affected_zones': 2,
            'world_shift': 'instability_increase'
        },
        'metrics': {
            'entropy': 0.65,
            'anomaly_score': 0.72,
            'player_disruption': 0.45
        },
        'processing_time': 0.123
    }
    
    # Mock inject_player_action
    mock_engine.inject_player_action.return_value = {
        'event': {
            'type': 'energy_surge',
            'severity': 'moderate',
            'intensity': 0.65
        },
        'impact': {
            'zones_affected': 5,
            'instability_change': 0.15
        }
    }
    
    # Mock get_world_status
    mock_engine.get_world_status.return_value = {
        'status': 'active',
        'metrics': {
            'entropy': 0.65,
            'anomaly_score': 0.72,
            'stability': 0.35
        },
        'state_distribution': {0: 20, 1: 15, 2: 12, 3: 10, 4: 5, 5: 2},
        'active_events': 2,
        'total_events': 15
    }
    
    # Mock visualize_world_state
    mock_engine.visualize_world_state.return_value = "Estado simbólico del mundo..."
    
    # Mock get_event_history
    mock_engine.get_event_history.return_value = [
        {
            'timestamp': 1234567890.0,
            'event': {'type': 'electromagnetic_storm'},
            'narrative': 'Narrativa...',
            'metrics': {'entropy': 0.65}
        }
    ]
    
    # Mock get_statistics
    mock_engine.get_statistics.return_value = {
        'total_updates': 100,
        'total_events': 50,
        'avg_processing_time': 0.123,
        'token_savings': 45000
    }
    
    # Mock configure
    mock_engine.configure.return_value = None
    mock_engine.hrm_cycles = 2
    mock_engine.enable_propagation = True
    mock_engine.propagation_steps = 3
    mock_engine.enable_cascade = True
    
    # Mock clear_active_events
    mock_engine.clear_active_events.return_value = None
    
    return mock_engine


@pytest.fixture
def test_client(mock_world_engine):
    """Cliente de test con WorldEngine mockeado"""
    with patch('backend.world.api_endpoints.world_engine', mock_world_engine):
        from backend.world.api_endpoints import router
        from fastapi import FastAPI
        
        app = FastAPI()
        app.include_router(router)
        
        client = TestClient(app)
        yield client


class TestWorldAPIEndpoints:
    """Tests de endpoints REST"""
    
    def test_update_world(self, test_client):
        """Test POST /world/update"""
        request_data = {
            'player_position': [0, 0, 0],
            'player_velocity': [1, 0, 1],
            'climate_state': {'temperature': 0.5, 'humidity': 0.6, 'pressure': 0.7},
            'biome_type': 'desert',
            'time_of_day': 12.0,
            'active_npcs': [],
            'active_anomalies': [],
            'terrain_elevation': 100.0,
            'weather_intensity': 0.3,
            'player_zone': 32
        }
        
        response = test_client.post('/world/update', json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'event' in data
        assert 'narrative' in data
        assert 'analysis' in data
        assert 'metrics' in data
        assert data['event']['type'] == 'electromagnetic_storm'
    
    def test_inject_player_action(self, test_client):
        """Test POST /world/action"""
        request_data = {
            'action_intensity': 0.8,
            'player_zone': 32
        }
        
        response = test_client.post('/world/action', json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'event' in data
        assert 'impact' in data
        assert data['event']['type'] == 'energy_surge'
    
    def test_get_world_status(self, test_client):
        """Test GET /world/status"""
        response = test_client.get('/world/status')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'status' in data
        assert 'metrics' in data
        assert 'state_distribution' in data
        assert data['status'] == 'active'
    
    def test_visualize_world_state(self, test_client):
        """Test GET /world/visualize"""
        response = test_client.get('/world/visualize')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'visualization' in data
        assert isinstance(data['visualization'], str)
    
    def test_get_event_history(self, test_client):
        """Test GET /world/history"""
        response = test_client.get('/world/history?limit=10')
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'timestamp' in data[0]
            assert 'event' in data[0]
            assert 'narrative' in data[0]
    
    def test_get_statistics(self, test_client):
        """Test GET /world/statistics"""
        response = test_client.get('/world/statistics')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'total_updates' in data
        assert 'total_events' in data
        assert 'avg_processing_time' in data
        assert 'token_savings' in data
    
    def test_configure_engine(self, test_client):
        """Test POST /world/configure"""
        request_data = {
            'hrm_cycles': 3,
            'enable_propagation': True,
            'propagation_steps': 5,
            'enable_cascade': True
        }
        
        response = test_client.post('/world/configure', json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'status' in data
        assert 'config' in data
        assert data['status'] == 'configured'
    
    def test_clear_active_events(self, test_client):
        """Test DELETE /world/events"""
        response = test_client.delete('/world/events')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'status' in data
        assert data['status'] == 'cleared'
    
    def test_health_check(self, test_client):
        """Test GET /world/health"""
        response = test_client.get('/world/health')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'status' in data
        assert 'engine_initialized' in data
        assert 'active_websockets' in data


class TestWebSocket:
    """Tests de WebSocket"""
    
    def test_websocket_connection(self, test_client):
        """Test conexión WebSocket"""
        with test_client.websocket_connect('/world/ws') as websocket:
            # Debería recibir estado inicial
            data = websocket.receive_json()
            
            assert 'type' in data
            # Puede ser 'status' o 'echo' dependiendo del flujo
            assert data['type'] in ['status', 'echo']
    
    def test_websocket_echo(self, test_client):
        """Test echo en WebSocket"""
        with test_client.websocket_connect('/world/ws') as websocket:
            # Enviar mensaje
            websocket.send_text('test message')
            
            # Recibir respuesta
            data = websocket.receive_json()
            
            # Debería ser echo
            assert data['type'] == 'echo'
            assert data['data'] == 'test message'


class TestErrorHandling:
    """Tests de manejo de errores"""
    
    def test_update_without_engine(self):
        """Test update sin engine inicializado"""
        with patch('backend.world.api_endpoints.world_engine', None):
            from backend.world.api_endpoints import router
            from fastapi import FastAPI
            
            app = FastAPI()
            app.include_router(router)
            client = TestClient(app)
            
            request_data = {
                'player_position': [0, 0, 0],
                'player_velocity': [0, 0, 0],
                'climate_state': {},
                'biome_type': 'desert',
                'time_of_day': 12.0,
                'player_zone': 32
            }
            
            response = client.post('/world/update', json=request_data)
            
            assert response.status_code == 500
            assert 'not initialized' in response.json()['detail'].lower()
    
    def test_invalid_request_data(self, test_client):
        """Test con datos inválidos"""
        request_data = {
            'player_position': [0, 0],  # Debería ser [x, y, z]
            'player_velocity': [0, 0, 0],
            'climate_state': {},
            'biome_type': 'desert',
            'time_of_day': 12.0
        }
        
        response = test_client.post('/world/update', json=request_data)
        
        # Debería fallar validación
        assert response.status_code == 422


class TestRequestModels:
    """Tests de modelos Pydantic"""
    
    def test_world_state_request_valid(self):
        """Test WorldStateRequest válido"""
        from backend.world.api_endpoints import WorldStateRequest
        
        request = WorldStateRequest(
            player_position=[0, 0, 0],
            player_velocity=[1, 0, 1],
            climate_state={'temperature': 0.5},
            biome_type='desert',
            time_of_day=12.0
        )
        
        assert request.player_position == [0, 0, 0]
        assert request.player_zone == 32  # Default
    
    def test_player_action_request_valid(self):
        """Test PlayerActionRequest válido"""
        from backend.world.api_endpoints import PlayerActionRequest
        
        request = PlayerActionRequest(
            action_intensity=0.8,
            player_zone=40
        )
        
        assert request.action_intensity == 0.8
        assert request.player_zone == 40
    
    def test_config_request_valid(self):
        """Test ConfigRequest válido"""
        from backend.world.api_endpoints import ConfigRequest
        
        request = ConfigRequest(
            hrm_cycles=3,
            enable_propagation=True
        )
        
        assert request.hrm_cycles == 3
        assert request.enable_propagation == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
