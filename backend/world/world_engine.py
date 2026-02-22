"""
WorldEngine - Orquestador principal del sistema HRM-World

Integra todos los componentes:
1. WorldMetricsCollector
2. WorldSymbolizer
3. HRMWorldAnalyzer
4. EventInterpreter
5. NarrativeGenerator
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
import time

from .metrics_collector import WorldMetricsCollector, WorldState, WorldMetrics
from .symbolizer import WorldSymbolizer
from .hrm_analyzer import HRMWorldAnalyzer
from .event_interpreter import EventInterpreter, Event
from .narrative_generator import NarrativeGenerator


class WorldEngine:
    """
    Motor principal del mundo emergente
    
    Pipeline completo:
    1. Recopila métricas del mundo
    2. Simboliza en secuencia 0-5
    3. Analiza con HRM
    4. Interpreta eventos
    5. Genera narrativa
    6. Aplica efectos
    """
    
    def __init__(
        self,
        hrm_checkpoint_path: str,
        llm_model: str = "qwen2.5:3b",
        ollama_url: str = "http://localhost:11434",
        device: str = "cpu"
    ):
        """
        Inicializa World Engine
        
        Args:
            hrm_checkpoint_path: Ruta al checkpoint HRM
            llm_model: Modelo LLM para narrativa
            ollama_url: URL de Ollama
            device: 'cpu' o 'cuda'
        """
        # Componentes
        self.metrics_collector = WorldMetricsCollector()
        self.symbolizer = WorldSymbolizer(zones=64)
        self.hrm_analyzer = HRMWorldAnalyzer(hrm_checkpoint_path, device=device)
        self.event_interpreter = EventInterpreter()
        self.narrative_generator = NarrativeGenerator(llm_model, ollama_url)
        
        # Estado
        self.current_metrics: Optional[WorldMetrics] = None
        self.current_sequence: Optional[List[int]] = None
        self.active_events: List[Event] = []
        self.event_history: List[Dict] = []
        
        # Configuración
        self.hrm_cycles = 2
        self.enable_propagation = True
        self.propagation_steps = 3
        self.enable_cascade = True
        
        # Estadísticas
        self.stats = {
            "total_updates": 0,
            "total_events": 0,
            "avg_processing_time": 0.0,
            "token_savings": 0
        }
    
    def update(
        self, 
        world_state: WorldState,
        player_zone: int = 32
    ) -> Dict:
        """
        Actualización principal del mundo
        
        Args:
            world_state: Estado actual del mundo
            player_zone: Zona donde está el jugador (0-63)
            
        Returns:
            Dict con evento generado y narrativa
        """
        start_time = time.time()
        
        # 1. Recopilar métricas
        metrics = self.metrics_collector.collect(world_state)
        self.current_metrics = metrics
        
        # 2. Simbolizar
        symbolic_sequence = self.symbolizer.symbolize(metrics, player_zone)
        self.current_sequence = symbolic_sequence
        
        # 3. Analizar con HRM
        if self.enable_propagation:
            # Propagación multi-step
            hrm_output = self.hrm_analyzer.simulate_propagation(
                symbolic_sequence,
                steps=self.propagation_steps,
                cycles_per_step=self.hrm_cycles
            )
            # Usar último paso
            analysis = hrm_output["steps"][-1]
            analysis["emergence"] = hrm_output["emergence"]
        else:
            # Análisis simple
            analysis = self.hrm_analyzer.analyze(
                symbolic_sequence,
                cycles=self.hrm_cycles
            )
        
        # 4. Interpretar evento
        event = self.event_interpreter.interpret(analysis)
        
        # 5. Generar narrativa
        context = {
            "location": world_state.biome_type,
            "time_of_day": self._time_to_text(world_state.time_of_day)
        }
        
        if self.enable_cascade:
            narrative = self.narrative_generator.generate_with_cascade(event, context)
        else:
            narrative = self.narrative_generator.generate(event, context)
        
        # 6. Guardar evento
        self.active_events.append(event)
        self.event_history.append({
            "timestamp": time.time(),
            "event": event.to_dict(),
            "narrative": narrative,
            "metrics": {
                "entropy": metrics.world_entropy,
                "instability": analysis["instability_level"],
                "confidence": analysis["confidence"]
            }
        })
        
        # Actualizar estadísticas
        processing_time = time.time() - start_time
        self._update_stats(processing_time, len(narrative.split()))
        
        # Resultado
        return {
            "event": event.to_dict(),
            "narrative": narrative,
            "analysis": {
                "instability": analysis["instability_level"],
                "confidence": analysis["confidence"],
                "affected_zones": len(analysis["affected_zones"]),
                "world_shift": analysis["world_state_shift"]
            },
            "metrics": {
                "entropy": metrics.world_entropy,
                "anomaly_score": metrics.anomaly_score,
                "player_disruption": metrics.player_disruption
            },
            "processing_time": processing_time
        }
    
    def inject_player_action(
        self,
        action_intensity: float,
        player_zone: int = 32
    ) -> Dict:
        """
        Inyecta acción del jugador en el mundo
        
        Modifica la secuencia simbólica y re-analiza
        
        Args:
            action_intensity: Intensidad de la acción (0-1)
            player_zone: Zona del jugador
            
        Returns:
            Análisis del impacto
        """
        if self.current_sequence is None:
            return {"error": "No current sequence"}
        
        # Inyectar perturbación
        modified_sequence = self.hrm_analyzer.inject_player_action(
            self.current_sequence,
            player_zone,
            action_intensity
        )
        
        # Re-analizar
        analysis = self.hrm_analyzer.analyze(modified_sequence, cycles=self.hrm_cycles)
        
        # Interpretar
        event = self.event_interpreter.interpret(analysis)
        
        return {
            "event": event.to_dict(),
            "impact": {
                "zones_affected": len(analysis["affected_zones"]),
                "instability_change": analysis["instability_level"] - (
                    self.current_metrics.world_entropy if self.current_metrics else 0
                )
            }
        }
    
    def get_world_status(self) -> Dict:
        """
        Obtiene estado actual del mundo
        """
        if not self.current_metrics or not self.current_sequence:
            return {"status": "not_initialized"}
        
        # Analizar secuencia actual
        state_distribution = {i: self.current_sequence.count(i) for i in range(6)}
        
        # Calcular estabilidad global
        unstable_zones = sum(1 for s in self.current_sequence if s >= 3)
        stability = 1.0 - (unstable_zones / 64.0)
        
        return {
            "status": "active",
            "metrics": {
                "entropy": self.current_metrics.world_entropy,
                "anomaly_score": self.current_metrics.anomaly_score,
                "stability": stability
            },
            "state_distribution": state_distribution,
            "active_events": len(self.active_events),
            "total_events": self.stats["total_events"]
        }
    
    def visualize_world_state(self) -> str:
        """
        Visualiza estado simbólico del mundo
        """
        if not self.current_sequence:
            return "No current sequence"
        
        return self.symbolizer.visualize_sequence(self.current_sequence)
    
    def get_event_history(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene historial de eventos
        """
        return self.event_history[-limit:]
    
    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas del motor
        """
        return {
            **self.stats,
            "metrics_history": self.metrics_collector.get_history_summary(),
            "active_events": len(self.active_events),
            "total_events_history": len(self.event_history)
        }
    
    def clear_active_events(self):
        """
        Limpia eventos activos (eventos que ya terminaron)
        """
        current_time = time.time()
        
        # Filtrar eventos que ya terminaron
        self.active_events = [
            event for event in self.active_events
            if self._is_event_active(event, current_time)
        ]
    
    def _is_event_active(self, event: Event, current_time: float) -> bool:
        """
        Verifica si un evento sigue activo
        """
        # Buscar en historial
        for entry in reversed(self.event_history):
            if entry["event"]["type"] == event.type.value:
                event_time = entry["timestamp"]
                duration = event.duration
                return (current_time - event_time) < duration
        
        return False
    
    def _update_stats(self, processing_time: float, narrative_tokens: int):
        """
        Actualiza estadísticas
        """
        self.stats["total_updates"] += 1
        self.stats["total_events"] += 1
        
        # Promedio móvil de tiempo de procesamiento
        alpha = 0.1
        self.stats["avg_processing_time"] = (
            alpha * processing_time +
            (1 - alpha) * self.stats["avg_processing_time"]
        )
        
        # Calcular ahorro de tokens (vs sistema tradicional)
        # Sistema tradicional: ~500 tokens input
        # Sistema HRM: ~40 tokens input
        traditional_tokens = 500
        hrm_tokens = 40
        savings = traditional_tokens - hrm_tokens
        self.stats["token_savings"] += savings
    
    def _time_to_text(self, time_of_day: float) -> str:
        """
        Convierte hora del día a texto
        """
        if 5 <= time_of_day < 12:
            return "por la mañana"
        elif 12 <= time_of_day < 18:
            return "por la tarde"
        elif 18 <= time_of_day < 22:
            return "al atardecer"
        else:
            return "por la noche"
    
    def configure(
        self,
        hrm_cycles: Optional[int] = None,
        enable_propagation: Optional[bool] = None,
        propagation_steps: Optional[int] = None,
        enable_cascade: Optional[bool] = None
    ):
        """
        Configura parámetros del motor
        """
        if hrm_cycles is not None:
            self.hrm_cycles = hrm_cycles
        if enable_propagation is not None:
            self.enable_propagation = enable_propagation
        if propagation_steps is not None:
            self.propagation_steps = propagation_steps
        if enable_cascade is not None:
            self.enable_cascade = enable_cascade
