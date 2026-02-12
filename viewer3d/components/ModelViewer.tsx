'use client'

import { useGLTF, useAnimations } from '@react-three/drei'
import { useEffect, useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useSceneStore } from '@/store/scene-store'

interface ModelViewerProps {
  modelPath: string
}

export default function ModelViewer({ modelPath }: ModelViewerProps) {
  const group = useRef<THREE.Group>(null)
  const { scene, animations } = useGLTF(modelPath)
  const { actions, names } = useAnimations(animations, group)
  
  const autoRotate = useSceneStore((state) => state.autoRotate)
  const setAutoRotate = useSceneStore((state) => state.setAutoRotate)
  const currentAnimation = useSceneStore((state) => state.currentAnimation)
  const setAnimationPlaying = useSceneStore((state) => state.setAnimationPlaying)

  // Reproducir animaciones si existen
  useEffect(() => {
    if (names.length > 0 && actions[names[currentAnimation]]) {
      console.log('🎬 Animaciones disponibles:', names)
      const action = actions[names[currentAnimation]]
      action?.reset().play()
      setAnimationPlaying(true)
    }
  }, [actions, names, currentAnimation, setAnimationPlaying])

  // Auto-rotación suave (solo si no hay animación activa)
  useFrame((state, delta) => {
    if (group.current && autoRotate && names.length === 0) {
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

      // Enable shadows y fix materials
      scene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh
          child.castShadow = true
          child.receiveShadow = true
          
          // Fix material uniforms
          if (mesh.material) {
            const material = mesh.material as THREE.Material
            if ((material as any).needsUpdate !== undefined) {
              (material as any).needsUpdate = true
            }
            
            // Si es MeshStandardMaterial, asegurar que tenga valores por defecto
            if ((material as any).type === 'MeshStandardMaterial') {
              const stdMat = material as THREE.MeshStandardMaterial
              if (stdMat.roughness === undefined) stdMat.roughness = 0.5
              if (stdMat.metalness === undefined) stdMat.metalness = 0.5
            }
          }
        }
      })

      // Calcular estadísticas del modelo
      let totalVertices = 0
      let totalTriangles = 0
      scene.traverse((child) => {
        if ((child as THREE.Mesh).isMesh) {
          const mesh = child as THREE.Mesh
          if (mesh.geometry) {
            const positions = mesh.geometry.attributes.position
            if (positions) {
              totalVertices += positions.count
            }
            if (mesh.geometry.index) {
              totalTriangles += mesh.geometry.index.count / 3
            }
          }
        }
      })

      console.log('📦 Modelo cargado:', {
        dimensiones: size,
        centro: center,
        escala: scale,
        animaciones: names.length,
        vertices: totalVertices,
        triangulos: Math.floor(totalTriangles)
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
