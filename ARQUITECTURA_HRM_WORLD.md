# 🧠 ARQUITECTURA HRM-WORLD: Motor Cognitivo Jerárquico para Mundo 3D

**Fecha**: 19 de febrero de 2026  
**Rama**: `hrmBackendWorld`  
**Estado**: 🚧 EN DESARROLLO

---

## 🎯 VISIÓN

Transformar el mundo 3D de ArcheoScope en un **sistema emergente con razonamiento jerárquico**, donde:

- El **HRM (27M parámetros)** analiza el estado estructurado del mundo
- El **LLM (Qwen 3B)** solo narra los eventos
- Los eventos emergen de la dinámica del sistema, no de scripts

---

## 🧩 PROBLEMA ACTUAL

### Lo que tenemos hoy
```
Jugador actúa → LLM genera respuesta → Texto
```

**Problemas**:
- ❌ HRM infrautilizado (solo para TIMT, no para mundo 3D)
- ❌ LLM decide todo (alto costo de tokens)
- ❌ No hay emergencia real
- ❌ No hay memoria estructural del mundo

### Lo que queremos
```
Jugador actúa → World Engine → HRM analiza → Evento emergente → LLM narra
```

**Beneficios**:
- ✅ HRM razona sobre estado estructurado
- ✅ LLM solo verbaliza (reducción de tokens)
- ✅ Eventos emergentes no programados
- ✅ Mundo con memoria y entropía

---

## 🔥 ARQUITECTURA PROPUESTA

### Pipeline Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    JUGADOR ACTÚA                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              WORLD ENGINE (Three.js)                        │
│  - Posición, clima, bioma, tiempo                           │
│  - Interacciones físicas                                    │
│  - Métricas continuas                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              SYMBOLIZER (Nueva Capa)                        │
│  Convierte métricas continuas → secuencia discreta 0-5      │
│                                                             │
│  world_entropy: 0.63 → token 2                              │
│  climate_vector: [0.4,0.8,0.2] → token 3                    │
│  anomaly_score: 0.81 → token 4                              │
│  player_disruption: 0.55 → token 2                          │
│                                                             │
│  Output: [0,0,2,3,1,1,4,5,2,3,...] (64 tokens)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           HRM (27M params, maze checkpoint)                 │
│  - 2 ciclos H-level / L-level                               │
│  - Detecta patrones jerárquicos                             │
│  - Predice transiciones                                     │
│  - Simula propagación                                       │
│                                                             │
│  Output estructurado:                                       │
│  {                                                          │
│    "world_state_shift": "instability_increase",             │
│    "emergent_event": "electromagnetic_storm",               │
│    "confidence": 0.74,                                      │
│    "instability_level": 0.82,                               │
│    "affected_zones": [2, 3, 8]                              │
│  }                                                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              EVENT INTERPRETER                              │
│  Convierte output HRM → parámetros de evento                │
│                                                             │
│  {                                                          │
│    "event": "magnetic_anomaly",                             │
│    "intensity": 0.82,                                       │
│    "zone": "desierto",                                      │
│    "visibility": "baja",                                    │
│    "duration": 120                                          │
│  }                                                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              MINI LLM (Qwen 3B o 0.5B)                      │
│  Solo narra el evento (20-40 tokens input)                  │
│                                                             │
│  "Una tormenta electromagnética se aproxima desde el        │
│   desierto. La visibilidad es baja. Sientes una extraña    │
│   vibración en el aire..."                                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              WORLD ENGINE (Actualización)                   │
│  - Aplica efectos del evento                                │
│  - Actualiza clima, luz, audio                              │
│  - Modifica entropía acumulativa                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 DISEÑO DE LOS 6 ESTADOS DISCRETOS

### Semántica de Tokens (0-5)

Reinterpretamos los 6 tokens del checkpoint Maze para representar **dinámica del mundo**:

```
0 = ESTABLE
    - Entropía < 0.3
    - Sin anomalías
    - Clima normal
    - Jugador pasivo

1 = TENSIÓN LEVE
    - Entropía 0.3-0.5
    - Anomalías menores
    - Clima cambiante
    - Jugador explorando

2 = TENSIÓN MEDIA
    - Entropía 0.5-0.7
    - Anomalías detectables
    - Clima inestable
    - Jugador activo

3 = INESTABILIDAD ACTIVA
    - Entropía 0.7-0.85
    - Anomalías fuertes
    - Clima hostil
    - Jugador en riesgo

4 = ANOMALÍA
    - Entropía > 0.85
    - Evento emergente
    - Clima extremo
    - Jugador en peligro

5 = TRANSICIÓN / COLAPSO
    - Cambio de estado
    - Propagación activa
    - Umbral crítico
    - Reset inminente
```

### Representación del Mundo

El mundo se divide en **64 zonas conceptuales** (no necesariamente visibles):

```
Zona 0-7   → Región Norte
Zona 8-15  → Región Este
Zona 16-23 → Región Sur
Zona 24-31 → Región Oeste
Zona 32-39 → Región Central
Zona 40-47 → Región Subterránea
Zona 48-55 → Región Atmosférica
Zona 56-63 → Región Temporal
```

Cada zona tiene un estado 0-5 en cada momento.

---

## ⚙️ COMPONENTES TÉCNICOS

### 1. World Metrics Collector

**Ubicación**: `backend/world/metrics_collector.py`

**Responsabilidad**: Recopilar métricas continuas del mundo

```python
class WorldMetricsCollector:
    def collect(self, world_state: WorldState) -> WorldMetrics:
        return {
            "world_entropy": self.calculate_entropy(world_state),
            "climate_vector": self.get_climate_vector(world_state),
            "npc_density": self.calculate_npc_density(world_state),
            "energy_flux": self.calculate_energy_flux(world_state),
            "player_disruption": self.calculate_player_impact(world_state),
            "anomaly_score": self.calculate_anomaly_score(world_state),
            "temporal_drift": self.calculate_temporal_drift(world_state),
            "spatial_coherence": self.calculate_spatial_coherence(world_state)
        }
```

### 2. Symbolizer

**Ubicación**: `backend/world/symbolizer.py`

**Responsabilidad**: Convertir métricas continuas → secuencia discreta 0-5

```python
class WorldSymbolizer:
    def symbolize(self, metrics: WorldMetrics, zones: int = 64) -> List[int]:
        """
        Convierte métricas continuas en secuencia de 64 tokens (0-5)
        """
        sequence = []
        
        for zone_id in range(zones):
            # Calcular estado de la zona
            zone_entropy = self.get_zone_entropy(metrics, zone_id)
            zone_anomaly = self.get_zone_anomaly(metrics, zone_id)
            zone_climate = self.get_zone_climate(metrics, zone_id)
            
            # Clasificar en 0-5
            token = self.classify_zone_state(
                zone_entropy, 
                zone_anomaly, 
                zone_climate
            )
            
            sequence.append(token)
        
        return sequence
    
    def classify_zone_state(self, entropy, anomaly, climate) -> int:
        """
        Clasificación en 6 estados
        """
        if entropy < 0.3 and anomaly < 0.2:
            return 0  # ESTABLE
        elif entropy < 0.5 and anomaly < 0.4:
            return 1  # TENSIÓN LEVE
        elif entropy < 0.7 and anomaly < 0.6:
            return 2  # TENSIÓN MEDIA
        elif entropy < 0.85 and anomaly < 0.8:
            return 3  # INESTABILIDAD ACTIVA
        elif anomaly > 0.8:
            return 4  # ANOMALÍA
        else:
            return 5  # TRANSICIÓN
```

### 3. HRM World Analyzer

**Ubicación**: `backend/world/hrm_analyzer.py`

**Responsabilidad**: Ejecutar HRM sobre secuencia simbólica

```python
class HRMWorldAnalyzer:
    def __init__(self, checkpoint_path: str):
        self.model = load_hrm_model(checkpoint_path)
    
    def analyze(self, symbolic_sequence: List[int], cycles: int = 2) -> Dict:
        """
        Ejecuta HRM con ciclos H-level / L-level
        """
        # Convertir a tensor
        input_tensor = torch.tensor(symbolic_sequence).unsqueeze(0)
        
        # Ejecutar HRM
        with torch.no_grad():
            output = self.model(input_tensor, num_cycles=cycles)
        
        # Analizar output
        analysis = self.interpret_output(output, symbolic_sequence)
        
        return analysis
    
    def interpret_output(self, output, input_seq) -> Dict:
        """
        Interpreta output del HRM
        """
        # Detectar cambios de estado
        state_changes = self.detect_state_changes(output, input_seq)
        
        # Detectar patrones globales
        global_patterns = self.detect_global_patterns(output)
        
        # Calcular confianza
        confidence = self.calculate_confidence(output)
        
        return {
            "world_state_shift": self.classify_shift(state_changes),
            "emergent_event": self.predict_event(global_patterns),
            "confidence": confidence,
            "instability_level": self.calculate_instability(output),
            "affected_zones": self.get_affected_zones(state_changes),
            "propagation_vector": self.calculate_propagation(output)
        }
```

### 4. Event Interpreter

**Ubicación**: `backend/world/event_interpreter.py`

**Responsabilidad**: Convertir output HRM → evento estructurado

```python
class EventInterpreter:
    def interpret(self, hrm_output: Dict) -> Event:
        """
        Convierte análisis HRM en evento concreto
        """
        event_type = self.map_event_type(hrm_output["emergent_event"])
        intensity = hrm_output["instability_level"]
        zones = hrm_output["affected_zones"]
        
        return Event(
            type=event_type,
            intensity=intensity,
            affected_zones=zones,
            duration=self.calculate_duration(intensity),
            effects=self.generate_effects(event_type, intensity),
            narrative_seed=self.create_narrative_seed(event_type, intensity)
        )
```

### 5. Narrative Generator (Mini LLM)

**Ubicación**: `backend/world/narrative_generator.py`

**Responsabilidad**: Generar narrativa del evento (solo verbalización)

```python
class NarrativeGenerator:
    def __init__(self, model_name: str = "qwen2.5:3b"):
        self.llm = Ollama(model=model_name)
    
    def generate(self, event: Event) -> str:
        """
        Genera narrativa corta del evento (20-40 tokens input)
        """
        prompt = f"""Evento: {event.type}
Intensidad: {event.intensity}
Zona: {event.affected_zones[0]}
Duración: {event.duration}s

Narra en 2-3 frases cortas lo que el jugador percibe."""
        
        response = self.llm.generate(prompt, max_tokens=100)
        return response
```

---

## 🔥 MEJORAS AVANZADAS

### 1. Propagación Multi-Step

Ejecutar HRM en **múltiples iteraciones** para simular evolución temporal:

```python
def simulate_propagation(self, initial_state: List[int], steps: int = 5):
    """
    Simula evolución del mundo en múltiples pasos
    """
    states = [initial_state]
    
    for step in range(steps):
        current_state = states[-1]
        next_state = self.hrm_analyzer.analyze(current_state)
        states.append(next_state)
    
    # Detectar emergencia
    emergence = self.detect_emergence(states)
    
    return emergence
```

### 2. Inyección de Perturbaciones

Modificar tokens específicos para simular **impacto del jugador**:

```python
def inject_player_action(self, symbolic_seq: List[int], player_zone: int, action_intensity: float):
    """
    Modifica secuencia según acción del jugador
    """
    # Aumentar inestabilidad en zona del jugador
    symbolic_seq[player_zone] = min(5, symbolic_seq[player_zone] + int(action_intensity * 2))
    
    # Propagar a zonas adyacentes
    for adjacent in self.get_adjacent_zones(player_zone):
        symbolic_seq[adjacent] = min(5, symbolic_seq[adjacent] + 1)
    
    return symbolic_seq
```

### 3. Cascada Cognitiva (Modelo Adaptativo)

Usar **modelo pequeño o grande** según complejidad:

```python
def select_llm_model(self, event_complexity: float) -> str:
    """
    Selecciona modelo según complejidad del evento
    """
    if event_complexity < 0.3:
        return "qwen2.5:0.5b"  # Eventos simples
    elif event_complexity < 0.7:
        return "qwen2.5:1.5b"  # Eventos medios
    else:
        return "qwen2.5:3b"    # Eventos complejos
```

---

## 📊 MÉTRICAS Y MONITOREO

### Métricas del Sistema

```python
class WorldMetrics:
    # Entropía acumulativa (0-1)
    world_entropy: float
    
    # Vector climático [temp, humedad, presión]
    climate_vector: List[float]
    
    # Densidad de NPCs (0-1)
    npc_density: float
    
    # Flujo de energía (0-1)
    energy_flux: float
    
    # Disrupción del jugador (0-1)
    player_disruption: float
    
    # Score de anomalía (0-1)
    anomaly_score: float
    
    # Deriva temporal (0-1)
    temporal_drift: float
    
    # Coherencia espacial (0-1)
    spatial_coherence: float
```

---

## 🚀 ROADMAP DE IMPLEMENTACIÓN

### Fase 1: Fundación (Semana 1)
- [ ] Crear `WorldMetricsCollector`
- [ ] Crear `WorldSymbolizer`
- [ ] Integrar HRM existente
- [ ] Tests unitarios

### Fase 2: Análisis (Semana 2)
- [ ] Implementar `HRMWorldAnalyzer`
- [ ] Implementar `EventInterpreter`
- [ ] Propagación multi-step
- [ ] Tests de emergencia

### Fase 3: Narrativa (Semana 3)
- [ ] Integrar `NarrativeGenerator`
- [ ] Cascada cognitiva
- [ ] Optimización de tokens
- [ ] Tests end-to-end

### Fase 4: Integración (Semana 4)
- [ ] Conectar con World Engine (Three.js)
- [ ] API REST para frontend
- [ ] WebSocket para eventos en tiempo real
- [ ] Deploy y monitoreo

---

## 🎯 BENEFICIOS ESPERADOS

### Performance
- ✅ Reducción de tokens: 80-90% (de 500+ a 20-40)
- ✅ Latencia: 50% menor (modelo pequeño para eventos simples)
- ✅ Costo: 90% menor (menos llamadas a LLM grande)

### Emergencia
- ✅ Eventos no programados
- ✅ Mundo con memoria
- ✅ Propagación realista
- ✅ Escalamiento natural

### Experiencia
- ✅ Mundo vivo y reactivo
- ✅ Consecuencias a largo plazo
- ✅ Narrativa coherente
- ✅ Rejugabilidad infinita

---

**Autor**: Kiro AI Assistant  
**Proyecto**: ArcheoScope 3D Engine  
**Rama**: hrmBackendWorld  
**Estado**: 🚧 Arquitectura definida, implementación pendiente
