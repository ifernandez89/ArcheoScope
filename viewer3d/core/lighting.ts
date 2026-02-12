// Dynamic Lighting System
import * as THREE from 'three'
import type { LightingConfig } from './types'

export class LightingSystem {
  private scene: THREE.Scene
  private lights: Map<string, THREE.Light> = new Map()
  private config: LightingConfig

  constructor(scene: THREE.Scene, config: LightingConfig) {
    this.scene = scene
    this.config = config
    this.initialize()
  }

  private initialize() {
    // Ambient light
    const ambient = new THREE.AmbientLight(
      this.config.ambient.color,
      this.config.ambient.intensity
    )
    this.lights.set('ambient', ambient)
    this.scene.add(ambient)

    // Directional light (sun)
    const directional = new THREE.DirectionalLight(0xffffff, this.config.directional.intensity)
    directional.position.set(...this.config.directional.position)
    
    if (this.config.directional.castShadow) {
      directional.castShadow = true
      directional.shadow.mapSize.width = 2048
      directional.shadow.mapSize.height = 2048
      directional.shadow.camera.near = 0.5
      directional.shadow.camera.far = 500
    }
    
    this.lights.set('directional', directional)
    this.scene.add(directional)

    // Point light (optional)
    if (this.config.point) {
      const point = new THREE.PointLight(0xffffff, this.config.point.intensity)
      point.position.set(...this.config.point.position)
      this.lights.set('point', point)
      this.scene.add(point)
    }

    // Spot light (optional)
    if (this.config.spot) {
      const spot = new THREE.SpotLight(0xffffff, this.config.spot.intensity)
      spot.position.set(...this.config.spot.position)
      spot.angle = this.config.spot.angle
      spot.penumbra = 1
      spot.castShadow = true
      this.lights.set('spot', spot)
      this.scene.add(spot)
    }
  }

  updateDirectionalLight(position: THREE.Vector3, intensity?: number) {
    const light = this.lights.get('directional') as THREE.DirectionalLight
    if (light) {
      light.position.copy(position)
      if (intensity !== undefined) {
        light.intensity = intensity
      }
    }
  }

  setTimeOfDay(hour: number) {
    // Simulate sun position based on time (0-24)
    const angle = (hour / 24) * Math.PI * 2 - Math.PI / 2
    const height = Math.sin(angle) * 10
    const distance = Math.cos(angle) * 10
    
    const position = new THREE.Vector3(distance, Math.max(height, -2), 5)
    const intensity = Math.max(0.2, Math.sin(angle))
    
    this.updateDirectionalLight(position, intensity)
  }

  getLight(name: string): THREE.Light | undefined {
    return this.lights.get(name)
  }

  dispose() {
    this.lights.forEach(light => {
      this.scene.remove(light)
      light.dispose()
    })
    this.lights.clear()
  }
}
