'use client'

import { useRef, useMemo, useEffect, useState } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import * as THREE from 'three'
import { calculateSolarPosition, calculateLunarPosition } from '@/lib/astronomy'
import { getAssetPath } from '@/lib/paths'
import { useTexture as useTextureLoader } from '@react-three/drei'

/**
 * CAPA 2 — MANIFESTACIÓN VISIBLE
 * Sistema Solar contemplativo con leyes reales
 * Escalas desacopladas para coherencia visual
 */

interface SolarSystemProps {
  latitude: number;
  longitude: number;
  mode: 'contemplation' | 'revelation' | 'expansion' | 'system';
  showEcliptic?: boolean;
  showOrbits?: boolean;
}

export default function SolarSystem({
  latitude,
  longitude,
  mode = 'contemplation',
  showEcliptic = false,
  showOrbits = false
}: SolarSystemProps) {
  const sunRef = useRef<THREE.Mesh>(null)
  const earthRef = useRef<THREE.Group>(null)
  const moonRef = useRef<THREE.Mesh>(null)
  const marsRef = useRef<THREE.Mesh>(null)
  const venusRef = useRef<THREE.Mesh>(null)
  const earthOrbitRef = useRef<THREE.Line>(null)
  const eclipticRef = useRef<THREE.Mesh>(null)
  
  const { camera } = useThree()
  
  // Escalas desacopladas según modo
  const scales = useMemo(() => {
    switch (mode) {
      case 'contemplation':
        return {
          earth: 1,
          sun: 0, // Sol implícito (luz direccional)
          moon: 0.27,
          mars: 0,
          venus: 0,
          earthSunDistance: 1000, // "infinito"
          earthMoonDistance: 15,
          marsDistance: 0,
          venusDistance: 0
        }
      case 'revelation':
        return {
          earth: 1,
          sun: 3,
          moon: 0.27,
          mars: 0,
          venus: 0,
          earthSunDistance: 150,
          earthMoonDistance: 15,
          marsDistance: 0,
          venusDistance: 0
        }
      case 'expansion':
        return {
          earth: 1,
          sun: 10,
          moon: 0.27,
          mars: 0.53, // Tamaño real relativo
          venus: 0.95,
          earthSunDistance: 100,
          earthMoonDistance: 15,
          marsDistance: 152, // 1.52 UA
          venusDistance: 72  // 0.72 UA
        }
      case 'system':
        return {
          earth: 1,
          sun: 15,
          moon: 0.27,
          mars: 0.53,
          venus: 0.95,
          earthSunDistance: 80,
          earthMoonDistance: 12,
          marsDistance: 120,
          venusDistance: 58
        }
    }
  }, [mode])
  
  // Órbita terrestre (elíptica)
  const earthOrbitGeometry = useMemo(() => {
    const points: THREE.Vector3[] = []
    const segments = 128
    const a = scales.earthSunDistance // Semi-eje mayor
    const e = 0.0167 // Excentricidad real de la órbita terrestre
    const b = a * Math.sqrt(1 - e * e) // Semi-eje menor
    
    for (let i = 0; i <= segments; i++) {
      const theta = (i / segments) * Math.PI * 2
      const r = (a * (1 - e * e)) / (1 + e * Math.cos(theta))
      const x = r * Math.cos(theta)
      const z = r * Math.sin(theta)
      points.push(new THREE.Vector3(x, 0, z))
    }
    
    return new THREE.BufferGeometry().setFromPoints(points)
  }, [scales.earthSunDistance])
  
  // Plano eclíptico
  const eclipticGeometry = useMemo(() => {
    return new THREE.CircleGeometry(scales.earthSunDistance * 1.5, 64)
  }, [scales.earthSunDistance])
  
  // Tiempo continuo que nunca se detiene
  useFrame((state) => {
    const currentDate = new Date()
    
    // Calcular posiciones astronómicas reales
    const solarPos = calculateSolarPosition(currentDate, latitude, longitude)
    const lunarPos = calculateLunarPosition(currentDate, latitude, longitude)
    
    // Posición orbital (año) - calculado una vez para todos
    const yearStart = new Date(currentDate.getFullYear(), 0, 1)
    const yearProgress = (currentDate.getTime() - yearStart.getTime()) / 
                        (365.25 * 24 * 60 * 60 * 1000)
    
    if (earthRef.current) {
      // Inclinación axial real: 23.44°
      earthRef.current.rotation.z = (23.44 * Math.PI) / 180
      
      // Rotación diaria
      const dayProgress = (currentDate.getUTCHours() * 3600 + 
                          currentDate.getUTCMinutes() * 60 + 
                          currentDate.getUTCSeconds()) / 86400
      earthRef.current.rotation.y = dayProgress * Math.PI * 2
      
      const orbitalAngle = yearProgress * Math.PI * 2
      
      // Órbita elíptica
      const e = 0.0167
      const a = scales.earthSunDistance
      const r = (a * (1 - e * e)) / (1 + e * Math.cos(orbitalAngle))
      
      earthRef.current.position.x = r * Math.cos(orbitalAngle)
      earthRef.current.position.z = r * Math.sin(orbitalAngle)
    }
    
    // Luna orbitando la Tierra
    if (moonRef.current && earthRef.current) {
      const lunarMonth = 29.530588853 // días
      const monthProgress = (lunarPos.age / lunarMonth)
      const lunarAngle = monthProgress * Math.PI * 2
      
      const moonDistance = scales.earthMoonDistance
      moonRef.current.position.x = earthRef.current.position.x + moonDistance * Math.cos(lunarAngle)
      moonRef.current.position.z = earthRef.current.position.z + moonDistance * Math.sin(lunarAngle)
      moonRef.current.position.y = moonDistance * 0.1 * Math.sin(lunarAngle * 5.145) // Inclinación 5.145°
    }
    
    // Marte - Órbita más lenta (687 días terrestres)
    if (marsRef.current && scales.mars > 0) {
      const marsYearProgress = (yearProgress * 365.25) / 687
      const marsAngle = marsYearProgress * Math.PI * 2
      const marsDistance = scales.marsDistance
      
      marsRef.current.position.x = marsDistance * Math.cos(marsAngle)
      marsRef.current.position.z = marsDistance * Math.sin(marsAngle)
      marsRef.current.rotation.y = yearProgress * Math.PI * 2 * 1.03 // Rotación diaria (24.6h)
    }
    
    // Venus - Órbita más rápida (225 días terrestres)
    if (venusRef.current && scales.venus > 0) {
      const venusYearProgress = (yearProgress * 365.25) / 225
      const venusAngle = venusYearProgress * Math.PI * 2
      const venusDistance = scales.venusDistance
      
      venusRef.current.position.x = venusDistance * Math.cos(venusAngle)
      venusRef.current.position.z = venusDistance * Math.sin(venusAngle)
      venusRef.current.rotation.y = -yearProgress * Math.PI * 2 * 0.004 // Rotación retrógrada muy lenta (243 días)
    }
    
    // Sol (solo visible en modos revelation+)
    if (sunRef.current) {
      sunRef.current.visible = mode !== 'contemplation' && scales.sun > 0
      
      if (sunRef.current.visible) {
        // Pulsación sutil
        const pulse = 1 + Math.sin(state.clock.elapsedTime * 0.5) * 0.02
        sunRef.current.scale.setScalar(scales.sun * pulse)
      }
    }
    
    // Eclíptica (visible bajo demanda) - Deshabilitada temporalmente
    // if (eclipticRef.current && eclipticRef.current.material) {
    //   eclipticRef.current.visible = showEcliptic
    //   const material = eclipticRef.current.material as THREE.MeshBasicMaterial
    //   material.opacity = showEcliptic ? 0.1 : 0
    // }
    
    // Órbita (visible bajo demanda) - Deshabilitada temporalmente
    // if (earthOrbitRef.current && earthOrbitRef.current.material) {
    //   earthOrbitRef.current.visible = showOrbits
    //   const material = earthOrbitRef.current.material as THREE.LineBasicMaterial
    //   material.opacity = showOrbits ? 0.3 : 0
    // }
  })
  
  return (
    <group>
      {/* Sol - Siempre presente pero invisible en contemplation */}
      <mesh ref={sunRef} position={[0, 0, 0]} visible={scales.sun > 0}>
        <sphereGeometry args={[Math.max(scales.sun, 0.1), 64, 64]} />
        <meshBasicMaterial 
          color="#FDB813"
        />
      </mesh>
      
      {/* Luz solar direccional */}
      <directionalLight
        position={[0, 50, 0]}
        intensity={2}
        color="#FFF5E1"
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={500}
        shadow-camera-left={-100}
        shadow-camera-right={100}
        shadow-camera-top={100}
        shadow-camera-bottom={-100}
      />
      
      {/* Luz ambiental muy sutil */}
      <ambientLight intensity={0.05} color="#1a1a2e" />
      
      {/* Tierra */}
      <group ref={earthRef}>
        <mesh castShadow receiveShadow>
          <sphereGeometry args={[scales.earth, 64, 64]} />
          <meshStandardMaterial
            color="#2E5266"
            roughness={0.8}
            metalness={0.2}
          />
        </mesh>
        
        {/* Atmósfera sutil */}
        <mesh scale={1.02}>
          <sphereGeometry args={[scales.earth, 32, 32]} />
          <meshBasicMaterial
            color="#4A90E2"
            transparent
            opacity={0.1}
            side={THREE.BackSide}
          />
        </mesh>
      </group>
      
      {/* Luna */}
      <mesh ref={moonRef} castShadow>
        <sphereGeometry args={[scales.moon, 32, 32]} />
        <meshStandardMaterial
          color="#8B8B8B"
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>
      
      {/* Marte - Siempre presente pero invisible hasta expansion */}
      <mesh ref={marsRef} castShadow visible={scales.mars > 0}>
        <sphereGeometry args={[Math.max(scales.mars, 0.1), 32, 32]} />
        <meshStandardMaterial
          color="#CD5C5C"
          roughness={0.95}
          metalness={0.05}
        />
      </mesh>
      
      {/* Venus - Siempre presente pero invisible hasta expansion */}
      <mesh ref={venusRef} castShadow visible={scales.venus > 0}>
        <sphereGeometry args={[Math.max(scales.venus, 0.1), 32, 32]} />
        <meshStandardMaterial
          color="#FFC649"
          roughness={0.7}
          metalness={0.1}
        />
      </mesh>
      
      {/* Órbita terrestre - Deshabilitada temporalmente */}
      {/* <line ref={earthOrbitRef} geometry={earthOrbitGeometry}>
        <lineBasicMaterial
          color="#4A90E2"
          transparent
          opacity={0}
          linewidth={1}
        />
      </line> */}
      
      {/* Plano eclíptico - Deshabilitado temporalmente */}
      {/* <mesh
        ref={eclipticRef}
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
      >
        <primitive object={eclipticGeometry} />
        <meshBasicMaterial
          color="#FFD700"
          transparent
          opacity={0}
          side={THREE.DoubleSide}
        />
      </mesh> */}
      
      {/* Estrellas de fondo */}
      <Stars />
    </group>
  )
}

/**
 * Campo estelar realista
 */
function Stars() {
  const starsRef = useRef<THREE.Points>(null)
  
  const starGeometry = useMemo(() => {
    const geometry = new THREE.BufferGeometry()
    const positions: number[] = []
    const colors: number[] = []
    
    // 2000 estrellas pequeñas y sutiles
    for (let i = 0; i < 2000; i++) {
      const theta = Math.random() * Math.PI * 2
      const phi = Math.acos(2 * Math.random() - 1)
      const r = 800 + Math.random() * 200
      
      positions.push(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
      )
      
      // Colores estelares muy sutiles
      const temp = Math.random()
      if (temp < 0.3) {
        colors.push(0.6, 0.6, 0.8) // Azul muy suave
      } else if (temp < 0.7) {
        colors.push(0.8, 0.8, 0.8) // Blanco muy suave
      } else {
        colors.push(0.8, 0.7, 0.6) // Naranja muy suave
      }
    }
    
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3))
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3))
    
    return geometry
  }, [])
  
  useFrame((state) => {
    if (starsRef.current) {
      // Rotación muy lenta (rotación celeste)
      starsRef.current.rotation.y = state.clock.elapsedTime * 0.00005
    }
  })
  
  return (
    <points ref={starsRef} geometry={starGeometry}>
      <pointsMaterial
        size={0.4}
        vertexColors
        transparent
        opacity={0.5}
        sizeAttenuation
      />
    </points>
  )
}
