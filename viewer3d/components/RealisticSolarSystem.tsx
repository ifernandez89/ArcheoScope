'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Html, useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { AstronomicalSystem } from '@/lib/astronomyEngine'
import { getAssetPath } from '@/lib/paths'
import Sun from './Sun'
import Globe3D from './Globe3D'
import RealisticOrbits from './RealisticOrbits'
import RealisticLunarOrbit from './RealisticLunarOrbit'

/**
 * Sistema Solar Realista
 * 
 * CARACTERÍSTICAS:
 * ✅ Posiciones astronómicas REALES según fecha (astronomy-engine)
 * ✅ Velocidades orbitales REALES (calculadas dinámicamente)
 * ✅ Time-scale: 1 hora real = 1 día simulado
 * ✅ Distancias escaladas visualmente (no reales)
 * ✅ Tamaños artísticos (no reales)
 */

interface RealisticSolarSystemProps {
  onLocationClick?: (lat: number, lon: number) => void
  markerPosition?: { lat: number, lon: number } | null
}

export default function RealisticSolarSystem({ 
  onLocationClick, 
  markerPosition 
}: RealisticSolarSystemProps) {
  // Cargar texturas de planetas
  const mercuryTexture = useTexture(getAssetPath('/textures/8k_mercury.jpg'))
  const venusAtmosphereTexture = useTexture(getAssetPath('/textures/4k_venus_atmosphere.jpg'))
  const marsTexture = useTexture(getAssetPath('/textures/8k_mars.jpg'))
  const moonTexture = useTexture(getAssetPath('/textures/8k_moon.jpg'))
  
  // Sistema astronómico
  const astroSystemRef = useRef<AstronomicalSystem>(
    new AstronomicalSystem(
      new Date(), // Fecha actual
      24,         // 1 hora real = 1 día simulado (86400/3600 = 24)
      200         // Escala visual (Tierra a 200 unidades)
    )
  )
  
  // Referencias a planetas
  const mercuryRef = useRef<THREE.Group>(null)
  const mercuryMeshRef = useRef<THREE.Mesh>(null)
  const venusRef = useRef<THREE.Group>(null)
  const venusMeshRef = useRef<THREE.Mesh>(null)
  const earthGroupRef = useRef<THREE.Group>(null)
  const marsRef = useRef<THREE.Group>(null)
  const marsMeshRef = useRef<THREE.Mesh>(null)
  const moonRef = useRef<THREE.Group>(null)
  const moonMeshRef = useRef<THREE.Mesh>(null)
  
  // Actualización del sistema
  useFrame((state, delta) => {
    const astroSystem = astroSystemRef.current
    const positions = astroSystem.update(delta)
    
    // Actualizar posiciones de planetas
    if (mercuryRef.current) {
      mercuryRef.current.position.set(positions.mercury.x, positions.mercury.y, positions.mercury.z)
    }
    
    // Rotación axial de Mercurio (muy lenta, 58.6 días terrestres)
    if (mercuryMeshRef.current) {
      mercuryMeshRef.current.rotation.y += delta * 0.00017 // Muy lenta
    }
    
    if (venusRef.current) {
      venusRef.current.position.set(positions.venus.x, positions.venus.y, positions.venus.z)
    }
    
    // Rotación axial de Venus (retrógrada, 243 días terrestres)
    if (venusMeshRef.current) {
      venusMeshRef.current.rotation.y -= delta * 0.00004 // Muy lenta y al revés
    }
    
    if (earthGroupRef.current) {
      earthGroupRef.current.position.set(positions.earth.x, positions.earth.y, positions.earth.z)
    }
    // La Tierra ya rota en Globe3D
    
    if (marsRef.current) {
      marsRef.current.position.set(positions.mars.x, positions.mars.y, positions.mars.z)
    }
    
    // Rotación axial de Marte (similar a la Tierra, 24.6 horas)
    if (marsMeshRef.current) {
      marsMeshRef.current.rotation.y += delta * 0.05 // Similar a la Tierra
    }
    
    // Luna relativa a la Tierra con TIDAL LOCKING
    if (moonRef.current && moonMeshRef.current && earthGroupRef.current) {
      // Actualizar posición
      moonRef.current.position.set(positions.moon.x, positions.moon.y, positions.moon.z)
      
      // 🌙 TIDAL LOCKING (Bloqueo por marea)
      // La Luna siempre muestra la misma cara hacia la Tierra
      // Hacer que la Luna mire hacia el origen (donde está la Tierra en coordenadas locales)
      const moonPos = new THREE.Vector3(positions.moon.x, positions.moon.y, positions.moon.z)
      const earthPos = new THREE.Vector3(0, 0, 0)
      const direction = new THREE.Vector3().subVectors(earthPos, moonPos).normalize()
      
      // Crear una matriz de rotación que apunte hacia la Tierra
      const matrix = new THREE.Matrix4()
      matrix.lookAt(moonPos, earthPos, new THREE.Vector3(0, 1, 0))
      moonMeshRef.current.quaternion.setFromRotationMatrix(matrix)
    }
  })
  
  return (
    <group>
      {/* Sol en el centro */}
      <Sun />
      
      {/* Órbitas reales visibles */}
      <RealisticOrbits />
      
      {/* Mercurio - Posición real con rotación axial */}
      <group ref={mercuryRef}>
        <mesh ref={mercuryMeshRef}>
          <sphereGeometry args={[0.38, 64, 64]} />
          <meshStandardMaterial 
            map={mercuryTexture}
            color="#9c9c9c" 
            roughness={0.95} 
            metalness={0.05} 
          />
        </mesh>
        <Html position={[0, 0.8, 0]} center>
          <div style={{
            color: '#9c9c9c',
            fontSize: '11px',
            fontWeight: 'bold',
            textShadow: '0 0 4px rgba(0,0,0,0.9)',
            pointerEvents: 'none',
            whiteSpace: 'nowrap'
          }}>
            ☿ Mercurio
          </div>
        </Html>
      </group>
      
      {/* Venus - Posición real con atmósfera densa y rotación retrógrada */}
      <group ref={venusRef}>
        {/* Núcleo de Venus con rotación */}
        <mesh ref={venusMeshRef}>
          <sphereGeometry args={[0.95, 64, 64]} />
          <meshStandardMaterial 
            map={venusAtmosphereTexture}
            color="#f5e6d3" 
            roughness={0.9} 
            metalness={0.0}
            emissive="#f5e6d3"
            emissiveIntensity={0.15}
          />
        </mesh>
        {/* Atmósfera densa de Venus - Capa 1 (más cercana) */}
        <mesh scale={1.05}>
          <sphereGeometry args={[0.95, 32, 32]} />
          <meshStandardMaterial
            color="#f5e6d3"
            transparent
            opacity={0.4}
            roughness={0.8}
            metalness={0.0}
            side={THREE.DoubleSide}
          />
        </mesh>
        {/* Atmósfera densa de Venus - Capa 2 (exterior brillante) */}
        <mesh scale={1.08}>
          <sphereGeometry args={[0.95, 32, 32]} />
          <meshBasicMaterial
            color="#fff5e6"
            transparent
            opacity={0.25}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
            side={THREE.BackSide}
          />
        </mesh>
        {/* Atmósfera densa de Venus - Capa 3 (glow exterior) */}
        <mesh scale={1.12}>
          <sphereGeometry args={[0.95, 24, 24]} />
          <meshBasicMaterial
            color="#ffe4b3"
            transparent
            opacity={0.15}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
            side={THREE.BackSide}
          />
        </mesh>
        <Html position={[0, 1.5, 0]} center>
          <div style={{
            color: '#f5e6d3',
            fontSize: '11px',
            fontWeight: 'bold',
            textShadow: '0 0 4px rgba(0,0,0,0.9)',
            pointerEvents: 'none',
            whiteSpace: 'nowrap'
          }}>
            ♀ Venus
          </div>
        </Html>
      </group>
      
      {/* Tierra + Luna - Posición real */}
      <group ref={earthGroupRef}>
        <Globe3D 
          onLocationClick={onLocationClick}
          markerPosition={markerPosition}
        />
        
        {/* Órbita lunar visible */}
        <RealisticLunarOrbit />
        
        {/* Luna relativa a la Tierra con etiqueta y tidal locking */}
        <group ref={moonRef}>
          <mesh ref={moonMeshRef}>
            <sphereGeometry args={[0.27, 64, 64]} />
            <meshStandardMaterial 
              map={moonTexture}
              color="#FFFFFF" 
              roughness={0.95} 
              metalness={0.05} 
            />
          </mesh>
          <Html position={[0, 0.8, 0]} center>
            <div style={{
              color: '#FFFFFF',
              fontSize: '10px',
              fontWeight: 'bold',
              textShadow: '0 0 4px rgba(0,0,0,0.9)',
              pointerEvents: 'none',
              whiteSpace: 'nowrap'
            }}>
              ☾ Luna
            </div>
          </Html>
        </group>
      </group>
      
      {/* Marte - Posición real con rotación axial */}
      <group ref={marsRef}>
        <mesh ref={marsMeshRef}>
          <sphereGeometry args={[0.5, 64, 64]} />
          <meshStandardMaterial 
            map={marsTexture}
            color="#8b6f5f" 
            roughness={0.95} 
            metalness={0.0} 
          />
        </mesh>
        {/* Atmósfera marciana tenue */}
        <mesh scale={1.03}>
          <sphereGeometry args={[0.5, 32, 32]} />
          <meshBasicMaterial
            color="#c97a5f"
            transparent
            opacity={0.04}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
            side={THREE.BackSide}
          />
        </mesh>
        <Html position={[0, 1.2, 0]} center>
          <div style={{
            color: '#c97a5f',
            fontSize: '11px',
            fontWeight: 'bold',
            textShadow: '0 0 4px rgba(0,0,0,0.9)',
            pointerEvents: 'none',
            whiteSpace: 'nowrap'
          }}>
            ♂ Marte
          </div>
        </Html>
      </group>
    </group>
  )
}
