/**
 * ResonanceAudioAdapter - Adapta resonancia a parámetros de audio
 * 
 * Recibe: resonance ∈ [-1, 1]
 * Modula: pitch, filtros, stereo, armónicos
 * 
 * NO genera audio.
 * Solo convierte valores matemáticos a parámetros de audio.
 */

import type { ResonanceState } from './ResonanceSystem'

export interface AudioModulation {
  pitchShift: number         // Multiplicador de pitch [0.8 - 1.2]
  filterFrequency: number    // Frecuencia de filtro [Hz]
  stereoSpread: number       // Separación estéreo [0 - 1]
  harmonicBoost: number      // Boost de armónicos [0 - 1]
  noiseReduction: number     // Reducción de ruido [0 - 1]
  lfoRate: number            // Velocidad de LFO [Hz]
  reverbMix: number          // Mezcla de reverb [0 - 1]
}

export class ResonanceAudioAdapter {
  /**
   * Convertir resonancia a modulación de audio
   */
  static toAudioModulation(resonance: ResonanceState): AudioModulation {
    const { value, stability, profile } = resonance
    
    // Pitch: sube con resonancia positiva, baja con negativa
    // Rango: 0.8 - 1.2 (±20%)
    const pitchShift = 1 + (value * 0.2)
    
    // Filtro: más abierto con resonancia positiva
    // Rango: 500Hz - 1500Hz
    const filterFrequency = 1000 + (value * 500)
    
    // Stereo: más spread con inestabilidad
    // Rango: 0 - 0.5
    const stereoSpread = (1 - stability) * 0.5
    
    // Armónicos: boost con resonancia positiva
    // Rango: 0 - 1
    const harmonicBoost = Math.max(0, value)
    
    // Reducción de ruido: más con estabilidad
    // Rango: 0 - 0.5
    const noiseReduction = stability * 0.5
    
    // LFO: más rápido con inestabilidad
    // Rango: 0.1Hz - 2Hz
    const lfoRate = 0.1 + (1 - stability) * 1.9
    
    // Reverb: más con estabilidad (sensación de espacio)
    // Rango: 0 - 0.4
    const reverbMix = stability * 0.4
    
    return {
      pitchShift,
      filterFrequency,
      stereoSpread,
      harmonicBoost,
      noiseReduction,
      lfoRate,
      reverbMix
    }
  }
  
  /**
   * Obtener perfil de audio según resonancia
   */
  static getAudioProfile(resonance: ResonanceState): {
    profile: 'harmonic' | 'dissonant' | 'neutral'
    description: string
    effects: string[]
  } {
    const { profile, stability, value } = resonance
    
    switch (profile) {
      case 'harmonic':
        return {
          profile: 'harmonic',
          description: 'Zona armónica - Claridad y alineación',
          effects: [
            'Ruido blanco reducido',
            'Pink noise enfatizado',
            'Filtro más abierto',
            'Pitch estable',
            'Reverb largo'
          ]
        }
      
      case 'dissonant':
        return {
          profile: 'dissonant',
          description: 'Zona disonante - Inestabilidad dimensional',
          effects: [
            'Brown noise aumentado',
            'LFO irregular',
            'Filtro cerrado',
            'Micro variación de pitch',
            'Tremolo leve'
          ]
        }
      
      case 'neutral':
      default:
        return {
          profile: 'neutral',
          description: 'Zona neutral - Estado normal',
          effects: [
            'Balance de ruidos',
            'Filtro moderado',
            'Pitch normal',
            'LFO suave'
          ]
        }
    }
  }
  
  /**
   * Calcular intensidad de efectos según perfil
   */
  static getEffectIntensities(resonance: ResonanceState): {
    whiteNoise: number    // [0 - 1]
    pinkNoise: number     // [0 - 1]
    brownNoise: number    // [0 - 1]
    clarity: number       // [0 - 1]
    distortion: number    // [0 - 1]
  } {
    const { value, stability, profile } = resonance
    
    if (profile === 'harmonic') {
      // Zona armónica: claridad, menos ruido
      return {
        whiteNoise: 0.2,
        pinkNoise: 0.8,
        brownNoise: 0.1,
        clarity: 0.9,
        distortion: 0.1
      }
    } else if (profile === 'dissonant') {
      // Zona disonante: más ruido, menos claridad
      return {
        whiteNoise: 0.4,
        pinkNoise: 0.3,
        brownNoise: 0.8,
        clarity: 0.2,
        distortion: 0.7
      }
    } else {
      // Zona neutral: balance
      return {
        whiteNoise: 0.5,
        pinkNoise: 0.5,
        brownNoise: 0.5,
        clarity: 0.5,
        distortion: 0.3
      }
    }
  }
  
  /**
   * Interpolar suavemente entre dos modulaciones
   */
  static lerp(from: AudioModulation, to: AudioModulation, t: number): AudioModulation {
    const clampedT = Math.max(0, Math.min(1, t))
    
    return {
      pitchShift: from.pitchShift + (to.pitchShift - from.pitchShift) * clampedT,
      filterFrequency: from.filterFrequency + (to.filterFrequency - from.filterFrequency) * clampedT,
      stereoSpread: from.stereoSpread + (to.stereoSpread - from.stereoSpread) * clampedT,
      harmonicBoost: from.harmonicBoost + (to.harmonicBoost - from.harmonicBoost) * clampedT,
      noiseReduction: from.noiseReduction + (to.noiseReduction - from.noiseReduction) * clampedT,
      lfoRate: from.lfoRate + (to.lfoRate - from.lfoRate) * clampedT,
      reverbMix: from.reverbMix + (to.reverbMix - from.reverbMix) * clampedT
    }
  }
}

export default ResonanceAudioAdapter
