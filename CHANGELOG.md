# Changelog

All notable changes to Archeoscope: The Forgotten Relics will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.9] - 2026-05-04

### Fixed
- **Astrología — actualización diaria**: eliminado `moonPhase` useMemo que era código muerto (se calculaba pero nunca se renderizaba). La sección FASE LUNAR ya usaba `getLunarPreciseDataAstro()` con astronomy-engine
- **Astrología — rendimiento**: `getLunarPreciseDataAstro()` se llamaba 3 veces en el JSX en cada render; ahora memoizado como `lunarData` con `useMemo([selectedDate])`
- **Astrología — rendimiento**: `generateInterpretation()` se llamaba sin memoizar; ahora memoizado como `interpretation`
- **Astrología — Fase Lunar**: próxima Luna Nueva y Luna Llena ahora calculadas con `Astronomy.SearchMoonPhase()` (astronomy-engine, precisión ~1 min) en lugar de cálculo manual aproximado. Incluye signo zodiacal donde cae cada luna
- **Calendarios/Hoy**: `const today = new Date()` estaba fuera de `useState` con `useMemo([])` — los datos nunca se recalculaban si el componente se remontaba. Corregido con `useState(() => new Date())` y `useMemo([today])`
- **Calendario Babilónico**: hora babilónica (Beru/Uš/Ninda) usaba `new Date()` dentro de `calcSexagesimal()` — se congelaba en el primer render. Separada en `useState` + `useEffect` con `setInterval(1000)` para actualización en tiempo real
- **Clima Local (Weather)**: `getLunarPreciseData()` se llamaba 3 veces en el JSX en cada render (condiciones de observación + moon card + getMoonPhase). Ahora memoizado como `lunarData` y `moon` con `useMemo([])`
- **Build**: import `useState` faltante en `calendarios/today/page.tsx` — causaba error de compilación en CI

## [1.0.8] - 2026-05-04

### Changed
- **Fuente global**: reemplazada Archeoscope-Regular.ttf por Spaceport_2006.otf como fuente principal del proyecto (prueba visual)

### Fixed
- **Build CI**: raíz del problema — `package-lock.json` estaba en `.gitignore`, por lo que `npm install` en CI resolvía versiones libremente e instalaba Next.js 16 (Turbopack). Fix: removido `package-lock.json` del `.gitignore`, generado lockfile con Next.js `14.2.35` exacto, CI usa `npm ci`. También corregido `.gitignore` que tenía `*.js` ignorando todos los JS incluyendo `next.config.js`

## [1.0.7] - 2026-05-04

### Added
- **Astrología — Fase Lunar**: cálculo correcto de iluminación (0% nueva → 100% llena → 0% menguante), antes mostraba porcentaje de fase en vez de iluminación
- **Astrología — Fase Lunar**: próxima Luna Nueva y Luna Llena con fecha y días restantes
- **Astrología — Fase Lunar**: signo zodiacal donde cae la Luna con interpretación astrológica completa

### Fixed
- **Calendarios mobile**: tipografía de textos descriptivos aumentada 2-3 puntos en Cholq'ij, Tzolk'in Clásico y Tzolk'in simple — mejora legibilidad en dispositivos móviles
- **globals.css**: `.text-responsive` base aumentada de 14px a 16px

## [1.0.6] - 2026-05-03

### Added
- **Astrología**: card "🌕✨🌕 Doble Luna Llena" — detecta dinámicamente cuando hay dos lunas llenas en el mismo mes (Luna Rosa + Luna Azul). Muestra fechas exactas, signos, mensaje interpretativo especial y datos curiosos del fenómeno. Para mayo 2026: Luna Rosa en Escorpio (1 mayo) + Luna Azul en Sagitario (31 mayo)

### Fixed
- **Botón "Entrar" mobile** (pantalla de inicio): centrado en la parte inferior, ancho `min(320px, 80vw)`, padding 18px, border-radius 14px, touch feedback `onTouchStart/End`, `backdropFilter blur(8px)`. PC sin cambios
- **Botones "Volver" mobile**: mejor UX — padding aumentado (16px), ancho máximo 340px, min-height 54px (mejor touch target), border-radius 12px, feedback táctil `:active` con scale(0.97), `-webkit-tap-highlight-color: transparent`

## [1.0.5] - 2026-05-02

### Added
- **Menú mobile**: rediseño con propósito — "Hoy" como botón principal verde destacado, cada opción con subtítulo descriptivo, logo más pequeño, touch feedback

### Changed
- **Menú mobile**: "Hoy" accesible directamente desde el menú (antes requería Calendarios → Hoy)
- **Menú mobile**: botones con emoji + título + subtítulo en lugar de solo texto uppercase

## [1.0.4] - 2026-05-02

### Added
- **Calendarios/Hoy**: "Tonight Sky" — condiciones de observación nocturna, planetas visibles con signo/grado, calidad basada en fase lunar + clima
- **Astrología**: "Energía del Día" — resumen rápido arriba de la rueda (elemento dominante, clima armónico/tenso, luna, clave del día, retrogradaciones)
- **Clima Local**: "Condiciones de Observación" — conecta clima + fase lunar → calidad astronómica (🟢🟡🟠🔴)

### Changed
- **Menú mobile**: eliminado "3D Solar System" (menú queda con 6 opciones limpias)

## [1.0.3] - 2026-05-02

### Added
- **Eclipses dinámicos**: módulo `eclipse-calculator.ts` con `astronomy-engine` — busca eclipses solares y lunares dinámicamente para cualquier año (reemplaza lista estática 2026)
- **Códice de Dresde**: datos de la tabla de eclipses maya (páginas 51-58), ciclos de 177/148 días, eclipses históricos verificados, detección de "ventana de peligro" maya
- **Página Hoy**: sección de próximos eclipses con countdown + ventana de eclipse del Códice de Dresde
- **Página Hoy**: eventos astronómicos por día del año (funciona cualquier año, no solo 2026)

### Changed
- **Página Hoy**: reemplazada lista estática `ASTRO_EVENTS_2026` por cálculos dinámicos

## [1.0.2] - 2026-05-02

### Added
- **Calendarios**: nueva página "Hoy" — vista integrada diaria con fase lunar, Sol en signo, Cholq'ij/Tzolk'in, estación solar con barra de progreso, y próximos eventos astronómicos (eclipses, lluvias de meteoros, solsticios/equinoccios 2026)
- **Calendarios**: card "Hoy" en la página principal de calendarios
- **Astrología**: sección "Luna y Agricultura" — recomendaciones agrícolas dinámicas según fase lunar (siembra, cosecha, poda, trasplante)
- **Astrología**: sección solo disponible en mobile (removida del menú PC)

### Changed
- **Calendarios**: título actualizado de "Calendarios Antiguos" a "Calendarios" (incluye sistemas modernos)

## [1.0.1] - 2026-05-01

### Added
- **Astrología**: Fase lunar precisa con grado exacto en signo, barra de intensidad lunar, peak energético con timestamp exacto, ventana activa en signo, días restantes
- **Clima Local**: Moon card reemplazada con datos precisos de astronomy-engine — fase + signo + grado + intensidad + peak energético + ventana activa
- **Clima Local**: Pronóstico 6 días (temperatura máx/mín + probabilidad de lluvia)
- **Clima Local**: Animaciones CSS adaptativas día/noche (estrellas + luna de noche, sol cálido de día)
- **Clima Local**: Amanecer/atardecer con duración del día
- **Astrología**: Elementos predominantes del día con barra visual y consejo
- **Astrología**: Nodos lunares (Norte/Sur) con signo, grado e interpretación
- **Astrología**: Velocidad instantánea dλ/dt y detección de planetas estacionarios

### Fixed
- **Clima Local**: Fase lunar mostraba "Gibosa Creciente" en lugar de "Luna Llena en Escorpio" — reemplazado algoritmo simplificado por astronomy-engine
- **Clima Local**: Cache invalidado automáticamente cuando faltan campos nuevos
- **Clima Local**: Detección día/noche mejorada (fallback 20:00-06:00, validación de sunrise/sunset)

## [1.0.0] - 2026-05-01

### 🌌 Escenas 3D
- **Sistema Solar 3D** — 9 planetas con texturas reales, órbitas astronómicas, asteroides, anillos de Saturno
- **Constelaciones** — 27 constelaciones con líneas y nombres, 83,130 estrellas en 3 capas, Vía Láctea procedimental, luna billboard con textura, terreno desierto con vegetación
- **Escenas terrestres** — 7 sitios arqueológicos (Puma Punku, Giza, Teotihuacán, Isla de Pascua, Veracruz, Göbekli Tepe, Mictlán)
- **Sistema climático** — lluvia, nieve, viento, rayos, tormentas, terremotos, erupciones volcánicas

### 🔭 Astronomía y Astrología
- **Motor astronómico** — astronomy-engine (VSOP87/ELP, precisión ~1 arcmin)
- **Rueda astrológica SVG** — 12 signos, 10 planetas, aspectos ptolemaicos, casas
- **Velocidad instantánea dλ/dt** — detección de planetas estacionarios y retrogradaciones (Δt=1h)
- **Elementos predominantes** — balance Fuego/Tierra/Aire/Agua con interpretación diaria
- **Nodos lunares** — Nodo Norte/Sur con signo, grado e interpretación del alma
- **Lectura astrológica dinámica** — interpretación profesional generada por fecha
- **Notas metodológicas** — fuentes citadas (Ptolomeo, Greene, Arroyo, JPL/NASA)

### 📅 Calendarios
- **Cholq'ij** — calendario sagrado maya (13 números × 20 nawales), información espiritual, tabla comparativa con Tzolk'in clásico
- **Tzolk'in Clásico** — correlación GMT 584283, Cuenta Larga + Haab
- **Calendario Babilónico** — sistema sexagesimal base 60, coordenadas celestes RA/Dec

### 🌤️ Clima Local
- **Open-Meteo API** — temperatura, humedad, viento, probabilidad de lluvia
- **Fase lunar precisa** — astronomy-engine con signo zodiacal (ej: "Luna Llena en Escorpio")
- **Amanecer/Atardecer** — hora local exacta + duración del día
- **Animaciones CSS** — día soleado, noche estrellada, lluvia, nieve, tormenta, niebla (adaptativas día/noche)
- **Geocoding** — ciudad y país via OpenStreetMap Nominatim
- **Cache 30 minutos** — localStorage para reducir llamadas API

### 📱 Mobile
- **Menú demo** — Controles, Constelaciones, Astrología, Calendarios, Clima Local, Información, 3D Solar System
- **Touch D-pad** — movimiento WASD + rotación Q/R para escenas terrestres
- **Landscape lock** — orientación horizontal forzada con fallback portrait overlay
- **Optimizaciones GPU** — pixelRatio 1.2, sin bloom/vignette, partículas reducidas 50%, terreno 48×48, frame skip
- **MOBILE_STORM_WEATHER** — tormenta reducida sin rayos para evitar crash de memoria en Edge

### 🎮 Juego (PC)
- **5 naves UFO** — cada una con habilidad especial (cloaking, campo EM, teletransporte, escáner, fuerza bruta)
- **Sistema de misiones** — 5 sitios principales con NPCs, diálogos interactivos, items coleccionables
- **Inventario** — items recolectables con drag & drop
- **HarmoniaMundi** — música cósmica procedural que se desbloquea con misiones
- **Audio procedural** — clima, viento, lluvia, truenos generados en tiempo real

### ⚖️ Licencia y PWA
- **CC BY-NC 4.0** — código fuente abierto para uso no comercial
- **All Rights Reserved** — assets protegidos (modelos, texturas, audio)
- **Service Worker** — soporte offline, cache de assets estáticos
- **Digital Asset Links** — preparado para Google Play Store via TWA

### 🛠️ Infraestructura
- Next.js 14 (App Router) + Three.js + React Three Fiber + TypeScript + Bun
- GitHub Pages deployment con basePath `/ArcheoScope`
- Yale Bright Star Catalogue (~130 estrellas reales con RA/Dec)
- Catálogo de 27 constelaciones IAU

---

Copyright (c) 2026 Ignacio Fernandez
