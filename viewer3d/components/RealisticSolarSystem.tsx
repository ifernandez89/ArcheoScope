'use client'

import { useRef, useEffect, useState, useMemo } from 'react'
import { useFrame, useThree } from '@react-three/fiber'
import { useTexture } from '@react-three/drei'
import * as THREE from 'three'
import { SolarEngine } from '@/engines/SolarEngine'
import { calculateAllPlanets } from '@/utils/planetary-orbits'
import { calculateLunarPhase } from '@/utils/lunar-system'
import { getAssetPath } from '@/lib/paths'
import { getSphereSegments } from '@/lib/mobileOptimizations'
import Sun from './Sun'
import Globe3D from './Globe3D'
import RealisticOrbits from './RealisticOrbits'
import RealisticLunarOrbit from './RealisticLunarOrbit'
import CelestialTooltip from './CelestialTooltip'
import { CelestialOverlay3D } from './CelestialOverlay'
import AsteroidBelt3D from './AsteroidBelt3D'
import { getCosmicResonance } from '@/systems/CosmicResonanceSystem'
import { getKeplerHarmonices } from '@/systems/KeplerHarmonicesSystem'
import { MultiPlanetWaves } from './SoundWaveVisualization'
import SaturnRings from './SaturnRings'
import OrbitalGenerativeArt from './OrbitalGenerativeArt'

// Importar datos de colores de planetas de Kepler
const KEPLER_PLANETARY_DATA = new Map([
  ['mercury', { color: '#9c9c9c' }],
  ['venus', { color: '#f5e6d3' }],
  ['earth', { color: '#4A90E2' }],
  ['mars', { color: '#E27B58' }],
  ['jupiter', { color: '#D4A574' }],
  ['saturn', { color: '#FAD5A5' }],
  ['uranus', { color: '#4FD0E7' }],
  ['neptune', { color: '#4166F5' }]
])

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
  showWaves?: boolean
}

export default function RealisticSolarSystem({ 
  onLocationClick, 
  markerPosition,
  showWaves = true
}: RealisticSolarSystemProps) {
  // Three.js scene para el sistema de resonancia
  const { scene } = useThree()
  
  // 📱 Segmentos optimizados para mobile (24) vs PC (64)
  const segments = useMemo(() => getSphereSegments('high'), [])
  
  // Cargar texturas de planetas
  const mercuryTexture = useTexture(getAssetPath('/textures/2k_mercury.jpg'))
  const venusAtmosphereTexture = useTexture(getAssetPath('/textures/4k_venus_atmosphere.jpg'))
  const marsTexture = useTexture(getAssetPath('/textures/2k_mars.jpg'))
  const moonTexture = useTexture(getAssetPath('/textures/2k_moon.jpg'))
  const jupiterTexture = useTexture(getAssetPath('/textures/2k_jupiter.jpg'))
  const saturnTexture = useTexture(getAssetPath('/textures/2k_saturn.jpg'))
  const saturnRingTexture = useTexture(getAssetPath('/textures/2k_saturn_ring_alpha.png'))
  const uranusTexture = useTexture(getAssetPath('/textures/2k_uranus.jpg'))
  const neptuneTexture = useTexture(getAssetPath('/textures/2k_neptune.jpg'))
  const plutoTexture = useTexture(getAssetPath('/textures/1k_pluto.png'))
  
  // 🌌 Sistema de Resonancia Cósmica
  const cosmicRef = useRef(getCosmicResonance())
  
  // 🎼 Sistema de Harmonices Mundi de Kepler
  const keplerRef = useRef(getKeplerHarmonices())
  
  // 🌊 Estado de ondas sonoras para visualización
  const [soundWaves, setSoundWaves] = useState<Array<{
    id: string
    position: THREE.Vector3
    frequency: number
    amplitude: number
    color: string
  }>>([])
  
  // 🎨 Estado de arte generativo orbital
  const [orbitalArtData, setOrbitalArtData] = useState<Array<{
    position: THREE.Vector3
    color: string
    orbitalPeriod: number
  }>>([])
  
  // Usar prop externa para controlar visualización
  const wavesEnabled = showWaves
  
  // Sistema astronómico actualizado
  const solarEngineRef = useRef<SolarEngine>(
    new SolarEngine(0, 0) // Coordenadas del sistema solar (centro)
  )
  
  // Tiempo de referencia para órbitas
  const startTimeRef = useRef(new Date())
  
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
  const plutoRef = useRef<THREE.Group>(null)
  const plutoMeshRef = useRef<THREE.Mesh>(null)
  
  // Vector reutilizable para posición lunar (evita clone() cada frame)
  const moonPosTemp = useRef(new THREE.Vector3())
  
  // Cache de índices de planetas para evitar .find() cada frame
  const planetIndices = useRef<Map<string, number> | null>(null)
  
  // 🌌 Inicializar sistema de resonancia cósmica
  useEffect(() => {
    const cosmic = cosmicRef.current
    const kepler = keplerRef.current
    
    // Verificar si ya fue descubierto
    if (cosmic.isDiscovered()) {
      cosmic.enable(scene)
      console.log('🌌 Sistema de Resonancia Cósmica habilitado')
    }
    
    // 🎼 Habilitar sistema de Kepler Harmonices
    kepler.enable().then(() => {
      console.log('🎼 Kepler Harmonices System habilitado')
      // Activar modo Kepler automáticamente
      kepler.activateKeplerMode(scene)
    })
    
    // Registrar planetas en el sistema de resonancia
    // Datos astronómicos reales
    cosmic.registerCelestialBody({
      id: 'mercury',
      name: 'Mercurio',
      position: new THREE.Vector3(0, 0, 0), // Se actualiza cada frame
      orbitalPeriod: 88,
      orbitalFrequency: 1 / 88,
      audioFrequency: 141.27, // Hz (C#)
      color: '#9c9c9c'
    })
    
    cosmic.registerCelestialBody({
      id: 'venus',
      name: 'Venus',
      position: new THREE.Vector3(0, 0, 0),
      orbitalPeriod: 225,
      orbitalFrequency: 1 / 225,
      audioFrequency: 221.23, // Hz (A)
      color: '#f5e6d3'
    })
    
    cosmic.registerCelestialBody({
      id: 'earth',
      name: 'Tierra',
      position: new THREE.Vector3(0, 0, 0),
      orbitalPeriod: 365.25,
      orbitalFrequency: 1 / 365.25,
      audioFrequency: 136.10, // Hz (C# - "Om cósmico")
      color: '#4A90E2'
    })
    
    cosmic.registerCelestialBody({
      id: 'mars',
      name: 'Marte',
      position: new THREE.Vector3(0, 0, 0),
      orbitalPeriod: 687,
      orbitalFrequency: 1 / 687,
      audioFrequency: 144.72, // Hz (D)
      color: '#E27B58'
    })
    
    cosmic.registerCelestialBody({
      id: 'jupiter',
      name: 'Júpiter',
      position: new THREE.Vector3(0, 0, 0),
      orbitalPeriod: 4333,
      orbitalFrequency: 1 / 4333,
      audioFrequency: 183.58, // Hz (F#)
      color: '#D4A574'
    })
    
    cosmic.registerCelestialBody({
      id: 'saturn',
      name: 'Saturno',
      position: new THREE.Vector3(0, 0, 0),
      orbitalPeriod: 10759,
      orbitalFrequency: 1 / 10759,
      audioFrequency: 147.85, // Hz (D)
      color: '#FAD5A5'
    })
    
    cosmic.registerCelestialBody({
      id: 'uranus',
      name: 'Urano',
      position: new THREE.Vector3(0, 0, 0),
      orbitalPeriod: 30687,
      orbitalFrequency: 1 / 30687,
      audioFrequency: 207.36, // Hz (G#)
      color: '#4FD0E7'
    })
    
    cosmic.registerCelestialBody({
      id: 'neptune',
      name: 'Neptuno',
      position: new THREE.Vector3(0, 0, 0),
      orbitalPeriod: 60190,
      orbitalFrequency: 1 / 60190,
      audioFrequency: 211.44, // Hz (G#)
      color: '#4166F5'
    })
    
    console.log('🪐 8 planetas registrados en el sistema de resonancia cósmica')
    
    return () => {
      cosmic.dispose()
      kepler.dispose()
    }
  }, [scene])
  
  // Actualización del sistema
  useFrame((state, delta) => {
    const solarEngine = solarEngineRef.current
    const solarState = solarEngine.update(delta)
    const cosmic = cosmicRef.current
    const kepler = keplerRef.current
    
    // Calcular tiempo en días desde el inicio
    const timeInDays = (solarState.simulatedTime.getTime() - startTimeRef.current.getTime()) / (1000 * 60 * 60 * 24)
    
    // Usar nuestro sistema planetario mejorado para TODOS los planetas
    const planets = calculateAllPlanets(timeInDays, 200) // escala 200 para visualización
    
    // Construir índice de planetas una sola vez
    if (!planetIndices.current) {
      planetIndices.current = new Map()
      planets.forEach((p, i) => planetIndices.current!.set(p.planet.name, i))
    }
    
    // Acceso directo por índice (O(1) en lugar de O(n) con find)
    const idx = planetIndices.current
    
    // Función helper para calcular fase orbital (0-1)
    const calculatePhase = (position: THREE.Vector3): number => {
      const angle = Math.atan2(position.z, position.x)
      return (angle + Math.PI) / (Math.PI * 2)
    }
    
    // Actualizar posiciones de planetas interiores
    const mercuryIdx = idx.get('Mercurio')
    if (mercuryIdx !== undefined && mercuryRef.current) {
      mercuryRef.current.position.copy(planets[mercuryIdx].position)
      // 🌌 Actualizar posición en sistema de resonancia
      cosmic.updateBodyPosition('mercury', mercuryRef.current.position)
      // 🎼 Actualizar sistema de Kepler con fase orbital
      const phase = calculatePhase(mercuryRef.current.position)
      kepler.updatePlanet('mercury', mercuryRef.current.position, phase)
    }
    if (mercuryMeshRef.current) {
      mercuryMeshRef.current.rotation.y += delta * 0.00017 // Rotación lenta
    }
    
    const venusIdx = idx.get('Venus')
    if (venusIdx !== undefined && venusRef.current) {
      venusRef.current.position.copy(planets[venusIdx].position)
      // 🌌 Actualizar posición en sistema de resonancia
      cosmic.updateBodyPosition('venus', venusRef.current.position)
      // 🎼 Actualizar sistema de Kepler
      const phase = calculatePhase(venusRef.current.position)
      kepler.updatePlanet('venus', venusRef.current.position, phase)
    }
    if (venusMeshRef.current) {
      venusMeshRef.current.rotation.y -= delta * 0.00004 // Retrógrada
    }
    
    const earthIdx = idx.get('Tierra')
    if (earthIdx !== undefined && earthGroupRef.current) {
      earthGroupRef.current.position.copy(planets[earthIdx].position)
      // 🌌 Actualizar posición en sistema de resonancia
      cosmic.updateBodyPosition('earth', earthGroupRef.current.position)
      // 🎼 Actualizar sistema de Kepler
      const phase = calculatePhase(earthGroupRef.current.position)
      kepler.updatePlanet('earth', earthGroupRef.current.position, phase)
    }
    
    const marsIdx = idx.get('Marte')
    if (marsIdx !== undefined && marsRef.current) {
      marsRef.current.position.copy(planets[marsIdx].position)
      // 🌌 Actualizar posición en sistema de resonancia
      cosmic.updateBodyPosition('mars', marsRef.current.position)
      // 🎼 Actualizar sistema de Kepler
      const phase = calculatePhase(marsRef.current.position)
      kepler.updatePlanet('mars', marsRef.current.position, phase)
    }
    if (marsMeshRef.current) {
      marsMeshRef.current.rotation.y += delta * 0.05
    }

    // Planetas exteriores - ahora también usan nuestro sistema
    const jupiterIdx = idx.get('Júpiter')
    if (jupiterIdx !== undefined && jupiterRef.current) {
      jupiterRef.current.position.copy(planets[jupiterIdx].position)
      // 🌌 Actualizar posición en sistema de resonancia
      cosmic.updateBodyPosition('jupiter', jupiterRef.current.position)
      // 🎼 Actualizar sistema de Kepler
      const phase = calculatePhase(jupiterRef.current.position)
      kepler.updatePlanet('jupiter', jupiterRef.current.position, phase)
    }
    if (jupiterMeshRef.current) jupiterMeshRef.current.rotation.y += delta * 0.045

    const saturnIdx = idx.get('Saturno')
    if (saturnIdx !== undefined && saturnRef.current) {
      saturnRef.current.position.copy(planets[saturnIdx].position)
      // 🌌 Actualizar posición en sistema de resonancia
      cosmic.updateBodyPosition('saturn', saturnRef.current.position)
      // 🎼 Actualizar sistema de Kepler
      const phase = calculatePhase(saturnRef.current.position)
      kepler.updatePlanet('saturn', saturnRef.current.position, phase)
    }
    if (saturnMeshRef.current) saturnMeshRef.current.rotation.y += delta * 0.043

    const uranusIdx = idx.get('Urano')
    if (uranusIdx !== undefined && uranusRef.current) {
      uranusRef.current.position.copy(planets[uranusIdx].position)
      // 🌌 Actualizar posición en sistema de resonancia
      cosmic.updateBodyPosition('uranus', uranusRef.current.position)
      // 🎼 Actualizar sistema de Kepler
      const phase = calculatePhase(uranusRef.current.position)
      kepler.updatePlanet('uranus', uranusRef.current.position, phase)
    }
    if (uranusMeshRef.current) uranusMeshRef.current.rotation.y += delta * 0.03

    const neptuneIdx = idx.get('Neptuno')
    if (neptuneIdx !== undefined && neptuneRef.current) {
      neptuneRef.current.position.copy(planets[neptuneIdx].position)
      // 🌌 Actualizar posición en sistema de resonancia
      cosmic.updateBodyPosition('neptune', neptuneRef.current.position)
      // 🎼 Actualizar sistema de Kepler
      const phase = calculatePhase(neptuneRef.current.position)
      kepler.updatePlanet('neptune', neptuneRef.current.position, phase)
    }
    if (neptuneMeshRef.current) neptuneMeshRef.current.rotation.y += delta * 0.032
    
    const plutoIdx = idx.get('Plutón')
    if (plutoIdx !== undefined && plutoRef.current) {
      plutoRef.current.position.copy(planets[plutoIdx].position)
    }
    if (plutoMeshRef.current) plutoMeshRef.current.rotation.y += delta * 0.02 // Muy lento
    
    // 🌌 Actualizar sistema de resonancia cósmica
    if (cosmic.isEnabled()) {
      cosmic.update(delta)
      
      // Obtener eventos activos (opcional: hacer algo con ellos)
      const events = cosmic.getActiveEvents()
      if (events.length > 0) {
        // Los eventos se muestran en el UI, pero aquí podrías añadir efectos
        // Por ejemplo: sonidos, partículas, etc.
      }
    }
    
    // 🎼 Analizar acorde cósmico cada 5 segundos
    if (kepler.isKeplerModeActive() && Math.floor(timeInDays * 10) % 50 === 0) {
      const chord = kepler.analyzeCosmicChord()
      if (chord && chord.consonance > 0.7) {
        console.log(`🎵 ${chord.description}: ${chord.harmonicRatio}`)
      }
    }
    
    // 🌊 Actualizar ondas sonoras para visualización
    if (kepler.isKeplerModeActive()) {
      const planetaryStates = kepler.getPlanetaryStates()
      setSoundWaves(planetaryStates.map(state => ({
        id: state.id,
        position: state.position.clone(),
        frequency: state.frequency,
        amplitude: 0.5,  // Amplitud constante
        color: KEPLER_PLANETARY_DATA.get(state.id)?.color || '#ffffff'
      })))
    }
    
    // 🎨 Actualizar datos para arte generativo orbital
    const artData: Array<{ position: THREE.Vector3; color: string; orbitalPeriod: number }> = []
    
    if (mercuryRef.current) artData.push({ 
      position: mercuryRef.current.position.clone(), 
      color: '#9c9c9c', 
      orbitalPeriod: 88 
    })
    if (venusRef.current) artData.push({ 
      position: venusRef.current.position.clone(), 
      color: '#f5e6d3', 
      orbitalPeriod: 225 
    })
    if (earthGroupRef.current) artData.push({ 
      position: earthGroupRef.current.position.clone(), 
      color: '#4A90E2', 
      orbitalPeriod: 365.25 
    })
    if (marsRef.current) artData.push({ 
      position: marsRef.current.position.clone(), 
      color: '#E27B58', 
      orbitalPeriod: 687 
    })
    if (jupiterRef.current) artData.push({ 
      position: jupiterRef.current.position.clone(), 
      color: '#D4A574', 
      orbitalPeriod: 4333 
    })
    if (saturnRef.current) artData.push({ 
      position: saturnRef.current.position.clone(), 
      color: '#FAD5A5', 
      orbitalPeriod: 10759 
    })
    if (uranusRef.current) artData.push({ 
      position: uranusRef.current.position.clone(), 
      color: '#4FD0E7', 
      orbitalPeriod: 30687 
    })
    if (neptuneRef.current) artData.push({ 
      position: neptuneRef.current.position.clone(), 
      color: '#4166F5', 
      orbitalPeriod: 60190 
    })
    
    setOrbitalArtData(artData)
    
    // Luna usando nuestro sistema lunar - POSICIÓN ABSOLUTA CON ESCALA CONSISTENTE
    const lunarState = calculateLunarPhase(timeInDays)
    if (moonRef.current && moonMeshRef.current && earthGroupRef.current) {
      // Posición de la Tierra (absoluta)
      const earthPos = earthGroupRef.current.position
      
      // Posición lunar ABSOLUTA - ya viene en la escala correcta (1 AU = 200 unidades)
      // Luna está a 0.00257 AU = 0.514 unidades de la Tierra
      // Multiplicamos por 10 para visualización (sino es invisible)
      const VISUAL_SCALE = 10
      // Usar vector temporal en lugar de clone()
      moonPosTemp.current.copy(lunarState.position).multiplyScalar(VISUAL_SCALE)
      moonRef.current.position.set(
        earthPos.x + moonPosTemp.current.x,
        earthPos.y + moonPosTemp.current.y,
        earthPos.z + moonPosTemp.current.z
      )
      
      // 🌙 TIDAL LOCKING (Bloqueo por marea)
      // La Luna siempre muestra la misma cara hacia la Tierra
      moonMeshRef.current.rotation.set(0, 0, 0)
      moonMeshRef.current.lookAt(earthPos) // Mirar hacia la TIERRA, no el Sol
      moonMeshRef.current.rotateY(0) // Sin rotación adicional
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
          <sphereGeometry args={[1.9, segments, segments]} />
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
          <sphereGeometry args={[0.95, segments, segments]} />
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
        
        {/* Órbita lunar visible - DENTRO del grupo de la Tierra para que se mueva con ella */}
        <RealisticLunarOrbit />
      </group>
      
      {/* Luna con posición ABSOLUTA - FUERA del grupo de la Tierra */}
      <group ref={moonRef}>
        <mesh ref={moonMeshRef}>
          <sphereGeometry args={[0.27, segments, segments]} />
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
      
      {/* Marte - Posición real con rotación axial */}
      <group ref={marsRef}>
        <mesh ref={marsMeshRef}>
          <sphereGeometry args={[0.5, segments, segments]} />
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
          <sphereGeometry args={[55, segments, segments]} />
          <meshStandardMaterial map={jupiterTexture} roughness={0.9} metalness={0.0} />
        </mesh>
        <CelestialTooltip name="Júpiter" symbol="♃" type="Gigante gaseoso"
          data={{ orbitalPeriod: "11.86 años", day: "9h 56m", diameter: "139.820 km",
            temperature: "-110°C", moons: "95 conocidas", atmosphere: "H₂, He, NH₃",
            funFact: "El planeta más grande — cabe 1.300 Tierras" }}
          position={[0, 60, 0]} color="#c8a87a" />
      </group>

      {/* ── Saturno + anillos ────────────────────────────────────────────── */}
      <group ref={saturnRef}>
        {/* Planeta */}
        <mesh ref={saturnMeshRef} castShadow>
          <sphereGeometry args={[38, segments, segments]} />
          <meshStandardMaterial map={saturnTexture} roughness={0.9} metalness={0.0} />
        </mesh>
        
        {/* 🪐 Anillos con mapeo UV correcto e inclinación real */}
        <SaturnRings 
          saturnRadius={38}
          ringTexture={saturnRingTexture}
          tilt={26.7}
        />
        
        <CelestialTooltip name="Saturno" symbol="♄" type="Gigante gaseoso"
          data={{ orbitalPeriod: "29.46 años", day: "10h 42m", diameter: "116.460 km",
            temperature: "-140°C", moons: "146 conocidas", atmosphere: "H₂, He",
            funFact: "Sus anillos tienen 270.000 km de diámetro pero solo 1 km de grosor" }}
          position={[0, 55, 0]} color="#e8d5a0" />
      </group>

      {/* ── Urano ────────────────────────────────────────────────────────── */}
      <group ref={uranusRef}>
        <mesh ref={uranusMeshRef}>
          <sphereGeometry args={[20, segments, segments]} />
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
          <sphereGeometry args={[19, segments, segments]} />
          <meshStandardMaterial map={neptuneTexture} roughness={0.85} metalness={0.0}
            emissive="#4b70dd" emissiveIntensity={0.06} />
        </mesh>
        <CelestialTooltip name="Neptuno" symbol="♆" type="Gigante de hielo"
          data={{ orbitalPeriod: "164.8 años", day: "16h 6m", diameter: "49.244 km",
            temperature: "-200°C", moons: "16 conocidas", atmosphere: "H₂, He, CH₄",
            funFact: "Vientos de hasta 2.100 km/h — los más rápidos del sistema solar" }}
          position={[0, 24, 0]} color="#4b70dd" />
      </group>

      {/* ── Plutón ──────────────────────────────────────────────────────── */}
      <group ref={plutoRef}>
        <mesh ref={plutoMeshRef}>
          <sphereGeometry args={[2.5, 32, 32]} />
          <meshStandardMaterial 
            map={plutoTexture} 
            roughness={0.95} 
            metalness={0.0}
            color="#8c7853"
          />
        </mesh>
        <CelestialTooltip 
          name="Plutón" 
          symbol="♇" 
          type="Planeta enano"
          data={{ 
            orbitalPeriod: "248 años", 
            day: "6.4 días terrestres", 
            diameter: "2.374 km",
            temperature: "-230°C", 
            moons: "5 conocidas (Caronte, Nix, Hidra...)", 
            atmosphere: "N₂, CH₄, CO",
            funFact: "Órbita muy elíptica e inclinada — a veces más cerca que Neptuno" 
          }}
          position={[0, 3.5, 0]} 
          color="#8c7853" 
        />
      </group>
      
      {/* 🌊 Ondas Sonoras Visuales - Representación gráfica de frecuencias */}
      {wavesEnabled && soundWaves.length > 0 && (
        <MultiPlanetWaves 
          planets={soundWaves}
          enabled={wavesEnabled}
        />
      )}
      
      {/* 🎨 Arte Generativo Cósmico - Mandalas gravitacionales y patrones orbitales */}
      {orbitalArtData.length > 0 && (
        <OrbitalGenerativeArt
          planets={orbitalArtData}
          enabled={true}
          intensity={0.3}
        />
      )}
    </group>
  )
}
