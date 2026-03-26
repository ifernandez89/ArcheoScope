'use client'

import { useRef, useMemo, useEffect } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

interface VisualLightningBoltProps {
  startPosition: [number, number, number]
  endPosition: [number, number, number]
  onComplete?: () => void
  duration?: number
}

// Vectores reutilizables para subdivideLightning (evita crear en cada llamada recursiva)
const _mid = new THREE.Vector3()
const _direction = new THREE.Vector3()
const _perpendicular = new THREE.Vector3()

// Subdivisión fractal para generar rayo irregular
function subdivideLightning(
  start: THREE.Vector3,
  end: THREE.Vector3,
  depth: number,
  displacement: number
): THREE.Vector3[] {
  if (depth === 0) {
    return [start, end]
  }

  // Usar vectores reutilizables para cálculos intermedios
  _mid.lerpVectors(start, end, 0.5)
  _direction.subVectors(end, start)
  _perpendicular.set(-_direction.z, 0, _direction.x).normalize()
  
  // Crear nuevo vector para el punto medio (necesario porque se guarda en el array)
  const midPoint = _mid.clone()
  midPoint.addScaledVector(_perpendicular, (Math.random() - 0.5) * displacement)
  midPoint.y += (Math.random() - 0.5) * displacement * 0.5
  
  const left = subdivideLightning(start, midPoint, depth - 1, displacement * 0.6)
  const right = subdivideLightning(midPoint, end, depth - 1, displacement * 0.6)
  
  return [...left.slice(0, -1), ...right]
}

// Generar ramificaciones
function generateBranches(
  points: THREE.Vector3[],
  branchProbability: number
): THREE.Vector3[][] {
  const branches: THREE.Vector3[][] = []
  
  for (let i = 2; i < points.length - 2; i++) {
    if (Math.random() < branchProbability) {
      const branchStart = points[i].clone()
      const branchLength = (points.length - i) * 0.4
      const branchEnd = branchStart.clone()
      
      // Dirección aleatoria para la rama
      const angle = Math.random() * Math.PI * 2
      branchEnd.x += Math.cos(angle) * branchLength * 0.5
      branchEnd.z += Math.sin(angle) * branchLength * 0.5
      branchEnd.y -= branchLength * 0.3
      
      const branchPoints = subdivideLightning(branchStart, branchEnd, 2, 2)
      branches.push(branchPoints)
    }
  }
  
  return branches
}

export default function VisualLightningBolt({
  startPosition,
  endPosition,
  onComplete,
  duration = 0.15
}: VisualLightningBoltProps) {
  const groupRef = useRef<THREE.Group>(null)
  const timeRef = useRef(0)
  const completedRef = useRef(false)
  
  // Cache de líneas para evitar traverse cada frame
  const cachedLines = useRef<THREE.Line[]>([])
  const linesCached = useRef(false)
  
  // Generar geometría del rayo con subdivisión fractal
  const { mainGeometry, branchGeometries } = useMemo(() => {
    const start = new THREE.Vector3(...startPosition)
    const end = new THREE.Vector3(...endPosition)
    
    // Generar puntos principales con subdivisión fractal
    const mainPoints = subdivideLightning(start, end, 4, 8)
    
    // Generar ramificaciones
    const branches = generateBranches(mainPoints, 0.25)
    
    // Crear geometría principal
    const mainGeo = new THREE.BufferGeometry().setFromPoints(mainPoints)
    
    // Crear geometrías de ramas
    const branchGeos = branches.map(branch => 
      new THREE.BufferGeometry().setFromPoints(branch)
    )
    
    return { mainGeometry: mainGeo, branchGeometries: branchGeos }
  }, [startPosition, endPosition])
  
  // Material brillante con glow
  const material = useMemo(() => {
    return new THREE.LineBasicMaterial({
      color: '#a0d0ff',
      linewidth: 2,
      transparent: true,
      opacity: 1,
      blending: THREE.AdditiveBlending
    })
  }, [])
  
  const branchMaterial = useMemo(() => {
    return new THREE.LineBasicMaterial({
      color: '#7090c0',
      linewidth: 1,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending
    })
  }, [])
  
  // Crear objetos Line una sola vez en useMemo (no en render)
  const { mainLine, branchLines } = useMemo(() => {
    const main = new THREE.Line(mainGeometry, material)
    const branches = branchGeometries.map(geo => new THREE.Line(geo, branchMaterial))
    return { mainLine: main, branchLines: branches }
  }, [mainGeometry, branchGeometries, material, branchMaterial])
  
  useFrame((state, delta) => {
    if (completedRef.current) return
    
    timeRef.current += delta
    
    if (timeRef.current >= duration) {
      completedRef.current = true
      if (onComplete) onComplete()
    }
    
    // Cachear líneas una sola vez
    if (!linesCached.current && groupRef.current) {
      cachedLines.current = [mainLine, ...branchLines]
      linesCached.current = true
    }
    
    // Fade out usando cache (sin traverse)
    const fadeProgress = timeRef.current / duration
    for (const line of cachedLines.current) {
      const mat = line.material as THREE.LineBasicMaterial
      mat.opacity = 1 - fadeProgress
    }
  })
  
  return (
    <group ref={groupRef}>
      {/* Rayo principal */}
      <primitive object={mainLine} />
      
      {/* Ramificaciones */}
      {branchLines.map((line, i) => (
        <primitive key={i} object={line} />
      ))}
      
      {/* Glow adicional en el punto de impacto */}
      <pointLight
        position={endPosition}
        intensity={3}
        distance={15}
        color="#a0d0ff"
        decay={2}
      />
    </group>
  )
}
