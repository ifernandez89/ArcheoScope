# 🎼 Plan: Sistema de Audio + Resonancia Dimensional

**Fecha:** 24 de Febrero 2026  
**Estado:** Planificación  
**Objetivo:** Convertir audio climático en sistema de resonancia dimensional

---

## 🎯 Filosofía del Sistema

### ❌ NO hacer:
- Frecuencias "mágicas" (432 Hz, 528 Hz)
- Sonidos místicos hardcodeados
- Audio que "sana"
- Mezclar matemática con generación sonora

### ✅ SÍ hacer:
- Resonancia como variable matemática `[-1, 1]`
- Modular audio existente
- Separación clara: Matemática → Adapter → Audio
- Audio como subproducto de resonancia

---

## 📊 ETAPA 1: Arreglar lo Crítico (URGENTE)

### 1.1 Fix Memory Leaks

**Problema:**
```typescript
// ❌ MALO - Memory leak
source.start(0)
// No hay cleanup
```

**Solución:**
```typescript
// ✅ BUENO
source.start(0)
source.onended = () => {
  source.disconnect()
  source.buffer = null
}
```

**Archivos a modificar:**
- `viewer3d/systems/ProceduralAudio.ts`
- `viewer3d/systems/LightningSystem.ts`

**Checklist:**
- [ ] Agregar `onended` a todos los `AudioBufferSourceNode`
- [ ] Agregar `disconnect()` en todos los stops
- [ ] Verificar que no queden referencias colgadas

---

### 1.2 Fix Type Safety

**Problema:**
```typescript
// ❌ MALO - Rompe type system
;(this as any).windSource = source
```

**Solución:**
```typescript
// ✅ BUENO - Type safety
private windSource?: AudioBufferSourceNode
private windGain?: GainNode
private windFilter?: BiquadFilterNode
private windLFO?: OscillatorNode
```

**Checklist:**
- [ ] Definir todas las propiedades privadas con tipos correctos
- [ ] Eliminar todos los `(this as any)`
- [ ] Usar optional chaining `?.` donde sea necesario

---

### 1.3 Control de Usuario Obligatorio

**Problema:**
```typescript
// ❌ MALO - AudioContext sin interacción
this.context = new AudioContext()
```

**Solución:**
```typescript
// ✅ BUENO - Requiere interacción
private context?: AudioContext
private enabled: boolean = false

async enable(): Promise<void> {
  if (!this.context) {
    this.context = new AudioContext()
  }
  
  if (this.context.state === 'suspended') {
    await this.context.resume()
  }
  
  this.enabled = true
}
```

**Checklist:**
- [ ] Agregar método `enable()` async
- [ ] Agregar propiedad `enabled`
- [ ] Verificar `enabled` antes de reproducir audio
- [ ] Agregar `resume()` en interacción

---

### 1.4 UI de Control

**Crear:** `viewer3d/components/AudioControl.tsx`

```typescript
interface AudioControlProps {
  onEnable: () => Promise<void>
  enabled: boolean
  masterVolume: number
  onVolumeChange: (volume: number) => void
}

export default function AudioControl({ 
  onEnable, 
  enabled, 
  masterVolume, 
  onVolumeChange 
}: AudioControlProps) {
  return (
    <div style={{ position: 'absolute', top: 20, right: 20 }}>
      {!enabled ? (
        <button onClick={onEnable}>
          🔊 Enable Audio
        </button>
      ) : (
        <div>
          <span>🔊 Audio: ON</span>
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.01"
            value={masterVolume}
            onChange={(e) => onVolumeChange(parseFloat(e.target.value))}
          />
        </div>
      )}
    </div>
  )
}
```

**Checklist:**
- [ ] Crear componente AudioControl
- [ ] Integrar en ImmersiveScene
- [ ] Conectar con ProceduralAudio

---

## 🌌 ETAPA 2: Sistema de Resonancia

### 2.1 Crear ResonanceSystem (Matemático Puro)

**Crear:** `viewer3d/systems/ResonanceSystem.ts`

```typescript
/**
 * ResonanceSystem - Sistema matemático de resonancia dimensional
 * 
 * NO genera audio directamente.
 * Solo calcula valores de resonancia [-1, 1]
 */

export interface ResonanceConfig {
  baseFrequency: number      // Frecuencia base (no Hz literal)
  intensity: number           // Intensidad [0, 1]
  falloff: number            // Caída con distancia
  harmonics: number[]        // Armónicos relativos
}

export interface ResonanceState {
  value: number              // [-1, 1] - Valor principal
  phase: number              // [0, 2π] - Fase actual
  harmonicValues: number[]   // Valores de armónicos
  stability: number          // [0, 1] - Estabilidad
}

class ResonanceSystem {
  private time: number = 0
  private config: ResonanceConfig
  
  constructor(config: ResonanceConfig) {
    this.config = config
  }
  
  /**
   * Actualizar sistema (llamar cada frame)
   */
  update(deltaTime: number): ResonanceState {
    this.time += deltaTime
    
    // Calcular resonancia base
    const phase = (this.time * this.config.baseFrequency) % (Math.PI * 2)
    const baseValue = Math.sin(phase) * this.config.intensity
    
    // Calcular armónicos
    const harmonicValues = this.config.harmonics.map((harmonic, i) => {
      const harmonicPhase = phase * harmonic
      return Math.sin(harmonicPhase) * (this.config.intensity / (i + 2))
    })
    
    // Valor final (base + armónicos)
    const value = baseValue + harmonicValues.reduce((a, b) => a + b, 0)
    const normalizedValue = Math.max(-1, Math.min(1, value))
    
    // Estabilidad (qué tan cerca está de 0)
    const stability = 1 - Math.abs(normalizedValue)
    
    return {
      value: normalizedValue,
      phase,
      harmonicValues,
      stability
    }
  }
  
  /**
   * Calcular resonancia en punto específico
   */
  getResonanceAt(x: number, y: number, z: number): number {
    const distance = Math.sqrt(x * x + y * y + z * z)
    const falloff = Math.exp(-distance * this.config.falloff)
    
    const state = this.update(0)
    return state.value * falloff
  }
  
  /**
   * Verificar si entidad está en resonancia
   */
  isInResonance(entityFreq: number, threshold: number = 0.1): boolean {
    const diff = Math.abs(entityFreq - this.config.baseFrequency)
    return diff < threshold
  }
}

export default ResonanceSystem
```

**Checklist:**
- [ ] Crear ResonanceSystem
- [ ] Implementar update()
- [ ] Implementar getResonanceAt()
- [ ] Implementar isInResonance()
- [ ] NO generar audio aquí

---

### 2.2 Crear ResonanceAudioAdapter

**Crear:** `viewer3d/systems/ResonanceAudioAdapter.ts`

```typescript
/**
 * ResonanceAudioAdapter - Adapta resonancia a parámetros de audio
 * 
 * Recibe: resonance ∈ [-1, 1]
 * Modula: pitch, filtros, stereo, armónicos
 */

import type { ResonanceState } from './ResonanceSystem'

export interface AudioModulation {
  pitchShift: number         // Multiplicador de pitch
  filterFrequency: number    // Frecuencia de filtro
  stereoSpread: number       // Separación estéreo
  harmonicBoost: number      // Boost de armónicos
  noiseReduction: number     // Reducción de ruido
}

export class ResonanceAudioAdapter {
  /**
   * Convertir resonancia a modulación de audio
   */
  static toAudioModulation(resonance: ResonanceState): AudioModulation {
    const { value, stability } = resonance
    
    // Pitch: sube con resonancia positiva, baja con negativa
    const pitchShift = 1 + (value * 0.2)
    
    // Filtro: más abierto con resonancia positiva
    const filterFrequency = 1000 + (value * 500)
    
    // Stereo: más spread con inestabilidad
    const stereoSpread = (1 - stability) * 0.5
    
    // Armónicos: boost con resonancia positiva
    const harmonicBoost = Math.max(0, value)
    
    // Reducción de ruido: más con estabilidad
    const noiseReduction = stability
    
    return {
      pitchShift,
      filterFrequency,
      stereoSpread,
      harmonicBoost,
      noiseReduction
    }
  }
  
  /**
   * Determinar tipo de audio según resonancia
   */
  static getAudioProfile(resonance: ResonanceState): 'harmonic' | 'dissonant' | 'neutral' {
    if (resonance.stability > 0.7) return 'harmonic'
    if (resonance.stability < 0.3) return 'dissonant'
    return 'neutral'
  }
}
```

**Checklist:**
- [ ] Crear ResonanceAudioAdapter
- [ ] Implementar toAudioModulation()
- [ ] Implementar getAudioProfile()
- [ ] NO generar audio aquí tampoco

---

## 🔗 ETAPA 3: Integración

### 3.1 Modificar ProceduralAudio para aceptar modulación

**Agregar a ProceduralAudio:**

```typescript
/**
 * Aplicar modulación de resonancia
 */
applyResonanceModulation(modulation: AudioModulation) {
  if (!this.context || !this.enabled) return
  
  const currentTime = this.context.currentTime
  
  // Modular filtros activos
  if (this.windFilter) {
    this.windFilter.frequency.linearRampToValueAtTime(
      modulation.filterFrequency,
      currentTime + 0.5
    )
  }
  
  if (this.rainFilter) {
    this.rainFilter.frequency.linearRampToValueAtTime(
      modulation.filterFrequency * 2, // Lluvia más aguda
      currentTime + 0.5
    )
  }
  
  // Modular gain según reducción de ruido
  if (this.masterGain) {
    const targetGain = this.baseVolume * (1 - modulation.noiseReduction * 0.3)
    this.masterGain.gain.linearRampToValueAtTime(
      targetGain,
      currentTime + 0.5
    )
  }
}
```

**Checklist:**
- [ ] Agregar método `applyResonanceModulation()`
- [ ] Modular filtros existentes
- [ ] Modular gain master
- [ ] NO agregar nuevos sonidos

---

### 3.2 Integrar en ClimateAudioSystem

**Modificar ClimateAudioSystem:**

```typescript
import ResonanceSystem from './ResonanceSystem'
import { ResonanceAudioAdapter } from './ResonanceAudioAdapter'

class ClimateAudioManager {
  private resonanceSystem?: ResonanceSystem
  
  /**
   * Actualizar con resonancia
   */
  updateWithResonance(deltaTime: number) {
    if (!this.resonanceSystem) return
    
    // Obtener estado de resonancia
    const resonanceState = this.resonanceSystem.update(deltaTime)
    
    // Convertir a modulación de audio
    const modulation = ResonanceAudioAdapter.toAudioModulation(resonanceState)
    
    // Aplicar al audio
    this.audioGenerator.applyResonanceModulation(modulation)
    
    // Log del perfil
    const profile = ResonanceAudioAdapter.getAudioProfile(resonanceState)
    console.log(`🌊 Resonancia: ${resonanceState.value.toFixed(2)}, Perfil: ${profile}`)
  }
}
```

**Checklist:**
- [ ] Agregar ResonanceSystem a ClimateAudioManager
- [ ] Implementar updateWithResonance()
- [ ] Llamar desde loop principal

---

## 🏗️ Arquitectura Final

```
┌─────────────────────────────────────┐
│     ResonanceSystem (Matemático)    │
│  - Calcula resonance [-1, 1]        │
│  - Sin audio                         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   ResonanceAudioAdapter              │
│  - Convierte resonancia → modulación │
│  - Sin audio                         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   ClimateAudioSystem                 │
│  - Recibe modulación                 │
│  - Aplica a audio existente          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   ProceduralAudio (Web Audio API)   │
│  - Genera sonido                     │
│  - Aplica modulación                 │
└─────────────────────────────────────┘
```

---

## 🎮 Resultado Final

### Zona Armónica (resonance > 0.5, stability > 0.7)
- ✅ Ruido blanco reducido
- ✅ Pink noise enfatizado
- ✅ Filtro más abierto
- ✅ Pitch estable
- ✅ Sensación: claridad, alineación

### Zona Disonante (resonance < -0.5, stability < 0.3)
- ✅ Brown noise aumentado
- ✅ LFO irregular
- ✅ Filtro cerrado
- ✅ Micro variación de pitch
- ✅ Sensación: inestabilidad dimensional

### Sin agregar nuevos sonidos
Todo es modulación del audio existente.

---

## 📋 Checklist General

### ETAPA 1: Crítico
- [ ] Fix memory leaks (onended, disconnect)
- [ ] Fix type safety (eliminar `as any`)
- [ ] Agregar control de usuario (enable, resume)
- [ ] Crear UI de control (AudioControl.tsx)
- [ ] Build y test

### ETAPA 2: Resonancia
- [ ] Crear ResonanceSystem.ts
- [ ] Crear ResonanceAudioAdapter.ts
- [ ] Build y test

### ETAPA 3: Integración
- [ ] Modificar ProceduralAudio (applyResonanceModulation)
- [ ] Modificar ClimateAudioSystem (updateWithResonance)
- [ ] Integrar en loop principal
- [ ] Build y test

---

## 🚀 Orden de Implementación

1. **ETAPA 1** - Arreglar crítico (1-2 horas)
2. **Build y test** - Verificar que no hay leaks
3. **ETAPA 2** - Sistema de resonancia (1 hora)
4. **Build y test** - Verificar matemática
5. **ETAPA 3** - Integración (1 hora)
6. **Build y test final** - Verificar todo junto

**Tiempo total estimado:** 3-4 horas

---

**Creado por:** Kiro AI  
**Basado en:** Recomendaciones de arquitectura avanzada  
**Estado:** Listo para implementar
