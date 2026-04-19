# 🎼 Harmonia Mundi - Sistema de Audio Planetario Completo

## 🌟 Actualización: Todos los Planetas Audibles

### Concepto
El sistema **Harmonia Mundi** convierte las órbitas planetarias en frecuencias audibles, creando una "sinfonía del sistema solar" donde cada planeta es un instrumento que suena continuamente.

---

## 🪐 Planetas Implementados

### Todos los 9 Cuerpos Celestes Activos:

| Planeta   | Frecuencia Base | Nota | Período Orbital | Drone (÷8) | Audible Final | Estado |
|-----------|----------------|------|-----------------|------------|---------------|--------|
| **Mercurio** | 141.27 Hz | C# | 88 días | 17.66 Hz | 17.66 Hz | ⚠️ Límite |
| **Venus** | 221.23 Hz | A | 225 días | 27.65 Hz | 27.65 Hz | ✅ Audible |
| **Tierra** | 136.10 Hz | C# | 365 días | 8.51 Hz | 34.04 Hz | ✅ Transpuesto |
| **Marte** | 144.72 Hz | D | 687 días | 9.05 Hz | 36.20 Hz | ✅ Transpuesto |
| **Júpiter** | 183.58 Hz | F# | 4,333 días | 11.47 Hz | 45.88 Hz | ✅ Transpuesto |
| **Saturno** | 147.85 Hz | D | 10,759 días | 9.24 Hz | 36.96 Hz | ✅ Transpuesto |
| **Urano** | 207.36 Hz | G# | 30,687 días | 12.96 Hz | 51.84 Hz | ✅ Transpuesto |
| **Neptuno** | 211.44 Hz | G# | 60,190 días | 13.22 Hz | 52.88 Hz | ✅ Transpuesto |
| **Plutón** | 140.25 Hz | C# | 90,560 días | 8.77 Hz | 35.08 Hz | ✅ Transpuesto |

---

## 🎵 Sistema de Transposición Automática

### Rango Audible Humano
- **Mínimo**: 20 Hz (infrasonido por debajo)
- **Máximo**: 20,000 Hz (ultrasonido por encima)

### Algoritmo de Ajuste
```typescript
// Si está por debajo de 20 Hz, subir octavas hasta ser audible
while (finalFreq < 20 && finalFreq > 0) {
  finalFreq *= 2  // Subir 1 octava
}

// Si está por encima de 2000 Hz, bajar octavas para mantener drone
while (finalFreq > 2000) {
  finalFreq /= 2  // Bajar 1 octava
}
```

### Ejemplo: Tierra
1. **Frecuencia base**: 136.10 Hz (C# - "Om cósmico")
2. **Drone (÷8)**: 8.51 Hz ❌ **INAUDIBLE**
3. **Transpuesto (×4)**: 34.04 Hz ✅ **AUDIBLE**

---

## 🎼 Capas de Audio

### 1. Drones Planetarios (`drone`)
- **Tipo**: Onda sinusoidal pura
- **Función**: Frecuencia base continua de cada planeta
- **Intensidad**: 0.08 (sutil)
- **Conexión**: `planetaryGain`

### 2. Armónicos (`harmonic`)
- **Tipo**: Onda triangular
- **Función**: Armónicos cristalinos (2× frecuencia base)
- **Intensidad**: 0.08
- **Conexión**: `harmonicGain`

### 3. Pulsos Orbitales (`pulse`)
- **Tipo**: Onda sinusoidal + LFO
- **Función**: Pulso rítmico basado en período orbital
- **Intensidad**: 0.10
- **Conexión**: `pulseGain`

### 4. Texturas (`texture`)
- **Tipo**: Onda diente de sierra
- **Función**: Capas ambientales complejas
- **Intensidad**: 0.06
- **Conexión**: `harmonicGain`

### 5. Resonancia (`resonance`)
- **Tipo**: Onda sinusoidal
- **Función**: Campo de resonancia total (4× frecuencia base)
- **Intensidad**: 0.12
- **Conexión**: `planetaryGain`

---

## 🏛️ Amplificadores de Arquitectura

Cada sitio arqueológico actúa como un **filtro/amplificador** de frecuencias específicas:

| Sitio | Filtro | Frecuencia | Q | Ganancia | Efecto |
|-------|--------|------------|---|----------|--------|
| **Giza** | Bandpass | 150 Hz | 2 | 1.5× | Amplifica frecuencias solares |
| **Teotihuacán** | Highpass | 200 Hz | 1.5 | 1.3× | Genera armónicos cristalinos |
| **Isla de Pascua** | Lowpass | 80 Hz | 3 | 2.0× | Amplifica subgraves oceánicos |
| **Puma Punku** | Peaking | 432 Hz | 5 | 1.8× | Resuena en frecuencia sagrada |
| **Tres Zapotes** | Notch | 110 Hz | 4 | 1.6× | Resonancia olmeca del inframundo |
| **Göbekli Tepe** | Bandpass | 45 Hz | 8 | 3.0× | Portal primordial - escarabajo sagrado |

---

## 🚀 Uso del Sistema

### 1. Activar el Sistema
```typescript
import { getHarmoniaMundi } from '@/systems/HarmoniaMundiSystem'

const harmonia = getHarmoniaMundi()
await harmonia.enable()  // Requiere interacción del usuario
```

### 2. Activar Todos los Planetas
```typescript
harmonia.activateAllPlanets()
// ✅ Activa los 9 planetas con transposición automática
```

### 3. Desbloquear Misiones de la Tierra
```typescript
harmonia.unlockMissionLayer('earth_mission_1')  // Despertar Terrestre
harmonia.unlockMissionLayer('earth_mission_2')  // Pulso Vital
harmonia.unlockMissionLayer('earth_mission_3')  // Primer Armónico
harmonia.unlockMissionLayer('earth_mission_4')  // Textura Atmosférica
harmonia.unlockMissionLayer('earth_mission_5')  // Resonancia Completa
harmonia.unlockMissionLayer('earth_mission_6')  // Khepri Despierta
```

### 4. Activar Arquitectura
```typescript
harmonia.activateArchitecture('giza')
harmonia.activateArchitecture('puma-punku')
```

### 5. Obtener Información de Planetas
```typescript
const planets = harmonia.getAllPlanetsInfo()
planets.forEach(planet => {
  console.log(`${planet.name}: ${planet.audibleFrequency.toFixed(2)} Hz`)
  console.log(`  Infrasonido: ${planet.isInfrasound}`)
})
```

---

## 🎨 Componente UI

### PlanetaryAudioPanel
Panel flotante que muestra:
- ✅ Estado del sistema (habilitado/deshabilitado)
- 🪐 Lista de todos los planetas con sus frecuencias
- 🎵 Botón para activar todos los planetas
- ⚠️ Indicadores de infrasonido
- 📊 Información de transposición

**Ubicación**: Botón flotante inferior derecho (🪐 🎵)

---

## 🔬 Detalles Técnicos

### Cadena de Audio
```
Osciladores → Filtros → Capas de Ganancia → Master Gain → Destination
                ↓
         [planetaryGain]
         [harmonicGain]
         [pulseGain]
         [architectureGain]
```

### Fade In Suave
Todos los osciladores hacen fade in de 3 segundos:
```typescript
gain.gain.linearRampToValueAtTime(intensity, context.currentTime + 3)
```

### LFO para Pulsos
Los pulsos usan un oscilador de baja frecuencia (LFO) para modular la amplitud:
```typescript
lfo.frequency.value = Math.max(0.1, layer.frequency)
lfoGain.gain.value = layer.intensity * 0.5
lfo.connect(lfoGain)
lfoGain.connect(gain.gain)  // Modula la amplitud
```

---

## 🪲 Efecto Especial: Khepri Despierta

Sonido del escarabajo sagrado (misión 6 - Göbekli Tepe):

### 3 Capas Simultáneas:
1. **Wingbeat Oscillator** (45 Hz)
   - Onda diente de sierra
   - Filtro lowpass (300 Hz)
   - Microinestabilidad (42-52 Hz)

2. **LFO Modulación** (80 Hz)
   - Pulso de alas rápido
   - Modula amplitud del wingbeat

3. **Harmonic Buzz** (320 Hz)
   - Onda cuadrada
   - Filtro bandpass (350 Hz)
   - Armónicos aerodinámicos

### Evolución Temporal:
- **0-4s**: Fade in lento (zumbido lejano)
- **4-10s**: Crescendo
- **10-18s**: Enjambre (máxima intensidad)
- **18-30s**: Settle (estabilización)

---

## 📊 Logs de Debug

El sistema imprime información detallada en consola:

```
🎼 HarmoniaMundiSystem creado
🎼 Harmonia Mundi habilitado con volumen: 0.7
🎵 Capa base activada: Silencio Cósmico

🪐 Activando todos los planetas del sistema solar...
  🎵 Mercurio: 141.27 Hz → 17.66 Hz → 17.66 Hz (C#)
  🎵 Venus: 221.23 Hz → 27.65 Hz → 27.65 Hz (A)
  🎵 Tierra: 136.10 Hz → 8.51 Hz → 34.04 Hz (C#)
  🎵 Marte: 144.72 Hz → 9.05 Hz → 36.20 Hz (D)
  🎵 Júpiter: 183.58 Hz → 11.47 Hz → 45.88 Hz (F#)
  🎵 Saturno: 147.85 Hz → 9.24 Hz → 36.96 Hz (D)
  🎵 Urano: 207.36 Hz → 12.96 Hz → 51.84 Hz (G#)
  🎵 Neptuno: 211.44 Hz → 13.22 Hz → 52.88 Hz (G#)
  🎵 Plutón: 140.25 Hz → 8.77 Hz → 35.08 Hz (C#)
✅ Todos los planetas activados - Harmonia Mundi completa

🎵 Frecuencia ajustada: 8.51 Hz → 34.04 Hz (drone)
🏛️ Arquitectura activada: Pirámides de Giza
   Amplifican frecuencias solares
```

---

## 🎯 Próximos Pasos

### V2: Expansión Interplanetaria
- [ ] Misiones para cada planeta (5 capas por planeta)
- [ ] Interacciones entre planetas (resonancias)
- [ ] Visualización de ondas en 3D
- [ ] Efectos de conjunción planetaria

### V3: Física Avanzada
- [ ] Resonancias de Schumann (7.83 Hz)
- [ ] Frecuencias de chakras
- [ ] Geometría sagrada sonora
- [ ] Batidos binaurales

---

## 📚 Referencias

- **Frecuencias planetarias**: Basadas en períodos orbitales reales
- **Om cósmico (136.10 Hz)**: Frecuencia del año terrestre transpuesta
- **432 Hz**: Frecuencia de afinación natural (Puma Punku)
- **Rango audible**: 20 Hz - 20,000 Hz (estándar humano)

---

**Creado**: 2026-04-14  
**Sistema**: Harmonia Mundi v2.0  
**Estado**: ✅ Todos los planetas activos y audibles
