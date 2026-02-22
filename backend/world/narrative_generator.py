"""
NarrativeGenerator - Genera narrativa usando LLM (solo verbalización)

El LLM NO decide eventos, solo los narra.
Input: 20-40 tokens (evento estructurado)
Output: 2-3 frases descriptivas
"""

from typing import Dict, Optional
import requests
import json
from .event_interpreter import Event


class NarrativeGenerator:
    """
    Genera narrativa corta de eventos usando LLM
    
    El LLM recibe un evento ya decidido por el HRM y solo lo verbaliza.
    Esto reduce drásticamente el uso de tokens (80-90% menos).
    """
    
    def __init__(
        self, 
        model_name: str = "qwen2.5:3b",
        ollama_url: str = "http://localhost:11434"
    ):
        """
        Inicializa generador de narrativa
        
        Args:
            model_name: Modelo de Ollama a usar
            ollama_url: URL del servidor Ollama
        """
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.api_endpoint = f"{ollama_url}/api/generate"
        
    def generate(self, event: Event, context: Optional[Dict] = None) -> str:
        """
        Genera narrativa del evento
        
        Args:
            event: Evento estructurado
            context: Contexto adicional (ubicación, hora, etc.)
            
        Returns:
            Texto narrativo (2-3 frases)
        """
        # Crear prompt minimalista
        prompt = self._create_prompt(event, context)
        
        # Generar con LLM
        try:
            response = self._call_ollama(prompt, max_tokens=150)
            return response.strip()
        except Exception as e:
            # Fallback a narrativa procedural
            return self._generate_procedural(event)
    
    def _create_prompt(self, event: Event, context: Optional[Dict]) -> str:
        """
        Crea prompt minimalista para el LLM
        
        Solo información esencial (20-40 tokens)
        """
        seed = event.narrative_seed
        
        # Contexto básico
        location = context.get("location", "un lugar desconocido") if context else "este lugar"
        time = context.get("time_of_day", "ahora") if context else "en este momento"
        
        # Prompt ultra-compacto
        prompt = f"""Evento: {seed['event']}
Severidad: {seed['severity_text']}
Región: {seed['region']}
Dirección: {seed['direction']}
Intensidad: {seed['intensity_text']}

Narra en 2-3 frases cortas lo que el jugador percibe en {location} {time}. Sé descriptivo pero conciso."""
        
        return prompt
    
    def _call_ollama(self, prompt: str, max_tokens: int = 150) -> str:
        """
        Llama a Ollama API
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = requests.post(
            self.api_endpoint,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
    
    def _generate_procedural(self, event: Event) -> str:
        """
        Genera narrativa procedural (fallback sin LLM)
        
        Usa templates simples basados en el evento
        """
        seed = event.narrative_seed
        
        # Templates por tipo de evento
        templates = {
            "tormenta electromagnética": [
                f"Una {seed['event']} se aproxima {seed['direction']}. El aire se carga de electricidad estática.",
                f"Sientes {seed['sensation']} mientras la tormenta se intensifica. Los rayos iluminan el horizonte.",
                f"La {seed['event']} avanza {seed['speed_text']} hacia tu posición. La visibilidad disminuye."
            ],
            "fractura en la realidad": [
                f"El espacio a tu alrededor comienza a distorsionarse. Una {seed['event']} se abre {seed['direction']}.",
                f"Percibes {seed['sensation']} mientras la realidad se fragmenta. Las formas se vuelven inestables.",
                f"Una grieta dimensional aparece con intensidad {seed['intensity_text']}. El mundo tiembla."
            ],
            "anomalía temporal": [
                f"El tiempo parece ralentizarse. Una {seed['event']} se manifiesta {seed['direction']}.",
                f"Experimentas {seed['sensation']} mientras el flujo temporal se distorsiona.",
                f"Los momentos se superponen. La {seed['event']} avanza {seed['speed_text']}."
            ],
            "oleada de energía": [
                f"Una {seed['event']} recorre el área {seed['direction']}. El aire brilla con intensidad {seed['intensity_text']}.",
                f"Sientes {seed['sensation']} mientras la energía se acumula. Todo vibra a tu alrededor.",
                f"La oleada se expande {seed['speed_text']}. Puedes sentir su poder."
            ],
            "onda de caos": [
                f"Una {seed['event']} se desata {seed['direction']}. El orden se desintegra.",
                f"Percibes {seed['sensation']} mientras el caos se propaga. Nada es predecible.",
                f"La onda avanza {seed['speed_text']} con intensidad {seed['intensity_text']}."
            ],
            "cambio dimensional": [
                f"Un {seed['event']} ocurre {seed['direction']}. La realidad se reescribe.",
                f"Sientes {seed['sensation']} mientras las dimensiones se entrelazan.",
                f"El cambio se completa {seed['speed_text']}. Todo es diferente ahora."
            ],
            "perturbación menor": [
                f"Una {seed['event']} recorre el área. Apenas perceptible.",
                f"Sientes {seed['sensation']} por un momento. Luego pasa.",
                f"Algo cambió, pero no estás seguro de qué."
            ]
        }
        
        # Seleccionar template
        event_key = seed.get("event", "perturbación menor")
        sentences = templates.get(event_key, templates["perturbación menor"])
        
        # Combinar 2-3 frases
        if event.severity.value in ["critical", "catastrophic"]:
            return " ".join(sentences)
        elif event.severity.value in ["major"]:
            return " ".join(sentences[:2])
        else:
            return sentences[0]
    
    def generate_with_cascade(
        self, 
        event: Event, 
        context: Optional[Dict] = None
    ) -> str:
        """
        Genera narrativa con cascada cognitiva
        
        Usa modelo pequeño para eventos simples, grande para complejos
        """
        # Determinar complejidad
        complexity = self._calculate_complexity(event)
        
        # Seleccionar modelo
        if complexity < 0.3:
            model = "qwen2.5:0.5b"  # Modelo pequeño
        elif complexity < 0.7:
            model = "qwen2.5:1.5b"  # Modelo medio
        else:
            model = "qwen2.5:3b"    # Modelo grande
        
        # Guardar modelo original
        original_model = self.model_name
        
        # Cambiar modelo temporalmente
        self.model_name = model
        
        try:
            # Generar
            narrative = self.generate(event, context)
        finally:
            # Restaurar modelo original
            self.model_name = original_model
        
        return narrative
    
    def _calculate_complexity(self, event: Event) -> float:
        """
        Calcula complejidad del evento (0-1)
        
        Basado en:
        - Severidad
        - Número de efectos
        - Número de regiones afectadas
        """
        # Factor de severidad
        severity_scores = {
            "minor": 0.1,
            "moderate": 0.3,
            "major": 0.5,
            "critical": 0.7,
            "catastrophic": 0.9
        }
        severity_factor = severity_scores.get(event.severity.value, 0.5)
        
        # Factor de efectos
        effects_factor = min(1.0, len(event.effects) / 5.0)
        
        # Factor de regiones
        regions_factor = min(1.0, len(event.affected_regions) / 4.0)
        
        # Combinar
        complexity = (
            severity_factor * 0.5 +
            effects_factor * 0.3 +
            regions_factor * 0.2
        )
        
        return complexity
    
    def generate_batch(
        self, 
        events: list[Event], 
        context: Optional[Dict] = None
    ) -> list[str]:
        """
        Genera narrativas para múltiples eventos
        
        Útil para eventos simultáneos o secuenciales
        """
        narratives = []
        
        for event in events:
            narrative = self.generate(event, context)
            narratives.append(narrative)
        
        return narratives
    
    def generate_continuation(
        self,
        previous_narrative: str,
        new_event: Event,
        context: Optional[Dict] = None
    ) -> str:
        """
        Genera continuación de narrativa previa
        
        Mantiene coherencia con eventos anteriores
        """
        seed = new_event.narrative_seed
        
        # Prompt con contexto previo
        prompt = f"""Narrativa previa: {previous_narrative}

Nuevo evento: {seed['event']}
Severidad: {seed['severity_text']}
Región: {seed['region']}

Continúa la narrativa en 2 frases, manteniendo coherencia."""
        
        try:
            response = self._call_ollama(prompt, max_tokens=100)
            return response.strip()
        except Exception:
            return self._generate_procedural(new_event)
    
    def test_connection(self) -> bool:
        """
        Prueba conexión con Ollama
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_available_models(self) -> list[str]:
        """
        Obtiene lista de modelos disponibles en Ollama
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception:
            return []
