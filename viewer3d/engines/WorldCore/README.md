# 🌍 WorldCore - Motor de Mundo Modular

Sistema modular para gestión de mundo 3D en ArcheoScope. Diseñado como motor escalable, no como aplicación monolítica.

---

## 📦 Módulos

### 1. WorldState
**Responsabilidad**: Estado global del mundo

**Características**:
- Configuración centralizada (render distance, LOD levels, chunk size)
- Métricas en tiempo real (FPS, draw calls, triangles, memoria)
- Pause/Resume del mundo
- Time scale (slow motion / fast forward)
- Sistema de eventos (EventEmitter)

**Uso**:
```typescript
import { WorldCore } from '@/engines/WorldCore'

// Configurar
WorldCore.State.updateConfig({
  renderDistance: 1500,
  lodLevels: 5
})

// Pausar/Resumir
WorldCore.State.pause()
WorldCore.State.resume()

// Escuchar eventos
WorldCore.State.on('config:changed', (config) => {
  console.log('Config actualizada', config)
})

// Métricas
const metrics = WorldCore.State.getMetrics()
console.log('FPS:', metrics.fps)
```

---

### 2. WorldTime
**Responsabilidad**: Sistema de tiempo simulado

**Características**:
- Ciclo día/noche configurable
- Estaciones del año (spring, summer, autumn, winter)
- Time scale independiente
- Queries útiles (isDaytime, getHourOfDay, getSunAngle)

**Uso**:
```typescript
import { WorldCore } from '@/engines/WorldCore'

// Actualizar (llamar cada frame)
WorldCore.Time.update(deltaTime, timeScale)

// Obtener estado
const state = WorldCore.Time.getState()
console.log('Hora:', state.dayTime * 24)
console.log('Estación:', state.season)

// Establecer hora específica
WorldCore.Time.setTime(12) // Mediodía

// Verificar día/noche
if (WorldCore.Time.isDaytime()) {
  // Lógica de día
}

// Ángulo solar para iluminación
const sunAngle = WorldCore.Time.getSunAngle()
```

---

### 3. WorldSpatialIndex
**Responsabilidad**: Índice espacial para queries eficientes

**Características**:
- Grid espacial con O(1) en promedio
- Query por radio
- K-nearest neighbors
- Frustum culling (placeholder)
- Actualización dinámica de objetos

**Uso**:
```typescript
import { WorldCore } from '@/engines/WorldCore'
import * as THREE from 'three'

// Agregar objeto
WorldCore.SpatialIndex.add({
  id: 'tree_001',
  position: new THREE.Vector3(10, 0, 20),
  bounds: new THREE.Box3(),
  data: { type: 'tree' }
})

// Buscar en radio
const nearby = WorldCore.SpatialIndex.queryRadius(
  playerPosition,
  50 // radio
)

// K más cercanos
const nearest = WorldCore.SpatialIndex.queryKNearest(
  playerPosition,
  5 // cantidad
)

// Actualizar posición
WorldCore.SpatialIndex.update('tree_001', newPosition)

// Estadísticas
const stats = WorldCore.SpatialIndex.getStats()
console.log('Objetos:', stats.totalObjects)
```

---

### 4. WorldLOD
**Responsabilidad**: Level of Detail automático

**Características**:
- Múltiples niveles de LOD configurables
- Transiciones automáticas basadas en distancia
- Estadísticas por nivel
- Optimización de rendimiento

**Uso**:
```typescript
import { WorldCore } from '@/engines/WorldCore'

// Configurar niveles
WorldCore.LOD.setLODLevels([
  { distance: 50, detail: 1.0 },
  { distance: 150, detail: 0.6 },
  { distance: 300, detail: 0.3 },
  { distance: 500, detail: 0.1 }
])

// Registrar objeto con LOD
WorldCore.LOD.register(
  'building_001',
  position,
  [highDetailMesh, mediumDetailMesh, lowDetailMesh, veryLowDetailMesh]
)

// Actualizar cámara (cada frame)
WorldCore.LOD.updateCamera(camera.position)

// Actualizar LOD (cada frame)
const result = WorldCore.LOD.update()
console.log('Cambios:', result.changed)

// Estadísticas
const stats = WorldCore.LOD.getStats()
console.log('Por nivel:', stats.byLevel)
```

---

### 5. WorldStreaming
**Responsabilidad**: Streaming dinámico de contenido

**Características**:
- Sistema de chunks
- Carga/descarga automática basada en distancia
- Cola de prioridad
- Carga asíncrona con límite de concurrencia
- Gestión de memoria

**Uso**:
```typescript
import { WorldCore } from '@/engines/WorldCore'

// Configurar
WorldCore.Streaming.configure({
  chunkSize: 50,
  loadRadius: 3,
  unloadRadius: 5,
  maxConcurrentLoads: 4
})

// Actualizar posición del jugador
WorldCore.Streaming.updatePlayerPosition(playerPosition)

// Actualizar streaming (cada frame)
WorldCore.Streaming.update()

// Estadísticas
const stats = WorldCore.Streaming.getStats()
console.log('Chunks cargados:', stats.loadedChunks)
console.log('En cola:', stats.queuedChunks)
```

---

### 6. WorldPersistence
**Responsabilidad**: Persistencia de estado

**Características**:
- Save/Load en localStorage
- Auto-save configurable
- Versionado de saves
- Export/Import JSON
- Migración de datos (placeholder)

**Uso**:
```typescript
import { WorldCore } from '@/engines/WorldCore'

// Guardar
await WorldCore.Persistence.save({
  worldState: { time: 12000 },
  playerState: { position: [0, 0, 0] },
  customData: { score: 100 }
})

// Cargar
const data = await WorldCore.Persistence.load()
if (data) {
  console.log('Timestamp:', data.timestamp)
}

// Auto-save
WorldCore.Persistence.enableAutoSave(() => ({
  worldState: getCurrentWorldState(),
  playerState: getCurrentPlayerState()
}))

// Verificar si existe save
if (WorldCore.Persistence.hasSave()) {
  // Mostrar botón "Continuar"
}

// Exportar/Importar
const json = await WorldCore.Persistence.exportSave()
await WorldCore.Persistence.importSave(json)
```

---

## 🎯 Filosofía de Diseño

### 1. Modularidad
Cada módulo tiene una responsabilidad única y bien definida.

### 2. Singleton Pattern
Todos los módulos son singletons para acceso global consistente.

### 3. Escalabilidad
Diseñado para crecer como motor, no como aplicación.

### 4. Performance First
Estructuras de datos eficientes (spatial grid, LOD, streaming).

### 5. Extensibilidad
Fácil agregar nuevos módulos sin romper existentes.

---

## 🔄 Integración Típica

```typescript
import { WorldCore } from '@/engines/WorldCore'

// Setup inicial
function setupWorld() {
  // Configurar estado
  WorldCore.State.updateConfig({
    renderDistance: 1000,
    lodLevels: 4,
    chunkSize: 50
  })
  
  // Configurar LOD
  WorldCore.LOD.setLODLevels([
    { distance: 50, detail: 1.0 },
    { distance: 150, detail: 0.6 },
    { distance: 300, detail: 0.3 }
  ])
  
  // Configurar streaming
  WorldCore.Streaming.configure({
    loadRadius: 3,
    unloadRadius: 5
  })
  
  // Habilitar auto-save
  WorldCore.Persistence.enableAutoSave(() => ({
    worldState: WorldCore.Time.getState(),
    playerState: { /* ... */ }
  }))
}

// Loop de actualización
function update(deltaTime: number) {
  // Actualizar tiempo
  WorldCore.Time.update(deltaTime, WorldCore.State.getTimeScale())
  
  // Actualizar LOD
  WorldCore.LOD.updateCamera(camera.position)
  WorldCore.LOD.update()
  
  // Actualizar streaming
  WorldCore.Streaming.updatePlayerPosition(player.position)
  WorldCore.Streaming.update()
  
  // Actualizar métricas
  WorldCore.State.updateMetrics({
    fps: 1 / deltaTime,
    drawCalls: renderer.info.render.calls,
    triangles: renderer.info.render.triangles
  })
}
```

---

## 📈 Próximas Expansiones

### Corto Plazo
- [ ] WorldPhysics - Sistema de física
- [ ] WorldAudio - Audio espacial
- [ ] WorldWeather - Sistema climático integrado

### Medio Plazo
- [ ] WorldMultiplayer - Sincronización de red
- [ ] WorldAI - Pathfinding y comportamiento
- [ ] WorldVFX - Sistema de efectos visuales

### Largo Plazo
- [ ] WorldEditor - Editor in-game
- [ ] WorldScripting - Sistema de scripting
- [ ] WorldAnalytics - Telemetría y analytics

---

## 🧪 Testing

Cada módulo debe tener tests unitarios:

```bash
npm test WorldState
npm test WorldTime
npm test WorldSpatialIndex
```

---

**Arquitectura**: Modular y escalable  
**Patrón**: Singleton + EventEmitter  
**Objetivo**: Motor de mundo profesional
