# Sistema Solar Completo - ArcheoScope 3D

## 🌟 Descripción

Sistema solar interactivo con proporciones orbitales reales y escala artística coherente. El Sol está en el centro y todos los planetas orbitan alrededor de él, incluyendo la Tierra con su Luna.

## 🎯 Arquitectura: Sistema Híbrido Profesional

### Filosofía de Escala

- **Tamaños planetarios:** Proporciones reales respetadas
- **Órbitas:** Proporciones reales respetadas (Tierra = 100 unidades)
- **Sol:** Comprimido a 15 radios (real sería 109) para visibilidad

### Unidad Base

`1 unidad = radio de la Tierra`

## 🪐 Planetas Implementados

### ☀️ Sol (Centro del Sistema)
- **Posición:** (0, 0, 0) - Centro absoluto
- **Radio:** 15 unidades (comprimido)
- **Características:**
  - Shader procedural con plasma turbulento
  - Textura 8K NASA
  - Granulación celular visible
  - Manchas solares
  - Corona irregular
  - Iluminación direccional y puntual

### ☿ Mercurio
- **Radio:** 0.38 unidades (38% de la Tierra)
- **Órbita:** 39 unidades (0.39 UA)
- **Velocidad:** 4.15 (el más rápido)
- **Textura:** 8K lunar (placeholder similar)
- **Color:** Gris rocoso (#9c9c9c)
- **Características:** Sin atmósfera, superficie craterizada

### ♀ Venus
- **Radio:** 0.95 unidades (95% de la Tierra)
- **Órbita:** 72 unidades (0.72 UA)
- **Velocidad:** 1.62
- **Textura:** 4K atmósfera densa
- **Color:** Crema pálido (#f5e6d3)
- **Características:** 
  - Atmósfera densa opaca
  - Emisión 0.15 (brilla más que Marte)
  - Rotación retrógrada

### 🌍 Tierra
- **Radio:** 1.0 unidad (referencia)
- **Órbita:** 100 unidades (1.0 UA)
- **Velocidad:** 1.0 (referencia)
- **Textura:** 8K superficie + nubes
- **Características:**
  - Globe3D interactivo
  - Click para teletransporte
  - Marcadores de coordenadas
  - Rotación propia

### 🌙 Luna (Satélite de la Tierra)
- **Radio:** 0.27 unidades (27% de la Tierra)
- **Órbita:** 12 unidades de la Tierra
- **Velocidad:** 0.08
- **Textura:** 8K superficie lunar
- **Características:**
  - Tidal locking (misma cara siempre visible)
  - Inclinación orbital 5°
  - Órbita visible en gris
  - Orbita en coordenadas relativas a la Tierra

### ♂ Marte
- **Radio:** 0.53 unidades (53% de la Tierra)
- **Órbita:** 152 unidades (1.52 UA)
- **Velocidad:** 0.53 (más lento)
- **Textura:** 8K superficie marciana
- **Color:** Rojo terroso (#8b6f5f)
- **Características:**
  - Atmósfera tenue rojiza
  - Superficie visible con cráteres
  - Tonos desaturados (óxido, no semáforo)

## 🎨 Características Visuales

### Órbitas Visibles
- Cada planeta tiene su órbita marcada con color distintivo
- Opacidad ajustada para visibilidad sin saturar
- Siempre visibles para orientación

### Etiquetas Dinámicas
- Cada planeta tiene su etiqueta con símbolo astronómico
- Las etiquetas siguen a los planetas en su órbita
- Actualizadas en cada frame
- Colores coordinados con cada planeta

### Iluminación
- Sol como fuente de luz principal
- Luz direccional para sombras realistas
- Luz puntual para iluminación ambiental
- Todos los planetas reciben iluminación del Sol

## 🎮 Interactividad

### Controles de Cámara
- **Zoom:** Scroll del mouse (8-300 unidades)
- **Rotación:** Click + arrastrar
- **Pan:** Click derecho + arrastrar
- **Damping:** Movimiento suave y fluido

### Sistema de Zoom Narrativo
- **Nivel Mundo (8-50):** Tierra y Luna
- **Nivel Orbital (50-100):** Aparecen planetas interiores
- **Nivel Solar (100-200):** Sistema completo visible
- **Nivel Sistema (200+):** Vista panorámica

## 📊 Proporciones Orbitales Reales

| Planeta | UA Real | Unidades | Proporción |
|---------|---------|----------|------------|
| Mercurio | 0.39 | 39 | ✓ |
| Venus | 0.72 | 72 | ✓ |
| Tierra | 1.00 | 100 | ✓ |
| Marte | 1.52 | 152 | ✓ |

## 🔧 Componentes Técnicos

### Módulos Independientes
- `Sun.tsx` - Sol con shader procedural
- `Mercury.tsx` - Mercurio con textura y etiqueta
- `Venus.tsx` - Venus con atmósfera y etiqueta
- `Mars.tsx` - Marte con atmósfera y etiqueta
- `SimpleMoon.tsx` - Luna con tidal locking
- `EarthOrbitWrapper.tsx` - Wrapper que hace orbitar la Tierra
- `LunarOrbitLine.tsx` - Órbita de la Luna
- `PlanetaryOrbits.tsx` - Órbitas planetarias visibles

### Shaders
- `sunShader.ts` - Shader procedural del Sol
  - Voronoi noise para granulación
  - FBM para turbulencia
  - Vertex displacement para protuberancias
  - 5 niveles de color (negro rojizo → blanco caliente)

## 🚀 Performance

### Optimizaciones
- Geometrías con LOD apropiado
- Texturas comprimidas
- Shaders optimizados
- Culling automático
- Damping para suavidad

### Métricas
- **FPS:** 60fps en hardware moderno
- **Polígonos:** ~500k totales
- **Texturas:** ~150MB en memoria
- **Límite:** Muy lejos del techo WebGL

## 🎯 Jerarquía Visual

La obra mantiene una jerarquía contemplativa:

1. **Sol** → Fuente dominante (centro)
2. **Tierra** → Protagonista emocional
3. **Luna** → Ritmo cercano
4. **Venus** → Presencia brillante discreta
5. **Mercurio** → Pequeño y veloz
6. **Marte** → Presencia distante y sobria

## 📝 Notas de Diseño

### Escala Artística vs Real
- **Real:** Distancias absurdamente grandes, planetas invisibles
- **Artística:** Proporciones respetadas, visibilidad garantizada
- **Resultado:** Experiencia contemplativa y educativa

### Filosofía
> "No es exactitud matemática. Es percepción humana."

La obra es contemplativa, no arcade. Cada decisión de escala busca mantener:
- Proporciones planetarias reales
- Distancias expresivas (no literales)
- Jerarquía visual clara
- Descubrimiento progresivo
- Coherencia emocional

## 🔮 Futuras Expansiones

Posibles adiciones:
- Júpiter y Saturno (requiere repensar escala)
- Cinturón de asteroides
- Cometas
- Modo "escala real" (distancias brutales)
- Trayectorias históricas de sondas espaciales

---

**Versión:** 1.0.0  
**Fecha:** Febrero 2026  
**Estado:** Producción  
**Despliegue:** GitHub Pages
