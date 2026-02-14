# 🌌 Sistema Solar Contemplativo

## Visión

Una obra interactiva estructurada por leyes reales. No es una herramienta educativa, es una experiencia contemplativa donde el usuario habita e intuye el cosmos.

## Filosofía

> "No estás construyendo una app. Estás construyendo una obra interactiva estructurada por leyes reales."

### Principios

1. **Nada didáctico explícito** - El sistema existe, el usuario lo descubre
2. **Nada técnico visible por defecto** - Todo debe revelarse lentamente
3. **Todo obedece leyes reales** - Cálculos astronómicos precisos
4. **La profundidad se revela lentamente** - Capas de descubrimiento

## Arquitectura de 3 Capas

### CAPA 1 — Ley Real (Oculta)
**Archivo**: `lib/astronomy.ts`

Cálculos astronómicos precisos:
- Posición solar real según fecha y ubicación
- Órbita terrestre elíptica (excentricidad 0.0167)
- Inclinación axial 23.44°
- Órbita lunar (29.53 días)
- Inclinación lunar 5.145°
- Ecuación del tiempo
- Declinación solar
- Azimut y elevación

Nada de esto se anuncia. Todo es consecuencia.

### CAPA 2 — Manifestación Visible
**Archivo**: `components/SolarSystem.tsx`

Lo que el usuario percibe:
- Sombras que cambian lentamente
- Estaciones perceptibles
- El arco solar que aparece si se detiene
- La eclíptica revelándose como plano tenue
- La órbita visible solo en cierto modo contemplativo
- La Luna cruzando el cielo lentamente

#### Escalas Desacopladas

El sistema usa 3 escalas distintas (nunca 1:1 real):
- Escala de tamaños
- Escala de distancias
- Escala de órbitas

**Escala real sería inutilizable**:
- Sol = 109 Tierras de diámetro
- Distancia Tierra-Sol = 107 diámetros solares
- La Tierra sería microscópica
- La Luna invisible

### CAPA 3 — Poética

**Tiempo continuo**: El tiempo nunca se detiene, aunque el usuario no haga nada

**Sonido** (futuro):
- Drone ambiental casi imperceptible
- Viento leve que cambia con elevación solar
- Pájaros sutiles en amanecer
- Silencio profundo en noche
- No soundtrack, atmósfera

## Modos de Vista

### 🌍 MODO 1 — Contemplación (Vista Local)
**Objetivo**: Arqueoastronomía

- Tierra dominante
- Sol como fuente de luz distante (direccional)
- No se muestra tamaño real del Sol
- Se muestra vector solar
- Plano eclíptico bajo demanda

**Escalas**:
- Tierra: 1
- Sol: implícito (luz direccional)
- Luna: 0.27
- Distancia Sol: "infinita"
- Distancia Luna: 15 radios terrestres

### ☀️ MODO 2 — Revelación (Vista Orbital Conceptual)
**Objetivo**: Comprender estaciones

- Sol visible pequeño
- Órbita terrestre visible
- Inclinación axial visible
- Plano eclíptico visible
- Distancias comprimidas

**Escalas**:
- Tierra: 1
- Sol: 3
- Distancia Sol: 150
- Mantiene proporciones legibles

### 🌌 MODO 3 — Expansión (Vista Sistema)
**Objetivo**: Coherencia visual

- Sol visible
- Tierra y Luna
- Órbitas visibles como líneas
- Distancias reinterpretadas

**Escalas**:
- Tierra: 1
- Sol: 10
- Distancia Sol: 100

### 🪐 MODO 4 — Sistema (Vista Completa)
**Objetivo**: Contexto cósmico

- Sistema solar completo
- Marte y Venus visibles
- Distancias logarítmicas
- `distance_display = log(real_distance) * k`

## Elementos del Sistema

### ☀️ Sol
- Mesh emisivo con textura real (NASA SDO)
- Pulsación sutil (respiración)
- Luz direccional realista
- Visible solo en modos revelation+

### 🌍 Tierra
- Inclinación axial real: 23.44°
- Rotación diaria (24h)
- Órbita anual elíptica
- Textura 8K de NASA
- Atmósfera sutil
- Nubes dinámicas (futuro)

### 🌙 Luna
- Órbita mensual (29.53 días)
- Inclinación orbital 5.145°
- Fases lunares calculadas
- Textura 8K de NASA LRO
- Afecta luminosidad nocturna

### 🔴 Marte (Futuro)
- Solo visible en elongación favorable
- No como lista, como aparición
- Textura 8K de NASA Viking

### 🌟 Venus (Futuro)
- Atmósfera visible
- Superficie bajo nubes
- Fases visibles

## Texturas

### Disponibles
- ✅ Tierra 8K (NASA Visible Earth)
- ✅ Nubes 8K
- ✅ Tierra nocturna 8K

### Por Descargar
Ver: `DESCARGAR_TEXTURAS.md`

- ⬜ Luna 8K (NASA LRO)
- ⬜ Sol 8K (NASA SDO)
- ⬜ Marte 8K (NASA Viking)
- ⬜ Venus 8K (NASA Magellan)

## Implementación

### Uso Básico

```tsx
import SolarSystem from '@/components/SolarSystem'

<SolarSystem
  latitude={-13.163}
  longitude={-72.545}
  mode="contemplation"
  showEcliptic={false}
  showOrbits={false}
/>
```

### Transiciones entre Modos

```tsx
const [mode, setMode] = useState('contemplation')

// Transición suave
useEffect(() => {
  // Animar cámara
  // Fade in/out de elementos
  // Cambiar escalas gradualmente
}, [mode])
```

## Cálculos Astronómicos

### Posición Solar

```typescript
import { calculateSolarPosition } from '@/lib/astronomy'

const solarPos = calculateSolarPosition(
  new Date(),
  -13.163,  // Machu Picchu
  -72.545
)

console.log(solarPos.azimuth)     // 0-360°
console.log(solarPos.elevation)   // -90 a 90°
console.log(solarPos.declination) // -23.44 a 23.44°
```

### Arco Solar

```typescript
import { calculateSolarArc } from '@/lib/astronomy'

const arc = calculateSolarArc(
  new Date(),
  -13.163,
  -72.545,
  48  // 48 puntos
)

// Visualizar recorrido del Sol en un día
```

### Arcos Anuales

```typescript
import { calculateAnnualSolarArcs } from '@/lib/astronomy'

const arcs = calculateAnnualSolarArcs(2026, -13.163, -72.545)

console.log(arcs.summerSolstice)  // 21 junio
console.log(arcs.winterSolstice)  // 21 diciembre
console.log(arcs.equinox)         // 20 marzo
```

## Próximos Pasos

### Fase 1 - Base (Actual)
- [x] Cálculos astronómicos reales
- [x] Sol, Tierra, Luna
- [x] 4 modos de vista
- [x] Escalas desacopladas
- [x] Tiempo continuo
- [ ] Descargar texturas
- [ ] Integrar en escena principal

### Fase 2 - Refinamiento
- [ ] Transiciones suaves entre modos
- [ ] Cámara con movimiento orgánico
- [ ] Arco solar visible
- [ ] Plano eclíptico animado
- [ ] Órbitas con fade in/out

### Fase 3 - Poética
- [ ] Sonido ambiental (drone)
- [ ] Viento reactivo
- [ ] Pájaros en amanecer
- [ ] Silencio nocturno
- [ ] Luna afecta ambiente

### Fase 4 - Expansión
- [ ] Marte visible
- [ ] Venus visible
- [ ] Apariciones en elongación
- [ ] Sistema vivo

## Referencias

- **Algoritmos**: Jean Meeus - "Astronomical Algorithms"
- **NASA**: https://nasa3d.arc.nasa.gov/
- **LRO**: https://svs.gsfc.nasa.gov/4720
- **Texturas**: https://www.solarsystemscope.com/textures/

## Inspiración

- CSS 3D Solar System
- Planetarios contemplativos
- Instalaciones digitales
- Esculturas temporales interactivas
- Instrumentos poéticos

---

**"Que lo descubran / que lo sientan"**
