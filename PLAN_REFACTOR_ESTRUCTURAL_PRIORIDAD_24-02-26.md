# 🏗️ Plan de Refactorización Estructural - Prioridad Alta

**Fecha:** 24 de Febrero 2026  
**Estado Actual:** 7/10 - Buena calidad técnica, falta madurez estructural  
**Meta:** 9/10 - Arquitectura de plataforma seria

---

## 📊 Diagnóstico Real

### ✅ Lo que TIENES (Fortalezas)
- 70+ componentes frontend
- 6 engines modulares
- 100+ módulos backend
- Conectores satelitales
- TF + PyTorch en memoria
- LOD + Instancing + Lazy loading
- 60 FPS estables
- Sistema de resonancia implementado
- WorldManager con gobernanza

### ⚠️ Lo que FALTA (Deuda Técnica)
- 70 componentes en carpeta plana (sin dominio)
- Backend 0% testing
- Componentes deshabilitados (AI Assistant, CoreAnomalyDetector)
- Memoria alta (TF + PyTorch cargados permanentemente)
- Falta Event Bus global
- Falta separación clara de capas

---

## 🚨 PRIORIDAD 1: Estructura por Dominio (NO por tipo)

### ❌ Estructura Actual (Plana)
```
viewer3d/components/
  ├── Button.tsx
  ├── Globe3D.tsx
  ├── WeatherControl.tsx
  ├── AnomalyVisualization.tsx
  ├── ResonanceDemo.tsx
  ├── ... (70+ archivos)
```

**Problema:** Escala mal, difícil de mantener

---

### ✅ Estructura Propuesta (Por Dominio)

```
viewer3d/
├── app/                    # Routing, layout, bootstrap
│   ├── page.tsx
│   ├── layout.tsx
│   └── realistic-solar/
│
├── features/               # Dominios de gameplay
│   ├── globe/
│   │   ├── Globe3D.tsx
│   │   ├── GlobeScene.tsx
│   │   ├── SiteMarkers.tsx
│   │   ├── GlobeLOD.ts
│   │   └── GlobeShaders.ts
│   │
│   ├── weather/
│   │   ├── WeatherControl.tsx
│   │   ├── WeatherSystem.tsx
│   │   ├── ClimateAudioSystem.ts
│   │   └── effects/
│   │       ├── RainEffect.tsx
│   │       ├── WindEffect.tsx
│   │       └── LightningEffect.tsx
│   │
│   ├── anomalies/
│   │   ├── AnomalyManager.ts
│   │   ├── AnomalyVisualization.tsx
│   │   ├── ResonanceSystem.ts
│   │   └── ResonanceDemo.tsx
│   │
│   ├── player/
│   │   ├── WalkableAvatar.tsx
│   │   ├── SpaceUfo.tsx
│   │   ├── PlayerControls.ts
│   │   └── CameraSystem.ts
│   │
│   ├── terrain/
│   │   ├── ProceduralTerrain.tsx
│   │   ├── VolcanicTerrain.tsx
│   │   ├── IceTerrain.tsx
│   │   ├── EnhancedTerrain.tsx
│   │   └── TerrainControl.tsx
│   │
│   ├── ui/
│   │   ├── CoordinateInput.tsx
│   │   ├── LocationInfo.tsx
│   │   ├── AudioControl.tsx
│   │   └── HUD/
│   │
│   └── solar-system/
│       ├── RealisticSolarSystem.tsx
│       ├── planets/
│       └── orbits/
│
├── engines/                # Lógica pura (NO React)
│   ├── GlobeEngine.ts
│   ├── PhysicsEngine.ts
│   ├── ResonanceEngine.ts  # ← NUEVO: Transversal
│   ├── AudioEngine.ts
│   ├── WorldManager.ts
│   └── WorldCore/
│
├── systems/                # Sistemas transversales
│   ├── audio/
│   │   ├── ProceduralAudio.ts
│   │   ├── ClimateAudioSystem.ts
│   │   └── ResonanceAudioAdapter.ts
│   │
│   ├── rendering/
│   │   ├── LightingSystem.tsx
│   │   ├── PostProcessingSystem.tsx
│   │   └── CullingSystem.ts
│   │
│   └── physics/
│       └── CollisionSystem.ts
│
├── shared/                 # Utils, hooks, types
│   ├── hooks/
│   ├── utils/
│   ├── types/
│   └── constants/
│
└── core/                   # Core framework
    ├── Logger.ts
    └── EventBus.ts         # ← NUEVO
```

**Beneficio:** Dominio > Tipo = Escalabilidad

---

## 🚨 PRIORIDAD 2: Event Bus Global

### Problema Actual
Sistemas se llaman directamente:
```typescript
// ❌ Acoplamiento directo
climateAudio.updateWithResonance(deltaTime)
shaderSystem.setResonance(value)
physicsEngine.applyResonance(value)
```

### Solución: Event Bus

**Crear:** `viewer3d/core/EventBus.ts`

```typescript
/**
 * EventBus - Sistema de eventos global
 * Desacopla sistemas completamente
 */

type EventCallback = (data: any) => void

class EventBus {
  private events: Map<string, EventCallback[]> = new Map()
  
  on(event: string, callback: EventCallback): void {
    if (!this.events.has(event)) {
      this.events.set(event, [])
    }
    this.events.get(event)!.push(callback)
  }
  
  off(event: string, callback: EventCallback): void {
    const callbacks = this.events.get(event)
    if (callbacks) {
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }
  
  emit(event: string, data?: any): void {
    const callbacks = this.events.get(event)
    if (callbacks) {
      callbacks.forEach(cb => cb(data))
    }
  }
}

export const eventBus = new EventBus()
```

**Uso:**
```typescript
// ResonanceEngine emite
eventBus.emit('RESONANCE_UPDATE', { value: 0.5, stability: 0.8 })

// Audio escucha
eventBus.on('RESONANCE_UPDATE', (data) => {
  climateAudio.updateWithResonance(data.value)
})

// Shader escucha
eventBus.on('RESONANCE_UPDATE', (data) => {
  shaderSystem.setResonance(data.value)
})

// Physics escucha
eventBus.on('RESONANCE_UPDATE', (data) => {
  physicsEngine.applyResonance(data.value)
})
```

**Beneficio:** Desacoplamiento total

---

## 🚨 PRIORIDAD 3: Separar IA Pesada

### Problema Actual
```python
# backend/main.py
# ❌ TF + PyTorch cargados al iniciar
model_tf = load_tensorflow_model()
model_pytorch = load_pytorch_model()
```

**Impacto:** Memoria alta, startup lento

### Solución: Microservicio de IA

**Arquitectura propuesta:**

```
┌─────────────────────────────────────┐
│   FastAPI Main Server (Ligero)     │
│   - API endpoints                   │
│   - DB queries                      │
│   - Coordinación                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   AI Microservice (Pesado)         │
│   - TensorFlow                      │
│   - PyTorch                         │
│   - Inference on-demand             │
│   - Puerto: 8001                    │
└─────────────────────────────────────┘
```

**Implementación:**

```python
# backend/services/ai_service.py
import httpx

class AIService:
    def __init__(self):
        self.ai_url = "http://localhost:8001"
    
    async def detect_anomaly(self, image_data):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.ai_url}/detect",
                json={"image": image_data}
            )
            return response.json()
```

**Beneficio:** Memoria reducida, startup rápido

---

## 🚨 PRIORIDAD 4: Testing Mínimo Viable (Backend)

### Meta Realista
- ❌ NO intentar 100% coverage
- ✅ SÍ testear módulos críticos

### Tests Prioritarios

**1. Anomaly Logic**
```python
# backend/tests/test_anomaly_logic.py
def test_resonance_calculation():
    anomaly = Anomaly(position=(0,0,0), radius=10, intensity=0.5)
    resonance = anomaly.get_resonance_at((5, 0, 0))
    assert -1 <= resonance <= 1

def test_falloff():
    anomaly = Anomaly(position=(0,0,0), radius=10, intensity=1.0)
    # En el centro
    assert anomaly.get_resonance_at((0,0,0)) == 1.0
    # En el borde
    assert anomaly.get_resonance_at((10,0,0)) == 0.0
```

**2. Core API Endpoints**
```python
# backend/tests/test_api.py
from fastapi.testclient import TestClient

def test_get_anomalies():
    response = client.get("/api/anomalies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_anomaly():
    data = {"position": [0,0,0], "radius": 10}
    response = client.post("/api/anomalies", json=data)
    assert response.status_code == 201
```

**3. DB Queries Críticas**
```python
# backend/tests/test_database.py
def test_save_anomaly():
    anomaly = create_anomaly(...)
    saved = db.save(anomaly)
    assert saved.id is not None

def test_query_anomalies_in_radius():
    anomalies = db.query_in_radius(center=(0,0,0), radius=100)
    assert len(anomalies) > 0
```

**Setup:**
```bash
pip install pytest pytest-asyncio pytest-cov
pytest --cov=backend --cov-report=html
```

**Meta:** 40-50% coverage en módulos críticos

---

## 🚨 PRIORIDAD 5: Limpiar Componentes Deshabilitados

### Componentes Identificados
- `AIAssistant` (deshabilitado)
- `CoreAnomalyDetector` (deshabilitado)

### Decisión Requerida

**Opción A: Eliminar**
```bash
# Si no se usan y no hay plan claro
rm -rf viewer3d/components/AIAssistant.tsx
rm -rf backend/ai/core_anomaly_detector.py
```

**Opción B: Estabilizar**
```typescript
// Si se van a usar, moverlos a features/ai/
viewer3d/features/ai/
  ├── AIAssistant.tsx
  ├── CoreAnomalyDetector.ts
  └── README.md  # Documentar estado y plan
```

**Opción C: Feature Flag**
```typescript
// Si son experimentales
const FEATURES = {
  AI_ASSISTANT: false,
  CORE_ANOMALY: false
}

{FEATURES.AI_ASSISTANT && <AIAssistant />}
```

**Regla:** Código muerto = deuda conceptual

---

## 📋 Plan de Implementación (Orden Sugerido)

### Fase 1: Fundamentos (1-2 días)
1. ✅ Crear EventBus
2. ✅ Crear estructura de carpetas por dominio
3. ✅ Mover componentes a features/ (gradual)
4. ✅ Actualizar imports

### Fase 2: Backend (1 día)
5. ✅ Setup pytest
6. ✅ Tests de anomaly logic
7. ✅ Tests de API endpoints
8. ✅ Tests de DB queries

### Fase 3: Optimización (1 día)
9. ✅ Separar IA en microservicio (opcional)
10. ✅ Limpiar componentes deshabilitados
11. ✅ Documentar decisiones

### Fase 4: Integración (1 día)
12. ✅ Integrar EventBus en ResonanceEngine
13. ✅ Refactorizar llamadas directas
14. ✅ Testing de integración

**Tiempo total:** 4-5 días

---

## 🎯 Resultado Esperado

### De 7/10 a 9/10

**Antes:**
- ❌ 70 componentes planos
- ❌ 0% testing backend
- ❌ Acoplamiento directo
- ❌ IA pesada siempre cargada
- ❌ Código muerto

**Después:**
- ✅ Estructura por dominio
- ✅ 40-50% coverage en críticos
- ✅ EventBus desacoplado
- ✅ IA en microservicio
- ✅ Código limpio

---

## 🧠 Filosofía del Refactor

### Reglas de Oro

1. **Dominio > Tipo**
   - Organizar por qué hace, no qué es

2. **Engines NO dependen de React**
   - React depende de engines

3. **Event Bus para comunicación**
   - No llamadas directas entre sistemas

4. **Testing mínimo viable**
   - 40-50% en críticos, no 100%

5. **Separar IA pesada**
   - Microservicio o lazy loading

6. **Eliminar código muerto**
   - O estabilizar con plan claro

---

## 📊 Métricas de Éxito

### Performance
- ✅ 60 FPS estables (ya tienes)
- ✅ Memoria < 500MB
- ✅ Startup < 3s

### Arquitectura
- ✅ Estructura por dominio
- ✅ EventBus implementado
- ✅ Engines desacoplados

### Testing
- ✅ 40-50% coverage backend
- ✅ Tests de lógica crítica
- ✅ CI básico

### Código
- ✅ Sin componentes deshabilitados
- ✅ Sin código muerto
- ✅ Documentación clara

---

## 🚀 Próximo Paso Inmediato

**NO agregar features nuevas.**

**SÍ hacer refactor estructural:**

1. Crear EventBus (30 min)
2. Crear estructura features/ (1 hora)
3. Mover 5 componentes clave (2 horas)
4. Setup pytest (30 min)
5. Escribir 3 tests críticos (1 hora)

**Total:** 1 día de trabajo

**Resultado:** Fundamentos sólidos para escalar

---

## 💡 Conclusión

Tu proyecto ya tiene:
- ✅ Stack ambicioso
- ✅ Calidad técnica
- ✅ Features interesantes

Lo que falta:
- ⚠️ Madurez estructural
- ⚠️ Testing básico
- ⚠️ Desacoplamiento

**Con este refactor:** 7/10 → 9/10

**Sin este refactor:** Deuda técnica creciente

---

**Creado por:** Kiro AI  
**Basado en:** Diagnóstico de arquitectura real  
**Prioridad:** ALTA  
**Tiempo estimado:** 4-5 días  
**ROI:** Escalabilidad a largo plazo
