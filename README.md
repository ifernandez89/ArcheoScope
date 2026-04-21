# Archeoscope: The Forgotten Relics
### Versión 1.0 — Abril 2026

Experiencia interactiva 3D en navegador que combina arqueología, astronomía y narrativa mítica. El jugador explora sitios arqueológicos reales del mundo antiguo, resuelve misiones, recolecta artefactos sagrados y completa el ritual final en Göbekli Tepe.

**Demo:** https://ifernandez89.github.io/ArcheoScope

---

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Framework | Next.js 14 (App Router, Static Export) |
| 3D Engine | Three.js + React Three Fiber + Drei |
| Lenguaje | TypeScript |
| Estado | Zustand + useState + localStorage |
| Audio | Web Audio API (procedural) |
| Física | Custom (colisiones, órbitas keplerianas) |
| Deploy | GitHub Pages |

---

## Estructura del Proyecto

```
viewer3d/
├── app/                    # Next.js App Router
│   ├── game/               # Escena principal del juego
│   ├── menu/               # Menú principal, audio, controles, info/créditos
│   ├── player-setup/       # Selección de nave y nombre
│   └── reset/              # Resetear partida
├── components/             # Componentes React/R3F
│   ├── ImmersiveScene.tsx  # Componente raíz del juego (orquesta todo)
│   ├── GizaScene.tsx       # Escena de Giza con pirámide y esfinge
│   ├── EasterIslandScene.tsx
│   ├── TeotihuacanScene.tsx
│   ├── PumaPunkuScene.tsx
│   ├── VeracruzScene.tsx
│   ├── MictlanScene.tsx    # Inframundo azteca
│   ├── GobekliTepeScene.tsx # Escena final con altares
│   ├── DroppableItem.tsx   # Item flotante recogible en el mundo
│   ├── InventoryItem.tsx   # Item en el inventario (Canvas 3D)
│   ├── ToroidalSphere.tsx  # Esfera final que asciende al cielo
│   └── ...
├── systems/
│   ├── HarmoniaMundiSystem.ts  # Audio procedural planetario
│   ├── AudioSystem.ts
│   └── CosmicResonanceSystem.ts
├── engines/
│   ├── SolarEngine.ts      # Cálculo astronómico real
│   ├── AstroEngine.ts
│   └── WorldCore/
├── types/
│   ├── missionState.ts     # Sistema de misiones y progreso
│   ├── player.ts           # Estado del jugador
│   └── gameSettings.ts     # Configuración de audio/video
└── public/                 # Assets estáticos (GLB, texturas, audio)
```

---

## Sitios Arqueológicos y Misiones

### 1. Puma Punku — Bolivia (-16.56°, -68.68°)
- **Misión:** Mover el bloque H para revelar la estructura oculta
- **NPC:** Viracocha — entrega la Fuente Magna prestada al completar 5 misiones
- **Item:** Fuente Magna (no se puede soltar hasta entregarla a Viracocha)

### 2. Giza — Egipto (29.98°, 31.13°)
- **Misión:** Devolver el Piramidión a la cima de la Gran Pirámide
- **Item:** Escarabajo sagrado (bajo la momia)
- **Castigo:** Robar el escarabajo antes de tiempo activa la inundación → Game Over
- **NPC:** Esfinge, Akhenaton, Ramsés II, Hatshepsut

### 3. Teotihuacán — México (19.69°, -98.84°)
- **Misión:** Plantar la semilla de maíz sagrada
- **Item:** Semilla de maíz
- **NPC:** Quetzalcóatl

### 4. Tres Zapotes — Veracruz, México (18.47°, -95.45°)
- **Misión:** Entregar la Máscara de Jade al Olmeca
- **Item:** Máscara de Jade
- **NPC:** Cabeza Colosal Olmeca

### 5. Isla de Pascua — Chile (-27.13°, -109.28°)
- **Misión:** Activar el Merkaba con la nave Titan
- **Items:** Tonatiuh (recogido en Mictlán), Calavera de Cristal
- **Portal:** Obelisco que lleva a Göbekli Tepe

### 6. Mictlán — Inframundo (0.0001°, 0.0001°)
- **Mecánica:** El jugador queda atrapado hasta ver 10 apariciones de Mictlantecuhtli
- **Item:** Tonatiuh (visible solo con nave Phantom + habilidad activa)
- **Botones bloqueados:** Coordenadas y Globo deshabilitados durante el encierro

### 7. Göbekli Tepe — Turquía (37.22°, 38.92°) — FINAL
- **Misión:** Colocar los 4 artefactos en sus altares cardinales
  - Norte: Tonatiuh 🌞
  - Sur: Escarabajo 🪲
  - Este: Calavera de Cristal 💀
  - Oeste: Fuente Magna 🏺
- **Secuencia final:** Esfera toroidal emerge del centro y asciende al cielo (30s)
- **Mensaje:** "Archeoscope / Regresará..."
- **Redirección:** Créditos con auto-scroll

---

## Sistema de Naves (UFOs)

| # | Nombre | Habilidad |
|---|--------|-----------|
| 1 | Phantom | Invisibilidad — revela Tonatiuh en Mictlán |
| 2 | Avenger | Escudo |
| 3 | UAP | Velocidad |
| 4 | Oracle | Escaneo de entidades |
| 5 | Titan | Pulso — activa el Merkaba en Isla de Pascua |

---

## Sistema de Inventario

Los items persisten en `localStorage` y sobreviven recargas de página (F5). Se resetean al iniciar nueva partida.

| Item | Origen | Destino |
|------|--------|---------|
| Fuente Magna (Titicaca) | Lago Titicaca | Viracocha (Puma Punku) |
| Fuente Magna (prestada) | Viracocha | Altar Oeste — Göbekli |
| Escarabajo | Bajo la momia — Giza | Altar Sur — Göbekli |
| Calavera de Cristal | Isla de Pascua | Altar Este — Göbekli |
| Tonatiuh | Mictlán (Phantom) | Altar Norte — Göbekli |
| Semilla de Maíz | Teotihuacán | Plantar en tierra |
| Piramidión | Giza | Cima de la pirámide |
| Máscara de Jade | Isla de Pascua | Olmeca — Veracruz |
| Roca | Entorno | Decorativo |

---

## Sistema de Audio — Harmonia Mundi

Motor de audio procedural basado en frecuencias orbitales reales. Cada misión completada desbloquea una capa sonora.

**Frecuencias planetarias (transpuestas al rango audible):**
- Tierra: 136.10 Hz (C# — "Om cósmico")
- Marte: 144.72 Hz (D)
- Júpiter: 183.58 Hz (F#)
- Saturno: 147.85 Hz (D)
- Urano: 207.36 Hz (G#)
- Neptuno: 211.44 Hz (G#)

**Amplificadores arquitectónicos:**
- Giza → bandpass 150 Hz (frecuencias solares)
- Teotihuacán → highpass 200 Hz (armónicos cristalinos)
- Isla de Pascua → lowpass 80 Hz (subgraves oceánicos)
- Puma Punku → peaking 432 Hz (frecuencia sagrada)
- Göbekli Tepe → bandpass 45 Hz (portal primordial)

**Sonido especial:** Al completar Göbekli Tepe se activa el sonido del escarabajo sagrado (Khepri) — 3 capas de síntesis: wingbeat oscillator, LFO de aleteo, armónicos aerodinámicos.

---

## Sistema Astronómico

Cálculo en tiempo real de posiciones planetarias usando `astronomy-engine`. Escala temporal: 1 segundo real = 1 hora simulada.

- Posición solar real por coordenadas geográficas y fecha
- Fases lunares y eclipses
- Órbitas keplerianas de 8 planetas + Plutón
- Cinturón de asteroides con 1600 instancias (10 modelos × 160)
- Arte generativo orbital basado en resonancias armónicas

---

## Persistencia de Datos (localStorage)

| Clave | Contenido |
|-------|-----------|
| `player_state` | Nombre, nave, última ubicación |
| `mission_state` | Misiones completadas por sitio |
| `game_settings` | Volumen master, volumen Harmonia |
| `inv_scarab` | Escarabajo en inventario |
| `inv_skull` | Calavera en inventario |
| `inv_tonatiuh` | Tonatiuh en inventario |
| `inv_rock` | Roca en inventario |
| `inv_magna_bowl` | Fuente Magna prestada |
| `inv_magna_bowl_original` | Fuente Magna original |
| `game_timer_seconds` | Tiempo total de partida |
| `magna_bowl_thanked` | Si Viracocha ya agradeció |

---

## Modelos 3D (public/)

Todos los modelos están optimizados con Draco compression + simplificación + texturas WebP.

| Modelo | Tamaño | Uso |
|--------|--------|-----|
| mictlantecuhtli.glb | 814 KB | Guardián del Mictlán |
| atlante.glb | 694 KB | Isla de Pascua |
| quetzalcoatl.glb | 858 KB | Teotihuacán |
| akenaton.glb | 534 KB | Giza |
| ramses2.glb | 480 KB | Giza |
| hatshepsut.glb | 331 KB | Giza |
| lanzon_chavin.glb | 237 KB | Decorativo |
| calendario_maya.glb | 1.2 MB | Teotihuacán |
| gobekli_tepe.glb | 910 KB | Escena final |
| tonatiuh_aztec_sun.glb | 704 KB | Altar Norte |
| escarabajo.glb | 679 KB | Altar Sur |
| crystal-skull.glb | 45 KB | Altar Este |
| fuente_magna.glb | 11 MB | Altar Oeste |

---

## Comandos de Desarrollo

```bash
# Instalar dependencias
cd viewer3d && bun install

# Desarrollo local
bun run dev

# Build para producción (GitHub Pages)
bun run build

# Verificar tipos TypeScript
npx tsc --noEmit
```

---

## Mecánicas Especiales

### Inundación de Giza
Si el jugador roba el escarabajo antes de completar las 5 misiones previas:
1. El escarabajo aparece en el inventario
2. Los botones de navegación se bloquean
3. El agua sube 1m/segundo hasta alcanzar al jugador
4. Game Over → limpia localStorage → redirige al menú

### Trampa del Mictlán
Al entrar al Mictlán, los botones de coordenadas y globo se deshabilitan. La única salida es esperar 10 apariciones de Mictlantecuhtli (cada 4-10 segundos).

### Ritual de Göbekli Tepe
Los 4 items deben colocarse en sus altares cardinales. Si el jugador se equivoca, puede recoger el item y reposicionarlo. Una vez los 4 están correctos, la secuencia es irreversible.

---

## Créditos y Referencias

- **Harmonices Mundi** — Johannes Kepler (1619): frecuencias orbitales
- **Teoría Sintérgica** — Jacobo Grinberg-Zylberbaum: red energética planetaria
- **Frecuencia 136.10 Hz** — "Om cósmico" (año terrestre transpuesto)
- **432 Hz** — Frecuencia de afinación natural (Puma Punku)
- **Yale Bright Star Catalogue** — ~250 estrellas con RA/Dec reales implementadas
- **Arqueoastronomía** — Alineaciones solares calculadas con fórmula `cos(Az) = sin(δ) / cos(φ)`

*Estas referencias han sido reinterpretadas libremente con fines artísticos y narrativos.*

---

## Módulo Científico — Panel de Información

Al activar "Mostrar Info" en el juego, se despliega un panel científico con datos en tiempo real:

### 📍 Ubicación
- Nombre del sitio arqueológico, cultura y período histórico
- Coordenadas geográficas con precisión de 5 decimales

### ☀️ Astronomía Solar (tiempo real)
- **Azimut solar** — dirección del sol en el horizonte (0°=Norte, 90°=Este)
- **Elevación** — altura sobre el horizonte en grados
- **Declinación** — inclinación axial de la Tierra en la fecha simulada
- **Fase** — día o noche según posición solar
- **Estación** — calculada por hemisferio y día del año

### 🕐 Tiempo Simulado
- Fecha y hora calculadas por el motor astronómico `SolarEngine`
- Escala temporal: 1 segundo real = 2 minutos simulados

### 🌍 Entorno
- Bioma detectado por coordenadas geográficas
- Temperatura y humedad del bioma

### ✦ Alineaciones Solares Arqueoastronómicas
Líneas visuales desde el sitio hacia el horizonte mostrando dónde sale/pone el sol en:

| Evento | Declinación | Color |
|--------|-------------|-------|
| Solsticio de Verano | +23.44° | Naranja |
| Equinoccios | 0° | Azul |
| Solsticio de Invierno | -23.44° | Violeta |

Fórmula utilizada: `cos(Az_salida) = sin(δ) / cos(φ)` donde δ = declinación solar, φ = latitud

Ejemplo en Giza (lat 29.98°N):
- Solsticio verano: sale a **62.5°** (NE), pone a **297.5°** (NO)
- Equinoccio: sale a **90°** (E exacto), pone a **270°** (O exacto)
- Solsticio invierno: sale a **117.5°** (SE), pone a **242.5°** (SO)

### 🌟 Cielo Estelar Real
~250 estrellas del Yale Bright Star Catalogue en posición astronómica exacta:
- **Sirio** (mag -1.46), **Vega** (0.03), **Betelgeuse** (0.45), **Rigel** (0.12)
- **Orión**, **Cruz del Sur**, **Osa Mayor**, **Casiopea** reconocibles
- Color espectral correcto: O=azul, B=azul-blanco, A=blanco, G=amarillo, K=naranja, M=rojo
- Tamaño proporcional a la magnitud visual

---

## Calidad Gráfica

Menú Video → 3 presets:

| Preset | Sombras | Bloom | Antialiasing | Pixel Ratio | Uso |
|--------|---------|-------|--------------|-------------|-----|
| **Baja** | ✗ | ✗ | ✗ | 0.75x | Laptops / navegadores lentos |
| **Media** | ✓ básicas | ✗ | ✓ | 1.0x | Balance rendimiento/calidad |
| **Alta** | ✓ suaves | ✓ | ✓ | nativo | GPU dedicada |

---

## Créditos y Referencias

- **Harmonices Mundi** — Johannes Kepler (1619): frecuencias orbitales
- **Teoría Sintérgica** — Jacobo Grinberg-Zylberbaum: red energética planetaria
- **Frecuencia 136.10 Hz** — "Om cósmico" (año terrestre transpuesto)
- **432 Hz** — Frecuencia de afinación natural (Puma Punku)

*Estas referencias han sido reinterpretadas libremente con fines artísticos y narrativos.*

---

**Archeoscope v1.0** — 2026 | [GitHub](https://github.com/ifernandez89/ArcheoScope)
