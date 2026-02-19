# ⚡ Estrategia de Performance - ArcheoScope

## 🎯 Objetivo

ArcheoScope debe sentirse **instantáneo**. Un motor profesional no bloquea, no carga todo de golpe, no inicializa sistemas que aún no se usan.

---

## 📊 Dos Tipos de Performance (NO confundir)

### 1. Bundle Performance (Carga Inicial)
**Afecta**:
- Tiempo de arranque
- Experiencia inicial
- Eficiencia general
- Uso de memoria al inicio

**Optimizaciones**:
- Code splitting
- Dynamic imports
- Tree shaking
- Lazy loading

### 2. Runtime Performance (FPS)
**Afecta**:
- Draw calls
- Geometrías
- Shaders
- CPU frame loop

**Optimizaciones**:
- LOD
- Instancing
- Frustum culling
- Occlusion culling

**⚠️ Error común**: Pensar que optimizar bundle mejora FPS. Son cosas distintas pero ambas importantes.

---

## 🏗️ Arquitectura Ideal

### Bundle Principal (Ligero)
```
app/
├── page.tsx              # Home ligera
├── layout.tsx            # Layout base
└── components/
    ├── UI básica
    ├── Configuración
    └── WorldState base
```

**Tamaño objetivo**: < 200KB (gzipped)

### Chunk 3D Pesado (Lazy)
```
app/viewer/
└── page.tsx
    └── dynamic(() => import('ImmersiveScene'))
```

**Contenido**:
- Three.js (~500KB)
- R3F (~100KB)
- Postprocessing (~150KB)
- Modelos GLTF (bajo demanda)
- Texturas (bajo demanda)

**Carga**: Solo cuando el usuario entra al viewer

---

## 📈 Mejoras Esperadas

En proyectos similares:
- Bundle principal: ↓ 40-70%
- Tiempo de carga inicial: ↓ notable
- Performance en móviles: ↑ significativa
- Memoria al inicio: ↓ 50%

---

## 🔄 Proceso de Optimización (Orden Correcto)

### ❌ Orden Incorrecto
```
1. Ejecutar bundle analyzer
2. Ver qué pesa
3. Intentar optimizar sin estructura
4. Frustración
```

### ✅ Orden Correcto

#### Fase 1: Refactorizar Estructura (ACTUAL)
- [x] Crear WorldCore modular
- [x] Separar engines en módulos
- [x] Implementar LOD system
- [x] Tests para lógica core
- [ ] Separar UI de lógica 3D
- [ ] Identificar dependencias pesadas
- [ ] Preparar dynamic imports

#### Fase 2: Análisis (PRÓXIMA)
- [ ] Ejecutar `npm run analyze`
- [ ] Identificar módulos pesados
- [ ] Medir impacto real
- [ ] Priorizar optimizaciones

#### Fase 3: Optimización (FUTURA)
- [ ] Dynamic imports para engines
- [ ] Code splitting por ruta
- [ ] Lazy loading de assets
- [ ] Tree shaking agresivo

#### Fase 4: Validación (FUTURA)
- [ ] Medir mejoras reales
- [ ] Testing en diferentes dispositivos
- [ ] Lighthouse scores
- [ ] Real User Monitoring

---

## 🛠️ Infraestructura Ya Implementada

### 1. Bundle Analyzer ✅
```bash
npm run analyze              # Analizar todo
npm run analyze:browser      # Solo browser
npm run analyze:server       # Solo server
```

**Configuración**: `next.config.js`
- Split chunks por vendor
- Three.js en chunk separado
- R3F en chunk separado
- Engines en chunk separado

### 2. Lazy Loading System ✅
```typescript
// utils/lazy-engines.ts
export const loadWorldCore = async () => {
  const { WorldCore } = await import('@/engines/WorldCore')
  return WorldCore
}

// Componentes lazy
export const LazyImmersiveScene = dynamic(
  () => import('@/components/ImmersiveScene'),
  { ssr: false }
)
```

### 3. Performance Monitor ✅
```typescript
// utils/performance-monitor.ts
PerformanceMonitor.getMetrics()
PerformanceMonitor.getOptimizationSuggestions()
PerformanceMonitor.exportMetrics()
```

### 4. Performance Dashboard ✅
```typescript
// components/debug/PerformanceDashboard.tsx
<PerformanceDashboard />
```

---

## 📋 Checklist Pre-Análisis

Antes de ejecutar bundle analyzer, asegurarse de:

- [ ] **Estructura modular clara**
  - Engines separados
  - WorldCore independiente
  - UI desacoplada de lógica 3D

- [ ] **Identificar dependencias pesadas**
  - Three.js (~500KB)
  - @react-three/fiber (~100KB)
  - @react-three/drei (~200KB)
  - postprocessing (~150KB)
  - astronomy-engine (~50KB)

- [ ] **Rutas bien definidas**
  - `/` - Home ligera
  - `/viewer` - Escena 3D pesada
  - `/realistic-solar` - Sistema solar

- [ ] **Dynamic imports preparados**
  - Componentes 3D
  - Engines pesados
  - Assets bajo demanda

---

## 🎯 Estrategia de Carga

### Nivel 1: Crítico (Inmediato)
```typescript
// Carga síncrona
- Layout base
- UI básica
- Configuración
- WorldState (solo estado)
```

### Nivel 2: Importante (Lazy)
```typescript
// Carga cuando se necesita
- ImmersiveScene (dynamic import)
- WorldCore completo
- Three.js + R3F
```

### Nivel 3: Bajo Demanda (Async)
```typescript
// Carga progresiva
- Modelos GLTF
- Texturas HD
- Engines específicos (Astro, Solar)
```

### Nivel 4: Preload (Background)
```typescript
// Precarga inteligente
- Siguiente escena probable
- Assets comunes
- Engines frecuentes
```

---

## 🧪 Métricas Objetivo

### Bundle Size
- **Principal**: < 200KB (gzipped)
- **3D Chunk**: < 800KB (gzipped)
- **Total**: < 1.5MB (gzipped)

### Load Time
- **First Contentful Paint**: < 1s
- **Time to Interactive**: < 2s
- **3D Scene Ready**: < 3s

### Runtime Performance
- **FPS**: > 55 (desktop), > 30 (mobile)
- **Frame Time**: < 16.67ms
- **Memory**: < 500MB

### Lighthouse Scores
- **Performance**: > 90
- **Accessibility**: > 95
- **Best Practices**: > 90
- **SEO**: > 90

---

## 🔍 Cuándo Ejecutar Bundle Analysis

### ✅ Ejecutar AHORA si:
- Estructura modular completa
- Engines bien separados
- UI desacoplada de 3D
- Dynamic imports preparados

### ❌ NO ejecutar si:
- Código monolítico
- Todo mezclado
- Sin separación clara
- Imports directos everywhere

**Estado actual**: ✅ Casi listo (falta separar UI de 3D)

---

## 📚 Próximos Pasos

### 1. Separar UI de Lógica 3D
```typescript
// ❌ Actual
ImmersiveScene.tsx (todo junto)

// ✅ Objetivo
app/
├── page.tsx (UI ligera)
└── viewer/
    └── page.tsx (dynamic import)
```

### 2. Identificar Imports Pesados
```bash
# Buscar imports directos de Three.js
grep -r "from 'three'" --include="*.tsx"

# Buscar imports de engines
grep -r "from '@/engines'" --include="*.tsx"
```

### 3. Preparar Dynamic Imports
```typescript
// Convertir imports estáticos
import { ImmersiveScene } from '@/components/ImmersiveScene'

// A dynamic imports
const ImmersiveScene = dynamic(
  () => import('@/components/ImmersiveScene'),
  { ssr: false }
)
```

### 4. Ejecutar Análisis
```bash
npm run analyze
```

### 5. Interpretar Resultados
- Identificar módulos > 100KB
- Verificar duplicados
- Buscar oportunidades de splitting

---

## 🎓 Conceptos Clave

### Code Splitting
Dividir código en chunks que se cargan bajo demanda.

### Tree Shaking
Eliminar código no usado del bundle final.

### Dynamic Import
Cargar módulos solo cuando se necesitan.

### Lazy Loading
Diferir carga de recursos no críticos.

### Preloading
Cargar recursos en background antes de necesitarlos.

### Critical Path
Recursos mínimos necesarios para renderizar la página.

---

## 🚀 Visión a Largo Plazo

### Fase 1 (Actual): Fundación
- Estructura modular
- Engines separados
- LOD implementado
- Tests básicos

### Fase 2 (Próxima): Optimización
- Bundle analysis
- Dynamic imports
- Code splitting
- Lazy loading

### Fase 3 (Futura): Avanzado
- Service Workers
- Caching estratégico
- Preloading inteligente
- Progressive Web App

### Fase 4 (Profesional): Monitoreo
- Real User Monitoring
- Performance budgets
- Automated testing
- CI/CD integration

---

## 💡 Principios Guía

1. **No optimizar prematuramente**
   - Primero estructura
   - Luego medir
   - Después optimizar

2. **Medir siempre**
   - Antes de optimizar
   - Durante optimización
   - Después de optimizar

3. **Priorizar impacto**
   - 80/20 rule
   - Optimizar lo que más pesa
   - Ignorar micro-optimizaciones

4. **Mantener simplicidad**
   - Código claro > código rápido
   - Optimización debe ser invisible
   - No sacrificar mantenibilidad

---

## 📖 Referencias

- [Next.js Bundle Analyzer](https://www.npmjs.com/package/@next/bundle-analyzer)
- [Web.dev Performance](https://web.dev/performance/)
- [Three.js Performance Tips](https://threejs.org/docs/#manual/en/introduction/Performance-tips)
- [React Performance](https://react.dev/learn/render-and-commit)

---

**Estado**: 🟡 Infraestructura lista, esperando refactorización final  
**Próximo paso**: Separar UI de lógica 3D  
**Objetivo**: Motor profesional que se siente instantáneo
