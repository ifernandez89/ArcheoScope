# 🎓 Tooltips Educativos - Sistema Solar Interactivo

## 📚 Descripción

Sistema de tooltips informativos con hover para cada cuerpo celeste del sistema solar. Proporciona información científica precisa de manera visual y accesible.

---

## 🌟 Características

### Diseño UX Optimizado
- ✅ **Hover interactivo** - Aparece al pasar el mouse sobre las etiquetas
- ✅ **Máximo 4 datos clave** - Información concisa y relevante
- ✅ **1 dato curioso destacado** - En color dorado para impacto visual
- ✅ **Animación suave** - Transición fadeIn de 0.2s
- ✅ **Borde del color del planeta** - Identidad visual clara
- ✅ **Fondo oscuro con blur** - Legibilidad óptima

### Información Mostrada

#### ☀️ SOL
- **Tipo**: Estrella (G2V)
- **Diámetro**: 1.39 millones km
- **Temperatura**: 5.500°C (superficie)
- **Rotación**: ~27 días
- **Dato curioso**: Contiene el 99.86% de la masa del sistema solar

#### ☿ MERCURIO
- **Periodo orbital**: 88 días
- **Día solar**: 176 días terrestres
- **Diámetro**: 4.879 km
- **Temperatura**: -173°C a 427°C
- **Atmósfera**: Sin atmósfera
- **Dato curioso**: Un año dura menos que su día

#### ♀ VENUS
- **Periodo orbital**: 225 días
- **Día**: 243 días (retrógrado)
- **Diámetro**: 12.104 km
- **Temperatura**: 465°C
- **Atmósfera**: CO₂ extremadamente densa
- **Dato curioso**: El planeta más caliente del sistema

#### 🌍 TIERRA
- **Periodo orbital**: 365.25 días
- **Día**: 24 horas
- **Diámetro**: 12.742 km
- **Temperatura**: -88°C a 58°C
- **Lunas**: 1 (Luna)
- **Atmósfera**: N₂ 78%, O₂ 21%
- **Dato curioso**: Único planeta conocido con vida

#### 🌙 LUNA
- **Periodo orbital**: 27.3 días
- **Diámetro**: 3.474 km
- **Temperatura**: -173°C a 127°C
- **Dato curioso**: Siempre muestra la misma cara a la Tierra

#### ♂ MARTE
- **Periodo orbital**: 687 días
- **Día**: 24h 37m
- **Diámetro**: 6.779 km
- **Temperatura**: -60°C
- **Lunas**: 2 (Fobos y Deimos)
- **Dato curioso**: Día casi igual al terrestre

---

## 🎨 Diseño Visual

### Estructura del Tooltip
```
┌─────────────────────────────┐
│ NOMBRE DEL PLANETA          │ ← Color del planeta
├─────────────────────────────┤
│ Tipo de cuerpo              │ ← Gris
├─────────────────────────────┤
│ 🪐 Dato 1                   │
│ ☀️ Dato 2                   │
│ 🌡️ Dato 3                   │
│ 📏 Dato 4                   │
├─────────────────────────────┤
│ ✨ Dato curioso destacado   │ ← Dorado
└─────────────────────────────┘
```

### Colores por Planeta
- **Sol**: `#ffaa00` (Naranja dorado)
- **Mercurio**: `#9c9c9c` (Gris)
- **Venus**: `#f5e6d3` (Crema)
- **Tierra**: `#4a9eff` (Azul)
- **Luna**: `#FFFFFF` (Blanco)
- **Marte**: `#c97a5f` (Rojo terroso)

---

## 💻 Implementación Técnica

### Componente Principal
```typescript
<CelestialTooltip
  name="Tierra"
  symbol="🌍"
  type="Planeta rocoso"
  data={{
    orbitalPeriod: "365.25 días",
    day: "24 horas",
    diameter: "12.742 km",
    temperature: "-88°C a 58°C",
    moons: "1 (Luna)",
    atmosphere: "N₂ 78%, O₂ 21%",
    funFact: "Único planeta conocido con vida"
  }}
  position={[0, 7, 0]}
  color="#4a9eff"
/>
```

### Props del Componente
- `name`: Nombre del cuerpo celeste
- `symbol`: Emoji o símbolo astronómico
- `type`: Clasificación (Estrella, Planeta rocoso, Satélite natural)
- `data`: Objeto con información científica
- `position`: Posición 3D del tooltip
- `color`: Color del borde y título

---

## 🎯 Filosofía de Diseño

### Lo que SÍ mostramos:
✅ Datos comprensibles (días, horas, km, °C)
✅ Información relevante y curiosa
✅ Comparaciones con la Tierra
✅ Hechos impactantes

### Lo que NO mostramos:
❌ Masa en notación científica larga
❌ Densidad detallada
❌ Gravedad con 6 decimales
❌ Inclinaciones orbitales complejas

**Principio**: Hover debe ser rápido, legible e impactante.

---

## 🚀 Mejoras Futuras (Nivel Pro)

### Datos Dinámicos en Tiempo Real
- [ ] Distancia actual al Sol (calculada con astronomy-engine)
- [ ] Velocidad orbital actual
- [ ] Fase lunar actual
- [ ] Posición en el cielo desde la Tierra

### Interactividad Avanzada
- [ ] Click para fijar el tooltip
- [ ] Botón "Más información" que abre panel detallado
- [ ] Comparador de planetas (seleccionar 2 para comparar)
- [ ] Modo "Quiz" educativo

---

## 📊 Métricas de Éxito

- **Legibilidad**: Información clara en menos de 3 segundos
- **Engagement**: Usuarios exploran múltiples planetas
- **Educativo**: Datos científicos precisos y verificables
- **Accesibilidad**: Contraste WCAG AA compliant

---

## 🔗 Referencias Científicas

- NASA Solar System Exploration
- JPL Horizons System
- IAU (International Astronomical Union)
- astronomy-engine library

---

## 📝 Notas de Desarrollo

**Archivo**: `viewer3d/components/CelestialTooltip.tsx`

**Dependencias**:
- `@react-three/drei` (Html component)
- React hooks (useState)

**Estilo**: Inline styles con animaciones CSS

**Performance**: Tooltips se renderizan solo en hover (optimizado)
