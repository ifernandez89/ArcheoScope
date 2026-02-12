// Advanced Camera System (Orbital + Cinematic)
import * as THREE from 'three'
import type { CameraMode } from './types'

export class CameraController {
  private camera: THREE.PerspectiveCamera
  private currentMode: CameraMode['type'] = 'orbital'
  private targetPosition: THREE.Vector3 = new THREE.Vector3()
  private targetLookAt: THREE.Vector3 = new THREE.Vector3()
  private transitionSpeed: number = 0.05

  constructor(camera: THREE.PerspectiveCamera) {
    this.camera = camera
  }

  setMode(mode: CameraMode, duration: number = 2000) {
    this.currentMode = mode.type
    this.targetPosition.copy(mode.position)
    this.targetLookAt.copy(mode.target)
    
    if (mode.fov) {
      this.animateFOV(mode.fov, duration)
    }
  }

  private animateFOV(targetFOV: number, duration: number) {
    const startFOV = this.camera.fov
    const startTime = Date.now()

    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = this.easeInOutCubic(progress)
      
      this.camera.fov = startFOV + (targetFOV - startFOV) * eased
      this.camera.updateProjectionMatrix()

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    animate()
  }

  update() {
    // Smooth camera transition
    this.camera.position.lerp(this.targetPosition, this.transitionSpeed)
  }

  flyTo(position: THREE.Vector3, target: THREE.Vector3, duration: number = 2000) {
    this.targetPosition.copy(position)
    this.targetLookAt.copy(target)
    
    const startPos = this.camera.position.clone()
    const startTime = Date.now()

    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = this.easeInOutCubic(progress)
      
      this.camera.position.lerpVectors(startPos, position, eased)
      this.camera.lookAt(target)

      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }

    animate()
  }

  private easeInOutCubic(t: number): number {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
  }

  getCurrentMode() {
    return this.currentMode
  }
}
