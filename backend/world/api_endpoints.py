"""
API REST Endpoints para HRM-World Engine

Expone funcionalidad del World Engine vía FastAPI
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
from pydantic import BaseModel
import asyncio
import json

from .world_engine import WorldEngine
from .metrics_collector import WorldState


# Modelos Pydantic para requests
class WorldStateRequest(BaseModel):
    """Request para actualizar estado del mundo"""
    player_position: List[float]  # [x, y, z]
    player_velocity: List[float]  # [vx, vy, vz]
    climate_state: Dict[str, float]  # {temp, humidity, pressure}
    biome_type: str
    time_of_day: float  # 0-24
    active_npcs: List[Dict] = []
    active_anomalies: List[Dict] = []
    terrain_elevation: float = 0.0
    weather_intensity: float = 0.0
    player_zone: int = 32  # Zona del jugador (0-63)


class PlayerActionRequest(BaseModel):
    """Request para inyectar acción del jugador"""
    action_intensity: float  # 0-1
    player_zone: int = 32


class ConfigRequest(BaseModel):
    """Request para configurar motor"""
    hrm_cycles: Optional[int] = None
    enable_propagation: Optional[bool] = None
    propagation_steps: Optional[int] = None
    enable_cascade: Optional[bool] = None


# Router
router = APIRouter(prefix="/world", tags=["world"])

# Instancia global del World Engine (se inicializa en startup)
world_engine: Optional[WorldEngine] = None

# WebSocket connections activas
active_connections: List[WebSocket] = []


def init_world_engine(
    hrm_checkpoint_path: str,
    llm_model: str = "qwen2.5:3b",
    ollama_url: str = "http://localhost:11434",
    device: str = "cpu"
):
    """
    Inicializa World Engine global
    
    Debe llamarse en el startup de FastAPI
    """
    global world_engine
    world_engine = WorldEngine(
        hrm_checkpoint_path=hrm_checkpoint_path,
        llm_model=llm_model,
        ollama_url=ollama_url,
        device=device
    )


@router.post("/update")
async def update_world(request: WorldStateRequest) -> JSONResponse:
    """
    Actualiza estado del mundo y genera eventos
    
    POST /world/update
    
    Body:
    {
        "player_position": [x, y, z],
        "player_velocity": [vx, vy, vz],
        "climate_state": {"temperature": 0.5, "humidity": 0.6, "pressure": 0.7},
        "biome_type": "desert",
        "time_of_day": 14.5,
        "active_npcs": [],
        "active_anomalies": [],
        "terrain_elevation": 100.0,
        "weather_intensity": 0.3,
        "player_zone": 32
    }
    
    Returns:
    {
        "event": {...},
        "narrative": "...",
        "analysis": {...},
        "metrics": {...},
        "processing_time": 0.123
    }
    """
    if world_engine is None:
        raise HTTPException(status_code=500, detail="World Engine not initialized")
    
    try:
        # Convertir request a WorldState
        world_state = WorldState(
            player_position=tuple(request.player_position),
            player_velocity=tuple(request.player_velocity),
            climate_state=request.climate_state,
            biome_type=request.biome_type,
            time_of_day=request.time_of_day,
            active_npcs=request.active_npcs,
            active_anomalies=request.active_anomalies,
            terrain_elevation=request.terrain_elevation,
            weather_intensity=request.weather_intensity
        )
        
        # Actualizar mundo
        result = world_engine.update(world_state, request.player_zone)
        
        # Broadcast a WebSocket clients
        await broadcast_event(result)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/action")
async def inject_player_action(request: PlayerActionRequest) -> JSONResponse:
    """
    Inyecta acción del jugador en el mundo
    
    POST /world/action
    
    Body:
    {
        "action_intensity": 0.8,
        "player_zone": 32
    }
    
    Returns:
    {
        "event": {...},
        "impact": {...}
    }
    """
    if world_engine is None:
        raise HTTPException(status_code=500, detail="World Engine not initialized")
    
    try:
        result = world_engine.inject_player_action(
            request.action_intensity,
            request.player_zone
        )
        
        # Broadcast a WebSocket clients
        await broadcast_event(result)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_world_status() -> JSONResponse:
    """
    Obtiene estado actual del mundo
    
    GET /world/status
    
    Returns:
    {
        "status": "active",
        "metrics": {...},
        "state_distribution": {...},
        "active_events": 2,
        "total_events": 15
    }
    """
    if world_engine is None:
        raise HTTPException(status_code=500, detail="World Engine not initialized")
    
    try:
        status = world_engine.get_world_status()
        return JSONResponse(content=status)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visualize")
async def visualize_world_state() -> JSONResponse:
    """
    Visualiza estado simbólico del mundo
    
    GET /world/visualize
    
    Returns:
    {
        "visualization": "..."
    }
    """
    if world_engine is None:
        raise HTTPException(status_code=500, detail="World Engine not initialized")
    
    try:
        visualization = world_engine.visualize_world_state()
        return JSONResponse(content={"visualization": visualization})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_event_history(limit: int = 10) -> JSONResponse:
    """
    Obtiene historial de eventos
    
    GET /world/history?limit=10
    
    Returns:
    [
        {
            "timestamp": 1234567890.0,
            "event": {...},
            "narrative": "...",
            "metrics": {...}
        },
        ...
    ]
    """
    if world_engine is None:
        raise HTTPException(status_code=500, detail="World Engine not initialized")
    
    try:
        history = world_engine.get_event_history(limit)
        return JSONResponse(content=history)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics() -> JSONResponse:
    """
    Obtiene estadísticas del motor
    
    GET /world/statistics
    
    Returns:
    {
        "total_updates": 100,
        "total_events": 50,
        "avg_processing_time": 0.123,
        "token_savings": 45000,
        ...
    }
    """
    if world_engine is None:
        raise HTTPException(status_code=500, detail="World Engine not initialized")
    
    try:
        stats = world_engine.get_statistics()
        return JSONResponse(content=stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/configure")
async def configure_engine(request: ConfigRequest) -> JSONResponse:
    """
    Configura parámetros del motor
    
    POST /world/configure
    
    Body:
    {
        "hrm_cycles": 3,
        "enable_propagation": true,
        "propagation_steps": 5,
        "enable_cascade": true
    }
    
    Returns:
    {
        "status": "configured",
        "config": {...}
    }
    """
    if world_engine is None:
        raise HTTPException(status_code=500, detail="World Engine not initialized")
    
    try:
        world_engine.configure(
            hrm_cycles=request.hrm_cycles,
            enable_propagation=request.enable_propagation,
            propagation_steps=request.propagation_steps,
            enable_cascade=request.enable_cascade
        )
        
        return JSONResponse(content={
            "status": "configured",
            "config": {
                "hrm_cycles": world_engine.hrm_cycles,
                "enable_propagation": world_engine.enable_propagation,
                "propagation_steps": world_engine.propagation_steps,
                "enable_cascade": world_engine.enable_cascade
            }
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/events")
async def clear_active_events() -> JSONResponse:
    """
    Limpia eventos activos que ya terminaron
    
    DELETE /world/events
    
    Returns:
    {
        "status": "cleared"
    }
    """
    if world_engine is None:
        raise HTTPException(status_code=500, detail="World Engine not initialized")
    
    try:
        world_engine.clear_active_events()
        return JSONResponse(content={"status": "cleared"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket para eventos en tiempo real
    
    WS /world/ws
    
    Envía eventos automáticamente cuando ocurren
    """
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Enviar estado inicial
        if world_engine:
            status = world_engine.get_world_status()
            await websocket.send_json({
                "type": "status",
                "data": status
            })
        
        # Mantener conexión abierta
        while True:
            # Recibir mensajes del cliente (opcional)
            data = await websocket.receive_text()
            
            # Echo (opcional)
            await websocket.send_json({
                "type": "echo",
                "data": data
            })
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


async def broadcast_event(event_data: Dict):
    """
    Broadcast evento a todos los clientes WebSocket conectados
    """
    if not active_connections:
        return
    
    message = {
        "type": "event",
        "data": event_data
    }
    
    # Enviar a todos los clientes
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.append(connection)
    
    # Limpiar conexiones muertas
    for connection in disconnected:
        active_connections.remove(connection)


# Health check
@router.get("/health")
async def health_check() -> JSONResponse:
    """
    Health check del World Engine
    
    GET /world/health
    
    Returns:
    {
        "status": "healthy",
        "engine_initialized": true,
        "active_websockets": 2
    }
    """
    return JSONResponse(content={
        "status": "healthy" if world_engine else "not_initialized",
        "engine_initialized": world_engine is not None,
        "active_websockets": len(active_connections)
    })
