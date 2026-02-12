// AI Animator - Procedural Animation Generator
// Generates smooth animations procedurally without pre-baked data

import * as THREE from 'three'

export interface AnimationConfig {
  model: THREE.Object3D
  action: 'idle' | 'walk' | 'wave' | 'nod' | 'turn' | 'custom'
  style?: 'subtle' | 'normal' | 'exaggerated'
  duration: number
  loop?: boolean
  easing?: 'linear' | 'easeIn' | 'easeOut' | 'easeInOut'
}

export interface KeyFrame {
  time: number
  position?: THREE.Vector3
  rotation?: THREE.Euler
  scale?: THREE.Vector3
}

export class AIAnimator {
  private animations: Map<string, THREE.AnimationMixer> = new Map()
  private clock: THREE.Clock = new THREE.Clock()

  // Generar animación procedural
  generateAnimation(config: AnimationConfig): THREE.AnimationClip {
    const { action, style = 'normal', duration } = config

    let keyframes: KeyFrame[] = []

    switch (action) {
      case 'idle':
        keyframes = this.generateIdleAnimation(duration, style)
        break
      case 'walk':
        keyframes = this.generateWalkAnimation(duration, style)
        break
      case 'wave':
        keyframes = this.generateWaveAnimation(duration, style)
        break
      case 'nod':
        keyframes = this.generateNodAnimation(duration, style)
        break
      case 'turn':
        keyframes = this.generateTurnAnimation(duration, style)
        break
      default:
        keyframes = this.generateIdleAnimation(duration, style)
    }

    return this.createAnimationClip(action, keyframes, duration)
  }

  // Idle: Respiración sutil
  private generateIdleAnimation(duration: number, style: string): KeyFrame[] {
    const amplitude = style === 'subtle' ? 0.01 : style === 'exaggerated' ? 0.05 : 0.02
    const frequency = 2 // respiraciones por segundo

    const frames: KeyFrame[] = []
    const steps = 30

    for (let i = 0; i <= steps; i++) {
      const t = (i / steps) * duration
      const phase = (t / duration) * frequency * Math.PI * 2
      const offset = Math.sin(phase) * amplitude

      frames.push({
        time: t,
        position: new THREE.Vector3(0, offset, 0),
        rotation: new THREE.Euler(0, 0, 0)
      })
    }

    return frames
  }

  // Walk: Caminar procedural
  private generateWalkAnimation(duration: number, style: string): KeyFrame[] {
    const stepLength = style === 'subtle' ? 0.3 : style === 'exaggerated' ? 0.8 : 0.5
    const bobAmount = style === 'subtle' ? 0.05 : style === 'exaggerated' ? 0.15 : 0.1
    const frequency = 1.5

    const frames: KeyFrame[] = []
    const steps = 40

    for (let i = 0; i <= steps; i++) {
      const t = (i / steps) * duration
      const phase = (t / duration) * frequency * Math.PI * 2

      // Movimiento hacia adelante
      const z = Math.sin(phase) * stepLength

      // Bob vertical
      const y = Math.abs(Math.sin(phase * 2)) * bobAmount

      // Rotación sutil
      const rotY = Math.sin(phase) * 0.1

      frames.push({
        time: t,
        position: new THREE.Vector3(0, y, z),
        rotation: new THREE.Euler(0, rotY, 0)
      })
    }

    return frames
  }

  // Wave: Saludo con la mano
  private generateWaveAnimation(duration: number, style: string): KeyFrame[] {
    const amplitude = style === 'subtle' ? 0.3 : style === 'exaggerated' ? 0.8 : 0.5
    const frequency = 2

    const frames: KeyFrame[] = []
    const steps = 30

    for (let i = 0; i <= steps; i++) {
      const t = (i / steps) * duration
      const phase = (t / duration) * frequency * Math.PI * 2

      // Rotación del brazo (simulado con rotación del modelo)
      const rotZ = Math.sin(phase) * amplitude

      frames.push({
        time: t,
        rotation: new THREE.Euler(0, 0, rotZ)
      })
    }

    return frames
  }

  // Nod: Asentir con la cabeza
  private generateNodAnimation(duration: number, style: string): KeyFrame[] {
    const amplitude = style === 'subtle' ? 0.1 : style === 'exaggerated' ? 0.4 : 0.2
    const frequency = 1.5

    const frames: KeyFrame[] = []
    const steps = 20

    for (let i = 0; i <= steps; i++) {
      const t = (i / steps) * duration
      const phase = (t / duration) * frequency * Math.PI * 2

      // Rotación de cabeza (pitch)
      const rotX = Math.sin(phase) * amplitude

      frames.push({
        time: t,
        rotation: new THREE.Euler(rotX, 0, 0)
      })
    }

    return frames
  }

  // Turn: Girar sobre su eje
  private generateTurnAnimation(duration: number, style: string): KeyFrame[] {
    const totalRotation = style === 'subtle' ? Math.PI / 4 : style === 'exaggerated' ? Math.PI * 2 : Math.PI

    const frames: KeyFrame[] = []
    const steps = 30

    for (let i = 0; i <= steps; i++) {
      const t = (i / steps) * duration
      const progress = i / steps

      // Rotación suave con easing
      const easedProgress = this.easeInOutCubic(progress)
      const rotY = easedProgress * totalRotation

      frames.push({
        time: t,
        rotation: new THREE.Euler(0, rotY, 0)
      })
    }

    return frames
  }

  // Crear AnimationClip desde keyframes
  private createAnimationClip(name: string, keyframes: KeyFrame[], duration: number): THREE.AnimationClip {
    const times: number[] = []
    const positionValues: number[] = []
    const rotationValues: number[] = []

    keyframes.forEach(frame => {
      times.push(frame.time / 1000) // Convertir a segundos

      // Position
      if (frame.position) {
        positionValues.push(frame.position.x, frame.position.y, frame.position.z)
      } else {
        positionValues.push(0, 0, 0)
      }

      // Rotation (como quaternion)
      if (frame.rotation) {
        const quat = new THREE.Quaternion().setFromEuler(frame.rotation)
        rotationValues.push(quat.x, quat.y, quat.z, quat.w)
      } else {
        rotationValues.push(0, 0, 0, 1)
      }
    })

    // Crear tracks
    const positionTrack = new THREE.VectorKeyframeTrack(
      '.position',
      times,
      positionValues
    )

    const rotationTrack = new THREE.QuaternionKeyframeTrack(
      '.quaternion',
      times,
      rotationValues
    )

    return new THREE.AnimationClip(name, duration / 1000, [positionTrack, rotationTrack])
  }

  // Reproducir animación en un modelo
  playAnimation(model: THREE.Object3D, clip: THREE.AnimationClip, loop: boolean = true): THREE.AnimationMixer {
    const mixer = new THREE.AnimationMixer(model)
    const action = mixer.clipAction(clip)
    
    action.setLoop(loop ? THREE.LoopRepeat : THREE.LoopOnce, loop ? Infinity : 1)
    action.play()

    this.animations.set(model.uuid, mixer)
    return mixer
  }

  // Detener animación
  stopAnimation(model: THREE.Object3D): void {
    const mixer = this.animations.get(model.uuid)
    if (mixer) {
      mixer.stopAllAction()
      this.animations.delete(model.uuid)
    }
  }

  // Actualizar todas las animaciones
  update(deltaTime?: number): void {
    const delta = deltaTime !== undefined ? deltaTime : this.clock.getDelta()
    
    this.animations.forEach(mixer => {
      mixer.update(delta)
    })
  }

  // Easing functions
  private easeInOutCubic(t: number): number {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
  }

  private easeInQuad(t: number): number {
    return t * t
  }

  private easeOutQuad(t: number): number {
    return t * (2 - t)
  }

  // Blend entre dos animaciones
  blendAnimations(
    model: THREE.Object3D,
    fromClip: THREE.AnimationClip,
    toClip: THREE.AnimationClip,
    duration: number
  ): void {
    const mixer = this.animations.get(model.uuid)
    if (!mixer) return

    const fromAction = mixer.clipAction(fromClip)
    const toAction = mixer.clipAction(toClip)

    fromAction.fadeOut(duration)
    toAction.reset().fadeIn(duration).play()
  }

  // Limpiar recursos
  dispose(): void {
    this.animations.forEach(mixer => {
      mixer.stopAllAction()
    })
    this.animations.clear()
  }

  // Obtener mixer de un modelo
  getMixer(model: THREE.Object3D): THREE.AnimationMixer | undefined {
    return this.animations.get(model.uuid)
  }

  // Verificar si tiene animación activa
  hasActiveAnimation(model: THREE.Object3D): boolean {
    return this.animations.has(model.uuid)
  }
}

// Motion Generator - Generador de movimientos complejos
export class MotionGenerator {
  // Generar trayectoria circular
  static generateCircularPath(
    center: THREE.Vector3,
    radius: number,
    steps: number
  ): THREE.Vector3[] {
    const points: THREE.Vector3[] = []

    for (let i = 0; i <= steps; i++) {
      const angle = (i / steps) * Math.PI * 2
      const x = center.x + Math.cos(angle) * radius
      const z = center.z + Math.sin(angle) * radius
      points.push(new THREE.Vector3(x, center.y, z))
    }

    return points
  }

  // Generar trayectoria de Bezier
  static generateBezierPath(
    start: THREE.Vector3,
    control1: THREE.Vector3,
    control2: THREE.Vector3,
    end: THREE.Vector3,
    steps: number
  ): THREE.Vector3[] {
    const curve = new THREE.CubicBezierCurve3(start, control1, control2, end)
    return curve.getPoints(steps)
  }

  // Generar movimiento de patrulla
  static generatePatrolPath(waypoints: THREE.Vector3[], smooth: boolean = true): THREE.Vector3[] {
    if (!smooth) return waypoints

    const curve = new THREE.CatmullRomCurve3(waypoints, true)
    return curve.getPoints(waypoints.length * 10)
  }

  // Generar movimiento aleatorio (random walk)
  static generateRandomWalk(
    start: THREE.Vector3,
    steps: number,
    stepSize: number
  ): THREE.Vector3[] {
    const points: THREE.Vector3[] = [start.clone()]
    let current = start.clone()

    for (let i = 0; i < steps; i++) {
      const angle = Math.random() * Math.PI * 2
      const dx = Math.cos(angle) * stepSize
      const dz = Math.sin(angle) * stepSize

      current = current.clone().add(new THREE.Vector3(dx, 0, dz))
      points.push(current)
    }

    return points
  }
}
