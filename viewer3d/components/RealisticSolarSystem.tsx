'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { AstronomicalSystem } from '@/lib/astronomyEngine'
import { getAssetPath } from '@/lib/paths'
import Sun from './Sun'
import Globe3D from './Globe3D'
import RealisticOrbits from './RealisticOrbits'
import RealisticLunarOrbit from './RealisticLunarOrbit'
import CelestialTooltip from './CelestialTooltip'
import { CelestialOverlay3D } from './CelestialOverlay'
import AsteroidBelt3D from './AsteroidBelt3D'

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
  const jupiterTexture = useTexture(getAssetPath('/textures/2k_jupiter.jpg'))
  const saturnTexture = useTexture(getAssetPath('/textures/2k_saturn.jpg'))
  const saturnRingTexture = useTexture(getAssetPath('/textures/2k_saturn_ring_alpha.png'))
  const uranusTexture = useTexture(getAssetPath('/textures/2k_uranus.jpg'))
  const neptuneTexture = useTexture(getAssetPath('/textures/2k_neptune.jpg'))
  
  // Sistema astronómico
  const astroSystemRef = useRef<AstronomicalSystem>(
    new AstronomicalSystem(
      new Date(), // Fecha actual
      3600,       // 1 segundo real = 1 hora simulada (más rápido para ver la Luna)
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

  // Planetas exteriores
  const jupiterRef = useRef<THREE.Group>(null)
  const jupiterMeshRef = useRef<THREE.Mesh>(null)
  const saturnRef = useRef<THREE.Group>(null)
  const saturnMeshRef = useRef<THREE.Mesh>(null)
  const uranusRef = useRef<THREE.Group>(null)
  const uranusMeshRef = useRef<THREE.Mesh>(null)
  const neptuneRef = useRef<THREE.Group>(null)
  const neptuneMeshRef = useRef<THREE.Mesh>(null)
  
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
    if (marsMeshRef.current) {
      marsMeshRef.current.rotation.y += delta * 0.05
    }

    // Planetas exteriores — Kepler calibrado con longitudes medias J2000.0 reales
    // Fuente: Astronomical Almanac / JPL (L0 en radianes, n en rad/s)
    // J2000.0 = 2000-01-01 12:00 UTC = unix 946728000
    const J2000_UNIX = 946728000
    const t = astroSystem.getTimeEngine().getCurrentTime().getTime() / 1000
    const t_j2000 = t - J2000_UNIX // segundos desde J2000
    const AU = 200 // escala visual

    // Longitudes medias J2000 (radianes) + velocidades medias (rad/s)
    // L0 fuente: Astronomical Almanac Table C24
    const DEG = Math.PI / 180

    // Júpiter: L0=34.35°, T=11.86 años
    const jAngle = 34.351519 * DEG + (t_j2000 / (11.86 * 365.25 * 86400)) * Math.PI * 2
    if (jupiterRef.current) jupiterRef.current.position.set(Math.cos(jAngle) * 5.2 * AU, 0, Math.sin(jAngle) * 5.2 * AU)
    if (jupiterMeshRef.current) jupiterMeshRef.current.rotation.y += delta * 0.045

    // Saturno: L0=50.08°, T=29.46 años
    const sAngle = 50.077444 * DEG + (t_j2000 / (29.46 * 365.25 * 86400)) * Math.PI * 2
    if (saturnRef.current) saturnRef.current.position.set(Math.cos(sAngle) * 9.58 * AU, 0, Math.sin(sAngle) * 9.58 * AU)
    if (saturnMeshRef.current) saturnMeshRef.current.rotation.y += delta * 0.043

    // Urano: L0=314.06°, T=84.01 años
    const uAngle = 314.055005 * DEG + (t_j2000 / (84.01 * 365.25 * 86400)) * Math.PI * 2
    if (uranusRef.current) uranusRef.current.position.set(Math.cos(uAngle) * 19.2 * AU, 0, Math.sin(uAngle) * 19.2 * AU)
    if (uranusMeshRef.current) uranusMeshRef.current.rotation.y += delta * 0.03

    // Neptuno: L0=304.35°, T=164.8 años
    const nAngle = 304.348665 * DEG + (t_j2000 / (164.8 * 365.25 * 86400)) * Math.PI * 2
    if (neptuneRef.current) neptuneRef.current.position.set(Math.cos(nAngle) * 30.05 * AU, 0, Math.sin(nAngle) * 30.05 * AU)
    if (neptuneMeshRef.current) neptuneMeshRef.current.rotation.y += delta * 0.032
    
    // Luna relativa a la Tierra con TIDAL LOCKING
    if (moonRef.current && moonMeshRef.current && earthGroupRef.current) {
      // Actualizar posición
      moonRef.current.position.set(positions.moon.x, positions.moon.y, positions.moon.z)
      
      // 🌙 TIDAL LOCKING (Bloqueo por marea)
      // La Luna siempre muestra la misma cara hacia la Tierra
      // Resetear rotación antes de aplicar lookAt
      moonMeshRef.current.rotation.set(0, 0, 0)
      
      // Hacer que la Luna mire hacia el centro (Tierra en 0,0,0)
      // lookAt hace que el eje -Z apunte hacia el objetivo
      moonMeshRef.current.lookAt(0, 0, 0)
      
      // Ajuste de rotación para que la cara correcta de la textura mire hacia la Tierra
      // La textura 2K puede tener orientación diferente, ajustamos con rotación en Y
      // Probamos sin rotación adicional primero para ver la orientación base
      moonMeshRef.current.rotateY(0) // Sin rotación adicional - cara frontal hacia Tierra
    }
  })
  
  return (
    <group>
      {/* Sol en el centro con tooltip */}
      <group>
        <Sun />
        <CelestialTooltip
          name="Sol"
          symbol="☀"
          type="Estrella (G2V)"
          data={{
            diameter: "1.39 millones km",
            temperature: "5.500°C (superficie)",
            day: "~27 días (rotación)",
            funFact: "Contiene el 99.86% de la masa del sistema solar"
          }}
          position={[0, 50, 0]}
          color="#ffaa00"
        />
      </group>
      
      {/* Órbitas reales visibles */}
      <RealisticOrbits />
      
      {/* Mercurio - Posición real con rotación axial */}
      <group ref={mercuryRef}>
        <mesh ref={mercuryMeshRef}>
          <sphereGeometry args={[1.9, 64, 64]} />
          <meshStandardMaterial 
            map={mercuryTexture}
            color="#9c9c9c" 
            roughness={0.95} 
            metalness={0.05} 
          />
        </mesh>
        <CelestialTooltip
          name="Mercurio"
          symbol="☿"
          type="Planeta rocoso"
          data={{
            orbitalPeriod: "88 días",
            day: "176 días terrestres",
            diameter: "4.879 km",
            temperature: "-173°C a 427°C",
            atmosphere: "Sin atmósfera",
            funFact: "Un año dura menos que su día"
          }}
          position={[0, 3, 0]}
          color="#9c9c9c"
        />
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
        <CelestialTooltip
          name="Venus"
          symbol="♀"
          type="Planeta rocoso"
          data={{
            orbitalPeriod: "225 días",
            day: "243 días (retrógrado)",
            diameter: "12.104 km",
            temperature: "465°C",
            atmosphere: "CO₂ extremadamente densa",
            funFact: "El planeta más caliente del sistema"
          }}
          position={[0, 1.5, 0]}
          color="#f5e6d3"
        />
      </group>
      
      {/* Tierra + Luna - Posición real */}
      <group ref={earthGroupRef}>
        <Globe3D 
          onLocationClick={onLocationClick}
          markerPosition={markerPosition}
        />
        
        {/* Tooltip de la Tierra */}
        <CelestialTooltip
          name="Tierra"
          symbol="🌍"
          type="Planeta rocoso"
          data={{
            orbitalPeriod: "365.25 días",
            day: "24 horas",
            diameter: "12.742 km",
            temperature: "-88°C a 58°C",
            moons: "1 (Luna)",
            atmosphere: "N₂ 78%, O₂ 21%",
            funFact: "Único planeta conocido con vida"
          }}
          position={[0, 7, 0]}
          color="#4a9eff"
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
          <CelestialTooltip
            name="Luna"
            symbol="☾"
            type="Satélite natural"
            data={{
              orbitalPeriod: "27.3 días",
              diameter: "3.474 km",
              temperature: "-173°C a 127°C",
              funFact: "Siempre muestra la misma cara a la Tierra"
            }}
            position={[0, 0.8, 0]}
            color="#FFFFFF"
          />
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
        <CelestialTooltip
          name="Marte"
          symbol="♂"
          type="Planeta rocoso"
          data={{
            orbitalPeriod: "687 días",
            day: "24h 37m",
            diameter: "6.779 km",
            temperature: "-60°C",
            moons: "2 (Fobos y Deimos)",
            funFact: "Día casi igual al terrestre"
          }}
          position={[0, 1.2, 0]}
          color="#c97a5f"
        />
      </group>

      {/* Cinturón de asteroides — modelos GLB reales instanciados */}
      <AsteroidBelt3D />

      {/* Convergencias planetarias reales — líneas 3D */}
      <CelestialOverlay3D />

      {/* ── Júpiter ─────────────────────────────────────────────────────── */}
      <group ref={jupiterRef}>
        <mesh ref={jupiterMeshRef}>
          <sphereGeometry args={[55, 64, 64]} />
          <meshStandardMaterial map={jupiterTexture} roughness={0.9} metalness={0.0} />
        </mesh>
        <CelestialTooltip name="Júpiter" symbol="♃" type="Gigante gaseoso"
          data={{ orbitalPeriod: "11.86 años", day: "9h 56m", diameter: "139.820 km",
            temperature: "-110°C", moons: "95 conocidas", atmosphere: "H₂, He, NH₃",
            funFact: "El planeta más grande — cabe 1.300 Tierras" }}
          position={[0, 60, 0]} color="#c8a87a" />
      </group>

      {/* ── Saturno + anillos ────────────────────────────────────────────── */}
      {/* saturnRef mueve el grupo en el plano orbital */}
      <group ref={saturnRef}>
        {/* Subgrupo con tilt axial real de Saturno (26.7°) + leve rotación Y para perspectiva */}
        <group rotation={[0, 0.3, THREE.MathUtils.degToRad(26.7)]}>
          {/* Planeta */}
          <mesh ref={saturnMeshRef} castShadow>
            <sphereGeometry args={[38, 64, 64]} />
            <meshStandardMaterial map={saturnTexture} roughness={0.9} metalness={0.0} />
          </mesh>
          {/* Anillos — en el plano ecuatorial del planeta (XZ), heredan el tilt del grupo */}
          <mesh rotation={[Math.PI / 2, 0, 0]} receiveShadow>
            <ringGeometry args={[46, 88, 128]} />
            <meshStandardMaterial
              map={saturnRingTexture}
              alphaMap={saturnRingTexture}
              side={THREE.DoubleSide}
              transparent
              opacity={0.85}
              depthWrite={false}
              roughness={0.8}
              metalness={0.0}
            />
          </mesh>
          {/* Segunda capa sutil para sensación de volumen */}
          <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, 0.4, 0]}>
            <ringGeometry args={[46, 88, 128]} />
            <meshBasicMaterial
              map={saturnRingTexture}
              side={THREE.DoubleSide}
              transparent
              opacity={0.18}
              depthWrite={false}
            />
          </mesh>
        </group>
        <CelestialTooltip name="Saturno" symbol="♄" type="Gigante gaseoso"
          data={{ orbitalPeriod: "29.46 años", day: "10h 42m", diameter: "116.460 km",
            temperature: "-140°C", moons: "146 conocidas", atmosphere: "H₂, He",
            funFact: "Sus anillos tienen 270.000 km de diámetro pero solo 1 km de grosor" }}
          position={[0, 55, 0]} color="#e8d5a0" />
      </group>

      {/* ── Urano ────────────────────────────────────────────────────────── */}
      <group ref={uranusRef}>
        <mesh ref={uranusMeshRef}>
          <sphereGeometry args={[20, 64, 64]} />
          <meshStandardMaterial map={uranusTexture} roughness={0.85} metalness={0.0}
            emissive="#7de8e8" emissiveIntensity={0.04} />
        </mesh>
        {/* Anillos tenues de Urano — inclinados ~98° (eje casi horizontal) */}
        <mesh rotation={[0, 0, Math.PI / 2]}>
          <ringGeometry args={[24, 30, 64]} />
          <meshBasicMaterial color="#7de8e8" side={THREE.DoubleSide}
            transparent opacity={0.18} depthWrite={false} blending={THREE.AdditiveBlending} />
        </mesh>
        <CelestialTooltip name="Urano" symbol="⛢" type="Gigante de hielo"
          data={{ orbitalPeriod: "84 años", day: "17h 14m", diameter: "50.724 km",
            temperature: "-195°C", moons: "28 conocidas", atmosphere: "H₂, He, CH₄",
            funFact: "Rota de lado — su eje está inclinado 98°" }}
          position={[0, 25, 0]} color="#7de8e8" />
      </group>

      {/* ── Neptuno ──────────────────────────────────────────────────────── */}
      <group ref={neptuneRef}>
        <mesh ref={neptuneMeshRef}>
          <sphereGeometry args={[19, 64, 64]} />
          <meshStandardMaterial map={neptuneTexture} roughness={0.85} metalness={0.0}
            emissive="#4b70dd" emissiveIntensity={0.06} />
        </mesh>
        <CelestialTooltip name="Neptuno" symbol="♆" type="Gigante de hielo"
          data={{ orbitalPeriod: "164.8 años", day: "16h 6m", diameter: "49.244 km",
            temperature: "-200°C", moons: "16 conocidas", atmosphere: "H₂, He, CH₄",
            funFact: "Vientos de hasta 2.100 km/h — los más rápidos del sistema solar" }}
          position={[0, 24, 0]} color="#4b70dd" />
      </group>
    </group>
  )
}
