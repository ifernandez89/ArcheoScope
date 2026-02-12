'use client'

import { useRef, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import { useGLTF, useAnimations } from '@react-three/drei'
import * as THREE from 'three'

interface AnimatedAvatarProps {
  modelPath: string
  emotion?: 'neutral' | 'happy' | 'thinking' | 'explaining'
  gesture?: 'idle' | 'point_left' | 'point_right' | 'wave' | 'nod'
  isSpeaking?: boolean
}

export default function AnimatedAvatar({ 
  modelPath, 
  emotion = 'neutral',
  gesture = 'idle',
  isSpeaking = false
}: AnimatedAvatarProps) {
  const group = useRef<THREE.Group>(null)
  const { scene, animations } = useGLTF(modelPath)
  const { actions, names } = useAnimations(animations, group)
  
  // Animación de respiración
  useFrame((state) => {
    if (group.current && !isSpeaking) {
      const breathe = Math.sin(state.clock.elapsedTime * 2) * 0.01
      group.current.scale.y = 1 + breathe
    }
  })
  
  // Mirar al usuario
  useFrame(({ camera }) => {
    if (group.current) {
      const direction = new THREE.Vector3()
      camera.getWorldPosition(direction)
      group.current.lookAt(direction.x, group.current.position.y, direction.z)
    }
  })
  
  // Ejecutar gestos
  useEffect(() => {
    if (gesture !== 'idle' && actions[gesture]) {
      actions[gesture]?.reset().play()
      
      // Volver a idle después del gesto
      setTimeout(() => {
        actions[gesture]?.fadeOut(0.5)
      }, 2000)
    }
  }, [gesture, actions])
  
  // Animación de habla
  useEffect(() => {
    if (isSpeaking && group.current) {
      // Micro movimientos de cabeza al hablar
      const interval = setInterval(() => {
        if (group.current) {
          group.current.rotation.y += (Math.random() - 0.5) * 0.05
          group.current.rotation.x += (Math.random() - 0.5) * 0.02
        }
      }, 100)
      
      return () => clearInterval(interval)
    }
  }, [isSpeaking])
  
  return (
    <group ref={group}>
      <primitive object={scene} />
    </group>
  )
}
