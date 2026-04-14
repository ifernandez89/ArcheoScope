# 🌌 Cosmic Resonance System - Guía de Integración

## 📋 Resumen

Sistema de **resonancia cósmica** que conecta geometría sagrada, órbitas planetarias y frecuencias armónicas. Inspirado en física teórica (String Theory, E8, Loop Quantum Gravity) y la antigua "Music of the Spheres".

**Estado:** ✅ Implementado, listo para integrar
**Impacto:** ⚠️ CERO - No rompe nada existente
**Activación:** 🔒 Opcional - Requiere descubrimiento del jugador

---

## 🎯 Concepto Fundamental

```
Geometría → Vibraciones → Partículas → Eventos

Dodecaedro Cósmico (estructura invisible)
    ↓
Órbitas Planetarias (frecuencias)
    ↓
Alineaciones Geométricas (triángulo, pentágono, dodecaedro)
    ↓
Eventos de Resonancia (impulsos, energía, portales)
```

---

## 🔧 Integración Paso a Paso

### 1️⃣ Importar el Sistema

```typescript
import { getCosmicResonance, type CelestialBody } from '@/systems/CosmicResonanceSystem'
```

### 2️⃣ Inicializar (en tu escena principal)

```typescript
// En tu componente principal (ej: Scene3D.tsx)
const cosmicResonance = getCosmicResonance()

// Habilitar cuando el jugador lo descubra
function onDiscoverCosmicMap() {
  cosmicResonance.discover()
  cosmicResonance.enable(scene) // scene = THREE.Scene
  
  console.log('✨ Mapa Armónico del Sistema Solar desbloqueado!')
}
```

### 3️⃣ Registrar Planetas

```typescript
// Registrar cada planeta del sistema solar
cosmicResonance.registerCelestialBody({
  id: 'earth',
  name: 'Tierra',
  position: new THREE.Vector3(0, 0, 0), // Se actualiza cada frame
  orbitalPeriod: 365.25, // días
  orbitalFrequency: 1 / 365.25, // Hz
  audioFrequency: 136.10, // Hz (C# - "Om cósmico")
  color: '#4A90E2'
})

cosmicResonance.registerCelestialBody({
  id: 'mars',
  name: 'Marte',
  position: new THREE.Vector3(0, 0, 0),
  orbitalPeriod: 687,
  orbitalFrequency: 1 / 687,
  audioFrequency: 144.72, // Hz (D)
  color: '#E27B58'
})

// ... más planetas
```

### 4️⃣ Actualizar Posiciones (cada frame)

```typescript
// En tu loop de animación
function animate() {
  // Actualizar posiciones de planetas
  cosmicResonance.updateBodyPosition('earth', earthMesh.position)
  cosmicResonance.updateBodyPosition('mars', marsMesh.position)
  // ... más planetas
  
  // Actualizar sistema (detecta alineaciones automáticamente)
  cosmicResonance.update(deltaTime)
  
  // Obtener eventos activos
  const events = cosmicResonance.getActiveEvents()
  events.forEach(event => {
    console.log(`✨ ${event.description}`)
    // Aquí puedes activar efectos visuales, audio, recompensas, etc.
  })
}
```

### 5️⃣ UI de Control (opcional)

```typescript
// Botón para mostrar/ocultar visualización
<button onClick={() => {
  const visible = !cosmicResonance.isEnabled()
  cosmicResonance.setVisualizationVisible(visible)
}}>
  {cosmicResonance.isEnabled() ? '🌌 Ocultar Red Cósmica' : '🌌 Mostrar Red Cósmica'}
</button>

// Panel de estadísticas
const stats = cosmicResonance.getStats()
console.log('Cuerpos celestes:', stats.celestialBodies)
console.log('Alineaciones activas:', stats.activeAlignments)
console.log('Eventos totales:', stats.totalEvents)
```

---

## 🎮 Mecánica Jugable

### Descubrimiento

El jugador descubre el sistema al:
- Completar una misión específica (ej: "Göbekli Tepe")
- Encontrar un artefacto antiguo
- Alcanzar cierto nivel de conocimiento

```typescript
// Ejemplo: Al completar misión 6
if (missionId === 'earth_mission_6') {
  cosmicResonance.discover()
  cosmicResonance.enable(scene)
  
  // Mostrar mensaje al jugador
  showNotification('✨ Has descubierto el Mapa Armónico del Sistema Solar!')
}
```

### Eventos de Resonancia

Cuando planetas se alinean en geometrías específicas:

| Geometría | Cuerpos | Efecto | Ratio Armónico |
|-----------|---------|--------|----------------|
| **Triángulo** | 3 | ⚡ Impulso Gravitacional | 1:1:1 |
| **Pentágono** | 5 | 🌟 Energía Orbital | 1:φ (áurea) |
| **Hexágono** | 6 | 🔷 Resonancia Cristalina | 1:2:3 |
| **Dodecaedro** | 12 | 💫 Evento Cósmico Raro | 1:φ:φ² |

### Recompensas Sugeridas

```typescript
const events = cosmicResonance.getActiveEvents()

events.forEach(event => {
  switch (event.type) {
    case 'gravitational_pulse':
      // Impulso de velocidad para la nave
      ship.velocity.multiplyScalar(1.5)
      break
      
    case 'orbital_energy':
      // Recarga de energía
      ship.energy += 50
      break
      
    case 'cosmic_event':
      // Portal a zona secreta
      openPortal(event.alignment.center)
      break
      
    case 'harmonic_resonance':
      // Bonus de experiencia
      player.experience += 100
      break
  }
})
```

---

## 🎨 Visualización

### Elementos Visuales

1. **Dodecaedro Cósmico** (estructura invisible)
   - 20 nodos de resonancia
   - Líneas azules tenues (opacity: 0.1)
   - Siempre presente, pero casi invisible

2. **Líneas de Resonancia** (cuando hay alineaciones)
   - Color según geometría:
     - Triángulo: 🟠 Naranja (#ff6600)
     - Pentágono: 🟡 Amarillo (#ffaa00)
     - Hexágono: 🟢 Verde (#00ff88)
     - Dodecaedro: 🟣 Magenta (#ff00ff)
   - Opacity basada en intensidad de resonancia
   - Blending aditivo (brillan)

3. **Esferas de Energía** (en centros de alineación)
   - Radio proporcional a la alineación
   - Pulsan con la frecuencia de resonancia
   - Semi-transparentes

### Controles de Visualización

```typescript
// Mostrar/ocultar todo
cosmicResonance.setVisualizationVisible(true/false)

// Verificar si está visible
const isVisible = cosmicResonance.isEnabled()
```

---

## 🔊 Audio (Integración con HarmoniaMundiSystem)

El sistema calcula frecuencias, pero **no genera audio directamente**. Se integra con `HarmoniaMundiSystem`:

```typescript
import { getHarmoniaMundi } from '@/systems/HarmoniaMundiSystem'

const harmonia = getHarmoniaMundi()

// Cuando se detecta un evento de resonancia
cosmicResonance.getActiveEvents().forEach(event => {
  if (event.type === 'harmonic_resonance') {
    // Activar capa de audio correspondiente
    harmonia.unlockMissionLayer('earth_mission_resonance')
  }
})
```

---

## 📊 Datos de Planetas (Frecuencias Reales)

Basado en periodos orbitales reales:

| Planeta | Periodo (días) | Frecuencia Base | Nota Musical | Color |
|---------|----------------|-----------------|--------------|-------|
| Mercurio | 88 | 141.27 Hz | C# | #8C7853 |
| Venus | 225 | 221.23 Hz | A | #FFC649 |
| **Tierra** | 365.25 | **136.10 Hz** | **C#** | #4A90E2 |
| Marte | 687 | 144.72 Hz | D | #E27B58 |
| Júpiter | 4333 | 183.58 Hz | F# | #D4A574 |
| Saturno | 10759 | 147.85 Hz | D | #FAD5A5 |
| Urano | 30687 | 207.36 Hz | G# | #4FD0E7 |
| Neptuno | 60190 | 211.44 Hz | G# | #4166F5 |

**Nota:** Frecuencias calculadas como `f = 1/T` y escaladas a rango audible.

---

## 🧪 Testing

### Test Básico

```typescript
// 1. Crear sistema
const cosmic = getCosmicResonance()

// 2. Registrar 3 planetas en triángulo equilátero
cosmic.registerCelestialBody({
  id: 'test1',
  name: 'Test 1',
  position: new THREE.Vector3(100, 0, 0),
  orbitalPeriod: 365,
  orbitalFrequency: 1/365,
  audioFrequency: 136.10,
  color: '#ff0000'
})

cosmic.registerCelestialBody({
  id: 'test2',
  name: 'Test 2',
  position: new THREE.Vector3(-50, 86.6, 0),
  orbitalPeriod: 365,
  orbitalFrequency: 1/365,
  audioFrequency: 136.10,
  color: '#00ff00'
})

cosmic.registerCelestialBody({
  id: 'test3',
  name: 'Test 3',
  position: new THREE.Vector3(-50, -86.6, 0),
  orbitalPeriod: 365,
  orbitalFrequency: 1/365,
  audioFrequency: 136.10,
  color: '#0000ff'
})

// 3. Habilitar y actualizar
cosmic.discover()
cosmic.enable(scene)
cosmic.update(0.016) // 60 FPS

// 4. Verificar detección
const events = cosmic.getActiveEvents()
console.log('Eventos detectados:', events.length)
// Debería detectar 1 triángulo equilátero
```

### Test de Performance

```typescript
// Registrar muchos cuerpos
for (let i = 0; i < 50; i++) {
  const angle = (i / 50) * Math.PI * 2
  const radius = 100 + Math.random() * 200
  
  cosmic.registerCelestialBody({
    id: `body_${i}`,
    name: `Body ${i}`,
    position: new THREE.Vector3(
      Math.cos(angle) * radius,
      0,
      Math.sin(angle) * radius
    ),
    orbitalPeriod: 365 + Math.random() * 1000,
    orbitalFrequency: 1 / (365 + Math.random() * 1000),
    audioFrequency: 100 + Math.random() * 400,
    color: `#${Math.floor(Math.random()*16777215).toString(16)}`
  })
}

// Medir tiempo de actualización
console.time('cosmic_update')
cosmic.update(0.016)
console.timeEnd('cosmic_update')
// Debería ser < 5ms
```

---

## ⚠️ Consideraciones Importantes

### 1. Performance

- **Complejidad:** O(n³) para detectar triángulos (n = número de cuerpos)
- **Optimización:** Limitar a ~20 cuerpos celestes máximo
- **Alternativa:** Usar spatial hashing para grandes cantidades

### 2. Compatibilidad

- ✅ No interfiere con sistemas existentes
- ✅ Puede deshabilitarse completamente
- ✅ Visualización opcional
- ✅ Audio independiente

### 3. Guardado de Estado

```typescript
// Guardar descubrimiento
localStorage.setItem('cosmic_resonance_discovered', 'true')

// Cargar al iniciar
if (localStorage.getItem('cosmic_resonance_discovered') === 'true') {
  cosmicResonance.discover()
  cosmicResonance.enable(scene)
}
```

---

## 🚀 Roadmap de Implementación

### Fase 1: Básico (1-2 horas)
- [x] Sistema creado
- [ ] Integrar en Scene3D
- [ ] Registrar planetas del sistema solar
- [ ] Test de detección de triángulos

### Fase 2: Visualización (2-3 horas)
- [ ] Mejorar shaders de líneas de resonancia
- [ ] Añadir partículas que fluyen por las líneas
- [ ] Animaciones de pulso en esferas de energía
- [ ] UI de control (mostrar/ocultar)

### Fase 3: Gameplay (3-4 horas)
- [ ] Sistema de descubrimiento (misión específica)
- [ ] Recompensas por eventos de resonancia
- [ ] Portales cósmicos (dodecaedro)
- [ ] Integración con progresión del jugador

### Fase 4: Audio (2-3 horas)
- [ ] Conectar con HarmoniaMundiSystem
- [ ] Sonidos específicos por tipo de evento
- [ ] Música procedural basada en alineaciones
- [ ] Efectos de audio espacial (3D)

### Fase 5: Polish (2-3 horas)
- [ ] Tutoriales in-game
- [ ] Codex de eventos descubiertos
- [ ] Estadísticas y achievements
- [ ] Optimización final

**Total estimado:** 10-15 horas

---

## 📚 Referencias Científicas

### String Theory
- Partículas como modos de vibración de cuerdas
- Dimensiones extra compactificadas
- Resonancias fundamentales

### Loop Quantum Gravity
- Espacio-tiempo discreto (spin networks)
- Geometría cuántica
- Nodos y conexiones

### E8 Symmetry (Garrett Lisi)
- 248 dimensiones de simetría
- Proyecciones icosaédricas/dodecaédricas
- Unificación geométrica

### Music of the Spheres (Kepler)
- Órbitas planetarias como intervalos musicales
- Resonancias orbitales reales (ej: Júpiter-Saturno 5:2)
- Armonía cósmica

---

## 🎓 Conclusión

Este sistema añade una **capa conceptual profunda** sin romper nada existente. Es:

- ✅ **Opcional** - Se activa solo cuando el jugador lo descubre
- ✅ **Modular** - Puede deshabilitarse completamente
- ✅ **Educativo** - Basado en física teórica real
- ✅ **Único** - Muy pocas simulaciones hacen esto
- ✅ **Jugable** - Mecánicas claras y recompensas

**¿Listo para integrar?** Sigue los pasos de la sección "Integración Paso a Paso" y estarás funcionando en menos de 1 hora. 🚀

---

**Autor:** Kiro AI  
**Fecha:** 2026-04-12  
**Versión:** 1.0.0
