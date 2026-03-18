'use client'

import { useState, useRef } from 'react'
import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Escena de Teotihuacán
 * Pirámide del Sol, Templo Mayor Azteca, Calendario Maya y Quetzalcoatl
 * 
 * Datos reales:
 * - Pirámide del Sol: 65m altura, 225m base (similar a Giza pero más pequeña)
 * - Templo Mayor: ~45m altura
 * 
 * Escala Giza para referencia: Gran Pirámide usa escala ~0.08
 * Pirámide del Sol: ~65m vs 146m de Giza = 44% del tamaño
 */

interface TeotihuacanSceneProps {
  avatarPositionRef?: React.RefObject<THREE.Vector3>
}

export default function TeotihuacanScene({ avatarPositionRef }: TeotihuacanSceneProps) {
  // Cargar modelos
  const piramideSolModel = useGLTF(getAssetPath('/piramide_del_sol.glb'))
  const aztecTempleModel = useGLTF(getAssetPath('/aztec_temple.glb'))
  const calendarioModel = useGLTF(getAssetPath('/calendario_maya.glb'))
  const quetzalcoatlModel = useGLTF(getAssetPath('/quetzalcoatl.glb'))
  
  console.log('🏛️ Escena de Teotihuacán cargada')
  
  // Estados
  const [isCalendarioSpinning, setIsCalendarioSpinning] = useState(true)
  const [showQuetzalcoatl, setShowQuetzalcoatl] = useState(false)
  const [quetzalcoatlOpacity, setQuetzalcoatlOpacity] = useState(0)
  
  const calendarioRef = useRef<THREE.Group>(null)
  const quetzalcoatlRef = useRef<THREE.Group>(null)
  
  // Rotación del calendario
  useFrame((state, delta) => {
    if (calendarioRef.current && isCalendarioSpinning) {
      calendarioRef.current.rotation.y += delta * 0.5 // Velocidad de rotación
    }
    
    // Fade-in de Quetzalcoatl
    if (showQuetzalcoatl && quetzalcoatlOpacity < 1) {
      setQuetzalcoatlOpacity(prev => Math.min(prev + delta * 0.3, 1))
    }
  })
  
  // Handler para click en calendario
  const handleCalendarioClick = () => {
    if (isCalendarioSpinning) {
      setIsCalendarioSpinning(false)
      console.log('🗓️ Calendario detenido - Iniciando misión de Teotihuacán')
      
      // Aparecer Quetzalcoatl después de 1 segundo
      setTimeout(() => {
        setShowQuetzalcoatl(true)
      }, 1000)
    }
  }
  
  return (
    <group>
      {/* Pirámide del Sol - Estructura principal, más grande y visible */}
      <group position={[0, 0, -20]} rotation={[0, 0, 0]}>
        <primitive 
          object={piramideSolModel.scene.clone()} 
          scale={0.08}
        />
      </group>
      
      {/* Calendario Maya - Flotando sobre la punta de la Pirámide del Sol */}
      <group 
        ref={calendarioRef}
        position={[0, 8, -20]} // Ajustado para estar sobre la pirámide
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
        <primitive 
          object={calendarioModel.scene.clone()} 
          scale={1.5}
        />
      </group>
      
      {/* Templo Mayor Azteca - Más cerca del jugador */}
      <group position={[20, 0, 5]} rotation={[0, -Math.PI / 4, 0]}>
        <primitive 
          object={aztecTempleModel.scene.clone()} 
          scale={0.05}
        />
      </group>
      
      {/* Quetzalcoatl - Aparece después de detener el calendario */}
      {showQuetzalcoatl && (
        <group position={[-15, 0, -10]} rotation={[0, Math.PI / 4, 0]}>
          <primitive 
            object={quetzalcoatlModel.scene.clone()} 
            scale={5}
          />
          {/* Material con transparencia para fade-in */}
          <meshStandardMaterial 
            transparent 
            opacity={quetzalcoatlOpacity}
            attach="material"
          />
        </group>
      )}
      
      {/* Iluminación específica para la escena */}
      <ambientLight intensity={0.6} />
      <directionalLight position={[10, 15, 5]} intensity={1.0} castShadow />
      <directionalLight position={[-10, 10, -5]} intensity={0.4} />
      
      {/* Luz especial para el calendario */}
      <pointLight position={[0, 10, -20]} intensity={1.2} color="#ffd700" distance={15} />
    </group>
  )
}

// Precargar modelos
useGLTF.preload(getAssetPath('/piramide_del_sol.glb'))
useGLTF.preload(getAssetPath('/aztec_temple.glb'))
useGLTF.preload(getAssetPath('/calendario_maya.glb'))
useGLTF.preload(getAssetPath('/quetzalcoatl.glb'))
