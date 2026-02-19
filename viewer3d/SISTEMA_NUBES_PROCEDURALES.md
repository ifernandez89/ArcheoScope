# Sistema de Nubes Procedurales

## Descripción
Sistema de nubes atmosféricas con generación procedural, aspecto esponjoso tipo algodón, y cambio dinámico según condiciones climáticas.

## Características

### Generación Procedural
- **Textura canvas 1024x512**: Generada en tiempo real, cero archivos externos
- **Nubes esponjosas**: 4-7 "puffs" por nube con forma ovalada horizontal
- **Distribución inteligente**: Solo en mitad superior del cielo (no bajan del horizonte)
- **Variación aleatoria**: Cada nube es única en tamaño, forma y posición

### Modos Climáticos

#### Modo Normal (Clima Despejado)
- Color: Blanco puro con gradientes suaves
- Cantidad: 30 nubes
- Tamaño: 20-50px ancho, 40-70% de altura
- Opacidad: 0.85
- Aspecto: Algodón esponjoso

#### Modo Tormenta
- Color: Gris oscuro (RGB 60-120)
- Cantidad: 40 nubes (más densas)
- Tamaño: 25-65px ancho, 40-70% de altura
- Opacidad: 0.95
- Aspecto: Nubes de tormenta amenazantes

### Arquitectura

```
CloudSky (componente base)
├── Sky Dome (esfera invertida)
│   ├── Radio: 400 unidades
│   ├── Altura: +80 sobre cámara
│   └── Sigue posición de cámara
├── Textura Procedural
│   ├── Canvas 2D context
│   ├── Gradientes radiales escalados (elipses)
│   └── Regenera según stormMode
└── Rotación lenta (sincronizada con viento)

LightClouds (preset recomendado)
└── Wrapper con configuración óptima
```

## Integración

### En WeatherSystem
```tsx
{weather.clouds && (
  <LightClouds 
    opacity={0.9} 
    stormMode={weather.storm || weather.lightning}
  />
)}
```

### Props de CloudSky
```typescript
interface CloudSkyProps {
  enabled?: boolean      // Activar/desactivar
  opacity?: number       // 0-1, transparencia
  speed?: number         // Velocidad de rotación
  height?: number        // Altura sobre cámara
  radius?: number        // Radio del sky dome
  stormMode?: boolean    // Nubes oscuras
}
```

## Técnica de Generación

### Forma Ovalada Esponjosa
```javascript
// Cada nube tiene ancho y alto separados
const baseWidth = 20 + Math.random() * 30
const baseHeight = baseWidth * (0.4 + Math.random() * 0.3) // 40-70% del ancho

// Múltiples puffs con distribución horizontal
for (let j = 0; j < puffCount; j++) {
  const offsetX = (Math.random() - 0.5) * baseWidth * 1.5  // Más ancho
  const offsetY = (Math.random() - 0.5) * baseHeight * 0.8 // Menos alto
  
  // Escalar para crear elipse
  ctx.scale(puffRadiusX / puffRadiusY, 1)
  ctx.arc(0, 0, puffRadiusY, 0, Math.PI * 2)
}
```

### Gradientes Suaves
```javascript
gradient.addColorStop(0, cloudColors.core)    // Centro sólido
gradient.addColorStop(0.3, cloudColors.mid)   // Transición
gradient.addColorStop(0.6, cloudColors.edge)  // Borde suave
gradient.addColorStop(1, cloudColors.fade)    // Fade a transparente
```

## Rendimiento

### Optimizaciones
- **Textura única**: 1024x512 compartida por todas las nubes
- **Sin física**: Solo rotación lenta, no simulación compleja
- **Frustum culling desactivado**: `frustumCulled={false}` (siempre visible)
- **Depth write off**: `depthWrite: false` (no afecta z-buffer)
- **Regeneración condicional**: Solo cuando cambia `stormMode`

### Impacto
- **Memoria**: ~2MB VRAM (textura canvas)
- **CPU**: Mínimo (solo rotación)
- **GPU**: Mínimo (1 draw call)
- **Bundle**: 0 bytes (procedural)

## Coherencia Sistémica

### Sincronización con Viento
```typescript
// Rotación basada en globalWind
const rotationSpeed = windStrength * speed * 0.00005
meshRef.current.rotation.y += rotationSpeed
```

### Integración con Clima
- Activa automáticamente con toggle "☁️ Nubes"
- Cambia a modo tormenta con `weather.storm` o `weather.lightning`
- Compatible con niebla, lluvia, viento simultáneos

## Filosofía de Diseño

### Zero Bundle Weight
- Sin archivos de textura externos
- Generación procedural en cliente
- Variación infinita sin assets

### Realismo Estilizado
- No fotorrealista, pero creíble
- Coherente con estilo low-poly del engine
- Aspecto esponjoso tipo algodón

### Modularidad
- Componente independiente
- Props configurables
- Fácil de extender (más presets)

## Futuras Mejoras (Opcionales)

### Textura Real
```typescript
// Cuando esté disponible
const cloudTexture = useTexture('/textures/clouds_1024.jpg')
```

### Animación de Forma
```typescript
// Morphing sutil de nubes
const noiseOffset = state.clock.elapsedTime * 0.1
material.uniforms.uTime.value = noiseOffset
```

### Parallax Multi-Capa
```typescript
// Capas a diferentes alturas
<CloudSky height={60} speed={0.8} />
<CloudSky height={100} speed={1.2} />
```

## Archivos del Sistema

```
viewer3d/components/weather/
└── CloudSky.tsx                    # Componente principal
    ├── CloudSky (base)
    ├── CloudLayers (alternativa)
    ├── LightClouds (preset)
    └── LayeredClouds (preset avanzado)

viewer3d/components/systems/
└── WeatherSystem.tsx               # Integración

viewer3d/components/
└── WeatherControl.tsx              # Toggle UI
```

## Estado Actual

✅ Implementado y funcional
✅ Integrado en WeatherSystem
✅ Toggle en panel de clima
✅ Modo tormenta automático
✅ Forma esponjosa ovalada
✅ Solo en cielo superior
✅ Build exitoso
✅ Listo para producción

---

**Versión**: 1.0  
**Fecha**: 2026-02-19  
**Bundle Impact**: 0 KB  
**Performance**: Excelente
