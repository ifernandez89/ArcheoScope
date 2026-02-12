# 🚀 Guía Rápida - FASE 2: Motor de Experiencias

## 🎬 Navegación de Escenas

### Botón Flotante
- **Ubicación**: Esquina inferior izquierda
- **Icono**: 🎬 (púrpura)
- **Acción**: Click para abrir/cerrar panel

### Panel de Navegación
```
┌─────────────────────────────────┐
│ 🎬 Navegador de Escenas         │
├─────────────────────────────────┤
│ ESCENA ACTUAL                   │
│ Moai de Rapa Nui 🗿             │
│ Estatuas monolíticas...         │
├─────────────────────────────────┤
│ [← Anterior] [Siguiente →]      │
├─────────────────────────────────┤
│ TODAS LAS ESCENAS (6)           │
│ 🎬 Introducción                 │
│ 🗿 Moai de Rapa Nui ✓           │
│ 🦁 Esfinge de Giza              │
│ ⚔️ Guerrero Antiguo             │
│ 🌍 Comparación Cultural         │
│ 🎉 Final del Tour               │
└─────────────────────────────────┘
```

### Atajos
- Click en escena → Cargar inmediatamente
- Botones Anterior/Siguiente → Navegación secuencial
- Barra de progreso → Ver carga en tiempo real

---

## 🔊 Control de Audio

### Botón Flotante
- **Ubicación**: Esquina superior derecha
- **Icono**: 🔊 (activo) / 🔇 (silenciado)
- **Color**: Azul (activo) / Rojo (silenciado)
- **Acción**: Click para abrir/cerrar panel

### Panel de Control
```
┌─────────────────────────────────┐
│ 🎵 Control de Audio             │
├─────────────────────────────────┤
│ [🔊 Silenciar Todo]             │
├─────────────────────────────────┤
│ 🎚️ Volumen General      [80%]  │
│ ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░        │
├─────────────────────────────────┤
│ 🎵 Música de Fondo      [70%]  │
│ ▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░        │
├─────────────────────────────────┤
│ 🎙️ Narración           [100%]  │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       │
├─────────────────────────────────┤
│ 🔔 Efectos de Sonido    [80%]  │
│ ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░       │
└─────────────────────────────────┘
```

### Controles
- **Volumen General**: Afecta todo el audio
- **Música**: Solo música de fondo
- **Narración**: Solo voice-over
- **Efectos**: Solo sonidos de UI/eventos
- **Silenciar Todo**: Mute instantáneo

---

## 🎯 Escenas Disponibles

### 1. 🎬 Introducción
- **Duración**: 5 segundos
- **Modelos**: Ninguno
- **Cámara**: Vista panorámica
- **Auto-play**: Sí → Pasa a Moai

### 2. 🗿 Moai de Rapa Nui
- **Duración**: 15 segundos
- **Modelos**: moai.glb
- **Cámara**: Vista frontal cercana
- **Audio**: Olas del océano
- **Narración**: Historia de Rapa Nui

### 3. 🦁 Esfinge de Giza
- **Duración**: 15 segundos
- **Modelos**: sphinxWithBase.glb
- **Cámara**: Vista lateral elevada
- **Audio**: Viento del desierto
- **Narración**: Historia de Egipto

### 4. ⚔️ Guerrero Antiguo
- **Duración**: 12 segundos
- **Modelos**: warrior.glb (con animación)
- **Cámara**: Vista media
- **Audio**: Ambiente de batalla
- **Animación**: Idle loop

### 5. 🌍 Comparación Cultural
- **Duración**: 20 segundos
- **Modelos**: moai.glb + sphinx.glb (lado a lado)
- **Cámara**: Vista amplia frontal
- **Iluminación**: Neutral para comparación

### 6. 🎉 Final del Tour
- **Duración**: 5 segundos
- **Modelos**: Ninguno
- **Cámara**: Vista alejada
- **Iluminación**: Atardecer (hora 18)

---

## 💻 API Programática

### SceneSystem

```typescript
// Obtener instancia
const sceneSystem = useSceneStore(state => state.sceneSystem)

// Cargar escena
await sceneSystem.loadScene('moai-scene', (progress) => {
  console.log(`${progress}%`)
})

// Navegar
sceneSystem.nextScene()
sceneSystem.previousScene()

// Consultar
const current = sceneSystem.getCurrentScene()
const all = sceneSystem.getAllScenes()
const isTransitioning = sceneSystem.isInTransition()
```

### AudioSystem

```typescript
// Obtener instancia
const audioSystem = useSceneStore(state => state.audioSystem)

// Cargar track
await audioSystem.loadTrack({
  id: 'music-ocean',
  url: '/audio/ocean.mp3',
  volume: 0.7,
  loop: true,
  type: 'music'
})

// Reproducir
audioSystem.play('music-ocean')
audioSystem.pause('music-ocean')
audioSystem.stop('music-ocean')

// Efectos
audioSystem.fadeIn('music-ocean', 2000)
audioSystem.fadeOut('music-ocean', 2000)
audioSystem.crossfade('music-ocean', 'music-desert', 2000)

// Volumen
audioSystem.setMasterVolume(0.8)
audioSystem.setMusicVolume(0.6)
audioSystem.toggleMute()
```

---

## 🎨 Personalización

### Crear Escena Personalizada

```typescript
// En viewer3d/data/scenes.ts
import * as THREE from 'three'

const miEscena: SceneDefinition = {
  id: 'mi-escena',
  name: 'Mi Escena Personalizada',
  description: 'Una escena única',
  
  models: [
    {
      id: 'modelo1',
      path: '/mi-modelo.glb',
      position: new THREE.Vector3(0, 0, 0),
      rotation: new THREE.Euler(0, Math.PI / 2, 0),
      scale: 1.5
    }
  ],
  
  camera: {
    position: new THREE.Vector3(10, 5, 10),
    target: new THREE.Vector3(0, 1, 0),
    fov: 45,
    transition: {
      duration: 3000,
      easing: 'easeInOut'
    }
  },
  
  lighting: {
    timeOfDay: 14, // 2 PM
    ambient: { 
      intensity: 0.6, 
      color: '#ffffff' 
    },
    directional: { 
      intensity: 1.5, 
      position: [10, 15, 5] 
    }
  },
  
  audio: {
    background: '/audio/mi-musica.mp3',
    narration: '/audio/mi-narracion.mp3',
    volume: 0.8,
    loop: true
  },
  
  duration: 10000, // 10 segundos
  autoPlay: false,
  
  onEnter: () => {
    console.log('🎬 Entrando a mi escena')
  },
  
  onExit: () => {
    console.log('👋 Saliendo de mi escena')
  }
}

// Agregar al array
export const ARCHAEOLOGICAL_SCENES = [
  // ... escenas existentes
  miEscena
]
```

### Agregar Audio Personalizado

```typescript
// 1. Colocar archivo en /public/audio/
// Ejemplo: /public/audio/mi-musica.mp3

// 2. Cargar en código
const audioSystem = new AudioSystem()

await audioSystem.loadTrack({
  id: 'custom-music',
  url: '/audio/mi-musica.mp3',
  volume: 0.7,
  loop: true,
  type: 'music'
})

// 3. Reproducir
audioSystem.fadeIn('custom-music', 2000)
```

---

## 🔧 Troubleshooting

### Escena no carga
```typescript
// Verificar en consola
sceneSystem.getScene('scene-id')
// Si retorna undefined, la escena no está registrada

// Verificar registro
sceneSystem.getAllScenes()
// Debe incluir tu escena
```

### Audio no reproduce
```typescript
// Verificar carga
audioSystem.getAllTracks()
// Debe incluir tu track

// Verificar volumen
audioSystem.getMasterVolume() // > 0
audioSystem.isMutedState() // false

// Verificar reproducción
audioSystem.isPlaying('track-id') // true
```

### Transición bloqueada
```typescript
// Verificar estado
sceneSystem.isInTransition() // false para permitir cambio

// Si está bloqueado, esperar o forzar
// (no recomendado, pero posible)
```

---

## 📊 Performance Tips

### Optimizar Carga
- Usar modelos GLB comprimidos
- Limitar polígonos a <100k por modelo
- Usar texturas comprimidas (JPG/WebP)

### Optimizar Audio
- Usar MP3 comprimido (128-192 kbps)
- Limitar duración de loops
- Precargar audio crítico

### Optimizar Transiciones
- Duración óptima: 2000-3000ms
- Evitar transiciones muy rápidas (<1000ms)
- Usar easing apropiado

---

## 🎓 Ejemplos de Uso

### Tour Automático
```typescript
// Configurar auto-play en todas las escenas
ARCHAEOLOGICAL_SCENES.forEach(scene => {
  scene.autoPlay = true
  scene.duration = 10000 // 10 segundos cada una
})

// Iniciar desde intro
sceneSystem.loadScene('intro')
// Se reproducirá automáticamente
```

### Modo Exploración Libre
```typescript
// Desactivar auto-play
ARCHAEOLOGICAL_SCENES.forEach(scene => {
  scene.autoPlay = false
})

// Usuario navega manualmente
// con SceneNavigator UI
```

### Sincronizar Audio con Escena
```typescript
const scene: SceneDefinition = {
  // ... config
  onEnter: () => {
    audioSystem.fadeIn('music-ocean', 2000)
  },
  onExit: () => {
    audioSystem.fadeOut('music-ocean', 1000)
  }
}
```

---

## 🚀 Próximos Pasos

### Agregar Assets
1. Crear `/public/audio/` directory
2. Agregar archivos MP3
3. Actualizar rutas en `scenes.ts`

### Texto 3D (Opcional)
1. Instalar fuentes typeface.json
2. Crear componente Text3DLabel
3. Agregar a escenas

### Narrativa (Opcional)
1. Crear NarrativeSystem
2. Definir capítulos
3. Implementar ProgressTracker

---

**¿Preguntas?** Consulta `FASE2_PROGRESO.md` para detalles técnicos completos.

**Fecha**: 12 de Febrero, 2026  
**Estado**: ✅ Listo para usar
