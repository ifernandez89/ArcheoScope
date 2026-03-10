'use client'

import { useRef, useEffect, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF, useAnimations } from '@react-three/drei'
import * as THREE from 'three'
import CosmicEntity from './CosmicEntity'
import { loggers } from '@/core/Logger'

interface WalkableAvatarProps {
  modelPath: string
  terrainRef?: React.RefObject<THREE.Mesh>
  onPositionChange?: (position: THREE.Vector3) => void
  onModelChange?: () => void
  solarDirection?: { x: number, y: number, z: number }
  isDay?: boolean
  showCosmicEffects?: boolean
  disableCameraControl?: boolean // Nuevo prop para deshabilitar control de cámara
  initialPosition?: [number, number, number] // Posición inicial
}

// Detectar tipo de avatar según el path
function getAvatarType(modelPath: string): 'humanoid' | 'statue' | 'creature' | 'flying' {
  if (modelPath.includes('warrior')) return 'humanoid'
  if (modelPath.includes('moai')) return 'statue'
  if (modelPath.includes('sphinx')) return 'creature'
  if (modelPath.includes('avenger') || modelPath.includes('ufo')) return 'flying'
  return 'humanoid'
}

export default function WalkableAvatar({ 
  modelPath, 
  terrainRef,
  onPositionChange,
  onModelChange,
  solarDirection = { x: 0, y: 1, z: 0 },
  isDay = true,
  showCosmicEffects = true,  // Reactivado
  disableCameraControl = false, // Por defecto controla la cámara
  initialPosition = [0, 0, 0] // Posición inicial por defecto
}: WalkableAvatarProps) {
  const group = useRef<THREE.Group>(null)
  const modelRef = useRef<THREE.Group>(null) // Ref para el modelo interno (solo para rotación)
  const sunLightRef = useRef<THREE.DirectionalLight>(null)
  const { scene, animations } = useGLTF(modelPath)
  const { actions, names } = useAnimations(animations, group)
  const { camera } = useThree()
  
  // Convertir solarDirection de objeto plano a Vector3
  const solarDirectionVec3 = new THREE.Vector3(solarDirection.x, solarDirection.y, solarDirection.z)
  
  // Estado del avatar
  const [state, setState] = useState<'idle' | 'walking'>('idle')
  const velocity = useRef(new THREE.Vector3())
  const moveSpeed = 20.0  // Duplicado: de 10.0 a 20.0 para movimiento más rápido
  const rotationSpeed = 8.0  // Aumentado para rotación más rápida
  const keys = useRef<{ [key: string]: boolean }>({})
  const raycaster = useRef(new THREE.Raycaster())
  
  // Control vertical con SHIFT + mouse
  const isShiftPressed = useRef(false)
  const mousePosition = useRef({ x: 0, y: 0 })
  const targetDirection = useRef(new THREE.Vector3())
  
  // Configurar raycaster para que solo detecte capa 0 (terreno)
  // Ignorar capa 1 (efectos visuales)
  useEffect(() => {
    raycaster.current.layers.set(0)
  }, [])
  const idleTimer = useRef(0)  // Timer para detectar cuando está quieto
  const timeAccumulator = useRef(0)  // Para animaciones procedurales
  const avatarType = getAvatarType(modelPath)
  
  // Estado de salto
  const isJumping = useRef(false)
  const verticalVelocity = useRef(0)
  const jumpForce = 10.0  // Aumentado para salto más visible
  const gravity = -25.0  // Aumentado para caída más natural
  const groundLevel = useRef(0)  // Nivel del suelo
  const flyingHeight = 10.0  // Altura de vuelo para el OVNI (2x la original)
  
  // Resetear avatar al cambiar modelo
  useEffect(() => {
    loggers.avatar.debug('Tipo de avatar:', avatarType)
    loggers.avatar.debug('Model path:', modelPath)
    loggers.avatar.debug('Es UFO 1?', modelPath.includes('ufo_1'))
    
    // Solo resetear posición al montar el componente inicialmente
    if (group.current && group.current.position.length() === 0) {
      group.current.position.set(initialPosition[0], initialPosition[1], initialPosition[2])
      group.current.rotation.set(0, 0, 0)
    }
    
    // Resetear timer de idle para forzar reposicionamiento de cámara
    idleTimer.current = 2.0  // Forzar reposicionamiento inmediato
    
  }, [modelPath, avatarType]) // Removido initialPosition de las dependencias
  
  // Configurar controles de teclado
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const key = e.key.toLowerCase()
      keys.current[key] = true
      
      // Detectar SHIFT para control de vuelo libre
      if (e.key === 'Shift') {
        isShiftPressed.current = true
      }
      
      // Detectar salto con barra espaciadora (solo si NO es Avenger)
      if (e.code === 'Space' && !isJumping.current && avatarType !== 'flying') {
        isJumping.current = true
        verticalVelocity.current = jumpForce
        loggers.avatar.debug('Salto iniciado')
      }
    }
    
    const handleKeyUp = (e: KeyboardEvent) => {
      keys.current[e.key.toLowerCase()] = false
      
      // Detectar liberación de SHIFT
      if (e.key === 'Shift') {
        isShiftPressed.current = false
      }
    }
    
    const handleMouseMove = (e: MouseEvent) => {
      // Normalizar coordenadas del mouse (-1 a 1)
      mousePosition.current.x = (e.clientX / window.innerWidth) * 2 - 1
      mousePosition.current.y = -(e.clientY / window.innerHeight) * 2 + 1
    }

    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)
    window.addEventListener('mousemove', handleMouseMove)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('keyup', handleKeyUp)
      window.removeEventListener('mousemove', handleMouseMove)
    }
  }, [avatarType])
  
  // Configurar modelo
  useEffect(() => {
    if (scene && group.current) {
      // Calcular bounding box y centrar
      const box = new THREE.Box3().setFromObject(scene)
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())

      // Centrar horizontalmente
      scene.position.x = -center.x
      scene.position.z = -center.z
      
      // IMPORTANTE: Elevar el modelo para que los pies estén en y=0 del grupo
      // El grupo ya está en el suelo, así que el modelo debe estar elevado
      const modelHeight = size.y
      scene.position.y = 0  // El modelo empieza en 0 del grupo
      
      // Ajustar la posición del grupo para compensar
      group.current.position.y = modelHeight * 0.5  // Elevar el grupo

      const maxDim = Math.max(size.x, size.y, size.z)
      const scale = 1.8 / maxDim
      scene.scale.setScalar(scale)
      
      scene.rotation.set(0, 0, 0)

      // Habilitar sombras y configurar materiales para reaccionar a luz
      scene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh
          child.castShadow = true
          child.receiveShadow = true
          
          // Asegurar que el material reaccione a la luz
          if (mesh.material) {
            const material = mesh.material as THREE.Material
            
            // Si es MeshBasicMaterial, convertir a MeshStandardMaterial
            if ((material as any).type === 'MeshBasicMaterial') {
              const basicMat = material as THREE.MeshBasicMaterial
              const standardMat = new THREE.MeshStandardMaterial({
                color: basicMat.color,
                map: basicMat.map,
                roughness: 0.7,
                metalness: 0.1
              })
              mesh.material = standardMat
              loggers.avatar.debug('Material convertido a MeshStandardMaterial')
            }
            
            // Si ya es MeshStandardMaterial, ajustar propiedades
            if ((material as any).type === 'MeshStandardMaterial') {
              const stdMat = material as THREE.MeshStandardMaterial
              if (stdMat.roughness === undefined) stdMat.roughness = 0.7
              if (stdMat.metalness === undefined) stdMat.metalness = 0.1
              stdMat.needsUpdate = true
            }
            
            // Forzar actualización del material
            (material as any).needsUpdate = true
          }
        }
      })
      
      loggers.avatar.info('Avatar cargado:', {
        animaciones: names,
        totalAnimaciones: names.length,
        dimensiones: size,
        escala: scale,
        modelHeight,
        boxMin: box.min.y,
        boxMax: box.max.y
      })
      
      // Mostrar lista detallada de animaciones
      if (names.length > 0) {
        loggers.avatar.debug('Animaciones disponibles:', names)
      } else {
        loggers.avatar.warn('Este modelo NO tiene animaciones embebidas. Sugerencia: Usa Mixamo (https://www.mixamo.com/)')
      }
    }
  }, [scene, names])
  
  // Gestionar animaciones según estado con transiciones suaves
  // Solo para avatares humanoides con rig
  useEffect(() => {
    if (avatarType !== 'humanoid') {
      loggers.avatar.debug(`Avatar tipo "${avatarType}" usa animación procedural, no rig`)
      return
    }
    
    if (!actions || names.length === 0) {
      loggers.avatar.warn('No hay animaciones disponibles para este humanoide')
      return
    }
    
    // Buscar animaciones por nombre común
    const idleAnim = names.find(n => 
      n.toLowerCase().includes('idle') || 
      n.toLowerCase().includes('stand')
    ) || names[0]
    
    const walkAnim = names.find(n => 
      n.toLowerCase().includes('walk') || 
      n.toLowerCase().includes('run')
    ) || names[1]
    
    loggers.avatar.debug('Animaciones detectadas:', {
      idle: idleAnim,
      walk: walkAnim,
      todas: names,
      estado: state
    })
    
    // Transición suave entre animaciones
    if (state === 'walking' && walkAnim && actions[walkAnim]) {
      // Fade out idle
      if (idleAnim && actions[idleAnim]) {
        actions[idleAnim]?.fadeOut(0.3)
      }
      // Fade in walk
      actions[walkAnim]?.reset().fadeIn(0.3).play()
      loggers.avatar.debug('Reproduciendo animación: Walk')
    } else if (state === 'idle' && idleAnim && actions[idleAnim]) {
      // Fade out walk
      if (walkAnim && actions[walkAnim]) {
        actions[walkAnim]?.fadeOut(0.3)
      }
      // Fade in idle
      actions[idleAnim]?.reset().fadeIn(0.3).play()
      loggers.avatar.debug('Reproduciendo animación: Idle')
    }
    
  }, [state, actions, names, avatarType])
  
  // Loop de movimiento
  useFrame((state, delta) => {
    if (!group.current) return
    
    const camera = state.camera
    
    // MODO VUELO LIBRE: SHIFT presionado (solo para Avenger)
    if (avatarType === 'flying' && isShiftPressed.current) {
      // El mouse controla la DIRECCIÓN (pitch) de la nave
      // mousePosition.y: 1 (arriba) = mirar hacia arriba, -1 (abajo) = mirar hacia abajo
      
      // Calcular pitch (inclinación vertical) basado en posición Y del mouse
      // Rango: -45° (abajo) a +45° (arriba)
      const targetPitch = mousePosition.current.y * (Math.PI / 4)  // ±45 grados
      
      // Aplicar rotación suave
      const currentRotation = group.current.rotation.clone()
      currentRotation.x = THREE.MathUtils.lerp(currentRotation.x, targetPitch, 0.15)
      group.current.rotation.x = currentRotation.x
      
      // Calcular dirección de movimiento basada en las teclas Y la orientación de la nave
      const moveDirection = new THREE.Vector3()
      
      // Obtener la dirección frontal de la nave (considerando su rotación completa)
      const avatarForward = new THREE.Vector3(0, 0, 1)
      avatarForward.applyQuaternion(group.current.quaternion)
      avatarForward.normalize()
      
      // Calcular dirección derecha
      const avatarRight = new THREE.Vector3()
      avatarRight.crossVectors(avatarForward, new THREE.Vector3(0, 1, 0)).normalize()
      
      // Input de teclado (igual que modo normal)
      let isMoving = false
      
      if (keys.current['w']) {
        // Adelante en la dirección que mira (INCLUYE componente vertical)
        moveDirection.add(avatarForward)
        isMoving = true
      }
      if (keys.current['s']) {
        // Atrás (opuesto a la dirección)
        moveDirection.sub(avatarForward)
        isMoving = true
      }
      if (keys.current['a']) {
        // Izquierda
        moveDirection.sub(avatarRight)
        isMoving = true
      }
      if (keys.current['d']) {
        // Derecha
        moveDirection.add(avatarRight)
        isMoving = true
      }
      
      // Rotación con Q/E (yaw)
      if (keys.current['q']) {
        group.current.rotation.y += 2.0 * delta
      }
      if (keys.current['e']) {
        group.current.rotation.y -= 2.0 * delta
      }
      
      // Aplicar movimiento solo si hay input de teclado
      if (isMoving) {
        moveDirection.normalize()
        const flySpeed = moveSpeed * 1.5  // Velocidad aumentada en modo vuelo libre (era 1.2)
        velocity.current.copy(moveDirection.multiplyScalar(flySpeed * delta))
        group.current.position.add(velocity.current)
      }
      
      // Limitar altura
      if (group.current.position.y < 2) {
        group.current.position.y = 2
      }
      if (group.current.position.y > 150) {  // Aumentado de 100 a 150
        group.current.position.y = 150
      }
      
      return  // Salir del frame, no procesar movimiento normal
    }
    
    // MODO NORMAL: Movimiento basado en teclado
    // Calcular dirección de movimiento basada en el AVATAR, no en la cámara
    const moveDirection = new THREE.Vector3()
    
    // Obtener la dirección frontal del avatar (hacia donde mira)
    // Por defecto, los modelos miran hacia -Z en Three.js
    const avatarForward = new THREE.Vector3(0, 0, 1)  // Cambiado de -1 a 1
    avatarForward.applyQuaternion(group.current.quaternion)
    avatarForward.y = 0
    avatarForward.normalize()
    
    // Calcular dirección derecha del avatar
    const avatarRight = new THREE.Vector3()
    avatarRight.crossVectors(avatarForward, new THREE.Vector3(0, 1, 0)).normalize()
    
    // Input de teclado
    let isMoving = false
    
    if (keys.current['w']) {
      moveDirection.add(avatarForward)  // Adelante
      isMoving = true
    }
    if (keys.current['s']) {
      moveDirection.sub(avatarForward)  // Atrás
      isMoving = true
    }
    if (keys.current['a']) {
      moveDirection.sub(avatarRight)  // Izquierda
      isMoving = true
    }
    if (keys.current['d']) {
      moveDirection.add(avatarRight)  // Derecha
      isMoving = true
    }
    
    // Rotación del avatar con Q/E (todos los UFOs pueden rotar manualmente)
    if (keys.current['q']) {
      group.current.rotation.y += 2.0 * delta  // Rotar izquierda
    }
    if (keys.current['e']) {
      group.current.rotation.y -= 2.0 * delta  // Rotar derecha
    }
    
    // Actualizar estado
    setState(isMoving ? 'walking' : 'idle')
    
    // Incrementar timer cuando está quieto
    if (!isMoving) {
      idleTimer.current += delta
    } else {
      idleTimer.current = 0
    }
    
    // Aplicar movimiento
    if (isMoving) {
      moveDirection.normalize()
      velocity.current.copy(moveDirection.multiplyScalar(moveSpeed * delta))
      group.current.position.add(velocity.current)
    }
    
    // Física de salto (solo para avatares terrestres)
    if (avatarType !== 'flying') {
      if (isJumping.current) {
        // Aplicar gravedad
        verticalVelocity.current += gravity * delta
        
        // Aplicar velocidad vertical
        group.current.position.y += verticalVelocity.current * delta
        
        // Detectar aterrizaje
        if (group.current.position.y <= groundLevel.current) {
          group.current.position.y = groundLevel.current
          isJumping.current = false
          verticalVelocity.current = 0
          loggers.avatar.debug('Aterrizaje completado')
        }
      } else {
        // Guardar nivel del suelo cuando está en tierra
        groundLevel.current = group.current.position.y
      }
    }
    
    // Animaciones procedurales según tipo de avatar
    timeAccumulator.current += delta
    
    if (avatarType === 'flying') {
      // 🚀 Avenger: Vuelo flotante con oscilación suave
      // Calcular altura objetivo sobre el terreno
      let targetHeight = flyingHeight
      
      if (terrainRef?.current) {
        raycaster.current.set(
          new THREE.Vector3(
            group.current.position.x,
            group.current.position.y + 10,
            group.current.position.z
          ),
          new THREE.Vector3(0, -1, 0)
        )
        
        const intersects = raycaster.current.intersectObject(terrainRef.current, true)
        
        if (intersects.length > 0) {
          const groundHeight = intersects[0].point.y
          targetHeight = groundHeight + flyingHeight
        }
      }
      
      // Oscilación desactivada para evitar meneo de la nave
      const oscillation = 0  // Era: Math.sin(timeAccumulator.current * 2) * 0.15
      const finalTargetHeight = targetHeight + oscillation
      
      // Suavizar transición a altura objetivo solo si hay diferencia significativa
      const heightDifference = Math.abs(finalTargetHeight - group.current.position.y)
      if (heightDifference > 0.01) {  // Solo ajustar si la diferencia es mayor a 1cm
        group.current.position.y += (finalTargetHeight - group.current.position.y) * 8 * delta
      }
      
      // ========================================
      // ROTACIÓN AUTOMÁTICA DE MODELOS
      // ========================================
      // Esta lógica permite que ciertos modelos roten automáticamente sobre su eje Y
      // mientras mantienen la capacidad de ser controlados con Q/E.
      // 
      // IMPORTANTE: Usar modelRef.current.rotation.y (NO group.current.rotation.y)
      // para rotar solo el modelo interno sin afectar la cámara ni el movimiento.
      //
      // Para agregar rotación automática a otros modelos en el futuro:
      // 1. Agregar condición: if (modelPath.includes('nombre_modelo') && modelRef.current)
      // 2. Aplicar rotación: modelRef.current.rotation.y += velocidad * delta
      // 3. Velocidad recomendada: 0.5 a 2.0 * delta (más alto = más rápido)
      // ========================================
      
      // UFO 1: Rotación automática a velocidad normal
      if (modelPath.includes('ufo_1') && modelRef.current) {
        modelRef.current.rotation.y += 1.0 * delta
      }
      
      // UFO 5: Rotación automática a mitad de velocidad
      if (modelPath.includes('ufo_5') && modelRef.current) {
        modelRef.current.rotation.y += 0.5 * delta
      }
      
      // ========================================
      // FIN ROTACIÓN AUTOMÁTICA
      // ========================================
      
      // Inclinación sutil según dirección de movimiento (todos los UFOs)
      if (isMoving) {
        // Inclinación MUY sutil hacia adelante al moverse
        const targetX = Math.sin(timeAccumulator.current * 3) * 0.02 + 0.05
        const targetZ = Math.sin(timeAccumulator.current * 2.5) * 0.03
        group.current.rotation.x += (targetX - group.current.rotation.x) * 0.1
        group.current.rotation.z += (targetZ - group.current.rotation.z) * 0.1
      } else {
        // Volver a posición horizontal rápidamente
        group.current.rotation.x *= 0.85
        group.current.rotation.z *= 0.85
      }
      
    } else if (avatarType === 'statue') {
      // 🗿 MOAI: Deslizamiento místico con oscilación vertical
      if (isMoving) {
        // Oscilación sutil al moverse
        group.current.position.y += Math.sin(timeAccumulator.current * 3) * 0.015
        // Leve inclinación hacia adelante
        group.current.rotation.x = Math.sin(timeAccumulator.current * 2) * 0.03
      } else {
        // Respiración desactivada - mantener posición estable
        // group.current.position.y += Math.sin(timeAccumulator.current * 1.5) * 0.005
        // Volver a posición vertical
        group.current.rotation.x *= 0.95
      }
    } else if (avatarType === 'creature') {
      // 🦁 SPHINX: Movimiento con peso, majestuoso
      if (isMoving) {
        // Balanceo lateral al caminar
        group.current.rotation.z = Math.sin(timeAccumulator.current * 2.5) * 0.05
        // Inclinación hacia adelante con peso
        group.current.rotation.x = 0.08
      } else {
        // Volver a posición neutral suavemente
        group.current.rotation.z *= 0.9
        group.current.rotation.x *= 0.9
      }
    }
    // humanoid usa animaciones normales (si las tiene)
    
    // Mantener avatar pegado al terreno (solo avatares terrestres)
    if (avatarType !== 'flying' && terrainRef?.current) {
      raycaster.current.set(
        new THREE.Vector3(
          group.current.position.x,
          group.current.position.y + 10,
          group.current.position.z
        ),
        new THREE.Vector3(0, -1, 0)
      )
      
      const intersects = raycaster.current.intersectObject(terrainRef.current, true)
      
      if (intersects.length > 0) {
        const groundHeight = intersects[0].point.y
        // Mantener los pies del avatar en el suelo (no el centro)
        group.current.position.y = groundHeight + 0.9  // Offset para altura del modelo
      }
    }
    
    // Límites del mundo
    const worldLimit = 95
    group.current.position.x = Math.max(-worldLimit, Math.min(worldLimit, group.current.position.x))
    group.current.position.z = Math.max(-worldLimit, Math.min(worldLimit, group.current.position.z))
    
    // Actualizar posición de la cámara para seguir al avatar (solo si no está deshabilitado)
    if (!disableCameraControl) {
      // Cámara en tercera persona detrás del avatar
      const cameraDistance = 6  // Distancia de la cámara
      const cameraHeight = 3    // Altura de la cámara
      
      // Calcular posición de cámara detrás del avatar
      const avatarRotation = group.current.rotation.y
      const cameraX = group.current.position.x - Math.sin(avatarRotation) * cameraDistance
      const cameraZ = group.current.position.z - Math.cos(avatarRotation) * cameraDistance
      let cameraY = group.current.position.y + cameraHeight
      
      // Camera bob desactivado para eliminar oscilación
      // if (isMoving) {
      //   const bobSpeed = 8
      //   const bobAmount = 0.08
      //   cameraY += Math.sin(timeAccumulator.current * bobSpeed) * bobAmount
      // }
      
      // Velocidad de seguimiento adaptativa
      let followSpeed
      if (idleTimer.current > 1.0) {
        // Si ha estado quieto >1 seg, reposicionar agresivamente
        followSpeed = 15 * delta
      } else if (isMoving) {
        // Cuando se mueve, seguimiento rápido
        followSpeed = 10 * delta
      } else {
        // Transición suave cuando acaba de detenerse
        followSpeed = 5 * delta
      }
      
      // Suavizar movimiento de cámara
      camera.position.lerp(
        new THREE.Vector3(cameraX, cameraY, cameraZ),
        followSpeed
      )
      
      // Siempre mirar al avatar (un poco arriba del centro)
      const lookAtTarget = new THREE.Vector3(
        group.current.position.x,
        group.current.position.y + 1.5,
        group.current.position.z
      )
      camera.lookAt(lookAtTarget)
    }
    
    // Actualizar luz del Sol en el espacio para que apunte desde el Sol (0,0,0) hacia el Avenger
    if (disableCameraControl && sunLightRef.current && group.current) {
      // Calcular dirección desde el Sol hacia el Avenger
      const sunPosition = new THREE.Vector3(0, 0, 0)
      const avengerPosition = group.current.position.clone()
      const direction = avengerPosition.sub(sunPosition).normalize()
      
      // Posicionar la luz en dirección opuesta al Avenger (desde el Sol)
      const lightDistance = 50
      sunLightRef.current.position.copy(direction.multiplyScalar(-lightDistance))
    }
    
    // Notificar cambio de posición
    if (onPositionChange) {
      onPositionChange(group.current.position)
    }
  })
  
  return (
    <>
      <group ref={group} position={[0, 0, 0]} scale={avatarType === 'flying' ? 1.2 : 1}>
        {/* Grupo interno para el modelo (permite rotación independiente) */}
        <group ref={modelRef}>
          {/* Efectos cósmicos envolviendo el avatar (solo en Tierra, no en espacio, y NO para Avenger) */}
          {showCosmicEffects && !disableCameraControl && avatarType !== 'flying' && (
            <CosmicEntity
              solarDirection={solarDirectionVec3}
              isDay={isDay}
            >
              <primitive object={scene} />
            </CosmicEntity>
          )}
          
          {/* Sin efectos cósmicos, solo el modelo */}
          {(!showCosmicEffects || disableCameraControl || avatarType === 'flying') && <primitive object={scene} />}
        </group>
        
        {/* Iluminación mejorada para Avenger en el espacio */}
        {disableCameraControl && (
          <>
            {/* Luz del Sol - Direccional que simula la luz solar */}
            <directionalLight 
              ref={sunLightRef}
              intensity={2.5} 
              color="#fff5e6"
              castShadow
              shadow-mapSize-width={1024}
              shadow-mapSize-height={1024}
            />
            
            {/* Luces de relleno suaves para visibilidad */}
            <ambientLight intensity={0.2} />
            <pointLight position={[10, 10, 10]} intensity={0.3} color="#ffffff" />
          </>
        )}
        
        {/* Iluminación mejorada para visibilidad del avatar en Tierra */}
        {!disableCameraControl && (
          <>
            {/* Luz principal desde arriba con sombras */}
            <spotLight
              position={[0, 8, 0]}
              intensity={8.0}
              angle={Math.PI / 2.5}
              penumbra={0.3}
              distance={20}
              decay={1.5}
              color="#ffffff"
              castShadow
              shadow-mapSize-width={2048}
              shadow-mapSize-height={2048}
              shadow-camera-near={0.5}
              shadow-camera-far={25}
              shadow-bias={-0.0001}
            />
            
            {/* Luz de relleno desde arriba-atrás */}
            <pointLight position={[0, 6, -4]} intensity={5.0} color="#ffffff" distance={15} />
            
            {/* Luz frontal cálida */}
            <pointLight position={[0, 3, 5]} intensity={4.0} color="#ffe8d0" distance={12} />
            
            {/* Luz lateral izquierda */}
            <pointLight position={[-4, 3, 0]} intensity={3.0} color="#e0f0ff" distance={10} />
            
            {/* Luz lateral derecha */}
            <pointLight position={[4, 3, 0]} intensity={3.0} color="#ffe8d0" distance={10} />
          </>
        )}
      </group>
    </>
  )
}

import { getAssetPath } from '@/lib/paths'

// Precargar modelos comunes
useGLTF.preload(getAssetPath('/warrior.glb'))
useGLTF.preload(getAssetPath('/moai.glb'))
useGLTF.preload(getAssetPath('/sphinx.glb'))

// Precargar todos los UFOs
useGLTF.preload(getAssetPath('/ufo_1.glb'))
useGLTF.preload(getAssetPath('/ufo_2.glb'))
useGLTF.preload(getAssetPath('/ufo_3.glb'))
useGLTF.preload(getAssetPath('/ufo_4.glb'))
useGLTF.preload(getAssetPath('/ufo_5.glb'))

useGLTF.preload(getAssetPath('/avenger_01.glb'))
