// Cinematic Transitions
import * as THREE from 'three'
import type { Engine3D } from '@/core/engine'

export interface TransitionConfig {
  duration: number
  easing?: 'linear' | 'easeIn' | 'easeOut' | 'easeInOut'
  onComplete?: () => void
}

export class TransitionManager {
  private engine: Engine3D

  constructor(engine: Engine3D) {
    this.engine = engine
  }

  fadeToBlack(config: TransitionConfig) {
    // This would be implemented with postprocessing
    console.log('Fade to black transition', config)
  }

  cameraFlyTo(
    position: THREE.Vector3,
    target: THREE.Vector3,
    config: TransitionConfig
  ) {
    this.engine.cameraController.flyTo(position, target, config.duration)
    
    if (config.onComplete) {
      setTimeout(config.onComplete, config.duration)
    }
  }

  dollyZoom(targetFOV: number, config: TransitionConfig) {
    const camera = this.engine.cameraController['camera']
    const startFOV = camera.fov
    const startTime = Date.now()

    const animate = () => {
      const elapsed = Date.now() - startTime
      const progress = Math.min(elapsed / config.duration, 1)
      const eased = this.applyEasing(progress, config.easing || 'easeInOut')
      
      camera.fov = startFOV + (targetFOV - startFOV) * eased
      camera.updateProjectionMatrix()

      if (progress < 1) {
        requestAnimationFrame(animate)
      } else if (config.onComplete) {
        config.onComplete()
      }
    }

    animate()
  }

  private applyEasing(t: number, easing: string): number {
    switch (easing) {
      case 'linear':
        return t
      case 'easeIn':
        return t * t
      case 'easeOut':
        return t * (2 - t)
      case 'easeInOut':
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t
      default:
        return t
    }
  }
}
