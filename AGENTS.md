# AGENTS.md — Archeoscope: The Forgotten Relics

Guía de trabajo para agentes de IA (Kiro, Claude, etc.) que colaboren en este proyecto.
Captura las convenciones, reglas y flujos de trabajo establecidos a lo largo del desarrollo.

---

## 🧭 Contexto del Proyecto

**Archeoscope: The Forgotten Relics** es una aplicación web 3D arqueológica/astronómica con dos modos:

- **PC (juego completo)**: exploración 3D de sitios arqueológicos, misiones, NPCs, inventario, naves UFO, HarmoniaMundi
- **Mobile (demo astronómica)**: menú con secciones independientes — Hoy, Constelaciones, Astrología, Calendarios, Clima, Brújula, Información

**Stack**: Next.js 14.2.35 (App Router) · React 18 · Three.js · React Three Fiber · TypeScript · Bun · GitHub Pages

**Repositorio**: `ifernandez89/ArcheoScope`  
**Deploy**: GitHub Pages en `/ArcheoScope` (basePath en producción)  
**Autor**: Ignacio Fernandez — `nacho.xiphos@gmail.com`

---

## 🚨 REGLAS ABSOLUTAS — Leer antes de cualquier acción

### 1. NUNCA hacer git commit ni git push sin permiso explícito

```
❌ PROHIBIDO ejecutar git commit o git push sin que el usuario lo pida en ese mensaje.
✅ El usuario testea primero, luego pide explícitamente "commit y push".
```

Esta regla está reforzada por el hook `.kiro/hooks/no-commit-without-permission.kiro.hook`.

### 2. SIEMPRE actualizar CHANGELOG.md antes de pushear

- Formato: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- Versionado: Semantic Versioning (`v1.x.x`)
- Entrada nueva al tope del archivo, con fecha y sección `### Added / ### Fixed / ### Changed`
- Si hay conflicto de merge en CHANGELOG.md: mantener AMBAS versiones, crear entrada nueva con versión superior

### 3. NUNCA afectar la versión PC al modificar mobile

- PC y mobile tienen layouts completamente separados
- `menuOptions` (PC) y `mobileOptions` (mobile) son arrays independientes en `menu/page.tsx`
- Cambios en mobile NO deben tocar la lógica del juego PC

### 4. Build exit code 1 es NORMAL

```bash
bun run build  # exit code 1 = solo ESLint warnings — NO es un error real
               # exit code 1 con "Type error:" o "Failed to compile" = SÍ es error
```

Siempre verificar el output completo, no solo el exit code.

---

## 🛠️ Skills Instaladas — USO OBLIGATORIO

El proyecto tiene **24 skills instaladas** en `.kiro/skills/` y `.agents/skills/`. Deben usarse activamente para mantener calidad y consistencia:

| Skill | Cuándo usarla |
|-------|--------------|
| `react-three-fiber` | Cualquier componente dentro del Canvas de R3F |
| `threejs-fundamentals` | Geometrías, escenas, cámara, renderer |
| `threejs-animation` | `useFrame`, animaciones, interpolaciones |
| `threejs-geometry` | Creación/modificación de geometrías |
| `threejs-interaction` | Raycasting, eventos de pointer, click en 3D |
| `threejs-lighting` | Luces, sombras, iluminación de escenas |
| `threejs-loaders` | Carga de GLB/GLTF, texturas, assets |
| `threejs-materials` | Materiales, shaders básicos, emissive |
| `threejs-postprocessing` | Bloom, SSAO, efectos de post-proceso |
| `threejs-shaders` | GLSL, ShaderMaterial, uniforms |
| `threejs-textures` | Texturas, UV mapping, optimización |
| `react-best-practices` | Hooks, memoización, patrones de componentes |
| `composition-patterns` | Composición de componentes React |
| `next-best-practices` | App Router, SSR/SSG, optimizaciones Next.js |
| `next-cache-components` | Caching, revalidación, Server Components |
| `frontend-design` | CSS responsive, `clamp()`, mobile UX |
| `typescript-advanced-types` | Tipos complejos, generics, type guards |
| `accessibility` | ARIA, touch targets, contraste, WCAG |
| `bun` | Scripts, instalación de dependencias, build |
| `nodejs-best-practices` | Patrones de módulos, async/await |
| `nodejs-backend-patterns` | API routes, middleware |
| `vitest` | Tests unitarios, mocks, coverage |
| `seo` | Meta tags, Open Graph, manifest |
| `next-upgrade` | Migraciones de versión de Next.js |

**Regla**: Antes de implementar cualquier feature que involucre estas áreas, consultar la skill correspondiente para seguir los patrones establecidos.

---

## 📁 Estructura del Proyecto

```
ArcheoScope/
├── AGENTS.md                    ← este archivo
├── CHANGELOG.md                 ← historial de versiones (SIEMPRE actualizar)
├── CONTRIBUTING.md
├── .kiro/
│   ├── hooks/                   ← hooks de Kiro (no-commit-without-permission)
│   └── steering/                ← reglas auto-incluidas (3d-performance-rules.md)
└── viewer3d/                    ← aplicación Next.js
    ├── app/                     ← páginas (App Router)
    │   ├── page.tsx             ← landing (botón Entrar)
    │   ├── menu/page.tsx        ← menú PC + mobile
    │   ├── menu/astrology/      ← astrología (mobile + PC)
    │   ├── menu/calendarios/    ← calendarios (Hoy, Tzolk'in, Babilónico, Dreamspell)
    │   ├── menu/weather/        ← clima local
    │   ├── menu/brujula/        ← brújula (mobile only)
    │   ├── menu/info/           ← información (filtra secciones PC en mobile)
    │   ├── game/                ← juego PC
    │   └── training/            ← training room
    ├── components/              ← componentes React/Three.js
    ├── systems/                 ← sistemas de audio, ayuda, gráficos
    │   ├── HarmoniaMundiSystem.ts
    │   ├── helpSystem.ts        ← toggle de ayuda contextual
    │   ├── ProceduralAudio.ts
    │   └── GraphicsPresets.ts
    ├── data/                    ← JSON de datos
    │   ├── helpTips.json        ← tips de ayuda contextual
    │   └── archaeological-sites.json
    ├── engines/                 ← motores (Solar, Terrain, Avatar, etc.)
    ├── types/                   ← gameSettings, missionState, player
    ├── lib/                     ← utilidades (paths, astronomy, performance)
    └── public/                  ← assets estáticos (GLB, texturas, fuentes)
```

---

## 🔧 Comandos Esenciales

```bash
# Siempre ejecutar desde viewer3d/
bun run build          # build de producción (verificar antes de commit)
bun run dev            # servidor de desarrollo (puerto 3000)
bun run test           # tests con vitest
bun run lint           # ESLint

# Git (solo cuando el usuario lo pide explícitamente)
git add -A
git commit -m "vX.X.X: descripción concisa"
git push origin main
```

**Importante**: Usar `cwd: viewer3d` en todos los comandos de build/dev/test.

---

## 🎨 Convenciones de Código

### TypeScript / React

```typescript
// ✅ Componentes funcionales con hooks
export default function MyComponent({ prop }: { prop: string }) { ... }

// ✅ Memoización obligatoria para cálculos costosos
const data = useMemo(() => expensiveCalc(dep), [dep])

// ✅ Refs para valores que no deben causar re-render
const posRef = useRef(new THREE.Vector3())

// ✅ Imports de assets siempre con getAssetPath()
import { getAssetPath } from '@/lib/paths'
const model = getAssetPath('/ufo_1.glb')

// ❌ NUNCA hardcodear rutas de assets
const model = '/ArcheoScope/ufo_1.glb'  // ❌
```

### CSS / Estilos Mobile

```css
/* ✅ Siempre usar clamp() para tipografía responsive */
font-size: clamp(14px, 3.5vw, 18px);

/* ✅ Touch targets mínimo 44px (WCAG) */
min-height: 44px;
-webkit-tap-highlight-color: transparent;
touch-action: manipulation;

/* ❌ NUNCA hardcodear font-sizes fijos en mobile */
font-size: 14px;  /* ❌ en componentes mobile */
```

### Three.js / React Three Fiber

Ver `.kiro/steering/3d-performance-rules.md` para reglas completas. Resumen:

```typescript
// ✅ Reutilizar vectores — NUNCA crear en useFrame
const tmpVec = useRef(new THREE.Vector3())
useFrame(() => { tmpVec.current.set(x, y, z) })

// ✅ Cachear meshes — NUNCA traverse() en useFrame
const meshes = useRef<THREE.Mesh[]>([])
useEffect(() => { scene.traverse(c => { if (c.isMesh) meshes.current.push(c) }) }, [])

// ✅ Frame skip para operaciones costosas
const skip = useRef(0)
useFrame(() => { if (++skip.current < 10) return; skip.current = 0; /* lógica */ })

// ✅ Dynamic imports para componentes pesados del Canvas
const HeavyComponent = dynamic(() => import('./HeavyComponent'), { ssr: false })

// ✅ ProximityHelpDetector y CompassTracker: import directo (no dynamic) — usan useFrame
import ProximityHelpDetector from './ProximityHelpDetector'
```

---

## 📱 Mobile vs PC — Separación Estricta

### Detección de dispositivo

```typescript
// Patrón estándar del proyecto
const [isMobile, setIsMobile] = useState(false)
useEffect(() => {
  const check = () => setIsMobile(
    /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth < 768
  )
  check()
  window.addEventListener('resize', check)
  return () => window.removeEventListener('resize', check)
}, [])
```

### Secciones exclusivas

| Feature | PC | Mobile |
|---------|----|----|
| Juego 3D completo | ✅ | ❌ |
| Misiones / NPCs | ✅ | ❌ |
| HarmoniaMundi | ✅ | ❌ |
| Requerimientos mínimos (info) | ✅ | ❌ |
| Arte Generativo / Calidad Gráfica | ✅ | ❌ |
| Brújula | ❌ | ✅ |
| Astrología | ✅ | ✅ |
| Calendarios | ✅ | ✅ |
| Clima Local | ✅ | ✅ |
| Constelaciones | ✅ | ✅ |

### Menú mobile — orden fijo

```
🌍 Hoy (primary — verde)
✦ Constelaciones
🪐 Astrología
📅 Calendarios
🌦 Clima
🧭 Brújula
ℹ Información
```

---

## 🌐 Rutas de Assets

```typescript
// En producción: /ArcheoScope/modelo.glb
// En desarrollo: /modelo.glb
// SIEMPRE usar getAssetPath():
import { getAssetPath } from '@/lib/paths'
const path = getAssetPath('/ufo_1.glb')

// Excepción: logos en page.tsx y menu/page.tsx usan process.env.NODE_ENV directamente
const LOGO = process.env.NODE_ENV === 'production'
  ? '/ArcheoScope/branding/logo/logo-main.png'
  : '/branding/logo/logo-main.png'
```

---

## 🔊 Sistema de Audio

### HarmoniaMundiSystem

- Singleton: `getHarmoniaMundi()`
- Solo PC — NO cargar en mobile
- Frecuencias planetarias basadas en Kepler (Harmonices Mundi)
- Tierra: 136.10 Hz ("Om cósmico")
- `enable()` requiere interacción del usuario (AudioContext policy)
- `dispose()` al salir del juego

### ProceduralAudio / ClimateAudioSystem

- Disponibles en PC y mobile (versión reducida)
- `MOBILE_STORM_WEATHER`: tormenta sin rayos para evitar crash de memoria en Edge mobile

---

## 🗺️ Sitios Arqueológicos — Posiciones NPC

Posiciones hardcodeadas en `ImmersiveScene.tsx` (usadas por Oracle scan y ProximityHelpDetector):

| Sitio | NPC | Posición [x, z] |
|-------|-----|-----------------|
| Giza | Sphinx | [100, 50] |
| Giza | Ramesses | [-20, -50] |
| Giza | Hatshepsut | [20, -50] |
| Giza | Akhenaten | [0, 0] |
| Giza | Mummy | [-72, -2] |
| Puma Punku | Viracocha | [14.5, 0.83] |
| Puma Punku | FuenteMagna | [0, 0] |
| Easter Island | Hotu Matua | [0, 0] |
| Easter Island | Merkaba | [0, 0] |
| Easter Island | Ballena | [-55, 55] |
| Teotihuacán | Quetzalcóatl | [0, 0] |
| Teotihuacán | CalendarioMaya | [0, -20] |
| Tres Zapotes | Atlante | [0, 0] |
| Göbekli Tepe | Monolito | [0, 0] |
| Göbekli Tepe | Astronauta | [-55, -55] |

Geoglifos (todos los sitios): posición `[-83, -67]`, radio 18 unidades.

---

## 🔭 Motor Astronómico

**Librería**: `astronomy-engine` (VSOP87/ELP, precisión ~1 arcmin)

```typescript
import * as Astronomy from 'astronomy-engine'

// Posición lunar
const t = Astronomy.MakeTime(new Date())
const moonLon = Astronomy.EclipticLongitude(Astronomy.Body.Moon, t)
const phaseAngle = Astronomy.MoonPhase(t)

// Próxima fase
const nextQ = Astronomy.SearchMoonQuarter(t)

// Búsqueda de luna llena
const nextFull = Astronomy.SearchMoonPhase(180, t, 35)
```

**Regla**: NUNCA usar algoritmos manuales de fase lunar — siempre `astronomy-engine`.

---

## 💾 Estado Persistente

| Sistema | Clave localStorage | Descripción |
|---------|-------------------|-------------|
| Game settings | `game_settings` | Audio, video, controles |
| Help toggle | `archeoscope_help_enabled` | Ayuda contextual ON/OFF |
| Weather cache | `archeoscope_weather_full` | Cache 30 min |
| Inventory | `inv_scarab`, `inv_skull`, etc. | Items del juego |
| Game timer | `game_timer_seconds` | Cronómetro de partida |
| Graphics preset | `graphics_preset` | LOW/MEDIUM/HIGH/ULTRA |
| Magna Bowl | `magna_bowl_thanked` | Flag de diálogo |

**Patrón de lectura**:
```typescript
import { loadGameSettings } from '@/types/gameSettings'
const settings = loadGameSettings() // siempre con fallback a DEFAULT_GAME_SETTINGS
```

---

## 🎮 Sistema de Ayuda Contextual

Implementado en `v1.1.2`. Archivos clave:

- `systems/helpSystem.ts` — toggle global (`isHelpEnabled()`, `toggleHelp()`)
- `components/HelpBubble.tsx` — UI del botón `?` + diálogo
- `components/ProximityHelpDetector.tsx` — detector dentro del Canvas (usa `useFrame`)
- `data/helpTips.json` — 30+ tips por tipo de objeto

**Regla**: `ProximityHelpDetector` debe importarse directamente (NO con `dynamic()`), ya que usa `useFrame` y debe estar dentro del Canvas sin Suspense boundary.

**Toggle en menú PC**: opción "Ayuda ON/OFF" — verde cuando activa, gris cuando desactivada.

---

## 🔄 Flujo de Trabajo Estándar

### Para cada feature nueva:

1. **Leer código existente** antes de escribir — nunca asumir la estructura
2. **Verificar qué skills aplican** y consultarlas
3. **Implementar** siguiendo las convenciones del proyecto
4. **Verificar build**: `bun run build` en `viewer3d/` — confirmar que no hay `Type error:`
5. **Actualizar CHANGELOG.md** con la nueva entrada
6. **Esperar confirmación del usuario** para testear
7. **Solo cuando el usuario pide explícitamente**: `git add -A && git commit -m "vX.X.X: ..." && git push origin main`

### Para fixes:

- Commits de fix: `fix: descripción del problema resuelto`
- Si el fix es parte de una versión: incluir en la entrada del CHANGELOG correspondiente

### Mensajes de commit:

```
v1.1.2: descripción concisa del feature principal
fix: descripción del bug resuelto
```

---

## ⚠️ Errores Conocidos y Soluciones

### Build CI falla con Next.js 16 / Turbopack

**Causa**: `package-lock.json` en `.gitignore` → `npm install` resuelve versiones libremente  
**Solución**: `package-lock.json` debe estar en el repo. CI usa `npm ci`. Next.js fijado en `14.2.35`.

### `git push` queda colgado con prompt interactivo

**Causa**: Git GC intenta limpiar pack files bloqueados en Windows  
**Solución**: `git config gc.auto 0` antes del push, o esperar que el proceso background termine.

### `DeviceOrientationEvent` falla en SSR

**Causa**: La API no existe en Node.js  
**Solución**: Siempre guardar con `typeof window !== 'undefined'` y `typeof (DeviceOrientationEvent as any).requestPermission === 'function'`

### Componentes Three.js con `dynamic()` rompen `useFrame`

**Causa**: `dynamic()` envuelve en Suspense boundary que rompe el contexto de R3F  
**Solución**: Importar directamente los componentes que usan `useFrame` (`ProximityHelpDetector`, `CompassTracker`, etc.)

### CHANGELOG con conflicto de merge

**Causa**: Commits paralelos en el mismo archivo  
**Solución**: Mantener ambas versiones, crear entrada nueva con versión superior, eliminar markers `<<<<<<< HEAD`.

---

## 📐 Posiciones Fijas Importantes (Three.js)

```typescript
// Giza
const PYRAMIDION_GROUND: [number, number, number] = [100, 0.5, 35]
const PYRAMIDION_TOP: [number, number, number] = [0, 45.48, 0]

// Geoglifos (todos los sitios)
const GEOGLYPH_POSITION: [number, number, number] = [-83, 0.3, -67]

// Portales genéricos
const PORTAL_POSITION: [number, number, number] = [0, 0, 30]

// Training Room — avatar inicial
const TRAINING_INITIAL_POSITION: [number, number, number] = [0, 10, 0]
```

---

## 🔑 Fuente del Proyecto

**Fuente principal**: `Spaceport_2006.otf` (cargada como `--font-archeoscope` en `layout.tsx`)

```typescript
// En componentes: usar fontFamily: 'Archeoscope, serif'
// Con font-weight: normal (la fuente no tiene variante bold — faux bold distorsiona los glifos)
style={{ fontFamily: 'Archeoscope, serif', fontWeight: 'normal' }}
```

---

## 📋 Checklist Pre-Commit

Antes de hacer commit (cuando el usuario lo pida):

- [ ] `bun run build` pasa sin `Type error:` ni `Failed to compile`
- [ ] CHANGELOG.md actualizado con la versión correcta y fecha
- [ ] No hay `console.log` de debug innecesarios
- [ ] Assets referenciados con `getAssetPath()`
- [ ] Mobile no afectado si el cambio es solo PC (y viceversa)
- [ ] Sin conflictos de merge en ningún archivo

---

## 🌐 Deploy

**GitHub Pages** — deploy automático via GitHub Actions al pushear a `main`.

```javascript
// next.config.js
basePath: process.env.NODE_ENV === 'production' ? '/ArcheoScope' : ''
assetPrefix: process.env.NODE_ENV === 'production' ? '/ArcheoScope/' : ''
```

URL producción: `https://ifernandez89.github.io/ArcheoScope`

---

## 📜 Licencia

- **Código fuente**: CC BY-NC 4.0 (uso educativo/investigación con atribución)
- **Assets** (modelos 3D, texturas, audio, música): All Rights Reserved © 2026 Ignacio Fernandez
- Licencias comerciales disponibles bajo solicitud

---

*Última actualización: v1.1.2 — Mayo 2026*
