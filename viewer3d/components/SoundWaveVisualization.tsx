/**
 * 🌊 Sound Wave Visualization
 * 
 * Visualización de ondas sonoras alrededor de los planetas
 * Representa gráficamente las frecuencias musicales de Kepler
 * 
 * CONCEPTO:
 * - Cada planeta emite ondas concéntricas
 * - La frecuencia determina el color y velocidad
 * - La amplitud determina el tamaño
 * - Cuando dos ondas se encuentran → interferencia visual
 */

'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface SoundWaveVisualizationProps {
  position: THREE.Vector3
  frequency: number  // Hz
  amplitude: number  // 0-1
  color: string
  enabled?: boolean
}

export default function SoundWaveVisualization({
  position,
  frequency,
  amplitude,
  color,
  enabled = true
}: SoundWaveVisualizationProps) {
  const groupRef = useRef<THREE.Group>(null)
  const wavesRef = useRef<THREE.Mesh[]>([])
  
  // Número de ondas concéntricas
  const waveCount = 5
  
  // Crear geometrías de ondas
  const waves = useMemo(() => {
    const waveArray: THREE.Mesh[] = []
    
    for (let i = 0; i < waveCount; i++) {
      const geometry = new THREE.RingGeometry(1, 1.2, 32)
      const material = new THREE.MeshBasicMaterial({
        color: new THREE.Color(color),
        transparent: true,
        opacity: 0,
        side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending,
        depthWrite: false
      })
      
      const mesh = new THREE.Mesh(geometry, material)
      mesh.rotation.x = Math.PI / 2  // Horizontal
      waveArray.push(mesh)
    }
    
    return waveArray
  }, [color, waveCount])
  
  // Actualizar ondas cada frame
  useFrame((state, delta) => {
    if (!enabled || !groupRef.current) return
    
    // Actualizar posición del grupo
    groupRef.current.position.copy(position)
    
    // Velocidad de expansión basada en frecuencia
    // Frecuencia alta = ondas rápidas
    const speed = (frequency / 200) * 2  // Normalizado
    
    waves.forEach((wave, i) => {
      const material = wave.material as THREE.MeshBasicMaterial
      
      // Fase de la onda (desfasadas entre sí)
      const phase = (state.clock.elapsedTime * speed + i * 0.5) % 2
      
      // Escala de la onda (expande desde el centro)
      const scale = 1 + phase * 10
      wave.scale.set(scale, scale, 1)
      
      // Opacidad (fade out mientras se expande)
      const opacity = Math.max(0, (1 - phase / 2) * amplitude * 0.3)
      material.opacity = opacity
      
      // Color pulsante basado en frecuencia
      const hue = (frequency / 400) % 1  // Mapear frecuencia a hue
      const saturation = 0.8
      const lightness = 0.5 + Math.sin(state.clock.elapsedTime * 2) * 0.1
      material.color.setHSL(hue, saturation, lightness)
    })
  })
  
  return (
    <group ref={groupRef}>
      {waves.map((wave, i) => (
        <primitive key={i} object={wave} />
      ))}
    </group>
  )
}

/**
 * Componente para múltiples planetas
 */
interface MultiPlanetWavesProps {
  planets: Array<{
    id: string
    position: THREE.Vector3
    frequency: number
    amplitude: number
    color: string
  }>
  enabled?: boolean
}

export function MultiPlanetWaves({ planets, enabled = true }: MultiPlanetWavesProps) {
  return (
    <group>
      {planets.map(planet => (
        <SoundWaveVisualization
          key={planet.id}
          position={planet.position}
          frequency={planet.frequency}
          amplitude={planet.amplitude}
          color={planet.color}
          enabled={enabled}
        />
      ))}
    </group>
  )
}
