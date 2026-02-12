# 🤖 Guía Rápida - FASE 3: Motor IA

## 🎯 Sistemas Disponibles

### 1. Comportamiento Reactivo
El modelo reacciona a tu proximidad y mirada en tiempo real.

### 2. Animaciones Procedurales
Movimientos generados algorítmicamente sin archivos pre-grabados.

### 3. Expresiones Faciales
8 emociones con transiciones suaves y parpadeo automático.

### 4. Chat con IA (Ollama)
Conversación natural con el modelo usando LLM local.

---

## 🤖 Controles IA

### Botón Flotante
- **Ubicación**: Top-right (debajo de Audio Controls)
- **Icono**: 🤖 (rosa/púrpura)
- **Acción**: Click para abrir/cerrar panel

### Panel de Controles
```
┌─────────────────────────────────┐
│ 🤖 Controles IA                 │
├─────────────────────────────────┤
│ 👁️ Comportamiento Reactivo  [●]│
│ 🎭 Animaciones Auto         [○]│
│ 😊 Expresiones Faciales     [●]│
└─────────────────────────────────┘
```

### Toggles
- **Comportamiento Reactivo**: Modelo mira hacia ti cuando te acercas
- **Animaciones Auto**: Movimientos idle continuos
- **Expresiones Faciales**: Emociones y parpadeo automático

---

## 💬 Chat con IA

### Botón Flotante
- **Ubicación**: Bottom-right
- **Icono**: 💬 (púrpura)
- **Acción**: Click para abrir/cerrar chat

### Requisitos
1. Ollama instalado y corriendo
2. Modelo descargado (llama2, mistral, etc.)

### Instalación de Ollama
```bash
# Windows
winget install Ollama.Ollama

# Iniciar servicio
ollama serve

# Descargar modelo
ollama pull llama2
```

### Uso del Chat
1. Click en botón 💬
2. Click en "Conectar"
3. Escribe tu pregunta
4. El modelo responde con emoción y gesto

---

## 🎭 Animaciones Disponibles

### Idle (Respiración)
- **Descripción**: Movimiento sutil de respiración
- **Estilos**: subtle, normal, exaggerated
- **Uso**: Animación de fondo continua

### Walk (Caminar)
- **Descripción**: Caminar procedural con bob vertical
- **Estilos**: subtle (0.3m), normal (0.5m), exaggerated (0.8m)
- **Uso**: Movimiento de patrulla

### Wave (Saludo)
- **Descripción**: Saludo con la mano
- **Estilos**: subtle (30°), normal (50°), exaggerated (80°)
- **Uso**: Reacción a proximidad

### Nod (Asentir)
- **Descripción**: Asentir con la cabeza
- **Estilos**: subtle (10°), normal (20°), exaggerated (40°)
- **Uso**: Confirmación o acuerdo

### Turn (Girar)
- **Descripción**: Girar sobre su eje
- **Estilos**: subtle (45°), normal (180°), exaggerated (360°)
- **Uso**: Cambio de dirección

---

## 😊 Emociones Disponibles

| Emoción | Descripción | Uso |
|---------|-------------|-----|
| 😐 Neutral | Estado base | Default |
| 😊 Happy | Feliz, sonriente | Respuesta positiva |
| 😢 Sad | Triste | Respuesta negativa |
| 😠 Angry | Enojado | Frustración |
| 😲 Surprised | Sorprendido | Descubrimiento |
| 🤔 Curious | Curioso | Pregunta |
| 😕 Confused | Confundido | No entender |
| 🤩 Excited | Emocionado | Entusiasmo |

---

## 💻 Uso Programático

### Comportamiento Reactivo
```typescript
import { ReactiveBehavior } from '@/ai/reactive-behavior'

const behavior = new ReactiveBehavior(engine, {
  proximityRadius: 5.0,
  gazeRadius: 2.0,
  enableLookAt: true
})

behavior.on('proximity', (event) => {
  console.log('Distancia:', event.distance)
})

behavior.start()
```

### Animaciones
```typescript
import { AIAnimator } from '@/ai/animator'

const animator = new AIAnimator()

const idleClip = animator.generateAnimation({
  model: warrior,
  action: 'idle',
  style: 'subtle',
  duration: 3000,
  loop: true
})

animator.playAnimation(warrior, idleClip, true)

// En render loop
animator.update(deltaTime)
```

### Expresiones
```typescript
import { ExpressionSystem } from '@/ai/expression-system'

const expressions = new ExpressionSystem()

// Cambiar emoción
expressions.setEmotion('happy', 500)

// Parpadeo automático
const blinkId = expressions.startAutoBlink(model)

// En render loop
expressions.update(model)
```

### Chat con LLM
```typescript
import { LLMIntegration } from '@/ai/llm-integration'

const llm = new LLMIntegration({
  baseUrl: 'http://localhost:11434',
  model: 'llama2'
})

// Establecer contexto
llm.setContext({
  modelName: 'Moai',
  modelDescription: 'Estatua de Rapa Nui',
  currentScene: 'moai-scene',
  userHistory: []
})

// Enviar mensaje
const response = await llm.sendMessage('¿Qué es esto?')
console.log(response.text)
console.log(response.emotion) // 'curious'
console.log(response.gesture) // 'nod'
```

---

## 🎯 Casos de Uso

### 1. Tour Interactivo
```typescript
// Usuario se acerca
behavior.on('proximity', async (event) => {
  if (event.distance < 3) {
    // Modelo saluda
    expressions.setEmotion('happy', 500)
    const waveClip = animator.generateAnimation({
      model, action: 'wave', duration: 2000
    })
    animator.playAnimation(model, waveClip, false)
    
    // Genera bienvenida
    const response = await llm.generateNarration('Bienvenida')
    console.log(response)
  }
})
```

### 2. Conversación Educativa
```typescript
// Usuario pregunta
const response = await llm.sendMessage(
  '¿Cuándo se construyó?'
)

// Aplicar emoción
if (response.emotion) {
  expressions.setEmotion(response.emotion, 500)
}

// Aplicar gesto
if (response.gesture === 'nod') {
  const nodClip = animator.generateAnimation({
    model, action: 'nod', duration: 1500
  })
  animator.playAnimation(model, nodClip, false)
}
```

### 3. Idle Continuo
```typescript
// Generar idle loop
const idleClip = animator.generateAnimation({
  model,
  action: 'idle',
  style: 'subtle',
  duration: 3000,
  loop: true
})

animator.playAnimation(model, idleClip, true)

// Actualizar en loop
function animate() {
  animator.update()
  expressions.update(model)
  requestAnimationFrame(animate)
}
```

---

## 🔧 Configuración

### Ollama
```bash
# Verificar instalación
ollama --version

# Iniciar servicio
ollama serve

# Listar modelos
ollama list

# Descargar modelo
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

### Configuración en Código
```typescript
// Cambiar modelo
llm.setModel('mistral')

// Cambiar temperatura (creatividad)
llm.config.temperature = 0.9 // Más creativo
llm.config.temperature = 0.3 // Más preciso

// Cambiar max tokens
llm.config.maxTokens = 1000
```

---

## 📊 Performance Tips

### Optimizar Detección
```typescript
// Reducir frecuencia de checks
const behavior = new ReactiveBehavior(engine, {
  proximityRadius: 5.0,
  reactionSpeed: 0.5 // Más lento = menos CPU
})
```

### Optimizar Animaciones
```typescript
// Usar estilos sutiles
const clip = animator.generateAnimation({
  model,
  action: 'idle',
  style: 'subtle', // Menos movimiento = mejor performance
  duration: 3000
})
```

### Cache de Respuestas LLM
```typescript
const cache = new Map<string, OllamaResponse>()

async function getCachedResponse(question: string) {
  if (cache.has(question)) {
    return cache.get(question)
  }
  
  const response = await llm.sendMessage(question)
  cache.set(question, response)
  return response
}
```

---

## 🐛 Troubleshooting

### Ollama no conecta
```typescript
// Verificar disponibilidad
const available = await llm.checkAvailability()
if (!available) {
  console.error('Ollama no disponible')
  console.log('1. Verifica que Ollama esté instalado')
  console.log('2. Ejecuta: ollama serve')
  console.log('3. Verifica puerto 11434')
}
```

### Animaciones no se ven
```typescript
// Asegúrate de llamar update()
function animate() {
  const delta = clock.getDelta()
  animator.update(delta) // ← IMPORTANTE
  requestAnimationFrame(animate)
}
```

### Expresiones no funcionan
```typescript
// Verificar morph targets
model.traverse((child) => {
  if (child.isMesh && child.morphTargetDictionary) {
    console.log('Morph targets:', 
      Object.keys(child.morphTargetDictionary))
  }
})

// Si no hay morph targets, las expresiones no funcionarán
```

### Comportamiento reactivo no responde
```typescript
// Verificar que está iniciado
if (!behavior.isRunning()) {
  behavior.start()
}

// Verificar radio de proximidad
behavior.setConfig({
  proximityRadius: 10.0 // Aumentar radio
})
```

---

## 🎓 Ejemplos Avanzados

### Secuencia de Emociones
```typescript
import { FacialAnimator } from '@/ai/expression-system'

const facial = new FacialAnimator()

await facial.playEmotionSequence(
  model,
  ['neutral', 'curious', 'happy', 'excited'],
  1000 // 1 segundo cada una
)
```

### Trayectoria Circular
```typescript
import { MotionGenerator } from '@/ai/animator'

const path = MotionGenerator.generateCircularPath(
  new THREE.Vector3(0, 0, 0),
  5, // radio
  50 // steps
)

// Animar por la trayectoria
path.forEach((point, i) => {
  setTimeout(() => {
    model.position.copy(point)
  }, i * 100)
})
```

### Blend de Animaciones
```typescript
// Transición suave entre animaciones
animator.blendAnimations(
  model,
  idleClip,
  walkClip,
  1000 // 1 segundo de blend
)
```

---

## 🚀 Integración con Escenas

### Activar IA en Escena
```typescript
// En scene-system.ts
const scene: SceneDefinition = {
  id: 'interactive-moai',
  name: 'Moai Interactivo',
  onEnter: () => {
    // Activar comportamiento
    behavior.start()
    
    // Iniciar idle
    const idleClip = animator.generateAnimation({
      model: moai,
      action: 'idle',
      style: 'subtle',
      duration: 3000
    })
    animator.playAnimation(moai, idleClip, true)
    
    // Emoción neutral
    expressions.setEmotion('neutral', 500)
    
    // Conectar chat
    conversationManager.start({
      modelName: 'Moai',
      modelDescription: 'Estatua de Rapa Nui',
      currentScene: 'interactive-moai',
      userHistory: []
    })
  },
  onExit: () => {
    behavior.stop()
    animator.stopAnimation(moai)
    conversationManager.stop()
  }
}
```

---

## 📚 Recursos

### Documentación
- `FASE3_COMPLETADA.md` - Documentación técnica completa
- `CORE_ENGINE.md` - Arquitectura del Core Engine
- `FASE2_PROGRESO.md` - Sistema de escenas y audio

### Ollama
- [Ollama Website](https://ollama.ai/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Modelos disponibles](https://ollama.ai/library)

### Three.js
- [AnimationMixer](https://threejs.org/docs/#api/en/animation/AnimationMixer)
- [Morph Targets](https://threejs.org/docs/#api/en/core/BufferGeometry.morphAttributes)
- [Raycaster](https://threejs.org/docs/#api/en/core/Raycaster)

---

**¿Preguntas?** Consulta `FASE3_COMPLETADA.md` para detalles técnicos completos.

**Fecha**: 12 de Febrero, 2026  
**Estado**: ✅ Listo para usar
