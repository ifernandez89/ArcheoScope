/**
 * Sistema de Física de Resonancia Dimensional
 * Tipos y interfaces
 */

import * as THREE from 'three'

export type AnomalyType = 'gravity' | 'mass' | 'spatial' | 'temporal'

export interface AnomalyField {
  id: string
  position: THREE.Vector3
  radius: number
  intensity: number
  frequency: number
  type: AnomalyType
  active: boolean
}

export interface ResonanceData {
  value: number
  distance: number
  anomalyId: string
  type: AnomalyType
}

export interface PhysicsConfig {
  gravity: THREE.Vector3
  enableResonance: boolean
  maxAnomalies: number
}

export interface ResonanceEffect {
  massMultiplier: number
  gravityScale: number
  spatialDistortion: number
  temporalDilation: number
}
