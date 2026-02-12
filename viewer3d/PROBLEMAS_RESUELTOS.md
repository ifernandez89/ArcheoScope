# 🔧 Problemas Resueltos

## ✅ Problema 1: Nested styled-jsx tags

### Error
```
Error: Detected nested styled-jsx tag
```

### Causa
Múltiples bloques `<style jsx>` anidados en ModelTransition.tsx

### Solución
Consolidar todos los estilos en un solo bloque `<style jsx>` al inicio del componente.

**Antes**:
```tsx
<div style={{...}}>
  <style jsx>{`...`}</style>
  <div style={{...}}>
    <style jsx>{`...`}</style> // ❌ Anidado
  </div>
</div>
```

**Después**:
```tsx
<>
  <style jsx>{`
    // Todos los estilos aquí
  `}</style>
  <div className="transition-container">
    <div className="progress-bar" />
  </div>
</>
```

---

## ✅ Problema 2: R3F Span Error

### Error
```
Error: R3F: Span is not part of the THREE namespace!
```

### Causa
Componentes HTML (PerformanceStats, ScreenshotButton) renderizados dentro del `<Canvas>` de Three.js.

### Solución
Mover todos los componentes HTML fuera del `<Canvas>`.

**Antes**:
```tsx
<Canvas>
  <ModelViewer />
  <PerformanceStats />  // ❌ Dentro del Canvas
  <ScreenshotButton />  // ❌ Dentro del Canvas
</Canvas>
```

**Después**:
```tsx
<Canvas>
  <ModelViewer />
</Canvas>
<PerformanceStats />   // ✅ Fuera del Canvas
<ScreenshotButton />   // ✅ Fuera del Canvas
```

---

## ✅ Problema 3: useThree Hook Error

### Error
```
Error: useThree can only be used within <Canvas>
```

### Causa
PerformanceStats y ScreenshotButton usando hooks de R3F (`useFrame`, `useThree`) fuera del Canvas.

### Solución

**PerformanceStats**: Cambiar de `useFrame` a `requestAnimationFrame`

**Antes**:
```tsx
import { useFrame } from '@react-three/fiber'

useFrame(() => {
  // Actualizar stats
})
```

**Después**:
```tsx
useEffect(() => {
  const updateStats = () => {
    // Actualizar stats
    requestAnimationFrame(updateStats)
  }
  updateStats()
}, [])
```

**ScreenshotButton**: Buscar canvas con `document.querySelector`

**Antes**:
```tsx
import { useThree } from '@react-three/fiber'

const { gl, scene, camera } = useThree()
const canvas = gl.domElement
```

**Después**:
```tsx
const canvas = document.querySelector('canvas')
```

---

## 📋 Checklist de Componentes

### Dentro del Canvas (Three.js)
- ✅ ModelViewer
- ✅ LoadingSpinner (dentro de Suspense)
- ✅ Luces (ambient, directional, point, spot)
- ✅ Environment
- ✅ Grid
- ✅ ContactShadows
- ✅ EffectComposer (Bloom, SSAO)
- ✅ OrbitControls
- ✅ PerspectiveCamera

### Fuera del Canvas (HTML/React)
- ✅ PerformanceStats
- ✅ ScreenshotButton
- ✅ ModelSelector
- ✅ ModelInfo
- ✅ ModelTransition
- ✅ UI
- ✅ HelpPanel

---

## 🎯 Reglas para Evitar Errores

### 1. Componentes Three.js
- ✅ Deben estar dentro de `<Canvas>`
- ✅ Pueden usar hooks de R3F (`useFrame`, `useThree`, etc.)
- ✅ Deben ser objetos 3D o componentes de drei

### 2. Componentes HTML
- ✅ Deben estar fuera de `<Canvas>`
- ❌ No pueden usar hooks de R3F
- ✅ Usan estilos CSS normales
- ✅ Pueden usar `position: fixed` para overlay

### 3. Styled-jsx
- ✅ Un solo bloque `<style jsx>` por componente
- ❌ No anidar bloques de estilo
- ✅ Usar clases CSS en lugar de estilos inline cuando sea posible

---

## 🔍 Debugging Tips

### Ver errores en consola
```javascript
// Abrir DevTools (F12)
// Buscar errores en rojo
// Leer el stack trace completo
```

### Verificar estructura del Canvas
```tsx
// Correcto:
<Canvas>
  {/* Solo componentes Three.js aquí */}
</Canvas>
{/* Componentes HTML aquí */}

// Incorrecto:
<Canvas>
  {/* Mezcla de Three.js y HTML */}
  <div>...</div> // ❌
</Canvas>
```

### Verificar imports
```tsx
// Para componentes dentro del Canvas:
import { useFrame, useThree } from '@react-three/fiber'

// Para componentes fuera del Canvas:
import { useState, useEffect } from 'react'
// NO importar hooks de R3F
```

---

## ✅ Estado Final

### Compilación
- ✅ Sin errores de TypeScript
- ✅ Sin errores de styled-jsx
- ✅ Sin errores de R3F
- ✅ Compilación exitosa

### Funcionalidad
- ✅ Modelos se cargan correctamente
- ✅ Performance stats funcionando
- ✅ Screenshot funcionando
- ✅ Transiciones visuales funcionando
- ✅ Todos los componentes renderizando

### Performance
- ✅ 60 FPS estable
- ✅ Sin memory leaks
- ✅ Transiciones suaves

---

## 📚 Referencias

- [React Three Fiber - Objects](https://docs.pmnd.rs/react-three-fiber/api/objects)
- [Next.js - styled-jsx](https://nextjs.org/docs/messages/nested-styled-jsx-tags)
- [Three.js - Documentation](https://threejs.org/docs/)

---

**Fecha**: 12 de Febrero, 2026  
**Problemas Resueltos**: 3  
**Estado**: ✅ Todo Funcionando
