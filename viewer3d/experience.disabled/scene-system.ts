// Enhanced Scene System for FASE 2
import * as THREE from 'three'
import type { Engine3D } from '@/core/engine'

export interface SceneDefinition {
  id: string
  name: string
  description: string
  models: ModelConfig[]
  camera: CameraConfig
  lighting: LightingConfig
  audio?: AudioConfig
  duration?: number
  autoPlay?: boolean
  onEnter?: () => void
  onExit?: () => void
  onProgress?: (progress: number) => void
}

export interface ModelConfig {
  id: string
  path: string
  position?: THREE.Vector3
  rotation?: THREE.Euler
  scale?: number
  animation?: string
}

export interface CameraConfig {
  position: THREE.Vector3
  target: THREE.Vector3
  fov?: number
  transition?: {
    duration: number
    easing: 'linear' | 'easeIn' | 'easeOut' | 'easeInOut'
  }
}

export interface LightingConfig {
  timeOfDay?: number
  ambient?: { intensity: number; color: string }
  directional?: { intensity: number; position: [number, number, number] }
}

export interface AudioConfig {
  background?: string
  narration?: string
  effects?: string[]
  volume?: number
  loop?: boolean
}

export class SceneSystem {
  private engine: Engine3D
  private scenes: Map<string, SceneDefinition> = new Map()
  private currentScene: string | null = null
  private isTransitioning: boolean = false

  constructor(engine: Engine3D) {
    this.engine = engine
  }

  // Registrar una escena
  registerScene(scene: SceneDefinition) {
    this.scenes.set(scene.id, scene)
    console.log(`📋 Escena registrada: ${scene.name}`)
  }

  // Registrar múltiples escenas
  registerScenes(scenes: SceneDefinition[]) {
    scenes.forEach(scene => this.registerScene(scene))
  }

  // Cargar y activar una escena
  async loadScene(sceneId: string, onProgress?: (progress: number) => void): Promise<void> {
    if (this.isTransitioning) {
      console.warn('⚠️ Transición en progreso, espera...')
      return
    }

    const scene = this.scenes.get(sceneId)
    if (!scene) {
      throw new Error(`❌ Escena no encontrada: ${sceneId}`)
    }

    this.isTransitioning = true

    try {
      // Salir de escena actual
      if (this.currentScene) {
        await this.exitScene(this.currentScene)
      }

      // Cargar modelos
      const totalModels = scene.models.length
      let loadedModels = 0

      for (const modelConfig of scene.models) {
        await this.engine.loadModel(
          modelConfig.id,
          modelConfig.path,
          (progress) => {
            const totalProgress = ((loadedModels + progress / 100) / totalModels) * 100
            if (onProgress) {
              onProgress(totalProgress)
            }
            if (scene.onProgress) {
              scene.onProgress(totalProgress)
            }
          }
        )

        // Aplicar transformaciones
        const model = this.engine.getModel(modelConfig.id)
        if (model) {
          if (modelConfig.position) {
            model.scene.position.copy(modelConfig.position)
          }
          if (modelConfig.rotation) {
            model.scene.rotation.copy(modelConfig.rotation)
          }
          if (modelConfig.scale) {
            model.scene.scale.setScalar(modelConfig.scale)
          }
          if (modelConfig.animation) {
            this.engine.playAnimation(modelConfig.id, 0)
          }
        }

        loadedModels++
      }

      // Configurar cámara
      const duration = scene.camera.transition?.duration || 2000
      this.engine.cameraController.flyTo(
        scene.camera.position,
        scene.camera.target,
        duration
      )

      // Configurar iluminación
      if (scene.lighting.timeOfDay !== undefined) {
        this.engine.lighting.setTimeOfDay(scene.lighting.timeOfDay)
      }

      // Callback onEnter
      if (scene.onEnter) {
        scene.onEnter()
      }

      this.currentScene = sceneId
      console.log(`✅ Escena cargada: ${scene.name}`)

      // Auto-play si está configurado
      if (scene.autoPlay && scene.duration) {
        setTimeout(() => {
          this.nextScene()
        }, scene.duration)
      }

    } finally {
      this.isTransitioning = false
    }
  }

  // Salir de una escena
  private async exitScene(sceneId: string): Promise<void> {
    const scene = this.scenes.get(sceneId)
    if (!scene) return

    // Callback onExit
    if (scene.onExit) {
      scene.onExit()
    }

    // Limpiar modelos de la escena
    scene.models.forEach(modelConfig => {
      this.engine.removeModel(modelConfig.id)
    })

    console.log(`👋 Saliendo de escena: ${scene.name}`)
  }

  // Ir a la siguiente escena
  async nextScene(): Promise<void> {
    if (!this.currentScene) return

    const sceneIds = Array.from(this.scenes.keys())
    const currentIndex = sceneIds.indexOf(this.currentScene)
    const nextIndex = (currentIndex + 1) % sceneIds.length

    await this.loadScene(sceneIds[nextIndex])
  }

  // Ir a la escena anterior
  async previousScene(): Promise<void> {
    if (!this.currentScene) return

    const sceneIds = Array.from(this.scenes.keys())
    const currentIndex = sceneIds.indexOf(this.currentScene)
    const prevIndex = (currentIndex - 1 + sceneIds.length) % sceneIds.length

    await this.loadScene(sceneIds[prevIndex])
  }

  // Obtener escena actual
  getCurrentScene(): SceneDefinition | null {
    if (!this.currentScene) return null
    return this.scenes.get(this.currentScene) || null
  }

  // Obtener todas las escenas
  getAllScenes(): SceneDefinition[] {
    return Array.from(this.scenes.values())
  }

  // Obtener escena por ID
  getScene(sceneId: string): SceneDefinition | undefined {
    return this.scenes.get(sceneId)
  }

  // Verificar si está en transición
  isInTransition(): boolean {
    return this.isTransitioning
  }

  // Limpiar todas las escenas
  clear() {
    this.scenes.clear()
    this.currentScene = null
    this.isTransitioning = false
  }
}
