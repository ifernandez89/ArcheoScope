Auditoría Arquitectónica - ArcheoScope 3D Viewer
Resumen Ejecutivo
| Métrica | Valor Actual | Estado |
|---------|-------------|--------|
| First Load JS | 266 kB | ✅ Bueno |
| Bundle chunks | 3 (vendor, three, r3f) | ✅ Implementado |
| Dynamic imports | ✅ Parcial | ⚠️ Mejora posible |
| LOD | ✅ Implementado | ✅ Bueno |
| Instancing | ✅ Implementado | ✅ Bueno |
| Frustum Culling | ✅ Por defecto | ✅ Bueno |
---
1. Análisis de Arquitectura
Estructura Actual
/app          - Next.js App Router (2 páginas)
/components   - ~90+ componentes React
/engines      - Motores especializados (8 archivos)
/systems      - Sistemas aislados (audio, clima, física)
/hooks        - Custom hooks de React
/store        - Zustand state management
/workers      - Web Workers para procesamiento
Lo que está BIEN implementado:
- Arquitectura modular - Sistemas separados por dominio
- Lazy loading parcial - Scene3D carga dinámica con SSR false
- SplitChunks - Three.js y R3F en chunks separados
- EngineCore - Loop centralizado sin re-renders innecesarios
- Zustand - State management ligero (no Redux)
---
2. Problemas Identificados
🔴 Críticos
1. Componente ImmersiveScene sobredimensionado (1,500+ líneas)
- Un solo componente que maneja: modo globe/model, clima, avatar, terreno, elementos del entorno, biome, audio, transiciones
- Impacto: Re-renders frecuentes afectan toda la escena
2. Importaciones directas de todos los sistemas en ImmersiveScene
// Líneas 3-75: ~70 imports en un solo archivo
import Globe3D from './Globe3D'
import ModelViewer from './ModelViewer'
// ... 70+ más
Esto carga TODO al inicio aunque no se use.
3. No hay code splitting por rutas
- /realistic-solar carga el mismo bundle que /
- Los sistemas solares deberían lazy-loadarse
🟡 Medios
4. Estado local excesivo con useState
- Scene3D.tsx: 10+ estados locales
- ImmersiveScene.tsx: 15+ estados locales
- Debería centralizarse más en Zustand
5. Sistemas "lazy" que no son lazy
// lazy-systems.ts - todos son imports directos
export { default as WeatherSystem } from '@/components/systems/WeatherSystem'
6. Sin memoización en componentes hijos
- EnvironmentElements regenera arrays en cada render (líneas 1094-1244)
7. Documentos de Markdown innecesarios
- ~30 archivos .md en raíz que aumentan tiempo de indexing
- Algunos pesan varios KB
---
3. Recomendaciones de Optimización
Prioridad ALTA (Impacto inmediato)
| # | Optimización | Ahorro estimado |
|---|-------------|-----------------|
| 1 | Lazy load de páginas y componentes pesados | ~80-100 kB inicial |
| 2 | Extraer sistemas de ImmersiveScene a componentes separados | Faster initial parse |
| 3 | Implementar React.memo en componentes 3D | Reduce re-renders 40-60% |
| 4 | Mover estado local a Zustand | Re-renders predecibles |
| 5 | Dynamic imports reales en lazy-systems.ts | Code splitting efectivo |
Prioridad MEDIA
| # | Optimización | Impacto |
|---|-------------|---------|
| 6 | Eliminar ~30 archivos .md de raíz | Limpieza proyecto |
| 7 | Implementar Suspense con fallback | UX mejorada |
| 8 | Usar useMemo para geometrías | GPU menos trabajo |
| 9 | Prefetch de rutas con next/link | Navegación instantánea |
---
4. Plan de Acción Sugerido
Fase 1: Limpieza (~10 min)
1. Mover archivos .md a /docs/
2. Eliminar código muerto en ImmersiveScene
3. Instalar ESLint para prevenir regresiones
Fase 2: Code Splitting (~30 min)
// next.config.js - agregar
experimental: {
  optimizePackageImports: ['three', '@react-three/fiber', '@react-three/drei'],
}
// Importaciones reales lazy:
export const WeatherSystem = dynamic(
  () => import('@/components/systems/WeatherSystem'),
  { ssr: false, loading: () => null }
)
Fase 3: Estado (~20 min)
// Mover a store/scene-store.ts
- movementMode
- selectedLocation
- weather
- isDay
- audioEnabled
Fase 4: Memoización (~15 min)
// Componentes 3D envolver con memo
const Tree3DModel = memo(function Tree3DModel({...}) {
  // ... implementation
})
---
5. Métricas Objetivo
| Métrica | Actual | Objetivo |
|---------|--------|----------|
| First Load JS | 266 kB | < 200 kB |
| Time to Interactive | ~3s | < 2s |
| Bundle chunks | 3 | 5-7 |
| Componentes en memory | 90+ | < 50 principales |
---
6. Tecnologías & Patrones a Conservar
✅ Mantener:
- Next.js 14 con App Router
- React Three Fiber + Drei
- Zustand para estado global
- EngineCore como loop central
- LOD, Instancing, Culling systems