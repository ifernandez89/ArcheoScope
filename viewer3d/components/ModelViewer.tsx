'use client'

import { useGLTF, useAnimations } from '@react-three/drei'
import { useEffect, useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface ModelViewerProps {
  modelPath: string
}

export default function ModelViewer({ modelPath }: ModelViewerProps) {
  const group = useRef<THREE.Group>(null)
  const { scene, animations } = useGLTF(modelPath)
  const { actions, names } = useAnimations(animations, group)
  const [autoRotate, setAutoRotate] = useState(true)

  // Reproducir animaciones si existen
  useEffect(() => {
    if (names.length > 0 && actions[names[0]]) {
      console.log('🎬 Animaciones disponibles:', names)
      actions[names[0]]?.play()
    }
  }, [actions, names])

  // Auto-rotación suave
  useFrame((state, delta) => {
    if (group.current && autoRotate) {
      group.current.rotation.y += delta * 0.3
    }
  })

  // Centrar y escalar el modelo
  useEffect(() => {
    if (scene) {
      // Calcular bounding box
      const box = new THREE.Box3().setFromObject(scene)
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())

      // Centrar
      scene.position.x = -center.x
      scene.position.y = -center.y
      scene.position.z = -center.z

      // Escalar para que quepa en la vista
      const maxDim = Math.max(size.x, size.y, size.z)
      const scale = 2 / maxDim
      scene.scale.setScalar(scale)

      console.log('📦 Modelo cargado:', {
        dimensiones: size,
        centro: center,
        escala: scale,
        animaciones: names.length
      })
    }
  }, [scene, names])

  // Toggle auto-rotate con click
  const handleClick = () => {
    setAutoRotate(!autoRotate)
    console.log('🔄 Auto-rotación:', !autoRotate ? 'ON' : 'OFF')
  }

  return (
    <group ref={group} onClick={handleClick}>
      <primitive object={scene} />
    </group>
  )
}

// Precargar el modelo
useGLTF.preload('/warrior.glb')
