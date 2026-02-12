// Reactive Behavior System for FASE 3
// Models react to user proximity, gaze, and interactions

import * as THREE from 'three'
import type { Engine3D } from '@/core/engine'

export interface BehaviorConfig {
  proximityRadius: number
  gazeRadius: number
  reactionSpeed: number
  enableLookAt: boolean
  enableGestures: boolean
  enableEmotions: boolean
}

export interface BehaviorEvent {
  type: 'proximity' | 'gaze' | 'click' | 'hover'
  distance?: number
  position?: THREE.Vector3
  target?: THREE.Object3D
}

export type BehaviorCallback = (event: BehaviorEvent) => void

export class ReactiveBehavior {
  private engine: Engine3D
  private config: BehaviorConfig
  private callbacks: Map<string, BehaviorCallback[]> = new Map()
  private isActive: boolean = false
  private animationFrameId: number | null = null

  // Estado interno
  private lastProximityState: boolean = false
  private lastGazeState: boolean = false

  constructor(engine: Engine3D, config?: Partial<BehaviorConfig>) {
    this.engine = engine
    this.config = {
      proximityRadius: 5.0,
      gazeRadius: 2.0,
      reactionSpeed: 1.0,
      enableLookAt: true,
      enableGestures: true,
      enableEmotions: true,
      ...config
    }
  }

  // Iniciar sistema reactivo
  start(): void {
    if (this.isActive) return

    this.isActive = true
    this.update()
    console.log('🤖 Reactive Behavior started')
  }

  // Detener sistema reactivo
  stop(): void {
    this.isActive = false
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId)
      this.animationFrameId = null
    }
    console.log('🤖 Reactive Behavior stopped')
  }

  // Loop de actualización
  private update = (): void => {
    if (!this.isActive) return

    // Detectar proximidad
    this.checkProximity()

    // Detectar gaze (mirada)
    this.checkGaze()

    // Continuar loop
    this.animationFrameId = requestAnimationFrame(this.update)
  }

  // Detectar proximidad del usuario
  private checkProximity(): void {
    const camera = this.engine.getCamera()
    const models = this.engine.getAllModels()

    models.forEach(model => {
      const distance = camera.position.distanceTo(model.scene.position)
      const isNear = distance < this.config.proximityRadius

      // Trigger evento si cambió el estado
      if (isNear !== this.lastProximityState) {
        this.trigger('proximity', {
          type: 'proximity',
          distance,
          position: model.scene.position.clone(),
          target: model.scene
        })

        // Look at camera si está cerca
        if (isNear && this.config.enableLookAt) {
          this.lookAtCamera(model.scene)
        }

        this.lastProximityState = isNear
      }
    })
  }

  // Detectar gaze (mirada hacia el modelo)
  private checkGaze(): void {
    const camera = this.engine.getCamera()
    const models = this.engine.getAllModels()

    // Crear raycaster desde la cámara
    const raycaster = new THREE.Raycaster()
    raycaster.setFromCamera(new THREE.Vector2(0, 0), camera)

    models.forEach(model => {
      const intersects = raycaster.intersectObject(model.scene, true)
      const isGazing = intersects.length > 0 && intersects[0].distance < this.config.gazeRadius

      // Trigger evento si cambió el estado
      if (isGazing !== this.lastGazeState) {
        this.trigger('gaze', {
          type: 'gaze',
          distance: intersects[0]?.distance,
          position: intersects[0]?.point,
          target: model.scene
        })

        this.lastGazeState = isGazing
      }
    })
  }

  // Hacer que el modelo mire a la cámara
  private lookAtCamera(model: THREE.Object3D): void {
    const camera = this.engine.getCamera()
    
    // Smooth look at con interpolación
    const targetQuaternion = new THREE.Quaternion()
    const lookAtMatrix = new THREE.Matrix4()
    lookAtMatrix.lookAt(model.position, camera.position, new THREE.Vector3(0, 1, 0))
    targetQuaternion.setFromRotationMatrix(lookAtMatrix)

    // Interpolar suavemente
    model.quaternion.slerp(targetQuaternion, 0.05 * this.config.reactionSpeed)
  }

  // Registrar callback para evento
  on(eventType: BehaviorEvent['type'], callback: BehaviorCallback): void {
    if (!this.callbacks.has(eventType)) {
      this.callbacks.set(eventType, [])
    }
    this.callbacks.get(eventType)!.push(callback)
  }

  // Remover callback
  off(eventType: BehaviorEvent['type'], callback: BehaviorCallback): void {
    const callbacks = this.callbacks.get(eventType)
    if (callbacks) {
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  // Trigger evento
  private trigger(eventType: BehaviorEvent['type'], event: BehaviorEvent): void {
    const callbacks = this.callbacks.get(eventType)
    if (callbacks) {
      callbacks.forEach(callback => callback(event))
    }
  }

  // Configurar comportamiento
  setConfig(config: Partial<BehaviorConfig>): void {
    this.config = { ...this.config, ...config }
  }

  // Obtener configuración
  getConfig(): BehaviorConfig {
    return { ...this.config }
  }

  // Verificar si está activo
  isRunning(): boolean {
    return this.isActive
  }

  // Limpiar recursos
  dispose(): void {
    this.stop()
    this.callbacks.clear()
  }
}

// Proximity Detector standalone
export class ProximityDetector {
  private threshold: number
  private onEnter?: (distance: number) => void
  private onExit?: (distance: number) => void
  private isInside: boolean = false

  constructor(threshold: number = 5.0) {
    this.threshold = threshold
  }

  // Actualizar detección
  update(distance: number): void {
    const wasInside = this.isInside
    this.isInside = distance < this.threshold

    // Trigger callbacks
    if (this.isInside && !wasInside && this.onEnter) {
      this.onEnter(distance)
    } else if (!this.isInside && wasInside && this.onExit) {
      this.onExit(distance)
    }
  }

  // Registrar callbacks
  setOnEnter(callback: (distance: number) => void): void {
    this.onEnter = callback
  }

  setOnExit(callback: (distance: number) => void): void {
    this.onExit = callback
  }

  // Setters
  setThreshold(threshold: number): void {
    this.threshold = threshold
  }

  // Getters
  getThreshold(): number {
    return this.threshold
  }

  isInsideRadius(): boolean {
    return this.isInside
  }
}

// Gaze Tracker standalone
export class GazeTracker {
  private camera: THREE.Camera
  private raycaster: THREE.Raycaster
  private onGazeEnter?: (object: THREE.Object3D) => void
  private onGazeExit?: (object: THREE.Object3D) => void
  private currentTarget: THREE.Object3D | null = null

  constructor(camera: THREE.Camera) {
    this.camera = camera
    this.raycaster = new THREE.Raycaster()
  }

  // Actualizar tracking
  update(objects: THREE.Object3D[]): void {
    // Raycast desde el centro de la pantalla
    this.raycaster.setFromCamera(new THREE.Vector2(0, 0), this.camera)

    // Buscar intersecciones
    const intersects = this.raycaster.intersectObjects(objects, true)
    const newTarget = intersects.length > 0 ? intersects[0].object : null

    // Detectar cambios
    if (newTarget !== this.currentTarget) {
      // Exit anterior
      if (this.currentTarget && this.onGazeExit) {
        this.onGazeExit(this.currentTarget)
      }

      // Enter nuevo
      if (newTarget && this.onGazeEnter) {
        this.onGazeEnter(newTarget)
      }

      this.currentTarget = newTarget
    }
  }

  // Registrar callbacks
  setOnGazeEnter(callback: (object: THREE.Object3D) => void): void {
    this.onGazeEnter = callback
  }

  setOnGazeExit(callback: (object: THREE.Object3D) => void): void {
    this.onGazeExit = callback
  }

  // Getters
  getCurrentTarget(): THREE.Object3D | null {
    return this.currentTarget
  }

  isGazing(): boolean {
    return this.currentTarget !== null
  }
}
