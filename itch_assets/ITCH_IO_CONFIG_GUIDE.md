# 🎮 Guía de Publicación y Ficha para itch.io
## Archeoscope: The Forgotten Relics

Esta guía contiene la configuración exacta recomendada para crear la ficha en **itch.io** y subir el archivo HTML5 ejecutable en el navegador.

---

## 1. Configuración Básica (Project Details)

| Campo | Valor recomendado |
| :--- | :--- |
| **Title** | `Archeoscope: The Forgotten Relics` |
| **Project URL** | `https://tu-usuario.itch.io/archeoscope` |
| **Short description / Tagline** | *Exploración 3D arqueoastronómica interactiva en tiempo real por civilizaciones antiguas y sus misterios.* |
| **Classification** | **Games** |
| **Kind of project** | **HTML** *(You have a ZIP or HTML file that will be played in the browser)* |
| **Release status** | **In development** / **Released** (según preferencia) |
| **Pricing** | **$0 or donate** (o Free) |

---

## 2. Archivo del Juego (Uploads)

1. Compila y empaqueta el juego ejecutando en la terminal:
   ```bash
   cd viewer3d
   bun run build:itch
   ```
2. Esto generará el archivo:
   `viewer3d/releases/ArcheoScope_Web.zip`
3. En la sección **Uploads** de itch.io:
   - Haz clic en **Upload files** y selecciona `ArcheoScope_Web.zip`.
   - Marca la casilla: **[x] This file will be played in the browser**.
   - (Opcional) Activa también la casilla `Executable` si deseas permitir que la gente descargue el ZIP offline.

---

## 3. Configuración de Pantalla (Embed Options)

| Ajuste | Valor recomendado | Explicación |
| :--- | :--- | :--- |
| **Viewport dimensions** | `1280` × `720` | Proporción 16:9 HD estándar. También puedes usar `1920` × `1080` si prefieres Full HD. |
| **Orientation** | `Landscape` | El juego 3D está diseñado principalmente para formato horizontal. |
| **Frame options** | **[x] Enable fullscreen button** | Permite a los usuarios jugar a pantalla completa inmersiva con un clic. |
| | **[x] Auto-load on page load** | Carga el juego automáticamente (o *Click to play* para no consumir ancho de banda de inmediato). |
| | **[ ] Scrollbars** *(desmarcado)* | Evita que aparezcan barras de desplazamiento molestas en el canvas 3D. |
| **Mobile friendly** | **[x] Automatically detect mobile** | ArcheoScope cuenta con menú astronómico responsive adaptado para móviles. |

---

## 4. Clasificación, Géneros y Etiquetas (Tags)

- **Genre**: `Adventure` / `Simulation` / `Educational`
- **Tags sugeridos**:
  ```text
  3D, HTML5, WebGL, Three.js, Astronomy, Archaeology, Exploration, Ancient, Aliens, Historical, Sci-fi, Atmospheric, Interactive Fiction, Next.js
  ```

---

## 5. Descripción de la Ficha (Text formatting)

Puedes copiar y pegar este texto formateado directamente en el editor de descripción de itch.io:

```markdown
# 🏺 Archeoscope: The Forgotten Relics

**Archeoscope** es una experiencia inmersiva en 3D que fusiona la **arqueología de civilizaciones antiguas**, la **astronomía posicional en tiempo real** y el **misterio de reliquias perdidas**.

---

### ✨ Características Principales

- 🌍 **Exploración 3D de Sitios Arqueológicos**: Recorre reconstrucciones interactivas de las Pirámides y Esfinge de Giza, templos mesoamericanos de Teotihuacán, las estructuras ciclópeas de Puma Punku, las misteriosas cabezas Olmecas de Tres Zapotes y los Moáis de la Isla de Pascua.
- 🔭 **Motor Astronómico en Tiempo Real**: Cálculos precisos de posición lunar, fases, constelaciones, cartas natales y alineaciones celestes antiguas (mediante algoritmos VSOP87).
- 🛸 **Reliquias y Enigmas Ocultos**: Encuentra artefactos perdidos (Máscara de Jade, Cráneo de Cristal, Piramidión, Fuente Magna, Escarabajo Sagrado) y activa portales interdimensionales.
- 🎼 **Harmonia Mundi**: Frecuencias planetarias y paisaje sonoro procedural basado en las leyes de Kepler (*Harmonices Mundi*).
- 🌦️ **Sistema Climático Dinámico**: Transiciones de día, noche, niebla desértica, lluvias y tormentas.

---

### 🕹️ Controles

| Acción | Teclado / Mouse |
| :--- | :--- |
| **Moverse / Navegar** | `W`, `A`, `S`, `D` o `Flechas` |
| **Girar cámara** | Click izquierdo y arrastrar el mouse |
| **Zoom** | Rueda del mouse (Scroll) |
| **Interactuar / Escanear** | Click sobre objetos, monolitos y NPCs |
| **Modo Cámara (Órbita / Avatar)** | Botón en el HUD superior |
| **Pantalla Completa** | Botón en la esquina inferior del marco |

---

### 📜 Créditos y Tecnologías

- **Desarrollo**: Ignacio Fernandez
- **Tecnologías**: Three.js, React Three Fiber, Next.js, WebGL, Web Audio API, Astronomy Engine.
- **Licencia**: Creative Commons BY-NC 4.0 (código) · Todos los derechos reservados © Ignacio Fernandez (modelos 3D y diseño sonoro).
```

---

## 6. Checklist de Material Gráfico

- [x] **Cover image**: 630×500 px (o 1260×1000 px) ubicado en `itch_assets/cover.png` o `viewer3d/public/branding/logo/logo-main.png`.
- [x] **Screenshots**: Disponibles en `viewer3d/public/screenshots/desktop.png` y `viewer3d/public/screenshots/mobile.png`.
