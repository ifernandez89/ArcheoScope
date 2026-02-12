# 🚀 Quick Start - Core Engine

## Inicio Rápido en 5 Minutos

### 1. Verificar que el servidor está corriendo

```bash
# El servidor debería estar en http://localhost:3000
# Si no está corriendo:
cd viewer3d
npm run dev
```

### 2. Abrir en el navegador

```
http://localhost:3000
```

Deberías ver el modelo warrior.glb cargado y rotando.

---

## 🎮 Controles Básicos

### Navegación
- **Click izquierdo + arrastrar**: Rotar cámara
- **Click derecho + arrastrar**: Mover cámara (pan)
- **Scroll**: Zoom in/out
- **Click en modelo**: Toggle auto-rotación

### Panel de Controles (esquina superior derecha)
- **🔄 Auto-Rotación**: Activar/desactivar rotación automática
- **📐 Grid**: Mostrar/ocultar grid de referencia

---

## 💻 Usar el Core Engine (Código)

### Ejemplo Básico

```typescript
import { Engine3D } from '@/core/engine'
import * as THREE from 'three'

// Configuración de iluminación
const lightingConfig = {
  ambient: { intensity: 0.4, color: '#ffffff' },
  directional: { 
    intensity: 1.2, 
    position: [10, 10, 5], 
    castShadow: true 
  }
}

// Crear engine
const engine = new Engine3D(scene, camera, lightingConfig)

// Cargar modelo
await engine.loadModel('warrior', '/warrior.glb', (progress) => {
  console.log(`Cargando: ${progress}%`)
})

// Reproducir animación
engine.playAnimation('warrior', 0)

// Update loop
function animate() {
  engine.update()
  requestAnimationFrame(animate)
}
animate()
```

---

## 🎬 Ejemplos Prácticos

### 1. Cambiar Hora del Día

```typescript
// Amanecer (6 AM)
engine.lighting.setTimeOfDay(6)

// Mediodía (12 PM)
engine.lighting.setTimeOfDay(12)

// Atardecer (18 PM)
engine.lighting.setTimeOfDay(18)

// Medianoche (0 AM)
engine.lighting.setTimeOfDay(0)
```

### 2. Vuelo Cinematográfico de Cámara

```typescript
// Volar a una nueva posición
engine.cameraController.flyTo(
  new THREE.Vector3(10, 5, 10),  // posición destino
  new THREE.Vector3(0, 0, 0),     // punto a mirar
  2000                             // duración en ms
)
```

### 3. Eventos Interactivos

```typescript
// Click en objetos
engine.events.on('click', (event) => {
  console.log('Clicked:', event.target.name)
  console.log('Position:', event.position)
})

// Hover sobre objetos
engine.events.on('hover', (event) => {
  console.log('Hovering:', event.target.name)
})

// Proximidad
engine.events.on('proximity', (event) => {
  console.log('Near:', event.target.name)
  console.log('Distance:', event.data.distance)
})
```

### 4. Timeline de Eventos

```typescript
// Crear secuencia temporal
engine.timeline.addEvent({
  time: 0,
  name: 'start',
  action: () => {
    console.log('Inicio de la experiencia')
  }
})

engine.timeline.addEvent({
  time: 2000,
  name: 'camera-move',
  action: () => {
    engine.cameraController.flyTo(
      new THREE.Vector3(5, 3, 5),
      new THREE.Vector3(0, 0, 0),
      1500
    )
  }
})

engine.timeline.addEvent({
  time: 4000,
  name: 'play-animation',
  action: () => {
    engine.playAnimation('warrior', 0)
  }
})

// Iniciar timeline
engine.timeline.play()
```

### 5. Gestión de Escenas

```typescript
import { SceneManager } from '@/experience/scene-manager'

const sceneManager = new SceneManager(engine)

// Registrar escena
sceneManager.registerScene({
  name: 'intro',
  models: [
    { 
      id: 'warrior', 
      url: '/warrior.glb',
      position: new THREE.Vector3(0, 0, 0)
    }
  ],
  camera: {
    position: new THREE.Vector3(5, 3, 5),
    target: new THREE.Vector3(0, 0, 0)
  },
  lighting: {
    timeOfDay: 14  // 2 PM
  },
  onEnter: () => {
    console.log('Entrando a escena intro')
    engine.playAnimation('warrior', 0)
  }
})

// Cargar escena
await sceneManager.loadScene('intro', (progress) => {
  console.log(`Cargando escena: ${progress}%`)
})
```

---

## 🎨 Personalización

### Cambiar Modelo

1. Coloca tu archivo .glb en `viewer3d/public/`
2. Actualiza `components/ModelViewer.tsx`:

```typescript
<ModelViewer modelPath="/tu-modelo.glb" />
```

### Cambiar Iluminación

Edita `components/Scene3D.tsx`:

```typescript
<ambientLight intensity={0.6} />  // Más luz ambiental
<directionalLight
  position={[5, 10, 5]}           // Nueva posición
  intensity={1.5}                  // Más intensidad
  castShadow
/>
```

### Cambiar Cámara Inicial

```typescript
<PerspectiveCamera 
  makeDefault 
  position={[10, 5, 10]}  // Nueva posición
  fov={45}                 // Nuevo FOV
/>
```

---

## 🔧 Troubleshooting

### El modelo no se ve

1. Verifica que el archivo existe en `public/`
2. Abre la consola del navegador (F12)
3. Busca errores de carga

### El modelo está muy grande/pequeño

El sistema auto-escala, pero puedes ajustar manualmente en `ModelViewer.tsx`:

```typescript
const scale = 3 / maxDim  // Cambiar el 2 por otro valor
```

### Las sombras no se ven

Verifica que:
1. `castShadow` está en true en las luces
2. Los meshes tienen `castShadow` y `receiveShadow`
3. El renderer tiene `shadows` habilitado

### Performance bajo

1. Reduce la resolución de sombras:
   ```typescript
   shadow-mapSize-width={1024}
   shadow-mapSize-height={1024}
   ```

2. Desactiva postprocessing (si está activo)

3. Reduce la complejidad del modelo

---

## 📚 Recursos

### Documentación
- [Core Engine](./CORE_ENGINE.md) - Arquitectura completa
- [Setup Guide](./SETUP.md) - Instalación y configuración
- [FASE 1 Complete](./FASE1_COMPLETE.md) - Resumen de features

### APIs
- [Three.js Docs](https://threejs.org/docs/)
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber)
- [Zustand](https://github.com/pmndrs/zustand)

### Ejemplos
- [Three.js Examples](https://threejs.org/examples/)
- [R3F Examples](https://docs.pmnd.rs/react-three-fiber/getting-started/examples)

---

## 🎯 Próximos Pasos

1. ✅ Familiarízate con los controles básicos
2. ✅ Prueba los ejemplos de código
3. ✅ Lee la documentación del Core Engine
4. ✅ Experimenta con iluminación y cámara
5. ✅ Crea tu primera escena personalizada

---

## 💡 Tips

- **Usa la consola del navegador** (F12) para ver logs y errores
- **Experimenta con los valores** de iluminación y cámara
- **Lee el código fuente** en `core/` para entender cómo funciona
- **Consulta CORE_ENGINE.md** para ejemplos avanzados

---

**¡Disfruta creando experiencias 3D!** 🎨✨
