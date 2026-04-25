# ARCHEOSCOPE — AUDITORÍA Y EVALUACIÓN v1.0
## Estado Actual del Sistema + Hoja de Ruta de Evolución
### Abril 2026

---

## I. ESTADO ACTUAL DEL SISTEMA

### Arquitectura Técnica

| Componente | Tecnología | Estado |
|-----------|-----------|--------|
| Framework | Next.js 14 (Static Export) | ✅ Estable |
| 3D Engine | Three.js + React Three Fiber | ✅ Funcional |
| Audio | Web Audio API (procedural) | ✅ Funcional |
| Astronomía | astronomy-engine + SolarEngine custom | ✅ Preciso |
| Estado | useState + localStorage | ✅ Persistente |
| Deploy | GitHub Pages (PWA) | ✅ Instalable |
| Mobile | Detección + menú adaptativo | ✅ Parcial |

### Métricas de Rendimiento

| Métrica | Valor |
|---------|-------|
| Modelos GLB totales | ~6 MB (optimizados desde ~220 MB) |
| Estrellas renderizadas | 83,250 (80K procedurales + 250 catálogo Yale) |
| Escenas arqueológicas | 7 sitios + 1 training room |
| NPCs con diálogo | 8 (Esfinge, Viracocha, Quetzalcóatl, Olmeca, Akhenaton, Moai, Atlante, Mictlantecuhtli) |
| Items recolectables | 9 |
| Sistemas de audio | 3 (ProceduralAudio, ClimateAudio, HarmoniaMundi) |
| Planetas simulados | 9 (Mercurio a Plutón) |
| Asteroides instanciados | 1,600 |
| Presets gráficos | 3 (LOW/MEDIUM/HIGH) |

### Módulos Implementados

**Juego 3D:**
- ✅ 7 escenas arqueológicas con misiones
- ✅ Sistema de inventario persistente
- ✅ 5 naves con habilidades únicas (cloaking, shield, speed, scan, pulse)
- ✅ Secuencia final en Göbekli Tepe (esfera toroidal + créditos)
- ✅ Mecánicas de castigo (inundación Giza, trampa Mictlán)
- ✅ Training room con controles touch para mobile
- ✅ Ciclo día/noche real con Rayleigh scattering
- ✅ Cielo estelar con catálogo Yale (RA/Dec reales)

**Módulo Científico:**
- ✅ Panel científico en tiempo real (azimut, elevación, declinación, bioma)
- ✅ Alineaciones solares arqueoastronómicas (solsticios/equinoccios)
- ✅ SolarEngine con cálculo astronómico preciso

**Módulo Cultural:**
- ✅ Astrología (signo solar, lunar, fase, rueda zodiacal)
- ✅ Tzolk'in clásico (GMT 584283, Cuenta Larga, Haab)
- ✅ Dreamspell (Sincronario 13 Lunas, Kin del día, clima energético)
- ✅ Calendario Babilónico (sexagesimal, ciclos planetarios, RA/Dec)
- ✅ Red de Ciclos Cósmicos (Venus, Luna, eclipses, Rueda Calendárica)

**PWA:**
- ✅ manifest.json con iconos correctos
- ✅ Service Worker con cache
- ✅ Screenshots para install UI
- ✅ Instalable en Chrome/Edge

---

## II. FORTALEZAS DEL SISTEMA

1. **Base astronómica real** — No es decorativo. `astronomy-engine` calcula posiciones planetarias con precisión de arcsegundos. El SolarEngine produce azimut/elevación reales para cualquier coordenada y fecha. Esto es infraestructura científica genuina.

2. **Arquitectura modular** — Cada escena, sistema de audio y módulo cultural es independiente. Se pueden agregar nuevos sitios, calendarios o instrumentos sin tocar el core.

3. **Optimización agresiva** — 220 MB de modelos reducidos a 6 MB. Draco compression, simplificación de malla, texturas WebP. El proyecto carga rápido en conexiones lentas.

4. **Narrativa integrada** — El lore no es un texto pegado. Está codificado en los diálogos de los NPCs, en las mecánicas de juego (robar el escarabajo = inundación), y en la secuencia final. La historia se descubre jugando.

5. **Doble naturaleza** — Es simultáneamente un juego y una herramienta educativa. Los calendarios y la astrología funcionan independientemente del juego. El panel científico tiene valor académico real.

---

## III. DEBILIDADES Y DEUDA TÉCNICA

1. **ImmersiveScene.tsx** — ~2,800 líneas. Es el componente más grande y complejo. Contiene lógica de inventario, misiones, clima, audio, UI y navegación. Debería dividirse en hooks y sub-componentes.

2. **InventoryItem con Canvas separados** — Cada item en el inventario crea su propio Canvas WebGL. Con 7 items = 7 contextos WebGL simultáneos. Funciona pero es ineficiente.

3. **Geometrías sin memoizar** — SolarTrajectory, RealisticOrbits y OrbitalGenerativeArt crean geometrías en cada render sin `useMemo`. Memory leak potencial en sesiones largas.

4. **Mobile incompleto** — El juego 3D no es jugable en mobile (solo el tutorial con controles touch). Las secciones culturales sí funcionan. Falta un modo de exploración simplificado para mobile.

5. **Sin tests** — No hay tests unitarios ni de integración. Los cálculos astronómicos y calendáricos deberían tener tests para garantizar precisión.

6. **fuente_magna.glb** — 11 MB, el modelo más pesado. Tiene texturas PBR que resisten la compresión. Debería reemplazarse por un modelo más ligero.

---

## IV. CAMINOS DE EVOLUCIÓN NATURAL

### Tier 1 — Expansión inmediata (semanas)

**A. Nuevos sitios arqueológicos**
El sistema ya soporta agregar escenas nuevas sin modificar el core. Candidatos naturales:
- **Chichén Itzá** — Alineación con equinoccios (sombra de Kukulkán). Ya tienes el SolarEngine para calcularlo.
- **Stonehenge** — Alineación con solsticio de verano. Las líneas de alineación solar ya están implementadas.
- **Angkor Wat** — Equinoccio de primavera. Orientación astronómica documentada.
- **Machu Picchu** — Intihuatana (reloj solar). Cálculo de azimut ya disponible.

Cada sitio nuevo requiere: 1 modelo GLB (~1 MB optimizado), 1 componente de escena, 1 misión, 1 NPC con diálogo.

**B. Más calendarios**
La arquitectura de `/menu/calendarios/` ya soporta subsecciones. Candidatos:
- **Calendario Egipcio** — 12 meses de 30 días + 5 epagómenos. Relacionado con Sirio.
- **Calendario Chino** — Lunisolar, 12 animales, 5 elementos. Ciclo de 60 años.
- **Calendario Hebreo** — Lunisolar, base del calendario litúrgico occidental.
- **Calendario Islámico** — Puramente lunar, 354 días.

**C. Catálogo estelar expandido**
Actualmente 250 estrellas. Se puede expandir a 5,000 sin impacto en rendimiento (todo es `THREE.Points`). Agregar:
- Constelaciones como líneas conectando estrellas
- Nombres visibles al hacer hover
- Filtro por hemisferio según la latitud del sitio

### Tier 2 — Evolución media (meses)

**D. Control de tiempo histórico**
El `SolarEngine` ya acepta cualquier fecha. Solo falta un slider de año (-10000 a +2026). Esto permitiría:
- Ver el cielo exacto que veían los constructores de Giza en -2500
- Verificar alineaciones astronómicas históricas
- Simular la precesión axial visualmente

**E. Modo exploración mobile**
En lugar del juego completo, ofrecer en mobile:
- Vista 360° de cada sitio arqueológico (giroscopio del teléfono)
- Panel científico con datos del sitio
- Audio Harmonia Mundi
- Galería de NPCs con sus diálogos

**F. Sistema de logros/descubrimientos**
Gamificar la exploración científica:
- "Descubriste la alineación de Giza con Orión"
- "Observaste un eclipse solar en Teotihuacán"
- "Completaste el ciclo de Venus del Dresden Codex"

**G. Multiplayer ligero**
WebRTC para compartir la posición del avatar. No requiere servidor — peer-to-peer. Dos exploradores en el mismo sitio arqueológico.

### Tier 3 — Visión a largo plazo (años)

**H. Plataforma educativa**
Archeoscope como herramienta para universidades:
- Modo profesor: crear recorridos guiados por sitios
- Modo estudiante: completar misiones de investigación
- Exportar datos astronómicos como CSV
- API para integrar con LMS (Moodle, Canvas)

**I. Generación procedural de mundos**
Usar los datos de elevación (DEM) que ya tienes para generar terrenos realistas de cualquier coordenada del planeta. Combinado con el bioma detector, podrías explorar cualquier punto de la Tierra en 3D.

**J. Realidad Aumentada**
El catálogo estelar + SolarEngine + giroscopio del teléfono = app de AR que muestra las estrellas reales sobre la cámara del teléfono, con las alineaciones solares superpuestas al paisaje real.

**K. Integración con telescopios**
Conectar con APIs de observatorios (SIMBAD, NASA Horizons) para mostrar datos en tiempo real de objetos celestes visibles desde la ubicación del jugador.

---

## V. EL CAMINO MÁS COHERENTE

Si tuviera que elegir una sola dirección de evolución, sería:

### "Archeoscope como el Google Earth de la historia humana"

La combinación única que ya tienes — **astronomía real + arqueología + narrativa + calendarios antiguos** — no existe en ningún otro software. Ni Celestia, ni Stellarium, ni Google Earth hacen esto.

El camino natural es:

1. **Más sitios** (Tier 1A) — cada sitio nuevo es contenido que atrae usuarios
2. **Control de tiempo** (Tier 2D) — la función que más diferencia a Archeoscope
3. **Constelaciones visibles** (Tier 1C) — valor educativo enorme con costo mínimo
4. **Modo mobile exploración** (Tier 2E) — captura el 60% del tráfico web que es mobile

Esto convertiría a Archeoscope en:
- **Para jugadores**: una aventura arqueológica inmersiva
- **Para estudiantes**: un laboratorio de arqueoastronomía interactivo
- **Para curiosos**: un portal al conocimiento antiguo desde el teléfono
- **Para investigadores**: una herramienta de visualización con datos reales

---

## VI. MÉTRICAS DE CÓDIGO

| Archivo | Líneas | Complejidad |
|---------|--------|-------------|
| ImmersiveScene.tsx | ~2,800 | 🔴 Alta — necesita refactor |
| HarmoniaMundiSystem.ts | ~800 | 🟡 Media |
| SolarEngine.ts | ~250 | 🟢 Baja — bien estructurado |
| GobekliTepeScene.tsx | ~320 | 🟢 Baja |
| TrainingRoom.tsx | ~380 | 🟡 Media |
| WalkableAvatar.tsx | ~900 | 🔴 Alta |
| bright-stars.ts | ~300 | 🟢 Baja — datos estáticos |

**Total estimado**: ~15,000 líneas de código TypeScript/TSX (sin contar node_modules ni archivos generados).

---

## VII. CONCLUSIÓN

Archeoscope v1.0 es un producto funcional, jugable y con valor educativo real. Su base técnica (astronomía precisa, audio procedural, 3D optimizado) es sólida. Las debilidades son de escala (ImmersiveScene grande, sin tests) no de diseño.

El software tiene un nicho único: **la intersección entre juego, ciencia y cultura antigua**. Ese nicho no está ocupado por nadie. La evolución natural es expandir el contenido (sitios, calendarios, estrellas) manteniendo la calidad técnica y narrativa que ya tiene.

*"Antes de que el tiempo se fracture."*

---

*Documento generado: Abril 2026*
*Versión: 1.0*
*Commits en main: ~40 en esta sesión*
