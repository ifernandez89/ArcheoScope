'use client'

import { useState, useRef, Suspense, useEffect } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { Group } from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Escena de Teotihuacán - OPTIMIZADA
 * 
 * Optimizaciones aplicadas:
 * - Eliminado .clone() de modelos (muy costoso)
 * - useFrame solo ejecuta cuando es necesario
 * - Fade-in aplicado correctamente a materiales
 * - Reducción de re-renders innecesarios
 */

interface TeotihuacanSceneProps {
  avatarPositionRef?: React.RefObject<THREE.Vector3>
}

export default function TeotihuacanScene({ avatarPositionRef }: TeotihuacanSceneProps) {
  return (
    <Suspense fallback={<LoadingTeotihuacan />}>
      <TeotihuacanSceneContent avatarPositionRef={avatarPositionRef} />
    </Suspense>
  )
}

function TeotihuacanSceneContent({ avatarPositionRef }: TeotihuacanSceneProps) {
  // Cargar modelos
  const kukulkanModel = useGLTF(getAssetPath('/kukulkan.glb'))
  const aztecTempleModel = useGLTF(getAssetPath('/aztec_temple.glb'))
  const calendarioModel = useGLTF(getAssetPath('/calendario_maya.glb'))
  const quetzalcoatlModel = useGLTF(getAssetPath('/quetzalcoatl.glb'))
  
  // Estados (solo los que necesitan re-render)
  const [isCalendarioSpinning, setIsCalendarioSpinning] = useState(true)
  const [showQuetzalcoatl, setShowQuetzalcoatl] = useState(false)
  
  // Usar ref para opacidad (evita re-renders cada frame)
  const quetzalcoatlOpacityRef = useRef(0)
  
  const calendarioRef = useRef<Group>(null)
  const quetzalcoatlRef = useRef<Group>(null)
  
  // Cache de meshes para evitar traverse cada frame
  const cachedQuetzalcoatlMeshes = useRef<THREE.Mesh[]>([])
  const meshesCached = useRef(false)
  
  // 🎼 Activar arquitectura de Teotihuacán
  useEffect(() => {
    import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
      const harmonia = getHarmoniaMundi()
      if (harmonia.isEnabled()) {
        harmonia.activateArchitecture('teotihuacan')
      }
    })
    
    return () => {
      import('@/systems/HarmoniaMundiSystem').then(({ getHarmoniaMundi }) => {
        const harmonia = getHarmoniaMundi()
        harmonia.deactivateArchitecture('teotihuacan')
      })
    }
  }, [])
  
  // Rotación del calendario - SOLO si está girando
  useFrame((state, delta) => {
    if (calendarioRef.current && isCalendarioSpinning) {
      calendarioRef.current.rotation.y += delta * 0.5
    }
    
    // Fade-in de Quetzalcoatl - SOLO si está apareciendo (usa ref, no setState)
    if (showQuetzalcoatl && quetzalcoatlOpacityRef.current < 1 && quetzalcoatlRef.current) {
      quetzalcoatlOpacityRef.current = Math.min(quetzalcoatlOpacityRef.current + delta * 0.3, 1)
      
      // Cachear meshes una sola vez (evita traverse cada frame)
      if (!meshesCached.current) {
        cachedQuetzalcoatlMeshes.current = []
        quetzalcoatlRef.current.traverse((child: any) => {
          if (child.isMesh && child.material) {
            child.material.transparent = true
            cachedQuetzalcoatlMeshes.current.push(child)
          }
        })
        meshesCached.current = true
      }
      
      // Aplicar opacidad usando cache
      for (const mesh of cachedQuetzalcoatlMeshes.current) {
        if (mesh.material && !Array.isArray(mesh.material)) {
          (mesh.material as THREE.MeshStandardMaterial).opacity = quetzalcoatlOpacityRef.current
        }
      }
    }
  })
  
  // Handler para click en calendario
  const handleCalendarioClick = () => {
    if (isCalendarioSpinning) {
      setIsCalendarioSpinning(false)
      setTimeout(() => setShowQuetzalcoatl(true), 1000)
    }
  }
  
  return (
    <group>
      {/* Templo de Kukulkán - SIN CLONE (30m altura) */}
      <group position={[0, 0, -20]}>
        <primitive object={kukulkanModel.scene} scale={0.3} />
      </group>
      
      {/* Calendario Maya - SIN CLONE */}
      <group 
        ref={calendarioRef}
        position={[0, 10, -20]}
        onClick={handleCalendarioClick}
        onPointerOver={(e) => {
          e.stopPropagation()
          document.body.style.cursor = 'pointer'
        }}
        onPointerOut={(e) => {
          e.stopPropagation()
          document.body.style.cursor = 'default'
        }}
      >
        <primitive object={calendarioModel.scene} scale={1.5} />
      </group>
      
      {/* Templo Mayor Azteca - SIN CLONE (60m altura) */}
      <group position={[25, 0, 10]} rotation={[0, -Math.PI / 3, 0]}>
        <primitive object={aztecTempleModel.scene} scale={0.26} />
      </group>
      
      {/* Quetzalcoatl - SIN CLONE, con fade-in optimizado */}
      {showQuetzalcoatl && (
        <group ref={quetzalcoatlRef} position={[-15, 0, -10]} rotation={[0, Math.PI / 4, 0]}>
          <primitive object={quetzalcoatlModel.scene} scale={5} />
        </group>
      )}
      
      {/* Iluminación */}
      <ambientLight intensity={0.6} />
      <directionalLight position={[10, 15, 5]} intensity={1.0} />
      <directionalLight position={[-10, 10, -5]} intensity={0.4} />
      <pointLight position={[0, 10, -20]} intensity={1.2} color="#ffd700" distance={15} />
    </group>
  )
}

function LoadingTeotihuacan() {
  return (
    <Html center>
      <div style={{
        background: 'rgba(0, 0, 0, 0.8)',
        padding: '20px 40px',
        borderRadius: '12px',
        color: 'white',
        fontFamily: 'system-ui, sans-serif',
        textAlign: 'center',
        border: '2px solid rgba(255, 215, 0, 0.3)'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>🏛️</div>
        <div>Cargando Teotihuacán...</div>
      </div>
    </Html>
  )
}

// Precargar modelos
useGLTF.preload(getAssetPath('/kukulkan.glb'))
useGLTF.preload(getAssetPath('/aztec_temple.glb'))
useGLTF.preload(getAssetPath('/calendario_maya.glb'))
useGLTF.preload(getAssetPath('/quetzalcoatl.glb'))
