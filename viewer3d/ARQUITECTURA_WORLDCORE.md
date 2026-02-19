# 🏗️ Arquitectura WorldCore - Motor de Mundo Modular

## 📋 Visión General

WorldCore es el núcleo modular del motor de mundo 3D de ArcheoScope. Diseñado como un motor escalable y profesional, no como una aplicación monolítica.

---

## 🎯 Filosofía

### Antes (Disperso)
```
engines/
├── WorldEngine.ts (todo mezclado)
├── GeoEngine.ts
├── ArcheoEngine.ts
└── ... (engines sin estructura clara)
```

### Ahora (Modular)
```
engines/
├── WorldCore/
│   ├── WorldState.ts          # Estado global
│   ├── WorldTime.ts           # Sistema de tiempo
│   ├── WorldSpatialIndex.ts   # Índice espacial
│   ├── WorldLOD.ts            # Level of Detail
│   ├── WorldStreaming.ts      # Streaming de contenido
│   ├── WorldPersistence.ts    # Save/Load
│   └── index.ts               # Exports unificados
├── GeoEngine.ts
├── ArcheoEngine.ts
└── ...
```

---

## 🧩 Módulos del WorldCore

### 1. WorldState 🌍
**Responsabilidad**: Estado global y configuración

**Características**:
- Configuración centralizada (render distance, LOD, chunks)
- Métricas en tiempo real (FPS, draw calls, memoria)
- Pause/Resume
- Time scale
- Sistema de eventos

**Casos de uso**:
- Panel de configuración del motor
- Debug overlay con métricas
- Pause menu
- Slow motion / fast forward

---

### 2. WorldTime ⏰
**Responsabilidad**: Sistema de tiempo simulado

**Características**:
- Ciclo día/noche configurable
- Estaciones del año
- Queries útiles (isDaytime, getSunAngle)
- Time scale independiente

**Casos de uso**:
- Iluminación dinámica día/noche
- Cambios estacionales en vegetación
- Comportamiento de NPCs según hora
- Sistema de misiones temporales

---

### 3. WorldSpatialIndex 🗺️
**Responsabilidad**: Índice espacial para queries eficientes

**Características**:
- Grid espacial O(1)
- Query por radio
- K-nearest neighbors
- Frustum culling

**Casos de uso**:
- Encontrar objetos cercanos al jugador
- Culling de objetos fuera de vista
- Pathfinding
- Detección de colisiones broad-phase

---

### 4. WorldLOD 🎚️
**Responsabilidad**: Level of Detail automático

**Características**:
- Múltiples niveles configurables
- Transiciones automáticas
- Estadísticas por nivel

**Casos de uso**:
- Optimización de rendimiento
- Modelos con múltiples niveles de detalle
- Terreno con LOD
- Vegetación instanciada

---

### 5. WorldStreaming 📦
**Responsabilidad**: Streaming dinámico de contenido

**Características**:
- Sistema de chunks
- Carga/descarga automática
- Cola de prioridad
- Límite de concurrencia

**Casos de uso**:
- Mundos grandes sin loading screens
- Gestión de memoria
- Carga progresiva de assets
- Open world seamless

---

### 6. WorldPersistence 💾
**Responsabilidad**: Persistencia de estado

**Características**:
- Save/Load en localStorage
- Auto-save configurable
- Versionado
- Export/Import JSON

**Casos de uso**:
- Sistema de guardado
- Continuar partida
- Cloud saves (futuro)
- Replay system

---

## 🔄 Flujo de Integración

### Setup Inicial
```typescript
import { WorldCore } from '@/engines/WorldCore'

function initializeWorld() {
  // 1. Configurar estado
  WorldCore.State.updateConfig({
    renderDistance: 1000,
    lodLevels: 4,
    chunkSize: 50,
    enableStreaming: true
  })
  
  // 2. Configurar LOD
  WorldCore.LOD.setLODLevels([
    { distance: 50, detail: 1.0 },
    { distance: 150, detail: 0.6 },
    { distance: 300, detail: 0.3 },
    { distance: 500, detail: 0.1 }
  ])
  
  // 3. Configurar streaming
  WorldCore.Streaming.configure({
    loadRadius: 3,
    unloadRadius: 5,
    maxConcurrentLoads: 4
  })
  
  // 4. Cargar save si existe
  if (WorldCore.Persistence.hasSave()) {
    const data = await WorldCore.Persistence.load()
    // Restaurar estado
  }
  
  // 5. Habilitar auto-save
  WorldCore.Persistence.enableAutoSave(() => ({
    worldState: WorldCore.Time.getState(),
    playerState: getPlayerState()
  }))
}
```

### Loop de Actualización
```typescript
function update(deltaTime: number) {
  // 1. Verificar si está pausado
  if (WorldCore.State.getPaused()) return
  
  // 2. Actualizar tiempo
  const timeScale = WorldCore.State.getTimeScale()
  WorldCore.Time.update(deltaTime, timeScale)
  
  // 3. Actualizar LOD
  WorldCore.LOD.updateCamera(camera.position)
  const lodResult = WorldCore.LOD.update()
  
  // 4. Actualizar streaming
  WorldCore.Streaming.updatePlayerPosition(player.position)
  WorldCore.Streaming.update()
  
  // 5. Actualizar métricas
  WorldCore.State.updateMetrics({
    fps: 1 / deltaTime,
    drawCalls: renderer.info.render.calls,
    triangles: renderer.info.render.triangles,
    loadedChunks: WorldCore.Streaming.getStats().loadedChunks
  })
}
```

### Queries Espaciales
```typescript
// Encontrar objetos cercanos
const nearby = WorldCore.SpatialIndex.queryRadius(
  playerPosition,
  50 // radio
)

// K más cercanos
const nearest = WorldCore.SpatialIndex.queryKNearest(
  playerPosition,
  5 // cantidad
)

// Iterar resultados
for (const result of nearby) {
  console.log(result.object.id, result.distance)
}
```

---

## 📊 Arquitectura de Datos

### Estado Global (WorldState)
```typescript
{
  config: {
    renderDistance: 1000,
    lodLevels: 4,
    chunkSize: 50,
    enableStreaming: true,
    enablePersistence: false
  },
  metrics: {
    fps: 60,
    drawCalls: 150,
    triangles: 50000,
    loadedChunks: 9,
    activeObjects: 234,
    memoryUsage: 128000000
  },
  isPaused: false,
  timeScale: 1.0
}
```

### Estado de Tiempo (WorldTime)
```typescript
{
  worldTime: 3600,      // segundos desde inicio
  dayTime: 0.5,         // 0-1 (0.5 = mediodía)
  season: 'summer',
  dayOfYear: 180,
  year: 2024
}
```

### Objeto Espacial (WorldSpatialIndex)
```typescript
{
  id: 'tree_001',
  position: Vector3(10, 0, 20),
  bounds: Box3(...),
  data: { type: 'tree', health: 100 }
}
```

---

## 🎮 Casos de Uso Reales

### 1. Sistema de Día/Noche
```typescript
function updateLighting() {
  const isDaytime = WorldCore.Time.isDaytime()
  const sunAngle = WorldCore.Time.getSunAngle()
  
  directionalLight.intensity = isDaytime ? 1.0 : 0.1
  directionalLight.position.setFromSphericalCoords(
    100,
    sunAngle,
    0
  )
  
  skyColor = isDaytime ? '#87ceeb' : '#0a0a1a'
}
```

### 2. LOD Automático
```typescript
// Registrar edificio con 4 niveles
WorldCore.LOD.register(
  'building_001',
  buildingPosition,
  [
    highDetailMesh,    // < 50m
    mediumDetailMesh,  // 50-150m
    lowDetailMesh,     // 150-300m
    billboardSprite    // > 300m
  ]
)

// El sistema cambia automáticamente según distancia
```

### 3. Streaming de Mundo Abierto
```typescript
// El jugador se mueve
WorldCore.Streaming.updatePlayerPosition(player.position)

// Sistema carga/descarga chunks automáticamente
// - Carga chunks en radio de 3
// - Descarga chunks en radio > 5
// - Máximo 4 cargas concurrentes
```

### 4. Save/Load
```typescript
// Guardar
await WorldCore.Persistence.save({
  worldState: {
    time: WorldCore.Time.getState(),
    weather: currentWeather
  },
  playerState: {
    position: player.position.toArray(),
    inventory: player.inventory
  }
})

// Cargar
const save = await WorldCore.Persistence.load()
if (save) {
  WorldCore.Time.setTime(save.worldState.time.dayTime * 24)
  player.position.fromArray(save.playerState.position)
}
```

---

## 🚀 Roadmap de Expansión

### Fase 1 (Actual) ✅
- [x] WorldState
- [x] WorldTime
- [x] WorldSpatialIndex
- [x] WorldLOD
- [x] WorldStreaming
- [x] WorldPersistence

### Fase 2 (Próxima)
- [ ] WorldPhysics - Sistema de física
- [ ] WorldAudio - Audio espacial 3D
- [ ] WorldWeather - Clima integrado con WorldTime

### Fase 3 (Futuro)
- [ ] WorldMultiplayer - Sincronización de red
- [ ] WorldAI - Pathfinding y comportamiento
- [ ] WorldVFX - Sistema de efectos visuales

### Fase 4 (Avanzado)
- [ ] WorldEditor - Editor in-game
- [ ] WorldScripting - Sistema de scripting Lua/JS
- [ ] WorldAnalytics - Telemetría y heatmaps

---

## 🧪 Testing

Cada módulo debe tener tests unitarios:

```bash
# Tests individuales
npm test WorldState
npm test WorldTime
npm test WorldSpatialIndex
npm test WorldLOD
npm test WorldStreaming
npm test WorldPersistence

# Suite completa
npm test WorldCore
```

---

## 📈 Métricas de Éxito

### Performance
- FPS estable > 60
- Draw calls < 200
- Memoria < 500MB
- Tiempo de carga de chunk < 100ms

### Escalabilidad
- Soportar 10,000+ objetos
- Mundo de 10km x 10km
- 100+ chunks activos simultáneos

### Usabilidad
- API clara y consistente
- Documentación completa
- Ejemplos de uso
- TypeScript types completos

---

## 🎯 Principios de Diseño

1. **Modularidad**: Cada módulo tiene una responsabilidad única
2. **Singleton**: Acceso global consistente
3. **Performance**: Estructuras de datos eficientes
4. **Escalabilidad**: Diseñado para crecer
5. **Testabilidad**: Lógica determinista testeable
6. **Documentación**: Código auto-documentado

---

## 🔗 Integración con Otros Engines

```
WorldCore (núcleo)
    ↓
    ├─→ GeoEngine (terreno geográfico)
    ├─→ ArcheoEngine (sitios arqueológicos)
    ├─→ AvatarEngine (personajes)
    ├─→ AstroEngine (astronomía)
    └─→ SkyEngine (cielo dinámico)
```

WorldCore provee la infraestructura base que otros engines utilizan.

---

**Arquitectura**: Modular y escalable  
**Patrón**: Singleton + EventEmitter  
**Estado**: ✅ Implementado y documentado  
**Próximo paso**: Integración con componentes React
