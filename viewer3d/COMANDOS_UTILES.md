# 🛠️ Comandos Útiles - ArcheoScope 3D Engine

## 🚀 Desarrollo

### Iniciar servidor de desarrollo
```bash
npm run dev
```

### Build de producción
```bash
npm run build
```

### Iniciar producción
```bash
npm start
```

---

## 🧪 Testing

### Ejecutar todos los tests
```bash
npm test
```

### Tests en modo watch
```bash
npm run test:watch
```

### Tests con coverage
```bash
npm run test:coverage
```

### Tests específicos
```bash
npm test -- scene-store
npm test -- biome-detector
npm test -- ArcheoEngine
```

---

## 📊 Performance Analysis

### Bundle analyzer (NO ejecutar todavía)
```bash
npm run analyze
npm run analyze:browser
npm run analyze:server
```

### Diagnóstico en consola
```typescript
import PerformanceDiagnostics from '@/utils/performance-diagnostics'

// Reporte completo
PerformanceDiagnostics.report()

// Sugerencia de preset
const preset = PerformanceDiagnostics.suggestPreset()
console.log('Preset sugerido:', preset)
```

### Métricas en tiempo real
```typescript
import PerformanceMonitor from '@/utils/performance-monitor'

const metrics = PerformanceMonitor.getMetrics()
console.log('FPS:', metrics.fps)
console.log('Draw calls:', metrics.drawCalls)
console.log('Memory:', metrics.memory, 'MB')
```

---

## 🎨 Graphics Presets

### Cambiar preset en código
```typescript
import GraphicsPresetManager from '@/systems/GraphicsPresets'

// Cambiar preset
GraphicsPresetManager.setPreset('LOW')
GraphicsPresetManager.setPreset('MEDIUM')
GraphicsPresetManager.setPreset('HIGH')
GraphicsPresetManager.setPreset('ULTRA')

// Obtener configuración
const config = GraphicsPresetManager.getConfig()
console.log('Shadows:', config.shadows)
console.log('Bloom:', config.bloom)
console.log('Max distance:', config.maxDrawDistance)
```

### Preset custom
```typescript
GraphicsPresetManager.setCustomConfig({
  shadows: true,
  shadowMapSize: 2048,
  bloom: false,
  ssao: false,
  maxDrawDistance: 2500
})
```

---

## ✂️ Culling System

### Estadísticas
```typescript
import CullingSystem from '@/systems/CullingSystem'

const stats = CullingSystem.getStats()
console.log('Total objects:', stats.totalObjects)
console.log('Visible:', stats.visibleObjects)
console.log('Culled:', stats.culledObjects)
console.log('Disposed:', stats.disposedObjects)
console.log('Saved draw calls:', stats.savedDrawCalls)
```

### Configurar
```typescript
CullingSystem.configure({
  enableFrustumCulling: true,
  enableDistanceCulling: true,
  enableDisposal: true,
  maxRenderDistance: 2000,
  disposalDistance: 2500
})
```

### Limpiar objetos disposed
```typescript
CullingSystem.cleanupDisposed()
```

### Reset completo
```typescript
CullingSystem.reset()
```

---

## 🎨 Instance Manager

### Estadísticas
```typescript
import InstanceManager from '@/systems/InstanceManager'

const stats = InstanceManager.getStats()
console.log('Total types:', stats.totalTypes)
console.log('Total instances:', stats.totalInstances)
console.log('Draw calls:', stats.drawCalls)
console.log('Saved draw calls:', stats.savedDrawCalls)
```

### Crear instanced mesh
```typescript
const mesh = InstanceManager.create('trees', {
  geometry: new THREE.CylinderGeometry(0.5, 0.5, 5),
  material: new THREE.MeshStandardMaterial({ color: 'brown' }),
  count: 1000
})
```

### Actualizar instancias
```typescript
// Individual
InstanceManager.setInstance('trees', 0, {
  position: new THREE.Vector3(10, 0, 10),
  rotation: new THREE.Euler(0, Math.PI / 4, 0),
  scale: new THREE.Vector3(1, 1, 1)
})

// Batch (más eficiente)
InstanceManager.setInstances('trees', instances)

// Aplicar cambios
InstanceManager.update()
```

---

## 🌍 WorldCore

### Estado del mundo
```typescript
import { WorldCore } from '@/engines/WorldCore'

// Estado
console.log('Paused:', WorldCore.State.getPaused())
console.log('Time scale:', WorldCore.State.getTimeScale())

// Pausar/Resumir
WorldCore.State.pause()
WorldCore.State.resume()

// Time scale
WorldCore.State.setTimeScale(2.0) // 2x velocidad
```

### Tiempo
```typescript
// Obtener tiempo
const time = WorldCore.Time.getTime()
console.log('Elapsed:', time.elapsed)
console.log('Delta:', time.delta)
console.log('Day time:', time.dayTime)

// Configurar
WorldCore.Time.configure({
  dayDuration: 120, // 2 minutos = 1 día
  startTime: 0.5    // Empezar al mediodía
})
```

### Spatial Index
```typescript
// Insertar objeto
WorldCore.SpatialIndex.insert({
  id: 'tree-1',
  position: new THREE.Vector3(10, 0, 10),
  data: { type: 'tree' }
})

// Query por radio
const nearby = WorldCore.SpatialIndex.queryRadius(
  playerPosition,
  100 // 100m
)

// K-nearest
const nearest = WorldCore.SpatialIndex.kNearest(
  playerPosition,
  5 // 5 objetos más cercanos
)
```

### Entities
```typescript
// Crear entidad
WorldCore.Entities.create(
  'tree-1',
  'tree',
  new THREE.Vector3(10, 0, 10),
  { health: 100 }
)

// Obtener entidad
const entity = WorldCore.Entities.get('tree-1')

// Obtener por tipo
const trees = WorldCore.Entities.getByType('tree')

// Query por radio
const nearby = WorldCore.Entities.queryRadius(
  playerPosition,
  50
)

// Estadísticas
const stats = WorldCore.Entities.getStats()
console.log('Total entities:', stats.totalEntities)
console.log('Active:', stats.activeEntities)
console.log('Types:', stats.entityTypes)
```

### Procedural Generator
```typescript
// Generar posiciones en grid
const positions = WorldCore.Procedural.generateGrid(
  {
    seed: 42,
    density: 0.5,
    minDistance: 10
  },
  {
    min: new THREE.Vector2(-100, -100),
    max: new THREE.Vector2(100, 100)
  }
)

// Generar en círculo
const positions = WorldCore.Procedural.generateCircle(
  { seed: 42, density: 0.5, minDistance: 10 },
  new THREE.Vector2(0, 0),
  100 // radio
)

// Generar terreno
const terrain = WorldCore.Procedural.generateTerrain(
  1000, // width
  1000, // height
  128   // resolution
)

// Cambiar seed
WorldCore.Procedural.setSeed(123)
```

---

## 🎮 EngineCore

### Estado
```typescript
import EngineCore from '@/engines/EngineCore'

const state = EngineCore.getState()
console.log('Running:', state.isRunning)
console.log('Paused:', state.isPaused)
console.log('Time scale:', state.timeScale)
console.log('Systems:', state.systemCount)
```

### Control
```typescript
EngineCore.start()
EngineCore.stop()
EngineCore.pause()
EngineCore.resume()
```

### Registrar sistema
```typescript
EngineCore.registerSystem('physics', {
  update: (delta) => {
    // Lógica de física
  },
  enabled: true
})

// Desregistrar
EngineCore.unregisterSystem('physics')
```

---

## 🐛 Debug en Consola

### Performance completo
```typescript
import PerformanceMonitor from '@/utils/performance-monitor'
import CullingSystem from '@/systems/CullingSystem'
import InstanceManager from '@/systems/InstanceManager'
import { WorldCore } from '@/engines/WorldCore'

console.log('=== PERFORMANCE ===')
console.log(PerformanceMonitor.getMetrics())

console.log('\n=== CULLING ===')
console.log(CullingSystem.getStats())

console.log('\n=== INSTANCING ===')
console.log(InstanceManager.getStats())

console.log('\n=== WORLD ===')
console.log('Entities:', WorldCore.Entities.getStats())
console.log('Spatial Index:', WorldCore.SpatialIndex.getStats())
```

### Diagnóstico automático
```typescript
import PerformanceDiagnostics from '@/utils/performance-diagnostics'

// Reporte completo
PerformanceDiagnostics.report()

// Solo resultados
const results = PerformanceDiagnostics.diagnose()
results.forEach(r => {
  console.log(`[${r.severity}] ${r.message}`)
  console.log(`  → ${r.suggestion}`)
})
```

---

## 📱 Paneles de Debug

### Activar paneles
```typescript
import PerformanceDashboard from '@/components/debug/PerformanceDashboard'
import CullingDebugPanel from '@/components/debug/CullingDebugPanel'
import GraphicsPresetPanel from '@/components/debug/GraphicsPresetPanel'

function App() {
  return (
    <>
      <Canvas>...</Canvas>
      
      <PerformanceDashboard />
      <CullingDebugPanel />
      <GraphicsPresetPanel />
    </>
  )
}
```

---

## 🔍 Troubleshooting

### FPS bajo

1. **Verificar preset**
```typescript
GraphicsPresetManager.setPreset('LOW')
// Si mejora → problema en postprocesado
// Si no mejora → problema en lógica/geometría
```

2. **Verificar draw calls**
```typescript
const metrics = PerformanceMonitor.getMetrics()
if (metrics.drawCalls > 100) {
  console.log('⚠️ Usar más instancing')
}
```

3. **Verificar culling**
```typescript
const stats = CullingSystem.getStats()
const efficiency = (stats.culledObjects / stats.totalObjects) * 100
console.log('Culling efficiency:', efficiency, '%')
```

### Memoria alta

1. **Activar disposal**
```typescript
CullingSystem.configure({
  enableDisposal: true,
  disposalDistance: 2500
})
```

2. **Limpiar disposed**
```typescript
CullingSystem.cleanupDisposed()
```

3. **Verificar instancing**
```typescript
const stats = InstanceManager.getStats()
console.log('Instances:', stats.totalInstances)
console.log('Types:', stats.totalTypes)
```

### Re-renders excesivos

1. **Verificar useFrame**
```bash
# Buscar todos los useFrame
grep -r "useFrame" --include="*.tsx"
```

2. **Convertir a EngineCore**
```typescript
// ❌ MALO
useFrame(() => {
  setRotation(r => r + 0.01)
})

// ✅ BIEN
useEngineUpdate((delta) => {
  meshRef.current.rotation.y += delta
})
```

---

## 📚 Documentación

### Leer documentación
```bash
# Arquitectura
cat ARQUITECTURA_FINAL.md
cat ARQUITECTURA_ENGINECORE.md
cat ARQUITECTURA_WORLDCORE.md

# Sistemas
cat SISTEMA_CULLING.md
cat SISTEMA_INSTANCING.md
cat SISTEMA_LOD.md
cat SISTEMA_WORKERS.md

# Estrategias
cat ESTRATEGIA_PERFORMANCE.md
cat TEST_STRATEGY.md

# Resumen
cat RESUMEN_IMPLEMENTACION.md
```

---

## 🎯 Comandos Rápidos

### Diagnóstico completo
```typescript
import PerformanceDiagnostics from '@/utils/performance-diagnostics'
PerformanceDiagnostics.report()
```

### Cambiar a LOW y medir
```typescript
import GraphicsPresetManager from '@/systems/GraphicsPresets'
import PerformanceMonitor from '@/utils/performance-monitor'

GraphicsPresetManager.setPreset('LOW')
setTimeout(() => {
  const metrics = PerformanceMonitor.getMetrics()
  console.log('FPS en LOW:', metrics.fps)
}, 2000)
```

### Limpiar todo
```typescript
CullingSystem.reset()
InstanceManager.clear()
WorldCore.Entities.clear()
WorldCore.SpatialIndex.clear()
```

---

**Tip**: Agregar estos comandos a snippets de VS Code para acceso rápido
