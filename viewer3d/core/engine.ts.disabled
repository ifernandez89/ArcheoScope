// Core Engine - Runtime Principal
import * as THREE from 'three'
import { ModelLoader } from './loader'
import { CameraController } from './camera'
import { LightingSystem } from './lighting'
import { EventSystem } from './events'
import { Timeline } from './timeline'
import type { ModelData, LightingConfig, CameraMode } from './types'

export class Engine3D {
  private scene: THREE.Scene
  private camera: THREE.PerspectiveCamera
  private renderer: THREE.WebGLRenderer | null = null
  
  public loader: ModelLoader
  public cameraController: CameraController
  public lighting: LightingSystem
  public events: EventSystem
  public timeline: Timeline
  
  private models: Map<string, ModelData> = new Map()
  private animationMixers: THREE.AnimationMixer[] = []
  private clock: THREE.Clock = new THREE.Clock()

  constructor(
    scene: THREE.Scene,
    camera: THREE.PerspectiveCamera,
    lightingConfig: LightingConfig
  ) {
    this.scene = scene
    this.camera = camera
    
    // Initialize subsystems
    this.loader = new ModelLoader()
    this.cameraController = new CameraController(camera)
    this.lighting = new LightingSystem(scene, lightingConfig)
    this.events = new EventSystem()
    this.timeline = new Timeline()
  }

  async loadModel(id: string, url: string, onProgress?: (progress: number) => void): Promise<ModelData> {
    const modelData = await this.loader.load(url, (progress) => {
      if (onProgress) {
        onProgress(progress.percentage)
      }
    })

    // Setup animation mixer
    if (modelData.animations.length > 0) {
      const mixer = new THREE.AnimationMixer(modelData.scene)
      modelData.mixer = mixer
      this.animationMixers.push(mixer)
    }

    this.models.set(id, modelData)
    this.scene.add(modelData.scene)

    return modelData
  }

  getModel(id: string): ModelData | undefined {
    return this.models.get(id)
  }

  removeModel(id: string) {
    const model = this.models.get(id)
    if (model) {
      this.scene.remove(model.scene)
      
      if (model.mixer) {
        const index = this.animationMixers.indexOf(model.mixer)
        if (index > -1) {
          this.animationMixers.splice(index, 1)
        }
      }
      
      this.models.delete(id)
    }
  }

  playAnimation(modelId: string, animationIndex: number = 0) {
    const model = this.models.get(modelId)
    if (model && model.mixer && model.animations[animationIndex]) {
      const action = model.mixer.clipAction(model.animations[animationIndex])
      action.play()
      return action
    }
    return null
  }

  setCameraMode(mode: CameraMode, duration?: number) {
    this.cameraController.setMode(mode, duration)
  }

  update() {
    const delta = this.clock.getDelta()
    
    // Update animation mixers
    this.animationMixers.forEach(mixer => mixer.update(delta))
    
    // Update camera
    this.cameraController.update()
  }

  dispose() {
    this.loader.dispose()
    this.lighting.dispose()
    this.timeline.clear()
    
    this.models.forEach(model => {
      this.scene.remove(model.scene)
    })
    
    this.models.clear()
    this.animationMixers = []
  }
}
