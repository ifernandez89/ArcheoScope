'use client'

import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import { useRef, useState } from 'react'
import * as THREE from 'three'
import RealisticSolarSystem from './RealisticSolarSystem'
import MilkyWayBackground from './MilkyWayBackground'
import Stars from './Stars'
import CosmicResonanceDemo from './CosmicResonanceDemo'

/**
 * Escena de prueba para el Sistema Solar Realista
 * 
 * Usa astronomy-engine para calcular posiciones reales
 * según la fecha actual del sistema
 */

interface RealisticSolarSystemSceneProps {
  onLocationClick?: (lat: number, lon: number) => void
  markerPosition?: { lat: number, lon: number } | null
}

export default function RealisticSolarSystemScene({
  onLocationClick,
  markerPosition
}: RealisticSolarSystemSceneProps) {
  const sceneRef = useRef<THREE.Scene | null>(null)
  const [showWaves, setShowWaves] = useState(true)
  
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      {/* Instrucciones */}
      <div style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        zIndex: 1000,
        background: 'rgba(0, 0, 0, 0.8)',
        backdropFilter: 'blur(10px)',
        padding: '16px',
        borderRadius: '8px',
        border: '1px solid rgba(255,255,255,0.2)',
        color: 'white',
        fontSize: '12px',
        maxWidth: '300px'
      }}>
        <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '8px', color: '#fbbf24' }}>
          🌌 Sistema Solar con Posiciones Reales
        </div>
        <div style={{ marginBottom: '8px', color: '#888' }}>
          Usa <strong>astronomy-engine</strong> para calcular posiciones astronómicas reales según la fecha.
        </div>
        <div style={{ fontSize: '11px', color: '#666' }}>
          ✅ Posiciones reales por fecha<br/>
          ✅ Velocidades orbitales reales<br/>
          ✅ Time-scale configurable<br/>
          ✅ Sistema de Resonancia Cósmica<br/>
          ✅ Música de Kepler (Harmonices Mundi)<br/>
          ✅ Ondas sonoras visuales<br/>
          ❌ Distancias escaladas visualmente<br/>
          ❌ Tamaños artísticos
        </div>
      </div>
      
      <Canvas
        camera={{ position: [0, 300, 1200], fov: 50 }}
        style={{ background: '#000' }}
        onCreated={({ scene }) => {
          sceneRef.current = scene
        }}
      >
        <PerspectiveCamera makeDefault position={[0, 300, 1200]} fov={50} />
        <OrbitControls
          enableDamping
          dampingFactor={0.05}
          minDistance={50}
          maxDistance={150000}
          autoRotate={false}
        />
        
        {/* Fondo espacial */}
        <MilkyWayBackground />
        <Stars />
        
        {/* Sistema solar realista */}
        <RealisticSolarSystem 
          onLocationClick={onLocationClick}
          markerPosition={markerPosition}
          showWaves={showWaves}
        />
        
        {/* Iluminación */}
        <ambientLight intensity={0.3} />
      </Canvas>
      
      {/* 🌌 UI de Resonancia Cósmica */}
      {sceneRef.current && (
        <CosmicResonanceDemo 
          scene={sceneRef.current} 
          enabled={true}
          onToggleWaves={setShowWaves}
          showWaves={showWaves}
        />
      )}
    </div>
  )
}
