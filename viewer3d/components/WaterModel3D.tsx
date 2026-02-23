/**
 * WaterModel3D - Agua 3D usando modelo GLB de Blender
 * 
 * Carga el modelo water_blender.glb
 */

import { useRef, useEffect } from 'react'
import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface WaterModel3DProps {
  position?: [number, number, number]
  size?: number
  color?: string
}

export default function WaterModel3D({ 
  position = [0, -0.5, 0], 
  size = 150,
  color = '#1e3a5f'
}: WaterModel3DProps) {
  const groupRef = useRef<THREE.Group>(null)
  
  // Cargar modelo GLB
  const { scene } = useGLTF('/water_blender.glb')
  
  // Clonar el modelo
  const clonedScene = scene.clone()
  
  useEffect(() => {
    if (clonedScene) {
      // Ajustar escala según el tamaño deseado
      const scale = size / 10 // Ajustar según el tamaño del modelo original
      clonedScene.scale.set(scale, 1, scale)
      
      // Configurar materiales
      clonedScene.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.receiveShadow = true
          
          // Si el material existe, ajustar propiedades
          if (child.material) {
            if (Array.isArray(child.material)) {
              child.material.forEach(mat => {
                if (mat instanceof THREE.MeshStandardMaterial) {
                  mat.transparent = true
                  mat.opacity = 0.8
                  mat.roughness = 0.1
                  mat.metalness = 0.1
                  mat.color = new THREE.Color(color)
                }
              })
            } else if (child.material instanceof THREE.MeshStandardMaterial) {
              child.material.transparent = true
              child.material.opacity = 0.8
              child.material.roughness = 0.1
              child.material.metalness = 0.1
              child.material.color = new THREE.Color(color)
            }
          }
        }
      })
    }
  }, [clonedScene, size, color])
  
  // Animación sutil de ondulación
  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 0.5) * 0.02
    }
  })
  
  return (
    <group ref={groupRef} position={position}>
      <primitive object={clonedScene} />
    </group>
  )
}

// Precargar el modelo
useGLTF.preload('/water_blender.glb')
