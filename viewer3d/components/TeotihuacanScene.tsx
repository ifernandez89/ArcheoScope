'use client'

import { useState, useRef, Suspense } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { Group } from 'three'
import { getAssetPath } from '@/lib/paths'

/**
 * Escena de Teotihuacán
 * Templo de Kukulkán (Chichén Itzá), Templo Mayor Azteca, Calendario Maya y Quetzalcoatl
 * 
 * Proporciones reales:
 * - Templo de Kukulkán: 30m altura, 55x55m base (escala 0.3)
 *   • Precisión astronómica: 91 escalones × 4 lados + 1 = 365 días
 *   • Fenómeno de equinoccio: sombra de serpiente descendiendo
 * 
 * - Templo Mayor Azteca: 60m altura, 80m base (escala 0.6 - el doble que Kukulkán)
 *   • Doble templo ritual dedicado a Tláloc y Huitzilopochtli
 *   • Centro ceremonial de Tenochtitlán
 * 
 * Relación de tamaños: Templo Mayor es 2x más alto que Kukulkán (60m vs 30m)
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
  
  console.log('🏛️ Escena de Teotihuacán cargada')
  
  // Estados
  const [isCalendarioSpinning, setIsCalendarioSpinning] = useState(true)
  const [showQuetzalcoatl, setShowQuetzalcoatl] = useState(false)
  const [quetzalcoatlOpacity, setQuetzalcoatlOpacity] = useState(0)
  
  const calendarioRef = useRef<Group>(null)
  const quetzalcoatlRef = useRef<Group>(null)
  
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
      {/* Templo de Kukulkán - Pirámide maya con precisión astronómica (30m altura, 55x55m base) */}
      <group position={[0, 0, -20]} rotation={[0, 0, 0]}>
        <primitive 
          object={kukulkanModel.scene.clone()} 
          scale={0.3} // Escala base para 30m
        />
      </group>
      
      {/* Calendario Maya - Flotando sobre la punta de Kukulkán */}
      <group 
        ref={calendarioRef}
        position={[0, 10, -20]} // Ajustado a la nueva altura de Kukulkán (30m)
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
      
      {/* Templo Mayor Azteca - El doble de alto que Kukulkán (60m altura, 80m base) */}
      <group position={[25, 0, 10]} rotation={[0, -Math.PI / 3, 0]}>
        <primitive 
          object={aztecTempleModel.scene.clone()} 
          scale={0.26}
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

/**
 * 🔄 Loading placeholder para Teotihuacán
 */
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
