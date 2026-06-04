# Changelog

All notable changes to Archeoscope: The Forgotten Relics will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.3] - 2026-06-04

### Fixed — Brújula mobile (memory leak de event listeners)
- **Bug crítico**: los listeners `deviceorientationabsolute` y `deviceorientation` no se removían al navegar fuera de la página — quedaban vivos en memoria durante toda la sesión
- **Fix**: agregado `handlerRef` para guardar referencia al handler activo; el `useEffect` cleanup ahora remueve correctamente ambos listeners al desmontar el componente
- **Refactor**: extraída función `attachListeners()` separada de `startCompass()` para que el cleanup funcione tanto en Android (auto-inicio) como en iOS (inicio manual por botón)
- Comportamiento funcional sin cambios: iOS pide permiso, Android inicia automático, suavizado exponencial, wrap-around 359°→0°, precisión del sensor

## [1.2.2] - 2026-05-31

### Fixed — Veracidad de datos (auditoría de integridad)
- **Conteo de estrellas Yale corregido**: la info decía "~250" en una sección y "~130" en otra; el número real es **148 estrellas** en `bright-stars.ts`. Corregido en `bright-stars.ts`, `Stars.tsx` e Información
- **Total de estrellas corregido**: 83,130 → **83,148** (80,000 procedurales + 3,000 brillantes + 148 reales del catálogo Yale)
- Auditoría completa confirmó que el resto de claims son verídicos: 27 constelaciones ✓, Rayleigh scattering real (Sky shader) ✓, Geometría Sagrada (6 generadores Lissajous/Hilbert/etc.) ✓, Arte Generativo Orbital (curvas de Lissajous con posiciones planetarias reales) ✓, Panel Científico (azimut/elevación/declinación con SolarEngine) ✓, Alineaciones Solares (fórmula cos(Az)=sin(δ)/cos(φ)) ✓

### Added — Toasts de descubrimiento (minimalistas, no intrusivos)
- **`discoveryToasts.ts`** + **`DiscoveryToast.tsx`**: mensajes contextuales breves que aparecen UNA sola vez por vida del juego cuando el jugador experimenta un sistema:
  - 🎨 Al entrar al globo: "El sistema dibuja arte único con las posiciones reales de los planetas"
  - 🌍 Al entrar a un sitio: "Cada lugar tiene una frecuencia que lo hace sentir distinto"
  - 🎵 Al completar misión: "Una nueva capa de la música cósmica despertó"
  - ✦ En constelaciones: "El cielo que ves es real: cada estrella está en su posición exacta"
- **UX responsable**: respetan el toggle de Ayuda (OFF = no aparecen), cooldown de 30s entre toasts, localStorage permanente (no se repiten), texto inmersivo no técnico, auto-dismiss a 7s, tocables para cerrar
- Se resetean al iniciar nueva partida

## [1.2.1] - 2026-05-31

### Changed
- **Pantalla principal**: eliminado botón "Entrar" — toda la pantalla (imagen) es ahora clickeable/tocable. Indicador sutil pulsante "toca / click para continuar" en la parte inferior. El logo tiene cursor `pointer` y feedback de opacidad al hacer click

### Added — Tips contextuales de arquitectura (ayuda in-game)
- **6 tips específicos** para estructuras megalíticas por sitio, visibles al acercarse con la ayuda encendida:
  - 🔺 Gran Pirámide de Giza: 144k bloques, alineación 0.05° al norte, solsticio 62.5° NE
  - 🏛️ Pirámide del Sol (Teo): base 220×220m, orientada al 13 de agosto, resonancia 104 Hz
  - 🧱 Puma Punku: tolerancias de 0.5mm, ensambles en H únicos, resonancia 432 Hz
  - 🗿 Pilares de Göbekli Tepe: 12,000 años, registro astronómico de 10,900 a.C., 45 Hz
  - 🗿 Moáis de Rapa Nui: 900 estatuas, "caminaban" con cuerdas, resonancia oceánica 63 Hz
  - 🗿 Cabeza Colosal Olmeca (Tres Zapotes): retratos de gobernantes, 6-50 ton, geometría estelar
- **Tips genéricos reemplazados**: las zonas `monument` ahora usan el tip específico del sitio
- Göbekli Tepe: el monolito ahora usa `gobekliMonolith` (datos arqueológicos reales)

## [1.2.0] - 2026-05-31

### Fixed
- **Coordenadas — Cuerpos Celestes**: la sección 🪐 (Sol, Mercurio, Venus, etc.) ahora solo aparece en modo globo/espacio. En escenas terrestres (misiones, sitios arqueológicos) el panel muestra únicamente los sitios arqueológicos. Al volver al globo, los cuerpos celestes vuelven a aparecer automáticamente

## [1.1.9] - 2026-05-31

### Added — World Resonance (capa de resonancia subconsciente)
- **`WorldResonanceSystem.ts`**: nueva capa de audio única y sutil (5-7% de volumen) que aporta una "firma sonora" simbólica por escena/sitio. Diseñada para sentirse, no escucharse — "no sé por qué, pero este lugar se siente diferente"
- **Frecuencias simbólicas por escena**:
  - Exploración (globo): 72 Hz (9×8, atención tranquila)
  - Descubrimiento (sitio sin identificar): 108 Hz (tradición hindú/budista/astronómica)
  - Giza: 111 Hz (monumentalidad) · Teotihuacán: 104 Hz (aérea) · Isla de Pascua: 63 Hz (oceánica) · Puma Punku: 432 Hz (identidad existente, ganancia muy baja) · Veracruz: 55 Hz (subterránea) · Göbekli Tepe: 45 Hz (integrada con Khepri)
- **Oscilador sine + sub-octava** con lowpass suave — el sub-grave da "cuerpo" que se siente físicamente
- **Resonancia temporal**: la frecuencia varía imperceptiblemente con la hora del día (noche -5%, mediodía base) — transición de 20s, el mundo "respira"
- **Transición suave de 4s** al cambiar de sitio — la frecuencia hace glissando entre escenas
- **Información**: sección 🌍 World Resonance agregada al menú de Información (visible en mobile y PC)
- Sincronizado con el volumen master del juego, se libera (`dispose`) al iniciar nueva partida

### Fixed — Ayuda contextual (ProximityHelpDetector)
- **Bug crítico de distancia**: el detector usaba `distanceTo` 3D — cuando el avatar vuela a Y=10 y las zonas están en Y=0, la distancia era siempre ≥10 y nunca activaba zonas con radio <10. **Fix**: ahora usa distancia XZ únicamente (ignora altura), igual que el Oracle scan del juego
- **Puma Punku**: radios de bloques aumentados de 7→10 y estructura de 18→22 para compensar
- **Árboles del entorno**: reemplazadas 8 posiciones hardcodeadas por 16 zonas en anillo interior+exterior (radio 18 c/u) que cubren el área real donde `EnvironmentElements` genera los árboles proceduralmente

### Nota de diseño
Se eligió una ÚNICA capa derivada de la frecuencia del sitio actual en lugar de múltiples frecuencias permanentes — más limpio, más ligero (1 oscilador) y no satura el mix de HarmoniaMundi. Ganancias ajustadas por frecuencia: las graves (45-72 Hz) se sienten, las agudas (108-432 Hz) se atenúan más para que no se escuchen conscientemente.

## [1.1.8] - 2026-05-31

### Fixed — Ayuda contextual ahora reconoce estructuras, bloques y árboles en sitios
- **Detección de sitio por coordenadas**: antes `helpZones` dependía solo de `selectedSite?.id`, que es `null` al navegar por coordenadas → en ese caso no se creaba ninguna zona. Ahora hay fallback que detecta el sitio por `selectedLocation` (lat/lon) igual que el resto del juego
- **Puma Punku**: agregadas zonas para la estructura megalítica (`[8,0,-8]`), los 9 bloques tallados dispersos (rocas, posiciones reales de `extraBlocks`), la Puerta del Sol (`[70,8,60]`) y el geoglifo del Cóndor
- **Estructuras megalíticas / monumentos**: agregadas zonas amplias para la Gran Pirámide (Giza r60), Moai (Isla de Pascua r40), Pirámide de Teotihuacán (r40)
- **Árboles del entorno**: 8 zonas en anillo exterior (radio 9) presentes en todos los sitios — reconoce los árboles de `EnvironmentElements`
- **Nuevos tips**: `megalith` (estructura), `ppBlock` (bloque Puma Punku), `sunGate` (Puerta del Sol)
- **Calendario Maya (Teo)**: corregida posición de zona de `[0,0,-20]` a `[0,10,-20]` (estaba elevado)

## [1.1.7] - 2026-05-31

### Added
- **Toast orientativo de zoom**: al viajar a un cuerpo celeste, aparece un mensaje flotante 5s — "🪐 Viajando a [Planeta] · usá la rueda del mouse para acercar/alejar 🔍". Animación de entrada suave, fondo blur, se auto-oculta

### Fixed — Tipografía responsive en todos los diálogos de NPCs
- **Patrón unificado**: todos los diálogos interactivos ahora usan `clamp()` para tipografía responsive (antes tenían font-sizes hardcodeados que se veían gigantes y desbordaban en mobile)
- **ViracochaInteractiveDialogue**: nombre 22px → `clamp(18px, 5vw, 22px)`, mensaje 18px → `clamp(14px, 3.5vw, 18px)`, opciones y botón con clamp + `maxHeight: 85vh` + scroll
- **OlmecInteractiveDialogue**: mismo tratamiento + agregado título "Olmeca" que faltaba
- **QuetzalcoatlDialogue**: nombre 28px → `clamp(20px, 6vw, 28px)`, mensaje 20px → `clamp(14px, 3.8vw, 20px)` + agregado nombre "Quetzalcóatl" que faltaba
- **SphinxInteractiveDialogue**: mensaje 24px → `clamp(15px, 4vw, 24px)`, opciones 18px → `clamp(13px, 3.5vw, 18px)`
- **VeracruzScene/OlmecDialogue**: nombre 26px → `clamp(18px, 5.5vw, 26px)`, mensaje 20px → `clamp(14px, 3.8vw, 20px)` + agregado título "Olmeca"
- **Touch targets**: todos los botones "Cerrar" ahora tienen `min-height: 44px` (WCAG)
- **Padding del contenedor**: `30px 40px` fijo → `clamp(18px, 5vw, 36px)` para mejor uso del espacio en mobile

## [1.1.6] - 2026-05-31

### Changed — Menú in-game unificado
- **InGameMenu (tecla M)**: ahora tiene las mismas opciones generales que el menú principal PC — Nueva, Audio, Video, Controles, Constelaciones, Calendarios, **Ayuda ON/OFF**, Información. Antes solo tenía 4 opciones y faltaba el toggle de Ayuda
- **Ayuda ON/OFF en escenas terrestres**: ahora accesible desde el menú M dentro de Giza, Teo, Puma Punku, etc. — mismo patrón verde/gris que el menú principal, sincronizado vía evento `help-toggle`

### Fixed — Enfoque de cuerpos celestes (posición real)
- **Navegación a planetas**: antes usaba posiciones de cámara hardcodeadas que no coincidían con la posición orbital real del planeta (los planetas orbitan en tiempo real) → la nave/cámara quedaba en el vacío
- **Ahora**: lee la posición REAL del planeta desde su ref (actualizada cada frame), calcula una posición de cámara frente al cuerpo (distancia = radio × 4, lado opuesto al sol, ligeramente elevada) y anima la cámara + el target del OrbitControls con `lerp`
- **CelestialFocusController**: ahora actualiza el `target` del OrbitControls (antes solo movía la cámara, que OrbitControls revertía al instante)
- **OrbitControls del globo**: agregado `ref` + `enableDamping` para transiciones suaves

## [1.1.5] - 2026-05-31

### Fixed — Diálogos de NPCs: eliminado auto-close, patrón UX unificado
- **AkhenatonDialogue**: eliminado `setTimeout(() => onClose(), 8000)` al elegir opción — el usuario cierra cuando quiera
- **OlmecInteractiveDialogue**: eliminados 3 `setTimeout(() => onClose(), 5000/6000)` — saludo inicial, respuestas y entrega de jade. El timer de 3s para entrar a la cueva se mantiene (es funcional, no cierra el diálogo)
- **ViracochaInteractiveDialogue**: eliminados `setTimeout(() => onClose(), 5000/6000)` en opciones y el auto-close de 6s del mensaje de agradecimiento
- **QuetzalcoatlDialogue**: eliminados 3 `setTimeout(() => onClose(), 4000/5000/6000)` en los tres estados del diálogo (pedir semilla, tiene semilla, maíz plantado)
- **VeracruzScene — OlmecDialogue**: eliminado `setTimeout(onClose, 6000)`
- **Patrón unificado**: todos los diálogos interactivos ahora tienen solo un botón "Cerrar" visible. El usuario lee a su tiempo y cierra cuando quiere
- **Nota**: `SphinxDialogue` y `ViracochaDialogue` son notificaciones flotantes de sistema (no interactivas) — mantienen su comportamiento auto-dismiss por diseño

## [1.1.4] - 2026-05-31

### Added
- **Botón Coordenadas — rediseño reactivo**: color cambia según estado del juego (verde=todas misiones, dorado=progreso, rojo=tormenta, azul=default). Pulso animado cada 4s en modo globo. Ícono 🧭 + contador de misiones completadas. Glow dinámico
- **Cuerpos Celestes en panel de navegación**: nueva sección "🪐 CUERPOS CELESTES" con Sol, Mercurio, Venus, Tierra, Luna, Marte, Júpiter, Saturno, Urano, Neptuno y Plutón. Al hacer click, la cámara del Sistema Solar se anima suavemente hacia una posición cercana al cuerpo celeste seleccionado
- **CelestialFocusController**: componente Three.js dentro del Canvas que interpola la cámara con `lerp` hacia el planeta objetivo usando `useFrame`
- **Sitios arqueológicos con nombre**: los sitios ahora muestran nombre + emoji (Puma Punku, Giza, Teotihuacán, etc.) en lugar de solo coordenadas. Agregado Göbekli Tepe

## [1.1.3] - 2026-05-31

### Performance — Compresión masiva de modelos GLB (Draco + WebP)
- **calendario_maya.glb**: 49.9 MB → 1.79 MB (-96.4%)
- **quetzalcoatl.glb**: 30.6 MB → 1.13 MB (-96.3%)
- **mictlantecuhtli.glb**: 42.1 MB → 1.41 MB (-96.7%)
- **atlante.glb**: 33.4 MB → 1.00 MB (-97.0%)
- **akenaton.glb**: 13.6 MB → 0.80 MB (-94.1%)
- **ramses2.glb**: 12.1 MB → 0.67 MB (-94.5%)
- **hatshepsut.glb**: 11.8 MB → 0.50 MB (-95.8%)
- **lanzon_chavin.glb**: 11.2 MB → 0.33 MB (-97.1%)
- **fuente_magna.glb**: 11.1 MB → 0.53 MB (-95.2%)
- **Total ahorrado**: ~215 MB → ~8 MB en los 9 modelos más pesados
- Herramienta: `@gltf-transform/cli optimize --compress draco --texture-compress webp`

### Fixed
- **Flash PC→Mobile en menú**: `isMobile` ahora inicializa como `null` (no `false`). El menú se oculta hasta que la detección del dispositivo se completa en el cliente, eliminando el flash del layout PC que aparecía por un instante en mobile
- **Flash en landing (Entrar)**: mismo fix aplicado a `app/page.tsx` — el botón Entrar se oculta hasta detectar el dispositivo
- **Tipografía — Design System**: Inter como fuente UI (body, labels, descripciones) + Spaceport para brand headings. `globals.css` reescrito con sistema de spacing 8px, WCAG AA, touch targets 56px, `clamp()` responsive, `:focus-visible`, utilidades de spacing
- **Botón "FINALIZAR TUTORIAL"**: `font-weight: normal` (Spaceport no tiene variante bold — faux bold distorsionaba los glifos). Ahora coincide visualmente con el h1 "TRAINING ROOM"

## [1.1.2] - 2026-05-31

### Added
- **AGENTS.md**: guía completa para agentes de IA — convenciones, reglas absolutas, skills obligatorias, estructura del proyecto, flujo de trabajo, errores conocidos, posiciones NPC, sistema de audio, estado persistente, checklist pre-commit
- **Sistema de Ayuda Contextual** — botón `?` flotante que aparece al acercarse a objetos en Training Room y escenas terrestres
  - `helpTips.json` — 30+ tips para rocas, árboles, portales, NPCs (Esfinge, Viracocha, Quetzalcóatl, Atlante, etc.), geoglifos, ítems coleccionables, monumentos, agua, cuevas
  - `helpSystem.ts` — toggle global en `localStorage` con evento `help-toggle` para sincronización reactiva
  - `ProximityHelpDetector.tsx` — componente Three.js (dentro del Canvas) que detecta la zona más cercana cada 10 frames usando `distanceTo()`
  - `HelpBubble.tsx` — botón `?` animado (pulse dorado) + diálogo desplegable con ícono, título y tip. Se cierra solo al alejarse del objeto
  - **Training Room**: zonas de ayuda para cada roca y árbol con radio 10-12 unidades
  - **ImmersiveScene**: zonas por sitio (Giza, Puma Punku, Isla de Pascua, Teotihuacán, Tres Zapotes, Göbekli Tepe) con posiciones exactas de NPCs
  - **Menú PC**: opción "Ayuda ON/OFF" — verde cuando activa, gris cuando desactivada. Persiste en `localStorage`

## [1.1.1] - 2026-05-07

### Added
- **Brújula** (`/menu/brujula`): nueva sección mobile con orientación magnética en tiempo real. Disco giratorio estilo vintage con marcas de grados, letras cardinales, aguja roja/blanca fija, heading numérico grande, indicador de dirección con color dinámico por punto cardinal. Usa `DeviceOrientationEvent` + `webkitCompassHeading` (iOS) / `alpha` (Android). Suavizado exponencial α=0.15 para evitar jitter. Muestra precisión del sensor (±°) cuando está disponible. Tip de calibración en "8". Permiso explícito en iOS via `requestPermission()`
- **Menú mobile**: agregada opción 🧭 Brújula entre Clima e Información
- **Información**: sección 🧭 Brújula agregada al listado de features técnicas

## [1.1.0] - 2026-05-04

### Fixed — Mobile responsive audit (frontend-design skill)
- **Menú mobile**: font-sizes hardcodeados → `clamp()` en label (17/20px → clamp(15/18px, 4vw)) y subtitle (12px → clamp(12px, 2.8vw, 14px))
- **Tzolk'in Clásico**: grid `minmax(180px)` causaba overflow horizontal en 320px → `minmax(min(180px, 100%), 1fr)`. Mismo fix en grid de ciclos astronómicos mayas
- **Tzolk'in Clásico**: múltiples font-sizes hardcodeados (14px labels, 32px/28px números, 16px/18px textos) → todos con `clamp()`
- **Tzolk'in Clásico**: ciclos cósmicos (Venus/Luna/Eclipses) tenían 13px/12px hardcodeados → `clamp(13-14px, 3vw, 16-17px)`
- **Calendario Babilónico**: grid `minmax(180px)` y `minmax(150px)` → `minmax(min(180/150px, 100%), 1fr)`. Grid de tiempo fijo `minmax(130px)` → `repeat(3, 1fr)` (siempre 3 columnas)
- **Calendario Babilónico**: font-sizes hardcodeados (14px labels, 28px números, 15px/16px textos) → todos con `clamp()`
- **Cholq'ij**: grid `repeat(2, 1fr)` → `repeat(auto-fit, minmax(min(140px, 100%), 1fr))` para colapsar en pantallas muy pequeñas
- **Cholq'ij**: font-sizes hardcodeados (13px labels, 28px números, 16px/20px textos) → todos con `clamp()`

### Added
- **Calendario Babilónico**: barra de progreso del ciclo actual (día X de 60, días para el siguiente ciclo)
- **Calendario Babilónico**: mapa visual de los 6 ciclos del año con el ciclo actual resaltado

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
- **Información mobile**: secciones exclusivas del juego PC ocultas en mobile (Requerimientos Mínimos, Arte Generativo, Harmonia Mundi, Sistema 3D, Calidad Gráfica, Cielo Atmosférico). Secciones 🔷 Geometría Sagrada, 🔭 Panel Científico y ☀️ Alineaciones Solares reescritas sin referencias al juego — describen los sistemas técnicos de forma neutral
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
