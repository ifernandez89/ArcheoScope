"""
Demo del HRM-World Engine

Script de ejemplo para probar el sistema completo
"""

import sys
from pathlib import Path
import time
import numpy as np

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from world.world_engine import WorldEngine
from world.metrics_collector import WorldState


def create_sample_world_state(
    player_pos: tuple = (0, 0, 0),
    player_vel: tuple = (0, 0, 0),
    time_of_day: float = 12.0,
    weather_intensity: float = 0.3
) -> WorldState:
    """Crea estado de mundo de ejemplo"""
    return WorldState(
        player_position=player_pos,
        player_velocity=player_vel,
        climate_state={
            'temperature': 0.5 + np.random.uniform(-0.1, 0.1),
            'humidity': 0.6 + np.random.uniform(-0.1, 0.1),
            'pressure': 0.7 + np.random.uniform(-0.1, 0.1)
        },
        biome_type="desert",
        time_of_day=time_of_day,
        active_npcs=[],
        active_anomalies=[],
        terrain_elevation=100.0,
        weather_intensity=weather_intensity
    )


def demo_basic_update():
    """Demo 1: Actualización básica del mundo"""
    print("\n" + "="*60)
    print("DEMO 1: Actualización Básica del Mundo")
    print("="*60)
    
    # Inicializar engine (sin checkpoint real por ahora)
    print("\n[1] Inicializando World Engine...")
    engine = WorldEngine(
        hrm_checkpoint_path="dummy_checkpoint.pt",  # Placeholder
        llm_model="qwen2.5:3b",
        device="cpu"
    )
    print("✓ Engine inicializado")
    
    # Crear estado del mundo
    print("\n[2] Creando estado del mundo...")
    world_state = create_sample_world_state()
    print(f"✓ Estado creado: jugador en {world_state.player_position}")
    
    # Actualizar mundo
    print("\n[3] Actualizando mundo...")
    try:
        result = engine.update(world_state, player_zone=32)
        
        print("\n[4] Resultado:")
        print(f"  Evento: {result['event']['type']}")
        print(f"  Severidad: {result['event']['severity']}")
        print(f"  Intensidad: {result['event']['intensity']:.2f}")
        print(f"  Confianza: {result['analysis']['confidence']:.2f}")
        print(f"  Zonas afectadas: {result['analysis']['affected_zones']}")
        print(f"  Tiempo de procesamiento: {result['processing_time']:.3f}s")
        
        print(f"\n[5] Narrativa:")
        print(f"  {result['narrative']}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("  (Esto es esperado sin checkpoint real)")


def demo_player_action():
    """Demo 2: Inyección de acción del jugador"""
    print("\n" + "="*60)
    print("DEMO 2: Inyección de Acción del Jugador")
    print("="*60)
    
    engine = WorldEngine(
        hrm_checkpoint_path="dummy_checkpoint.pt",
        llm_model="qwen2.5:3b",
        device="cpu"
    )
    
    # Estado inicial
    print("\n[1] Estado inicial del mundo...")
    world_state = create_sample_world_state()
    engine.update(world_state, player_zone=32)
    
    # Jugador realiza acción intensa
    print("\n[2] Jugador realiza acción intensa (intensidad=0.9)...")
    try:
        result = engine.inject_player_action(
            action_intensity=0.9,
            player_zone=32
        )
        
        print("\n[3] Impacto de la acción:")
        print(f"  Evento generado: {result['event']['type']}")
        print(f"  Zonas afectadas: {result['impact']['zones_affected']}")
        print(f"  Cambio de inestabilidad: {result['impact']['instability_change']:.3f}")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_propagation():
    """Demo 3: Propagación multi-step"""
    print("\n" + "="*60)
    print("DEMO 3: Propagación Multi-Step")
    print("="*60)
    
    engine = WorldEngine(
        hrm_checkpoint_path="dummy_checkpoint.pt",
        llm_model="qwen2.5:3b",
        device="cpu"
    )
    
    # Habilitar propagación
    engine.configure(
        enable_propagation=True,
        propagation_steps=5,
        hrm_cycles=2
    )
    
    print("\n[1] Configuración:")
    print(f"  Propagación: {engine.enable_propagation}")
    print(f"  Pasos: {engine.propagation_steps}")
    print(f"  Ciclos HRM: {engine.hrm_cycles}")
    
    # Crear estado con alta inestabilidad
    print("\n[2] Creando estado con alta inestabilidad...")
    world_state = create_sample_world_state(
        weather_intensity=0.9
    )
    
    print("\n[3] Simulando propagación...")
    try:
        result = engine.update(world_state, player_zone=32)
        
        print("\n[4] Resultado de propagación:")
        print(f"  Inestabilidad final: {result['analysis']['instability']:.2f}")
        print(f"  Evento emergente: {result['event']['type']}")
        print(f"  Cambio de estado: {result['analysis']['world_shift']}")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def demo_cascade():
    """Demo 4: Cascada cognitiva (modelo adaptativo)"""
    print("\n" + "="*60)
    print("DEMO 4: Cascada Cognitiva")
    print("="*60)
    
    engine = WorldEngine(
        hrm_checkpoint_path="dummy_checkpoint.pt",
        llm_model="qwen2.5:3b",
        device="cpu"
    )
    
    # Habilitar cascada
    engine.configure(enable_cascade=True)
    
    print("\n[1] Probando eventos de diferentes complejidades...")
    
    # Evento simple
    print("\n[2] Evento simple (baja intensidad)...")
    world_state = create_sample_world_state(weather_intensity=0.2)
    try:
        result = engine.update(world_state, player_zone=32)
        print(f"  Modelo usado: pequeño (0.5B)")
        print(f"  Evento: {result['event']['type']}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Evento complejo
    print("\n[3] Evento complejo (alta intensidad)...")
    world_state = create_sample_world_state(weather_intensity=0.9)
    try:
        result = engine.update(world_state, player_zone=32)
        print(f"  Modelo usado: grande (3B)")
        print(f"  Evento: {result['event']['type']}")
    except Exception as e:
        print(f"  ✗ Error: {e}")


def demo_statistics():
    """Demo 5: Estadísticas y monitoreo"""
    print("\n" + "="*60)
    print("DEMO 5: Estadísticas y Monitoreo")
    print("="*60)
    
    engine = WorldEngine(
        hrm_checkpoint_path="dummy_checkpoint.pt",
        llm_model="qwen2.5:3b",
        device="cpu"
    )
    
    print("\n[1] Ejecutando múltiples actualizaciones...")
    
    # Simular 10 actualizaciones
    for i in range(10):
        world_state = create_sample_world_state(
            time_of_day=12.0 + i,
            weather_intensity=0.3 + i * 0.05
        )
        try:
            engine.update(world_state, player_zone=32 + (i % 8))
        except Exception:
            pass
    
    print(f"✓ {10} actualizaciones completadas")
    
    # Obtener estadísticas
    print("\n[2] Estadísticas del motor:")
    stats = engine.get_statistics()
    print(f"  Total actualizaciones: {stats['total_updates']}")
    print(f"  Total eventos: {stats['total_events']}")
    print(f"  Tiempo promedio: {stats['avg_processing_time']:.3f}s")
    print(f"  Ahorro de tokens: {stats['token_savings']}")
    
    # Estado del mundo
    print("\n[3] Estado actual del mundo:")
    status = engine.get_world_status()
    print(f"  Status: {status['status']}")
    print(f"  Entropía: {status['metrics']['entropy']:.2f}")
    print(f"  Estabilidad: {status['metrics']['stability']:.2f}")
    print(f"  Eventos activos: {status['active_events']}")
    
    # Visualización
    print("\n[4] Visualización del estado simbólico:")
    visualization = engine.visualize_world_state()
    print(visualization)


def demo_history():
    """Demo 6: Historial de eventos"""
    print("\n" + "="*60)
    print("DEMO 6: Historial de Eventos")
    print("="*60)
    
    engine = WorldEngine(
        hrm_checkpoint_path="dummy_checkpoint.pt",
        llm_model="qwen2.5:3b",
        device="cpu"
    )
    
    print("\n[1] Generando eventos...")
    
    # Generar varios eventos
    for i in range(5):
        world_state = create_sample_world_state(
            time_of_day=12.0 + i * 2,
            weather_intensity=0.3 + i * 0.1
        )
        try:
            engine.update(world_state, player_zone=32)
            time.sleep(0.1)  # Pequeña pausa
        except Exception:
            pass
    
    print(f"✓ {5} eventos generados")
    
    # Obtener historial
    print("\n[2] Historial de eventos (últimos 5):")
    history = engine.get_event_history(limit=5)
    
    for i, entry in enumerate(history, 1):
        print(f"\n  Evento {i}:")
        print(f"    Tipo: {entry['event']['type']}")
        print(f"    Timestamp: {entry['timestamp']:.0f}")
        print(f"    Entropía: {entry['metrics']['entropy']:.2f}")
        print(f"    Narrativa: {entry['narrative'][:60]}...")


def main():
    """Ejecuta todos los demos"""
    print("\n" + "="*60)
    print("HRM-WORLD ENGINE - DEMOS")
    print("="*60)
    print("\nNOTA: Estos demos usan un checkpoint placeholder.")
    print("Para funcionamiento real, necesitas el checkpoint HRM real.")
    print("="*60)
    
    demos = [
        ("Actualización Básica", demo_basic_update),
        ("Acción del Jugador", demo_player_action),
        ("Propagación Multi-Step", demo_propagation),
        ("Cascada Cognitiva", demo_cascade),
        ("Estadísticas", demo_statistics),
        ("Historial", demo_history)
    ]
    
    print("\nDemos disponibles:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  0. Ejecutar todos")
    
    try:
        choice = input("\nSelecciona demo (0-6): ").strip()
        
        if choice == "0":
            # Ejecutar todos
            for name, demo_func in demos:
                demo_func()
                time.sleep(1)
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # Ejecutar demo específico
            demos[int(choice) - 1][1]()
        else:
            print("Opción inválida")
    
    except KeyboardInterrupt:
        print("\n\nDemo interrumpido")
    except Exception as e:
        print(f"\nError: {e}")
    
    print("\n" + "="*60)
    print("FIN DE DEMOS")
    print("="*60)


if __name__ == "__main__":
    main()
