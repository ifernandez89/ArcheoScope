// Robust GLB Loader with progress tracking
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader'
import type { LoaderProgress, ModelData } from './types'

export class ModelLoader {
  private loader: GLTFLoader
  private dracoLoader: DRACOLoader

  constructor() {
    this.loader = new GLTFLoader()
    this.dracoLoader = new DRACOLoader()
    this.dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/')
    this.loader.setDRACOLoader(this.dracoLoader)
  }

  async load(
    url: string,
    onProgress?: (progress: LoaderProgress) => void
  ): Promise<ModelData> {
    return new Promise((resolve, reject) => {
      this.loader.load(
        url,
        (gltf) => {
          const modelData: ModelData = {
            scene: gltf.scene,
            animations: gltf.animations,
            gltf
          }
          resolve(modelData)
        },
        (xhr) => {
          if (onProgress && xhr.total > 0) {
            const progress: LoaderProgress = {
              loaded: xhr.loaded,
              total: xhr.total,
              percentage: (xhr.loaded / xhr.total) * 100
            }
            onProgress(progress)
          }
        },
        (error) => {
          reject(error)
        }
      )
    })
  }

  dispose() {
    this.dracoLoader.dispose()
  }
}
