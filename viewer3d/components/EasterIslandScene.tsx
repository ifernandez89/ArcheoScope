'use client'

import { useRef, Suspense } from 'react'
import { useGLTF, Html } from '@react-three/drei'
import { Vector3 } from 'three'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'
import { getAssetPath } from '@/lib/paths'
import EasterIslandDialogue from './EasterIslandDialogue'

/**
 * Escena de Isla de Pascua (Rapa Nui)
 * Moai y Atlante enfrentados "charlando"
 * Modelos optimizados con compresión Draco
 * Sistema de diálogo sobre la red energética planetaria
 */

/**
 * 🔄 Loading placeholder para Isla de Pascua
 */
function LoadingEasterIsland() {
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
        <div style={{ fontSize: '48px', marginBottom: '10px' }}>🗿</div>
        <div>Cargando Isla de Pascua...</div>
      </div>
    </Html>
  )
}

interface EasterIslandSceneProps {
  avatarPositionRef?: React.RefObject<Vector3>
}

export default function EasterIslandScene({ avatarPositionRef }: EasterIslandSceneProps) {
  return (
    <Suspense fallback={<LoadingEasterIsland />}>
      <EasterIslandSceneContent avatarPositionRef={avatarPositionRef} />
    </Suspense>
  )
}

function EasterIslandSceneContent({ avatarPositionRef }: EasterIslandSceneProps) {
  // Cargar modelos (optimizados con Draco)
  const moaiModel = useGLTF(getAssetPath('/moai.glb'))
  const atlanteModel = useGLTF(getAssetPath('/atlante.glb'))
  
  // Posiciones para el sistema de diálogo
  const moaiPosition = new Vector3(-4, 3, 0)
  const atlantePosition = new Vector3(4, 2, 0)
  
  return (
    <group>
      {/* Moai - Lado izquierdo, girado 30° hacia el noroeste desde la dirección original, elevado 3m */}
      <group position={[-4, 3, 0]} rotation={[0, Math.PI / 4 - Math.PI / 6, 0]}>
        <primitive 
          object={moaiModel.scene.clone()} 
          scale={5}
        />
      </group>
      
      {/* Atlante - Lado derecho, girado 45° hacia el este desde la dirección original, elevado 2m */}
      <group position={[4, 2, 0]} rotation={[0, -Math.PI / 4 + Math.PI / 4, 0]}>
        <primitive 
          object={atlanteModel.scene.clone()} 
          scale={5}
        />
      </group>
      
      {/* Sistema de diálogo entre Moai y Atlante */}
      <EasterIslandDialogue
        moaiPosition={moaiPosition}
        atlantePosition={atlantePosition}
        enabled={true}
      />
      
      {/* Luz ambiental para iluminar la escena */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={0.8} />
    </group>
  )
}

// Precargar modelos
useGLTF.preload(getAssetPath('/moai.glb'))
useGLTF.preload(getAssetPath('/atlante.glb'))
