'use client'

import { useState, useRef, Suspense, useEffect, useMemo } from 'react'
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
  onQuetzalcoatlClick?: () => void
  onQuetzalcoatlAppear?: () => void
  onCornCollect?: () => void
  cornCollected?: boolean
  showCornSeed?: boolean
}

export default function TeotihuacanScene({ 
  avatarPositionRef,
  onQuetzalcoatlClick,
  onQuetzalcoatlAppear,
  onCornCollect,
  cornCollected,
  showCornSeed
}: TeotihuacanSceneProps) {
  return (
    <Suspense fallback={<LoadingTeotihuacan />}>
      <TeotihuacanSceneContent 
        avatarPositionRef={avatarPositionRef}
        onQuetzalcoatlClick={onQuetzalcoatlClick}
        onQuetzalcoatlAppear={onQuetzalcoatlAppear}
        onCornCollect={onCornCollect}
        cornCollected={cornCollected}
        showCornSeed={showCornSeed}
      />
    </Suspense>
  )
}

function TeotihuacanSceneContent({ 
  avatarPositionRef,
  onQuetzalcoatlClick,
  onQuetzalcoatlAppear,
  onCornCollect,
  cornCollected,
  showCornSeed
}: TeotihuacanSceneProps) {
  // Cargar modelos
  const kukulkanModel = useGLTF(getAssetPath('/kukulkan.glb'))
  const aztecTempleModel = useGLTF(getAssetPath('/aztec_temple.glb'))
  const calendarioModel = useGLTF(getAssetPath('/calendario_maya.glb'))
  const quetzalcoatlModel = useGLTF(getAssetPath('/quetzalcoatl.glb'))
  const maizModel = useGLTF(getAssetPath('/maiz.glb'))
  
  // Estados (solo los que necesitan re-render)
  const [isCalendarioSpinning, setIsCalendarioSpinning] = useState(true)
  const [showQuetzalcoatl, setShowQuetzalcoatl] = useState(false)
  const [isQuetzalcoatlHovered, setIsQuetzalcoatlHovered] = useState(false)
  const [isCornHovered, setIsCornHovered] = useState(false)
  const [isCornDisappearing, setIsCornDisappearing] = useState(false)
  
  // Usar ref para opacidad (evita re-renders cada frame)
  const quetzalcoatlOpacityRef = useRef(0)
  const cornDisappearTimer = useRef(0)
  
  const calendarioRef = useRef<Group>(null)
  const quetzalcoatlRef = useRef<Group>(null)
  const cornRef = useRef<Group>(null)
  
  // Cache de meshes para evitar traverse cada frame
  const cachedQuetzalcoatlMeshes = useRef<THREE.Mesh[]>([])
  const cachedCornMeshes = useRef<THREE.Mesh[]>([])
  const meshesCached = useRef(false)
  const cornMeshesCached = useRef(false)
  
  // Clonar escena del maíz para independencia
  const clonedCornScene = useMemo(() => {
    const cloned = maizModel.scene.clone(true)
    cloned.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh
        if (mesh.material) {
          mesh.material = (mesh.material as THREE.Material).clone()
          const mat = mesh.material as THREE.MeshStandardMaterial
          mat.transparent = true
          mat.opacity = 1
          mat.needsUpdate = true
        }
      }
    })
    return cloned
  }, [maizModel.scene])
  
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
  
  // Rotación del calendario y seguimiento de mirada de Quetzalcoatl
  useFrame(({ camera }, delta) => {
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
    
    // Quetzalcoatl sigue con la mirada al jugador (solo eje Y)
    if (showQuetzalcoatl && quetzalcoatlRef.current && quetzalcoatlOpacityRef.current > 0) {
      const pos = quetzalcoatlRef.current.position
      const dx = camera.position.x - pos.x
      const dz = camera.position.z - pos.z
      quetzalcoatlRef.current.rotation.y = Math.atan2(dx, dz)
    }
    
    // Animación de desaparición del maíz
    if (isCornDisappearing && cornRef.current) {
      cornDisappearTimer.current += delta
      const progress = Math.min(cornDisappearTimer.current / 1.0, 1)
      
      cornRef.current.scale.setScalar(2 * (1 + progress * 0.5))
      
      // Cache meshes del maíz
      if (!cornMeshesCached.current) {
        cachedCornMeshes.current = []
        cornRef.current.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            cachedCornMeshes.current.push(child as THREE.Mesh)
          }
        })
        cornMeshesCached.current = true
      }
      
      // Aplicar fade
      for (const mesh of cachedCornMeshes.current) {
        if (mesh.material) {
          const material = mesh.material as THREE.MeshStandardMaterial
          material.transparent = true
          material.opacity = 1 - progress
        }
      }
      
      if (progress >= 1 && onCornCollect) {
        onCornCollect()
      }
    }
  })
  
  // Handler para click en calendario
  const handleCalendarioClick = () => {
    if (isCalendarioSpinning) {
      setIsCalendarioSpinning(false)
      setTimeout(() => {
        setShowQuetzalcoatl(true)
        if (onQuetzalcoatlAppear) {
          onQuetzalcoatlAppear()
        }
      }, 1000)
    }
  }
  
  // Handler para click en Quetzalcoatl
  const handleQuetzalcoatlClick = (e: any) => {
    if (showQuetzalcoatl && quetzalcoatlOpacityRef.current > 0.5 && onQuetzalcoatlClick) {
      e.stopPropagation()
      onQuetzalcoatlClick()
    }
  }
  
  // Handler para click en maíz
  const handleCornClick = (e: any) => {
    if (showCornSeed && !cornCollected && !isCornDisappearing) {
      e.stopPropagation()
      setIsCornDisappearing(true)
      console.log('🌽 Semilla de maíz recogida!')
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
      
      {/* Quetzalcoatl - Clickeable, con fade-in optimizado */}
      {showQuetzalcoatl && (
        <group 
          ref={quetzalcoatlRef} 
          position={[-15, 0, -10]} 
          rotation={[0, Math.PI / 4, 0]}
          onClick={handleQuetzalcoatlClick}
          onPointerOver={() => {
            if (quetzalcoatlOpacityRef.current > 0.5) {
              setIsQuetzalcoatlHovered(true)
              document.body.style.cursor = 'pointer'
            }
          }}
          onPointerOut={() => {
            setIsQuetzalcoatlHovered(false)
            document.body.style.cursor = 'default'
          }}
        >
          <primitive object={quetzalcoatlModel.scene} scale={5} />
          
          {/* Outline cuando está hover */}
          {isQuetzalcoatlHovered && quetzalcoatlOpacityRef.current > 0.5 && (
            <mesh position={[0, 2, 0]}>
              <sphereGeometry args={[3, 16, 16]} />
              <meshBasicMaterial
                color="#7cfc00"
                wireframe
                transparent
                opacity={0.3}
              />
            </mesh>
          )}
        </group>
      )}
      
      {/* Semilla de Maíz - Aparece después de hablar con Quetzalcoatl */}
      {showCornSeed && !cornCollected && (
        <group
          ref={cornRef}
          position={[10, 0.5, 5]}
          onClick={handleCornClick}
          onPointerOver={() => {
            if (!isCornDisappearing) {
              setIsCornHovered(true)
              document.body.style.cursor = 'pointer'
            }
          }}
          onPointerOut={() => {
            setIsCornHovered(false)
            document.body.style.cursor = 'default'
          }}
        >
          <primitive object={clonedCornScene} scale={2} />
          
          {/* Outline cuando está hover */}
          {isCornHovered && !isCornDisappearing && (
            <mesh>
              <sphereGeometry args={[1.5, 16, 16]} />
              <meshBasicMaterial
                color="#ffff00"
                wireframe
                transparent
                opacity={0.3}
              />
            </mesh>
          )}
          
          {/* Luz para destacar el maíz */}
          <pointLight color="#ffd700" intensity={2} distance={5} />
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
useGLTF.preload(getAssetPath('/maiz.glb'))
