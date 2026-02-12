// Expression System - Micro-expresiones y emociones
// Sistema de expresiones faciales y emociones para modelos 3D

import * as THREE from 'three'

export type Emotion = 
  | 'neutral' 
  | 'happy' 
  | 'sad' 
  | 'angry' 
  | 'surprised' 
  | 'curious' 
  | 'confused'
  | 'excited'

export interface ExpressionConfig {
  emotion: Emotion
  intensity: number // 0-1
  duration: number // ms
  easing?: 'linear' | 'easeIn' | 'easeOut' | 'easeInOut'
}

export interface MorphTarget {
  name: string
  influence: number
}

export class ExpressionSystem {
  private currentEmotion: Emotion = 'neutral'
  private targetEmotion: Emotion = 'neutral'
  private transitionProgress: number = 1.0
  private transitionDuration: number = 500
  private lastUpdateTime: number = Date.now()

  // Mapeo de emociones a morph targets
  private emotionMorphs: Map<Emotion, MorphTarget[]> = new Map([
    ['neutral', [
      { name: 'browInnerUp', influence: 0 },
      { name: 'mouthSmile', influence: 0 },
      { name: 'eyeWide', influence: 0 }
    ]],
    ['happy', [
      { name: 'mouthSmile', influence: 0.8 },
      { name: 'eyeSquint', influence: 0.3 },
      { name: 'cheekPuff', influence: 0.2 }
    ]],
    ['sad', [
      { name: 'browInnerUp', influence: 0.6 },
      { name: 'mouthFrown', influence: 0.7 },
      { name: 'eyeSquint', influence: 0.2 }
    ]],
    ['angry', [
      { name: 'browDown', influence: 0.8 },
      { name: 'mouthFrown', influence: 0.5 },
      { name: 'eyeSquint', influence: 0.6 }
    ]],
    ['surprised', [
      { name: 'browInnerUp', influence: 0.9 },
      { name: 'eyeWide', influence: 0.9 },
      { name: 'mouthOpen', influence: 0.6 }
    ]],
    ['curious', [
      { name: 'browInnerUp', influence: 0.4 },
      { name: 'eyeWide', influence: 0.3 },
      { name: 'headTilt', influence: 0.2 }
    ]],
    ['confused', [
      { name: 'browInnerUp', influence: 0.5 },
      { name: 'browDown', influence: 0.3 },
      { name: 'mouthFrown', influence: 0.2 }
    ]],
    ['excited', [
      { name: 'mouthSmile', influence: 0.9 },
      { name: 'eyeWide', influence: 0.7 },
      { name: 'browInnerUp', influence: 0.4 }
    ]]
  ])

  // Establecer emoción
  setEmotion(emotion: Emotion, duration: number = 500): void {
    if (emotion === this.targetEmotion) return

    this.currentEmotion = this.targetEmotion
    this.targetEmotion = emotion
    this.transitionProgress = 0
    this.transitionDuration = duration
    this.lastUpdateTime = Date.now()

    console.log(`😊 Transición a emoción: ${emotion}`)
  }

  // Actualizar expresión (llamar en loop de animación)
  update(model: THREE.Object3D): void {
    if (this.transitionProgress >= 1.0) return

    const now = Date.now()
    const deltaTime = now - this.lastUpdateTime
    this.lastUpdateTime = now

    // Actualizar progreso
    this.transitionProgress += deltaTime / this.transitionDuration
    this.transitionProgress = Math.min(this.transitionProgress, 1.0)

    // Aplicar transición
    const t = this.easeInOutCubic(this.transitionProgress)
    this.applyExpression(model, t)
  }

  // Aplicar expresión al modelo
  private applyExpression(model: THREE.Object3D, t: number): void {
    const currentMorphs = this.emotionMorphs.get(this.currentEmotion) || []
    const targetMorphs = this.emotionMorphs.get(this.targetEmotion) || []

    // Interpolar entre emociones
    model.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        if (mesh.morphTargetInfluences && mesh.morphTargetDictionary) {
          // Aplicar morphs interpolados
          this.interpolateMorphs(mesh, currentMorphs, targetMorphs, t)
        }
      }
    })
  }

  // Interpolar morph targets
  private interpolateMorphs(
    mesh: THREE.Mesh,
    from: MorphTarget[],
    to: MorphTarget[],
    t: number
  ): void {
    const dict = mesh.morphTargetDictionary!
    const influences = mesh.morphTargetInfluences!

    // Reset all influences
    for (let i = 0; i < influences.length; i++) {
      influences[i] = 0
    }

    // Interpolar desde emoción actual
    from.forEach(morph => {
      const index = dict[morph.name]
      if (index !== undefined) {
        influences[index] = morph.influence * (1 - t)
      }
    })

    // Interpolar hacia emoción objetivo
    to.forEach(morph => {
      const index = dict[morph.name]
      if (index !== undefined) {
        influences[index] = (influences[index] || 0) + morph.influence * t
      }
    })
  }

  // Parpadeo aleatorio
  blink(model: THREE.Object3D, duration: number = 150): void {
    model.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        if (mesh.morphTargetInfluences && mesh.morphTargetDictionary) {
          const blinkIndex = mesh.morphTargetDictionary['eyeBlink']
          if (blinkIndex !== undefined) {
            // Cerrar ojos
            mesh.morphTargetInfluences[blinkIndex] = 1.0

            // Abrir después de duration
            setTimeout(() => {
              mesh.morphTargetInfluences![blinkIndex] = 0
            }, duration)
          }
        }
      }
    })
  }

  // Parpadeo automático aleatorio
  startAutoBlink(model: THREE.Object3D): number {
    const blinkInterval = () => {
      this.blink(model)
      // Siguiente parpadeo en 2-6 segundos
      const nextBlink = 2000 + Math.random() * 4000
      return setTimeout(blinkInterval, nextBlink)
    }

    return blinkInterval() as unknown as number
  }

  // Detener parpadeo automático
  stopAutoBlink(intervalId: number): void {
    clearTimeout(intervalId)
  }

  // Movimiento sutil de cabeza
  subtleHeadMovement(model: THREE.Object3D, intensity: number = 0.02): void {
    const time = Date.now() * 0.001
    
    // Movimiento sutil en múltiples ejes
    const rotX = Math.sin(time * 0.5) * intensity
    const rotY = Math.sin(time * 0.3) * intensity * 1.5
    const rotZ = Math.sin(time * 0.7) * intensity * 0.5

    model.rotation.x += rotX * 0.1
    model.rotation.y += rotY * 0.1
    model.rotation.z += rotZ * 0.1
  }

  // Obtener emoción actual
  getCurrentEmotion(): Emotion {
    return this.transitionProgress >= 1.0 ? this.targetEmotion : this.currentEmotion
  }

  // Obtener emoción objetivo
  getTargetEmotion(): Emotion {
    return this.targetEmotion
  }

  // Verificar si está en transición
  isTransitioning(): boolean {
    return this.transitionProgress < 1.0
  }

  // Easing function
  private easeInOutCubic(t: number): number {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
  }

  // Reset a neutral
  reset(): void {
    this.currentEmotion = 'neutral'
    this.targetEmotion = 'neutral'
    this.transitionProgress = 1.0
  }
}

// Facial Animator - Animaciones faciales específicas
export class FacialAnimator {
  private expressionSystem: ExpressionSystem

  constructor() {
    this.expressionSystem = new ExpressionSystem()
  }

  // Sonreír gradualmente
  smile(model: THREE.Object3D, intensity: number = 0.8, duration: number = 500): void {
    this.expressionSystem.setEmotion('happy', duration)
  }

  // Fruncir el ceño
  frown(model: THREE.Object3D, intensity: number = 0.7, duration: number = 500): void {
    this.expressionSystem.setEmotion('sad', duration)
  }

  // Sorprenderse
  surprise(model: THREE.Object3D, duration: number = 300): void {
    this.expressionSystem.setEmotion('surprised', duration)
  }

  // Mostrar curiosidad
  showCuriosity(model: THREE.Object3D, duration: number = 600): void {
    this.expressionSystem.setEmotion('curious', duration)
  }

  // Secuencia de emociones
  async playEmotionSequence(
    model: THREE.Object3D,
    emotions: Emotion[],
    durationPerEmotion: number = 1000
  ): Promise<void> {
    for (const emotion of emotions) {
      this.expressionSystem.setEmotion(emotion, 500)
      await new Promise(resolve => setTimeout(resolve, durationPerEmotion))
    }
  }

  // Reacción a evento
  reactToEvent(model: THREE.Object3D, eventType: 'positive' | 'negative' | 'neutral'): void {
    switch (eventType) {
      case 'positive':
        this.expressionSystem.setEmotion('happy', 400)
        break
      case 'negative':
        this.expressionSystem.setEmotion('sad', 400)
        break
      case 'neutral':
        this.expressionSystem.setEmotion('neutral', 300)
        break
    }
  }

  // Obtener sistema de expresiones
  getExpressionSystem(): ExpressionSystem {
    return this.expressionSystem
  }

  // Actualizar (llamar en loop)
  update(model: THREE.Object3D): void {
    this.expressionSystem.update(model)
  }
}

// Emotion Engine - Motor de emociones con estado
export class EmotionEngine {
  private currentMood: Emotion = 'neutral'
  private moodIntensity: number = 0.5
  private moodDecayRate: number = 0.1 // Por segundo
  private lastUpdateTime: number = Date.now()

  // Establecer mood base
  setMood(emotion: Emotion, intensity: number = 0.5): void {
    this.currentMood = emotion
    this.moodIntensity = Math.max(0, Math.min(1, intensity))
  }

  // Actualizar mood (decay con el tiempo)
  update(): void {
    const now = Date.now()
    const deltaTime = (now - this.lastUpdateTime) / 1000
    this.lastUpdateTime = now

    // Decay hacia neutral
    if (this.currentMood !== 'neutral') {
      this.moodIntensity -= this.moodDecayRate * deltaTime
      
      if (this.moodIntensity <= 0) {
        this.currentMood = 'neutral'
        this.moodIntensity = 0.5
      }
    }
  }

  // Trigger emoción temporal
  triggerEmotion(emotion: Emotion, intensity: number = 0.8): void {
    this.currentMood = emotion
    this.moodIntensity = intensity
  }

  // Obtener mood actual
  getCurrentMood(): { emotion: Emotion; intensity: number } {
    return {
      emotion: this.currentMood,
      intensity: this.moodIntensity
    }
  }

  // Configurar decay rate
  setDecayRate(rate: number): void {
    this.moodDecayRate = rate
  }
}
