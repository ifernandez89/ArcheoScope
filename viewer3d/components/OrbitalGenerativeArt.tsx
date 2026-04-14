/**
 * 🎨 Orbital Generative Art - Arte Generativo Cósmico
 * 
 * Genera patrones visuales basados en las órbitas planetarias:
 * - Mandalas gravitacionales (resonancias orbitales)
 * - Patrones geométricos (conexiones planetarias)
 * - Redes orbitales (líneas de fuerza gravitacional)
 */

'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface Planet {
  position: THREE.Vector3
  color: string
  orbitalPeriod: number
}

interface OrbitalGenerativeArtProps {
  planets: Planet[]
  enabled?: boolean
  intensity?: number  // 0-1
}

export default function OrbitalGenerativeArt({
  planets,
  enabled = true,
  intensity = 0.3
}: OrbitalGenerativeArtProps) {
  const mandalaRef = useRef<THREE.Group>(null)
  const timeRef = useRef(0)
  
  // Crear mandalas gravitacionales (patrones de resonancia)
  const mandalaLines = useMemo(() => {
    if (!enabled || planets.length < 2) return []
    
    const lines: JSX.Element[] = []
    
    // Conectar planetas con resonancias orbitales interesantes
    for (let i = 0; i < planets.length; i++) {
      for (let j = i + 1; j < planets.length; j++) {
        const p1 = planets[i]
        const p2 = planets[j]
        
        // Calcular ratio de períodos orbitales
        const ratio = p1.orbitalPeriod / p2.orbitalPeriod
        
        // Solo mostrar resonancias "armónicas" (ratios simples)
        if (isHarmonicRatio(ratio)) {
          const points: THREE.Vector3[] = []
          const segments = 64
          
          // Crear curva de Lissajous entre los dos planetas
          for (let k = 0; k <= segments; k++) {
            const t = (k / segments) * Math.PI * 2
            const x = Math.cos(t * ratio) * p1.position.length()
            const z = Math.sin(t) * p2.position.length()
            points.push(new THREE.Vector3(x, 0, z))
          }
          
          const geometry = new THREE.BufferGeometry().setFromPoints(points)
          
          lines.push(
            <primitive 
              key={`mandala-${i}-${j}`} 
              object={new THREE.Line(
                geometry,
                new THREE.LineBasicMaterial({
                  color: p1.color,
                  transparent: true,
                  opacity: intensity * 0.15,
                  blending: THREE.AdditiveBlending
                })
              )}
            />
          )
        }
      }
    }
    
    return lines
  }, [planets, enabled, intensity])
  
  // Crear red orbital (conexiones gravitacionales)
  const orbitalNetwork = useMemo(() => {
    if (!enabled || planets.length < 2) return null
    
    const points: THREE.Vector3[] = []
    const colors: number[] = []
    
    // Conectar planetas cercanos
    for (let i = 0; i < planets.length; i++) {
      for (let j = i + 1; j < planets.length; j++) {
        const p1 = planets[i]
        const p2 = planets[j]
        const distance = p1.position.distanceTo(p2.position)
        
        // Solo conectar si están relativamente cerca
        if (distance < 400) {
          points.push(p1.position.clone())
          points.push(p2.position.clone())
          
          // Color basado en distancia
          const color = new THREE.Color(p1.color)
          colors.push(color.r, color.g, color.b)
          colors.push(color.r, color.g, color.b)
        }
      }
    }
    
    if (points.length === 0) return null
    
    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))
    
    return (
      <lineSegments geometry={geometry}>
        <lineBasicMaterial
          vertexColors
          transparent
          opacity={intensity * 0.08}
          blending={THREE.AdditiveBlending}
        />
      </lineSegments>
    )
  }, [planets, enabled, intensity])
  
  // Crear patrones geométricos (spirograph cósmico)
  const geometricPatterns = useMemo(() => {
    if (!enabled || planets.length < 3) return []
    
    const patterns: JSX.Element[] = []
    
    // Crear patrones para cada planeta
    planets.forEach((planet, idx) => {
      const points: THREE.Vector3[] = []
      const segments = 128
      const radius = planet.position.length()
      
      // Patrón de espiral basado en período orbital
      for (let i = 0; i <= segments; i++) {
        const t = (i / segments) * Math.PI * 4
        const r = radius * (1 + 0.1 * Math.sin(t * planet.orbitalPeriod / 100))
        const x = r * Math.cos(t)
        const z = r * Math.sin(t)
        points.push(new THREE.Vector3(x, 0, z))
      }
      
      const geometry = new THREE.BufferGeometry().setFromPoints(points)
      
      patterns.push(
        <primitive
          key={`pattern-${idx}`}
          object={new THREE.Line(
            geometry,
            new THREE.LineBasicMaterial({
              color: planet.color,
              transparent: true,
              opacity: intensity * 0.1,
              blending: THREE.AdditiveBlending
            })
          )}
        />
      )
    })
    
    return patterns
  }, [planets, enabled, intensity])
  
  // Animación sutil de pulsación
  useFrame((state, delta) => {
    if (!enabled || !mandalaRef.current) return
    
    timeRef.current += delta
    
    // Pulsación suave
    const pulse = 1 + Math.sin(timeRef.current * 0.5) * 0.05
    mandalaRef.current.scale.setScalar(pulse)
    
    // Rotación muy lenta
    mandalaRef.current.rotation.y += delta * 0.02
  })
  
  if (!enabled) return null
  
  return (
    <group ref={mandalaRef}>
      {/* Mandalas gravitacionales */}
      {mandalaLines}
      
      {/* Red orbital */}
      {orbitalNetwork}
      
      {/* Patrones geométricos */}
      {geometricPatterns}
    </group>
  )
}

/**
 * Determina si un ratio orbital es "armónico" (resonancia interesante)
 */
function isHarmonicRatio(ratio: number): boolean {
  // Ratios armónicos comunes en el sistema solar
  const harmonics = [
    1/2, 2/3, 3/4, 3/5, 4/5, 5/6,  // Fracciones simples
    2, 3/2, 5/3, 5/4, 8/5           // Ratios de Fibonacci
  ]
  
  const tolerance = 0.15
  
  return harmonics.some(h => Math.abs(ratio - h) < tolerance)
}
