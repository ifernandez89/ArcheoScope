// Avatar Body - Control físico del avatar (animaciones, expresiones, presencia)
// Separa el control físico de la lógica cognitiva

import * as THREE from 'three'
import { AIAnimator } from './animator'
import { ExpressionSystem, FacialAnimator } from './expression-system'
import type { AvatarResponse } from './avatar-brain'
import type { Emotion } from './expression-system'

export interface PresenceConfig {
  enableBreathing: boolean
  enableBlinking: boolean
  enableGaze: boolean
  enableSubtleMovement: boolean
  breathingIntensity: number // 0-1
  blinkFrequency: number // segundos entre parpadeos
}

export class AvatarBody {
  private model: THREE.Object3D
  private animator: AIAnimator
  private expressions: ExpressionSystem
  private facialAnimator: FacialAnimator
  private presenceConfig: PresenceConfig
  
  // Estado de presencia
  private isBreathing: boolean = false
  private isBlinking: boolean = false
  private breathingPhase: number = 0
  private lastBlinkTime: number = 0
  private gazeTarget: THREE.Vector3 | null = null
  
  // Timers
  private breathingInterval: number | null = null
  private blinkingInterval: number | null = null
  private subtleMovementInterval: number | null = null

  constructor(
    model: THREE.Object3D,
    animator: AIAnimator,
    expressions: ExpressionSystem,
    config?: Partial<PresenceConfig>
  ) {
    this.model = model
    this.animator = animator
    this.expressions = expressions
    this.facialAnimator = new FacialAnimator()
    
    this.presenceConfig = {
      enableBreathing: true,
      enableBlinking: true,
      enableGaze: true,
      enableSubtleMovement: true,
      breathingIntensity: 0.02,
      blinkFrequency: 4, // cada 4 segundos
      ...config
    }
  }

  // Iniciar presencia (respiración, parpadeo, etc.)
  startPresence(): void {
    if (this.presenceConfig.enableBreathing) {
      this.startBreathing()
    }
    
    if (this.presenceConfig.enableBlinking) {
      this.startBlinking()
    }
    
    if (this.presenceConfig.enableSubtleMovement) {
      this.startSubtleMovement()
    }
    
    console.log('👁️ Presencia del avatar activada')
  }

  // Detener presencia
  stopPresence(): void {
    this.stopBreathing()
    this.stopBlinking()
    this.stopSubtleMovement()
    console.log('👁️ Presencia del avatar desactivada')
  }

  // Respiración sutil
  private startBreathing(): void {
    if (this.isBreathing) return
    
    this.isBreathing = true
    
    const breathe = () => {
      if (!this.isBreathing) return
      
      this.breathingPhase += 0.02
      const breathOffset = Math.sin(this.breathingPhase) * this.presenceConfig.breathingIntensity
      
      // Aplicar movimiento sutil al torso/cuerpo
      this.model.traverse((child) => {
        if (child.name.includes('body') || child.name.includes('torso')) {
          child.position.y += breathOffset * 0.1
        }
      })
      
      this.breathingInterval = requestAnimationFrame(breathe) as unknown as number
    }
    
    breathe()
  }

  private stopBreathing(): void {
    this.isBreathing = false
    if (this.breathingInterval !== null) {
      cancelAnimationFrame(this.breathingInterval)
      this.breathingInterval = null
    }
  }

  // Parpadeo automático
  private startBlinking(): void {
    if (this.isBlinking) return
    
    this.isBlinking = true
    this.lastBlinkTime = Date.now()
    
    const checkBlink = () => {
      if (!this.isBlinking) return
      
      const now = Date.now()
      const timeSinceLastBlink = (now - this.lastBlinkTime) / 1000
      
      // Parpadeo aleatorio dentro del rango
      const shouldBlink = timeSinceLastBlink > this.presenceConfig.blinkFrequency + (Math.random() * 2 - 1)
      
      if (shouldBlink) {
        this.expressions.blink(this.model, 150)
        this.lastBlinkTime = now
      }
      
      this.blinkingInterval = setTimeout(checkBlink, 100) as unknown as number
    }
    
    checkBlink()
  }

  private stopBlinking(): void {
    this.isBlinking = false
    if (this.blinkingInterval !== null) {
      clearTimeout(this.blinkingInterval)
      this.blinkingInterval = null
    }
  }

  // Movimiento sutil de cabeza
  private startSubtleMovement(): void {
    let phase = 0
    
    const move = () => {
      if (!this.presenceConfig.enableSubtleMovement) return
      
      phase += 0.005
      
      // Movimiento muy sutil en múltiples ejes
      const rotX = Math.sin(phase * 0.7) * 0.01
      const rotY = Math.sin(phase * 0.5) * 0.015
      const rotZ = Math.sin(phase * 0.9) * 0.008
      
      this.model.rotation.x += rotX * 0.1
      this.model.rotation.y += rotY * 0.1
      this.model.rotation.z += rotZ * 0.1
      
      this.subtleMovementInterval = requestAnimationFrame(move) as unknown as number
    }
    
    move()
  }

  private stopSubtleMovement(): void {
    if (this.subtleMovementInterval !== null) {
      cancelAnimationFrame(this.subtleMovementInterval)
      this.subtleMovementInterval = null
    }
  }

  // Ejecutar respuesta del avatar (animación + emoción)
  async executeResponse(response: AvatarResponse): Promise<void> {
    // 1. Fase de pensamiento (inclinación leve)
    await this.thinkingPhase(response.thinkingTime)
    
    // 2. Cambiar expresión
    this.expressions.setEmotion(response.emotion, 500)
    
    // 3. Ejecutar gesto
    await this.executeGesture(response.gesture, response.intensity)
    
    // 4. Volver a idle
    await this.returnToIdle()
  }

  // Fase de pensamiento (antes de responder)
  private async thinkingPhase(duration: number): Promise<void> {
    // Inclinación leve de cabeza
    const tiltClip = this.animator.generateAnimation({
      model: this.model,
      action: 'nod',
      style: 'subtle',
      duration: 800,
      loop: false
    })
    
    this.animator.playAnimation(this.model, tiltClip, false)
    
    // Cambiar a expresión contemplativa
    this.expressions.setEmotion('curious', 300)
    
    // Esperar tiempo de pensamiento
    await new Promise(resolve => setTimeout(resolve, duration))
  }

  // Ejecutar gesto específico
  private async executeGesture(
    gesture: AvatarResponse['gesture'],
    intensity: number
  ): Promise<void> {
    const style = intensity > 0.7 ? 'normal' : 'subtle'
    const duration = 1500
    
    let action: 'nod' | 'wave' | 'turn' | 'idle' = 'idle'
    
    switch (gesture) {
      case 'nod':
        action = 'nod'
        break
      case 'shake':
        // Shake es como nod pero invertido (simplificado)
        action = 'nod'
        break
      case 'tilt':
        action = 'turn'
        break
      case 'turn':
        action = 'turn'
        break
      case 'wave':
        action = 'wave'
        break
      default:
        action = 'idle'
    }
    
    if (action !== 'idle') {
      const clip = this.animator.generateAnimation({
        model: this.model,
        action,
        style,
        duration,
        loop: false
      })
      
      this.animator.playAnimation(this.model, clip, false)
      await new Promise(resolve => setTimeout(resolve, duration))
    }
  }

  // Volver a idle
  private async returnToIdle(): Promise<void> {
    const idleClip = this.animator.generateAnimation({
      model: this.model,
      action: 'idle',
      style: 'subtle',
      duration: 3000,
      loop: true
    })
    
    this.animator.playAnimation(this.model, idleClip, true)
    
    // Volver a expresión neutral gradualmente
    setTimeout(() => {
      this.expressions.setEmotion('neutral', 1000)
    }, 2000)
  }

  // Mirar hacia un objetivo (cámara, punto, etc.)
  lookAt(target: THREE.Vector3, smooth: boolean = true): void {
    if (!this.presenceConfig.enableGaze) return
    
    this.gazeTarget = target.clone()
    
    if (smooth) {
      // Interpolación suave
      const currentRotation = this.model.quaternion.clone()
      this.model.lookAt(target)
      const targetRotation = this.model.quaternion.clone()
      this.model.quaternion.copy(currentRotation)
      
      // Animar hacia target
      const duration = 1000
      const startTime = Date.now()
      
      const animate = () => {
        const elapsed = Date.now() - startTime
        const progress = Math.min(elapsed / duration, 1)
        
        this.model.quaternion.slerp(targetRotation, progress * 0.1)
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        }
      }
      
      animate()
    } else {
      this.model.lookAt(target)
    }
  }

  // Mirar a la cámara
  lookAtCamera(camera: THREE.Camera): void {
    this.lookAt(camera.position, true)
  }

  // Actualizar (llamar en loop de render)
  update(deltaTime: number): void {
    // Actualizar animator
    this.animator.update(deltaTime)
    
    // Actualizar expresiones
    this.expressions.update(this.model)
    this.facialAnimator.update(this.model)
    
    // Si hay gaze target, mantener mirada
    if (this.gazeTarget && this.presenceConfig.enableGaze) {
      // Actualización continua de mirada (muy sutil)
      const targetQuat = new THREE.Quaternion()
      const lookAtMatrix = new THREE.Matrix4()
      lookAtMatrix.lookAt(this.model.position, this.gazeTarget, new THREE.Vector3(0, 1, 0))
      targetQuat.setFromRotationMatrix(lookAtMatrix)
      
      this.model.quaternion.slerp(targetQuat, 0.02)
    }
  }

  // Configurar presencia
  setPresenceConfig(config: Partial<PresenceConfig>): void {
    this.presenceConfig = { ...this.presenceConfig, ...config }
    
    // Reiniciar presencia con nueva config
    this.stopPresence()
    this.startPresence()
  }

  // Getters
  getModel(): THREE.Object3D {
    return this.model
  }

  getAnimator(): AIAnimator {
    return this.animator
  }

  getExpressions(): ExpressionSystem {
    return this.expressions
  }

  isPresenceActive(): boolean {
    return this.isBreathing || this.isBlinking
  }

  // Dispose
  dispose(): void {
    this.stopPresence()
    this.animator.dispose()
  }
}

// Sistema de mirada inteligente
export class IntelligentGaze {
  private body: AvatarBody
  private camera: THREE.Camera
  private isActive: boolean = false
  private updateInterval: number | null = null

  constructor(body: AvatarBody, camera: THREE.Camera) {
    this.body = body
    this.camera = camera
  }

  // Activar mirada inteligente
  start(): void {
    if (this.isActive) return
    
    this.isActive = true
    
    const update = () => {
      if (!this.isActive) return
      
      // Mirar a la cámara con variación aleatoria
      const cameraPos = this.camera.position.clone()
      
      // Agregar variación sutil para naturalidad
      cameraPos.x += (Math.random() - 0.5) * 0.2
      cameraPos.y += (Math.random() - 0.5) * 0.2
      
      this.body.lookAt(cameraPos, true)
      
      this.updateInterval = setTimeout(update, 2000 + Math.random() * 3000) as unknown as number
    }
    
    update()
  }

  // Detener mirada
  stop(): void {
    this.isActive = false
    if (this.updateInterval !== null) {
      clearTimeout(this.updateInterval)
      this.updateInterval = null
    }
  }

  isGazing(): boolean {
    return this.isActive
  }
}
