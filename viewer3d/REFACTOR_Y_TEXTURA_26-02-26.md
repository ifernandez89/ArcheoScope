# Refactor ImmersiveScene + Textura Tierra 2K — 26/02/26

## 1. Refactor ImmersiveScene.tsx

### Problema
`ImmersiveScene.tsx` superaba las 1500 líneas — componente "Dios" con todo mezclado: lógica, escenas 3D, elementos de entorno, UI. Deuda técnica real que dificultaba mantenimiento y escalabilidad.

### Solución
Extracción de componentes autónomos a archivos propios:

| Archivo nuevo | Contenido extraído |
|---|---|
| `AmbientParticles.tsx` | Partículas ambientales flotantes |
| `CinematicZoom.tsx` | Zoom cinematográfico al entrar a sitio |
| `SiteInfo.tsx` | Panel de info del sitio arqueológico |
| `SolarSimulation.tsx` | Simulación solar/astronómica |
| `SpaceUfo.tsx` | UFO controlado por mouse en escena espacial |
| `PumaPunkuScene.tsx` | Escena completa Puma Punku (estructura + bloques) |
| `EnvironmentElements.tsx` | Vegetación, rocas, flores, cristales procedurales + `EnvironmentElementsWithTrees` |

### Resultado
- `ImmersiveScene.tsx`: **1591 → 931 líneas** (−41%)
- Duplicados eliminados: `PumaPunkuScene`, `MovablePumaPunkuStructure`, `MovableExtraBlock`, `MovablePumaPunkuBlock`, fragmento roto de SpaceUfo
- `CameraCapture` y `ModelCapture` se mantienen como utilidades locales (acoplamiento directo con Canvas)

---

## 2. Textura Tierra 2K

### Cambio
Reemplazada textura `earth_8k.jpg` (9 MB) por `2k_earth_daymap.jpg` (~1 MB).

### Archivos modificados
- `components/Globe3D.tsx` — carga principal del globo
- `engines/GeoEngine.ts` — carga en engine geoespacial
- `public/textures/2k_earth_daymap.jpg` — textura añadida

### Beneficio
Reducción de ~8 MB en carga inicial del globo sin pérdida visual perceptible.
