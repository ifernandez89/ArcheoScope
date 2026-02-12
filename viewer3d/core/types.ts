// Core Engine Types
import * as THREE from 'three'
import { GLTF } from 'three/examples/jsm/loaders/GLTFLoader'

export interface LoaderProgress {
  loaded: number
  total: number
  percentage: number
}

export interface CameraMode {
  type: 'orbital' | 'cinematic' | 'first-person'
  position: THREE.Vector3
  target: THREE.Vector3
  fov?: number
}

export interface SceneEvent {
  type: 'click' | 'hover' | 'proximity' | 'custom'
  target?: THREE.Object3D
  position?: THREE.Vector3
  data?: any
}

export interface TimelineEvent {
  time: number
  action: () => void
  name?: string
}

export interface ModelData {
  scene: THREE.Group
  animations: THREE.AnimationClip[]
  mixer?: THREE.AnimationMixer
  gltf: GLTF
}

export interface LightingConfig {
  ambient: { intensity: number; color: string }
  directional: { intensity: number; position: [number, number, number]; castShadow: boolean }
  point?: { intensity: number; position: [number, number, number] }
  spot?: { intensity: number; position: [number, number, number]; angle: number }
  hdri?: string
}
