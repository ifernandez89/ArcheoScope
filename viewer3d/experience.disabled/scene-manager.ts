// Scene Management System
import * as THREE from 'three'
import type { Engine3D } from '@/core/engine'

export interface SceneConfig {
  name: string
  models: { id: string; url: string; position?: THREE.Vector3 }[]
  camera: { position: THREE.Vector3; target: THREE.Vector3 }
  lighting?: { timeOfDay?: number }
  onEnter?: () => void
  onExit?: () => void
}

export class SceneManager {
  private engine: Engine3D
  private scenes: Map<string, SceneConfig> = new Map()
  private currentScene: string | null = null

  constructor(engine: Engine3D) {
    this.engine = engine
  }

  registerScene(config: SceneConfig) {
    this.scenes.set(config.name, config)
  }

  async loadScene(name: string, onProgress?: (progress: number) => void) {
    const config = this.scenes.get(name)
    if (!config) {
      throw new Error(`Scene "${name}" not found`)
    }

    // Exit current scene
    if (this.currentScene) {
      const currentConfig = this.scenes.get(this.currentScene)
      if (currentConfig?.onExit) {
        currentConfig.onExit()
      }
    }

    // Load models
    const totalModels = config.models.length
    let loadedModels = 0

    for (const modelConfig of config.models) {
      await this.engine.loadModel(
        modelConfig.id,
        modelConfig.url,
        (progress) => {
          const totalProgress = ((loadedModels + progress / 100) / totalModels) * 100
          if (onProgress) {
            onProgress(totalProgress)
          }
        }
      )

      const model = this.engine.getModel(modelConfig.id)
      if (model && modelConfig.position) {
        model.scene.position.copy(modelConfig.position)
      }

      loadedModels++
    }

    // Set camera
    this.engine.cameraController.flyTo(
      config.camera.position,
      config.camera.target,
      2000
    )

    // Set lighting
    if (config.lighting?.timeOfDay !== undefined) {
      this.engine.lighting.setTimeOfDay(config.lighting.timeOfDay)
    }

    // Enter new scene
    if (config.onEnter) {
      config.onEnter()
    }

    this.currentScene = name
  }

  getCurrentScene(): string | null {
    return this.currentScene
  }

  getSceneConfig(name: string): SceneConfig | undefined {
    return this.scenes.get(name)
  }
}
