'use client'

import { useMemo } from 'react'
import * as THREE from 'three'
import { useGLTF } from '@react-three/drei'
import { getAssetPath } from '@/lib/paths'

interface GizaSceneProps {
  avatarPositionRef: React.MutableRefObject<THREE.Vector3>
  onSphinxClick?: () => void
}

/**
 * 🏜️ Escena de Giza - Gran Pirámide y Esfinge
 * 
 * Características astronómicas reales:
 * - Alineación cardinal casi perfecta (~0.05° de error)
 * - Cada cara mira exactamente: Norte, Sur, Este, Oeste
 * - Orientación basada en observaciones estelares de 2500 a.C.
 * 
 * Escala adaptada para juego:
 * - Gran Pirámide (Keops): 138m base × 88m altura (60% escala real)
 * - Esfinge: 73m largo × 20m alto (escala real)
 * 
 * Ambiente desértico realista:
 * - Arena color ocre/beige (#d9c8a3, #cdb68e, #bfa77f)
 * - Dunas suaves con ruido Perlin
 * - Niebla amarillenta atmosférica
 * - Piedras dispersas
 */
export default function GizaScene({ avatarPositionRef, onSphinxClick }: GizaSceneProps) {
  return (
    <group name="giza-complex">
        {/* 🌫️ Niebla desértica amarillenta */}
        <fog attach="fog" args={['#e8d5b7', 50, 400]} />
        
        {/* 🏜️ Terreno desértico con dunas suaves */}
        <DesertTerrain />
        
        {/* 🔺 Gran Pirámide de Keops (Khufu) */}
        <GreatPyramid 
          position={[0, 0, 0]}
          rotation={[0, Math.PI / 4, 0]} // Rotación 45° para alinear caras con cardinales
        />
        
        {/* 🦁 La Gran Esfinge - Al este de la pirámide, mirando al Este */}
        <Sphinx 
          position={[100, 5, 50]}
          rotation={[0, Math.PI / 2, 0]} // Mira hacia el Este (salida del sol)
          onClick={onSphinxClick}
        />
        
        {/* 🏛️ Templo del Valle de Kefrén - Debajo de la pirámide */}
        <ValleyTemple 
          position={[0, -5, 0]} // Justo debajo de la pirámide, 5m bajo la arena
        />
        
        {/* 🪨 Piedras dispersas del desierto */}
        <DesertRocks />
      </group>
  )
}

/**
 * 🔺 Gran Pirámide de Keops
 * La más grande y precisa
 */
function GreatPyramid({ position, rotation }: { position: [number, number, number], rotation: [number, number, number] }) {
  const baseSize = 138 // 60% de 230m real
  const height = 88 // 60% de 146m real
  
  // Geometría con ligera concavidad en las caras (detalle histórico real)
  const geometry = useMemo(() => {
    const geo = new THREE.ConeGeometry(baseSize / Math.sqrt(2), height, 4)
    geo.rotateY(Math.PI / 4) // Alinear caras con ejes
    
    // Aplicar concavidad sutil (las caras están ligeramente hundidas)
    const positions = geo.attributes.position
    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i)
      const y = positions.getY(i)
      const z = positions.getZ(i)
      
      // Solo afectar vértices de las caras (no base ni cima)
      if (y > 1 && y < height - 1) {
        const distFromCenter = Math.sqrt(x * x + z * z)
        const concavity = 0.3 // Sutil hundimiento
        const factor = 1 - (concavity * (y / height))
        positions.setXYZ(i, x * factor, y, z * factor)
      }
    }
    
    geo.computeVertexNormals()
    return geo
  }, [baseSize, height])
  
  return (
    <group position={position} rotation={rotation}>
      <mesh geometry={geometry} castShadow receiveShadow>
        <meshStandardMaterial
          color="#d4a574" // Caliza amarillenta (núcleo expuesto)
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>
    </group>
  )
}

/**
 * 🦁 La Gran Esfinge
 * Dimensiones reales: 73m largo × 20m alto × 19m ancho
 * Tallada en roca caliza natural
 * Mira hacia el Este (salida del sol en equinoccio)
 */
function Sphinx({ position, rotation, onClick }: { position: [number, number, number], rotation: [number, number, number], onClick?: () => void }) {
  const { scene } = useGLTF(getAssetPath('/sphinx_base.glb'))
  
  // Clonar la escena para evitar problemas de reutilización
  const clonedScene = useMemo(() => scene.clone(), [scene])
  
  // La Esfinge real mide 73m de largo × 20m de alto
  // Escala proporcional a la pirámide (60% escala real)
  // Escala del modelo: ajustar según el tamaño del .glb original
  const scale = 20 // Ajustar según necesidad
  
  return (
    <group position={position} rotation={rotation} onClick={onClick} onPointerOver={() => document.body.style.cursor = 'pointer'} onPointerOut={() => document.body.style.cursor = 'default'}>
      <primitive 
        object={clonedScene}
        scale={[scale, scale, scale]}
        castShadow
        receiveShadow
      />
    </group>
  )
}

// Precargar modelo
useGLTF.preload(getAssetPath('/sphinx_base.glb'))

/**
 * 🏜️ Terreno desértico con dunas suaves
 * Usa ruido Perlin para generar ondulaciones naturales
 */
function DesertTerrain() {
  const geometry = useMemo(() => {
    const size = 500 // Tamaño del terreno
    const segments = 100 // Resolución
    const geo = new THREE.PlaneGeometry(size, size, segments, segments)
    
    // Aplicar ruido Perlin para dunas suaves
    const positions = geo.attributes.position
    for (let i = 0; i < positions.count; i++) {
      const x = positions.getX(i)
      const z = positions.getY(i) // En PlaneGeometry, Y es Z en el mundo
      
      // Ruido Perlin simplificado (ondulaciones suaves)
      const noise1 = Math.sin(x * 0.002) * Math.cos(z * 0.002) * 2
      const noise2 = Math.sin(x * 0.005 + 10) * Math.cos(z * 0.005 + 10) * 1
      const noise3 = Math.sin(x * 0.01 + 20) * Math.cos(z * 0.01 + 20) * 0.5
      
      const height = noise1 + noise2 + noise3
      positions.setZ(i, height)
    }
    
    geo.computeVertexNormals()
    geo.rotateX(-Math.PI / 2) // Horizontal
    return geo
  }, [])
  
  return (
    <mesh geometry={geometry} receiveShadow position={[0, -0.5, 0]}>
      <meshStandardMaterial
        color="#d9c8a3" // Arena ocre/beige real de Giza
        roughness={0.95}
        metalness={0.05}
      />
    </mesh>
  )
}

/**
 * 🪨 Piedras dispersas del desierto
 * Pequeñas rocas distribuidas aleatoriamente
 */
function DesertRocks() {
  const rocks = useMemo(() => {
    const rockArray: JSX.Element[] = []
    const rockCount = 30 // Pocas piedras, realista
    
    for (let i = 0; i < rockCount; i++) {
      // Distribución aleatoria pero no cerca de la pirámide
      const angle = Math.random() * Math.PI * 2
      const distance = 80 + Math.random() * 150 // Entre 80m y 230m de distancia
      const x = Math.cos(angle) * distance
      const z = Math.sin(angle) * distance
      
      // Tamaño variable de rocas
      const size = 0.5 + Math.random() * 2
      const height = size * (0.5 + Math.random() * 0.5)
      
      rockArray.push(
        <mesh
          key={i}
          position={[x, height / 2, z]}
          rotation={[
            Math.random() * 0.3,
            Math.random() * Math.PI * 2,
            Math.random() * 0.3
          ]}
          castShadow
        >
          <boxGeometry args={[size, height, size * 0.8]} />
          <meshStandardMaterial
            color={new THREE.Color().setHSL(0.08, 0.15, 0.4 + Math.random() * 0.2)}
            roughness={0.9}
          />
        </mesh>
      )
    }
    
    return rockArray
  }, [])
  
  return <>{rocks}</>
}

/**
 * 🏛️ Templo del Valle de Kefrén
 * Estructura megalítica junto a la Esfinge
 * Construido proceduralmente con geometría básica
 * 
 * Dimensiones: 30m × 30m × 8m altura
 * Materiales: Granito oscuro (muros), Alabastro (piso)
 * Arquitectura: Planta cuadrada con sala de columnas
 */
function ValleyTemple({ position }: { position: [number, number, number] }) {
  return (
    <group position={position}>
      {/* 🏺 Piso de alabastro (blanco crema) */}
      <mesh position={[0, 0.25, 0]} receiveShadow>
        <boxGeometry args={[30, 0.5, 30]} />
        <meshStandardMaterial
          color="#f5f5dc" // Alabastro blanco crema
          roughness={0.3}
          metalness={0.1}
        />
      </mesh>
      
      {/* 🧱 Muros exteriores de granito oscuro */}
      {/* Muro Norte */}
      <mesh position={[0, 4, -15]} castShadow receiveShadow>
        <boxGeometry args={[30, 8, 1]} />
        <meshStandardMaterial
          color="#3b3b3b" // Granito oscuro
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>
      
      {/* Muro Sur */}
      <mesh position={[0, 4, 15]} castShadow receiveShadow>
        <boxGeometry args={[30, 8, 1]} />
        <meshStandardMaterial
          color="#3b3b3b"
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>
      
      {/* Muro Este */}
      <mesh position={[15, 4, 0]} castShadow receiveShadow>
        <boxGeometry args={[1, 8, 30]} />
        <meshStandardMaterial
          color="#3b3b3b"
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>
      
      {/* Muro Oeste (con entrada) */}
      <mesh position={[-15, 4, 0]} castShadow receiveShadow>
        <boxGeometry args={[1, 8, 30]} />
        <meshStandardMaterial
          color="#3b3b3b"
          roughness={0.8}
          metalness={0.2}
        />
      </mesh>
      
      {/* 🏛️ Columnas cuadradas de granito (8 columnas) */}
      {/* Fila frontal */}
      <Column position={[-8, 3, -8]} />
      <Column position={[0, 3, -8]} />
      <Column position={[8, 3, -8]} />
      
      {/* Fila central */}
      <Column position={[-8, 3, 0]} />
      <Column position={[8, 3, 0]} />
      
      {/* Fila posterior */}
      <Column position={[-8, 3, 8]} />
      <Column position={[0, 3, 8]} />
      <Column position={[8, 3, 8]} />
      
      {/* 🗿 Altar central */}
      <mesh position={[0, 0.75, 0]} castShadow receiveShadow>
        <boxGeometry args={[4, 1.5, 4]} />
        <meshStandardMaterial
          color="#6f6f6f" // Piedra gris
          roughness={0.9}
          metalness={0.1}
        />
      </mesh>
      
      {/* ☀️ Abertura en el techo para luz (simulada con luz puntual) */}
      <pointLight
        position={[0, 7, 0]}
        intensity={2}
        distance={20}
        color="#ffd700"
        castShadow
      />
      
      {/* 🌫️ Luz ambiental tenue interior */}
      <ambientLight intensity={0.2} />
    </group>
  )
}

/**
 * Columna cuadrada individual
 */
function Column({ position }: { position: [number, number, number] }) {
  return (
    <mesh position={position} castShadow receiveShadow>
      <boxGeometry args={[1.5, 6, 1.5]} />
      <meshStandardMaterial
        color="#3b3b3b" // Granito oscuro
        roughness={0.8}
        metalness={0.2}
      />
    </mesh>
  )
}
