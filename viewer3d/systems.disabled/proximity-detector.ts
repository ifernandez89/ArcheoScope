// Sistema de detección de proximidad para activación automática del avatar
import * as THREE from 'three'

export interface ProximityConfig {
  activationDistance: number // Distancia para activar interacción
  greetingDistance: number // Distancia para saludo automático
  onEnterProximity?: () => void
  onExitProximity?: () => void
  onGreetingDistance?: () => void
}

export class ProximityDetector {
  private camera: THREE.Camera
  private target: THREE.Object3D
  private config: ProximityConfig
  private isInProximity: boolean = false
  private hasGreeted: boolean = false
  private animationFrameId: number | null = null

  constructor(camera: THREE.Camera, target: THREE.Object3D, config: ProximityConfig) {
    this.camera = camera
    this.target = target
    this.config = {
      activationDistance: 5,
      greetingDistance: 3,
      ...config
    }
  }

  // Iniciar detección
  start(): void {
    if (this.animationFrameId !== null) return

    const check = () => {
      this.checkProximity()
      this.animationFrameId = requestAnimationFrame(check)
    }

    check()
  }

  // Detener detección
  stop(): void {
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId)
      this.animationFrameId = null
    }
  }

  // Verificar proximidad
  private checkProximity(): void {
    const distance = this.getDistance()

    // Verificar entrada a zona de activación
    if (!this.isInProximity && distance <= this.config.activationDistance) {
      this.isInProximity = true
      this.config.onEnterProximity?.()
    }

    // Verificar salida de zona de activación
    if (this.isInProximity && distance > this.config.activationDistance) {
      this.isInProximity = false
      this.hasGreeted = false
      this.config.onExitProximity?.()
    }

    // Verificar distancia de saludo (solo una vez)
    if (this.isInProximity && !this.hasGreeted && distance <= this.config.greetingDistance) {
      this.hasGreeted = true
      this.config.onGreetingDistance?.()
    }
  }

  // Calcular distancia entre cámara y target
  private getDistance(): number {
    const cameraPos = new THREE.Vector3()
    this.camera.getWorldPosition(cameraPos)

    const targetPos = new THREE.Vector3()
    this.target.getWorldPosition(targetPos)

    return cameraPos.distanceTo(targetPos)
  }

  // Obtener distancia actual
  getCurrentDistance(): number {
    return this.getDistance()
  }

  // Verificar si está en proximidad
  isInRange(): boolean {
    return this.isInProximity
  }

  // Reset del estado de saludo
  resetGreeting(): void {
    this.hasGreeted = false
  }
}
