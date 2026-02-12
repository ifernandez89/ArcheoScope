'use client'

import { useGLTF, useAnimations } from '@react-three/drei'
import { useEffect, useRef, forwardRef } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useSceneStore } from '@/store/scene-store'

interface ModelViewerProps {
  modelPath: string
}

const ModelViewer = forwardRef<THREE.Group, ModelViewerProps>(
  function ModelViewer({ modelPath }, ref) {
  const group = useRef<THREE.Group>(null)
  const { scene, animations } = useGLTF(modelPath)
  const { actions, names } = useAnimations(animations, group)
  
  // Usar ref externo si se proporciona, sino usar interno
  const actualRef = (ref as React.RefObject<THREE.Group>) || group
  
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

  // Auto-rotación suave SOLO en eje Y (horizontal) si está activada
  useFrame((state, delta) => {
    if (actualRef.current && autoRotate && names.length === 0) {
      // Solo rotar en el eje Y para mantener el modelo vertical
      actualRef.current.rotation.y += delta * 0.3
    }
  })

  // Centrar y escalar el modelo, manteniéndolo vertical
  useEffect(() => {
    if (scene) {
      // Calcular bounding box
      const box = new THREE.Box3().setFromObject(scene)
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())

      // Centrar horizontalmente, pero mantener base en el suelo
      scene.position.x = -center.x
      scene.position.y = -box.min.y  // Base pegada al suelo (y=0)
      scene.position.z = -center.z

      // Escalar para que quepa en la vista
      const maxDim = Math.max(size.x, size.y, size.z)
      const scale = 2 / maxDim
      scene.scale.setScalar(scale)
      
      // Asegurar que el modelo esté completamente vertical (sin rotación en X o Z)
      scene.rotation.set(0, 0, 0)

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

  // Toggle auto-rotate con click (desactivado por defecto)
  const handleClick = () => {
    setAutoRotate(!autoRotate)
    console.log('🔄 Auto-rotación horizontal:', !autoRotate ? 'ON' : 'OFF')
  }

  return (
    <group 
      ref={actualRef} 
      onClick={handleClick}
      // Mantener el grupo siempre vertical
      rotation={[0, 0, 0]}
    >
      <primitive object={scene} />
    </group>
  )
})

export default ModelViewer

import { getAssetPath } from '@/lib/paths'

// Precargar el modelo
useGLTF.preload(getAssetPath('/warrior.glb'))
