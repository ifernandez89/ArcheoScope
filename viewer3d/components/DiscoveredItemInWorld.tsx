'use client'

import { useRef, useEffect, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useGLTF, Html } from '@react-three/drei'
import * as THREE from 'three'

interface DiscoveredItemInWorldProps {
  modelPath: string
  position: [number, number, number]
  onCollect?: () => void
}

export default function DiscoveredItemInWorld({
  modelPath,
  position,
  onCollect
}: DiscoveredItemInWorldProps) {
  const groupRef = useRef<THREE.Group>(null)
  const { scene } = useGLTF(modelPath)
  const timeRef = useRef(0)
  const [isHovered, setIsHovered] = useState(false)
  const [isSelected, setIsSelected] = useState(false)
  const [isDisappearing, setIsDisappearing] = useState(false)
  const disappearTimer = useRef(0)
  const { camera } = useThree()
  
  // Cache de meshes para evitar traverse cada frame
  const cachedMeshes = useRef<THREE.Mesh[]>([])
  const meshesCached = useRef(false)

  // Configurar modelo
  useEffect(() => {
    if (scene) {
      // Calcular bounding box y centrar
      const box = new THREE.Box3().setFromObject(scene)
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())

      // Centrar modelo
      scene.position.x = -center.x
      scene.position.y = -center.y
      scene.position.z = -center.z

      // Escalar para que sea visible
      const maxDim = Math.max(size.x, size.y, size.z)
      const scale = 2.0 / maxDim
      scene.scale.setScalar(scale)

      // Habilitar sombras
      scene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          child.castShadow = true
          child.receiveShadow = true
        }
      })
      
      console.log('🏺 Magna Bowl visible en el lago:', { size, scale, position })
    }
  }, [scene])

  // Animación: rotación suave y desaparición
  useFrame((state, delta) => {
    if (groupRef.current) {
      timeRef.current += delta
      
      // Rotación lenta
      groupRef.current.rotation.y += delta * 0.3
      
      // Animación de desaparición
      if (isDisappearing) {
        disappearTimer.current += delta
        
        // Fade out y escala hacia arriba
        const progress = Math.min(disappearTimer.current / 1.0, 1) // 1 segundo
        groupRef.current.scale.setScalar(1 + progress * 0.5) // Crece un poco
        
        // Cache meshes solo una vez
        if (!meshesCached.current) {
          cachedMeshes.current = []
          scene.traverse((child) => {
            if ((child as THREE.Mesh).isMesh) {
              cachedMeshes.current.push(child as THREE.Mesh)
            }
          })
          meshesCached.current = true
        }
        
        // Fade out de meshes cacheados
        for (const mesh of cachedMeshes.current) {
          if (mesh.material) {
            const material = mesh.material as THREE.MeshStandardMaterial
            material.transparent = true
            material.opacity = 1 - progress
          }
        }
        
        // Llamar callback cuando termine
        if (progress >= 1 && onCollect) {
          onCollect()
        }
      }
    }
  })

  const handleClick = (e: any) => {
    e.stopPropagation()
    if (!isSelected) {
      setIsSelected(true)
      setIsDisappearing(true)
      console.log('🎉 Magna Bowl recogida! Desapareciendo...')
    }
  }

  return (
    <group ref={groupRef} position={position}>
      {/* Modelo del item - clickeable */}
      <group
        onClick={handleClick}
        onPointerOver={() => !isSelected && setIsHovered(true)}
        onPointerOut={() => setIsHovered(false)}
      >
        <primitive object={scene} />
        
        {/* Outline cuando está hover o seleccionado */}
        {(isHovered || isSelected) && !isDisappearing && (
          <mesh>
            <sphereGeometry args={[1.5, 16, 16]} />
            <meshBasicMaterial
              color={isSelected ? "#00ff00" : "#ffff00"}
              wireframe
              transparent
              opacity={0.3}
            />
          </mesh>
        )}
      </group>
    </group>
  )
}
