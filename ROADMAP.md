# 🗺️ Roadmap — Archeoscope: The Forgotten Relics

> Estado actual: **v1.2.8** — activo en desarrollo  
> Deploy: [ifernandez89.github.io/ArcheoScope](https://ifernandez89.github.io/ArcheoScope)

---

## ✅ Completado

### v1.0 — Base
- [x] Exploración 3D con React Three Fiber + Next.js
- [x] 6 sitios arqueológicos (Giza, Puma Punku, Teotihuacán, Isla de Pascua, Tres Zapotes, Göbekli Tepe)
- [x] NPCs interactivos con diálogos
- [x] Sistema de misiones e inventario
- [x] Sistema Solar 3D con órbitas keplerianas en tiempo real
- [x] 83,148 estrellas (148 catálogo Yale + procedurales)
- [x] Deploy automático en GitHub Pages

### v1.1 — Mobile + Herramientas
- [x] Brújula magnética (DeviceOrientationEvent)
- [x] Sistema de ayuda contextual (ProximityHelpDetector)
- [x] World Resonance — frecuencias simbólicas por sitio
- [x] Arte generativo orbital (curvas de Lissajous)
- [x] PWA instalable (manifest + service worker)
- [x] Compresión GLB (Draco) — -96% en modelos pesados

### v1.2 — Pulido + Features Astronómicas
- [x] Carta astrológica completa (10 planetas, aspectos, nodos lunares)
- [x] Calendarios: Tzolk'in GMT, Cholq'ij k'iche', Babilónico sexagesimal
- [x] Vista "Hoy" — resumen diario astronómico completo
- [x] Clima local (Open-Meteo, pronóstico 6 días, condiciones de observación)
- [x] Cinemática final épica (Göbekli Tepe)
- [x] Harmonia Mundi — audio perceptible con frecuencias audibles
- [x] Anillos de Saturno realistas (División de Cassini)
- [x] Fix bug cámara atrapada en Saturno
- [x] Fix bug volumen de audio (musicVolume vs masterVolume)
- [x] Toasts de descubrimiento no intrusivos

---

## 🔄 En progreso

### v1.3 — Mejoras de contenido
- [ ] **Nuevas constelaciones** — completar el catálogo a 88 constelaciones IAU
- [ ] **Clima: mapa visual** — mapa regional con iconos meteorológicos
- [ ] **Calendario lunar detallado** — calendario mensual con todas las fases
- [ ] **Screenshots PWA** — imágenes para prompt de instalación mejorado en Chrome
- [ ] **Icono maskable** — dedicado para launchers Android (padding 20%)

---

## 📋 Planificado

### v1.4 — Plataforma móvil nativa
- [ ] **TWA (Trusted Web Activity)** — empaquetado para Google Play Store
- [ ] **Notificaciones push** — alertas de eventos astronómicos (eclipses, lluvias de meteoros, planetas en conjunción)
- [ ] **Widget de fase lunar** — para pantalla de inicio Android
- [ ] **Modo offline completo** — caché de todos los cálculos astronómicos

### v1.5 — Nuevos sitios arqueológicos
- [ ] **Stonehenge** (Reino Unido) — alineaciones solares del solsticio
- [ ] **Machu Picchu** (Perú) — intihuatana, ventanas solares
- [ ] **Angkor Wat** (Camboya) — orientación estelar, calendario khmer
- [ ] **Nabta Playa** (Egipto) — calendario más antiguo del mundo (~7,000 a.C.)

### v1.6 — IA y datos
- [ ] **Asistente astronómico** — chatbot con datos en tiempo real (usando módulos documentados)
- [ ] **Endpoint API público** — `/api/sky-now`, `/api/calendars`, `/api/astrology` para IA externa
- [ ] **Interpretaciones IA** — generación dinámica de interpretaciones astrológicas
- [ ] **Arqueología generativa** — procedural lore por sitio basado en datos reales

### v2.0 — Comunidad
- [ ] **Modo multijugador cooperativo** — exploración simultánea (WebSocket / Liveblocks / Partykit)
- [ ] **Editor de misiones** — crear y compartir misiones personalizadas
- [ ] **Galería de arte orbital** — exportar y compartir los mandalas generativos
- [ ] **Perfil de usuario** — historial de exploraciones, logros, reliquias

---

## 💡 Ideas en evaluación

| Idea | Estado | Notas |
|------|--------|-------|
| VR con WebXR | 🤔 Evaluando | Requiere refactor de controles |
| Modo educativo con cuestionarios | 🤔 Evaluando | Útil para escuelas |
| Sonificación de datos astronómicos | 🤔 Evaluando | Extensión natural de Harmonia Mundi |
| Integración con telescopios reales (SLOOH API) | 🤔 Evaluando | Requiere suscripción |
| Realidad aumentada (AR) para constelaciones | 🤔 Evaluando | WebXR AR mode |
| Mapa de energía ley lines interactivo | 🤔 Evaluando | Tema sensible, enfoque histórico |

---

## 🐛 Bugs conocidos / deuda técnica

| Issue | Prioridad | Notas |
|-------|-----------|-------|
| Screenshots PWA faltantes | Alta | Chrome las necesita para prompt enriquecido |
| SW hardcodeado `/ArcheoScope/sw.js` en layout.tsx | Media | No registra en localhost |
| `theme-color` solo en manifest, no en `<head>` | Baja | Safari iOS |
| Icono maskable usa mismo PNG que `any` | Baja | Puede recortarse en launchers |

---

## 📊 Métricas de desarrollo

| Versión | Fecha | Features principales |
|---------|-------|---------------------|
| v1.0 | Ene 2026 | Base 3D + 6 sitios + Sistema Solar |
| v1.1 | May 2026 | Mobile + Brújula + Ayuda contextual |
| v1.2 | Jun 2026 | Astrología + Calendarios + Audio + Saturno |
| v1.3 | Q3 2026 | Contenido + PWA completa |
| v1.4 | Q4 2026 | Android nativo + Notificaciones |
| v1.5 | Q1 2027 | Nuevos sitios arqueológicos |
| v2.0 | 2027 | Multijugador + Comunidad |

---

*Última actualización: Junio 2026 · [Ver CHANGELOG](CHANGELOG.md)*
