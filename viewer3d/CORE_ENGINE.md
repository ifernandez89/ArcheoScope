# Core Engine - Motor de Experiencias 3D

## 🎯 Visión General

El Core Engine es un **runtime profesional** para experiencias 3D interactivas. No es solo un viewer, es un motor completo que permite crear narrativas inmersivas con modelos 3D.

## 🏗️ Arquitectura

### CAPA 1: Core Engine (Base Estable)

El Core Engine está dividido en módulos especializados:

```
viewer3d/
├── core/
│   ├── engine.ts          # Runtime principal
│   ├── loader.ts          # Cargador robusto de GLB
│   ├── camera.ts          # Sistema de cámara avanzado
│   ├── lighting.ts        # Sistema de iluminación dinámica
│   ├── events.ts          # Sistema de eventos (click, hover, proximity)
│   ├── timeline.ts        # Timeline interno
│   └── types.ts           # Tipos TypeScript
├── experience/
│   ├── scene-manager.ts   # Gestor de escenas
│   └── transitions.ts     # Transiciones cinematográficas
└── store/
    └── scene-store.ts     # Estado global (Zustand)
```

## 📦 Módulos del Core Engine

### 1. Engine3D (`core/engine.ts`)

Runtime principal que coordina todos los subsistemas.

```typescript
import { Engine3D } from '@/core/engine'

const engine = new Engine3D(scene, camera, lightingConfig)

// Cargar modelo
await engine.loadModel('warrior', '/warrior.glb', (progress) => {
  console.log(`Cargando: ${progress}%`)
})

// Reproducir animación
engine.playAnimation('warrior', 0)

// Cambiar modo de cámara
engine.setCameraMode({
  type: 'cinematic',
  position: new THREE.Vector3(5, 3, 5),
  target: new THREE.Vector3(0, 0, 0),
  fov: 45
})

// Update loop
function animate() {
  engine.update()
  requestAnimationFrame(animate)
}
```

### 2. ModelLoader (`core/loader.ts`)

Cargador robusto con soporte para DRACO compression y tracking de progreso.

```typescript
const loader = new ModelLoader()

const model = await loader.load('/model.glb', (progress) => {
  console.log(`${progress.percentage}% cargado`)
})
```

### 3. CameraController (`core/camera.ts`)

Sistema de cámara con modos orbital y cinematográfico.

```typescript
// Modo orbital (default)
cameraController.setMode({
  type: 'orbital',
  position: new THREE.Vector3(5, 3, 5),
  target: new THREE.Vector3(0, 0, 0)
})

// Vuelo cinematográfico
cameraController.flyTo(
  new THREE.Vector3(10, 5, 10),
  new THREE.Vector3(0, 0, 0),
  2000 // duración en ms
)
```

### 4. LightingSystem (`core/lighting.ts`)

Sistema de iluminación dinámica con simulación de hora del día.

```typescript
// Configurar hora del día (0-24)
lighting.setTimeOfDay(12) // mediodía
lighting.setTimeOfDay(18) // atardecer
lighting.setTimeOfDay(0)  // medianoche

// Actualizar luz direccional manualmente
lighting.updateDirectionalLight(
  new THREE.Vector3(10, 10, 5),
  1.2 // intensidad
)
```

### 5. EventSystem (`core/events.ts`)

Sistema de eventos para interactividad.

```typescript
// Click en objetos
events.on('click', (event) => {
  console.log('Clicked:', event.target)
  console.log('Position:', event.position)
})

// Hover sobre objetos
events.on('hover', (event) => {
  console.log('Hovering:', event.target)
})

// Proximidad
events.on('proximity', (event) => {
  console.log('Near:', event.target)
  console.log('Distance:', event.data.distance)
})
```

### 6. Timeline (`core/timeline.ts`)

Sistema de timeline para eventos temporales.

```typescript
// Agregar eventos
timeline.addEvent({
  time: 1000, // 1 segundo
  name: 'intro',
  action: () => {
    console.log('Intro triggered')
  }
})

timeline.addEvent({
  time: 3000, // 3 segundos
  name: 'camera-move',
  action: () => {
    engine.setCameraMode(cinematicMode)
  }
})

// Controlar timeline
timeline.play()
timeline.pause()
timeline.seek(2000) // ir a 2 segundos
timeline.stop()
```

## 🎬 Capa de Experiencia

### SceneManager (`experience/scene-manager.ts`)

Gestor de escenas para experiencias multi-escena.

```typescript
const sceneManager = new SceneManager(engine)

// Registrar escena
sceneManager.registerScene({
  name: 'intro',
  models: [
    { id: 'warrior', url: '/warrior.glb', position: new THREE.Vector3(0, 0, 0) }
  ],
  camera: {
    position: new THREE.Vector3(5, 3, 5),
    target: new THREE.Vector3(0, 0, 0)
  },
  lighting: {
    timeOfDay: 12
  },
  onEnter: () => {
    console.log('Entrando a escena intro')
  }
})

// Cargar escena
await sceneManager.loadScene('intro', (progress) => {
  console.log(`Cargando escena: ${progress}%`)
})
```

### TransitionManager (`experience/transitions.ts`)

Transiciones cinematográficas entre estados.

```typescript
const transitions = new TransitionManager(engine)

// Vuelo de cámara
transitions.cameraFlyTo(
  new THREE.Vector3(10, 5, 10),
  new THREE.Vector3(0, 0, 0),
  {
    duration: 2000,
    easing: 'easeInOut',
    onComplete: () => {
      console.log('Transición completa')
    }
  }
)

// Dolly zoom (efecto Hitchcock)
transitions.dollyZoom(30, {
  duration: 1500,
  easing: 'easeIn'
})
```

## 🎮 Estado Global

### SceneStore (`store/scene-store.ts`)

Estado global con Zustand para sincronización UI-Engine.

```typescript
import { useSceneStore } from '@/store/scene-store'

function Component() {
  const autoRotate = useSceneStore((state) => state.autoRotate)
  const setAutoRotate = useSceneStore((state) => state.setAutoRotate)
  const cameraMode = useSceneStore((state) => state.cameraMode)
  
  return (
    <button onClick={() => setAutoRotate(!autoRotate)}>
      Toggle Rotation
    </button>
  )
}
```

## 🎨 Postprocessing

El engine incluye efectos de postprocesamiento:

- **Bloom**: Resplandor en áreas brillantes
- **SSAO**: Ambient occlusion para profundidad
- **Depth of Field**: Desenfoque cinematográfico (próximamente)

## 🚀 Ejemplo Completo

```typescript
import { Engine3D } from '@/core/engine'
import { SceneManager } from '@/experience/scene-manager'
import { TransitionManager } from '@/experience/transitions'
import * as THREE from 'three'

// Configuración de iluminación
const lightingConfig = {
  ambient: { intensity: 0.4, color: '#ffffff' },
  directional: { 
    intensity: 1.2, 
    position: [10, 10, 5], 
    castShadow: true 
  },
  point: { intensity: 0.3, position: [-10, -10, -5] }
}

// Crear engine
const engine = new Engine3D(scene, camera, lightingConfig)
const sceneManager = new SceneManager(engine)
const transitions = new TransitionManager(engine)

// Registrar escena
sceneManager.registerScene({
  name: 'warrior-showcase',
  models: [
    { id: 'warrior', url: '/warrior.glb' }
  ],
  camera: {
    position: new THREE.Vector3(5, 3, 5),
    target: new THREE.Vector3(0, 0, 0)
  },
  lighting: { timeOfDay: 14 },
  onEnter: () => {
    // Reproducir animación
    engine.playAnimation('warrior', 0)
    
    // Timeline de eventos
    engine.timeline.addEvent({
      time: 2000,
      action: () => {
        transitions.cameraFlyTo(
          new THREE.Vector3(3, 2, 3),
          new THREE.Vector3(0, 1, 0),
          { duration: 1500 }
        )
      }
    })
    
    engine.timeline.play()
  }
})

// Cargar escena
await sceneManager.loadScene('warrior-showcase')

// Loop de actualización
function animate() {
  engine.update()
  requestAnimationFrame(animate)
}
animate()
```

## 🔮 Próximas Fases

### FASE 2: Motor de Experiencias
- Sistema de escenas completo
- Audio reactivo
- Texto contextual 3D
- Narrativa temporal

### FASE 3: Motor IA
- Animaciones procedurales
- Movimiento reactivo
- Micro-expresiones
- Control por LLM

### FASE 4: Motor Astronómico + Geoespacial
- Mapa 3D global (Cesium)
- Simulación solar real
- Alineamientos astronómicos
- Coordenadas geoespaciales

## 📚 Referencias

- [Three.js Documentation](https://threejs.org/docs/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Zustand](https://github.com/pmndrs/zustand)
- [Postprocessing](https://github.com/pmndrs/postprocessing)

---

**Motor de Simulación Interpretativa** - No es un viewer. Es un runtime.
