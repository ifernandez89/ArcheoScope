# 🎬 Guía de Animaciones para Avatares

## ✅ Verificar si tu modelo tiene animaciones

### Opción 1: Visor Online
Abre tu modelo en: **https://gltf-viewer.donmccurdy.com/**

Si abajo ves algo como:
```
Animations:
  - Idle
  - Walk
  - Run
```
✅ Perfecto! Ya están embebidas.

Si NO aparecen animaciones → el modelo no tiene rig animado.

### Opción 2: Consola del Navegador
Al cargar el avatar en ArcheoScope, revisa la consola:
```
🚶 Avatar cargado: { animaciones: ['Idle', 'Walk', 'Run'] }
🎬 Animaciones disponibles:
  1. Idle
  2. Walk
  3. Run
```

## 🚀 Agregar Animaciones con Mixamo

Si tu modelo NO tiene animaciones:

1. Ve a **https://www.mixamo.com/**
2. Sube tu modelo `.glb` o `.fbx`
3. Selecciona animaciones:
   - **Idle** (recomendado: "Idle" o "Standing Idle")
   - **Walk** (recomendado: "Walking" o "Standard Walk")
   - **Run** (opcional)
   - **Talking** (opcional para IA)
4. Descarga como `.glb` con:
   - ✅ Skin
   - ✅ Without Skin (si quieres solo animaciones)
5. Reemplaza tu modelo en `/public/`

## 🎭 Tipos de Avatares y Movimiento

### Sistema de Detección Automática

El sistema detecta automáticamente el tipo de avatar y aplica el movimiento apropiado:

#### 🗿 Estatua (Moai)
**Estilo**: Deslizamiento místico
- ✅ Se desplaza suavemente sin caminar
- ✅ Oscilación vertical sutil al moverse (0.015 unidades)
- ✅ Leve inclinación hacia adelante
- ✅ "Respiración" cuando está quieto (0.005 unidades)
- ✅ No requiere animaciones de rig

**Animación Procedural**:
```javascript
// Oscilación al moverse
position.y += Math.sin(time * 3) * 0.015
rotation.x = Math.sin(time * 2) * 0.03

// Respiración quieto
position.y += Math.sin(time * 1.5) * 0.005
```

#### 🦁 Criatura (Sphinx)
**Estilo**: Movimiento con peso majestuoso
- ✅ Balanceo lateral al caminar
- ✅ Inclinación con peso hacia adelante
- ✅ Retorno suave a posición neutral
- ✅ No requiere animaciones de rig

**Animación Procedural**:
```javascript
// Balanceo al moverse
rotation.z = Math.sin(time * 2.5) * 0.05
rotation.x = 0.08

// Volver a neutral
rotation.z *= 0.9
rotation.x *= 0.9
```

#### ⚔️ Humanoide (Warrior)
**Estilo**: Caminar normal con animaciones
- ✅ Usa animaciones de rig (Idle/Walk)
- ✅ Transiciones suaves fadeIn/fadeOut
- ✅ Requiere modelo con animaciones embebidas

## 📁 Modelos Actuales

### `/public/warrior.glb`
- Tipo: 🗡️ Humanoide
- Estado: ❓ Verificar animaciones
- Uso: Avatar principal con rig
- Requiere: Idle + Walk animations

### `/public/moai.glb`
- Tipo: 🗿 Estatua
- Estado: ✅ Funciona sin animaciones
- Uso: Deslizamiento místico
- Animación: Procedural (oscilación)

### `/public/sphinx.glb`
- Tipo: 🦁 Criatura
- Estado: ✅ Funciona sin animaciones
- Uso: Movimiento majestuoso
- Animación: Procedural (balanceo)

## 🎮 Cómo Funcionan las Animaciones

### Sistema Actual
```typescript
// Estado del avatar
state = 'idle' | 'walking'

// Detección automática de animaciones
const idleAnim = names.find(n => 
  n.toLowerCase().includes('idle') || 
  n.toLowerCase().includes('stand')
)

const walkAnim = names.find(n => 
  n.toLowerCase().includes('walk') || 
  n.toLowerCase().includes('run')
)

// Transición suave
if (state === 'walking') {
  actions[idleAnim]?.fadeOut(0.3)
  actions[walkAnim]?.fadeIn(0.3).play()
}
```

### Controles
- **W/S/A/D** → Activa estado `walking`
- **Sin teclas** → Activa estado `idle`
- **Q/E** → Rotación (mantiene animación actual)

## 🔧 Solución de Problemas

### Problema: Avatar no se anima
**Causa**: Modelo sin animaciones embebidas

**Solución**:
1. Verifica en gltf-viewer.donmccurdy.com
2. Si no tiene animaciones, usa Mixamo
3. Descarga con animaciones incluidas
4. Reemplaza el archivo en `/public/`

### Problema: Animación incorrecta
**Causa**: Nombres de animaciones no detectados

**Solución**:
Revisa la consola para ver nombres exactos:
```javascript
🎬 Animaciones detectadas: {
  idle: "Standing Idle",
  walk: "Walking Forward",
  todas: ["Standing Idle", "Walking Forward", "Running"]
}
```

Ajusta la búsqueda en `WalkableAvatar.tsx` si es necesario.

## 🎯 Animaciones Recomendadas

### Básicas (Mínimo)
- ✅ **Idle** - Estar quieto
- ✅ **Walk** - Caminar

### Intermedias
- **Run** - Correr (para velocidad aumentada)
- **Strafe Left/Right** - Movimiento lateral

### Avanzadas (Futuro)
- **Talking** - Hablar (para IA conversacional)
- **Head Turn** - Girar cabeza
- **Wave** - Saludar
- **Point** - Señalar

## 📊 Estado Actual del Sistema

✅ Sistema de animaciones implementado  
✅ Detección automática de nombres  
✅ Transiciones suaves (fadeIn/fadeOut)  
✅ Logs de debug en consola  
❓ Verificar modelos actuales  
⏳ Agregar más animaciones según necesidad

## 🔗 Recursos

- **Mixamo**: https://www.mixamo.com/
- **GLTF Viewer**: https://gltf-viewer.donmccurdy.com/
- **Three.js Animations**: https://threejs.org/docs/#api/en/animation/AnimationMixer
- **React Three Fiber**: https://docs.pmnd.rs/react-three-fiber/
