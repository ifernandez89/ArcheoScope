'use client'

import { useEffect, useRef, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { getAnomalyManager } from '../systems/AnomalyManager'
import { getResonanceFieldSystem } from '../systems/ResonanceFieldSystem'
import { getClimateAudio } from '../systems/ClimateAudioSystem'

interface ResonanceDemoProps {
  playerPosition?: THREE.Vector3
  enabled?: boolean
}

/**
 * ResonanceDemo - Demo simple de campo de resonancia
 * 
 * Crea 1 anomalía visible con:
 * - Radio visible sutil
 * - Sonido que cambia gradualmente
 * - Shader ondulante leve (opcional)
 */
export default function ResonanceDemo({ 
  playerPosition, 
  enabled = true 
}: ResonanceDemoProps) {
  const anomalyManager = getAnomalyManager()
  const resonanceField = getResonanceFieldSystem()
  const climateAudio = getClimateAudio()
  const [initialized, setInitialized] = useState(false)
  
  // Inicializar anomalía de demo
  useEffect(() => {
    if (!enabled || initialized) return
    
    // Crear anomalía de demo
    anomalyManager.addAnomaly({
      id: 'demo-anomaly',
      position: new THREE.Vector3(10, 0, 10), // 10m adelante y a la derecha
      radius: 15, // Radio de 15 metros
      intensity: 0.7, // Intensidad moderada
      frequency: 0.5, // Oscilación lenta (0.5 Hz)
      active: true
    })
    
    // Habilitar resonancia en audio
    climateAudio.enableResonance({
      baseFrequency: 0.5,
      intensity: 0.7,
      harmonics: [2, 3, 4]
    })
    
    console.log('🌀 Demo de resonancia iniciada')
    setInitialized(true)
    
    // Cleanup
    return () => {
      anomalyManager.removeAnomaly('demo-anomaly')
      climateAudio.disableResonance()
      console.log('🌀 Demo de resonancia detenida')
    }
  }, [enabled, initialized, anomalyManager, climateAudio])
  
  // Actualizar cada frame
  useFrame((state, delta) => {
    if (!enabled || !initialized) return
    
    // Actualizar sistema de resonancia
    resonanceField.update(delta, playerPosition)
  })
  
  if (!enabled || !initialized) return null
  
  return (
    <>
      {/* Visualización de la anomalía */}
      <AnomalyVisualization />
      
      {/* HUD de debug */}
      <ResonanceHUD />
    </>
  )
}

/**
 * Visualización de anomalía (esfera sutil)
 */
function AnomalyVisualization() {
  const anomalyManager = getAnomalyManager()
  const meshRef = useRef<THREE.Mesh>(null)
  
  useFrame((state) => {
    if (!meshRef.current) return
    
    const anomalies = anomalyManager.getAllAnomalies()
    if (anomalies.length === 0) return
    
    const anomaly = anomalies[0]
    
    // Posicionar en la anomalía
    meshRef.current.position.copy(anomaly.position)
    
    // Escala pulsante
    const time = anomalyManager.getTime()
    const pulse = Math.sin(time * anomaly.frequency) * 0.1 + 1
    meshRef.current.scale.setScalar(pulse)
    
    // Opacidad basada en intensidad
    const material = meshRef.current.material as THREE.MeshBasicMaterial
    material.opacity = 0.1 + Math.abs(Math.sin(time * anomaly.frequency)) * 0.1
  })
  
  const anomalies = anomalyManager.getAllAnomalies()
  if (anomalies.length === 0) return null
  
  const anomaly = anomalies[0]
  
  return (
    <mesh ref={meshRef} position={anomaly.position}>
      <sphereGeometry args={[anomaly.radius, 32, 32]} />
      <meshBasicMaterial 
        color="#667eea" 
        transparent 
        opacity={0.15}
        wireframe
      />
    </mesh>
  )
}

/**
 * HUD de debug para mostrar estado de resonancia
 */
function ResonanceHUD() {
  const resonanceField = getResonanceFieldSystem()
  const [state, setState] = useState({
    resonance: 0,
    state: 'neutral' as 'harmonic' | 'dissonant' | 'neutral',
    description: ''
  })
  
  useFrame(() => {
    // Actualizar cada 10 frames
    if (Math.random() < 0.1) {
      setState(resonanceField.getStateDescription())
    }
  })
  
  return (
    <div style={{
      position: 'absolute',
      bottom: '80px',
      left: '20px',
      zIndex: 1001,
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(10px)',
      padding: '12px 16px',
      borderRadius: '8px',
      border: '1px solid rgba(255,255,255,0.2)',
      color: 'white',
      fontSize: '12px',
      fontFamily: 'monospace',
      minWidth: '250px'
    }}>
      <div style={{ marginBottom: '8px', fontWeight: 'bold', color: '#667eea' }}>
        🌊 Campo de Resonancia
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
        <div>
          <span style={{ color: '#888' }}>Valor:</span>{' '}
          <span style={{ 
            color: state.resonance > 0 ? '#4ade80' : state.resonance < 0 ? '#f87171' : '#888'
          }}>
            {state.resonance.toFixed(3)}
          </span>
        </div>
        
        <div>
          <span style={{ color: '#888' }}>Estado:</span>{' '}
          <span style={{ 
            color: state.state === 'harmonic' ? '#4ade80' : 
                   state.state === 'dissonant' ? '#f87171' : '#888'
          }}>
            {state.state}
          </span>
        </div>
        
        <div style={{ 
          marginTop: '4px', 
          fontSize: '10px', 
          color: '#aaa',
          fontStyle: 'italic'
        }}>
          {state.description}
        </div>
      </div>
      
      {/* Barra visual */}
      <div style={{
        marginTop: '8px',
        height: '4px',
        background: 'rgba(255,255,255,0.1)',
        borderRadius: '2px',
        overflow: 'hidden'
      }}>
        <div style={{
          height: '100%',
          width: `${Math.abs(state.resonance) * 100}%`,
          background: state.resonance > 0 ? '#4ade80' : '#f87171',
          transition: 'width 0.3s ease'
        }} />
      </div>
    </div>
  )
}
