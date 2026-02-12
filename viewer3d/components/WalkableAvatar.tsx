'use client'

import { useRef, useEffect, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF, useAnimations } from '@react-three/drei'
import * as THREE from 'three'

interface WalkableAvatarProps {
  modelPath: string
  terrainRef?: React.RefObject<THREE.Mesh>
  onPositionChange?: (position: THREE.Vector3) => void
  onModelChange?: () => void
}

export default function WalkableAvatar({ 
  modelPath, 
  terrainRef,
  onPositionChange,
  onModelChange
}: WalkableAvatarProps) {
  const group = useRef<THREE.Group>(null)
  const { scene, animations } = useGLTF(modelPath)
  const { actions, names } = useAnimations(animations, group)
  const { camera } = useThree()
  
  // Estado del avatar
  const [state, setState] = useState<'idle' | 'walking'>('idle')
  const velocity = useRef(new THREE.Vector3())
  const moveSpeed = 5.0  // Aumentado para movimiento más visible
  const rotationSpeed = 8.0  // Aumentado para rotación más rápida
  const keys = useRef<{ [key: string]: boolean }>({})
  const raycaster = useRef(new THREE.Raycaster())
  
  // Notificar cambio de modelo
  useEffect(() => {
    if (onModelChange) {
      onModelChange()
    }
  }, [modelPath, onModelChange])
  
  // Configurar controles de teclado
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      keys.current[e.key.toLowerCase()] = true
    }
    const handleKeyUp = (e: KeyboardEvent) => {
      keys.current[e.key.toLowerCase()] = false
    }

    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('keyup', handleKeyUp)
    }
  }, [])
  
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

      // Habilitar sombras
      scene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          child.castShadow = true
          child.receiveShadow = true
        }
      })
      
      console.log('🚶 Avatar cargado:', {
        animaciones: names,
        dimensiones: size,
        escala: scale,
        modelHeight,
        boxMin: box.min.y,
        boxMax: box.max.y
      })
    }
  }, [scene, names])
  
  // Gestionar animaciones según estado
  useEffect(() => {
    if (!actions || names.length === 0) return
    
    // Buscar animaciones por nombre común
    const idleAnim = names.find(n => 
      n.toLowerCase().includes('idle') || 
      n.toLowerCase().includes('stand')
    ) || names[0]
    
    const walkAnim = names.find(n => 
      n.toLowerCase().includes('walk') || 
      n.toLowerCase().includes('run')
    ) || names[1]
    
    // Detener todas las animaciones
    Object.values(actions).forEach(action => action?.stop())
    
    // Reproducir animación según estado
    if (state === 'walking' && walkAnim && actions[walkAnim]) {
      actions[walkAnim]?.reset().fadeIn(0.2).play()
    } else if (state === 'idle' && idleAnim && actions[idleAnim]) {
      actions[idleAnim]?.reset().fadeIn(0.2).play()
    }
    
  }, [state, actions, names])
  
  // Loop de movimiento
  useFrame((_, delta) => {
    if (!group.current) return
    
    // Calcular dirección de movimiento
    const moveDirection = new THREE.Vector3()
    const forward = new THREE.Vector3()
    const right = new THREE.Vector3()
    
    // Obtener dirección de la cámara (solo en plano XZ)
    camera.getWorldDirection(forward)
    forward.y = 0
    forward.normalize()
    
    right.crossVectors(forward, new THREE.Vector3(0, 1, 0)).normalize()
    
    // Input de teclado
    let isMoving = false
    
    if (keys.current['w']) {
      moveDirection.add(forward)
      isMoving = true
    }
    if (keys.current['s']) {
      moveDirection.sub(forward)
      isMoving = true
    }
    if (keys.current['a']) {
      moveDirection.add(right)
      isMoving = true
    }
    if (keys.current['d']) {
      moveDirection.sub(right)
      isMoving = true
    }
    
    // Actualizar estado
    setState(isMoving ? 'walking' : 'idle')
    
    // Aplicar movimiento
    if (isMoving) {
      moveDirection.normalize()
      velocity.current.copy(moveDirection.multiplyScalar(moveSpeed * delta))
      group.current.position.add(velocity.current)
      
      // Rotar avatar hacia dirección de movimiento
      const targetRotation = Math.atan2(moveDirection.x, moveDirection.z)
      group.current.rotation.y = THREE.MathUtils.lerp(
        group.current.rotation.y,
        targetRotation,
        rotationSpeed * delta
      )
      
      console.log('🚶 Moviendo:', {
        position: group.current.position,
        direction: moveDirection,
        velocity: velocity.current
      })
    }
    
    // Mantener avatar pegado al terreno
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
        // Mantener los pies del avatar en el suelo (no el centro)
        group.current.position.y = groundHeight + 0.9  // Offset para altura del modelo
      }
    }
    
    // Límites del mundo
    const worldLimit = 95
    group.current.position.x = Math.max(-worldLimit, Math.min(worldLimit, group.current.position.x))
    group.current.position.z = Math.max(-worldLimit, Math.min(worldLimit, group.current.position.z))
    
    // Actualizar posición de la cámara para seguir al avatar
    const cameraOffset = new THREE.Vector3(0, 2, 5)
    const targetCameraPos = group.current.position.clone().add(
      cameraOffset.applyQuaternion(
        new THREE.Quaternion().setFromEuler(
          new THREE.Euler(0, group.current.rotation.y, 0)
        )
      )
    )
    
    camera.position.lerp(targetCameraPos, 3 * delta)
    camera.lookAt(
      group.current.position.x,
      group.current.position.y + 1,
      group.current.position.z
    )
    
    // Notificar cambio de posición
    if (onPositionChange) {
      onPositionChange(group.current.position)
    }
  })
  
  return (
    <group ref={group} position={[0, 0, 0]}>
      <primitive object={scene} />
    </group>
  )
}

// Precargar modelos comunes
useGLTF.preload('/warrior.glb')
useGLTF.preload('/moai.glb')
