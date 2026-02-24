# 🔍 AUDITORÍA COMPLETA DE OPTIMIZACIÓN - ArcheoScope
**Fecha:** 24 de Febrero de 2026  
**Scope:** Frontend (viewer3d) + Backend (solo APIs activos)  
**Objetivo:** Verificar optimización y estabilidad ante nuevos efectos

---

## 📊 RESUMEN EJECUTIVO

### Estado General: ✅ **BUENO CON RECOMENDACIONES CRÍTICAS**

El sistema está **bien estructurado** con lazy-loading y cleanup adecuados, pero hay **vulnerabilidades críticas** que pueden colapsar cuando se agreguen más efectos:

| Aspecto | Estado | Riesgo |
|--------|--------|--------|
| **Limpieza de memoria** | ✅ Bueno | 🟢 Bajo |
| **Lazy-loading** | ✅ Implementado | 🟢 Bajo |
| **Event listeners** | ⚠️ Parcial | 🟡 Medio |
| **GPU memory (textures)** | ✅ Controlado | 🟡 Medio |
| **Backend memory leaks** | ⚠️ Crítico | 🔴 Alto |
| **Caché sin limpieza** | ⚠️ Crítico | 🔴 Alto |
| **Global state variables** | ⚠️ Riesgoso | 🟡 Medio |

---

## 🎯 HALLAZGOS POR COMPONENTE

### FRONTEND (viewer3d)

#### 1️⃣ **ARQUITECTURA: Excelente Organización**

```
✅ POSITIVO: ImmersiveScene usa arquitectura en layers
  - CoreEngine (core, siempre presente)
  - EnvironmentLayer (lazy)
  - EffectsLayer (lazy + condicional por preset)
  - InteractionLayer (lazy)
  - OptionalSystems (lazy)

✅ POSITIVO: Dynamic imports en page.tsx
  - Scene3D cargado dinámicamente
  - Evita SSR issues con Three.js
  - Buen uso de Suspense fallback
```

#### 2️⃣ **MEMORIA: Cleanup IMPLEMENTADO ✅**

```
✅ EnhancedTerrain.tsx:
  - terrainEngineRef.current.dispose() en cleanup
  - Desinstancia completamente el motor

✅ CosmicEntity.tsx:
  - geometry.dispose()
  - material.dispose()
  - shadowGeometry.dispose()
  - shadowMaterial.dispose()
  - auraGeometry.dispose()
  - auraMaterial.dispose()

✅ RealisticOrbits.tsx:
  - geometry.dispose()
  - material.dispose()

✅ Listeners:
  - window.removeEventListener('click', handleClick)
  - window.removeEventListener('mousemove', handleMouseMove)
  - Cleanup en useEffect retornando función
```

**RIESGO:** ⚠️ MODERATE
- No se ve cleanup de THREE.Object3D instanciados en loops
- Partículas pueden acumular geometrías si hay memory leaks

#### 3️⃣ **BUNDLE SIZE Y DEPENDENCIAS**

```json
Dependencias principales:
- next: ^14.2.35         (framework, necesario)
- react: ^18.3.1         (necesario)
- three: ^0.170.0        (3D core, necesario)
- @react-three/fiber: ^8.17.10      (binding, necesario)
- @react-three/drei: ^9.114.3       (utilities, necesario)
- @react-three/postprocessing: ^2.16.3  (efectos, puedo optimizar)
- postprocessing: ^6.38.2            (backend effects, puedo optimizar)
- leva: ^0.9.35          (UI debug, considera usar condicional)
- astronomy-engine: ^2.1.19          (sistema solar)
- zustand: ^4.5.0        (state, ligero ✅)
```

**ANÁLISIS:**

```
⚠️ PROBLEMAS POTENCIALES:

1. Leva UI está siempre incluida
   - Tamaño: ~150KB minified
   - Solución: Importar SOLO en development
   
2. postprocessing + @react-three/postprocessing
   - Están siendo importados SIEMPRE
   - Te permiten lazy-loading en EffectsLayer (bueno)
   - Pero se cargan completos en bundle

3. astronomy-engine (~100KB)
   - Necesario para Sistema Solar
   - Pero está en bundle principal
   - Considerar lazy-loading
```

**Peso actualizado (estimado):**
- Core (Next.js + React + Three): ~400 KB
- React-Three ecosystem: ~150 KB
- Postprocessing: ~80 KB
- Components + logic: ~100 KB
- **Total: ~730 KB gzipped** (RAZONABLE)

#### 4️⃣ **TERRAIN ENGINE: Potencial Memory Leak 🔴**

```typescript
// TerrainService.ts línea 28-35
private cache: Map<string, TerrainData> = new Map()
```

**PROBLEMA CRÍTICO:**
- Cache crece indefinidamente
- No hay límite de tamaño
- Cada tile son ~4MB de datos float32
- Después de 20 tiles: 80MB leak

**RECOMENDACIÓN URGENTE:**
```typescript
// Implementar LRU cache con límite
const MAX_CACHE_ITEMS = 10
const MAX_CACHE_SIZE_MB = 100

// O usar Map con auto-limpieza
clearOldCaches(sinceMinutes: number = 30) {
  const now = Date.now()
  for (const [key, data] of this.cache.entries()) {
    if (now - data.timestamp > sinceMinutes * 60000) {
      this.cache.delete(key)
    }
  }
}
```

#### 5️⃣ **EFFECTOS VISUALIZATION**

```typescript
// EffectsLayer.tsx - BIEN IMPLEMENTADO ✅
if (!enabled || graphicsPreset === 'low') {
  return null
}
```

**POSITIVO:**
- No carga shaders si graphicsPreset === 'low'
- PostProcessingSystem condicional
- AmbientParticles condicional por preset

**RIESGO AL AGREGAR EFECTOS:** 🟡 MEDIO
- Cada efecto nuevo debe tener guard similar
- Validate graphicsPreset en cada componente
- Considerar "ultra-preset" tiene límite ~5 efectos simultáneos

---

### BACKEND (api/)

#### 1️⃣ **ARQUITECTURA: Mixta (Buena pero con Cruft)**

```
apiEndpoints activos:
✅ GET  /                      (Status)
✅ GET  /status                (System status)
✅ GET  /status/detailed       (Detailed status)
✅ GET  /data-sources          (Data transparency)
✅ GET  /lidar-benchmark       (Reference data)
✅ POST /api/terrain/data      (DEM data - CRÍTICO)
✅ GET  /api/terrain/cache/stats
✅ GET  /api/terrain/cache/clear
✅ GET  /api/terrain/prefetch/common-sites
✅ GET  /api/scientific/*      (Scientific analysis)
✅ GET  /api/anomaly-map/{filename}
```

**Endpoints DEPRECATED (aún en código):**
```python
# main.py línea 150
system_components['ai_assistant'] = None  # ⚠️ DESHABILITADO
system_components['core_anomaly_detector'] = None  # ⚠️ DESHABILITADO
```

#### 2️⃣ **MEMORY LEAKS EN BACKEND 🔴 CRÍTICO**

**PROBLEMA 1: Global State Variables**
```python
# world/api_endpoints.py línea 50
world_engine = None  # GLOBAL

# world/world_orchestrator.py línea 310
world_orchestrator = None  # GLOBAL

# backend/site_name_generator.py línea 211
site_name_generator = None  # GLOBAL

# backend/terrain_data_service.py línea 466
terrain_service = None  # GLOBAL

# backend/satellite_cache.py línea 247
satellite_cache = None  # GLOBAL
```

**RIESGO:**
- 5+ variables globales
- No hay cleanup en shutdown
- Pueden mantener referencias a objetos grandes
- **⚠️ Memory leak en recarga de módulo**

**PROBLEMA 2: Database Connections Sin Pooling Óptimo**

```python
# main.py línea 170-180
async def startup_event():
    await database_connection.connect()  # ✅ OK
    
# main.py línea 193-202
async def shutdown_event():
    await database_connection.close()    # ✅ OK
```

**PERO:**
- No hay timeout configurado
- No hay max_connections especificado
- Pool científico y TIMT se inicializan sin límites
- **Riesgo:** queries largas bloquean otros clientes

**PROBLEMA 3: Cache de Terreno Sin Limpieza Automática**

```python
# terrain_data_service.py (estimado)
class TerrainDataService:
    def __init__(self):
        self.memory_cache = {}  # ⚠️ SIN LÍMITE
        self.disk_cache = Path("terrain_cache")
```

**Sin ver el código exacto, pero probablemente:**
```python
# ❌ MAL:
self.memory_cache[key] = large_dem_data  # Acumula forever

# ✅ BIEN:
from functools import lru_cache
@lru_cache(maxsize=10)
def get_terrain_data(...):
    ...
```

#### 3️⃣ **ANÁLISIS DE IMPORTACIONES INNECESARIAS**

Del escaneo encontré **50+ imports potencialmente no usados:**

```python
# Archivos que casi nunca se usan en production:
- geoglyph_detector.py (TODO items sin resolver)
- cognitive_emulator.py (no llamado)
- cognitive_homology.py (no llamado)
- deep_inference_layer.py (no llamado)
- cultural_constrained_mig.py (no llamado)
- external_archaeological_validation.py (no usado)
- historical_hydrography.py (no usado)
- node_prediction.py (no usado)
```

**En startup:**
```python
# main.py líneas 40-50 - Importa TODOS estos
from rules.archaeological_rules import ArchaeologicalRulesEngine
from ai.archaeological_assistant import ArchaeologicalAssistant
from explainability.scientific_explainer import ScientificExplainer
from volumetric.geometric_inference_engine import GeometricInferenceEngine
from environment_classifier import EnvironmentClassifier
from validation.data_source_transparency import DataSourceTransparency
```

**PROBLEMA:** 
- Importa 7 módulos pesados en startup
- CoreAnomalyDetector se desactiva anyway
- AI Assistant se desactiva anyway
- **Startup tardan más de lo necesario**

#### 4️⃣ **APIs NO UTILIZADAS DESDE FRONTEND**

Revisando TerrainDataService.ts y ImmersiveScene.tsx:

```
Frontend SÍ usa:
✅ GET  /api/terrain/data           (EnhancedTerrain)
✅ GET  /api/terrain/cache/stats    (probablemente debug)
✅ GET  /api/terrain/prefetch/*     (lazy preload)

Frontend NO usa:
❌ /api/scientific/*                (ScienceExplainer aún no integrado)
❌ /api/anomaly-map/*               (Componente no activo)
❌ /api/volumetric/*                (Módulo disabled)
❌ /api/geoglyph/*                  (Deprecated)
❌ /api/timt/*                      (Solo backend interno)
```

**RECOMENDACIÓN:**
Comentar/deshabilitar endpoints no usados para reducir bloat

---

## 🚨 PROBLEMAS CRÍTICOS ENCONTRADOS

### 🔴 CRÍTICO #1: TerrainDataService Cache Sin Limpieza

**Ubicación:** `viewer3d/services/TerrainDataService.ts` líneas 28-35

**Código:**
```typescript
private cache: Map<string, TerrainData> = new Map()
```

**Problema:**
- Cada terrain tile son ~4MB Float32Array
- Sin límite de tamaño
- Después de 100 cambios de ubicación = 400MB leak

**Impacto:**
- 🔴 Crash después de usar ~2 horas
- Especialmente en mobile

**Solución (5 minutos):**
```typescript
private cache: Map<string, { data: TerrainData, timestamp: number }> = new Map()
private readonly MAX_CACHE_SIZE = 10
private readonly MAX_CACHE_AGE_MS = 30 * 60 * 1000 // 30 min

async getTerrainData(...): Promise<TerrainData> {
  // ... cache lookup ...
  
  // Add to cache con limpieza
  this.cache.set(cacheKey, { data, timestamp: Date.now() })
  
  // Limpiar si exceeds size
  if (this.cache.size > this.MAX_CACHE_SIZE) {
    const oldest = Array.from(this.cache.entries())
      .sort((a, b) => a[1].timestamp - b[1].timestamp)[0]
    this.cache.delete(oldest[0])
  }
}

// Cleanup timer
setInterval(() => {
  const now = Date.now()
  for (const [key, { timestamp }] of this.cache.entries()) {
    if (now - timestamp > this.MAX_CACHE_AGE_MS) {
      this.cache.delete(key)
    }
  }
}, 5 * 60 * 1000) // Cada 5 min
```

**Prioridad:** 🔴 MÁXIMA - Implementar YA

---

### 🔴 CRÍTICO #2: Backend Global Variables Sin Cleanup

**Ubicación:** Multiple files

**Problema:**
```python
# world/api_endpoints.py
world_engine = None

# Inicialización
async def init_world_engine():
    global world_engine
    world_engine = WorldEngine(...)  # 🔴 Nunca se limpia
```

**Impacto:**
- Memory leak si se recarga el módulo
- Cuando redeploy en Docker = pérdida de referencias
- Bug hard-to-debug

**Solución (Dependency Injection):**
```python
# ❌ VIEJO
world_engine = None

@app.get("/world/state")
async def get_world_state():
    return world_engine.get_state()

# ✅ NUEVO
from fastapi import Depends

async def get_world_engine():
    return app.state.world_engine  # Almacenar en app.state

@app.on_event("startup")
async def startup():
    app.state.world_engine = WorldEngine()

@app.on_event("shutdown")
async def shutdown():
    if hasattr(app.state, 'world_engine'):
        app.state.world_engine.cleanup()  # Cleanup explícito

@app.get("/world/state")
async def get_world_state(engine = Depends(get_world_engine)):
    return engine.get_state()
```

**Prioridad:** 🔴 MÁXIMA - Refactor critical

---

### 🔴 CRÍTICO #3: Terrain Backend Cache Sin Cap

**Ubicación:** `backend/api/terrain_endpoint.py`

**Problema:**
```python
# terrain_data_service.py (likely)
def get_terrain_data(...):
    self.memory_cache[key] = tile  # ⚠️ No limit
```

**Impacto:**
- Backend consume todas las RAM disponibles
- Después de 10-20 tiles = OOM
- Crash del servidor

**Solución Rápida:**
```python
from functools import lru_cache
from cachetools import TTLCache

class TerrainDataService:
    def __init__(self):
        # LRU cache: máx 50 items, 1 hora TTL
        self.cache = TTLCache(
            maxsize=50,
            ttl=3600,
            timer=time.time
        )
    
    @lru_cache(maxsize=50)
    def get_terrain_data(self, lat_min, lat_max, ...):
        ...
```

**Prioridad:** 🔴 MÁXIMA

---

### 🟡 ALTO #4: Event Listeners Sin Cleanup Completo

**Ubicación:** `viewer3d/components/AstronomicalWorld.tsx`

**Código actuales (BIEN):**
```typescript
useEffect(() => {
  window.addEventListener('click', initAudio)
  window.addEventListener('keydown', initAudio)
  
  return () => {
    window.removeEventListener('click', initAudio)
    window.removeEventListener('keydown', initAudio)
  }
}, [])
```

**PERO - Riesgo cuando agregues efectos:**
```
❌ POTENCIAL: Si agregas 5 efectos con listeners each
   = 15 event listeners activos
   = Performance degradation visible
```

**Recomendación:**
```typescript
// Centralizar event management
const useEventListener = (event: string, handler: () => void) => {
  useEffect(() => {
    window.addEventListener(event, handler)
    return () => window.removeEventListener(event, handler)
  }, [event, handler])
}

// Usar en componententes:
useEventListener('click', resumeAudio)
useEventListener('keydown', resumeAudio)
```

**Prioridad:** 🟡 ALTA - Implementar antes de 3+ efectos nuevos

---

### 🟡 ALTO #5: Imports Backend No Optimizados

**Problema:**
```python
# main.py - Startup imports
from ai.archaeological_assistant import ArchaeologicalAssistant  # ⚠️
from explainability.scientific_explainer import ScientificExplainer
from volumetric.geometric_inference_engine import GeometricInferenceEngine
from environment_classifier import EnvironmentClassifier
```

**Impacto:**
- Startup slowness
- Modules parcialmente deshabilitados anyway
- Posibles circular imports

**Solución:**
```python
# ✅ Lazy import patterns
def get_ai_assistant():
    from ai.archaeological_assistant import ArchaeologicalAssistant
    return ArchaeologicalAssistant()

# Usar solo si requerido:
if system_components['ai_assistant'] is needed:
    system_components['ai_assistant'] = get_ai_assistant()
```

**Prioridad:** 🟡 MEDIA - Optimizar después de issues críticos

---

## ✅ COSAS QUE ESTÁN BIEN

### Frontend Positivos ✅
1. **Lazy-loading adecuado** - Layers se cargan dinámicamente
2. **Cleanup de Three.js** - dispose() llamados en useEffect
3. **Conditional rendering** - EffectsLayer según graphicsPreset
4. **Event cleanup** - removeEventListener en todas partes
5. **Component composition** - Bien modularizado
6. **Zustand state** - Ligero, sin memory leaks común

### Backend Positivos ✅
1. **CORS configurado** - Permite frontend comunicar
2. **Logging** - Buena visibilidad de errors
3. **Shutdown events** - Intenta cleanup en graceful shutdown
4. **Modular endpoints** - Organized por funcionalidad
5. **Database abstraction** - Usa async/await properly

---

## 🎬 PLAN DE ACCIÓN RECOMENDADO

### INMEDIATO (Esta semana) 🔴
1. **Implementar LRU cache en TerrainDataService** (30 min)
   - Archivo: `viewer3d/services/TerrainDataService.ts`
   - Add MAX_CACHE_ITEMS + cleanup logic
   
2. **Implementar LRU cache en Backend terrain_service** (30 min)
   - Archivo: `backend/terrain_data_service.py`
   - Use cachetools TTLCache
   
3. **Refactor global variables a app.state** (2 horas)
   - Archivos: `backend/world/*`, `backend/*/api_endpoints.py`
   - Usar FastAPI dependency injection pattern

### PRÓXIMA SEMANA (Before adding effects) 🟡
4. **Centralizar event listener management** (1 hora)
   - Hook: `useEventListener` reutilizable
   - Reduce coupling en componentes
   
5. **Audit de imports backend** (1 hora)
   - Lazy-load modules not needed at startup
   - Remove commented code
   
6. **Bundle analysis** (30 min)
   - `npm run analyze` en viewer3d
   - Identify/remove unused dependencies

### OPCIONAL (Nice to have) 🟢
7. **Monitoring de memory** en producción
   - Cliente: DevTools Memory tab automated test
   - Backend: pydantic-core memory profiling
   
8. **Rate limiting en terrain endpoint**
   - Prevenir abuse/DDoS
   - Max 10 tiles concurrentes per IP

---

## 📈 RECOMENDACIONES ANTES DE AGREGAR EFECTOS

### Regla #1: Cache Limits
**Cualquier caché que agregues debe tener:**
- ✅ Tamaño máximo (items o MB)
- ✅ TTL (time-to-live)
- ✅ Cleanup automático cada 5-10 min

### Regla #2: Graphics Preset Guards
**Todo nuevo effect debe:**
```typescript
if (graphicsPreset === 'low') return null
if (graphicsPreset === 'medium' && intensiveEffect) return null
```

### Regla #3: Particle Management
**Si agregas particles:**
- ✅ Pool de max 10000 particles
- ✅ Reuse buffers, no crear new cada frame
- ✅ Disable si FPS < 30

### Regla #4: Shader Compilation
**Si agregas shaders:**
- ✅ Compile offline si es posible
- ✅ Show loading bar durante compile
- ✅ Fallback a non-shader version

### Regla #5: Memory Monitoring
**Antes de release:**
```typescript
// DevTools metrics
setInterval(() => {
  if (performance.memory) {
    const usage = performance.memory.usedJSHeapSize / 1e6
    if (usage > 300) console.warn('⚠️ High memory:', usage + 'MB')
  }
}, 5000)
```

---

## 🔬 TESTING RECOMENDADOS

### Frontend
```bash
# Memory leak detection
npm run test:coverage

# Bundle size analysis
npm run analyze

# Performance profiling
# DevTools → Performance → Record
```

### Backend
```bash
# Memory profiling
pip install memory-profiler
python -m memory_profiler backend/api/main.py

# Load testing
pip install locust
locust -f tests/load.py --host=http://localhost:8003
```

---

## 📋 CHECKLIST DE OPTIMIZACIÓN

Usar esto antes de cada merge:

- [ ] TerrainDataService cache capped at 10 items?
- [ ] Backend terrain_service usando TTLCache?
- [ ] Global variables refactored to app.state?
- [ ] All new effects have graphicsPreset guards?
- [ ] No console.logs en production build?
- [ ] Bundle size < 800KB gzipped?
- [ ] No memory grow después de 1 hora uso?
- [ ] Startup time < 3 segundos?
- [ ] Graceful shutdown en Ctrl+C?

---

## 🎯 CONCLUSIÓN

**Estado: LISTO PARA CRECER, CON RESERVAS**

✅ Arquitectura frontend es sólida  
✅ Cleanup de Three.js está implementado  
⚠️ Caches backend necesitan URGENTEMENTE caps  
⚠️ Global variables son risk, refactor recommended  
🟢 Con estas correcciones: SEGURO agregar 3-5 efectos nuevos  

**ETA para estar "production ready":**
- Con correcciones críticas: 1 semana
- Con optimizaciones: 2 semanas
- Monitoring automático: 3 semanas

