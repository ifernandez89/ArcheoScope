/**
 * 🌌 Cosmic Resonance Demo
 * 
 * Componente de demostración para el sistema de resonancia cósmica.
 * Muestra cómo integrar el sistema sin romper nada existente.
 * 
 * USO:
 * 1. Importar en tu escena principal
 * 2. Pasar la referencia de THREE.Scene
 * 3. El sistema se activa automáticamente si fue descubierto
 * 4. UI de control incluida
 */

'use client'

import { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { getCosmicResonance, type ResonanceEvent } from '@/systems/CosmicResonanceSystem'

interface CosmicResonanceDemoProps {
  scene: THREE.Scene
  enabled?: boolean
  onToggleWaves?: (show: boolean) => void
  showWaves?: boolean
}

export default function CosmicResonanceDemo({ scene, enabled = false, onToggleWaves, showWaves = true }: CosmicResonanceDemoProps) {
  const [isDiscovered, setIsDiscovered] = useState(false)
  const [isVisible, setIsVisible] = useState(true)
  const [activeEvents, setActiveEvents] = useState<ResonanceEvent[]>([])
  const [stats, setStats] = useState({
    celestialBodies: 0,
    activeAlignments: 0,
    totalEvents: 0
  })
  
  const cosmicRef = useRef(getCosmicResonance())
  const animationFrameRef = useRef<number>()
  const lastTimeRef = useRef(Date.now())
  
  // Inicializar sistema
  useEffect(() => {
    const cosmic = cosmicRef.current
    
    // Verificar si ya fue descubierto
    if (cosmic.isDiscovered()) {
      setIsDiscovered(true)
      cosmic.enable(scene)
    }
    
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [scene])
  
  // Loop de actualización
  useEffect(() => {
    if (!isDiscovered || !enabled) return
    
    const cosmic = cosmicRef.current
    
    const animate = () => {
      const now = Date.now()
      const deltaTime = (now - lastTimeRef.current) / 1000
      lastTimeRef.current = now
      
      // Actualizar sistema
      cosmic.update(deltaTime)
      
      // Actualizar estado
      setActiveEvents(cosmic.getActiveEvents())
      setStats(cosmic.getStats())
      
      animationFrameRef.current = requestAnimationFrame(animate)
    }
    
    animate()
    
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [isDiscovered, enabled])
  
  // Función para descubrir el sistema (llamar desde gameplay)
  const handleDiscover = () => {
    const cosmic = cosmicRef.current
    cosmic.discover()
    cosmic.enable(scene)
    setIsDiscovered(true)
    
    console.log('✨ Mapa Armónico del Sistema Solar descubierto!')
  }
  
  // Toggle visualización
  const handleToggleVisibility = () => {
    const cosmic = cosmicRef.current
    const newVisible = !isVisible
    cosmic.setVisualizationVisible(newVisible)
    setIsVisible(newVisible)
  }
  
  // Si no está descubierto, no mostrar nada
  if (!isDiscovered) {
    return (
      <div style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        padding: '10px',
        background: 'rgba(0,0,0,0.7)',
        borderRadius: '8px',
        color: 'white',
        fontSize: '12px'
      }}>
        <button
          onClick={handleDiscover}
          style={{
            padding: '8px 16px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            borderRadius: '6px',
            color: 'white',
            cursor: 'pointer',
            fontSize: '12px'
          }}
        >
          🌌 Descubrir Resonancia Cósmica
        </button>
      </div>
    )
  }
  
  // UI de control
  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: '320px',
      background: 'rgba(0, 0, 0, 0.85)',
      backdropFilter: 'blur(10px)',
      borderRadius: '12px',
      padding: '15px',
      color: 'white',
      fontSize: '13px',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      border: '1px solid rgba(255,255,255,0.1)'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '12px',
        paddingBottom: '10px',
        borderBottom: '1px solid rgba(255,255,255,0.1)'
      }}>
        <h3 style={{
          margin: 0,
          fontSize: '15px',
          fontWeight: 'bold'
        }}>
          🌌 Resonancia Cósmica
        </h3>
        
        <div style={{ display: 'flex', gap: '6px' }}>
          <button
            onClick={handleToggleVisibility}
            style={{
              padding: '4px 10px',
              background: isVisible ? 'rgba(67, 233, 123, 0.2)' : 'rgba(255,255,255,0.1)',
              border: isVisible ? '1px solid #43e97b' : '1px solid rgba(255,255,255,0.2)',
              borderRadius: '4px',
              color: 'white',
              cursor: 'pointer',
              fontSize: '11px'
            }}
          >
            {isVisible ? '👁️ Red' : '👁️‍🗨️ Red'}
          </button>
          
          {onToggleWaves && (
            <button
              onClick={() => onToggleWaves(!showWaves)}
              style={{
                padding: '4px 10px',
                background: showWaves ? 'rgba(67, 233, 123, 0.2)' : 'rgba(255,255,255,0.1)',
                border: showWaves ? '1px solid #43e97b' : '1px solid rgba(255,255,255,0.2)',
                borderRadius: '4px',
                color: 'white',
                cursor: 'pointer',
                fontSize: '11px'
              }}
            >
              {showWaves ? '🌊 Ondas' : '🌊 Ondas'}
            </button>
          )}
        </div>
      </div>
      
      {/* Estadísticas */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '8px',
        marginBottom: '12px'
      }}>
        <div style={{
          padding: '8px',
          background: 'rgba(255,255,255,0.05)',
          borderRadius: '6px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.6)' }}>Cuerpos</div>
          <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#4A90E2' }}>
            {stats.celestialBodies}
          </div>
        </div>
        
        <div style={{
          padding: '8px',
          background: 'rgba(255,255,255,0.05)',
          borderRadius: '6px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '11px', color: 'rgba(255,255,255,0.6)' }}>Alineaciones</div>
          <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#ffaa00' }}>
            {stats.activeAlignments}
          </div>
        </div>
      </div>
      
      {/* Eventos activos */}
      <div style={{
        marginBottom: '10px'
      }}>
        <div style={{
          fontSize: '12px',
          color: 'rgba(255,255,255,0.7)',
          marginBottom: '6px',
          fontWeight: 'bold'
        }}>
          ✨ Eventos Activos ({activeEvents.length})
        </div>
        
        {activeEvents.length === 0 ? (
          <div style={{
            padding: '10px',
            background: 'rgba(255,255,255,0.03)',
            borderRadius: '6px',
            fontSize: '11px',
            color: 'rgba(255,255,255,0.5)',
            textAlign: 'center'
          }}>
            No hay eventos de resonancia activos
          </div>
        ) : (
          <div style={{
            maxHeight: '150px',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '6px'
          }}>
            {activeEvents.map(event => {
              const colors = {
                gravitational_pulse: '#ff6600',
                orbital_energy: '#ffaa00',
                cosmic_event: '#ff00ff',
                harmonic_resonance: '#00ff88'
              }
              
              const icons = {
                gravitational_pulse: '⚡',
                orbital_energy: '🌟',
                cosmic_event: '💫',
                harmonic_resonance: '🎵'
              }
              
              const elapsed = (Date.now() - event.timestamp) / 1000
              const remaining = Math.max(0, event.duration - elapsed)
              
              return (
                <div
                  key={event.id}
                  style={{
                    padding: '8px',
                    background: 'rgba(255,255,255,0.05)',
                    borderLeft: `3px solid ${colors[event.type]}`,
                    borderRadius: '4px',
                    fontSize: '11px'
                  }}
                >
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    marginBottom: '4px'
                  }}>
                    <span style={{ fontWeight: 'bold' }}>
                      {icons[event.type]} {event.alignment.type}
                    </span>
                    <span style={{ color: 'rgba(255,255,255,0.6)' }}>
                      {remaining.toFixed(0)}s
                    </span>
                  </div>
                  
                  <div style={{
                    fontSize: '10px',
                    color: 'rgba(255,255,255,0.7)',
                    marginBottom: '4px'
                  }}>
                    {event.description}
                  </div>
                  
                  <div style={{
                    fontSize: '10px',
                    color: 'rgba(255,255,255,0.5)'
                  }}>
                    Ratio: {event.alignment.harmonicRatio} | 
                    Intensidad: {(event.intensity * 100).toFixed(0)}%
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
      
      {/* Footer */}
      <div style={{
        paddingTop: '10px',
        borderTop: '1px solid rgba(255,255,255,0.1)',
        fontSize: '10px',
        color: 'rgba(255,255,255,0.5)',
        textAlign: 'center'
      }}>
        Total de eventos: {stats.totalEvents}
      </div>
    </div>
  )
}

/**
 * EJEMPLO DE USO EN TU ESCENA PRINCIPAL:
 * 
 * import CosmicResonanceDemo from '@/components/CosmicResonanceDemo'
 * import { getCosmicResonance } from '@/systems/CosmicResonanceSystem'
 * 
 * function MyScene() {
 *   const sceneRef = useRef<THREE.Scene>()
 *   
 *   useEffect(() => {
 *     const scene = new THREE.Scene()
 *     sceneRef.current = scene
 *     
 *     // Registrar planetas
 *     const cosmic = getCosmicResonance()
 *     
 *     cosmic.registerCelestialBody({
 *       id: 'earth',
 *       name: 'Tierra',
 *       position: new THREE.Vector3(0, 0, 0),
 *       orbitalPeriod: 365.25,
 *       orbitalFrequency: 1 / 365.25,
 *       audioFrequency: 136.10,
 *       color: '#4A90E2'
 *     })
 *     
 *     // ... más planetas
 *     
 *     // En tu loop de animación
 *     function animate() {
 *       cosmic.updateBodyPosition('earth', earthMesh.position)
 *       // ... actualizar más posiciones
 *     }
 *   }, [])
 *   
 *   return (
 *     <>
 *       <Canvas>
 *         // ... tu escena
 *       </Canvas>
 *       
 *       {sceneRef.current && (
 *         <CosmicResonanceDemo 
 *           scene={sceneRef.current} 
 *           enabled={true}
 *         />
 *       )}
 *     </>
 *   )
 * }
 */
