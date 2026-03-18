# Análisis de Bundle y Propuestas de Optimización
**Fecha**: 18 de marzo de 2026

## 📊 Análisis del Bundle Actual

### Problemas Identificados

#### 🔴 CRÍTICO: Three.js domina el bundle
- **Problema**: `import * as THREE from 'three'` en ~50+ archivos
- **Impacto**: Tree-shaking NO funciona, se importa TODO Three.js
- **Tamaño estimado**: ~600KB+ de Three.js sin comprimir
- **Archivos afectados**: Casi todos los componentes 3D

#### 🟡 MEDIO: Lazy loading insuficiente
- **Problema**: Escenas 3D ya usan `dynamic()` pero podrían optimizarse más
- **Impacto**: Bundle inicial más grande de lo necesario
- **Estado actual**: 
  - ✅ GizaScene, PumaPunkuScene, TeotihuacanScene, EasterIslandScene usan lazy loading
  - ❌ Muchos componentes weather/effects se cargan eager

#### 🟡 MEDIO: Sistema de clima pesado
- **Componentes weather**: ~15 archivos
- **Todos importan**: `import * as THREE`
- **Problema**: Se cargan todos aunque solo uses algunos efectos

#### 🟢 BAJO: Dependencias "ruido"
- `ua-parser.js` visible en bundle
- Algunas utilidades que podrían ser más ligeras

---

## 🚀 Plan de Optimización (Priorizado)

### FASE 1: Quick Wins (Alto Impacto, Bajo Esfuerzo)

#### 1.1 Optimizar importaciones de Three.js
**Impacto**: 🔥🔥🔥 (Reducción estimada: 30-40% del bundle de Three.js)

**Antes**:
```typescript
import * as THREE from 'three'
const geometry = new THREE.BoxGeometry()
const material = new THREE.MeshStandardMaterial()
```

**Después**:
```typescript
import { BoxGeometry, MeshStandardMaterial, Vector3, Mesh } from 'three'
const geometry = new BoxGeometry()
const material = new MeshStandardMaterial()
```

**Archivos prioritarios** (más usados):
1. `ImmersiveScene.tsx` - Core del juego
2. `TeotihuacanScene.tsx` - Escena pesada
3. `GizaScene.tsx` - Escena pesada
4. `PumaPunkuScene.tsx` - Escena pesada
5. Todos los componentes `weather/*` (15 archivos)

**Estimación**: 2-3 horas de trabajo, 200-300KB de reducción

---

#### 1.2 Lazy load agresivo del sistema de clima
**Impacto**: 🔥🔥 (Reducción estimada: 100-150KB del bundle inicial)

**Crear**: `viewer3d/components/weather/index.ts`
```typescript
import dynamic from 'next/dynamic'

export const RainEffect = dynamic(() => import('./RainEffect'), { ssr: false })
export const SnowEffect = dynamic(() => import('./SnowParticles'), { ssr: false })
export const LightningEffect = dynamic(() => import('./LightningEffect'), { ssr: false })
export const TornadoEffect = dynamic(() => import('./TornadoEffect'), { ssr: false })
export const EarthquakeEffect = dynamic(() => import('./EarthquakeEffect'), { ssr: false })
export const WindEffect = dynamic(() => import('./WindEffect'), { ssr: false })
export const FogEffect = dynamic(() => import('./DynamicFog'), { ssr: false })
export const CloudSky = dynamic(() => import('./CloudSky'), { ssr: false })
```

**Uso**:
```typescript
// En WeatherControl.tsx
import { RainEffect, SnowEffect, LightningEffect } from './weather'

// Solo se cargan cuando se activan
{weather.rainHeavy && <RainEffect />}
{weather.snow && <SnowEffect />}
```

**Estimación**: 1 hora de trabajo, 100-150KB de reducción

---

#### 1.3 Optimizar modelos 3D con mejor compresión
**Impacto**: 🔥🔥 (Reducción estimada: 20-30% de tamaño de modelos)

**Estado actual**:
- ✅ Draco compression nivel 10 (ya implementado)
- ❌ Texturas sin optimizar
- ❌ Algunos modelos podrían usar meshopt compression

**Acciones**:
1. Revisar texturas de modelos (convertir a WebP si es posible)
2. Considerar meshopt compression para modelos muy grandes
3. Verificar que todos los modelos usen Draco

**Estimación**: 2 horas de trabajo, mejora en tiempo de carga

---

### FASE 2: Optimizaciones Arquitectónicas (Alto Impacto, Medio Esfuerzo)

#### 2.1 Separar motor 3D de UI
**Impacto**: 🔥🔥🔥 (Mejora arquitectura + performance)

**Estructura propuesta**:
```
viewer3d/
├── engine/           # Lógica Three.js pura (sin React)
│   ├── core/
│   ├── loaders/
│   └── utils/
├── components/       # React components (UI)
│   ├── ui/          # Componentes UI puros
│   └── 3d/          # Wrappers React para engine
└── scenes/          # Composición de escenas
```

**Beneficios**:
- Mejor tree-shaking
- Posibilidad de mover lógica pesada a Web Workers
- Código más mantenible
- Testing más fácil

**Estimación**: 8-12 horas de trabajo, mejora significativa en arquitectura

---

#### 2.2 Sistema de clima modular con estado global
**Impacto**: 🔥🔥 (Reduce re-renders + bundle)

**Crear**: `viewer3d/systems/WeatherSystem.ts`
```typescript
// Sistema centralizado que maneja estado del clima
// Solo carga efectos cuando se necesitan
class WeatherSystem {
  private effects = new Map()
  
  async enableEffect(type: 'rain' | 'snow' | 'lightning') {
    if (!this.effects.has(type)) {
      const module = await import(`./weather/${type}`)
      this.effects.set(type, module.default)
    }
    return this.effects.get(type)
  }
}
```

**Estimación**: 4-6 horas de trabajo

---

### FASE 3: Optimizaciones Avanzadas (Medio Impacto, Alto Esfuerzo)

#### 3.1 Web Workers para cálculos pesados
**Impacto**: 🔥 (Mejora FPS, no reduce bundle)

**Candidatos**:
- Cálculos astronómicos (SolarEngine)
- Generación procedural de terreno
- Cálculos de física/colisiones

**Estimación**: 12-16 horas de trabajo

---

#### 3.2 Streaming de assets
**Impacto**: 🔥 (Mejora tiempo de carga inicial)

**Implementar**:
- Carga progresiva de modelos 3D
- LOD (Level of Detail) automático
- Priorización de assets visibles

**Estimación**: 8-12 horas de trabajo

---

## 📈 Impacto Estimado Total

### FASE 1 (Quick Wins)
- **Tiempo**: 5-6 horas
- **Reducción bundle**: 300-450KB (~20-25%)
- **Mejora LCP**: 15-20%
- **Prioridad**: 🔥🔥🔥 HACER YA

### FASE 2 (Arquitectura)
- **Tiempo**: 12-18 horas
- **Reducción bundle**: 200-300KB adicional
- **Mejora mantenibilidad**: Significativa
- **Prioridad**: 🔥🔥 HACER PRONTO

### FASE 3 (Avanzado)
- **Tiempo**: 20-28 horas
- **Mejora performance runtime**: Significativa
- **Prioridad**: 🔥 HACER DESPUÉS

---

## 🎯 Recomendación Inmediata

### Empezar con FASE 1.1 + 1.2 (4 horas de trabajo)

**Orden de ejecución**:
1. ✅ Optimizar importaciones Three.js en componentes weather (1h)
2. ✅ Lazy load sistema de clima (1h)
3. ✅ Optimizar importaciones en escenas principales (2h)

**Resultado esperado**:
- Bundle inicial: ~1.5MB → ~1.1MB (27% reducción)
- LCP: ~2.5s → ~2.0s (20% mejora)
- FCP: ~1.2s → ~1.0s (17% mejora)

---

## 🧠 Diagnóstico Final

**Nivel actual**: 70-75% de madurez
**Nivel objetivo**: 85-90% de madurez

**Fortalezas**:
- ✅ Ya usas lazy loading para escenas
- ✅ Modelos optimizados con Draco
- ✅ Code splitting básico funciona
- ✅ Arquitectura de engines separada

**Debilidades**:
- ❌ Importaciones de Three.js sin tree-shaking
- ❌ Sistema de clima carga todo eager
- ❌ Algunos componentes podrían ser más modulares

**Conclusión**: 
Estás en buen camino, pero hay optimizaciones de "bajo esfuerzo, alto impacto" que deberías hacer YA. La FASE 1 te dará el 80% del beneficio con el 20% del esfuerzo.

---

## 📝 Próximos Pasos

1. [ ] Implementar FASE 1.1 (optimizar importaciones Three.js)
2. [ ] Implementar FASE 1.2 (lazy load clima)
3. [ ] Medir impacto con bundle analyzer
4. [ ] Decidir si continuar con FASE 2
