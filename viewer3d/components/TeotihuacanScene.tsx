'use client'

import { useState, useRef, Suspense, useEffect, useMemo } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { Group } from 'three'
import { getAssetPath } from '@/lib/paths'
import CropCircle from './CropCircle'
import { isMissionCompleted } from '@/types/missionState'

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
  cornDropPosition?: {x: number, z: number} | null
  cornPlanted?: boolean
}

export default function TeotihuacanScene({ 
  avatarPositionRef,
  onQuetzalcoatlClick,
  onQuetzalcoatlAppear,
  onCornCollect,
  cornCollected,
  showCornSeed,
  cornDropPosition,
  cornPlanted
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
        cornDropPosition={cornDropPosition}
        cornPlanted={cornPlanted}
      />
    </Suspense>
  )
}

// Posiciones de las 20 plantas - nivel módulo para compartir entre componentes
const PLANT_POSITIONS: [number, number][] = [
  [-1.5, -1.5], [-0.5, -1.5], [0.5, -1.5], [1.5, -1.5],
  [-1.5, -0.5], [-0.5, -0.5], [0.5, -0.5], [1.5, -0.5],
  [-1.5,  0.5], [-0.5,  0.5], [0.5,  0.5], [1.5,  0.5],
  [-1.5,  1.5], [-0.5,  1.5], [0.5,  1.5], [1.5,  1.5],
  [-1.0,  0.0], [ 1.0,  0.0], [0.0, -1.0], [0.0,  1.0],
]

function TeotihuacanSceneContent({ 
  avatarPositionRef,
  onQuetzalcoatlClick,
  onQuetzalcoatlAppear,
  onCornCollect,
  cornCollected,
  showCornSeed,
  cornDropPosition,
  cornPlanted
}: TeotihuacanSceneProps) {
  // Cargar modelos base (livianos: kukulkan 0.6MB, aztec 1.9MB, calendario 49.9MB)
  const kukulkanModel = useGLTF(getAssetPath('/kukulkan.glb'))
  const aztecTempleModel = useGLTF(getAssetPath('/aztec_temple.glb'))
  const calendarioModel = useGLTF(getAssetPath('/calendario_maya.glb'))
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
  
  // Verificar si la misión está completa para el Crop Circle
  const missionDone = useMemo(() => isMissionCompleted('teotihuacan', 'plant_corn'), [cornPlanted])
  
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
  
  // Resetear estado de desaparición cuando el maíz vuelve al piso
  useEffect(() => {
    if (showCornSeed && !cornCollected) {
      setIsCornDisappearing(false)
      cornDisappearTimer.current = 0
      
      // Restaurar opacidad usando cache si existe, sino traverse una vez
      if (cachedCornMeshes.current.length > 0) {
        for (const mesh of cachedCornMeshes.current) {
          if (mesh.material) {
            (mesh.material as THREE.MeshStandardMaterial).opacity = 1
          }
        }
      } else if (clonedCornScene) {
        clonedCornScene.traverse((child) => {
          if ((child as THREE.Mesh).isMesh && (child as THREE.Mesh).material) {
            ((child as THREE.Mesh).material as THREE.MeshStandardMaterial).opacity = 1
          }
        })
      }
      cornMeshesCached.current = false
      
      if (cornRef.current) {
        cornRef.current.scale.setScalar(2)
      }
    }
  }, [showCornSeed, cornCollected, clonedCornScene])
  
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
      
      {/* 💠 Crop Circle: Mandala Solar (Activación de Pirámide) */}
      <CropCircle 
        type="toroid" 
        position={[30, 2.4, 0]} 
        scale={22} 
        visible={missionDone} 
      />
      
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
      
      {/* Quetzalcoatl - se carga SOLO cuando el calendario se detiene (42.7MB diferido) */}
      {showQuetzalcoatl && (
        <Suspense fallback={null}>
          <QuetzalcoatlModel
            quetzalcoatlRef={quetzalcoatlRef}
            quetzalcoatlOpacityRef={quetzalcoatlOpacityRef}
            cachedQuetzalcoatlMeshes={cachedQuetzalcoatlMeshes}
            meshesCached={meshesCached}
            onQuetzalcoatlClick={handleQuetzalcoatlClick}
            setIsQuetzalcoatlHovered={setIsQuetzalcoatlHovered}
          />
        </Suspense>
      )}
      
      {/* Semilla de Maíz - Posición dinámica (donde cayó o posición inicial) */}
      {showCornSeed && !cornCollected && (
        <group
          ref={cornRef}
          position={[
            cornDropPosition?.x ?? 35, 
            1.0, 
            cornDropPosition?.z ?? 20
          ]}
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
      
      {/* Parche de tierra para plantar - 4m x 4m - Detrás del Templo Azteca hacia el oeste */}
      <group position={[60, 2.3, 0]}>
        {/* Base elevada de tierra */}
        <mesh position={[0, -0.05, 0]}>
          <boxGeometry args={[9, 0.2, 9]} />
          <meshStandardMaterial color="#8B4513" roughness={0.9} metalness={0} />
        </mesh>
        {/* Tierra marrón principal */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.06, 0]}>
          <planeGeometry args={[8, 8]} />
          <meshStandardMaterial color="#CD853F" roughness={1} metalness={0} />
        </mesh>
        {/* Surcos en la tierra */}
        {[-2.4, -0.8, 0.8, 2.4].map((z, i) => (
          <mesh key={i} position={[0, 0.08, z]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[7, 0.4]} />
            <meshStandardMaterial color="#8B4513" roughness={1} metalness={0} />
          </mesh>
        ))}
        
        {/* Planta de maíz cuando está plantado - carga diferida (1.5MB) */}
        {cornPlanted && (
          <Suspense fallback={null}>
            <CornPlantsModel />
          </Suspense>
        )}
      </group>
      
      {/* Iluminación */}
      <ambientLight intensity={0.6} />
      <directionalLight position={[10, 15, 5]} intensity={1.0} />
      <directionalLight position={[-10, 10, -5]} intensity={0.4} />
      <pointLight position={[0, 10, -20]} intensity={1.2} color="#ffd700" distance={15} />
    </group>
  )
}

// Subcomponente lazy: Quetzalcoatl (42.7MB) - se carga solo al detener el calendario
function QuetzalcoatlModel({ 
  quetzalcoatlRef,
  quetzalcoatlOpacityRef,
  cachedQuetzalcoatlMeshes,
  meshesCached,
  onQuetzalcoatlClick,
  setIsQuetzalcoatlHovered
}: {
  quetzalcoatlRef: React.RefObject<THREE.Group>
  quetzalcoatlOpacityRef: React.MutableRefObject<number>
  cachedQuetzalcoatlMeshes: React.MutableRefObject<THREE.Mesh[]>
  meshesCached: React.MutableRefObject<boolean>
  onQuetzalcoatlClick: (e: any) => void
  setIsQuetzalcoatlHovered: (v: boolean) => void
}) {
  const quetzalcoatlModel = useGLTF(getAssetPath('/quetzalcoatl.glb'))
  return (
    <group
      ref={quetzalcoatlRef}
      position={[-15, 0, -10]}
      rotation={[0, Math.PI / 4, 0]}
      onClick={onQuetzalcoatlClick}
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
    </group>
  )
}

// Subcomponente lazy: Plantas de maíz (1.5MB) - se cargan solo al plantar
function CornPlantsModel() {
  const plantaMaizModel = useGLTF(getAssetPath('/planta_maiz.glb'))
  const clonedPlants = useMemo(() => 
    PLANT_POSITIONS.map(() => plantaMaizModel.scene.clone(true))
  , [plantaMaizModel.scene])
  
  return (
    <>
      {PLANT_POSITIONS.map(([x, z], i) => (
        <group key={i} position={[x, 0.3, z]}>
          <primitive object={clonedPlants[i]} scale={0.8} />
        </group>
      ))}
      <pointLight color="#7cfc00" intensity={2} distance={6} position={[0, 2, 0]} />
    </>
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
// ELIMINADO: Los preloads se hacen solo cuando se entra a la escena
// useGLTF.preload(getAssetPath('/kukulkan.glb'))
// useGLTF.preload(getAssetPath('/aztec_temple.glb'))
// useGLTF.preload(getAssetPath('/calendario_maya.glb'))
// useGLTF.preload(getAssetPath('/quetzalcoatl.glb'))
// useGLTF.preload(getAssetPath('/maiz.glb'))
// useGLTF.preload(getAssetPath('/planta_maiz.glb'))
