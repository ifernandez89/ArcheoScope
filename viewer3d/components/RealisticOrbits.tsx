'use client'

import { useRef, useEffect } from 'react'
import * as THREE from 'three'
import { calculatePlanetPosition, PLANETS } from '@/utils/planetary-orbits'

// ── Planetas interiores: órbitas reales via astronomy-engine ─────────────────

interface OrbitProps {
  body: string
  color: string
  opacity?: number
  segments?: number
  scale?: number
}

function RealisticOrbit({ body, color, opacity = 0.35, segments = 256, scale = 200 }: OrbitProps) {
  const groupRef = useRef<THREE.Group>(null)

  useEffect(() => {
    if (!groupRef.current) return

    // Mapear nombres de astronomy-engine a nuestro sistema
    const planetMap: Record<string, string> = {
      'Mercury': 'mercury',
      'Venus': 'venus', 
      'Earth': 'earth',
      'Mars': 'mars',
      'Jupiter': 'jupiter',
      'Saturn': 'saturn',
      'Uranus': 'uranus',
      'Neptune': 'neptune',
      'Pluto': 'pluto'
    }
    
    const planetKey = planetMap[body]
    if (!planetKey || !PLANETS[planetKey]) return

    const planet = PLANETS[planetKey]
    const points: THREE.Vector3[] = []
    
    // Generar órbita completa usando nuestro sistema
    for (let i = 0; i <= segments; i++) {
      const timeInDays = (i / segments) * planet.period // Un período completo
      const position = calculatePlanetPosition(planet, timeInDays, scale)
      points.push(position.position)
    }

    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    const material = new THREE.LineBasicMaterial({
      color, transparent: true, opacity, depthWrite: false,
      blending: THREE.AdditiveBlending
    })
    const line = new THREE.Line(geometry, material)
    groupRef.current.add(line)

    return () => {
      groupRef.current?.remove(line)
      geometry.dispose(); material.dispose()
    }
  }, [body, segments, scale, color, opacity])

  return <group ref={groupRef} />
}

// ── Planetas exteriores: órbita circular simple en plano XZ ─────────────────
// Consistente con el movimiento en useFrame de RealisticSolarSystem

interface CircleOrbitProps {
  radiusAU: number
  color: string
  opacity?: number
  segments?: number
  scale?: number
}

function CircleOrbit({ radiusAU, color, opacity = 0.28, segments = 200, scale = 200 }: CircleOrbitProps) {
  const groupRef = useRef<THREE.Group>(null)

  useEffect(() => {
    if (!groupRef.current) return

    const r = radiusAU * scale
    const points: THREE.Vector3[] = []
    for (let i = 0; i <= segments; i++) {
      const angle = (i / segments) * Math.PI * 2
      points.push(new THREE.Vector3(Math.cos(angle) * r, 0, Math.sin(angle) * r))
    }

    const geometry = new THREE.BufferGeometry().setFromPoints(points)
    const material = new THREE.LineBasicMaterial({
      color, transparent: true, opacity, depthWrite: false,
      blending: THREE.AdditiveBlending
    })
    const line = new THREE.Line(geometry, material)
    groupRef.current.add(line)

    return () => {
      groupRef.current?.remove(line)
      geometry.dispose(); material.dispose()
    }
  }, [radiusAU, segments, scale, color, opacity])

  return <group ref={groupRef} />
}

// ── Cinturón de asteroides ────────────────────────────────────────────────────

function AsteroidBelt({ scale = 200 }: { scale?: number }) {
  const groupRef = useRef<THREE.Group>(null)

  useEffect(() => {
    if (!groupRef.current) return

    const rings = [
      { r: 2.2, opacity: 0.22 },
      { r: 2.7, opacity: 0.32 },
      { r: 3.2, opacity: 0.18 },
    ]
    const added: { line: THREE.Line; geo: THREE.BufferGeometry; mat: THREE.LineBasicMaterial }[] = []

    for (const { r, opacity } of rings) {
      const points: THREE.Vector3[] = []
      for (let i = 0; i <= 256; i++) {
        const angle = (i / 256) * Math.PI * 2
        const tilt = Math.sin(angle) * 0.026
        points.push(new THREE.Vector3(
          Math.cos(angle) * r * scale,
          tilt * scale,
          Math.sin(angle) * r * scale
        ))
      }
      const geo = new THREE.BufferGeometry().setFromPoints(points)
      const mat = new THREE.LineBasicMaterial({
        color: '#8a7a5a', transparent: true, opacity,
        depthWrite: false, blending: THREE.AdditiveBlending
      })
      const line = new THREE.Line(geo, mat)
      groupRef.current.add(line)
      added.push({ line, geo, mat })
    }

    return () => {
      for (const { line, geo, mat } of added) {
        groupRef.current?.remove(line)
        geo.dispose(); mat.dispose()
      }
    }
  }, [scale])

  return <group ref={groupRef} />
}

// ── Export principal ──────────────────────────────────────────────────────────

export default function RealisticOrbits() {
  return (
    <group>
      {/* Planetas interiores */}
      <RealisticOrbit body="Mercury" color="#9c9c9c" opacity={0.30} />
      <RealisticOrbit body="Venus"   color="#f5e6d3" opacity={0.30} />
      <RealisticOrbit body="Earth"   color="#4a9eff" opacity={0.40} />
      <RealisticOrbit body="Mars"    color="#c97a5f" opacity={0.30} />
      
      {/* Planetas exteriores */}
      <RealisticOrbit body="Jupiter" color="#c8a87a" opacity={0.35} />
      <RealisticOrbit body="Saturn"  color="#e8d5a0" opacity={0.35} />
      
      {/* Planetas exteriores lejanos - OPACIDAD AUMENTADA PARA VISIBILIDAD */}
      <RealisticOrbit body="Uranus"  color="#7de8e8" opacity={0.50} segments={512} />
      <RealisticOrbit body="Neptune" color="#4b70dd" opacity={0.50} segments={512} />
      <RealisticOrbit body="Pluto"   color="#ff8c00" opacity={0.60} segments={512} />
    </group>
  )
}
