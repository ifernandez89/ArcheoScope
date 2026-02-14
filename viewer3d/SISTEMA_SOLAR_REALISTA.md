# Sistema Solar Realista con Astronomy Engine

## 🌌 Filosofía

Este sistema implementa un simulador solar con **posiciones astronómicas reales** calculadas dinámicamente según la fecha, pero con **distancias y tamaños escalados visualmente** para una experiencia contemplativa.

### ✅ Lo que SÍ es real:
- **Posiciones heliocéntricas** calculadas con `astronomy-engine`
- **Velocidades orbitales** reales (los planetas se mueven a su velocidad correcta)
- **Fecha y hora** del sistema (puedes ver dónde están los planetas HOY)
- **Relaciones orbitales** (proporciones entre órbitas)

### ❌ Lo que NO es real (y por qué):
- **Distancias**: Escaladas visualmente (si fueran reales, no verías nada)
- **Tamaños**: Artísticos (el Sol real es 109x la Tierra, aquí es 46x)
- **Inclinaciones orbitales**: Simplificadas (para mejor visualización)

---

## 🏗️ Arquitectura Modular

### 1. Motor Astronómico (`lib/astronomyEngine.ts`)

Tres capas independientes:

#### **Capa 1: Cálculo Astronómico**
```typescript
calculateOrbitalPositions(date: Date): OrbitalState
```
- Usa `astronomy-engine` para calcular posiciones heliocéntricas reales
- Retorna coordenadas en AU (Unidades Astronómicas)
- Incluye Sol, Mercurio, Venus, Tierra, Luna, Marte

#### **Capa 2: Motor de Tiempo**
```typescript
class TimeEngine {
  update(deltaSeconds: number): Date
  setTimeScale(scale: number): void
}
```
- Acelera el tiempo de forma configurable
- Por defecto: **1 segundo real = 1 día simulado**
- Configurable: 1 hora real = 1 día, 1 seg = 1 año, etc.

#### **Capa 3: Escalador Visual**
```typescript
class VisualScaler {
  toSceneCoordinates(pos: PlanetPosition): Vector3
}
```
- Convierte AU a unidades de escena Three.js
- Mantiene proporciones relativas
- Escala configurable (por defecto: Tierra a 200 unidades)

---

## 🎮 Controles

### Teclado:
- **ESPACIO**: Pausar/Reanudar simulación
- **+/-**: Aumentar/Disminuir velocidad de tiempo
- **R**: Resetear a fecha actual

### Mouse:
- **Click izquierdo + arrastrar**: Rotar cámara
- **Rueda**: Zoom in/out
- **Click derecho + arrastrar**: Pan

---

## 🚀 Uso

### Acceso directo:
```
http://localhost:3000/realistic-solar
```

### Integración en código:
```tsx
import RealisticSolarSystem from '@/components/RealisticSolarSystem'

<RealisticSolarSystem 
  onLocationClick={(lat, lon) => console.log(lat, lon)}
  markerPosition={{ lat: 0, lon: 0 }}
/>
```

---

## 📊 Escalas de Tiempo Disponibles

| Escala | Descripción | Uso |
|--------|-------------|-----|
| `1` | Tiempo real | Observación lenta |
| `60` | 1 seg = 1 min | Movimiento visible |
| `3600` | 1 seg = 1 hora | Órbitas perceptibles |
| `86400` | 1 seg = 1 día | **Por defecto** - Movimiento fluido |
| `604800` | 1 seg = 1 semana | Órbitas rápidas |
| `2592000` | 1 seg = 1 mes | Muy rápido |
| `31536000` | 1 seg = 1 año | Extremadamente rápido |

---

## 🔬 Datos Técnicos

### Posiciones Heliocéntricas (AU):
- **Mercurio**: ~0.39 AU del Sol
- **Venus**: ~0.72 AU del Sol
- **Tierra**: ~1.0 AU del Sol (por definición)
- **Marte**: ~1.52 AU del Sol

### Escalado Visual (unidades de escena):
- **Mercurio**: ~78 unidades
- **Venus**: ~144 unidades
- **Tierra**: ~200 unidades (referencia)
- **Marte**: ~304 unidades

### Tamaños Artísticos (radios terrestres):
- **Sol**: 46.56 (real: 109)
- **Mercurio**: 0.38 (real: 0.38) ✅
- **Venus**: 0.95 (real: 0.95) ✅
- **Tierra**: 1.0 (referencia)
- **Marte**: 0.5 (real: 0.53) ≈

---

## 🧪 Ejemplo de Uso Avanzado

```typescript
import { AstronomicalSystem } from '@/lib/astronomyEngine'

// Crear sistema personalizado
const system = new AstronomicalSystem(
  new Date('2024-01-01'), // Fecha inicial
  86400,                  // 1 seg = 1 día
  200                     // Escala visual
)

// En tu loop de animación
const positions = system.update(deltaTime)

// Usar posiciones
planet.position.set(
  positions.earth.x,
  positions.earth.y,
  positions.earth.z
)

// Cambiar velocidad en runtime
system.getTimeEngine().setTimeScale(604800) // 1 seg = 1 semana
```

---

## 📚 Dependencias

- **astronomy-engine**: Cálculos astronómicos precisos
- **Three.js**: Renderizado 3D
- **React Three Fiber**: Integración React + Three.js

---

## 🎯 Próximas Mejoras (Opcionales)

- [ ] Inclinación orbital real (7° Mercurio, 3.4° Venus, etc.)
- [ ] Excentricidad orbital real (órbitas elípticas)
- [ ] Rotación axial real (23.5° Tierra)
- [ ] Fases lunares reales
- [ ] Eclipses calculados
- [ ] Trayectorias históricas (ver dónde estaban los planetas en el pasado)
- [ ] Predicción futura (ver dónde estarán)

---

## 🌟 Resultado Visual

El sistema muestra:
- **Mercurio**: Moviéndose rápido cerca del Sol
- **Venus**: Velocidad moderada
- **Tierra**: Velocidad de referencia (constante)
- **Marte**: Más lento que la Tierra
- **Luna**: Orbitando la Tierra muy rápido (13.4x más rápida)

Todo con **posiciones reales** según la fecha actual del sistema.

---

## 🔗 Referencias

- [astronomy-engine](https://github.com/cosinekitty/astronomy) - Librería de cálculos astronómicos
- [VSOP87](https://en.wikipedia.org/wiki/VSOP_(planets)) - Teoría planetaria usada internamente
- [Three.js](https://threejs.org/) - Motor de renderizado 3D
